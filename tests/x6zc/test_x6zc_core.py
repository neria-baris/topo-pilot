"""Author A (job 0120): X6ZC core tests (TEST_PLAN.md §2) from the protocol copy, API.md, CONTRACT,
TEST_PLAN and the 0117 review only (tools/x6zc/*.py never read). Expected values: protocol closed
forms or exact Fractions via reused X6S1 / stage-0 code (on sys.path via zc, API §1); synthetic."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6zc"))
import x6zc_core as zc  # noqa: E402
import x6zc_census as zs  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6s1_stats as ss  # noqa: E402
from topo_pilot.contracts import SeedTree, canonical_json  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "x6zc" / "CONTRACT.json").read_text("utf-8"))
P3, FAMS, VARS = [(), (10,), (6, 5, 9)], ("W2", "W1"), ("PP", "MM", "PM", "MP")
LAM, C, C2 = {"W2": xm.lam(18), "W1": xm.lam(8)}, (1, 2, 0), (2, 0, 1)
W1 = {  # member a / b paths, shared tail, crossing steps, bag difference (a, b), letters a / b
    "PP": ((14, 15, 3, 0, 4, 5, 6), (14, 15, 12, 0, 4, 5, 6), 4, (3, 4), (3, 12), "x+y+", "y+x+"),
    "MM": ((6, 5, 4, 0, 12, 15, 14), (6, 5, 4, 0, 3, 15, 14), 2, (5, 6), (12, 3), "x-y-", "y-x-"),
    "PM": ((14, 13, 12, 0, 3, 7, 6), (14, 13, 12, 15, 3, 7, 6), 3, (4, 5), (0, 15), "x+y-", "y-x+"),
    "MP": ((6, 7, 3, 15, 12, 13, 14), (6, 7, 3, 0, 12, 13, 14), 3, (4, 5), (15, 0), "x-y+", "y+x-")}

qfn = lambda tk, t: se.qstar("NA", tk, t)  # noqa: E731
hist = lambda f, v, m, p=(), y=0: tuple(map(int, zc.variant_history(f, v, m, p, y)))  # noqa: E731
row = lambda A, k, r: tuple(map(int, A[k][r, :int(A[k[:-1] + "t"][r])]))  # noqa: E731 (unpadded)
cue = lambda q: tuple(x / sum(q[15:18]) for x in q[15:18])  # noqa: E731 (exact cue normalisation)

crossings = lambda path: [(k + 1, lt) for k, (u, w) in  # noqa: E731 (edge index, letter)
                          enumerate(zip((10,) + tuple(path), path)) if (lt := xm.seam_letter(u, w))]

def expected_beta(kind, p, lam) -> tuple:  # §3.1 / TEST_PLAN closed forms, (PP, MM, PM, MP)
    g = lambda k: Fr(str(p[k]))  # noqa: E731
    if kind in ("M0", "M1"):
        d = g("w") if kind == "M0" else (g("kappa_a") - g("kappa_b")) / (2 * lam)
        return (d,) * 4 if kind == "M0" else (d, -d, Fr(0), Fr(0))
    if kind == "M4":
        pi = g("pi")
        x = {"x": (-pi, pi, pi / 2, -pi / 2), "y": (-pi, pi, -pi / 2, pi / 2)}[p["seam"]]
        return x if p["member"] == "a" else tuple(-e for e in x)
    a, b = g("pi_a"), g("pi_b")
    s = (a + b) / 2
    return {"M2a": (b - a, a - b, s, -s), "M2b": (b - a, a - b, -s, s),
            "M6": ((b - a) / 2, (a - b) / 2, Fr(0), Fr(0))}[kind]

fam = pytest.fixture(params=FAMS, name="fam")(lambda request: request.param)

@pytest.fixture(scope="module")
def pool():  # 4,096 random legal walks (stay included); cue 15 + y, y uniform, at anchor visits
    rng, nb = np.random.default_rng(20261026), np.array(xm.NEIGHBOURS)
    tok, out = np.array([0 if i == 10 else xm.tok(i) for i in range(16)]), np.zeros((4096, 33))
    v = rng.choice([i for i in range(16) if i != 10], 4096)
    for k in range(33):
        out[:, k] = np.where(v == 10, 15 + rng.integers(0, 3, 4096), tok[v])
        v = nb[v, rng.integers(0, 5, 4096)]
    return out.astype(np.uint8)

dset = pytest.fixture(scope="module", name="dset")(lambda pool: sp.designed_set(pool))

def test_pp_equals_x6s1_construction():
    assert zc.VARIANTS["W2"]["PP"] == sp.W2_LETTERS
    for p, y in ((p, y) for p in P3 for y in range(3)):
        assert [zc.variant_history(f, "PP", m, p, y) for f in FAMS for m in "ab"] == [
            sp.designed_history(p, ("A+", "B+"), y), sp.designed_history(p, ("B+", "A+"), y),
            sp._w1_history(p, "U", y), sp._w1_history(p, "D", y)]

def test_variant_arrays_layout(fam):
    A, off = zc.variant_arrays(P3, fam), {"W2": 18, "W1": 8}[fam]
    assert A["prefix"].dtype == np.int32 and A["prefix"].tolist() == [0, 0, 0, 1, 1, 1, 2, 2, 2]
    for v, m in ((v, m) for v in VARS for m in "ab"):
        t, y, X = A[f"{v}_t"], A[f"{v}_y"], A[f"{v}_{m}"]
        assert (t.dtype, y.dtype, X.dtype, X.shape) == (np.int16, np.int8, np.uint8, (9, 33))
        assert y.tolist() == [0, 1, 2] * 3
        assert t.tolist() == [len(P3[r // 3]) + off for r in range(9)]
        for r in range(9):  # history up to t, zero padding after
            assert row(A, f"{v}_{m}", r) == hist(fam, v, m, P3[r // 3], r % 3)
            assert len(row(A, f"{v}_{m}", r)) == t[r] and not X[r, t[r]:].any()

def test_w2_variant_matching():
    for v in VARS:
        assert tuple(map(tuple, zc.VARIANTS["W2"][v])) == tuple(map(tuple, CONTRACT["constants"][
            "variants"]["W2"][v]))  # e.g. MM: (A-, B-) / (B-, A-)
        for y in range(3):
            ha, hb = hist("W2", v, "a", (), y), hist("W2", v, "b", (), y)
            pa, pb = xm.parse(ha), xm.parse(hb)
            assert ha != hb and Counter(ha) == Counter(hb)
            assert Counter(zip(ha, ha[1:])) == Counter(zip(hb, hb[1:]))  # directed bigrams
            assert xm.parikh(pa["segment"]) == xm.parikh(pb["segment"])
            assert (pa["n"], pa["v"], pa["y"]) == (pb["n"], pb["v"], pb["y"]) == (17, 14, y)
            assert ha[-8:] == hb[-8:] == (5, 1, 2, 3, 7, 10, 14, 13)

def w1_stats(h) -> tuple:  # the x6_exact._EQUAL_ROWS statistics, computed here
    p = xm.parse(h)
    k = xm.parikh(p["segment"])
    return (len(h), len(p["segment"]) - 1, p["v"], p["prefix"], p["y"], k,
            *(xm.statistic(S, k) for S in ("H1", "counts", "parity")))

def test_w1_variant_matching():
    assert dict(zc.W1_TAIL) == {v: W1[v][2] for v in VARS}
    assert {k: tuple(s) for k, s in zc.W1_CROSS_STEPS.items()} == {v: W1[v][3] for v in VARS}
    for v in VARS:
        pa, pb, tail, steps, (da, db), la, lb = W1[v]
        assert tuple(map(tuple, zc.VARIANTS["W1"][v])) == (pa, pb)
        for y in range(3):
            ha, hb = hist("W1", v, "a", (), y), hist("W1", v, "b", (), y)
            assert w1_stats(ha) == w1_stats(hb) and ha != hb
            assert next(k for k in range(1, 9) if ha[-k] != hb[-k]) - 1 == tail
        ca, cb = crossings(pa), crossings(pb)
        assert [s for s, _ in ca] == [s for s, _ in cb] == list(steps)
        assert ("".join(lt for _, lt in ca), "".join(lt for _, lt in cb)) == (la, lb)
        assert Counter(pa) - Counter(pb) == Counter([da]) and Counter(pb) - Counter(pa) == {db: 1}
        for f in ((10,) + pa, (10,) + pb):  # anchor-neighbour start and end; legal steps
            assert f[1] in xm.ANCHOR_NB and f[-1] in xm.ANCHOR_NB
            assert all(w in xm.NEIGHBOURS[u] for u, w in zip(f, f[1:]))

def test_k0_on_pi0_exact(fam):
    A, lam = zc.variant_arrays(P3, fam), LAM[fam]
    res = zc.oracle_geometry(A, fam)
    assert res["status"] == "PASS" and res["counterexample"] is None and all(res["checks"].values())
    den = {"W2": 0.9664262564114334, "W1": 1.4475954411849916}[fam]
    assert abs(float(2 * lam * lam) - den) <= 1e-15
    for v in VARS:
        ref = {}
        for r in range(9):
            y, ha, hb = r % 3, row(A, f"{v}_a", r), row(A, f"{v}_b", r)
            for arm in ("ZC", "AB"):
                assert sp.q_exact(arm, ha, len(ha)) == sp.q_exact(arm, hb, len(hb))
            na, nb = sp.q_exact("NA", ha, len(ha)), sp.q_exact("NA", hb, len(hb))
            assert sum(na[15:18]) == sum(nb[15:18]) == Fr(1, 5)
            d = [a - b for a, b in zip(cue(na), cue(nb))]
            assert d == [lam * ((z == C2[y]) - (z == C[y])) for z in range(3)]
            assert sum(x * x for x in d) == 2 * lam * lam
            for m, q in (("a", na), ("b", nb)):  # q*_NA identical across the three prefixes
                assert ref.setdefault((m, y), q) == q

def test_k0_answer_table():
    ans = CONTRACT["constants"]["answers"]
    for fam_, v in ((f, v) for f in FAMS for v in VARS):
        hs = (hist(fam_, v, "a"), hist(fam_, v, "b"))
        got = [zc.answer_names(h) for h in hs]
        for k in ("NA", "ZC", "AB", "ZC_miss1", "ZC_miss2", "ZC_miss_both"):
            assert (got[0][k], got[1][k]) == tuple(ans[v][k])
        assert (got[0]["NA"], got[1]["NA"]) == ("c2", "c")
        for h, g in zip(hs, got):  # independent: names of the segment holonomies
            seg = xm.parse(h)["segment"]
            for a in ("NA", "ZC", "AB"):
                assert g[a] == xm.perm_name(xm.holonomy(seg, xm.edge_labels(a)))

def test_k0_detects_violation():
    A, B = zc.variant_arrays(P3, "W1"), zc.variant_arrays(P3, "W2")
    A["PM_b"] = A["PM_a"].copy()  # member b path (14, 13, 12, 0, 3, 7, 6) = member a
    B["MM_b"] = sp._pad([sp.designed_history(P3[r // 3], ("A-", "B+"), r % 3) for r in range(9)])
    for arrays, f, key in ((A, "W1", "PM"), (B, "W2", "MM")):
        res = zc.oracle_geometry(arrays, f)
        assert res["status"] == "FAIL"
        assert (res["counterexample"]["key"], res["counterexample"]["row"]) == (key, 0)

def test_missed_law():
    h, lam = hist("W2", "PP", "a", (), 0), LAM["W2"]
    z = sp.q_exact("ZC", h, len(h))
    for which, idx in (("miss1", 1), ("miss2", 1), ("miss_both", 0)):  # c[0] = 1, e[0] = 0
        m = tuple(zc.missed_law(h, which))
        want = tuple((1 - lam) / 3 + (lam if k == idx else 0) for k in range(3))
        assert len(m) == 18 and m[:15] == z[:15] and sum(m[15:18]) == Fr(1, 5)
        assert cue(m) == want == xm.point_law(18, idx)

def test_coupling_table():
    ct = zc.coupling_table()
    for f, y in ((f, y) for f in FAMS for y in ("0", "1", "2")):
        pp, mm, pm = (ct[f][v][y] for v in ("PP", "MM", "PM"))
        a, m1, m2 = pp["a"], pp["a"]["miss1"], pm["a"]["miss1"]
        assert (a["zc"], a["cos2_e"], a["sign_e"], pp["b"]["cos2_e"]) == ("c2", "3/4", 1, "3/4")
        assert (m1["to"], m1["cos2"], m1["sign"]) == ("c", "1", -1)
        assert abs(a["cos_e"] - math.sqrt(3) / 2) <= 1e-12 and abs(m1["cos"] + 1) <= 1e-12
        assert (mm["a"]["cos2_e"], mm["a"]["sign_e"], pm["a"]["zc"], pm["a"]["cos2_e"],
                pm["a"]["sign_e"]) == ("3/4", -1, "e", "0", 0)
        assert (m2["to"], m2["cos2"], m2["sign"]) == ("c2", "1/4", 1)

def test_k3_exact_values(fam):
    k3, grid, lam = zc.k3_exact(fam), zc.k3_grid(), LAM[fam]
    assert len(grid) == len(k3) == 18
    assert Counter(k for k, _ in grid) == Counter(M0=2, M1=2, M2a=2, M2b=2, M6=2, M4=8)
    for e in k3.values():
        want = expected_beta(e["kind"], e["params"], lam)
        assert tuple(e["beta"][v] for v in VARS) == want
        assert all(e["r"][v] == want[i] / want[0] for i, v in enumerate(VARS) if i)
        if e["kind"] == "M1" and Fr(str(e["params"]["kappa_a"])) == Fr(1, 20):
            flt = {"W2": -0.10789266013501635, "W1": -0.08815615865908194}[fam]
            assert abs(float(e["beta"]["PP"]) - flt) <= 1e-15

def test_f1_passes(fam):
    f = zc.f1(zc.k3_exact(fam))  # r values themselves: test_k3_exact_values
    assert f["passed"] and f["failed"] == [] and f["m0_ok"]

def test_partial_composite(fam):
    pred = zc.SyntheticPredictor("M0+M2a", w=Fr(3, 20), pi_a=Fr(0), pi_b=Fr(1, 20))
    want = (Fr(1, 5), Fr(1, 10), Fr(7, 40), Fr(1, 8))  # r = (1/2, 7/8, 5/8)
    assert tuple(zc.beta_exact_pi0(pred.exact, fam, v) for v in VARS) == want

def test_k3_float_path(fam):
    A, lam = zc.variant_arrays(P3, fam), LAM[fam]
    assert zc.k3_float_check(fam, A, qfn)["status"] == "PASS"  # API-AMBIGUITY: keys unlisted
    for kind, params in zc.k3_grid():
        pred, want = zc.SyntheticPredictor(kind, **params), expected_beta(kind, params, lam)
        for i, v in enumerate(VARS):
            T = zc.pair_arrays(pred, A, v, qfn)
            assert abs(se.beta_fsum(T["num"], T["den"]) - float(want[i])) <= 1e-12

def mk_key(h) -> int:  # the matched-key K of API §6 / C-11, recomputed here
    p = xm.parse(h)
    blob = canonical_json([list(p["prefix"]), p["y"], p["n"], p["v"],
                           list(xm.parikh(p["segment"]))]).encode("utf-8")
    return int(hashlib.sha256(blob).hexdigest()[:8], 16) % 1000

def test_k1_exact_zero(fam):
    A, rng = zc.variant_arrays(P3, fam), np.random.default_rng(3)
    mk, sc = zc.SyntheticPredictor("matched_key"), zc.SyntheticPredictor("set_constant")
    preds = [zc.oracle("ZC", "qstar"), zc.oracle("AB", "qstar"), sc, mk] + [
        zc.oracle("NA", k) for k in ("q_empty", "q_parity", "q_counts", "q_H1", "q_Parikh")]
    for v, pred in ((v, p) for v in VARS for p in preds + [zc.oracle("NA", "q_8")] * (fam == "W2")):
        T = zc.pair_arrays(pred, A, v, qfn)
        res = zc.k1_check(T)
        assert res["status"] == "PASS" and res["beta"] == 0.0 and res["rho"] == 0.0
        assert res["num_zero"] and res["beta_exact_zero"]
        assert (T["num"] == 0.0).all() and se.beta_exact(T["num"], T["den"]) == 0
    for v, r in ((v, r) for v in VARS for r in range(9)):
        K, m = mk_key(row(A, f"{v}_a", r)), Fr(1 + mk_key(row(A, f"{v}_a", r)) % 7, 10)
        assert K == mk_key(row(A, f"{v}_b", r))  # the same K for both members
        assert tuple(mk.exact(row(A, f"{v}_a", r)))[15:] == tuple(
            m * Fr(K + 1 + z, 3 * K + 6) for z in range(3))
    pa, pb = rng.dirichlet(np.ones(18), 9), rng.dirichlet(np.ones(18), 9)
    sa, sb = zc.sym_arrays(pa, pb)
    assert np.array_equal(sa, sb) and np.array_equal(sa, (pa + pb) / 2)
    q_a, q_b = qfn(A["PP_a"], A["PP_t"])[0], qfn(A["PP_b"], A["PP_t"])[0]
    assert (se.pair_terms(sa, sb, q_a, q_b)[0] == 0.0).all()

def skew_a(tokens, t):  # q*_ZC + 1e-6 on token 15 for member a (x crossing first), renormalised
    p = zc.oracle("ZC", "qstar")(tokens, t)
    for i, k in enumerate(np.broadcast_to(np.asarray(t, np.int64), (len(tokens),))):
        if crossings(xm.parse(tuple(int(w) for w in tokens[i, :k]))["segment"][1:])[0][1] < "y":
            p[i, 15] += 1e-6
            p[i] /= p[i].sum()
    return p

def test_k1_detects_noninvariance(fam):
    res = zc.k1_check(zc.pair_arrays(skew_a, zc.variant_arrays(P3, fam), "PP", qfn))
    assert res["status"] == "FAIL" and not res["num_zero"]

def test_k2_references(fam):
    A, h = zc.variant_arrays(P3, fam), Fr(1, 2)
    per_y = {"qstar": (1, 1, 1), "h_last": (h, -1, h), "h_first": (-h, 1, -h)}
    pooled = {"qstar": 1.0, "h_last": 0.0, "h_first": 0.0, "h_rev": -1.0}
    T = {k: zc.pair_arrays(zc.oracle("NA", k), A, "PP", qfn) for k in pooled}
    for k, Tk in T.items():
        st, y = zc.pair_stats(Tk), np.asarray(Tk["y"])
        assert abs(st["beta"] - pooled[k]) <= 1e-12
        for z, want in enumerate(per_y.get(k, ())):
            assert abs(st["beta_y"][z] - float(want)) <= 1e-12
            assert abs(se.beta_fsum(Tk["num"][y == z], Tk["den"][y == z]) - float(want)) <= 1e-12
    assert (res := zc.k2_check(T, fam))["status"] == "PASS" and res["failed"] == []
    sw = {k: {**Tk, "p_a": Tk["p_b"], "p_b": Tk["p_a"],  # DR13: swapped on the predictor side
              "num": se.pair_terms(Tk["p_b"], Tk["p_a"], Tk["q_a"], Tk["q_b"])[0]}
          for k, Tk in T.items()}
    assert abs(zc.pair_stats(sw["qstar"])["beta"] + 1) <= 1e-12
    assert (res := zc.k2_check(sw, fam))["status"] == "FAIL" and "qstar" in res["failed"]

def test_fresh_prefix_continuation(pool, dset):
    gen = lambda: SeedTree(2026101861).generator("x6s1", "prefix_len")  # noqa: E731
    rnd, ys = gen(), []
    for r, toks in enumerate(pool):  # this test's own yield loop: one integers(1, 15) per row
        lmax = int(rnd.integers(1, 15))
        ok = [L for L in range(1, lmax + 1) if xm.vertex(int(toks[L - 1])) in (6, 9, 10, 11, 14)]
        ys += [(r, tuple(int(w) for w in toks[:ok[-1]]))] if ok else []
    first, dpre = [p for _, p in ys[:1024]], dset["prefixes"]
    assert first == sp.natural_prefixes(pool, gen()) == [tuple(p) for _, p in dpre[6:]]
    assert [(int(r), tuple(map(int, p))) for r, p in zc.prefix_yields(pool, gen())] == ys
    res, r_star = zc.fresh_prefixes(pool, dpre), ys[1023][0]
    fresh = [(r, p) for r, p in ys if r > r_star]
    assert res["first_1024_equal"] and res["d_equal"]
    assert (res["n_rows"], res["n_yields"], res["r_star"]) == (4096, len(ys), r_star)
    assert [(int(r), tuple(map(int, p))) for r, p in res["fresh"]] == fresh
    assert res["n_avail"] == len(fresh) == len(ys) - 1024
    coinc = [p in {tuple(map(int, q)) for _, q in dpre} for _, p in fresh]
    assert [bool(x) for x in res["d_coincident"]] == coinc
    assert res["n_d_coincident"] == sum(coinc) and res["not_enough_data"] == (len(fresh) < 512)
    with pytest.raises(ValueError):
        zc.fresh_prefixes(pool[:1000], dpre)  # fewer than 1,024 yields

def test_qstar_cache_bitwise(tmp_path):
    arrs = [zc.variant_arrays(P3, f) for f in FAMS]
    cache = zc.QStarCache.build(arrs)
    def check(c):
        for A, v, m in ((A, v, m) for A in arrs for v in VARS for m in "ab"):
            (q, cd), (q0, c0) = c(A[f"{v}_{m}"], A[f"{v}_t"]), qfn(A[f"{v}_{m}"], A[f"{v}_t"])
            assert q.dtype == np.float64 and cd.dtype == np.int16
            assert q.tobytes() == q0.tobytes() and cd.tobytes() == c0.tobytes()
    check(cache)
    h = hist("W2", "PP", "a", (13,), 0)  # a prefix absent from the cached arrays
    with pytest.raises(KeyError):
        cache(sp._pad([h]), np.array([len(h)], np.int64))
    cache.save(str(path := tmp_path / "qstar_NA.npz"))
    check(zc.QStarCache.load(str(path), hashlib.sha256(path.read_bytes()).hexdigest()))
    with pytest.raises((ValueError, RuntimeError)):  # API-AMBIGUITY: exception type unnamed
        zc.QStarCache.load(str(path), "0" * 64)

def test_paired_boot_equals_boot_beta():
    rng, keys = np.random.default_rng(11), ("ZC-s1|W2|PP|beta", "ZC-s1|W2|MM|beta")
    num = {k: rng.normal(0.1, 0.3, 50) for k in keys}
    den = {k: rng.uniform(0.5, 1.5, 50) for k in keys}
    one = {k: zc.paired_cluster_boot({k: num[k]}, {k: den[k]}, 200, np.random.default_rng(5))[k]
           for k in keys}
    for k in keys:
        ref = ss.boot_beta(num[k], den[k], 200, np.random.default_rng(5))
        assert one[k].shape == (200,) and one[k].tobytes() == ref.tobytes()
    both = zc.paired_cluster_boot(num, den, 200, np.random.default_rng(5))
    assert all(both[k].tobytes() == one[k].tobytes() for k in keys)  # one index array per draw

def test_cluster_sums_and_ratio_interval():
    cs = zc.cluster_sums(np.arange(1.0, 5.0), np.array([0, 0, 1, 1]), 2)
    assert np.asarray(cs).tolist() == [3.0, 7.0]
    rng = np.random.default_rng(7)
    pp, dv = rng.uniform(0.1, 0.3, 200), rng.uniform(-0.2, 0.3, 200)
    pp[[5, 50, 150]] = [-0.1, 0.0, -0.2]  # 3 draws with sign * draws_pp <= 0
    q = (1 / 120, 119 / 120)
    out, rat = zc.ratio_interval(dv, pp, 1, q), dv[pp > 0] / pp[pp > 0]
    assert (out["undefined"], out["n_defined"], out["undefined_frac"]) == (3, 197, 3 / 200)
    assert (out["lo"], out["hi"]) == (ss.quantile(rat, q[0]), ss.quantile(rat, q[1]))
    d = rng.normal(size=100)
    assert tuple(zc.interval(d, (0.025, 0.975))) == (ss.quantile(d, 0.025), ss.quantile(d, 0.975))
    d[3] = np.nan
    with pytest.raises(ValueError):
        zc.interval(d, (0.025, 0.975))

def test_halfwidth_and_choose_n():
    bd = {"P": 0.20930750050575797, "S3": -0.13252283561285252, "S4": -0.21837877479808415}
    assert abs(zc.halfwidth(1024, 0.01, bd["P"], 2.394) - 0.179366) <= 1e-6
    full, ok, up = [1024, 2048, 2400], "OK", "UNDERPOWERED"
    cases = {(2400, 0.01): (1024, ok, full), (2400, 0.015): (2048, ok, full),
             (1500, 0.015): (1500, ok, [1024, 1500]), (2400, 0.03): (2400, up, full),
             (800, 0.01): (800, ok, [800]), (800, 0.015): (800, up, [800])}
    res = {}
    for (n_avail, se_p), want in cases.items():
        r = res[n_avail, se_p] = zc.choose_n(n_avail, {"P": se_p, "S3": 0.01, "S4": 0.01})
        assert (r["n"], r["status"], list(r["candidates"])) == want
        assert bool(r["underpowered"]["P"]) == (want[1] == up) and r["low_feasibility"] == ["S3"]
    r = res[2400, 0.01]  # se S3 = 0.01: underpowered at n 1024, not at n 2048
    assert (r["underpowered"]["S3"], r["underpowered"]["S4"]) == (True, False)
    assert abs(r["h"]["S3"]["1024"] - 0.33252) <= 1e-5
    r = res[2400, 0.015]
    assert not r["underpowered"]["S3"] and abs(r["h"]["S3"]["2048"] - 0.235127) <= 1e-5
    assert abs(res[1500, 0.015]["h"]["P"]["1500"] - 0.23470) <= 2e-5
    r = zc.choose_n(300, {"P": 0.01, "S3": 0.01, "S4": 0.01})
    assert (r["n"], r["status"]) == (300, "NOT_ENOUGH_DATA") and not any(r["underpowered"].values())

def rand_pred(tokens, t, rng=np.random.default_rng(13)):  # cue mass uniform in [0.1, 0.3]
    n = len(tokens)
    m, out = rng.uniform(0.1, 0.3, n), np.empty((n, 18))
    out[:, :15] = rng.dirichlet(np.ones(15), n) * (1 - m)[:, None]
    out[:, 15:] = rng.dirichlet(np.ones(3), n) * m[:, None]
    return out

skew_a.name, rand_pred.name = "skew_a", "rand"  # the predictor interface has a name (API §2)

def test_d2_identity():
    A = zc.variant_arrays([(), (10,), (10,), (6, 5, 9), ()], "W2")  # duplicated prefixes (DR20)
    T = zc.pair_arrays(rand_pred, A, "PP", qfn)
    out = zs.d2_decompose(T)
    dq = se.cue_normalise(T["q_a"]) - se.cue_normalise(T["q_b"])
    dpr = np.asarray(T["p_a"])[:, 15:18] - np.asarray(T["p_b"])[:, 15:18]
    want = math.fsum((5 * dpr * dq).sum(1)) / math.fsum((dq * dq).sum(1))
    assert out["identity_max_abs"] <= 1e-12 and abs(out["beta_fixed"] - want) <= 1e-12
    T = zc.pair_arrays(zc.oracle("NA", "qstar"), A, "PP", qfn)  # cue mass exactly 1/5
    out, beta = zs.d2_decompose(T), se.beta_fsum(T["num"], T["den"])
    assert out["identity_max_abs"] <= 1e-12 and abs(out["beta_fixed"] - beta) <= 1e-12

def test_audit_pairs(dset):
    for f, v, y in ((f, v, y) for f in FAMS for v in VARS for y in range(3)):
        assert [zc.member_of(hist(f, v, m, (10,), y)) for m in "ab"] == ["a", "b"]
    with pytest.raises(ValueError):
        zc.member_of((15, 9, 5))  # no seam crossing after the cue
    A, npre = sp.designed_arrays(dset), len(dset["prefixes"])  # 1,030 prefixes
    assert [zs.audit_pairs(A, f, n_prefixes=npre)["status"] for f in FAMS] == ["PASS"] * 2
    B, C = ({k: v.copy() for k, v in A.items()} for _ in range(2))
    B["W2_a"][7], B["W2_b"][7] = A["W2_b"][7], A["W2_a"][7]
    C["W1_t"][4] += 1  # a stored t that is not the unpadded length
    for arrays, f, r in ((B, "W2", 7), (C, "W1", 4)):
        res = zs.audit_pairs(arrays, f, n_prefixes=npre)
        assert res["status"] == "DEFECT_CANDIDATE" and res["counterexample"]["row"] == r
