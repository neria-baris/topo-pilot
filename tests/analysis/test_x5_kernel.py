"""Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
before reading the implementation.

Exact process diagnostics (protocol x5g1-feas-v2 §3.2, API §2 ``x5_kernel``): movement rate,
connectivity, spectrum with the ceil mixing bound and statuses, integrated autocorrelation of
state functions, and the rate-matched flat kernel.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from topo_pilot.analysis import (
    SpectrumReport,
    integrated_autocorrelation,
    is_connected,
    movement_rate,
    rate_matched_kernel,
    spectrum_report,
)
from topo_pilot.contracts.testing import tiny_hmm

pytestmark = pytest.mark.analysis


def _two_state(p: float) -> np.ndarray:
    return np.array([[1.0 - p, p], [p, 1.0 - p]])


def _blocks() -> np.ndarray:
    """Block-diagonal (reducible) 4-state chain: two lazy 2-state blocks."""
    T = np.zeros((4, 4))
    T[:2, :2] = _two_state(0.3)
    T[2:, 2:] = _two_state(0.4)
    return T


HALF = np.array([0.5, 0.5])
U4 = np.full(4, 0.25)


# ---------------------------------------------------------------- movement rate


def test_movement_rate_hand_value_nonuniform_pi():
    T = np.array([[0.9, 0.1], [0.2, 0.8]])
    pi = np.array([2.0 / 3.0, 1.0 / 3.0])
    assert movement_rate(T, pi) == pytest.approx(2 / 3 * 0.1 + 1 / 3 * 0.2, abs=1e-15)


def test_movement_rate_lazy_cycle():
    T, _, pi = tiny_hmm()
    assert movement_rate(T, pi) == pytest.approx(0.5, abs=1e-15)
    assert movement_rate(np.eye(3), np.full(3, 1 / 3)) == 0.0


# ---------------------------------------------------------------- connectivity


def test_is_connected_true_false():
    T, _, _ = tiny_hmm()
    assert is_connected(T)
    assert not is_connected(_blocks())
    assert not is_connected(np.eye(3))


def test_is_connected_uses_either_direction():
    # only T_01 > 0 (T_10 = 0): the undirected graph {i != j: T_ij > 0 or T_ji > 0} is connected
    T = np.array([[0.5, 0.5], [0.0, 1.0]])
    assert is_connected(T)


# ---------------------------------------------------------------- spectrum


def test_spectrum_two_state_hand_values():
    p = 0.3
    rep = spectrum_report(_two_state(p), HALF)
    assert isinstance(rep, SpectrumReport)
    assert rep.status == "ok"
    np.testing.assert_allclose(rep.eigenvalues, [1.0, 1.0 - 2 * p], atol=1e-14)
    assert rep.gap == pytest.approx(2 * p, abs=1e-14)
    assert rep.abs_gap == pytest.approx(2 * p, abs=1e-14)
    assert rep.t_rel == pytest.approx(1 / (2 * p), rel=1e-13)


def test_spectrum_abs_gap_uses_negative_eigenvalue():
    # p = 0.8: eigenvalues 1, -0.6 -> gap 1.6, abs_gap 1 - 0.6 = 0.4, t_rel 2.5
    rep = spectrum_report(_two_state(0.8), HALF)
    np.testing.assert_allclose(rep.eigenvalues, [1.0, -0.6], atol=1e-14)
    assert rep.gap == pytest.approx(1.6, abs=1e-14)
    assert rep.abs_gap == pytest.approx(0.4, abs=1e-14)
    assert rep.t_rel == pytest.approx(2.5, rel=1e-13)


def test_spectrum_eigenvalues_descending_lazy_cycle():
    T, _, pi = tiny_hmm()
    rep = spectrum_report(T, pi)
    # lazy 4-cycle: 0.5 + 0.5 cos(2 pi k / 4) = 1, 0.5, 0.5, 0
    np.testing.assert_allclose(rep.eigenvalues, [1.0, 0.5, 0.5, 0.0], atol=1e-14)
    assert np.all(np.diff(rep.eigenvalues) <= 0)
    assert rep.gap == pytest.approx(0.5, abs=1e-14)
    assert rep.abs_gap == pytest.approx(0.5, abs=1e-14)


def test_mixing_bound_uses_ceil():
    # p = 0.3, pi_min = 0.5, eps = 0.25: t_rel log(1/(eps pi_min)) = log(8) / 0.6 = 3.4657...
    p = 0.3
    raw = (1 / (2 * p)) * math.log(1 / (0.25 * 0.5))
    assert raw != math.floor(raw)
    rep = spectrum_report(_two_state(p), HALF, eps=0.25)
    assert rep.mixing_bound == math.ceil(raw) == 4
    assert isinstance(rep.mixing_bound, int)


def test_mixing_bound_eps_and_pi_min():
    T, _, pi = tiny_hmm()
    rep = spectrum_report(T, pi, eps=0.1)
    raw = 2.0 * math.log(1 / (0.1 * 0.25))       # t_rel = 2
    assert raw != math.floor(raw)
    assert rep.mixing_bound == math.ceil(raw)


def test_spectrum_reducible_status():
    rep = spectrum_report(_blocks(), U4)
    assert rep.status == "REDUCIBLE"
    assert rep.t_rel is None and rep.mixing_bound is None


def test_spectrum_near_unit_gap_status():
    T = _two_state(1e-14)
    assert is_connected(T)
    rep = spectrum_report(T, HALF)
    assert rep.status == "NEAR_UNIT_GAP"
    assert rep.t_rel is None and rep.mixing_bound is None
    assert rep.abs_gap <= 1e-12


# ---------------------------------------------------------------- integrated autocorrelation


@pytest.mark.parametrize("p", [0.1, 0.3, 0.45])
def test_iat_two_state_hand_value(p):
    lam = 1.0 - 2.0 * p
    tau, status = integrated_autocorrelation(_two_state(p), HALF, np.array([0.0, 1.0]))
    assert status == "ok"
    assert tau == pytest.approx((1 + lam) / (1 - lam), rel=1e-12)


def test_iat_two_state_p01_is_nine():
    tau, status = integrated_autocorrelation(_two_state(0.1), HALF, np.array([3.0, -2.0]))
    assert status == "ok" and tau == pytest.approx(9.0, rel=1e-12)


def test_iat_eigenfunction_of_lazy_cycle():
    # g = cos(2 pi x / 4) lies in the lambda = 0.5 eigenspace -> tau = 1.5 / 0.5 = 3
    T, _, pi = tiny_hmm()
    tau, status = integrated_autocorrelation(T, pi, np.array([1.0, 0.0, -1.0, 0.0]))
    assert status == "ok" and tau == pytest.approx(3.0, rel=1e-12)
    # g = (1, -1, 1, -1) is the lambda = 0 mode -> tau = 1
    tau0, _ = integrated_autocorrelation(T, pi, np.array([1.0, -1.0, 1.0, -1.0]))
    assert tau0 == pytest.approx(1.0, rel=1e-12)


def test_iat_affine_invariance():
    rng = np.random.default_rng(3)
    A = rng.random((5, 5)) + 0.1
    T = (A + A.T) / 2
    T = T / T.sum(axis=1).max()
    T = T + np.diag(1.0 - T.sum(axis=1))         # symmetric, stochastic, uniform pi
    pi = np.full(5, 0.2)
    g = rng.normal(size=5)
    tau, s = integrated_autocorrelation(T, pi, g)
    tau2, s2 = integrated_autocorrelation(T, pi, 3.7 * g - 11.0)
    tau3, s3 = integrated_autocorrelation(T, pi, -0.01 * g + 2.0)
    assert s == s2 == s3 == "ok"
    assert tau2 == pytest.approx(tau, rel=1e-10) and tau3 == pytest.approx(tau, rel=1e-10)


def test_iat_constant_function_undefined():
    tau, status = integrated_autocorrelation(_two_state(0.3), HALF, np.array([2.5, 2.5]))
    assert (tau, status) == (None, "UNDEFINED_CONSTANT")
    T, _, pi = tiny_hmm()
    tau, status = integrated_autocorrelation(T, pi, np.full(4, 1e-7))
    assert (tau, status) == (None, "UNDEFINED_CONSTANT")


def test_iat_reducible():
    tau, status = integrated_autocorrelation(_blocks(), U4, np.array([0.0, 1.0, 2.0, 5.0]))
    assert (tau, status) == (None, "REDUCIBLE")


# ---------------------------------------------------------------- rate-matched kernel


def test_rate_matched_valid_equals_formula():
    T, _, _ = tiny_hmm()
    for alpha in (0.5, 1.0, 1.3):
        Ta, status = rate_matched_kernel(T, alpha)
        assert status == "ok"
        np.testing.assert_allclose(Ta, np.eye(4) + alpha * (T - np.eye(4)), atol=1e-15)


def test_rate_matched_diag_boundary():
    T, _, _ = tiny_hmm()                         # diag 0.5 -> diag(T_a) = 1 - alpha / 2
    Ta, status = rate_matched_kernel(T, 1.6)     # diag 0.2 (within float rounding)
    assert status == "ok" and np.diag(Ta).min() == pytest.approx(0.2, abs=1e-15)
    assert rate_matched_kernel(T, 1.6 + 1e-9) == (None, "INVALID_KERNEL")


@pytest.mark.parametrize("alpha", [0.0, -0.5])
def test_rate_matched_nonpositive_alpha_invalid(alpha):
    T, _, _ = tiny_hmm()
    Ta, status = rate_matched_kernel(T, alpha)
    assert Ta is None and status == "INVALID_KERNEL"


def test_rate_matched_negative_entry_invalid():
    T, _, _ = tiny_hmm()
    Ta, status = rate_matched_kernel(T, 3.0)     # diag 1 - 1.5 = -0.5
    assert Ta is None and status == "INVALID_KERNEL"


def test_rate_matched_diag_below_floor_invalid():
    T, _, _ = tiny_hmm()
    Ta, status = rate_matched_kernel(T, 1.8)     # diag 0.1 >= 0 but < 0.2; off 0.45
    assert Ta is None and status == "INVALID_KERNEL"
