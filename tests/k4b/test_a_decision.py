"""K4b author A, TEST_PLAN A6, A10, A11 (protocol §5.4, §5.5, §7.1, §8.1-§8.3).

A6: B_num (k4b_cert.b_num, margin) and the decision boundaries of k4b_stats.model_status and
overall, in exact rationals with strict inequalities. A10 (v2, RC1): an analytically specified,
enumerable zero-width law of the two one-sided bounds; the false-SUPPORT and false-EXCLUDE
events are disjoint opposite tails whose probabilities add (exact, not simulated). A11 (v2):
the deterministic F_plan and F_test <= F_plan under the cap and P2 for n <= 12,288.
Bound values L and U are chosen exactly representable in binary64 where they sit on a
boundary, so a Fraction(float(x)) reading inside the module cannot move them."""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction as Fr
from itertools import product
from math import comb
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
             "tools/x4_circle_history", "tools/x4_oracle_profile"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import c1_bounds  # noqa: E402
import k4b_cert  # noqa: E402
import k4b_config  # noqa: E402
import k4b_stats  # noqa: E402

M = Fr(1, 100)
ALPHA = Fr(5, 300)
U53 = Fr(1, 2 ** 53)
ZETA = Fr(1, 2 ** 800)
CAP = Fr(1, 10 ** 4)
FLOOR = Fr(1, 10 ** 9)
TINY = Fr(1, 10 ** 30)
MODELS = (1729, 2718, 3141)


def F(x):
    return Fr(float(x))


def gamma(m):
    return m * U53 / (1 - m * U53)


def ref_B_constant(max_b, max_abs, n):
    d = 0
    while 2 ** d < n:
        d += 1
    return (1 + Fr(1, 2 ** 30)) * Fr(max_b) + ZETA + gamma(d + 1) * Fr(float(max_abs)) + ZETA


def status(L, U, Fm, Fp):
    return k4b_stats.model_status(L, U, Fm, Fp)


def ref_status(L, U, Fm, Fp):
    def core(fm, fp):
        if L - fm > M:
            return "SUPPORT"
        if U + fp < M and L - fm > -M:
            return "EXCLUDE"
        return "UNRESOLVED"
    s, s0 = core(Fm, Fp), core(0, 0)
    if s == "UNRESOLVED" and s0 != "UNRESOLVED":
        s = "UNRESOLVED/NUMERICAL"
    return s, s0, U + Fp < -M


# ---------------------------------------------------------------- constants, b_num, margin

def test_threshold_constants():
    assert k4b_config.MARGIN == M
    assert k4b_config.CAP == CAP
    assert k4b_config.FLOOR == FLOOR == c1_bounds.FLOOR
    assert k4b_config.ALPHA == ALPHA


@pytest.mark.parametrize("n,d", [(1, 0), (2, 1), (3, 2), (3072, 12), (4096, 12), (4097, 13),
                                 (6144, 13), (8192, 13), (8193, 14), (12288, 14)])
def test_b_num_matches_B_constant_and_closed_form(n, d):
    assert (n - 1).bit_length() == d
    for max_b, max_abs in ((Fr(0), 0.0), (Fr(1, 10 ** 15), 0.37), (CAP, 4.0), (Fr(3, 7), 1.5)):
        got = k4b_cert.b_num(max_b, max_abs, n)
        assert got == c1_bounds.B_constant(max_b, max_abs, n)
        assert got == ref_B_constant(max_b, max_abs, n)
        assert got == (1 + Fr(1, 2 ** 30)) * max_b + gamma(d + 1) * F(max_abs) + 2 * ZETA


def test_b_num_is_monotone():
    base = k4b_cert.b_num(Fr(1, 10 ** 6), 1.0, 3072)
    assert k4b_cert.b_num(Fr(2, 10 ** 6), 1.0, 3072) > base
    assert k4b_cert.b_num(Fr(1, 10 ** 6), 2.0, 3072) > base
    assert k4b_cert.b_num(Fr(1, 10 ** 6), 1.0, 4097) > base
    assert k4b_cert.b_num(Fr(1, 10 ** 6), 1.0, 4096) == base


def test_margin_floor_and_transport():
    Z = Fr(212, 10 ** 14)
    assert k4b_cert.margin(Fr(1, 10 ** 15), Z) == FLOOR + Z
    assert k4b_cert.margin(FLOOR, Z) == FLOOR + Z
    assert k4b_cert.margin(Fr(1, 10 ** 6), Z) == Fr(1, 10 ** 6) + Z
    assert k4b_cert.margin(Fr(1, 10 ** 6), Fr(0)) == Fr(1, 10 ** 6)
    assert isinstance(k4b_cert.margin(Fr(0), Z), Fr)


