"""Job binding for the reused job-0014 meter (standard library only; base interpreter, -I).

Reuses tools/x4_oracle_profile/{meter,controls,winjob}.py UNCHANGED from this worktree. It
rebinds their module-level constants to this job's task digest, output store and ledger, and adds
per-stage CPU ceilings. Nothing is copied or edited. The stage is recorded as a label prefix
"<stage>:<label>"; a stage total is the sum of charged CPU over that prefix.

Usage: python -I meter_bind.py --stage STAGE [--release RELEASE.json] --label L
       [meter options] -- CMD...
Without a verified release only the 0016 stages (implementation, export <= 80 s) are released.
An exhausted or unreleased stage still runs, as a metered no-op child that exits 4, so even the
refusal is charged.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORACLE_TOOLS = HERE.parent / "x4_oracle_profile"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ORACLE_TOOLS))

import controls  # noqa: E402  (job-0014, unchanged)
import meter  # noqa: E402  (job-0014, unchanged)
import release  # noqa: E402

CONTRACT = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
MARGIN_S = 1.0  # supervisor + tail allowance kept inside a stage ceiling


def bind(job_id: str, task_sha256: str, out: Path) -> None:
    """Point the unchanged modules at this job and store (module constants only)."""
    controls.JOB_ID = job_id
    controls.TASK_SHA256 = task_sha256.upper()
    meter.OUT = out
    meter.LEDGER = out / "cpu_ledger.json"
    meter.EMERGENCY = out / "cpu_ledger.emergency.jsonl"
    meter.LOCK = out / "RUN.lock"
    meter.ACTIVE = out / "METER_ACTIVE.lock"
    meter.LOG_DIR = out / "logs"
    res = CONTRACT["resources"]
    meter.CAP_S = float(res["cumulative_cpu_cap_s"])
    meter.STOP_NEW_S = float(res["stop_new_work_at_s"])
    meter.OUTPUT_CAP = int(res["output_bytes"])


def stage_caps(rel: dict | None) -> dict:
    res = CONTRACT["resources"]
    caps = dict(res["stage_caps_s"])
    if rel is None:
        released = set(res["job_0016_released_stages"])
        caps["export"] = min(caps["export"], float(res["job_0016_export_max_s"]))
    else:
        released = set(rel["released_stages"])
        caps.update({k: min(caps[k], float(v)) for k, v in rel.get("stage_ceilings_s", {}).items()})
    return {k: v for k, v in caps.items() if k in released}


def stage_spent(ledger_path: Path, stage: str) -> float:
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    return sum(
        float(e.get("charged_cpu_s") or 0.0)
        for e in ledger["entries"]
        if str(e.get("label", "")).startswith(f"{stage}:")
    )


def rewrite_argv(argv: list[str]) -> list[str]:
    """Extract --stage/--release, enforce the stage ceiling, return argv for meter.main()."""
    args, stage, release_path = list(argv), None, None
    for flag in ("--stage", "--release"):
        if flag in args:
            i = args.index(flag)
            value = args[i + 1]
            del args[i : i + 2]
            stage, release_path = (value, release_path) if flag == "--stage" else (stage, value)
    if stage is None:
        raise SystemExit("meter_bind: --stage is required")
    rel = release.verify(Path(release_path)) if release_path else None
    job_id = rel["job_id"] if rel else CONTRACT["job_id"]
    task_sha = rel["task_sha256"] if rel else CONTRACT["task_sha256"]
    out = Path(CONTRACT["resources"]["output_root"])
    bind(job_id, task_sha, out)
    caps = stage_caps(rel)
    remaining = (caps[stage] - stage_spent(meter.LEDGER, stage)) if stage in caps else 0.0
    i = args.index("--label")
    args[i + 1] = f"{stage}:{args[i + 1]}"
    sep = args.index("--") if "--" in args else len(args)
    if remaining <= MARGIN_S:
        args[i + 1] += ":REFUSED_stage_ceiling_or_unreleased"
        return args[:sep] + ["--", sys.executable, "-I", "-c", "raise SystemExit(4)"]
    if "--max-cpu" in args[:sep]:
        j = args.index("--max-cpu")
        args[j + 1] = str(min(float(args[j + 1]), remaining - MARGIN_S))
    else:
        args[sep:sep] = ["--max-cpu", str(remaining - MARGIN_S)]
    return args


def main() -> int:
    sys.argv = [sys.argv[0]] + rewrite_argv(sys.argv[1:])
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
