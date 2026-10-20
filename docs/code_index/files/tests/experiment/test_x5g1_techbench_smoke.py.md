# `tests/experiment/test_x5g1_techbench_smoke.py`

- Source: [tests/experiment/test_x5g1_techbench_smoke.py](../../../../../tests/experiment/test_x5g1_techbench_smoke.py)
- Kind: python
- Lines: 30

## Module docstring

> Builder-authored smoke test of the technical benchmark plumbing (tiny sizes; timing values are
> not checked): outputs, decision field, separate technical ledger, immutable output directory.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x5g1_techbench` -> [src/topo_pilot/experiment/x5g1_techbench.py](../../src/topo_pilot/experiment/x5g1_techbench.py.md) (line 7, via package root)
- `from topo_pilot.experiment.x5g1_safety import OutputExists` -> [src/topo_pilot/experiment/x5g1_safety.py](../../src/topo_pilot/experiment/x5g1_safety.py.md) (line 8, via package root)

### External (third-party)

- `pytest` (lines 5)

### Standard library

- `json` (lines 3)

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

- **test `test_techbench_plumbing`** [L13-30]: `def test_techbench_plumbing(tmp_path, monkeypatch)`

