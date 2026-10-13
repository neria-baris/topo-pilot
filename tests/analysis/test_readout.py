"""Independent tests N14-N19 for the readout-geometry helpers (SPEC part (d), WX4)."""
import numpy as np
import pytest

from topo_pilot.analysis import (
    PointSet,
    ln_gauge_free,
    predictive_pointset,
    readout_projector,
    split_readout,
)
from topo_pilot.contracts import ErrorCode, StageFailure

pytestmark = pytest.mark.analysis


def hand_ln(Z, eps):
    """Reference LayerNorm without affine part (population variance)."""
    Z = np.asarray(Z, dtype=np.float64)
    mu = Z.mean(axis=1, keepdims=True)
    var = ((Z - mu) ** 2).mean(axis=1, keepdims=True)
    return (Z - mu) / np.sqrt(var + eps)


def unit_var_rows(M, d, seed):
    """Random rows rescaled so that each row has population variance exactly 1."""
    rng = np.random.default_rng(seed)
    Z = rng.normal(size=(M, d))
    Z = Z - Z.mean(axis=1, keepdims=True)
    return Z / Z.std(axis=1, keepdims=True)


def build_A(gamma, W_U):
    return np.asarray(gamma, dtype=np.float64)[:, None] * np.asarray(W_U, dtype=np.float64).T


def is_projector(P, tol=1e-10):
    return np.allclose(P, P.T, atol=tol) and np.allclose(P @ P, P, atol=tol)


def expect_code(code, fn, *args, **kwargs):
    with pytest.raises(StageFailure) as ei:
        fn(*args, **kwargs)
    assert ei.value.code == code


# ---------------------------------------------------------------- N14


@pytest.mark.parametrize("alpha", [0.3, 1.0, 7.5])
def test_N14_ln_gauge_free_affine_invariance(alpha):
    M, d = 12, 10
    Z = unit_var_rows(M, d, seed=1)
    rng = np.random.default_rng(2)
    c = rng.normal(scale=5.0, size=(M, 1))
    U = ln_gauge_free(Z, eps=0.0)
    U2 = ln_gauge_free(alpha * Z + c, eps=0.0)
    assert np.max(np.abs(U - U2)) < 1e-6


def test_N14_ln_gauge_free_shift_exact_with_eps():
    M, d = 12, 10
    Z = unit_var_rows(M, d, seed=3)
    rng = np.random.default_rng(4)
    c = rng.normal(scale=5.0, size=(M, 1))
    U = ln_gauge_free(Z, eps=1e-5)
    U2 = ln_gauge_free(Z + c, eps=1e-5)
    assert np.max(np.abs(U - U2)) < 1e-6


@pytest.mark.parametrize("alpha", [0.3, 1.0, 7.5])
def test_N14_ln_gauge_free_scaling_with_eps_is_an_eps_rescaling(alpha):
    # With eps > 0 scaling is not an invariance; the exact identity is
    # U_eps(alpha Z) = U_{eps / alpha^2}(Z).
    Z = unit_var_rows(12, 10, seed=7)
    U_scaled = ln_gauge_free(alpha * Z, eps=1e-5)
    assert np.max(np.abs(U_scaled - ln_gauge_free(Z, eps=1e-5 / alpha**2))) < 1e-12


def test_N14_ln_gauge_free_not_scale_invariant_with_eps_at_small_variance():
    Z = 1e-3 * unit_var_rows(12, 10, seed=8)  # row variance 1e-6 << eps
    diff = np.max(np.abs(ln_gauge_free(10.0 * Z, eps=1e-5) - ln_gauge_free(Z, eps=1e-5)))
    assert diff > 1e-2


def test_N14_ln_gauge_free_rows_have_mean_zero_and_shape():
    Z = np.random.default_rng(5).normal(loc=3.0, scale=2.0, size=(9, 7))
    U = ln_gauge_free(Z)
    assert U.shape == (9, 7)
    assert U.dtype == np.float64
    assert np.allclose(U.mean(axis=1), 0.0, atol=1e-12)


def test_N14_ln_gauge_free_hand_computed_row():
    # z = [1, 3, 5, 7]: mean 4, deviations [-3,-1,1,3], population variance 5.
    z = np.array([[1.0, 3.0, 5.0, 7.0]])
    expected0 = np.array([[-3.0, -1.0, 1.0, 3.0]]) / np.sqrt(5.0)
    assert np.allclose(ln_gauge_free(z, eps=0.0), expected0, atol=1e-12)
    expected = np.array([[-3.0, -1.0, 1.0, 3.0]]) / np.sqrt(5.0 + 1e-5)
    assert np.allclose(ln_gauge_free(z, eps=1e-5), expected, atol=1e-12)
    # default eps is 1e-5
    assert np.allclose(ln_gauge_free(z), expected, atol=1e-12)


