"""T03, T04, T05, T08, T09, T10 and contract checks for PH, summaries, landmarks."""
import math

import numpy as np
import pytest
from scipy.spatial.distance import cdist

from topo_pilot.contracts import ErrorCode, StageFailure, Status
from topo_pilot.topology import (
    DistancePipeline,
    Euclidean,
    PersistenceComputer,
    PHConfig,
    Summaries,
)

pytestmark = pytest.mark.topology


def ids(n):
    return [f"p{i}" for i in range(n)]


def circle_pts(m, radius=1.0, ambient=2):
    th = 2 * np.pi * np.arange(m) / m
    X = np.zeros((m, ambient))
    X[:, 0], X[:, 1] = radius * np.cos(th), radius * np.sin(th)
    return X


def noisy_circle(m, seed, ambient=8, noise=0.02):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, m)
    X = np.zeros((m, ambient))
    X[:, 0], X[:, 1] = np.cos(th), np.sin(th)
    return X + noise * rng.normal(size=X.shape)


def rows_of(diag):
    return np.asarray(diag.rows, dtype=np.float64)


def bars(diag, dim):
    r = rows_of(diag)
    return r[r[:, 0] == dim]


def sorted_rows(r):
    r = np.asarray(r, dtype=np.float64)
    return r[np.lexsort((r[:, 3], r[:, 2], r[:, 1], r[:, 0]))]


def test_T03_unit_square_known_answer():
    # Corners of a unit square: sides 1, diagonals sqrt2.  One H1 class born when the
    # 4-cycle closes (1) and killed when the diagonals enter (sqrt2).
    P = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    D = cdist(P, P)
    diag = PersistenceComputer(PHConfig(maxdim=1)).diagrams(D)
    r = rows_of(diag)
    assert r.ndim == 2 and r.shape[1] == 4 and r.dtype == np.float64
    h1 = bars(diag, 1)
    assert h1.shape[0] == 1
    np.testing.assert_allclose(h1[0, 1:3], [1.0, math.sqrt(2.0)], atol=1e-6)  # ripser is float32
    assert h1[0, 3] == 0
    h0 = bars(diag, 0)
    assert h0.shape[0] == 4
    assert np.sum(np.isinf(h0[:, 2])) == 1 and np.all(h0[:, 3] == 0)
    np.testing.assert_allclose(np.sort(h0[np.isfinite(h0[:, 2]), 2]), [1, 1, 1], atol=1e-6)
    assert diag.coeff_p == 2 and diag.maxdim == 1


def test_T04_scale_covariance():
    X = noisy_circle(70, seed=1)
    c = 3.7
    r1 = DistancePipeline(Euclidean()).compute(X, ids(70))
    r2 = DistancePipeline(Euclidean()).compute(c * X, ids(70))
    d1 = PersistenceComputer(PHConfig()).diagrams(r1.D)
    d2 = PersistenceComputer(PHConfig()).diagrams(r2.D)
    a, b = sorted_rows(rows_of(d1)), sorted_rows(rows_of(d2))
    assert a.shape == b.shape
    scaled = a.copy()
    scaled[:, 1:3] *= c  # inf stays inf
    # ripser stores float32
    np.testing.assert_allclose(b[:, 1:3], scaled[:, 1:3], rtol=1e-5, atol=1e-6)
    np.testing.assert_array_equal(a[:, [0, 3]], b[:, [0, 3]])
    np.testing.assert_allclose(r2.scale_s, c * r1.scale_s, rtol=1e-9)
    s1 = Summaries.S(d1, 1, r1.scale_s)
    s2 = Summaries.S(d2, 1, r2.scale_s)
    assert s1 > 0
    np.testing.assert_allclose(s1, s2, rtol=1e-5)


def test_scale_s_is_q95_of_positive_distances():
    X = noisy_circle(50, seed=2)
    res = DistancePipeline(Euclidean()).compute(X, ids(50))
    D = cdist(X, X)
    pos = D[np.triu_indices(50, 1)]
    pos = pos[pos > 0]
    # numpy default (linear interpolation) percentile convention
    np.testing.assert_allclose(res.scale_s, np.percentile(pos, 95), rtol=1e-6)
    assert res.status == Status.OK
    assert len(res.point_ids) == res.D.shape[0] == 50


