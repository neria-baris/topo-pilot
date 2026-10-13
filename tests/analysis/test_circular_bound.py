"""circ-audit-v1: symbol-only optimistic bound A*_symbol (known answers and properties)."""
import numpy as np
import pytest

from topo_pilot.analysis import circular_agreement, symbol_only_bound
from topo_pilot.contracts import StageFailure

pytestmark = pytest.mark.analysis


def test_bound_is_one_when_symbol_determines_angle():
    sym = np.array([0, 0, 1, 1, 2])
    theta = np.array([0.3, 0.3, 2.0, 2.0, -1.0])
    assert symbol_only_bound(theta, sym) == pytest.approx(1.0)


def test_bound_hand_value_and_opposite_angles():
    sym = np.array([0, 0, 1])
    theta = np.array([0.0, np.pi, 1.0])          # group 0 cancels, group 1 has modulus 1
    assert symbol_only_bound(theta, sym) == pytest.approx(1 / 3)


def test_bound_dominates_every_symbol_function_and_is_attained():
    rng = np.random.default_rng(0)
    sym = rng.integers(0, 6, 300)
    theta = 0.8 * sym + rng.normal(0, 0.7, 300)
    bound = symbol_only_bound(theta, sym)
    for _ in range(50):
        f = rng.uniform(0, 2 * np.pi, 6)
        assert circular_agreement(f[sym], theta) <= bound + 1e-12
        assert circular_agreement(-f[sym], theta) <= bound + 1e-12
    groups = np.array([np.angle(np.exp(1j * theta[sym == w]).sum()) for w in range(6)])
    assert circular_agreement(groups[sym], theta) == pytest.approx(bound)


def test_bound_invariant_to_rotation_and_relabelling():
    rng = np.random.default_rng(1)
    sym, theta = rng.integers(0, 5, 100), rng.uniform(0, 2 * np.pi, 100)
    base = symbol_only_bound(theta, sym)
    assert symbol_only_bound(theta + 1.3, sym) == pytest.approx(base)
    assert symbol_only_bound(-theta, (sym * 7 + 3) % 11) == pytest.approx(base)


def test_bound_error_paths():
    with pytest.raises(StageFailure):
        symbol_only_bound(np.zeros(3), np.zeros(2))
    with pytest.raises(StageFailure):
        symbol_only_bound(np.array([np.nan]), np.array([0]))