# ---------------------------------------------------------------- model_status boundaries (A6)

def test_support_boundary_is_strict():
    L, U = F(0.0125), F(0.05)
    Fm = L - M  # L - F- == 1/100 exactly
    r = status(L, U, Fm, FLOOR)
    assert r["status"] == "UNRESOLVED/NUMERICAL" and r["status_without_F"] == "SUPPORT"
    r = status(L, U, Fm - TINY, FLOOR)
    assert r["status"] == "SUPPORT" and r["status_without_F"] == "SUPPORT"


def test_exclude_upper_boundary_is_strict():
    L, U = F(0.0), F(0.0075)
    Fp = M - U  # U + F+ == 1/100 exactly
    r = status(L, U, FLOOR, Fp)
    assert r["status"] == "UNRESOLVED/NUMERICAL" and r["status_without_F"] == "EXCLUDE"
    assert status(L, U, FLOOR, Fp - TINY)["status"] == "EXCLUDE"


def test_exclude_lower_boundary_is_strict():
    L, U = F(-0.0075), F(0.0)
    Fm = L + M  # L - F- == -1/100 exactly
    r = status(L, U, Fm, FLOOR)
    assert r["status"] == "UNRESOLVED/NUMERICAL" and r["status_without_F"] == "EXCLUDE"
    assert status(L, U, Fm - TINY, FLOOR)["status"] == "EXCLUDE"


def test_plain_support_exclude_unresolved():
    r = status(F(0.03), F(0.05), FLOOR, FLOOR)
    assert r["status"] == "SUPPORT" and "NEGATIVE_ALIGNMENT" not in r["labels"]
    r = status(F(-0.002), F(0.004), FLOOR, FLOOR)
    assert r["status"] == "EXCLUDE" and r["status_without_F"] == "EXCLUDE"
    r = status(F(0.005), F(0.02), FLOOR, FLOOR)
    assert r["status"] == "UNRESOLVED" and r["status_without_F"] == "UNRESOLVED"


def test_negative_alignment_label():
    r = status(F(-0.03), F(-0.02), FLOOR, FLOOR)
    assert r["status"] == "UNRESOLVED" and "NEGATIVE_ALIGNMENT" in r["labels"]
    U = F(-0.0125)
    r = status(F(-0.03), U, FLOOR, -M - U)  # U + F+ == -1/100 exactly: no label
    assert "NEGATIVE_ALIGNMENT" not in r["labels"]
    r = status(F(-0.03), U, FLOOR, -M - U - TINY)
    assert "NEGATIVE_ALIGNMENT" in r["labels"]
    r = status(F(0.0), F(0.004), FLOOR, FLOOR)
    assert "NEGATIVE_ALIGNMENT" not in r["labels"]


def test_status_table_and_exclusivity():
    vals = [F(v) for v in (-0.03, -0.0125, -0.01, -0.0075, 0.0, 0.0075, 0.01, 0.0125, 0.03)]
    margins = [Fr(0), FLOOR, Fr(1, 400), M]
    allowed = {"SUPPORT", "EXCLUDE", "UNRESOLVED", "UNRESOLVED/NUMERICAL"}
    for L, U in product(vals, vals):
        if L > U:
            continue
        for Fm, Fp in product(margins, margins):
            r = status(L, U, Fm, Fp)
            s, s0, neg = ref_status(L, U, Fm, Fp)
            assert r["status"] in allowed
            assert (r["status"], r["status_without_F"]) == (s, s0)
            assert ("NEGATIVE_ALIGNMENT" in r["labels"]) == neg
            sup, exc = L - Fm > M, U + Fp < M and L - Fm > -M
            assert not (sup and exc)


def test_overall_table():
    states = ["SUPPORT", "EXCLUDE", "UNRESOLVED", "UNRESOLVED/NUMERICAL"]
    for combo in product(states, repeat=3):
        per = dict(zip(MODELS, combo))
        if all(s == "SUPPORT" for s in combo):
            want = "SUPPORT"
        elif all(s == "EXCLUDE" for s in combo):
            want = "EXCLUSION"
        elif any(s in ("SUPPORT", "EXCLUDE") for s in combo):
            want = "MIXED"
        elif "UNRESOLVED/NUMERICAL" in combo:
            want = "INCONCLUSIVE/NUMERICAL"
        else:
            want = "INCONCLUSIVE"
        assert k4b_stats.overall(per) == want, combo


# ---------------------------------------------------------------- RC1 counterexample (A10)

MU = Fr(1, 100)  # zero width: E X- = E X+ = 0.01; neither SUPPORT nor EXCLUDE is true
DELTA = Fr(1, 2 ** 10)
HALF_W = Fr(11, 2) * DELTA


