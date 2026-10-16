"""K4b author A, TEST_PLAN A1 (protocol §1.2, §11.4): Proposition 1 by exact enumeration.

A tiny asymmetric stationary HMM (S = 3 states, V = 3 symbols, L = 6, K = 2) is enumerated in
exact Fraction arithmetic. m_K is the restart-at-pi suffix filter (emit first, transitions
between emissions), m_L the full-history filter, r_K = m_L - m_K. Proposition 1 says
E[g(S_K) . r_K] = 0 for every bounded suffix-only g under the stationary law; a
prefix-dependent g gives a non-zero value. Self-contained exact code (TEST_PLAN A1)."""

from __future__ import annotations

import random
import sys
from fractions import Fraction as Fr
from functools import lru_cache
from itertools import product
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
             "tools/x4_circle_history", "tools/x4_oracle_profile"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

S, V, L, K = 3, 3, 6, 2
T = ((Fr(1, 2), Fr(1, 3), Fr(1, 6)),
     (Fr(1, 5), Fr(1, 2), Fr(3, 10)),
     (Fr(2, 5), Fr(1, 10), Fr(1, 2)))
E = ((Fr(7, 10), Fr(1, 5), Fr(1, 10)),
     (Fr(1, 5), Fr(3, 5), Fr(1, 5)),
     (Fr(1, 10), Fr(3, 10), Fr(3, 5)))
# Unit feature vectors with rational coordinates (|c_s| = 1 exactly).
C = ((Fr(1), Fr(0)), (Fr(-3, 5), Fr(4, 5)), (Fr(-3, 5), Fr(-4, 5)))


