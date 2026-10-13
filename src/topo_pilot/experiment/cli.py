"""The ``topo-pilot`` command line (W0 skeleton: ``status`` and ``stage``)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path

from topo_pilot.contracts import (
    ARTIFACT_CLASSES,
    ArtifactMeta,
    ArtifactStore,
    GateReport,
    LocalFSBackend,
    MetricRecords,
    StageFailure,
)

from .config import ResolvedConfig, load_config, producer_version
from .prereg import write_prereg
from .report import build_e0
from .report_e2 import build_e2
from .report_x4 import x4_section
from .stages import STAGE_REGISTRY, run_stage

MAX_STATUS_LINES = 40


def open_store(cfg: ResolvedConfig) -> ArtifactStore:
    """The local artifact store at ``cfg.artifact_root`` (created on first write)."""
    return ArtifactStore(LocalFSBackend(cfg.artifact_root),
                         producer_version=producer_version(cfg.repo_root))


def status_lines(cfg: ResolvedConfig, store: ArtifactStore) -> list[str]:
    """At most 40 lines: artifact counts per type, the latest verdict per gate, config hash."""
    counts: Counter[str] = Counter()
    gates: dict[str, tuple[str, str]] = {}
    for atype in ARTIFACT_CLASSES:
        for key in store.backend.list(f"{atype}/"):
            if not key.endswith("/meta.json"):
                continue
            meta = ArtifactMeta.from_json_dict(json.loads(store.backend.get(key)))
            counts[atype if meta.status == "complete" else f"{atype} (incomplete)"] += 1
            if atype == "GateReport" and meta.status == "complete":
                report = store.load(GateReport, meta.artifact_id, consumer="experiment")
                prev = gates.get(report.gate_id)
                if prev is None or meta.created_utc >= prev[1]:
                    gates[report.gate_id] = (report.verdict, meta.created_utc)
    lines = [f"topo-pilot status | config {cfg.config_hash} | store {cfg.artifact_root.name}/",
             f"stages implemented: {', '.join(sorted(STAGE_REGISTRY)) or 'none'}",
             "artifacts:" if counts else "artifacts: none"]
    lines += [f"  {name}: {n}" for name, n in sorted(counts.items())]
    lines.append("gates:" if gates else "gates: none evaluated")
    lines += [f"  {gid}: {verdict} ({when})" for gid, (verdict, when) in sorted(gates.items())]
    if len(lines) > MAX_STATUS_LINES:
        lines = lines[: MAX_STATUS_LINES - 1] + [f"... ({len(lines) - MAX_STATUS_LINES + 1} more)"]
    return lines


def build_reports(level: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[Path]:
    """Write the report(s) for ``level``; ``all`` skips E2 until an S4 analysis exists."""
    out = []
    if level in ("all", "E0"):
        out.append(build_e0(store, cfg.repo_root / "reports" / "E0"))
    s4_done = bool(store.find(MetricRecords, stage="S4", kind="analysis"))
    if level == "E2" or (level == "all" and s4_done):
        final = int(cfg.base["training"]["primary_checkpoint"])
        extra = x4_section(store, cfg.repo_root / "PREREGISTRATION_X4.md", "O", final)
        out.append(build_e2(store, cfg.repo_root / "reports" / "E2", "S4", final, extra))
    return out


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="topo-pilot", description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    st = sub.add_parser("status", help="artifacts, gates, and stages (≤ 40 lines)")
    st.add_argument("--config", default="configs/stages.yaml")
    sg = sub.add_parser("stage", help="run a stage")
    sg.add_argument("stage_id")
    sg.add_argument("--config", default="configs/stages.yaml")
    sg.add_argument("--executor", default="local", choices=["local", "bundle", "ssh"])
    rp = sub.add_parser("report", help="summary + figures from MetricRecords only")
    rp.add_argument("--level", default="all", choices=["all", "E0", "E2"],
                    help="exit level; 'all' regenerates every level whose data exists")
    rp.add_argument("--config", default="configs/stages.yaml")
    pr = sub.add_parser("prereg", help="write PREREGISTRATION.md from S2 outputs (H1 draft)")
    pr.add_argument("--config", default="configs/stages.yaml")
    pr.add_argument("--note", default="", help="conductor note on decidable hypotheses")
    pr.add_argument("--force", action="store_true",
                    help="overwrite an existing PREREGISTRATION.md")
    return ap


def main(argv: list[str] | None = None) -> int:
    """Entry point. Exit codes: 0 ok, 1 ``StageFailure``, 2 usage error."""
    args = _parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    try:
        cfg = load_config(Path(args.config))
        store = open_store(cfg)
        if args.command == "status":
            print("\n".join(status_lines(cfg, store)))
            return 0
        if args.command == "prereg":
            out = write_prereg(cfg, store, args.note, force=args.force)
            print(f"prereg: {out.relative_to(cfg.repo_root).as_posix()}")
            return 0
        if args.command == "report":
            for out in build_reports(args.level, cfg, store):
                print(f"report: {out.relative_to(cfg.repo_root).as_posix()}")
            return 0
        if args.executor != "local":
            print(f"executor {args.executor!r} arrives in wave W1/W4; use --executor local")
            return 2
        written = run_stage(args.stage_id, cfg, store)
        print(f"stage {args.stage_id}: ok, wrote {len(written)} artifact(s): {', '.join(written)}")
        return 0
    except StageFailure as exc:
        print(f"FAILED {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
