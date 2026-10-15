"""C1' chart: the frozen K4 construction restricted to the largest connected component at the
selected bar's midpoint (API.md §3; protocol §14). Every step calls the frozen chart/cochain
function named, unchanged, in fit_chart's order; persistence goes through an injected callable."""

from __future__ import annotations

import json
from pathlib import Path

import c1_config  # noqa: F401  (sys.path)
import chart
import numpy as np
import ripser
from c1_records import C1GateFailure
from cochain import edge_list, integer_lift, primitive_class, smooth_phase, triangle_system
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

IDENTITY_CARRIER = chart.Gauge(sign=1, shift=0.0, alignment=0.0)
ROLES = ("production", "direct")
MAX_CONSTRUCTIONS = 6


def landmark_ids(seq_ids) -> np.ndarray:
    return np.array([f"{int(s):020d}" for s in np.asarray(seq_ids)])


class ConstructionLedger:
    """At most six constructions in total, one per (model, role); never retried (§14)."""

    def __init__(self, path):
        self.path = Path(path)

    def claims(self) -> list:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))["claims"]

    def claim(self, model, role) -> None:
        if role not in ROLES:
            raise C1GateFailure("FAIL_TECHNICAL", f"unknown chart role {role!r}")
        claims = self.claims()
        if [int(model), role] in [[int(m), r] for m, r in claims]:
            raise C1GateFailure("FAIL_TECHNICAL", f"chart ({model}, {role}) already constructed")
        if len(claims) >= MAX_CONSTRUCTIONS:
            raise C1GateFailure("FAIL_TECHNICAL", "six-construction limit reached")
        claims.append([int(model), role])
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"claims": claims}, indent=1), encoding="utf-8")
        tmp.replace(self.path)


def components(edges, n) -> tuple:
    edges = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    graph = coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])), shape=(n, n))
    _, labels = connected_components(graph, directed=False)
    labels = np.asarray(labels, dtype=np.int64)
    return labels, np.bincount(labels).astype(np.int64)


def giant(labels, sizes) -> tuple:
    """Largest component; ties to the component containing the smallest index."""
    labels = np.asarray(labels)
    first = {int(c): int(np.flatnonzero(labels == c)[0]) for c in range(len(sizes))}
    best = min(range(len(sizes)), key=lambda c: (-int(sizes[c]), first[c]))
    cstar = np.flatnonzero(labels == best).astype(np.int64)
    return cstar, int(len(cstar))


def giant_pass(m, n=512) -> bool:
    return 100 * int(m) >= 95 * int(n)


def restrict(edges, cocycle, cstar, n) -> tuple:
    edges = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    cocycle = np.asarray(cocycle, dtype=np.int64)
    new = np.full(int(n), -1, dtype=np.int64)
    new[np.asarray(cstar, dtype=np.int64)] = np.arange(len(cstar), dtype=np.int64)
    keep = (new[edges[:, 0]] >= 0) & (new[edges[:, 1]] >= 0)
    return np.column_stack((new[edges[keep, 0]], new[edges[keep, 1]])).astype(np.int64), \
        cocycle[keep].copy()


def _largest_finite_h0(dgm0) -> float:
    d = np.asarray(dgm0, dtype=np.float64).reshape(-1, 2)[:, 1]
    d = d[np.isfinite(d)]
    return float(d.max()) if d.size else float("nan")


