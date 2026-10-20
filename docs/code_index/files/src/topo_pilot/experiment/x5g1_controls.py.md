# `src/topo_pilot/experiment/x5g1_controls.py`

- Source: [src/topo_pilot/experiment/x5g1_controls.py](../../../../../../src/topo_pilot/experiment/x5g1_controls.py)
- Kind: python
- Lines: 109

## Module docstring

> X5 G1 run controls (x5g1-feas-v2 §7): STOP/budget guard and a crash-safe cumulative ledger.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `json` (lines 5)
- `math` (lines 6)
- `os` (lines 7)
- `pathlib` (lines 9)
- `time` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 39, import)
- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 31, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 41, import)
- [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 13, import)
- [src/topo_pilot/experiment/x5g1_scorebench.py](x5g1_scorebench.py.md) (line 37, import)
- [src/topo_pilot/experiment/x5g1_techbench.py](x5g1_techbench.py.md) (line 29, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 45, import)
- [src/topo_pilot/experiment/x5g1t_exports.py](x5g1t_exports.py.md) (line 16, import)
- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 22, import)
- [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 23, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 38, import)
- [tests/experiment/test_x4f_maintenance.py](../../../tests/experiment/test_x4f_maintenance.py.md) (line 11, import)
- [tests/experiment/test_x5g1_controls.py](../../../tests/experiment/test_x5g1_controls.py.md) (line 19, import)
- [tests/experiment/test_x5g1_export_integration.py](../../../tests/experiment/test_x5g1_export_integration.py.md) (line 26, import)
- [tests/experiment/test_x5g1_safety.py](../../../tests/experiment/test_x5g1_safety.py.md) (line 18, import)
- [tests/experiment/test_x5g1_smoke.py](../../../tests/experiment/test_x5g1_smoke.py.md) (line 43, import)
- [tests/experiment/test_x5g1t_export_checks.py](../../../tests/experiment/test_x5g1t_export_checks.py.md) (line 18, import)
- [tests/experiment/test_x5g1t_runtime.py](../../../tests/experiment/test_x5g1t_runtime.py.md) (line 19, import)
- [tests/experiment/test_x5g1t_runtime_boundary.py](../../../tests/experiment/test_x5g1t_runtime_boundary.py.md) (line 21, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 21, import)

## Top-level constants

- none

## Classes and functions

- **class `StopRequested(RuntimeError)`** [L14-15] - The mailbox STOP file exists.
- **class `BudgetExceeded(RuntimeError)`** [L18-19] - The per-run or cumulative CPU cap was reached.
- **class `LedgerCorrupt(RuntimeError)`** [L22-23] - The existing ledger cannot be parsed; it is left untouched.
- **class `RunControls`** [L26-91] - Guard before/after operations and always persist a ledger entry on exit.
- **method `RunControls.__init__`** [L36-43]: `def __init__(self, ledger_path: Path, cap_s: float, stop_path: Path, job: str, cumulative_cap_s: float) -> None`
- **method `RunControls._read`** [L45-59]: `def _read(self) -> dict`
- **method `RunControls.cpu`** [L61-62]: `def cpu(self) -> float`
- **method `RunControls.guard`** [L64-70]: `def guard(self, step: str) -> None`
- **method `RunControls.__enter__`** [L72-74]: `def __enter__(self) -> RunControls`
- **method `RunControls.__exit__`** [L76-91]: `def __exit__(self, exc_type, exc, tb) -> bool`
- **function `verify_parents`** [L94-109]: `def verify_parents(store: ArtifactStore, expected: dict[str, str]) -> list[str]` - Failures for artifacts that are missing or whose payload_sha256 lacks the expected

