"""Independent tests, author A (job 0026): donors, symmetry, the closed-form donor posterior and
the v4 comparison rules (TEST_PLAN A-3; protocol sections 3.1, 3.2, 3.4, 15.3.16 item 15).

Fixture: a tiny periodic HMM on a 12 x 2 cylinder (x periodic; state s = 2x + y), 36 symbols
j = 6a + b, a lazy walk with entries 0.2/0.4 and emission rows that are exact column
permutations of two normalised templates, so E[rho_k z, tau_k j] == E[z, j] bitwise. Every
expected value is computed here from the protocol formulas (numpy, Fraction, Decimal) or with
the unchanged oracle.BayesFilter / error_bound / independent_reference code.
"""

from __future__ import annotations

import decimal
import sys
from decimal import Decimal
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

import c1_oracle  # noqa: E402
import error_bound  # noqa: E402
from topo_pilot.oracle import BayesFilter  # noqa: E402

NX, NY, V = 12, 2, 36
COORDS = np.array([[x, y] for x in range(NX) for y in range(NY)], dtype=np.float64)
N = len(COORDS)
DELTA = Fraction(2, 10**12)  # protocol section 3.2: delta = 2 * 10^-12 (exact)
A_TOL = Fraction(2, 10**12)  # protocol section 3.4: a = 2 * 10^-12 (exact)


def state(x, y):
    return 2 * (x % NX) + y


def tau_ref(j, k):
    a, b = divmod(int(j), 6)
    return 6 * ((a + k) % 6) + b


def make_T():
    T = np.zeros((N, N))
    for x in range(NX):
        for y in range(NY):
            s = state(x, y)
            T[s, state(x + 1, y)] = 0.2
            T[s, state(x - 1, y)] = 0.2
            T[s, state(x, 1 - y)] = 0.2
            T[s, s] = 0.4
    return T


def make_E():
    E = np.empty((N, V))
    for x0 in (0, 1):
        for y in range(NY):
            logit = np.empty(V)
            for j in range(V):
                a, b = divmod(j, 6)
                dx = abs(x0 - 2 * a) % NX
                dx = min(dx, NX - dx)
                logit[j] = -dx**2 / (2 * 1.25**2) - (y - 0.2 * b) ** 2 / 2.0
            template = np.exp(logit)
            template = template / template.sum()
            for m in range(6):
                row = np.empty(V)
                row[[tau_ref(j, m) for j in range(V)]] = template
                E[state(x0 + 2 * m, y)] = row
    return E


T, E, PI = make_T(), make_E(), np.full(N, 1.0 / N)


def rho_ref(k):
    return np.array([state(int(x) + 2 * k, int(y)) for x, y in COORDS], dtype=np.int64)


def histories(rows, seed):
    return np.random.default_rng(seed).integers(0, V, size=(rows, 32)).astype(np.uint8)


def exact_r_E(Em):
    worst = Fraction(0)
    for k in (1, -1):
        rho = rho_ref(k)
        for z in range(N):
            for v in range(V):
                ratio = Fraction(float(Em[rho[z], tau_ref(v, k)])) / Fraction(float(Em[z, v]))
                worst = max(worst, abs(ratio - 1))
    return worst


def test_tau_maps_symbol_columns_and_inverts():
    sym = np.arange(V)
    for k in (1, -1):
        got = np.asarray(c1_oracle.tau(sym, k)).astype(int)
        assert got.tolist() == [tau_ref(j, k) for j in range(V)]
    back = np.asarray(c1_oracle.tau(np.asarray(c1_oracle.tau(sym, 1)), -1)).astype(int)
    assert back.tolist() == sym.tolist()


def test_donors_shift_w1_to_w31_and_keep_w32():
    canon = histories(6, 1)
    keep = canon.copy()
    H, Hp, Hm = c1_oracle.donors(canon)
    assert np.array_equal(canon, keep)
    assert np.array_equal(np.asarray(H).astype(int), canon.astype(int))
    for D, k in ((Hp, 1), (Hm, -1)):
        D = np.asarray(D).astype(int)
        want = np.vectorize(lambda j: tau_ref(j, k))(canon[:, :31].astype(int))
        assert np.array_equal(D[:, :31], want)
        assert np.array_equal(D[:, 31], canon[:, 31].astype(int))


