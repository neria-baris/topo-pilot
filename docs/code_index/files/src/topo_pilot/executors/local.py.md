# `src/topo_pilot/executors/local.py`

- Source: [src/topo_pilot/executors/local.py](../../../../../../src/topo_pilot/executors/local.py)
- Kind: python
- Lines: 111

## Module docstring

> LocalExecutor: run ``python -m topo_pilot.executors.entry`` in a subprocess.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)
- `from ._outputs import check_types, raise_if_failed` -> [src/topo_pilot/executors/_outputs.py](_outputs.py.md) (line 16, via relative)
- `from .base import Executor, JobHandle, JobSpec, Status, default_repo_root, executor_error, git_sha, job_to_dict, local_root, register_executor` -> [src/topo_pilot/executors/base.py](base.py.md) (line 17, via relative)
- `from .entry import result_path_for` -> [src/topo_pilot/executors/entry.py](entry.py.md) (line 29, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `collections` (lines 10)
- `json` (lines 5)
- `os` (lines 6)
- `pathlib` (lines 11)
- `subprocess` (lines 7)
- `sys` (lines 8)
- `tempfile` (lines 9)
- `typing` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/__init__.py](__init__.py.md) (line 7, import)
- [src/topo_pilot/executors/bundle.py](bundle.py.md) (line 25, import)
- [tests/executors/test_local.py](../../../tests/executors/test_local.py.md) (line 14, import)

## Top-level constants

- none

## Classes and functions

- **function `write_job_json`** [L32-40]: `def write_job_json(path: Path, job: JobSpec, *, store_root: str, repo_root: str, executor: str, sha: str, stages_yaml: str = 'configs/stages.yaml') -> Path` - Write the ``job.json`` that ``entry`` reads.
- **class `LocalExecutor(Executor)`** [L44-111] decorators: @register_executor - Runs the job in a subprocess of the same Python environment, on the same store.
- **method `LocalExecutor.__init__`** [L56-62]: `def __init__(self, work_dir: Path | None = None, repo_root: Path | None = None, env: Mapping[str, str] | None = None) -> None`
- **method `LocalExecutor.submit`** [L64-79]: `def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle` - Start the subprocess; ``store`` must be a ``LocalFSBackend`` store.
- **method `LocalExecutor._proc`** [L81-84]: `def _proc(self, handle: JobHandle) -> subprocess.Popen`
- **method `LocalExecutor.status`** [L86-91]: `def status(self, handle: JobHandle) -> Status` - ``running`` while the subprocess lives, then ``done`` (exit 0) or ``failed``.
- **method `LocalExecutor.fetch`** [L93-111]: `def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]` - Wait for the subprocess; return the output ids (already in the shared store).

