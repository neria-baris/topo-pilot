# `tests/executors/test_local.py`

- Source: [tests/executors/test_local.py](../../../../../tests/executors/test_local.py)
- Kind: python
- Lines: 96

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from exec_helpers import STUB_ENV, make_job, make_store, seed_input` -> [tests/executors/exec_helpers.py](exec_helpers.py.md) (line 8, via same directory)
- `from topo_pilot.contracts import ErrorCode, MetricRecords, RunManifest, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.executors import EXECUTOR_REGISTRY, LocalExecutor, entry` -> [src/topo_pilot/executors/__init__.py](../../src/topo_pilot/executors/__init__.py.md), [src/topo_pilot/executors/entry.py](../../src/topo_pilot/executors/entry.py.md) (line 11, via package root)
- `from topo_pilot.executors._outputs import check_types` -> [src/topo_pilot/executors/_outputs.py](../../src/topo_pilot/executors/_outputs.py.md) (line 12, via package root)
- `from topo_pilot.executors.base import job_to_dict` -> [src/topo_pilot/executors/base.py](../../src/topo_pilot/executors/base.py.md) (line 13, via package root)
- `from topo_pilot.executors.local import write_job_json` -> [src/topo_pilot/executors/local.py](../../src/topo_pilot/executors/local.py.md) (line 14, via package root)

### External (third-party)

- `pytest` (lines 4)

### Standard library

- `collections` (lines 2)
- `json` (lines 1)

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

- **function `run_local`** [L19-24]: `def run_local(fake_repo, root, **job_kwargs)`
- **function `local_ok`** [L28-29]: `def local_ok(fake_repo, tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `local_fail`** [L33-34]: `def local_fail(fake_repo, tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_E01_local_runs_stub_in_subprocess_and_imports_output`** [L37-44]: `def test_E01_local_runs_stub_in_subprocess_and_imports_output(local_ok)`
- **test `test_E01_manifest_records_executor_hardware_and_time`** [L47-55]: `def test_E01_manifest_records_executor_hardware_and_time(local_ok)`
- **test `test_E01_failing_stage_records_failure_and_raises_executor_error`** [L58-64]: `def test_E01_failing_stage_records_failure_and_raises_executor_error(local_fail)`
- **test `test_E01_unknown_stage_returns_1_and_records_executor_error`** [L67-76]: `def test_E01_unknown_stage_returns_1_and_records_executor_error(fake_repo, tmp_path)`
- **test `test_E01_unreadable_job_json_is_executor_error`** [L79-84]: `def test_E01_unreadable_job_json_is_executor_error(tmp_path)`
- **test `test_E01_type_whitelist_allows_manifest_and_rejects_others`** [L87-91]: `def test_E01_type_whitelist_allows_manifest_and_rejects_others()`
- **test `test_E01_registry_lists_all_executors`** [L94-96]: `def test_E01_registry_lists_all_executors()`

