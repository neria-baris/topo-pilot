"""Author A (job 0224): KG6 port, the K4b/HWSC known statements under the hi binding (§5 KG6).

Written from the K4b protocol statements (Proposition 1, Theorem A, Lemma N, the decision rule)
and tools/hwsc/API.md, not from tests/k4b or tests/hwsc. Every test runs inside
`with gb.world("hi"):` (which nests hwsc_bind.bound_stage_c) and checks restoration afterwards.
"""

from __future__ import annotations  # noqa: I001

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _d in ("c1prime", "k4b", "hwsb", "hwsc", "x4_circle_history", "hwsg"):
    if str(REPO / "tools" / _d) not in sys.path:
        sys.path.insert(0, str(REPO / "tools" / _d))
_ERR = None
try:
    import hwsg_config as gc  # noqa: F401
    import hwsg_bind as gb
    import hwsc_bind
    import hwsc_outcome
    import k4b_cert
    import k4b_stats
    import process_law
except Exception as e:
    _ERR = e

HI = (620631, 620632, 620633)
M = Fraction(1, 100)


@pytest.fixture
def hi():
    if _ERR is not None:
        pytest.fail(f"hwsg modules not importable: {_ERR!r}")
    before = (k4b_stats.MODELS, gb.ACTIVE)
    with gb.world("hi") as info:
        assert gb.ACTIVE == "hi" and hwsc_bind.ACTIVE is True
        yield info
    assert gb.ACTIVE is None and not hwsc_bind.ACTIVE
    assert k4b_stats.MODELS is before[0]


# ------------------------------------------------------------------ a tiny asymmetric HMM (exact)

T = [[Fraction(6, 10), Fraction(3, 10), Fraction(1, 10)],
     [Fraction(1, 10), Fraction(7, 10), Fraction(2, 10)],
     [Fraction(3, 10), Fraction(1, 10), Fraction(6, 10)]]
E = [[Fraction(8, 10), Fraction(2, 10)], [Fraction(3, 10), Fraction(7, 10)],
     [Fraction(1, 2), Fraction(1, 2)]]
FEAT = [(Fraction(1), Fraction(0)), (Fraction(-1, 2), Fraction(3, 4)),
        (Fraction(-1, 2), Fraction(-3, 4))]
L, K = 6, 2


