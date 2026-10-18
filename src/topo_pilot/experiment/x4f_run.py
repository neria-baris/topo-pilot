"""Prospective X4-F maintenance runner; the historical x4f-exec-v2 cohort stays closed.

``python -m topo_pilot.experiment.x4f_run --main-store <artifacts> --out-store <dir>
--tables <dir> --mailbox <dir>``. Gates run in order G1..G5 over all three models; a later gate
runs only when the previous one passed in every model (else NOT_RUN). The main store is
read-only (listing hash before/after); new artifacts go to the independent store.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

from topo_pilot.analysis import fit_oblique_eraser, gate_verdict, whiten
from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
)
from topo_pilot.learner import load_model

from .config import load_config, producer_version
from .s4_analysis import AnalysisJob
from .x4b import ReadThroughBackend, provenance_row
from .x4b_run import Budget, _sha256, listing_hash, peak_memory_bytes
from .x4f_damage import g3, g4, g5
from .x4f_data import SEEDS, extract, load_model_data, resolve
from .x4f_gates import ValForward, control_targets, g1, g2
from .x5g1_controls import BudgetExceeded, RunControls, StopRequested

log = logging.getLogger(__name__)
PROTOCOL = "x4f-maintenance-v1"
PROTOCOL_DOC = "docs/proposals/X4F_MAINTENANCE_V1.md"
CPU_CAP_S, CUMULATIVE_CAP_S = 3600.0, 10800.0


def _gate(status: str) -> str:
    return status.split(":")[0]


def run_gates(repo: Path, main_root: Path, out_root: Path, tables: Path, mailbox: Path) -> dict:
    """Prospective maintenance runner; never overwrite an earlier cohort's exports."""
    for path in (tables, out_root / "exports"):
        if path.exists() and any(path.iterdir()):
            raise FileExistsError(f"refusing to overwrite prior outputs: {path}")
    ctl = RunControls(out_root / "cpu_ledger.json", CPU_CAP_S, mailbox / "STOP",
                      PROTOCOL, CUMULATIVE_CAP_S)
    with ctl:
        ctl.guard("before inputs")
        summary = _run_gates(repo, main_root, out_root, tables, ctl)
        ctl.outcome = summary["overall"]
        ctl.guard("exports complete")
        return summary


def _run_gates(repo, main_root, out_root, tables, ctl):
    ledger_path = out_root / "cpu_ledger.json"
    ledger = (json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists()
              else {"entries": [], "cumulative_cpu_s": 0.0})
    if ledger["cumulative_cpu_s"] >= CUMULATIVE_CAP_S:
        raise BudgetExceeded("cumulative X4-F cap already reached")
    budget = Budget(min(CPU_CAP_S, CUMULATIVE_CAP_S - ledger["cumulative_cpu_s"]))
    budget.t0, budget.steps = ctl.t0, ctl.steps

    def checkpoint(step: str) -> None:
        ctl.guard(step)

    before = listing_hash(main_root)
    main = ArtifactStore(LocalFSBackend(main_root))
    rw = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root), LocalFSBackend(out_root /
                                                                                  "store")),
                       producer_version=producer_version(repo))
    aj = AnalysisJob("S4", load_config(repo / "configs" / "stages.yaml", repo), main)
    ids, act_ids, data, models = {}, {}, {}, {}
    for s in SEEDS:
        checkpoint(f"before inputs {s}")
        ids[s] = resolve(aj, main, s)
        act_ids[s] = extract(rw, ids[s])
        data[s] = load_model_data(rw, ids[s], act_ids[s], s)
        models[s] = load_model(main.load(Checkpoint, ids[s]["checkpoint"], consumer="experiment"))
        checkpoint(f"extract+targets {s}")
    rec = {s: {} for s in SEEDS}
    status = {s: {} for s in SEEDS}
    for s in SEEDS:
        rec[s]["G1"] = g1(data[s], checkpoint)
        status[s]["G1"] = _gate(rec[s]["G1"]["status"])
        checkpoint(f"G1 {s}")
    state = {}
    for gate in ("G2", "G3", "G4", "G5"):
        prev = f"G{int(gate[1]) - 1}"
        if any(status[s][prev] != "PASS" for s in SEEDS):
            for s in SEEDS:
                status[s][gate] = "NOT_RUN"
                rec[s][gate] = {"status": f"NOT_RUN: {prev} did not pass in every model"}
            continue
        for s in SEEDS:
            d = data[s]
            if gate == "G2":
                wh = whiten(d.acts["resid_post_1"][d.cal])
                primary = fit_oblique_eraser(d.acts["resid_post_1"][d.cal],
                                             d.targets["m32"][d.cal], wh)
                state[s] = {"wh": wh, "primary": primary, "vf": ValForward(models[s], d)}
                rec[s]["G2"] = g2(d, models[s], state[s]["vf"], primary)
            elif gate == "G3":
                rec[s]["G3"] = g3(d, state[s]["wh"], state[s]["primary"], checkpoint)
            elif gate == "G4":
                rec[s]["G4"], state[s]["clouds"] = g4(d, state[s]["vf"], state[s]["wh"],
                                                     state[s]["primary"], control_targets(d),
                                                     checkpoint)
                state[s]["maps"] = rec[s]["G4"].pop("_maps", {})
            else:
                rec[s]["G5"] = g5(d, state[s]["clouds"])
            status[s][gate] = _gate(rec[s][gate]["status"])
            checkpoint(f"{gate} {s}")
    overall, reason = gate_verdict(status)
    after = listing_hash(main_root)
    summary = {"protocol": PROTOCOL, "overall": overall, "reason": reason, "status": status,
               "main_store_unchanged": after == before}
    _export(repo, main, rw, out_root, tables, ids, act_ids, data, rec, state, summary, budget,
            before, after, ledger, checkpoint)
    return summary


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


