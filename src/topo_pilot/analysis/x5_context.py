"""X5 G1 context gate and verdict precedence (x5g1-feas-v2 §5, §8)."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

GC_THRESHOLD = 0.03
PASS, FAIL, NEAR_THRESHOLD, INVALID_PREDICTIVE = ("PASS", "FAIL", "NEAR_THRESHOLD",
                                                  "INVALID_PREDICTIVE")


def percentile_interval(values: NDArray) -> tuple[float, float]:
    """``np.quantile(values, [0.025, 0.975], method="linear")``."""
    lo, hi = np.quantile(np.asarray(values, float), [0.025, 0.975], method="linear")
    return float(lo), float(hi)


def context_status(lo: float, hi: float, valid: bool = True) -> str:
    """PASS iff ``lo >= 0.03``; FAIL iff ``hi < 0.03`` (a valid G_C of 0 included);
    NEAR_THRESHOLD otherwise; INVALID_PREDICTIVE only for invalid or non-finite input."""
    if not valid or not (math.isfinite(lo) and math.isfinite(hi)):
        return INVALID_PREDICTIVE
    if lo >= GC_THRESHOLD:
        return PASS
    if hi < GC_THRESHOLD:
        return FAIL
    return NEAR_THRESHOLD


def x5_overall_verdict(arms: dict[str, dict], global_failed: list[str],
                       global_inconclusive: list[str]) -> tuple[str, str]:
    """Precedence FAILED > INCONCLUSIVE > WEAK_CONTEXT > FEASIBLE (a weak arm never conceals an
    invalid one). Arm dicts carry ``op`` and ``context`` (None when not computed)."""
    if global_failed:
        return "FAILED", global_failed[0]
    for name, a in arms.items():
        if a.get("op") == "FAILED":
            return "FAILED", f"arm {name} FAILED"
    if global_inconclusive:
        return "INCONCLUSIVE", global_inconclusive[0]
    for name, a in arms.items():
        if a.get("op") in ("INVALID_KERNEL", "NEAR_UNIT_GAP"):
            return "INCONCLUSIVE", f"arm {name} {a['op']}"
        if a.get("context") in (INVALID_PREDICTIVE, NEAR_THRESHOLD, None):
            return "INCONCLUSIVE", f"arm {name} context {a.get('context')}"
    for name, a in arms.items():
        if a.get("context") == FAIL:
            return "WEAK_CONTEXT", f"arm {name} G_C upper bound < {GC_THRESHOLD}"
    return "FEASIBLE", "both kernels valid and G_C PASS in both arms"
