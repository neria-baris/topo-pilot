"""Author B, job 0120: the X6ZC synthetic dry run (PROTOCOL_X6ZC_v1 §12-§14; API.md §11, §15;
TEST_PLAN.md §4), report schema, stage-1 no-write check, EXPOSURE/EVALUATIONS, ledger, pauses.
Synthetic data only; planted predictors are described at class Planted."""
from __future__ import annotations
import copy
import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path
import numpy as np
import pytest
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6zc"))
import x6zc_core as zc  # noqa: E402
import x6zc_census as zs  # noqa: E402
import x6zc_run as zr  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_data as sd  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6s1_stats as ss  # noqa: E402
from topo_pilot.contracts import SeedTree, canonical_json  # noqa: E402
VO, FAMS, B_TEST, CO = ("PP", "MM", "PM", "MP"), ("W2", "W1"), 500, ("P", "S3", "S4")
F5, F20, R6 = Fr(1, 5), Fr(1, 20), "ZC_NOT_COMMUTATIVE/NOT_REPLICATED"
KAPPA = {"kappa_a": Fr(17, 20), "kappa_b": Fr(11, 20)}
CC = json.loads((REPO / "tools/x6zc/CONTRACT.json").read_text("utf-8"))["constants"]
PATHS = {}  # vertex path after the cue -> (family, variant, member), from CONTRACT data
for _v in VO:
    for _m, _lets, _w1 in zip("ab", CC["variants"]["W2"][_v], CC["variants"]["W1"][_v]):
        _loops = xe.LOOPS[_lets[0]] + xe.LOOPS[_lets[1]]
        _w2 = tuple(CC["w2_scaffold"]["head"]) + _loops + tuple(CC["w2_scaffold"]["tail"])
        PATHS[_w2], PATHS[tuple(_w1)] = ("W2", _v, _m), ("W1", _v, _m)
UTC = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
_syn, _ZC, _ZMEMO, _STATS = zc.SyntheticPredictor, se.OraclePredictor("ZC", "qstar"), {}, {}
# API-AMBIGUITY: unplanted focal cells read q*_ZC: beta_PP = 0 in every draw, all r draws undefined
def _pool(seed, rows=4096):  # random legal walks; cue 15 + y (y uniform) at anchor visits
    g, out = np.random.default_rng(seed), np.zeros((rows, 33), np.uint8)
    for r in range(rows):
        v = int(g.choice([i for i in range(16) if i != xm.ANCHOR]))  # first token: a vertex
        for k in range(33):
            v = xm.NEIGHBOURS[v][int(g.integers(0, 5))] if k else v
            out[r, k] = 15 + int(g.integers(0, 3)) if v == xm.ANCHOR else xm.tok(v)
    return out
def _yield_rows(pool):  # the author's natural_prefixes rule without the 1,024 cap
    rnd, nb, rows = SeedTree(sd.DATA_MASTER).generator("x6s1", "prefix_len"), xm.ANCHOR_NB, []
    for r, row in enumerate(pool):
        lmax = int(rnd.integers(1, 15))
        if any(xm.vertex(int(row[L - 1])) in nb | {xm.ANCHOR} for L in range(1, lmax + 1)):
            rows.append(r)
    return rows
def _jit(prefixes, seed):
    keys = sorted(set(prefixes))
    u = np.random.default_rng(seed).uniform(-0.1, 0.1, len(keys))
    cnt = np.array([prefixes.count(k) for k in keys], np.float64)
    u -= (cnt * u).sum() / cnt.sum()  # centred over the prefix rows; |u| <= 1/5
    return {k: 1.0 + float(x) for k, x in zip(keys, u)}
def _info(row, t):  # (family, variant, member, prefix tokens)
    p = xm.parse([int(w) for w in row[:t]])
    return PATHS[tuple(p["segment"][1:])] + (tuple(int(w) for w in p["prefix"]),)
def _ts(tokens, t):
    tok = np.asarray(tokens)
    return tok, np.broadcast_to(np.asarray(t, np.int64), (len(tok),)).copy()
