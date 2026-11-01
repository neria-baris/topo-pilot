"""Author A (job 0197): KD6, the K4b known cases at the hwsd constants (§6 KD6; TEST_PLAN A).

`hwsd_known.kd6` runs this file alone; every check below runs inside `hwsd_bind.bound_hwsd()`.
(1) Proposition 1 by exact enumeration; (2) Theorem A on endpoint arrays; (3) Lemma N on
planted inputs; (4) the k4b_stats.model_status boundaries at M = 1/100; (5) the ranks
84/4,917/125/4,875/250 at 5,000 draws and 70/49,931 at 50,000 draws; (6) the chart section
and protocol sha inside the binding; (7) the K4b constants restored after the block.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import random
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsd"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsd_config as dc  # noqa: E402, I001
import hwsd_bind as db  # noqa: E402
import c1_means  # noqa: E402
import k4b_cert  # noqa: E402
import k4b_config  # noqa: E402
import k4b_scores  # noqa: E402
import k4b_stats  # noqa: E402
import test_a_hwsd_ref as ref  # noqa: E402

M = Fraction(1, 100)


@pytest.fixture
def bound():
    with db.bound_hwsd() as info:
        assert k4b_config.MODELS == (620301, 620302, 620303)
        yield info


# ---- (1) Proposition 1: E[f(last K) . (m_full - m_K)] = 0 for every suffix-only f ----
def _hmm(S, A, seed):
    rnd = random.Random(seed)

    def stoch(n):
        w = [rnd.randint(1, 9) for _ in range(n)]
        return [Fraction(x, sum(w)) for x in w]

    return ([stoch(S) for _ in range(S)], [stoch(A) for _ in range(S)], stoch(S),
            [(Fraction(rnd.randint(-5, 5), 7), Fraction(rnd.randint(-5, 5), 3)) for _ in range(A)])


def _enumerate(T, E, pi, c, L):
    S, A = len(pi), len(E[0])
    out = {}
    for h in itertools.product(range(A), repeat=L):
        al = [pi[s] * E[s][h[0]] for s in range(S)]
        for x in h[1:]:
            al = [sum(al[r] * T[r][s] for r in range(S)) * E[s][x] for s in range(S)]
        pred = [sum(al[r] * T[r][s] for r in range(S)) for s in range(S)]
        num = [sum(pred[s] * E[s][a] for s in range(S)) for a in range(A)]
        N = (sum(num[a] * c[a][0] for a in range(A)), sum(num[a] * c[a][1] for a in range(A)))
        out[h] = (sum(al), N)
    return out


@pytest.mark.parametrize("S,A,seed", [(2, 2, 1), (3, 2, 2), (2, 3, 3), (3, 3, 4)])
def test_proposition_1_exact(bound, S, A, seed):
    T, E, pi, c = _hmm(S, A, seed)
    L, K = 6, 4
    tab = _enumerate(T, E, pi, c, L)
    assert sum(p for p, _ in tab.values()) == 1
    agg = {}
    for h, (p, N) in tab.items():
        s = h[L - K:]
        P, Nx, Ny = agg.get(s, (0, 0, 0))
        agg[s] = (P + p, Nx + N[0], Ny + N[1])
    rnd = random.Random(seed)
    f = {s: (Fraction(rnd.randint(-9, 9), 5), Fraction(rnd.randint(-9, 9), 11)) for s in agg}
    total = [Fraction(0), Fraction(0)]
    for h, (p, N) in tab.items():
        s = h[L - K:]
        P, Nx, Ny = agg[s]
        r4 = (N[0] - p * Nx / P, N[1] - p * Ny / P)  # P(h) (m_full(h) - m_K(s))
        total[0] += f[s][0] * r4[0] + f[s][1] * r4[1]
    assert total[0] == 0
    g = {h: Fraction(rnd.randint(-9, 9), 5) for h in tab}  # a whole-history field: not zero
    whole = sum(g[h] * (N[0] - p * agg[h[L - K:]][1] / agg[h[L - K:]][0])
                for h, (p, N) in tab.items())
    assert whole != 0


# ---- (2) Theorem A: every completion lies in [E X-, E X+] ----
def test_theorem_a_completions(bound):
    rng = np.random.default_rng(12)
    n = 50
    m32, m4 = rng.normal(size=(n, 2)), rng.normal(size=(n, 2))
    phi = rng.uniform(0, 2 * np.pi, n)
    sup = rng.random(n) < 0.6
    a = k4b_scores.endpoint_arrays(phi, sup, m32, m4)
    r4 = m32 - m4
    lo, hi = float(np.mean(a["X_minus"])), float(np.mean(a["X_plus"]))
    base = np.cos(phi) * r4[:, 0] + np.sin(phi) * r4[:, 1]
    for t in range(200):
        ang = rng.uniform(0, 2 * np.pi, n)
        if t == 0:
            ang = np.arctan2(-r4[:, 1], -r4[:, 0])  # the minimising completion
        elif t == 1:
            ang = np.arctan2(r4[:, 1], r4[:, 0])  # the maximising completion
        comp = np.where(sup, base, np.cos(ang) * r4[:, 0] + np.sin(ang) * r4[:, 1])
        assert np.all(a["X_minus"] <= comp + 1e-12) and np.all(comp <= a["X_plus"] + 1e-12)
        assert lo - 1e-12 <= float(np.mean(comp)) <= hi + 1e-12
    np.testing.assert_allclose(a["X_minus"][sup], base[sup], rtol=0, atol=1e-15)


# ---- (3) Lemma N ----
def test_lemma_n_isqrt_bracket(bound):
    assert k4b_cert.isqrt_bracket(Fraction(2), D=10**6) == 1414213
    D = 10**80
    k = k4b_cert.isqrt_bracket(Fraction(2))
    assert k * k <= 2 * D * D < (k + 1) * (k + 1)
    assert k4b_cert.isqrt_bracket(Fraction(9, 100)) == 3 * 10**79
    assert k4b_cert.isqrt_bracket(Fraction(0)) == 0


def test_lemma_n_norm_bound_planted(bound):
    D = 10**80
    eps = Fraction(1, 10**12)
    M32, M4 = (Decimal("0.3"), Decimal("0.4")), (Decimal("0"), Decimal("0"))  # |r| = 1/2
    B = k4b_cert.norm_bound(0.5, M32, M4, eps, eps)
    assert B == Fraction(1, D) + 3 * eps
    n = Fraction(0.3)
    B = k4b_cert.norm_bound(0.3, M32, M4, eps, eps)
    assert B == max(abs(n - Fraction(1, 2)), abs(n - Fraction(1, 2) - Fraction(1, D))) + 3 * eps
    B = k4b_cert.norm_bound(0.5, M32, M4, Fraction(0), Fraction(1, 10**9))
    assert B == Fraction(1, D) + Fraction(3, 2) * Fraction(1, 10**9)


# ---- (4) model_status boundaries at M = 1/100 ----
def test_model_status_boundaries(bound):
    assert k4b_config.MARGIN == M == dc.M
    cases = [
        (0.5, 0.6, Fraction(49, 100), Fraction(0)),  # L - F- = 1/100 exactly
        (0.5, 0.6, Fraction(48, 100), Fraction(0)),
        (0.0, 0.005, Fraction(0), M - Fraction(0.005)),  # U + F+ = 1/100 exactly
        (0.0, math.nextafter(0.005, 0.0), Fraction(0), M - Fraction(0.005)),
        (-0.5, -0.4, Fraction(0), Fraction(0)),  # NEGATIVE_ALIGNMENT, not EXCLUDE
        (-0.0099, 0.0, Fraction(0), Fraction(0)),
        (0.02, 0.03, Fraction(0), Fraction(0)),
        (0.004, 0.02, Fraction(1, 10**9), Fraction(1, 10**9)),
    ]
    want = ["UNRESOLVED/NUMERICAL", "SUPPORT", "UNRESOLVED/NUMERICAL", "EXCLUDE",
            "UNRESOLVED", "EXCLUDE", "SUPPORT", "UNRESOLVED"]
    for (L, U, Fm, Fp), w in zip(cases, want):
        got = k4b_stats.model_status(L, U, Fm, Fp)
        assert got["status"] == w, (L, U, Fm, Fp)
        r = ref.ref_model_status(L, U, Fm, Fp)
        assert got["status"] == r["status"] and got["status_without_F"] == r["status_without_F"]
        assert ("NEGATIVE_ALIGNMENT" in got["labels"]) == ("NEGATIVE_ALIGNMENT" in r["labels"])
    up = math.nextafter(0.5, 1.0)
    assert k4b_stats.model_status(up, 0.6, Fraction(49, 100), Fraction(0))["status"] == "SUPPORT"


def test_model_status_random_grid(bound):
    rnd = random.Random(6)
    for _ in range(2000):
        L = rnd.choice([-0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.0100001, 0.02])
        U = L + rnd.choice([0.0, 0.001, 0.01, 0.03])
        Fm = rnd.choice([Fraction(0), Fraction(1, 10**9), Fraction(1, 10**3)])
        Fp = rnd.choice([Fraction(0), Fraction(1, 10**9), Fraction(1, 10**3)])
        got, r = k4b_stats.model_status(L, U, Fm, Fp), ref.ref_model_status(L, U, Fm, Fp)
        assert got["status"] == r["status"] and got["status_without_F"] == r["status_without_F"]
        assert got["status"] != "SUPPORT" or "EXCLUDE" not in got["status"]


# ---- (5) ranks ----
def test_ranks(bound):
    assert c1_means.rank_for(k4b_config.ALPHA, 5000) == 84
    assert c1_means.rank_for(1 - k4b_config.ALPHA, 5000) == 4917
    assert c1_means.rank_for(Fraction(1, 40), 5000) == 125
    assert c1_means.rank_for(Fraction(39, 40), 5000) == 4875
    assert c1_means.rank_for(Fraction(1, 20), 5000) == 250
    assert c1_means.rank_for(Fraction(1, 720), 50000) == 70
    assert c1_means.rank_for(Fraction(719, 720), 50000) == 49931
    assert c1_means.rank_for(dc.P_LO, dc.STRONG_DRAWS) == dc.STRONG_RANKS["lo"]
    assert c1_means.rank_for(dc.P_HI, dc.STRONG_DRAWS) == dc.STRONG_RANKS["hi"]
    assert k4b_config.DRAWS == 5000 and k4b_config.ALPHA == Fraction(1, 60)
    v = np.random.default_rng(1).permutation(np.arange(50000, dtype=np.float64))
    val, kk = c1_means.quantile_with_rank(v, Fraction(1, 720))
    assert kk == 70 and val == 69.0 and c1_means.rank_check(v, val, 70)
    val, kk = c1_means.quantile_with_rank(v, Fraction(719, 720))
    assert kk == 49931 and val == 49930.0


def test_bounds_ranks_84_4917(bound):
    d = np.random.default_rng(2).permutation(np.arange(5000, dtype=np.float64))
    b = k4b_stats.bounds(d, d[::-1].copy())
    assert b["L"][0] == 83.0 and b["U"][0] == 4916.0


# ---- (6) chart section and protocol inside the binding ----
def test_chart_equality_and_protocol_inside_binding(bound):
    assert k4b_config.check_chart_equality()["equal"] is True
    assert k4b_config.CONTRACT["protocol_sha256"] == dc.PROTOCOL_SHA256
    sha = hashlib.sha256(dc.PROTOCOL_PATH.read_bytes()).hexdigest()
    assert sha == dc.PROTOCOL_SHA256 == (
        "938cebd599d2256b1ba4bb7d58c62a62c495d30b46cfb70c45215cca9b197775")
    assert k4b_config.SEEDS == dc.SEEDS and k4b_config.SEEDS["endpoint"] == 620413


# ---- (7) restoration ----
def test_constants_restored_after_the_block():
    before = k4b_config.MODELS
    with db.bound_hwsd():
        assert k4b_config.MODELS == (620301, 620302, 620303)
    assert k4b_config.MODELS is before
    assert k4b_config.MODELS == (1729, 2718, 3141)
