# `tests/contracts/test_layout.py`

- Source: [tests/contracts/test_layout.py](../../../../../tests/contracts/test_layout.py)
- Kind: python
- Lines: 65

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)

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

- `ROW`

## Classes and functions

- **test `test_C11_inputs_targets_history_known_answer`** [L13-32]: `def test_C11_inputs_targets_history_known_answer()`
- **test `test_C11_history`** [L35-41]: `def test_C11_history()`
- **test `test_C11_targets_is_a_copy`** [L44-48]: `def test_C11_targets_is_a_copy()`
- **test `test_C11_alignment_errors`** [L62-65]: `def test_C11_alignment_errors(call)` decorators: @pytest.mark.parametrize('call', [lambda L: L.model_inputs(np.zeros((2, 32), dtype=np.uint8), 5), lambda L: L.model_inputs(np.zeros((33,), dtype=np.uint8), 5), lambda L: L.model_inputs(np.zeros((2, 33), dtype=np.float64), 5), lambda L: L.targets(np.zeros((2, 34), dtype=np.int64)), lambda L: L.targets(np.zeros((33,), dtype=np.int64)), lambda L: L.history(np.zeros(32, dtype=np.int64), 3), lambda L: L.history(np.zeros((2, 33), dtype=np.int64), 3), lambda L: L.history(np.zeros(33, dtype=np.int64), 33), lambda L: L.history(np.zeros(33, dtype=np.int64), -1)])