def _rows(pred, tok, ts, memo):
    keys = [(bytes(r[:k]), int(k)) for r, k in zip(tok, ts)]
    miss = [i for i, k in enumerate(keys) if k not in memo]
    for i, row in zip(miss, pred(tok[miss], ts[miss]) if miss else []):
        memo[keys[i]] = np.array(row, np.float64)
    return np.array([memo[k] for k in keys], np.float64).reshape(len(keys), 18)
class Fn:  # a named predictor from a function of (tokens, t)
    def __init__(self, name, fn):
        self.name, self.fn = name, fn
    def __call__(self, tokens, t):
        return self.fn(*_ts(tokens, t))
class Planted:
    """p = Z + sum_k f_k(prefix)(P_k - Z), Z = q*_ZC, P_k a SyntheticPredictor; equal cue masses
    scale each numerator by f_k = 1 + u, u in [-1/5, 1/5] centred: exact points, wide intervals."""
    def __init__(self, name, comps):
        self.name, self.comps, self.memo = name, comps, [{} for _ in comps]
    def __call__(self, tokens, t):
        tok, ts = _ts(tokens, t)
        z = _rows(_ZC, tok, ts, _ZMEMO)
        out, info = z.copy(), [_info(r, k) for r, k in zip(tok, ts)]
        for (sel, pred, wt), memo in zip(self.comps, self.memo):
            f = np.array([wt(i[3]) if {i[0], f"{i[0]}|{i[1]}"} & sel else 0.0 for i in info])
            idx = np.flatnonzero(f)
            if len(idx):
                out[idx] += f[idx, None] * (_rows(pred, tok[idx], ts[idx], memo) - z[idx])
        return out
def _partner(tok, ts):  # DR13: the other member of each pair, same prefix and cue
    part = np.zeros_like(tok)
    for i, (r, k) in enumerate(zip(tok, ts)):
        fam, v, m, pre = _info(r, k)
        other = next(p for p, x in PATHS.items() if x == (fam, v, "ab"[m == "a"]))
        h = pre + (int(r[len(pre)]),) + tuple(xm.tok(x) for x in other)
        part[i, :len(h)] = h
    return part
def _nudge(tok, ts):  # DR14: q*_ZC plus 1e-6 on token 15 for member a only, re-normalised
    p = _rows(_ZC, tok, ts, _ZMEMO).copy()
    p[[_info(r, k)[2] == "a" for r, k in zip(tok, ts)], 15] += 1e-6
    return p / p.sum(1)[:, None]
def _pl(W, model, *comps):  # comps: (selection, kind, jitter key or None, params)
    return {model: Planted(model, [(sel, _syn(kind, **par), lambda p, d=W.get(j, {}):
                                    d.get(p, 1.0)) for sel, kind, j, par in comps])}
FIX = {  # id: (planted, cell, outcome, b, exact r_v points, licence phrase); §12, TEST_PLAN §4
    "DR01": (lambda W: _pl(W, "ZC-s1", ({"W2|PP", "W2|MM", "W2|MP"}, "M0", "jit", {"w": F5}),
                           ({"W2|PM"}, "M0", "jit", {"w": 2 * F5})),
             "P", "UNEXPLAINED/NOT_NA_INVARIANT", 0.2, {"MM": 1, "PM": 2}, "matches neither"),
    "DR02": (lambda W: _pl(W, "ZC-s1", (set(FAMS), "M0", "jit", {"w": F5})), "P",
             "ZC_NOT_COMMUTATIVE/NA_DIRECTION", 0.2, dict.fromkeys(VO[1:], 1), "not explained"),
    "DR03": (lambda W: _pl(W, "ZC-s1", ({"W2"}, "M2a", "jit", {"pi_a": F20, "pi_b": F5 + F20})),
             "P", "ZC_NOT_COMMUTATIVE/ZC_COORDINATE", 0.2, {"MM": -1}, "reverses sign"),
    "DR04": (lambda W: _pl(W, "ZC-s3", ({"W1"}, "M2a", "jit", {"pi_a": F5 + F20, "pi_b": F20})),
             "S3", "ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION", 0.2, {"MM": -1}, "reverses sign"),
    "DR05": (lambda W: _pl(W, "ZC-s1", ({"W2"}, "M1", "jit", KAPPA)), "P",  # 0.3/(2 lam_18)
             "ZC_NOT_COMMUTATIVE/ZC_COORDINATE", 0.2157853202700327, {"MM": -1, "PM": 0},
             "reverses sign"),
    "DR06": (lambda W: {"ZC-s1": Planted("DR06", [({"W2"}, _syn("M0", w=F5),
                                                   lambda p: float(p in W["S"]))])},
             "P", R6, 0.0, {}, "did not replicate"),
    "DR07": (lambda W: _pl(W, "ZC-s1", ({"W2"}, "M0", "jit", {"w": F20})),
             "P", "UNEXPLAINED/WEAK_REPLICATION", 0.05, {}, "positive but below the 0.10"),
    "DR08": (lambda W: _pl(W, "ZC-s1", ({"W2"}, "M0", "jit", {"w": 3 * F20}),
                           ({"W2"}, "M2a", "jit2", {"pi_a": Fr(0), "pi_b": F20})), "P",
             "UNEXPLAINED/PARTIAL", 0.2, {"MM": 0.5, "PM": 0.875, "MP": 0.625}, "cannot be"),
    "DR10": (lambda W: {**FIX["DR03"][0](W), **_pl(W, "AB-s1", ({"W2"}, "M0", None, {"w": F5})),
                        **_pl(W, "ZC-s2", ({"W2"}, "M0", None, {"w": F5}))},
             "P", "UNEXPLAINED/FRESH_SET_UNSTABLE", 0.2, {"MM": -1}, "FRESH_SET_UNSTABLE")}
