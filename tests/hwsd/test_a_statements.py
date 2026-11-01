"""Author A (job 0197): statements D1-D6 per model and the aggregate rule (§5.4, §5.5; DRD5).

Hand values from PROTOCOL_HWSD_v1.md §5.4/§5.5 and API.md §7 (RC-4, RC-5, F-2, S1, S3, S6),
cross-checked against the independent reference in test_a_hwsd_ref.py.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsd"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsd_config as dc  # noqa: E402, I001
import hwsd_statements as dst  # noqa: E402
import pytest  # noqa: E402
import test_a_hwsd_ref as ref  # noqa: E402
from test_a_hwsd_ref import EXC, NOC, SC, SU, SUP, UC, UNR, UNV, row, seq  # noqa: E402

M = Fraction(1, 100)
J1, J2, J3 = 620301, 620302, 620303
NE = "NOT_EVALUABLE"


def check(res, reading, reason=None, qualifier=None):
    assert res["reading"] == reading, res
    if reading == NE:
        assert res["reason"] == reason, res
    if qualifier is not None:
        assert res["qualifier"] == qualifier, res


def agg(statement, tables_by_model):
    f = getattr(dst, statement.lower())
    per = {j: f(rows) for j, rows in tables_by_model.items()}
    res = dst.aggregate(statement, per)
    assert res["statement"] == statement
    return res["reading"], {r: sorted(m) for r, m in (res["reasons"] or {}).items()}


# ---- D1 ----
def test_d1_every_reading():
    num = row(SC, L=0.5, U=0.6, L_S=0.4, U_S=0.7, Fm=Fraction(49, 100), Fp=Fraction(0))
    check(dst.d1(seq(NOC(), SUP())), "TRUE")
    check(dst.d1(seq(SUP(), EXC())), "FALSE")
    check(dst.d1(seq(NOC(), UNR())), NE, "UNRESOLVED")
    check(dst.d1(seq(NOC(), num)), NE, "UNRESOLVED")  # UNRESOLVED/NUMERICAL
    for last in (NOC(), UNV(), SUP(status=UC)):
        check(dst.d1(seq(SUP(), last)), NE, "FINAL_NA")


# ---- D2 per model ----
def test_d2_chart_at_init_evaluated_first():
    check(dst.d2(seq(SUP(), SUP())), NE, "CHART_AT_INIT")
    check(dst.d2(seq(EXC(), EXC())), NE, "CHART_AT_INIT")  # before FINAL_NOT_SUPPORT
    check(dst.d2(seq(SUP(status=UC), UNV(), SUP())), NE, "CHART_AT_INIT")


def test_d2_no_chart_false_and_final_not_support():
    check(dst.d2(seq(NOC(), UNV(), NOC())), NE, "NO_CHART")
    check(dst.d2(seq(NOC(), UNV(), EXC(), SUP())), "FALSE")
    check(dst.d2(seq(NOC(), UNV(), EXC(), EXC())), "FALSE")  # BEFORE beats a final not SUPPORT
    check(dst.d2(seq(NOC(), EXC(), EXC())), NE, "FINAL_NOT_SUPPORT")
    check(dst.d2(seq(NOC(), EXC(), NOC())), NE, "FINAL_NOT_SUPPORT")


def test_d2_true_qualifier_uses_unvalidated_rows():
    check(dst.d2(seq(NOC(), EXC(status=SU), EXC(), SUP())), "TRUE", qualifier="INFORMATIVE")
    check(dst.d2(seq(NOC(), UNR(status=SU), EXC(), SUP())), "TRUE", qualifier="UNINFORMATIVE")


def test_d2_qualifier_boundary_exact():
    U_S = 0.005
    Fp = M - Fraction(U_S)  # U^S + F+ = 1/100 exactly
    pre = row(SU, L=-0.01, U=0.004, L_S=-0.02, U_S=U_S, Fm=Fraction(0), Fp=Fp)
    check(dst.d2(seq(NOC(), pre, EXC(), SUP())), "TRUE", qualifier="UNINFORMATIVE")
    below = dict(pre, U_S=math.nextafter(U_S, 0.0))
    check(dst.d2(seq(NOC(), below, EXC(), SUP())), "TRUE", qualifier="INFORMATIVE")


def test_d2_by_construction_and_unavailable_not_counted():
    check(dst.d2(seq(NOC(), EXC(), SUP())), "BY_CONSTRUCTION")
    check(dst.d2(seq(NOC(), EXC(status=UC, valid=False), EXC(), SUP())), "BY_CONSTRUCTION")


# ---- D2 aggregate ----
BYC = seq(NOC(), EXC(), SUP())
TINF = seq(NOC(), EXC(status=SU), EXC(), SUP())
TUNI = seq(NOC(), UNR(status=SU), EXC(), SUP())
INIT = seq(EXC(), SUP())
BEF = seq(NOC(), UNV(), EXC(), SUP())


@pytest.mark.parametrize("tabs,expected", [
    ((BYC, BYC, BYC), (NE, {"BY_CONSTRUCTION": [J1, J2, J3]})),
    ((BYC, TINF, TINF), ("TRUE", {})),
    ((BYC, BYC, TINF), ("TRUE", {})),
    ((TINF, TUNI, BYC), ("TRUE", {})),
    ((TINF, TINF, TINF), ("TRUE", {})),
    ((TUNI, TUNI, BYC), (NE, {"UNINFORMATIVE_PRE_CHART": [J1, J2, J3]})),
    ((TUNI, TUNI, TUNI), (NE, {"UNINFORMATIVE_PRE_CHART": [J1, J2, J3]})),
    ((INIT, TINF, TINF), (NE, {"CHART_AT_INIT": [J1]})),  # F-2
    ((INIT, BEF, TINF), ("FALSE", {})),
    ((BEF, BYC, BYC), ("FALSE", {})),
])
def test_d2_aggregate(tabs, expected):
    reading, reasons = agg("D2", dict(zip((J1, J2, J3), tabs)))
    assert reading == expected[0]
    if reading == NE:
        assert reasons == expected[1]


def test_d2_aggregate_mixed_not_evaluable_names_the_models():
    reading, reasons = agg("D2", {J1: seq(NOC(), NOC()), J2: TINF, J3: seq(NOC(), EXC(), EXC())})
    assert reading == NE
    assert reasons["NO_CHART"] == [J1] and reasons["FINAL_NOT_SUPPORT"] == [J3]


# ---- D3 ----
def test_d3_per_model_readings():
    check(dst.d3(seq(NOC(), EXC(), SUP())), "TRUE")
    check(dst.d3(seq(NOC(), SUP())), "FALSE")
    check(dst.d3(BEF), "FALSE")
    for rows, reason in ((seq(NOC(), NOC()), "NO_CHART"), (INIT, "CHART_AT_INIT"),
                         (seq(NOC(), SUP(status=UC), SUP()), "UNCERTIFIED_AT_ANCHOR"),
                         (seq(NOC(), EXC(), EXC()), "NEVER"),
                         (seq(NOC(), EXC(), NOC()), "FINAL_NA"),
                         (seq(NOC(), EXC(), UNR()), "UNRESOLVED")):
        check(dst.d3(rows), NE, reason)


def test_d3_chart_at_init_rc4():
    aft = seq(NOC(), EXC(), SUP())
    assert agg("D3", {J1: INIT, J2: aft, J3: aft}) == (NE, {"CHART_AT_INIT": [J1]})
    assert agg("D3", {J1: INIT, J2: seq(NOC(), SUP()), J3: aft})[0] == "FALSE"
    assert agg("D3", {J1: aft, J2: aft, J3: aft}) == ("TRUE", {})


# ---- D4 ----
def test_d4_per_model_readings():
    check(dst.d4(seq(EXC(), EXC(learn=True), SUP())), "TRUE")
    check(dst.d4(seq(NOC(), SUP(learn=True))), "FALSE")
    check(dst.d4(seq(UNV(), NOC(learn=True), SUP())), "FALSE")
    for rows, reason in ((seq(EXC(), SUP()), "NO_LEARNING"),
                         (seq(NOC(learn=True), EXC(), SUP()), "LEARNING_BEFORE_CHART"),
                         (seq(EXC(), NOC(learn=True), SUP()), "UNCERTIFIED_AT_ANCHOR"),
                         (seq(EXC(learn=True), EXC()), "NEVER"),
                         (seq(EXC(learn=True), NOC()), "FINAL_NA"),
                         (seq(EXC(learn=True), UNR()), "UNRESOLVED")):
        check(dst.d4(rows), NE, reason)


# ---- D5 ----
def test_d5_per_model_readings():
    check(dst.d5(seq(NOC(), SUP(b2=0.1))), "TRUE")
    check(dst.d5(seq(EXC(), SUP(b2=0.1))), "TRUE")  # k_C < k_P
    check(dst.d5(seq(NOC(b2=0.1), NOC())), "FALSE")  # k_C undefined
    check(dst.d5(seq(NOC(b2=0.1), SUP())), "FALSE")  # k_C > k_P
    check(dst.d5(seq(EXC(b2=0.1), SUP())), "FALSE")  # sigma(k_P) EXCLUDE
    check(dst.d5(seq(SUP(), SUP(b2=0.0))), NE, "NO_PREDICTIVE_ONSET")
    check(dst.d5(seq(SUP(), NOC(b2=0.2))), NE, "NA_AT_PREDICTIVE_ONSET")
    check(dst.d5(seq(SUP(), SUP(status=UC, b2=0.2))), NE, "NA_AT_PREDICTIVE_ONSET")
    check(dst.d5(seq(SUP(), UNV(b2=0.2))), NE, "NA_AT_PREDICTIVE_ONSET")
    check(dst.d5(seq(UNR(b2=0.1))), NE, "UNRESOLVED")


# ---- D6 (S3) ----
def test_d6_loss_on_ok_rows_only():
    check(dst.d6(seq(NOC(), SUP(), EXC(), SUP())), "FALSE")
    check(dst.d6(seq(NOC(), SUP(), SUP(status=UC), EXC(status=SU))), "TRUE")
    check(dst.d6(seq(EXC(), SUP(), SUP())), "TRUE")  # below before above is not a loss


def test_d6_est_only_crossing_is_diagnostic_not_false():
    rows = seq(NOC(), UNV(), EXC(), EXC())
    check(dst.d6(rows), NE, "NO_STRONG_CROSSING")
    d = dst.diagnostics({J1: rows})[J1]
    assert sorted(tuple(p) for p in d["est_loss"]) == [(2, 3), (2, 4)]


def test_d6_vacuous_and_true_needs_k1_below_K():
    check(dst.d6(seq(NOC(), EXC(), SUP())), NE, "NO_STRONG_CROSSING")
    check(dst.d6(seq(NOC(), SUP(), SUP())), "TRUE")
    check(dst.d6(seq(SUP())), NE, "NO_STRONG_CROSSING")


# ---- aggregate (all statements) ----
def test_aggregate_rule_generic():
    t, f = seq(NOC(), SUP()), seq(NOC(), EXC())
    u = seq(NOC(), UNR())
    assert agg("D1", {J1: t, J2: t, J3: t}) == ("TRUE", {})
    assert agg("D1", {J1: t, J2: f, J3: u})[0] == "FALSE"
    assert agg("D1", {J1: t, J2: u, J3: seq(NOC())}) == (NE, {"UNRESOLVED": [J2],
                                                              "FINAL_NA": [J3]})


def test_reasons_are_contract_reasons():
    reasons = dc.CONTRACT["statements"]["reasons"]
    rng = random.Random(1970)
    seen = set()
    for _ in range(300):
        t = ref.random_table(rng)
        for s in ("D1", "D2", "D3", "D4", "D5", "D6"):
            _, rs = agg(s, t)
            for r in rs:
                assert r in reasons[s], (s, r)
                seen.add((s, r))
    assert len(seen) >= 12


def test_random_tables_match_reference():
    rng = random.Random(1971)
    for _ in range(400):
        t = ref.random_table(rng)
        want = ref.evaluate(t)
        for s, f in ref.PER_MODEL.items():
            g = getattr(dst, s.lower())
            for j, rows in t.items():
                res, exp = g(rows), f(rows)
                assert res["reading"] == exp[0], (s, rows)
                if exp[0] == NE:
                    assert res["reason"] == exp[1]
                if s == "D2" and exp[0] == "TRUE":
                    assert res["qualifier"] == exp[2]
            reading, reasons = agg(s, t)
            assert reading == want[s][0], (s, t)
            if reading == NE:
                assert reasons == {r: sorted(m) for r, m in want[s][1].items()}