def test_T05_permutation_invariance():
    X = noisy_circle(60, seed=3)
    perm = np.random.default_rng(4).permutation(60)
    D = cdist(X, X)
    cfg = PHConfig()
    a = sorted_rows(rows_of(PersistenceComputer(cfg).diagrams(D)))
    b = sorted_rows(rows_of(PersistenceComputer(cfg).diagrams(D[np.ix_(perm, perm)])))
    assert a.shape == b.shape
    np.testing.assert_allclose(a, b, atol=1e-12)
    # and through the full pipeline
    r1 = DistancePipeline(Euclidean()).compute(X, ids(60))
    r2 = DistancePipeline(Euclidean()).compute(X[perm], [ids(60)[i] for i in perm])
    c = sorted_rows(rows_of(PersistenceComputer(cfg).diagrams(r1.D)))
    d = sorted_rows(rows_of(PersistenceComputer(cfg).diagrams(r2.D)))
    np.testing.assert_allclose(c, d, atol=1e-6)
    np.testing.assert_allclose(r1.scale_s, r2.scale_s, rtol=1e-9)


def test_T08_dedup_same_diagrams():
    X = noisy_circle(60, seed=5)
    X_dup = np.vstack([X, X[:15], X[5:10]])
    r_u = DistancePipeline(Euclidean()).compute(X, ids(60))
    r_d = DistancePipeline(Euclidean()).compute(X_dup, ids(len(X_dup)))
    assert r_d.D.shape == (60, 60)
    assert len(r_d.point_ids) == 60
    assert r_d.dedup_map is not None and len(r_d.dedup_map) >= 60
    np.testing.assert_allclose(r_d.scale_s, r_u.scale_s, rtol=1e-9)
    a = sorted_rows(rows_of(PersistenceComputer(PHConfig()).diagrams(r_u.D)))
    b = sorted_rows(rows_of(PersistenceComputer(PHConfig()).diagrams(r_d.D)))
    np.testing.assert_allclose(a, b, atol=1e-6)


def test_T08_all_identical_cloud_collapsed():
    X = np.tile(np.array([[1.0, -2.0, 3.0]]), (12, 1))
    res = DistancePipeline(Euclidean()).compute(X, ids(12))
    assert res.status == Status.COLLAPSED
    assert res.scale_s == 0.0


def test_T08_all_zero_D_collapsed_and_S_zero():
    D = np.zeros((6, 6))
    diag = PersistenceComputer(PHConfig()).diagrams(D)
    assert diag.status == Status.COLLAPSED
    assert Summaries.S(diag, 1, 0.0) == 0.0


def test_T09_small_threshold_marks_censored_not_dropped():
    X = circle_pts(60)  # H1 born ~0.1, dies ~1.7 (well after threshold 0.5)
    D = cdist(X, X)
    diag = PersistenceComputer(PHConfig(threshold=0.5)).diagrams(D)
    h1 = bars(diag, 1)
    assert h1.shape[0] >= 1, "H1 bar was dropped instead of censored"
    assert np.all(np.isinf(h1[:, 2])) and np.all(h1[:, 3] == 1)
    h0 = bars(diag, 0)
    ess = h0[np.isinf(h0[:, 2])]
    assert ess.shape[0] == 1 and ess[0, 3] == 0  # H0 essential bar is not censored
    assert diag.threshold == pytest.approx(0.5)
    # censored bars are not finite: they do not contribute to S
    assert Summaries.S(diag, 1, 1.0) == 0.0
    # auto threshold closes every H1 bar
    auto = PersistenceComputer(PHConfig()).diagrams(D)
    h1a = bars(auto, 1)
    assert h1a.shape[0] >= 1 and np.all(np.isfinite(h1a[:, 2])) and np.all(h1a[:, 3] == 0)
    assert auto.threshold == pytest.approx(D.max())
    assert Summaries.S(auto, 1, 1.0) > 1.0


