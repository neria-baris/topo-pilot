"""X6 stage 0 independent tests (X6-FROZEN-v1 section 10.4: tests 6-8, 10-12, 15-17), written
from the protocol and API.md only; references: brute force, Fractions, ints, Decimal, hashlib,
json and the independent helpers of test_x6_stage0.py. Stores live under pytest's tmp_path."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_x6_stage0 import (  # noqa: E402  (also puts tools/x6_stage0 on sys.path)
    ANC, NB, A, C, C2, E0, comp, dec, dkl, emis, filt, labels, lam, letter, lift, mu,
    nbrs, w_tokens)

import x6_dp as xd  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
import x6_run as xr  # noqa: E402
from independent_reference import decimal_suffix_posterior  # noqa: E402

IDX = {"x+": 0, "x-": 1, "y+": 2, "y-": 3}
LADDER = ("empty", "parity", "counts", "H1", "Parikh")
INV = "INVALID/LINEAGE"
DP_ITEMS = {"AB.ambiguity", "AB.G_S", "AB.D_blk", "ZC.ambiguity", "ZC.G_S", "ZC.D_blk",
            "TRIV.G_S", "TRIV.D_blk", "ETA1.G_S", "FIXED-POINT"}  # section 8.5, S8


def stat(s, k):
    return {"empty": (), "parity": sum(k) % 2, "counts": (k[0] + k[1], k[2] + k[3]),
            "H1": (k[0] - k[1], k[2] - k[3]), "Parikh": k}[s]

def brute_layers(arm, n_max):  # every anchor-avoiding path, keyed by (v, kappa, g)
    lab, layers = labels(arm), [Counter() for _ in range(n_max + 1)]
    def go(v, kap, g, n):
        layers[n][(v, kap, g)] += 1
        for j in (nbrs(v) if n < n_max else ()):
            if j != ANC:
                k = list(kap)
                if letter(v, j):
                    k[IDX[letter(v, j)]] += 1
                go(j, tuple(k), comp(lab[(v, j)], g), n + 1)
    go(ANC, (0, 0, 0, 0), E0, 0)
    return layers

def brute_tally(start, m_max):  # end vertices of m-step paths that never step onto the anchor
    tally = [Counter() for _ in range(m_max + 1)]
    def go(v, m):
        tally[m][v] += 1
        for j in (nbrs(v) if m < m_max else ()):
            if j != ANC:
                go(j, m + 1)
    go(start, 0)
    return tally

def layer_at(arm, n):
    for k, layer in xd.segment_dp(arm, n):
        if k == n:
            return dict(layer)


def test_06_zc_witness_and_ab_fixed_point():  # section 10.4 test 6
    p1, p2 = (10, 14, 2, 6, 6, 6, 6, 6), (10, 9, 5, 1, 13, 9, 5, 6)
    assert tuple(map(tuple, xm.ZC_WITNESS)) == (p1, p2)
    assert all(v != ANC for v in p1[1:] + p2[1:]) and p1[-1] == p2[-1] == 6
    assert [tuple(xm.holonomy(p, xm.edge_labels("ZC"))) for p in (p1, p2)] == [C, C2]
    k1, k2 = (1, 0, 0, 0), (0, 1, 0, 0)
    assert (tuple(xm.parikh(p1)), tuple(xm.parikh(p2))) == (k1, k2)
    assert (list(xm.path_letters(p1)), list(xm.path_letters(p2))) == (["x+"], ["x-"])
    assert all(xm.statistic(s, k) == stat(s, k) for s in LADDER for k in (k1, k2))
    lay = layer_at("ZC", 7)
    assert lay[(6, k1, C)] >= 1 and lay[(6, k2, C2)] >= 1
    cls = xd.classes(lay, "counts")[(6, (1, 0))]  # parity and counts cannot separate them
    assert cls.get(C, 0) > 0 and cls.get(C2, 0) > 0 and all(xd.ambiguous(cls, y) for y in (0, 1, 2))
    assert not any(xd.ambiguous(c, y) for c in xd.classes(lay, "H1").values() for y in (0, 1, 2))
    for n in range(1, 7):  # AB: a fixes 2, so no empty-statistic class is ambiguous at y = 2
        for c in xd.classes(layer_at("AB", n), "empty").values():
            assert not xd.ambiguous(c, 2) and tuple(xd.weights(c, 2)) == (0, 0, 1)
    c2n = xd.classes(layer_at("AB", 2), "empty")[(2, ())]  # 10-6-2 (e) and 10-14-2 (a)
    assert dict(c2n) == {E0: 1, A: 1} and xd.ambiguous(c2n, 0) and xd.ambiguous(c2n, 1)
    assert tuple(xd.weights(c2n, 0)) == (F(1, 2), F(1, 2), 0)


def test_07_gauge_nocue_tokperm_eta1():  # section 10.4 test 7
    hist = [w_tokens("W1", m, y) for m in ("U", "D") for y in range(3)]
    hist += [(15, 13, 17, 9), (16, 13, 12, 9, 5, 9) + w_tokens("W1", "D", 2)]
    for kind in ("E", "E_cov", "E_nc", "E_sigma"):
        assert xm.emission(kind) == emis(kind)
    sig = [(w + 7) % 15 if w <= 14 else w for w in range(18)]
    assert [xm.sigma_tok(w) for w in range(18)] == sig
    ref = {a: [filt(lift(a), emis(), h)[0] for h in hist] for a in ("NA", "TRIV")}
    for g, base in (("GAUGE-NA", "NA"), ("GAUGE-COV", "NA"), ("GAUGE-TRIV", "TRIV")):
        m = xm.model(g)
        assert m["E"] == emis("E_cov" if g == "GAUGE-COV" else "E")
        assert [filt(m["T"], m["E"], h)[0] for h in hist] == ref[base]
    gt = xm.edge_labels("GAUGE-TRIV")  # non-commuting pure-gauge labels
    assert (tuple(gt[(0, 1)]), tuple(gt[(1, 2)])) == (A, C2) and comp(A, C2) != comp(C2, A)
    for fam in ("W1", "W2"):
        na = xe.family_values("NA", fam)["members"]
        for g in ("GAUGE-NA", "GAUGE-COV"):
            gm = xe.family_values(g, fam)["members"]
            assert all(list(gm[k]["q"][y]) == list(na[k]["q"][y]) for k in na for y in range(3))
        assert xe.family_values("GAUGE-TRIV", fam)["spread"] == 0
    m_na, m_tr = xm.model("NA", "E_nc"), xm.model("TRIV", "E_nc")  # NOCUE
    for path in ((10, 14, 15, 3, 0, 4, 5, 6), (10, 11, 8, 9, 10, 10, 6)):
        qa, _, ba = filt(m_na["T"], m_na["E"], path)
        assert qa == filt(m_tr["T"], m_tr["E"], path)[0]
        for t, v in enumerate(path, start=1):
            assert qa[t] == [F(1, 5) if k in nbrs(v) else 0 for k in range(16)]
            assert [ba[t - 1][3 * v + x] for x in range(3)] == [F(1, 3)] * 3
    ms = xm.model("NA", "E_sigma")  # TOKPERM
    for h, qe in zip(hist, ref["NA"]):
        qs = filt(ms["T"], ms["E"], [sig[w] for w in h])[0]
        assert all(qs[t][sig[w]] == qe[t][w] for t in range(len(h) + 1) for w in range(18))
    for h in hist[:6]:  # ETA1: the fibre is redrawn at every step
        qs = filt(lift("ETA1"), emis(), h)[0]
        assert list(xm.closed_form("ETA1", h)["q"]) == qs[-1] and qs[-1][15:] == [F(1, 15)] * 3


def test_08_dp_against_brute_force():  # section 10.4 test 8
    for arm in ("NA", "AB", "ZC", "TRIV", "ETA1"):
        ref = brute_layers(arm, 6)
        for i, (n, layer) in enumerate(xd.segment_dp(arm, 6)):
            assert n == i and dict(layer) == dict(ref[n])
            assert all(type(c) is int for c in layer.values())  # Python ints, never fixed-width
            for s in (LADDER if n == 6 else ()):  # aggregation of the one Parikh DP
                agg = {}
                for (v, k, g), c in ref[6].items():
                    agg.setdefault((v, stat(s, k)), Counter())[g] += c
                got = {key: dict(c) for key, c in xd.classes(layer, s).items()}
                assert got == {key: dict(c) for key, c in agg.items()}
        assert n == 6
    at = brute_tally(ANC, 8)
    a_ref = [sum(t.values()) for t in at]
    b_ref = [sum(c for v, c in t.items() if v in NB) for t in at]
    assert a_ref[1:] == [4, 16, 76, 352, 1684, 7984, 38236, 182464]  # Theorem 7 [W]
    d_ref = [{} for _ in range(8)]
    for v in (v for v in range(16) if v != ANC):
        for m, t in enumerate(brute_tally(v, 7)):
            d_ref[m][v] = sum(t.values())
    counts = xd.avoid_counts(8)
    assert list(counts["A"]) == a_ref and list(counts["B"]) == b_ref
    assert [dict(d) for d in counts["D"][:8]] == d_ref
    for t in range(1, 9):  # total-mass identity from the brute-force counts
        tot = F(1, 16) + sum(F(a_ref[n], 16 * 5 ** n) for n in range(1, t))
        assert tot + F(sum(d_ref[t - 1].values()), 16 * 5 ** (t - 1)) == 1
        assert xd.total_mass(t, counts) == 1
    cnt, a_n = {ANC: 1}, [1]
    for _ in range(31):
        new = Counter()
        for v, c in cnt.items():
            for j in (j for j in nbrs(v) if j != ANC):
                new[j] += c
        cnt = new
        a_n.append(sum(cnt.values()))
    big = xd.avoid_counts(31)["A"]
    assert type(big[31]) is int and big[31] == a_n[31] > 2 ** 64 and 7.8e20 < a_n[31] < 8e20


def test_10_decimal_inputs_pass_through():  # section 10.4 test 10
    T, E, pi = xd.decimal_model("NA", 80)
    Tf, Ef = lift("NA"), emis()
    assert all(type(v) is Decimal for row in T + E + [pi] for v in row)
    assert all(T[i][j] == dec(Tf[i][j]) for i in range(48) for j in range(48))
    assert all(E[i][j] == dec(Ef[i][j]) for i in range(48) for j in range(18))
    assert pi == [dec(F(1, 48))] * 48 and T[0][12] == dec(F(74, 375))
    assert xd.to_decimal(F(1, 3), 90) == dec(F(1, 3))
    assert xd.to_decimal(F(1, 3), 130) == dec(F(1, 3), 130)
    suffix = (15, 13, 14, 3)  # cue y = 0, then 14, 15, 3 (one x+ crossing)
    b = filt(Tf, Ef, suffix)[2][-1]
    post = decimal_suffix_posterior(T, E, pi, suffix, 80)
    assert all(type(p) is Decimal for p in post)
    assert max(abs(p - dec(r)) for p, r in zip(post, b)) <= Decimal("1e-45")
    post_f = decimal_suffix_posterior([[float(v) for v in r] for r in T], E, pi, suffix, 80)
    assert max(abs(p - dec(r)) for p, r in zip(post_f, b)) > Decimal("1e-45")  # floats differ


def test_11_enclosures_certification_memo():  # section 10.4 test 11
    with localcontext() as ctx:
        ctx.prec = 200
        v, eps, tiny = Decimal("0.5"), Decimal("3e-60"), Decimal("1e-80")
        enc = xd.enclosure(v, v + Decimal("1e-70"), Decimal(3), 10)
        assert (enc["type"], enc["N"], enc["eps"]) == ("enclosure", 10, eps)
        assert (enc["lo"], enc["hi"], enc["consistent"], enc["n_ok"]) == (
            v - eps, v + eps, True, True)
        assert xd.enclosure(v, v, Decimal("0.2"), 0)["eps"] == Decimal("1e-60")
        assert xd.enclosure(v, v + Decimal("2e-60"), Decimal(1), 5)["consistent"] is False
        assert xd.enclosure(v, v, Decimal(1), 10 ** 17 - 10)["n_ok"] is True  # RC6 bound
        assert xd.enclosure(v, v, Decimal(1), 10 ** 17 - 9)["n_ok"] is False
        for theta, cert in ((v - eps, "PASS"), (v - eps + tiny, "UNCERTIFIED"),
                            (v + eps, "UNCERTIFIED"), (v + eps + tiny, "FAIL"),
                            (F(1, 2), "UNCERTIFIED"), (F(1, 4), "PASS"), (1, "FAIL")):
            assert xd.certify(enc, theta) == cert, theta
        s = xd.enclose_sum([(Decimal("0.1"), Decimal("0.1")), (Decimal("-0.3"), Decimal("-0.3"))])
        assert (s["v80"], s["abs_sum"], s["N"]) == (Decimal("-0.2"), Decimal("0.4"), 2)
        assert s["eps"] == Decimal("1e-60") and s["consistent"] is True
        encs = [xd.enclosure(Decimal(x), Decimal(x), Decimal(1), 1)
                for x in ("0.02", "0.005", "0.01")]
        assert [xd.certify(e, F(1, 100)) for e in encs] == ["PASS", "FAIL", "UNCERTIFIED"]
        rows = list(zip((F(1, 10), F(1, 5), F(1, 20)), encs))
        assert tuple(xd.mass_bounds(rows, F(1, 100))) == (F(1, 10), F(3, 20))  # M_lo, M_up
    for lo, up, cert in ((F(1, 10), F(3, 20), "PASS"), (F(1, 32), F(1, 16), "PASS"),
                         (F(1, 64), F(1, 40), "FAIL"), (F(1, 64), F(1, 32), "UNCERTIFIED")):
        assert xd.certify_mass(lo, up, F(1, 32)) == cert
    with pytest.raises(ValueError):
        xd.kl_decimal([F(1), F(0)], [F(0), F(1)], 80)
    xd.memo_clear()
    w = (F(2, 4), F(1, 2), 0)
    assert xd.memo_key(80, "next", 7, w, 1) == (80, "next", 7, (F(1, 2), F(1, 2), F(0)), 1)
    for kind, m in (("next", 8), ("fibre", 7)):
        first, again = xd.kl_term(80, kind, 7, w, 2), xd.kl_term(80, kind, 7, w, 2)
        fresh = xd.kl_term_uncached(80, kind, 7, w, 2)
        assert first == again == fresh and str(first) == str(fresh)
        mix = [lam(m) * a + (1 - lam(m)) / 3 for a in (F(1, 2), F(1, 2), F(0))]
        assert abs(first - dkl(mu(m, 2), mix, 80)) < Decimal("1e-70")
        assert abs(xd.kl_term(120, kind, 7, w, 2) - dkl(mu(m, 2), mix, 120)) < Decimal("1e-110")
        assert {xd.memo_key(p, kind, 7, w, 2) for p in (80, 120)} <= set(xd.MEMO)
    assert len(xd.MEMO) == 4  # one entry per (precision, kind): never shared
    xd.memo_clear()
    assert len(xd.MEMO) == 0


def _st(**over):
    return {**{k: "PASS" for k in xr.ORDER}, **over}


def test_12_outcome_logic():  # section 10.4 test 12
    assert tuple(xr.ORDER) == ("PF", "S0", "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7")
    ok8 = {"completed_checks_pass": True, "theorem4": True}
    nr = {g: "NOT_RUN" for g in ("G5", "G6", "G7")}
    s8 = _st(G4="RESOURCE_LIMIT", G6="NOT_RUN")
    cases = [  # statuses, o1, o2, s8 -> verdict, first_failed (None: not checked), outcome
        (_st(), True, "PASS", None, "PASS", None, "GO_X6_NATURAL", True),
        (_st(), True, "FAIL", None, "PASS", None, "GO_X6_CHALLENGE_ONLY", True),
        (_st(), True, "UNCERTIFIED", None, "PASS", None, "INCONCLUSIVE_NATURAL", True),
        (_st(), False, "PASS", None, "PASS", None, "STOP_X6", False),
        (_st(G3="FAIL", G4="NOT_RUN", **nr), None, None, None, "FAIL", "G3", "WITHHELD", False),
        (_st(PF="INVALID"), True, "PASS", None, "INVALID", "PF", "WITHHELD", False),
        (_st(S0="INVALID"), True, "PASS", None, "INVALID", "S0", "WITHHELD", False),
        (_st(G6="NOT_RUN"), True, "PASS", None, "INVALID", "G6", "WITHHELD", False),
        (_st(G4="INVALID", **nr), True, None, None, "INVALID", "G4", "WITHHELD", False),  # S7
        (_st(G4="INVALID", **nr), True, None, ok8, "INVALID", "G4", "WITHHELD", False),
        (s8, True, None, ok8, "RESOURCE_LIMIT", None, "INCONCLUSIVE_NATURAL", True),
        (s8, True, None, {**ok8, "theorem4": False}, "RESOURCE_LIMIT", None,
         "INCONCLUSIVE_NATURAL", False),
        (s8, False, None, ok8, "RESOURCE_LIMIT", None, "STOP_X6", False),
        (s8, True, None, None, "FAIL", "G4", "WITHHELD", False),  # S3, never INCONCLUSIVE
        (s8, True, None, {**ok8, "completed_checks_pass": False}, "FAIL", "G4", "WITHHELD",
         False),
        ({**s8, "G5": "FAIL", "G7": "NOT_RUN"}, True, None, ok8, "FAIL", "G5", "WITHHELD", False),
    ]
    for st, o1, o2, s8_arg, verdict, first, outcome, window in cases:
        r = xr.decide(st, o1, o2, s8_arg)
        assert (r["verdict"], r["outcome"], r["window_clause"]) == (verdict, outcome, window)
        assert first is None or r["first_failed"] == first
        if outcome == "WITHHELD" and first not in ("PF", "S0"):
            assert list(r["not_run"]) == list(xr.ORDER[xr.ORDER.index(first) + 1:]) + ["D"]
        if verdict == "RESOURCE_LIMIT":
            assert list(r["not_run"]) == list(xr.S8_NOT_RUN)
    assert set(xr.S8_NOT_RUN) == {"G6"} | DP_ITEMS and len(xr.S8_NOT_RUN) == 11
    assert set(xr.G7_DP_ITEMS) == DP_ITEMS and DP_ITEMS <= set(xr.G7_ITEMS)
    assert [xr.label_cert(c, "Y", "N") for c in ("PASS", "FAIL", "UNCERTIFIED")] == [
        "Y", "N", "UNRESOLVED"]


def test_15_indicator_se_and_rs_keys():  # section 10.4 test 15
    n = 2 ** 18
    assert xr.indicator_se(F(1, 4), n) == pytest.approx(math.sqrt(0.25 * 0.75 / n), rel=1e-12)
    zero = xr.indicator_check(0, n, F(0))  # p = 0 with zero hits passes
    assert zero["pass"] is True and zero["exact"] == 0.0 and zero["se"] == 0.0
    for hits, p, ok in ((0, F(15, n + 16), True), (0, F(17, n + 16), False), (1, F(0), False),
                        (n // 4, F(1, 4), True)):  # zero hits fail iff p > 16/(2^18 + 16)
        res = xr.indicator_check(hits, n, p)
        assert res["pass"] is ok and res["type"] == "mc" and res["estimate"] == hits / n
    assert (xr.mc_check(0.5, 0.54 + 1e-12, 0.01), xr.mc_check(0.5, 0.54 + 1e-11, 0.01)) == (
        True, False)  # |estimate - exact| <= 4 SE + 2e-12
    u, d = w_tokens("W1", "U", 0), w_tokens("W1", "D", 0)
    for s in LADDER:  # W1-U and W1-D share the Parikh vector (1, 0, 1, 0)
        ku, kd, kp = xe.rs_key(s, u), xe.rs_key(s, d), xe.rs_key(s, (10,) + u)
        assert tuple(ku) == (False, (), 7, 0, 6, stat(s, (1, 0, 1, 0))) and ku == kd
        assert tuple(kp) == (False, (10,), 7, 0, 6, stat(s, (1, 0, 1, 0)))
        assert xe.constant_by_keys([ku, kd]) is True and xe.constant_by_keys([ku, kp]) is False
    assert tuple(xe.rs_key("H1", (5, 6, 7))) == (True, (5, 6, 7), None, None, 7, None)
    assert xe.constant_by_keys([]) is False


def put(path, data=b"x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def test_16_rerun_and_lineage_rule(tmp_path):  # section 10.4 test 16
    store, run = tmp_path / "store", tmp_path / "store" / "run"
    assert xr.lineage_precheck(store)["status"] == "PASS"  # an absent store passes
    for name in ("x6_meter_bind.py", "cpu_ledger.json", "RUN.lock"):
        put(store / name)
    log = put(store / "logs" / "m.log", b"log\n")
    assert xr.lineage_precheck(store)["status"] == "PASS"
    stray = put(store / "stray.txt")
    pre = xr.lineage_precheck(store)
    assert pre["status"] == INV and "stray.txt" in list(pre["unrecognised"])
    rec = {"job": "0058", "head": "h", "head_expected": "h", "porcelain": [], "suites": {},
           "tempdir": str(tmp_path), "basetemp": str(tmp_path), "new_tests": 0, "file_sizes": 0}
    assert xr.write_preflight(store, rec)["status"] == "INVALID" and not run.exists()
    stray.unlink()
    xr.write_marker(run, "G0")
    with pytest.raises(FileExistsError):
        xr.write_marker(run, "G0")
    xr.write_gate(run, "G0", "PASS", {"value": F(1, 3), "cpu_s": 1.5, "out_dir": "X:/a"})
    gdir = run / "gates" / "G0"
    assert (gdir / "values.json").read_bytes() == json.dumps(
        {"value": "1/3"}, sort_keys=True, separators=(",", ":")).encode("ascii")
    (line,) = [json.loads(x) for x in (run / "GATES.jsonl").read_bytes().splitlines()]
    assert (line["gate"], line["status"]) == ("G0", "PASS")
    assert line["files"] == {"STARTED": sha(gdir / "STARTED"),
                             "values.json": sha(gdir / "values.json")}
    assert xr.lineage_precheck(store)["status"] == INV  # run/ present
    dest = Path(xr.archive_attempt(store, "0058", ledger_entries=[{"k": 1}], logs=[log]))
    assert dest == store / "superseded" / "0058-a1" and not run.exists()
    entries = dict(ln.split("  ", 1)[::-1] for ln in
                   (dest / "SHA256SUMS").read_bytes().decode("ascii").splitlines())
    files = {p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file()}
    assert set(entries) == files - {"SHA256SUMS"}  # the manifest does not list itself
    assert all(sha(dest / rel) == h for rel, h in entries.items())
    assert {"run/gates/G0/values.json", "run/gates/G0/STARTED", "run/GATES.jsonl",
            "ledger_entries.json", "logs/m.log"} <= set(entries)
    assert xr.lineage_precheck(store)["status"] == "PASS"
    same, bad, empty = tmp_path / "rerun", tmp_path / "bad", tmp_path / "empty"
    xr.write_marker(same, "G0")
    xr.write_gate(same, "G0", "PASS", {"value": F(1, 3), "wall_s": 9.0, "utc": "later"})
    assert xr.compare_attempt(dest, same)["status"] == "PASS"  # volatile fields excluded
    xr.write_marker(bad, "G0")
    put(bad / "gates" / "G0" / "values.json", b'{"value":"1/4"}')  # one byte differs
    res = xr.compare_attempt(dest, bad)
    assert res["status"] == INV and list(res["mismatch"])
    assert xr.compare_attempt(dest, bad, affected=("G0",))["status"] == "PASS"
    empty.mkdir()
    assert xr.compare_attempt(dest, empty)["status"] == "PASS"  # not yet produced: missing only
    xr.write_marker(run, "G0")
    assert Path(xr.archive_attempt(store, "0058")) == store / "superseded" / "0058-a2"
    a = {"x": 1, "cpu_s": 1, "wall_s": 2, "utc": "u", "started_utc": "s", "store": "p",
         "sub": {"log_path": "a", "tmp_dir": "b", "y": F(1, 2), "timestamp": 3}}
    b = {"x": 1, "cpu_s": 7, "wall_s": 8, "utc": "v", "started_utc": "t", "store": "q",
         "sub": {"log_path": "c", "tmp_dir": "d", "y": F(1, 2), "timestamp": 4}}
    assert xr.strip_volatile(a) == {"x": 1, "sub": {"y": F(1, 2)}}
    assert xr.reports_equal(a, b) and not xr.reports_equal(a, {**b, "x": 2})


def test_17_eta1_markers_manifests(tmp_path):  # section 10.4 test 17
    assert tuple(xm.flux(xm.build_world(), xm.edge_labels("ETA1"))) == C  # NA's flux
    for y in range(3):
        u, d = w_tokens("W1", "U", y), w_tokens("W1", "D", y)
        qu, qd = xm.closed_form("ETA1", u)["q"], xm.closed_form("ETA1", d)["q"]
        assert list(qu) == list(qd) == filt(lift("ETA1"), emis(), u)[0][-1]
        assert list(qu)[15:] == [F(1, 15)] * 3
        assert list(xm.closed_form("NA", u)["q"]) != list(xm.closed_form("NA", d)["q"])
    layer = layer_at("ETA1", 7)  # one Parikh class at N(a*) holds two holonomies ...
    cls = xd.classes(layer, "Parikh")[(6, (1, 0, 1, 0))]
    assert all(xd.ambiguous(cls, y) for y in range(3)) and set(cls) >= {C, C2}
    assert all(list(xm.point_law(m, z, eta=F(1))) == [F(1, 3)] * 3  # ... with equal laws
               for m in range(1, 9) for z in range(3))  # hence q* = q_H1 = q_Parikh
    store = tmp_path / "s0"
    put(store / "run" / "preflight.json", b"{}")
    assert xr.s0_lineage(store)["status"] == "PASS"
    for extra in ("GATES.jsonl", "gates/PF/STARTED", "gates/S0/values.json", "gates/"):
        target = store / "run" / extra
        target.mkdir() if extra.endswith("/") else put(target)
        assert xr.s0_lineage(store)["status"] == INV, extra
        shutil.rmtree(store / "run" / "gates", ignore_errors=True)
        (store / "run" / "GATES.jsonl").unlink(missing_ok=True)
    assert xr.s0_lineage(store)["status"] == "PASS"
    st = tmp_path / "lin"
    att = st / "superseded" / "0058-a1"
    f = put(att / "run" / "preflight.json", b"{}")
    put(att / "SHA256SUMS", f"{sha(f)}  run/preflight.json\n".encode("ascii"))
    assert xr.lineage_precheck(st)["status"] == "PASS"  # the manifest need not hash itself
    rel = "superseded/0058-a1/run/preflight.json"
    f.write_bytes(b"{ }")
    res = xr.lineage_precheck(st)
    assert res["status"] == INV and rel in list(res["mismatch"])
    f.unlink()
    res = xr.lineage_precheck(st)
    assert res["status"] == INV and rel in list(res["missing"])
    put(f, b"{}")
    assert xr.lineage_precheck(st)["status"] == "PASS"
    shutil.copytree(att, st / "superseded" / "0058-b1")  # not a recorded attempt name
    assert xr.lineage_precheck(st)["status"] == INV
