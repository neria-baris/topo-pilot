"""X5 G1 exact-process and calibration gate run (x5g1-feas-v2; handoff job 0006). No training.

``python -m topo_pilot.experiment.x5g1_run --main-store <artifacts> --out-store <dir>
--tables <dir> --mailbox <dir>``. Everything runs inside ``RunControls`` so the X5 ledger is
written on success, failure, STOP and budget stops, including the export.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

from topo_pilot.analysis import (
    context_status,
    integrated_autocorrelation,
    is_connected,
    movement_rate,
    percentile_interval,
    rate_matched_kernel,
    spectrum_report,
)
from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    SeedTree,
    TransitionSpec,
    WorldSpec,
)
from topo_pilot.oracle import FutureOperator
from topo_pilot.process import ConductanceConfig, ProcessStage, conductance_kernel

from .config import producer_version
from .x4b import ReadThroughBackend, provenance_row
from .x4b2 import ROLES as B2_ROLES
from .x4b2 import sequence_ids as b2_sequence_ids
from .x4b2 import stored_sequence_ids, windows
from .x4b_run import listing_hash
from .x5g1_controls import RunControls, verify_parents
from .x5g1_lineage import ARMS, STREAM, calibration_obs, paired_generators, sample_named
from .x5g1_lineage import sequence_ids as x5_sequence_ids
from .x5g1_oracle import bootstrap_means, gate_quantities

log = logging.getLogger(__name__)
PROTOCOL = "x5g1-feas-v2"
PROTOCOL_DOC = "docs/proposals/X5_G1_FEASIBILITY_PROTOCOL_V2.md"
PARENTS = {"21feee1d8ee5422e": "b6f0746e46d20d20", "e4dafc7b9785c172": "f94340a64769df1c",
           "3633ac27dab50cf4": "f5b6197c22e3613f"}
WORLD, T_FLAT, EMIS = "21feee1d8ee5422e", "e4dafc7b9785c172", "3633ac27dab50cf4"
CAP_S, CUMULATIVE_CAP_S = 3600.0, 21600.0


class GateFailed(RuntimeError):
    """A FAILED condition (integrity, state order, a0 equivalence, namespace collision)."""


def kernel_validity(T: np.ndarray, pi: np.ndarray, world: WorldSpec, E: np.ndarray) -> dict:
    """x5g1-feas-v2 §3.1 checks; ``ok`` iff all hold."""
    n = T.shape[0]
    allowed = np.eye(n, dtype=bool)
    e = np.asarray(world.edges, dtype=np.int64)
    allowed[e[:, 0], e[:, 1]] = allowed[e[:, 1], e[:, 0]] = True
    chk = {"row_sum_err": float(np.max(np.abs(T.sum(1) - 1))), "min_entry": float(T.min()),
           "asym": float(np.max(np.abs(T - T.T))), "min_diag": float(np.diag(T).min()),
           "support_ok": bool(not np.any((T > 0) & ~allowed)),
           "stationarity_err": float(np.max(np.abs(pi @ T - pi))),
           "connected": is_connected(T), "min_p_w": float((pi @ E).min())}
    chk["ok"] = (chk["row_sum_err"] <= 1e-12 and chk["min_entry"] >= 0 and chk["asym"] <= 1e-12
                 and chk["min_diag"] >= 0.2 - 1e-12 and chk["support_ok"]
                 and chk["stationarity_err"] <= 1e-12 and chk["connected"]
                 and chk["min_p_w"] >= 1e-4)
    return chk


def diagnostics(T: np.ndarray, pi: np.ndarray, world: WorldSpec, E: np.ndarray) -> dict:
    """Rate, spectrum, mixing bound and conditional-state integrated autocorrelations."""
    xy = np.asarray(world.coords, dtype=np.float64)
    ang = 2 * np.pi * xy[:, 0] / 12.0
    funcs = {"cos_x": np.cos(ang), "sin_x": np.sin(ang), "y_centred": xy[:, 1] - xy[:, 1].mean()}
    sp = spectrum_report(T, pi)
    out = {"movement_rate": movement_rate(T, pi), "gap": sp.gap, "abs_gap": sp.abs_gap,
           "t_rel": sp.t_rel, "mixing_bound_steps": sp.mixing_bound, "spectrum_status": sp.status,
           "lambda_top5": sp.eigenvalues[:5].tolist(), "lambda_min": float(sp.eigenvalues[-1])}
    out["iat"] = {k: integrated_autocorrelation(T, pi, g) for k, g in funcs.items()}
    gw = [integrated_autocorrelation(T, pi, E[:, w]) for w in range(E.shape[1])]
    vals = [v for v, s in gw if s == "ok"]
    out["iat_g_w"] = {"mean": float(np.mean(vals)) if vals else None,
                      "min": float(np.min(vals)) if vals else None,
                      "max": float(np.max(vals)) if vals else None,
                      "statuses": sorted({s for _, s in gw})}
    return out


def _entropy(p: np.ndarray) -> float:
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def body(res: dict, ctl: RunControls, repo: Path, main_root: Path, out_root: Path) -> None:
    g = ctl.guard
    g("listing before")
    res["listing_before"] = listing_hash(main_root)
    main = ArtifactStore(LocalFSBackend(main_root))
    rw = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root), LocalFSBackend(out_root /
                                                                                  "store")),
                       producer_version=producer_version(repo))
    bad = verify_parents(main, PARENTS)
    if bad:
        raise GateFailed("integrity: " + "; ".join(bad))
    world = main.load(WorldSpec, WORLD, consumer="experiment")
    flat = main.load(TransitionSpec, T_FLAT, consumer="experiment")
    emis = main.load(EmissionSpec, EMIS, consumer="experiment")
    E, perm, pi = np.asarray(emis.E, float), np.asarray(emis.symbol_perm), np.asarray(flat.pi)
    res["provenance"] = [provenance_row(main, a, r) for a, r in ((WORLD, "world"),
                         (T_FLAT, "T_a0"), (EMIS, "emission"))]
    g("integrity")
    T0_built, meta0 = conductance_kernel(world, ConductanceConfig(a=0.0))
    if meta0["n_edges_h"] != 144 or meta0["n_edges_v"] != 132:
        raise GateFailed(f"state order: edges {meta0['n_edges_h']}/{meta0['n_edges_v']}")
    a0_diff = float(np.max(np.abs(T0_built.T - flat.T)))
    res["a0_equivalence_max_diff"] = a0_diff
    if a0_diff > 1e-15:
        raise GateFailed(f"a0 equivalence {a0_diff:.3e}")
    t_a020 = ProcessStage().run_conductance_transition(WORLD, ConductanceConfig(), rw)
    res["T_a020_id"] = t_a020
    res["T_a020_meta"] = rw.meta(t_a020).config
    kernels = {"a0": np.asarray(flat.T), "a020": np.asarray(
        rw.load(TransitionSpec, t_a020, consumer="experiment").T)}
    g("kernels")
    for arm, T in kernels.items():
        v, d = kernel_validity(T, pi, world, E), diagnostics(T, pi, world, E)
        op = "INVALID_KERNEL" if not v["ok"] else (
            "NEAR_UNIT_GAP" if d["spectrum_status"] == "NEAR_UNIT_GAP" else "ok")
        res["arms"][arm] = {"op": op, "context": None, "validity": v, "diagnostics": d}
        g(f"diagnostics {arm}")
    alpha = res["arms"]["a020"]["diagnostics"]["movement_rate"] / \
        res["arms"]["a0"]["diagnostics"]["movement_rate"]
    T_alpha, a_status = rate_matched_kernel(kernels["a0"], alpha)
    res["rate_matched"] = {"alpha": alpha, "status": a_status,
                           "note": "process diagnostic only; never decisive"}
    if T_alpha is not None:
        res["rate_matched"]["diagnostics"] = diagnostics(T_alpha, pi, world, E)
    g("rate matched")
    rngs = dict(zip(ARMS, paired_generators()))
    named, seqs = {}, {}
    for arm in ARMS:
        g(f"sample {arm}")
        named[arm] = sample_named(kernels[arm], E, perm, pi, rngs[arm])
        seqs[arm] = x5_sequence_ids(arm)
        tid = T_FLAT if arm == "a0" else t_a020
        res["arms"][arm]["obs_id"] = rw.save(
            calibration_obs(named[arm], seqs[arm]),
            config={"role": "calibration", "protocol": PROTOCOL, "arm": arm,
                    "stream": "/".join(STREAM), "namespace_code": 8},
            parents=[tid, EMIS], seed_map={"/".join(STREAM): SeedTree(0).seed(*STREAM)},
            consumer="experiment")
        g(f"sample {arm} done")
    res["paired_first_symbol_equal"] = bool(np.array_equal(named["a0"][:, 0], named["a020"][:, 0]))
    old = stored_sequence_ids(main)
    b2 = np.concatenate([b2_sequence_ids(r) for r in B2_ROLES])
    clash = {arm: int(np.intersect1d(seqs[arm], np.concatenate([old, b2])).size) for arm in ARMS}
    clash["a0~a020"] = int(np.intersect1d(seqs["a0"], seqs["a020"]).size)
    res["disjointness"] = clash
    if any(clash.values()):
        raise GateFailed(f"namespace collision {clash}")
    inv = np.argsort(perm)
    res["identical_windows_between_arms"] = int(np.intersect1d(
        windows(inv[named["a0"][:, :32].astype(np.int64)]),
        windows(inv[named["a020"][:, :32].astype(np.int64)])).size)
    g("disjointness")
    kl = {}
    for arm in ARMS:
        q = gate_quantities(kernels[arm], E, pi, named[arm], guard=g)
        a = res["arms"][arm]
        a["valid_predictive"] = q["valid"]
        kl[arm] = q["kl_last"]
        a["GC"] = float(np.mean(q["kl_last"])) if q["valid"] else None
        a["GC_stationary"] = float(np.mean(q["kl_stationary"])) if q["valid"] else None
        a["two_token_regret"] = float(np.mean(q["kl_two"])) if q["valid"] else None
        a["position_entropy"] = q["position_entropy"].tolist()
        a["H_W_given_Z"] = float(np.sum(pi * np.array([_entropy(r) for r in E])))
        a["H_W"] = _entropy(pi @ E)
        sv = FutureOperator(kernels[arm], E).observability_singular_values(2)
        a["observability_sv"] = {"O1": sv[0].tolist(), "O2_top10": sv[1][:10].tolist(),
                                 "O2_rank_1e-10": int(np.sum(sv[1] > 1e-10 * sv[1][0]))}
        if q["valid"]:
            boots = bootstrap_means(q["kl_last"], SeedTree(0).generator("x5g1-v1",
                                    "gc_bootstrap", arm), guard=g)
            lo, hi = percentile_interval(boots)
            a["GC_ci95"] = [lo, hi]
            a["context"] = context_status(lo, hi, True)
        else:
            a["context"] = context_status(float("nan"), float("nan"), False)
        g(f"context {arm}")
    if all(res["arms"][a]["valid_predictive"] for a in ARMS):
        res["paired_diff_ci95"] = _paired(kl, g)
    res["listing_after"] = listing_hash(main_root)
    if res["listing_after"] != res["listing_before"]:
        raise GateFailed("main store listing changed")


def _paired(kl: dict, g) -> list[float]:
    """Descriptive paired G_C difference (a020 - a0), shared indices, frozen stream."""
    rng = SeedTree(0).generator("x5g1-v1", "gc_bootstrap_paired")
    n = kl["a0"].size
    diffs = np.empty(2000)
    for start in range(0, 2000, 500):
        g(f"paired {start}")
        for j in range(start, start + 500):
            idx = rng.integers(0, n, n)
            diffs[j] = kl["a020"][idx].mean() - kl["a0"][idx].mean()
        g(f"paired {start} done")
    return list(percentile_interval(diffs))
