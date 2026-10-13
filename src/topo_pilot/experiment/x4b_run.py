"""X4 Phase B run (M7): orchestrate protocol x4b-v1, enforce the budget, export outputs.

``python -m topo_pilot.experiment.x4b_run --main-store <artifacts> --out-store <dir>
--tables <dir>``. The main store is read-only (its file listing is hashed before and after);
outputs are one MetricRecords plus npz exports in the independent store, and JSON/CSV tables.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import json
import logging
import os
import time
from pathlib import Path

import numpy as np

from topo_pilot.analysis import overall_verdict, practical_verdict, strict_verdict, tangent_audit
from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
    OracleOutputs,
    ProcessDiagnostics,
    TransitionSpec,
)
from topo_pilot.oracle import BayesFilter

from .config import load_config, producer_version
from .x4b import (
    END,
    PROTOCOL_VERSION,
    S7_RECORDS,
    SEEDS,
    SHARED,
    ReadThroughBackend,
    build_pool,
    future_maps,
    index_tokens,
    map_failures,
    pool_checks,
    pool_failures,
    provenance_row,
    resolve_inputs,
)
from .x4b_audit import agreement_check, agreement_failures, pool_audit

log = logging.getLogger(__name__)
CPU_CAP_S = 3600.0
PROTOCOL_DOC = "docs/proposals/X4_FEASIBILITY_PROTOCOL.md"


class BudgetExceeded(RuntimeError):
    """The 1 CPU-hour cap of protocol §9 was reached."""


def peak_memory_bytes() -> int | None:
    """Peak working set of this process (Windows) or max RSS (POSIX); None if unavailable."""
    try:
        if os.name == "nt":
            class _PMC(ctypes.Structure):
                _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
                            ("PeakWorkingSetSize", ctypes.c_size_t),
                            ("WorkingSetSize", ctypes.c_size_t)] + [
                    (n, ctypes.c_size_t) for n in ("QPPPU", "QPPU", "QPNPPU", "QNPPU",
                                                   "PagefileUsage", "PeakPagefileUsage")]
            pmc = _PMC()
            pmc.cb = ctypes.sizeof(_PMC)
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb)
            return int(pmc.PeakWorkingSetSize)
        import resource
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024
    except (OSError, AttributeError, ImportError):
        return None


def listing_hash(root: Path) -> tuple[str, int]:
    """sha256 over sorted (relative path, size, mtime_ns) of every file under ``root``."""
    entries = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            st = os.stat(os.path.join(dirpath, f))
            rel = os.path.relpath(os.path.join(dirpath, f), root).replace(os.sep, "/")
            entries.append(f"{rel}|{st.st_size}|{st.st_mtime_ns}")
    entries.sort()
    return hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest(), len(entries)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Budget:
    """Process CPU time since construction, checked between steps."""

    def __init__(self, cap_s: float = CPU_CAP_S) -> None:
        self.cap, self.t0, self.w0, self.steps = cap_s, time.process_time(), time.time(), []

    def check(self, step: str) -> None:
        used = time.process_time() - self.t0
        self.steps.append({"step": step, "cpu_s": round(used, 3),
                           "wall_s": round(time.time() - self.w0, 3)})
        log.info("x4b: %s done (cpu %.1f s)", step, used)
        if used > self.cap:
            raise BudgetExceeded(f"{used:.0f} CPU s after {step}")


def _ambient_json(audit) -> dict:
    return {"verdict": audit.verdict, "factor_conditioned": audit.factor_conditioned,
            "certificate": audit.certificate, "certificate_ratio": audit.certificate_ratio,
            "basis_orthonormality": audit.basis_orthonormality, "basis_sum": audit.basis_sum,
            "H_singular_values": list(audit.H_singular_values),
            "G2_singular_values": list(audit.G2_singular_values),
            "rows": [{**r.__dict__, "D_singular_values": list(r.D_singular_values)}
                     for r in audit.rows]}


def _load_process(main: ArtifactStore, inputs: dict) -> dict:
    trans = main.load(TransitionSpec, SHARED["transition"], consumer="experiment")
    emis = {s: main.load(EmissionSpec, inputs[s]["emission"], consumer="experiment")
            for s in SEEDS}
    canon = {s: np.asarray(emis[s].E)[:, np.asarray(emis[s].symbol_perm)] for s in SEEDS}
    canon_diff = max(float(np.max(np.abs(canon[s] - canon[SEEDS[0]]))) for s in SEEDS)
    stat = float(np.max(np.abs(trans.pi @ trans.T - trans.pi)))
    return {"T": np.asarray(trans.T), "pi": np.asarray(trans.pi), "emis": emis,
            "E_canon": canon[SEEDS[0]], "checks": {"E_canon_max_diff": canon_diff,
                                                   "pi_stationarity": stat}}


def _maps_section(main: ArtifactStore, inputs: dict, proc: dict) -> tuple[dict, dict, list]:
    maps = {"canonical": future_maps(proc["T"], proc["E_canon"])}
    maps.update({s: future_maps(proc["T"], proc["emis"][s].E) for s in SEEDS})
    fails = [f"maps[{k}]:{c}" for k, m in maps.items() for c in map_failures(m)]
    diag_rows = {}
    for s in SEEDS:
        stored = main.load(ProcessDiagnostics, inputs[s]["diagnostics"], consumer="experiment")
        rel = [float(np.max(np.abs(np.asarray(stored.O_singular_values[k]) - maps[s]
                                   .O_singular_values[k]) / max(maps[s].O_singular_values[k][0],
                                                                1e-300))) for k in (0, 1)]
        perm = np.asarray(proc["emis"][s].symbol_perm)
        g1p = float(np.max(np.abs(maps[s].G1[:, perm] - maps["canonical"].G1)))
        g2p = float(np.max(np.abs(maps[s].G2.reshape(-1, 36, 36)[:, perm][:, :, perm]
                                  .reshape(-1, 1296) - maps["canonical"].G2)))
        diag_rows[s] = {"stored_O1_rel_diff": rel[0], "stored_O2_rel_diff": rel[1],
                        "G1_perm_diff": g1p, "G2_perm_diff": g2p}
        fails += [f"diag[{s}]:{k}" for k, v in diag_rows[s].items()
                  if not v <= (1e-10 if "stored" in k else 1e-14)]
    checks = {k: m.checks for k, m in maps.items()}
    return maps, {"maps": checks, "diagnostics_and_permutation": diag_rows}, fails


def _pools(main: ArtifactStore, inputs: dict, proc: dict, maps: dict) -> tuple[dict, dict]:
    runs_test, toks = [], {}
    for s in SEEDS:
        idx, tok = index_tokens(main, inputs[s]["history_index"], inputs[s]["obs_test"])
        runs_test.append((s, idx, tok, np.asarray(proc["emis"][s].symbol_perm)))
        toks[s] = (idx, tok)
    args = (proc["T"], proc["E_canon"], proc["pi"], maps["canonical"])
    pools = {"test": build_pool("test", "test", runs_test, *args)}
    for s in SEEDS:
        idx, tok = index_tokens(main, inputs[s]["dev_index"], inputs[s]["obs_dev"])
        pools[f"dev{s}"] = build_pool(f"dev{s}", "dev", [(s, idx, tok, np.asarray(
            proc["emis"][s].symbol_perm))], *args)
    return pools, toks


def _metric_rows(ambient, results: dict, verdicts: dict, parents: tuple) -> list[MetricRow]:
    rows = []
    for r in ambient.rows:
        for m, v in (("rank_H", r.rank_H), ("null_dim", r.null_dim), ("rho", r.rho),
                     ("rank_G2", r.rank_G2), ("amplification", r.amplification)):
            rows.append(MetricRow(run_id="X4B", space=f"x4b:ambient:tau={r.tau:g}",
                                  metric_id=m, value=float(v), world="cylinder", condition="O",
                                  parent_ids=parents))
    for name, res in results.items():
        s = res["summary"]
        for m in ("n_eligible", "n_witness", "witness_fraction", "max_d2_admissible"):
            v = s[m]
            rows.append(MetricRow(run_id="X4B", space=f"x4b:pool:{name}", metric_id=m,
                                  value=None if v is None else float(v),
                                  status="ok" if v is not None else "inconclusive",
                                  world="cylinder", condition="O", parent_ids=parents))
    for k, v in verdicts.items():
        rows.append(MetricRow(run_id="X4B", space="x4b:verdict", metric_id=f"{k}={v}",
                              value=1.0, world="cylinder", condition="O", parent_ids=parents))
    return rows


def run_phase_b(repo_root: Path, main_root: Path, out_root: Path, tables: Path) -> dict:
    """Run protocol x4b-v1 once; write tables/exports; return the verdict summary."""
    budget, failures = Budget(), []
    before = listing_hash(main_root)
    cfg = load_config(repo_root / "configs" / "stages.yaml", repo_root)
    main = ArtifactStore(LocalFSBackend(main_root))
    inputs = resolve_inputs(cfg, main)
    proc = _load_process(main, inputs)
    if proc["checks"]["E_canon_max_diff"] != 0.0 or proc["checks"]["pi_stationarity"] > 1e-12:
        failures.append("process_inputs")
    budget.check("inputs")
    maps, map_checks, fails = _maps_section(main, inputs, proc)
    failures += fails
    ambient = tangent_audit(maps["canonical"].G1, maps["canonical"].G2)
    amb_runs = {s: tangent_audit(maps[s].G1, maps[s].G2) for s in SEEDS}
    for s, a in amb_runs.items():
        if a.verdict != ambient.verdict or not np.allclose(
                a.H_singular_values, ambient.H_singular_values, rtol=1e-10, atol=1e-14):
            failures.append(f"ambient_permutation[{s}]")
    budget.check("ambient")
    pools, toks = _pools(main, inputs, proc, maps)
    pool_chk = {n: pool_checks(p, 36) for n, p in pools.items()}
    failures += [f"pool[{n}]:{c}" for n, ch in pool_chk.items() for c in pool_failures(ch)]
    budget.check("pools")
    results = {n: pool_audit(p) for n, p in pools.items()}
    budget.check("audit")
    agreement = {}
    test = pools["test"]
    for s in SEEDS:
        idx, tok = toks[s]
        pos = {int(q): i for i, q in enumerate(idx.sequence_id.tolist())}
        tok_pool = tok[[pos[int(q)] for q in test.sequence_id.tolist()]]
        b_run = BayesFilter(proc["T"], proc["emis"][s].E, proc["pi"]).run(tok_pool).b[:, END - 1]
        oracle = main.load(OracleOutputs, inputs[s]["oracle"], consumer="experiment")
        agreement[s] = agreement_check(test, results["test"], s, tok_pool, oracle, maps[s],
                                      np.asarray(proc["emis"][s].symbol_perm), b_run)
        failures += [f"agreement[{s}]:{c}" for c in
                     agreement_failures(agreement[s], results["test"]["screen"].status)]
    budget.check("agreement")
    statuses = {n: r["screen"].status for n, r in results.items()}
    practical, p_reason = practical_verdict(statuses)
    overall, o_reason = overall_verdict(ambient.verdict, ambient.factor_conditioned, practical,
                                        not failures)
    verdicts = {"ambient": ambient.verdict, "practical": practical,
                "strict": strict_verdict(ambient.verdict), "overall": overall}
    after = listing_hash(main_root)
    if after != before:
        failures.append("main_store_changed")
        verdicts["overall"], o_reason = "INCONCLUSIVE", "main store changed during the run"
    summary = {"protocol": PROTOCOL_VERSION, "verdicts": verdicts,
               "reasons": {"practical": p_reason, "overall": o_reason},
               "pool_status": statuses, "failures": failures}
    _export(repo_root, main_root, out_root, tables, inputs, main, proc, map_checks, ambient,
            amb_runs, pool_chk, results, agreement, pools, summary, budget, before, after)
    return summary


def _export(repo_root, main_root, out_root, tables, inputs, main, proc, map_checks, ambient,
            amb_runs, pool_chk, results, agreement, pools, summary, budget, before, after):
    tables.mkdir(parents=True, exist_ok=True)
    exports = out_root / "exports"
    exports.mkdir(parents=True, exist_ok=True)
    prov = [provenance_row(main, SHARED["world"], "world"),
            provenance_row(main, SHARED["transition"], "transition")]
    for s in SEEDS:
        prov += [provenance_row(main, inputs[s][k], f"{k}[{s}]") for k in
                 ("emission", "obs_test", "history_index", "oracle", "diagnostics", "obs_dev",
                  "dev_index")]
    prov += [provenance_row(main, v, f"S7:{k}") for k, v in S7_RECORDS.items()]
    parents = tuple(sorted({r["artifact_id"] for r in prov}))
    npz_files = {}
    for name, pool in pools.items():
        r = results[name]
        path = exports / f"pool_{name}.npz"
        np.savez(path, canonical_ids=np.array(pool.canonical_ids), b32=pool.b32, Q1=pool.Q1,
                 anchors=r["anchors"], partner_idx=r["partners"].idx, d1=r["partners"].d1,
                 d2=r["screen"].d2, eligible=r["screen"].eligible, witness=r["screen"].witness)
        npz_files[path.name] = _sha256(path)
    cpu = time.process_time() - budget.t0
    meta = {"protocol": PROTOCOL_VERSION, "protocol_doc_sha256": _sha256(repo_root /
                                                                         PROTOCOL_DOC),
            "producer_version": producer_version(repo_root),
            "source_commit": "f8afc2a5e43309aa4bf2d402f2be4e38470df180",
            "cpu_s": round(cpu, 2), "wall_s": round(time.time() - budget.w0, 2),
            "cpu_cap_s": CPU_CAP_S, "peak_memory_bytes": peak_memory_bytes(),
            "budget_steps": budget.steps, "main_store_listing_before": before,
            "main_store_listing_after": after, "exports_sha256": npz_files}
    store = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root),
                                             LocalFSBackend(out_root / "store")),
                          producer_version=meta["producer_version"])
    rec = MetricRecords(rows=tuple(_metric_rows(ambient, results, summary["verdicts"], parents)))
    meta["metric_records_id"] = store.save(
        rec, config={"stage": "X4B", "kind": "x4_phase_b", "protocol": PROTOCOL_VERSION,
                     "protocol_doc_sha256": meta["protocol_doc_sha256"],
                     "exports_sha256": npz_files}, parents=parents, seed_map={},
        consumer="experiment")
    files = {"inputs.json": prov, "process_and_map_checks.json": {**proc["checks"],
                                                                  **map_checks},
             "ambient.json": {"canonical": _ambient_json(ambient),
                              "per_run_verdicts": {s: a.verdict for s, a in amb_runs.items()}},
             "pool_checks.json": pool_chk,
             "pools.json": {n: {"primary": r["summary"], "unrestricted": r["unrestricted"]}
                            for n, r in results.items()},
             "test_agreement.json": agreement, "run.json": meta, "verdicts.json": summary}
    for name, obj in files.items():
        (tables / name).write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")
    for name, r in results.items():
        with open(tables / f"anchors_{name}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(r["table"][0]))
            w.writeheader()
            w.writerows(r["table"])
    manifest = {p.name: _sha256(p) for p in sorted(tables.iterdir()) if p.name != "MANIFEST.json"}
    (tables / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X4 Phase B feasibility audit (protocol x4b-v1)")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--out-store", type=Path, required=True)
    ap.add_argument("--tables", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        summary = run_phase_b(args.repo, args.main_store, args.out_store, args.tables)
    except BudgetExceeded as exc:
        args.tables.mkdir(parents=True, exist_ok=True)
        (args.tables / "verdicts.json").write_text(json.dumps(
            {"verdicts": {"overall": "INCONCLUSIVE"}, "reasons": {"overall": f"budget: {exc}"}}),
            encoding="utf-8")
        log.error("x4b: budget exceeded: %s", exc)
        return 2
    log.info("x4b: %s", json.dumps(summary["verdicts"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
