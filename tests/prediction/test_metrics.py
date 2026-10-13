"""R01, R02, R06, R07, R08: predictive metrics, learning gate, bootstrap, join."""

import math

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, StageFailure, Status
from topo_pilot.prediction import LearningGate, PredictiveMetrics, join_by_history_id

pytestmark = pytest.mark.prediction


def test_R01_kl_zero_hand_value_and_nonnegative():
    q = np.array([[0.25, 0.75], [1.0, 0.0]])
    np.testing.assert_allclose(PredictiveMetrics.kl(q, q), 0.0, atol=1e-15)
    p = np.array([[0.5, 0.5]])
    expected = 0.5 * math.log(2.0) + 0.5 * math.log(2.0 / 3.0)
    np.testing.assert_allclose(PredictiveMetrics.kl(p, np.array([[0.25, 0.75]])), [expected])
    rng = np.random.default_rng(0)
    a = rng.dirichlet(np.ones(5), size=50)
    b = rng.dirichlet(np.ones(5), size=50)
    assert np.all(PredictiveMetrics.kl(a, b) >= 0.0)


def test_R01_kl_zero_log_zero_convention_and_regret_mean():
    p = np.array([[1.0, 0.0], [0.5, 0.5]])
    q = np.array([[0.5, 0.5], [0.5, 0.5]])
    np.testing.assert_allclose(PredictiveMetrics.kl(p, q), [math.log(2.0), 0.0], atol=1e-15)
    assert PredictiveMetrics.regret(p, q) == pytest.approx(math.log(2.0) / 2)


def test_R01_kl_error_paths():
    good = np.array([[0.5, 0.5]])
    with pytest.raises(StageFailure) as exc:
        PredictiveMetrics.kl(np.array([[0.5, 0.5]]), np.array([[1.0, 0.0]]))
    assert exc.value.code == ErrorCode.NUMERICAL_FAILURE and exc.value.check == "support"
    with pytest.raises(StageFailure) as exc:
        PredictiveMetrics.kl(good, np.array([[0.5, 0.4]]))
    assert exc.value.code == ErrorCode.NUMERICAL_FAILURE and exc.value.check == "normalised"
    with pytest.raises(StageFailure):
        PredictiveMetrics.nll(np.array([[0.7, 0.7]]), np.array([0]))


def test_R02_nll_uniform_is_log_v():
    for v in (2, 7):
        probs = np.full((4, v), 1.0 / v)
        np.testing.assert_allclose(PredictiveMetrics.nll(probs, np.arange(4) % v), math.log(v))


def test_R02_nll_picks_target_column():
    probs = np.array([[0.1, 0.9], [0.8, 0.2]])
    np.testing.assert_allclose(PredictiveMetrics.nll(probs, np.array([1, 0])),
                               [-math.log(0.9), -math.log(0.8)])


def test_R06_captured_and_gate_hand_values():
    assert PredictiveMetrics.captured(0.05, 0.5) == pytest.approx(0.9)
    gate = LearningGate()
    check, status = gate.evaluate_with_status(0.9)
    assert (check.name, check.passed, check.value, check.threshold) == ("learning_gate", True,
                                                                         0.9, 0.8)
    assert status == Status.OK
    low, status = gate.evaluate_with_status(0.7)
    assert low.passed is False and low.value == 0.7 and status == Status.OK
    assert gate.evaluate(0.8).passed is True


def test_R06_zero_context_gain_is_inconclusive():
    captured = PredictiveMetrics.captured(0.1, 1e-7)
    assert math.isnan(captured)
    check, status = LearningGate().evaluate_with_status(captured)
    assert status == Status.INCONCLUSIVE and check.passed is False and check.value is None
    assert LearningGate().evaluate(captured).value is None


def test_R07_bootstrap_resamples_groups_not_rows():
    group_means = np.array([0.0, 1.0, 2.0, 3.0])
    values = np.repeat(group_means, 5)
    groups = np.repeat(np.arange(4), 5)
    ci = PredictiveMetrics.bootstrap_ci(values, groups, 500, np.random.default_rng(1))
    ref = PredictiveMetrics.bootstrap_ci(group_means, np.arange(4), 500, np.random.default_rng(1))
    assert ci == pytest.approx(ref)
    assert 0.0 < ci[0] < 1.5 < ci[1] < 3.0


def test_R07_constant_array_has_degenerate_ci():
    lo, hi = PredictiveMetrics.bootstrap_ci(np.full(20, 2.5), np.repeat(np.arange(4), 5), 100,
                                            np.random.default_rng(0))
    assert lo == pytest.approx(2.5) and hi == pytest.approx(2.5)


def test_R08_join_returns_alignment_permutation():
    a = np.array(["x", "y", "z"])
    b = np.array(["z", "x", "y"])
    idx = join_by_history_id(a, b)
    assert b[idx].tolist() == a.tolist()


@pytest.mark.parametrize("ids_b", [["x", "y"], ["x", "y", "w"], ["x", "y", "y"]])
def test_R08_join_mismatch_raises(ids_b):
    with pytest.raises(StageFailure) as exc:
        join_by_history_id(np.array(["x", "y", "z"]), np.array(ids_b))
    assert exc.value.code == ErrorCode.JOIN_CARDINALITY
