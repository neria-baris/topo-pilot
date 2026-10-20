# `tests/experiment/test_s6_rules.py`

- Source: [tests/experiment/test_s6_rules.py](../../../../../tests/experiment/test_s6_rules.py)
- Kind: python
- Lines: 40

## Module docstring

> S6 H4 rule (D-034): per-run classification and the verdict over the cylinder runs.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment.s6 import first_step, h4_class, h4_verdict` -> [src/topo_pilot/experiment/s6.py](../../src/topo_pilot/experiment/s6.py.md) (line 4, via package root)

### External (third-party)

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

- `STEPS`

## Classes and functions

- **test `test_first_step`** [L11-13]: `def test_first_step()`
- **test `test_h4_class`** [L23-24]: `def test_h4_class(t_h, t_s, cls)` decorators: @pytest.mark.parametrize('t_h, t_s, cls', [(100, 200, 'consistent'), (100, 100, 'consistent'), (200, 100, 'violated'), (100, None, 'no_rise'), (None, 100, 'no_history_use')])
- **test `test_h4_supported_needs_all_three_consistent`** [L27-30]: `def test_h4_supported_needs_all_three_consistent()`
- **test `test_h4_rejected_by_any_violation_with_gates_passed`** [L33-34]: `def test_h4_rejected_by_any_violation_with_gates_passed()`
- **test `test_h4_failed_gate_or_no_rise_is_inconclusive`** [L37-40]: `def test_h4_failed_gate_or_no_rise_is_inconclusive()`

