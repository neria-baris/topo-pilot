"""X5 G1 deterministic post-hoc verification (job 0007) of the SAME saved calibration pools.

No sampling and no rerun of the gate driver: loads the immutable calibration ObservationSets and
transitions, recomputes every reported quantity with the frozen kernels/streams, exports full
arrays to a new immutable output version and compares against job 0006's result (tolerance
1e-12 absolute). Not an independent replication. ``python -m topo_pilot.experiment.x5g1_verify
--repo . --main-store <artifacts> --x5-store <dir> --out <dir> --mailbox <dir>``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

from topo_pilot.analysis import (
    integrated_autocorrelation,
    movement_rate,
    percentile_interval,
    rate_matched_kernel,
    spectrum_report,
)
from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    ObservationSet,
    SeedTree,
    TransitionSpec,
    WorldSpec,
)
from topo_pilot.oracle import FutureOperator
from topo_pilot.process import ConductanceConfig, conductance_kernel

from .config import producer_version
from .x4b import ReadThroughBackend
from .x4b_run import peak_memory_bytes
from .x5g1_controls import RunControls
from .x5g1_oracle import bootstrap_means, gate_quantities
from .x5g1_run import PARENTS_FULL, diagnostics, kernel_validity
from .x5g1_safety import checked_computation, ensure_new_output_dir, guarded_export

log = logging.getLogger(__name__)
TOL = 1e-12
OLD_RESULT = "docs/proposals/X5_G1_FEASIBILITY_OUTPUTS/result.json"
OLD_RESULT_SHA = "5962cb5c2f4994cd9d4318dacb7e155d1be34ebaee9a5a79a73a902db327bddf"
T_A020, OBS = "08a22a03727d2295", {"a0": "eb3170a226f03bd0", "a020": "e574367fd00ccf02"}
SOURCES = {**PARENTS_FULL,
           T_A020: (TransitionSpec,
                    "663d0011c7f9b541a436359c885a9f367dda280b20b594e484ff1492b8686b7b"),
           OBS["a0"]: (ObservationSet,
                       "cd7ac874a89bf46e80ccc7f2424a25862e56de4783b43982bd81ce51276622ac"),
           OBS["a020"]: (ObservationSet,
                         "a5bba39669225d766b061dcce2f6219f7e32306caeaa17ef99fb28cd25e37de3")}
FIRST_STAGE_CAP_S, CUMULATIVE_CAP_S = 3600.0, 21600.0


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compute(store: ArtifactStore, g) -> dict:
    """Recompute all reported quantities from the saved pools (no sampling)."""
    world = store.load(WorldSpec, "21feee1d8ee5422e", consumer="experiment")
    emis = store.load(EmissionSpec, "3633ac27dab50cf4", consumer="experiment")
    E, perm = np.asarray(emis.E, float), np.asarray(emis.symbol_perm)
    T = {"a0": store.load(TransitionSpec, "e4dafc7b9785c172", consumer="experiment"),
         "a020": store.load(TransitionSpec, T_A020, consumer="experiment")}
    pi = np.asarray(T["a0"].pi, float)
    Tm = {k: np.asarray(v.T, float) for k, v in T.items()}
    recon, meta = conductance_kernel(world, ConductanceConfig())
    coords = np.asarray(world.coords, float)
    e = np.asarray(world.edges, dtype=np.int64)
    l_h = np.asarray(meta["l_h"])
    same_y = coords[e[:, 0], 1] == coords[e[:, 1], 1]
    c = np.zeros_like(Tm["a0"])
    w = np.where(same_y, 1.0 / l_h[coords[e[:, 0], 1].astype(int)] ** 2, 1.0)
    c[e[:, 0], e[:, 1]] = w
    c[e[:, 1], e[:, 0]] = w
    out = {"arrays": {"T_a0": Tm["a0"], "T_a020": Tm["a020"], "pi": pi, "E": E, "perm": perm,
                      "f_y": np.asarray(meta["f_y"]), "l_h": l_h,
                      "conductance_reconstructed": c}, "summary": {}}
    s = out["summary"]
    s["a020_reconstruction_max_diff"] = float(np.max(np.abs(np.asarray(recon.T) - Tm["a020"])))
    s["T_a020_meta"] = meta
    g("kernels")
    alpha = movement_rate(Tm["a020"], pi) / movement_rate(Tm["a0"], pi)
    T_alpha, a_status = rate_matched_kernel(Tm["a0"], alpha)
    kernels = {"a0": Tm["a0"], "a020": Tm["a020"]}
    if T_alpha is not None:
        kernels["rate_matched"] = T_alpha
        out["arrays"]["T_rate_matched"] = T_alpha
    s["rate_matched"] = {"alpha": alpha, "status": a_status}
    for name, K in kernels.items():
        sp = spectrum_report(K, pi)
        out["arrays"][f"spectrum_{name}"] = sp.eigenvalues
        s[f"diagnostics_{name}"] = diagnostics(K, pi, world, E)
        s[f"iat_g_w_all_{name}"] = [list(integrated_autocorrelation(K, pi, E[:, j]))
                                    for j in range(E.shape[1])]
        if name != "rate_matched":
            s[f"validity_{name}"] = kernel_validity(K, pi, world, E)
            sv = FutureOperator(K, E).observability_singular_values(2)
            out["arrays"][f"O1_sv_{name}"], out["arrays"][f"O2_sv_{name}"] = sv
        g(f"diagnostics {name}")
    kl = {}
    for arm in ("a0", "a020"):
        obs = store.load(ObservationSet, OBS[arm], consumer="experiment")
        q = gate_quantities(Tm[arm], E, pi, np.asarray(obs.tokens), guard=g)
        kl[arm] = q["kl_last"]
        out["arrays"][f"seq_{arm}"] = np.asarray(obs.sequence_id)
        for k in ("kl_last", "kl_stationary", "kl_two", "position_entropy"):
            out["arrays"][f"{k}_{arm}"] = q[k]
        boots = bootstrap_means(q["kl_last"], SeedTree(0).generator("x5g1-v1", "gc_bootstrap",
                                                                   arm), guard=g)
        out["arrays"][f"bootstrap_means_{arm}"] = boots
        s[arm] = {"valid": q["valid"], "GC": float(np.mean(q["kl_last"])),
                  "GC_ci95": list(percentile_interval(boots)),
                  "GC_stationary": float(np.mean(q["kl_stationary"])),
                  "two_token_regret": float(np.mean(q["kl_two"])),
                  "position_entropy": q["position_entropy"].tolist(),
                  "paired_first_symbol_equal": None}
    rng = SeedTree(0).generator("x5g1-v1", "gc_bootstrap_paired")
    n = kl["a0"].size
    diffs = np.empty(2000)
    for start in range(0, 2000, 500):
        g(f"paired {start}")
        for j in range(start, start + 500):
            idx = rng.integers(0, n, n)
            diffs[j] = kl["a020"][idx].mean() - kl["a0"][idx].mean()
    out["arrays"]["bootstrap_paired_diff"] = diffs
    s["paired_diff_ci95"] = list(percentile_interval(diffs))
    return out


def _pairs(old: dict, new: dict) -> list[tuple[str, object, object]]:
    """(name, old, new) for every reported quantity of job 0006 that is recomputed here."""
    s = new["summary"]
    rows = [("a0_equivalence_max_diff", old["a0_equivalence_max_diff"], 0.0),
            ("paired_diff_ci95", old["paired_diff_ci95"], s["paired_diff_ci95"]),
            ("rate_matched.alpha", old["rate_matched"]["alpha"], s["rate_matched"]["alpha"]),
            ("T_a020.C_max", old["T_a020_meta"]["C_max"], s["T_a020_meta"]["C_max"]),
            ("T_a020.l_h", old["T_a020_meta"]["l_h"], s["T_a020_meta"]["l_h"]),
            ("T_a020.f_y", old["T_a020_meta"]["f_y"], s["T_a020_meta"]["f_y"])]
    if "diagnostics" in old["rate_matched"]:
        rows.append(("rate_matched.diagnostics", old["rate_matched"]["diagnostics"],
                     s["diagnostics_rate_matched"]))
    for arm in ("a0", "a020"):
        o, n = old["arms"][arm], s[arm]
        for k in ("GC", "GC_ci95", "GC_stationary", "two_token_regret", "position_entropy"):
            rows.append((f"{arm}.{k}", o[k], n[k]))
        rows.append((f"{arm}.validity", o["validity"], s[f"validity_{arm}"]))
        rows.append((f"{arm}.diagnostics", o["diagnostics"], s[f"diagnostics_{arm}"]))
        sv1, sv2 = new["arrays"][f"O1_sv_{arm}"], new["arrays"][f"O2_sv_{arm}"]
        rows.append((f"{arm}.O1", o["observability_sv"]["O1"], sv1.tolist()))
        rows.append((f"{arm}.O2_top10", o["observability_sv"]["O2_top10"], sv2[:10].tolist()))
        rows.append((f"{arm}.O2_rank", o["observability_sv"]["O2_rank_1e-10"],
                     int(np.sum(sv2 > 1e-10 * sv2[0]))))
    return rows


def _maxdiff(a, b) -> float:
    if isinstance(a, dict):
        if not isinstance(b, dict) or set(a) != set(b):
            return float("inf")
        return max([_maxdiff(a[k], b[k]) for k in a] + [0.0])
    if isinstance(a, (list, tuple)):
        if not isinstance(b, (list, tuple)) or len(a) != len(b):
            return float("inf")
        return max([_maxdiff(x, y) for x, y in zip(a, b)] + [0.0])
    if isinstance(a, bool) or a is None or isinstance(a, str):
        return 0.0 if a == b else float("inf")
    return abs(float(a) - float(b))


def compare(repo: Path, new: dict) -> dict:
    old_path = repo / OLD_RESULT
    if _sha(old_path) != OLD_RESULT_SHA:
        return {"status": "OLD_RESULT_HASH_MISMATCH", "items": []}
    old = json.loads(old_path.read_text(encoding="utf-8"))
    items = [{"name": n, "max_abs_diff": _maxdiff(o, v)} for n, o, v in _pairs(old, new)]
    bad = [i for i in items if not i["max_abs_diff"] <= TOL]
    return {"status": "CONSISTENT" if not bad else "DISCREPANCY", "tolerance": TOL,
            "items": items, "discrepancies": bad}


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


def run_verify(repo: Path, main_root: Path, x5_store: Path, out: Path, mailbox: Path) -> dict:
    ensure_new_output_dir(out)
    store = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root),
                                             LocalFSBackend(x5_store / "store")))
    ledger = x5_store / "cpu_ledger.json"
    prior = json.loads(ledger.read_text(encoding="utf-8"))["cumulative_cpu_s"]
    ctl = RunControls(ledger, FIRST_STAGE_CAP_S - prior, mailbox / "STOP", "0007-verify",
                      CUMULATIVE_CAP_S)
    with ctl:
        new = checked_computation(store, SOURCES, lambda: compute(store, ctl.guard))
        cmp = compare(repo, new)
        ctl.outcome = cmp["status"]
        meta = {"kind": "deterministic post-hoc verification of the same saved data; not an "
                        "independent replication", "producer_version": producer_version(repo),
                "python": sys.executable, "topo_pilot_file": __import__("topo_pilot").__file__,
                "numpy": np.__version__, "blas_threads": {k: os.environ.get(k) for k in (
                    "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS")},
                "sources_full_sha256": {k: v[1] for k, v in SOURCES.items()},
                "old_result_sha256": OLD_RESULT_SHA, "cpu_s_before_export": round(ctl.cpu(), 3),
                "cpu_prior_cumulative": prior, "peak_memory_bytes": peak_memory_bytes(),
                "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

        def arrays() -> None:
            np.savez(out / "verification_arrays.npz", **new["arrays"])

        def write(name: str, obj) -> None:
            (out / name).write_text(json.dumps(_jsonable(obj), indent=1), encoding="utf-8")

        def manifest() -> None:
            sums = {f.name: _sha(f) for f in sorted(out.iterdir()) if f.name != "MANIFEST.json"}
            (out / "MANIFEST.json").write_text(json.dumps(sums, indent=1), encoding="utf-8")

        guarded_export(ctl, [("arrays", arrays),
                             ("summary", lambda: write("summary.json", new["summary"])),
                             ("comparison", lambda: write("comparison.json", cmp)),
                             ("run", lambda: write("run.json", meta)),
                             ("manifest", manifest)], out / "EXPORT_STATUS.json")
    return cmp


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X5 G1 deterministic post-hoc verification")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--x5-store", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mailbox", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    cmp = run_verify(args.repo, args.main_store, args.x5_store, args.out, args.mailbox)
    log.info("x5g1 verify: %s (%d items, %d discrepancies)", cmp["status"], len(cmp["items"]),
             len(cmp.get("discrepancies", [])))
    return 0 if cmp["status"] == "CONSISTENT" else 3


if __name__ == "__main__":
    raise SystemExit(main())