def test_N14_ln_gauge_free_matches_reference_and_accepts_float32():
    Z = np.random.default_rng(6).normal(size=(6, 8))
    assert np.allclose(ln_gauge_free(Z, eps=1e-5), hand_ln(Z, 1e-5), atol=1e-12)
    out = ln_gauge_free(Z.astype(np.float32), eps=1e-5)
    assert out.dtype == np.float64
    assert np.allclose(out, hand_ln(Z.astype(np.float32), 1e-5), atol=1e-12)


# ---------------------------------------------------------------- N15


def _check_projector(gamma, W_U):
    A = build_A(gamma, W_U)
    P = readout_projector(gamma, W_U)
    d = A.shape[0]
    assert P.shape == (d, d)
    assert is_projector(P)
    rank = np.linalg.matrix_rank(A)
    assert np.trace(P) == pytest.approx(rank, abs=1e-8)
    assert np.allclose(P @ A, A, atol=1e-10)
    # P is the orthogonal projector onto range(A): P x = A lstsq(A, x)
    x = np.random.default_rng(11).normal(size=(d, 4))
    coef = np.linalg.lstsq(A, x, rcond=None)[0]
    assert np.allclose(P @ x, A @ coef, atol=1e-9)
    return P, rank


def test_N15_readout_projector_full_rank():
    rng = np.random.default_rng(0)
    d, V = 16, 5
    gamma = rng.uniform(0.5, 2.0, size=d)
    W_U = rng.normal(size=(V, d))
    _, rank = _check_projector(gamma, W_U)
    assert rank == V


def test_N15_readout_projector_rank_deficient_duplicate_rows():
    rng = np.random.default_rng(1)
    d, V = 16, 6
    gamma = rng.uniform(0.5, 2.0, size=d)
    W_U = rng.normal(size=(V, d))
    W_U[4] = W_U[1]
    W_U[5] = W_U[0]
    _, rank = _check_projector(gamma, W_U)
    assert rank == V - 2


def test_N15_readout_projector_gamma_with_zeros():
    rng = np.random.default_rng(2)
    d, V = 16, 5
    gamma = rng.uniform(0.5, 2.0, size=d)
    gamma[[0, 3, 7]] = 0.0
    W_U = rng.normal(size=(V, d))
    P, _ = _check_projector(gamma, W_U)
    # zeroed coordinates cannot be in the range of A
    assert np.allclose(P[[0, 3, 7], :], 0.0, atol=1e-10)
    assert np.allclose(P[:, [0, 3, 7]], 0.0, atol=1e-10)


def test_N15_readout_projector_gamma_zeros_make_rank_drop():
    # keep only 3 coordinates alive with V = 5: rank(A) = 3
    rng = np.random.default_rng(3)
    d, V = 8, 5
    gamma = np.zeros(d)
    gamma[[1, 4, 6]] = [1.0, 2.0, 0.5]
    W_U = rng.normal(size=(V, d))
    _, rank = _check_projector(gamma, W_U)
    assert rank == 3


def test_N15_readout_projector_zero_A_gives_zero_P():
    rng = np.random.default_rng(4)
    P = readout_projector(np.zeros(6), rng.normal(size=(3, 6)))
    assert np.allclose(P, 0.0)


def test_N15_readout_projector_accepts_float32():
    rng = np.random.default_rng(5)
    gamma = rng.uniform(0.5, 2.0, size=10).astype(np.float32)
    W_U = rng.normal(size=(4, 10)).astype(np.float32)
    P = readout_projector(gamma, W_U)
    assert P.dtype == np.float64
    assert is_projector(P)
    assert np.trace(P) == pytest.approx(4, abs=1e-8)


# ---------------------------------------------------------------- N16


def _setup_split(seed=0, d=16, V=5, M=20):
    rng = np.random.default_rng(seed)
    gamma = rng.uniform(0.5, 2.0, size=d)
    W_U = rng.normal(size=(V, d))
    A = build_A(gamma, W_U)
    P = readout_projector(gamma, W_U)
    U = rng.normal(size=(M, d))
    return gamma, W_U, A, P, U


def test_N16_split_readout_sums_and_orthogonality():
    _, _, _, P, U = _setup_split()
    U_vis, U_null = split_readout(U, P)
    assert U_vis.shape == U.shape and U_null.shape == U.shape
    assert np.allclose(U_vis + U_null, U, atol=1e-12)
    assert np.max(np.abs(np.einsum("ij,ij->i", U_vis, U_null))) < 1e-10
    # hand formula: rows are points, U_visible = U P
    assert np.allclose(U_vis, U @ P, atol=1e-12)