def test_rho_index_from_coordinates():
    for k in (1, -1):
        idx = np.asarray(c1_oracle.rho_index(COORDS, k))
        assert idx.dtype == np.int64 and np.array_equal(idx, rho_ref(k))
        assert sorted(idx.tolist()) == list(range(N))


def test_fixture_is_exactly_symmetric():
    for k in (1, -1):
        rho = rho_ref(k)
        tau = [tau_ref(j, k) for j in range(V)]
        assert np.array_equal(T[np.ix_(rho, rho)], T)
        assert np.array_equal(E[rho][:, tau], E)


def test_symmetry_report_on_the_exact_fixture():
    rep = c1_oracle.symmetry_report(T, E, PI, COORDS)
    assert rep["max_dev"] <= 1e-14 and bool(rep["exact_invariance"]) is True
    assert rep["r_E"] == 0 and rep["eps_sym"] == 0


def test_symmetry_report_measures_r_E_exactly_for_a_perturbed_emission():
    E2 = E.copy()
    E2[5, 7] = E2[5, 7] * (1.0 + 3e-13)
    E2[16, 30] = np.nextafter(E2[16, 30], 1.0)
    rep = c1_oracle.symmetry_report(T, E2, PI, COORDS)
    r_E = exact_r_E(E2)
    assert r_E > 0 and isinstance(rep["r_E"], Fraction) and rep["r_E"] == r_E
    assert rep["eps_sym"] == r_E / (1 - r_E)
    dev = max(float(np.max(np.abs(E2[rho_ref(k)][:, [tau_ref(j, k) for j in range(V)]] - E2)))
              for k in (1, -1))
    assert rep["max_dev"] == pytest.approx(dev, rel=1e-12, abs=0.0)
    assert bool(rep["exact_invariance"]) is True  # T and pi untouched


@pytest.mark.parametrize("which", ["T", "pi"])
def test_exact_invariance_fails_on_one_ulp(which):
    T2, pi2 = T.copy(), PI.copy()
    if which == "T":
        T2[0, 2] = np.nextafter(T2[0, 2], 1.0)
    else:
        pi2[3] = np.nextafter(pi2[3], 1.0)
    assert bool(c1_oracle.symmetry_report(T2, E, pi2, COORDS)["exact_invariance"]) is False


def my_closed_form(b31, w32, k):
    t = np.zeros_like(b31)
    t[:, rho_ref(k)] = b31  # t(rho_k s) = b31(s)
    u = (t @ T) * E[:, w32].T
    return u / u.sum(axis=1, keepdims=True)


def test_closed_form_index_convention_on_a_nonsymmetric_posterior():
    rng = np.random.default_rng(7)
    b31 = rng.uniform(0.1, 1.0, size=(4, N))
    b31 /= b31.sum(axis=1, keepdims=True)
    w32 = np.array([0, 13, 22, 35])
    for k in (1, -1):
        got = np.asarray(c1_oracle.closed_form_b32(b31, T, E, w32, c1_oracle.rho_index(COORDS, k)))
        want = my_closed_form(b31, w32, k)
        assert np.allclose(got, want, rtol=1e-13, atol=0.0)
        wrong = b31[:, rho_ref(k)]  # the opposite transport convention
        u = (wrong @ T) * E[:, w32].T
        assert not np.allclose(got, u / u.sum(axis=1, keepdims=True), rtol=1e-6)


