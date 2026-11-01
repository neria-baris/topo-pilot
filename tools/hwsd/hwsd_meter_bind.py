"""HWSD meter binding (API.md §13; protocol §11.3; DRD12).

Thin main over the unchanged K4b binding (the hwsc_meter_bind pattern): memory cap per stage,
measure-only (--max-cpu inf --max-wall inf), single-thread child env. J-D1 and DRY (kind "test")
put out and TEMP_ROOT under X:/Downloads/topo-scratch/test_hwsd-<job>; KD, SAMPLE, SCORE and SUMMARY
(kind "store") use hwsd-store and hwsd-store/tmp.
"""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import os
import sys
from pathlib import Path

import k4b_meter_bind
import meter
import op_guard
import winjob

INF = float("inf")


def job_paths(job, kind) -> dict:
    if kind == "test":
        out = dc.SCRATCH / f"test_hwsd-{job}"
        return {"kind": kind, "out": out, "temp_root": out, "basetemp": out / "pytest"}
    if kind == "store":
        return {"kind": kind, "out": dc.STORE, "temp_root": dc.STORE / "tmp", "basetemp": None}
    raise ValueError(f"unknown job kind {kind!r}")


def memory_cap(stage) -> int:
    caps = dc.CONTRACT["resources"]["memory_cap_bytes"]
    if stage not in caps:
        raise ValueError(f"unknown stage {stage!r}")
    return int(caps[stage])


def bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None:
    cap = memory_cap(stage)
    k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)
    winjob.MEMORY_CAP = cap
    k4b_meter_bind.TEMP_ROOT = str(temp_root if temp_root is not None else out)
    meter.CAP_S = meter.STOP_NEW_S = INF
    meter.OUTPUT_CAP = int(dc.CONTRACT["resources"]["output_cap_bytes"])  # whole out folder


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


def placement_ok(paths, root=dc.ROOT) -> dict:
    out, temp, base = paths.get("out"), paths.get("temp_root"), paths.get("basetemp")
    if paths.get("kind") == "store":
        checks = {"out_is_store": out is not None and Path(out).resolve() == dc.STORE.resolve(),
                  "temp_under_store_tmp": _under(temp, dc.STORE / "tmp")}
        return {"ok": all(checks.values()), "checks": checks}
    checks = {"out_outside_root": _outside(out, root),
              "temp_outside_root": _outside(temp, root),
              "basetemp_outside_root": _outside(base, root),
              "test_prefixed": out is not None
              and Path(out).resolve().parent == dc.SCRATCH.resolve()
              and Path(out).name.startswith("test_hwsd-")}
    return {"ok": all(checks.values()), "checks": checks}


def child_env_d(job) -> dict:
    """k4b_meter_bind.child_env(job) with its TEMP folder created (the D-0177-1 fix)."""
    env = k4b_meter_bind.child_env(job)
    Path(env["TEMP"]).mkdir(parents=True, exist_ok=True)
    return env


def effective_settings() -> dict:
    return {"memory_cap": winjob.MEMORY_CAP, "temp_root": k4b_meter_bind.TEMP_ROOT,
            "ledger": str(meter.LEDGER), "cap_s": meter.CAP_S, "output_cap": meter.OUTPUT_CAP,
            "thread_vars": list(meter.THREAD_VARS)}


def _pop(argv, flag):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[:i] + argv[i + 2:], argv[i + 1]
    return argv, None


def main() -> int:
    """--job, --task-sha256, --session, --kind, --stage (all required), then the meter argv."""
    argv, opts = sys.argv[1:], {}
    for flag in ("--job", "--task-sha256", "--session", "--kind", "--stage"):
        argv, opts[flag] = _pop(argv, flag)
    missing = [f for f, v in opts.items() if v is None]
    if missing:
        print(f"hwsd_meter_bind: missing {missing}", file=sys.stderr)
        return 2
    job, session = opts["--job"], opts["--session"]
    try:
        paths = job_paths(job, opts["--kind"])
        memory_cap(opts["--stage"])
    except ValueError as exc:
        print(f"hwsd_meter_bind: {exc}", file=sys.stderr)
        return 2
    out = Path(paths["out"])
    out.mkdir(parents=True, exist_ok=True)
    bind(job, opts["--task-sha256"], out, session, opts["--stage"], paths["temp_root"])
    if meter.LOCK.exists() and session not in meter.LOCK.read_text("utf-8"):
        print("hwsd_meter_bind: RUN.lock names another session", file=sys.stderr)
        return 3
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    os.environ.update(child_env_d(job))
    sys.argv = [sys.argv[0]] + k4b_meter_bind.rewrite_argv(argv)
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
