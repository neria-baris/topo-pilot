# `src/topo_pilot/executors/entry.py`

- Source: [src/topo_pilot/executors/entry.py](../../../../../../src/topo_pilot/executors/entry.py)
- Kind: python
- Lines: 142

## Module docstring

> In-bundle / subprocess entry point: ``python -m topo_pilot.executors.entry <job.json>``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, LocalFSBackend, RunManifest, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 16, via package root)
- `from .base import JobSpec, executor_error, git_sha, job_from_dict, job_to_dict` -> [src/topo_pilot/executors/base.py](base.py.md) (line 18, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `importlib` (lines 5)
- `json` (lines 6)
- `logging` (lines 7)
- `os` (lines 8)
- `pathlib` (lines 13)
- `platform` (lines 9)
- `shutil` (lines 10)
- `subprocess` (lines 33)
- `sys` (lines 11)
- `time` (lines 12)
- `typing` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 56: `dynamic: module`
- `import_module` line 57: `topo_pilot.experiment` -> [src/topo_pilot/experiment/__init__.py](../experiment/__init__.py.md)

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/__init__.py](__init__.py.md) (line 6, import)
- [src/topo_pilot/executors/local.py](local.py.md) (line 29, import)
- [tests/executors/test_local.py](../../../tests/executors/test_local.py.md) (line 11, import)

## Top-level constants

- `LOG`

## Classes and functions

- **function `result_path_for`** [L23-25]: `def result_path_for(job_json: Path) -> Path` - Where ``entry`` writes its result summary (next to the job file).
- **function `hardware_info`** [L28-42]: `def hardware_info() -> dict[str, Any]` - Host description recorded in the RunManifest (stdlib only; GPU via ``nvidia-smi``).
- **function `_failure_dict`** [L45-50]: `def _failure_dict(exc: BaseException) -> dict[str, Any]`
- **function `_dispatch`** [L53-63]: `def _dispatch(job: JobSpec, store: ArtifactStore, repo_root: Path, stages_yaml: Path) -> list[str]`
- **function `_write_manifest`** [L66-77]: `def _write_manifest(store: ArtifactStore, job: JobSpec, executor: str, outputs: list[str], failures: list[dict[str, Any]], started_ns: int, wall: float) -> str`
- **function `_resolve`** [L80-82]: `def _resolve(base: Path, value: str) -> Path`
- **function `entry`** [L85-125]: `def entry(job_json: Path) -> int` - Run the job described by ``job_json``; return 0 on success, 1 after recording a failure.
- **function `main`** [L128-138]: `def main(argv: list[str] | None = None) -> int` - CLI wrapper around :func:`entry`.

