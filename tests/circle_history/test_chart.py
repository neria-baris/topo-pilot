"""Independent synthetic tests, author A (spec v2.3): chart bar selection, cocycle mapping,
fit_chart and gauge (TEST_PLAN A8, A9, A10; A13 is in test_chart_arrays.py).

Written from tools/x4_circle_history/API.md, CONTRACT.json and TEST_PLAN.md only. Diagrams,
distances, d8, sigma and certificates are recomputed here from the written definitions (ripser
and numpy only); production helpers are never used to check production results.
"""

from __future__ import annotations

import dataclasses
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest
from ripser import ripser

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG = REPO_ROOT / "tools" / "x4_circle_history"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import chart  # noqa: E402
import errors  # noqa: E402

pytestmark = pytest.mark.analysis

P = 47
TWO_PI = 2.0 * math.pi
CHART_KEYS = (
    "field", "lift_bounds", "lift_node_limit", "lift_cpu_cap_s", "lift_rounding_tol",
    "local_passes", "local_vertices", "extension_k", "support_min_resultant",
    "fidelity_min_agreement", "phase_bins", "phase_bin_min_rows", "overall_resultant_max",
    "smoothing_residual_max",
)
ARRAY_FIELDS = ("landmark_ids", "landmarks", "phi", "d8", "edges", "cocycle", "integer_lift",
                "lift_correction", "primitive", "tree_potential")
INT_FIELDS = ("edges", "cocycle", "integer_lift", "lift_correction", "primitive",
              "tree_potential")


def make_cfg(**overrides):
    chart_cfg = json.loads((PKG / "CONTRACT.json").read_text(encoding="utf-8"))["chart"]
    cfg = {key: chart_cfg[key] for key in CHART_KEYS}
    cfg["lift_bounds"] = list(cfg["lift_bounds"])
    cfg.update(overrides)
    return cfg


def make_ids(n):
    return np.array([f"h{k:04d}" for k in range(n)])


def circle_points(theta):
    """Deterministic circle in R^4 with small, symmetry-breaking offsets."""
    r = 1.0 + 0.02 * np.cos(7 * theta + 0.4)
    return np.column_stack([r * np.cos(theta), r * np.sin(theta),
                            0.03 * np.sin(3 * theta + 1.1), 0.02 * np.cos(5 * theta + 2.3)])


def distance_matrix(X):
    diff = X[:, None, :] - X[None, :, :]
    return np.sqrt(np.einsum("ijk,ijk->ij", diff, diff))


def eighth_neighbour(dist):
    return np.array([np.sort(np.delete(dist[i], i))[7] for i in range(dist.shape[0])])


def my_select_bar(dgm):
    best = None
    for index, (birth, death) in enumerate(np.asarray(dgm, dtype=np.float64).tolist()):
        life = death - birth
        if math.isfinite(life) and life > 0:
            key = (-life, birth, death, index)
            best = key if best is None or key < best else best
    return best[3]


def edge_index(edges):
    return {(int(i), int(j)): e for e, (i, j) in enumerate(np.asarray(edges).tolist())}


def clique_triangles(edges, n):
    forward = [set() for _ in range(n)]
    for i, j in np.asarray(edges).tolist():
        forward[i].add(j)
    return [(i, j, k) for i in range(n) for j in sorted(forward[i])
            for k in sorted(forward[i] & forward[j])]


def triangle_sums(c, edges, triangles):
    idx = edge_index(edges)
    vals = [int(v) for v in np.asarray(c).tolist()]
    return [vals[idx[(j, k)]] - vals[idx[(i, k)]] + vals[idx[(i, j)]] for i, j, k in triangles]


def unit_columns(angle, scale=1.0):
    return scale * np.column_stack([np.cos(angle), np.sin(angle)])


CIRCLE_THETA = TWO_PI * np.arange(48) / 48
CIRCLE_X = circle_points(CIRCLE_THETA)


@pytest.fixture(scope="module")
def circle_chart():
    return chart.fit_chart(CIRCLE_X.copy(), make_ids(48), make_cfg())


@pytest.fixture(scope="module")
def dup_fit():
    X = np.vstack([CIRCLE_X[:5], CIRCLE_X[4:5], CIRCLE_X[5:]])  # rows 4 and 5 identical
    given = X.copy()
    fitted = chart.fit_chart(given, make_ids(49), make_cfg())
    given[:] = 0.0  # the chart must hold its own copy
    return X, fitted


# ----------------------------------------------------------------------------------------- A8
INF = math.inf


