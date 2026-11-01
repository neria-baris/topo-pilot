"""Author A (job 0198): Lemmas P1, P2, P3 and J (protocol §2.2; §5.1 KS-P), by exact enumeration
of the natural suffix-matched pair law on the CONTRACT_OF KS-PAIR chain (L = 8, suffix 4,
test-side Fractions), and the HWSU pair functions on planted arrays (API §3)."""

from __future__ import annotations  # noqa: I001

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import hwsu_oracle as uo  # noqa: E402
import c1_oracle  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

L, S = 8, 4
P = L - S
c = uc.CONTRACT["dry_run"]["ks_pair_chain"]
TF = [[Fraction(x) for x in r] for r in c["T"]]
EF = [[Fraction(x) for x in r] for r in c["E"]]
PF = [Fraction(x) for x in c["pi"]]
NS, V = len(PF), len(EF[0])


def joint(length):
    out = {}
    for w in itertools.product(range(V), repeat=length):
        a = [PF[z] * EF[z][w[0]] for z in range(NS)]
        for t in range(1, length):
            a = [sum(a[y] * TF[y][z] for y in range(NS)) * EF[z][w[t]] for z in range(NS)]
        out[w] = sum(a)
    return out


J8, J9 = joint(L), joint(L + 1)
SUF = list(itertools.product(range(V), repeat=S))
PRE = list(itertools.product(range(V), repeat=P))
PS = {s: sum(J8[p + s] for p in PRE) for s in SUF}
COND = {s: {p: J8[p + s] / PS[s] for p in PRE} for s in SUF}
# q8(h) = P(w9 | w1..w8); q4(s) = P(w9 | w5..w8): exact predictive laws (they sum to 1)
Q8 = {p + s: [J9[p + s + (v,)] / J8[p + s] for v in range(V)] for s in SUF for p in PRE}
Q4 = {s: [sum(J9[p + s + (v,)] for p in PRE) / PS[s] for v in range(V)] for s in SUF}


def lg(x):
    """A fixed rational stand-in for log x: every identity below is algebraic in these values
    (it uses only the pair law and the tower property), so it holds exactly in Fractions."""
    return Fraction(math.log(float(x)))


LQ8 = {h: [lg(x) for x in q] for h, q in Q8.items()}
LQ4 = {s: [lg(x) for x in q] for s, q in Q4.items()}


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def pair_mean(f):
    """E over the natural pair law: P(s) P(p1 | s) P(p2 | s) (Lemma P0)."""
    tot = Fraction(0)
    for s in SUF:
        for p1, p2 in itertools.product(PRE, PRE):
            tot += PS[s] * COND[s][p1] * COND[s][p2] * f(p1 + s, p2 + s, s)
    return tot


def row_mean(f):
    return sum((J8[p + s] * f(p + s, s) for s in SUF for p in PRE), Fraction(0))


def test_predictives_and_tower_property():
    for s in SUF:
        assert sum(Q4[s]) == 1
        for v in range(V):  # E[q8 | S4] = q4, exactly
            assert sum(COND[s][p] * Q8[p + s][v] for p in PRE) == Q4[s][v]
    assert all(sum(q) == 1 for q in Q8.values())


def test_lemma_p2_pair_covariance_identity():
    """½E[(a¹−a²)ᵀ(b¹−b²)] = E[(a − E[a|S4])ᵀ(b − E[b|S4])], a = log q̄8, b = q̄8."""
    lhs = pair_mean(lambda h1, h2, s: dot(sub(LQ8[h1], LQ8[h2]), sub(Q8[h1], Q8[h2])) / 2)
    ea = {s: [sum(COND[s][p] * LQ8[p + s][v] for p in PRE) for v in range(V)] for s in SUF}
    rhs = row_mean(lambda h, s: dot(sub(LQ8[h], ea[s]), sub(Q8[h], Q4[s])))
    assert lhs == rhs
    # so E[A_full] (z = log q̄, d = Δq̄) equals the single-row E[zᵀρ4], ρ4 = q̄8 − q̄4
    assert lhs == row_mean(lambda h, s: dot(LQ8[h], sub(Q8[h], Q4[s])))
    assert lhs > 0


