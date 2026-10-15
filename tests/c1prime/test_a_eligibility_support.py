"""Independent tests, author A (job 0026): eligibility, kappa_nu and the covariates (TEST_PLAN
A-4; protocol sections 3.3 and 4), and the support gate M3 (TEST_PLAN A-5; protocol section 9).

Expected values are hand-derived (inverted_cdf ranks), recomputed in exact rationals, or
recomputed with numpy and the unchanged x4f_scores.ledoit_wolf / oracle_profile.circle_features.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_fit  # noqa: E402
import c1_gates  # noqa: E402
import c1_oracle  # noqa: E402
import oracle_profile  # noqa: E402
from topo_pilot.analysis import x4f_scores  # noqa: E402

GRID = np.array([[x, y] for x in range(12) for y in range(12)], dtype=np.float64)  # 144 states


# ---------------------------------------------------------------- A-4 eligibility (section 4)

@pytest.mark.parametrize("n, expected", [(1000, 998.0), (8192, 8183.0), (10, 9.0)])
def test_s_max_inverted_cdf_rank(n, expected):
    """Ranks: 1000 * 0.999 = 999 exactly in float -> 999th smallest (value 998);
    ceil(8192 * 0.999) = 8184 -> value 8183; ceil(9.99) = 10 -> value 9."""
    s = np.random.default_rng(n).permutation(np.arange(n, dtype=np.float64))
    got = c1_oracle.s_max(s)
    assert got == expected
    assert got == np.quantile(s, 0.999, method="inverted_cdf")


def test_s_max_with_ties_at_the_boundary_returns_an_input_value():
    """n = 1000: the 999th smallest value (sorted index 998) is returned, never interpolated."""
    s = np.r_[np.zeros(998), np.full(2, 5.0)]
    assert c1_oracle.s_max(s) == 5.0  # sorted[998] is the first 5.0
    s2 = np.r_[np.zeros(999), np.full(1, 5.0)]
    assert c1_oracle.s_max(s2) == 0.0  # sorted[998] is the last 0.0


def test_eligibility_rule_boundaries():
    smax = 3.25
    up = np.nextafter(smax, np.inf)
    sp = np.array([3.25, up, 1.0, 1.0, 1.0, 1.0, 0.0])
    sm = np.array([1.0, 1.0, up, 3.25, 1.0, 1.0, 0.0])
    fin = np.zeros(7)
    le_H, le_p, le_m = fin.copy(), fin.copy(), fin.copy()
    le_H[4], le_p[5], le_m[6] = -np.inf, np.nan, -np.inf
    got = np.asarray(c1_oracle.eligible(sp, sm, smax, le_H, le_p, le_m))
    assert got.dtype == bool
    assert got.tolist() == [True, False, False, True, False, False, False]


def test_eligible_fraction_and_the_h4_threshold():
    mask = np.zeros(1000, dtype=bool)
    mask[:900] = True
    f = c1_oracle.eligible_fraction(mask)
    assert f == 0.9 and f >= 0.90
    mask[0] = False
    assert c1_oracle.eligible_fraction(mask) == 899 / 1000 < 0.90


def test_kappa_nu_population_covariance_and_eligible_mean():
    rng = np.random.default_rng(3)
    n = 50
    nu_nat = rng.dirichlet(np.ones(12), size=n)
    nu_p, nu_m = rng.dirichlet(np.ones(12), size=n), rng.dirichlet(np.ones(12), size=n)
    elig = rng.uniform(size=n) < 0.8
    num = sum((Fraction(float(v)) for v in np.sum((nu_p - nu_m) ** 2, axis=1)[elig]),
              Fraction(0)) / int(elig.sum())
    tr = sum(Fraction(float(v)) for v in np.var(nu_nat, axis=0, ddof=0))
    want = float(num / tr)
    got = c1_oracle.kappa_nu(nu_p, nu_m, nu_nat, elig)
    assert got == pytest.approx(want, rel=1e-12)
    wrong_ddof = float(num / sum(Fraction(float(v)) for v in np.var(nu_nat, axis=0, ddof=1)))
    assert got != pytest.approx(wrong_ddof, rel=1e-6)


def test_leakage_trigger_at_001():
    assert bool(c1_oracle.leakage_active(0.01)) is True
    assert bool(c1_oracle.leakage_active(np.nextafter(0.01, 0.0))) is False
    assert bool(c1_oracle.leakage_active(0.5)) is True


def test_y_marginal_m32_and_nuisance():
    rng = np.random.default_rng(4)
    b = rng.dirichlet(np.ones(144), size=5)
    ym = np.asarray(c1_oracle.y_marginal(b, GRID))
    assert ym.shape == (5, 12)
    for c in range(12):
        assert np.allclose(ym[:, c], b[:, GRID[:, 1] == c].sum(axis=1), rtol=1e-14, atol=0)
    m32 = np.asarray(c1_oracle.m32(b, GRID))
    assert np.allclose(m32, b @ oracle_profile.circle_features(GRID), rtol=1e-13, atol=1e-16)
    z = np.asarray(c1_oracle.nuisance(b, GRID))
    y = GRID[:, 1]
    ybar = b @ y
    var = (b * (y[None, :] - ybar[:, None]) ** 2).sum(axis=1)  # population variance under b
    assert z.shape == (5, 3)
    assert np.allclose(z[:, 0], ybar, rtol=1e-13)
    assert np.allclose(z[:, 1], var, rtol=1e-10)
    assert np.allclose(z[:, 2], np.hypot(m32[:, 0], m32[:, 1]), rtol=1e-13)


# ---------------------------------------------------------------- A-5 support M3 (section 9)

@pytest.mark.parametrize("n, expected", [(100, 98.0), (8192, 8110.0)])
def test_q99_inverted_cdf_rank(n, expected):
    """100 * 0.99 = 99 exactly in float -> 99th smallest (98); ceil(8110.08) = 8111 -> 8110."""
    x = np.random.default_rng(n + 1).permutation(np.arange(n, dtype=np.float64))
    assert c1_gates.q99(x) == expected


def test_frac_beyond_is_strict():
    assert c1_gates.frac_beyond(np.array([1.0, 2.0, 3.0, 3.0, 4.0]), 3.0) == 0.2


def whitened_fixture(d=128, n=3000, seed=5):
    rng = np.random.default_rng(seed)
    mix = 0.3 * rng.normal(size=(d, d)) / np.sqrt(d) + np.eye(d)
    r_cal = rng.normal(size=(n, d)) @ mix.T + 0.3
    mean, cov = x4f_scores.ledoit_wolf(r_cal)
    lam, vec = np.linalg.eigh(cov)
    W = (vec * lam**-0.5) @ vec.T
    fit = {"alpha": rng.normal(size=(36, d)), "Gamma": rng.normal(size=(3, d)),
           "B": rng.normal(size=(d, 2))}
    return r_cal, mean, W, fit, rng


def test_mahalanobis_with_source_or_donor_nuisance():
    r_cal, mean, W, fit, rng = whitened_fixture()
    white = c1_fit.whitening(r_cal)
    R = 7
    w = rng.integers(0, 36, size=R)
    zt_src, zt_don = rng.normal(size=(R, 3)), rng.normal(size=(R, 3))
    a = rng.normal(size=(R, 128)) * 2.0
    got_src = np.asarray(c1_gates.mahalanobis(a, w, zt_src, fit, white))
    got_don = np.asarray(c1_gates.mahalanobis(a, w, zt_don, fit, white))
    for zt, got in ((zt_src, got_src), (zt_don, got_don)):
        resid = a - fit["alpha"][w] - zt @ fit["Gamma"] - mean
        want = np.linalg.norm(resid @ W.T, axis=1)
        assert got.shape == (R,) and np.allclose(got, want, rtol=1e-8)
    assert not np.allclose(got_src, got_don)


def m3(F_T, F_C, F_D=0.0, F_S=0.0, sup=(0.995, 0.985, 0.985, 0.985)):
    S, D, T, C = sup
    Sup = {"S": S, "D": D, "T": T, "C": C, "C_mean": C, "Cbar": C, "C_bar": C}
    res = c1_gates.m3(F_S, F_D, F_T, [F_C] * 32, Sup)
    assert res["status"] in ("PASS", "INCONCLUSIVE/SUPPORT")
    return res["status"] == "PASS"


# Frame fractions below are dyadic (3/64, 1/16, 7/128, 1/32, 7/128), so the mean over 32 equal
# frames is exact whatever summation order the implementation uses.


def test_m3_primary_ceiling():
    assert m3(F_T=0.05, F_C=0.046875) is True  # max(0.05, 0 + 0.02) = 0.05, equality passes
    assert m3(F_T=np.nextafter(0.05, 1.0), F_C=0.046875) is False
    assert m3(F_T=0.0799, F_C=0.0625, F_D=0.06) is True  # bound F(D) + 0.02 ~ 0.08
    assert m3(F_T=0.0801, F_C=0.0625, F_D=0.06) is False


def test_m3_family_ceiling():
    assert m3(F_T=0.046875, F_C=0.046875) is True
    assert m3(F_T=0.046875, F_C=0.0546875, F_D=0.0390625) is True  # bound 0.0590625
    assert m3(F_T=0.046875, F_C=0.0546875, F_D=0.0) is False  # bound 0.05


def test_m3_matching_within_002():
    fc = 0.03125
    assert m3(F_T=fc + 0.02 - 1e-9, F_C=fc, F_D=0.04) is True  # ceilings 0.06
    assert m3(F_T=fc + 0.02 + 1e-9, F_C=fc, F_D=0.04) is False
    fc = 0.0546875  # F(T) below F(C-bar): the absolute difference counts
    assert m3(F_T=fc - 0.02 + 1e-9, F_C=fc, F_D=0.04) is True
    assert m3(F_T=fc - 0.02 - 1e-9, F_C=fc, F_D=0.04) is False


@pytest.mark.parametrize("which, edge", [(0, 0.99), (1, 0.98), (2, 0.98), (3, 0.98)])
def test_m3_support_fractions(which, edge):
    sup = [0.995, 0.985, 0.985, 0.985]
    sup[which] = edge
    assert m3(F_T=0.01, F_C=0.01, sup=tuple(sup)) is True
    sup[which] = np.nextafter(edge, 0.0)
    assert m3(F_T=0.01, F_C=0.01, sup=tuple(sup)) is False