def test_closed_form_agrees_with_the_direct_donor_filter_within_t_plus_t2():
    canon = histories(8, 2)
    H, Hp, Hm = (np.asarray(x).astype(np.int64) for x in c1_oracle.donors(canon))
    flt = BayesFilter(T, E, PI)
    b31 = flt.run(H).b[:, 30]
    t = 2 * DELTA / (1 - DELTA)  # eps_sym = 0 on this fixture
    for Hk, k in ((Hp, 1), (Hm, -1)):
        direct = flt.run(Hk).b[:, 31]
        cf = np.asarray(c1_oracle.closed_form_b32(b31, T, E, H[:, 31],
                                                  c1_oracle.rho_index(COORDS, k)))
        worst = max(abs(Fraction(float(x)) / Fraction(float(y)) - 1)
                    for x, y in zip(direct.ravel(), cf.ravel()))
        assert worst <= t + t * t
        assert bool(c1_oracle.rel_agree(direct.ravel(), cf.ravel(), t + t * t)) is True


def test_closed_form_tolerance_values_and_the_three_halves_switch():
    t0 = 2 * DELTA / (1 - DELTA)
    assert c1_oracle.closed_form_tolerance(Fraction(0)) == (t0, t0 + t0 * t0)
    eps = Fraction(1, 10**15)
    t1 = t0 + 62 * eps
    got = c1_oracle.closed_form_tolerance(eps)
    assert got == (t1, t1 + t1 * t1) and all(isinstance(x, Fraction) for x in got)
    assert c1_oracle.closed_form_tolerance(None) is None
    edge = (Fraction(3, 2) - t0) / 62  # t == 3/2 exactly: still the fast path
    three_halves = Fraction(3, 2)
    assert c1_oracle.closed_form_tolerance(edge) == (three_halves, three_halves + Fraction(9, 4))
    assert c1_oracle.closed_form_tolerance(edge + Fraction(1, 10**30)) is None


ULP1 = 2.0**-52


@pytest.mark.parametrize("k, ok", [(9007, True), (9008, False)])
def test_rel_agree_at_the_relative_boundary(k, ok):
    """9007 * 2^-52 < 2e-12 < 9008 * 2^-52 (exact rationals)."""
    xref = np.ones(3)
    xhat = np.array([1.0, 1.0 - 5 * ULP1, 1.0 + k * ULP1])
    assert bool(c1_oracle.rel_agree(xhat, xref, Fraction(2, 10**12))) is ok
    assert bool(c1_oracle.rel_agree(xhat, xref, Fraction(k, 2**52))) is True
    assert bool(c1_oracle.rel_agree(xhat, xref, Fraction(k, 2**52) - Fraction(1, 10**40))) is False


def test_named_canonical_four_e_minus_12_rule_boundary():
    tol = Fraction(4, 10**12)
    k_ok = int(tol * 2**52)  # largest k with k * 2^-52 <= 4e-12
    assert Fraction(k_ok, 2**52) <= tol < Fraction(k_ok + 1, 2**52)
    xref = np.full(2, 0.5)
    for k, ok in ((k_ok, True), (k_ok + 1, False)):
        xhat = np.array([0.5, 0.5 * (1.0 + k * ULP1)])
        assert bool(c1_oracle.rel_agree(xhat, xref, tol)) is ok


def dec_minus(x, text):
    with decimal.localcontext(decimal.Context(prec=80)):
        return Decimal(x) - Decimal(text)


def test_interval_rule_three_way_at_its_boundaries():
    x = 0.5
    # beta = 0: I = {x~}, D_low = D_high = |x^ - x~|
    assert c1_oracle.interval_rule([x], [dec_minus(x, "2E-12")], Fraction(0)) == "PASS"
    assert c1_oracle.interval_rule([x], [dec_minus(x, "2.00000001E-12")], Fraction(0)) == \
        "FAIL_TECHNICAL/ORACLE"
    assert c1_oracle.interval_rule([x], [dec_minus(x, "1.99999999E-12")], Fraction(0)) == "PASS"
    # x^ inside I with an endpoint farther than a: undetermined
    beta = Fraction(1, 10**11)
    xt = Fraction(Decimal(x))
    assert xt / (1 - beta) - xt > A_TOL and xt - xt / (1 + beta) > A_TOL
    assert c1_oracle.interval_rule([x], [Decimal(x)], beta) == "INCONCLUSIVE/NUMERICAL"
    # vectors: the worst component decides
    good, bad = Decimal(x), dec_minus(x, "3E-12")
    assert c1_oracle.interval_rule([x, x], [good, Decimal(x)], beta) == "INCONCLUSIVE/NUMERICAL"
    assert c1_oracle.interval_rule([x, x], [good, bad], Fraction(0)) == "FAIL_TECHNICAL/ORACLE"
    for nonfinite in (float("nan"), float("inf")):
        assert c1_oracle.interval_rule([x, nonfinite], [good, good], Fraction(0)) == \
            "FAIL_TECHNICAL/ORACLE"


