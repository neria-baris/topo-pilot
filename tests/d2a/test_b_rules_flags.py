"""Independent tests (author B, job 0028): T-RULES, the per-model and per-contrast flag functions
of ``d2a_decide`` (learned, stage1_decision, arm_value, carries, low_increment, beta2_pass,
precision_ok, c_hor, c_len, pipeline_null_ok).

Written from D2A-FROZEN-v1 (§0, §6, §10.1-§10.5, rulings D1 and D3) and tools/d2a/API.md (§2.5)
only; no tools/d2a source was read. Thresholds are tested at the exact boundary in the direction
the protocol writes (>= for effect thresholds, > 0 / < 0 for interval bounds).
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/d2a", "tools/d1_seam", "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import d2a_decide as dd  # noqa: E402

NAN = math.nan
EPS = 1e-9
PASS_ARGS = (0.30, 0.15, 0.20, 1e-12)  # every learned() condition met at its boundary


# ------------------------------------------------------------------ learned(m), §6

def test_learned_pass_at_exact_boundaries():
    assert dd.learned(*PASS_ARGS) == "PASS"
    assert dd.learned(0.9, 0.6, 0.7, 0.2) == "PASS"


@pytest.mark.parametrize("slot, value", [
    (0, 0.30 - EPS),   # beta1 >= 0.30
    (1, 0.15 - EPS),   # lower bound >= 0.15
    (2, 0.20 - EPS),   # kappa1 >= 0.20
    (3, 0.0),          # paired lower bound of beta1 - beta1^(8) > 0 (strict)
    (3, -0.01),
    (0, -0.5),
])
def test_learned_defined_fail_on_any_single_condition(slot, value):
    args = list(PASS_ARGS)
    args[slot] = value
    assert dd.learned(*args) == "FAIL"


@pytest.mark.parametrize("slot", range(4))
def test_learned_undefined_statistic_is_unresolved_not_fail(slot):
    args = list(PASS_ARGS)
    args[slot] = NAN
    assert dd.learned(*args) == "UNRESOLVED"


def test_learned_undefined_with_another_failing_condition_is_still_unresolved():
    # §6: a defined FAIL needs every statistic and interval defined
    assert dd.learned(0.05, NAN, 0.5, 0.1) == "UNRESOLVED"
    assert dd.learned(0.05, 0.01, NAN, -0.2) == "UNRESOLVED"


@pytest.mark.parametrize("slot", range(4))
def test_learned_single_none_statistic_of_present_model_is_unresolved(slot):
    # beta() reports an undefined slope as None (API §2.2); §6 forbids turning it into a FAIL
    args = list(PASS_ARGS)
    args[slot] = None
    assert dd.learned(*args) == "UNRESOLVED"


def test_learned_missing_model_is_defined_fail():
    assert dd.learned(None, None, None, None) == "FAIL"


# ------------------------------------------------------------- stage1_decision, §6 / S4

def _ref_stage1(v1, v2):
    if "PASS" in (v1, v2):
        return "GO"
    if (v1, v2) == ("FAIL", "FAIL"):
        return "NOT_LEARNED"
    return "LEARNING_UNRESOLVED"


@pytest.mark.parametrize("v1, v2", list(itertools.product(("PASS", "FAIL", "UNRESOLVED"),
                                                          repeat=2)))
def test_stage1_decision_all_branches(v1, v2):
    assert dd.stage1_decision(v1, v2) == _ref_stage1(v1, v2)


def test_stage1_named_branches():
    assert dd.stage1_decision("PASS", "UNRESOLVED") == "GO"
    assert dd.stage1_decision("FAIL", "FAIL") == "NOT_LEARNED"
    assert dd.stage1_decision("FAIL", "UNRESOLVED") == "LEARNING_UNRESOLVED"
    assert dd.stage1_decision("UNRESOLVED", "UNRESOLVED") == "LEARNING_UNRESOLVED"


# ---------------------------------------------------------------- arm value L, §10.5

def _ref_arm(values):
    n_pass = sum(v == "PASS" for v in values)
    n_unres = sum(v == "UNRESOLVED" for v in values)
    if n_pass >= 3:
        return "TRUE"
    return "FALSE" if n_pass + n_unres < 3 else "UNRESOLVED"


@pytest.mark.parametrize("values", [list(v) for v in itertools.product(
    ("PASS", "FAIL", "UNRESOLVED", None), repeat=4)])
def test_arm_value_exhaustive(values):
    assert dd.arm_value(values) == _ref_arm(values)


@pytest.mark.parametrize("values, expected", [
    (["PASS", "PASS", "PASS", "FAIL"], "TRUE"),
    (["PASS", "PASS", "PASS", None], "TRUE"),
    (["PASS", "PASS", "UNRESOLVED", "FAIL"], "UNRESOLVED"),
    (["PASS", "PASS", "UNRESOLVED", None], "UNRESOLVED"),
    (["PASS", "PASS", None, None], "FALSE"),          # missing models count as failing
    (["PASS", "UNRESOLVED", None, None], "FALSE"),
    (["UNRESOLVED"] * 4, "UNRESOLVED"),
    ([None] * 4, "FALSE"),
])
def test_arm_value_named_cases(values, expected):
    assert dd.arm_value(values) == expected


# ------------------------------------------------- carries / low_increment / beta2_pass, §10.2

@pytest.mark.parametrize("d, d_lo, expected", [
    (0.15, 0.05 + EPS, True),
    (0.15, 0.05, False),          # lower bound must be strictly above 0.05
    (0.15 - EPS, 0.10, False),    # point increment must be >= 0.15
    (0.60, 0.40, True),
    (None, 0.10, False),
    (0.30, None, False),
    (None, None, False),
    (NAN, 0.10, False),
    (0.30, NAN, False),
])
def test_carries(d, d_lo, expected):
    assert bool(dd.carries(d, d_lo)) is expected


@pytest.mark.parametrize("d, expected", [
    (0.05 - EPS, True), (0.05, False), (0.0, True), (-0.3, True), (0.2, False),
    (None, False), (NAN, False),   # an undefined increment fails every per-seed condition
])
def test_low_increment(d, expected):
    assert bool(dd.low_increment(d)) is expected


@pytest.mark.parametrize("b, lo, expected", [
    (0.30, 0.15, True), (0.30 - EPS, 0.20, False), (0.40, 0.15 - EPS, False),
    (1.2, 0.9, True), (None, 0.2, False), (0.5, None, False), (NAN, 0.2, False),
])
def test_beta2_pass(b, lo, expected):
    assert bool(dd.beta2_pass(b, lo)) is expected


# -------------------------------------------------------------------- precision_ok, §10.2

@pytest.mark.parametrize("args, expected", [
    ((0.03, 0.03, 0.05, 0.05), True),
    ((0.01, 0.02, 0.04, 0.0), True),
    ((0.03 + EPS, 0.03, 0.05, 0.05), False),
    ((0.03, 0.03 + EPS, 0.05, 0.05), False),
    ((0.03, 0.03, 0.05 + EPS, 0.05), False),
    ((0.03, 0.03, 0.05, 0.05 + EPS), False),
    ((0.05, 0.03, 0.03, 0.03), False),   # R_pi limit is 0.03, not C_8's 0.05 (argument order)
    ((0.03, 0.05, 0.03, 0.03), False),
    ((None, 0.01, 0.01, 0.01), False),
    ((0.01, 0.01, 0.01, None), False),
    ((0.01, NAN, 0.01, 0.01), False),
])
def test_precision_ok(args, expected):
    assert bool(dd.precision_ok(*args)) is expected


# ------------------------------------------------------------------------- C-HOR, §10.4

@pytest.mark.parametrize("mean, p2_5, per_seed, expected", [
    (0.10, 1e-12, [0.1, 0.1, 0.1, 0.1], "SUPPORTED"),            # boundaries met
    (0.10, 0.01, [0.15, 0.15, 0.1, -0.0], "SUPPORTED"),          # exactly 3 positive
    (0.10 - EPS, 0.01, [0.1, 0.1, 0.1, 0.1], "NOT_SUPPORTED"),   # mean >= 0.10
    (0.20, 0.0, [0.2, 0.2, 0.2, 0.2], "NOT_SUPPORTED"),          # 2.5th percentile > 0 strict
    (0.10, 0.01, [0.2, 0.2, 0.0, 0.0], "NOT_SUPPORTED"),         # 0 is not positive
    (0.25, 0.05, [0.5, 0.5, -0.1, 0.0], "NOT_SUPPORTED"),
    (None, 0.05, [0.2] * 4, "UNRESOLVED"),
    (0.20, None, [0.2] * 4, "UNRESOLVED"),
    (0.20, 0.05, None, "UNRESOLVED"),
    (0.20, 0.05, [0.2, 0.2, 0.2, None], "UNRESOLVED"),           # a missing H1/H2 model
    (0.20, 0.05, [0.2, 0.2, 0.2, NAN], "UNRESOLVED"),            # an undefined score
    (NAN, 0.05, [0.2] * 4, "UNRESOLVED"),
    (0.20, NAN, [0.2] * 4, "UNRESOLVED"),
])
def test_c_hor(mean, p2_5, per_seed, expected):
    assert dd.c_hor(mean, p2_5, per_seed) == expected


# ------------------------------------------------------------------- C-LEN, §10.4, ruling D1

GAIN = (0.10, 1e-12, 0.5, [0.1, 0.1, 0.1, -0.05])
LOSS = (-0.10, -0.5, -1e-12, [-0.1, -0.1, -0.1, 0.05])


def test_c_len_gain_and_loss_at_boundaries():
    assert dd.c_len(*GAIN, True) == "LENGTH_GAIN"
    assert dd.c_len(*LOSS, True) == "LENGTH_LOSS"


@pytest.mark.parametrize("args", [
    (0.10 - EPS, 0.01, 0.5, [0.1, 0.1, 0.1, 0.1]),     # mean >= 0.10
    (0.10, 0.0, 0.5, [0.1, 0.1, 0.1, 0.1]),            # 1.25th percentile > 0 strict
    (0.10, 0.01, 0.5, [0.2, 0.2, 0.0, 0.0]),           # >= 3 positive seeds
    (-0.10 + EPS, -0.5, -0.01, [-0.1] * 4),            # mean <= -0.10
    (-0.10, -0.5, 0.0, [-0.1] * 4),                    # 98.75th percentile < 0 strict
    (-0.10, -0.5, -0.01, [-0.2, -0.2, 0.0, 0.0]),      # >= 3 negative seeds
    (0.0, -0.1, 0.1, [0.01, -0.01, 0.02, -0.02]),
])
def test_c_len_not_detected(args):
    assert dd.c_len(*args, True) == "LENGTH_NOT_DETECTED"


@pytest.mark.parametrize("base", [GAIN, LOSS, (0.0, -0.1, 0.1, [0.0] * 4)])
def test_c_len_precision_failure_overrides_every_result(base):
    # ruling D1: LENGTH_UNRESOLVED takes precedence even when GAIN or LOSS criteria are met
    assert dd.c_len(*base, False) == "LENGTH_UNRESOLVED"


@pytest.mark.parametrize("slot", range(4))
def test_c_len_missing_input_is_unresolved(slot):
    args = list(GAIN)
    args[slot] = None
    assert dd.c_len(*args, True) == "LENGTH_UNRESOLVED"


def test_c_len_missing_or_undefined_seed_is_unresolved():
    assert dd.c_len(0.2, 0.05, 0.5, [0.2, 0.2, 0.2, None], True) == "LENGTH_UNRESOLVED"
    assert dd.c_len(0.2, 0.05, 0.5, [0.2, 0.2, 0.2, NAN], True) == "LENGTH_UNRESOLVED"


# ----------------------------------------------------- pipeline null, §10.1, ruling D3

NULL_KEYS = [("d2a-s1-N", 16), ("d2a-s1-N", 28), ("d2a-s2-N", 16), ("d2a-s2-N", 28)]


def _upper(value, changes=None):
    out = {k: value for k in NULL_KEYS}
    out.update(changes or {})
    return out


def test_pipeline_null_passes_at_boundary():
    assert bool(dd.pipeline_null_ok(_upper(0.02))) is True
    assert bool(dd.pipeline_null_ok(_upper(-0.01))) is True


@pytest.mark.parametrize("key", NULL_KEYS)
@pytest.mark.parametrize("bad", [0.02 + EPS, 0.5, None, NAN])
def test_pipeline_null_any_single_check_fails(key, bad):
    # each N-model x position check is separate; the other three passing never compensates
    assert bool(dd.pipeline_null_ok(_upper(0.0, {key: bad}))) is False


def test_pipeline_null_needs_all_four_checks():
    upper = _upper(0.0)
    del upper[NULL_KEYS[3]]
    assert bool(dd.pipeline_null_ok(upper)) is False


def test_pipeline_null_mean_below_threshold_does_not_rescue():
    # mean of the four upper bounds is 0.015 <= 0.02, but one check is 0.03
    upper = _upper(0.01, {NULL_KEYS[0]: 0.03})
    assert sum(upper.values()) / 4 <= 0.02
    assert bool(dd.pipeline_null_ok(upper)) is False
