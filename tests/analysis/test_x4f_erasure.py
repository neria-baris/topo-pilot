"""Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
before reading the implementation.

Whitening, oblique erasers and matched random families (X4F_GATES_API section 2.2;
x4f-exec-v2 sections 5, 6 and 11; addendum v2 section B2 fixtures).
"""
import numpy as np
import pytest

from topo_pilot.analysis import (
    Eraser,
    Whitening,
    apply_map,
    displacements,
    eraser_from_basis,
    fit_oblique_eraser,
    whiten,
)

pytestmark = pytest.mark.analysis

CHECK_KEYS = {"rho_max", "idempotence", "rank_loss", "exactness_ratio", "discarded_residual"}


# --------------------------------------------------------------------------- fixtures / helpers

def pop_cov(A, B=None):
    A = A - A.mean(0)
    B = A if B is None else B - B.mean(0)
    return A.T @ B / A.shape[0]


def anisotropic_X(n=3000, d=6, seed=0, top=2.5):
    """Correlated anisotropic features; covariance condition number about 10**(2*top)."""
    rng = np.random.default_rng(seed)
    R, _ = np.linalg.qr(rng.normal(size=(d, d)))
    scales = np.logspace(0, top, d)
    return rng.normal(size=(n, d)) @ np.diag(scales) @ R.T + rng.normal(size=d) * 5


def rank_deficient_X(n=600, d=8, r=5, seed=1):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n, r)) @ rng.normal(size=(r, d)) + rng.normal(size=d) * 3


def numerical_rank(A, rel=1e-8):
    s = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(s > rel * s.max())) if s.max() > 0 else 0


def rng_for_seed(seed):
    return lambda j: np.random.default_rng([seed, j])


def ref_family_draw(X, wh, rank, rng):
    """Spec section 2.2 draw: G in R^{k x rank}, Q from QR, E = W+ Q Q^T W, M = I - E."""
    G = rng.standard_normal((wh.k, rank))
    Q, _ = np.linalg.qr(G)
    E = wh.W_pinv @ Q @ Q.T @ wh.W
    M = np.eye(X.shape[1]) - E
    Xp = (X - wh.mu) @ M.T + wh.mu
    return M, float(np.mean(np.linalg.norm(Xp - X, axis=1)))


# --------------------------------------------------------------------------- whiten

def test_whiten_anisotropic_correlated():
    X = anisotropic_X()
    S = pop_cov(X)
    ev = np.linalg.eigvalsh(S)
    assert ev.max() / ev.min() >= 1e4  # fixture validity
    wh = whiten(X)
    assert isinstance(wh, Whitening)
    assert wh.status == "ok" and wh.k == 6
    assert wh.mu.shape == (6,) and wh.U_keep.shape == (6, 6) and wh.lam_keep.shape == (6,)
    assert wh.W.shape == (6, 6) and wh.W_pinv.shape == (6, 6)
    np.testing.assert_allclose(wh.mu, X.mean(0), atol=1e-10)
    np.testing.assert_allclose(wh.W @ S @ wh.W.T, np.eye(6), atol=1e-8)
    np.testing.assert_allclose(wh.W @ wh.W_pinv, np.eye(6), atol=1e-10)
    np.testing.assert_allclose(wh.W_pinv @ wh.W, wh.U_keep @ wh.U_keep.T, atol=1e-10)
    np.testing.assert_allclose(wh.U_keep.T @ wh.U_keep, np.eye(6), atol=1e-10)
    # population (1/n) eigenvalues, and the stated forms of W and W+
    np.testing.assert_allclose(np.sort(wh.lam_keep), np.sort(ev), rtol=1e-8)
    np.testing.assert_allclose(wh.W, np.diag(wh.lam_keep ** -0.5) @ wh.U_keep.T, atol=1e-10)
    np.testing.assert_allclose(wh.W_pinv, wh.U_keep @ np.diag(wh.lam_keep ** 0.5), atol=1e-10)


