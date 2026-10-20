# `tests/integration/test_s2_mini.py`

- Source: [tests/integration/test_s2_mini.py](../../../../../tests/integration/test_s2_mini.py)
- Kind: python
- Lines: 70

## Module docstring

> I02: S1 -> S2 on a scaled-down config (n = 4, V = 4, small data) runs end to end.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, BaselineOutputs, ErrorCode, GateCheck, GateReport, LocalFSBackend, MetricRecords, OracleOutputs, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 9, via package root)
- `from topo_pilot.experiment import load_config, run_stage` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 20, via package root)

### External (third-party)

- `pytest` (lines 6)
- `yaml` (lines 7)

### Standard library

- `pathlib` (lines 4)
- `shutil` (lines 3)

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

- **function `_mini_configs`** [L27-36]: `def _mini_configs(tmp: Path) -> Path`
- **test `test_I02_s2_mini_end_to_end`** [L39-70]: `def test_I02_s2_mini_end_to_end(tmp_path)`

