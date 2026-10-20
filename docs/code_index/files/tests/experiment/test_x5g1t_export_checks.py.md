# `tests/experiment/test_x5g1t_export_checks.py`

- Source: [tests/experiment/test_x5g1t_export_checks.py](../../../../../tests/experiment/test_x5g1t_export_checks.py)
- Kind: python
- Lines: 204

## Module docstring

> Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
> (docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
> modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
> full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
> Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment.x5g1_controls import BudgetExceeded, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 18, via package root)
- `from topo_pilot.experiment.x5g1t_runtime import ResourceExceeded` -> [src/topo_pilot/experiment/x5g1t_runtime.py](../../src/topo_pilot/experiment/x5g1t_runtime.py.md) (line 19, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `hashlib` (lines 10)
- `importlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 24: `topo_pilot.experiment.x5g1t_config` -> [src/topo_pilot/experiment/x5g1t_config.py](../../src/topo_pilot/experiment/x5g1t_config.py.md)
- `import_module` line 28: `topo_pilot.experiment.x5g1t_exports` -> [src/topo_pilot/experiment/x5g1t_exports.py](../../src/topo_pilot/experiment/x5g1t_exports.py.md)
- `import_module` line 32: `topo_pilot.experiment.x5g1t_checks` -> [src/topo_pilot/experiment/x5g1t_checks.py](../../src/topo_pilot/experiment/x5g1t_checks.py.md)

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `FILES`
- `STATUS`

## Classes and functions

- **function `_cm`** [L23-24]: `def _cm()`
- **function `_ex`** [L27-28]: `def _ex()`
- **function `_ck`** [L31-32]: `def _ck()`
- **function `_sha_file`** [L35-36]: `def _sha_file(p: Path) -> str`
- **class `FakeSC`** [L40-50] - StudyControls stand-in: records each boundary and raises ``exc`` where ``stop_at``.
- **method `FakeSC.__init__`** [L43-45]: `def __init__(self, stop_at=None, exc=StopRequested)`
- **method `FakeSC.boundary`** [L47-50]: `def boundary(self, what, next_estimate=0.0, reserve=0.0, audit=dict)`
- **function `_out`** [L58-61]: `def _out(tmp_path: Path) -> Path`
- **function `_data_files`** [L64-66]: `def _data_files(out: Path) -> list[str]`
- **function `_status`** [L69-70]: `def _status(out: Path) -> dict`
- **function `_complete`** [L73-76]: `def _complete(tmp_path: Path, arrays=None) -> Path`
- **test `test_export_roundtrip_complete_and_guarded`** [L79-101]: `def test_export_roundtrip_complete_and_guarded(tmp_path)`
- **test `test_export_roundtrip_with_arrays`** [L104-109]: `def test_export_roundtrip_with_arrays(tmp_path)`
- **test `test_export_interrupted_before_second_file`** [L113-128]: `def test_export_interrupted_before_second_file(tmp_path, exc)` decorators: @pytest.mark.parametrize('exc', [StopRequested, BudgetExceeded, ResourceExceeded])
- **test `test_export_stop_after_file_done_writes_nothing_further`** [L131-141]: `def test_export_stop_after_file_done_writes_nothing_further(tmp_path)`
- **test `test_export_stop_before_manifest`** [L144-156]: `def test_export_stop_before_manifest(tmp_path)`
- **test `test_export_tampered_file_bytes_incomplete`** [L159-164]: `def test_export_tampered_file_bytes_incomplete(tmp_path)`
- **test `test_export_extra_file_incomplete`** [L167-171]: `def test_export_extra_file_incomplete(tmp_path)`
- **test `test_export_missing_manifest_incomplete`** [L174-178]: `def test_export_missing_manifest_incomplete(tmp_path)`
- **test `test_export_missing_data_file_incomplete`** [L181-185]: `def test_export_missing_data_file_incomplete(tmp_path)`
- **test `test_export_missing_or_non_complete_status_incomplete`** [L188-198]: `def test_export_missing_or_non_complete_status_incomplete(tmp_path)`
- **test `test_export_error_classes_are_runtime_errors`** [L201-204]: `def test_export_error_classes_are_runtime_errors()`

