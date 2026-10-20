# `tests/analysis/test_x5_endpoint.py`

- Source: [tests/analysis/test_x5_endpoint.py](../../../../../tests/analysis/test_x5_endpoint.py)
- Kind: python
- Lines: 363

## Module docstring

> Independent contract tests for ``topo_pilot.analysis.x5_endpoint`` (part 1 of 2).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis.x5_endpoint import DELAY, GRID, THRESHOLD, DiffBounds, GridEvent, dev_auc, difference_bounds, grid_event, pass_sequence, quantile_inverted_cdf, ratio_curve` -> [src/topo_pilot/analysis/x5_endpoint.py](../../src/topo_pilot/analysis/x5_endpoint.py.md) (line 21, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 34, via package root)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 13)
- `dataclasses` (lines 15)
- `math` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `EXPECTED_GRID`

## Classes and functions

- **function `_passes`** [L41-43]: `def _passes(pass_steps, grid=EXPECTED_GRID) -> list[bool]`
- **function `_from`** [L46-47]: `def _from(start: int, grid=EXPECTED_GRID) -> list[int]`
- **function `_assert_observed`** [L50-54]: `def _assert_observed(ev: GridEvent, t: int) -> None`
- **function `_assert_censored`** [L57-62]: `def _assert_censored(ev: GridEvent, lower: float, trailing: tuple[int, ...]) -> None`
- **test `test_constants`** [L68-71]: `def test_constants() -> None`
- **test `test_pass_sequence_threshold_equality_passes`** [L77-80]: `def test_pass_sequence_threshold_equality_passes() -> None`
- **test `test_pass_sequence_custom_threshold`** [L83-84]: `def test_pass_sequence_custom_threshold() -> None`
- **test `test_pass_sequence_rejects_nan`** [L87-89]: `def test_pass_sequence_rejects_nan() -> None`
- **test `test_hand_example_non_monotone_2500`** [L95-97]: `def test_hand_example_non_monotone_2500() -> None`
- **test `test_hand_example_1000_then_fail`** [L100-103]: `def test_hand_example_1000_then_fail() -> None`
- **test `test_hand_example_tau_zero`** [L106-108]: `def test_hand_example_tau_zero() -> None`
- **test `test_non_monotone_runs_of_two_do_not_qualify`** [L111-113]: `def test_non_monotone_runs_of_two_do_not_qualify() -> None`
- **test `test_hand_example_4500_edge_observed`** [L116-118]: `def test_hand_example_4500_edge_observed() -> None`
- **test `test_hand_example_first_pass_4750_censored`** [L121-123]: `def test_hand_example_first_pass_4750_censored() -> None`
- **test `test_pass_only_at_5000_censored`** [L126-127]: `def test_pass_only_at_5000_censored() -> None`
- **test `test_pass_at_4750_only_censored`** [L130-131]: `def test_pass_at_4750_only_censored() -> None`
- **test `test_never_pass_censored`** [L134-135]: `def test_never_pass_censored() -> None`
- **test `test_grid_event_accepts_numpy_bool_array`** [L138-140]: `def test_grid_event_accepts_numpy_bool_array() -> None`
- **test `test_grid_event_default_grid_is_GRID`** [L143-145]: `def test_grid_event_default_grid_is_GRID() -> None`
- **test `test_grid_event_small_custom_grids`** [L148-157]: `def test_grid_event_small_custom_grids() -> None`
- **test `test_grid_event_is_frozen`** [L160-163]: `def test_grid_event_is_frozen() -> None`
- **test `test_grid_event_length_mismatch`** [L171-173]: `def test_grid_event_length_mismatch(passes) -> None` decorators: @pytest.mark.parametrize('passes', [[True] * 26, [True] * 28, []])
- **test `test_grid_event_rejects_non_bool`** [L177-181]: `def test_grid_event_rejects_non_bool(bad) -> None` decorators: @pytest.mark.parametrize('bad', [None, 1, 0, 1.0, 'True', np.int64(1), np.float64(0.0)])
- **test `test_grid_event_rejects_none_incomplete_curve`** [L184-187]: `def test_grid_event_rejects_none_incomplete_curve() -> None`
- **test `test_grid_event_short_grid`** [L191-193]: `def test_grid_event_short_grid(grid) -> None` decorators: @pytest.mark.parametrize('grid', [(0, 100), (0,), ()])
- **test `test_grid_event_non_increasing_grid`** [L197-199]: `def test_grid_event_non_increasing_grid(grid) -> None` decorators: @pytest.mark.parametrize('grid', [(0, 100, 100, 200), (0, 200, 100, 300), (300, 200, 100)])
- **function `_obs`** [L205-206]: `def _obs(t: int) -> GridEvent`
- **function `_cens`** [L209-210]: `def _cens(trailing=()) -> GridEvent`
- **function `_no_nan`** [L213-214]: `def _no_nan(b: DiffBounds) -> None`
- **test `test_bounds_both_observed`** [L217-222]: `def test_bounds_both_observed() -> None`
- **test `test_bounds_d_low_equality_250`** [L225-228]: `def test_bounds_d_low_equality_250() -> None`
- **test `test_bounds_curved_censored_flat_observed`** [L231-235]: `def test_bounds_curved_censored_flat_observed() -> None`
- **test `test_bounds_flat_censored_curved_observed`** [L238-242]: `def test_bounds_flat_censored_curved_observed() -> None`
- **test `test_bounds_both_censored`** [L245-249]: `def test_bounds_both_censored() -> None`
- **test `test_bounds_custom_grid_censoring`** [L252-257]: `def test_bounds_custom_grid_censoring() -> None`
- **test `test_ratio_curve_values`** [L263-267]: `def test_ratio_curve_values() -> None`
- **test `test_ratio_curve_bad_gc`** [L271-273]: `def test_ratio_curve_bad_gc(gc) -> None` decorators: @pytest.mark.parametrize('gc', [0.0, -1.0, math.nan, math.inf, -math.inf])
- **test `test_ratio_curve_empty_rows`** [L276-278]: `def test_ratio_curve_empty_rows() -> None`
- **function `_ref_q`** [L284-287]: `def _ref_q(values, q) -> float`
- **test `test_quantile_matches_numpy_on_random_finite`** [L290-306]: `def test_quantile_matches_numpy_on_random_finite() -> None`
- **test `test_quantile_2000_draws_order_statistics`** [L309-312]: `def test_quantile_2000_draws_order_statistics() -> None`
- **test `test_quantile_with_infinities`** [L315-328]: `def test_quantile_with_infinities() -> None`
- **test `test_quantile_returns_float_and_accepts_list`** [L331-333]: `def test_quantile_returns_float_and_accepts_list() -> None`
- **test `test_quantile_errors`** [L343-345]: `def test_quantile_errors(values, q) -> None` decorators: @pytest.mark.parametrize('values,q', [([], 0.5), (np.array([]), 0.0), ([1.0, math.nan], 0.5), ([1.0, 2.0], -0.01), ([1.0, 2.0], 1.01)])
- **test `test_dev_auc_uneven_grid`** [L351-354]: `def test_dev_auc_uneven_grid() -> None`
- **test `test_dev_auc_on_study_grid`** [L357-363]: `def test_dev_auc_on_study_grid() -> None`

