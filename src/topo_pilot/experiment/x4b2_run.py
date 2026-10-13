"""X4 Phase B2 run (protocol x4b2-v1): four fresh pools, one at a time, under the x4b-v1 screen.

``python -m topo_pilot.experiment.x4b2_run --main-store <artifacts> --out-store <dir>
--tables <dir> --phase-b-tables <X4_FEASIBILITY_OUTPUTS>``. The main store is read-only (listing
hash before and after); outputs are one MetricRecords and npz exports in an independent store.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import time
from pathlib import Path

import numpy as np

from topo_pilot.analysis import (
    hellinger,
    overall_verdict,
    practical_verdict,
    screen_pool,
    strict_verdict,
    tangent_audit,
)
from topo_pilot.contracts import (
    ArtifactStore,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
    ObservationSet,
)

from .config import load_config, producer_version
from .x4b import (
    SHARED,
    ReadThroughBackend,
    canonical_tokens,
    future_maps,
    index_tokens,
    map_failures,
    pool_checks,
    pool_failures,
    provenance_row,
    resolve_inputs,
)
from .x4b2 import (
    PROTOCOL_VERSION,
    ROLES,
    TEST_ROLE,
    ambient_match,
    beliefs_p32,
    build_b2_pool,
    sample_pool,
    sequence_ids,
    stored_sequence_ids,
    windows,
)
from .x4b_audit import pool_audit, screen
from .x4b_run import (
    Budget,
    BudgetExceeded,
    _ambient_json,
    _load_process,
    _sha256,
    listing_hash,
    peak_memory_bytes,
)

log = logging.getLogger(__name__)
PROTOCOL_DOC = "docs/proposals/X4B2_COVERAGE_PROTOCOL.md"
CODE_NOTES = {"zero_map_guard": "analysis.tangent_audit (5b2f384), inert for this process",
              "memory_query_fix": "experiment.x4b_run.peak_memory_bytes (741333c)"}


def _float32_check(res: dict, pool) -> dict:
    """Q2 distances from float32-cast Q2 for the same pairs; flips and status."""
    part, ref = res["partners"], res["screen"]
    q2 = pool.Q2.astype(np.float32).astype(np.float64)
    d2 = np.full(part.idx.shape, np.nan)
    rr, cc = np.nonzero(part.idx >= 0)
    d2[rr, cc] = hellinger(q2[res["anchors"][rr]], q2[part.idx[rr, cc]])
    s = screen_pool(part.d1, d2)
    return {"float32_status": s.status, "float32_witness_flips": int(np.sum(s.witness !=
                                                                           ref.witness)),
            "float32_max_d2_diff": float(np.nanmax(np.abs(d2 - ref.d2)))}


def _permutation_check(res: dict, pool, proc: dict, seed: int = 1729) -> dict:
    """Reference pool recomputed in replicate ``seed``'s vocabulary; must screen identically."""
    emis = proc["emis"][seed]
    perm = np.asarray(emis.symbol_perm)
    run_tok = perm[pool.canonical]
    b_run = beliefs_p32(proc["T"], emis.E, proc["pi"], run_tok)
    maps = future_maps(proc["T"], emis.E)
    p_run, s_run = screen(pool, b_run @ maps.G1, b_run @ maps.G2, run_tok[:, -1],
                          res["anchors"])
    return {"seed": seed, "b32_diff": float(np.max(np.abs(b_run - pool.b32))),
            "partners_identical": bool(np.array_equal(p_run.idx, res["partners"].idx)),
            "flags_identical": bool(np.array_equal(s_run.eligible, res["screen"].eligible)
                                    and np.array_equal(s_run.witness, res["screen"].witness)),
            "max_d1_diff": float(np.nanmax(np.abs(p_run.d1 - res["partners"].d1))),
            "max_d2_diff": float(np.nanmax(np.abs(s_run.d2 - res["screen"].d2)))}


def _old_windows(main: ArtifactStore, inputs: dict, proc: dict) -> dict:
    """Canonical 32-symbol windows of the old cylinder-O test, dev and train splits."""
    out = {}
    for split, idx_key in (("test", "history_index"), ("dev", "dev_index")):
        arrs = []
        for s in inputs:
            _, tok = index_tokens(main, inputs[s][idx_key], inputs[s][f"obs_{split}"])
            arrs.append(canonical_tokens(tok, proc["emis"][s].symbol_perm))
            if split == "test":
                break  # shared test trajectories (D-019)
        out[split] = windows(np.vstack(arrs))
    train = [canonical_tokens(np.asarray(main.load(ObservationSet, inputs[s]["obs_train"],
                                                   consumer="experiment").tokens[:, :32]),
                              proc["emis"][s].symbol_perm) for s in inputs]
    out["train"] = windows(np.vstack(train))
    return out