def test_N16_split_readout_vector_already_visible_has_zero_null():
    _, _, A, P, _ = _setup_split(seed=1)
    C = np.random.default_rng(9).normal(size=(7, A.shape[1]))
    U = C @ A.T  # rows lie in range(A)
    U_vis, U_null = split_readout(U, P)
    assert np.allclose(U_null, 0.0, atol=1e-9)
    assert np.allclose(U_vis, U, atol=1e-9)


def test_N16_split_readout_null_part_is_invisible():
    _, _, A, P, U = _setup_split(seed=2)
    _, U_null = split_readout(U, P)
    assert np.allclose(U_null @ A, 0.0, atol=1e-9)


# ---------------------------------------------------------------- N17


def _tiny_model(seed, d=16, V=5, M=30, zero_gamma_idx=()):
    rng = np.random.default_rng(seed)
    Z = rng.normal(loc=1.0, scale=3.0, size=(M, d))
    gamma = rng.uniform(0.5, 2.0, size=d)
    for i in zero_gamma_idx:
        gamma[i] = 0.0
    beta = rng.normal(size=d)
    W_U = rng.normal(size=(V, d))
    return Z, gamma, beta, W_U


def _logits(U, gamma, beta, W_U):
    return (gamma * U + beta) @ W_U.T


@pytest.mark.parametrize("zero_idx", [(), (2,), (0, 5, 9)])
def test_N17_tiny_model_visible_part_reproduces_logits(zero_idx):
    Z, gamma, beta, W_U = _tiny_model(seed=21, zero_gamma_idx=zero_idx)
    U = ln_gauge_free(Z, eps=1e-5)
    P = readout_projector(gamma, W_U)
    U_vis, U_null = split_readout(U, P)
    assert np.max(np.abs(_logits(U_vis, gamma, beta, W_U) - _logits(U, gamma, beta, W_U))) < 1e-10
    # the null part contributes nothing beyond the beta term
    assert np.max(np.abs(gamma * U_null @ W_U.T)) < 1e-10
    # null part is non-trivial (V < d), otherwise the test would be vacuous
    assert np.linalg.norm(U_null) > 1e-3


def test_N17_tiny_model_against_hand_layernorm():
    Z, gamma, beta, W_U = _tiny_model(seed=22)
    U = hand_ln(Z, 1e-5)
    P = readout_projector(gamma, W_U)
    U_vis, _ = split_readout(ln_gauge_free(Z, eps=1e-5), P)
    assert np.max(np.abs(_logits(U_vis, gamma, beta, W_U) - _logits(U, gamma, beta, W_U))) < 1e-10


# ---------------------------------------------------------------- N18


