"""Independent tests (author B, job 0026), TEST_PLAN B-4 items 1-3, 6, 12, 13 (oracle side).

Protocol §15.3.2 C0, §15.3.3 P0-P4 and A1, §15.3.6 (Theorems 1 and 1', M-ln), §15.3.7 (route F);
CERTIFICATE.md §2-§6; API.md §5. Written from the protocol and the four contract documents only;
no tools/c1prime source was read and nothing was executed by the author.

References: a pure-Python replica of the prescribed C0 expressions (bitwise target), an exact
Fraction forward filter (literal stored weights; unnormalised forward sums, normalised once), the
unchanged `independent_reference.decimal_suffix_posterior` and K4 `error_bound` envelopes, and
40-digit Decimal logarithms. Ambiguities recorded: `route_f` is called on one 32-token history
and its [V] predictive; `measured_log_error` receives [R, k] arrays and the maximum is taken over
each row's k values; API.md does not say whether `rho_main` itself enforces P4 (r_h <= 1/2).
"""

from __future__ import annotations

import decimal
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest
from topo_pilot.oracle import BayesFilter

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_cert  # noqa: E402
import c1_records  # noqa: E402
import error_bound  # noqa: E402
import independent_reference  # noqa: E402

pytestmark = pytest.mark.analysis

U = Fraction(1, 2**53)
U1 = U / (1 - U)
TWO_M1000 = Fraction(1, 2**1000)


def _ring(N, stay=0.5):
    T = np.zeros((N, N))
    for i in range(N):
        T[i, i] = stay
        T[i, (i + 1) % N] += (1 - stay) / 2
        T[i, (i - 1) % N] += (1 - stay) / 2
    return T


def _hmm(N, V, kind, seed):
    rng = np.random.default_rng(seed)
    T = _ring(N) if kind == "ring" else rng.random((N, N)) + 0.1
    T = T / T.sum(axis=1, keepdims=True)
    E = rng.random((N, V)) + 0.2
    return T, E / E.sum(axis=1, keepdims=True), np.full(N, 1.0 / N)


def _support(T) -> int:
    nz = T > 0
    return int(max(nz.sum(axis=0).max(), nz.sum(axis=1).max()))


def _c0(T, E, pi, tok, include_zeros=False):
    """The C0 expressions of §15.3.2 in Python floats (IEEE binary64, no FMA)."""
    N, V = E.shape
    keep = (lambda x: True) if include_zeros else (lambda x: x > 0)
    scol = [[zp for zp in range(N) if keep(T[zp, z])] for z in range(N)]
    srow = [[zp for zp in range(N) if keep(T[z, zp])] for z in range(N)]
    R, L = tok.shape
    b = np.empty((R, L, N))
    for i in range(R):
        u = [float(pi[s]) * float(E[s, tok[i, 0]]) for s in range(N)]
        for t in range(L):
            if t:
                prev, u = b[i, t - 1], []
                for z in range(N):
                    acc = None
                    for zp in scol[z]:
                        term = float(prev[zp]) * float(T[zp, z])
                        acc = term if acc is None else acc + term
                    u.append(acc * float(E[z, tok[i, t]]))
            D = u[0]
            for s in range(1, N):
                D = D + u[s]
            b[i, t] = [x / D for x in u]
    TE = []
    for z in range(N):
        row = []
        for v in range(V):
            acc = None
            for zp in srow[z]:
                term = float(T[z, zp]) * float(E[zp, v])
                acc = term if acc is None else acc + term
            row.append(acc)
        TE.append(row)
    q = np.empty((R, V))
    for i in range(R):
        for v in range(V):
            acc = float(b[i, L - 1, 0]) * TE[0][v]
            for z in range(1, N):
                acc = acc + float(b[i, L - 1, z]) * TE[z][v]
            q[i, v] = acc
    return b, q


def _exact(T, E, pi, row):
    """Exact b*_32 and literal q* = b*_32 T E (stored weights read as exact rationals)."""
    N, V = E.shape
    Tf = [[Fraction(float(x)) for x in r] for r in T]
    Ef = [[Fraction(float(x)) for x in r] for r in E]
    alpha = [Fraction(float(pi[s])) * Ef[s][int(row[0])] for s in range(N)]
    for w in row[1:]:
        alpha = [sum((alpha[zp] * Tf[zp][z] for zp in range(N) if Tf[zp][z]), Fraction(0))
                 * Ef[z][int(w)] for z in range(N)]
    total = sum(alpha, Fraction(0))
    b = [a / total for a in alpha]
    TE = [[sum((Tf[z][zp] * Ef[zp][v] for zp in range(N)), Fraction(0)) for v in range(V)]
          for z in range(N)]
    return b, [sum((b[z] * TE[z][v] for z in range(N)), Fraction(0)) for v in range(V)]


