# `tests/experiment/test_x5g1_smoke.py`

- Source: [tests/experiment/test_x5g1_smoke.py](../../../../../tests/experiment/test_x5g1_smoke.py)
- Kind: python
- Lines: 49

## Module docstring

> Builder-authored smoke tests (not the independent X5 G1 tests): integrity failure gives FAILED
> with a ledger entry and exports; STOP before data gives an INCONCLUSIVE outcome, a stopped
> export status and ledger entry; existing output versions are refused; no real artifacts used.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment.x5g1_main import run_gate` -> [src/topo_pilot/experiment/x5g1_main.py](../../src/topo_pilot/experiment/x5g1_main.py.md) (line 8, via package root)
- `from topo_pilot.experiment.x5g1_safety import OutputExists` -> [src/topo_pilot/experiment/x5g1_safety.py](../../src/topo_pilot/experiment/x5g1_safety.py.md) (line 9, via package root)
- `from topo_pilot.experiment.x5g1_controls import StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 43, via package root) (inside a function)

### External (third-party)

- `pytest` (lines 6)

### Standard library

- `json` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 21: `pathlib`
- `__import__` line 42: `pathlib`

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **test `test_missing_parents_is_failed_not_a_scientific_verdict`** [L14-33]: `def test_missing_parents_is_failed_not_a_scientific_verdict(tmp_path)`
- **test `test_stop_before_data_is_inconclusive`** [L36-49]: `def test_stop_before_data_is_inconclusive(tmp_path)`

