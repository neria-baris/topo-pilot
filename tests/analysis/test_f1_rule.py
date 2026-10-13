"""Independent tests N01-N06 for the F1 decision rule (RESEARCH_SUMMARY 7.4)."""
import itertools

import numpy as np
import pytest

from topo_pilot.analysis import F1Decision
from topo_pilot.contracts import StageFailure

pytestmark = pytest.mark.analysis


def make_table(cf, ci, sf, si, panels=None):
    panels = panels or list(range(1, len(cf) + 1))
    S = {}
    for k, p in enumerate(panels):
        S[("cylinder", "final", p)] = cf[k]
        S[("cylinder", "init", p)] = ci[k]
        S[("square", "final", p)] = sf[k]
        S[("square", "init", p)] = si[k]
    return S


# ---------------------------------------------------------------- N01
def test_contrasts_known_answer():
    # cyl diff: .8 .6 .4 .2 ; sq diff: .1 0 .4 .8  ->  D = .7 .6 0 -.6
    S = make_table([0.9, 0.8, 0.7, 0.6], [0.1, 0.2, 0.3, 0.4],
                   [0.2, 0.1, 0.5, 0.9], [0.1, 0.1, 0.1, 0.1])
    D = F1Decision().contrasts(S)
    assert D.shape == (4,)
    np.testing.assert_allclose(D, [0.7, 0.6, 0.0, -0.6], atol=1e-12)


def test_contrasts_ordered_by_sorted_panel_ids():
    S1 = make_table([1.0, 2.0, 3.0, 4.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                    panels=[1, 3, 5, 8])
    S2 = dict(reversed(list(S1.items())))
    np.testing.assert_allclose(F1Decision().contrasts(S2), [1.0, 2.0, 3.0, 4.0])


def test_contrasts_missing_key_is_invalid_config():
    S = make_table([1, 1], [0, 0], [0, 0], [0, 0])
    del S[("square", "init", 2)]
    with pytest.raises(StageFailure) as ei:
        F1Decision().contrasts(S)
    assert ei.value.code.value == "INVALID_CONFIG"


# ---------------------------------------------------------------- N02
def test_noise_envelope_known_answer():
    # cyl-final [0,1,2,4]: diffs sorted 1,1,2,2,3,4 -> q95 = 3 + .75*1 = 3.75
    # sq-init  [0,2,4,8]: diffs sorted 2,2,4,4,6,8 -> q95 = 6 + .75*2 = 7.5 (the max cell)
    S = make_table([0, 1, 2, 4], [0, 0.1, 0.2, 0.3], [1, 1, 1, 1], [0, 2, 4, 8])
    assert F1Decision().noise_envelope(S) == pytest.approx(7.5)
    assert np.percentile([1, 1, 2, 2, 3, 4], 95) == pytest.approx(3.75)


def test_noise_envelope_matches_bruteforce_and_picks_max_cell():
    rng = np.random.default_rng(3)
    vals = {c: rng.uniform(0, 1, 8) * s for c, s in
            zip(["cf", "ci", "sf", "si"], [1.0, 0.5, 3.0, 0.2])}
    S = make_table(vals["cf"], vals["ci"], vals["sf"], vals["si"])
    best = max(np.percentile([abs(v[i] - v[j]) for i, j in itertools.combinations(range(8), 2)], 95)
               for v in vals.values())
    assert F1Decision().noise_envelope(S) == pytest.approx(best)


# ---------------------------------------------------------------- verdicts
def rep(D, u=0.1):
    return (np.asarray(D, dtype=float), u)


GOOD = [0.5] * 8


def reasons_text(v):
    return " | ".join(v.reasons)


# N03
def test_verdict_supported():
    v = F1Decision().verdict([rep(GOOD), rep([0.4] * 8), rep([0.9] * 8)], [True] * 3)
    assert v.status == "SUPPORTED"


# N04
def test_verdict_rejected_when_six_of_eight_positive():
    bad = [0.5] * 6 + [-0.1, -0.2]
    v = F1Decision().verdict([rep(GOOD), rep(bad), rep(GOOD)], [True] * 3)
    assert v.status == "REJECTED"


def test_verdict_rejected_when_median_below_envelope():
    v = F1Decision().verdict([rep(GOOD), rep(GOOD, u=0.6), rep(GOOD)], [True] * 3)
    assert v.status == "REJECTED"


# N05
def test_verdict_inconclusive_on_learning_gate():
    v = F1Decision().verdict([rep(GOOD)] * 3, [True, False, True])
    assert v.status == "INCONCLUSIVE"
    assert "learning_gate" in reasons_text(v)


def test_learning_gate_failure_beats_a_rejecting_replicate():
    v = F1Decision().verdict([rep(GOOD), rep([-0.5] * 8), rep(GOOD)], [True, False, True])
    assert v.status == "INCONCLUSIVE"


def test_verdict_inconclusive_on_input_status():
    v = F1Decision().verdict([rep(GOOD)] * 3, [True] * 3, input_statuses=("ok", "censored", "ok"))
    assert v.status == "INCONCLUSIVE"
    assert "status" in reasons_text(v)


def test_verdict_all_ok_statuses_do_not_block():
    v = F1Decision().verdict([rep(GOOD)] * 3, [True] * 3, input_statuses=("ok", "ok"))
    assert v.status == "SUPPORTED"


def test_verdict_inconclusive_with_fewer_than_three_replicates():
    v = F1Decision().verdict([rep(GOOD), rep(GOOD)], [True, True])
    assert v.status == "INCONCLUSIVE"
    assert "replicates" in reasons_text(v)


def test_learning_gate_reason_present_even_with_few_replicates():
    v = F1Decision().verdict([rep(GOOD)], [False])
    assert v.status == "INCONCLUSIVE"
    assert "learning_gate" in reasons_text(v)


# N06
def test_exactly_seven_of_eight_positive_passes():
    v = F1Decision().verdict([rep([0.5] * 7 + [-0.3])] * 3, [True] * 3)
    assert v.status == "SUPPORTED"


def test_zero_contrast_is_not_positive():
    assert F1Decision().verdict([rep([0.5] * 7 + [0.0])] * 3, [True] * 3).status == "SUPPORTED"
    assert F1Decision().verdict([rep([0.5] * 6 + [0.0, 0.0])] * 3, [True] * 3).status == "REJECTED"


def test_median_equal_to_envelope_fails_strictly():
    assert F1Decision().verdict([rep([0.25] * 8, u=0.25)] * 3, [True] * 3).status == "REJECTED"
    assert F1Decision().verdict([rep([0.25] * 8, u=0.125)] * 3, [True] * 3).status == "SUPPORTED"


def test_one_failing_replicate_among_three_is_enough_to_reject():
    for pos in range(3):
        reps = [rep(GOOD)] * 3
        reps[pos] = rep([0.5] * 6 + [-0.1] * 2)
        assert F1Decision().verdict(reps, [True] * 3).status == "REJECTED"
