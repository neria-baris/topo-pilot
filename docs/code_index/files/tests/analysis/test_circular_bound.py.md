# `tests/analysis/test_circular_bound.py`

- Source: [tests/analysis/test_circular_bound.py](../../../../../tests/analysis/test_circular_bound.py)
- Kind: python
- Lines: 48

## Module docstring

> circ-audit-v1: symbol-only optimistic bound A*_symbol (known answers and properties).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import circular_agreement, symbol_only_bound` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 5, via package root)
- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)

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

- **test `test_bound_is_one_when_symbol_determines_angle`** [L11-14]: `def test_bound_is_one_when_symbol_determines_angle()`
- **test `test_bound_hand_value_and_opposite_angles`** [L17-20]: `def test_bound_hand_value_and_opposite_angles()`
- **test `test_bound_dominates_every_symbol_function_and_is_attained`** [L23-33]: `def test_bound_dominates_every_symbol_function_and_is_attained()`
- **test `test_bound_invariant_to_rotation_and_relabelling`** [L36-41]: `def test_bound_invariant_to_rotation_and_relabelling()`
- **test `test_bound_error_paths`** [L44-48]: `def test_bound_error_paths()`

