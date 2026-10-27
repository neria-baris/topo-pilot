"""Author A (job 0119): identities on a tiny rational HMM by exact enumeration (TEST_PLAN §2).

Protocol §2.2 I1-I4, §2.3 (KL rows, row-wise Pinsker), §2.4 Proposition F, DR1. The world is
written here: a 6 x 2 cylinder (N = 12, state z = 2x + y), dyadic T and E, the anchored (6, 2)
labels with n_axial = 2 (V' = 4), L = 6, Ks = (1, 2, 4). Rational parts are exact Fractions.
The feature sin(2 pi x / 6) is sqrt(3) times a rational, so every m_K is held as (a, c) meaning
(a, sqrt(3) c) and every inner product is rational. Identities with logarithms reduce to the
tower property (checked exactly on integers) and are evaluated in Decimal at 40 digits.
Expected values never come from the functions under test.
"""

import itertools
import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
HWS_DIR = str(REPO / "tools" / "hws")
if HWS_DIR not in sys.path:
    sys.path.insert(0, HWS_DIR)

import hws_worlds as hw  # noqa: E402
import hws_oracle as ho  # noqa: E402
import hws_exact as he  # noqa: E402
from topo_pilot.oracle import context_gain  # noqa: E402

W, HH, N, V, NAX, L, KS = 6, 2, 12, 4, 2, 6, (1, 2, 4)
LABELS = (0, 1, 1)  # anchored_labels(6, 2): groups {0}, {1, 2}
SIZES = (1, 1, 2, 2)  # centres merged into v = 2g + b
C2 = (2, 1, -1, -2, -1, 1)  # 2 cos(2 pi x / 6)
S2 = (0, 1, 1, 0, -1, -1)  # 2 sin(2 pi x / 6) / sqrt(3)
# 16 * E_centres; row z = 2x + y; column j = 2i + b (centre i at x = 0.5 + 2i, axial b)
EC16 = (
    (6, 2, 1, 1, 4, 2), (2, 5, 1, 2, 2, 4), (5, 2, 4, 1, 3, 1), (2, 4, 1, 5, 1, 3),
    (2, 1, 7, 2, 3, 1), (1, 3, 2, 6, 1, 3), (1, 1, 5, 2, 6, 1), (1, 2, 1, 4, 2, 6),
    (3, 1, 1, 1, 8, 2), (1, 3, 1, 1, 3, 7), (5, 1, 2, 1, 6, 1), (2, 4, 1, 2, 1, 6),
)
TOL_DEC = Decimal("1e-24")  # sums run at 40 digits; test-side arithmetic at the default 28


def _t8():
    """8 * T: stay 4/8, x-neighbours 1/8 each (periodic), y-neighbour 2/8. Symmetric."""
    t = [[0] * N for _ in range(N)]
    for x, y in itertools.product(range(W), range(HH)):
        z = HH * x + y
        t[z][z] += 4
        t[z][HH * ((x + 1) % W) + y] += 1
        t[z][HH * ((x - 1) % W) + y] += 1
        t[z][HH * x + (1 - y)] += 2
    return t