def _export(repo, main, rw, out_root, tables, ids, act_ids, data, rec, state, summary, budget,
            before, after, ledger, checkpoint=lambda _: None) -> None:
    tables.mkdir(parents=True, exist_ok=True)
    exports = out_root / "exports"
    exports.mkdir(parents=True, exist_ok=True)
    prov, sums = [], {}
    for s in SEEDS:
        checkpoint(f"before export {s}")
        prov += [provenance_row(main, v, f"{k}[{s}]") for k, v in ids[s].items()]
        prov.append(provenance_row(rw, act_ids[s], f"dev_activations[{s}]"))
        d, st = data[s], state.get(s, {})
        arrays = {"history_id": np.array(d.history_id), "panel": d.panel,
                  **{k: v for k, v in d.targets.items() if k != "onehot_w32"}}
        if "primary" in st:
            arrays.update(primary_M=st["primary"].M, primary_mu=st["primary"].mu,
                          whitening_k=np.array(st["wh"].k))
        for name, (mu, M, rank, status) in st.get("maps", {}).items():
            arrays.update({f"map_{name}_mu": mu, f"map_{name}_M": M,
                           f"map_{name}_rank": np.array(rank),
                           f"map_{name}_status": np.array(status)})
        path = exports / f"x4f_gates_{s}.npz"
        np.savez(path, **arrays)
        sums[path.name] = _sha256(path)
        checkpoint(f"export {s} complete")
    parents = tuple(sorted({r["artifact_id"] for r in prov}))
    meta = {"protocol": PROTOCOL, "protocol_doc_sha256": _sha256(repo / PROTOCOL_DOC),
            "producer_version": producer_version(repo), "python": sys.executable,
            "topo_pilot_file": __import__("topo_pilot").__file__,
            "blas_threads": {k: os.environ.get(k) for k in
                             ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS")},
            "cpu_s": round(time.process_time() - budget.t0, 2),
            "wall_s": round(time.time() - budget.w0, 2), "cpu_cap_s": budget.cap,
            "peak_memory_bytes": peak_memory_bytes(), "budget_steps": budget.steps,
            "ledger_before_run": ledger, "ledger_path": str(out_root / "cpu_ledger.json"),
            "main_store_listing_before": before,
            "main_store_listing_after": after, "exports_sha256": sums}
    rows = [MetricRow(run_id="X4F_GATES", space="x4f:gate", metric_id=f"{g}={v}", value=1.0,
                      replicate=s, world="cylinder", condition="O", checkpoint=5000,
                      hook="resid_post_1", parent_ids=parents)
            for s, gs in summary["status"].items() for g, v in gs.items()]
    rows.append(MetricRow(run_id="X4F_GATES", space="x4f:verdict",
                          metric_id=f"overall={summary['overall']}", value=1.0,
                          world="cylinder", condition="O", parent_ids=parents))
    meta["metric_records_id"] = rw.save(
        MetricRecords(rows=tuple(rows)),
        config={"stage": "X4F_GATES", "protocol": PROTOCOL,
                "protocol_doc_sha256": meta["protocol_doc_sha256"], "exports_sha256": sums},
        parents=parents, seed_map={}, consumer="experiment")
    files = {"inputs.json": prov, "gates.json": rec, "verdict.json": summary, "run.json": meta}
    for name, obj in files.items():
        checkpoint(f"export table {name}")
        (tables / name).write_text(json.dumps(_jsonable(obj), indent=1, default=str),
                                   encoding="utf-8")
    _profiles_csv(tables / "profiles.csv", rec)
    manifest = {f.name: _sha256(f) for f in sorted(tables.iterdir()) if f.name != "MANIFEST.json"}
    (tables / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


def _profiles_csv(path: Path, rec: dict) -> None:
    rows = []
    for s, gates in rec.items():
        for name, p in gates.get("G4", {}).get("profiles", {}).items():
            flat = {"seed": s, "map": name, **{k: v for k, v in p.items() if k != "disp_val"}}
            flat.update({f"disp_val_{k}": v for k, v in p.get("disp_val", {}).items()})
            rows.append(flat)
    if rows:
        keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("seed", "map"), k))
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X4-F calibration/validation gates (x4f-exec-v2)")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--out-store", type=Path, required=True)
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--mailbox", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        summary = run_gates(args.repo, args.main_store, args.out_store, args.tables, args.mailbox)
    except (BudgetExceeded, StopRequested) as exc:
        log.error("x4f: stopped: %s: %s", type(exc).__name__, exc)
        return 2
    log.info("x4f: %s", json.dumps({k: summary[k] for k in ("overall", "reason", "status")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
