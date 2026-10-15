"""Independent tests, author A (job 0026): the operational oracle wrapper, G (C3), named /
canonical joins, the cross-model G identity and the Decimal reference (TEST_PLAN A-3; protocol
sections 3.3, 3.4 and 15.3.2 C3).

Fixture: the tiny periodic 12 x 2 cylinder HMM of test_a_oracle.py (rebuilt here). Expected
values come from oracle.BayesFilter unchanged, from explicit left-to-right float64 loops that
follow the protocol's ordered-sum definition, and from exact Fraction filters.
"""

from __future__ import annotations

import decimal
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_oracle  # noqa: E402
from topo_pilot.oracle import BayesFilter  # noqa: E402

NX, NY, V = 12, 2, 36
COORDS = np.array([[x, y] for x in range(NX) for y in range(NY)], dtype=np.float64)
N = len(COORDS)
U = Fraction(1, 2**53)
PERMS = [np.random.default_rng(seed).permutation(V) for seed in (11, 12, 13)]


def state(x, y):
    return 2 * (x % NX) + y


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
    for x in range(NX):
        for y in range(NY):
            logit = np.empty(V)
            for j in range(V):
                a, b = divmod(j, 6)
                dx = abs(x - 2 * a) % NX
                dx = min(dx, NX - dx)
                logit[j] = -dx**2 / (2 * 1.25**2) - (y - 0.2 * b) ** 2 / 2.0
            row = np.exp(logit)
            E[state(x, y)] = row / row.sum()
    return E


T, E, PI = make_T(), make_E(), np.full(N, 1.0 / N)


def histories(rows, seed):
    return np.random.default_rng(seed).integers(0, V, size=(rows, 32)).astype(np.int64)


def ordered_half_dot(d, x):
    """0.5 * osum_v fl(d_v * x_v), left to right in column order (protocol C3/C4)."""
    acc = d[:, 0] * x[:, 0]
    for v in range(1, d.shape[1]):
        acc = acc + d[:, v] * x[:, v]
    return 0.5 * acc


def to_named(x, perm):
    out = np.empty_like(x)
    out[:, perm] = x  # x_named[perm[j]] = x_canon[j]
    return out


def gamma(n):
    return n * U / (1 - n * U)


def donor_predictives(rows=10, seed=4):
    canon = histories(rows, seed)
    H, Hp, Hm = (np.asarray(x).astype(np.int64) for x in c1_oracle.donors(canon))
    flt = BayesFilter(T, E, PI)
    return flt.run(Hp).q[:, 32], flt.run(Hm).q[:, 32]


def test_run_oracle_is_bayesfilter_with_the_section_3_3_indices():
    tokens = histories(5, 1)
    got = c1_oracle.run_oracle(T, E, PI, tokens)
    res = BayesFilter(T, E, PI).run(tokens)
    for key, want in (("b31", res.b[:, 30]), ("b32", res.b[:, 31]), ("q", res.q[:, 32]),
                      ("s", res.ce[:, 31]), ("log_evidence", res.log_evidence), ("b_all", res.b)):
        assert np.asarray(got[key]).tobytes() == np.asarray(want).tobytes(), key


def test_G_hat_is_the_ordered_C3_kernel():
    qp, qm = donor_predictives()
    G, d, lam, lp, lm = c1_oracle.G_hat(qp, qm)
    assert np.asarray(lp).tobytes() == np.log(qp).tobytes()
    assert np.asarray(lm).tobytes() == np.log(qm).tobytes()
    assert np.asarray(d).tobytes() == (qp - qm).tobytes()
    assert np.asarray(lam).tobytes() == (np.log(qp) - np.log(qm)).tobytes()
    assert np.asarray(G).tobytes() == ordered_half_dot(qp - qm, np.log(qp) - np.log(qm)).tobytes()
    assert np.all(np.asarray(G) >= 0.0)
    sym_kl = 0.5 * (np.sum(qp * np.log(qp / qm), 1) + np.sum(qm * np.log(qm / qp), 1))
    assert np.allclose(G, sym_kl, rtol=1e-10, atol=1e-18)


def test_G_named_uses_the_permuted_canonical_arrays():
    qp, qm = donor_predictives(seed=5)
    G, d, lam, _, _ = c1_oracle.G_hat(qp, qm)
    d, lam = np.asarray(d), np.asarray(lam)
    for perm in PERMS:
        got = np.asarray(c1_oracle.G_named(d, lam, perm))
        assert got.tobytes() == ordered_half_dot(to_named(d, perm), to_named(lam, perm)).tobytes()
        prods = np.abs(d * lam)
        for i in range(len(G)):
            bound = gamma(35) * sum(Fraction(float(p)) for p in prods[i])
            assert abs(Fraction(float(got[i])) - Fraction(float(G[i]))) <= bound
            assert abs(float(got[i]) - float(G[i])) <= 1e-12