def test_whiten_rank_deficient_keeps_exact_rank():
    X = rank_deficient_X()
    wh = whiten(X)
    assert wh.status == "ok" and wh.k == 5
    assert wh.U_keep.shape == (8, 5) and wh.W.shape == (5, 8) and wh.W_pinv.shape == (8, 5)
    np.testing.assert_allclose(wh.W @ wh.W_pinv, np.eye(5), atol=1e-10)
    np.testing.assert_allclose(wh.W @ pop_cov(X) @ wh.W.T, np.eye(5), atol=1e-8)
    P_disc = np.eye(8) - wh.U_keep @ wh.U_keep.T
    assert np.abs((X - wh.mu) @ P_disc).max() <= 1e-8 * np.abs(X - wh.mu).max()


def _diag_cov_X(variances):
    """Four rows whose population covariance is exactly diag(variances)."""
    H = np.array([[1.0, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    return H @ np.diag(np.sqrt(variances)) + np.array([2.0, -3.0, 1.0])


@pytest.mark.parametrize("floor,k", [(1e-1, 1), (1e-4, 2), (1e-8, 3), (None, 3)])
def test_whiten_floor_is_relative_to_lambda_max(floor, k):
    X = _diag_cov_X([100.0, 1.0, 1e-4])
    wh = whiten(X) if floor is None else whiten(X, floor=floor)
    assert wh.status == "ok" and wh.k == k
    np.testing.assert_allclose(np.sort(wh.lam_keep)[::-1], [100.0, 1.0, 1e-4][:k], rtol=1e-8)


@pytest.mark.parametrize("X", [np.zeros((20, 4)), np.tile([1.0, -2.0, 3.0, 0.5], (20, 1)),
                               1e-7 * np.random.default_rng(0).normal(size=(20, 4))])
def test_whiten_degenerate(X):
    wh = whiten(X)
    assert wh.status == "FEATURES_DEGENERATE"
    assert wh.k == 0
    assert wh.U_keep.shape == (4, 0) and wh.lam_keep.shape == (0,)
    assert wh.W.shape == (0, 4) and wh.W_pinv.shape == (4, 0)


# --------------------------------------------------------------------------- apply_map / basis

def test_apply_map_batch_convention_non_symmetric():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(7, 3))
    mu = rng.normal(size=3)
    M = np.array([[1.0, 2.0, 0.0], [0.0, 1.0, -3.0], [0.5, 0.0, 1.0]])
    assert not np.allclose(M, M.T)
    out = apply_map(X, mu, M)
    expected = np.stack([M @ (x - mu) + mu for x in X])
    np.testing.assert_allclose(out, expected, atol=1e-12)
    wrong = (X - mu) @ M + mu
    assert np.abs(out - wrong).max() > 1e-3


def test_eraser_from_basis_formula():
    X = anisotropic_X(n=1000)
    wh = whiten(X)
    Q, _ = np.linalg.qr(np.random.default_rng(4).normal(size=(wh.k, 2)))
    E, M = eraser_from_basis(wh, Q)
    np.testing.assert_allclose(E, wh.W_pinv @ Q @ Q.T @ wh.W, atol=1e-10)
    np.testing.assert_allclose(M, np.eye(6) - E, atol=1e-12)
    assert numerical_rank(E) == 2
    np.testing.assert_allclose(M @ M, M, atol=1e-10 * max(1.0, np.abs(M).max()))


def test_displacements_known_answer():
    X = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, -1.0]])
    Xp = np.array([[3.0, 4.0], [1.0, 1.0], [2.0, 1.0]])
    np.testing.assert_allclose(displacements(X, Xp), [5.0, 0.0, 2.0], atol=1e-14)


# --------------------------------------------------------------------------- fit_oblique_eraser

def _planted_2d(seed=5, n=3000):
    X = anisotropic_X(n=n, seed=seed)
    rng = np.random.default_rng(seed + 100)
    B = rng.normal(size=(6, 2))
    S = (X - X.mean(0)) @ B
    Z = S + 0.3 * S.std(0) * rng.normal(size=(n, 2)) + np.array([1.0, -4.0])
    return X, Z