def _stats(key, w, planted, seed=20261026):  # B = 500 draws; models not planted read q*_ZC
    if key not in _STATS:
        outs = {m: zr.predict_variants(planted[m], w["arr"]) if m in planted else w["zc_out"]
                for m in zc.STAGE_B_ORDER}
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(zc, "B_DRAWS", B_TEST)
            mp.setattr(zr, "B_DRAWS", B_TEST, raising=False)
            _STATS[key] = zr.stage_c_statistics(outs, w["arr"], w["qfn"],
                                                np.random.default_rng(seed))
    return _STATS[key]
def _st(W, fid):
    return _stats(fid, W, FIX[fid][0](W))
def _ev(**kw):
    ev = {"k0": "PASS", "incomplete": False, "rulings": [], "k1": "PASS", "a2_k5_pass": True,
          "checks": dict.fromkeys(("A1", "A2", "A_audit", "K2", "K4", "K5"), "PASS"),
          "n_avail": 2400, "k6": {"W2": True, "W1": True},
          "b9": {"n": 1024, "status": "OK", "candidates": [1024, 2048, 2400], "h": {},
                 "underpowered": dict.fromkeys(CO, False), "low_feasibility": ["S3"]},
          "f1": {F: {"m0_ok": True, "passed": True, "failed": []} for F in FAMS}}
    return {**ev, **kw}
def _out(rep, cell="P"):
    return rep["decision"]["cells"][cell]["outcome"]
def _lic(rep, cell="P"):  # a licence with an unfilled placeholder reads as None
    return None if set("{}") & set(rep["licences"][cell]) else rep["licences"][cell]
def _world(fresh):
    arr = {F: zc.variant_arrays(fresh, F) for F in FAMS}
    w = {"arr": arr, "qfn": zc.QStarCache.build([arr["W2"], arr["W1"]])}
    return {**w, "zc_out": zr.predict_variants(Planted("ZC", []), arr)}
@pytest.fixture(scope="module")
def W():
    pool = _pool(2026102601)
    D = sp.designed_set(pool)
    fr = zc.fresh_prefixes(pool, D["prefixes"])
    fresh = [tuple(int(x) for x in p) for _, p in fr["fresh"]]
    d_only = {tuple(int(x) for x in p) for _, p in D["prefixes"]} - set(fresh)
    return {"pool": pool, "D": D, "fr": fr, "fresh": fresh, "S": d_only, **_world(fresh[:128]),
            "jit": _jit(fresh[:128], 5), "jit2": _jit(fresh[:128], 6)}
