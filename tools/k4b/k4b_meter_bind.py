"""K4b meter binding (API.md §12.2; protocol §11.7, RC11).

Rebinds the unchanged job-0014 meter, controls and winjob modules to the K4b store and the
verified release; wraps the supervisor hook. Disk safe-STOP and the op-marker limiter are
re-implemented here (provenance: c1_meter_bind.disk_reason/make_limiter, not imported); the
legacy hook is called exactly once per poll and its control state is always returned.
"""

from __future__ import annotations  # noqa: I001  (k4b_config sets sys.path first)

import os
import shutil
import sys
import time
from pathlib import Path

import k4b_config
import controls
import meter
import op_guard
import winjob

LEGACY_LIMIT = meter.limit_reason
INF = float("inf")
DISK_MIN_FREE = {"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}
TEMP_ROOT = "X:/Downloads/projects/topo-pilot/k4b-store"
RESOURCE_MARKS = ("native operation wall", "disk safe-STOP", "memory", "output cap")


def bind(job_id, task_sha256, out, worker_session) -> None:
    out = Path(out)
    controls.JOB_ID = str(job_id)
    controls.TASK_SHA256 = str(task_sha256).upper()
    meter.OUT = out
    meter.LEDGER = out / "cpu_ledger.json"
    meter.EMERGENCY = out / "cpu_ledger.emergency.jsonl"
    meter.LOCK = out / "RUN.lock"
    meter.ACTIVE = out / "METER_ACTIVE.lock"
    meter.LOG_DIR = out / "logs"
    meter.CAP_S = meter.STOP_NEW_S = INF
    meter.OUTPUT_CAP = 4 * 1024**3
    winjob.MEMORY_CAP = 12 * 1024**3
    meter.WORKER_SESSION = worker_session


def disk_reason(usage=shutil.disk_usage, minima=DISK_MIN_FREE):
    for drive, minimum in minima.items():
        try:
            free = usage(drive).free
        except Exception as exc:  # noqa: BLE001  unreadable free space is a safe-STOP
            return f"disk safe-STOP: {drive} free space unreadable ({type(exc).__name__}: {exc})"
        if free < minimum:
            return f"disk safe-STOP: {drive} free {free} < {minimum} bytes"
    return None


def make_limiter(op_marker, disk=disk_reason, legacy=None, clock=time.time):
    legacy = LEGACY_LIMIT if legacy is None else legacy

    def limit_reason(ledger, child, args, active_wall, polls, mailboxes):
        reason, state = legacy(ledger, child, args, active_wall, polls, mailboxes)
        if reason:
            return reason, state
        if op_marker is not None:
            over = op_guard.overdue(op_marker, clock())
            if over:
                return over, state
        if polls % 8 == 0:
            d = disk()
            if d:
                return d, state
        return None, state

    return limit_reason


def rewrite_argv(argv) -> list:
    out, skip = [], False
    for a in argv:
        if skip:
            skip = False
            continue
        if a in ("--max-cpu", "--max-wall"):
            skip = True
            continue
        if a.startswith(("--max-cpu=", "--max-wall=")):
            continue
        out.append(a)
    if "--" in out:
        i = out.index("--")
        return out[:i] + ["--max-cpu", "inf", "--max-wall", "inf"] + out[i:]
    return out + ["--max-cpu", "inf", "--max-wall", "inf"]


def child_env(job, base=None) -> dict:
    env = dict(os.environ if base is None else base)
    tmp = f"{TEMP_ROOT}/tmp-{job}"
    env.update(TEMP=tmp, TMP=tmp, TMPDIR=tmp)
    for var in meter.THREAD_VARS:
        env[var] = "1"
    return env


def classify_stop(reason, state) -> str:
    if state in (controls.STOP, controls.INVALID) and not any(
            m in str(reason) for m in RESOURCE_MARKS):
        return state
    if reason and any(m in str(reason) for m in RESOURCE_MARKS):
        return "INCONCLUSIVE/RESOURCE"
    return state


def _pop(argv, flag):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[:i] + argv[i + 2:], argv[i + 1]
    return argv, None


def main() -> int:
    """--release (required), --kind (A|B), --task-sha256, --session; then the meter argv."""
    import k4b_release

    argv = sys.argv[1:]
    argv, release = _pop(argv, "--release")
    argv, kind = _pop(argv, "--kind")
    argv, task = _pop(argv, "--task-sha256")
    argv, session = _pop(argv, "--session")
    if release is None:
        print("k4b_meter_bind: --release is required", file=sys.stderr)
        return 2
    rel = k4b_release.verify_release(release, kind or "A", task or "", session or "")
    out = Path(k4b_config.STORE)
    bind(rel["job_id"], rel["task_sha256"], out, rel["worker_session"])
    if meter.LOCK.exists() and rel["worker_session"] not in meter.LOCK.read_text("utf-8"):
        print("k4b_meter_bind: RUN.lock identity differs from the release", file=sys.stderr)
        return 3
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    meter.limit_reason = make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    os.environ.update(child_env(rel["job_id"]))
    sys.argv = [sys.argv[0]] + rewrite_argv(argv)
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
