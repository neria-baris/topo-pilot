"""Independent tests (author B, job 0028): T-RULES for ``d2a_decide.decide(flags)``.

Written from D2A-FROZEN-v1 (§1.4, §10.4, §10.5, rulings D1 and D3) and tools/d2a/API.md (§2.5,
the ``decide`` flag schema and the qualifier list) only; no tools/d2a source was read. Each test
builds a synthetic flag table, so some tables are deliberately incoherent: they exist only to show
which rule matches first. Seeds are list slots 0..3 (seeds 1..4); a missing model is ``None``.
"""

from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/d2a", "tools/d1_seam", "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import d2a_decide as dd  # noqa: E402

T, F = True, False
P, X, U = "PASS", "FAIL", "UNRESOLVED"
LENGTHS = ("LENGTH_GAIN", "LENGTH_LOSS", "LENGTH_NOT_DETECTED", "LENGTH_UNRESOLVED")


def base():
    """Every arm learned, nothing carried, nothing low: falls to rule 10 (INCONCLUSIVE)."""
    return {
        "s_fail": None, "stage1": "GO", "validity_ok": True,
        "learned": {"H1": [P] * 4, "H2": [P] * 4, "H3": [P] * 4},
        "c_hor": "NOT_SUPPORTED", "delta_h": [0.02, -0.01, 0.0, 0.01],
        "carries": {"H1": [F] * 4, "H2": [F] * 4},
        "low_inc": {"H1": [F] * 4, "H2": [F] * 4},
        "beta2_direct_H2": [F] * 4, "beta2_ar_H1": [F] * 4,
        "precision_ok": {"H1": [T] * 4, "H2": [T] * 4},
        "controls_valid": True, "c_len": "LENGTH_NOT_DETECTED", "world_ceiling_28": 0.10,
        "behaviour": {h: {11: F, 16: F, 28: F} for h in ("H1", "H2", "H3")},
    }


def loud(flags):
    """Make every qualifier source true, so an empty qualifier list is a real check."""
    flags = copy.deepcopy(flags)
    flags["c_len"], flags["world_ceiling_28"] = "LENGTH_GAIN", 0.9
    flags["low_inc"]["H1"], flags["beta2_ar_H1"] = [T] * 4, [T] * 4
    flags["precision_ok"]["H1"][0] = F
    flags["behaviour"]["H2"] = {11: T, 16: T, 28: T}
    return flags


def horizon_dependent():
    f = base()
    f["c_hor"], f["delta_h"] = "SUPPORTED", [0.3, 0.3, 0.3, -0.1]
    f["carries"]["H2"], f["low_inc"]["H1"] = [T, T, T, F], [T, T, T, F]
    return f


def carried():
    f = base()
    f["carries"]["H1"], f["carries"]["H2"] = [T, T, T, F], [T, T, F, T]
    return f


def predictive():
    f = base()
    f["low_inc"]["H2"], f["beta2_direct_H2"] = [T, T, T, F], [T, F, T, T]
    return f


def not_recovered():
    f = base()
    f["low_inc"]["H1"], f["low_inc"]["H2"] = [T, T, F, T], [T, T, T, T]
    f["beta2_direct_H2"] = [T, T, F, F]
    return f


def run(flags):
    res = dd.decide(flags)
    rule = int(re.match(r"\D*(\d+)", str(res["rule"])).group(1))
    return res["outcome"], rule, list(res["qualifiers"])


def lengths(quals):
    return [q for q in quals if q in LENGTHS]


# ---------------------------------------------------------------- rules 1-3 (no qualifiers)

@pytest.mark.parametrize("s_fail, outcome", [
    ("S0", "INVALID"), ("S1", "INVALID"), ("S2", "CONSTRUCTION_FAIL"),
    ("S3", "FEASIBILITY_NO_GO"),
])
def test_rule1_stop_failures(s_fail, outcome):
    f = loud(horizon_dependent())
    f["s_fail"], f["stage1"], f["validity_ok"] = s_fail, "NOT_LEARNED", False
    assert run(f) == (outcome, 1, [])


