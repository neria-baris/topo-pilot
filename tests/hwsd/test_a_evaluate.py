"""Author A (job 0197): evaluate, diagnostics, reading texts and the outcome precedence.

PROTOCOL_HWSD_v1.md §5.2 (k_C^+, onset-order line), §5.6 (MC diagnostic), §5.7, §8.1, §8.2;
API.md §7 (evaluate, diagnostics) and §8 (fill_templates, outcome_d); decision 9 (HEADROOM).
"""

from __future__ import annotations

import re
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
import hwsd_summary as dsum  # noqa: E402
import test_a_hwsd_ref as ref  # noqa: E402
from test_a_hwsd_ref import EXC, NOC, SC, SU, SUP, UC, UNR, UNV, row, seq  # noqa: E402

J = (620301, 620302, 620303)
NE = "NOT_EVALUABLE"


def table(*rows_per_model):
    return dict(zip(J, rows_per_model))


def category(v):  # API-AMBIGUITY: evaluate's order entries may be the order() dict or its category
    return v["category"] if isinstance(v, dict) else v


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from strings(v)


AFTER = seq(NOC(), EXC(learn=True), SUP(b2=0.1), SUP())


def test_evaluate_structure_and_values():
    t = table(AFTER, seq(NOC(), SUP(learn=True)), seq(EXC(), SUP()))
    ev = dst.evaluate(t)
    for key in ("onsets", "n_pre", "pre_chart_max", "order", "statements", "onset_order_line",
                "diagnostics"):
        assert key in ev
    assert set(ev["statements"]) == {"D1", "D2", "D3", "D4", "D5", "D6"}
    for j, rows in t.items():
        o = ref.onsets(rows)
        assert {k: ev["onsets"][j][k] for k in o} == o
        assert ev["n_pre"][j] == ref.n_pre(rows)
        assert category(ev["order"][j]["chart"]) == ref.order(rows, "chart")
        assert category(ev["order"][j]["learning"]) == ref.order(rows, "learning")
    want = ref.evaluate(t)
    for s, (reading, reasons) in want.items():
        assert ev["statements"][s]["reading"] == reading, s
        if reading == NE:
            got = {r: sorted(m) for r, m in ev["statements"][s]["reasons"].items()}
            assert got == reasons
    assert ev["statements"]["D3"]["reading"] == "FALSE"  # WITH in 620302 beats CHART_AT_INIT


def test_evaluate_headroom_and_resource():
    t = table(AFTER, AFTER, AFTER)
    full = dst.evaluate(t)
    assert full["statements"]["D3"]["reading"] == "TRUE"
    hr = dst.evaluate(t, headroom_ok=False)
    for s in ("D1", "D2", "D3", "D4", "D5", "D6"):
        assert hr["statements"][s]["reading"] == NE
        assert {r: sorted(m) for r, m in hr["statements"][s]["reasons"].items()} == {
            "HEADROOM": list(J)}
    assert hr["onsets"] == full["onsets"] and hr["n_pre"] == full["n_pre"]
    assert hr["order"] == full["order"]
    rs = dst.evaluate(t, headroom_ok=False, resource_ok=False)  # RESOURCE before HEADROOM
    for s in ("D1", "D2", "D3", "D4", "D5", "D6"):
        assert set(rs["statements"][s]["reasons"]) == {"RESOURCE"}
    rs2 = dst.evaluate(t, resource_ok=False)
    assert set(rs2["statements"]["D6"]["reasons"]) == {"RESOURCE"}


def test_evaluate_any_sequence_length():  # decision 20: sigma(12) reads sigma(K)
    t = table(seq(SUP()), seq(NOC(), EXC()), seq(*([NOC()] * 11), SUP()))
    ev = dst.evaluate(t)
    assert ev["statements"]["D1"]["reading"] == "FALSE"
    assert ev["onsets"][J[2]]["k_C"] == 12


def test_diagnostics_mc_positive():
    mc1 = row(SC, L=0.01, U=0.02, L_S=0.012, U_S=0.03)  # L^S > L
    mc2 = row(SU, L=0.01, U=0.02, L_S=0.0, U_S=0.019)  # U^S < U
    unc = row(UC, L=0.01, U=0.02, L_S=0.011, U_S=0.03)  # has arrays, uncertified
    rows = seq(NOC(), mc1, EXC(), mc2, unc, SUP(), UNV(), UNR())
    d = dst.diagnostics({J[0]: rows})[J[0]]
    steps = [r["step"] for r in rows]
    assert sorted(d["mc"]) == sorted([steps[1], steps[3], steps[4]])
    # positive: est and L - F- > 0 (UNCERTIFIED is not est; EXC has L < 0)
    assert sorted(d["positive"]) == sorted([steps[1], steps[3], steps[5], steps[6], steps[7]])


