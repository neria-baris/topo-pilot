"""Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
before reading the implementation.

Context gate and verdict (protocol x5g1-feas-v2 §5 and §8, API §2 ``x5_context``). The verdict
function is exported as ``x5_overall_verdict`` (conductor correction: ``overall_verdict``
belongs to the X4 Phase B screen).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from topo_pilot.analysis import (
    GC_THRESHOLD,
    context_status,
    percentile_interval,
    x5_overall_verdict,
)

pytestmark = pytest.mark.analysis


def _arm(op="ok", context="PASS"):
    return {"op": op, "context": context}


def _verdict(a0, a020, failed=(), inconclusive=()):
    return x5_overall_verdict({"a0": a0, "a020": a020}, list(failed), list(inconclusive))


# ---------------------------------------------------------------- percentile interval


def test_threshold_constant():
    assert GC_THRESHOLD == 0.03


def test_percentile_interval_matches_numpy_linear():
    rng = np.random.default_rng(11)
    vals = rng.gamma(2.0, 0.02, size=2000)
    lo, hi = percentile_interval(vals)
    ref = np.quantile(vals, [0.025, 0.975], method="linear")
    assert (lo, hi) == (ref[0], ref[1])
    assert lo <= hi


def test_percentile_interval_hand_value():
    # 0..40: linear quantiles at 0.025 * 40 = 1 and 0.975 * 40 = 39
    lo, hi = percentile_interval(np.arange(41, dtype=np.float64))
    assert lo == pytest.approx(1.0, abs=1e-12) and hi == pytest.approx(39.0, abs=1e-12)
    # 0..10: positions 0.25 and 9.75 (interpolated, not nearest)
    lo, hi = percentile_interval(np.arange(11, dtype=np.float64))
    assert lo == pytest.approx(0.25, abs=1e-12) and hi == pytest.approx(9.75, abs=1e-12)


# ---------------------------------------------------------------- context status


def test_lower_exactly_threshold_passes():
    assert context_status(0.03, 0.05) == "PASS"
    assert context_status(0.03, 0.03) == "PASS"


def test_upper_exactly_threshold_is_near():
    assert context_status(0.01, 0.03) == "NEAR_THRESHOLD"
    assert context_status(0.029999, 0.2) == "NEAR_THRESHOLD"


def test_upper_below_threshold_fails():
    assert context_status(0.01, 0.0299999) == "FAIL"
    assert context_status(0.0, 0.0) == "FAIL"             # valid G_C of exactly 0
    assert context_status(0.0, 0.0, valid=True) == "FAIL"
    assert context_status(1e-9, 2e-9) == "FAIL"


@pytest.mark.parametrize("lo,hi", [(math.nan, 0.05), (0.04, math.inf), (-math.inf, 0.0),
                                   (math.nan, math.nan)])
def test_non_finite_is_invalid(lo, hi):
    assert context_status(lo, hi) == "INVALID_PREDICTIVE"


def test_invalid_flag_beats_values():
    assert context_status(0.05, 0.06, valid=False) == "INVALID_PREDICTIVE"
    assert context_status(0.0, 0.0, valid=False) == "INVALID_PREDICTIVE"


# ---------------------------------------------------------------- overall verdict


def test_all_pass_feasible():
    verdict, reason = _verdict(_arm(), _arm())
    assert verdict == "FEASIBLE" and isinstance(reason, str)


def test_global_failed_beats_everything():
    verdict, reason = _verdict(_arm(), _arm(), failed=["integrity"])
    assert verdict == "FAILED" and "integrity" in reason
    verdict, _ = _verdict(_arm("INVALID_KERNEL", "INVALID_PREDICTIVE"), _arm("ok", "FAIL"),
                          failed=["integrity"], inconclusive=["stop"])
    assert verdict == "FAILED"


def test_arm_op_failed_gives_failed():
    verdict, reason = _verdict(_arm(), _arm("FAILED", None))
    assert verdict == "FAILED" and "a020" in reason
    verdict, _ = _verdict(_arm("FAILED", "PASS"), _arm("NEAR_UNIT_GAP", "FAIL"),
                          inconclusive=["budget"])
    assert verdict == "FAILED"


def test_invalid_kernel_plus_weak_arm_is_inconclusive():
    # a weak arm can never conceal an invalid one
    verdict, reason = _verdict(_arm("INVALID_KERNEL", None), _arm("ok", "FAIL"))
    assert verdict == "INCONCLUSIVE" and "a0" in reason
    verdict, _ = _verdict(_arm("ok", "FAIL"), _arm("INVALID_KERNEL", "PASS"))
    assert verdict == "INCONCLUSIVE"


def test_near_unit_gap_is_inconclusive():
    assert _verdict(_arm(), _arm("NEAR_UNIT_GAP", "PASS"))[0] == "INCONCLUSIVE"


def test_near_threshold_plus_fail_is_inconclusive():
    assert _verdict(_arm("ok", "NEAR_THRESHOLD"), _arm("ok", "FAIL"))[0] == "INCONCLUSIVE"
    assert _verdict(_arm("ok", "FAIL"), _arm("ok", "NEAR_THRESHOLD"))[0] == "INCONCLUSIVE"


def test_invalid_predictive_is_inconclusive():
    assert _verdict(_arm("ok", "INVALID_PREDICTIVE"), _arm("ok", "FAIL"))[0] == "INCONCLUSIVE"


def test_context_none_is_inconclusive():
    verdict, reason = _verdict(_arm(), _arm("ok", None))
    assert verdict == "INCONCLUSIVE" and "a020" in reason


def test_global_inconclusive():
    verdict, reason = _verdict(_arm(), _arm(), inconclusive=["STOP"])
    assert verdict == "INCONCLUSIVE" and "STOP" in reason
    assert _verdict(_arm("ok", "FAIL"), _arm(), inconclusive=["budget"])[0] == "INCONCLUSIVE"


def test_one_fail_other_pass_is_weak_context():
    verdict, reason = _verdict(_arm("ok", "FAIL"), _arm())
    assert verdict == "WEAK_CONTEXT" and "a0" in reason
    assert _verdict(_arm(), _arm("ok", "FAIL"))[0] == "WEAK_CONTEXT"
    assert _verdict(_arm("ok", "FAIL"), _arm("ok", "FAIL"))[0] == "WEAK_CONTEXT"


def test_verdict_is_pure():
    arms = {"a0": _arm(), "a020": _arm("ok", "FAIL")}
    before = {k: dict(v) for k, v in arms.items()}
    assert x5_overall_verdict(arms, [], []) == x5_overall_verdict(arms, [], [])
    assert arms == before
