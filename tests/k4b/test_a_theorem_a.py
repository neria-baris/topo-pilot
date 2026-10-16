"""K4b author A, TEST_PLAN A2 (protocol §1.4, §11.4): Theorem A on the Proposition-1 HMM.

The same tiny asymmetric stationary HMM (L = 6, K = 2) is enumerated exactly. m_L plays m32
and m_K plays m4; r = m_L - m_K. The support set S depends on the prefix w1 and on the residual
sign. Norms are irrational, so |r| is bracketed by integers: k = isqrt(a D^2 // b), D = 10^40,
k/D <= |r| < (k+1)/D. Every pointwise comparison is exact (squares). Row construction of X-
and X+ is checked against k4b_scores.endpoint_arrays."""

from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
             "tools/x4_circle_history", "tools/x4_oracle_profile"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

S, V, L, K = 3, 3, 6, 2
D = 10 ** 40
T = ((Fr(1, 2), Fr(1, 3), Fr(1, 6)),
     (Fr(1, 5), Fr(1, 2), Fr(3, 10)),
     (Fr(2, 5), Fr(1, 10), Fr(1, 2)))
E = ((Fr(7, 10), Fr(1, 5), Fr(1, 10)),
     (Fr(1, 5), Fr(3, 5), Fr(1, 5)),
     (Fr(1, 10), Fr(3, 10), Fr(3, 5)))
C = ((Fr(1), Fr(0)), (Fr(-3, 5), Fr(4, 5)), (Fr(-3, 5), Fr(-4, 5)))
UNITS = ((Fr(1), Fr(0)), (Fr(3, 5), Fr(4, 5)), (Fr(0), Fr(1)), (Fr(-5, 13), Fr(12, 13)))
GRID = tuple((Fr(a, 4), Fr(b, 4)) for a in range(-4, 5) for b in range(-4, 5)
             if a * a + b * b <= 16)
E1 = (Fr(1), Fr(0))


