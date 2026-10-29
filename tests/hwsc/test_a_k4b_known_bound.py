"""Author A (job 0176): KC8, K4b's own known cases at the bound constants.

Protocol HWSC §4 KC8 (RC-5); K4B §1.2-§1.4 (Proposition 1, Theorem A),
§5.3 (Lemma N), §5.4-§5.5, §7.1 (F_plan), §8.1 (decision), §11.4. Every
test runs inside `hwsc_bind.bound_stage_c()` (stage-C model keys 620301-620303,
K4b seed names bound to 620311-620315). Exact arithmetic is Fraction; the
HMM, arrays and inputs are synthetic and in memory. `hwsc_known.kc8` runs
this file alone.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from decimal import Decimal
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[:1] != [_HWSC]:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402,I001
import hwsc_bind as cb  # noqa: E402
import c1_means  # noqa: E402
import k4b_cert  # noqa: E402
import k4b_config  # noqa: E402
import k4b_scores  # noqa: E402
import k4b_stats  # noqa: E402

K4B_MODELS = (1729, 2718, 3141)
STAGE_C = (620301, 620302, 620303)
SEEDS_C = {"val_sd": 620311, "val_b4": 620312, "endpoint": 620313,
           "fresh_b4": 620314, "val_projection": 620315}
M = Fr(1, 100)
D80 = 10**80


@pytest.fixture
def bound():
    with cb.bound_stage_c():
        assert k4b_config.MODELS == STAGE_C == k4b_stats.MODELS
        assert dict(k4b_config.SEEDS) == SEEDS_C
        yield
    assert k4b_config.MODELS == K4B_MODELS
    assert k4b_config.SEEDS["endpoint"] == 610103


# --------------------------------------------- Proposition 1 (exact enumeration)

T3 = [[Fr(1, 2), Fr(1, 3), Fr(1, 6)], [Fr(1, 5), Fr(3, 5), Fr(1, 5)],
      [Fr(1, 4), Fr(1, 8), Fr(5, 8)]]
E3 = [[Fr(7, 10), Fr(1, 5), Fr(1, 10)], [Fr(1, 6), Fr(1, 2), Fr(1, 3)],
      [Fr(1, 9), Fr(2, 9), Fr(2, 3)]]
C3 = [(Fr(1), Fr(0)), (Fr(-1, 2), Fr(3, 4)), (Fr(1, 3), Fr(-1))]
S3 = range(3)


def stationary(T):
    n = len(T)
    A = [[T[j][i] - (1 if i == j else 0) for j in range(n)] + [Fr(0)] for i in range(n)]
    A[-1] = [Fr(1)] * n + [Fr(1)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]


PI3 = stationary(T3)


def filt(obs):
    """Forward filter restarted at pi: (P(obs), posterior mean of c(z_last))."""
    a = [PI3[z] * E3[z][obs[0]] for z in S3]
    for w in obs[1:]:
        a = [sum(a[z] * T3[z][y] for z in S3) * E3[y][w] for y in S3]
    tot = sum(a)
    return tot, tuple(sum(a[z] * C3[z][i] for z in S3) / tot for i in (0, 1))


def enumerate_r(L, K):
    out = []
    for h in itertools.product(range(3), repeat=L):
        p, mL = filt(h)
        _, mK = filt(h[L - K:])
        out.append((h, p, (mL[0] - mK[0], mL[1] - mK[1])))
    return out


def test_stationary_law(bound):
    assert sum(PI3) == 1
    for y in S3:
        assert sum(PI3[z] * T3[z][y] for z in S3) == PI3[y]


@pytest.mark.parametrize("L, K", [(6, 1), (6, 2), (6, 4), (5, 4)])
def test_proposition1_suffix_only_zero(bound, L, K):
    rows = enumerate_r(L, K)
    assert sum(p for _, p, _ in rows) == 1
    acc = {}
    for h, p, r in rows:
        s = h[L - K:]
        ax, ay = acc.get(s, (Fr(0), Fr(0)))
        acc[s] = (ax + p * r[0], ay + p * r[1])
    assert all(v == (0, 0) for v in acc.values())  # E[1{S_K = s} r_K] = 0
    rnd = np.random.default_rng(L * 10 + K)
    for _ in range(5):  # random rational suffix tables g: E[g(S_K) . r_K] = 0
        g = {s: (Fr(int(rnd.integers(-9, 10)), 7), Fr(int(rnd.integers(-9, 10)), 5)) for s in acc}
        assert sum(p * (g[h[L - K:]][0] * r[0] + g[h[L - K:]][1] * r[1])
                   for h, p, r in rows) == 0
    # a prefix-dependent field is not covered by the identity
    pref = [sum(p * r[i] for h, p, r in rows if h[0] == v) for v in range(3) for i in (0, 1)]
    assert any(x != 0 for x in pref)
    # conditioning on support breaks it: S = {e1 . r > 0}, g = e1
    assert sum(p * r[0] for _, p, r in rows if r[0] > 0) > 0


# ------------------------------------------------ Theorem A (bounded estimand)

R_ROWS = [(Fr(3, 10), Fr(4, 10)), (Fr(-5, 26), Fr(12, 26)), (Fr(8, 17), Fr(-15, 17)),
          (Fr(0), Fr(0)), (Fr(-6, 25), Fr(-8, 25)), (Fr(7, 25), Fr(24, 25))]
SUP = [True, False, True, False, False, False]
U_SUP = {0: (Fr(3, 5), Fr(4, 5)), 2: (Fr(5, 13), Fr(12, 13))}


def qsqrt(x):
    a, b = math.isqrt(x.numerator), math.isqrt(x.denominator)
    assert Fr(a * a, b * b) == x
    return Fr(a, b)


def norm(r):
    return qsqrt(r[0] ** 2 + r[1] ** 2)


def dot(u, r):
    return u[0] * r[0] + u[1] * r[1]


def endpoints():
    xm = [dot(U_SUP[i], r) if SUP[i] else -norm(r) for i, r in enumerate(R_ROWS)]
    xp = [dot(U_SUP[i], r) if SUP[i] else norm(r) for i, r in enumerate(R_ROWS)]
    n = len(R_ROWS)
    return sum(xm) / n, sum(xp) / n


def test_theorem_a_every_completion_in_bracket(bound):
    lo, hi = endpoints()
    grid0 = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(-1)), (Fr(3, 5), Fr(4, 5)),
             (Fr(-4, 5), Fr(3, 5)), (Fr(1, 2), Fr(1, 3))]
    uns = [i for i, s in enumerate(SUP) if not s]
    grids = []
    for i in uns:
        nr = norm(R_ROWS[i])
        ext = [] if nr == 0 else [(-R_ROWS[i][0] / nr, -R_ROWS[i][1] / nr),
                                 (R_ROWS[i][0] / nr, R_ROWS[i][1] / nr)]
        grids.append(grid0 + ext)
    vals = set()
    for combo in itertools.product(*grids):
        u = dict(U_SUP)
        u.update(zip(uns, combo))
        assert all(c[0] ** 2 + c[1] ** 2 <= 1 for c in combo)
        vals.add(sum(dot(u[i], r) for i, r in enumerate(R_ROWS)) / len(R_ROWS))
    assert min(vals) == lo and max(vals) == hi  # bound and sharpness
    assert all(lo <= v <= hi for v in vals)


def test_theorem_a_no_gaps_rotation_path(bound):
    lo, hi = endpoints()
    n = len(R_ROWS)
    on_s = sum(dot(U_SUP[i], r) for i, r in enumerate(R_ROWS) if SUP[i]) / n
    off_mass = sum(norm(r) for i, r in enumerate(R_ROWS) if not SUP[i]) / n
    prev = None
    for c, s in [(Fr(1), Fr(0)), (Fr(4, 5), Fr(3, 5)), (Fr(0), Fr(1)),
                 (Fr(-3, 5), Fr(4, 5)), (Fr(-1), Fr(0))]:
        tot = Fr(0)
        for i, r in enumerate(R_ROWS):
            if SUP[i]:
                tot += dot(U_SUP[i], r)
            elif norm(r) != 0:
                v = (-r[0] / norm(r), -r[1] / norm(r))
                tot += dot((c * v[0] - s * v[1], s * v[0] + c * v[1]), r)
        val = tot / n
        assert val == on_s - c * off_mass
        assert prev is None or val > prev
        prev = val
    assert on_s - off_mass == lo and on_s + off_mass == hi


def test_endpoint_arrays_match_exact(bound):
    phi = np.array([math.atan2(float(U_SUP[i][1]), float(U_SUP[i][0])) if SUP[i] else 0.0
                    for i in range(len(R_ROWS))])
    m32 = np.array([[float(r[0]), float(r[1])] for r in R_ROWS])
    a = k4b_scores.endpoint_arrays(phi, np.array(SUP), m32, np.zeros_like(m32))
    for i, r in enumerate(R_ROWS):
        ex = dot(U_SUP[i], r) if SUP[i] else -norm(r)
        assert abs(a["X_minus"][i] - float(ex)) <= 1e-15
        assert abs(a["X_plus"][i] - float(ex if SUP[i] else norm(r))) <= 1e-15
        assert abs(a["r4n"][i] - float(norm(r))) <= 1e-15
    assert np.all(a["X_minus"] <= a["X_plus"])


# ------------------------------------------------------------- Lemma N

@pytest.mark.parametrize("s, D, k", [(Fr(0), D80, 0), (Fr(1, 4), D80, D80 // 2),
                                     (Fr(2), 10, 14), (Fr(1, 10**170), D80, 0),
                                     (Fr(9, 16), 10**3, 750)])
def test_isqrt_bracket_values(bound, s, D, k):
    assert k4b_cert.isqrt_bracket(s, D) == k


@pytest.mark.parametrize("s", [Fr(1, 3), Fr(2), Fr(10**6 + 1, 7), Fr(1, 10**161), Fr(5, 4)])
def test_isqrt_bracket_property(bound, s):
    k = k4b_cert.isqrt_bracket(s)
    assert Fr(k * k, D80 * D80) <= s < Fr((k + 1) ** 2, D80 * D80)


def ref_bn(n_hat, M32, M4, e4, e32):
    r = [Fr(M32[i]) - Fr(M4[i]) for i in (0, 1)]
    s = r[0] ** 2 + r[1] ** 2
    k = math.isqrt(s.numerator * D80 * D80 // s.denominator)
    n = Fr(float(n_hat))
    return max(abs(n - Fr(k, D80)), abs(n - Fr(k + 1, D80))) + Fr(3, 2) * (e4 + e32), r


def within(sq, lo, hi):
    """lo <= sqrt(sq) <= hi, exactly (sq >= 0)."""
    return (lo <= 0 or lo * lo <= sq) and hi >= 0 and sq <= hi * hi


E4, E32 = Fr(1, 10**50), Fr(3, 10**50)
LN_CASES = [
    (0.5, (Decimal("0.3"), Decimal("0.4")), (Decimal(0), Decimal(0))),
    (0.0, (Decimal("0.25"), Decimal("-0.5")), (Decimal("0.25"), Decimal("-0.5"))),
    (1e-85, (Decimal("1E-85"), Decimal(0)), (Decimal(0), Decimal(0))),
    (3.0, (Decimal("0.3"), Decimal("0.4")), (Decimal(0), Decimal(0))),
    (math.hypot(0.1, 0.2), (Decimal("0.1"), Decimal("0.2")), (Decimal(0), Decimal(0))),
    (0.7, (Decimal("0.55"), Decimal("-0.125")), (Decimal("-0.05"), Decimal("0.3"))),
]


@pytest.mark.parametrize("n_hat, M32, M4", LN_CASES)
def test_lemma_n_norm_bound(bound, n_hat, M32, M4):
    got = k4b_cert.norm_bound(n_hat, M32, M4, E4, E32)
    exp, r = ref_bn(n_hat, M32, M4, E4, E32)
    assert got == exp
    n = Fr(float(n_hat))
    for dx, dy in itertools.product((-E4 - E32, Fr(0), E4 + E32), repeat=2):
        rs = (r[0] + dx, r[1] + dy)  # |r~ - r*| <= eps4 + eps32 per coordinate
        assert within(rs[0] ** 2 + rs[1] ** 2, n - got, n + got)


def test_lemma_n_zero_and_square_brackets(bound):
    b0 = k4b_cert.norm_bound(0.0, (Decimal(1), Decimal(2)), (Decimal(1), Decimal(2)), E4, E32)
    assert b0 == Fr(1, D80) + Fr(3, 2) * (E4 + E32)
    b1 = k4b_cert.norm_bound(0.5, (Decimal("0.3"), Decimal("0.4")), (Decimal(0), Decimal(0)),
                             E4, E32)
    assert b1 == Fr(1, D80) + Fr(3, 2) * (E4 + E32)


# ------------------------------------------- cap, B_num, F and F_plan

def test_cap_and_margin(bound):
    cap = Fr(1, 10**4)
    assert k4b_cert.cap_ok(cap) and not k4b_cert.cap_ok(cap + Fr(1, 10**40))
    Z = Fr(cc.CONTRACT["handoff"]["values"]["Z_bound"])
    assert k4b_cert.margin(Fr(1, 10**12), Z) == Fr(1, 10**9) + Z
    assert k4b_cert.margin(Fr(3, 10**9), Z) == Fr(3, 10**9) + Z


def test_f_plan_formula_and_dominance(bound):
    u = Fr(1, 2**53)
    gamma15 = 15 * u / (1 - 15 * u)
    b_const = (1 + Fr(1, 2**30)) * Fr(1, 10**4) + Fr(1, 2**800) + gamma15 * 4 + Fr(1, 2**800)
    Z = Fr(cc.CONTRACT["handoff"]["values"]["Z_bound"])
    fp = k4b_cert.F_plan(Z)
    assert fp == max(b_const, Fr(1, 10**9)) + Z
    assert fp == Fr(cc.CONTRACT["handoff"]["values"]["F_plan"])
    for n in (2, 3072, 6144, 9000, 12288):
        for mb in (Fr(0), Fr(1, 10**15), Fr(1, 10**4)):
            for ma in (0.0, 1.5, 4.0):
                assert k4b_cert.margin(k4b_cert.b_num(mb, ma, n), Z) <= fp


# ------------------------------------------------- decision (K4B §8.1)

def test_decision_boundaries(bound):
    Fs = Fr(1, 10**9)
    L = 0.01 + 1e-9
    r = k4b_stats.model_status(L, 0.05, Fr(L) - M, Fs)
    assert r["status"] == "UNRESOLVED/NUMERICAL"
    assert k4b_stats.model_status(math.nextafter(L, 1.0), 0.05, Fr(L) - M, Fs)["status"] == "SUPPORT"
    U = 0.01 - 1e-9
    assert k4b_stats.model_status(0.0, U, Fs, M - Fr(U))["status"] == "UNRESOLVED/NUMERICAL"
    assert k4b_stats.model_status(0.0, math.nextafter(U, 0.0), Fs, M - Fr(U))["status"] == "EXCLUDE"
    Ln = -0.01 + 1e-9
    assert k4b_stats.model_status(Ln, 0.0, Fr(Ln) + M, Fs)["status"] == "UNRESOLVED/NUMERICAL"
    Un = -0.01 - 1e-9
    r = k4b_stats.model_status(-0.05, Un, Fs, -M - Fr(Un))
    assert "NEGATIVE_ALIGNMENT" not in r["labels"]
    r = k4b_stats.model_status(-0.05, math.nextafter(Un, -1.0), Fs, -M - Fr(Un))
    assert "NEGATIVE_ALIGNMENT" in r["labels"]
    rnd = np.random.default_rng(84)
    for _ in range(300):
        a, b = sorted(rnd.uniform(-0.03, 0.03, 2))
        st = k4b_stats.model_status(float(a), float(b), Fs, Fs)["status"]
        assert not (st == "SUPPORT" and Fr(float(b)) + Fs < M)
        assert (st == "SUPPORT") == (Fr(float(a)) - Fs > M)
    per = dict(zip(STAGE_C, ("SUPPORT", "EXCLUDE", "UNRESOLVED")))
    assert k4b_stats.overall(per) == "MIXED"
    assert k4b_stats.overall(dict.fromkeys(STAGE_C, "EXCLUDE")) == "EXCLUSION"
    assert k4b_stats.overall(dict.fromkeys(STAGE_C, "SUPPORT")) == "SUPPORT"


# ------------------------------------------------------------------ ranks

def test_ranks(bound):
    ps = (c1_means.P_THIRD, 1 - c1_means.P_THIRD, 0.05, 0.025, 0.975)
    want = [math.ceil(5000 * Fr(p) if isinstance(p, Fr) else 5000 * Fr(str(p))) for p in ps]
    assert want == [84, 4917, 250, 125, 4875]
    assert [c1_means.rank_for(p) for p in ps] == want
    assert dict(k4b_config.RANKS) == dict(cc.RANKS) == cc.CONTRACT["thresholds"]["ranks"]


def test_bounds_ranks_on_bound_endpoint_seed(bound):
    rng = np.random.default_rng(4917)
    x = rng.standard_normal(257)
    arrays = {"X:620301:-": x, "X:620301:+": x + np.abs(rng.standard_normal(257))}
    d = k4b_stats.joint_bootstrap(arrays, k4b_config.SEEDS["endpoint"])
    ref = c1_means.bootstrap_means(arrays, 620313, 5000)
    for k in arrays:
        assert np.array_equal(d[k], ref[k])
    dm, dp = np.sort(d["X:620301:-"]), np.sort(d["X:620301:+"])
    assert len(set(dm)) == 5000 and len(set(dp)) == 5000
    b = k4b_stats.bounds(d["X:620301:-"], d["X:620301:+"])

    def val(v):
        return v[0] if isinstance(v, tuple) else v

    assert val(b["L"]) == dm[83] and val(b["U"]) == dp[4916]
    assert b["L_rank"] == 84 and b["U_rank"] == 4917
    (lo, klo), (hi, khi) = b["central95_minus"]
    assert (lo, klo, hi, khi) == (dm[124], 125, dm[4874], 4875)
    (lo, klo), (hi, khi) = b["central95_plus"]
    assert (lo, hi) == (dp[124], dp[4874])
    v, k = c1_means.quantile_with_rank(d["X:620301:-"], 0.05)
    assert (v, k) == (dm[249], 250)


# ------------------------------------------- sealing, chart cfg, restoration

def test_write_sealed_stage_c_protocol(bound, tmp_path):
    proto = hashlib.sha256(cc.PROTOCOL_PATH.read_bytes()).hexdigest()
    assert proto == cc.CONTRACT["protocol_sha256"]
    rng = np.random.default_rng(3)
    xm = {j: rng.standard_normal(64) for j in STAGE_C}
    xp = {j: xm[j] + 0.1 for j in STAGE_C}
    sha = k4b_stats.write_sealed(tmp_path, {"mean_X_minus": xm, "mean_X_plus": xp})
    f = tmp_path / k4b_stats.SEALED_FILE
    raw = f.read_bytes()
    assert sha == hashlib.sha256(raw).hexdigest()
    rec = json.loads(raw)
    assert rec["protocol_sha256"] == proto
    for j in STAGE_C:
        assert rec["means"]["mean_X_minus"][str(j)] == float(c1_means.tree_mean(xm[j]))
        assert rec["means"]["mean_X_plus"][str(j)] == float(c1_means.tree_mean(xp[j]))
    with pytest.raises(Exception):
        k4b_stats.write_sealed(tmp_path, {"mean_X_minus": xm})
    assert f.read_bytes() == raw


def test_chart_equality_inside_binding(bound):
    r = k4b_config.check_chart_equality()
    assert r["equal"] and r["giant_equal"] and r["val_support_equal"]
    assert list(r["cfg_diff"]) == []


def test_binding_restored_after_exit():
    before = (k4b_config.MODELS, k4b_config.SEEDS, k4b_stats.MODELS, k4b_config.CONTRACT)
    assert before[0] == K4B_MODELS
    with cb.bound_stage_c():
        assert k4b_config.MODELS == STAGE_C
        assert k4b_config.CONTRACT["protocol_sha256"] == cc.CONTRACT["protocol_sha256"]
    assert k4b_config.MODELS == K4B_MODELS
    after = (k4b_config.MODELS, k4b_config.SEEDS, k4b_stats.MODELS, k4b_config.CONTRACT)
    assert all(a is b for a, b in zip(after, before))
