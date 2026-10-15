"""C1' binding of the unchanged job-0014 meter (API.md §14; protocol §18 field 2; standard
library only; base interpreter, -I). Rebinds module-level names of meter/controls/winjob: job
and task digest, store paths, CAP_S = STOP_NEW_S = inf (measure-only), OUTPUT_CAP 16 GiB,
MEMORY_CAP 12 GiB, WORKER_SESSION (the same identity must own RUN.lock); forces --max-cpu inf
--max-wall inf; installs a limiter with the owner disk safe-STOP and the op-marker deadline.

K4 meter_bind is NOT imported (its import reads the K4 CONTRACT, changes sys.path, imports the
K4 release module and captures _LEGACY_LIMIT). disk_reason and the limiter below are extracted
from tools/x4_circle_history/meter_bind.py (disk_reason, make_stage_limiter) with the stage
ceiling removed; provenance recorded here, regression-tested by the S1 tests.

Usage: python -I c1_meter_bind.py --label <stage>__<label> [meter options] -- CMD...
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [p for p in (str(HERE), str(HERE.parent / "x4_oracle_profile"),
                            str(HERE.parent / "x4_circle_history")) if p not in sys.path]

import controls  # noqa: E402  (job-0014, unchanged)
import meter  # noqa: E402  (job-0014, unchanged)
import op_guard  # noqa: E402  (K4, unchanged)
import winjob  # noqa: E402  (job-0014, unchanged)

CONTRACT = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
RES = CONTRACT["resources"]
DISK_MIN_FREE = {k: int(v) for k, v in RES["disk_min_free"].items()}
_LEGACY = meter.limit_reason


def bind(job_id, task_sha256, out, worker_session) -> None:
    out = Path(out)
    controls.JOB_ID = str(job_id)
    controls.TASK_SHA256 = str(task_sha256).upper()
    meter.OUT, meter.LEDGER = out, out / "cpu_ledger.json"
    meter.EMERGENCY, meter.LOCK = out / "cpu_ledger.emergency.jsonl", out / "RUN.lock"
    meter.ACTIVE, meter.LOG_DIR = out / "METER_ACTIVE.lock", out / "logs"
    meter.CAP_S = meter.STOP_NEW_S = float("inf")
    meter.OUTPUT_CAP = int(RES["output_bytes"])
    winjob.MEMORY_CAP = int(RES["memory_bytes"])
    meter.WORKER_SESSION = str(worker_session)


def disk_reason(usage=shutil.disk_usage):
    for drive, minimum in DISK_MIN_FREE.items():
        try:
            free = usage(drive).free
        except OSError as exc:
            return f"disk safe-STOP: {drive} free space unreadable ({type(exc).__name__})"
        if free < minimum:
            return f"disk safe-STOP: {drive} free {free} < {minimum} bytes"
    return None


def make_limiter(op_marker=None, disk=disk_reason, legacy=None, clock=time.time):
    legacy = legacy or _LEGACY

    def limit_reason(ledger, child, args, active_wall, polls, mailboxes):
        if op_marker is not None:
            overdue = op_guard.overdue(op_marker, clock())
            if overdue:
                return overdue, "CONTINUE"
        if disk is not None and polls % 8 == 0:
            reason = disk()
            if reason:
                return reason, "CONTINUE"
        return legacy(ledger, child, args, active_wall, polls, mailboxes)

    return limit_reason


def _drop(args, flag):
    while flag in args:
        i = args.index(flag)
        del args[i:i + 2]


def rewrite_argv(argv) -> list:
    args = list(argv)
    sep = args.index("--") if "--" in args else len(args)
    head, tail = args[:sep], args[sep:]
    _drop(head, "--max-cpu")
    _drop(head, "--max-wall")
    return head + ["--max-cpu", "inf", "--max-wall", "inf"] + tail


def _pop_release(argv) -> tuple:
    args = list(argv)
    if "--release" not in args[: args.index("--") if "--" in args else len(args)]:
        return args, None
    i = args.index("--release")
    path = args[i + 1]
    del args[i:i + 2]
    return args, path


def main() -> int:
    out = Path(RES["output_root"])
    argv, release_path = _pop_release(sys.argv[1:])
    job, task = CONTRACT["job_id"], CONTRACT["task_sha256"]
    if release_path is not None:
        import c1_release  # standard library only; reads git files, spawns no process

        rel = c1_release.verify(Path(release_path))
        job, task = rel["job_id"], rel["task_sha256"]
    bind(job, task, out, RES["worker_session"])
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    reason = disk_reason()
    args = rewrite_argv(argv)
    if reason:
        i = args.index("--label")
        args[i + 1] += "__REFUSED_disk_safe_stop"
        sep = args.index("--")
        args = args[:sep] + ["--", sys.executable, "-I", "-c", "raise SystemExit(4)"]
    meter.limit_reason = make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    sys.argv = [sys.argv[0]] + args
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