def test_diagnostics_chart_at_init_rc4():
    rows = seq(EXC(), NOC(), SUP(), SUP())
    d = dst.diagnostics({J[0]: rows})[J[0]]
    assert d["chart_at_init"]["sigma_step0"] == "EXCLUDE"
    assert d["chart_at_init"]["order_at_k_C_plus"] == "WITH"
    d = dst.diagnostics({J[0]: seq(SUP(), SUP())})[J[0]]
    assert d["chart_at_init"]["sigma_step0"] == "SUPPORT"
    assert d["chart_at_init"]["order_at_k_C_plus"] == "NO_CHART"
    d = dst.diagnostics({J[0]: seq(SUP(), NOC(), EXC(), SUP())})[J[0]]
    assert d["chart_at_init"]["order_at_k_C_plus"] == "BEFORE"


def test_diagnostics_est_loss_only_unvalidated_k1():
    rows = seq(NOC(), UNV(), SUP(), EXC())
    d = dst.diagnostics({J[0]: rows})[J[0]]
    assert sorted(tuple(p) for p in d["est_loss"]) == [(2, 4)]  # (3, 4) is a real LOSS (D6)
    assert dst.d6(rows)["reading"] == "FALSE"


def test_fill_templates_texts():
    t = table(AFTER, AFTER, AFTER)
    ev = dst.evaluate(t)
    texts = list(strings(dsum.fill_templates(ev, t)))
    tpl = dc.CONTRACT["statements"]["templates"]
    assert texts and not any(re.search(r"\{[A-Za-z_]+\}", s) for s in texts)  # all filled
    assert tpl["D6_TRUE"] in texts
    assert any(s.startswith(tpl["D3_TRUE"].split("{")[0]) for s in texts)
    assert any("is not evaluable" in s for s in texts)  # D2 BY_CONSTRUCTION in all three


def test_fill_templates_d4_second_sentence_and_d3_chart_at_init():
    t = table(seq(NOC(), EXC(learn=True), SUP()), seq(NOC(), EXC(learn=True), SUP()),
              seq(EXC(learn=True), SUP()))
    ev = dst.evaluate(t)
    assert ev["statements"]["D4"]["reading"] == "TRUE"
    texts = list(strings(dsum.fill_templates(ev, t)))
    tpl = dc.CONTRACT["statements"]["templates"]
    assert any("Captured 0.8 can be reached with last-four information alone" in s for s in texts)
    assert any(tpl["D3_CHART_AT_INIT"] in s for s in texts)


def test_fill_templates_missing_field_reads_n_a(monkeypatch):
    t = table(AFTER, AFTER, AFTER)
    ev = dst.evaluate(t)
    tpls = dc.CONTRACT["statements"]["templates"]
    monkeypatch.setitem(tpls, "D6_TRUE", tpls["D6_TRUE"] + " [{no_such_field_a}]")
    texts = list(strings(dsum.fill_templates(ev, t)))
    assert any("[n/a]" in s for s in texts)


def test_outcome_precedence():
    base = {"fail": None, "resource": False, "registry": False, "headroom": False, "partial": []}

    def out(**kw):
        return dsum.outcome_d(dict(base, **kw))["outcome"]

    assert out() == "HWSD_REPORT"
    assert out(headroom=True) == "INCONCLUSIVE/HEADROOM"
    assert out(registry=True, headroom=True) == "INCONCLUSIVE/REGISTRY_INCOMPLETE"
    assert out(resource=True, registry=True, headroom=True, partial=[J[0]]) == (
        "INCONCLUSIVE/RESOURCE_OR_AUTHORITY")
    assert out(fail="FAIL_TECHNICAL/NUMERICAL", resource=True) == "FAIL_TECHNICAL/NUMERICAL"
    assert out(fail="LINEAGE", headroom=True) == "FAIL_TECHNICAL/LINEAGE"
    assert dc.CONTRACT["outcomes"]["precedence"][-1] == "HWSD_REPORT"


def test_order_categories_reachable_in_evaluate():
    rows = {
        "NO_CHART": seq(NOC()), "CHART_AT_INIT": seq(EXC(), SUP()),
        "BEFORE": seq(UNV(), EXC(), SUP()), "UNCERTIFIED_AT_ANCHOR": seq(NOC(), SUP(status=UC)),
        "WITH": seq(NOC(), SUP()), "AFTER": seq(NOC(), EXC(), SUP()),
        "NEVER": seq(NOC(), EXC()), "FINAL_NA": seq(NOC(), EXC(), NOC()),
        "UNRESOLVED": seq(NOC(), EXC(), UNR()),
    }
    for name, r in rows.items():
        ev = dst.evaluate({J[0]: r})
        assert category(ev["order"][J[0]]["chart"]) == name
    assert Fraction(1, 100) == dc.M
