"""K4b author A, TEST_PLAN A3, A5, A8 (protocol §5.2, §5.3; CERTIFICATE §1, §3).

A3: Lemma N (k4b_cert.isqrt_bracket, norm_bound) against exact rationals: s = 0, tiny values,
adversarial n_hat. A5: phase_bound (= error_bound.row_bound B) at K = 1 and 2, envelopes.
A8: the cap (1/10^4 passes, anything above fails) and the P2 analogue (|X| <= 4, finite).
Reference moments are passed as Decimal pairs, the type error_bound.reference_moments returns."""

from __future__ import annotations

import math
import random
import sys
from decimal import Decimal
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
             "tools/x4_circle_history", "tools/x4_oracle_profile"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import error_bound  # noqa: E402
import k4b_cert  # noqa: E402
import k4b_config  # noqa: E402

D80 = 10 ** 80
ONE_D = Fr(1, D80)
THREE_HALVES = Fr(3, 2)


def dec2(x, y):
    return (Decimal(x), Decimal(y))


def ref_k(s, D=D80):
    return math.isqrt(s.numerator * D * D // s.denominator)


def ref_norm_bound(n_hat, M32, M4, e4, e32):
    r = (Fr(M32[0]) - Fr(M4[0]), Fr(M32[1]) - Fr(M4[1]))
    k = ref_k(r[0] ** 2 + r[1] ** 2)
    n = Fr(float(n_hat))
    return max(abs(n - Fr(k, D80)), abs(n - Fr(k + 1, D80))) + THREE_HALVES * (e4 + e32)


def covers(n, B, s_star):
    """Exact test of |n - sqrt(s_star)| <= B by squares."""
    n, lo, hi = Fr(float(n)), Fr(float(n)) - B, Fr(float(n)) + B
    return hi >= 0 and hi * hi >= s_star and (lo <= 0 or lo * lo <= s_star)


@pytest.fixture(scope="module")
def eps():
    return k4b_cert.envelopes()


# ---------------------------------------------------------------- isqrt_bracket (A3)

def test_isqrt_zero():
    assert k4b_cert.isqrt_bracket(Fr(0)) == 0
    assert k4b_cert.isqrt_bracket(Fr(0), D=10) == 0


def test_isqrt_perfect_squares_are_exact():
    assert k4b_cert.isqrt_bracket(Fr(1, 4)) == D80 // 2
    assert k4b_cert.isqrt_bracket(Fr(9, 16)) == 3 * D80 // 4
    assert k4b_cert.isqrt_bracket(Fr(25)) == 5 * D80
    assert k4b_cert.isqrt_bracket(Fr(1)) == D80


def test_isqrt_sqrt2_digits_and_bracket():
    k = k4b_cert.isqrt_bracket(Fr(2))
    assert k * k <= 2 * D80 * D80 < (k + 1) ** 2
    assert str(k).startswith("14142135623730950488016887242096980785696")
    assert k4b_cert.isqrt_bracket(Fr(2), D=10) == 14
    assert k4b_cert.isqrt_bracket(Fr(2), D=1000) == 1414


def test_isqrt_tiny_values():
    assert k4b_cert.isqrt_bracket(Fr(1, 10 ** 200)) == 0
    assert k4b_cert.isqrt_bracket(Fr(1, 10 ** 160)) == 1  # sqrt = 1/D exactly
    assert k4b_cert.isqrt_bracket(Fr(10 ** 160 - 1, 10 ** 320)) == 0  # just below 1/D
    assert k4b_cert.isqrt_bracket(Fr(4, 10 ** 160)) == 2
    assert k4b_cert.isqrt_bracket(Fr(1, 10 ** 100)) == 10 ** 30


def test_isqrt_bracket_property_random():
    rng = random.Random(20261016)
    for _ in range(200):
        s = Fr(rng.randint(0, 10 ** rng.randint(1, 40)), rng.randint(1, 10 ** rng.randint(1, 60)))
        k = k4b_cert.isqrt_bracket(s)
        assert k == ref_k(s)
        assert Fr(k, D80) ** 2 <= s < Fr(k + 1, D80) ** 2


# ---------------------------------------------------------------- norm_bound (A3)

def test_norm_bound_s_zero(eps):
    e = THREE_HALVES * (eps[4] + eps[32])
    M = dec2("0.25", "-0.5")
    assert k4b_cert.norm_bound(0.0, M, M, eps[4], eps[32]) == ONE_D + e
    tiny = 1e-300
    assert k4b_cert.norm_bound(tiny, M, M, eps[4], eps[32]) == ONE_D - Fr(tiny) + e
    assert k4b_cert.norm_bound(1e-3, M, M, eps[4], eps[32]) == Fr(1e-3) + e
    sub = 5e-324  # smallest subnormal
    assert k4b_cert.norm_bound(sub, M, M, eps[4], eps[32]) == ONE_D - Fr(sub) + e


def test_norm_bound_exact_pythagorean(eps):
    e = THREE_HALVES * (eps[4] + eps[32])
    M32, M4 = dec2("0.35", "0.45"), dec2("0.05", "0.05")  # r = (0.3, 0.4), |r| = 1/2
    assert k4b_cert.norm_bound(0.5, M32, M4, eps[4], eps[32]) == ONE_D + e
    above = math.nextafter(0.5, 1.0)
    assert k4b_cert.norm_bound(above, M32, M4, eps[4], eps[32]) == Fr(above) - Fr(1, 2) + e
    below = math.nextafter(0.5, 0.0)
    assert k4b_cert.norm_bound(below, M32, M4, eps[4], eps[32]) == \
        Fr(1, 2) + ONE_D - Fr(below) + e


@pytest.mark.parametrize("n_hat", [0.0, -0.5, 2.0, 1e308, 5e-324, 0.49999999, 0.25])
def test_norm_bound_adversarial_n_hat(eps, n_hat):
    M32, M4 = dec2("0.35", "0.45"), dec2("0.05", "0.05")
    B = k4b_cert.norm_bound(n_hat, M32, M4, eps[4], eps[32])
    assert isinstance(B, Fr)
    assert B == ref_norm_bound(n_hat, M32, M4, eps[4], eps[32])
    assert abs(Fr(n_hat) - Fr(1, 2)) <= B - THREE_HALVES * (eps[4] + eps[32])


@pytest.mark.parametrize("pair", [("1", "1"), ("0.1", "0.1"), ("-0.7", "0.2"), ("1.3", "-0.9")])
def test_norm_bound_irrational_norms(eps, pair):
    M32, M4 = dec2(*pair), dec2("0", "0")
    s = Fr(Decimal(pair[0])) ** 2 + Fr(Decimal(pair[1])) ** 2
    n_hat = math.hypot(float(pair[0]), float(pair[1]))
    B = k4b_cert.norm_bound(n_hat, M32, M4, eps[4], eps[32])
    assert B == ref_norm_bound(n_hat, M32, M4, eps[4], eps[32])
    k = ref_k(s)
    core = B - THREE_HALVES * (eps[4] + eps[32])
    assert abs(Fr(n_hat) - Fr(k, D80)) <= core and abs(Fr(n_hat) - Fr(k + 1, D80)) <= core
    assert core < Fr(1, 10 ** 15)  # a correctly rounded float norm is close
    assert covers(n_hat, B, s)


def test_norm_bound_tiny_values(eps):
    e = THREE_HALVES * (eps[4] + eps[32])
    Z = dec2("0", "0")
    M = dec2("1E-50", "0")  # s = 1e-100, sqrt = 1e-50 = 10^30 / D exactly
    n = 1e-50
    expect = max(abs(Fr(n) - Fr(10 ** 30, D80)), abs(Fr(n) - Fr(10 ** 30 + 1, D80))) + e
    assert k4b_cert.norm_bound(n, M, Z, eps[4], eps[32]) == expect
    M = dec2("3E-90", "4E-90")  # |r| = 5e-90 < 1/D: k = 0
    n = 5e-90
    assert k4b_cert.norm_bound(n, M, Z, eps[4], eps[32]) == ONE_D - Fr(n) + e


def test_norm_bound_covers_perturbed_true_residual():
    """Lemma N soundness: every r* within eps4 + eps32 per coordinate of r~ is covered."""
    e4 = e32 = Fr(1, 1000)
    e = e4 + e32
    M32, M4 = dec2("0.35", "0.45"), dec2("0.05", "0.05")
    B = k4b_cert.norm_bound(0.5, M32, M4, e4, e32)
    assert B == ONE_D + THREE_HALVES * e
    r = (Fr(3, 10), Fr(2, 5))
    for dx in (-e, Fr(0), e):
        for dy in (-e, Fr(0), e):
            assert covers(0.5, B, (r[0] + dx) ** 2 + (r[1] + dy) ** 2)
    t = e / 4  # radial: per-coordinate gap 4t = e, |r*| = 1/2 + 5t (rational)
    r_star_norm = Fr(1, 2) + 5 * t
    assert abs(Fr(1, 2) - r_star_norm) <= B


def test_norm_bound_other_K_uses_its_envelope(eps):
    M32, M2 = dec2("0.2", "-0.1"), dec2("0.15", "0.05")
    n = math.hypot(0.05, -0.15)
    b4 = k4b_cert.norm_bound(n, M32, M2, eps[4], eps[32])
    b2 = k4b_cert.norm_bound(n, M32, M2, eps[2], eps[32])
    assert b4 - b2 == THREE_HALVES * (eps[4] - eps[2])


# ---------------------------------------------------------------- envelopes, phase_bound (A5)

def test_envelopes_match_error_bound(eps):
    assert set(eps) == {1, 2, 4, 32}
    for K in (1, 2, 4, 32):
        ref = error_bound.moment_envelope(error_bound.posterior_envelope(K, 144), 144)
        assert eps[K] == ref and isinstance(eps[K], Fr)
        assert 0 < eps[K] < Fr(1, 10 ** 50)
    assert eps[1] < eps[2] < eps[4] < eps[32]
    assert set(k4b_cert.envelopes((1, 2))) == {1, 2}


@pytest.mark.parametrize("K", [1, 2])
def test_phase_bound_at_K_equals_row_bound(eps, K):
    M32, MK = dec2("0.31", "-0.12"), dec2("0.05", "0.02")
    for phi in (0.0, 1.0, 2.5, 6.0):
        r = (0.31 - 0.05, -0.12 - 0.02)
        x_hat = math.cos(phi) * r[0] + math.sin(phi) * r[1]
        B = k4b_cert.phase_bound(x_hat, phi, MK, M32, eps[K], eps[32])
        ref = error_bound.row_bound(x_hat, phi, MK, M32, eps[K], eps[32])["B"]
        assert B == ref and isinstance(B, Fr)
        assert B < Fr(1, 10 ** 15)
        assert k4b_cert.cap_ok(B)


@pytest.mark.parametrize("K", [1, 2])
def test_phase_bound_closed_form_at_phi_zero(eps, K):
    M32, MK = dec2("0.31", "-0.12"), dec2("0.05", "0.02")
    rx, ry = Fr(26, 100), Fr(-14, 100)
    x_hat = 0.26
    B = k4b_cert.phase_bound(x_hat, 0.0, MK, M32, eps[K], eps[32])
    expect = abs(Fr(x_hat) - rx) + error_bound.EPS_V * (abs(rx) + abs(ry)) \
        + 2 * (eps[K] + eps[32])
    assert B == expect


def test_phase_bound_K1_K2_differ_by_envelopes(eps):
    M32, MK = dec2("0.4", "0.1"), dec2("-0.2", "0.3")
    x_hat, phi = 0.123, 0.7
    b1 = k4b_cert.phase_bound(x_hat, phi, MK, M32, eps[1], eps[32])
    b2 = k4b_cert.phase_bound(x_hat, phi, MK, M32, eps[2], eps[32])
    assert b2 - b1 == 2 * (eps[2] - eps[1])


def test_phase_bound_detects_a_wrong_score(eps):
    M32, MK = dec2("0.31", "-0.12"), dec2("0.05", "0.02")
    B = k4b_cert.phase_bound(0.26 + 1e-3, 0.0, MK, M32, eps[1], eps[32])
    assert B >= Fr(1, 1000) - Fr(1, 10 ** 15)
    assert not k4b_cert.cap_ok(B)


def test_phase_bound_refuses_phase_outside_domain(eps):
    M32, MK = dec2("0.31", "-0.12"), dec2("0.05", "0.02")
    with pytest.raises(Exception):
        k4b_cert.phase_bound(0.1, 7.0, MK, M32, eps[1], eps[32])
    with pytest.raises(Exception):
        k4b_cert.phase_bound(0.1, -0.5, MK, M32, eps[2], eps[32])


# ---------------------------------------------------------------- cap and P2 (A8)

def test_cap_constant_and_boundary():
    cap = k4b_config.CAP
    assert cap == Fr(1, 10 ** 4)
    assert k4b_cert.cap_ok(cap)
    assert k4b_cert.cap_ok(Fr(0))
    assert not k4b_cert.cap_ok(cap + Fr(1, 10 ** 200))
    assert k4b_cert.cap_ok(cap - Fr(1, 10 ** 200))


def test_cap_is_exact_not_float():
    f = 1e-4  # the double nearest 1e-4 lies above 1/10^4
    assert Fr(f) > Fr(1, 10 ** 4)
    assert not k4b_cert.cap_ok(Fr(f))
    below = math.nextafter(f, 0.0)
    assert Fr(below) < Fr(1, 10 ** 4)
    assert k4b_cert.cap_ok(Fr(below))


def test_p2_analogue():
    assert k4b_config.P2_MAX_ABS == 4
    assert k4b_cert.p2_ok(np.array([4.0, -4.0, 0.0, 3.999, -1e-300]))
    assert not k4b_cert.p2_ok(np.array([0.0, np.nextafter(4.0, 5.0)]))
    assert not k4b_cert.p2_ok(np.array([np.nextafter(-4.0, -5.0)]))
    for bad in (np.nan, np.inf, -np.inf):
        assert not k4b_cert.p2_ok(np.array([0.1, bad]))
