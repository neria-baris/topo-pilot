# `src/topo_pilot/executors/ssh.py`

- Source: [src/topo_pilot/executors/ssh.py](../../../../../../src/topo_pilot/executors/ssh.py)
- Kind: python
- Lines: 130

## Module docstring

> SSHExecutor: the same bundle, copied and run with the system ``ssh`` and ``scp``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from ._outputs import import_outputs, raise_if_failed` -> [src/topo_pilot/executors/_outputs.py](_outputs.py.md) (line 14, via relative)
- `from .base import Executor, JobHandle, JobSpec, Status, default_repo_root, executor_error, register_executor` -> [src/topo_pilot/executors/base.py](base.py.md) (line 15, via relative)
- `from .bundle import build_bundle` -> [src/topo_pilot/executors/bundle.py](bundle.py.md) (line 24, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `collections` (lines 8)
- `logging` (lines 5)
- `pathlib` (lines 9)
- `shlex` (lines 6)
- `subprocess` (lines 7)
- `typing` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/__init__.py](__init__.py.md) (line 9, import)

## Top-level constants

- `LOG`

## Classes and functions

- **class `SSHExecutor(Executor)`** [L30-130] decorators: @register_executor - Runs a bundle on a reachable machine. Credentials come from the user's SSH config
- **method `SSHExecutor.__init__`** [L45-58]: `def __init__(self, local: Mapping[str, Any], out_dir: Path | None = None, repo_root: Path | None = None) -> None`
- **method `SSHExecutor.target`** [L61-63]: `def target(self) -> str` decorators: @property - ``user@host`` or ``host``.
- **method `SSHExecutor._remote_job_dir`** [L65-66]: `def _remote_job_dir(self, job_id: str) -> str`
- **method `SSHExecutor.upload_cmd`** [L69-71]: `def upload_cmd(self, bundle: Path) -> list[str]` - ``scp`` of the bundle into ``remote_dir``.
- **method `SSHExecutor.run_cmd`** [L73-81]: `def run_cmd(self, job_id: str) -> list[str]` - ``ssh`` command that unpacks the bundle and starts ``run_bundle.py`` detached;
- **method `SSHExecutor.status_cmd`** [L83-86]: `def status_cmd(self, job_id: str) -> list[str]` - ``ssh`` command printing the exit code, or ``running``.
- **method `SSHExecutor.download_cmd`** [L88-91]: `def download_cmd(self, job_id: str, dest: Path) -> list[str]` - ``scp`` of ``outputs_<job>.tar.gz`` back to ``dest``.
- **method `SSHExecutor._exec`** [L94-101]: `def _exec(self, cmd: Sequence[str]) -> str`
- **method `SSHExecutor.submit`** [L103-111]: `def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle` - Build the bundle, copy it over, and start it remotely.
- **method `SSHExecutor.status`** [L113-118]: `def status(self, handle: JobHandle) -> Status` - ``running`` until the remote ``exit_code`` file exists, then ``done`` or ``failed``.
- **method `SSHExecutor.fetch`** [L120-130]: `def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]` - Download the outputs and import them (same checks as ``BundleExecutor``).

