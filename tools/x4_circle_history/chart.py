"""Fitted, certified circular chart with separate calibration gauge and transform (API.md).

Provenance: minimal extraction of construct_chart/orient/extend/agreement from the stopped
history-feasibility core (frozen; inspected after the independent authors received the spec),
restructured into fit / gauge / transform. Pure kernels: arrays, config and injected guard/timer
only; no file I/O and no randomness. fit_chart never receives labels or validation data.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import ripser
from cochain import edge_list, integer_lift, primitive_class, smooth_phase, triangle_system
from errors import Invalid, Unresolved
from scipy.spatial.distance import cdist

TWO_PI = 2.0 * np.pi


def _cmean(values) -> complex:
    """Complex mean as sum / n: one correctly rounded division per component (numpy's mean
    multiplies by a rounded reciprocal, which can sit one ulp off an exact boundary)."""
    values = np.asarray(values)
    return complex(np.sum(values) / values.size)


@dataclass(frozen=True)
class Chart:
    landmark_ids: np.ndarray
    landmarks: np.ndarray
    phi: np.ndarray
    sigma: float
    support_radius: float
    d8: np.ndarray
    edges: np.ndarray
    cocycle: np.ndarray
    integer_lift: np.ndarray
    lift_correction: np.ndarray
    primitive: np.ndarray
    tree_potential: np.ndarray
    period_gcd: int
    info: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Gauge:
    sign: int
    shift: float
    alignment: float


@dataclass(frozen=True)
class Extension:
    phase: np.ndarray
    resultant: np.ndarray
    eighth_distance: np.ndarray
    supported: np.ndarray
    duplicate: np.ndarray


def select_h1_bar(dgm) -> int:
    """Index of the largest strictly positive finite lifetime; ties birth, death, index."""
    dgm = np.asarray(dgm, dtype=np.float64).reshape(-1, 2)
    candidates = [k for k, (b, d) in enumerate(dgm) if np.isfinite(b) and np.isfinite(d) and d > b]
    if not candidates:
        raise Unresolved("no finite strictly positive H1 bar")
    return min(candidates, key=lambda k: (-(dgm[k, 1] - dgm[k, 0]), dgm[k, 0], dgm[k, 1], k))


def cocycle_to_edges(cocycle_rows, edges, p) -> np.ndarray:
    """Centred, oriented integer representative of a ripser F_p cocycle on ``edges``."""
    edges = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    index = {(int(i), int(j)): k for k, (i, j) in enumerate(edges)}
    a = np.zeros(len(edges), dtype=np.int64)
    for x, y, value in np.asarray(cocycle_rows).reshape(-1, 3):
        x, y, value = int(x), int(y), int(value) % p
        sign = 1 if x < y else -1
        lo, hi = min(x, y), max(x, y)
        if (lo, hi) in index:
            a[index[(lo, hi)]] = sign * (value if value <= p // 2 else value - p)
    return a


def _neighbor_scale(D):
    masked = D.copy()
    np.fill_diagonal(masked, np.inf)
    d8 = np.sort(masked, axis=1)[:, 7]
    sigma = float(np.median(d8))
    support = 2.0 * float(np.quantile(d8, 0.99, method="inverted_cdf"))
    if not np.isfinite(sigma) or not sigma > 0:
        raise Unresolved("zero or non-finite extension bandwidth")
    return d8, sigma, support


def _check_landmarks(X, landmark_ids):
    X = np.asarray(X, dtype=np.float64)
    ids = np.asarray(landmark_ids).astype(str)
    if X.ndim != 2 or X.shape[0] < 9 or not np.isfinite(X).all():
        raise Invalid(f"landmarks must be finite [n>=9, d], got {X.shape}")
    if ids.shape != (X.shape[0],) or not all(ids[k] < ids[k + 1] for k in range(len(ids) - 1)):
        raise Invalid("landmark_ids must be unique and strictly ascending")
    return X, ids


def fit_chart(X, landmark_ids, cfg, guard=None, timed=None) -> Chart:
    """Fixed-rule certified chart on all landmarks (API.md fit_chart)."""
    X, ids = _check_landmarks(X, landmark_ids)
    timed = timed or (lambda label, fn: fn())
    p, n = int(cfg["field"]), X.shape[0]
    D = cdist(X, X)
    result = timed(
        "ph", lambda: ripser.ripser(D, maxdim=1, coeff=p, distance_matrix=True, do_cocycles=True)
    )
    dgm = result["dgms"][1]
    k = select_h1_bar(dgm)
    birth, death = float(dgm[k, 0]), float(dgm[k, 1])
    radius = (birth + death) / 2.0
    edges = edge_list(D, radius)
    a = cocycle_to_edges(result["cocycles"][1][k], edges, p)
    if guard is not None:
        guard()
    D1, triangles = timed("two_skeleton", lambda: triangle_system(edges, n))
    alpha, lift_info = timed(
        "integer_lift", lambda: integer_lift(a, D1, edges, triangles, n, cfg, guard)
    )
    beta, q, g = timed("primitive", lambda: primitive_class(alpha, edges, triangles, n, p))
    phi, residual = timed("smoothing", lambda: smooth_phase(beta, edges, n))
    d8, sigma, support = _neighbor_scale(D)
    correction = lift_info.pop("correction", np.zeros(len(edges), dtype=np.int64))
    info = {
        "birth": birth,
        "death": death,
        "radius": radius,
        "bar_index": int(k),
        "n_edges": int(len(edges)),
        "n_triangles": int(len(triangles)),
        "lift": lift_info,
        "smoothing_residual": float(residual),
    }
    return Chart(
        ids,
        X.copy(),
        phi,
        sigma,
        support,
        d8,
        edges,
        a,
        alpha,
        np.asarray(correction, dtype=np.int64),
        beta,
        q,
        g,
        info,
    )


def fit_gauge(chart: Chart, m32) -> Gauge:
    """Calibration-only reflection/rotation gauge (API.md fit_gauge)."""
    m32 = np.asarray(m32, dtype=np.float64)
    if m32.shape != (len(chart.phi), 2) or not np.isfinite(m32).all():
        raise Invalid("m32 must be finite [n, 2] aligned to the landmarks")
    target = np.conj(m32[:, 0] + 1j * m32[:, 1])
    values = {s: _cmean(np.exp(1j * s * chart.phi) * target) for s in (1, -1)}
    sign = 1 if abs(values[1]) >= abs(values[-1]) else -1
    c = values[sign]
    alignment = float(abs(c))
    if not np.isfinite(alignment):
        raise Invalid("non-finite gauge alignment")
    if alignment == 0.0:
        raise Unresolved("zero gauge alignment")
    return Gauge(sign=sign, shift=float(np.angle(c)), alignment=alignment)


def apply_gauge(phi, gauge: Gauge) -> np.ndarray:
    return (gauge.sign * np.asarray(phi, dtype=np.float64) - gauge.shift) % TWO_PI


def extend(chart: Chart, gauge: Gauge, Q, cfg) -> Extension:
    """Out-of-sample phase by the fixed 8-nearest Gaussian rule (API.md extend)."""
    Q = np.asarray(Q, dtype=np.float64)
    if Q.ndim != 2 or Q.shape[1] != chart.landmarks.shape[1] or not np.isfinite(Q).all():
        raise Invalid("queries must be finite [m, d] with the landmark dimension")
    k = int(cfg["extension_k"])
    phi_g = apply_gauge(chart.phi, gauge)
    dist = cdist(Q, chart.landmarks)
    order = np.argsort(dist, axis=1, kind="stable")[:, :k]
    nearest = np.take_along_axis(dist, order, axis=1)
    log_w = -0.5 * (nearest / chart.sigma) ** 2
    weights = np.exp(log_w - log_w.max(axis=1, keepdims=True))  # same normalised weights
    z = (weights * np.exp(1j * phi_g[order])).sum(1) / weights.sum(1)
    if not np.isfinite(z).all():
        raise Invalid("non-finite extension resultant")
    duplicate = (dist == 0.0).any(axis=1)
    for row in np.flatnonzero(duplicate):
        z[row] = _cmean(np.exp(1j * phi_g[dist[row] == 0.0]))
        if 1.0 - abs(z[row]) > 1e-8:
            raise Invalid("exact duplicate landmarks carry conflicting phases")
    resultant = np.abs(z)
    eighth = nearest[:, -1]
    supported = (resultant >= cfg["support_min_resultant"]) & (eighth <= chart.support_radius)
    return Extension(np.angle(z) % TWO_PI, resultant, eighth, supported, duplicate)


def agreement(phi_a, phi_b) -> float:
    a, b = np.asarray(phi_a, dtype=np.float64), np.asarray(phi_b, dtype=np.float64)
    if (
        a.shape != b.shape
        or a.ndim != 1
        or not a.size
        or not (np.isfinite(a).all() and np.isfinite(b).all())
    ):
        raise Invalid("agreement needs equal-length finite phase vectors")
    return min(1.0, max(abs(_cmean(np.exp(1j * (a - s * b)))) for s in (1, -1)))


def phase_bin_counts(phi, bins: int = 12) -> np.ndarray:
    phi = np.asarray(phi, dtype=np.float64)
    if not np.isfinite(phi).all():
        raise Invalid("non-finite phase")
    idx = np.minimum(np.floor(phi * bins / TWO_PI).astype(np.int64), bins - 1)
    return np.bincount(idx % bins, minlength=bins)


def overall_resultant(phi) -> float:
    phi = np.asarray(phi, dtype=np.float64)
    if not phi.size or not np.isfinite(phi).all():
        raise Invalid("non-finite or empty phase")
    return float(abs(_cmean(np.exp(1j * phi))))


def _record(met: bool, value, threshold) -> dict:
    return {
        "status": "PASS" if met else "INCONCLUSIVE",
        "criterion_met": bool(met),
        "value": value,
        "threshold": threshold,
    }


def chart_gates(ext: Extension, direct_phi, cfg) -> dict:
    """Support, fidelity, bins and overall-resultant criteria (API.md chart_gates)."""
    a = agreement(ext.phase, direct_phi)
    counts = phase_bin_counts(ext.phase, int(cfg["phase_bins"]))
    res = overall_resultant(ext.phase)
    gates = {
        "support": _record(
            bool(np.all(ext.supported)), int(np.sum(ext.supported)), len(ext.supported)
        ),
        "fidelity": _record(a >= cfg["fidelity_min_agreement"], a, cfg["fidelity_min_agreement"]),
        "bins": _record(
            bool(np.all(counts >= cfg["phase_bin_min_rows"])),
            counts.tolist(),
            cfg["phase_bin_min_rows"],
        ),
        "resultant": _record(
            res <= cfg["overall_resultant_max"], res, cfg["overall_resultant_max"]
        ),
    }
    gates["overall"] = next(
        (
            gates[g]["status"]
            for g in ("support", "fidelity", "bins", "resultant")
            if gates[g]["status"] != "PASS"
        ),
        "PASS",
    )
    return gates


_ARRAY_FIELDS = (
    "landmark_ids",
    "landmarks",
    "phi",
    "d8",
    "edges",
    "cocycle",
    "integer_lift",
    "lift_correction",
    "primitive",
    "tree_potential",
)


def chart_to_arrays(chart: Chart, gauge: Gauge) -> dict:
    """Arrays for an immutable NPZ; info travels as a JSON string in a unicode array (no pickle)."""
    out = {name: np.asarray(getattr(chart, name)) for name in _ARRAY_FIELDS}
    out["landmark_ids"] = np.asarray(chart.landmark_ids).astype(str)
    out["scalars"] = np.array(
        [
            chart.sigma,
            chart.support_radius,
            float(chart.period_gcd),
            float(gauge.sign),
            gauge.shift,
            gauge.alignment,
        ]
    )
    out["info_json"] = np.array(json.dumps(chart.info, sort_keys=True, default=_jsonable))
    return out


def _jsonable(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(f"not JSON serialisable: {type(value).__name__}")


def chart_from_arrays(d) -> tuple[Chart, Gauge]:
    s = np.asarray(d["scalars"], dtype=np.float64)
    chart = Chart(
        *(np.asarray(d[name]) for name in ("landmark_ids", "landmarks", "phi")),
        float(s[0]),
        float(s[1]),
        np.asarray(d["d8"]),
        *(
            np.asarray(d[name])
            for name in (
                "edges",
                "cocycle",
                "integer_lift",
                "lift_correction",
                "primitive",
                "tree_potential",
            )
        ),
        int(s[2]),
        json.loads(str(d["info_json"])) if "info_json" in d else {},
    )
    return chart, Gauge(sign=int(s[3]), shift=float(s[4]), alignment=float(s[5]))
