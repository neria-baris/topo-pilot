"""Job binding for the reused job-0014 meter (standard library only; base interpreter, -I).

Reuses tools/x4_oracle_profile/{meter,controls,winjob}.py UNCHANGED from this worktree. It
rebinds their module-level names to this job's task digest, output store and ledger, and to:
- a stage-aware limiter: the stage ceiling is checked against stage spent + current child +
  current supervisor CPU + tail allowance, continuously during supervision, alongside the
  unchanged global limits;
- the finalization rule: only an explicit `--finalization` export may proceed past 3480 toward
  3600; every other stage stops new work at 3480.

The stage is recorded as the Windows-safe label prefix "<stage>__<label>" (a colon would create
an NTFS alternate data stream in log file names; legacy "<stage>:" entries are still counted).
The release check (release.verify) reads git files directly and spawns no process before the
Job Object exists.
An exhausted or unreleased stage still runs, as a metered no-op child that exits 4, so the
refusal is charged.

Usage: python -I meter_bind.py --stage STAGE [--release RELEASE.json] [--finalization]
       --label L [meter options] -- CMD...
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
MARGIN_S = 1.0
_LEGACY_LIMIT = meter.limit_reason


def bind(job_id: str, task_sha256: str, out: Path, finalization: bool = False) -> None:
    """Point the unchanged modules at this job and store (module-level names only)."""
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
    meter.STOP_NEW_S = meter.CAP_S if finalization else float(res["stop_new_work_at_s"])
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
    ledger = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    return sum(
        float(e.get("charged_cpu_s") or 0.0)
        for e in ledger["entries"]
        if str(e.get("label", "")).startswith((f"{stage}__", f"{stage}:"))
    )


def make_stage_limiter(stage_cap: float, spent: float, own_cpu=None, legacy=None):
    """Limiter for meter.limit_reason: stage spent + child + supervisor + tail < stage cap."""
    own_cpu = own_cpu or meter.own_cpu_s
    legacy = legacy or _LEGACY_LIMIT

    def limit_reason(ledger, child, args, active_wall, polls, mailboxes):
        used = spent + child + own_cpu() + meter.TAIL_ALLOWANCE_S
        if used >= stage_cap:
            return f"stage ceiling {stage_cap} reached ({used:.3f} incl. supervisor)", "CONTINUE"
        return legacy(ledger, child, args, active_wall, polls, mailboxes)

    return limit_reason


def _pop(args: list, flag: str, has_value: bool = True):
    if flag not in args:
        return None
    i = args.index(flag)
    value = args[i + 1] if has_value else True
    del args[i : i + (2 if has_value else 1)]
    return value


def rewrite_argv(argv: list[str]) -> list[str]:
    """Extract --stage/--release/--finalization, bind, install limiter, return meter argv."""
    args = list(argv)
    stage = _pop(args, "--stage")
    release_path = _pop(args, "--release")
    finalization = bool(_pop(args, "--finalization", has_value=False))
    if stage is None:
        raise SystemExit("meter_bind: --stage is required")
    if finalization and stage != "export":
        raise SystemExit("meter_bind: --finalization is only valid for the export stage")
    rel = release.verify(Path(release_path)) if release_path else None
    job_id = rel["job_id"] if rel else CONTRACT["job_id"]
    task_sha = rel["task_sha256"] if rel else CONTRACT["task_sha256"]
    bind(job_id, task_sha, Path(CONTRACT["resources"]["output_root"]), finalization)
    caps = stage_caps(rel)
    spent = stage_spent(meter.LEDGER, stage)
    remaining = (caps[stage] - spent) if stage in caps else 0.0
    i = args.index("--label")
    args[i + 1] = f"{stage}__{args[i + 1]}"
    sep = args.index("--") if "--" in args else len(args)
    if remaining <= MARGIN_S:
        args[i + 1] += "__REFUSED_stage_ceiling_or_unreleased"
        meter.limit_reason = make_stage_limiter(float("inf"), 0.0)
        return args[:sep] + ["--", sys.executable, "-I", "-c", "raise SystemExit(4)"]
    meter.limit_reason = make_stage_limiter(caps[stage], spent)
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
