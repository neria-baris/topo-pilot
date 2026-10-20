# `tests/analysis/test_x5_context.py`

- Source: [tests/analysis/test_x5_context.py](../../../../../tests/analysis/test_x5_context.py)
- Kind: python
- Lines: 157

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import GC_THRESHOLD, context_status, percentile_interval, x5_overall_verdict` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 16, via package root)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 9)
- `math` (lines 11)

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

- none

## Classes and functions

- **function `_arm`** [L26-27]: `def _arm(op='ok', context='PASS')`
- **function `_verdict`** [L30-31]: `def _verdict(a0, a020, failed=(), inconclusive=())`
- **test `test_threshold_constant`** [L37-38]: `def test_threshold_constant()`
- **test `test_percentile_interval_matches_numpy_linear`** [L41-47]: `def test_percentile_interval_matches_numpy_linear()`
- **test `test_percentile_interval_hand_value`** [L50-56]: `def test_percentile_interval_hand_value()`
- **test `test_lower_exactly_threshold_passes`** [L62-64]: `def test_lower_exactly_threshold_passes()`
- **test `test_upper_exactly_threshold_is_near`** [L67-69]: `def test_upper_exactly_threshold_is_near()`
- **test `test_upper_below_threshold_fails`** [L72-76]: `def test_upper_below_threshold_fails()`
- **test `test_non_finite_is_invalid`** [L81-82]: `def test_non_finite_is_invalid(lo, hi)` decorators: @pytest.mark.parametrize('lo,hi', [(math.nan, 0.05), (0.04, math.inf), (-math.inf, 0.0), (math.nan, math.nan)])
- **test `test_invalid_flag_beats_values`** [L85-87]: `def test_invalid_flag_beats_values()`
- **test `test_all_pass_feasible`** [L93-95]: `def test_all_pass_feasible()`
- **test `test_global_failed_beats_everything`** [L98-103]: `def test_global_failed_beats_everything()`
- **test `test_arm_op_failed_gives_failed`** [L106-111]: `def test_arm_op_failed_gives_failed()`
- **test `test_invalid_kernel_plus_weak_arm_is_inconclusive`** [L114-119]: `def test_invalid_kernel_plus_weak_arm_is_inconclusive()`
- **test `test_near_unit_gap_is_inconclusive`** [L122-123]: `def test_near_unit_gap_is_inconclusive()`
- **test `test_near_threshold_plus_fail_is_inconclusive`** [L126-128]: `def test_near_threshold_plus_fail_is_inconclusive()`
- **test `test_invalid_predictive_is_inconclusive`** [L131-132]: `def test_invalid_predictive_is_inconclusive()`
- **test `test_context_none_is_inconclusive`** [L135-137]: `def test_context_none_is_inconclusive()`
- **test `test_global_inconclusive`** [L140-143]: `def test_global_inconclusive()`
- **test `test_one_fail_other_pass_is_weak_context`** [L146-150]: `def test_one_fail_other_pass_is_weak_context()`
- **test `test_verdict_is_pure`** [L153-157]: `def test_verdict_is_pure()`

