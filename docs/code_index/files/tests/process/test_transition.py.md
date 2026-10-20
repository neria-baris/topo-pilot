# `tests/process/test_transition.py`

- Source: [tests/process/test_transition.py](../../../../../tests/process/test_transition.py)
- Kind: python
- Lines: 105

## Module docstring

> P01-P03 and error paths of the transition builder.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 11, via package root)
- `from topo_pilot.process import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 12, via package root)
- `from topo_pilot.process.transition import check_support` -> [src/topo_pilot/process/transition.py](../../src/topo_pilot/process/transition.py.md) (line 13, via package root)

### External (third-party)

- `numpy` (lines 8)
- `pytest` (lines 9)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)
- `inspect` (lines 6)

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

- **function `_build`** [L18-19]: `def _build(world, p_stay=0.2)`
- **test `test_P01_square_n3_hand_values`** [L22-34]: `def test_P01_square_n3_hand_values(square3)`
- **test `test_P02_cylinder_n3_no_corners_and_wrap`** [L37-50]: `def test_P02_cylinder_n3_no_corners_and_wrap(cylinder3)`
- **test `test_P03_contract_invariants`** [L54-68]: `def test_P03_contract_invariants(family, square12, cylinder12)` decorators: @pytest.mark.parametrize('family', ['square', 'cylinder'])
- **test `test_p_stay_changes_values_only_by_formula`** [L71-74]: `def test_p_stay_changes_values_only_by_formula(square3)`
- **test `test_error_illegal_support`** [L77-84]: `def test_error_illegal_support(square3)`
- **test `test_error_bad_p_stay_and_kind`** [L87-92]: `def test_error_bad_p_stay_and_kind(square3)`
- **test `test_error_state_order_mismatch`** [L95-99]: `def test_error_state_order_mismatch(square3)`
- **test `test_P11_transition_builder_does_not_accept_emission`** [L102-105]: `def test_P11_transition_builder_does_not_accept_emission()`

