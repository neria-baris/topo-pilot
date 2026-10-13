"""Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
before reading the implementation.

Targets (X4F_GATES_API section 2.1): circle_expectation, leading_components, pc_scores.
"""
import numpy as np
import pytest

from topo_pilot.analysis import PCMap, circle_expectation, leading_components, pc_scores
from topo_pilot.contracts import ErrorCode, StageFailure

pytestmark = pytest.mark.analysis


def _code(fn):
    with pytest.raises(StageFailure) as exc:
        fn()
    return exc.value.code


# --------------------------------------------------------------------------- circle_expectation

@pytest.mark.parametrize("s", range(12))
def test_delta_belief_gives_unit_vector_at_state_angle(s):
    b = np.zeros((1, 12))
    b[0, s] = 1.0
    m = circle_expectation(b, np.arange(12), 12)
    assert m.shape == (1, 2)
    theta = 2 * np.pi * s / 12
    np.testing.assert_allclose(m[0], [np.cos(theta), np.sin(theta)], atol=1e-14)
    assert abs(np.linalg.norm(m[0]) - 1.0) <= 1e-14


def test_uniform_belief_over_full_period_is_zero():
    b = np.full((3, 12), 1 / 12)
    m = circle_expectation(b, np.arange(12), 12)
    assert m.shape == (3, 2)
    assert np.abs(m).max() <= 1e-14


def test_hand_values_mixed_beliefs_and_non_integer_positions():
    # x = [0, 1.5, 3, 4.5] on period 6 -> angles 0, pi/2, pi, 3pi/2
    x = np.array([0.0, 1.5, 3.0, 4.5])
    b = np.array([[0.5, 0.5, 0.0, 0.0],
                  [0.25, 0.0, 0.75, 0.0],
                  [0.0, 0.1, 0.0, 0.9]])
    m = circle_expectation(b, x, 6.0)
    np.testing.assert_allclose(m, [[0.5, 0.5], [-0.5, 0.0], [0.0, -0.8]], atol=1e-14)


def test_linear_in_belief_and_bounded():
    rng = np.random.default_rng(0)
    b = rng.random((50, 7))
    b /= b.sum(1, keepdims=True)
    x = np.arange(7)
    m = circle_expectation(b, x, 7)
    expected = b @ np.stack([np.cos(2 * np.pi * x / 7), np.sin(2 * np.pi * x / 7)], axis=1)
    np.testing.assert_allclose(m, expected, atol=1e-14)
    assert np.all(np.linalg.norm(m, axis=1) <= 1 + 1e-12)


def test_circle_expectation_errors():
    b = np.full((2, 12), 1 / 12)
    assert _code(lambda: circle_expectation(b, np.arange(11), 12)) is ErrorCode.ALIGNMENT_ERROR
    assert _code(lambda: circle_expectation(b, np.arange(13), 12)) is ErrorCode.ALIGNMENT_ERROR
    assert _code(lambda: circle_expectation(b, np.arange(12), 0)) is ErrorCode.INVALID_CONFIG
    assert _code(lambda: circle_expectation(b, np.arange(12), -12)) is ErrorCode.INVALID_CONFIG


# --------------------------------------------------------------------------- leading_components

def _flip_to_convention(V):
    V = V.copy()
    for j in range(V.shape[1]):
        i = np.argmax(np.abs(V[:, j]))
        if V[i, j] < 0:
            V[:, j] = -V[:, j]
    return V


def _anisotropic(n=4000, seed=0):
    rng = np.random.default_rng(seed)
    R, _ = np.linalg.qr(rng.normal(size=(4, 4)))
    return rng.normal(size=(n, 4)) @ np.diag([3.0, 2.0, 1.0, 0.5]) @ R.T + np.array([1, -2, 3, 0])


def test_leading_components_hand_case():
    Z = np.array([[2.0, 0.0], [-2.0, 0.0], [0.0, 1.0], [0.0, -1.0]]) + np.array([5.0, -1.0])
    pc = leading_components(Z, 2)
    assert isinstance(pc, PCMap)
    np.testing.assert_allclose(pc.mean, [5.0, -1.0], atol=1e-14)
    np.testing.assert_allclose(pc.components, np.eye(2), atol=1e-12)


def test_leading_components_match_eigh_of_population_covariance():
    Z = _anisotropic()
    pc = leading_components(Z, 3)
    assert pc.components.shape == (4, 3)
    assert pc.mean.shape == (4,)
    Zc = Z - Z.mean(0)
    S = Zc.T @ Zc / Z.shape[0]
    vals, vecs = np.linalg.eigh(S)
    order = np.argsort(vals)[::-1]
    ref = _flip_to_convention(vecs[:, order[:3]])
    np.testing.assert_allclose(pc.components, ref, atol=1e-8)
    np.testing.assert_allclose(pc.mean, Z.mean(0), atol=1e-12)
    np.testing.assert_allclose(pc.components.T @ pc.components, np.eye(3), atol=1e-10)


def test_eigen_order_is_descending():
    Z = _anisotropic(seed=1)
    pc = leading_components(Z, 4)
    var = pc_scores(Z, pc).var(axis=0)
    assert np.all(np.diff(var) < 0)


def test_sign_convention_largest_abs_entry_positive_and_stable_under_negation():
    Z = _anisotropic(seed=2)
    pc = leading_components(Z, 4)
    for j in range(4):
        i = np.argmax(np.abs(pc.components[:, j]))
        assert pc.components[i, j] > 0
    pc_neg = leading_components(-Z, 4)  # same covariance, so the same components
    np.testing.assert_allclose(pc_neg.components, pc.components, atol=1e-8)


def test_leading_components_errors():
    Z = _anisotropic(n=100)
    assert _code(lambda: leading_components(Z, 5)) is ErrorCode.ALIGNMENT_ERROR
    assert _code(lambda: leading_components(Z, 0)) is ErrorCode.ALIGNMENT_ERROR
    assert leading_components(Z, 4).components.shape == (4, 4)  # c == q is allowed


# --------------------------------------------------------------------------- pc_scores

def test_pc_scores_definition_on_new_rows():
    Z = _anisotropic(seed=3)
    pc = leading_components(Z[:2000], 2)
    Znew = Z[2000:2050]
    s = pc_scores(Znew, pc)
    assert s.shape == (50, 2)
    np.testing.assert_allclose(s, (Znew - pc.mean) @ pc.components, atol=1e-12)


def test_pc_scores_hand_case_and_decorrelation():
    Z = np.array([[2.0, 0.0], [-2.0, 0.0], [0.0, 1.0], [0.0, -1.0]]) + np.array([5.0, -1.0])
    pc = leading_components(Z, 1)
    np.testing.assert_allclose(pc_scores(Z, pc)[:, 0], [2.0, -2.0, 0.0, 0.0], atol=1e-12)
    Zr = _anisotropic(seed=4)
    pcr = leading_components(Zr, 4)
    s = pc_scores(Zr, pcr)
    np.testing.assert_allclose(s.mean(0), 0.0, atol=1e-10)
    C = s.T @ s / s.shape[0]
    np.testing.assert_allclose(C - np.diag(np.diag(C)), 0.0, atol=1e-8)
