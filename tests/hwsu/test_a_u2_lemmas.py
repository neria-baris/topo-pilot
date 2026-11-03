"""Author A (job 0223): Lemmas P1, P2 and J by exact enumeration in Fractions on the phase-1
non-reversible chain (protocol 2.2, 2.6; 5.1 KS-P), and the DRU case udry2.ks_p.

Pair law: two histories drawn independently given their shared last-four suffix S4.
Every identity is algebraic in the stand-in values (tower property only), so it holds exactly."""

from __future__ import annotations  # noqa: I001

import importlib
import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import hwsu_dry as udry  # noqa: E402

L, S = 8, 4
P = L - S


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


def _chain():
    c = udry.nonreversible_chain()
    T = [[Fraction(x) for x in r] for r in c["T"]]
    E = [[Fraction(x) for x in r] for r in c["E"]]
    pi = [Fraction(x) for x in c["pi"]]
    return T, E, pi


T, E, PI = _chain()
NS, V = len(PI), len(E[0])


def joint(length):
    out = {}
    for w in itertools.product(range(V), repeat=length):
        a = [PI[z] * E[z][w[0]] for z in range(NS)]
        for t in range(1, length):
            a = [sum(a[y] * T[y][z] for y in range(NS)) * E[z][w[t]] for z in range(NS)]
        out[w] = sum(a)
    return out


J8, J9 = joint(L), joint(L + 1)
SUF = list(itertools.product(range(V), repeat=S))
PRE = list(itertools.product(range(V), repeat=P))
PS = {s: sum(J8[p + s] for p in PRE) for s in SUF}
Q8 = {p + s: [J9[p + s + (v,)] / J8[p + s] for v in range(V)] for s in SUF for p in PRE}
Q4 = {s: [sum(J9[p + s + (v,)] for p in PRE) / PS[s] for v in range(V)] for s in SUF}


def lg(x):
    return Fraction(math.log(float(x)))


L8 = {h: [lg(x) for x in q] for h, q in Q8.items()}
L4 = {s: [lg(x) for x in q] for s, q in Q4.items()}


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def pair_moment(fa, fb, matched=True):
    """1/2 E[(a1 - a2)^T (b1 - b2)] under the pair law (matched) or independent histories."""
    tot = Fraction(0)
    if matched:
        for s in SUF:
            for p1 in PRE:
                for p2 in PRE:
                    w = J8[p1 + s] * J8[p2 + s] / PS[s]
                    h1, h2 = p1 + s, p2 + s
                    tot += w * dot(sub(fa(h1), fa(h2)), sub(fb(h1), fb(h2)))
    else:
        hs = list(J8)
        for h1 in hs:
            for h2 in hs:
                tot += J8[h1] * J8[h2] * dot(sub(fa(h1), fa(h2)), sub(fb(h1), fb(h2)))
    return tot / 2


def cond_cov(fa, fb):
    tot = Fraction(0)
    for s in SUF:
        ea = [sum(J8[p + s] * fa(p + s)[v] for p in PRE) / PS[s] for v in range(V)]
        eb = [sum(J8[p + s] * fb(p + s)[v] for p in PRE) / PS[s] for v in range(V)]
        eab = sum(J8[p + s] * dot(fa(p + s), fb(p + s)) for p in PRE) / PS[s]
        tot += PS[s] * (eab - dot(ea, eb))
    return tot


def fa(h):
    return [Fraction(h[0] + 2 * h[2] * (v + 1), 3) + Fraction(h[-1], 5) for v in range(V)]


def fb(h):
    return [Fraction((h[1] + 1) * (v + 2), 7) - Fraction(h[3] * h[-2], 2) for v in range(V)]


def test_chain_is_valid_and_nonreversible():
    assert all(sum(r) == 1 for r in T) and all(sum(r) == 1 for r in E) and sum(PI) == 1
    assert sum(J8.values()) == 1
    rev = [[PI[j] * T[j][i] / PI[i] for j in range(NS)] for i in range(NS)]
    assert rev != T


def test_lemma_p2_pair_moment_equals_conditional_covariance():
    assert pair_moment(fa, fb) == cond_cov(fa, fb)
    assert pair_moment(fa, fa) == cond_cov(fa, fa) >= 0


def test_lemma_p2_A_full_mean_equals_z_rho4():
    """E[A_full] with d = q1 - q2 equals E[z^T rho4], rho4 = q32 - q4 (z any history function)."""

    def q(h):
        return Q8[h]

    lhs = pair_moment(q, fb)
    rhs = sum(J8[h] * dot(fb(h), sub(Q8[h], Q4[h[P:]])) for h in J8)
    assert lhs == rhs


def test_lemma_j_G_equals_two_kls():
    def q(h):
        return Q8[h]

    def lq(h):
        return L8[h]

    EG = pair_moment(q, lq)
    kl = sum(J8[h] * dot(sub(Q8[h], Q4[h[P:]]), sub(L8[h], L4[h[P:]])) for h in J8)
    assert EG == kl
    assert float(EG) > 0


def test_lemma_p1_suffix_only_predictor_has_zero_effect():
    def suf_only(h):
        return [Fraction(h[-1] * (v + 1) + 3 * h[-4], 11) for v in range(V)]

    assert pair_moment(fa, suf_only) == 0
    assert pair_moment(suf_only, suf_only) == 0


def test_planted_defect_independent_suffixes_breaks_identity():
    """Pairs built from independent histories (suffix not shared) do not satisfy Lemma P2/P1."""

    def suf_only(h):
        return [Fraction(h[-1] * (v + 1), 11) for v in range(V)]

    assert pair_moment(fa, fb, matched=False) != cond_cov(fa, fb)
    assert pair_moment(suf_only, suf_only, matched=False) != 0


def test_ks_p_dru_case_passes(tmp_path):
    udry2 = mod("hwsu_dry2")
    r = udry2.ks_p(tmp_path)
    assert r["status"] == "PASS"


def test_uc_contract_loaded():
    assert uc.CONTRACT is not None
