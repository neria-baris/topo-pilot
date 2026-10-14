"""Independent contract tests for ``topo_pilot.analysis.x5_endpoint`` (part 1 of 2).

Written by an independent test writer from the API contract only
(docs/proposals/X5_G1_TRAINING_API.md §1 and §8 "Endpoint"; protocol x5g1-train-v3 §4-§7),
without reading the implementation.

Covers: constants, ``pass_sequence``, ``grid_event`` (protocol hand examples on the real
27-point grid, censoring at grid[-3] strict, trailing PASS), ``difference_bounds`` (all four
censoring combinations, never NaN), ``ratio_curve``, ``quantile_inverted_cdf`` and ``dev_auc``.
The bootstrap, pair flags and cohort verdict are in ``test_x5_endpoint_bootstrap.py``.
"""

from __future__ import annotations

import dataclasses
import math

import numpy as np
import pytest

from topo_pilot.analysis.x5_endpoint import (
    DELAY,
    GRID,
    THRESHOLD,
    DiffBounds,
    GridEvent,
    dev_auc,
    difference_bounds,
    grid_event,
    pass_sequence,
    quantile_inverted_cdf,
    ratio_curve,
)
from topo_pilot.contracts import SeedTree

pytestmark = pytest.mark.analysis

EXPECTED_GRID = tuple(range(0, 1001, 100)) + tuple(range(1250, 5001, 250))


def _passes(pass_steps, grid=EXPECTED_GRID) -> list[bool]:
    steps = set(pass_steps)
    return [t in steps for t in grid]


def _from(start: int, grid=EXPECTED_GRID) -> list[int]:
    return [t for t in grid if t >= start]


def _assert_observed(ev: GridEvent, t: int) -> None:
    assert ev.tau == t and isinstance(ev.tau, int)
    assert ev.lower == t and ev.upper == t
    assert not ev.censored and not ev.lower_strict
    assert ev.trailing_pass == ()


def _assert_censored(ev: GridEvent, lower: float, trailing: tuple[int, ...]) -> None:
    assert ev.tau is None
    assert ev.lower == lower and math.isfinite(ev.lower)
    assert math.isinf(ev.upper) and ev.upper > 0
    assert ev.censored and ev.lower_strict
    assert tuple(ev.trailing_pass) == trailing


# --------------------------------------------------------------------------- constants


def test_constants() -> None:
    assert tuple(GRID) == EXPECTED_GRID
    assert len(GRID) == 27 and GRID[-3] == 4500 and GRID[0] == 0 and GRID[-1] == 5000
    assert THRESHOLD == 0.05 and DELAY == 250


# ----------------------------------------------------------------------- pass_sequence


def test_pass_sequence_threshold_equality_passes() -> None:
    out = pass_sequence(np.array([0.0, 0.05, 0.0500001, 0.2, np.inf]))
    assert isinstance(out, np.ndarray) and out.dtype == np.bool_
    assert out.tolist() == [True, True, False, False, False]


def test_pass_sequence_custom_threshold() -> None:
    assert pass_sequence(np.array([0.1, 0.11]), threshold=0.1).tolist() == [True, False]


def test_pass_sequence_rejects_nan() -> None:
    with pytest.raises(ValueError):
        pass_sequence(np.array([0.01, np.nan, 0.01]))


# -------------------------------------------------------------------------- grid_event


def test_hand_example_non_monotone_2500() -> None:
    ev = grid_event(_passes([2000] + _from(2500)))
    _assert_observed(ev, 2500)


def test_hand_example_1000_then_fail() -> None:
    _assert_observed(grid_event(_passes([1000, 1250, 1500])), 1000)
    # Later PASSes do not move the first qualifying event.
    _assert_observed(grid_event(_passes([1000, 1250, 1500] + _from(2000))), 1000)


def test_hand_example_tau_zero() -> None:
    _assert_observed(grid_event(_passes([0, 100, 200])), 0)
    _assert_observed(grid_event(_passes(EXPECTED_GRID)), 0)


def test_non_monotone_runs_of_two_do_not_qualify() -> None:
    pattern = [100, 200, 400, 500, 700, 800, 900]
    _assert_observed(grid_event(_passes(pattern)), 700)


def test_hand_example_4500_edge_observed() -> None:
    ev = grid_event(_passes([4500, 4750, 5000]))
    _assert_observed(ev, 4500)  # observed: trailing_pass stays empty


def test_hand_example_first_pass_4750_censored() -> None:
    ev = grid_event(_passes([4750, 5000]))
    _assert_censored(ev, 4500.0, (4750, 5000))


def test_pass_only_at_5000_censored() -> None:
    _assert_censored(grid_event(_passes([5000])), 4500.0, (5000,))


def test_pass_at_4750_only_censored() -> None:
    _assert_censored(grid_event(_passes([4500, 4750])), 4500.0, (4750,))


