# `src/topo_pilot/executors/_outputs.py`

- Source: [src/topo_pilot/executors/_outputs.py](../../../../../../src/topo_pilot/executors/_outputs.py)
- Kind: python
- Lines: 66

## Module docstring

> Output checks shared by all executors: type whitelist, bundle peeking, failure lookup.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, RunManifest` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)
- `from .base import executor_error` -> [src/topo_pilot/executors/base.py](base.py.md) (line 11, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `collections` (lines 6)
- `pathlib` (lines 7)
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

- [src/topo_pilot/executors/bundle.py](bundle.py.md) (line 14, import)
- [src/topo_pilot/executors/local.py](local.py.md) (line 16, import)
- [src/topo_pilot/executors/ssh.py](ssh.py.md) (line 14, import)
- [tests/executors/test_local.py](../../../tests/executors/test_local.py.md) (line 12, import)

## Top-level constants

- `ALWAYS_ALLOWED`

## Classes and functions

- **function `check_types`** [L16-21]: `def check_types(types: Sequence[str], expected: Sequence[str], where: str) -> None` - Reject any artifact type outside ``expected`` (``RunManifest`` is always allowed).
- **function `peek_bundle_types`** [L24-37]: `def peek_bundle_types(path: Path) -> dict[str, str]` - ``artifact_id -> artifact_type`` read from the member names of a bundle, without writing
- **function `import_outputs`** [L40-55]: `def import_outputs(store: ArtifactStore, outputs_path: Path, expected: Sequence[str]) -> tuple[list[str], list[str]]` - Check types, then verify-and-import an outputs tarball.
- **function `raise_if_failed`** [L58-66]: `def raise_if_failed(store: ArtifactStore, manifest_ids: Sequence[str], job_id: str) -> None` - ``EXECUTOR_ERROR`` wrapping the failures recorded in the job's RunManifest(s).