def fit_chart_lcc(X, ids, cfg, guard=None, timed=None, persist=None) -> chart.Chart:
    """§14 steps 1-10; equals chart.fit_chart bitwise (arrays, scalars) on a connected graph."""
    X, ids = chart._check_landmarks(X, ids)
    timed = timed or (lambda label, fn: fn())
    persist = persist or (lambda name, obj: None)
    p, n = int(cfg["field"]), X.shape[0]
    D = timed("distance", lambda: chart.cdist(X, X))
    result = timed(
        "ph", lambda: ripser.ripser(D, maxdim=1, coeff=p, distance_matrix=True, do_cocycles=True)
    )
    dgm = result["dgms"][1]
    k = chart.select_h1_bar(dgm)
    birth, death = float(dgm[k, 0]), float(dgm[k, 1])
    radius = (birth + death) / 2.0
    edges = timed("edges", lambda: edge_list(D, radius))
    a = chart.cocycle_to_edges(result["cocycles"][1][k], edges, p)
    labels, sizes = components(edges, n)
    cstar, m = giant(labels, sizes)
    excluded = [str(ids[i]) for i in np.flatnonzero(~np.isin(np.arange(n), cstar))]
    ok = giant_pass(m, n)
    l_max = _largest_finite_h0(result["dgms"][0])
    persist("giant", {"birth": birth, "death": death, "radius": radius, "bar_index": int(k),
                      "l_max": l_max, "n_components": int(len(sizes)),
                      "component_sizes": sorted((int(s) for s in sizes), reverse=True),
                      "excluded_ids": excluded, "m": m, "n": int(n), "giant_pass": ok})
    if not ok:
        raise C1GateFailure("INCONCLUSIVE/CHART_UNAVAILABLE", "GIANT_BELOW_0.95")
    edges_c, a_c = restrict(edges, a, cstar, n)
    if guard is not None:
        guard()
    D1, triangles = timed("two_skeleton", lambda: triangle_system(edges_c, m))
    alpha, lift_info = timed(
        "integer_lift", lambda: integer_lift(a_c, D1, edges_c, triangles, m, cfg, guard)
    )
    persist("lift", {"kind": lift_info.get("kind")})
    beta, q, g = timed("primitive", lambda: primitive_class(alpha, edges_c, triangles, m, p))
    persist("primitive", {"g": int(g)})
    phi, residual = timed("smoothing", lambda: smooth_phase(beta, edges_c, m))
    persist("smoothing", {"residual": float(residual)})
    d8, sigma, support = chart._neighbor_scale(D[np.ix_(cstar, cstar)])
    correction = lift_info.pop("correction", np.zeros(len(edges_c), dtype=np.int64))
    info = {
        "birth": birth, "death": death, "radius": radius, "bar_index": int(k),
        "n_edges": int(len(edges_c)), "n_triangles": int(len(triangles)), "lift": lift_info,
        "smoothing_residual": float(residual),
        "n": int(n), "m": m, "l_max": l_max, "n_components": int(len(sizes)),
        "component_sizes": sorted((int(s) for s in sizes), reverse=True),
        "excluded_ids": excluded, "lift_kind": lift_info.get("kind"), "cstar": cstar.tolist(),
    }
    return chart.Chart(ids[cstar], X[cstar].copy(), phi, sigma, support, d8, edges_c, a_c,
                       alpha, np.asarray(correction, dtype=np.int64), beta, q, g, info)


def fit_production_gauge(ch, m32_cstar) -> chart.Gauge:
    return chart.fit_gauge(ch, m32_cstar)


def serialise(ch, gauge, role) -> dict:
    production = role == "production"
    info = dict(ch.info, role="production" if production else "validation_only",
                gauge_fitted=bool(production))
    view = chart.Chart(*(getattr(ch, f) for f in (
        "landmark_ids", "landmarks", "phi", "sigma", "support_radius", "d8", "edges", "cocycle",
        "integer_lift", "lift_correction", "primitive", "tree_potential", "period_gcd")), info)
    return chart.chart_to_arrays(view, gauge if production else IDENTITY_CARRIER)


def extend_phase(prod, gauge, Q, cfg, timed=None):
    return chart.extend(prod, gauge, Q, cfg, timed=timed)


def c0_val(prod, gauge, val_X, direct, cfg) -> dict:
    """The four C0-val criteria (§14) with the frozen kernels; chart_gates is never called."""
    ext = chart.extend(prod, gauge, val_X, cfg)
    n = int(len(ext.supported))
    n_sup = int(np.sum(ext.supported))
    cstar = np.asarray(direct.info["cstar"], dtype=np.int64)
    fid = float(chart.agreement(ext.phase[cstar], direct.phi))
    bins = chart.phase_bin_counts(ext.phase, int(cfg["phase_bins"]))
    res = float(chart.overall_resultant(ext.phase))
    crit = {"support": 100 * n_sup >= 99 * n,
            "fidelity": fid >= cfg["fidelity_min_agreement"],
            "bins": bool(np.all(bins >= cfg["phase_bin_min_rows"])),
            "resultant": res <= cfg["overall_resultant_max"]}
    return {"n": n, "n_supported": n_sup, "fidelity": fid, "bins": bins.tolist(),
            "resultant": res, "criteria": crit,
            "status": "PASS" if all(crit.values()) else "INCONCLUSIVE/CHART_UNAVAILABLE"}
