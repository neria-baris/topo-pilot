"""Author A: T-RULES (X6S1-FROZEN-v1 §2.4-§2.7, §3, §7.2, §7.6, §7.9, §10.1, §14.3; API.md §3.4,
§9). Every §7.9 branch and its precedence, the missing-model convention, UNRESOLVED routing,
SHARP/TARGET statuses, designed counts and the exact-rational thresholds (3/4)G0- and
(3/4)Delta_W2^lo, with float inputs placed one ulp either side of the exact rational edges."""
from __future__ import annotations

import copy
import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_data as sd  # noqa: E402
import x6s1_decide as sdc  # noqa: E402

G0_S = "0.0026358964806790516544074195299418525190876670746427621626951934793579293430931071"
G8_S = "0.0088553050512358844408577637624772307516013467873269249611029142273162701006695055"
G0, G8 = Fraction(G0_S), Fraction(G8_S)
DW2_LO = Fraction("0.06111937134189654795552480797123169528984655108737642130388")  # synthetic lo
BAND = Fraction(1, 10**9)
SEEDS = (1, 2, 3, 4)
VALIDITY = ("S0", "PF", "SMOKE_INGEST", "G0_ORC", "SCORE", "G0_POS", "G0_FEAS", "REGISTRY",
            "INCOMPLETE")


def float_le(x: Fraction) -> float:
    """Largest float f with Fraction(f) <= x."""
    f = float(x)
    while Fraction(f) > x:
        f = math.nextafter(f, -math.inf)
    return f


# ---------------------------------------------------------------- exact thresholds (API §3.4)
def test_stage0_thresholds_are_exact_rationals():
    assert sd.CONST_MAP["G_Parikh_32"]["lo"] == G0_S and sd.CONST_MAP["G_8_32"]["lo"] == G8_S
    assert sd.g0_lo() == G0 and sd.g8_lo() == G8
    assert sd.target_threshold() == Fraction(3, 4) * G0
    assert sd.prec_delta() == Fraction(1, 4) * G0
    assert sd.regret_bar(DW2_LO) == Fraction(3, 4) * DW2_LO
    assert all(isinstance(v, Fraction) for v in
               (sd.g0_lo(), sd.target_threshold(), sd.prec_delta()))


# ---------------------------------------------------------------- SHARP / TARGET
def test_sharp_target_statuses_at_exact_edges():
    tgt = Fraction(3, 4) * G0
    with localcontext() as c:
        c.prec = 200
        tgt_s = str(Decimal(G0_S) * Decimal("0.75"))        # exact decimal of (3/4) G0-
        eps = Decimal("1e-100")
        cases = {G0_S: (False, False, "NOT_CERTIFIED"),           # equality is not supported
                 str(Decimal(G0_S) - eps): (True, False, "GAIN_BELOW_TARGET"),
                 tgt_s: (True, False, "GAIN_BELOW_TARGET"),
                 str(Decimal(tgt_s) - eps): (True, True, "TARGET_MET"),
                 "0.01": (False, False, "NOT_CERTIFIED")}
    assert Fraction(tgt_s) == tgt
    for u, (sharp, target, status) in cases.items():
        got = sdc.sharp_target(u, G0)
        assert (got["SHARP"], got["TARGET"], got["status"]) == (sharp, target, status), u
    none = sdc.sharp_target(None, G0)
    assert none["status"] == "NOT_CERTIFIED" and not none["SHARP"] and not none["TARGET"]


# ---------------------------------------------------------------- C-ORD
def test_cord_rule():
    adj = {1: 0.3, 2: 0.2, 3: 0.4, 4: -0.1}
    assert sdc.cord(0.25, 0.0501, adj, "PASS", True) == "SUPPORTED"     # mean >= 1/4 inclusive
    assert sdc.cord(0.2499, 0.2, adj, "PASS", True) == "NOT_SUPPORTED"
    assert sdc.cord(0.3, 0.0499, adj, "PASS", True) == "NOT_SUPPORTED"
    two = {1: 0.9, 2: 0.9, 3: 0.0, 4: -0.1}                             # 0.0 is not > 0
    # API-AMBIGUITY: 'adjusted' read as the report's {s: value} dict (keys s = 1..4)
    assert sdc.cord(0.425, 0.2, two, "PASS", True) == "NOT_SUPPORTED"
    assert sdc.cord(0.5, 0.3, adj, "FAIL", True) == "UNRESOLVED"        # TAIL failure
    assert sdc.cord(0.5, 0.3, adj, "PASS", False) == "UNRESOLVED"       # missing/undefined term


