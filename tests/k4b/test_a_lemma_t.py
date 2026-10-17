"""K4b author A, TEST_PLAN A4 (protocol §1.3, CERTIFICATE §2): Lemma T on an exact toy.

P* is a 3-state HMM (L = 4, K = 2). P_op perturbs pairs of equal entries of T*, E* and pi* by
exactly +-kappa (relative), so every row stays stochastic and the relative deviation is
exactly kappa = 1/100. Q is taken to be P_op itself. For scores f(h, r) that are 1-Lipschitz in
r with |f| <= |r|, |E_Q f(h, r_op) - E_P* f(h, r_*)| <= 2(rho - 1) + 4 TV(Q, P*), with
rho = ((1 + kappa)/(1 - kappa))^(2L + 1). Everything is exact Fraction arithmetic."""

from __future__ import annotations

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

S, V, L, K = 3, 3, 4, 2
KAPPA = Fr(1, 100)  # was 1/40: then zb ~ 1.153 >= 1 (correction round 1)
H, Q4, Q5, F35 = Fr(1, 2), Fr(1, 4), Fr(1, 5), Fr(3, 5)
UP, DN = 1 + KAPPA, 1 - KAPPA
T_STAR = ((H, Q4, Q4), (Q4, H, Q4), (Q4, Q4, H))
E_STAR = ((F35, Q5, Q5), (Q5, F35, Q5), (Q5, Q5, F35))
PI_STAR = (Fr(1, 3), Fr(1, 3), Fr(1, 3))
T_OP = ((H, Q4 * UP, Q4 * DN), (Q4 * DN, H, Q4 * UP), (Q4 * UP, Q4 * DN, H))
E_OP = ((F35, Q5 * DN, Q5 * UP), (Q5 * UP, F35, Q5 * DN), (Q5 * DN, Q5 * UP, F35))
PI_OP = (Fr(1, 3) * UP, Fr(1, 3) * DN, Fr(1, 3))
C = ((Fr(1), Fr(0)), (Fr(-3, 5), Fr(4, 5)), (Fr(-3, 5), Fr(-4, 5)))
STAR, OP = (T_STAR, E_STAR, PI_STAR), (T_OP, E_OP, PI_OP)
UNITS = ((Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(3, 5), Fr(-4, 5)), (Fr(-5, 13), Fr(12, 13)))
RHO = ((1 + KAPPA) / (1 - KAPPA)) ** (2 * L + 1)


def forward(law, obs):
    Tm, Em, pi = law
    a = [pi[z] * Em[z][obs[0]] for z in range(S)]
    for w in obs[1:]:
        a = [sum(a[z] * Tm[z][y] for z in range(S)) * Em[y][w] for y in range(S)]
    return a


def normalise(a):
    tot = sum(a)
    return tuple(x / tot for x in a)


def mean_of(post):
    return (sum(post[z] * C[z][0] for z in range(S)), sum(post[z] * C[z][1] for z in range(S)))


@lru_cache(maxsize=None)
def history_law(law):
    """{w: (P(w), full posterior, suffix posterior restarted at pi, r = m_L - m_K)}."""
    out = {}
    for w in product(range(V), repeat=L):
        a = forward(law, w)
        post_full, post_suf = normalise(a), normalise(forward(law, w[L - K:]))
        mL, mK = mean_of(post_full), mean_of(post_suf)
        out[w] = (sum(a), post_full, post_suf, (mL[0] - mK[0], mL[1] - mK[1]))
    return out


def path_prob(law, z, w):
    Tm, Em, pi = law
    p = pi[z[0]] * Em[z[0]][w[0]]
    for t in range(1, L):
        p *= Tm[z[t - 1]][z[t]] * Em[z[t]][w[t]]
    return p


