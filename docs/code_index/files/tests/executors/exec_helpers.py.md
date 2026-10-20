# `tests/executors/exec_helpers.py`

- Source: [tests/executors/exec_helpers.py](../../../../../tests/executors/exec_helpers.py)
- Kind: python
- Lines: 48

## Module docstring

> Plain helpers shared by the executors tests.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.executors import JobSpec` -> [src/topo_pilot/executors/__init__.py](../../src/topo_pilot/executors/__init__.py.md) (line 9, via package root)

### External (third-party)

- none

### Standard library

- `io` (lines 3)
- `json` (lines 4)
- `pathlib` (lines 6)
- `tarfile` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/executors/conftest.py](conftest.py.md) (line 12, import)
- [tests/executors/test_bundle.py](test_bundle.py.md) (line 11, import)
- [tests/executors/test_exporter.py](test_exporter.py.md) (line 9, import)
- [tests/executors/test_local.py](test_local.py.md) (line 8, import)

## Top-level constants

- `STUB_ENV`

## Classes and functions

- **function `make_store`** [L12-14]: `def make_store(path: Path) -> ArtifactStore` - A LocalFS store with a fixed producer version.
- **function `seed_input`** [L17-20]: `def seed_input(store: ArtifactStore) -> str` - Save the MetricRecords input (value 10.0) of the stub jobs.
- **function `make_job`** [L23-29]: `def make_job(input_id: str, job_id: str = 'j1', expected=('MetricRecords',), **extra) -> JobSpec` - A STUB job reading ``input_id``.
- **function `tamper_tar`** [L32-45]: `def tamper_tar(src: Path, dest: Path) -> Path` - Copy a bundle, bumping the first metric value inside every ``extra.json`` that has rows