@pytest.mark.parametrize("fid", sorted(FIX))
def test_planted_fixture_outcomes(W, fid):
    _, cell, outcome, b, r, phrase = FIX[fid]
    s = _st(W, fid)
    c = s["cells"][cell]
    assert c["b"] == pytest.approx(b, abs=1e-12)
    for v, x in r.items():
        assert c["r"][v]["point"] == pytest.approx(x, abs=1e-9)
    rep = zr.decide_report(s, _ev())
    assert _out(rep, cell) == outcome and phrase in _lic(rep, cell)
    assert all(_out(rep, x) == R6 for x in CO if x != cell)  # unplanted focal: q*_ZC, b = 0
def test_planted_fixture_details(W):
    s = _st(W, "DR02")  # NA_BOTH_FAMILIES; K6 W1 holds with 9 of 10 controls within 0.10
    assert s["cells"]["P"]["r_w1_p"]["label"] == "NA_BOTH_FAMILIES" and s["k6"]["W1"]
    rep = zr.decide_report(s, _ev())
    q, rv = rep["qualifiers"], rep["reuse_verdict"]
    assert q["P"][0] == "ORIGIN_UNRESOLVED" and "NA_BOTH_FAMILIES" in q["P"]
    assert "LOW_FEASIBILITY(S3)" in q["S3"] and {2, 3} <= set(rv["amendments"])
    assert (rv["axis1"], rv["axis2"]) == ("VALID", "UNDETERMINED")
    rv = zr.decide_report(_st(W, "DR03"), _ev())["reuse_verdict"]
    assert (rv["axis1"], rv["axis2"], list(rv["amendments"]), rv["amendment_1_mark"]) == (
        "VALID", "FIT_WITH_AMENDMENT", [1, 2, 3, 4], None)
    assert rv["statement"] == zc.CONTRACT["reuse"]["statement"]
    assert _st(W, "DR01")["cells"]["P"]["r"]["PM"]["lo"] > 1.5
    assert _st(W, "DR03")["cells"]["P"]["r"]["MM"]["hi"] < 0
    assert float(Fr(3, 10) / (2 * xm.lam(18))) == pytest.approx(FIX["DR05"][3], abs=1e-15)
    c = _st(W, "DR06")["cells"]["P"]  # fresh: exactly q*_ZC; D's W2: M0 on D-only prefixes
    assert c["b_lo"] == c["b_hi"] == 0.0
    A = {k: v[:900] for k, v in sp.designed_arrays(W["D"]).items() if k.startswith("W2_")}
    t = zc.pair_arrays(FIX["DR06"][0](W)["ZC-s1"], A, "W2", lambda tk, u: se.qstar("NA", tk, u))
    k = sum(tuple(int(x) for x in p) in W["S"] for _, p in W["D"]["prefixes"][:300])
    assert 0.10 < se.beta_fsum(t["num"], t["den"]) == pytest.approx(0.2 * k / 300, abs=1e-12)
    rep = zr.decide_report(_st(W, "DR07"), _ev())  # positive case: b_lo > 0 and b < 0.10
    assert rep["decision"]["cells"]["P"]["licence_case"] == "positive"
    c = _st(W, "DR08")["cells"]["P"]  # independent factors for w and pi: not degenerate
    assert c["r"]["MM"]["lo"] < 0.5 < c["r"]["MM"]["hi"]
    s = _st(W, "DR10")
    assert sum(abs(s["point"][(m, "W2", "PP")]) <= 0.1 for m in zc.K6_CONTROLS["W2"]) == 9
    assert not s["k6"]["W2"] and s["k6"]["W1"]
def test_dr09_unstable_ratio():  # planted at the statistics level (API C-50, R-0117-1)
    P, pp, s3 = 128, np.r_[-9.8, np.full(127, 0.3)], (-0.3, 0.3, -0.15, 0.15)
    plant = {("ZC-s1", "W2"): (pp, 0.3, 0.3, 0.3), ("ZC-s1", "W1"): (0.3,) * 4,
             ("ZC-s3", "W1"): s3, ("ZC-s4", "W1"): s3}
    num = {f"{m}|{F}|{v}|beta": np.broadcast_to(np.asarray(x, np.float64), (P,)).copy()
           for (m, F), vals in plant.items() for v, x in zip(VO, vals)}
    draws = zc.paired_cluster_boot(num, {k: np.ones(P) for k in num}, 5000,
                                   np.random.default_rng(1))
    point = {tuple(k.split("|")[:3]): math.fsum(num[k]) / P for k in num}
    cells = {c: zc.cell_statistics(point, draws, c) for c in CO}
    c = cells["P"]
    assert c["b"] == pytest.approx(28.3 / 128, abs=1e-12)  # 0.2211
    assert c["b_lo"] > 0.05 and c["undefined_frac"] > 0.01  # the preconditions
    rep = zr.decide_report({"point": point, "draws": draws, "cells": cells, "beta_y": {}, "rho": {},
                            "k6": {"W2": True, "W1": True, "values": {}}, "n_clusters": P}, _ev())
    assert _out(rep) == "UNEXPLAINED/UNSTABLE_RATIO"
    assert _out(rep, "S3") == _out(rep, "S4") == "ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION"