# ---------------------------------------------------------------- designed flag ordD(s)
def ds(**kw):
    base = {"beta_W2": 0.6, "beta_W2_y": [0.6, 0.55, 0.65], "R_W2": 0.01, "Delta_W3": 0.02,
            "rho_C": 0.01, "rho_W2": 1.0, "cue_mass_median": 0.2, "beta_W1": 0.5,
            "beta_W3": 0.4, "beta_W3_bal": 0.4, "beta_W3p": 0.4, "nonfinite": False}
    base.update(kw)
    return base


def plc(**kw):
    return ds(**{"beta_W2": 0.01, "beta_W2_y": [0.0, 0.02, 0.01], "rho_W2": 0.02, **kw})


def ordd(na=None, init=None, ab=None, zc=None):
    return sdc.ord_d(na if na is not None else ds(), init or plc(), ab or plc(), zc or plc(),
                     DW2_LO)


def test_ord_d_pass_fail_and_regret_bar_exact():
    bar = Fraction(3, 4) * DW2_LO
    assert ordd()["status"] == "PASS"
    r_pass = float_le(bar - BAND)
    r_mid_lo = math.nextafter(r_pass, math.inf)                 # just above bar - 1e-9
    r_mid_hi = float_le(bar + BAND)                             # still <= bar + 1e-9
    r_fail = math.nextafter(r_mid_hi, math.inf)
    assert ordd(ds(R_W2=r_pass))["status"] == "PASS"
    assert ordd(ds(R_W2=r_mid_lo))["status"] == "NUMERICALLY_UNRESOLVED"
    assert ordd(ds(R_W2=r_mid_hi))["status"] == "NUMERICALLY_UNRESOLVED"
    assert ordd(ds(R_W2=r_fail))["status"] == "FAIL"
    assert ordd(ds(beta_W2=0.2499))["status"] == "FAIL"
    assert ordd(ds(beta_W2=0.25))["status"] == "NUMERICALLY_UNRESOLVED"
    assert ordd(ds(beta_W2=0.2500001))["status"] == "PASS"
    assert ordd(ds(beta_W2_y=[0.6, 0.2, 0.7]))["status"] == "FAIL"      # per-cue minimum
    assert ordd(ds(beta_W2_y=[0.6, 0.25, 0.7]))["status"] == "NUMERICALLY_UNRESOLVED"
    assert ordd(ds(beta_W2=0.1, R_W2=r_pass))["status"] == "FAIL"


@pytest.mark.parametrize("na,init,ab,zc,limited", [
    (ds(cue_mass_median=0.05), None, None, None, False),             # READOUT_LIMITED
    (ds(nonfinite=True), None, None, None, False),                   # non-finite alignment
    (ds(beta_W2=float("nan")), None, None, None, False),
    (ds(beta_W2_y=[0.6, float("nan"), 0.7]), None, None, None, False),
    (ds(rho_C=0.26), None, None, None, False),                       # NA spurious order
    (ds(beta_W2=0.0, cue_mass_median=0.05), None, None, None, False),  # undefined, never FAIL
    (None, plc(beta_W2=0.11), None, None, True),                    # designed placebos
    (None, None, plc(beta_W2=-0.2), None, True),
    (None, None, plc(rho_W2=0.26), None, True),
    (None, None, None, plc(rho_W2=0.3), True),
    (None, None, None, plc(beta_W2=float("nan")), True),
])
def test_ord_d_unresolved_routing(na, init, ab, zc, limited):
    out = ordd(na, init, ab, zc)
    assert out["status"] == "UNRESOLVED"
    if limited:
        assert out["control_limited"] is True
    else:
        assert out["control_limited"] is False


def test_ord_d_missing_model_fails_the_seed():
    out = sdc.ord_d(None, plc(), plc(), plc(), DW2_LO)
    assert out["status"] != "PASS"
    out = sdc.ord_d(ds(), None, plc(), plc(), DW2_LO)
    assert out["status"] != "PASS"


