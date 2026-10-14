"""Independent tests (author B) for error_bound.py: TEST_PLAN items B6 and B6b (spec v2.2,
ERROR_BOUND.md v2.1).

Written from API.md, ERROR_BOUND.md, CONTRACT.json and TEST_PLAN.md only; no production code was
read. Every envelope is re-derived here in exact Fractions; trigonometric references are exact
rational Taylor partial sums with a proven tail; posteriors come from the job-0014 independent
Decimal reference. reference_moments is not tested directly: its documented signature has no
coords argument, so its feature map is unspecified (reported as an ambiguity).
"""

from __future__ import annotations

import decimal
import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import error_bound  # noqa: E402
import errors  # noqa: E402
import independent_reference  # noqa: E402
import oracle_profile  # noqa: E402
import scores  # noqa: E402

pytestmark = pytest.mark.analysis

F = Fraction
X_MAX = F(6284, 1000)
TAYLOR_N = 48
A_COSH = 270


def _u(n: int) -> Fraction:
    return F(1, 2 * 10 ** (n - 1))                     # 1/2 * 10^(1-n)


def _gamma(k: int, n: int) -> Fraction:
    return k * _u(n) / (1 - k * _u(n))


def _beta(L: int, S: int) -> Fraction:
    v, n_ops = _u(60), 1 + (L - 1) * (2 * S + 2)
    h, t = _gamma(n_ops, 60), _gamma(S, 60)
    lo = (1 - h) * (1 - v) / ((1 + h) * (1 + t))
    hi = (1 + h) * (1 + v) / ((1 - h) * (1 - t))
    return max(1 - lo, hi - 1)


def _eps_m(beta: Fraction, S: int) -> Fraction:
    ec = 2 * _u(80)
    return beta + (1 + beta) * ec + (1 + beta) * (1 + ec) * _gamma(2 * S + 2, 80)


def _eps_v() -> Fraction:
    n = TAYLOR_N
    tails = max(X_MAX ** (2 * n + 2) / math.factorial(2 * n + 2),
                X_MAX ** (2 * n + 3) / math.factorial(2 * n + 3))
    g3 = _gamma(3 * n, 80)
    return tails + g3 * A_COSH + _gamma(n + 1, 80) * (1 + g3) * A_COSH


def _exact_cos_sin(x: Fraction, tail: Fraction) -> tuple[Fraction, Fraction]:
    """Exact rational Taylor partial sums. The loop stops at a term index n > 2|x| + 2 with
    |x^n/n!| < tail; later terms shrink by a factor < 1/2, so each series' error is < 2*tail."""
    c = s = F(0)
    term, n = F(1), 0
    while not (n > 2 * abs(x) + 2 and abs(term) < tail):
        if n % 4 == 0:
            c += term
        elif n % 4 == 1:
            s += term
        elif n % 4 == 2:
            c -= term
        else:
            s -= term
        n += 1
        term = term * x / n
    return c, s


def _sqrt3_half(prec: int) -> Fraction:
    with localcontext() as ctx:
        ctx.prec = prec
        return F(Decimal(3).sqrt() / 2)


# ---- envelope constants ---------------------------------------------------------------------
def test_u_and_gamma_digits_exact() -> None:
    for n in (1, 60, 80):
        assert error_bound.u_digits(n) == _u(n) and isinstance(error_bound.u_digits(n), Fraction)
    assert error_bound.u_digits(60) == F(1, 2 * 10**59)
    for k, n in ((3, 80), (8991, 60), (290, 80), (1, 1)):
        assert error_bound.gamma_digits(k, n) == _gamma(k, n)
    assert error_bound.gamma_digits(1, 1) == 1
    for k in (2, 3):                                   # k * u_1 = k / 2 >= 1
        with pytest.raises(ValueError):
            error_bound.gamma_digits(k, 1)


