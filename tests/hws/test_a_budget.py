"""Author A (job 0119): frozen CPU rates, stage forecasts and the two 3x pause triggers.

TEST_PLAN §2 `test_a_budget.py`; protocol §9.1-§9.3 (MD-16, OPEN-2; choice 26 strict ">").
Worklists are built here from the protocol's levels; expected sums are computed here.
"""

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HWS_DIR = str(REPO / "tools" / "hws")
if HWS_DIR not in sys.path:
    sys.path.insert(0, HWS_DIR)

import hws_worlds as hw  # noqa: E402
import hws_select as hsel  # noqa: E402

F = Fraction
P = [F(1, 5), F(1, 2), F(3, 4), F(7, 8), F(15, 16)]
S = [F(5, 4), F(3, 2), F(2), F(5, 2), F(3)]
CELLS = [(8, 1), (12, 1), (12, 2), (16, 1), (16, 2), (16, 3)]  # E3-eligible cells (§4.4)
SCREEN = {8: 4, 12: 8, 16: 13}


def _s1_max():
    return [hw.World(W, q, s, p) for W, q in CELLS for s in S for p in P]


def _x1_max():
    return [hw.World(W, q, s, p) for W, q in CELLS for s in S + [F(7, 2), F(4)]
            for p in P + [F(31, 32)] if not (s in S and p in P)]


@pytest.mark.parametrize("stage", ["S1", "X1", "S2"])
def test_screening_rates(stage):
    for W, q in CELLS:
        assert hsel.rate(stage, hw.World(W, q, F(5, 4), F(1, 5))) == SCREEN[W]


def test_s3_rates_and_s0_refused():
    assert hsel.rate("S3", hw.World(8, 1, F(2), F(1, 2))) == 70
    assert hsel.rate("S3", hw.World(12, 1, F(2), F(1, 2))) == 190  # tier 0
    assert hsel.rate("S3", hw.World(12, 2, F(2), F(1, 2))) == 160  # tier 1
    assert hsel.rate("S3", hw.World(16, 3, F(2), F(1, 2))) == 235
    with pytest.raises(ValueError):
        hsel.rate("S0", hw.W0)


def test_fixed_forecasts():
    assert hsel.forecast("S0", []) == 360
    assert hsel.forecast("J1", []) == 540


def test_maximal_s1_and_x1_forecasts():
    s1, x1 = _s1_max(), _x1_max()
    assert len(s1) == 150 and len(x1) == 102
    assert sum(1 for w in x1 if w.W == 8) == 17 and sum(1 for w in x1 if w.W == 16) == 51
    assert hsel.forecast("S1", s1) == 25 * 4 + 50 * 8 + 75 * 13 == 1475
    assert hsel.forecast("X1", x1) == 17 * 4 + 34 * 8 + 51 * 13 == 1003


def test_s2_and_s3_forecasts_are_sums_over_the_actual_worklist():
    s2 = [hw.World(12, 1, F(11, 8), F(1, 5))] * 32 + [hw.World(16, 1, F(5, 4), F(3, 8))] * 8
    assert hsel.forecast("S2", s2) == 32 * 8 + 8 * 13 == 360  # the §9.2 central S2 figure
    w16 = [hw.World(16, 1, F(5, 4), F(1, 5))] * 40
    assert hsel.forecast("S2", w16) == 520 and 3 * 520 == 1560
    mix = ([hw.World(8, 1, F(2), F(1, 2))] * 4 + [hw.World(12, 1, F(2), F(1, 2))] * 4
           + [hw.World(12, 2, F(2), F(1, 2))] * 4 + [hw.World(16, 2, F(2), F(1, 2))] * 4)
    assert hsel.forecast("S3", mix) == 4 * (70 + 190 + 160 + 235) == 2620
    assert hsel.forecast("S3", [hw.World(16, 1, F(3), F(1, 2))] * 16) == 3760
    assert 3 * 3760 == 11280  # §9.3 per-stage S3 maximum
    assert hsel.forecast("S3", []) == 0  # no finalist: S3 complete by definition


def test_pause_check_strict_triggers():
    none = hsel.pause_check(300.0, 100, 900.0, 300)  # exactly 3x on both: no pause
    assert not none["pause"] and none["trigger"] is None
    stage = hsel.pause_check(300.001, 100, 900.0, 300)
    assert stage["pause"] and stage["trigger"] == "STAGE"
    cum = hsel.pause_check(10.0, 100, 900.001, 300)
    assert cum["pause"] and cum["trigger"] == "CUMULATIVE"
    both = hsel.pause_check(301.0, 100, 901.0, 300)
    assert both["pause"] and both["trigger"] == "BOTH"


def _cumulative_table():
    s0, s1, x1 = 360, hsel.forecast("S1", _s1_max()), hsel.forecast("X1", _x1_max())
    s2, s3 = 360, 3200  # §9.2 central S2 and S3 figures (maximal worklists)
    return [("after S0", s0, 1080), ("after S1", s0 + s1, 5505),
            ("after X1", s0 + s1 + x1, 8514), ("after S2, no X1", s0 + s1 + s2, 6585),
            ("after S2, X1", s0 + s1 + x1 + s2, 9594),
            ("after S3, no X1", s0 + s1 + s2 + s3, 16185),
            ("after S3, X1", s0 + s1 + x1 + s2 + s3, 19194)]


def test_cumulative_thresholds_of_the_protocol_table():
    for name, fc, threshold in _cumulative_table():
        assert 3 * fc == threshold, name
        at = hsel.pause_check(0.0, 1, float(threshold), fc)
        assert not at["pause"], name
        above = hsel.pause_check(0.0, 1, threshold + 0.5, fc)
        assert above["pause"] and above["trigger"] == "CUMULATIVE", name


def test_per_stage_thresholds_of_the_protocol_table():
    for stage, fc, threshold in (("S0", 360, 1080), ("S1", 1475, 4425), ("X1", 1003, 3009)):
        assert 3 * fc == threshold
        assert not hsel.pause_check(float(threshold), fc, 0.0, 10**6)["pause"], stage
        got = hsel.pause_check(threshold + 0.5, fc, 0.0, 10**6)
        assert got["pause"] and got["trigger"] == "STAGE", stage
