"""HWSB meter binding (API.md §10; protocol §6.4 rule 1, §9.1, RC-5).

Thin main over the unchanged K4b binding (the hws_meter_bind pattern): memory cap 8 GiB,
measure-only (--max-cpu inf --max-wall inf), single-thread child env. J-B1 and DRY jobs
(kind "test") put the meter out, ledger and TEMP_ROOT under a test_-prefixed folder of
X:/Downloads/topo-scratch; KB, TRAIN and EVAL (kind "store") use hwsb-store and hwsb-store/tmp.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import os
import sys
from pathlib import Path

import k4b_meter_bind
import meter
import op_guard
import winjob

MEMORY_CAP = int(hc.CONTRACT["resources"]["memory_cap_bytes"])


def job_paths(job, kind) -> dict:
    if kind == "test":
        out = hc.SCRATCH / f"test_hwsb-{job}"
        return {"kind": kind, "out": out, "temp_root": out, "basetemp": out / "pytest"}
    if kind == "store":
        return {"kind": kind, "out": hc.STORE, "temp_root": hc.STORE / "tmp", "basetemp": None}
    raise ValueError(f"unknown job kind {kind!r}")


def bind(job_id, task_sha256, out, worker_session, temp_root=None) -> None:
    k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)
    winjob.MEMORY_CAP = MEMORY_CAP
    k4b_meter_bind.TEMP_ROOT = str(temp_root if temp_root is not None else out)


def _outside(p, root) -> bool:
    if p is None:
        return True
    try:
        Path(p).resolve().relative_to(Path(root).resolve())
    except ValueError:
        return True
    return False


def _under(p, base) -> bool:
    return p is not None and not _outside(p, base)


def placement_ok(paths, root=hc.ROOT) -> dict:
    out, temp, base = paths.get("out"), paths.get("temp_root"), paths.get("basetemp")
    if paths.get("kind") == "store":
        checks = {
            "out_is_store": Path(out).resolve() == hc.STORE.resolve(),
            "temp_under_store_tmp": _under(temp, hc.STORE / "tmp"),
        }
        return {"ok": all(checks.values()), "checks": checks}
    checks = {
        "out_outside_root": _outside(out, root),
        "temp_outside_root": _outside(temp, root),
        "basetemp_outside_root": _outside(base, root),
        "test_prefixed": out is not None
        and Path(out).resolve().parent == hc.SCRATCH.resolve()
        and Path(out).name.startswith("test_"),
    }
    return {"ok": all(checks.values()), "checks": checks}


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
    """--job, --task-sha256, --session, --kind (all required), then the meter argv."""
    argv, opts = sys.argv[1:], {}
    for flag in ("--job", "--task-sha256", "--session", "--kind"):
        argv, opts[flag] = _pop(argv, flag)
    missing = [f for f, v in opts.items() if v is None]
    if missing:
        print(f"hwsb_meter_bind: missing {missing}", file=sys.stderr)
        return 2
    job, session = opts["--job"], opts["--session"]
    try:
        paths = job_paths(job, opts["--kind"])
    except ValueError as exc:
        print(f"hwsb_meter_bind: {exc}", file=sys.stderr)
        return 2
    out = Path(paths["out"])
    out.mkdir(parents=True, exist_ok=True)
    bind(job, opts["--task-sha256"], out, session, paths["temp_root"])
    if meter.LOCK.exists() and session not in meter.LOCK.read_text("utf-8"):
        print("hwsb_meter_bind: RUN.lock names another session", file=sys.stderr)
        return 3
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    os.environ.update(k4b_meter_bind.child_env(job))
    sys.argv = [sys.argv[0]] + k4b_meter_bind.rewrite_argv(argv)
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
