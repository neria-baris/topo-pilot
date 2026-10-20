# `src/topo_pilot/experiment/x5g1t_exports.py`

- Source: [src/topo_pilot/experiment/x5g1t_exports.py](../../../../../../src/topo_pilot/experiment/x5g1t_exports.py)
- Kind: python
- Lines: 100

## Module docstring

> X5 G1 study exports under the full study controls (x5g1-train-v4 §8, §11; API v4 §4).

## Imports

### Internal (repo files)

- `from .x5g1_controls import BudgetExceeded, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 16, via relative)
- `from .x5g1t_runtime import ResourceExceeded, StudyControls` -> [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 17, via relative)

### External (third-party)

- `numpy` (lines 14)

### Standard library

- `__future__` (lines 8)
- `hashlib` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 26, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 42, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 46, import)
- [tests/experiment/test_x5g1t_export_checks.py](../../../tests/experiment/test_x5g1t_export_checks.py.md) (line 28, dynamic)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 19, import)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 20, import)

## Top-level constants

- `_STOPS`

## Classes and functions

- **class `ExportIncomplete(RuntimeError)`** [L24-25] - A prerequisite export is missing, stopped, tampered or has unexpected files.
- **function `_sha`** [L28-29]: `def _sha(path: Path) -> str`
- **function `_jsonable`** [L32-41]: `def _jsonable(obj)`
- **function `study_export`** [L44-78]: `def study_export(sc: StudyControls, out: Path, files: dict, arrays: dict | None = None, reserve: float = 0.0) -> None` - Guarded JSON files, npz arrays, manifest and COMPLETE status (in that order).
- **function `verify_export_complete`** [L81-100]: `def verify_export_complete(out: Path) -> dict` - Manifest of a COMPLETE export whose files match exactly; else ``ExportIncomplete``.

