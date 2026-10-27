"""HWS meter binding (API.md §7; protocol §9.2, §12.1, RC-9).

Thin main over the unchanged K4b binding functions: `k4b_meter_bind.bind` with the HWS store,
then the RC-9 overrides (memory cap 8 GiB, TEMP_ROOT = the HWS job's store); measure-only
(`--max-cpu inf --max-wall inf`), single thread, disk safe-STOP and classify_stop unchanged.
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import os
import sys
from pathlib import Path

import hws_worlds as hw  # noqa: F401  (sys.path for the meter modules)
import k4b_meter_bind
import meter
import op_guard
import winjob

MEMORY_CAP = int(hw.CONTRACT["resources"]["memory_cap_bytes"])


def bind(job_id, task_sha256, out, worker_session) -> None:
    k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)
    winjob.MEMORY_CAP = MEMORY_CAP
    k4b_meter_bind.TEMP_ROOT = str(out)


def effective_settings() -> dict:
    return {
        "memory_cap": winjob.MEMORY_CAP,
        "temp_root": k4b_meter_bind.TEMP_ROOT,
        "ledger": str(meter.LEDGER),
        "cap_s": meter.CAP_S,
        "output_cap": meter.OUTPUT_CAP,
        "thread_vars": list(meter.THREAD_VARS),
    }


def _pop(argv, flag):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[:i] + argv[i + 2 :], argv[i + 1]
    return argv, None


def main() -> int:
    """--job, --task-sha256, --session, --out (all required; choice 30), then the meter argv."""
    argv, opts = sys.argv[1:], {}
    for flag in ("--job", "--task-sha256", "--session", "--out"):
        argv, opts[flag] = _pop(argv, flag)
    missing = [f for f, v in opts.items() if v is None]
    if missing:
        print(f"hws_meter_bind: missing {missing}", file=sys.stderr)
        return 2
    out, job, session = Path(opts["--out"]), opts["--job"], opts["--session"]
    bind(job, opts["--task-sha256"], out, session)
    if meter.LOCK.exists() and session not in meter.LOCK.read_text("utf-8"):
        print("hws_meter_bind: RUN.lock names another session", file=sys.stderr)
        return 3
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    os.environ.update(k4b_meter_bind.child_env(job))
    sys.argv = [sys.argv[0]] + k4b_meter_bind.rewrite_argv(argv)
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
