"""Independent tests (author B, job 0026), TEST_PLAN B-4 items 4, 9 and 14 (row bounds).

Protocol §15.3.8-§15.3.10 (Theorems 2-4), §15.3.5 L5 and its expression-count table, §15.3.1
coverage; CERTIFICATE.md §7; API.md §7. Written from the protocol and the four contract documents
only; no tools/c1prime source was read and nothing was executed by the author.

Theorem checks: q-hat from the unchanged operational `BayesFilter`, the exact literal-weight
target from a Fraction forward filter, logarithms and log-softmax at 60 Decimal digits, and
|computed - exact| <= OUT(evaluated bound) in exact rationals. API.md says the bound functions
use only binary + and *, so every per-symbol leaf is passed as an absolute value (|d|, |lambda|,
|Delta|); that is correct under either reading of whether the function applies abs itself.
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
from topo_pilot.oracle import BayesFilter

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_bounds  # noqa: E402
import c1_endpoint  # noqa: E402
import c1_oracle  # noqa: E402
import error_bound  # noqa: E402

pytestmark = pytest.mark.analysis

U = Fraction(1, 2**53)
U1 = U / (1 - U)
ZETA = Fraction(1, 2**800)


def _up(c: Fraction) -> float:
    f = float(c)
    return math.nextafter(f, math.inf) if Fraction(f) < c else f


def _out(x) -> Fraction:
    return (1 + Fraction(1, 2**30)) * Fraction(float(x)) + ZETA


def _ring(N):
    T = np.zeros((N, N))
    for i in range(N):
        T[i, i], T[i, (i + 1) % N], T[i, (i - 1) % N] = 0.5, 0.25, 0.25
    return T


def _q_ref(T, E, pi, tok):
    """C0 (§15.3.2) in Python floats; returns q^ref [R, V] and min posterior per row."""
    N, V = E.shape
    q, nu = np.empty((tok.shape[0], V)), []
    for i, row in enumerate(tok):
        b = [float(pi[s]) * float(E[s, row[0]]) for s in range(N)]
        lo = 1.0
        for t in range(32):
            if t:
                b = [sum_ordered([b[zp] * float(T[zp, z]) for zp in range(N) if T[zp, z] > 0])
                     * float(E[z, row[t]]) for z in range(N)]
            D = sum_ordered(b)
            b = [x / D for x in b]
            lo = min(lo, min(b))
        TE = [[sum_ordered([float(T[z, zp]) * float(E[zp, v]) for zp in range(N) if T[z, zp] > 0])
               for v in range(V)] for z in range(N)]
        q[i] = [sum_ordered([b[z] * TE[z][v] for z in range(N)]) for v in range(V)]
        nu.append(lo)
    return q, nu


def sum_ordered(xs):
    acc = xs[0]
    for x in xs[1:]:
        acc = acc + x
    return acc


def _exact_q(T, E, pi, row):
    N, V = E.shape
    Tf = [[Fraction(float(x)) for x in r] for r in T]
    Ef = [[Fraction(float(x)) for x in r] for r in E]
    alpha = [Fraction(float(pi[s])) * Ef[s][int(row[0])] for s in range(N)]
    for w in row[1:]:
        alpha = [sum((alpha[zp] * Tf[zp][z] for zp in range(N) if Tf[zp][z]), Fraction(0))
                 * Ef[z][int(w)] for z in range(N)]
    tot = sum(alpha, Fraction(0))
    b = [a / tot for a in alpha]
    return [sum((b[z] * Tf[z][zp] * Ef[zp][v] for z in range(N) for zp in range(N)),
                Fraction(0)) for v in range(V)]


def _rho(q_hat, q_ref, N, d):
    """up(rho_bar_ref + r_h/(1 - r_h)) per row (Theorem 1')."""
    out = []
    for a, b in zip(q_hat, q_ref):
        r = max(abs(Fraction(float(x)) - Fraction(float(y))) / Fraction(float(y))
                for x, y in zip(a, b))
        out.append(_up((2 * 31 * (d + 2) + 2 + 2 * N + d) * U1 + r / (1 - r)))
    return np.array(out)


def _e_l(qp, qm, lp, lm):
    out = []
    with decimal.localcontext(error_bound.trapping_context(40)):
        for row in zip(qp, qm, lp, lm):
            worst = Fraction(0)
            for q, ell in ((row[0], row[2]), (row[1], row[3])):
                for a, b in zip(q, ell):
                    lg = Fraction(Decimal(float(a)).ln())
                    worst = max(worst, abs(Fraction(float(b)) - lg) + abs(lg) / 10**38)
            out.append(_up(worst))
    return np.array(out)


def _cols(x):
    return [np.ascontiguousarray(x[:, v]) for v in range(x.shape[1])]


def _ldec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


# --- Theorem 2 (b^G) with q entries near 1e-250 ---


def test_theorem2_b_G_contains_the_exact_G_and_does_not_blow_up():
    N, V = 6, 5
    rng = np.random.default_rng(51)
    T, pi = _ring(N), np.full(N, 1.0 / N)
    E = rng.random((N, V)) + 0.2
    E[:, 4] = 1e-250 * (1.0 + 4.0 * rng.random(N))
    E = E / E.sum(axis=1, keepdims=True)
    tp, tm = rng.integers(0, 4, size=(3, 32)), rng.integers(0, 4, size=(3, 32))
    qp, qm = BayesFilter(T, E, pi).run(tp).q[:, 32], BayesFilter(T, E, pi).run(tm).q[:, 32]
    (rp_ref, nu_p), (rm_ref, nu_m) = _q_ref(T, E, pi, tp), _q_ref(T, E, pi, tm)
    nu0 = Fraction(1, 2**1000) / (Fraction(0.25) * Fraction(float(E.min())))
    assert min(nu_p + nu_m) >= nu0  # P1 holds: the main route applies
    G, d, lam, lp, lm = c1_oracle.G_hat(qp, qm)
    assert np.array_equal(np.asarray(lp), np.log(qp)) and np.array_equal(np.asarray(d), qp - qm)
    rho_p, rho_m = _rho(qp, rp_ref, N, 3), _rho(qm, rm_ref, N, 3)
    e_l = _e_l(qp, qm, np.log(qp), np.log(qm))
    consts = c1_bounds.bound_constants()
    bG = np.asarray(c1_bounds.b_G(_cols(np.abs(d)), _cols(np.abs(lam)), _cols(qp), _cols(qm),
                                  rho_p, rho_m, e_l, consts), dtype=np.float64)
    assert bG.shape == (3,) and np.all(bG < 1e-10)
    with localcontext() as ctx:
        ctx.prec = 60
        for i in range(3):
            sp, sm = _exact_q(T, E, pi, tp[i]), _exact_q(T, E, pi, tm[i])
            g_star = sum(((_ldec(a) - _ldec(b)) * (_ldec(a).ln() - _ldec(b).ln())
                          for a, b in zip(sp, sm)), Decimal(0)) / 2
            err = abs(Fraction(float(np.asarray(G)[i])) - Fraction(g_star))
            assert err + Fraction(1, 10**50) <= _out(bG[i])
            assert float(sp[4]) < 1e-240  # the tiny symbol really is tiny


# --- Theorem 3 (b^A): the omega_TE term is required and sufficient ---


def test_theorem3_b_A_needs_and_is_saved_by_the_omega_term():
    N, V = 6, 4
    rng = np.random.default_rng(61)
    T, pi = _ring(N), np.full(N, 1.0 / N)
    E = rng.random((N, V)) + 0.2
    E = E / E.sum(axis=1, keepdims=True) * (1.0 + 1e-6 * rng.uniform(-1, 1, (N, 1)))
    tp, tm = rng.integers(0, V, size=(3, 32)), rng.integers(0, V, size=(3, 32))
    qp, qm = _q_ref(T, E, pi, tp)[0], _q_ref(T, E, pi, tm)[0]  # C0 output; r_h = 0
    zm = rng.normal(size=(3, V))
    zp = zm + 1.0 + 0.3 * rng.normal(size=(3, V))
    dh, Dl = qp - qm, zp - zm
    A = np.asarray(c1_endpoint.A_hat(dh, zp, zm), dtype=np.float64)
    rho = np.full(3, _up((2 * 31 * 5 + 2 + 2 * N + 3) * U1))
    row_e = [sum((Fraction(float(x)) for x in E[z]), Fraction(0)) for z in range(N)]
    r = [sum((Fraction(float(T[z, zp])) * row_e[zp] for zp in range(N)), Fraction(0))
         for z in range(N)]
    omega = _up(max(r) - min(r))
    consts = c1_bounds.bound_constants()
    args = (_cols(np.abs(dh)), _cols(np.abs(Dl)), _cols(qp), _cols(qm), rho, rho,
            np.max(np.abs(Dl), axis=1))
    with_omega = np.asarray(c1_bounds.b_A(*args, omega, consts), dtype=np.float64)
    without = np.asarray(c1_bounds.b_A(*args, 0.0, consts), dtype=np.float64)
    violated = []
    with localcontext() as ctx:
        ctx.prec = 60
        for i in range(3):
            sp, sm = _exact_q(T, E, pi, tp[i]), _exact_q(T, E, pi, tm[i])
            lse_p = sum((Decimal(float(z)).exp() for z in zp[i]), Decimal(0)).ln()
            lse_m = sum((Decimal(float(z)).exp() for z in zm[i]), Decimal(0)).ln()
            a_star = sum(((_ldec(a) - _ldec(b)) * ((Decimal(float(x)) - lse_p)
                                                   - (Decimal(float(y)) - lse_m))
                          for a, b, x, y in zip(sp, sm, zp[i], zm[i])), Decimal(0)) / 2
            err = abs(Fraction(float(A[i])) - Fraction(a_star))
            assert err + Fraction(1, 10**50) <= _out(with_omega[i])
            violated.append(err > _out(without[i]))
    assert any(violated)


# --- displayed shapes, zeta, coverage (items 9, 14) ---


def _exact_consts():
    g = lambda n: n * U / (1 - n * U)  # noqa: E731
    return {"half": Fraction(1, 2), "u1": U1, "gamma_V": g(36), "gamma31_32": g(31) / 32,
            "inv_1mu": 1 / (1 - U), "c1_term": U1 * Fraction(0.1) + Fraction(1, 5 * 2**55),
            "c3_term": U1 * Fraction(0.3) + Fraction(1, 5 * 2**54), "tenth": Fraction(1, 10),
            "three_tenths": Fraction(3, 10), "thirty_second": Fraction(1, 32), "zeta": ZETA,
            "two": Fraction(2)}


def _my_bA(d, Dl, qp, qm, rp, rm, mx, om, c):
    rbp, rbm = rp + rp * rp, rm + rm * rm
    s1 = s2 = None
    for v in range(len(d)):
        t1 = d[v] * Dl[v]
        t2 = (c["u1"] * d[v] + rbp * qp[v] + rbm * qm[v]) * Dl[v]
        s1, s2 = (t1, t2) if s1 is None else (s1 + t1, s2 + t2)
    return c["half"] * ((c["gamma_V"] + c["u1"]) * s1 + c["inv_1mu"] * (s2 + om * mx)) + c["zeta"]


def test_bound_values_follow_the_displayed_shapes_and_include_zeta():
    consts = c1_bounds.bound_constants()
    c = {k: _up(v) for k, v in _exact_consts().items()}
    for key, value in c.items():
        assert float(consts[key]) == value
    rng = np.random.default_rng(71)
    cols = [[np.abs(rng.normal(size=4)) * s for _ in range(36)] for s in (1e-2, 3.0, 0.03, 0.03)]
    rp, rm, mx = np.full(4, 1e-13), np.full(4, 2e-13), np.full(4, 5.0)
    bA = np.asarray(c1_bounds.b_A(*cols, rp, rm, mx, 1e-16, consts))
    np.testing.assert_allclose(bA, _my_bA(*cols, rp, rm, mx, 1e-16, c), rtol=1e-13)
    bAs = [np.asarray(c1_bounds.b_A(*cols, rp, rm, mx, 1e-16, consts)) for _ in range(32)]
    Ac = [np.abs(rng.normal(size=4)) for _ in range(32)]
    Y = np.abs(rng.normal(size=4))
    bY = np.asarray(c1_bounds.b_Y(Y, bA, bAs, Ac, consts))
    mine = c["u1"] * Y + bA + c["thirty_second"] * sum_ordered(bAs)
    mine = mine + c["gamma31_32"] * sum_ordered(Ac) + c["zeta"]
    np.testing.assert_allclose(bY, mine, rtol=1e-13)
    z4 = np.zeros(4)
    zero_cols = [[z4] * 36] * 4
    assert np.all(np.asarray(c1_bounds.b_A(*zero_cols, z4, z4, z4, 0.0, consts)) == 2.0**-800)
    assert np.all(np.asarray(c1_bounds.b_G(*zero_cols, z4, z4, z4, consts)) == 2.0**-800)
    assert np.all(np.asarray(c1_bounds.b_Y(z4, z4, [z4] * 32, [z4] * 32, consts)) == 2.0**-800)
    assert np.all(np.asarray(c1_bounds.b_Z(z4, z4, z4, z4, consts)) == 2.0**-800)
    assert np.all(np.asarray(c1_bounds.b_Zf(z4, z4, z4, z4, consts)) == 2.0**-800)
    G, bG = np.abs(rng.normal(size=4)) * 0.1, np.full(4, 3e-13)
    bZ = np.asarray(c1_bounds.b_Z(Y, bY, G, bG, consts))
    mine_z = c["u1"] * Y + bY + c["c1_term"] * G + c["tenth"] * bG + c["zeta"]
    np.testing.assert_allclose(bZ, mine_z, rtol=1e-13)
    bZf = np.asarray(c1_bounds.b_Zf(Y, bA, G, bG, consts))
    mine_zf = c["u1"] * Y + bA + c["c3_term"] * G + c["three_tenths"] * bG + c["zeta"]
    np.testing.assert_allclose(bZf, mine_zf, rtol=1e-13)


# --- L5 expression counts with c1_bounds.Sym (item 9) ---


def _leaves(k):
    return [c1_bounds.Sym.leaf() for _ in range(k)]


def _sym_bA(consts):
    S = c1_bounds.Sym
    return c1_bounds.b_A(_leaves(36), _leaves(36), _leaves(36), _leaves(36), S.leaf(), S.leaf(),
                         S.leaf(), 1e-16, consts)


def _sym_bG(consts):
    S = c1_bounds.Sym
    return c1_bounds.b_G(_leaves(36), _leaves(36), _leaves(36), _leaves(36), S.leaf(), S.leaf(),
                         S.leaf(), consts)


def _within(sym, nodes, monomials, degree):
    assert int(sym.nodes) <= nodes and int(sym.monomials) <= monomials
    assert int(sym.degree) <= degree
    assert int(sym.nodes) <= 2**17 and int(sym.monomials) <= 2**16 and int(sym.degree) <= 7


def test_expression_counts_do_not_exceed_the_section_15_3_5_table():
    consts, S = c1_bounds.bound_constants(), c1_bounds.Sym
    bG, bA = _sym_bG(consts), _sym_bA(consts)
    _within(bG, 1117, 1081, 6)
    _within(bA, 474, 254, 6)
    bY = c1_bounds.b_Y(S.leaf(), bA, [_sym_bA(consts) for _ in range(32)], _leaves(32), consts)
    _within(bY, 15711, 8416, 7)
    _within(c1_bounds.b_Z(S.leaf(), bY, S.leaf(), bG, consts), 16837, 9501, 7)
    _within(c1_bounds.b_Zf(S.leaf(), bA, S.leaf(), bG, consts), 1600, 1339, 7)