def test_dr11_dr12_sizing(W):
    rows = _yield_rows(W["pool"])
    assert W["fr"]["r_star"] == rows[1023] and not W["fr"]["not_enough_data"]
    short = W["pool"][:rows[1279] + 1]  # DR11: truncated after its 1,280th yield
    fr = zc.fresh_prefixes(short, sp.designed_set(short)["prefixes"])
    fresh = [tuple(int(x) for x in p) for _, p in fr["fresh"]]
    assert fr["n_avail"] == 256 and fr["not_enough_data"] and fresh == W["fresh"][:256]
    b9 = zc.choose_n(256, {"P": 0.01, "S3": 0.01, "S4": 0.01})
    assert b9["status"] == "NOT_ENOUGH_DATA" and b9["n"] == 256 and len(fresh) == 256
    s = _stats("DR11", _world(fresh), _pl(W, "ZC-s1", (set(FAMS), "M0", None, {"w": F5})))
    rep = zr.decide_report(s, _ev(n_avail=256, b9=b9))
    for c in CO:
        assert _out(rep, c) == "UNEXPLAINED/NOT_ENOUGH_DATA" and "(descriptive)" in _lic(rep, c)
        assert rep["decision"]["cells"][c]["descriptive"] and "DESCRIPTIVE" in rep["qualifiers"][c]
    h = 2.394 * math.sqrt(2) * 0.05 * math.sqrt(1030 / 2400) / (0.20930750050575797 - 0.1)
    b9 = zc.choose_n(2400, {"P": 0.05, "S3": 0.001, "S4": 0.001})  # DR12: no n qualifies
    assert h > 0.25 and b9["status"] == "UNDERPOWERED" and b9["n"] == 2400
    assert b9["underpowered"]["P"] and not (b9["underpowered"]["S3"] or b9["underpowered"]["S4"])
    rep = zr.decide_report(_st(W, "DR02"), _ev(b9=b9))
    assert _out(rep) == "UNEXPLAINED/UNDERPOWERED" and rep["decision"]["cells"]["P"]["descriptive"]
    assert _out(rep, "S3") == R6
def test_dr13_14_15_global(W):
    A, base = {F: zc.variant_arrays(W["fresh"][:4], F) for F in FAMS}, _st(W, "DR02")
    sw = {k: Fn(k, lambda tk, ts, o=zc.oracle("NA", k): o(_partner(tk, ts), ts))
          for k in ("qstar", "h_last", "h_first", "h_rev")}
    refs = {k: zc.pair_arrays(p, A["W2"], "PP", W["qfn"]) for k, p in sw.items()}
    assert se.beta_fsum(refs["qstar"]["num"], refs["qstar"]["den"]) == pytest.approx(-1, abs=1e-12)
    k2 = zc.k2_check(refs, "W2")  # DR13 (API-AMBIGUITY: K5 per API.md cannot see this swap)
    assert k2["status"] == "FAIL" and "qstar" in k2["failed"]
    rul = [{"id": f"DR13-{c}", "check": c, "cause_identified": True, "affects_beta": True,
            "cause": "a/b swapped between p and q*"} for c in ("K2", "K5")]
    chk = {**_ev()["checks"], "K2": "FAIL", "K5": "FAIL"}
    for ev, rule, outcome, axis1 in (
        (_ev(checks=chk, rulings=rul), "G-R2", "DEFECT_FOUND", "NOT_FIT"),
        (_ev(k1="FAIL", a2_k5_pass=True), "G-R3", "ESTIMATOR_ARTIFACT/NON_INVARIANT", "NOT_FIT"),
        (_ev(k0="FAIL"), "G-R0", "STOP_REPLAN", "UNDETERMINED")):
        rep = zr.decide_report(base, ev)
        assert rep["decision"]["global_rule"] == rule and rep["reuse_verdict"]["axis1"] == axis1
        assert all(_out(rep, c) == outcome for c in CO)
    assert all(_lic(rep, c) == "" for c in CO)  # STOP_REPLAN: no statement
    k1 = zc.k1_check(zc.pair_arrays(Fn("nudge", _nudge), A["W2"], "PP", W["qfn"]))
    assert k1["status"] == "FAIL" and not k1["num_zero"]  # DR14: the K1 failure itself
    assert zc.oracle_geometry(A["W1"], "W1")["status"] == "PASS"  # DR15: the K0 violation
    g = zc.oracle_geometry({**A["W1"], "PM_b": A["W1"]["PM_a"].copy()}, "W1")
    assert g["status"] == "FAIL" and (g["counterexample"]["key"], g["counterexample"]["row"]) == (
        "PM", 0)