@pytest.mark.parametrize("stage1", ["NOT_LEARNED", "LEARNING_UNRESOLVED"])
def test_rule2_stage1_stops_precede_validity_and_have_no_qualifiers(stage1):
    f = loud(horizon_dependent())
    f["stage1"], f["validity_ok"] = stage1, False
    assert run(f) == (stage1, 2, [])


def test_rule3_pipeline_invalid_precedes_rule4_and_has_no_qualifiers():
    f = loud(base())
    f["validity_ok"] = False
    f["learned"]["H1"] = [X] * 4  # would be MULTISTEP_ENABLES_LEARNING at rule 4
    assert run(f) == ("PIPELINE_INVALID", 3, [])  # §1.4: qualifiers attach to outcomes 4-10


# --------------------------------------------------------------------------- rule 4

@pytest.mark.parametrize("h1, h2, h3, outcome", [
    ([X] * 4, [P] * 4, [P] * 4, "MULTISTEP_ENABLES_LEARNING"),          # L1 F, L2 T
    ([P, P, X, X], [P, P, P, X], [X] * 4, "MULTISTEP_ENABLES_LEARNING"),
    ([P, P, None, None], [P, P, P, None], [P] * 4, "MULTISTEP_ENABLES_LEARNING"),  # missing fail
    ([X] * 4, [X] * 4, [X] * 4, "LEARNING_UNRESOLVED"),                 # L1 F, L2 F
    ([X] * 4, [P, P, X, X], [P] * 4, "LEARNING_UNRESOLVED"),            # only L3 TRUE
    ([P, P, U, X], [P] * 4, [P] * 4, "LEARNING_UNRESOLVED"),            # L1 UNRESOLVED
    ([P, U, U, None], [X] * 4, [P] * 4, "LEARNING_UNRESOLVED"),
    ([X] * 4, [P, P, U, None], [P] * 4, "LEARNING_UNRESOLVED"),         # L1 F, L2 UNRESOLVED
    ([P, X, X, X], [U, U, U, X], [P] * 4, "LEARNING_UNRESOLVED"),
])
def test_rule4_branches(h1, h2, h3, outcome):
    f = base()
    f["learned"] = {"H1": h1, "H2": h2, "H3": h3}
    got, rule, quals = run(f)
    assert (got, rule) == (outcome, 4)
    assert lengths(quals) == ["LENGTH_NOT_DETECTED"]  # outcomes 4 and 4b carry the qualifier


@pytest.mark.parametrize("h1, h2", [
    ([P] * 4, [P] * 4), ([P, P, P, None], [X] * 4), ([P, P, P, X], [U, U, U, U]),
    ([P, P, P, U], [P, X, None, None]),
])
def test_rule4_l1_true_continues(h1, h2):
    f = base()
    f["learned"]["H1"], f["learned"]["H2"] = h1, h2
    assert run(f)[:2] == ("INCONCLUSIVE", 10)
    f = horizon_dependent()
    f["learned"]["H1"], f["learned"]["H2"] = h1, h2
    assert run(f)[:2] == ("HORIZON_DEPENDENT", 5)


def test_rule4_precedes_rule5():
    f = horizon_dependent()
    f["learned"]["H1"] = [X, X, X, P]
    assert run(f)[:2] == ("MULTISTEP_ENABLES_LEARNING", 4)


# ------------------------------------------------------------------------ rules 5 and 6

def test_rule5_horizon_dependent():
    assert run(horizon_dependent())[:2] == ("HORIZON_DEPENDENT", 5)