def test_feature_posterior_and_moment_envelopes_match_formulas() -> None:
    assert error_bound.feature_envelope() == 2 * _u(80)
    for L, S in ((32, 144), (32, 3), (4, 3), (1, 3)):
        beta = error_bound.posterior_envelope(L, S)
        assert isinstance(beta, Fraction) and beta == _beta(L, S)
        assert error_bound.moment_envelope(beta, S) == _eps_m(beta, S)
    assert F(1, 10**56) < _beta(32, 144) < F(1, 10**54)  # "beta about 1e-55" (section 3)


# ---- trapping context -------------------------------------------------------------------------
def test_trapping_context_settings() -> None:
    ctx = error_bound.trapping_context(60)
    assert (ctx.prec, ctx.rounding, ctx.Emin, ctx.Emax, ctx.clamp) == (
        60, decimal.ROUND_HALF_EVEN, -999999, 999999, 0)
    for sig in (decimal.Underflow, decimal.Subnormal, decimal.Overflow, decimal.Clamped,
                decimal.InvalidOperation, decimal.DivisionByZero):
        assert ctx.traps[sig], sig
    for sig in (decimal.Inexact, decimal.Rounded, decimal.FloatOperation):
        assert not ctx.traps[sig], sig
    assert error_bound.trapping_context(80).prec == 80


def test_trapping_context_raises_on_constructed_underflow_and_overflow() -> None:
    with localcontext(error_bound.trapping_context(60)):
        with pytest.raises((decimal.Underflow, decimal.Subnormal, decimal.Clamped)):
            Decimal("1E-999999") / Decimal("1E+70")   # below Etiny = -1000058
        with pytest.raises(decimal.Overflow):
            Decimal("9E+999999") * 10
        with pytest.raises(decimal.DivisionByZero):
            Decimal(1) / Decimal(0)
        with pytest.raises(decimal.InvalidOperation):
            Decimal(0) / Decimal(0)
        assert Decimal(1) / Decimal(3) > 0             # Inexact/Rounded allowed
        assert Decimal(0.1) < 0.5                      # FloatOperation allowed


def test_smallest_valid_forward_product_does_not_trap() -> None:
    """Exponent reasoning of section 2: 64 factors of 2^-1074 stay far above 10^Emin."""
    tiny = Decimal(2.0 ** -1074)
    with localcontext(error_bound.trapping_context(60)) as ctx:
        prod = Decimal(1)
        for _ in range(64):
            prod = prod * tiny
        assert prod > 0 and prod.adjusted() < -20000
        assert not ctx.flags[decimal.Underflow] and not ctx.flags[decimal.Subnormal]


# ---- exact features ---------------------------------------------------------------------------
_CS = {0: (1, 0), 1: ("r", F(1, 2)), 2: (F(1, 2), "r"), 3: (0, 1), 4: (F(-1, 2), "r"),
       5: ("-r", F(1, 2)), 6: (-1, 0), 7: ("-r", F(-1, 2)), 8: (F(-1, 2), "-r"), 9: (0, -1),
       10: (F(1, 2), "-r"), 11: ("r", F(-1, 2))}


def test_exact_features_values() -> None:
    feats = error_bound.exact_features(np.array([[float(x), 1.0] for x in range(12)]))
    assert len(feats) == 12
    root, eps_c = _sqrt3_half(120), error_bound.feature_envelope()
    for x, pair in enumerate(feats):
        assert len(pair) == 2
        for got, want in zip(pair, _CS[x]):
            assert isinstance(got, Decimal)
            if isinstance(want, str):
                target = root if want == "r" else -root
                assert abs(F(got) - target) + F(1, 10**118) <= eps_c
            else:
                assert F(got) == want


@pytest.mark.parametrize("x", [1.5, 12.0, -1.0, np.nan])
def test_exact_features_rejects_bad_coordinates(x: float) -> None:
    with pytest.raises(errors.Invalid):
        error_bound.exact_features(np.array([[0.0, 0.0], [x, 0.0]]))