def test_dr16_dr17_mixtures_and_swaps(W):
    A = {F: zc.variant_arrays(W["fresh"][:4], F) for F in FAMS}
    for d in (Fr(0), F20, 2 * F20, F5, 5 * F20, Fr(1)):  # DR16: beta = delta exactly
        pred = _syn("mixture", S="Parikh", delta=d)
        for F in FAMS:
            t = zc.pair_arrays(pred, A[F], "PP", W["qfn"])
            assert zc.beta_exact_pi0(pred.exact, F, "PP") == d
            assert abs(se.beta_fsum(t["num"], t["den"]) - float(d)) <= 1e-12
    pred = _syn("M0+M2a", w=3 * F20, pi_a=Fr(0), pi_b=F20)  # DR17
    t = zc.pair_arrays(pred, A["W2"], "PM", W["qfn"])
    assert zs.k5_swap(t)["status"] == "PASS"
    assert zs.k5_permutation(t, np.random.default_rng(7))["status"] == "PASS"
    joint = se.pair_terms(t["p_b"], t["p_a"], t["q_b"], t["q_a"])[0]
    pred_only = se.pair_terms(t["p_b"], t["p_a"], t["q_a"], t["q_b"])[0]
    assert np.array_equal(joint, t["num"]) and np.array_equal(pred_only, -t["num"])
    dup = {k: np.concatenate([v, v]) for k, v in A["W2"].items()}
    s1, s2 = zc.pair_stats(t), zc.pair_stats(zc.pair_arrays(pred, dup, "PM", W["qfn"]))
    assert abs(s1["beta"] - s2["beta"]) <= 1e-15 and abs(s1["rho"] - s2["rho"]) <= 1e-15
def test_dr18_dr19_rejections(W):
    A, qfn = zc.variant_arrays(W["fresh"][:4], "W2"), (lambda tk, t: se.qstar("NA", tk, t))
    for bad in ({**A, "PP_b": A["PP_b"][:-3]}, {**A, "PP_y": A["PP_y"][:-1]}):
        with pytest.raises(ValueError):
            zc.pair_arrays(zc.oracle("NA", "qstar"), bad, "PP", qfn)
    early = {**A, "PP_t": (A["PP_t"].astype(np.int64) - 1).astype(np.int16)}
    g = zc.oracle_geometry(early, "W2", keys=("PP",))
    # API-AMBIGUITY: the label of K0 item 2 in "counterexample"/"checks" is not fixed (int 2?)
    assert g["status"] == "FAIL" and str(g["counterexample"]["item"]) in ("2", "item2", "item 2")
    no_cue = Fn("no_cue", lambda tk, ts: np.pad(np.full((len(tk), 15), 1 / 15), ((0, 0), (0, 3))))
    t0 = zc.pair_arrays(no_cue, A, "PP", W["qfn"])  # DR19: zero cue mass -> NaN, never 0.0
    st = zc.pair_stats(t0)
    assert np.isnan(se.cue_normalise(t0["p_a"])).all() and st["nonfinite"]
    assert math.isnan(st["beta"])
    tz = zc.pair_arrays(zc.oracle("NA", "qstar"), A, "PP", lambda tk, t: se.qstar("ZC", tk, t))
    assert not tz["den"].any() and math.isnan(se.beta_fsum(tz["num"], tz["den"]))
    with pytest.raises(ValueError):  # non-finite draws: no interval (C-21 -> G-R1)
        zc.interval(np.full(50, np.nan), (0.025, 0.975))
    rep = zr.decide_report(_st(W, "DR02"), _ev(incomplete=True))  # -> G-R1
    assert all(_out(rep, c) == "INVALID" and _lic(rep, c) == "" for c in CO)
