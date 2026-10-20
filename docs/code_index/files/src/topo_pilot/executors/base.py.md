# `src/topo_pilot/executors/base.py`

- Source: [src/topo_pilot/executors/base.py](../../../../../../src/topo_pilot/executors/base.py)
- Kind: python
- Lines: 129

## Module docstring

> Job description, executor ABC, registry, and job.json (de)serialisation (internal).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, LocalFSBackend, StageFailure, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 13, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `abc` (lines 7)
- `collections` (lines 8)
- `dataclasses` (lines 9)
- `json` (lines 5)
- `pathlib` (lines 10)
- `subprocess` (lines 6)
- `typing` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/__init__.py](__init__.py.md) (line 4, import)
- [src/topo_pilot/executors/_outputs.py](_outputs.py.md) (line 11, import)
- [src/topo_pilot/executors/bundle.py](bundle.py.md) (line 15, import)
- [src/topo_pilot/executors/entry.py](entry.py.md) (line 18, import)
- [src/topo_pilot/executors/local.py](local.py.md) (line 17, import)
- [src/topo_pilot/executors/ssh.py](ssh.py.md) (line 15, import)
- [tests/executors/test_local.py](../../../tests/executors/test_local.py.md) (line 13, import)

## Top-level constants

- `EXECUTOR_REGISTRY`

## Classes and functions

- **class `JobSpec`** [L25-41] decorators: @dataclass(frozen=True) - One unit of work: a stage plus the artifacts it reads.
- **class `JobHandle`** [L45-50] decorators: @dataclass(frozen=True) - Opaque reference to a submitted job (``location`` is a path, a remote path, or a pid).
- **class `Executor(ABC)`** [L53-69] - Where a job runs. Stage code is executor-agnostic; the executor decides where the store
- **method `Executor.submit`** [L60-61]: `def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle` decorators: @abstractmethod - Start (or prepare) the job.
- **method `Executor.status`** [L64-65]: `def status(self, handle: JobHandle) -> Status` decorators: @abstractmethod - Current state; ``awaiting_user`` means the user must move files by hand.
- **method `Executor.fetch`** [L68-69]: `def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]` decorators: @abstractmethod - Import the job outputs into ``store`` and return their artifact ids.
- **function `register_executor`** [L75-78]: `def register_executor(cls: type[Executor]) -> type[Executor]` - Class decorator adding an executor to ``EXECUTOR_REGISTRY`` under ``cls.name``.
- **function `executor_error`** [L81-84]: `def executor_error(check: str, detail: str, code: ErrorCode = ErrorCode.EXECUTOR_ERROR, artifact_id: str | None = None) -> StageFailure` - Build a ``StageFailure`` for the executors component.
- **function `job_to_dict`** [L87-95]: `def job_to_dict(job: JobSpec) -> dict[str, Any]` - JSON-ready dict of a JobSpec (tuples become lists).
- **function `job_from_dict`** [L98-107]: `def job_from_dict(data: Mapping[str, Any]) -> JobSpec` - Inverse of :func:`job_to_dict`.
- **function `local_root`** [L110-114]: `def local_root(store: ArtifactStore) -> Path` - Directory of a ``LocalFSBackend`` store; ``EXECUTOR_ERROR`` for any other backend.
- **function `git_sha`** [L117-124]: `def git_sha(repo_root: Path) -> str` - ``git rev-parse HEAD`` in ``repo_root``, or ``"unknown"``.
- **function `default_repo_root`** [L127-129]: `def default_repo_root() -> Path` - The repository root, found relative to this file (``src/topo_pilot/executors``).