# ---- decimal_cos_sin (fixed N = 48) -------------------------------------------------------------
def test_taylor_constants_and_exact_tail_inequalities() -> None:
    n = TAYLOR_N
    assert error_bound.TAYLOR_N == 48
    assert X_MAX ** 2 / ((2 * n + 3) * (2 * n + 4)) < 1
    assert X_MAX ** 2 / ((2 * n + 4) * (2 * n + 5)) < 1
    assert X_MAX ** 98 / math.factorial(98) < F(1, 10**75)
    assert X_MAX ** 99 / math.factorial(99) < F(1, 10**75)
    partial = sum((X_MAX ** k / math.factorial(k) for k in range(2 * n + 4)), F(0))
    tail = 2 * X_MAX ** (2 * n + 4) / math.factorial(2 * n + 4)    # later ratio < 1/2
    assert partial + tail <= 539                       # so cosh(X_MAX) <= (539 + 1)/2 = 270
    assert X_MAX > F(2 * np.pi)


def test_decimal_cos_sin_at_zero_is_exact() -> None:
    c, s, eps_v = error_bound.decimal_cos_sin(0.0)
    assert c == 1 and s == 0
    assert eps_v == _eps_v()


@pytest.mark.parametrize("x", [0.5, 1.0, math.pi / 2, 3.0, math.pi, 5.123456789, 6.28,
                               2 * math.pi])
def test_decimal_cos_sin_against_exact_rational_taylor(x: float) -> None:
    c, s, eps_v = error_bound.decimal_cos_sin(x)
    assert isinstance(c, Decimal) and isinstance(s, Decimal) and isinstance(eps_v, Fraction)
    assert eps_v == _eps_v()
    assert F(1, 10**75) < eps_v < F(1, 10**70)
    tail = F(1, 10**90)
    rc, rs = _exact_cos_sin(F(x), tail)
    assert abs(F(c) - rc) <= eps_v + 2 * tail          # eps_v >= the actual error
    assert abs(F(s) - rs) <= eps_v + 2 * tail
    with localcontext() as ctx:
        ctx.prec = 100
        assert abs(c * c + s * s - 1) < Decimal("1e-70")


@pytest.mark.parametrize("x", [-1e-12, -0.5, 6.2841, 7.0, math.nan, math.inf, -math.inf])
def test_decimal_cos_sin_rejects_outside_analytic_interval(x: float) -> None:
    with pytest.raises(errors.Invalid):
        error_bound.decimal_cos_sin(x)


# ---- row_bound (exact rational R, Delta, E_ref, B) ----------------------------------------------
M4_ROW = (Decimal("0.125"), Decimal("-0.375"))
M32_ROW = (Decimal("0.5"), Decimal("0.3333333333333333333333333333333333333333"))


def _row_reference(phi: float, eps4: Fraction, eps32: Fraction) -> tuple[Fraction, Fraction]:
    c, s, eps_v = error_bound.decimal_cos_sin(phi)
    r = [F(M32_ROW[j]) - F(M4_ROW[j]) for j in (0, 1)]
    big_r = F(c) * r[0] + F(s) * r[1]
    return big_r, eps_v * (abs(r[0]) + abs(r[1])) + 2 * (eps4 + eps32)


def test_row_bound_equals_independently_assembled_fractions() -> None:
    eps4, eps32 = _eps_m(_beta(4, 3), 3), _eps_m(_beta(32, 3), 3)
    for phi in (1.0, 4.75):
        big_r, e_ref = _row_reference(phi, eps4, eps32)
        for x_hat in (float(big_r), float(big_r) + 1e-3, float(big_r) - 2e-5):
            out = error_bound.row_bound(x_hat, phi, M4_ROW, M32_ROW, eps4, eps32)
            assert all(isinstance(out[k], Fraction) for k in ("R", "Delta", "E_ref", "B"))
            assert out["R"] == big_r
            assert out["Delta"] == abs(F(x_hat) - big_r)
            assert out["E_ref"] == e_ref
            assert out["B"] == out["Delta"] + out["E_ref"]
        assert error_bound.row_bound(float(big_r), phi, M4_ROW, M32_ROW, eps4, eps32)["B"] \
            <= F(1, 10000)
        assert error_bound.row_bound(float(big_r) + 1e-3, phi, M4_ROW, M32_ROW, eps4, eps32)[
            "B"] > F(1, 10000)