def test_dr22_random_init_models(W, tmp_path):
    import torch
    from topo_pilot.learner import TransformerLM
    preds = []
    for seed in (2026102611, 2026102612):
        torch.manual_seed(seed)
        preds.append(se.ModelPredictor.from_state(TransformerLM(sd.MODEL_CFG).state_dict(), "r"))
    kq, eps = np.arange(sd.Q + 1, dtype=np.float64), float(sd.EPS)
    qv = np.array([float(q) for q in ss.qvals()])  # cheap synthetic score tables for R_W2
    tables = {"lnp": np.log((1 - eps) * kq / sd.Q + eps / 18), "fl_q": qv,
              "qlnq": np.where(qv > 0, qv * np.log(np.where(qv > 0, qv, 1.0)), 0.0)}
    sub = {k: v if k.startswith("W3") else v[:192] for k, v in sp.designed_arrays(W["D"]).items()}
    cache = zc.QStarCache.build([sub])
    for m in preds:  # the first 64 prefixes of the synthetic D, through designed_stats
        ds = se.designed_stats(m, sub, cache, tables)
        assert not ds["nonfinite"] and math.isfinite(ds["beta_W2"]) and math.isfinite(ds["beta_W1"])
        o = zr.predict_variants(m, W["arr"])
        for p in (p for F in FAMS for v in VO for p in o[F][v]):
            assert p.shape == (384, 18) and np.isfinite(p).all()
            assert np.abs(p.sum(1) - 1).max() <= 1e-12
    s = _stats("DR22", W, {m: preds[i % 2] for i, m in enumerate(zc.STAGE_B_ORDER)})
    assert {"point", "beta_y", "rho", "draws", "cells", "k6", "n_clusters"} <= set(s)
    assert s["n_clusters"] == 128 and all(math.isfinite(x) for x in s["point"].values())
    (tmp_path / "cpu_ledger.json").write_text(json.dumps({"cumulative_cpu_s": 3 * 720 + 1}))
    cum = zr.ledger_cpu(str(tmp_path))
    assert cum == 2161 and zr.pause_check("0", cum, 0.0)["pause"]
