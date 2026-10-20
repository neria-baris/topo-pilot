# `tests/executors/test_bundle.py`

- Source: [tests/executors/test_bundle.py](../../../../../tests/executors/test_bundle.py)
- Kind: python
- Lines: 122

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from exec_helpers import make_job, make_store, seed_input, tamper_tar` -> [tests/executors/exec_helpers.py](exec_helpers.py.md) (line 11, via same directory)
- `from topo_pilot.contracts import ErrorCode, MetricRecords, RunManifest, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 13, via package root)
- `from topo_pilot.executors import BundleExecutor` -> [src/topo_pilot/executors/__init__.py](../../src/topo_pilot/executors/__init__.py.md) (line 14, via package root)
- `from stub_stage import StubStage` -> [tests/executors/stub_stage.py](stub_stage.py.md) (line 53, via same directory) (inside a function)

### External (third-party)

- `pytest` (lines 7)

### Standard library

- `collections` (lines 5)
- `os` (lines 1)
- `subprocess` (lines 2)
- `sys` (lines 3)
- `tarfile` (lines 4)

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

- **function `run_remote`** [L19-32]: `def run_remote(fake_repo, root, job_kwargs)` - Build the bundle for a stub job, unpack it in a fresh folder, run run_bundle.py there.
- **function `remote_ok`** [L36-37]: `def remote_ok(fake_repo, tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `remote_fail`** [L41-42]: `def remote_fail(fake_repo, tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `submitted`** [L45-48]: `def submitted(fake_repo, tmp_path, store, **job_kwargs)`
- **test `test_E02_bundle_round_trip_matches_local_run`** [L51-65]: `def test_E02_bundle_round_trip_matches_local_run(store, fake_repo, tmp_path, remote_ok)`
- **test `test_E02_bundle_layout_and_git_sha_recorded`** [L68-76]: `def test_E02_bundle_layout_and_git_sha_recorded(store, fake_repo, tmp_path)`
- **test `test_E02_failed_remote_job_comes_back_as_failure`** [L79-85]: `def test_E02_failed_remote_job_comes_back_as_failure(store, fake_repo, tmp_path, remote_fail)`
- **test `test_E03_tampered_outputs_raise_checksum_mismatch`** [L88-94]: `def test_E03_tampered_outputs_raise_checksum_mismatch(store, fake_repo, tmp_path, remote_ok)`
- **test `test_E03_unexpected_output_type_rejected_and_nothing_imported`** [L97-103]: `def test_E03_unexpected_output_type_rejected_and_nothing_imported(store, fake_repo, tmp_path, remote_ok)`
- **test `test_E03_missing_parent_is_reported`** [L106-111]: `def test_E03_missing_parent_is_reported(fake_repo, tmp_path, remote_ok)`
- **test `test_E05_status_awaiting_user_then_done`** [L114-122]: `def test_E05_status_awaiting_user_then_done(store, fake_repo, tmp_path, remote_ok)`