def test_h3_compare_branches_and_zero_posterior_entries():
    one = [Decimal(1)] * 3
    assert c1_oracle.h3_compare(np.array([1.0, 1.0, 1.0 + 9007 * ULP1]), one, True, None) == "PASS"
    assert c1_oracle.h3_compare(np.array([1.0, 1.0, 1.0 + 9008 * ULP1]), one, True, None) == \
        "FAIL_TECHNICAL/ORACLE"
    beta = error_bound.posterior_envelope(32, N)
    tiny = [Decimal("0.6"), Decimal("0.4"), Decimal("1E-300")]
    zero_entry = np.array([0.6, 0.4, 0.0])  # an underflowed operational posterior entry
    assert c1_oracle.h3_compare(zero_entry, tiny, False, beta) == "PASS"
    assert c1_oracle.h3_compare(zero_entry, tiny, True, beta) == "FAIL_TECHNICAL/ORACLE"
    gross = np.array([0.6, 0.4 + 1e-9, 0.0])
    assert c1_oracle.h3_compare(gross, tiny, False, beta) == "FAIL_TECHNICAL/ORACLE"


def decimal_closed_form(b31_dec, w32, k):
    rho = rho_ref(k)
    with decimal.localcontext(error_bound.trapping_context(60)):
        t = [Decimal(0)] * N
        for s in range(N):
            t[rho[s]] = b31_dec[s]
        u = [sum((t[s] * Decimal(float(T[s, z])) for s in range(N) if T[s, z] > 0), Decimal(0))
             * Decimal(float(E[z, w32])) for z in range(N)]
        total = sum(u, Decimal(0))
        return [x / total for x in u]


def test_enclosure_branch_corrupted_float_closed_form_fails():
    """Section 3.2 S1 fixture: corrupted float64 closed-form values on the enclosure branch,
    with both Decimal references correct -> FAIL_TECHNICAL/ORACLE."""
    h = histories(1, 3)[0].astype(np.int64)
    flt = BayesFilter(T, E, PI)
    b31 = flt.run(h[None, :]).b[:, 30]
    beta = error_bound.posterior_envelope(32, N)
    b31_dec = c1_oracle.decimal_posterior60(T, E, PI, h[:31])
    for k in (1, -1):
        cf = np.asarray(c1_oracle.closed_form_b32(b31, T, E, h[None, 31],
                                                  c1_oracle.rho_index(COORDS, k)))[0]
        ref_c = decimal_closed_form(b31_dec, int(h[31]), k)
        assert c1_oracle.interval_rule(cf, ref_c, beta) == "PASS"
        bad = cf.copy()
        j = int(np.argmax(bad))
        bad[j] = bad[j] * (1.0 + 1e-6)
        assert c1_oracle.interval_rule(bad, ref_c, beta) == "FAIL_TECHNICAL/ORACLE"
        hk = np.asarray(c1_oracle.donors(h[None, :])[1 if k == 1 else 2])[0].astype(np.int64)
        ref_d = c1_oracle.decimal_posterior60(T, E, PI, hk)
        s = 2 * beta / (1 - beta)  # eps_sym = 0
        worst = max(abs(Fraction(a) / Fraction(b) - 1) for a, b in zip(ref_d, ref_c))
        assert worst <= s + s * s
