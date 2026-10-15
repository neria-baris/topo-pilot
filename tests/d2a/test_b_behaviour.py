"""Independent tests (author B, job 0028): behavioural pair scores (``d2a_eval.pair_scores``) and
the label-shuffle stream (``d2a_eval.shuffle_perm``).

Written from D2A-FROZEN-v1 (§2.5 probe streams, §7.4 shuffle, §9.3 pair scores) and
tools/d2a/API.md (§2.4) only; no tools/d2a source was read. All probabilities are dyadic, so the
boundary cases E_contrast = 0.5, tv_pred = 0.5*Delta and tv_pred = 1.5*Delta are exact in float64.
The result is read as a mapping with the API names Delta, E_contrast, tv_pred, reproduced and
abs_resolved.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import SeedTree

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/d2a", "tools/d1_seam", "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import d2a_eval  # noqa: E402

DATA = 2026101531
E = 2.0 ** -10


def law(*head):
    """A 25-entry two-step law whose first entries are ``head`` (the rest zero)."""
    out = np.zeros(25)
    out[:len(head)] = head
    assert out.sum() == 1.0
    return out


J_A = law(0.5, 0.25, 0.25)   # d = J_A - J_B = (0.25, -0.25, 0, ...): Delta = 0.25
J_B = law(0.25, 0.5, 0.25)


def score(q_a, q_b, j_a=J_A, j_b=J_B):
    return d2a_eval.pair_scores(j_a, j_b, q_a, q_b)


def test_oracle_predictions_reproduce_and_resolve():
    s = score(J_A.copy(), J_B.copy())
    assert s["Delta"] == pytest.approx(0.25, abs=1e-15)
    assert s["E_contrast"] == pytest.approx(0.0, abs=1e-15)
    assert s["tv_pred"] == pytest.approx(0.25, abs=1e-15)
    assert bool(s["reproduced"]) and bool(s["abs_resolved"])


def test_contrast_error_exactly_one_half_is_reproduced():
    # dh = (0.25, -0.125, -0.125): 1/2 |dh - d|_1 = 0.125 = Delta / 2; tv_pred = Delta
    s = score(law(0.5, 0.375, 0.125), J_B.copy())
    assert s["E_contrast"] == 0.5 and s["tv_pred"] == 0.25
    assert bool(s["reproduced"])


def test_contrast_error_just_above_one_half_is_not_reproduced():
    # dh = (0.25 + e, -0.125, -0.125 - e): E_contrast = 0.5 + 4e > 0.5; tv_pred inside the band
    s = score(law(0.5 + E, 0.375, 0.125 - E), J_B.copy())
    assert s["E_contrast"] == pytest.approx(0.5 + 4 * E, abs=1e-15)
    assert 0.125 <= s["tv_pred"] <= 0.375
    assert not bool(s["reproduced"])


@pytest.mark.parametrize("q_a, tv, ok", [
    (law(0.375, 0.375, 0.25), 0.125, True),           # dh = 0.5 d: tv_pred = 0.5 Delta exactly
    (law(0.625, 0.125, 0.25), 0.375, True),           # dh = 1.5 d: tv_pred = 1.5 Delta exactly
    (law(0.375 - E, 0.375 + E, 0.25), 0.125 - E, False),  # just below 0.5 Delta
    (law(0.625 + E, 0.125 - E, 0.25), 0.375 + E, False),  # just above 1.5 Delta
])
def test_predicted_pair_tv_band_boundaries(q_a, tv, ok):
    s = score(q_a, J_B.copy())
    assert s["tv_pred"] == pytest.approx(tv, abs=1e-15)
    assert bool(s["reproduced"]) is ok


def test_zero_contrast_prediction_is_not_reproduced():
    s = score(J_B.copy(), J_B.copy())   # a pi-blind model predicts the same law for both
    assert s["E_contrast"] == pytest.approx(1.0, abs=1e-15) and s["tv_pred"] == 0.0
    assert not bool(s["reproduced"])


def test_reversed_contrast_is_not_reproduced():
    s = score(J_B.copy(), J_A.copy())
    assert s["tv_pred"] == pytest.approx(0.25) and s["E_contrast"] == pytest.approx(2.0)
    assert not bool(s["reproduced"])


@pytest.mark.parametrize("shift, resolved", [(0.0625, True), (0.125, False)])
def test_absolute_resolution_is_separate_and_strict(shift, resolved):
    # the same mass moved from entry 2 to entry 3 in both members: dh = d (reproduced), and each
    # member is off by TV = shift; resolution needs TV < Delta / 2 = 0.125 (strict)
    move = np.zeros(25)
    move[2], move[3] = -shift, shift
    s = score(J_A + move, J_B + move)
    assert s["E_contrast"] == pytest.approx(0.0, abs=1e-15) and bool(s["reproduced"])
    assert bool(s["abs_resolved"]) is resolved


@pytest.mark.parametrize("off_a", [True, False])
def test_absolute_resolution_needs_both_members(off_a):
    move = np.zeros(25)
    move[2], move[3] = -0.125, 0.125
    # one member exact, the other at TV = Delta / 2 exactly (not strictly below)
    s = score(J_A + move, J_B.copy()) if off_a else score(J_A.copy(), J_B + move)
    assert not bool(s["abs_resolved"])


def test_template_scale_pair():
    # the equal-gap template scale (pair TV 1/150) with an exact model: reproduced
    d = np.zeros(25)
    d[[3, 4]] = (1 / 150, -1 / 150)
    j_b = np.full(25, 1 / 25)
    j_a = j_b + d
    s = score(j_a.copy(), j_b.copy(), j_a, j_b)
    assert s["Delta"] == pytest.approx(1 / 150, rel=1e-12)
    assert bool(s["reproduced"]) and bool(s["abs_resolved"])


# ----------------------------------------------------------------------- shuffle_perm, §7.4

SCOPE = ("d2a-s1-H2", 28, "pi", "resid_post_3", "linear")


def test_shuffle_perm_is_the_registered_stream():
    expected = SeedTree(DATA).generator("d2a", "shuffle", *SCOPE).permutation(1000)
    np.testing.assert_array_equal(d2a_eval.shuffle_perm(1000, SCOPE), expected)


def test_shuffle_perm_is_deterministic_and_a_permutation():
    a = np.asarray(d2a_eval.shuffle_perm(4096, SCOPE))
    b = np.asarray(d2a_eval.shuffle_perm(4096, SCOPE))
    np.testing.assert_array_equal(a, b)
    np.testing.assert_array_equal(np.sort(a), np.arange(4096))
    assert not np.array_equal(a, np.arange(4096))


def test_shuffle_perm_depends_on_scope():
    a = np.asarray(d2a_eval.shuffle_perm(1000, SCOPE))
    for other in (("d2a-s2-H2",) + SCOPE[1:], SCOPE[:1] + (16,) + SCOPE[2:],
                  SCOPE[:2] + ("r8",) + SCOPE[3:]):
        assert not np.array_equal(a, np.asarray(d2a_eval.shuffle_perm(1000, other)))
