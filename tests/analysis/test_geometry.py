"""Independent tests N07, N08 for Delta_geom (RESEARCH_SUMMARY 7.5)."""
import numpy as np
import pytest
from scipy.stats import spearmanr

from topo_pilot.analysis import GeometryAlignment

pytestmark = pytest.mark.analysis


def mat_from_upper(vec, M):
    D = np.zeros((M, M))
    D[np.triu_indices(M, 1)] = vec
    return D + D.T


def pdist_mat(X):
    return np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))


def planted(M=40, seed=0):
    rng = np.random.default_rng(seed)
    X32 = rng.normal(size=(M, 5))
    XA = X32 + 0.1 * rng.normal(size=(M, 5))
    X1 = rng.normal(size=(M, 5))
    return pdist_mat(XA), pdist_mat(X32), pdist_mat(X1)


def test_delta_geom_known_answer_six_pairs():
    # pair order (0,1)(0,2)(0,3)(1,2)(1,3)(2,3); values in [5,10] keep triangle inequalities valid
    a = np.array([5, 6, 7, 8, 9, 10.0])
    D_A, D_32, D_1 = (mat_from_upper(v, 4) for v in (a, a, a[::-1]))
    assert GeometryAlignment().delta_geom(D_A, D_32, D_1)["all"] == pytest.approx(2.0)
    assert GeometryAlignment().delta_geom(D_A, D_1, D_32)["all"] == pytest.approx(-2.0)


def test_delta_geom_positive_for_planted_and_negative_when_swapped():
    D_A, D_32, D_1 = planted()
    iu = np.triu_indices(40, 1)
    expected = spearmanr(D_A[iu], D_32[iu])[0] - spearmanr(D_A[iu], D_1[iu])[0]
    g = GeometryAlignment()
    d = g.delta_geom(D_A, D_32, D_1)["all"]
    assert d > 0.3
    assert d == pytest.approx(expected)
    s = g.delta_geom(D_A, D_1, D_32)["all"]
    assert s < 0
    assert s == pytest.approx(-d)


def run_pairs(last):
    D_A, D_32, D_1 = planted(M=len(last), seed=1)
    return GeometryAlignment().delta_geom(D_A, D_32, D_1, last_symbol=np.asarray(last))


def test_same_pair_count_hand_array_and_inconclusive():
    out = run_pairs([0, 0, 0, 1, 1, 2, 3, 4])  # 3 + 1 pairs
    assert out["n_same_pairs"] == 4
    assert out["same_last_symbol"] is None
    assert out["status_same"] == "inconclusive"


def test_same_pairs_below_200_inconclusive():
    out = run_pairs(np.repeat(np.arange(4), 10))  # 4 * C(10,2) = 180
    assert out["n_same_pairs"] == 180
    assert out["same_last_symbol"] is None
    assert out["status_same"] == "inconclusive"


def test_same_pairs_199_inconclusive_and_200_ok():
    out = run_pairs([0] * 20 + [1] * 3 + [2] * 3 + [3] * 3 + [10, 11, 12, 13])  # 190 + 9
    assert out["n_same_pairs"] == 199
    assert out["status_same"] == "inconclusive" and out["same_last_symbol"] is None
    out = run_pairs([0] * 20 + [1] * 5 + [10, 11, 12, 13])  # 190 + 10
    assert out["n_same_pairs"] == 200
    assert out["status_same"] == "ok"
    assert isinstance(out["same_last_symbol"], float)


def test_same_last_symbol_value_matches_restricted_spearman():
    last = np.repeat(np.arange(2), 20)  # 2 * 190 = 380 same pairs
    D_A, D_32, D_1 = planted(M=40, seed=2)
    out = GeometryAlignment().delta_geom(D_A, D_32, D_1, last_symbol=last)
    iu = np.triu_indices(40, 1)
    keep = last[iu[0]] == last[iu[1]]
    exp = (spearmanr(D_A[iu][keep], D_32[iu][keep])[0]
           - spearmanr(D_A[iu][keep], D_1[iu][keep])[0])
    assert out["n_same_pairs"] == 380
    assert out["status_same"] == "ok"
    assert out["same_last_symbol"] == pytest.approx(exp)
    assert "all" in out