def test_readout_and_placebo_checks():
    assert sdc.cue_ok(0.1) and sdc.cue_ok(0.5)
    for bad in (0.0999, float("nan"), float("inf"), 0.0):
        assert not sdc.cue_ok(bad)
    out = sdc.placebo_natural({"init-s1": 0.05, "AB-s2": -0.15, "ZC-s3": float("nan"),
                               "ZC-s4": 0.0999})
    assert sorted(out["failed"]) == ["AB-s2", "ZC-s3"] and out["ok"] is False
    good = sdc.placebo_natural({f"{a}-s{s}": 0.01 * s for a in ("init", "AB", "ZC") for s in SEEDS})
    assert good["failed"] == [] and good["ok"] is True


def test_seed_flags_and_designed_counts():
    # API-AMBIGUITY: U025 read as the eb_report "U" Decimal string, xbar as its float
    f = sdc.seed_flags(0.3, 0.06, "0.0023", 0.002, 0.05, G0)
    assert (f["orderN"], f["lowN"], f["precision_ok"]) == (True, False, True)
    assert sdc.seed_flags(0.25, 0.051, "0.0023", 0.002, 0.05, G0)["orderN"] is True
    assert sdc.seed_flags(0.3, 0.049, "0.0023", 0.002, 0.05, G0)["orderN"] is False
    assert sdc.seed_flags(0.05, -0.1, "0.0023", 0.002, 0.05, G0)["lowN"] is True
    assert sdc.seed_flags(0.10, -0.1, "0.0023", 0.002, 0.05, G0)["lowN"] is False   # strict <
    assert sdc.seed_flags(0.3, 0.06, "0.0023", 0.002, 0.11, G0)["precision_ok"] is False
    assert sdc.seed_flags(0.3, 0.06, "0.0027", 0.002, 0.05, G0)["precision_ok"] is False
    # API-AMBIGUITY: 'statuses' read as a list of per-seed ordD statuses
    got = sdc.designed_counts(["PASS", "FAIL", "NUMERICALLY_UNRESOLVED", "UNRESOLVED"])
    assert got == {"PASS": 1, "FAIL": 1, "UNRESOLVED": 2}
    assert sdc.designed_counts(["PASS"] * 4) == {"PASS": 4, "FAIL": 0, "UNRESOLVED": 0}


# ---------------------------------------------------------------- §7.9 ordered rules
def ev(**paths):
    base = {"validity": {k: "PASS" for k in VALIDITY}, "learn": "GO",
            "pipeline": {"DET": "PASS", "XCHECK": "PASS", "QUANT": "PASS"},
            "learn_test": {f"NA-s{s}": "PASS" for s in SEEDS}, "cord": "SUPPORTED",
            "placebo_natural_ok": True, "ord_d": {s: "PASS" for s in SEEDS},
            "lowN": {s: False for s in SEEDS}, "precision_ok": {s: True for s in SEEDS},
            "checks_ok": True}
    out = copy.deepcopy(base)
    for path, value in paths.items():
        keys = path.split("__")
        node = out
        for k in keys[:-1]:
            node = node[k]
        last = keys[-1]
        node[int(last) if last.isdigit() else last] = value
    return out


NOT_DET = dict(cord="NOT_SUPPORTED", lowN__1=True, lowN__2=True, lowN__3=True, ord_d__1="FAIL",
               ord_d__2="FAIL", ord_d__3="FAIL", ord_d__4="PASS")

