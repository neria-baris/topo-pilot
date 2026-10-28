"""HWSB author A: outcomes, licences, HANDOFF blindness and B7 (protocol §5.1, §5.2, §6.1, RC-6;
§4 B7; DRB11).

Targets (API.md §6.4, §6.5): hwsb_gates.outcome, licence, handoff_record, check_handoff, b7.
Every row of §5.1 is planted, with the precedence of API §6.5 / choice 18. Licence texts are
expected from CONTRACT.json `licences` filled independently here; the "does not license"
clauses are the protocol §5.2 wording. Synthetic numbers only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_oracle_profile", "tools/x4_circle_history", "tools/c1prime_registry",
             "tools/c1prime", "tools/k4b", "tools/hws"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

try:
    import hwsb_config as hc  # noqa: E402
    import hwsb_gates as hg  # noqa: E402
except ImportError as _exc:  # the implementation is written in parallel
    hc = hg = None
    MISSING = repr(_exc)
else:
    MISSING = None

CONTRACT = json.loads((REPO / "tools" / "hwsb" / "CONTRACT.json").read_text(encoding="utf-8"))
LIC = CONTRACT["licences"]
KEYS = CONTRACT["handoff"]["keys"]
FORBIDDEN = CONTRACT["handoff"]["forbidden_keys"]
A, B = 620201, 620202
NO_STATEMENT = "No scientific statement is licensed."

# protocol §5.2 "does not license" clauses (ASCII w*)
CLAUSES = {
    "HWSB_PASS": ["that any circle carries beyond-four information (pilot statistics are "
                  "uncertified, multiplicity-uncontrolled and on pilot models)",
                  "that stage C will reach SUPPORT",
                  "that new stage-C models will pass their gates",
                  "anything about the E4 models, K4b's EXCLUSION or any earlier verdict",
                  "that w* is optimal"],
    "HWSB_NOT_LEARNED": ["that w* is unlearnable, or that a longer or larger recipe would fail",
                         "any statement about the circle"],
    "HWSB_NO_CIRCLE": ["that no circular structure exists (another chart method might find it)",
                       "anything about E4"],
    "HWSB_UNDERPOWERED": ["absence of the effect", "an effect below the margin as a finding"],
}


def need():
    if MISSING:
        pytest.fail("tools/hwsb modules not importable: " + MISSING)


def state(**kw):
    """An all-PASS state (API §6.5 keys); keyword arguments override."""
    s = {"fail": None, "incomplete": None, "b1": {A: "PASS", B: "PASS"},
         "b4": {A: "PASS", B: "PASS"}, "b6": "PASS", "b5": {A: "PASS", B: "PASS"},
         "b5_positive": False, "b8a": "PASS", "b9a": "PASS"}
    s.update(kw)
    return s


class NA(dict):
    def __missing__(self, key):
        return "n/a"


def fill_ref(head, fill, oc, models_text=None):
    vals = NA(fill)
    vals.update({"k": oc.get("k"), "models": oc.get("models") if models_text is None
                 else models_text, "criterion": oc.get("criterion")})
    return LIC[head].format_map(vals)


# ------------------------------------------------------------- pure reference checks

def test_reference_contract_licences_carry_protocol_clauses():
    for head, clauses in CLAUSES.items():
        assert "It does not license:" in LIC[head]
        for c in clauses:
            assert c in LIC[head], (head, c)
    assert LIC["FAIL_TECHNICAL"] == NO_STATEMENT
    assert LIC["INCONCLUSIVE/RESOURCE_OR_AUTHORITY"] == NO_STATEMENT
    assert "bootstrap lower bound > 0" in LIC["POSITIVE_BELOW_PLANNING"]
    assert set(FORBIDDEN) >= {"mean_X_minus", "c_hat", "c_min", "ci95", "regret", "captured",
                              "fidelity", "D4hat", "dev_ce"}


# ------------------------------------------------------------- §5.1 rows and precedence

def test_all_pass_is_hwsb_pass():
    need()
    oc = hg.outcome(state())
    assert oc["outcome"] == "HWSB_PASS" and list(oc["annotations"]) == []


@pytest.mark.parametrize("fail, expected", [
    ("FAIL_TECHNICAL/NONFINITE", "FAIL_TECHNICAL/NONFINITE"),
    ("LINEAGE", "FAIL_TECHNICAL/LINEAGE"),
    ("FAIL_TECHNICAL/KNOWN_CASE", "FAIL_TECHNICAL/KNOWN_CASE"),
])
def test_recorded_technical_failure_beats_everything(fail, expected):
    need()
    s = state(fail=fail, incomplete="lost process", b1={A: "INCONCLUSIVE", B: "FAIL"},
              b4={A: "C0_CAL", B: "C0_VAL"}, b6="FAIL", b5={A: "FAIL", B: "FAIL"},
              b5_positive=True, b8a="FAIL_TECHNICAL/LAW_BOUND", b9a="FAIL_TECHNICAL/REGISTRY")
    oc = hg.outcome(s)
    assert oc["outcome"] == expected
    assert "POSITIVE_BELOW_PLANNING" not in list(oc["annotations"])
    assert hg.outcome(state(fail=fail))["outcome"] == expected


def test_b1_inconclusive_is_numerical_failure():
    need()
    for b1 in ({A: "INCONCLUSIVE", B: "PASS"}, {A: "FAIL", B: "INCONCLUSIVE"}):
        s = state(b1=b1, b8a="FAIL_TECHNICAL/LAW_BOUND", incomplete="hold STOP")
        assert hg.outcome(s)["outcome"] == "FAIL_TECHNICAL/NUMERICAL"


def test_b8a_and_b9a_failures_even_when_b1_fails():
    need()
    bad_b1 = {A: "FAIL", B: "FAIL"}
    assert hg.outcome(state(b1=bad_b1, b8a="FAIL_TECHNICAL/LAW_BOUND"))["outcome"] == \
        "FAIL_TECHNICAL/LAW_BOUND"
    assert hg.outcome(state(b1=bad_b1, b9a="FAIL_TECHNICAL/REGISTRY"))["outcome"] == \
        "FAIL_TECHNICAL/REGISTRY"
    both = state(b8a="FAIL_TECHNICAL/LAW_BOUND", b9a="FAIL_TECHNICAL/REGISTRY")
    assert hg.outcome(both)["outcome"] == "FAIL_TECHNICAL/LAW_BOUND"
    # any non-PASS value that was computed counts (API §6.5 rule 3)
    assert hg.outcome(state(b8a="UNAVAILABLE"))["outcome"] == "FAIL_TECHNICAL/LAW_BOUND"
    assert hg.outcome(state(b9a="FAIL"))["outcome"] == "FAIL_TECHNICAL/REGISTRY"
    assert hg.outcome(state(incomplete="x", b9a="FAIL"))["outcome"] == "FAIL_TECHNICAL/REGISTRY"


def test_incomplete_before_any_scientific_outcome():
    need()
    s = state(incomplete="owner STOP at hold step 1000", b1={A: "FAIL", B: "PASS"},
              b4={A: "C0_CAL", B: "PASS"}, b6="FAIL")
    assert hg.outcome(s)["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    assert hg.outcome(state(incomplete="AUTH expired"))["outcome"] == \
        "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


@pytest.mark.parametrize("b1, k", [({A: "FAIL", B: "PASS"}, 1), ({A: "PASS", B: "FAIL"}, 1),
                                   ({A: "FAIL", B: "FAIL"}, 2)])
def test_not_learned_with_k(b1, k):
    need()
    oc = hg.outcome(state(b1=b1, b4={A: "C0_CAL", B: "C0_VAL"}, b6="FAIL",
                          b5={A: "FAIL", B: "FAIL"}, b5_positive=True))
    assert oc["outcome"] == "HWSB_NOT_LEARNED" and oc["k"] == k
    assert "POSITIVE_BELOW_PLANNING" not in list(oc["annotations"])


@pytest.mark.parametrize("b4, outcome, models", [
    ({A: "C0_CAL", B: "PASS"}, "HWSB_NO_CIRCLE/C0_CAL", [A]),
    ({A: "PASS", B: "C0_VAL"}, "HWSB_NO_CIRCLE/C0_VAL", [B]),
    ({A: "C0_VAL", B: "C0_CAL"}, "HWSB_NO_CIRCLE/C0_VAL", [A, B]),
    ({B: "C0_CAL", A: "C0_VAL"}, "HWSB_NO_CIRCLE/C0_VAL", [A, B]),   # MASTERS order, not dict
])
def test_no_circle_with_criterion_and_models(b4, outcome, models):
    need()
    oc = hg.outcome(state(b4=b4, b6="FAIL", b5={A: "FAIL", B: "FAIL"}, b5_positive=True))
    assert oc["outcome"] == outcome
    assert list(oc["models"]) == models
    assert oc["criterion"] == outcome.split("/")[1]
    assert "POSITIVE_BELOW_PLANNING" not in list(oc["annotations"])


def test_underpowered_ladder_before_capture():
    need()
    oc = hg.outcome(state(b6="FAIL", b5={A: "FAIL", B: "PASS"}, b5_positive=True))
    assert oc["outcome"] == "HWSB_UNDERPOWERED/LADDER"
    assert "POSITIVE_BELOW_PLANNING" not in list(oc["annotations"])
    assert hg.outcome(state(b6="FAIL"))["outcome"] == "HWSB_UNDERPOWERED/LADDER"


@pytest.mark.parametrize("positive", [True, False])
def test_underpowered_capture_and_annotation(positive):
    need()
    oc = hg.outcome(state(b5={A: "PASS", B: "FAIL"}, b5_positive=positive))
    assert oc["outcome"] == "HWSB_UNDERPOWERED/CAPTURE"
    assert list(oc["annotations"]) == (["POSITIVE_BELOW_PLANNING"] if positive else [])


def test_pass_needs_every_gate():
    need()
    assert hg.outcome(state(b5_positive=True))["outcome"] == "HWSB_PASS"
    assert list(hg.outcome(state(b5_positive=True))["annotations"]) == []
    for kw in ({"b6": None}, {"b5": None}, {"b8a": None}, {"b9a": None}):
        oc = hg.outcome(state(**kw))
        assert oc["outcome"] == "FAIL_TECHNICAL/OUTCOME", kw


def test_unmatched_state_is_returned_not_raised():
    need()
    oc = hg.outcome(state(b6=None, b5=None))
    assert oc["outcome"] == "FAIL_TECHNICAL/OUTCOME"


# ------------------------------------------------------------- licences (§5.2)

PASS_FILL = {"N_C": 6144, "training_forecast_s": 7500.0, "Z_bound": "1234567/10000000000"}


def test_licence_pass_filled():
    need()
    oc = {"outcome": "HWSB_PASS", "k": None, "models": [], "criterion": None,
          "annotations": []}
    text = hg.licence(oc, PASS_FILL)
    assert text == fill_ref("HWSB_PASS", PASS_FILL, oc)
    assert "N_C = 6144" in text and "7500.0 CPU-s" in text and "1234567/10000000000" in text
    for c in CLAUSES["HWSB_PASS"]:
        assert c in text


def test_licence_missing_field_is_na():
    need()
    oc = {"outcome": "HWSB_PASS", "k": None, "models": [], "criterion": None,
          "annotations": []}
    text = hg.licence(oc, {"N_C": 3072})
    assert "Z_bound(w*) = n/a." in text and "forecast of n/a CPU-s" in text


def test_licence_not_learned():
    need()
    oc = {"outcome": "HWSB_NOT_LEARNED", "k": 1, "models": [A], "criterion": None,
          "annotations": []}
    text = hg.licence(oc, {})
    assert text == fill_ref("HWSB_NOT_LEARNED", {}, oc)
    assert text.startswith("With the E4 recipe unchanged, 1 of 2 pilot models")
    for c in CLAUSES["HWSB_NOT_LEARNED"]:
        assert c in text


def test_licence_no_circle_uses_head_template():
    need()
    oc = {"outcome": "HWSB_NO_CIRCLE/C0_VAL", "k": None, "models": [B],
          "criterion": "C0_VAL", "annotations": []}
    text = hg.licence(oc, {})
    # API-AMBIGUITY: API §6.5 fills {models} by str.format_map from oc["models"] (a list); a
    # joined rendering of the model ids is also accepted.
    assert text in {fill_ref("HWSB_NO_CIRCLE", {}, oc),
                    fill_ref("HWSB_NO_CIRCLE", {}, oc, models_text=str(B))}
    assert "(criterion C0_VAL)" in text and str(B) in text
    for c in CLAUSES["HWSB_NO_CIRCLE"]:
        assert c in text


@pytest.mark.parametrize("positive", [False, True])
def test_licence_underpowered_with_annotation(positive):
    need()
    for outcome in ("HWSB_UNDERPOWERED/CAPTURE", "HWSB_UNDERPOWERED/LADDER"):
        ann = ["POSITIVE_BELOW_PLANNING"] if positive and outcome.endswith("CAPTURE") else []
        oc = {"outcome": outcome, "k": None, "models": [], "criterion": None,
              "annotations": ann}
        text = hg.licence(oc, {})
        expected = LIC["HWSB_UNDERPOWERED"] + (" " + LIC["POSITIVE_BELOW_PLANNING"] if ann
                                               else "")
        assert text == expected
        for c in CLAUSES["HWSB_UNDERPOWERED"]:
            assert c in text


@pytest.mark.parametrize("outcome", ["FAIL_TECHNICAL/LAW_BOUND", "FAIL_TECHNICAL/REGISTRY",
                                     "FAIL_TECHNICAL/OUTCOME", "FAIL_TECHNICAL/NUMERICAL",
                                     "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"])
def test_licence_no_statement(outcome):
    need()
    oc = {"outcome": outcome, "k": None, "models": [], "criterion": None, "annotations": []}
    assert hg.licence(oc, PASS_FILL) == NO_STATEMENT


def test_licence_from_outcome_end_to_end():
    need()
    oc = hg.outcome(state(b5={A: "FAIL", B: "FAIL"}, b5_positive=True))
    text = hg.licence(oc, {})
    assert text == LIC["HWSB_UNDERPOWERED"] + " " + LIC["POSITIVE_BELOW_PLANNING"]


# ------------------------------------------------------------- HANDOFF blindness (RC-6)

def full_fields():
    return {k: f"value-{i}" for i, k in enumerate(KEYS)}


def test_check_handoff_accepts_clean_record():
    need()
    rec = full_fields()
    rec["store_inventory"] = {"hist/LGATE.npz": "ab" * 32, "hist/VAL.npz": "cd" * 32}
    rec["stage_c_exclusions"] = ["0123456789abcdef"]
    assert hg.check_handoff(rec) is None


@pytest.mark.parametrize("key", FORBIDDEN)
def test_check_handoff_refuses_forbidden_key_at_any_depth(key):
    need()
    for rec in ({**full_fields(), key: 1},
                {**full_fields(), "store_inventory": {"a": {key: 0.5}}},
                {**full_fields(), "stage_c_exclusions": [{"x": {key: 0.5}}]}):
        with pytest.raises(hc.HwsbStop) as ei:
            hg.check_handoff(rec)
        assert ei.value.status == "FAIL_TECHNICAL/BLINDNESS"


def test_check_handoff_refuses_extra_top_level_key():
    need()
    with pytest.raises(hc.HwsbStop) as ei:
        hg.check_handoff({**full_fields(), "notes": "harmless"})
    assert ei.value.status == "FAIL_TECHNICAL/BLINDNESS"


def test_handoff_record_keeps_exactly_the_contract_keys():
    need()
    rec = hg.handoff_record({**full_fields(), "notes": "dropped"})
    assert set(rec) == set(KEYS) and len(rec) == len(KEYS)
    assert all(rec[k] == full_fields()[k] for k in KEYS)


def test_handoff_record_refuses_missing_key_and_nested_forbidden():
    need()
    fields = full_fields()
    del fields["Z_bound"]
    with pytest.raises(hc.HwsbStop) as ei:
        hg.handoff_record(fields)
    assert ei.value.status == "FAIL_TECHNICAL/BLINDNESS"
    with pytest.raises(hc.HwsbStop):
        hg.handoff_record({**full_fields(), "store_inventory": {"c_hat": 0.4}})


# ------------------------------------------------------------- B7 (report only)

def test_b7_forecasts():
    need()
    cpu = {A: 2345.0, B: 2820.9}
    for N_C in (3072, 6144, 12288):
        res = hg.b7(cpu, N_C)
        assert res["model_count"] == 3
        assert res["training_forecast_s"] == pytest.approx(3 * 2820.9, rel=1e-15)
        assert res["evaluation_forecast_s"] == pytest.approx(1280.5 + 1720.1 * N_C / 3072,
                                                             rel=1e-12)
        assert res["cpu_by_model"] == cpu
    assert hg.b7(cpu, 3072)["evaluation_forecast_s"] == pytest.approx(3000.6, rel=1e-12)


def test_b7_without_measurements_is_unavailable():
    need()
    res = hg.b7({}, 3072)
    assert res["model_count"] == 3
    assert res["training_forecast_s"] == "unavailable"
    assert res["evaluation_forecast_s"] == "unavailable"