def _one_pool(role: str, proc: dict, maps, budget: Budget, out: Path) -> tuple[dict, list]:
    tokens, lineage = sample_pool(role, proc["T"], proc["E_canon"], proc["pi"])
    seq = sequence_ids(role, tokens.shape[0])
    path = out / f"pool_{role}_tokens.npz"
    np.savez(path, canonical_tokens=tokens, sequence_id=seq)
    lineage["tokens_export_sha256"] = _sha256(path)
    pool = build_b2_pool(role, tokens, seq, proc["T"], proc["E_canon"], proc["pi"], maps)
    chk = pool_checks(pool, 36)
    fails = [f"pool[{role}]:{c}" for c in pool_failures(chk)]
    res = pool_audit(pool)
    f32 = _float32_check(res, pool)
    if f32["float32_status"] != res["screen"].status:
        fails.append(f"float32_status_change[{role}]")
    perm = _permutation_check(res, pool, proc) if role == TEST_ROLE else None
    if perm and not (perm["b32_diff"] <= 1e-12 and perm["partners_identical"]
                     and perm["flags_identical"]):
        fails.append("permutation[reference]")
    rpath = out / f"pool_{role}_screen.npz"
    np.savez(rpath, b32=pool.b32, Q1=pool.Q1, anchors=res["anchors"],
             partner_idx=res["partners"].idx, d1=res["partners"].d1, d2=res["screen"].d2,
             eligible=res["screen"].eligible, witness=res["screen"].witness)
    lineage["screen_export_sha256"] = _sha256(rpath)
    budget.check(role)
    return {"lineage": lineage, "checks": chk, "float32": f32, "permutation": perm,
            "summary": res["summary"], "unrestricted": res["unrestricted"],
            "table": res["table"], "seq": seq, "windows": windows(pool.canonical)}, fails


def run_b2(repo: Path, main_root: Path, out_root: Path, tables: Path, b_tables: Path) -> dict:
    """Run x4b2-v1 once; write tables and exports; return the verdict summary."""
    budget, failures = Budget(), []
    before = listing_hash(main_root)
    main = ArtifactStore(LocalFSBackend(main_root))
    inputs = resolve_inputs(load_config(repo / "configs" / "stages.yaml", repo), main)
    proc = _load_process(main, inputs)
    if proc["checks"]["E_canon_max_diff"] != 0.0 or proc["checks"]["pi_stationarity"] > 1e-12:
        failures.append("process_identity")
    maps = future_maps(proc["T"], proc["E_canon"])
    failures += [f"maps:{c}" for c in map_failures(maps)]
    ambient = tangent_audit(maps.G1, maps.G2)
    b_amb = json.loads((b_tables / "ambient.json").read_text(encoding="utf-8"))["canonical"]
    link = ambient_match(ambient, b_amb)
    if not link["ok"]:
        failures.append("ambient_link")
    budget.check("ambient")
    old_ids = stored_sequence_ids(main)
    old_win = _old_windows(main, inputs, proc)
    budget.check("old_data")
    exports = out_root / "exports"
    exports.mkdir(parents=True, exist_ok=True)
    pools = {}
    for role in ROLES:
        pools[role], fails = _one_pool(role, proc, maps, budget, exports)
        failures += fails
    sep = _separation(pools, old_ids, old_win)
    failures += sep.pop("failures")
    statuses = {r: p["summary"]["status"] for r, p in pools.items()}
    practical, p_reason = practical_verdict(statuses, test_pool=TEST_ROLE)
    overall, o_reason = overall_verdict(ambient.verdict, ambient.factor_conditioned, practical,
                                        not failures)
    after = listing_hash(main_root)
    if after != before:
        failures.append("main_store_changed")
        overall, o_reason = "INCONCLUSIVE", "main store changed during the run"
    summary = {"protocol": PROTOCOL_VERSION, "verdicts": {
        "ambient": f"{ambient.verdict} (inherited from Phase B, recomputation matched)"
        if link["ok"] else ambient.verdict, "practical": practical,
        "strict": strict_verdict(ambient.verdict), "overall": overall},
        "reasons": {"practical": p_reason, "overall": o_reason}, "pool_status": statuses,
        "failures": failures}
    _export(repo, main_root, out_root, tables, b_tables, main, inputs, proc, maps, ambient, link,
            pools, sep, summary, budget, before, after)
    return summary


def _separation(pools: dict, old_ids: np.ndarray, old_win: dict) -> dict:
    out: dict = {"failures": [], "n_stored_sequence_ids": int(old_ids.size)}
    roles = list(pools)
    for i, a in enumerate(roles):
        n_old = int(np.intersect1d(pools[a]["seq"], old_ids).size)
        out[f"{a}:ids_shared_with_store"] = n_old
        if n_old:
            out["failures"].append(f"separation:{a}:store")
        for split, win in old_win.items():
            out[f"{a}:identical_windows_with_old_{split}"] = int(
                np.intersect1d(pools[a]["windows"], win).size)
        for b in roles[i + 1:]:
            n_ab = int(np.intersect1d(pools[a]["seq"], pools[b]["seq"]).size)
            out[f"{a}~{b}:ids_shared"] = n_ab
            out[f"{a}~{b}:identical_windows"] = int(
                np.intersect1d(pools[a]["windows"], pools[b]["windows"]).size)
            if n_ab:
                out["failures"].append(f"separation:{a}~{b}")
        out[f"{a}:distinct_windows"] = int(pools[a]["windows"].size)
    return out


