# `tests/contracts/test_schemas.py`

- Source: [tests/contracts/test_schemas.py](../../../../../tests/contracts/test_schemas.py)
- Kind: python
- Lines: 140

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)

### Standard library

- `dataclasses` (lines 1)

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

- **function `_fails`** [L12-15]: `def _fails(art, code)`
- **test `test_C13_transition_row_sum`** [L18-27]: `def test_C13_transition_row_sum(builders)`
- **test `test_C13_transition_asymmetric_and_stationarity`** [L30-36]: `def test_C13_transition_asymmetric_and_stationarity(builders)`
- **test `test_C13_emission_dead_symbol`** [L39-45]: `def test_C13_emission_dead_symbol(builders)`
- **test `test_C13_emission_other_violations`** [L48-56]: `def test_C13_emission_other_violations(builders)`
- **test `test_C13_history_index_overlapping_panels`** [L59-64]: `def test_C13_history_index_overlapping_panels(make_hist)`
- **test `test_C13_history_index_other_violations`** [L67-73]: `def test_C13_history_index_other_violations(make_hist)`
- **test `test_C13_world_spec`** [L76-88]: `def test_C13_world_spec(builders)`
- **test `test_C13_data_artifacts`** [L91-100]: `def test_C13_data_artifacts(builders)`
- **test `test_C13_misc_artifacts`** [L103-130]: `def test_C13_misc_artifacts(builders)`
- **test `test_C13_stagefailure_basics`** [L133-140]: `def test_C13_stagefailure_basics()`