def _mag(approx, exact) -> Fraction:
    """A rational upper bound of max |log(approx/exact)|: log r <= r - 1, -log r <= 1/r - 1."""
    worst = Fraction(0)
    for x, y in zip(approx, exact):
        r = Fraction(float(x)) / y
        worst = max(worst, r - 1, 1 / r - 1)
    return worst


def _up(c: Fraction) -> float:
    f = float(c)
    return math.nextafter(f, math.inf) if Fraction(f) < c else f


# --- Theorem 1 and the C0 kernel (items 1, 13) ----------------------------------------------------


@pytest.mark.parametrize("N,V,kind,seed", [(4, 3, "ring", 1), (7, 4, "dense", 2),
                                           (12, 5, "ring", 3), (12, 3, "dense", 4)])
def test_reference_oracle_is_C0_bitwise_and_obeys_theorem1(N, V, kind, seed):
    T, E, pi = _hmm(N, V, kind, seed)
    tok = np.random.default_rng(seed + 10).integers(0, V, size=(3, 32))
    res = c1_cert.reference_oracle(T, E, pi, tok)
    b, q = _c0(T, E, pi, tok)
    assert np.array_equal(np.asarray(res["b"]), b)
    assert np.array_equal(np.asarray(res["q_ref"]), q)
    assert np.array_equal(np.asarray(res["nu_min"]), b.min(axis=(1, 2)))
    assert np.all(np.asarray(res["finite"]))
    d = _support(T)
    rho = Fraction(c1_cert.rho_bar_ref(32, N, d))
    assert rho == (2 * 31 * (d + 2) + 2 + 2 * N + d) * U1
    m_b = (2 * (31 * (d + 2) + 1) + N) * U1  # M_b with w_u <= 2u', m_u <= u'
    for i in range(3):
        b_star, q_star = _exact(T, E, pi, tok[i])
        assert _mag(b[i, 31], b_star) <= m_b
        assert _mag(q[i], q_star) <= rho


def test_skipping_zero_transition_entries_is_bitwise_neutral():
    T, E, pi = _hmm(9, 4, "ring", 5)
    tok = np.random.default_rng(15).integers(0, 4, size=(2, 32))
    b0, q0 = _c0(T, E, pi, tok)
    b1, q1 = _c0(T, E, pi, tok, include_zeros=True)
    assert np.array_equal(b0, b1) and np.array_equal(q0, q1)
    assert np.array_equal(np.asarray(c1_cert.reference_oracle(T, E, pi, tok)["q_ref"]), q0)


def test_rho_bar_ref_constants():
    assert Fraction(c1_cert.rho_bar_ref(32, 144, 5)) == 729 * U1
    assert Fraction(c1_cert.rho_bar_ref(32, 144, 144)) == 9486 * U1
    assert Fraction(c1_cert.U) == U and Fraction(c1_cert.U1) == U1


# --- Theorem 1' and P4 (item 2) ---


def test_measured_discrepancy_contains_the_exact_error():
    T, E, pi = _hmm(6, 4, "ring", 21)
    tok = np.random.default_rng(22).integers(0, 4, size=(4, 32))
    q_ref = _c0(T, E, pi, tok)[1]
    q_hat = q_ref * (1.0 + np.random.default_rng(23).uniform(-1e-9, 1e-9, size=q_ref.shape))
    r = c1_cert.discrepancy(q_hat, q_ref)
    rho_bar = Fraction(c1_cert.rho_bar_ref(32, 6, 3))
    for i in range(4):
        exact_r = max(abs(Fraction(a) - Fraction(b)) / Fraction(b)
                      for a, b in zip(q_hat[i], q_ref[i]))
        assert Fraction(r[i]) == exact_r
        rho_h = Fraction(c1_cert.rho_main(r[i], rho_bar))
        assert rho_h == rho_bar + exact_r / (1 - exact_r)
        assert _mag(q_hat[i], _exact(T, E, pi, tok[i])[1]) <= rho_h