def test_lemma_j_oracle_response_is_jeffreys():
    eg = pair_mean(lambda h1, h2, s: dot(sub(Q8[h1], Q8[h2]), sub(LQ8[h1], LQ8[h2])) / 2)
    kl_fwd = row_mean(lambda h, s: dot(Q8[h], sub(LQ8[h], LQ4[s])))
    kl_rev = row_mean(lambda h, s: dot(Q4[s], sub(LQ4[s], LQ8[h])))
    assert eg == kl_fwd + kl_rev
    assert kl_rev > 0 and eg > kl_fwd > 0


def test_lemma_p1_suffix_only_predictor_reads_nothing():
    """A predictor whose logits depend on the suffix only has A ≡ 0 on every pair."""
    for s in SUF:
        for p1, p2 in itertools.product(PRE, PRE):
            d = sub(Q8[p1 + s], Q8[p2 + s])
            assert dot(d, sub(LQ4[s], LQ4[s])) / 2 == 0
            assert sum(d) == 0  # d = ρ4¹ − ρ4² sums to zero
            assert d == sub(sub(Q8[p1 + s], Q4[s]), sub(Q8[p2 + s], Q4[s]))


def test_lemma_p3_code_interchange_moves_only_the_beyond_four_part():
    rng = np.random.Generator(np.random.PCG64(30))
    h = {s: [Fraction(int(x), 7) for x in rng.integers(-50, 50, 3)] for s in SUF}
    cb = {p + s: [Fraction(int(x), 11) for x in rng.integers(-50, 50, 3)] for s in SUF
          for p in PRE}
    for s in SUF:
        for p1, p2 in itertools.product(PRE, PRE):
            c1 = [a + b for a, b in zip(h[s], cb[p1 + s])]
            c2 = [a + b for a, b in zip(h[s], cb[p2 + s])]
            assert sub(c1, c2) == sub(cb[p1 + s], cb[p2 + s])


# ---- HWSU pair functions on planted arrays ---------------------------------------------------
def _simplex(rng, n, v=36):
    x = rng.gamma(0.7, size=(n, v)) + 1e-6
    return x / x.sum(axis=1, keepdims=True)


def _helmert(n=36):
    out = np.zeros((n, n - 1))
    for k in range(1, n):
        out[:k, k - 1] = 1.0 / math.sqrt(k * (k + 1.0))
        out[k, k - 1] = -k / math.sqrt(k * (k + 1.0))
    return out


@pytest.fixture(scope="module")
def planted():
    rng = np.random.Generator(np.random.PCG64(31))
    n = 300
    q1, q2, q4 = _simplex(rng, n), _simplex(rng, n), _simplex(rng, n)
    m1, m2, m4 = (rng.normal(size=(n, 2)) * 0.5 for _ in range(3))
    m1[7] = 0.0  # an invalid oracle phase (|m32| = 0 → φ* = 0, u° = (1, 0); D-9)
    o1 = {"qbar": q1, "logq": np.log(q1), "m32": m1}
    o2 = {"qbar": q2, "logq": np.log(q2), "m32": m2}
    s1 = {"q4bar": q4, "logq4": np.log(q4), "m4": m4}
    return o1, o2, s1


def test_pair_core_equals_c1_oracle_G_hat(planted):
    o1, o2, _ = planted
    pc = uo.pair_core(o1, o2)
    G, d = c1_oracle.G_hat(o1["qbar"], o2["qbar"])[:2]
    assert np.array_equal(pc["G"], G) and np.array_equal(pc["d"], d)
    assert pc["d"].shape == (300, 36) and np.all(pc["G"] >= 0)
    want = 0.5 * np.sum((o1["qbar"] - o2["qbar"]) * (o1["logq"] - o2["logq"]), axis=1)
    assert np.allclose(pc["G"], want, rtol=1e-12, atol=1e-15)