def _e16():
    """16 * E' with E'[:, 2g + b] = sum over i with g(i) = g of E_centres[:, 2i + b]."""
    return [[sum(row[NAX * i + b] for i in range(W // 2) if LABELS[i] == g)
             for g in range(V // NAX) for b in range(NAX)] for row in EC16]


T8, E16 = _t8(), _e16()


def _dec(f):
    return Decimal(f.numerator) / Decimal(f.denominator)


def _den(t):
    return N * 16**t * 8 ** (t - 1)


def _kget(d, k):
    """API-AMBIGUITY: dicts 'D[K]' may be keyed by int K or by str(K)."""
    return d[k] if k in d else d[str(k)]


@lru_cache(maxsize=1)
def _proc():
    from topo_pilot.world.config import WorldConfig
    from topo_pilot.world.registry import build_world

    coords = np.column_stack((np.repeat(np.arange(W), HH), np.tile(np.arange(HH), W))) * 1.0
    a = 2.0 * np.pi * coords[:, 0] / W
    return {
        "key": "TINY-RATIONAL-W6", "world_key": hw.World(W, 2, Fraction(1), Fraction(1, 2)),
        "W": W, "q": 2, "sigma": Fraction(1), "p": Fraction(1, 2), "tier": 0,
        "world": build_world(WorldConfig("cylinder", (W, HH), "flat")),
        "T": np.array(T8, dtype=np.float64) / 8.0, "pi": np.full(N, 1.0 / N),
        "E_centres": np.array(EC16, dtype=np.float64) / 16.0,
        "E": np.array(E16, dtype=np.float64) / 16.0,
        "labels": np.array(LABELS, dtype=np.int64), "sizes": np.array(SIZES, dtype=np.int64),
        "V": V, "N": N, "n_axial": NAX, "Hh": HH, "H": HH, "coords": coords,
        "features": np.column_stack((np.cos(a), np.sin(a))), "e1": {"status": "PASS"},
    }


def _dot(m, r):
    return m[0] * r[0] + 3 * m[1] * r[1]


def _norm2(m):
    return _dot(m, m)


@lru_cache(maxsize=1)
def _exact():  # noqa: C901 (one enumeration pass, kept together)
    tn = [[(u, T8[u][z]) for u in range(N) if T8[u][z]] for z in range(N)]
    te = [[sum(T8[z][u] * E16[u][v] for u in range(N)) for v in range(V)] for z in range(N)]
    stat = [Fraction(sum(E16[z][v] for z in range(N)), 16 * N) for v in range(V)]
    alpha, sfx, lncache = {}, {}, {}

    def fwd(seq):
        if seq not in alpha:
            if len(seq) == 1:
                alpha[seq] = tuple(E16[z][seq[0]] for z in range(N))
            else:
                prev, w = fwd(seq[:-1]), seq[-1]
                alpha[seq] = tuple(sum(prev[u] * t for u, t in tn[z]) * E16[z][w]
                                   for z in range(N))
        return alpha[seq]

    def summ(seq):
        a = fwd(seq)
        tot = sum(a)
        m = (Fraction(sum(a[z] * C2[z // HH] for z in range(N)), 2 * tot),
             Fraction(sum(a[z] * S2[z // HH] for z in range(N)), 2 * tot))
        q = [Fraction(sum(a[z] * te[z][v] for z in range(N)), tot * 128) for v in range(V)]
        return {"P": Fraction(tot, _den(len(seq))), "b": [Fraction(x, tot) for x in a],
                "bx": [Fraction(a[HH * x] + a[HH * x + 1], tot) for x in range(W)],
                "m": m, "q": q, "qA": [sum(q[NAX * g:NAX * g + NAX]) for g in range(V // NAX)]}

    def suffix(seq):
        return sfx[seq] if seq in sfx else sfx.setdefault(seq, summ(seq))

    def ln(f):
        return lncache[f] if f in lncache else lncache.setdefault(f, _dec(f).ln())

    def kl(p, q):
        return sum((_dec(a) * (ln(a) - ln(b)) for a, b in zip(p, q) if a), Decimal(0))

    def ent(p):
        return -sum((_dec(a) * ln(a) for a in p if a), Decimal(0))

    rng = np.random.default_rng(119001)
    gtab = {K: rng.integers(-3, 4, size=(3, V**K)).tolist() for K in KS}
    f3 = rng.integers(1, 6, size=(V**4, V)).tolist()
    preds = {"uniform": lambda s: [Fraction(1, V)] * V, "stationary": lambda s: stat,
             "random": lambda s: [Fraction(x, sum(f3[_idx(s)])) for x in f3[_idx(s)]]}
    z0 = (Fraction(0), Fraction(0))
    res = {"P": [], "V": {K: Fraction(0) for K in KS}, "EmK2": {K: Fraction(0) for K in KS},
           "EmL2": Fraction(0), "I1": {K: [z0] * 3 for K in KS}, "orth": dict.fromkeys(KS, 0),
           "w1": {K: [z0] * V for K in KS}, "I4_fail": 0, "pinsker_exact_fail": 0,
           "tower_fail": 0, "rows": {}}
    rows = {"D": {K: [] for K in KS}, "rn": {K: [] for K in KS}, "G": {K: [] for K in KS},
            "G4A": [], "IZ4": [], "IX4": [], "G0": [], "mL": [], "orth": {K: [] for K in KS}}
    dsum = {k: {K: Decimal(0) for K in KS} for k in ("D", "B", "G", "EHq")}
    dsc = dict.fromkeys("EHqL G4A IZ4 IX4 Hb4 HbL Hbx4 HbxL HqA4 HqAL".split(), Decimal(0))
    pf = {name: [Decimal(0), Decimal(0)] for name in preds}
    tower = {K: {} for K in KS}
    min_slack = None
    with localcontext() as ctx:
        ctx.prec = 40
        hists = list(itertools.product(range(V), repeat=L))
        for h in hists:
            f = summ(h)
            P, mL, dP = f["P"], f["m"], _dec(f["P"])
            res["P"].append(P)
            res["EmL2"] += P * _norm2(mL)
            dsc["EHqL"] += dP * ent(f["q"])
            rows["mL"].append((float(mL[0]), math.sqrt(3.0) * float(mL[1])))
            for K in KS:
                s = h[L - K:]
                g = suffix(s)
                acc = tower[K].setdefault(s, [0] * N)
                for z, x in enumerate(alpha[h]):
                    acc[z] += x
                mK = g["m"]
                r = (mL[0] - mK[0], mL[1] - mK[1])
                nr2 = _norm2(r)
                res["V"][K] += P * nr2
                res["EmK2"][K] += P * _norm2(mK)
                for j in range(3):
                    gv = gtab[K][j][_idx(s)]
                    old = res["I1"][K][j]
                    res["I1"][K][j] = (old[0] + P * gv * r[0], old[1] + P * gv * r[1])
                old = res["w1"][K][h[0]]
                res["w1"][K][h[0]] = (old[0] + P * r[0], old[1] + P * r[1])
                res["orth"][K] += P * _dot(mK, r)
                rows["orth"][K].append(float(_dot(mK, r)))
                n2 = _norm2(mL)
                if n2 == 0:
                    dm, ok, drow = r[0], True, _dec(r[0])
                else:
                    dm = _dot(mL, r)
                    ok = dm <= 0 or dm * dm <= n2 * nr2
                    drow = _dec(dm) / _dec(n2).sqrt()
                res["I4_fail"] += not ok
                rn = _dec(nr2).sqrt()
                grow = kl(f["q"], g["q"])
                if "Hq" not in g:
                    g["Hq"] = ent(g["q"])
                for key, val in (("D", drow), ("B", rn), ("G", grow), ("EHq", g["Hq"])):
                    dsum[key][K] += dP * val
                for key, val in (("D", drow), ("rn", rn), ("G", grow)):
                    rows[key][K].append(float(val))
            g4 = suffix(h[L - 4:])
            r4 = (mL[0] - g4["m"][0], mL[1] - g4["m"][1])
            ga, iz, ix = kl(f["qA"], g4["qA"]), kl(f["b"], g4["b"]), kl(f["bx"], g4["bx"])
            for key, val in (("G4A", ga), ("IZ4", iz), ("IX4", ix)):
                dsc[key] += dP * val
                rows[key].append(float(val))
            rows["G0"].append(float(kl(f["q"], stat)))
            for key, p4, pl in (("b", "Hb4", "HbL"), ("bx", "Hbx4", "HbxL"),
                                ("qA", "HqA4", "HqAL")):
                dsc[p4] += dP * ent(g4[key])
                dsc[pl] += dP * ent(f[key])
            slack = 2 * ix - _dec(_norm2(r4))
            min_slack = slack if min_slack is None else min(min_slack, slack)
            l1 = sum(abs(a - b) for a, b in zip(f["bx"], g4["bx"]))
            res["pinsker_exact_fail"] += not _norm2(r4) <= l1 * l1
            for name, fn in preds.items():
                fv = fn(h[L - 4:])
                pf[name][0] += dP * kl(f["q"], fv)
                pf[name][1] += dP * kl(g4["q"], fv)
        for K in KS:
            for s, acc in tower[K].items():
                res["tower_fail"] += any(acc[z] * _den(K) != alpha[s][z] * _den(L)
                                         for z in range(N))
    res.update(hists=np.array(hists, dtype=np.int64), dsum=dsum, dsc=dsc, propF=pf,
               min_slack=min_slack)
    res["rows"] = {k: ({K: np.array(x) for K, x in v.items()} if isinstance(v, dict)
                       else np.array(v)) for k, v in rows.items()}
    return res


def _flags(obj):
    """Every nested {"value", "pass"} record of a result dict."""
    if not isinstance(obj, dict):
        return []
    return [obj] if "pass" in obj else [f for v in obj.values() for f in _flags(v)]


def _idx(s):
    return int("".join(str(w) for w in s), V)  # base-V index of a suffix


def test_fixture_is_a_valid_rational_process():
    assert all(sum(r) == 8 for r in T8) and np.array_equal(np.array(T8), np.array(T8).T)
    assert all(sum(r) == 16 and min(r) > 0 for r in E16)
    ex = _exact()
    assert sum(ex["P"]) == 1 and len(ex["P"]) == V**L == 4096
    assert ex["tower_fail"] == 0  # b_K = E[b_L | S_K] exactly, K in {1, 2, 4}


def test_i1_suffix_functions_have_zero_covariance_with_r_k():
    ex = _exact()
    for K in KS:
        assert all(pair == (0, 0) for pair in ex["I1"][K]), K  # three random tables g
        assert ex["orth"][K] == 0  # g = m_K: E<m_K, r_K> = 0 (the orth_K null)


def test_i1_fails_for_a_prefix_dependent_function():
    ex = _exact()
    assert any(pair != (0, 0) for K in KS for pair in ex["w1"][K])  # g = 1{w1 = v}
    for K in KS:  # g = m_L: E<m_L, r_K> = V_K > 0
        assert ex["EmL2"] - ex["EmK2"][K] > 0


def test_i3_v_k_identity_and_monotone():
    ex = _exact()
    for K in KS:
        assert ex["V"][K] == ex["EmL2"] - ex["EmK2"][K]
    assert ex["V"][1] >= ex["V"][2] >= ex["V"][4] > 0


def test_i2_i4_and_d4_positive():
    ex = _exact()
    assert ex["I4_fail"] == 0  # row-wise v32 . r_K <= ||r_K||, decided on rationals
    D, B = ex["dsum"]["D"], ex["dsum"]["B"]
    assert D[4] > Decimal("1e-20")  # DR1: D4 > 0 on the broken-symmetry world
    for K in KS:
        assert Decimal(0) <= D[K] <= B[K]
        assert B[K] * B[K] <= _dec(ex["V"][K]) + TOL_DEC  # B_K <= sqrt(V_K)


def test_gain_identities_kl_rows_equal_entropy_differences():
    ex = _exact()
    d, s = ex["dsum"], ex["dsc"]
    for K in KS:
        assert abs(d["G"][K] - (d["EHq"][K] - s["EHqL"])) < TOL_DEC
        assert d["G"][K] > 0
    assert abs(s["G4A"] - (s["HqA4"] - s["HqAL"])) < TOL_DEC
    assert abs(s["IZ4"] - (s["Hb4"] - s["HbL"])) < TOL_DEC  # I_Z(4)
    assert abs(s["IX4"] - (s["Hbx4"] - s["HbxL"])) < TOL_DEC  # I^x_4
    assert Decimal(0) < s["IX4"] <= s["IZ4"] + TOL_DEC
    assert _dec(ex["V"][4]) <= 2 * s["IX4"] + TOL_DEC  # V4 <= 2 I^x_4 (population)


def test_proposition_f_for_three_suffix_predictors():
    ex = _exact()
    g4 = ex["dsum"]["G"][4]
    for name, (lhs, extra) in ex["propF"].items():
        assert abs(lhs - (g4 + extra)) < TOL_DEC, name
        assert lhs >= g4 - TOL_DEC and extra >= 0


def test_rowwise_pinsker():
    ex = _exact()
    assert ex["pinsker_exact_fail"] == 0  # ||r4||^2 <= ||b_L^x - b_4^x||_1^2, exact
    assert ex["min_slack"] >= -TOL_DEC  # ||r4||^2 <= 2 KL(b_L^x || b_4^x), every row


def test_enumerate_histories_order_and_probabilities():
    ex = _exact()
    hist, prob = he.enumerate_histories(_proc(), L)
    assert np.asarray(hist).shape == (V**L, L)
    assert np.array_equal(np.asarray(hist, dtype=np.int64), ex["hists"])
    ref = np.array([float(p) for p in ex["P"]])
    assert np.asarray(prob).dtype == np.float64
    assert np.max(np.abs(np.asarray(prob) - ref)) <= 1e-15
    assert abs(float(np.sum(prob)) - 1.0) <= 1e-12


def test_exact_expectations_matches_the_fraction_values():
    ex = _exact()
    got = he.exact_expectations(_proc(), L, KS)
    d, s = ex["dsum"], ex["dsc"]
    for K in KS:
        assert abs(float(_kget(got["D"], K)) - float(d["D"][K])) <= 1e-12
        assert abs(float(_kget(got["B"], K)) - float(d["B"][K])) <= 1e-12
        assert abs(float(_kget(got["V"], K)) - float(ex["V"][K])) <= 1e-12
        assert abs(float(_kget(got["G"], K)) - float(d["G"][K])) <= 1e-12
    for key in ("G4A", "IZ4", "IX4"):
        assert abs(float(got[key]) - float(s[key])) <= 1e-12, key
    # API-AMBIGUITY: the identity-check key names are not fixed by API.md; every
    # {"value", "pass"} entry (I1, I2, I3, I4, Proposition F, Pinsker) must pass.
    flags = _flags(got)
    assert len(flags) >= 6
    assert all(bool(v["pass"]) for v in flags)


def test_row_arrays_on_every_history():
    ex = _exact()
    rows = ho.row_arrays(_proc(), ex["hists"].astype(np.uint8), KS)
    ref = ex["rows"]
    for K in KS:
        for key in ("D", "rn", "G"):
            got = np.asarray(_kget(rows[key], K))
            assert got.shape == (V**L,) and got.dtype == np.float64
            assert np.max(np.abs(got - ref[key][K])) <= 1e-12, (key, K)
        orth = np.asarray(rows["nulls"]["orth_%d" % K])
        assert np.max(np.abs(orth - ref["orth"][K])) <= 1e-12
    for key in ("G4A", "IZ4", "IX4", "G0"):
        assert np.max(np.abs(np.asarray(rows[key]) - ref[key])) <= 1e-12, key
    assert np.max(np.abs(np.asarray(_kget(rows["m"], L)) - ref["mL"])) <= 1e-12
    slack = np.asarray(rows["pinsker_slack"])
    assert np.max(np.abs(slack - (2 * ref["IX4"] - ref["rn"][4] ** 2))) <= 1e-12
    assert np.min(slack) >= -1e-12


def test_kl_rows_zero_support_convention_and_entropy_rows():
    p = np.array([[0.5, 0.5, 0.0], [0.0, 0.0, 1.0]])
    q = np.array([[0.25, 0.25, 0.5], [0.0, 0.5, 0.5]])  # q = 0 only where p = 0
    got = np.asarray(ho.kl_rows(p, q))
    assert got.shape == (2,)
    assert np.max(np.abs(got - math.log(2.0))) <= 1e-15
    p = np.array([[0.5, 0.5, 0.0], [1.0, 0.0, 0.0], [1 / 3, 1 / 3, 1 / 3]])
    ref = np.array([math.log(2.0), 0.0, math.log(3.0)])
    assert np.max(np.abs(np.asarray(ho.entropy_rows(p)) - ref)) <= 1e-15


@pytest.mark.parametrize("bad", ["zero_q", "nan_p", "inf_q"])
def test_kl_rows_numerical_failures(bad):
    p = np.array([[0.5, 0.5], [0.25, 0.75]])
    q = np.array([[0.5, 0.5], [0.5, 0.5]])
    if bad == "zero_q":
        q[1] = (0.0, 1.0)  # q = 0 where p > 0
    elif bad == "nan_p":
        p[0, 0] = np.nan
    else:
        q[0, 1] = np.inf
    with pytest.raises(hw.HwsStop) as err:
        ho.kl_rows(p, q)
    assert err.value.status == "FAIL_TECHNICAL/NUMERICAL"


def test_kl_rows_mean_equals_context_gain_on_random_rows():
    rng = np.random.default_rng(119002)
    p = rng.dirichlet(np.ones(7), size=64)
    p[::5, 2] = 0.0
    p = p / p.sum(axis=1, keepdims=True)
    q = rng.dirichlet(np.ones(7), size=64)
    got = np.asarray(ho.kl_rows(p, q))
    assert np.all(got >= 0.0)
    assert abs(float(np.mean(got)) - context_gain(p, q)) <= 1e-14

