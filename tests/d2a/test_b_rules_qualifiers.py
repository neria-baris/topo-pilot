"""Independent tests (author B, job 0028): T-RULES qualifiers of ``d2a_decide.decide(flags)``.

Written from D2A-FROZEN-v1 (§1.4 qualifiers, §10.4 ruling D1, §10.5 qualifiers) and
tools/d2a/API.md (§2.5 qualifier list) only; no tools/d2a source was read. Qualifiers are compared
as sets; ``BEHAVIOUR(H, t)`` is matched by its prefix and its two integers (H number, t), because
API.md does not fix its spelling.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/d2a", "tools/d1_seam", "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import d2a_decide as dd  # noqa: E402

T, F, P, X = True, False, "PASS", "FAIL"
LENGTHS = ("LENGTH_GAIN", "LENGTH_LOSS", "LENGTH_NOT_DETECTED", "LENGTH_UNRESOLVED")
FIXED = ("PRECISION_LIMITED", "WORLD_CONDITIONAL_CEILING", "CAVEAT_REREAD")


def base():
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


def multistep():
    f = base()
    f["learned"]["H1"] = [X] * 4
    return f


def horizon_dependent():
    f = base()
    f["c_hor"], f["delta_h"] = "SUPPORTED", [0.3, 0.3, 0.3, -0.1]
    f["carries"]["H2"], f["low_inc"]["H1"] = [T, T, T, F], [T, T, T, F]
    return f


def enhanced():
    f = base()
    f["c_hor"], f["delta_h"] = "SUPPORTED", [0.2] * 4
    f["carries"]["H1"], f["carries"]["H2"] = [T] * 4, [T] * 4
    return f


def carried():
    f = base()
    f["carries"]["H1"], f["carries"]["H2"] = [T] * 4, [T] * 4
    return f


def predictive():
    f = base()
    f["low_inc"]["H2"], f["beta2_direct_H2"] = [T] * 4, [T] * 4
    return f


def not_recovered():
    f = base()
    f["low_inc"]["H1"], f["low_inc"]["H2"] = [T] * 4, [T] * 4
    return f


CASES = [(multistep, "MULTISTEP_ENABLES_LEARNING"), (horizon_dependent, "HORIZON_DEPENDENT"),
         (enhanced, "HORIZON_ENHANCED"), (carried, "CARRIED_WITHOUT_HORIZON_EFFECT"),
         (predictive, "PREDICTIVE_WITHOUT_LINEAR_POSTERIOR"),
         (not_recovered, "NOT_RECOVERED_WITH_REGISTERED_PROBES"), (base, "INCONCLUSIVE")]


def run(flags):
    res = dd.decide(flags)
    return res["outcome"], [str(q) for q in res["qualifiers"]]


def behaviour_cells(quals):
    out = set()
    for q in quals:
        if q.startswith("BEHAVIOUR"):
            h, t = re.findall(r"\d+", q)
            out.add((int(h), int(t)))
    return out


def test_builders_hit_their_outcomes():
    for make, outcome in CASES:
        assert run(make())[0] == outcome


@pytest.mark.parametrize("make, outcome", CASES)
def test_quiet_table_carries_only_the_length_qualifier(make, outcome):
    got, quals = run(make())
    assert got == outcome
    assert sorted(quals) == ["LENGTH_NOT_DETECTED"]


@pytest.mark.parametrize("c_len", LENGTHS)
@pytest.mark.parametrize("make, outcome", CASES)
def test_length_qualifier_on_outcomes_4_to_10(make, outcome, c_len):
    f = make()
    f["c_len"] = c_len
    got, quals = run(f)
    assert got == outcome  # the C-LEN result never changes the main outcome
    assert [q for q in quals if q in LENGTHS] == [c_len]


def test_length_qualifier_on_rule4_learning_unresolved():
    f = base()
    f["learned"]["H1"], f["learned"]["H2"] = [X] * 4, [X] * 4
    f["c_len"] = "LENGTH_UNRESOLVED"
    got, quals = run(f)
    assert got == "LEARNING_UNRESOLVED" and "LENGTH_UNRESOLVED" in quals


@pytest.mark.parametrize("arm, slot, value", [
    ("H1", 0, F), ("H1", 3, None), ("H2", 1, F), ("H2", 2, None),
])
@pytest.mark.parametrize("make, outcome", [c for c in CASES if c[0] is not not_recovered])
def test_precision_limited_on_any_h1_or_h2_failure(make, outcome, arm, slot, value):
    f = make()
    f["precision_ok"][arm][slot] = value
    got, quals = run(f)
    assert got == outcome  # the qualifier only flags; rule 9 is the only outcome it changes
    assert "PRECISION_LIMITED" in quals


def test_precision_limited_turns_outcome9_into_inconclusive():
    f = not_recovered()
    f["precision_ok"]["H2"][0] = F
    got, quals = run(f)
    assert got == "INCONCLUSIVE" and "PRECISION_LIMITED" in quals


@pytest.mark.parametrize("ceiling, present", [
    (0.30, True), (0.95, True), (0.30 - 1e-9, False), (0.0, False), (None, False),
])
@pytest.mark.parametrize("make", [enhanced, base, multistep])
def test_world_conditional_ceiling_threshold(make, ceiling, present):
    f = make()
    f["world_ceiling_28"] = ceiling
    assert ("WORLD_CONDITIONAL_CEILING" in run(f)[1]) is present


@pytest.mark.parametrize("low_h1, ar_h1, present", [
    ([T, T, T, F], [T, T, T, F], True),
    ([T, T, T, F], [F, T, T, T], True),        # counted separately, not as matched seeds
    ([T, T, T, T], [T, T, F, None], False),
    ([T, T, F, None], [T, T, T, T], False),
    ([F] * 4, [T] * 4, False),
])
def test_caveat_reread(low_h1, ar_h1, present):
    f = horizon_dependent()
    f["low_inc"]["H1"], f["beta2_ar_H1"] = low_h1, ar_h1
    assert ("CAVEAT_REREAD" in run(f)[1]) is present


def test_caveat_reread_on_not_recovered():
    f = not_recovered()
    f["beta2_ar_H1"] = [T, T, T, None]
    got, quals = run(f)
    assert got == "NOT_RECOVERED_WITH_REGISTERED_PROBES" and "CAVEAT_REREAD" in quals


def test_behaviour_cells_exactly_the_true_ones():
    f = carried()
    f["behaviour"] = {"H1": {11: F, 16: T, 28: F}, "H2": {11: T, 16: F, 28: T},
                      "H3": {11: F, 16: F, 28: T}}
    got, quals = run(f)
    assert got == "CARRIED_WITHOUT_HORIZON_EFFECT"
    assert behaviour_cells(quals) == {(1, 16), (2, 11), (2, 28), (3, 28)}
    assert sum(q.startswith("BEHAVIOUR") for q in quals) == 4


def test_all_qualifiers_together():
    f = horizon_dependent()
    f["c_len"], f["world_ceiling_28"] = "LENGTH_LOSS", 0.5
    f["beta2_ar_H1"] = [T] * 4
    f["precision_ok"]["H1"][2] = F
    f["behaviour"]["H3"][16] = T
    got, quals = run(f)
    assert got == "HORIZON_DEPENDENT"
    assert set(quals) >= {"LENGTH_LOSS", *FIXED}
    assert behaviour_cells(quals) == {(3, 16)}
    assert len(quals) == 5


@pytest.mark.parametrize("change", [
    {"s_fail": "S2"}, {"s_fail": "S0"}, {"stage1": "NOT_LEARNED"},
    {"stage1": "LEARNING_UNRESOLVED"}, {"validity_ok": False},
])
def test_no_qualifiers_for_outcomes_1_to_3(change):
    f = horizon_dependent()
    f["c_len"], f["world_ceiling_28"] = "LENGTH_GAIN", 0.5
    f["beta2_ar_H1"], f["precision_ok"]["H2"] = [T] * 4, [F] * 4
    f["behaviour"]["H2"] = {11: T, 16: T, 28: T}
    f.update(change)
    assert run(f)[1] == []