def test_store_records(tmp_path):  # stage-1 no-write check, EXPOSURE/EVALUATIONS, pause record
    st, zx = tmp_path / "x6-stage1-store", tmp_path / "x6zc-store"
    (st / "sealed").mkdir(parents=True)
    zx.mkdir()
    (st / "pool.npz").write_bytes(b"\0" * 7)
    (st / "sealed" / "zc_s1.json").write_bytes(b"x")
    inv = zr.x6s1_inventory(str(st))
    assert {k: list(v) for k, v in inv.items()} == {
        "pool.npz": [7, os.stat(st / "pool.npz").st_mtime_ns],
        "sealed/": [0, os.stat(st / "sealed").st_mtime_ns]}
    e1 = zr.log_exposure(str(zx), "A", "pool.npz", "0" * 64, "A3")
    e2 = zr.log_exposure(str(zx), "A", "tables/designed.npz", None, "A-audit")
    (st / "pool.npz").read_bytes()  # a read is not a write
    assert zr.inventory_equal(inv, zr.x6s1_inventory(str(st)))
    os.utime(st / "sealed", ns=(1, 1))  # what adding a file under sealed/ does
    assert not zr.inventory_equal(inv, zr.x6s1_inventory(str(st)))
    lines = (zx / "EXPOSURE.jsonl").read_text("utf-8").splitlines()
    assert [json.loads(x) for x in lines[-2:]] == [e1, e2]
    assert all(x == canonical_json(json.loads(x)) for x in lines)
    assert len(lines) == 2 or json.loads(lines[0])["id"] == "E0-PREFIX-READ"
    assert [(e["store"], e["stage"], e["artifact"]) for e in (e1, e2)] == [
        ("x6-stage1-store", "A", "pool.npz"), ("x6-stage1-store", "A", "tables/designed.npz")]
    assert all(re.fullmatch(r"X\d+", e["id"]) and UTC.match(e["utc"]) for e in (e1, e2))
    assert int(e2["id"][1:]) > int(e1["id"][1:]) and e2["expected_sha256"] is None
    want = [("ZC-s1", "designed_D", "B", "D"), ("ZC-s1", "fresh_variants", "C", "fresh")]
    for w in want:
        zr.log_evaluation(str(zx), *w)
    ev = [json.loads(x) for x in (zx / "EVALUATIONS.jsonl").read_text("utf-8").splitlines()]
    assert [(e["model"], e["kind"], e["stage"], e["set"]) for e in ev] == want
    with pytest.raises(RuntimeError):
        zr.guard("B", "fresh")
    pc = zr.pause_check("C", 21195.5, 100.0, n=128)  # C_any: 19,980 + 9.4921875 n
    assert pc["pause"] and not zr.pause_check("C", 21195.0, 1215.0, n=128)["pause"]
    rec = {"stage": "C", "head": "0" * 40, "env_local": {}, "env_diff": [], "gates": {},
           "values": {}, "inventory": {"equal": True}, "cpu_s": 100.0, "pause": pc,
           "cpu_cumulative_s": 21195.5, "stop": "PAUSE", "utc": "2026-10-26T00:00:00Z"}
    path = Path(zr.write_stage(str(zx), "C", rec))
    data = path.read_bytes()  # the pause record
    assert path == zx / "stages" / "C" / "record.json" and json.loads(data)["pause"]["pause"]
    line = json.loads((zx / "STAGES.jsonl").read_text("utf-8").splitlines()[-1])
    assert (line["stage"], line["stop"]) == ("C", "PAUSE") and UTC.match(line["utc"])
    assert line["record_sha256"] == hashlib.sha256(data).hexdigest()
    with pytest.raises(FileExistsError):
        zr.write_stage(str(zx), "C", rec)
def test_report_schema_from_pipeline(W):  # API §11.6 keys; cells from the DR03 pipeline output
    s, ev = _st(W, "DR03"), _ev()
    rep = zr.decide_report(s, ev)
    dec, x = rep["decision"], s["cells"]
    ck = ("model family rule outcome not_licensed b b_interval beta_pp r undefined_frac beta_sb n "
          "descriptive").split()  # API §11.6 cell keys; values from the pipeline
    cells = {c: {**dict.fromkeys(ck), **{k: v for k, v in {**x[c], **dec["cells"][c]}.items()
                                          if k in ck},
                 "licence": rep["licences"][c], "qualifiers": rep["qualifiers"][c]} for c in CO}
    top = ("r_w1_p k6 f1 k0 coupling stage_b descriptive exposure sensitivity follow_up budget "
           "n n_avail r_star stages env head").split()
    good = {**dict.fromkeys(top, {}), "schema": "x6zc-report-v1", "protocol_id": zc.PROTOCOL_ID,
            "protocol_sha256": zc.PROTOCOL_SHA256, "x6zc_master": zc.X6ZC_MASTER, "cells": cells,
            "outcome": dec["headline"], "global_rule": dec["global_rule"],
            "reuse_verdict": rep["reuse_verdict"], "x6s1_statement": zc.CONTRACT["x6s1_statement"]}
    assert dec["headline"] == "ZC_NOT_COMMUTATIVE/ZC_COORDINATE" and zr.validate_report(good) == []
    bogus, stop = copy.deepcopy(good), copy.deepcopy(good)
    bogus["cells"]["P"]["outcome"] = "ZC_NOT_COMMUTATIVE/BOGUS"
    stop["cells"]["P"].update(outcome="STOP_REPLAN", licence="a statement")
    for bad in ({k: v for k, v in good.items() if k != "cells"}, bogus, stop):
        assert zr.validate_report(bad) != []