def test_never_pass_censored() -> None:
    _assert_censored(grid_event(_passes([])), 4500.0, ())


def test_grid_event_accepts_numpy_bool_array() -> None:
    passes = pass_sequence(np.where(np.array(EXPECTED_GRID) >= 3000, 0.01, 0.5))
    _assert_observed(grid_event(passes), 3000)


def test_grid_event_default_grid_is_GRID() -> None:
    p = _passes(_from(1250))
    assert grid_event(p) == grid_event(p, grid=GRID)


def test_grid_event_small_custom_grids() -> None:
    g3 = (0, 5, 9)
    _assert_observed(grid_event([True, True, True], grid=g3), 0)
    _assert_censored(grid_event([False, True, True], grid=g3), 0.0, (5, 9))
    g5 = (10, 20, 40, 80, 160)
    _assert_observed(grid_event([False, False, True, True, True], grid=g5), 40)
    _assert_observed(grid_event([True, False, True, True, True], grid=g5), 40)
    _assert_censored(grid_event([True, True, False, True, True], grid=g5), 40.0, (80, 160))
    _assert_observed(grid_event([True, True, True, False, False], grid=g5), 10)
    _assert_censored(grid_event([False, True, False, False, True], grid=g5), 40.0, (160,))


def test_grid_event_is_frozen() -> None:
    ev = grid_event(_passes([]))
    with pytest.raises(dataclasses.FrozenInstanceError):
        ev.tau = 0  # type: ignore[misc]


@pytest.mark.parametrize("passes", [
    [True] * 26,
    [True] * 28,
    [],
])
def test_grid_event_length_mismatch(passes) -> None:
    with pytest.raises(ValueError):
        grid_event(passes)


@pytest.mark.parametrize("bad", [None, 1, 0, 1.0, "True", np.int64(1), np.float64(0.0)])
def test_grid_event_rejects_non_bool(bad) -> None:
    passes: list = _passes([0, 100, 200])
    passes[5] = bad
    with pytest.raises(ValueError):
        grid_event(passes)


def test_grid_event_rejects_none_incomplete_curve() -> None:
    passes: list = [True, True, True, None, False]
    with pytest.raises(ValueError):
        grid_event(passes, grid=(0, 1, 2, 3, 4))


@pytest.mark.parametrize("grid", [(0, 100), (0,), ()])
def test_grid_event_short_grid(grid) -> None:
    with pytest.raises(ValueError):
        grid_event([True] * len(grid), grid=grid)


@pytest.mark.parametrize("grid", [(0, 100, 100, 200), (0, 200, 100, 300), (300, 200, 100)])
def test_grid_event_non_increasing_grid(grid) -> None:
    with pytest.raises(ValueError):
        grid_event([True] * len(grid), grid=grid)


# ------------------------------------------------------------------- difference_bounds


def _obs(t: int) -> GridEvent:
    return grid_event(_passes([t, t + 250, t + 500] if t >= 1000 else [t, t + 100, t + 200]))


def _cens(trailing=()) -> GridEvent:
    return grid_event(_passes(trailing))


def _no_nan(b: DiffBounds) -> None:
    assert not math.isnan(b.low) and not math.isnan(b.high)


def test_bounds_both_observed() -> None:
    b = difference_bounds(_obs(3000), _obs(2750))
    assert (b.low, b.high, b.low_strict, b.high_strict) == (250, 250, False, False)
    b = difference_bounds(_obs(1000), _obs(2000))
    assert (b.low, b.high) == (-1000, -1000)
    _no_nan(b)


def test_bounds_d_low_equality_250() -> None:
    b = difference_bounds(_obs(1250), _obs(1000))
    assert b.low == 250 == DELAY and b.high == 250
    assert b.low >= DELAY


def test_bounds_curved_censored_flat_observed() -> None:
    b = difference_bounds(_cens(), _obs(1000))
    assert b.low == 3500 and math.isinf(b.high) and b.high > 0
    assert b.low_strict and not b.high_strict
    _no_nan(b)


def test_bounds_flat_censored_curved_observed() -> None:
    b = difference_bounds(_obs(2000), _cens((5000,)))
    assert math.isinf(b.low) and b.low < 0 and b.high == 2000 - 4500
    assert not b.low_strict and b.high_strict
    _no_nan(b)


def test_bounds_both_censored() -> None:
    b = difference_bounds(_cens((4750, 5000)), _cens())
    assert b.low == -math.inf and b.high == math.inf
    assert not b.low_strict and not b.high_strict
    _no_nan(b)


def test_bounds_custom_grid_censoring() -> None:
    g5 = (0, 10, 20, 30, 40)
    cens = grid_event([False] * 5, grid=g5)
    obs = grid_event([False, True, True, True, False], grid=g5)
    b = difference_bounds(cens, obs)
    assert b.low == 20 - 10 and b.high == math.inf and b.low_strict


# ------------------------------------------------------------------------- ratio_curve