def test_cross_model_G_identity_within_1e_12():
    qp, qm = donor_predictives(seed=6)
    _, d, lam, _, _ = c1_oracle.G_hat(qp, qm)
    values = [np.asarray(c1_oracle.G_named(np.asarray(d), np.asarray(lam), p)) for p in PERMS]
    for a in values:
        for b in values:
            assert np.max(np.abs(a - b)) <= 1e-12


def test_named_canonical_column_permutations_round_trip():
    x = np.random.default_rng(8).uniform(size=(3, V))
    for perm in PERMS:
        named = np.asarray(c1_oracle.named_from_canonical(x, perm))
        assert np.array_equal(named[:, perm], x)
        back = np.asarray(c1_oracle.canonical_from_named_cols(named, perm))
        assert np.array_equal(back, x)


def test_named_space_filter_agrees_with_canonical_within_4e_12():
    """Section 3.3: q_named[perm[j]] = q_canon[j], checked against direct named-space filtering
    with E_named = E_canon[:, argsort(perm)] on named tokens perm[canonical]."""
    canon = histories(6, 9)
    q_c = BayesFilter(T, E, PI).run(canon).q[:, 32]
    tol = Fraction(4, 10**12)
    for perm in PERMS:
        E_named = E[:, np.argsort(perm)]
        assert np.array_equal(E_named[:, perm], E)
        q_n = BayesFilter(T, E_named, PI).run(perm[canon]).q[:, 32]
        mapped = np.asarray(c1_oracle.named_from_canonical(q_c, perm))
        worst = max(abs(Fraction(float(a)) / Fraction(float(b)) - 1)
                    for a, b in zip(q_n.ravel(), mapped.ravel()))
        assert worst <= tol
        assert bool(c1_oracle.rel_agree(q_n.ravel(), mapped.ravel(), tol)) is True


def exact_forward(seq):
    """Unnormalised exact forward pass with the stored float weights read as rationals."""
    TF = [[Fraction(float(v)) for v in row] for row in T]
    EF = [[Fraction(float(v)) for v in row] for row in E]
    alpha = [Fraction(float(PI[i])) * EF[i][int(seq[0])] for i in range(N)]
    for w in seq[1:]:
        alpha = [sum((alpha[i] * TF[i][j] for i in range(N) if TF[i][j]), Fraction(0))
                 * EF[j][int(w)] for j in range(N)]
    total = sum(alpha, Fraction(0))
    return [a / total for a in alpha], TF, EF


def exact_predictive(b, TF, EF):
    te = [[sum((TF[z][y] * EF[y][v] for y in range(N) if TF[z][y]), Fraction(0))
           for v in range(V)] for z in range(N)]
    return [sum((b[z] * te[z][v] for z in range(N)), Fraction(0)) for v in range(V)]


def rel_gap(dec_list, exact_list):
    return max(abs(Fraction(x) - y) / y for x, y in zip(dec_list, exact_list))


def exact_ln(value, digits=90):
    with decimal.localcontext(decimal.Context(prec=digits)):
        return (Decimal(value.numerator) / Decimal(value.denominator)).ln()


def test_decimal_reference_against_exact_rationals():
    h = histories(1, 10)[0]
    ref = c1_oracle.decimal_reference(T, E, PI, h)
    b31, TF, EF = exact_forward(h[:31])
    b32, _, _ = exact_forward(h)
    q31, q32 = exact_predictive(b31, TF, EF), exact_predictive(b32, TF, EF)
    tol = Fraction(1, 10**50)
    assert all(isinstance(x, Decimal) for x in ref["b32"])
    assert rel_gap(ref["b31"], b31) <= tol and rel_gap(ref["b32"], b32) <= tol
    assert rel_gap(ref["q31"], q31) <= tol and rel_gap(ref["q32"], q32) <= tol
    s_exact = -exact_ln(q31[int(h[31])])
    assert abs(Fraction(ref["s"]) - Fraction(s_exact)) <= Fraction(1, 10**45)
    for got, want in zip(ref["ln_q32"], q32):
        assert abs(Fraction(got) - Fraction(exact_ln(want))) <= Fraction(1, 10**45)
    s_float = BayesFilter(T, E, PI).run(h[None, :]).ce[0, 31]
    assert abs(Fraction(float(s_float)) - Fraction(ref["s"])) <= Fraction(1, 10**10)


def test_decimal_predictive_is_b_T_E():
    b = [Fraction(k + 1, (N * (N + 1)) // 2) for k in range(N)]
    with decimal.localcontext(decimal.Context(prec=70)):
        b_dec = [Decimal(x.numerator) / Decimal(x.denominator) for x in b]
    got = c1_oracle.decimal_predictive(b_dec, T, E)
    _, TF, EF = exact_forward([0])
    want = exact_predictive([Fraction(x) for x in b_dec], TF, EF)
    assert len(got) == V
    assert rel_gap(got, want) <= Fraction(1, 10**55)


def test_decimal_posterior60_matches_the_exact_posterior():
    h = histories(1, 11)[0]
    got = c1_oracle.decimal_posterior60(T, E, PI, h)
    want, _, _ = exact_forward(h)
    assert rel_gap(got, want) <= Fraction(1, 10**50)