def _export(repo, main_root, out_root, tables, b_tables, main, inputs, proc, maps, ambient, link,
            pools, sep, summary, budget, before, after) -> None:
    tables.mkdir(parents=True, exist_ok=True)
    prov = [provenance_row(main, SHARED["world"], "world"),
            provenance_row(main, SHARED["transition"], "transition")]
    prov += [provenance_row(main, inputs[s]["emission"], f"emission[{s}]") for s in inputs]
    parents = tuple(sorted(r["artifact_id"] for r in prov))
    b_run = json.loads((b_tables / "run.json").read_text(encoding="utf-8"))
    meta = {"protocol": PROTOCOL_VERSION, "protocol_doc_sha256": _sha256(repo / PROTOCOL_DOC),
            "producer_version": producer_version(repo), "code_notes": CODE_NOTES,
            "phase_b_link": {"metric_records_id": b_run["metric_records_id"],
                             "ambient_json_sha256": _sha256(b_tables / "ambient.json")},
            "cpu_s": round(time.process_time() - budget.t0, 2),
            "wall_s": round(time.time() - budget.w0, 2), "cpu_cap_s": budget.cap,
            "peak_memory_bytes": peak_memory_bytes(), "budget_steps": budget.steps,
            "main_store_listing_before": before, "main_store_listing_after": after,
            "lineage": {r: p["lineage"] for r, p in pools.items()}}
    rows = [MetricRow(run_id="X4B2", space=f"x4b2:pool:{r}", metric_id=m,
                      value=None if p["summary"][m] is None else float(p["summary"][m]),
                      status="ok" if p["summary"][m] is not None else "inconclusive",
                      world="cylinder", condition="O", parent_ids=parents)
            for r, p in pools.items() for m in ("n_eligible", "n_witness", "witness_fraction",
                                                "max_d2_admissible")]
    rows += [MetricRow(run_id="X4B2", space="x4b2:verdict", metric_id=f"{k}={v}", value=1.0,
                       world="cylinder", condition="O", parent_ids=parents)
             for k, v in summary["verdicts"].items()]
    store = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root),
                                             LocalFSBackend(out_root / "store")),
                          producer_version=meta["producer_version"])
    meta["metric_records_id"] = store.save(
        MetricRecords(rows=tuple(rows)),
        config={"stage": "X4B2", "kind": "x4_phase_b2", "protocol": PROTOCOL_VERSION,
                "protocol_doc_sha256": meta["protocol_doc_sha256"],
                "lineage": meta["lineage"], "phase_b_link": meta["phase_b_link"]},
        parents=parents, seed_map={p["lineage"]["stream"]: p["lineage"]["seed"]
                                   for p in pools.values()}, consumer="experiment")
    files = {"inputs.json": prov, "process_and_map_checks.json": {**proc["checks"],
                                                                  "maps": maps.checks},
             "ambient.json": {"recomputed": _ambient_json(ambient), "phase_b_link": link},
             "separation.json": sep,
             "pools.json": {r: {"primary": p["summary"], "unrestricted": p["unrestricted"],
                                "checks": p["checks"], "float32": p["float32"],
                                "permutation": p["permutation"], "lineage": p["lineage"]}
                            for r, p in pools.items()},
             "run.json": meta, "verdicts.json": summary}
    for name, obj in files.items():
        (tables / name).write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")
    for r, p in pools.items():
        with open(tables / f"anchors_{r}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(p["table"][0]))
            w.writeheader()
            w.writerows(p["table"])
    manifest = {f.name: _sha256(f) for f in sorted(tables.iterdir()) if f.name != "MANIFEST.json"}
    (tables / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X4 Phase B2 coverage extension (x4b2-v1)")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--out-store", type=Path, required=True)
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--phase-b-tables", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        summary = run_b2(args.repo, args.main_store, args.out_store, args.tables,
                         args.phase_b_tables)
    except BudgetExceeded as exc:
        args.tables.mkdir(parents=True, exist_ok=True)
        (args.tables / "verdicts.json").write_text(json.dumps(
            {"verdicts": {"overall": "INCONCLUSIVE"}, "reasons": {"overall": f"budget: {exc}"}}),
            encoding="utf-8")
        log.error("x4b2: budget exceeded: %s", exc)
        return 2
    log.info("x4b2: %s", json.dumps(summary["verdicts"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
