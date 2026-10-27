"""Author A (job 0120): X6ZC decision rules (§9.1, every branch and its precedence, G-R0 first),
licences, qualifiers, reuse verdict, report schema, K4 tiers, the 0.10 band, the §13 pause points
and the stage-1 store guards (TEST_PLAN.md §3). Written from the protocol copy, API.md,
CONTRACT.json, TEST_PLAN.md and the 0117 review only (tools/x6zc/*.py never read). Evidence
records are synthetic dicts built here; stores are tmp_path directories (never a project store)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6zc"))
import x6zc_core as zc  # noqa: E402
import x6zc_census as zs  # noqa: E402
import x6zc_run as zr  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "x6zc" / "CONTRACT.json").read_text("utf-8"))
CELLS, SIGN = ("P", "S3", "S4"), {"P": 1, "S3": -1, "S4": -1}
NA_DIR, ZC_COORD = "ZC_NOT_COMMUTATIVE/NA_DIRECTION", "ZC_NOT_COMMUTATIVE/ZC_COORDINATE"
NOT_NA_DIR, NOT_REP = "ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION", "ZC_NOT_COMMUTATIVE/NOT_REPLICATED"
PARTIAL, NOT_NA_INV = "UNEXPLAINED/PARTIAL", "UNEXPLAINED/NOT_NA_INVARIANT"
WEAK, FRESH = "UNEXPLAINED/WEAK_REPLICATION", "UNEXPLAINED/FRESH_SET_UNSTABLE"
PRIME = ("'", "′")  # API-AMBIGUITY: CONTRACT writes G-R2' and R9'; API prose writes ′
BAND, F1_OK = (0.9, 1.1), {"m0_ok": True, "passed": True, "failed": []}
LV = {"model": "ZC-s1", "family": "W2", "n": 1024, "beta_d3": "0.209", "b_label": "β_PP",
      "b": "0.2000", "beta_pp": "0.2000", "lo": "0.1500", "hi": "0.2500", "level": "95", "k": 7,
      "exceptions": "", "r_mm": "-1.0000", "r_pm": "0.0000", "r_mp": "0.0000", "r_values": "(1, 2)",
      "intervals": "[0.9000, 1.1000]", "upper": "0.3000", "predictor": "set_constant",
      "value": "0.2093", "defect": "f.py, line 1, effect e", "corrected": "0.0000", "outcome": "",
      "descriptive": " (descriptive)", "numbers": "b = 0.2000", "cell": "P"}

def cell(c="P", b=0.2, lo=0.15, hi=0.25, und=0.0, mm=BAND, pm=BAND, mp=BAND, label=None):
    """Cell statistics in the API §8 cell_statistics layout; b is already σ·β_PP."""
    r = {v: {"point": (a + z) / 2, "lo": a, "hi": z} for v, (a, z) in zip(("MM", "PM", "MP"),
                                                                            (mm, pm, mp))}
    s = {"b": b, "b_lo": lo, "b_hi": hi, "beta_pp": SIGN[c] * b, "undefined_frac": und, "r": r,
         "beta_sb": {"point": 0.1, "lo": 0.0, "hi": 0.2}}
    if c == "P":
        s["r_w1_p"] = {"point": 1.0, "lo": 0.8, "hi": 1.2, "undefined_frac": 0.0, "label": label}
    return s

def ev(**kw) -> dict:  # API §9.1 evidence: every check PASS, every cell NA_DIRECTION-shaped
    e = {"k0": "PASS", "incomplete": False, "rulings": [], "k1": "PASS", "a2_k5_pass": True,
         "checks": dict.fromkeys(("A1", "A2", "A_audit", "K2", "K5", "K4"), "PASS"),
         "n_avail": 2400, "k6": {"W2": True, "W1": True}, "cells": {c: cell(c) for c in CELLS},
         "b9": {"n": 1024, "status": "OK", "candidates": [1024, 2048, 2400], "h": {},
                "underpowered": dict.fromkeys(CELLS, False), "low_feasibility": ["S3"]},
         "f1": {"W2": dict(F1_OK), "W1": dict(F1_OK)}}
    return {**e, **kw}

def ruling(check, ident=True, aff=True, rid="D1") -> dict:
    return {"id": rid, "check": check, "cause_identified": ident, "affects_beta": aff,
            "cause": "synthetic"}

def failed(check, status="FAIL", **kw) -> dict:  # ev with one failed check and its ruling
    e = ev(rulings=[ruling(check, **kw)])
    e["checks"][check] = status
    return e

def with_cell(c="P", **kw) -> dict:
    e = ev()
    e["cells"][c] = cell(c, **kw)
    return e

def outs(d) -> dict:
    return {c: d["cells"][c]["outcome"] for c in CELLS}

def ro(e, c="P") -> tuple:
    x = zc.decide_x6zc(e)["cells"][c]
    return x["rule"], x["outcome"]

def test_global_precedence_g_r0_first():
    e = ev(k0="FAIL", incomplete=True, k1="FAIL", rulings=[ruling("K4")])
    e["checks"]["K4"] = "DEFECT_CANDIDATE"
    d = zc.decide_x6zc(e)
    assert d["global_rule"] == "G-R0" and d["global_outcome"] == d["headline"] == "STOP_REPLAN"
    assert set(outs(d).values()) == {"STOP_REPLAN"} and zc.licence("STOP_REPLAN", LV) == ""
    assert zc.decide_x6zc(ev(k0="FAIL"))["global_rule"] == "G-R0"

def test_g_r1_invalid():
    for e in (ev(incomplete=True), ev(incomplete=True, k1="FAIL")):  # G-R1 before G-R3
        d = zc.decide_x6zc(e)
        assert d["global_rule"] == "G-R1" and set(outs(d).values()) == {"INVALID"}
        assert d["headline"] == "INVALID"

@pytest.mark.parametrize("chk", ["K4", "A1", "A2", "A_audit", "K2", "K5"])
def test_g_r2_defect_found(chk):
    e = failed(chk, "DEFECT_CANDIDATE" if chk in ("K4", "K5") else "FAIL")
    d = zc.decide_x6zc(e)
    assert d["global_rule"] == "G-R2" and set(outs(d).values()) == {"DEFECT_FOUND"}
    if chk in ("A1", "K2"):  # G-R2 before G-R3 (A2 and K5 still pass)
        assert zc.decide_x6zc({**e, "k1": "FAIL"})["global_rule"] == "G-R2"

def test_g_r2_prime_irreproducible():
    d = zc.decide_x6zc(failed("K2", ident=False, aff=False))
    assert d["global_rule"] in tuple("G-R2" + p for p in PRIME)
    assert set(outs(d).values()) == {"UNEXPLAINED/IRREPRODUCIBLE"}

def test_defect_elsewhere_does_not_preempt():
    e = failed("A1", ident=True, aff=False, rid="D1")
    d = zc.decide_x6zc(e)
    assert d["global_rule"] is None and d["defect_elsewhere"] == ["D1"]
    assert outs(d) == dict.fromkeys(CELLS, NA_DIR)
    q = zc.qualifiers(e, d, None)
    assert all("DEFECT_ELSEWHERE(D1)" in q[c] for c in CELLS)

@pytest.mark.parametrize("chk,status", [("K2", "DEFECT_CANDIDATE"), ("K2", "FAIL"),
                                        ("K4", "DEFECT_CANDIDATE")])
def test_missing_ruling_raises(chk, status):
    e = ev()
    e["checks"][chk] = status
    with pytest.raises(ValueError):
        zc.decide_x6zc(e)

def test_g_r3_non_invariant():
    d = zc.decide_x6zc(ev(k1="FAIL"))
    assert d["global_rule"] == "G-R3"
    assert set(outs(d).values()) == {"ESTIMATOR_ARTIFACT/NON_INVARIANT"}
    d = zc.decide_x6zc(ev(k1="FAIL", a2_k5_pass=False))  # G-R3 needs A2 and K5 passing
    assert d["global_rule"] is None and outs(d)["P"] == NA_DIR

def test_r4a_not_enough_data():
    e = ev(n_avail=300)
    e["b9"].update(status="NOT_ENOUGH_DATA", n=300, candidates=[])
    e["cells"] = {c: cell(c, mm=(-1.2, -0.8)) for c in CELLS}  # would satisfy R8
    d = zc.decide_x6zc(e)
    for x in d["cells"].values():
        assert (x["rule"], x["outcome"], x["descriptive"]) == (
            "R4a", "UNEXPLAINED/NOT_ENOUGH_DATA", True)
    q = zc.qualifiers(e, d, None)
    assert all("DESCRIPTIVE" in q[c] for c in CELLS)

def test_r4b_underpowered():
    e = ev()
    e["b9"].update(status="UNDERPOWERED", n=2400)
    e["b9"]["underpowered"]["P"] = True
    d = zc.decide_x6zc(e)
    p = d["cells"]["P"]
    assert (p["rule"], p["outcome"], p["descriptive"]) == ("R4b", "UNEXPLAINED/UNDERPOWERED", True)
    assert outs(d)["S3"] == outs(d)["S4"] == NA_DIR and not d["cells"]["S3"]["descriptive"]
    q = zc.qualifiers(e, d, None)
    assert "UNDERPOWERED(P)" in q["P"] and "DESCRIPTIVE" in q["P"]
    assert "UNDERPOWERED(S3)" not in q["S3"]

def test_r5_fresh_set_unstable():
    d = zc.decide_x6zc(ev(k6={"W2": False, "W1": True}))
    assert outs(d) == {"P": FRESH, "S3": NA_DIR, "S4": NA_DIR} and d["cells"]["P"]["rule"] == "R5"
    d = zc.decide_x6zc(ev(k6={"W2": True, "W1": False}))
    assert outs(d) == {"P": NA_DIR, "S3": FRESH, "S4": FRESH}

def test_r6_not_replicated():
    for lo in (-0.01, 0.0):  # lo(b) <= 0 includes 0.0 exactly
        assert ro(with_cell(b=0.02, lo=lo, hi=0.0999)) == ("R6", NOT_REP)
        assert ro(with_cell("S3", b=0.02, lo=lo, hi=0.0999), "S3") == ("R6", NOT_REP)
    assert ro(with_cell(b=0.02, lo=-0.01, hi=0.1)) == ("R7", WEAK)  # hi < 0.10 is strict

def test_r7_weak_replication_cases():
    # API-AMBIGUITY: API §9.2 compares Fraction(float(x)) with the bars, under which the float
    # 0.05 lies above 1/20 and the third case would not be R7. The protocol (lo(b) <= 0.05) and
    # TEST_PLAN expect R7 at b_lo = 0.05; this test follows them.
    for (b, lo, hi), case in (((0.05, 0.03, 0.07), "positive"), ((0.15, 0.04, 0.26), "ambiguous"),
                              ((0.12, 0.05, 0.2), "ambiguous"), ((0.08, -0.02, 0.18), "ambiguous")):
        x = zc.decide_x6zc(with_cell(b=b, lo=lo, hi=hi))["cells"]["P"]
        assert (x["rule"], x["outcome"], x["licence_case"], x["descriptive"]) == (
            "R7", WEAK, case, False)
    x = zc.decide_x6zc(with_cell(b=0.10, lo=0.06, hi=0.14))["cells"]["P"]
    assert (x["rule"], x["licence_case"]) == ("R9", None)  # b = 0.10 is not < 0.10

def test_r7b_unstable_ratio():
    assert ro(with_cell(b=0.2, lo=0.12, und=0.0101)) == ("R7b", "UNEXPLAINED/UNSTABLE_RATIO")
    # API-AMBIGUITY: 0.01 (= 50/5000 draws) is not "more than 1 %" (protocol §8); under the API's
    # Fraction(float(0.01)) > 1/100 it would fire. This test follows the protocol and TEST_PLAN.
    assert ro(with_cell(b=0.2, lo=0.12, und=50 / 5000)) == ("R9", NA_DIR)

def test_r8_zc_coordinate_and_w1():
    e = ev(cells={c: cell(c, mm=(-1.3, -1e-9)) for c in CELLS})
    d = zc.decide_x6zc(e)
    assert outs(d) == {"P": ZC_COORD, "S3": NOT_NA_DIR, "S4": NOT_NA_DIR}
    assert d["cells"]["P"]["rule"] == "R8" and d["headline"] == ZC_COORD
    assert ro(with_cell(mm=(-1.3, 0.0))) == ("R8b", NOT_NA_INV)  # hi < 0 is strict
    e = with_cell(mm=(-1.3, -1e-9))
    e["f1"]["W2"] = {"m0_ok": True, "passed": False, "failed": ["M1"]}
    assert ro(e) == ("R8", ZC_COORD)  # R8 does not need F1

def test_r8b_not_na_invariant():
    assert ro(with_cell(pm=(1.5000001, 2.0))) == ("R8b", NOT_NA_INV)
    assert ro(with_cell(pm=(1.5, 2.0))) == ("R10", PARTIAL)  # lo > 1.5 is strict
    assert ro(with_cell(mp=(0.3, 0.4999999))) == ("R8b", NOT_NA_INV)
    assert ro(with_cell("S4", mp=(0.3, 0.4999999)), "S4") == ("R8b", NOT_NA_INV)

def test_r9_na_direction():
    d = zc.decide_x6zc(ev())
    assert outs(d) == dict.fromkeys(CELLS, NA_DIR) and d["headline"] == NA_DIR
    assert all(d["cells"][c]["rule"] == "R9" for c in CELLS) and d["global_rule"] is None
    assert ro(with_cell(pm=(0.5, 1.2))) == ("R10", PARTIAL)  # 0.5 < lo is strict
    assert ro(with_cell(mm=(0.6, 1.5))) == ("R10", PARTIAL)  # hi < 1.5 is strict

def test_r9_prime_not_discriminable():
    e = ev()
    e["f1"]["W2"] = {"m0_ok": True, "passed": False, "failed": ["M1", "M4"]}
    d = zc.decide_x6zc(e)
    assert d["cells"]["P"]["rule"] in tuple("R9" + p for p in PRIME)
    assert outs(d) == {"P": "UNEXPLAINED/NOT_DISCRIMINABLE(M1, M4)", "S3": NA_DIR, "S4": NA_DIR}
    e = ev()
    e["f1"]["W1"] = {"m0_ok": True, "passed": False, "failed": ["M2a"]}
    nd = "UNEXPLAINED/NOT_DISCRIMINABLE(M2a)"
    assert outs(zc.decide_x6zc(e)) == {"P": NA_DIR, "S3": nd, "S4": nd}

def test_r10_partial():
    e = with_cell(b=0.2, lo=0.15, mm=(0.45, 0.55), pm=(0.8, 0.95), mp=(0.55, 0.7))
    assert ro(e) == ("R10", PARTIAL)

PHRASES = {ZC_COORD: "reverses sign", NOT_NA_DIR: "reverses sign", NOT_REP: "did not replicate",
           NA_DIR: "not explained by sign-symmetric Z₃ counting errors",
           PARTIAL: "cannot be excluded", NOT_NA_INV: "matches neither the NA oracle",
           "DEFECT_FOUND": "versioned corrected computation",
           "ESTIMATOR_ARTIFACT/NON_INVARIANT": "not invariant for set_constant"}
GENERIC = ("UNEXPLAINED/NOT_ENOUGH_DATA", "UNEXPLAINED/UNDERPOWERED", FRESH,
           "UNEXPLAINED/IRREPRODUCIBLE", "UNEXPLAINED/UNSTABLE_RATIO",
           "UNEXPLAINED/NOT_DISCRIMINABLE(M1, M4)")

def test_licences_filled():
    def ok(txt):
        return bool(txt) and "{" not in txt and "}" not in txt
    for o, ph in PHRASES.items():
        assert ok(txt := zc.licence(o, {**LV, "outcome": o})) and ph in txt
    for case, ph in (("positive", "positive but below the 0.10 placebo margin"),
                     ("ambiguous", "replication ambiguous")):
        assert ok(txt := zc.licence(WEAK, LV, case)) and ph in txt
    for o in GENERIC:  # the generic UNEXPLAINED/* row: the numbers only
        assert ok(txt := zc.licence(o, {**LV, "outcome": o})) and txt.startswith(o)
    # API-AMBIGUITY: licence() takes no cell; the cell (S3) and family (W1) are passed in values
    s3 = {**LV, "model": "ZC-s3", "family": "W1", "cell": "S3", "b_label": "−β_PP"}
    tail = "The four NA models' W1 r_v values are printed beside the cell."
    assert ok(zc.licence(NA_DIR, s3)) and zc.licence(NA_DIR, s3).endswith(tail)
    assert tail not in zc.licence(NA_DIR, LV) and zc.licence(NOT_NA_DIR, s3).endswith(tail)
    assert zc.licence("STOP_REPLAN", LV) == zc.licence("INVALID", LV) == ""
    for o in (ZC_COORD, NOT_NA_DIR, NA_DIR, PARTIAL, NOT_NA_INV, NOT_REP, "DEFECT_FOUND"):
        assert zc.not_licensed(o) == CONTRACT["not_licensed"][o]
    assert zc.not_licensed("UNEXPLAINED/UNDERPOWERED") == CONTRACT["not_licensed"]["UNEXPLAINED/*"]

def _q_case() -> tuple:  # P ZC_COORDINATE (W2_ONLY), S3 PARTIAL, S4 NA_DIRECTION, K4 ENV_DRIFT
    e = ev()
    e["cells"].update(P=cell("P", mm=(-1.3, -0.7), label="W2_ONLY"), S3=cell("S3", mm=(0.45, 0.55)))
    e["checks"]["K4"] = "ENV_DRIFT"
    return e, zc.decide_x6zc(e)

def test_qualifiers():
    e, d = _q_case()
    assert outs(d) == {"P": ZC_COORD, "S3": PARTIAL, "S4": NA_DIR}
    q = zc.qualifiers(e, d, None)
    assert q["P"][0] == "ORIGIN_UNRESOLVED" and "W2_ONLY" in q["P"]
    assert q["S4"][0] == "ORIGIN_UNRESOLVED" and "ORIGIN_UNRESOLVED" not in q["S3"]
    assert "LOW_FEASIBILITY(S3)" in q["S3"] and "LOW_FEASIBILITY(S3)" not in q["P"]
    assert all("ENV_DRIFT" in q[c] for c in CELLS) and "DESCRIPTIVE" not in q["P"]
    assert not any(x.startswith("READOUT_AMPLIFIED") for x in q["P"])

def test_qualifiers_census():
    # API-AMBIGUITY: API §9.4 does not define the census argument. Assumed layout: Stage-B
    # qualifiers per "<model>|<family>" and the sensitivity outcomes per line and cell.
    e, d = _q_case()
    census = {"qualifiers": {"ZC-s1|W2": ["READOUT_AMPLIFIED(ZC-s1, W2)"]},
              "sensitivity": {"A4": {"P": PARTIAL, "S3": PARTIAL, "S4": NA_DIR},
                              "DPREFIX": {"P": ZC_COORD, "S3": PARTIAL, "S4": NA_DIR}}}
    p, sens = zc.qualifiers(e, d, census)["P"], f"SENSITIVITY_A4({PARTIAL})"
    assert p[0] == "ORIGIN_UNRESOLVED"
    assert p.index("READOUT_AMPLIFIED(ZC-s1, W2)") < p.index("W2_ONLY") < p.index(sens)
    assert not any(x.startswith("SENSITIVITY_D_PREFIX") for x in p)  # same outcome: none

def test_reuse_verdict():
    st, mark = CONTRACT["reuse"]["statement"], CONTRACT["reuse"]["amendment_1_inconclusive_mark"]

    def rv(e, axes, amend=None):
        v = zc.reuse_verdict(e, zc.decide_x6zc(e))
        assert (v["axis1"], v["axis2"], v["statement"]) == axes
        assert amend is None or list(v["amendments"]) == amend
        return v
    for e in (failed("K2"), ev(k1="FAIL")):  # DEFECT_FOUND, NON_INVARIANT
        rv(e, ("NOT_FIT", "NOT_ASSESSED", None))
    for e in (failed("K2", ident=False, aff=False), ev(incomplete=True), ev(k0="FAIL")):
        rv(e, ("UNDETERMINED", "NOT_ASSESSED", None))
    e = ev()
    e["cells"].update(P=cell("P", mm=(-1.3, -0.7)), S3=cell("S3", mm=(-1.3, -0.7)),
                      S4=cell("S4", mm=(0.45, 0.55)))
    assert outs(zc.decide_x6zc(e)) == {"P": ZC_COORD, "S3": NOT_NA_DIR, "S4": PARTIAL}
    assert rv(e, ("VALID", "FIT_WITH_AMENDMENT", st), [1, 2, 3, 4])["amendment_1_mark"] is None
    rv(ev(), ("VALID", "UNDETERMINED", st), [2, 3])  # P NA_DIRECTION: axis 2 UNDETERMINED first
    e = ev(cells={c: cell(c, mm=(0.45, 0.55)) for c in CELLS})  # PARTIAL everywhere
    assert rv(e, ("VALID", "FIT_WITH_AMENDMENT", st), [1, 2, 3])["amendment_1_mark"] == mark
    rv(failed("A1", aff=False), ("VALID", "UNDETERMINED", st))  # DEFECT_ELSEWHERE: VALID (C-18)

TOP = ("schema", "protocol_id", "protocol_sha256", "head", "x6zc_master", "outcome",
       "global_rule", "cells", "r_w1_p", "k6", "f1", "k0", "coupling", "stage_b", "reuse_verdict",
       "x6s1_statement", "descriptive", "exposure", "sensitivity", "follow_up", "budget", "n",
       "n_avail", "r_star", "stages", "env")

def _report(outcome=NA_DIR, licence="L", rule="R9", g_rule=None) -> dict:
    r = {v: {"point": 1.0, "lo": 0.9, "hi": 1.1} for v in ("MM", "PM", "MP")}
    cells = {c: {"model": m, "family": f, "rule": rule, "outcome": outcome, "licence": licence,
                 "not_licensed": "x", "qualifiers": [], "b": 0.2, "b_interval": [0.15, 0.25],
                 "beta_pp": SIGN[c] * 0.2, "r": r, "undefined_frac": 0.0, "n": 1024,
                 "beta_sb": {"point": 0.1, "lo": 0.0, "hi": 0.2}, "descriptive": False}
             for c, m, f in (("P", "ZC-s1", "W2"), ("S3", "ZC-s3", "W1"), ("S4", "ZC-s4", "W1"))}
    return {"schema": "x6zc-report-v1", "protocol_id": CONTRACT["protocol"]["id"],
            "protocol_sha256": CONTRACT["protocol"]["sha256"], "head": "0" * 40,
            "x6zc_master": 2026102670, "outcome": outcome, "global_rule": g_rule, "cells": cells,
            "r_w1_p": None, "k6": {"W2": True, "W1": True}, "f1": {"W2": F1_OK, "W1": F1_OK},
            "k0": {"status": "PASS"}, "coupling": {},
            "stage_b": {"k4": {}, "k5": {}, "descriptive_tier": {}, "qualifiers": {}, "b9": {}},
            "reuse_verdict": {"axis1": "VALID", "axis2": "UNDETERMINED", "amendments": [2, 3],
                              "amendment_1_mark": None,
                              "statement": CONTRACT["reuse"]["statement"]},
            "x6s1_statement": CONTRACT["x6s1_statement"], "descriptive": {},
            "exposure": {"a4_matches": 0, "d_coincident": 0}, "sensitivity": {}, "follow_up": None,
            "budget": {"cpu_s": {"0": 0, "A": 0, "B": 0, "C": 0}, "pauses": []}, "n": 1024,
            "n_avail": 2400, "r_star": 1300, "stages": {}, "env": {}}

def test_report_schema():
    assert set(_report()) == set(TOP) and zr.validate_report(_report()) == []
    for k in TOP:
        r = _report()
        del r[k]
        assert zr.validate_report(r), k
    r = _report()
    r["outcome"] = r["cells"]["P"]["outcome"] = "ZC_NOT_COMMUTATIVE/NOT_AN_OUTCOME"
    assert zr.validate_report(r)
    assert zr.validate_report(_report("STOP_REPLAN", "", None, "G-R0")) == []
    r = _report("STOP_REPLAN", "", None, "G-R0")
    r["cells"]["P"]["licence"] = "a licensed sentence"
    assert zr.validate_report(r)

STORED = {"beta_W2": 0.2093075, "beta_W2_y": [0.205, 0.202, 0.221], "R_W2": 0.0766,
          "Delta_W3": 0.31, "rho_C": 0.0078, "rho_W2": 0.04594, "cue_mass_median": 0.199,
          "beta_W1": -0.0126, "beta_W3": 0.05, "beta_W3_bal": 0.04, "beta_W3p": 0.03,
          "nonfinite": False}

def test_k4_tiers_and_crosses():
    def tier(**kw):
        return zs.k4_compare(STORED, {**json.loads(json.dumps(STORED)), **kw})
    assert tier()["tier"] == "PASS"
    r = tier(R_W2=0.0766 * (1 + 5e-10))
    assert r["tier"] == "ENV_DRIFT" and 4e-10 < r["max_rel"] < 6e-10
    assert tier(beta_W2_y=[0.205, 0.202 * (1 + 5e-10), 0.221])["tier"] == "ENV_DRIFT"
    assert tier(R_W2=0.0766 * (1 + 2e-9))["tier"] == "DEFECT_CANDIDATE"
    assert tier(nonfinite=True)["tier"] == "DEFECT_CANDIDATE"
    assert zs.crosses(0.0999999, 0.1000001) and zs.crosses(-0.2, 0.05)  # DR21; |β| compared
    assert not zs.crosses(0.1 - 5e-10, 0.2)  # inside the 1e-9 band
    assert not zs.crosses(0.05, 0.08) and zs.crosses(0.05, 0.2)

def test_pause_check():
    assert not zr.pause_check("A", 11340, 100)["pause"]
    assert zr.pause_check("A", 11340.5, 100)["pause"]
    assert zr.pause_check("B", 1000, 8640.5)["pause"]
    assert not zr.pause_check("B", 1000, 8640)["pause"]
    assert zr.pause_check("0", 3 * 720 + 1, 10)["pause"]  # DR22
    assert not zr.pause_check("0", 2160, 2160)["pause"]
    for n, cum, stg in ((1024, 29700, 9720), (2048, 39420, 19440),
                        (1500, 34218.28125, 14238.28125)):
        r = zr.pause_check("C", 0, 0, n=n)
        assert (r["cumulative_threshold"], r["stage_threshold"], r["pause"]) == (cum, stg, False)
        assert zr.pause_check("C", cum + 0.5, 0, n=n)["pause"]
        assert zr.pause_check("C", 0, stg + 0.5, n=n)["pause"]

def test_inventory_and_guards(tmp_path):
    st = tmp_path / "x6-stage1-store"
    for rel, data in (("a.json", b'{"v": 1}'), ("sub/b.npz", b"\x00not an npz"),
                      ("sealed/x.json", b"{}")):
        (st / rel).parent.mkdir(parents=True, exist_ok=True)
        (st / rel).write_bytes(data)
    inv = zr.x6s1_inventory(str(st))
    assert set(inv) == {"a.json", "sub/b.npz", "sealed/"}  # nothing listed under sealed/
    assert inv["a.json"][0] == 8 and inv["sealed/"][0] == 0
    assert zr.inventory_equal(inv, zr.x6s1_inventory(str(st)))
    (st / "a.json").write_bytes(b'{"v": 22}')
    assert not zr.inventory_equal(inv, zr.x6s1_inventory(str(st)))
    with pytest.raises(RuntimeError):
        zr.guard("B", "fresh")
    zr.guard("C", "fresh")
    zr.guard("B", "D")
    meta, hit, miss = json.dumps({"seed_map": {"s": 2026102670}}), tmp_path / "r1", tmp_path / "r2"
    for d in (hit / "foo-store", miss / "foo-store" / "sealed"):
        d.mkdir(parents=True)
        (d / "meta.json").write_text(meta, "utf-8")
    r = zr.master_fresh(str(hit), 2026102670)
    assert not r["fresh"] and [Path(h).parts[-2:] for h in r["hits"]] == [("foo-store",
                                                                            "meta.json")]
    r = zr.master_fresh(str(miss), 2026102670)  # under sealed/: pruned, no hit
    assert r["fresh"] and list(r["hits"]) == []