@pytest.mark.parametrize("make_bad", [
    lambda D: np.triu(D) + 0.3 * np.tril(np.ones_like(D), -1),   # asymmetric
    lambda D: D - 5.0 * (1 - np.eye(len(D))),                     # negative entries
    lambda D: D + 0.5 * np.eye(len(D)),                           # nonzero diagonal
])
def test_non_metric_input_raises(make_bad):
    X = noisy_circle(20, seed=7)
    D = cdist(X, X)
    with pytest.raises(StageFailure) as ei:
        PersistenceComputer(PHConfig()).diagrams(make_bad(D))
    assert ei.value.code == ErrorCode.NON_METRIC


def test_summaries_hand_values():
    inf = np.inf
    rows = np.array([[0, 0.0, inf, 0], [0, 0.0, 1.0, 0],
                     [1, 0.2, 0.7, 0], [1, 0.1, inf, 1], [1, 0.5, 0.6, 0]])
    # finite H1 bars: (0.2,0.7) persistence .5 ; (0.5,0.6) persistence .1 ; inf excluded.
    assert Summaries.S(rows, 1, 0.5) == pytest.approx(1.0)
    assert Summaries.S(rows, 2, 0.5) == 0.0
    assert Summaries.pi_max(rows, 1) == pytest.approx(3.5)  # max(.7/.2, .6/.5)
    top = np.asarray(Summaries.top_k_persistence(rows, 1, k=3))
    np.testing.assert_allclose(top[:2], [0.5, 0.1], atol=1e-12)
    assert top.size in (2, 3) and (top.size == 2 or top[2] == 0.0)
    fin = np.array([[1, 0.2, 0.7, 0], [1, 0.5, 0.6, 0]])
    grid = np.array([0.1, 0.3, 0.55, 0.65, 0.8])  # points away from all endpoints
    np.testing.assert_array_equal(np.asarray(Summaries.betti_curve(fin, 1, grid)),
                                  [0, 1, 2, 1, 0])


def test_maxmin_landmarks():
    X = noisy_circle(80, seed=8)
    D = cdist(X, X)
    pc = PersistenceComputer(PHConfig())
    a = np.asarray(pc.maxmin_landmarks(D, 12, np.random.default_rng(0)))
    b = np.asarray(pc.maxmin_landmarks(D, 12, np.random.default_rng(0)))
    assert a.shape == (12,) and len(set(a.tolist())) == 12
    assert a.min() >= 0 and a.max() < 80
    np.testing.assert_array_equal(a, b)
    # maxmin property: every point is within the covering radius of some landmark, and the
    # landmarks are mutually at least that far apart (greedy farthest-point guarantee).
    cover = D[:, a].min(axis=1).max()
    sub = D[np.ix_(a, a)] + np.eye(12) * 1e9
    assert sub.min() >= cover - 1e-12


def rp2_sample(m, seed):
    """Veronese embedding x -> x x^T of random points on S^2: an embedded RP^2 in R^9."""
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(m, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return np.einsum("ni,nj->nij", v, v).reshape(m, 9)


@pytest.mark.slow
def test_T10_coeff_p_passed_through():
    # RP^2 has H1 = Z/2: beta_1 = 1 over F2, 0 over F3.  Over F3 only short noise bars
    # remain (measured offline with raw ripser at M=400: S ~0.7 for p=2, ~0.22 for p=3).
    Y = rp2_sample(400, seed=0)
    D = cdist(Y, Y)
    s = np.percentile(D[np.triu_indices(400, 1)], 95)
    d2 = PersistenceComputer(PHConfig(coeff_p=2)).diagrams(D)
    d3 = PersistenceComputer(PHConfig(coeff_p=3)).diagrams(D)
    assert d2.coeff_p == 2 and d3.coeff_p == 3
    s2, s3 = Summaries.S(d2, 1, s), Summaries.S(d3, 1, s)
    assert s2 > 0.4
    assert s2 > 2.0 * s3, (s2, s3)
