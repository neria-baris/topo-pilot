"""CPU-metering supervisor for job 0014 (standard library only; Windows Job Objects).

Runs ONE command inside a fresh Job Object, so the kernel accounts the CPU of the command and
of every descendant (venv launcher, interpreter, native threads), including exited processes.
The run ends only when the job has no active process. The supervisor's own CPU (GetProcessTimes
on itself, from interpreter start) is added; a fixed allowance covers the unmeasured tail after
the final self-measurement and is reported separately from measured CPU.

Usage: python -I meter.py --label L [--mode run|audit] [--lock-owner ID] -- CMD ARGS...
Run it with the BASE interpreter (no venv launcher) so no launcher CPU escapes accounting.
A STARTED ledger entry is written before launch and finalised in place. If finalisation fails,
an emergency record is appended to cpu_ledger.emergency.jsonl and METER_ACTIVE.lock is kept as
an unresolved-active marker; later runs refuse until it is resolved. Charges are never dropped.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I omits the script directory

import controls  # noqa: E402
from winjob import (  # noqa: E402, F401
    CREATE_SUSPENDED,
    JOB_ACCOUNTING,
    JOB_EXTENDED,
    BasicAccounting,
    ExtendedLimit,
    MeterError,
    _check,
    _query,
    job_cpu,
    job_peak_working_set,
    k32,
    make_job,
    ntdll,
    own_cpu_s,
    process_cpu_s,
    terminate_and_drain,
    wt,
)

OUT = Path(r"X:\Downloads\projects\topo-pilot\x4-oracle-profile-store-0014")
LEDGER = OUT / "cpu_ledger.json"
EMERGENCY = OUT / "cpu_ledger.emergency.jsonl"
LOCK = OUT / "RUN.lock"
ACTIVE = OUT / "METER_ACTIVE.lock"
LOG_DIR = OUT / "logs"
WORKER_SESSION = "88eb0214-46ad-4376-b93b-3da3034423d6"
CAP_S, STOP_NEW_S = 3600.0, 3480.0
TAIL_ALLOWANCE_S = 0.1
OUTPUT_CAP = 128 * 1024**2
THREAD_VARS = (
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OMP_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)
FAULTS = ("assign", "after_launch", "finalise")


def output_bytes() -> int:
    return sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())


def atomic_json(path: Path, obj) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    os.replace(tmp, path)


def limit_reason(ledger, child, args, active_wall, polls, mailboxes) -> tuple:
    """(kill reason or None, control state). HOLD never kills; STOP/INVALID always do."""
    state, why = controls.classify_all(mailboxes, OUT, args.mode)
    if state in (controls.STOP, controls.INVALID):
        return f"{state}: {why}", state
    if child >= args.max_cpu:
        return f"per-run CPU limit {args.max_cpu}", state
    if ledger["cumulative_cpu_s"] + child + own_cpu_s() + TAIL_ALLOWANCE_S >= STOP_NEW_S:
        return f"cumulative CPU reached {STOP_NEW_S}", state
    if active_wall >= args.max_wall:
        return f"non-hold wall limit {args.max_wall}", state
    if polls % 8 == 0 and output_bytes() > OUTPUT_CAP:
        return f"output cap {OUTPUT_CAP} bytes", state
    return None, state


def _launch(cmd, out, err, job, state, fault):
    env = dict(os.environ, **{name: "1" for name in THREAD_VARS}, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.Popen(cmd, stdout=out, stderr=err, env=env, creationflags=CREATE_SUSPENDED)
    state["proc"] = proc
    handle = wt.HANDLE(int(proc._handle))
    if fault == "assign" or not k32.AssignProcessToJobObject(job, handle):
        # Never left outside accounting: terminate the suspended process itself, wait, charge it.
        k32.TerminateProcess(handle, 75)
        k32.WaitForSingleObject(handle, 30000)
        state["outside_job_cpu_s"] = process_cpu_s(handle)
        raise MeterError(f"AssignProcessToJobObject failed (fault={fault})")
    state["assigned"] = True
    if ntdll.NtResumeProcess(handle) != 0:
        raise MeterError("NtResumeProcess failed")
    return proc


def supervise(cmd, args, ledger, state, mailboxes) -> dict:
    """Run cmd in the job; return only after the job has NO active process."""
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out_path = LOG_DIR / f"{stamp}_{args.label}.stdout.txt"
    err_path = LOG_DIR / f"{stamp}_{args.label}.stderr.txt"
    job = state["job"]
    holds, killed, peaks, polls, active_wall = [], None, {}, 0, 0.0
    with out_path.open("xb") as out, err_path.open("xb") as err:
        proc = _launch(cmd, out, err, job, state, args.inject_fault)
        if args.inject_fault == "after_launch":
            time.sleep(0.5)
            raise MeterError("injected fault after launch")
        start = last = time.monotonic()
        while True:
            time.sleep(0.25)
            polls += 1
            now = time.monotonic()
            job_peak_working_set(job, peaks)
            user, kernel, active = job_cpu(job)
            if proc.poll() is not None and active == 0:
                break
            killed, ctl = limit_reason(ledger, user + kernel, args, active_wall, polls, mailboxes)
            if ctl == controls.HOLD:
                if not holds or holds[-1]["end_s"] is not None:
                    holds.append({"start_s": round(now - start, 3), "end_s": None})
            else:
                active_wall += now - last
                if holds and holds[-1]["end_s"] is None:
                    holds[-1]["end_s"] = round(now - start, 3)
            last = now
            if killed:
                state["drained"] = terminate_and_drain(job)
                proc.wait()
                break
        wall = time.monotonic() - start
    user, kernel, _ = job_cpu(job)
    ext, acct = ExtendedLimit(), BasicAccounting()
    _query(job, JOB_EXTENDED, ext)
    _query(job, JOB_ACCOUNTING, acct)
    return {
        "status": "KILLED" if killed else "FINISHED",
        "exit_code": proc.returncode,
        "killed_reason": killed,
        "drained": state.get("drained", True),
        "wall_s": round(wall, 3),
        "pid": proc.pid,
        "child_user_s": user,
        "child_kernel_s": kernel,
        "child_cpu_s": user + kernel,
        "job_total_processes": int(acct.TotalProcesses),
        "holds_observed": holds,
        "peak_job_commit_bytes": int(ext.PeakJobMemoryUsed),
        "peak_process_commit_bytes": int(ext.PeakProcessMemoryUsed),
        "peak_working_set_bytes_polled": max(peaks.values(), default=None),
        "stdout": out_path.name,
        "stderr": err_path.name,
    }


def error_entry(base, exc, state) -> dict:
    child = state.get("outside_job_cpu_s", 0.0)
    drained = True
    if state.get("assigned"):
        drained = terminate_and_drain(state["job"])
        user, kernel, _ = job_cpu(state["job"])
        child = user + kernel
    if state.get("proc") is not None:
        state["proc"].wait(timeout=30)
    return dict(
        base,
        status="SUPERVISOR_ERROR",
        supervisor_error=repr(exc),
        child_cpu_s=child,
        killed_reason="supervisor error",
        drained=drained,
        pid=getattr(state.get("proc"), "pid", None),
    )


def finalise(ledger: dict, index: int, entry: dict, fault: str | None) -> None:
    entry["supervisor_cpu_s"] = own_cpu_s()
    entry["tail_allowance_s"] = TAIL_ALLOWANCE_S
    entry["measured_cpu_s"] = entry["child_cpu_s"] + entry["supervisor_cpu_s"]
    entry["charged_cpu_s"] = entry["measured_cpu_s"] + TAIL_ALLOWANCE_S
    entry["utc_end"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        if fault == "finalise":
            raise MeterError("injected fault during finalisation")
        entry["output_bytes_after"] = output_bytes()
        entry["output_cap_exceeded"] = entry["output_bytes_after"] > OUTPUT_CAP
        ledger["entries"][index] = entry
        ledger["cumulative_measured_cpu_s"] += entry["measured_cpu_s"]
        ledger["cumulative_tail_allowance_s"] += TAIL_ALLOWANCE_S
        ledger["cumulative_cpu_s"] = (
            ledger["cumulative_measured_cpu_s"] + ledger["cumulative_tail_allowance_s"]
        )
        atomic_json(LEDGER, ledger)
    except Exception as exc:
        record = dict(entry, emergency_reason=repr(exc), ledger_index=index)
        with EMERGENCY.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        ACTIVE.write_text(
            json.dumps(
                {
                    "unresolved": True,
                    "label": entry["label"],
                    "ledger_index": index,
                    "reason": repr(exc),
                    "measured_cpu_s": entry["measured_cpu_s"],
                }
            ),
            encoding="utf-8",
        )
        raise


def load_ledger() -> dict:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger.get("schema") != "x4-oracle-profile-ledger-v1":
        raise MeterError("ledger schema")
    return ledger


def lock_refusal(args) -> str | None:
    """Reason to refuse (charged as a REFUSED entry), or None."""
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return f"RUN.lock unreadable: {type(exc).__name__}"
    owner = args.lock_owner or WORKER_SESSION
    if lock.get("session") != owner or (args.mode == "run" and owner != WORKER_SESSION):
        return f"RUN.lock not owned by {owner} for mode {args.mode}"
    if EMERGENCY.exists():
        records = sum(1 for line in EMERGENCY.read_text(encoding="utf-8").splitlines() if line.strip())
        if records > int(lock.get("emergency_records_reconciled", 0)):
            return "unreconciled emergency charge records exist"
    return None


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--label", required=True)
    parser.add_argument("--mode", choices=("run", "audit"), default="run")
    parser.add_argument("--lock-owner", default=None)
    parser.add_argument("--max-cpu", type=float, default=600.0)
    parser.add_argument("--max-wall", type=float, default=3600.0)
    parser.add_argument(
        "--synthetic-mailbox",
        default=None,
        help="extra synthetic control directory (checks only; real controls still win)",
    )
    parser.add_argument(
        "--inject-fault",
        choices=FAULTS,
        default=None,
        help="TEST ONLY: simulate a supervisor failure path (recorded in the ledger)",
    )
    parser.add_argument("cmd", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    args.cmd = args.cmd[1:] if args.cmd[:1] == ["--"] else args.cmd
    if not args.cmd:
        parser.error("missing command")
    return args


def main() -> int:
    args = parse()
    mailboxes = [controls.MAILBOX] + (
        [Path(args.synthetic_mailbox)] if args.synthetic_mailbox else []
    )
    try:
        with ACTIVE.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps({"pid": os.getpid(), "label": args.label}))
    except FileExistsError:
        print("REFUSED: METER_ACTIVE.lock exists (active or unresolved run)", file=sys.stderr)
        return 3
    resolved = False
    try:
        ledger = load_ledger()
        LOG_DIR.mkdir(exist_ok=True)
        base = {
            "label": args.label,
            "argv": args.cmd,
            "mode": args.mode,
            "status": "STARTED",
            "mailboxes": [str(m) for m in mailboxes],
            "inject_fault": args.inject_fault,
            "child_cpu_s": None,
            "meter_pid": os.getpid(),
            "lock_owner": args.lock_owner,
            "utc_started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        ledger["entries"].append(dict(base))
        index = len(ledger["entries"]) - 1
        atomic_json(LEDGER, ledger)
        ctl, why = controls.classify_all(mailboxes, OUT, args.mode)
        refusal = lock_refusal(args) or (None if ctl == controls.CONTINUE else f"{ctl}: {why}")
        if ledger["cumulative_cpu_s"] >= STOP_NEW_S:
            refusal = refusal or f"cumulative {ledger['cumulative_cpu_s']} >= {STOP_NEW_S}"
        state: dict = {"job": None}
        try:
            if refusal:
                entry = dict(base, status="REFUSED", refused=refusal, child_cpu_s=0.0)
            else:
                state["job"] = make_job()
                try:
                    entry = dict(base, **supervise(args.cmd, args, ledger, state, mailboxes))
                except Exception as exc:
                    entry = error_entry(base, exc, state)
        finally:
            if state["job"]:
                k32.CloseHandle(state["job"])
        finalise(ledger, index, entry, args.inject_fault)
        resolved = True
        print(
            json.dumps(
                {
                    k: entry.get(k)
                    for k in (
                        "label",
                        "status",
                        "exit_code",
                        "killed_reason",
                        "refused",
                        "measured_cpu_s",
                        "wall_s",
                    )
                }
                | {"cumulative_cpu_s": ledger["cumulative_cpu_s"]}
            )
        )
        ok = entry["status"] == "FINISHED" and entry.get("exit_code") == 0
        return 0 if ok and not entry["output_cap_exceeded"] else 2
    finally:
        if resolved:
            ACTIVE.unlink()


if __name__ == "__main__":
    sys.exit(main())
