"""Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
before reading the implementation.
(Mechanically split out of test_x4f_erasure.py by the builder to respect the 400-line limit;
test bodies unchanged.)

Matched random families and mismatch report (X4F_GATES_API section 2.2; x4f-exec-v2 section 6).
"""
import numpy as np
import pytest

from topo_pilot.analysis import (
    Family,
    mismatch_report,
    random_family,
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



# --------------------------------------------------------------------------- random_family

def test_family_matches_spec_draw_procedure_and_window():
    X = anisotropic_X(n=500, seed=20)
    wh = whiten(X)
    rng_for = rng_for_seed(42)
    refs = [ref_family_draw(X, wh, 2, rng_for(j)) for j in range(200)]
    D = np.array([d for _, d in refs])
    D_t = float(np.median(D))
    tol = 0.05
    inside = np.abs(D - D_t) <= tol * D_t
    expected = [j for j in range(200) if inside[j]][:5]
    assert len(expected) == 5 and expected[-1] + 1 > 5   # some draws are rejected
    margin = np.abs(np.abs(D[: expected[-1] + 1] - D_t) - tol * D_t)
    assert margin.min() > 1e-9 * D_t                       # fixture: no borderline draw
    fam = random_family(X, wh, 2, D_t, rng_for, n_accept=5, max_draws=200, tol=tol)
    assert isinstance(fam, Family)
    assert fam.status == "ok"
    assert list(fam.accepted_draws) == expected
    assert fam.n_draws == expected[-1] + 1
    assert fam.n_degenerate_draws == 0
    assert fam.target_displacement == pytest.approx(D_t, rel=1e-12)
    assert len(fam.maps) == 5 and len(fam.mean_displacements) == 5
    for j, M, Dj in zip(expected, fam.maps, fam.mean_displacements):
        np.testing.assert_allclose(M, refs[j][0], atol=1e-10)
        assert Dj == pytest.approx(D[j], rel=1e-10)
        assert abs(Dj - D_t) <= tol * D_t


def test_family_rank_deficient_maps_live_in_retained_range():
    X = rank_deficient_X(seed=21)
    wh = whiten(X)
    assert wh.k == 5
    rng_for = rng_for_seed(7)
    _, D0 = ref_family_draw(X, wh, 2, rng_for(0))
    fam = random_family(X, wh, 2, D0, rng_for, n_accept=6, max_draws=6, tol=1e3)
    assert fam.status == "ok"
    assert list(fam.accepted_draws) == list(range(6))
    P_disc = np.eye(8) - wh.U_keep @ wh.U_keep.T
    for M in fam.maps:
        E = np.eye(8) - M
        assert numerical_rank(E) == 2
        assert np.abs(P_disc @ E).max() <= 1e-10 * np.abs(E).max()
        assert np.abs(E @ P_disc).max() <= 1e-10 * np.abs(E).max()
        np.testing.assert_allclose(M @ M, M, atol=1e-10 * max(1.0, np.abs(M).max()))


def test_family_rank_equal_to_k_allowed_and_rank_above_k_rejected():
    X = rank_deficient_X(seed=22)
    wh = whiten(X)
    fam = random_family(X, wh, 5, 1.0, rng_for_seed(1), n_accept=2, max_draws=2, tol=1e6)
    assert fam.status == "ok"
    for M in fam.maps:
        assert numerical_rank(np.eye(8) - M) == 5
    for rank in (6, 0):
        fam = random_family(X, wh, rank, 1.0, rng_for_seed(1), n_accept=2, max_draws=2, tol=1e6)
        assert fam.status == "RANK_EXCEEDS_RETAINED"
        assert list(fam.accepted_draws) == [] and fam.maps == []


def test_family_deterministic_given_rng_for():
    X = anisotropic_X(n=400, seed=23)
    wh = whiten(X)
    _, D0 = ref_family_draw(X, wh, 2, rng_for_seed(3)(0))
    a = random_family(X, wh, 2, D0, rng_for_seed(3), n_accept=4, max_draws=300, tol=0.2)
    b = random_family(X, wh, 2, D0, rng_for_seed(3), n_accept=4, max_draws=300, tol=0.2)
    assert a.status == b.status == "ok"
    assert list(a.accepted_draws) == list(b.accepted_draws)
    assert a.mean_displacements == b.mean_displacements
    for Ma, Mb in zip(a.maps, b.maps):
        assert np.array_equal(Ma, Mb)
    c = random_family(X, wh, 2, D0, rng_for_seed(4), n_accept=4, max_draws=300, tol=0.2)
    assert not np.allclose(c.maps[0], a.maps[0])


def test_family_zero_displacement_makes_no_draws():
    X = anisotropic_X(n=300, seed=24)
    wh = whiten(X)
    scale = float(np.mean(np.linalg.norm(X - X.mean(0), axis=1)))
    calls = []

    def rng_for(j):
        calls.append(j)
        return np.random.default_rng(j)

    for target in (0.0, 1e-13 * scale):
        fam = random_family(X, wh, 2, target, rng_for)
        assert fam.status == "ZERO_DISPLACEMENT"
        assert list(fam.accepted_draws) == [] and fam.maps == [] and fam.n_draws == 0
    assert calls == []


def test_family_degenerate_features():
    X = np.zeros((30, 4))
    wh = whiten(X)
    assert random_family(X, wh, 1, 0.0, rng_for_seed(0)).status == "ZERO_DISPLACEMENT"
    assert random_family(X, wh, 1, 1.0, rng_for_seed(0)).status == "FEATURES_DEGENERATE"


def test_family_unmatched_small_budget_returns_accepted():
    X = anisotropic_X(n=300, seed=25)
    wh = whiten(X)
    _, D0 = ref_family_draw(X, wh, 2, rng_for_seed(5)(0))
    fam = random_family(X, wh, 2, D0, rng_for_seed(5), n_accept=20, max_draws=3, tol=1e3)
    assert fam.status == "FAMILY_UNMATCHED"
    assert list(fam.accepted_draws) == [0, 1, 2]
    assert len(fam.maps) == 3
    assert fam.n_draws == 3


def test_family_unmatched_impossible_target():
    X = anisotropic_X(n=300, seed=26)
    wh = whiten(X)
    scale = float(np.mean(np.linalg.norm(X - X.mean(0), axis=1)))
    fam = random_family(X, wh, 2, 1e6 * scale, rng_for_seed(6), n_accept=20, max_draws=25)
    assert fam.status == "FAMILY_UNMATCHED"
    assert list(fam.accepted_draws) == []
    assert fam.n_draws == 25


class _DuplicatingGenerator:
    """A Generator whose standard_normal output has two identical columns (a degenerate draw)."""

    def __init__(self, real):
        self._real = real

    def standard_normal(self, *args, **kwargs):
        g = np.array(self._real.standard_normal(*args, **kwargs), dtype=np.float64)
        g[:, 1] = g[:, 0]
        return g

    def __getattr__(self, name):
        return getattr(self._real, name)


def test_family_degenerate_draws_rejected_and_counted():
    X = anisotropic_X(n=300, seed=27)
    wh = whiten(X)

    def rng_for(j):
        real = np.random.default_rng([8, j])
        return _DuplicatingGenerator(real) if j in (0, 3) else real

    _, D1 = ref_family_draw(X, wh, 2, rng_for(1))
    fam = random_family(X, wh, 2, D1, rng_for, n_accept=4, max_draws=50, tol=1e3)
    assert fam.status == "ok"
    assert list(fam.accepted_draws) == [1, 2, 4, 5]
    assert fam.n_degenerate_draws == 2
    assert fam.n_draws == 6


# --------------------------------------------------------------------------- mismatch_report

def test_mismatch_report_hand_values_and_exclusion():
    d_target = np.array([1.0, 2.0, 0.0, 4.0, 2.0])
    d_other = np.array([1.5, 1.0, 7.0, 4.0, 3.0])
    rep = mismatch_report(d_target, d_other, 1.0)
    assert rep["n_excluded"] == 1
    ratios = np.array([0.5, 0.5, 0.0, 0.5])
    assert rep["mismatch_median"] == pytest.approx(np.median(ratios), abs=1e-14)
    assert rep["mismatch_q90"] == pytest.approx(np.quantile(ratios, 0.9), abs=1e-14)
    assert rep["q50"] == pytest.approx(3.0, abs=1e-14)
    assert rep["q10"] == pytest.approx(np.quantile(d_other, 0.1), abs=1e-14)
    assert rep["q90"] == pytest.approx(np.quantile(d_other, 0.9), abs=1e-14)
    assert all(np.isfinite(rep[k]) for k in ("mismatch_median", "mismatch_q90"))


def test_mismatch_report_threshold_scales_with_scale():
    d_target = np.array([1e-13, 1e-11, 1.0])
    d_other = np.array([1.0, 1e-11, 1.0])
    assert mismatch_report(d_target, d_other, 1.0)["n_excluded"] == 1
    assert mismatch_report(d_target, d_other, 1e3)["n_excluded"] == 2
    rep = mismatch_report(d_target, d_other, 1.0)
    assert rep["mismatch_median"] == pytest.approx(0.0, abs=1e-12)