def hand_softmax(L):
    L = np.asarray(L, dtype=np.float64)
    e = np.exp(L - L.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def test_N18_predictive_pointset_known_answer():
    logits = np.array([[0.0, 0.0, 0.0, 0.0], [np.log(1.0), np.log(2.0), np.log(3.0), np.log(4.0)]])
    ps = predictive_pointset(logits, ["h0", "h1"])
    assert isinstance(ps, PointSet)
    assert ps.metric == "hellinger"
    assert ps.space == "pred:softmax"
    assert ps.D is None
    assert ps.ids == ["h0", "h1"]
    assert np.allclose(ps.X[0], 0.25, atol=1e-12)
    assert np.allclose(ps.X[1], np.array([1, 2, 3, 4]) / 10.0, atol=1e-12)


def test_N18_predictive_pointset_rows_sum_to_one_and_match_hand_softmax():
    logits = np.random.default_rng(0).normal(scale=4.0, size=(15, 7))
    ids = [f"h{i}" for i in range(15)]
    ps = predictive_pointset(logits, ids)
    assert ps.X.shape == (15, 7)
    assert ps.X.dtype == np.float64
    assert np.allclose(ps.X.sum(axis=1), 1.0, atol=1e-12)
    assert np.all(ps.X > 0)
    assert np.allclose(ps.X, hand_softmax(logits), atol=1e-12)
    assert ps.ids == ids


def test_N18_predictive_pointset_row_shift_invariant_and_stable():
    rng = np.random.default_rng(1)
    logits = rng.normal(size=(6, 5))
    ids = list("abcdef")
    base = predictive_pointset(logits, ids).X
    shifted = predictive_pointset(logits + rng.normal(scale=50.0, size=(6, 1)), ids).X
    assert np.allclose(base, shifted, atol=1e-12)
    huge = predictive_pointset(logits + 1000.0, ids).X  # would overflow without max-subtraction
    assert np.all(np.isfinite(huge))
    assert np.allclose(base, huge, atol=1e-12)


def test_N18_predictive_pointset_custom_space_and_float32():
    logits = np.random.default_rng(2).normal(size=(4, 3)).astype(np.float32)
    ps = predictive_pointset(logits, ["a", "b", "c", "d"], space="pred:custom")
    assert ps.space == "pred:custom"
    assert ps.X.dtype == np.float64
    assert np.allclose(ps.X, hand_softmax(logits), atol=1e-12)


# ---------------------------------------------------------------- N19


def test_N19_ln_gauge_free_errors():
    rng = np.random.default_rng(0)
    expect_code(ErrorCode.ALIGNMENT_ERROR, ln_gauge_free, rng.normal(size=8))
    expect_code(ErrorCode.ALIGNMENT_ERROR, ln_gauge_free, rng.normal(size=(2, 3, 4)))
    expect_code(ErrorCode.ALIGNMENT_ERROR, ln_gauge_free, rng.normal(size=(5, 1)))
    expect_code(ErrorCode.INVALID_CONFIG, ln_gauge_free, rng.normal(size=(4, 6)), eps=-1e-3)
    Z = rng.normal(size=(4, 6))
    Z[1, 2] = np.nan
    expect_code(ErrorCode.NUMERICAL_FAILURE, ln_gauge_free, Z)
    Z[1, 2] = np.inf
    expect_code(ErrorCode.NUMERICAL_FAILURE, ln_gauge_free, Z)


def test_N19_ln_gauge_free_zero_variance_row():
    Z = np.random.default_rng(1).normal(size=(4, 6))
    Z[2] = 3.0
    expect_code(ErrorCode.NUMERICAL_FAILURE, ln_gauge_free, Z, eps=0.0)
    # with eps > 0 the constant row is legitimate and maps to zero
    U = ln_gauge_free(Z, eps=1e-5)
    assert np.allclose(U[2], 0.0, atol=1e-12)


def test_N19_readout_projector_errors():
    rng = np.random.default_rng(2)
    gamma, W_U = rng.uniform(0.5, 2.0, size=8), rng.normal(size=(3, 8))
    expect_code(ErrorCode.ALIGNMENT_ERROR, readout_projector, gamma[:7], W_U)
    expect_code(ErrorCode.ALIGNMENT_ERROR, readout_projector, gamma, W_U.T)
    expect_code(ErrorCode.ALIGNMENT_ERROR, readout_projector, gamma, W_U[0])
    expect_code(ErrorCode.ALIGNMENT_ERROR, readout_projector, gamma[:, None], W_U)
    bad_g = gamma.copy()
    bad_g[0] = np.nan
    expect_code(ErrorCode.NUMERICAL_FAILURE, readout_projector, bad_g, W_U)
    bad_W = W_U.copy()
    bad_W[1, 1] = np.inf
    expect_code(ErrorCode.NUMERICAL_FAILURE, readout_projector, gamma, bad_W)
    expect_code(ErrorCode.INVALID_CONFIG, readout_projector, gamma, W_U, rtol=-1e-3)


def test_N19_split_readout_errors():
    rng = np.random.default_rng(3)
    d = 8
    P = np.eye(d)
    expect_code(ErrorCode.ALIGNMENT_ERROR, split_readout, rng.normal(size=(5, d + 1)), P)
    expect_code(ErrorCode.ALIGNMENT_ERROR, split_readout, rng.normal(size=(5, d)), np.eye(d + 1))
    expect_code(ErrorCode.ALIGNMENT_ERROR, split_readout, rng.normal(size=(5, d)), np.ones((d, 3)))
    expect_code(ErrorCode.ALIGNMENT_ERROR, split_readout, rng.normal(size=d), P)


def test_N19_predictive_pointset_errors():
    rng = np.random.default_rng(4)
    logits = rng.normal(size=(3, 4))
    expect_code(ErrorCode.ALIGNMENT_ERROR, predictive_pointset, rng.normal(size=4), ["a"])
    expect_code(ErrorCode.ALIGNMENT_ERROR, predictive_pointset, logits, ["a", "b"])
    expect_code(ErrorCode.ALIGNMENT_ERROR, predictive_pointset, logits, ["a", "b", "c", "d"])
    bad = logits.copy()
    bad[0, 0] = np.nan
    expect_code(ErrorCode.NUMERICAL_FAILURE, predictive_pointset, bad, ["a", "b", "c"])
    bad[0, 0] = -np.inf
    expect_code(ErrorCode.NUMERICAL_FAILURE, predictive_pointset, bad, ["a", "b", "c"])