@pytest.mark.parametrize("dgm, expected", [
    ([[0.0, 0.5], [0.25, 1.5], [0.125, 0.25]], 1),                 # largest lifetime
    ([[0.5, 1.25], [0.25, 1.0], [0.0, 0.25]], 1),                  # tie 0.75: lower birth
    ([[0.5, 1.0], [0.25, 0.75], [0.375, 0.875]], 1),               # three-way tie on birth
    ([[0.25, 1.0], [0.25, 1.0], [0.0, 0.125]], 0),                 # full tie: lower index
    ([[0.0, INF], [0.25, 0.5]], 1),                                # infinite excluded
    ([[0.5, 0.5], [0.25, 0.375]], 1),                              # zero lifetime excluded
    ([[0.5, 0.25], [0.0, 0.125]], 1),                              # negative excluded
])
def test_select_h1_bar(dgm, expected):
    # Dyadic values make the lifetime ties exact. With equal lifetime and equal birth the death
    # is equal too, so "death asc" can only separate exact duplicates (index asc then decides).
    assert int(chart.select_h1_bar(np.asarray(dgm, dtype=np.float64))) == expected


@pytest.mark.parametrize("dgm", [[[0.0, INF], [0.5, 0.5]], np.zeros((0, 2))])
def test_select_h1_bar_none(dgm):
    with pytest.raises(errors.Unresolved):
        chart.select_h1_bar(np.asarray(dgm, dtype=np.float64))


def test_cocycle_to_edges_sign_centring_and_unknown_edges():
    edges = np.array([[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]], dtype=np.int64)
    rows = np.array([
        [1, 0, 5],    # x > y: sign -1; 5 <= 23 -> 5; a(0,1) = -5
        [0, 2, 30],   # sign +1; 30 > 23 -> -17
        [1, 2, 23],   # p//2 = 23 stays 23
        [3, 2, 24],   # sign -1; 24 -> -23; a(2,3) = +23
        [0, 3, 7],    # (0,3) not an edge: ignored
    ], dtype=np.int64)
    a = np.asarray(chart.cocycle_to_edges(rows, edges, P))
    assert a.dtype == np.int64
    assert a.tolist() == [-5, -17, 23, 0, 23]  # (1,3) has no row: 0


# ----------------------------------------------------------------------------------------- A9
def test_fit_chart_exists(circle_chart):
    fitted = circle_chart
    assert isinstance(fitted, chart.Chart)
    assert fitted.landmark_ids.tolist() == make_ids(48).tolist()
    assert np.array_equal(fitted.landmarks, CIRCLE_X)
    phi = np.asarray(fitted.phi)
    assert phi.shape == (48,) and np.all(phi >= 0.0) and np.all(phi < TWO_PI)
    for name in INT_FIELDS:
        assert np.asarray(getattr(fitted, name)).dtype == np.int64
    assert float(fitted.info["smoothing_residual"]) <= 1e-8


def test_fit_chart_bar_radius_and_edges(circle_chart):
    dist = distance_matrix(CIRCLE_X)
    dgm = ripser(dist, maxdim=1, coeff=P, distance_matrix=True, do_cocycles=True)["dgms"][1]
    k = my_select_bar(dgm)
    birth, death = float(dgm[k][0]), float(dgm[k][1])
    radius = (birth + death) / 2
    info = circle_chart.info
    assert int(info["bar_index"]) == k
    assert float(info["birth"]) == pytest.approx(birth, rel=1e-9)
    assert float(info["death"]) == pytest.approx(death, rel=1e-9)
    assert float(info["radius"]) == pytest.approx(radius, rel=1e-9)
    expected = [[i, j] for i in range(48) for j in range(i + 1, 48) if dist[i, j] <= radius]
    assert np.asarray(circle_chart.edges).tolist() == expected
    assert int(info["n_edges"]) == len(expected)
    assert int(info["n_triangles"]) == len(clique_triangles(circle_chart.edges, 48))


