# `src/topo_pilot/contracts/store.py`

- Source: [src/topo_pilot/contracts/store.py](../../../../../../src/topo_pilot/contracts/store.py)
- Kind: python
- Lines: 239

## Module docstring

> Content-addressed artifact store with an access policy (DATA_SCHEMAS §1, §7).

## Imports

### Internal (repo files)

- `from . import _bundle` -> [src/topo_pilot/contracts/_bundle.py](_bundle.py.md) (line 14, via relative)
- `from .backends import ArtifactBackend` -> [src/topo_pilot/contracts/backends.py](backends.py.md) (line 15, via relative)
- `from .base import Artifact, ArtifactMeta, payload_checksum` -> [src/topo_pilot/contracts/base.py](base.py.md) (line 16, via relative)
- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 17, via relative)
- `from .ids import SCHEMA_VERSION, canonical_json, make_artifact_id` -> [src/topo_pilot/contracts/ids.py](ids.py.md) (line 18, via relative)
- `from .schemas import ARTIFACT_CLASSES` -> [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 19, via relative)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 7)
- `datetime` (lines 8)
- `io` (lines 5)
- `json` (lines 6)
- `pathlib` (lines 9)
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

- [src/topo_pilot/contracts/__init__.py](__init__.py.md) (line 39, import)
- [src/topo_pilot/contracts/_bundle.py](_bundle.py.md) (line 22, import)
- [src/topo_pilot/contracts/testing.py](testing.py.md) (line 16, import)

## Top-level constants

- `A`
- `DEFAULT_ACCESS_POLICY`
- `MODULES`
- `_SPEC_READERS`

## Classes and functions

- **class `AccessPolicy`** [L30-47] - Which consumers may load which artifact types.
- **method `AccessPolicy.__init__`** [L39-40]: `def __init__(self, rules: Mapping[str, frozenset[str]]) -> None`
- **method `AccessPolicy.check`** [L42-47]: `def check(self, artifact_type: str, consumer: str) -> None` - Raise ``LEAKAGE`` if ``consumer`` may not load ``artifact_type``.
- **class `ArtifactStore`** [L60-239] - Typed, content-addressed, immutable artifact storage.
- **method `ArtifactStore.__init__`** [L74-78]: `def __init__(self, backend: ArtifactBackend, policy: AccessPolicy = DEFAULT_ACCESS_POLICY, producer_version: str = 'unknown') -> None`
- **method `ArtifactStore._key`** [L82-83]: `def _key(artifact_type: str, artifact_id: str, name: str) -> str` decorators: @staticmethod
- **method `ArtifactStore._fail`** [L85-87]: `def _fail(self, code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure`
- **method `ArtifactStore.save`** [L90-124]: `def save(self, artifact: Artifact, *, config: Mapping[str, Any], parents: Sequence[str], seed_map: Mapping[str, int], consumer: str) -> str` - Validate, derive the id, and write; idempotent for identical content.
- **method `ArtifactStore._encode_files`** [L126-138]: `def _encode_files(self, artifact: Artifact, arrays: Mapping[str, np.ndarray | bytes], extra: Mapping[str, Any]) -> dict[str, bytes]`
- **method `ArtifactStore._write`** [L140-148]: `def _write(self, meta: ArtifactMeta, files: Mapping[str, bytes]) -> None`
- **method `ArtifactStore._read_meta`** [L151-155]: `def _read_meta(self, atype: str, aid: str) -> ArtifactMeta`
- **method `ArtifactStore._read_files`** [L157-171]: `def _read_files(self, meta: ArtifactMeta) -> tuple[dict[str, np.ndarray | bytes], dict]`
- **method `ArtifactStore._verify_stored`** [L173-178]: `def _verify_stored(self, meta: ArtifactMeta) -> tuple[dict[str, np.ndarray | bytes], dict]`
- **method `ArtifactStore._check_version`** [L180-183]: `def _check_version(self, meta: ArtifactMeta) -> None`
- **method `ArtifactStore.load`** [L185-199]: `def load(self, cls: type[A], artifact_id: str, *, consumer: str) -> A` - Load and re-validate an artifact. Order of checks: access policy (``LEAKAGE``),
- **method `ArtifactStore.meta`** [L201-207]: `def meta(self, artifact_id: str) -> ArtifactMeta` - The envelope of any stored artifact (no access check: metadata is not privileged).
- **method `ArtifactStore._is_complete`** [L209-213]: `def _is_complete(self, artifact_id: str) -> bool`
- **method `ArtifactStore.find`** [L215-228]: `def find(self, cls: type[Artifact], **config_filter: Any) -> list[str]` - Ids (sorted) of complete artifacts of ``cls`` whose top-level config entries equal
- **method `ArtifactStore.export_bundle`** [L231-233]: `def export_bundle(self, ids: Sequence[str], dest: Path, *, with_parents: bool = True) -> Path` - Write a deterministic ``.tar.gz`` holding ``ids`` (and, by default, all ancestors).
- **method `ArtifactStore.import_bundle`** [L235-239]: `def import_bundle(self, src: Path) -> list[str]` - Import a bundle; verifies schema versions, ids, checksums and parents first

