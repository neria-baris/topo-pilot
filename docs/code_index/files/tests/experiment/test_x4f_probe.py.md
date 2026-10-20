# `tests/experiment/test_x4f_probe.py`

- Source: [tests/experiment/test_x4f_probe.py](../../../../../tests/experiment/test_x4f_probe.py)
- Kind: python
- Lines: 174

## Module docstring

> Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment.x4f_probe import GRID, NestedResult, nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 9, via package root)
- `from topo_pilot.prediction import RidgeProbe` -> [src/topo_pilot/prediction/__init__.py](../../src/topo_pilot/prediction/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 6)
- `pytest` (lines 7)

### Standard library

- none

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

- **function `_std`** [L17-20]: `def _std(X)`
- **function `_ridge_pred`** [L23-26]: `def _ridge_pred(X_fit, Y_fit, X_new, lam)`
- **function `_ref_fold_mse`** [L29-38]: `def _ref_fold_mse(X, Y, panel, grid)`
- **function `_ref_choice`** [L41-42]: `def _ref_choice(fold)`
- **function `_data`** [L45-56]: `def _data(seed=0, per_panel=30, panels=(2, 3, 5, 7, 11, 13), noise=1.0, n_val=60)`
- **test `test_grid_constant`** [L61-62]: `def test_grid_constant()`
- **test `test_selection_and_fold_mse_match_reference`** [L66-76]: `def test_selection_and_fold_mse_match_reference(seed, noise)` decorators: @pytest.mark.parametrize('seed,noise', [(0, 1.0), (1, 5.0), (2, 0.05)])
- **test `test_predictions_equal_ridgeprobe_on_calibration_standardised_data`** [L79-84]: `def test_predictions_equal_ridgeprobe_on_calibration_standardised_data()`
- **test `test_r2_uses_calibration_mean_and_pooled_sst`** [L87-96]: `def test_r2_uses_calibration_mean_and_pooled_sst()`
- **test `test_validation_isolation_nan_poison`** [L99-112]: `def test_validation_isolation_nan_poison()`
- **test `test_inputs_not_mutated`** [L115-120]: `def test_inputs_not_mutated()`
- **test `test_tie_rule_larger_lambda_wins`** [L123-137]: `def test_tie_rule_larger_lambda_wins()`
- **test `test_fold_mse_is_unweighted_mean_over_sorted_panels`** [L140-147]: `def test_fold_mse_is_unweighted_mean_over_sorted_panels()`
- **test `test_determinism`** [L150-156]: `def test_determinism()`
- **test `test_permuting_rows_within_calibration_does_not_change_result`** [L159-167]: `def test_permuting_rows_within_calibration_does_not_change_result()`
- **test `test_zero_variance_validation_target_status`** [L170-174]: `def test_zero_variance_validation_target_status()`

