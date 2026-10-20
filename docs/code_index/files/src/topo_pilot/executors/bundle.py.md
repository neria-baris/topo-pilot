# `src/topo_pilot/executors/bundle.py`

- Source: [src/topo_pilot/executors/bundle.py](../../../../../../src/topo_pilot/executors/bundle.py)
- Kind: python
- Lines: 167

## Module docstring

> BundleExecutor: a self-contained ``bundle_<job>.tar.gz`` to run on any machine.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from ._outputs import import_outputs, raise_if_failed` -> [src/topo_pilot/executors/_outputs.py](_outputs.py.md) (line 14, via relative)
- `from .base import Executor, JobHandle, JobSpec, Status, default_repo_root, executor_error, git_sha, register_executor` -> [src/topo_pilot/executors/base.py](base.py.md) (line 15, via relative)
- `from .local import write_job_json` -> [src/topo_pilot/executors/local.py](local.py.md) (line 25, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `collections` (lines 9)
- `fnmatch` (lines 5)
- `logging` (lines 6)
- `pathlib` (lines 10)
- `tarfile` (lines 7)
- `tempfile` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/__init__.py](__init__.py.md) (line 5, import)
- [src/topo_pilot/executors/ssh.py](ssh.py.md) (line 24, import)
- [tests/executors/test_exporter.py](../../../tests/executors/test_exporter.py.md) (line 13, import)

## Top-level constants

- `LOG`
- `SECRET_GLOBS`
- `SECRET_NAMES`
- `SKIP_DIRS`
- `SKIP_SUFFIXES`
- `SOURCE_ENTRIES`

## Classes and functions

- **function `is_forbidden`** [L36-41]: `def is_forbidden(name: str) -> bool` - True for ``local.yaml``, ``.env`` (and ``.env.*``) and anything matching ``*key*`` or
- **function `_skip`** [L44-46]: `def _skip(path: Path) -> bool`
- **function `collect_files`** [L49-70]: `def collect_files(repo_root: Path, extra_files: Sequence[Path] = ()) -> dict[str, Path]` - ``bundle-relative posix path -> file`` for the source tree.
- **function `build_bundle`** [L73-99]: `def build_bundle(job: JobSpec, store: ArtifactStore, repo_root: Path, out_dir: Path, extra_files: Sequence[Path] = ()) -> Path` - Write ``out_dir/bundle_<job_id>.tar.gz`` (layout in docs/EXECUTION.md §3).
- **class `BundleExecutor(Executor)`** [L103-167] decorators: @register_executor - Packs the job for a machine the user operates by hand (Colab, Kaggle, a rented GPU).
- **method `BundleExecutor.__init__`** [L118-124]: `def __init__(self, out_dir: Path | None = None, repo_root: Path | None = None, extra_files: Sequence[Path] = ()) -> None`
- **method `BundleExecutor.submit`** [L126-133]: `def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle` - Write the bundle; the job is then ``awaiting_user``.
- **method `BundleExecutor.instructions`** [L135-142]: `def instructions(self, handle: JobHandle) -> str` - What the user must upload, run and download.
- **method `BundleExecutor.status`** [L144-148]: `def status(self, handle: JobHandle) -> Status` - ``awaiting_user`` after submit, ``done`` after a successful fetch.
- **method `BundleExecutor.fetch`** [L150-167]: `def fetch(self, handle: JobHandle, store: ArtifactStore, outputs_path: Path | None = None) -> list[str]` - Import the outputs tarball; returns the stage output ids (the RunManifest is imported

