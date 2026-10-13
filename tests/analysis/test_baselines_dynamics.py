"""Independent tests N11 (R2 baseline on a ring process) and N12 (checkpoint-order null)."""
import math

import numpy as np
import pytest

from topo_pilot.analysis import Dynamics, r2_points, r3_points, spectral_embedding
from topo_pilot.topology import (
    DistancePipeline,
    Euclidean,
    NullClouds,
    PersistenceComputer,
    PHConfig,
    Summaries,
)

pytestmark = pytest.mark.analysis

V = 12


def ring_process(eps=0.05):
    E = np.eye(V) * (1 - 2 * eps)
    T = np.zeros((V, V))
    for i in range(V):
        E[i, (i + 1) % V] += eps
        E[i, (i - 1) % V] += eps
        T[i, i] = 0.5
        T[i, (i + 1) % V] += 0.25
        T[i, (i - 1) % V] += 0.25
    return E, T, np.full(V, 1.0 / V)


def sample_histories(E, T, M, L, rng):
    state = rng.integers(0, V, size=M)
    out = np.empty((M, L), dtype=int)
    cumT, cumE = np.cumsum(T, 1), np.cumsum(E, 1)
    for t in range(L):
        u = rng.random(M)
        out[:, t] = np.minimum((u[:, None] > cumE[state]).sum(1), V - 1)
        v = rng.random(M)
        state = np.minimum((v[:, None] > cumT[state]).sum(1), V - 1)
    return out


def S_h1(X):
    res = DistancePipeline(Euclidean()).compute(X, [str(i) for i in range(len(X))])
    diag = PersistenceComputer(PHConfig()).diagrams(res.D)
    return Summaries.S(diag, 1, res.scale_s)


def test_spectral_embedding_shape_and_r2_r3_definitions():
    E, T, pi = ring_process()
    phi = spectral_embedding(E, T, pi, 8)
    assert phi.shape == (V, 8)
    hist = np.random.default_rng(1).integers(0, V, size=(3, 32))
    np.testing.assert_allclose(r2_points(hist, phi), 0.5 * (phi[hist[:, -1]] + phi[hist[:, -2]]))
    np.testing.assert_allclose(r3_points(hist, phi), phi[hist].mean(axis=1))


def test_r2_points_on_ring_process_have_h1_above_gaussian_null():
    E, T, pi = ring_process()
    rng = np.random.default_rng(0)
    phi = spectral_embedding(E, T, pi, 8)
    M = 120
    hist = sample_histories(E, T, M, 32, rng)
    X = np.asarray(r2_points(hist, phi), dtype=float)
    assert X.shape == (M, 8)
    s_r2 = S_h1(X)
    nulls = [S_h1(NullClouds.isotropic(M, X.shape[1], np.random.default_rng(100 + k)))
             for k in range(10)]
    assert s_r2 > max(nulls), (s_r2, max(nulls))


# ---------------------------------------------------------------- N12
def stat_ref(values):
    d = np.abs(np.diff(np.asarray(values, dtype=float)))
    k = math.ceil((len(values) - 1) / 3)
    return d[:k].sum() / d.sum()


EARLY = np.array([0, 2, 4, 6, 8, 10, 10.01, 10.0, 10.02, 10.01, 10.02, 10.01])


def test_checkpoint_order_statistic_hand_values():
    # [0,1,3,4,4,5,9]: |dS| = 1,2,1,0,1,4 (sum 9); k = ceil(6/3) = 2 -> 3/9
    out = Dynamics().checkpoint_order_null(np.array([0, 1, 3, 4, 4, 5, 9.0]), 50,
                                           np.random.default_rng(0))
    assert out["statistic"] == pytest.approx(1 / 3)
    assert 0.0 < out["p_value"] <= 1.0
    out = Dynamics().checkpoint_order_null(np.array([0, 6, 6, 6, 6, 6, 6.0]), 50,
                                           np.random.default_rng(0))
    assert out["statistic"] == pytest.approx(1.0)


def test_p_value_has_plus_one_form():
    out = Dynamics().checkpoint_order_null(EARLY, 99, np.random.default_rng(1))
    p100 = out["p_value"] * 100  # (1 + count) / (1 + 99)
    assert p100 >= 1 - 1e-9
    assert abs(p100 - round(p100)) < 1e-9


def test_early_jump_gives_small_p():
    out = Dynamics().checkpoint_order_null(EARLY, 2000, np.random.default_rng(2))
    assert out["statistic"] == pytest.approx(stat_ref(EARLY))
    assert out["p_value"] < 0.05


def test_p_value_matches_independent_monte_carlo():
    rng = np.random.default_rng(5)
    obs = stat_ref(EARLY)
    mc = np.mean([stat_ref(rng.permutation(EARLY)) >= obs - 1e-12 for _ in range(4000)])
    p = Dynamics().checkpoint_order_null(EARLY, 2000, np.random.default_rng(6))["p_value"]
    assert abs(p - mc) < 0.03


def test_random_sequences_are_not_systematically_small_p():
    rng = np.random.default_rng(11)
    ps = [Dynamics().checkpoint_order_null(rng.normal(size=12), 200, rng)["p_value"]
          for _ in range(50)]
    assert np.mean(np.array(ps) < 0.05) <= 0.2
