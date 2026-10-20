# `tests/c1prime/test_b_decoder.py`

- Source: [tests/c1prime/test_b_decoder.py](../../../../../tests/c1prime/test_b_decoder.py)
- Kind: python
- Lines: 77

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-3: RidgeProbe / nested_ridge equivalence.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis.x4f_scores import rbf_bandwidth, rbf_features, rbf_map, standardizer` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 21, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 22, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 23, via package root)
- `from topo_pilot.prediction.ridge import RidgeProbe` -> [src/topo_pilot/prediction/ridge.py](../../src/topo_pilot/prediction/ridge.py.md) (line 24, via package root)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 32, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 33, via sys.path edit)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 14)
- `pathlib` (lines 17)
- `sys` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 30: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `GRID`
- `REPO`

## Classes and functions

- **function `_reference`** [L41-54]: `def _reference(a_cal, Y, panel, a_new)`
- **test `test_decoder_refit_matches_nested_ridge_and_the_section7_recipe`** [L57-69]: `def test_decoder_refit_matches_nested_ridge_and_the_section7_recipe()`
- **test `test_degenerate_bandwidth_is_rbf_degenerate`** [L72-77]: `def test_degenerate_bandwidth_is_rbf_degenerate()`