def l1(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def tv_histories():
    hs, ho = history_law(STAR), history_law(OP)
    return sum(abs(ho[w][0] - hs[w][0]) for w in hs) / 2


def z_bound():
    return 2 * (RHO - 1) + 4 * tv_histories()


def test_kappa_is_known_exactly():
    for Tm, Em, pi in (STAR, OP):
        assert all(sum(row) == 1 for row in Tm) and all(sum(row) == 1 for row in Em)
        assert sum(pi) == 1 and all(x > 0 for x in pi)
    devs = []
    for a, b in ((T_OP, T_STAR), (E_OP, E_STAR)):
        devs += [abs(a[i][j] - b[i][j]) / b[i][j] for i in range(S) for j in range(len(b[i]))]
    devs += [abs(PI_OP[i] - PI_STAR[i]) / PI_STAR[i] for i in range(S)]
    assert max(devs) == KAPPA
    assert RHO > 1


def test_path_law_l1_within_rho():
    total = Fr(0)
    for z in product(range(S), repeat=L):
        for w in product(range(V), repeat=L):
            ps, po = path_prob(STAR, z, w), path_prob(OP, z, w)
            assert DN ** (2 * L) * ps <= po <= UP ** (2 * L) * ps  # 2L factors per path
            total += abs(po - ps)
    assert total <= UP ** (2 * L) - 1 <= RHO - 1
    assert tv_histories() <= total / 2


def test_posteriors_within_rho():
    hs, ho = history_law(STAR), history_law(OP)
    for w in hs:
        assert l1(ho[w][1], hs[w][1]) <= RHO - 1
        assert l1(ho[w][2], hs[w][2]) <= RHO - 1


def test_residual_difference_within_two_rho():
    hs, ho = history_law(STAR), history_law(OP)
    for w in hs:
        d = (ho[w][3][0] - hs[w][3][0], ho[w][3][1] - hs[w][3][1])
        for u in UNITS:
            assert abs(u[0] * d[0] + u[1] * d[1]) <= 2 * (RHO - 1)
        assert abs(d[0]) + abs(d[1]) <= 2 * 2 * (RHO - 1)  # |.|_1 <= sqrt(2) |.|_2


def _fields():
    """Scores f(h, r): 1-Lipschitz in r (Euclidean) and |f(h, r)| <= |r|."""
    out = [lambda w, r, u=u: u[0] * r[0] + u[1] * r[1] for u in UNITS]
    out.append(lambda w, r: (lambda u: u[0] * r[0] + u[1] * r[1])(UNITS[sum(w) % 4]))
    out.append(lambda w, r: abs(r[0]))
    out.append(lambda w, r: -abs(r[1]))
    out.append(lambda w, r: max(abs(r[0]), abs(r[1])))
    return out


@pytest.mark.parametrize("idx", range(len(_fields())))
def test_lemma_t_transport_bound(idx):
    f = _fields()[idx]
    hs, ho = history_law(STAR), history_law(OP)
    e_q = sum(ho[w][0] * f(w, ho[w][3]) for w in ho)
    e_s = sum(hs[w][0] * f(w, hs[w][3]) for w in hs)
    assert abs(e_q - e_s) <= z_bound()


def test_lemma_t_is_not_vacuous():
    hs, ho = history_law(STAR), history_law(OP)
    zb = z_bound()
    # By hand: (1 + x)^n <= e^(nx); RHO = (1 + 2/99)^9 < e^(18/99) < 6/5, and
    # 4 TV <= 2(UP^8 - 1) < 2(e^(8/100) - 1) < 0.167 (path-law bound above), so zb < 0.567.
    assert 0 < zb < 1
    diffs = []
    for f in _fields():
        e_q = sum(ho[w][0] * f(w, ho[w][3]) for w in ho)
        e_s = sum(hs[w][0] * f(w, hs[w][3]) for w in hs)
        diffs.append(abs(e_q - e_s))
    assert max(diffs) > 0  # the perturbation is visible in some score


def test_zero_perturbation_gives_zero_bound_and_zero_gap():
    hs = history_law(STAR)
    tv = sum(abs(hs[w][0] - hs[w][0]) for w in hs) / 2
    rho0 = ((1 + Fr(0)) / (1 - Fr(0))) ** (2 * L + 1)
    assert 2 * (rho0 - 1) + 4 * tv == 0
    for f in _fields():
        assert sum(hs[w][0] * f(w, hs[w][3]) for w in hs) - \
            sum(hs[w][0] * f(w, hs[w][3]) for w in hs) == 0