def test_row_bound_phi_outside_analytic_interval_is_invalid() -> None:
    eps = _eps_m(_beta(4, 3), 3)
    with pytest.raises(errors.Invalid):
        error_bound.row_bound(0.0, 7.0, M4_ROW, M32_ROW, eps, eps)


# ---- certify_rows / reference_check_rows on a tiny HMM -------------------------------------------
T_EXACT = [[F(1, 2), F(1, 2), F(0)], [F(1, 4), F(1, 4), F(1, 2)], [F(1, 2), F(0), F(1, 2)]]
E_EXACT = [[F(1, 2), F(1, 4), F(1, 4)], [F(1, 8), F(5, 8), F(1, 4)], [F(1, 4), F(0), F(3, 4)]]
PI_EXACT = [F(3, 7), F(2, 7), F(2, 7)]
T = np.array([[float(v) for v in row] for row in T_EXACT])
E = np.array([[float(v) for v in row] for row in E_EXACT])
PI = np.array([float(v) for v in PI_EXACT])
XS = (0, 3, 7)                                             # integer x: exact features apply
COORDS = np.array([[0.0, 2.0], [3.0, 0.0], [7.0, 1.0]])
HIST = np.array([[(r + t * (r + 1) + (t * t) // 3) % 3 for t in range(32)] for r in range(4)],
                dtype=np.int64)
PHI = np.array([0.3, 2.5, 5.9, 6.2])


def test_fixture_hmm_is_exactly_stationary() -> None:
    assert [sum(PI_EXACT[i] * T_EXACT[i][j] for i in range(3)) for j in range(3)] == PI_EXACT
    assert all(sum(row) == 1 for row in T_EXACT + E_EXACT) and sum(PI_EXACT) == 1


@pytest.fixture(scope="module")
def pipeline():
    """The production float pipeline: oracle_moments -> unit_vectors -> scores."""
    m = scores.oracle_moments(T, E, PI, HIST, oracle_profile.circle_features(COORDS))
    x_hat = scores.scores(scores.unit_vectors(PHI), m[32], m[4])
    return m, x_hat


def _ref_row(row: int, phi: float) -> tuple[Fraction, dict[int, list[Fraction]]]:
    """Independent reference score and moments for one row (Fractions)."""
    root = _sqrt3_half(120)
    feat = {0: (F(1), F(0)), 3: (F(0), F(1)), 7: (-root, F(-1, 2))}
    moments = {}
    for k in (1, 4, 32):
        post = independent_reference.decimal_suffix_posterior(T, E, PI, HIST[row, 32 - k:])
        moments[k] = [sum((F(p) * feat[x][j] for p, x in zip(post, XS)), F(0)) for j in (0, 1)]
    c, s = _exact_cos_sin(F(phi), F(1, 10**40))
    return c * (moments[32][0] - moments[4][0]) + s * (moments[32][1] - moments[4][1]), moments


def _certify(m4, m32, x_hat, phi=PHI, split="calibration", **kw) -> dict:
    return error_bound.certify_rows(T, E, PI, COORDS, HIST, phi, x_hat, m4, m32, split, **kw)


def test_pipeline_matches_independent_reference(pipeline) -> None:
    m, x_hat = pipeline
    for row in range(HIST.shape[0]):
        ref, moments = _ref_row(row, float(PHI[row]))
        assert abs(F(float(x_hat[row])) - ref) < F(1, 10**13)
        for k in (1, 4, 32):
            for j in (0, 1):
                assert abs(F(float(m[k][row, j])) - moments[k][j]) < F(1, 10**14)


@pytest.mark.parametrize("split", ["calibration", "validation"])
def test_certify_rows_certifies_exact_pipeline(pipeline, split: str) -> None:
    m, x_hat = pipeline
    out = _certify(m[4], m[32], x_hat, split=split)
    assert out["status"] == "CERTIFIED"
    assert out["rows"] == 4 and len(out["bounds"]) == 4
    assert 0.0 <= out["max_bound"] < 1e-12
    assert out["moment_check_max"] <= 1e-10


def test_certify_rows_shifted_score_is_inconclusive(pipeline) -> None:
    m, x_hat = pipeline
    bad = x_hat.copy()
    bad[1] += 2e-4
    out = _certify(m[4], m[32], bad)
    assert out["status"] == "INCONCLUSIVE"
    assert 1e-4 < out["max_bound"] and abs(out["max_bound"] - 2e-4) < 1e-12
    # the cap is honoured: half the smallest independent discrepancy cannot be certified
    deltas = [abs(F(float(x_hat[r])) - _ref_row(r, float(PHI[r]))[0]) for r in range(4)]
    cap = float(max(deltas)) / 2
    assert cap > 0
    assert _certify(m[4], m[32], x_hat, cap=cap)["status"] == "INCONCLUSIVE"


@pytest.mark.parametrize("which", ["m4", "m32"])
def test_certify_rows_moment_shift_is_fail_technical(pipeline, which: str) -> None:
    m, x_hat = pipeline
    m4, m32 = m[4].copy(), m[32].copy()
    (m4 if which == "m4" else m32)[2, 0] += 1e-9          # moment check is 1e-10
    out = _certify(m4, m32, x_hat)
    assert out["status"] == "FAIL_TECHNICAL"
    assert isinstance(out["reason"], str) and out["reason"]


def test_certify_rows_operational_range_and_nonfinite_fail_technical(pipeline) -> None:
    m, x_hat = pipeline
    two_pi = 2 * np.pi                                     # inside the analytic interval
    assert error_bound.decimal_cos_sin(two_pi)[0] > 0
    for phi_bad in (two_pi, 7.0, -1e-9, np.nan):
        phi = PHI.copy()
        phi[0] = phi_bad
        assert _certify(m[4], m[32], x_hat, phi=phi)["status"] == "FAIL_TECHNICAL", phi_bad
    nan_x = x_hat.copy()
    nan_x[3] = np.nan
    assert _certify(m[4], m[32], nan_x)["status"] == "FAIL_TECHNICAL"
    assert _certify(m[4], m[32], x_hat, phi=np.nextafter(PHI, 0.0))["status"] == "CERTIFIED"


def test_certify_rows_scoring_lock_precedes_any_computation(pipeline) -> None:
    with pytest.raises(errors.AccessDenied):              # every other input is invalid
        error_bound.certify_rows(None, "not-a-matrix", [], None, np.zeros((1, 33)),
                                 np.array([99.0]), np.array([np.nan]), None, None, "scoring")
    m, x_hat = pipeline
    # Interpretation: any non-None scoring_release counts as a release token here.
    out = _certify(m[4], m[32], x_hat, split="scoring", scoring_release="owner-release-token")
    assert out["status"] == "CERTIFIED"


# ---- B6b: reference_check_rows (early gate, K1/4/32) -------------------------------------------
def test_reference_check_rows_pass_and_fail(pipeline) -> None:
    m, _ = pipeline
    ks = (1, 4, 32)
    out = error_bound.reference_check_rows(T, E, PI, COORDS, HIST, m, ks, "calibration")
    assert out["status"] == "PASS" and out["rows"] == 4
    assert sorted(out["moment_check_max"]) == [1, 4, 32]
    assert all(0.0 <= out["moment_check_max"][k] <= 1e-12 for k in ks)
    for k in ks:
        shifted = {key: val.copy() for key, val in m.items()}
        shifted[k][3, 1] += 1e-9
        bad = error_bound.reference_check_rows(T, E, PI, COORDS, HIST, shifted, ks, "validation")
        assert bad["status"] == "FAIL_TECHNICAL"
        assert bad["moment_check_max"][k] > 1e-10


def test_reference_check_rows_scoring_lock_precedes_any_computation(pipeline) -> None:
    with pytest.raises(errors.AccessDenied):
        error_bound.reference_check_rows(None, None, None, None, np.zeros((1, 33)),
                                         {1: None}, (1, 4, 32), "scoring")
    m, _ = pipeline
    out = error_bound.reference_check_rows(T, E, PI, COORDS, HIST, m, (1, 4, 32), "scoring",
                                           scoring_release="owner-release-token")
    assert out["status"] == "PASS"
