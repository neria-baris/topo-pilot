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
    StageFailure,
)

from .config import ResolvedConfig, load_config, producer_version
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


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="topo-pilot", description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    st = sub.add_parser("status", help="artifacts, gates, and stages (≤ 40 lines)")
    st.add_argument("--config", default="configs/stages.yaml")
    sg = sub.add_parser("stage", help="run a stage")
    sg.add_argument("stage_id")
    sg.add_argument("--config", default="configs/stages.yaml")
    sg.add_argument("--executor", default="local", choices=["local", "bundle", "ssh"])
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