RULE_CASES = [
    ({}, "ORDER_USE_NATURAL_AND_DESIGNED", "5"),
    ({"validity__S0": "FAIL"}, "INVALID", "1"),
    ({"validity__PF": "FAIL"}, "INVALID", "1"),
    ({"validity__SMOKE_INGEST": "FAIL"}, "INVALID", "1"),
    ({"validity__G0_ORC": "FAIL"}, "CONSTRUCTION_FAIL", "1"),
    ({"validity__SCORE": "FAIL"}, "CONSTRUCTION_FAIL", "1"),
    ({"validity__G0_POS": "FAIL"}, "CONSTRUCTION_FAIL", "1"),
    ({"validity__G0_FEAS": "FAIL"}, "FEASIBILITY_NO_GO", "1"),
    ({"validity__REGISTRY": "FAIL_TECHNICAL/LINEAGE"}, "FAIL_TECHNICAL/LINEAGE", "1"),
    ({"validity__REGISTRY": "INCONCLUSIVE/REGISTRY_INCOMPLETE"},
     "INCONCLUSIVE/REGISTRY_INCOMPLETE", "1"),
    # API-AMBIGUITY: the INCOMPLETE validity entry read as a gate status ("FAIL" = incomplete)
    ({"validity__INCOMPLETE": "FAIL"}, "INCOMPLETE", "1"),
    # precedence inside rule 1 and across rules
    ({"validity__S0": "FAIL", "validity__G0_ORC": "FAIL"}, "INVALID", "1"),
    ({"validity__G0_ORC": "FAIL", "validity__G0_FEAS": "FAIL"}, "CONSTRUCTION_FAIL", "1"),
    ({"validity__G0_FEAS": "FAIL", "validity__REGISTRY": "FAIL_TECHNICAL/LINEAGE"},
     "FEASIBILITY_NO_GO", "1"),
    ({"validity__S0": "FAIL", "learn": "NOT_LEARNED"}, "INVALID", "1"),
    ({"learn": "NOT_LEARNED"}, "NOT_LEARNED", "2"),
    ({"learn": "LEARNING_UNRESOLVED"}, "LEARNING_UNRESOLVED", "2"),
    ({"learn": "NOT_LEARNED", "pipeline__DET": "FAIL"}, "NOT_LEARNED", "2"),
    ({"pipeline__DET": "FAIL"}, "PIPELINE_INVALID", "3"),
    ({"pipeline__XCHECK": "FAIL"}, "PIPELINE_INVALID", "3"),
    ({"pipeline__QUANT": "INVALID"}, "PIPELINE_INVALID", "3"),
    ({"pipeline__QUANT": "INVALID", "learn_test__NA-s1": "FAIL", "learn_test__NA-s2": "FAIL"},
     "PIPELINE_INVALID", "3"),
    # rule 4: LEARN-TEST; a missing model (None) fails
    ({"learn_test__NA-s1": "FAIL", "learn_test__NA-s2": "FAIL"}, "LEARNING_NOT_ROBUST", "4"),
    ({"learn_test__NA-s1": "FAIL", "learn_test__NA-s2": "UNRESOLVED", "learn_test__NA-s3": "FAIL"},
     "LEARNING_NOT_ROBUST", "4"),
    ({"learn_test__NA-s1": "FAIL", "learn_test__NA-s2": "UNRESOLVED"}, "LEARNING_UNRESOLVED", "4"),
    ({"learn_test__NA-s1": "UNRESOLVED", "learn_test__NA-s2": "UNRESOLVED",
      "learn_test__NA-s3": "FAIL"}, "LEARNING_UNRESOLVED", "4"),
    ({"learn_test__NA-s4": None}, "ORDER_USE_NATURAL_AND_DESIGNED", "5"),
    ({"learn_test__NA-s3": "UNRESOLVED", "learn_test__NA-s4": None}, "LEARNING_UNRESOLVED", "4"),
    ({"learn_test__NA-s3": None, "learn_test__NA-s4": None}, "LEARNING_NOT_ROBUST", "4"),
    # rules 5, 6, 6', 7
    ({"ord_d__4": "FAIL"}, "ORDER_USE_NATURAL_AND_DESIGNED", "5"),
    ({"ord_d__4": None}, "ORDER_USE_NATURAL_AND_DESIGNED", "5"),
    ({"ord_d__3": "FAIL", "ord_d__4": "NUMERICALLY_UNRESOLVED"}, "ORDER_USE_NATURAL", "6"),
    ({"ord_d__3": None, "ord_d__4": "UNRESOLVED"}, "ORDER_USE_NATURAL", "6"),
    ({"placebo_natural_ok": False}, "INCONCLUSIVE", "6'"),
    ({"placebo_natural_ok": False, "ord_d__4": "FAIL"}, "INCONCLUSIVE", "6'"),
    ({"cord": "NOT_SUPPORTED"}, "ORDER_USE_DESIGNED_ONLY", "7"),
    ({"cord": "NOT_SUPPORTED", "ord_d__1": "FAIL"}, "ORDER_USE_DESIGNED_ONLY", "7"),
    ({"cord": "UNRESOLVED"}, "INCONCLUSIVE", "9"),                    # 7 needs a resolved C-ORD
    ({"cord": "NOT_SUPPORTED", "ord_d__1": "FAIL", "ord_d__2": "FAIL"}, "INCONCLUSIVE", "9"),
    # rule 8 and each failed conjunct (RC12: all four ordD flags resolved)
    (NOT_DET, "ORDER_NOT_DETECTED", "8"),
    ({**NOT_DET, "ord_d__4": "FAIL", "lowN__4": True}, "ORDER_NOT_DETECTED", "8"),
    ({**NOT_DET, "lowN__3": False}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "lowN__3": None}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "ord_d__1": "UNRESOLVED"}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "ord_d__1": "NUMERICALLY_UNRESOLVED"}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "ord_d__1": None}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "ord_d__1": "PASS"}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "precision_ok__2": False}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "precision_ok__2": None}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "checks_ok": False}, "INCONCLUSIVE", "9"),
    ({**NOT_DET, "cord": "UNRESOLVED"}, "INCONCLUSIVE", "9"),
]