def solve(A, b):
    n = len(b)
    M = [list(row) + [bb] for row, bb in zip(A, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return tuple(M[i][n] / M[i][i] for i in range(n))


def stationary(Tm):
    n = len(Tm)
    A = [[Tm[s][t] - (1 if s == t else 0) for s in range(n)] for t in range(n)]
    A[-1] = [Fr(1)] * n
    return solve(A, [Fr(0)] * (n - 1) + [Fr(1)])


PI = stationary(T)


def forward(start, obs):
    """alpha_t(z) = P(w_1..w_t, z_t = z): emit first, transitions between emissions."""
    a = [start[z] * E[z][obs[0]] for z in range(S)]
    for w in obs[1:]:
        a = [sum(a[z] * T[z][y] for z in range(S)) * E[y][w] for y in range(S)]
    return a


def mean_of(a):
    tot = sum(a)
    return (sum(a[z] * C[z][0] for z in range(S)) / tot,
            sum(a[z] * C[z][1] for z in range(S)) / tot)


@lru_cache(maxsize=None)
def law(start, restart, k, length=L):
    """Rows (w, P(w), r_k(w)) over every history of the given length."""
    rows = []
    for w in product(range(V), repeat=length):
        a = forward(start, w)
        mL = mean_of(a)
        mK = mean_of(forward(restart, w[length - k:]))
        rows.append((w, sum(a), (mL[0] - mK[0], mL[1] - mK[1])))
    return tuple(rows)


def expect(rows, g):
    return sum(p * (g(w, r)[0] * r[0] + g(w, r)[1] * r[1]) for w, p, r in rows)


def random_table(seed, k):
    rng = random.Random(seed)
    q = lambda: Fr(rng.randint(-9, 9), rng.randint(1, 7))  # noqa: E731
    return {s: (q(), q()) for s in product(range(V), repeat=k)}


def test_hmm_is_asymmetric_stationary_and_positive():
    assert all(sum(row) == 1 for row in T) and all(sum(row) == 1 for row in E)
    assert any(T[s][t] != T[t][s] for s in range(S) for t in range(S))
    assert all(p > 0 for p in PI) and sum(PI) == 1
    assert tuple(sum(PI[s] * T[s][t] for s in range(S)) for t in range(S)) == PI
    assert len(set(PI)) > 1  # not uniform: stationarity is doing real work
    assert all(c[0] ** 2 + c[1] ** 2 == 1 for c in C)


def test_history_law_sums_to_one():
    rows = law(PI, PI, K)
    assert len(rows) == V ** L
    assert sum(p for _, p, _ in rows) == 1
    assert all(p > 0 for _, p, _ in rows)


def test_residual_is_not_identically_zero():
    rows = law(PI, PI, K)
    assert any(r != (0, 0) for _, _, r in rows)


@pytest.mark.parametrize("seed", range(8))
def test_random_suffix_table_has_zero_expectation(seed):
    rows = law(PI, PI, K)
    g = random_table(1000 + seed, K)
    assert expect(rows, lambda w, r: g[w[L - K:]]) == 0


@pytest.mark.parametrize("k", [1, 2, 3])
def test_suffix_identity_holds_for_other_suffix_lengths(k):
    rows = law(PI, PI, k)
    g = random_table(77 + k, k)
    assert expect(rows, lambda w, r: g[w[L - k:]]) == 0


def test_conditional_residual_vanishes_given_each_suffix():
    rows = law(PI, PI, K)
    acc = {}
    for w, p, r in rows:
        x, y = acc.get(w[L - K:], (Fr(0), Fr(0)))
        acc[w[L - K:]] = (x + p * r[0], y + p * r[1])
    assert len(acc) == V ** K
    assert all(v == (0, 0) for v in acc.values())


def test_rotated_and_reflected_suffix_fields_stay_zero():
    """Gauge invariance: a rotation or reflection of a suffix-only field is suffix-only."""
    rows = law(PI, PI, K)
    g = random_table(4242, K)
    cs, sn = Fr(3, 5), Fr(4, 5)
    rot = lambda v: (cs * v[0] - sn * v[1], sn * v[0] + cs * v[1])  # noqa: E731
    ref = lambda v: (v[0], -v[1])  # noqa: E731
    assert expect(rows, lambda w, r: rot(g[w[L - K:]])) == 0
    assert expect(rows, lambda w, r: ref(rot(g[w[L - K:]]))) == 0


def test_constant_field_is_zero():
    rows = law(PI, PI, K)
    assert expect(rows, lambda w, r: (Fr(1), Fr(0))) == 0
    assert expect(rows, lambda w, r: (Fr(0), Fr(1))) == 0


def test_prefix_dependent_field_is_nonzero():
    rows = law(PI, PI, K)
    # g = r_K itself depends on the whole history: E[r . r] = E|r|^2 > 0.
    assert expect(rows, lambda w, r: r) > 0
    # A bounded unit-valued history field: sign(e1 . r) e1 gives E|e1 . r| > 0.
    sgn = lambda w, r: (Fr(1) if r[0] >= 0 else Fr(-1), Fr(0))  # noqa: E731
    sgn2 = lambda w, r: (Fr(0), Fr(1) if r[1] >= 0 else Fr(-1))  # noqa: E731
    assert expect(rows, sgn) + expect(rows, sgn2) > 0
    assert expect(rows, sgn) >= 0 and expect(rows, sgn2) >= 0


def test_field_mixing_suffix_and_residual_sign_is_nonzero():
    """A suffix table multiplied by a residual-sign indicator is no longer suffix-only."""
    rows = law(PI, PI, K)
    g = random_table(9, K)

    def mixed(w, r):
        v = g[w[L - K:]]
        on = (v[0] * r[0] + v[1] * r[1]) > 0
        return v if on else (Fr(0), Fr(0))

    assert expect(rows, lambda w, r: g[w[L - K:]]) == 0
    assert expect(rows, mixed) > 0


def test_nonstationary_start_breaks_the_identity():
    """Sanity of the enumerator: with z1 from a non-stationary start and the suffix filter
    restarted at that start, E[r_K | S_K] is not zero for some suffix."""
    start = (Fr(1), Fr(0), Fr(0))
    rows = law(start, start, K)
    assert sum(p for _, p, _ in rows) == 1
    acc = {}
    for w, p, r in rows:
        x, y = acc.get(w[L - K:], (Fr(0), Fr(0)))
        acc[w[L - K:]] = (x + p * r[0], y + p * r[1])
    assert any(v != (0, 0) for v in acc.values())
