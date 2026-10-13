import math

import pytest

from topo_pilot.analysis import SigmaCalibrator, SigmaRow

pytestmark = pytest.mark.analysis

V = 36
LOG2 = math.log(2)
PW = 0.5 / V


def rows_for(sigma, cyl=None, sq=None):
    """cyl/sq: dict overriding the passing defaults for that world."""
    good = dict(mean_H_b1=LOG2 + 0.1, G_C=0.2, min_p_w=PW * 2, V=V)
    out = []
    for world, over in (("cylinder", cyl), ("square", sq)):
        kw = dict(good)
        kw.update(over or {})
        out.append(SigmaRow(sigma=sigma, world=world, **kw))
    return out


def select(*row_groups):
    rows = [r for g in row_groups for r in g]
    return SigmaCalibrator().select(rows)


def test_first_candidate_passes():
    d = select(rows_for(1.25), rows_for(0.75), rows_for(2.0))
    assert d.status == "ok"
    assert d.sigma == 1.25


def test_first_fails_in_one_world_second_passes():
    d = select(rows_for(1.25, sq={"G_C": 0.05}), rows_for(0.75), rows_for(2.0))
    assert d.status == "ok"
    assert d.sigma == 0.75


@pytest.mark.parametrize("world_kw", ["cyl", "sq"])
@pytest.mark.parametrize(
    "bad", [{"mean_H_b1": LOG2 - 0.01}, {"G_C": 0.09}, {"min_p_w": PW * 0.9}]
)
def test_each_criterion_in_each_world_can_fail(world_kw, bad):
    d = select(rows_for(1.25, **{world_kw: bad}), rows_for(0.75))
    assert d.status == "ok"
    assert d.sigma == 0.75


def test_candidate_order_is_first_appearance_not_value():
    d = select(rows_for(2.0), rows_for(0.75), rows_for(1.25))
    assert d.sigma == 2.0


def test_boundaries_pass_exactly():
    edge = dict(mean_H_b1=LOG2, G_C=0.10, min_p_w=0.5 / V)
    d = select(rows_for(1.25, cyl=edge, sq=edge), rows_for(0.75))
    assert d.status == "ok"
    assert d.sigma == 1.25


def test_second_candidate_chosen_even_if_third_better():
    d = select(rows_for(1.25, cyl={"G_C": 0.0}), rows_for(0.75), rows_for(2.0, cyl={"G_C": 5.0}))
    assert d.sigma == 0.75


def test_fallback_weak_context_picks_argmax_min_G_C():
    # none passes (mean_H_b1 too low everywhere); min-over-worlds G_C:
    # 1.25 -> 0.04, 0.75 -> 0.06, 2.0 -> 0.05
    low = {"mean_H_b1": 0.1}
    d = select(
        rows_for(1.25, cyl=dict(low, G_C=0.04), sq=dict(low, G_C=0.09)),
        rows_for(0.75, cyl=dict(low, G_C=0.06), sq=dict(low, G_C=0.08)),
        rows_for(2.0, cyl=dict(low, G_C=0.05), sq=dict(low, G_C=0.50)),
    )
    assert d.status == "weak_context"
    assert d.sigma == 0.75


def test_fallback_uses_min_over_worlds_not_max_or_mean():
    low = {"mean_H_b1": 0.1}
    # 1.25: min 0.03 (mean 0.515), 0.75: min 0.04 (mean 0.045)
    d = select(
        rows_for(1.25, cyl=dict(low, G_C=0.03), sq=dict(low, G_C=1.0)),
        rows_for(0.75, cyl=dict(low, G_C=0.04), sq=dict(low, G_C=0.05)),
    )
    assert d.status == "weak_context"
    assert d.sigma == 0.75


def test_fallback_threshold_exactly_003_accepted():
    low = {"mean_H_b1": 0.1}
    d = select(rows_for(1.25, cyl=dict(low, G_C=0.03), sq=dict(low, G_C=0.03)))
    assert d.status == "weak_context"
    assert d.sigma == 1.25


def test_stop_h3_when_fallback_below_003():
    low = {"mean_H_b1": 0.1}
    d = select(
        rows_for(1.25, cyl=dict(low, G_C=0.029), sq=dict(low, G_C=0.5)),
        rows_for(0.75, cyl=dict(low, G_C=0.01), sq=dict(low, G_C=0.02)),
        rows_for(2.0, cyl=dict(low, G_C=0.0), sq=dict(low, G_C=0.0)),
    )
    assert d.status == "stop_H3"
    assert d.sigma is None


def test_decision_has_reasons_and_table():
    d = select(rows_for(1.25))
    assert hasattr(d, "reasons")
    assert hasattr(d, "table")
    low = {"mean_H_b1": 0.1}
    d2 = select(rows_for(1.25, cyl=dict(low, G_C=0.0)))
    assert d2.status == "stop_H3"
    assert d2.reasons
