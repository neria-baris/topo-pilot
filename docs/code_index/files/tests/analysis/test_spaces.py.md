# `tests/analysis/test_spaces.py`

- Source: [tests/analysis/test_spaces.py](../../../../../tests/analysis/test_spaces.py)
- Kind: python
- Lines: 37

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import PointSet, require_same_ids` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 4, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 5, via package root)

### External (third-party)

- `numpy` (lines 1)
- `pytest` (lines 2)

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

- **function `ps`** [L10-12]: `def ps(space, ids)`
- **test `test_equal_ids_pass_silently`** [L15-16]: `def test_equal_ids_pass_silently()`
- **test `test_mismatched_ids_raise`** [L28-31]: `def test_mismatched_ids_raise(other)` decorators: @pytest.mark.parametrize('other', [['a', 'c', 'b'], ['a', 'b', 'd'], ['a', 'b'], ['a', 'b', 'c', 'd']])
- **test `test_mismatch_symmetric`** [L34-37]: `def test_mismatch_symmetric()`

