"""Independent synthetic tests, author A (spec v2.3): cochain complexes, explicit checks,
primitive class and smoothing (TEST_PLAN A1, A3, A6, A7).

Written from tools/x4_circle_history/API.md, CONTRACT.json and TEST_PLAN.md only. Every expected
value below is hand-derived in the comments; production code only produces results.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG = REPO_ROOT / "tools" / "x4_circle_history"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import cochain  # noqa: E402
import errors  # noqa: E402

pytestmark = pytest.mark.analysis

P = 47
TWO_PI = 2.0 * math.pi
NO_TRIANGLES = np.zeros((0, 3), dtype=np.int64)
EXPECTED_CHART_CFG = {
    "field": 47, "lift_bounds": [1, 2, 4, 8, 16], "lift_node_limit": 128,
    "lift_cpu_cap_s": 30, "lift_rounding_tol": 1e-7, "local_passes": 2, "local_vertices": 128,
    "extension_k": 8, "support_min_resultant": 0.2, "fidelity_min_agreement": 0.8,
    "phase_bins": 12, "phase_bin_min_rows": 8, "overall_resultant_max": 0.3,
    "smoothing_residual_max": 1e-8,
}


def as_int(values):
    return np.asarray(values, dtype=np.int64)


K4_EDGES = as_int([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])
K4_TRIS = as_int([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
C4_EDGES = as_int([[0, 1], [0, 3], [1, 2], [2, 3]])  # cycle 0-1-2-3-0, lexicographic


def edge_index(edges):
    return {(int(i), int(j)): e for e, (i, j) in enumerate(np.asarray(edges).tolist())}


def triangle_sums(c, edges, triangles):
    """Explicit c(j,k) - c(i,k) + c(i,j) for every triangle, as Python ints."""
    idx = edge_index(edges)
    vals = [int(v) for v in np.asarray(c).tolist()]
    tris = np.asarray(triangles, dtype=np.int64).reshape(-1, 3).tolist()
    return [vals[idx[(j, k)]] - vals[idx[(i, k)]] + vals[idx[(i, j)]] for i, j, k in tris]


def coboundary(f, edges):
    return [int(f[j]) - int(f[i]) for i, j in np.asarray(edges).tolist()]


def test_contract_chart_keys_match_job_values():
    chart_cfg = json.loads((PKG / "CONTRACT.json").read_text(encoding="utf-8"))["chart"]
    assert {key: chart_cfg[key] for key in EXPECTED_CHART_CFG} == EXPECTED_CHART_CFG
    assert chart_cfg["ripser"] == {
        "maxdim": 1, "coeff": 47, "distance_matrix": True, "do_cocycles": True}


# ----------------------------------------------------------------------------------------- A1
def hand_distance_matrix():
    upper = {(0, 1): 0.5, (0, 2): 1.0, (0, 3): 1.5, (0, 4): 2.0, (1, 2): 0.7, (1, 3): 0.9,
             (1, 4): 1.0000001, (2, 3): 0.3, (2, 4): 3.0, (3, 4): 0.8}
    dist = np.zeros((5, 5), dtype=np.float64)
    for (i, j), value in upper.items():
        dist[i, j] = value
        dist[j, i] = value
    return dist


def test_edge_list_hand_graph_inclusive_and_lexicographic():
    dist = hand_distance_matrix()
    edges = np.asarray(cochain.edge_list(dist, 1.0))
    assert edges.dtype == np.int64
    # D[0,2] == radius is kept (<=); D[1,4] = 1.0000001 is dropped; diagonal never appears.
    assert edges.tolist() == [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4]]
    assert np.asarray(cochain.edge_list(dist, 0.75)).tolist() == [[0, 1], [1, 2], [2, 3]]
    assert np.asarray(cochain.edge_list(dist, 0.1)).shape == (0, 2)


def test_triangle_system_hand_graph_rows():
    edges = as_int([[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4]])
    d1, tris = cochain.triangle_system(edges, 5)
    tris = np.asarray(tris)
    assert tris.dtype == np.int64
    # (0,1,3), (1,3,4), (2,3,4), (0,2,3) miss an edge; only two filled triangles remain.
    assert tris.tolist() == [[0, 1, 2], [1, 2, 3]]
    assert scipy.sparse.issparse(d1) and d1.format == "csr" and d1.dtype == np.int64
    assert d1.shape == (2, 6)
    # (0,1,2): +1 on (1,2)=col2, -1 on (0,2)=col1, +1 on (0,1)=col0
    # (1,2,3): +1 on (2,3)=col4, -1 on (1,3)=col3, +1 on (1,2)=col2
    assert d1.toarray().tolist() == [[1, -1, 1, 0, 0, 0], [0, 0, 1, -1, 1, 0]]
    a = as_int([5, -2, 7, 11, -3, 4])
    # explicit sums: 7 - (-2) + 5 = 14 and -3 - 11 + 7 = -7
    assert triangle_sums(a, edges, tris) == [14, -7]
    assert np.asarray(d1 @ a).ravel().tolist() == [14, -7]


def test_triangle_system_k4_and_tree():
    d1, tris = cochain.triangle_system(K4_EDGES, 4)
    assert np.asarray(tris).tolist() == K4_TRIS.tolist()
    assert d1.toarray().tolist() == [
        [1, -1, 0, 1, 0, 0],   # (0,1,2): +(1,2) -(0,2) +(0,1)
        [1, 0, -1, 0, 1, 0],   # (0,1,3): +(1,3) -(0,3) +(0,1)
        [0, 1, -1, 0, 0, 1],   # (0,2,3): +(2,3) -(0,3) +(0,2)
        [0, 0, 0, 1, -1, 1],   # (1,2,3): +(2,3) -(1,3) +(1,2)
    ]
    path = as_int([[0, 1], [1, 2], [2, 3]])
    d1_path, tris_path = cochain.triangle_system(path, 4)
    assert np.asarray(tris_path).shape == (0, 3)
    assert d1_path.shape == (0, 3)


# ----------------------------------------------------------------------------------------- A3
def test_check_closure_explicit():
    edges3 = as_int([[0, 1], [0, 2], [1, 2]])
    tri = as_int([[0, 1, 2]])
    assert cochain.check_closure(as_int([3, 5, 2]), edges3, tri) is None  # 2 - 5 + 3 = 0
    with pytest.raises(errors.Invalid):
        cochain.check_closure(as_int([20, -7, 20]), edges3, tri)  # 20 + 7 + 20 = 47 != 0
    # 47*z on K4 is closed mod 47 on every triangle but its integral sums are 47*(1,3,3,1).
    modular = 47 * as_int([1, 1, -1, 1, 1, 1])
    assert triangle_sums(modular, K4_EDGES, K4_TRIS) == [47, 141, 141, 47]
    with pytest.raises(errors.Invalid):
        cochain.check_closure(modular, K4_EDGES, K4_TRIS)
    exact = as_int(coboundary([0, 3, -5, 7], K4_EDGES))
    cochain.check_closure(exact, K4_EDGES, K4_TRIS)
    exact[5] += 1  # breaks only (0,2,3) and (1,2,3)
    with pytest.raises(errors.Invalid):
        cochain.check_closure(exact, K4_EDGES, K4_TRIS)


def test_check_congruence_explicit():
    a = as_int([3, 5, 2])
    assert cochain.check_congruence(a - 47 * as_int([1, -2, 0]), a, P) is None
    cochain.check_congruence(a.copy(), a, P)
    for bad in ([0, 1, 0], [0, 0, 46], [-48, 0, 0]):
        with pytest.raises(errors.Invalid):
            cochain.check_congruence(a + as_int(bad), a, P)


# ----------------------------------------------------------------------------------------- A6
def primitive(alpha, edges, n, triangles=NO_TRIANGLES):
    beta, q, g = cochain.primitive_class(as_int(alpha), as_int(edges), triangles, n, P)
    return np.asarray(beta), np.asarray(q), int(g)


def assert_decomposition(alpha, edges, beta, q, g):
    for e, (i, j) in enumerate(np.asarray(edges).tolist()):
        assert g * int(beta[e]) + int(q[j]) - int(q[i]) == int(alpha[e])


def test_primitive_class_cycle_known_period():
    alpha = [2, -1, 5, 3]  # on (0,1), (0,3), (1,2), (2,3)
    beta, q, g = primitive(alpha, C4_EDGES, 4)
    # BFS: 0 -> 1 (q=2), 0 -> 3 (q=0+alpha(0,3)=-1); then 1 -> 2 (q=2+5=7).
    # periods: (2,3) = 3 - (-1 - 7) = 11, all others 0; winding 2+5+3-(-1) = 11.
    # (Descending neighbour order would reach 2 from 3: q2=-4, beta=(0,0,1,0).)
    assert beta.dtype == np.int64 and q.dtype == np.int64
    assert g == 11
    assert q.tolist() == [0, 2, 7, -1]
    assert beta.tolist() == [0, 0, 0, 1]
    assert_decomposition(alpha, C4_EDGES, beta, q, g)


def test_primitive_class_bfs_not_dfs_order():
    edges = as_int([[0, 1], [0, 2], [1, 3], [2, 3]])  # cycle 0-1-3-2-0
    alpha = [4, 1, -2, 6]
    beta, q, g = primitive(alpha, edges, 4)
    # BFS from 0 discovers 1 (q=4) and 2 (q=1); dequeuing 1 discovers 3 (q=4-2=2).
    # periods: (2,3) = 6 - (2 - 1) = 5. A DFS 0->1->3->2 would give q2=-4, beta=(0,1,0,0).
    assert q.tolist() == [0, 4, 1, 2]
    assert g == 5
    assert beta.tolist() == [0, 0, 0, 1]
    assert_decomposition(alpha, edges, beta, q, g)


def test_primitive_class_gcd_of_two_periods():
    edges = as_int([[0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4]])  # K_{2,3}, no triangles
    alpha = [1, 2, 3, 4, 11, -3]
    beta, q, g = primitive(alpha, edges, 5)
    # q2=1, q3=2, q4=3 from 0; q1 = q2 + value(2->1) = 1 - 4 = -3.
    # periods (1,3) = 11 - (2+3) = 6, (1,4) = -3 - (3+3) = -9 -> g = 3, beta = (.., 2, -3).
    assert q.tolist() == [0, -3, 1, 2, 3]
    assert g == 3
    assert beta.tolist() == [0, 0, 0, 0, 2, -3]
    assert_decomposition(alpha, edges, beta, q, g)


def test_primitive_class_unresolved_cases():
    with pytest.raises(errors.Unresolved):  # exact: alpha = dq, all periods 0
        primitive(coboundary([0, 2, 7, -1], C4_EDGES), C4_EDGES, 4)
    exact_k4 = coboundary([0, 3, -5, 7], K4_EDGES)
    with pytest.raises(errors.Unresolved):  # closed on K4 triangles and exact
        primitive(exact_k4, K4_EDGES, 4, triangles=K4_TRIS)
    for winding in (47, 94):  # q = 0, the only period is on (2,3): g = 47 or 94
        with pytest.raises(errors.Unresolved):
            primitive([0, 0, 0, winding], C4_EDGES, 4)
    with pytest.raises(errors.Unresolved):  # vertex 4 is unreachable
        primitive([2, -1, 5, 3], C4_EDGES, 5)


def test_primitive_class_non_closed_alpha_invalid():
    # Single triangle, alpha=(1,0,0): q=(0,1,0), periods (0,0,1), g=1 (passes step 4), but
    # beta=(0,0,1) has triangle sum 1 - 0 + 0 = 1 != 0, so check_closure(beta) fails.
    edges = as_int([[0, 1], [0, 2], [1, 2]])
    with pytest.raises(errors.Invalid):
        primitive([1, 0, 0], edges, 3, triangles=as_int([[0, 1, 2]]))


# ----------------------------------------------------------------------------------------- A7
def assert_phases(phi, expected, tol=1e-9):
    phi = np.asarray(phi, dtype=np.float64)
    assert phi.shape == (len(expected),)
    assert np.all(phi >= 0.0) and np.all(phi < TWO_PI)
    gap = np.abs(np.exp(1j * phi) - np.exp(1j * np.asarray(expected, dtype=np.float64)))
    assert gap.max() < tol


def smooth(beta, edges, n):
    phi, residual = cochain.smooth_phase(as_int(beta), as_int(edges), n)
    residual = float(residual)
    assert 0.0 <= residual <= 1e-8
    return phi


def test_smooth_phase_cycle_four():
    # Harmonic h = beta + Bf is 1/4 on every edge oriented 0->1->2->3->0 (h(0,3) = -1/4):
    # f = (0, 1/4, 1/2, -1/4), so phi = 2*pi*(0, 1/4, 1/2, 3/4).
    phi = smooth([0, 0, 0, 1], C4_EDGES, 4)
    assert_phases(phi, TWO_PI * np.array([0.0, 0.25, 0.5, 0.75]))
    # winding 3: h = 3/4 per step, f = (0, 3/4, 3/2, -3/4) -> 2*pi*(0, 3/4, 1/2, 1/4)
    phi3 = smooth([0, 0, 0, 3], C4_EDGES, 4)
    assert_phases(phi3, TWO_PI * np.array([0.0, 0.75, 0.5, 0.25]))


def test_smooth_phase_cycle_five_winding_two():
    edges = as_int([[0, 1], [0, 4], [1, 2], [2, 3], [3, 4]])
    # beta = 1 on (0,1) and (2,3): h = 2/5 per oriented step, f = (0,-3/5,-1/5,-4/5,-2/5).
    phi = smooth([1, 0, 0, 1, 0], edges, 5)
    assert_phases(phi, TWO_PI * np.array([0.0, 0.4, 0.8, 0.2, 0.6]))


def test_smooth_phase_path_is_exact():
    # On a tree beta = -Bf exactly: f = (0, -1, -1, 1), all integers, so phi == 0 mod 2pi.
    phi = smooth([1, 0, -2], [[0, 1], [1, 2], [2, 3]], 4)
    assert_phases(phi, np.zeros(4))
    assert_phases(smooth([0, 0, 0], [[0, 1], [1, 2], [2, 3]], 4), np.zeros(4))


# A forced bad input for smooth_phase is NOT constructed: beta is an int64 array (cannot be
# non-finite) and for any graph the least-squares normal equations B^T(beta + Bf) = 0 are met to
# rounding by a correct solver, so the residual > 1e-8 branch is unreachable through the public
# API without patching internals, which an independent author cannot name.