@pytest.mark.parametrize("over,outcome,rule", RULE_CASES)
def test_decide_ordered_rules(over, outcome, rule):
    got = sdc.decide(ev(**over))
    assert (got["outcome"], got["rule"]) == (outcome, rule)


def test_decide_not_run_after_first_validity_failure():
    e = ev(validity__S0="FAIL")
    for k in VALIDITY[1:]:
        e["validity"][k] = "NOT_RUN"
    got = sdc.decide(e)
    assert (got["outcome"], got["rule"]) == ("INVALID", "1")


# ---------------------------------------------------------------- qualifiers and licences
REGISTERED = ("SHARP_NATURAL", "NATURAL_TARGET", "GAIN_BELOW_REGISTERED_TARGET", "W2_GAP_BEATEN",
              "CHALLENGE_BEATEN", "CONTROL_LIMITED", "READOUT_LIMITED", "CONTROLS_LEARNED",
              "LADDER", "PRECISION_LIMITED", "DESIGNED_UNRESOLVED", "LENGTH_PROFILE",
              "MIXED_DEVICE", "MIXED_ENV")


def test_qualifiers_registered_names_order_and_designed_unresolved():
    # API-AMBIGUITY: qualifiers(ev) read as taking the same ev dict as decide()
    e = ev(ord_d__3="NUMERICALLY_UNRESOLVED")
    q = sdc.qualifiers(e)
    assert all(isinstance(x, str) for x in q)
    names = [x.split("(")[0] for x in q]
    assert set(names) <= set(REGISTERED)
    assert [REGISTERED.index(n) for n in names] == sorted(REGISTERED.index(n) for n in names)
    assert "DESIGNED_UNRESOLVED(1)" in q
    assert not any(x.startswith("DESIGNED_UNRESOLVED") for x in sdc.qualifiers(ev()))


def test_licence_sentences_and_designed_counts():
    vals = {"beta_bar": 0.41, "lb": 0.33, "k": 3, "f": 1, "u": 0}
    for outcome in ("ORDER_USE_NATURAL_AND_DESIGNED", "ORDER_USE_NATURAL",
                    "ORDER_USE_DESIGNED_ONLY"):
        text = sdc.licence(outcome, vals)
        assert "[" not in text and "]" not in text
        assert "3 PASS" in text and "1 FAIL" in text and "0 UNRESOLVED" in text   # OS 2
    assert "not established in three models" in sdc.licence("ORDER_USE_NATURAL", vals)
    assert "natural-distribution order criterion was not met" in \
        sdc.licence("ORDER_USE_DESIGNED_ONLY", vals)
    assert "G_8(32) = 8.855e-3" in sdc.licence("NOT_LEARNED", vals)
    assert "below 0.10 in at least three of four seeds" in sdc.licence("ORDER_NOT_DETECTED", vals)
    assert "No statement about models" in sdc.licence("INVALID", vals)