def test_readout_A_formula_and_suffix_only_zero(planted):
    o1, o2, s1 = planted
    N = _helmert(36)
    d = o1["qbar"] - o2["qbar"]
    z1, z2 = o1["logq"], o2["logq"]
    got = uo.readout_A(d, z1, z2, N)
    want = 0.5 * np.sum(d * (((z1 - z2) @ N) @ N.T), axis=1)
    assert np.allclose(got, want, rtol=1e-12, atol=1e-15)
    G = 0.5 * np.sum(d * (z1 - z2), axis=1)  # Lemma D2: N Nᵀ projects off 1 and Σd = 0
    assert np.all(np.abs(got - G) <= 1e-12 * np.maximum(1.0, np.abs(G)))
    zero = uo.readout_A(d, s1["logq4"], s1["logq4"].copy(), N)
    assert np.array_equal(zero, np.zeros(len(d)))


def test_lemma_p_arrays_match_the_formulas(planted):
    o1, o2, s1 = planted
    pc = {"G": c1_oracle.G_hat(o1["qbar"], o2["qbar"])[0]}
    a = uo.lemma_p_arrays(o1, o2, s1, pc)

    def unit(m):
        ok = np.hypot(m[:, 0], m[:, 1]) > 1e-12
        ph = np.where(ok, np.arctan2(m[:, 1], m[:, 0]), 0.0)
        return np.column_stack((np.cos(ph), np.sin(ph)))

    u1, u2 = unit(o1["m32"]), unit(o2["m32"])
    want = {
        "pairU": 0.5 * np.sum((u1 - u2) * (o1["m32"] - o2["m32"]), axis=1),
        "rowU": np.sum(u1 * (o1["m32"] - s1["m4"]), axis=1),
        "pairG": pc["G"],
        "rowG": np.sum((o1["qbar"] - s1["q4bar"]) * o1["logq"], axis=1),
    }
    assert set(want) <= set(a)
    for k, w in want.items():
        assert np.asarray(a[k]).dtype == np.float64 and np.asarray(a[k]).shape == (300,)
        assert np.allclose(a[k], w, rtol=1e-12, atol=1e-15), k
    assert np.array_equal(a["pairG"], pc["G"])
    assert a["rowU"][7] == pytest.approx(o1["m32"][7, 0] - s1["m4"][7, 0], abs=1e-15)


def test_label_share_formula(planted):
    o1, o2, _ = planted
    q1, q2 = o1["qbar"], o2["qbar"]
    got = uo.label_share(q1, q2)
    n = len(q1)
    m1, m2 = np.zeros((n, 6)), np.zeros((n, 6))
    for v in range(36):  # canonical v = 6a + b, a = the circular label
        m1[:, v // 6] += q1[:, v]
        m2[:, v // 6] += q2[:, v]
    want = 0.5 * np.sum((m1 - m2) * (np.log(m1) - np.log(m2)), axis=1)
    assert np.allclose(got, want, rtol=1e-12, atol=1e-15)
    assert np.all(got <= c1_oracle.G_hat(q1, q2)[0] + 1e-12)  # data processing inequality


def test_label_share_zero_when_circular_marginals_agree():
    rng = np.random.Generator(np.random.PCG64(32))
    n = 50
    w = rng.integers(1, 40, size=(n, 36)).astype(np.float64)
    w[:, -1] += 1024 - w.sum(axis=1)
    assert np.all(w[:, -1] > 0)
    q1 = w / 1024.0  # dyadic: every partial sum is exact
    q2 = q1.copy()
    for a in range(6):  # permute the axial label within each circular label
        blk = q2[:, 6 * a:6 * a + 6]
        q2[:, 6 * a:6 * a + 6] = blk[:, rng.permutation(6)]
    assert not np.array_equal(q1, q2)
    assert np.array_equal(uo.label_share(q1, q2), np.zeros(n))
