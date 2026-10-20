# `tests/prediction/test_metrics.py`

- Source: [tests/prediction/test_metrics.py](../../../../../tests/prediction/test_metrics.py)
- Kind: python
- Lines: 104

## Module docstring

> R01, R02, R06, R07, R08: predictive metrics, learning gate, bootstrap, join.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, Status` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.prediction import LearningGate, PredictiveMetrics, join_by_history_id` -> [src/topo_pilot/prediction/__init__.py](../../src/topo_pilot/prediction/__init__.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 5)
- `pytest` (lines 6)

### Standard library

- `math` (lines 3)

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

- **test `test_R01_kl_zero_hand_value_and_nonnegative`** [L14-23]: `def test_R01_kl_zero_hand_value_and_nonnegative()`
- **test `test_R01_kl_zero_log_zero_convention_and_regret_mean`** [L26-30]: `def test_R01_kl_zero_log_zero_convention_and_regret_mean()`
- **test `test_R01_kl_error_paths`** [L33-42]: `def test_R01_kl_error_paths()`
- **test `test_R02_nll_uniform_is_log_v`** [L45-48]: `def test_R02_nll_uniform_is_log_v()`
- **test `test_R02_nll_picks_target_column`** [L51-54]: `def test_R02_nll_picks_target_column()`
- **test `test_R06_captured_and_gate_hand_values`** [L57-66]: `def test_R06_captured_and_gate_hand_values()`
- **test `test_R06_zero_context_gain_is_inconclusive`** [L69-74]: `def test_R06_zero_context_gain_is_inconclusive()`
- **test `test_R07_bootstrap_resamples_groups_not_rows`** [L77-84]: `def test_R07_bootstrap_resamples_groups_not_rows()`
- **test `test_R07_constant_array_has_degenerate_ci`** [L87-90]: `def test_R07_constant_array_has_degenerate_ci()`
- **test `test_R08_join_returns_alignment_permutation`** [L93-97]: `def test_R08_join_returns_alignment_permutation()`
- **test `test_R08_join_mismatch_raises`** [L101-104]: `def test_R08_join_mismatch_raises(ids_b)` decorators: @pytest.mark.parametrize('ids_b', [['x', 'y'], ['x', 'y', 'w'], ['x', 'y', 'y']])

