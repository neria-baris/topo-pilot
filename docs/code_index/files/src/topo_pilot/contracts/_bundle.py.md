# `src/topo_pilot/contracts/_bundle.py`

- Source: [src/topo_pilot/contracts/_bundle.py](../../../../../../src/topo_pilot/contracts/_bundle.py)
- Kind: python
- Lines: 154

## Module docstring

> Deterministic artifact bundles (tar.gz) for moving artifacts between stores (internal).

## Imports

### Internal (repo files)

- `from .base import ArtifactMeta, payload_checksum` -> [src/topo_pilot/contracts/base.py](base.py.md) (line 16, via relative)
- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 17, via relative)
- `from .ids import make_artifact_id` -> [src/topo_pilot/contracts/ids.py](ids.py.md) (line 18, via relative)
- `from .schemas import ARTIFACT_CLASSES` -> [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 19, via relative)
- `from .store import ArtifactStore` -> [src/topo_pilot/contracts/store.py](store.py.md) (line 22, via relative)

### External (third-party)

- `numpy` (lines 14)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 10)
- `gzip` (lines 5)
- `hashlib` (lines 6)
- `io` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 11)
- `tarfile` (lines 9)
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

- [src/topo_pilot/contracts/store.py](store.py.md) (line 14, import)

## Top-level constants

- `INDEX_NAME`
- `PREFIX`

## Classes and functions

- **function `_fail`** [L28-29]: `def _fail(code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure`
- **function `_closure`** [L32-49]: `def _closure(store: ArtifactStore, ids: Sequence[str], with_parents: bool) -> list[str]` - Ids in dependency order (parents first).
- **function `export_bundle`** [L52-77]: `def export_bundle(store: ArtifactStore, ids: Sequence[str], dest: Path, with_parents: bool) -> Path` - Tar every file of the selected artifacts under ``artifacts/<type>/<id>/`` plus an index.
- **function `_read_members`** [L80-92]: `def _read_members(src: Path) -> dict[str, bytes]`
- **function `import_bundle`** [L95-127]: `def import_bundle(store: ArtifactStore, src: Path) -> list[str]` - Verify everything first, then write in dependency order.
- **function `_verify_one`** [L130-154]: `def _verify_one(store: ArtifactStore, meta: ArtifactMeta, group: dict[str, bytes], bundle_ids: set[str]) -> None`