def test_rule5_needs_the_same_three_seeds_for_all_conditions():
    f = horizon_dependent()
    f["delta_h"] = [0.3, 0.3, 0.3, -0.1]          # seeds 1, 2, 3
    f["carries"]["H2"] = [F, T, T, T]             # seeds 2, 3, 4
    f["low_inc"]["H1"] = [T, F, T, T]             # seeds 1, 3, 4: only seed 3 is joint
    assert run(f)[:2] == ("HORIZON_ENHANCED", 6)  # rule 6 still has carries H2 in 3 seeds


def test_rule5_two_joint_seeds_is_not_enough():
    f = horizon_dependent()
    f["delta_h"] = [0.3, 0.3, 0.3, 0.3]
    f["carries"]["H2"], f["low_inc"]["H1"] = [T, T, T, F], [T, T, F, T]  # joint: seeds 1, 2
    assert run(f)[:2] == ("HORIZON_ENHANCED", 6)
    f["low_inc"]["H1"] = [T, T, T, T]                                   # joint: seeds 1, 2, 3
    assert run(f)[:2] == ("HORIZON_DEPENDENT", 5)


def test_rule5_nonpositive_or_missing_delta_fails_that_seed():
    f = horizon_dependent()
    f["carries"]["H2"], f["low_inc"]["H1"] = [T] * 4, [T] * 4
    f["delta_h"] = [0.3, 0.3, 0.0, None]          # 0 is not > 0; None is a missing model
    assert run(f)[:2] == ("HORIZON_ENHANCED", 6)
    f["delta_h"] = [0.3, 0.3, 1e-12, None]
    assert run(f)[:2] == ("HORIZON_DEPENDENT", 5)


def test_rule5_missing_h2_model_counts_as_failing():
    f = horizon_dependent()
    f["learned"]["H2"] = [P, P, P, None]
    f["carries"]["H2"], f["low_inc"]["H1"] = [T, T, F, None], [T] * 4
    f["delta_h"] = [0.3, 0.3, 0.3, None]
    # rule 5: joint seeds 1, 2; rule 6: carries H2 in 2 seeds; rule 7 needs NOT_SUPPORTED
    assert run(f)[:2] == ("INCONCLUSIVE", 10)


def test_rule6_horizon_enhanced():
    f = base()
    f["c_hor"], f["delta_h"] = "SUPPORTED", [0.2, 0.2, 0.2, 0.2]
    f["carries"]["H1"], f["carries"]["H2"] = [T] * 4, [T, T, F, T]
    assert run(f)[:2] == ("HORIZON_ENHANCED", 6)


def test_supported_c_hor_without_carries_is_inconclusive():
    f = base()
    f["c_hor"], f["delta_h"] = "SUPPORTED", [0.2, 0.2, 0.2, 0.2]
    f["carries"]["H1"], f["carries"]["H2"] = [T] * 4, [T, T, F, None]
    assert run(f)[:2] == ("INCONCLUSIVE", 10)  # also never rule 7: C-HOR is supported


# --------------------------------------------------------------------------- rule 7

def test_rule7_carried_without_horizon_effect():
    assert run(carried())[:2] == ("CARRIED_WITHOUT_HORIZON_EFFECT", 7)


@pytest.mark.parametrize("arm", ["H1", "H2"])
def test_rule7_needs_both_arms(arm):
    f = carried()
    f["carries"][arm] = [T, T, F, None]
    assert run(f)[:2] == ("INCONCLUSIVE", 10)


def test_unresolved_c_hor_never_fires_rule7():
    f = carried()
    f["c_hor"] = "UNRESOLVED"
    assert run(f)[:2] == ("INCONCLUSIVE", 10)


def test_unresolved_c_hor_can_still_match_a_later_rule():
    f = predictive()
    f["c_hor"] = "UNRESOLVED"
    f["carries"]["H1"], f["carries"]["H2"] = [T] * 4, [T] * 4  # rule 7 would match if resolved
    assert run(f)[:2] == ("PREDICTIVE_WITHOUT_LINEAR_POSTERIOR", 8)
    f["c_hor"] = "NOT_SUPPORTED"
    assert run(f)[:2] == ("CARRIED_WITHOUT_HORIZON_EFFECT", 7)


