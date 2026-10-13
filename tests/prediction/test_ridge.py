"""R09, R10: ridge probe."""

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.prediction import RidgeProbe

pytestmark = pytest.mark.prediction


def planted(seed=0, n=300):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 5))
    W = rng.normal(size=(5, 3))
    Y = X @ W + 2.0 + 0.01 * rng.normal(size=(n, 3))
    return X, Y, W


def test_R09_recovers_planted_affine_map():
    X, Y, W = planted()
    probe = RidgeProbe([1e-6, 1e-2, 10.0]).fit(X[:200], Y[:200], X[200:250], Y[200:250])
    scores = probe.score(X[250:], Y[250:])
    assert scores["r2"] > 0.99 and probe.lam == 1e-6
    np.testing.assert_allclose(probe.W, W, atol=0.01)
    np.testing.assert_allclose(probe.b, 2.0, atol=0.01)


def test_R09_shuffled_labels_give_near_zero_r2():
    X, Y, _ = planted(seed=1)
    perm = np.random.default_rng(2).permutation(200)
    probe = RidgeProbe([1.0, 100.0]).fit(X[:200], Y[:200][perm], X[200:250], Y[200:250])
    assert abs(probe.score(X[250:], Y[250:])["r2"]) < 0.1


def test_ridge_intercept_unpenalised_and_lambda_chosen_on_val():
    X = np.array([[0.0], [1.0], [2.0], [3.0]])
    Y = 10.0 + X[:, 0]
    probe = RidgeProbe([0.0]).fit(X, Y, X, Y)
    np.testing.assert_allclose(probe.predict(X)[:, 0], Y, atol=1e-10)
    huge = RidgeProbe([1e9]).fit(X, Y, X, Y)
    np.testing.assert_allclose(huge.predict(X)[:, 0], Y.mean(), atol=1e-4)


def test_R10_probe_fit_touching_test_raises_leakage():
    X, Y, _ = planted()
    with pytest.raises(StageFailure) as exc:
        RidgeProbe([1.0]).fit(X[:100], Y[:100], X[100:150], Y[100:150], splits=("dev_fit", "test"))
    assert exc.value.code == ErrorCode.LEAKAGE and exc.value.check == "probe_split"
    RidgeProbe([1.0]).fit(X[:100], Y[:100], X[100:150], Y[100:150])