def test_oblique_eraser_planted_2d_target():
    X, Z = _planted_2d()
    wh = whiten(X)
    er = fit_oblique_eraser(X, Z, wh)
    assert isinstance(er, Eraser)
    assert er.status == "ok" and er.rank == 2
    assert CHECK_KEYS <= set(er.checks)
    assert er.M.shape == (6, 6) and er.E.shape == (6, 6)
    np.testing.assert_allclose(er.mu, X.mean(0), atol=1e-10)
    np.testing.assert_allclose(er.E + er.M, np.eye(6), atol=1e-12)
    # exactness: cross-covariance after erasure, relative to before
    Xp = apply_map(X, er.mu, er.M)
    assert np.abs(pop_cov(Xp, Z)).max() <= 1e-8 * np.abs(pop_cov(X, Z)).max()
    assert er.checks["exactness_ratio"] <= 1e-8
    # idempotence and rank
    assert np.abs(er.M @ er.M - er.M).max() <= 1e-10 * max(1.0, np.abs(er.M).max())
    assert numerical_rank(er.E) == 2
    assert er.checks["rank_loss"] == 2
    assert 0.0 < er.checks["rho_max"] <= 1.0 + 1e-12


def test_oblique_eraser_keeps_orthogonal_signal():
    X, Z = _planted_2d(seed=6)
    wh = whiten(X)
    er = fit_oblique_eraser(X, Z, wh)
    assert er.status == "ok" and er.rank == 2
    G = wh.W @ pop_cov(X, Z)
    U_G = np.linalg.svd(G)[0]
    perp = U_G[:, 2:]                      # whitened directions uncorrelated with Z
    Xp = apply_map(X, er.mu, er.M)
    s_before = (X - wh.mu) @ wh.W.T @ perp
    s_after = (Xp - wh.mu) @ wh.W.T @ perp
    assert np.abs(pop_cov(s_before, Z)).max() <= 1e-8 * np.abs(pop_cov(X, Z)).max()
    np.testing.assert_allclose(s_before.std(0), 1.0, atol=1e-8)   # a real, unit-variance signal
    np.testing.assert_allclose(s_after, s_before, atol=1e-8)
    for g in perp.T:                       # the feature directions themselves are fixed by M
        v = wh.W_pinv @ g
        np.testing.assert_allclose(er.M @ v, v, atol=1e-8 * np.linalg.norm(v))
    # and the erased whitened directions are removed
    s_erased = (Xp - wh.mu) @ wh.W.T @ U_G[:, :2]
    assert np.abs(s_erased).max() <= 1e-8 * np.abs((X - wh.mu) @ wh.W.T @ U_G[:, :2]).max()


def test_two_column_target_in_one_direction_has_rank_one():
    X = anisotropic_X(n=2000, seed=7)
    rng = np.random.default_rng(8)
    s = (X - X.mean(0)) @ rng.normal(size=6)
    s = s + 0.5 * s.std() * rng.normal(size=s.shape)
    Z = np.stack([s, 2.0 * s - 1.0], axis=1)
    er = fit_oblique_eraser(X, Z, whiten(X))
    assert er.rank == 1, "rank must be reported as found, not assumed to be 2"
    assert er.status == "ok"
    assert numerical_rank(er.E) == 1
    Xp = apply_map(X, er.mu, er.M)
    assert np.abs(pop_cov(Xp, Z)).max() <= 1e-8 * np.abs(pop_cov(X, Z)).max()


def test_noise_free_scalar_target_has_rho_one():
    X = anisotropic_X(n=1500, seed=9)
    Z = (X @ np.random.default_rng(9).normal(size=6))[:, None]
    er = fit_oblique_eraser(X, Z, whiten(X))
    assert er.status == "ok" and er.rank == 1
    assert abs(er.checks["rho_max"] - 1.0) <= 1e-8


def _two_scale_target(seed=10):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(4000, 5))
    Z = np.stack([X[:, 0], 1e-6 * X[:, 1]], axis=1)  # second singular value ~1e-6 of the first
    return X, Z