# ------------------------------------------------------------------------ rules 8 and 9

def test_rule8_predictive_without_linear_posterior():
    assert run(predictive())[:2] == ("PREDICTIVE_WITHOUT_LINEAR_POSTERIOR", 8)


def test_rule8_precedes_rule9():
    f = predictive()
    f["low_inc"]["H1"] = [T] * 4
    assert run(f)[:2] == ("PREDICTIVE_WITHOUT_LINEAR_POSTERIOR", 8)


@pytest.mark.parametrize("key, value", [
    ("beta2_direct_H2", [T, T, F, None]), ("low_inc", [T, T, None, F]),
])
def test_rule8_needs_three_seeds_of_each(key, value):
    f = predictive()
    if key == "low_inc":
        f["low_inc"]["H2"] = value
    else:
        f[key] = value
    assert run(f)[:2] == ("INCONCLUSIVE", 10)


def test_rule9_not_recovered():
    assert run(not_recovered())[:2] == ("NOT_RECOVERED_WITH_REGISTERED_PROBES", 9)


@pytest.mark.parametrize("arm, slot, value", [
    ("H1", 0, F), ("H1", 3, None), ("H2", 2, F), ("H2", 1, None),
])
def test_rule9_precision_failure_gives_inconclusive_precision_limited(arm, slot, value):
    f = not_recovered()
    f["precision_ok"][arm][slot] = value
    outcome, rule, quals = run(f)
    assert (outcome, rule) == ("INCONCLUSIVE", 10)
    assert "PRECISION_LIMITED" in quals


def test_rule9_needs_valid_controls():
    f = not_recovered()
    f["controls_valid"] = False
    outcome, rule, quals = run(f)
    assert (outcome, rule) == ("INCONCLUSIVE", 10)
    assert "PRECISION_LIMITED" not in quals


@pytest.mark.parametrize("arm", ["H1", "H2"])
def test_rule9_needs_low_increment_in_both_arms(arm):
    f = not_recovered()
    f["low_inc"][arm] = [T, T, F, None]
    assert run(f)[:2] == ("INCONCLUSIVE", 10)


def test_split_seeds_are_inconclusive():
    f = base()
    f["carries"]["H1"], f["carries"]["H2"] = [T, T, F, F], [T, T, F, F]
    f["low_inc"]["H1"], f["low_inc"]["H2"] = [F, F, T, T], [F, F, T, T]
    f["beta2_direct_H2"] = [F, F, T, T]
    assert run(f)[:2] == ("INCONCLUSIVE", 10)


def test_first_match_ladder():
    """All of rules 5-9 hold; removing one condition at a time walks down the order."""
    f = base()
    f["c_hor"], f["delta_h"] = "SUPPORTED", [0.2] * 4
    for arm in ("H1", "H2"):
        f["carries"][arm], f["low_inc"][arm] = [T] * 4, [T] * 4
    f["beta2_direct_H2"] = [T] * 4
    steps = [(None, "HORIZON_DEPENDENT", 5),
             (("delta_h", [-0.1] * 4), "HORIZON_ENHANCED", 6),
             (("c_hor", "NOT_SUPPORTED"), "CARRIED_WITHOUT_HORIZON_EFFECT", 7),
             (("carries", {"H1": [F] * 4, "H2": [F] * 4}),
              "PREDICTIVE_WITHOUT_LINEAR_POSTERIOR", 8),
             (("beta2_direct_H2", [F] * 4), "NOT_RECOVERED_WITH_REGISTERED_PROBES", 9),
             (("controls_valid", False), "INCONCLUSIVE", 10)]
    for change, outcome, rule in steps:
        if change:
            f[change[0]] = change[1]
        assert run(f)[:2] == (outcome, rule)
