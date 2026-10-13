"""E4 circular-baseline audit (protocol circ-audit-v1): descriptive, existing artifacts only.

Per cylinder-O run and S7 test panel: the S7 circular estimator on the model (resid_post_3 at
step 5000) and R0 (step 0), both reproduced against the stored S7 rows, and on R1 (embed at p32),
R2 and R3 (existing k); the b1/b32 circular-mean angles; the y-axis control; and the in-sample
symbol-only bound. All values are privileged_eval. ``python -m topo_pilot.experiment.circ_audit
--main-store <artifacts> --out-store <dir> --tables <dir>``.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import time
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cdist

from topo_pilot.analysis import (
    CircularCorrespondence,
    SpaceBuilder,
    belief_angle,
    circular_agreement,
    lattice_angle,
    symbol_only_bound,
)
from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    EvalSidecar,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
    SeedTree,
    StageFailure,
    TransitionSpec,
    WorldSpec,
)

from .config import load_config, producer_version
from .s2 import child_of
from .s4_analysis import AnalysisJob
from .x4b import ReadThroughBackend, index_tokens, provenance_row
from .x4b_run import Budget, BudgetExceeded, _sha256, listing_hash, peak_memory_bytes

log = logging.getLogger(__name__)
CONS = "experiment"
PROTOCOL = "circ-audit-v1"
PROTOCOL_DOC = "docs/proposals/CIRCULAR_BASELINE_AUDIT_PROTOCOL.md"
S7_CIRCULAR = "a7a60592e32b26fb"
SEEDS = (1729, 2718, 3141)
PANELS = tuple(range(1, 9))
HOOK = "resid_post_3"
SPACE = "privileged_eval:circular_audit"
BASELINES = ("R1", "R2", "R3")
S7_KEYS = ("agreement_x", "agreement_x_null_q95", "agreement_x_p", "agreement_control",
           "agreement_oracle_x")


def _s7_rows(store: ArtifactStore) -> dict:
    out: dict = {}
    for r in store.load(MetricRecords, S7_CIRCULAR, consumer=CONS).rows:
        if r.world == "cylinder" and r.condition == "O" and r.panel is not None:
            out.setdefault((r.replicate, r.checkpoint, r.panel), {})[r.metric_id] = r.value
    return out


def _latent(store: ArtifactStore, sidecar_id: str, seqs: np.ndarray, ends: np.ndarray):
    side = store.load(EvalSidecar, sidecar_id, consumer=CONS)
    row_of = {int(s): i for i, s in enumerate(side.sequence_id)}
    if any(int(s) not in row_of for s in seqs):
        raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.circ_audit", "sidecar",
                           "a history's sequence is absent from the EvalSidecar", sidecar_id)
    rows = np.array([row_of[int(s)] for s in seqs], dtype=np.int64)
    return np.asarray(side.z)[rows, ends.astype(np.int64) - 1].astype(np.int64)


def _baseline_row(cc: CircularCorrespondence, X: np.ndarray, theta, theta_y, rng) -> dict:
    distinct = int(np.unique(np.round(X, 12), axis=0).shape[0])
    row = {"n_distinct_points": distinct, "n_duplicate_rows": int(X.shape[0] - distinct)}
    try:
        res = cc.compare(cdist(X, X), theta, rng)
    except StageFailure as exc:
        return {**row, "status": "estimator_failure", "error": f"{exc.code.value}:{exc.check}"}
    if res["status"] != "ok":
        return {**row, "status": res["status"]}
    return {**row, "status": "ok", "agreement": res["agreement"], "null_q95": res["null_q95"],
            "p": res["p_value"], "control": circular_agreement(res["phi"], theta_y)}


def _repro(cc, store, act, side, world, oracle, seed, step, p, stored) -> tuple[dict, bool]:
    rng = SeedTree(0).generator("circ_null", "cylinder", "O", seed, step, p)
    rows = cc.run(store, act, side, world, oracle, HOOK, p, rng, world="cylinder",
                  condition="O", replicate=seed, checkpoint=step)
    got = {r.metric_id: r.value for r in rows}
    same = all(got.get(k) == stored.get(k) for k in S7_KEYS)
    return {"status": "ok" if got["agreement_x"] is not None else "no_h1_class",
            "agreement": got["agreement_x"], "null_q95": got["agreement_x_null_q95"],
            "p": got["agreement_x_p"], "control": got["agreement_control"],
            "b32_angle": got["agreement_oracle_x"], "reproduces_s7": same}, same


def audit_run(store: ArtifactStore, aj: AnalysisJob, seed: int, s7: dict) -> tuple[list, list]:
    """All panel rows of one run, plus reproduction failures."""
    cc, sb = CircularCorrespondence(47, 1000), SpaceBuilder(store)
    inp = aj.inputs("cylinder", "O", seed)
    side = child_of(store, EvalSidecar, inp["emission"], split="test")
    acts = {step: aj.acts("cylinder", "O", seed, step) for step in (0, 5000)}
    coords = np.asarray(store.load(WorldSpec, inp["world"], consumer=CONS).coords, dtype=float)
    index, tok = index_tokens(store, inp["history_index"], inp["obs_test"])
    refs = {"activation_set_id": acts[5000], "emission_id": inp["emission"],
            "transition_id": child_of(store, TransitionSpec, inp["world"]),
            "obs_test_id": inp["obs_test"], "history_index_id": inp["history_index"],
            "k": 12}
    rows, fails = [], []
    for p in PANELS:
        mask = np.asarray(index.panel) == p
        ids = [str(h) for h in np.asarray(index.history_id)[mask]]
        z = _latent(store, side, np.asarray(index.sequence_id)[mask], np.asarray(index.end)[mask])
        theta, theta_y = lattice_angle(coords, z, 0, 12.0), lattice_angle(coords, z, 1, 12.0)
        w32 = tok[mask][:, -1]
        clouds = {"model": sb.activations(acts[5000], HOOK, p), "R0": sb.activations(
            acts[0], HOOK, p)} | {k: sb.baseline(k, p, **refs) for k in BASELINES}
        b1 = sb.beliefs(inp["oracle"], "b1", p)
        b32 = sb.beliefs(inp["oracle"], "b32", p)
        for name, ps in [*clouds.items(), ("b1", b1), ("b32", b32)]:
            if list(ps.ids) != ids:
                raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.circ_audit",
                                   "ids", f"{name} panel {p} ids differ (seed {seed})")
        panel = {"seed": seed, "panel": p, "M": len(ids),
                 "n_symbols": int(np.unique(w32).size),
                 "A_symbol_bound": symbol_only_bound(theta, w32),
                 "A_b1_angle": circular_agreement(belief_angle(b1.X, coords, 0, 12.0), theta),
                 "A_b32_angle": circular_agreement(belief_angle(b32.X, coords, 0, 12.0), theta)}
        reps = {}
        for step, name in ((5000, "model"), (0, "R0")):
            reps[name], ok = _repro(cc, store, acts[step], side, inp["world"], inp["oracle"],
                                    seed, step, p, s7.get((seed, step, p), {}))
            X = clouds[name].X
            distinct = int(np.unique(np.round(X, 12), axis=0).shape[0])
            reps[name].update(n_distinct_points=distinct, n_duplicate_rows=len(ids) - distinct)
            if not ok:
                fails.append(f"s7_reproduction[{seed},{step},{p}]")
        for k in BASELINES:
            rng = SeedTree(0).generator("circ_audit_null", k, "cylinder", "O", seed, p)
            reps[k] = _baseline_row(cc, clouds[k].X, theta, theta_y, rng)
        if abs(reps["model"]["b32_angle"] - panel["A_b32_angle"]) > 1e-12:
            fails.append(f"b32_angle[{seed},{p}]")
        rows.append({**panel, "reps": reps, **compare_panel(panel, reps)})
    return rows, fails


def compare_panel(panel: dict, reps: dict) -> dict:
    """Frozen C1/C2 of circ-audit-v1 for one panel."""
    a = reps["model"].get("agreement")
    avail = {k: reps[k]["agreement"] for k in BASELINES if reps[k]["status"] == "ok"}
    avail["b1_angle"] = panel["A_b1_angle"]
    best = max(avail.values())
    c1 = a is not None and a > panel["A_symbol_bound"]
    c2 = a is not None and a > best
    return {"C1": c1, "C2": c2, "best_baseline": max(avail, key=avail.get),
            "best_baseline_value": best,
            "baselines_not_ok": [k for k in BASELINES if reps[k]["status"] != "ok"],
            "margin_vs_symbol_bound": None if a is None else a - panel["A_symbol_bound"],
            "margin_vs_best_baseline": None if a is None else a - best}


def summarize(rows: list[dict]) -> dict:
    """Per-run counts and the frozen reading (all 3 / 0 / mixed)."""
    runs = {}
    for seed in SEEDS:
        rs = [r for r in rows if r["seed"] == seed]
        both = sum(r["C1"] and r["C2"] for r in rs)
        med = {k: float(np.median([r[k] for r in rs if r[k] is not None])) for k in
               ("margin_vs_symbol_bound", "margin_vs_best_baseline", "A_symbol_bound",
                "A_b1_angle", "A_b32_angle")}
        for rep in ("model", "R0", *BASELINES):
            vals = [r["reps"][rep].get("agreement") for r in rs]
            ok = [v for v in vals if v is not None]
            med[f"A_{rep}"] = float(np.median(ok)) if ok else None
            med[f"n_ok_{rep}"] = len(ok)
            med[f"n_above_null_{rep}"] = sum(1 for r in rs if r["reps"][rep].get("agreement")
                                            is not None and r["reps"][rep]["agreement"]
                                            > r["reps"][rep]["null_q95"])
        runs[seed] = {"n_C1": sum(r["C1"] for r in rs), "n_C2": sum(r["C2"] for r in rs),
                      "n_both": both, "adds_beyond": both >= 7, **med}
    n = sum(v["adds_beyond"] for v in runs.values())
    reading = ("BEYOND_SYMBOL_AND_MIXING" if n == 3 else
               "SYMBOL_MIXING_SUFFICES_FOR_NOW" if n == 0 else "NOT_ESTABLISHED_MIXED")
    return {"runs": runs, "n_runs_adding_beyond": n, "reading": reading}


def run_audit(repo: Path, main_root: Path, out_root: Path, tables: Path) -> dict:
    budget, before = Budget(), listing_hash(main_root)
    store = ArtifactStore(LocalFSBackend(main_root))
    aj = AnalysisJob("S4", load_config(repo / "configs" / "stages.yaml", repo), store)
    s7 = _s7_rows(store)
    rows, fails = [], []
    for seed in SEEDS:
        r, f = audit_run(store, aj, seed, s7)
        rows, fails = rows + r, fails + f
        budget.check(f"seed {seed}")
    summary = {"protocol": PROTOCOL, **summarize(rows), "failures": fails}
    after = listing_hash(main_root)
    if after != before:
        summary["failures"].append("main_store_changed")
    _export(repo, main_root, out_root, tables, store, aj, rows, summary, budget, before, after)
    return summary


def _export(repo, main_root, out_root, tables, store, aj, rows, summary, budget, before, after):
    tables.mkdir(parents=True, exist_ok=True)
    prov = [provenance_row(store, S7_CIRCULAR, "S7:circular")]
    for seed in SEEDS:
        inp = aj.inputs("cylinder", "O", seed)
        side = child_of(store, EvalSidecar, inp["emission"], split="test")
        prov += [provenance_row(store, aj.acts("cylinder", "O", seed, s), f"acts[{seed},{s}]")
                 for s in (0, 5000)]
        prov += [provenance_row(store, v, f"{k}[{seed}]") for k, v in
                 (("sidecar", side), ("oracle", inp["oracle"]), ("history_index",
                  inp["history_index"]), ("obs_test", inp["obs_test"]),
                  ("emission", inp["emission"]))]
    prov += [provenance_row(store, inp["world"], "world"),
             provenance_row(store, child_of(store, TransitionSpec, inp["world"]), "transition")]
    parents = tuple(sorted({r["artifact_id"] for r in prov}))
    flat = []
    for r in rows:
        base = {k: v for k, v in r.items() if k != "reps"}
        for rep, v in r["reps"].items():
            flat.append({**base, "representation": rep, **{k: v.get(k) for k in (
                "status", "agreement", "null_q95", "p", "control", "n_distinct_points",
                "n_duplicate_rows", "error", "reproduces_s7")}})
    meta = {"protocol": PROTOCOL, "protocol_doc_sha256": _sha256(repo / PROTOCOL_DOC),
            "producer_version": producer_version(repo),
            "cpu_s": round(time.process_time() - budget.t0, 2),
            "wall_s": round(time.time() - budget.w0, 2), "cpu_cap_s": budget.cap,
            "peak_memory_bytes": peak_memory_bytes(), "budget_steps": budget.steps,
            "main_store_listing_before": before, "main_store_listing_after": after}
    mrows = [MetricRow(run_id="CIRC_AUDIT", space=SPACE, metric_id=f"{f['representation']}:"
                       f"agreement", value=f["agreement"], status="ok" if f["agreement"]
                       is not None else "inconclusive", replicate=f["seed"], world="cylinder",
                       condition="O", checkpoint=0 if f["representation"] == "R0" else 5000,
                       hook=HOOK, panel=f["panel"], uncertainty_kind=None if f["agreement"]
                       is not None else f["status"], parent_ids=parents) for f in flat]
    mrows += [MetricRow(run_id="CIRC_AUDIT", space=SPACE, metric_id=m, value=float(r[m]),
                        replicate=r["seed"], world="cylinder", condition="O", panel=r["panel"],
                        uncertainty_kind="in_sample_optimistic_bound" if m == "A_symbol_bound"
                        else None, parent_ids=parents)
              for r in rows for m in ("A_symbol_bound", "A_b1_angle", "A_b32_angle")]
    out = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root),
                                           LocalFSBackend(out_root / "store")),
                        producer_version=meta["producer_version"])
    meta["metric_records_id"] = out.save(
        MetricRecords(rows=tuple(mrows)), config={"stage": "CIRC_AUDIT", "protocol": PROTOCOL,
                                                  "protocol_doc_sha256":
                                                  meta["protocol_doc_sha256"]},
        parents=parents, seed_map={}, consumer=CONS)
    for name, obj in {"inputs.json": prov, "summary.json": summary, "run.json": meta}.items():
        (tables / name).write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")
    with open(tables / "panels.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(flat[0]))
        w.writeheader()
        w.writerows(flat)
    manifest = {f.name: _sha256(f) for f in sorted(tables.iterdir()) if f.name != "MANIFEST.json"}
    (tables / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="E4 circular-baseline audit (circ-audit-v1)")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--out-store", type=Path, required=True)
    ap.add_argument("--tables", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        summary = run_audit(args.repo, args.main_store, args.out_store, args.tables)
    except BudgetExceeded as exc:
        log.error("circ_audit: budget exceeded: %s", exc)
        return 2
    log.info("circ_audit: %s", json.dumps({k: summary[k] for k in
                                           ("reading", "n_runs_adding_beyond", "failures")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