def test_ratio_curve_values() -> None:
    reg = np.array([[1.0, 2.0, 0.0], [3.0, 4.0, 0.5]])
    out = ratio_curve(reg, 2.0)
    np.testing.assert_allclose(out, [1.0, 1.5, 0.125], rtol=0, atol=1e-15)
    np.testing.assert_allclose(ratio_curve(reg[:1], 0.5), [2.0, 4.0, 0.0], rtol=0, atol=0)


@pytest.mark.parametrize("gc", [0.0, -1.0, math.nan, math.inf, -math.inf])
def test_ratio_curve_bad_gc(gc) -> None:
    with pytest.raises(ValueError):
        ratio_curve(np.ones((2, 3)), gc)


def test_ratio_curve_empty_rows() -> None:
    with pytest.raises(ValueError):
        ratio_curve(np.ones((0, 3)), 1.0)


# --------------------------------------------------------------- quantile_inverted_cdf


def _ref_q(values, q) -> float:
    s = sorted(float(v) for v in values)
    k = max(1, math.ceil(q * len(s) - 1e-9))
    return s[k - 1]


def test_quantile_matches_numpy_on_random_finite() -> None:
    gen = SeedTree(11).generator("t", "quantile")
    qs = [0.0, 0.025, 0.1, 0.5, 0.9, 0.975, 1.0]
    checked = 0
    for n in list(range(1, 41)) + [199, 500, 2000]:
        vals = gen.normal(size=n) * 1000
        if n % 3 == 0:
            vals = np.round(vals / 250) * 250  # ties
        for q in qs + list(gen.uniform(0, 1, size=5)):
            frac = abs(q * n - round(q * n))
            if 0 < frac < 1e-6:
                continue  # float-rounding edge where the 1e-9 tolerance may differ
            got = quantile_inverted_cdf(vals, q)
            want = float(np.quantile(vals, q, method="inverted_cdf"))
            assert got == want == _ref_q(vals, q), (n, q)
            checked += 1
    assert checked > 300


def test_quantile_2000_draws_order_statistics() -> None:
    vals = np.arange(2000, 0, -1, dtype=float)  # 1..2000 reversed
    assert quantile_inverted_cdf(vals, 0.025) == 50.0
    assert quantile_inverted_cdf(vals, 0.975) == 1950.0


def test_quantile_with_infinities() -> None:
    vals = np.array([np.inf, -np.inf, 1.0, 2.0, 3.0])
    assert quantile_inverted_cdf(vals, 0.0) == -math.inf
    assert quantile_inverted_cdf(vals, 0.2) == -math.inf
    assert quantile_inverted_cdf(vals, 0.21) == 1.0
    assert quantile_inverted_cdf(vals, 0.5) == 2.0
    assert quantile_inverted_cdf(vals, 0.8) == 3.0
    assert quantile_inverted_cdf(vals, 0.81) == math.inf
    assert quantile_inverted_cdf(vals, 1.0) == math.inf
    assert quantile_inverted_cdf([math.inf] * 4, 0.025) == math.inf
    assert quantile_inverted_cdf([-math.inf] * 4, 0.975) == -math.inf
    many = np.concatenate([np.full(60, -np.inf), np.arange(1940.0)])
    assert quantile_inverted_cdf(many, 0.025) == -math.inf
    assert quantile_inverted_cdf(many, 0.975) == 1889.0


def test_quantile_returns_float_and_accepts_list() -> None:
    out = quantile_inverted_cdf([3, 1, 2], 0.5)
    assert isinstance(out, float) and out == 2.0


@pytest.mark.parametrize("values,q", [
    ([], 0.5),
    (np.array([]), 0.0),
    ([1.0, math.nan], 0.5),
    ([1.0, 2.0], -0.01),
    ([1.0, 2.0], 1.01),
])
def test_quantile_errors(values, q) -> None:
    with pytest.raises(ValueError):
        quantile_inverted_cdf(values, q)


# ----------------------------------------------------------------------------- dev_auc


def test_dev_auc_uneven_grid() -> None:
    assert dev_auc(np.array([1.0, 0.5, 0.0]), grid=(0, 100, 300)) == pytest.approx(125.0)
    # Index spacing would give 1.0: the actual steps must be used.
    assert dev_auc(np.array([0.0, 1.0, 1.0]), grid=(0, 10, 1000)) == pytest.approx(995.0)


def test_dev_auc_on_study_grid() -> None:
    g = np.array(EXPECTED_GRID, dtype=float)
    assert dev_auc(np.ones(27)) == pytest.approx(5000.0)
    assert dev_auc(g) == pytest.approx(5000.0 ** 2 / 2)
    ratios = SeedTree(3).generator("t", "auc").uniform(0, 1, size=27)
    want = float(np.sum(np.diff(g) * (ratios[1:] + ratios[:-1]) / 2))
    assert dev_auc(ratios) == pytest.approx(want, rel=1e-12)
