"""Author A (job 0176): outcome precedence, gate-record mapping and licences.

Protocol HWSC §6.1-§6.4; DRC5, DRC7. API.md §12.1 (`outcome`,
`state_from_gates`), §12.3 (`licence`); CONTRACT `outcomes`, `licences`,
`disclosure`. Written from the specification only.
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[:1] != [_HWSC]:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402,I001
import hwsc_bind as cb  # noqa: E402
import hwsc_gates as cg  # noqa: E402
import k4b_stats  # noqa: E402

C = cc.CONTRACT
LIC = C["licences"]
J1, J2, J3 = 620301, 620302, 620303
MODELS = (J1, J2, J3)
NO_STATEMENT = "No scientific statement is licensed."
FS = Fraction(1, 10**9) + Fraction(1, 10**12)


def state(**kw):
    s = {"fail": None, "resource": None, "l1": None, "k4b": None,
         "criterion": None, "models": None, "endpoint": None}
    s.update(kw)
    return s


def endpoint(spec):
    """spec {j: (L, U)} -> an ENDPOINT-like result (statuses by k4b_stats)."""
    pm = {}
    with cb.bound_stage_c():
        for j, (L, U) in spec.items():
            r = k4b_stats.model_status(L, U, FS, FS)
            pm[j] = {"L": L, "U": U, "F_minus": str(FS), "F_plus": str(FS),
                     "status": r["status"], "labels": list(r["labels"]),
                     "status_without_F": r["status_without_F"]}
        overall = k4b_stats.overall({j: pm[j]["status"] for j in MODELS})
    return {"per_model": pm, "overall": overall, "fresh_B4": {"status": "PASS"},
            "N": 3072, "k": 1}


ALL = dict(fail="FAIL_TECHNICAL/LINEAGE", resource="meter safe-STOP",
           l1={"k": 2, "models": [J1, J2]}, k4b="INCONCLUSIVE/HEADROOM",
           endpoint=None)


# ------------------------------------------------------------------- outcome


def test_fail_beats_everything():
    ep = endpoint({j: (0.05, 0.06) for j in MODELS})
    oc = cg.outcome(state(**dict(ALL, endpoint=ep)))
    assert oc["outcome"] == "FAIL_TECHNICAL/LINEAGE"
    oc = cg.outcome(state(**dict(ALL, fail="NONFINITE")))
    assert oc["outcome"] == "FAIL_TECHNICAL/NONFINITE"


def test_resource_beats_not_learned_and_k4b():
    oc = cg.outcome(state(**dict(ALL, fail=None)))
    assert oc["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


@pytest.mark.parametrize("k", [1, 2, 3])
def test_not_learned_beats_k4b(k):
    models = list(MODELS[:k])
    oc = cg.outcome(state(l1={"k": k, "models": models}, k4b="INCONCLUSIVE/HEADROOM",
                          endpoint=endpoint({j: (0.05, 0.06) for j in MODELS})))
    assert oc["outcome"] == "INCONCLUSIVE/NOT_LEARNED"
    assert oc["k"] == k
    assert [int(m) for m in oc["models"]] == models
    assert oc["label"] == f"INCONCLUSIVE/NOT_LEARNED ({k}/3)"


@pytest.mark.parametrize("reason", C["outcomes"]["k4b_reasons"])
def test_k4b_reasons_pass_through(reason):
    st = f"INCONCLUSIVE/{reason}"
    kw = {"k4b": st}
    if reason == "CHART_UNAVAILABLE":
        kw.update(criterion="GIANT", models=[J2])
    oc = cg.outcome(state(**kw))
    assert oc["outcome"] == st
    if reason == "CHART_UNAVAILABLE":
        assert oc["criterion"] == "GIANT"
        assert [int(m) for m in oc["models"]] == [J2]


def test_k4b_beats_endpoint():
    oc = cg.outcome(state(k4b="INCONCLUSIVE/UNDERPOWERED",
                          endpoint=endpoint({j: (0.05, 0.06) for j in MODELS})))
    assert oc["outcome"] == "INCONCLUSIVE/UNDERPOWERED"


@pytest.mark.parametrize("st", ["INCONCLUSIVE/AUTHORITY", "INCONCLUSIVE/RESOURCE"])
def test_authority_resource_map_to_row2(st):
    assert cg.outcome(state(k4b=st))["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


def test_unknown_inconclusive_reason_is_fail_technical():
    assert cg.outcome(state(k4b="INCONCLUSIVE/SOMETHING_ELSE"))["outcome"] == \
        "FAIL_TECHNICAL/OUTCOME"


@pytest.mark.parametrize("spec, expected", [
    ({j: (0.05, 0.06) for j in MODELS}, "SUPPORT"),
    ({j: (0.002, 0.005) for j in MODELS}, "EXCLUSION"),
    ({J1: (0.05, 0.06), J2: (0.002, 0.005), J3: (0.0, 0.02)}, "MIXED"),
    ({j: (0.0, 0.02) for j in MODELS}, "INCONCLUSIVE"),
])
def test_endpoint_passes_through_with_annotations(spec, expected):
    ep = endpoint(spec)
    assert ep["overall"] == expected
    oc = cg.outcome(state(endpoint=ep))
    assert oc["outcome"] == expected
    assert list(oc["annotations"]) == list(cg.annotations(ep))
    assert oc["pbm"] == cg.positive_below_margin(ep["per_model"])


def test_endpoint_inconclusive_numerical():
    ep = endpoint({J1: (0.0, 0.02), J2: (0.01 + 5e-10, 0.02), J3: (0.0, 0.02)})
    assert ep["per_model"][J2]["status"] == "UNRESOLVED/NUMERICAL"
    assert cg.outcome(state(endpoint=ep))["outcome"] == "INCONCLUSIVE/NUMERICAL"


def test_empty_state_returns_fail_technical_outcome():
    oc = cg.outcome(state())
    assert oc["outcome"] == "FAIL_TECHNICAL/OUTCOME"


def test_literally_empty_dict_state():
    # API-AMBIGUITY: TEST_PLAN "empty state" read as {} (no keys at all).
    oc = cg.outcome({})
    assert oc["outcome"] == "FAIL_TECHNICAL/OUTCOME"


# ---------------------------------------------------------- state_from_gates


def rec(gate, status, **details):
    return dict({"gate": gate, "status": status, "utc": "2026-10-29T00:00:00Z"}, **details)


PASSES = [rec("G0C", "PASS"), rec("H1C", "PASS"), rec("REG1", "PASS"), rec("H2", "PASS")]


def test_state_from_gates_fail_first():
    recs = PASSES + [rec("L1", "FAIL_TECHNICAL/NUMERICAL"), rec("ORACLE-VAL", "NOT_RUN")]
    st = cg.state_from_gates(recs)
    assert st["fail"] == "FAIL_TECHNICAL/NUMERICAL"
    assert cg.outcome(st)["outcome"] == "FAIL_TECHNICAL/NUMERICAL"


@pytest.mark.parametrize("status", ["INCONCLUSIVE/RESOURCE_OR_AUTHORITY",
                                    "INCONCLUSIVE/AUTHORITY", "INCONCLUSIVE/RESOURCE"])
def test_state_from_gates_resource(status):
    st = cg.state_from_gates([rec("G0C", status), rec("H1C", "NOT_RUN")])
    assert st["resource"]
    assert cg.outcome(st)["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


def test_state_from_gates_not_learned():
    recs = PASSES + [rec("L1", "INCONCLUSIVE/NOT_LEARNED", k=1, models=[J2],
                         reason="1/3: [620302]"),
                     rec("ORACLE-VAL", "NOT_RUN")]
    # API-AMBIGUITY: L1 details may come from the gate record or from the
    # L1.json record; both carry k = 1 and models [620302] here.
    l1_record = {"per_model": {}, "failing": [J2], "k": 1}
    st = cg.state_from_gates(recs, l1_record=l1_record)
    assert st["l1"]["k"] == 1
    oc = cg.outcome(st)
    assert oc["outcome"] == "INCONCLUSIVE/NOT_LEARNED"
    assert oc["k"] == 1
    assert oc["label"] == "INCONCLUSIVE/NOT_LEARNED (1/3)"


def test_state_from_gates_k4b_and_endpoint():
    st = cg.state_from_gates(PASSES + [rec("L1", "PASS"), rec("B4-VAL", "INCONCLUSIVE/HEADROOM")])
    assert st["k4b"] == "INCONCLUSIVE/HEADROOM"
    assert cg.outcome(st)["outcome"] == "INCONCLUSIVE/HEADROOM"
    ep = endpoint({j: (0.002, 0.005) for j in MODELS})
    st = cg.state_from_gates(PASSES + [rec("L1", "PASS"), rec("ENDPOINT", "PASS")], result=ep)
    assert st["endpoint"] == ep
    assert cg.outcome(st)["outcome"] == "EXCLUSION"


# -------------------------------------------------------------------- licence


class _NA(dict):
    def __missing__(self, key):
        return "n/a"


FILL = {"N": "3072", "a": "11", "b": "12", "c": "13", "values": "V-VALUES",
        "B4": "B4-VALUE", "delta4_orc": "D4-VALUE",
        "delta4_orc_certified": True, "delta4_orc_lower": 0.02}


def oc_of(outcome, k=None, models=None, criterion=None, annotations=(), pbm=None):
    return {"outcome": outcome, "label": outcome, "k": k, "models": models,
            "criterion": criterion, "annotations": list(annotations), "pbm": pbm}


def expected(head, fill, oc):
    d = _NA(fill)
    d.update({"k": oc["k"], "models": oc["models"], "criterion": oc["criterion"]})
    for key in ("k", "models", "criterion"):
        if d[key] is None:
            d[key] = "n/a"
    return LIC[head].format_map(d)


def test_support_licence_exact():
    oc = oc_of("SUPPORT")
    text = cg.licence(oc, dict(FILL))
    assert text == expected("SUPPORT", FILL, oc)
    for v in ("3072", "11/3072", "V-VALUES", "B4-VALUE", "D4-VALUE"):
        assert v in text


def test_missing_fields_are_na():
    text = cg.licence(oc_of("SUPPORT"), {})
    assert "n/a" in text
    assert "{" not in text and "}" not in text


def excl(fill):
    return cg.licence(oc_of("EXCLUSION"), fill)


def test_exclusion_oracle_sentence_rules():
    base = expected("EXCLUSION", FILL, oc_of("EXCLUSION"))
    ora, tail = LIC["EXCLUSION_ORACLE_SENTENCE"], LIC["EXCLUSION_TAIL"]
    t = excl(dict(FILL))
    assert t == base + " " + ora + " " + tail
    t = excl(dict(FILL, delta4_orc_lower=0.01))  # strict: 0.01 exactly -> omitted
    assert ora not in t and t.endswith(tail)
    assert t == base + " " + tail
    t = excl(dict(FILL, delta4_orc_certified=False, delta4_orc_lower=0.5))
    assert ora not in t and t == base + " " + tail
    t = excl(dict(FILL, delta4_orc_lower=0.0100000001))
    assert ora in t and t.endswith(tail)


@pytest.mark.parametrize("outcome", ["FAIL_TECHNICAL/LINEAGE", "FAIL_TECHNICAL/OUTCOME",
                                     "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"])
def test_no_statement_heads(outcome):
    assert cg.licence(oc_of(outcome), dict(FILL)) == NO_STATEMENT


def test_not_learned_and_chart_unavailable_texts():
    t = cg.licence(oc_of("INCONCLUSIVE/NOT_LEARNED", k=2, models=[J1, J3]), dict(FILL))
    assert "2 of 3 new models" in t
    assert "The beyond-four question was not tested." in t
    t = cg.licence(oc_of("INCONCLUSIVE/CHART_UNAVAILABLE", models=[J2],
                         criterion="C0-val fidelity"), dict(FILL))
    assert str(J2) in t and "C0-val fidelity" in t
    assert t.startswith("The models learned (L1 PASS)")


@pytest.mark.parametrize("outcome", ["MIXED", "INCONCLUSIVE", "INCONCLUSIVE/NUMERICAL",
                                     "INCONCLUSIVE/HEADROOM", "INCONCLUSIVE/UNDERPOWERED",
                                     "INCONCLUSIVE/REGISTRY_INCOMPLETE"])
def test_limitation_heads(outcome):
    t = cg.licence(oc_of(outcome), dict(FILL))
    assert t == "Only the recorded per-model results and the identified limitations."


def test_every_contract_head_fills():
    heads = {"SUPPORT": "SUPPORT", "EXCLUSION": "EXCLUSION", "MIXED": "MIXED",
             "INCONCLUSIVE": "INCONCLUSIVE", "INCONCLUSIVE/NOT_LEARNED": "INCONCLUSIVE/NOT_LEARNED",
             "INCONCLUSIVE/CHART_UNAVAILABLE": "INCONCLUSIVE/CHART_UNAVAILABLE",
             "FAIL_TECHNICAL": "FAIL_TECHNICAL/IDENTITY",
             "INCONCLUSIVE/RESOURCE_OR_AUTHORITY": "INCONCLUSIVE/RESOURCE_OR_AUTHORITY",
             "INCONCLUSIVE/<K4b reason>": "INCONCLUSIVE/HEADROOM"}
    for head, outcome in heads.items():
        oc = oc_of(outcome, k=1, models=[J1], criterion="GIANT")
        t = cg.licence(oc, dict(FILL))
        assert t.startswith(expected(head, FILL, oc)[:40]), head
        assert not re.search(r"\{[A-Za-z_0-9]+\}", t), head


def test_positive_below_margin_licence_sentences():
    ep = endpoint({J1: (0.05, 0.06), J2: (0.002, 0.005), J3: (0.002, 0.02)})
    oc = cg.outcome(state(endpoint=ep))
    assert oc["outcome"] == "MIXED"
    t = cg.licence(oc, dict(FILL))
    head = LIC["POSITIVE_BELOW_MARGIN"].split("{models}")
    assert t.startswith(LIC["MIXED"])
    assert head[0] in t and head[1] in t
    assert LIC["POSITIVE_BELOW_MARGIN_EXCLUDE"] in t
    assert LIC["POSITIVE_BELOW_MARGIN_UNRESOLVED"] in t
    tail = t[t.index(head[0]):]
    assert str(J2) in tail and str(J3) in tail and str(J1) not in tail


def test_pbm_licence_only_exclude_kind():
    ep = endpoint({j: (0.002, 0.005) for j in MODELS})
    oc = cg.outcome(state(endpoint=ep))
    assert oc["outcome"] == "EXCLUSION"
    t = cg.licence(oc, dict(FILL, delta4_orc_certified=False))
    assert LIC["EXCLUSION_TAIL"] in t
    assert LIC["POSITIVE_BELOW_MARGIN_EXCLUDE"] in t
    assert LIC["POSITIVE_BELOW_MARGIN_UNRESOLVED"] not in t


# ----------------------------------------------------------------- disclosure


def test_disclosure_equals_protocol_6_4():
    text = cc.PROTOCOL_PATH.read_text(encoding="utf-8")
    sec = text[text.index("### 6.4 Disclosure carried by every report"):]
    line = sec.splitlines()[1].strip()
    assert line.startswith('"') and line.endswith('"')
    # the protocol is Markdown: "w\*" is the escaped "w*"
    proto = line[1:-1].replace("\\*", "*")
    assert C["disclosure"] == proto
    assert C["disclosure"].encode("utf-8") == proto.encode("utf-8")
    assert cc.DISCLOSURE == C["disclosure"]
