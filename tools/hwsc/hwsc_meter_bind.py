"""HWSC meter binding (API.md §9; protocol §8.3, RC-13; DRC13).

Thin main over the unchanged K4b binding (the hwsb_meter_bind pattern): memory cap per stage
(8 GiB J-C1/TRAIN, 12 GiB DRY/KC/E1/REG2/E2), measure-only (--max-cpu inf --max-wall inf),
single-thread child env. J-C1 and DRY (kind "test") put out, ledger and TEMP_ROOT under a
test_-prefixed folder of X:/Downloads/topo-scratch; KC, TRAIN, E1, REG2, E2 (kind "store") use
hwsc-store and hwsc-store/tmp.
"""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import os
import sys
from pathlib import Path

import k4b_meter_bind
import meter
import op_guard
import winjob

CAPS = cc.CONTRACT["resources"]["memory_cap_bytes"]
INF = float("inf")


def job_paths(job, kind) -> dict:
    if kind == "test":
        out = cc.SCRATCH / f"test_hwsc-{job}"
        return {"kind": kind, "out": out, "temp_root": out, "basetemp": out / "pytest"}
    if kind == "store":
        return {"kind": kind, "out": cc.STORE, "temp_root": cc.STORE / "tmp", "basetemp": None}
    raise ValueError(f"unknown job kind {kind!r}")


def memory_cap(stage) -> int:
    stage = "E2" if stage == "REG2" else stage
    if stage not in CAPS:
        raise ValueError(f"unknown stage {stage!r}")
    return int(CAPS[stage])


def bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None:
    cap = memory_cap(stage)
    k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)
    winjob.MEMORY_CAP = cap
    k4b_meter_bind.TEMP_ROOT = str(temp_root if temp_root is not None else out)
    meter.CAP_S = meter.STOP_NEW_S = INF
    meter.OUTPUT_CAP = int(cc.CONTRACT["resources"]["output_cap_bytes"])  # D-0192-1: whole store


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


def placement_ok(paths, root=cc.ROOT) -> dict:
    out, temp, base = paths.get("out"), paths.get("temp_root"), paths.get("basetemp")
    if paths.get("kind") == "store":
        checks = {"out_is_store": out is not None
                  and Path(out).resolve() == cc.STORE.resolve(),
                  "temp_under_store_tmp": _under(temp, cc.STORE / "tmp")}
        return {"ok": all(checks.values()), "checks": checks}
    checks = {"out_outside_root": _outside(out, root),
              "temp_outside_root": _outside(temp, root),
              "basetemp_outside_root": _outside(base, root),
              "test_prefixed": out is not None
              and Path(out).resolve().parent == cc.SCRATCH.resolve()
              and Path(out).name.startswith("test_")}
    return {"ok": all(checks.values()), "checks": checks}


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


def child_env_c(job) -> dict:
    """k4b_meter_bind.child_env(job) with its TEMP folder created (D-0177-1).

    Without the folder, tempfile.gettempdir() in the metered child skips TEMP/TMP/TMPDIR
    and falls back to the user temp folder on C:.
    """
    env = k4b_meter_bind.child_env(job)
    Path(env["TEMP"]).mkdir(parents=True, exist_ok=True)
    return env


def main() -> int:
    """--job, --task-sha256, --session, --kind, --stage (all required), then the meter argv."""
    argv, opts = sys.argv[1:], {}
    for flag in ("--job", "--task-sha256", "--session", "--kind", "--stage"):
        argv, opts[flag] = _pop(argv, flag)
    missing = [f for f, v in opts.items() if v is None]
    if missing:
        print(f"hwsc_meter_bind: missing {missing}", file=sys.stderr)
        return 2
    job, session = opts["--job"], opts["--session"]
    try:
        paths = job_paths(job, opts["--kind"])
        memory_cap(opts["--stage"])
    except ValueError as exc:
        print(f"hwsc_meter_bind: {exc}", file=sys.stderr)
        return 2
    out = Path(paths["out"])
    out.mkdir(parents=True, exist_ok=True)
    bind(job, opts["--task-sha256"], out, session, opts["--stage"], paths["temp_root"])
    if meter.LOCK.exists() and session not in meter.LOCK.read_text("utf-8"):
        print("hwsc_meter_bind: RUN.lock names another session", file=sys.stderr)
        return 3
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    os.environ.update(child_env_c(job))
    sys.argv = [sys.argv[0]] + k4b_meter_bind.rewrite_argv(argv)
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
