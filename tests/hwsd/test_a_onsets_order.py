"""Author A (job 0197): §5.1 notation, §5.2 onsets, §5.3 ORDER (TEST_PLAN A test_a_onsets_order).

Expected values are hand-derived from PROTOCOL_HWSD_v1.md §5.1-§5.3 and API.md §7, and
cross-checked against the independent reference in test_a_hwsd_ref.py (never hwsd code).
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
from test_a_hwsd_ref import CU, EXC, NOC, SC, SU, SUP, UC, UNR, UNV, row, seq  # noqa: E402

M = Fraction(1, 100)


def k(o):
    keys = ("k_C", "k_C_star", "k_C_plus", "k_L", "k_P", "k_B", "k_B_S")
    return {key: o.get(key) for key in keys}


def cat(rows, anchor, A=None):
    res = dst.order(rows, anchor) if A is None else dst.order(rows, anchor, A=A)
    return res["category"]


# ---- §5.1 ----
def test_est_ok_and_sigma_by_status():
    assert dst.est(SUP()) and dst.ok(SUP())
    assert dst.est(UNV()) and not dst.ok(UNV())
    assert not dst.est(NOC()) and not dst.ok(NOC())
    unc = SUP(status=UC)
    assert not dst.est(unc) and not dst.ok(unc)
    assert dst.sigma(SUP()) == "SUPPORT" and dst.sigma(EXC()) == "EXCLUDE"
    assert dst.sigma(UNR()) == "UNRESOLVED"
    for r in (UNV(), NOC(), unc):  # sigma is NA unless SCORED
        assert dst.sigma(r) == "NA"


def test_sigma_numerical_label_and_constants():
    r = row(SC, L=0.5, U=0.6, L_S=0.4, U_S=0.7, Fm=Fraction(49, 100), Fp=Fraction(0))
    assert dst.sigma(r) == "UNRESOLVED/NUMERICAL"  # L - F- = 1/100 exactly; without F: SUPPORT
    assert dc.M == M and dc.F_PLANTED == Fraction(1, 10**9)


def test_fr_rule():
    assert dst.fr(Fraction(1, 3)) == Fraction(1, 3)
    assert dst.fr(0.1) == Fraction(0.1) != Fraction(1, 10)


def test_above_below_strict_equality():
    L_S = 0.02
    F_eq = Fraction(L_S) - M  # L_S - F = 1/100 exactly
    eq = row(SC, L=0.03, U=0.04, L_S=L_S, U_S=0.05, Fm=F_eq, Fp=Fraction(0))
    assert not dst.above_s(eq) and not dst.above_s_ok(eq)
    up = dict(eq, L_S=math.nextafter(L_S, 1.0))  # one float step above
    assert dst.above_s(up) and dst.above_s_ok(up)
    U_S = 0.005
    Fp = M - Fraction(U_S)  # U_S + F = 1/100 exactly
    beq = row(SC, L=-0.01, U=0.0, L_S=-0.02, U_S=U_S, Fm=Fraction(0), Fp=Fp)
    assert not dst.below_s(beq)
    assert dst.below_s(dict(beq, U_S=math.nextafter(U_S, 0.0)))


def test_above_s_unvalidated_vs_ok_and_below_needs_ok():
    assert dst.above_s(UNV()) and not dst.above_s_ok(UNV())
    assert not dst.below_s(EXC(status=SU))  # below_s needs OK
    assert dst.below_s(EXC())
    for r in (NOC(), SUP(status=UC), EXC(status=UC)):
        assert not dst.above_s(r) and not dst.below_s(r) and not dst.above_s_ok(r)


def test_above_s_uses_F_minus_and_below_uses_F_plus():
    r = row(SC, L=0.04, U=0.05, L_S=0.039, U_S=0.051, Fm=Fraction(3, 100), Fp=Fraction(0))
    assert not dst.above_s(r)  # 0.039 - 0.03 < 0.01
    r2 = row(SC, L=-0.01, U=0.0, L_S=-0.02, U_S=0.004, Fm=Fraction(0), Fp=Fraction(1, 100))
    assert not dst.below_s(r2)  # 0.004 + 0.01 > 0.01


# ---- §5.2 onsets ----
def test_onsets_basic_and_undefined():
    o = dst.onsets(seq(NOC(), UNV(), EXC(), SUP(), SUP()))
    assert k(o) == {"k_C": 3, "k_C_star": 3, "k_C_plus": 3, "k_L": None, "k_P": None,
                    "k_B": 4, "k_B_S": 2}
    o = dst.onsets(seq(NOC(), NOC()))
    assert all(v is None for v in k(o).values())


def test_unvalidated_is_never_a_chart_onset():
    o = dst.onsets(seq(UNV(), UNV(), UNV()))
    assert o["k_C"] is None and o["k_C_star"] is None and o["k_C_plus"] is None
    assert o["k_B_S"] == 1 and o["k_B"] is None


def test_uncertified_valid_counts_for_k_C():
    o = dst.onsets(seq(NOC(), SUP(status=UC, valid=True), SUP()))
    assert o["k_C"] == 2 and o["k_B"] == 3
    o = dst.onsets(seq(NOC(), SUP(status=UC, valid=False), SUP()))
    assert o["k_C"] == 3


def test_chart_lost_after_k_C_keeps_k_C():
    rows = seq(NOC(), EXC(), NOC(), EXC(), SUP(), SUP())
    o = dst.onsets(rows)
    assert o["k_C"] == 2  # first validated chart stays the onset
    assert o["k_C_star"] == 4  # the stable onset shows the loss
    assert o["k_C_plus"] == 2


def test_k_C_star_none_when_final_not_valid_and_k_C_plus_from_init():
    o = dst.onsets(seq(EXC(), SUP(), NOC()))
    assert o["k_C"] == 1 and o["k_C_star"] is None and o["k_C_plus"] is None
    o = dst.onsets(seq(EXC(), NOC(), SUP(), SUP()))
    assert o["k_C"] == 1 and o["k_C_plus"] == 3 and o["k_C_star"] == 3


def test_k_L_and_k_P_strict():
    rows = seq(NOC(b2=0.0), NOC(b2=-1.0, learn=True), NOC(b2=5e-324), NOC(b2=None))
    o = dst.onsets(rows)
    assert o["k_L"] == 2  # learn_pass (captured >= 4/5 read by hwsb_eval.b1)
    assert o["k_P"] == 3  # B2 lower bound at z_S strictly > 0; 0.0 is not an onset


# ---- n_pre, pre_chart_max ----
def test_n_pre_counts_est_before_k_C_only():
    rows = seq(NOC(), UNV(), SUP(status=UC), EXC(), SUP(), UNV())
    assert dst.n_pre(rows) == 1  # k_C = 3 (UNCERTIFIED valid); before it only k=2 is est
    assert Fraction(dst.pre_chart_max(rows)) == Fraction(0.051) + ref.F9


def test_n_pre_zero_and_pre_chart_max_none():
    rows = seq(NOC(), NOC(), EXC())
    assert dst.n_pre(rows) == 0 and dst.pre_chart_max(rows) is None


def test_n_pre_without_chart_counts_every_est():
    rows = seq(NOC(), UNV(), UNR(status=SU), NOC())
    assert dst.n_pre(rows) == 2  # decision 19
    assert Fraction(dst.pre_chart_max(rows)) == max(Fraction(0.051), Fraction(0.021)) + ref.F9


# ---- §5.3 ORDER, every category ----
CHART_CASES = [
    ("NO_CHART", seq(NOC(), UNV(), NOC())),
    ("CHART_AT_INIT", seq(EXC(), SUP())),
    ("CHART_AT_INIT", seq(SUP(status=UC), SUP())),  # rule 1a before rule 3
    ("BEFORE", seq(NOC(), UNV(), EXC(), SUP())),
    ("BEFORE", seq(UNV(), SUP(status=UC), SUP())),  # BEFORE beats a NA anchor
    ("UNCERTIFIED_AT_ANCHOR", seq(NOC(), SUP(status=UC), SUP())),
    ("WITH", seq(NOC(), SUP(), EXC())),
    ("AFTER", seq(NOC(), EXC(), UNR(), SUP())),
    ("NEVER", seq(NOC(), EXC(), SUP(), EXC())),
    ("NEVER", seq(NOC(), UNR(), EXC())),  # sigma(A) unresolved, final EXCLUDE
    ("FINAL_NA", seq(NOC(), EXC(), NOC())),
    ("FINAL_NA", seq(NOC(), EXC(), UNV())),
    ("UNRESOLVED", seq(NOC(), EXC(), UNR())),
    ("UNRESOLVED", seq(NOC(), UNR(), SUP())),
    ("NEVER", seq(NOC(), EXC())),  # A = K
]


@pytest.mark.parametrize("expected,rows", CHART_CASES)
def test_order_chart_categories(expected, rows):
    assert cat(rows, "chart") == expected
    assert ref.order(rows, "chart") == expected


def test_order_unresolved_numerical_read_as_unresolved():
    num = row(SC, L=0.5, U=0.6, L_S=0.4, U_S=0.7, Fm=Fraction(49, 100), Fp=Fraction(0))
    rows = seq(NOC(), num, SUP())
    assert dst.sigma(rows[1]) == "UNRESOLVED/NUMERICAL"
    assert cat(rows, "chart") == "UNRESOLVED"
    assert cat(seq(NOC(), EXC(), num), "chart") == "UNRESOLVED"


LEARN_CASES = [
    ("NO_LEARNING", seq(EXC(), SUP())),
    ("LEARNING_BEFORE_CHART", seq(NOC(learn=True), EXC(), SUP())),  # k_C undefined at k_L
    ("LEARNING_BEFORE_CHART", seq(NOC(), UNR(status=SU, learn=True), EXC(), SUP())),
    ("UNCERTIFIED_AT_ANCHOR", seq(EXC(), NOC(learn=True), SUP())),  # k_C < k_L, not OK at k_L
    ("UNCERTIFIED_AT_ANCHOR", seq(NOC(), SUP(status=UC, learn=True), SUP())),  # k_C = k_L
    ("BEFORE", seq(UNV(), NOC(learn=True), SUP())),
    ("WITH", seq(NOC(), SUP(learn=True))),
    ("AFTER", seq(EXC(), EXC(learn=True), SUP())),
    ("NEVER", seq(NOC(), EXC(learn=True), EXC())),
    ("FINAL_NA", seq(NOC(), EXC(learn=True), NOC())),
    ("UNRESOLVED", seq(EXC(learn=True), UNR())),
]


@pytest.mark.parametrize("expected,rows", LEARN_CASES)
def test_order_learning_categories(expected, rows):
    assert cat(rows, "learning") == expected
    assert ref.order(rows, "learning") == expected


def test_learning_anchor_at_step0_is_not_chart_at_init():
    rows = seq(EXC(learn=True), SUP())
    assert cat(rows, "learning") == "AFTER"
    assert cat(rows, "chart") == "CHART_AT_INIT"


def test_order_returns_anchor_and_A():
    rows = seq(NOC(), EXC(), SUP(learn=True))
    res = dst.order(rows, "chart")
    assert res["anchor"] == "chart" and res["A"] == 2 and res["category"] == "AFTER"
    res = dst.order(rows, "learning")
    assert res["anchor"] == "learning" and res["A"] == 3 and res["category"] == "WITH"
    assert dst.order(seq(NOC()), "chart")["A"] is None


def test_order_explicit_A_for_k_C_plus():
    rows = seq(EXC(), NOC(), SUP(), SUP())
    assert cat(rows, "chart") == "CHART_AT_INIT"
    assert cat(rows, "chart", A=3) == "WITH"  # rule 1a not applied for A >= 2
    rows = seq(SUP(), NOC(), EXC(), SUP())
    assert cat(rows, "chart", A=3) == "BEFORE"  # the step-0 SCORED row is above_s
    assert cat(seq(EXC(), SUP()), "chart", A=1) == "CHART_AT_INIT"


def test_onset_order_line():
    t = {620301: seq(NOC(learn=True, b2=0.1), EXC(), SUP()),
         620302: seq(NOC(), EXC(learn=True, b2=0.1), SUP()),
         620303: seq(NOC(), NOC(), NOC(learn=True))}
    line = dst.onset_order_line(t)
    assert line[620301] == {"k_L_vs_k_C": "<", "k_P_vs_k_C": "<"}
    assert line[620302] == {"k_L_vs_k_C": "=", "k_P_vs_k_C": "="}
    assert line[620303] == {"k_L_vs_k_C": "undefined", "k_P_vs_k_C": "undefined"}
    t2 = {1: seq(EXC(), NOC(learn=True), NOC(b2=1.0))}
    assert dst.onset_order_line(t2)[1] == {"k_L_vs_k_C": ">", "k_P_vs_k_C": ">"}


# ---- randomized cross-check against the independent reference ----
def test_random_sequences_match_reference():
    rng = random.Random(197)
    for _ in range(400):
        t = ref.random_table(rng)
        for rows in t.values():
            assert k(dst.onsets(rows)) == ref.onsets(rows)
            assert dst.n_pre(rows) == ref.n_pre(rows)
            p = dst.pre_chart_max(rows)
            assert (None if p is None else Fraction(p)) == ref.pre_chart_max(rows)
            for anchor in ("chart", "learning"):
                assert cat(rows, anchor) == ref.order(rows, anchor)
            for r in rows:
                assert dst.sigma(r) == ref.sigma(r)
                assert (dst.above_s(r), dst.below_s(r), dst.above_s_ok(r)) == (
                    ref.above_s(r), ref.below_s(r), ref.above_s_ok(r))
        line = dst.onset_order_line(t)
        for j, rows in t.items():
            o = ref.onsets(rows)
            assert line[j] == {"k_L_vs_k_C": ref.cmp_line(o["k_L"], o["k_C"]),
                               "k_P_vs_k_C": ref.cmp_line(o["k_P"], o["k_C"])}


def test_categories_are_the_contract_list():
    assert set(dc.CONTRACT["statements"]["order_categories"]) == {
        "NO_CHART", "NO_LEARNING", "CHART_AT_INIT", "BEFORE", "LEARNING_BEFORE_CHART",
        "UNCERTIFIED_AT_ANCHOR", "WITH", "AFTER", "NEVER", "FINAL_NA", "UNRESOLVED"}
    assert CU in dc.CONTRACT["statuses"]["checkpoint"]
