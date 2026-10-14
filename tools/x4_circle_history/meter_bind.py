"""Job binding for the reused job-0014 meter (standard library only; base interpreter, -I).

Reuses tools/x4_oracle_profile/{meter,controls,winjob}.py UNCHANGED from this worktree. It
rebinds their module-level names to this job's task digest, output store and ledger, and to:
- a stage-aware limiter: the stage ceiling is checked against stage spent + current child +
  current supervisor CPU + tail allowance, continuously during supervision, alongside the
  unchanged global limits;
- the finalization rule: only an explicit `--finalization` export may proceed past 3480 toward
  3600; every other stage stops new work at 3480.

Spec v2.4 additions (items 7 and 13): the limiter also kills an operation whose
OPERATION_ACTIVE.json marker is past its native-operation deadline (the existing supervisor
loop is the enforcement; no new watcher), and applies the owner's disk safe-STOP (C: < 2 GB or
X: < 30 GB free). Before launch, a stale active marker of a killed attempt is archived, and the
recorded CONTRACT allocation is applied to the ledger cap metadata in this supervisor process
(charged to this run; every entry preserved).

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
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORACLE_TOOLS = HERE.parent / "x4_oracle_profile"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ORACLE_TOOLS))

import controls  # noqa: E402  (job-0014, unchanged)
import meter  # noqa: E402  (job-0014, unchanged)
import op_guard  # noqa: E402
import release  # noqa: E402

CONTRACT = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
MARGIN_S = 1.0
DISK_MIN_FREE = {"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}
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


def disk_reason(usage=shutil.disk_usage):
    """Owner disk safe-STOP: a reason when C: or X: free space is below its threshold."""
    for drive, minimum in DISK_MIN_FREE.items():
        try:
            free = usage(drive).free
        except OSError as exc:
            return f"disk safe-STOP: {drive} free space unreadable ({type(exc).__name__})"
        if free < minimum:
            return f"disk safe-STOP: {drive} free {free} < {minimum} bytes"
    return None


def make_stage_limiter(
    stage_cap: float,
    spent: float,
    own_cpu=None,
    legacy=None,
    op_marker=None,
    op_clock=time.time,
    disk=disk_reason,
):
    """Limiter for meter.limit_reason: stage spent + child + supervisor + tail < stage cap, the
    native-operation deadline of an active marker, and the disk safe-STOP (every 8th poll)."""
    own_cpu = own_cpu or meter.own_cpu_s
    legacy = legacy or _LEGACY_LIMIT

    def limit_reason(ledger, child, args, active_wall, polls, mailboxes):
        used = spent + child + own_cpu() + meter.TAIL_ALLOWANCE_S
        if used >= stage_cap:
            return f"stage ceiling {stage_cap} reached ({used:.3f} incl. supervisor)", "CONTINUE"
        if op_marker is not None:
            overdue = op_guard.overdue(op_marker, op_clock())
            if overdue:
                return overdue, "CONTINUE"
        if disk is not None and polls % 8 == 0:
            reason = disk()
            if reason:
                return reason, "CONTINUE"
        return legacy(ledger, child, args, active_wall, polls, mailboxes)

    return limit_reason


def sync_ledger_caps(ledger_path: Path) -> bool:
    """Apply the recorded CONTRACT allocation to the ledger cap metadata (entries untouched)."""
    res = CONTRACT["resources"]
    ledger = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    caps = {k: float(v) for k, v in res["stage_caps_s"].items()}
    current = {k: float(v) for k, v in ledger.get("stage_caps_s", {}).items()}
    if current == caps:
        return False
    history = res.get("allocation_history", [])
    previous = [{k: float(v) for k, v in h["stage_caps_s"].items()} for h in history]
    if current not in previous:
        raise SystemExit(
            "meter_bind: ledger stage caps match neither the current nor a recorded allocation"
        )
    record = history[previous.index(current)]
    entries_before = json.dumps(ledger["entries"], sort_keys=True)
    updated = dict(ledger, stage_caps_s=dict(res["stage_caps_s"]))
    updated["allocation_history"] = list(ledger.get("allocation_history", [])) + [
        {
            "from": ledger["stage_caps_s"],
            "to": dict(res["stage_caps_s"]),
            "authority": record["authority"],
            "note": record["note"],
            "applied_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "applied_by": "meter_bind supervisor (charged to this run)",
            "entries_at_apply": len(ledger["entries"]),
        }
    ]
    if "owner_override" in res:
        updated["owner_override"] = res["owner_override"]
    assert json.dumps(updated["entries"], sort_keys=True) == entries_before
    meter.atomic_json(Path(ledger_path), updated)
    return True


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
    if not meter.ACTIVE.exists():
        sync_ledger_caps(meter.LEDGER)
        op_guard.archive_stale(meter.OUT)
    caps = stage_caps(rel)
    spent = stage_spent(meter.LEDGER, stage)
    remaining = (caps[stage] - spent) if stage in caps else 0.0
    i = args.index("--label")
    args[i + 1] = f"{stage}__{args[i + 1]}"
    sep = args.index("--") if "--" in args else len(args)
    disk = disk_reason()
    if remaining <= MARGIN_S or disk:
        args[i + 1] += (
            "__REFUSED_disk_safe_stop" if disk else "__REFUSED_stage_ceiling_or_unreleased"
        )
        meter.limit_reason = make_stage_limiter(float("inf"), 0.0)
        return args[:sep] + ["--", sys.executable, "-I", "-c", "raise SystemExit(4)"]
    meter.limit_reason = make_stage_limiter(
        caps[stage], spent, op_marker=meter.OUT / op_guard.MARKER
    )
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
