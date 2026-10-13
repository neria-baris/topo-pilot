"""X4 Phase B reachable audit per pool and the test-pool agreement checks (protocol §5–§6).

Joins pure analysis screens to the pools built in :mod:`x4b`; returns plain dicts and arrays for
the run module to export. Pairs are descriptive; nothing here is a statistical test.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.analysis import (
    Partners,
    PoolScreen,
    hellinger,
    nearest_partners,
    pair_d2,
    screen_pool,
    select_anchors,
)
from topo_pilot.contracts import OracleOutputs

from .x4b import END, FutureMaps, Pool

Q1_EQUAL = 1e-15


def _q(x: NDArray, ps: tuple[float, ...] = (0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0)) -> list:
    v = np.asarray(x, dtype=np.float64)
    v = v[np.isfinite(v)]
    return [float(np.quantile(v, p)) for p in ps] if v.size else []


def screen(pool: Pool, Q1: NDArray, Q2: NDArray, last: NDArray | None,
           anchors: NDArray) -> tuple[Partners, PoolScreen]:
    """Partners (same last symbol unless ``last`` is None) and the frozen screen."""
    partners = nearest_partners(Q1, pool.history_keys, anchors, last, pool.canonical_ids)
    return partners, screen_pool(partners.d1, pair_d2(Q2, anchors, partners))


def describe(pool: Pool, anchors: NDArray, partners: Partners, scr: PoolScreen) -> dict:
    """Descriptive record of one screen (protocol §6 'recorded, never a verdict')."""
    have = partners.idx >= 0
    adm = scr.admissible
    b = pool.b32[anchors]
    ent = -(b * np.log(np.where(b > 0, b, 1.0))).sum(1)
    reuse = np.bincount(partners.idx[adm], minlength=len(pool.canonical_ids)) if adm.any() \
        else np.zeros(1, dtype=np.int64)
    d1, d2 = partners.d1, scr.d2
    ratio = np.where(have & (d1 > 0), d2 / np.where(d1 > 0, d1, 1.0), np.nan)
    q1diff = np.full(partners.idx.shape, np.nan)
    rows, cols = np.nonzero(have)
    q1diff[rows, cols] = np.max(np.abs(pool.Q1[anchors[rows]] - pool.Q1[partners.idx[rows, cols]]),
                                axis=1) if rows.size else []
    nearest = np.where(have[:, 0], d1[:, 0], np.inf)
    return {
        "n_anchors": int(len(anchors)), "n_eligible": scr.n_eligible,
        "n_witness": scr.n_witness, "witness_fraction": scr.fraction, "status": scr.status,
        "group_size_quantiles": _q(partners.group_size),
        "anchors_fewer_than_5_candidates": int(np.sum(partners.group_size < 5)),
        "anchors_no_candidate": int(np.sum(partners.group_size == 0)),
        "duplicate_history_rows_excluded": int(partners.n_duplicate.sum()),
        "discarded_nearest_d1_above_0.01": int(np.sum(~scr.eligible & (partners.group_size > 0))),
        "admissible_pairs": int(adm.sum()),
        "d1_quantiles_all": _q(d1[have]), "d2_quantiles_all": _q(d2[have]),
        "d1_quantiles_nearest": _q(nearest[np.isfinite(nearest)]),
        "d2_quantiles_admissible": _q(d2[adm]),
        "max_d2_admissible": float(np.max(d2[adm])) if adm.any() else None,
        "ratio_d2_d1_quantiles": _q(ratio[have]),
        "d2_below_d1_violations": int(np.sum(d2[have] < d1[have] - 1e-12)),
        "numerically_equal_Q1_pairs": int(np.sum(q1diff[have] <= Q1_EQUAL)),
        "partner_reuse_max": int(reuse.max()), "distinct_admissible_partners":
            int(np.sum(reuse > 0)),
        "anchor_entropy_quantiles_eligible": _q(ent[scr.eligible]),
        "anchor_entropy_quantiles_not_eligible": _q(ent[~scr.eligible]),
        "anchor_maxb_quantiles_eligible": _q(b.max(1)[scr.eligible]),
        "anchor_maxb_quantiles_not_eligible": _q(b.max(1)[~scr.eligible]),
    }


def anchor_table(pool: Pool, anchors: NDArray, partners: Partners, scr: PoolScreen) -> list[dict]:
    """One row per anchor with canonical/run ids, partners, distances and flags."""
    out = []
    for r, a in enumerate(anchors.tolist()):
        row = {"pool": pool.name, "anchor_canonical_id": pool.canonical_ids[a],
               "last_symbol_canonical": int(pool.last_symbol[a]),
               "group_size": int(partners.group_size[r]),
               "eligible": bool(scr.eligible[r]), "witness": bool(scr.witness[r])}
        for seed, ids in pool.run_history_ids.items():
            row[f"history_id_{seed}"] = ids[a]
        for k in range(partners.idx.shape[1]):
            p = int(partners.idx[r, k])
            row[f"p{k + 1}_canonical_id"] = pool.canonical_ids[p] if p >= 0 else ""
            row[f"p{k + 1}_d1"] = float(partners.d1[r, k]) if p >= 0 else ""
            row[f"p{k + 1}_d2"] = float(scr.d2[r, k]) if p >= 0 else ""
        out.append(row)
    return out


def pool_audit(pool: Pool) -> dict:
    """Primary (same last symbol) and secondary (unrestricted) screens of one pool."""
    anchors = select_anchors(pool.canonical_ids)
    partners, scr = screen(pool, pool.Q1, pool.Q2, pool.last_symbol, anchors)
    p_u, s_u = screen(pool, pool.Q1, pool.Q2, None, anchors)
    return {"anchors": anchors, "partners": partners, "screen": scr,
            "summary": describe(pool, anchors, partners, scr),
            "unrestricted": describe(pool, anchors, p_u, s_u),
            "table": anchor_table(pool, anchors, partners, scr)}


def agreement_check(pool: Pool, primary: dict, seed: int, run_tokens: NDArray,
                   oracle: OracleOutputs, maps_run: FutureMaps, perm: NDArray,
                   b32_run_filter: NDArray) -> dict:
    """Precision reconciliation and permutation invariance for the test pool in one run.

    ``run_tokens [M, 32]`` and ``b32_run_filter [M, N]`` are in pool row order;
    ``b32_run_filter`` is the run-vocabulary filter output on those tokens.
    """
    pos = {h: i for i, h in enumerate(oracle.history_id.tolist())}
    rows = [pos[h] for h in pool.run_history_ids[seed]]
    b_st = np.asarray(oracle.b32, dtype=np.float64)[rows]
    q_st = np.asarray(oracle.q, dtype=np.float64)[rows]
    f2_st = np.asarray(oracle.F2)[rows].reshape(len(rows), -1)
    q1_run, q2_run = b_st @ maps_run.G1, b_st @ maps_run.G2
    anchors, ref_p, ref_s = primary["anchors"], primary["partners"], primary["screen"]
    p_run, s_run = screen(pool, q1_run, q2_run, run_tokens[:, END - 1], anchors)
    d2_f32 = np.full(ref_p.idx.shape, np.nan)
    rr, cc = np.nonzero(ref_p.idx >= 0)
    f2 = f2_st.astype(np.float64)
    d2_f32[rr, cc] = hellinger(f2[anchors[rr]], f2[ref_p.idx[rr, cc]])
    s_f32 = screen_pool(ref_p.d1, d2_f32)
    return {
        "seed": seed, "F2_dtype": str(oracle.F2.dtype),
        "b32_run_filter_vs_canonical": float(np.max(np.abs(b32_run_filter - pool.b32))),
        "b32_stored_vs_canonical": float(np.max(np.abs(b_st - pool.b32))),
        "q_stored_vs_recomputed": float(np.max(np.abs(q_st - q1_run))),
        "Q1_run_perm_vs_canonical": float(np.max(np.abs(q1_run[:, perm] - pool.Q1))),
        "F2_float32_vs_float64_max": float(np.max(np.abs(f2 - q2_run))),
        "F2_float32_vs_float64_max_rel": float(np.max(np.abs(f2 - q2_run) /
                                                      np.maximum(q2_run, 1e-300))),
        "run_vocab_partners_identical": bool(np.array_equal(p_run.idx, ref_p.idx)),
        "run_vocab_flags_identical": bool(np.array_equal(s_run.eligible, ref_s.eligible)
                                          and np.array_equal(s_run.witness, ref_s.witness)),
        "run_vocab_status": s_run.status,
        "run_vocab_max_d1_diff": float(np.nanmax(np.abs(p_run.d1 - ref_p.d1))),
        "run_vocab_max_d2_diff": float(np.nanmax(np.abs(s_run.d2 - ref_s.d2))),
        "float32_witness_flips": int(np.sum(s_f32.witness != ref_s.witness)),
        "float32_status": s_f32.status, "float32_max_d2_diff":
            float(np.nanmax(np.abs(d2_f32 - ref_s.d2))),
    }


def agreement_failures(a: dict, primary_status: str) -> list[str]:
    """Protocol §5/§6 agreement failures for one run's test-pool check."""
    bad = []
    for key in ("b32_run_filter_vs_canonical", "b32_stored_vs_canonical",
                "q_stored_vs_recomputed", "Q1_run_perm_vs_canonical"):
        if not a[key] <= 1e-12:
            bad.append(key)
    if not a["F2_float32_vs_float64_max"] <= 1e-4:
        bad.append("F2_float32_vs_float64_max")
    if not (a["run_vocab_partners_identical"] and a["run_vocab_flags_identical"]):
        bad.append("run_vocab_permutation")
    if a["float32_status"] != primary_status:
        bad.append("float32_status_change")
    return bad
