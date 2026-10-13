"""X5 G1 gate driver: controls, verdict precedence and immutable exports (x5g1-feas-v2 §7–§8).

``python -m topo_pilot.experiment.x5g1_main --repo . --main-store <artifacts> --out-store <dir>
--tables <dir> --mailbox <dir>``.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

from topo_pilot.analysis import x5_overall_verdict
from topo_pilot.contracts import (
    ArtifactStore,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
    StageFailure,
)

from .config import producer_version
from .x4b import ReadThroughBackend
from .x4b_run import _sha256, peak_memory_bytes
from .x5g1_controls import BudgetExceeded, RunControls, StopRequested
from .x5g1_lineage import ARMS
from .x5g1_run import CAP_S, CUMULATIVE_CAP_S, PROTOCOL, PROTOCOL_DOC, GateFailed, body

log = logging.getLogger(__name__)


def _jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    return obj


def run_gate(repo: Path, main_root: Path, out_root: Path, tables: Path, mailbox: Path) -> dict:
    """Run once; the ledger entry is written by ``RunControls`` whatever happens."""
    res: dict = {"protocol": PROTOCOL, "arms": {}, "global_failed": [], "global_inconclusive": []}
    out_root.mkdir(parents=True, exist_ok=True)
    ctl = RunControls(out_root / "cpu_ledger.json", CAP_S, mailbox / "STOP", "0006",
                      CUMULATIVE_CAP_S)
    with ctl:
        try:
            body(res, ctl, repo, main_root, out_root)
        except GateFailed as exc:
            res["global_failed"].append(str(exc))
        except StageFailure as exc:
            res["global_failed"].append(f"{type(exc).__name__}: {exc}")
        except (StopRequested, BudgetExceeded) as exc:
            res["global_inconclusive"].append(f"{type(exc).__name__}: {exc}")
        arms = {a: {"op": res["arms"].get(a, {}).get("op"),
                    "context": res["arms"].get(a, {}).get("context")} for a in ARMS}
        res["verdict"], res["reason"] = x5_overall_verdict(arms, res["global_failed"],
                                                        res["global_inconclusive"])
        ctl.outcome = f"{res['verdict']}: {res['reason']}"
        _export(repo, main_root, out_root, tables, res, ctl)
    return res


def _export(repo: Path, main_root: Path, out_root: Path, tables: Path, res: dict,
            ctl: RunControls) -> None:
    tables.mkdir(parents=True, exist_ok=True)
    meta = {"protocol": PROTOCOL, "protocol_doc_sha256": _sha256(repo / PROTOCOL_DOC),
            "producer_version": producer_version(repo), "python": sys.executable,
            "topo_pilot_file": __import__("topo_pilot").__file__,
            "numpy": np.__version__,
            "blas_threads": {k: os.environ.get(k) for k in
                             ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS")},
            "cpu_s_before_export": round(ctl.cpu(), 3), "cpu_prior_cumulative": ctl.prior,
            "peak_memory_bytes": peak_memory_bytes(), "steps": ctl.steps,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    ids = [p["artifact_id"] for p in res.get("provenance", [])]
    ids += [x for x in (res.get("T_a020_id"),) + tuple(res["arms"].get(a, {}).get("obs_id")
                                                       for a in ARMS) if x]
    if ids and not res["global_failed"]:
        rw = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root),
                                              LocalFSBackend(out_root / "store")),
                           producer_version=meta["producer_version"])
        rows = [MetricRow(run_id="X5G1", space="x5g1:verdict",
                          metric_id=f"verdict={res['verdict']}", value=1.0, world="cylinder",
                          condition="O", parent_ids=tuple(ids))]
        for arm, a in res["arms"].items():
            for k in ("GC", "GC_stationary", "two_token_regret"):
                v = a.get(k)
                rows.append(MetricRow(run_id="X5G1", space=f"x5g1:{arm}", metric_id=k,
                                      value=None if v is None else float(v),
                                      status="ok" if v is not None else "inconclusive",
                                      world="cylinder", condition="O", parent_ids=tuple(ids)))
            rows.append(MetricRow(run_id="X5G1", space=f"x5g1:{arm}",
                                  metric_id=f"context={a.get('context')}", value=1.0,
                                  world="cylinder", condition="O", parent_ids=tuple(ids)))
        meta["metric_records_id"] = rw.save(
            MetricRecords(rows=tuple(rows)),
            config={"stage": "X5G1_GATE", "protocol": PROTOCOL,
                    "protocol_doc_sha256": meta["protocol_doc_sha256"]},
            parents=sorted(set(ids)), seed_map={}, consumer="experiment")
    files = {"verdict.json": {k: res.get(k) for k in ("protocol", "verdict", "reason",
                                                       "global_failed", "global_inconclusive")},
             "result.json": res, "run.json": meta}
    for name, obj in files.items():
        (tables / name).write_text(json.dumps(_jsonable(obj), indent=1, default=str),
                                   encoding="utf-8")
    manifest = {f.name: _sha256(f) for f in sorted(tables.iterdir()) if f.name != "MANIFEST.json"}
    (tables / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X5 G1 exact-process/calibration gate")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--out-store", type=Path, required=True)
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--mailbox", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        res = run_gate(args.repo, args.main_store, args.out_store, args.tables, args.mailbox)
    except (StopRequested, BudgetExceeded) as exc:
        log.error("x5g1: stopped during export: %s", exc)
        return 2
    log.info("x5g1: %s %s", res["verdict"], res["reason"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