def test_p4_boundary_and_a_discrepancy_above_one_half():
    T, E, pi = _hmm(5, 3, "ring", 24)
    tok = np.random.default_rng(25).integers(0, 3, size=(1, 32))
    q_ref = _c0(T, E, pi, tok)[1]
    q_bad = q_ref.copy()
    q_bad[0, 1] *= 1.6
    r = c1_cert.discrepancy(q_bad, q_ref)
    assert Fraction(r[0]) > Fraction(1, 2)
    rho_bar = Fraction(c1_cert.rho_bar_ref(32, 5, 3))
    assert Fraction(c1_cert.rho_main(Fraction(1, 2), rho_bar)) == rho_bar + 1
    try:
        value = c1_cert.rho_main(r[0], rho_bar)
    except Exception as exc:  # P4 enforced here: it must be FAIL_TECHNICAL/ORACLE
        status, reason = c1_records.classify_exception(exc)
        assert str(status).startswith("FAIL_TECHNICAL") and "ORACLE" in f"{status} {reason}"
    else:  # P4 then lives in the caller; the value is still the Theorem 1' formula
        assert Fraction(value) == rho_bar + Fraction(r[0]) / (1 - Fraction(r[0]))


# --- route F (item 3) ----------------------------------------------------------------------------


def _route_f_hmm():
    E = np.array([[1e-300, 0.4, 0.6], [0.3, 1e-300, 0.7], [0.5, 0.25, 0.25], [0.2, 0.3, 0.5]])
    return _ring(4), E, np.full(4, 0.25)


def _my_route_f_r(T, E, pi, h, q_hat) -> Fraction:
    N, V = E.shape
    with decimal.localcontext(error_bound.trapping_context(60)):
        b = independent_reference.decimal_suffix_posterior(T, E, pi, h, 60)
        TE = [[sum((Decimal(float(T[z, zp])) * Decimal(float(E[zp, v])) for zp in range(N)),
                   Decimal(0)) for v in range(V)] for z in range(N)]
        q = [sum((b[z] * TE[z][v] for z in range(N)), Decimal(0)) for v in range(V)]
    return max(abs(Fraction(float(a)) - Fraction(c)) / Fraction(c) for a, c in zip(q_hat, q))


