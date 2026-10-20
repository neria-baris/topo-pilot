# `tests/analysis/test_x4f_family_maintenance.py`

- Source: [tests/analysis/test_x4f_family_maintenance.py](../../../../../tests/analysis/test_x4f_family_maintenance.py)
- Kind: python
- Lines: 56

## Module docstring

> Synthetic fault injection into map construction and STOP within the draw loop.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import random_family, whiten` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 5, via package root)
- `from topo_pilot.analysis import x4f_erasure` -> [src/topo_pilot/analysis/x4f_erasure.py](../../src/topo_pilot/analysis/x4f_erasure.py.md) (line 6, via package root)

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

- **test `test_family_stop_before_second_draw`** [L11-25]: `def test_family_stop_before_second_draw()`
- **test `test_invalid_accepted_map_fails_closed`** [L30-56]: `def test_invalid_accepted_map_fails_closed(monkeypatch, defect)` decorators: @pytest.mark.parametrize('defect', ['idempotence', 'small_idempotence', 'rank', 'range', 'complement', 'nonfinite'])