def _stationary():
    # solve pi T = pi by power iteration in exact arithmetic is slow; use the closed form via
    # linear solve on 3 states (Cramer on (T^t - I) with sum constraint).
    a = [[T[j][i] - (1 if i == j else 0) for j in range(3)] for i in range(3)]
    a[2] = [Fraction(1)] * 3
    b = [Fraction(0), Fraction(0), Fraction(1)]
    n = 3
    for c in range(n):  # Gauss-Jordan
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p], b[c], b[p] = a[p], a[c], b[p], b[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
                b[r] -= f * b[c]
    return [b[i] / a[i][i] for i in range(n)]


PI = _stationary()


def _forward(obs):
    """Unnormalised P(obs, z_last) from the stationary start."""
    a = [PI[z] * E[z][obs[0]] for z in range(3)]
    for o in obs[1:]:
        a = [sum(a[y] * T[y][z] for y in range(3)) * E[z][o] for z in range(3)]
    return a


def _m(obs):
    a = _forward(obs)
    s = sum(a)
    post = [x / s for x in a]
    nxt = [sum(post[y] * T[y][z] for y in range(3)) for z in range(3)]
    return (sum(nxt[z] * FEAT[z][0] for z in range(3)), sum(nxt[z] * FEAT[z][1] for z in range(3)))


ROWS = []
for _h in itertools.product((0, 1), repeat=L):
    _p = sum(_forward(_h))
    _mL, _mK = _m(_h), _m(_h[-K:])
    ROWS.append((_h, _p, (_mL[0] - _mK[0], _mL[1] - _mK[1])))


def test_hmm_is_a_law(hi):
    assert sum(PI) == 1 and all(sum(PI[y] * T[y][z] for y in range(3)) == PI[z] for z in range(3))
    assert sum(p for _, p, _ in ROWS) == 1


def test_proposition_1_suffix_only_zero(hi):
    import random
    rnd = random.Random(3)
    for _ in range(5):
        g = {s: (Fraction(rnd.randint(-9, 9), 7), Fraction(rnd.randint(-9, 9), 5))
             for s in itertools.product((0, 1), repeat=K)}
        tot = sum(p * (g[h[-K:]][0] * r[0] + g[h[-K:]][1] * r[1]) for h, p, r in ROWS)
        assert tot == 0
    # a prefix-dependent g does not give zero
    tot = sum(p * ((1 if h[0] else -1) * r[0]) for h, p, r in ROWS)
    assert tot != 0


def _norm(r):
    return math.hypot(float(r[0]), float(r[1]))


def test_theorem_a_support_trap(hi):
    S = {h for h, _, r in ROWS if h[0] == 1 or r[0] > 0}  # correlated with prefix and sign
    u = {h: ((1.0, 0.0) if h[1] else (0.0, -1.0)) for h in S}
    xm = sum(float(p) * ((u[h][0] * float(r[0]) + u[h][1] * float(r[1])) if h in S
                         else -_norm(r)) for h, p, r in ROWS)
    xp = sum(float(p) * ((u[h][0] * float(r[0]) + u[h][1] * float(r[1])) if h in S
                         else _norm(r)) for h, p, r in ROWS)
    assert xm < xp
    for t, th in itertools.product((0.0, 0.5, 1.0), [k * math.pi / 6 for k in range(12)]):
        v = (t * math.cos(th), t * math.sin(th))
        d = sum(float(p) * ((u[h][0] * float(r[0]) + u[h][1] * float(r[1])) if h in S
                            else v[0] * float(r[0]) + v[1] * float(r[1])) for h, p, r in ROWS)
        assert xm - 1e-15 <= d <= xp + 1e-15
    # sharpness: the extremal completions -r/|r| and +r/|r| attain the bounds
    lo = sum(float(p) * ((u[h][0] * float(r[0]) + u[h][1] * float(r[1])) if h in S
                         else -_norm(r)) for h, p, r in ROWS)
    assert abs(lo - xm) <= 1e-15


# ------------------------------------------------------------------ Lemma N, transport bound


def _covers(nhat, s, B):
    lo, hi_ = Fraction(float(nhat)) - B, Fraction(float(nhat)) + B
    return hi_ >= 0 and hi_ * hi_ >= s and (lo <= 0 or lo * lo <= s)


@pytest.mark.parametrize("nhat,M32,M4", [
    (0.0, (0, 0), (0, 0)),
    (1e-300, (Fraction(1, 10**40), 0), (0, 0)),
    (0.5, (Fraction(3, 10), Fraction(4, 10)), (0, 0)),
    (10.0, (Fraction(3, 10), Fraction(4, 10)), (0, 0)),  # adversarial n_hat
    (0.1414213562373095, (Fraction(1, 10), 0), (0, Fraction(1, 10))),
])
def test_lemma_n_covers(hi, nhat, M32, M4):
    eps4, eps32 = Fraction(1, 10**12), Fraction(1, 10**12)
    B = k4b_cert.norm_bound(nhat, M32, M4, eps4, eps32)
    s = (Fraction(M32[0]) - Fraction(M4[0])) ** 2 + (Fraction(M32[1]) - Fraction(M4[1])) ** 2
    assert _covers(nhat, s, B)
    assert B >= Fraction(3, 2) * (eps4 + eps32)


def test_transport_bound_planted(hi, monkeypatch):
    monkeypatch.setattr(process_law, "process_law_bound", lambda *a: {
        "status": "BOUNDED", "Z_bound": {"exact_upper": "3/1000000", "float": 3e-6}})
    assert k4b_cert.transport_bound(None, None, None, None)["Z_bound"] == Fraction(3, 10**6)
    monkeypatch.setattr(process_law, "process_law_bound",
                        lambda *a: {"status": "UNAVAILABLE/NONTERMINATING_LOGIT"})
    with pytest.raises(Exception) as ei:
        k4b_cert.transport_bound(None, None, None, None)
    assert getattr(ei.value, "status", "") == "FAIL_TECHNICAL/IDENTITY"


# ------------------------------------------------------------------ decision boundaries


def test_support_equality_not_support(hi):
    r = k4b_stats.model_status(0.5, 0.6, Fraction(49, 100), Fraction(0))
    assert r["status"].startswith("UNRESOLVED")
    r = k4b_stats.model_status(0.5, 0.6, Fraction(49, 100) - Fraction(1, 10**30), Fraction(0))
    assert r["status"] == "SUPPORT"


def test_exclude_equality_not_exclude(hi):
    U = 0.0078125  # 2**-7, exact
    r = k4b_stats.model_status(0.0, U, Fraction(0), M - Fraction(U))
    assert r["status"].startswith("UNRESOLVED")
    r = k4b_stats.model_status(0.0, U, Fraction(0), M - Fraction(U) - Fraction(1, 10**30))
    assert r["status"] == "EXCLUDE"
    # lower side exactly at -M is not EXCLUDE
    r = k4b_stats.model_status(-0.5, 0.0, Fraction(-49, 100), Fraction(0))
    assert r["status"] != "EXCLUDE"


def test_support_exclude_exclusive_and_numerical(hi):
    r = k4b_stats.model_status(0.03, 0.04, Fraction(1, 50), Fraction(0))
    assert r["status"] == "UNRESOLVED/NUMERICAL" and r["status_without_F"] == "SUPPORT"
    for L_, U_ in ((0.02, 0.005), (0.5, 0.001)):
        s = k4b_stats.model_status(L_, U_, Fraction(0), Fraction(0))["status"]
        assert s in ("SUPPORT", "EXCLUDE", "UNRESOLVED", "UNRESOLVED/NUMERICAL")


def _pm(L_, F, st):
    return {"L": L_, "F_minus": F, "status": st}


@pytest.mark.parametrize("st,kind", [("EXCLUDE", "EXCLUDE"), ("UNRESOLVED", "UNRESOLVED"),
                                     ("UNRESOLVED/NUMERICAL", "UNRESOLVED"), ("SUPPORT", None)])
def test_positive_below_margin(hi, st, kind):
    F = Fraction(1e-6)
    zero = hwsc_outcome.positive_below_margin({HI[0]: _pm(1e-6, F, st)})
    assert zero["positive"][HI[0]] is False and zero["per_model"][HI[0]] is None
    up = hwsc_outcome.positive_below_margin({HI[0]: _pm(math.nextafter(1e-6, 1), F, st)})
    assert up["positive"][HI[0]] is True and up["per_model"][HI[0]] == kind


def test_overall_on_hi_masters(hi):
    assert tuple(k4b_stats.MODELS) == HI
    o = k4b_stats.overall
    assert o(dict.fromkeys(HI, "SUPPORT")) == "SUPPORT"
    assert o(dict.fromkeys(HI, "EXCLUDE")) == "EXCLUSION"
    assert o(dict(zip(HI, ("SUPPORT", "SUPPORT", "UNRESOLVED")))) == "MIXED"
    assert o(dict(zip(HI, ("SUPPORT", "EXCLUDE", "SUPPORT")))) == "MIXED"
    assert o(dict.fromkeys(HI, "UNRESOLVED")) == "INCONCLUSIVE"
    assert o(dict(zip(HI, ("UNRESOLVED", "UNRESOLVED/NUMERICAL", "UNRESOLVED")))) \
        == "INCONCLUSIVE/NUMERICAL"