def _frac(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def test_route_f_is_taken_when_p1_fails_and_bounds_the_exact_error():
    T, E, pi = _route_f_hmm()
    h = np.random.default_rng(41).integers(0, 3, size=32)
    q_hat = BayesFilter(T, E, pi).run(h[None, :]).q[0, 32]
    ref = c1_cert.reference_oracle(T, E, pi, h[None, :])
    nu0 = TWO_M1000 / (Fraction(0.25) * Fraction(1e-300))  # about 0.37: P1 must fail
    assert not bool(np.asarray(c1_cert.p1(ref["nu_min"], ref["finite"], nu0))[0])
    out = c1_cert.route_f(T, E, pi, h, q_hat)
    beta = error_bound.posterior_envelope(32, 4)
    beta_q = (1 + beta) * (1 + error_bound.gamma_digits(2 * 4 + 2, 60)) - 1
    r, x = _frac(out["r"]), _frac(out["x"])
    assert abs(r - _my_route_f_r(T, E, pi, h, q_hat)) <= Fraction(1, 10**45)
    assert x == (1 + r) * (1 + beta_q) - 1
    assert bool(out["ok"]) and x <= Fraction(1, 2)
    rho_f = _frac(out["rho_F"])
    assert x / (1 - x) <= rho_f <= x / (1 - x) * (1 + Fraction(1, 2**50))
    assert _mag(q_hat, _exact(T, E, pi, h)[1]) <= rho_f


def test_route_f_rejects_x_above_one_half():
    T, E, pi = _route_f_hmm()
    h = np.random.default_rng(42).integers(0, 3, size=32)
    q_hat = BayesFilter(T, E, pi).run(h[None, :]).q[0, 32].copy()
    q_hat[1] *= 1.6
    out = c1_cert.route_f(T, E, pi, h, q_hat)
    assert _frac(out["x"]) > Fraction(1, 2) and not bool(out["ok"])
    if "status" in out:
        assert out["status"] == "FAIL_TECHNICAL/ORACLE"


def test_p1_is_an_exact_rational_threshold():
    nu0 = Fraction(1, 2**988)  # tau+ = 2**-2, eps_E = 2**-10 make nu0 a float exactly
    nu_min = np.array([2.0**-988, np.nextafter(2.0**-988, 0.0), 0.5, np.nan])
    finite = np.array([True, True, True, False])
    assert np.asarray(c1_cert.p1(nu_min, finite, nu0)).tolist() == [True, False, True, False]


# --- M-ln (item 6) ---


def _mln(q, ell):
    out = []
    with decimal.localcontext(error_bound.trapping_context(40)):
        for qi, li in zip(q, ell):
            worst = Fraction(0)
            for a, b in zip(qi, li):
                lg = Fraction(Decimal(float(a)).ln())
                worst = max(worst, abs(Fraction(float(b)) - lg) + abs(lg) / 10**38)
            out.append(worst)
    return out


def test_measured_log_error_matches_forty_digit_ln_and_grows_with_injected_error():
    T, E, pi = _hmm(6, 5, "ring", 51)
    tok = np.random.default_rng(52).integers(0, 5, size=(6, 32))
    q = BayesFilter(T, E, pi).run(tok).q[:, 32]
    q = np.hstack([q[:3], q[3:]])  # [R, 2V]: both arms of a row
    ell = np.log(q)
    ell_bad = ell.copy()
    ell_bad[0, 3] += 1e-7
    for lv in (ell, ell_bad):
        got = c1_cert.measured_log_error(q, lv)
        for g, worst in zip(got, _mln(q, lv)):
            assert worst <= Fraction(g) <= Fraction(math.nextafter(_up(worst), math.inf))
    assert Fraction(c1_cert.measured_log_error(q, ell_bad)[0]) >= Fraction(99, 10**9)


def test_decimal_trap_in_m_ln_is_fail_technical_numerical():
    q = np.array([[0.25, -0.5]])
    with pytest.raises(Exception) as info:
        c1_cert.measured_log_error(q, np.array([[np.log(0.25), 0.0]]))
    status, reason = c1_records.classify_exception(info.value)
    assert str(status).startswith("FAIL_TECHNICAL") and "NUMERICAL" in f"{status} {reason}"


# --- P0 and the A1 self-test (item 12) ---


def _cylinder():
    T = np.zeros((144, 144))
    for x in range(12):
        for y in range(12):
            s = 12 * x + y
            nbrs = [12 * ((x + 1) % 12) + y, 12 * ((x - 1) % 12) + y]
            nbrs += [s - 1] if y > 0 else []
            nbrs += [s + 1] if y < 11 else []
            for t in nbrs:
                T[s, t] = 0.2
            T[s, s] = 1.0 - 0.2 * len(nbrs)
    E = np.random.default_rng(61).random((144, 36)) + 0.05
    return T, E / E.sum(axis=1, keepdims=True), np.full(144, 1.0 / 144)


def test_p0_constants_in_exact_rationals():
    T, E, pi = _cylinder()
    res = c1_cert.p0(T, [E, E.copy(), E.copy()], pi)
    assert res["ok"] and res["identical"]
    eps_e, tau = Fraction(float(E.min())), Fraction(float(T[T > 0].min()))
    row_e = [sum((Fraction(float(v)) for v in E[z]), Fraction(0)) for z in range(144)]
    r = [sum((Fraction(float(T[z, zp])) * row_e[zp] for zp in np.nonzero(T[z])[0]),
             Fraction(0)) for z in range(144)]
    assert _frac(res["eps_E"]) == eps_e and _frac(res["tau_plus"]) == tau
    assert _frac(res["pi_min"]) == Fraction(float(pi.min()))
    assert int(res["d"]) == 5 and int(res["N"]) == 144 and int(res["V"]) == 36
    assert _frac(res["nu0"]) == TWO_M1000 / (tau * eps_e)
    assert _frac(res["omega_TE"]) == max(r) - min(r)


def _edit(arr, index, value):
    out = arr.copy()
    out[index] = value
    return out


@pytest.mark.parametrize("case", ["not_identical", "E_zero", "T_zero_diag", "pi_zero",
                                  "T_negative", "E_below_floor", "E_tiny_ok"])
def test_p0_failures(case):
    T, E, pi = _cylinder()
    Es = [E, E.copy(), E.copy()]
    if case == "not_identical":
        Es[1] = _edit(E, (7, 3), np.nextafter(E[7, 3], 1.0))
    elif case == "E_zero":
        Es = [_edit(E, (3, 7), 0.0)] * 3
    elif case == "T_zero_diag":
        T = _edit(T, (0, 0), 0.0)
    elif case == "pi_zero":
        pi = _edit(pi, 5, 0.0)
    elif case == "T_negative":
        T = _edit(T, (0, 50), -1e-3)
    elif case in ("E_below_floor", "E_tiny_ok"):  # pi_min * eps_E >= 2**-1000 is the floor
        Es = [_edit(E, (5, 2), 1e-300 if case == "E_below_floor" else 1e-290)] * 3
    res = c1_cert.p0(T, Es, pi)
    assert bool(res["ok"]) is (case == "E_tiny_ok")
    if case == "not_identical":
        assert not res["identical"]


def test_a1_selftest_holds_on_this_platform():
    res = c1_cert.a1_selftest()
    assert bool(res["ok"])