def _events(law):
    """law: {offset k: probability}; estimate = MU + k*DELTA, L = est - HALF_W, U = est + HALF_W."""
    sup, exc = set(), set()
    for k in law:
        est = MU + k * DELTA
        st = status(est - HALF_W, est + HALF_W, FLOOR, FLOOR)["status"]
        if st == "SUPPORT":
            sup.add(k)
        elif st == "EXCLUDE":
            exc.add(k)
    return sup, exc


def test_truth_is_neither_support_nor_exclude():
    assert not (MU > M) and not (MU < M)


def test_rc1_binomial_tails_add():
    n = 20
    law = {x - 10: Fr(comb(n, x), 2 ** n) for x in range(n + 1)}
    assert sum(law.values()) == 1
    sup, exc = _events(law)
    assert sup == set(range(6, 11)) and exc == set(range(-10, -5))
    assert not (sup & exc)
    p_sup, p_exc = sum(law[k] for k in sup), sum(law[k] for k in exc)
    assert p_sup == p_exc == Fr(6196, 2 ** 20)  # closed form: C(20,16..20) / 2^20
    assert p_sup <= ALPHA and p_exc <= ALPHA
    combined = sum(law[k] for k in sup | exc)
    assert combined == p_sup + p_exc
    assert combined > p_sup and combined > p_exc
    assert combined <= 2 * ALPHA


def test_rc1_three_point_law_attains_two_alpha():
    law = {6: ALPHA, 0: 1 - 2 * ALPHA, -6: ALPHA}
    sup, exc = _events(law)
    assert sup == {6} and exc == {-6}
    p_sup, p_exc = law[6], law[-6]
    combined = sum(law[k] for k in sup | exc)
    assert p_sup == ALPHA and p_exc == ALPHA
    assert combined == p_sup + p_exc == 2 * ALPHA
    assert combined > ALPHA  # the v1 claim (per-model error <= alpha) fails


def test_rc1_family_arithmetic():
    assert 6 * ALPHA == Fr(1, 10)
    assert 3 * ALPHA == Fr(1, 20)


# ---------------------------------------------------------------- F_plan (A11)

@pytest.mark.parametrize("Z", [Fr(0), Fr(212, 10 ** 14), Fr(1, 10 ** 6)])
def test_F_plan_exact(Z):
    got = k4b_cert.F_plan(Z)
    assert isinstance(got, Fr)
    assert got == max(c1_bounds.B_constant(CAP, 4, 12288), FLOOR) + Z
    assert got == (1 + Fr(1, 2 ** 30)) * CAP + 2 * ZETA + gamma(15) * 4 + Z
    assert (12288 - 1).bit_length() == 14


def test_F_plan_desk_values():
    assert abs(float(k4b_cert.F_plan(Fr(0))) - 1.0000000009979e-4) < 1e-17
    assert abs(float(k4b_cert.F_plan(Fr(212, 10 ** 14))) - 1.0000000221979e-4) < 1e-17
    assert c1_bounds.B_constant(CAP, 4, 12288) > FLOOR


def test_F_test_never_exceeds_F_plan_under_cap_and_p2():
    Z = Fr(212, 10 ** 14)
    plan = k4b_cert.F_plan(Z)
    rng = random.Random(610103)
    max_bs = [Fr(0), Fr(1, 10 ** 15), FLOOR, Fr(1, 2 * 10 ** 4), CAP]
    max_bs += [CAP * Fr(rng.randint(0, 10 ** 6), 10 ** 6) for _ in range(5)]
    abses = [0.0, 0.5, 2.0, 3.999999, 4.0]
    ns = [1, 2, 3072, 6144, 8192, 8193, 12287, 12288]
    for mb, ma, n in product(max_bs, abses, ns):
        assert k4b_cert.margin(k4b_cert.b_num(mb, ma, n), Z) <= plan


def test_F_plan_conditions_are_needed():
    Z = Fr(212, 10 ** 14)
    plan = k4b_cert.F_plan(Z)
    assert k4b_cert.margin(k4b_cert.b_num(CAP, 4.0, 12288), Z) == plan
    assert k4b_cert.margin(k4b_cert.b_num(CAP + Fr(1, 10 ** 12), 4.0, 12288), Z) > plan
    above4 = math.nextafter(4.0, 5.0)
    assert k4b_cert.margin(k4b_cert.b_num(CAP, above4, 12288), Z) > plan
    assert k4b_cert.margin(k4b_cert.b_num(CAP, 4.0, 16384), Z) == plan  # same d_n = 14
    assert k4b_cert.margin(k4b_cert.b_num(CAP, 4.0, 16385), Z) > plan