def test_fit_chart_cocycle_matches_ripser_rows(circle_chart):
    # Possibly fragile: assumes production's distance matrix orders the filtration like ours.
    dist = distance_matrix(CIRCLE_X)
    res = ripser(dist, maxdim=1, coeff=P, distance_matrix=True, do_cocycles=True)
    k = my_select_bar(res["dgms"][1])
    idx = edge_index(circle_chart.edges)
    expected = np.zeros(len(idx), dtype=np.int64)
    for x, y, v in np.asarray(res["cocycles"][1][k]).astype(np.int64).tolist():
        key = (min(x, y), max(x, y))
        if key in idx:
            expected[idx[key]] = (1 if x < y else -1) * (v if v <= P // 2 else v - P)
    assert np.array_equal(np.asarray(circle_chart.cocycle), expected)


def test_fit_chart_certificates_explicit(circle_chart):
    c = circle_chart
    edges = np.asarray(c.edges)
    tris = clique_triangles(edges, 48)
    alpha, a = np.asarray(c.integer_lift), np.asarray(c.cocycle)
    assert triangle_sums(alpha, edges, tris) == [0] * len(tris)
    assert np.all((alpha - a) % P == 0)
    assert np.array_equal(alpha, a - P * np.asarray(c.lift_correction))  # alpha = a - p z
    q, g = np.asarray(c.tree_potential), int(c.period_gcd)
    assert q[0] == 0 and g > 0 and g % P != 0
    assert np.array_equal(g * np.asarray(c.primitive) + q[edges[:, 1]] - q[edges[:, 0]], alpha)
    assert triangle_sums(c.primitive, edges, tris) == [0] * len(tris)


def test_fit_chart_phi_ascending_up_to_reflection(circle_chart):
    phi = np.asarray(circle_chart.phi)
    steps = np.angle(np.exp(1j * (np.roll(phi, -1) - phi)))
    assert np.all(steps > 0) or np.all(steps < 0)
    assert np.all(np.abs(steps) < 0.5)  # uniform would be 2pi/48 = 0.131
    idx = edge_index(circle_chart.edges)
    beta = np.asarray(circle_chart.primitive)
    winding = sum(int(beta[idx[(k, k + 1)]]) for k in range(47)) - int(beta[idx[(0, 47)]])
    assert abs(winding) == 1
    assert steps.sum() == pytest.approx(TWO_PI * winding, abs=1e-6)


def test_fit_chart_extension_scale_recomputed(circle_chart, dup_fit):
    for X, fitted in ((CIRCLE_X, circle_chart), dup_fit):
        d8 = eighth_neighbour(distance_matrix(X))
        assert np.allclose(fitted.d8, d8, rtol=1e-10, atol=1e-12)
        assert fitted.sigma == pytest.approx(float(np.median(d8)), rel=1e-10)
        expected_radius = 2.0 * float(np.quantile(d8, 0.99, method="inverted_cdf"))
        assert fitted.support_radius == pytest.approx(expected_radius, rel=1e-10)


def test_fit_chart_duplicate_counts_at_distance_zero(dup_fit):
    X, fitted = dup_fit
    assert np.array_equal(fitted.landmarks, X)  # input mutation after the fit has no effect
    dist = distance_matrix(X)
    assert dist[4, 5] == 0.0
    others = np.sort(np.delete(dist[4], [4, 5]))
    # the twin at distance 0 is the 1st neighbour, so d8 is the 7th non-twin distance
    assert fitted.d8[4] == pytest.approx(others[6], rel=1e-10)
    assert fitted.d8[4] < others[7]


@pytest.mark.parametrize("case", ["unsorted", "duplicate", "length", "few", "nan", "inf"])
def test_fit_chart_invalid_inputs(case):
    X = circle_points(TWO_PI * np.arange(12) / 12)
    landmark_ids = make_ids(12)
    if case == "unsorted":
        landmark_ids = landmark_ids[[1, 0] + list(range(2, 12))]
    elif case == "duplicate":
        landmark_ids[5] = landmark_ids[4]
    elif case == "length":
        landmark_ids = landmark_ids[:11]
    elif case == "few":
        X, landmark_ids = circle_points(TWO_PI * np.arange(8) / 8), make_ids(8)
    elif case == "nan":
        X[3, 1] = np.nan
    else:
        X[2, 0] = np.inf
    with pytest.raises(errors.Invalid):
        chart.fit_chart(X, landmark_ids, make_cfg())


def hexagon_clusters(spread):
    rows = [[math.cos(k * math.pi / 3), math.sin(k * math.pi / 3), spread * j]
            for k in range(6) for j in range(9)]
    return np.asarray(rows, dtype=np.float64)


def test_fit_chart_zero_bandwidth_unresolved():
    # 6 hexagon sites x 9 exact copies: a clear H1 bar (side 1 to diagonal sqrt 3), but every
    # point has 8 others at distance 0, so d8 == 0 everywhere and sigma = 0.
    X = hexagon_clusters(0.0)
    assert np.all(eighth_neighbour(distance_matrix(X)) == 0.0)
    with pytest.raises(errors.Unresolved):
        chart.fit_chart(X, make_ids(54), make_cfg())


def test_fit_chart_spread_clusters_positive_bandwidth():
    X = hexagon_clusters(1e-3)  # control: same topology, copies 1e-3 apart
    fitted = chart.fit_chart(X, make_ids(54), make_cfg())
    d8 = eighth_neighbour(distance_matrix(X))
    assert fitted.sigma > 0 and fitted.sigma == pytest.approx(float(np.median(d8)), rel=1e-9)


# ---------------------------------------------------------------------------------------- A10
def explicit_c(phi, m32, s):
    return np.mean(np.exp(1j * s * phi) * np.conj(m32[:, 0] + 1j * m32[:, 1]))


@pytest.mark.parametrize("s0, t0", [(-1, 0.7), (1, -2.0)])
def test_fit_gauge_sign_shift_alignment(circle_chart, s0, t0):
    phi = np.asarray(circle_chart.phi)
    m32 = unit_columns(s0 * phi - t0, 0.5)
    assert abs(explicit_c(phi, m32, s0)) == pytest.approx(0.5, abs=1e-12)
    assert abs(explicit_c(phi, m32, -s0)) < 0.25
    gauge = chart.fit_gauge(circle_chart, m32)
    assert int(gauge.sign) == s0
    assert gauge.shift == pytest.approx(t0, abs=1e-9)
    assert gauge.alignment == pytest.approx(0.5, abs=1e-12)
    gauged = np.asarray(chart.apply_gauge(phi, gauge))
    assert np.all(gauged >= 0.0) and np.all(gauged < TWO_PI)
    assert np.max(np.abs(np.exp(1j * gauged) - np.exp(1j * (s0 * phi - t0)))) < 1e-9


def test_apply_gauge_known_values():
    gauge = chart.Gauge(sign=-1, shift=0.5, alignment=1.0)
    out = np.asarray(chart.apply_gauge(np.array([0.0, math.pi / 2, 1.0]), gauge))
    assert np.allclose(out, [TWO_PI - 0.5, 1.5 * math.pi - 0.5, TWO_PI - 1.5], rtol=0,
                       atol=1e-12)


def test_fit_gauge_exact_tie_chooses_plus(circle_chart):
    flat = dataclasses.replace(circle_chart, phi=np.zeros(48))  # c_+ == c_- bit for bit
    gauge = chart.fit_gauge(flat, unit_columns(np.full(48, 1.0)))
    assert int(gauge.sign) == 1
    assert gauge.shift == pytest.approx(-1.0, abs=1e-12)  # c = mean(conj(e^{i})) = e^{-i}
    assert gauge.alignment == pytest.approx(1.0, abs=1e-12)


def test_fit_gauge_alignment_zero_unresolved(circle_chart):
    with pytest.raises(errors.Unresolved):
        chart.fit_gauge(circle_chart, np.zeros((48, 2)))


@pytest.mark.parametrize("bad", ["nan", "inf", "cols", "rows"])
def test_fit_gauge_invalid_inputs(circle_chart, bad):
    m32 = unit_columns(CIRCLE_THETA)
    if bad == "nan":
        m32[3, 0] = np.nan
    elif bad == "inf":
        m32[7, 1] = np.inf
    elif bad == "cols":
        m32 = np.column_stack([m32, np.ones(48)])
    else:
        m32 = m32[:47]
    with pytest.raises(errors.Invalid):
        chart.fit_gauge(circle_chart, m32)


def snapshot(c):
    snap = {name: np.array(getattr(c, name), copy=True) for name in ARRAY_FIELDS}
    snap.update(sigma=c.sigma, support_radius=c.support_radius, period_gcd=c.period_gcd)
    return snap


def assert_same(c, snap):
    for name in ARRAY_FIELDS:
        assert np.array_equal(np.asarray(getattr(c, name)), snap[name])
    assert (c.sigma, c.support_radius, c.period_gcd) == (
        snap["sigma"], snap["support_radius"], snap["period_gcd"])


def test_gauge_isolation_from_validation_arrays(circle_chart):
    m32 = unit_columns(CIRCLE_THETA)
    first = chart.fit_gauge(circle_chart, m32)
    snap = snapshot(circle_chart)
    for shift in (0.05, 1.3):
        ext = chart.extend(circle_chart, first, circle_points(CIRCLE_THETA + shift), make_cfg())
        chart.chart_gates(ext, np.mod(CIRCLE_THETA + 0.4, TWO_PI), make_cfg())
    assert_same(circle_chart, snap)
    second = chart.fit_gauge(circle_chart, m32)
    assert (second.sign, second.shift, second.alignment) == (
        first.sign, first.shift, first.alignment)
    refit = chart.fit_chart(CIRCLE_X.copy(), make_ids(48), make_cfg())
    assert np.array_equal(refit.phi, circle_chart.phi)
