# `tests/prediction/test_ridge.py`

- Source: [tests/prediction/test_ridge.py](../../../../../tests/prediction/test_ridge.py)
- Kind: python
- Lines: 50

## Module docstring

> R09, R10: ridge probe.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.prediction import RidgeProbe` -> [src/topo_pilot/prediction/__init__.py](../../src/topo_pilot/prediction/__init__.py.md) (line 7, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)

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

- **function `planted`** [L12-17]: `def planted(seed=0, n=300)`
- **test `test_R09_recovers_planted_affine_map`** [L20-26]: `def test_R09_recovers_planted_affine_map()`
- **test `test_R09_shuffled_labels_give_near_zero_r2`** [L29-33]: `def test_R09_shuffled_labels_give_near_zero_r2()`
- **test `test_ridge_intercept_unpenalised_and_lambda_chosen_on_val`** [L36-42]: `def test_ridge_intercept_unpenalised_and_lambda_chosen_on_val()`
- **test `test_R10_probe_fit_touching_test_raises_leakage`** [L45-50]: `def test_R10_probe_fit_touching_test_raises_leakage()`