def stationary(Tm):
    n = len(Tm)
    M = [[Tm[s][t] - (1 if s == t else 0) for s in range(n)] + [Fr(0)] for t in range(n)]
    M[-1] = [Fr(1)] * n + [Fr(1)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return tuple(M[i][n] / M[i][i] for i in range(n))


PI = stationary(T)


def forward(start, obs):
    a = [start[z] * E[z][obs[0]] for z in range(S)]
    for w in obs[1:]:
        a = [sum(a[z] * T[z][y] for z in range(S)) * E[y][w] for y in range(S)]
    return a


def mean_of(a):
    tot = sum(a)
    return (sum(a[z] * C[z][0] for z in range(S)) / tot,
            sum(a[z] * C[z][1] for z in range(S)) / tot)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def in_support(w, r):
    """Correlated with the prefix (w1) and with the residual sign."""
    return (w[0] in (0, 1) and r[0] >= 0) or (w[0] == 2 and r[1] < 0)


@lru_cache(maxsize=None)
def rows():
    out = []
    for w in product(range(V), repeat=L):
        a = forward(PI, w)
        mL, mK = mean_of(a), mean_of(forward(PI, w[L - K:]))
        r = (mL[0] - mK[0], mL[1] - mK[1])
        s = dot(r, r)
        k = math.isqrt(s.numerator * D * D // s.denominator)
        out.append({"w": w, "p": sum(a), "alpha": tuple(a), "mL": mL, "mK": mK, "r": r,
                    "s": s, "lo": Fr(k, D), "hi": Fr(k + 1, D), "k": k,
                    "A": in_support(w, r), "u": UNITS[(w[0] + w[-1]) % 4]})
    return tuple(out)


def endpoints(sup=None, field=None):
    """Brackets of E X- and E X+: (EXm_lo, EXm_hi, EXp_lo, EXp_hi, supported part)."""
    sup = sup or (lambda row: row["A"])
    field = field or (lambda row: row["u"])
    part = sum(x["p"] * dot(field(x), x["r"]) for x in rows() if sup(x))
    m_lo = sum(x["p"] * x["lo"] for x in rows() if not sup(x))
    m_hi = sum(x["p"] * x["hi"] for x in rows() if not sup(x))
    return part - m_hi, part - m_lo, part + m_lo, part + m_hi, part


def delta(completion):
    """Delta4(u~) = E[u~ . r] over the joint law of (w, z_L); u~ = u on S."""
    tot = Fr(0)
    for x in rows():
        for z in range(S):
            v = x["u"] if x["A"] else completion(x, z)
            tot += x["alpha"][z] * dot(v, x["r"])
    return tot


def pointwise_ok(completion):
    for x in rows():
        if x["A"]:
            continue
        for z in range(S):
            v = completion(x, z)
            if dot(v, v) > 1 or dot(v, x["r"]) ** 2 > x["s"]:
                return False
    return True


def test_support_is_mixed_and_prefix_correlated():
    rs = rows()
    assert sum(x["p"] for x in rs) == 1
    assert any(x["A"] for x in rs) and any(not x["A"] for x in rs)
    by_suffix = {}
    for x in rs:
        by_suffix.setdefault(x["w"][L - K:], set()).add(x["A"])
    assert any(len(v) == 2 for v in by_suffix.values())  # S is not a suffix event
    assert all(dot(u, u) == 1 for u in UNITS)
    assert all(x["lo"] ** 2 <= x["s"] < x["hi"] ** 2 for x in rs)


def test_grid_completions_lie_in_bounds():
    m_lo, m_hi, p_lo, p_hi, _ = endpoints()
    assert m_hi < p_lo
    fams = [lambda x, z, v=v: v for v in GRID]
    fams.append(lambda x, z: GRID[(7 * sum(x["w"]) + x["w"][0]) % len(GRID)])  # history
    fams.append(lambda x, z: UNITS[z])  # hidden-path dependent
    fams.append(lambda x, z: UNITS[(z + x["w"][1]) % 4])
    for comp in fams:
        assert pointwise_ok(comp)
        d = delta(comp)
        assert m_hi <= d <= p_lo


def test_randomised_completion_lies_in_bounds():
    """Auxiliary randomness w': u~ = v1 w.p. 1/3 and v2 w.p. 2/3 (Fubini)."""
    m_lo, m_hi, p_lo, p_hi, _ = endpoints()
    v1, v2 = (Fr(-3, 5), Fr(4, 5)), (Fr(12, 13), Fr(-5, 13))
    d = delta(lambda x, z: v1) / 3 + 2 * delta(lambda x, z: v2) / 3
    assert m_hi <= d <= p_lo
    mix = lambda x, z: (v1[0] / 3 + 2 * v2[0] / 3, v1[1] / 3 + 2 * v2[1] / 3)  # noqa: E731
    assert pointwise_ok(mix) and delta(mix) == d


def scaled(sign, c=Fr(1)):
    """u~ = sign * c * r * D / (k+1) on S^c: |u~| < 1, and u~ . r = sign * c * s D / (k+1)."""
    return lambda x, z: (sign * c * x["r"][0] * D / (x["k"] + 1),
                         sign * c * x["r"][1] * D / (x["k"] + 1))


def test_sharpness_extremal_completions():
    m_lo, m_hi, p_lo, p_hi, _ = endpoints()
    up, dn = scaled(1), scaled(-1)
    assert pointwise_ok(up) and pointwise_ok(dn)
    d_up, d_dn = delta(up), delta(dn)
    assert p_lo - Fr(1, D) <= d_up <= p_hi
    assert m_lo <= d_dn <= m_hi + Fr(1, D)
    for v in GRID:  # the extremal completions dominate every grid completion
        dv = delta(lambda x, z, v=v: v)
        assert d_dn - Fr(1, D) <= dv <= d_up + Fr(1, D)


def test_continuity_path_exact_affine_family():
    m_lo, m_hi, p_lo, p_hi, part = endpoints()
    W = sum(x["p"] * x["s"] * D / (x["k"] + 1) for x in rows() if not x["A"])
    cs = [Fr(1), Fr(3, 4), Fr(1, 3), Fr(0), Fr(-1, 2), Fr(-1)]
    vals = [delta(scaled(-1, c)) for c in cs]
    assert vals == [part - c * W for c in cs]
    assert all(a < b for a, b in zip(vals, vals[1:]))
    assert abs(vals[0] - m_lo) <= Fr(2, D) and abs(vals[-1] - p_hi) <= Fr(2, D)
    for t in (Fr(1, 10), Fr(1, 2), Fr(9, 10)):  # no gaps: hit interior targets exactly
        target = (m_hi + Fr(2, D)) + t * ((p_lo - Fr(2, D)) - (m_hi + Fr(2, D)))
        c = (part - target) / W
        assert -1 <= c <= 1
        comp = scaled(-1, c)
        assert pointwise_ok(comp) and delta(comp) == target


def test_continuity_path_unit_rotation_float():
    """u~_theta = R_theta(-r/|r|): E[u~ . r] = E[X- 1_S] - cos(theta) E[|r| 1_{S^c}]."""
    rs = rows()
    p = np.array([float(x["p"]) for x in rs])
    r = np.array([[float(x["r"][0]), float(x["r"][1])] for x in rs])
    A = np.array([x["A"] for x in rs])
    part = float(sum(x["p"] * dot(x["u"], x["r"]) for x in rs if x["A"]))
    nr = np.sqrt(np.sum(r * r, axis=1))
    miss = float(np.sum(p[~A] * nr[~A]))
    m_lo, m_hi, p_lo, p_hi, _ = endpoints()
    for th in np.linspace(0.0, np.pi, 9):
        c, s = np.cos(th), np.sin(th)
        base = -r[~A] / nr[~A, None]
        ut = np.column_stack((c * base[:, 0] - s * base[:, 1], s * base[:, 0] + c * base[:, 1]))
        assert np.allclose(np.sum(ut * ut, axis=1), 1.0, atol=1e-14)
        val = part + float(np.sum(p[~A] * np.sum(ut * r[~A], axis=1)))
        assert abs(val - (part - c * miss)) < 1e-13
    assert abs((part - miss) - float(m_lo)) < 1e-13
    assert abs((part + miss) - float(p_hi)) < 1e-13
    target = 0.3 * float(m_lo) + 0.7 * float(p_hi)
    th = math.acos((part - target) / miss)
    assert 0.0 <= th <= math.pi
    assert abs((part - math.cos(th) * miss) - target) < 1e-13


def test_conditioning_on_support_is_spurious_but_bounds_hold():
    """u = e1 on S' (a suffix-only field). Delta4(e1) = 0 exactly (Proposition 1), yet the
    S'-conditional mean and the supported contribution are positive; [E X-, E X+] still
    contains 0 (Corollary A1)."""
    rs = rows()
    sup = lambda x: x["r"][0] > 0 and x["w"][0] != 2  # noqa: E731
    field = lambda x: E1  # noqa: E731
    assert sum(x["p"] * x["r"][0] for x in rs) == 0
    mass = sum(x["p"] for x in rs if sup(x))
    contrib = sum(x["p"] * x["r"][0] for x in rs if sup(x))
    assert mass > 0 and contrib > 0 and contrib / mass > 0
    m_lo, m_hi, p_lo, p_hi, part = endpoints(sup, field)
    assert part == contrib
    assert m_hi < 0 < p_lo


def test_endpoint_arrays_row_construction():
    import k4b_scores
    import scores

    rs = rows()
    A = np.array([x["A"] for x in rs], dtype=bool)
    m32 = np.array([[float(x["mL"][0]), float(x["mL"][1])] for x in rs])
    m4 = np.array([[float(x["mK"][0]), float(x["mK"][1])] for x in rs])
    ang = np.array([math.atan2(float(x["u"][1]), float(x["u"][0])) for x in rs])
    rng = np.random.default_rng(5)
    phi = np.where(A, np.mod(ang, 2 * np.pi), rng.uniform(0.0, 6.0, len(rs)))
    out = k4b_scores.endpoint_arrays(phi, A, m32, m4)
    xm, xp, r4n = (np.asarray(out[k]) for k in ("X_minus", "X_plus", "r4n"))
    assert np.array_equal(r4n, scores.r4_norms(m32, m4))
    assert np.all(xm <= xp)
    ph = scores.scores(scores.unit_vectors(phi), m32, m4)
    assert np.array_equal(xm[A], xp[A]) and np.array_equal(xm[A], ph[A])
    assert np.array_equal(xm[~A], -r4n[~A]) and np.array_equal(xp[~A], r4n[~A])
    exact = np.array([float(dot(x["u"], x["r"])) for x in rs])
    assert np.allclose(xm[A], exact[A], atol=1e-14, rtol=0)
    p = np.array([float(x["p"]) for x in rs])
    m_lo, m_hi, p_lo, p_hi, _ = endpoints()
    assert abs(float(np.sum(p * xm)) - float(m_lo)) < 1e-13
    assert abs(float(np.sum(p * xp)) - float(p_hi)) < 1e-13
    phi2 = np.where(A, phi, np.mod(phi + 1.234, 2 * np.pi))
    out2 = k4b_scores.endpoint_arrays(phi2, A, m32, m4)
    for key in ("X_minus", "X_plus", "r4n"):
        assert np.array_equal(np.asarray(out2[key]), np.asarray(out[key]))
    r = m32 - m4
    for v in GRID:  # every completion is bracketed rowwise (float, 1e-15 slack)
        val = r[~A] @ np.array([float(v[0]), float(v[1])])
        assert np.all(xm[~A] - 1e-15 <= val) and np.all(val <= xp[~A] + 1e-15)
