# `tests/integration/test_s1.py`

- Source: [tests/integration/test_s1.py](../../../../../tests/integration/test_s1.py)
- Kind: python
- Lines: 46

## Module docstring

> I01: S1 on the real core config produces the specs and passes G-A checks 1-2 (and 3).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, GateCheck, GateReport, LocalFSBackend, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.experiment import load_config, run_stage` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 16, via package root)

### External (third-party)

- `pytest` (lines 5)

### Standard library

- `pathlib` (lines 3)

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

- `REPO`

## Classes and functions

- **test `test_I01_s1_core_config`** [L23-46]: `def test_I01_s1_core_config(tmp_path)`