def test_rank_tolerance_is_relative_and_used():
    X, Z = _two_scale_target()
    wh = whiten(X)
    er = fit_oblique_eraser(X, Z, wh)                 # default 1e-8: both directions count
    assert er.status == "ok" and er.rank == 2
    er_loose = fit_oblique_eraser(X, Z, wh, rank_tol=1e-4, exact_tol=1e-3)
    assert er_loose.status == "ok" and er_loose.rank == 1


def test_eraser_invalid_keeps_computed_map():
    X, Z = _two_scale_target()
    wh = whiten(X)
    er = fit_oblique_eraser(X, Z, wh, rank_tol=1e-4)  # rank 1 leaves ~1e-6 relative covariance
    assert er.status == "ERASER_INVALID"
    assert er.rank == 1
    assert er.checks["exactness_ratio"] > 1e-8
    assert numerical_rank(er.E) == 1
    assert not np.allclose(er.M, np.eye(5))
    np.testing.assert_allclose(er.E + er.M, np.eye(5), atol=1e-12)


@pytest.mark.parametrize("Z", [np.full((800, 2), 3.0),
                               5.0 + 1e-8 * np.random.default_rng(11).normal(size=(800, 2))])
def test_constant_target_zero_variance(Z):
    X = anisotropic_X(n=800, seed=11)
    er = fit_oblique_eraser(X, Z, whiten(X))
    assert er.status == "TARGET_ZERO_VARIANCE"
    assert er.rank == 0
    assert np.array_equal(er.M, np.eye(6))
    assert np.array_equal(er.E, np.zeros((6, 6)))


def test_exactly_uncorrelated_target():
    rng = np.random.default_rng(12)
    X = rng.normal(size=(1000, 5)) @ rng.normal(size=(5, 5)) + 2.0
    Xc = X - X.mean(0)
    Zc = rng.normal(size=(1000, 2))
    Zc = Zc - Zc.mean(0)
    Z = Zc - Xc @ np.linalg.lstsq(Xc, Zc, rcond=None)[0] + 7.0
    assert np.abs(pop_cov(X, Z)).max() <= 1e-12  # fixture: exact zero cross-covariance
    er = fit_oblique_eraser(X, Z, whiten(X))
    assert er.status == "TARGET_UNCORRELATED"
    assert er.rank == 0
    assert np.array_equal(er.M, np.eye(5))
    assert np.array_equal(er.E, np.zeros((5, 5)))


def test_degenerate_whitening_propagates():
    X = np.zeros((50, 4))
    Z = np.random.default_rng(13).normal(size=(50, 2))
    er = fit_oblique_eraser(X, Z, whiten(X))
    assert er.status == "FEATURES_DEGENERATE"
    assert er.rank == 0
    assert np.array_equal(er.M, np.eye(4))
    assert np.array_equal(er.E, np.zeros((4, 4)))


def test_rank_deficient_X_erasure_stays_in_retained_range():
    X = rank_deficient_X(seed=14)
    rng = np.random.default_rng(14)
    S = (X - X.mean(0)) @ rng.normal(size=(8, 2))
    Z = S + 0.2 * S.std(0) * rng.normal(size=S.shape)
    wh = whiten(X)
    assert wh.k == 5
    er = fit_oblique_eraser(X, Z, wh)
    assert er.status == "ok" and er.rank == 2
    P_disc = np.eye(8) - wh.U_keep @ wh.U_keep.T
    scale = np.abs(er.E).max()
    assert np.abs(P_disc @ er.E).max() <= 1e-10 * scale    # removed component inside span(U_keep)
    assert np.abs(er.E @ P_disc).max() <= 1e-10 * scale    # discarded directions untouched
    # rows with a large component in the discarded eigen-directions keep it unchanged
    X_test = X[:50] + 10.0 * rng.normal(size=(50, 8)) @ P_disc
    Xp_test = apply_map(X_test, er.mu, er.M)
    np.testing.assert_allclose((Xp_test - er.mu) @ P_disc, (X_test - er.mu) @ P_disc, atol=1e-8)
    np.testing.assert_allclose(Xp_test - X_test, apply_map(X[:50], er.mu, er.M) - X[:50],
                               atol=1e-8)
    assert er.checks["discarded_residual"] <= 1e-8 * np.abs(pop_cov(X, Z)).max()


