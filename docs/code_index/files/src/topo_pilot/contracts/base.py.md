# `src/topo_pilot/contracts/base.py`

- Source: [src/topo_pilot/contracts/base.py](../../../../../../src/topo_pilot/contracts/base.py)
- Kind: python
- Lines: 185

## Module docstring

> Artifact envelope (``ArtifactMeta``) and the ``Artifact`` base class with generic
> serialisation.

## Imports

### Internal (repo files)

- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 17, via relative)
- `from .ids import _normalise, canonical_json` -> [src/topo_pilot/contracts/ids.py](ids.py.md) (line 18, via relative)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 4)
- `abc` (lines 10)
- `collections` (lines 11)
- `dataclasses` (lines 6, 12)
- `hashlib` (lines 7)
- `types` (lines 8)
- `typing` (lines 9, 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/__init__.py](__init__.py.md) (line 7, import)
- [src/topo_pilot/contracts/_bundle.py](_bundle.py.md) (line 16, import)
- [src/topo_pilot/contracts/_schemas_data.py](_schemas_data.py.md) (line 12, import)
- [src/topo_pilot/contracts/_schemas_results.py](_schemas_results.py.md) (line 13, import)
- [src/topo_pilot/contracts/_schemas_world.py](_schemas_world.py.md) (line 12, import)
- [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 25, import)
- [src/topo_pilot/contracts/store.py](store.py.md) (line 16, import)
- [tools/x4_oracle_profile/inputs.py](../../../tools/x4_oracle_profile/inputs.py.md) (line 57, import)

## Top-level constants

- `A`
- `META_STATUSES`

## Classes and functions

- **class `ArtifactMeta`** [L26-60] decorators: @dataclass(frozen=True) - Envelope stored as ``meta.json`` next to every payload (DATA_SCHEMAS §1).
- **method `ArtifactMeta.to_json_dict`** [L49-51]: `def to_json_dict(self) -> dict[str, Any]` - Plain-JSON form for ``meta.json``.
- **method `ArtifactMeta.from_json_dict`** [L54-60]: `def from_json_dict(cls, data: Mapping[str, Any]) -> ArtifactMeta` decorators: @classmethod - Inverse of :meth:`to_json_dict`; unknown keys are ignored (forward compatibility).
- **function `_coerce`** [L63-96]: `def _coerce(value: Any, hint: Any) -> Any` - Convert a JSON-decoded value back to the type named by a dataclass field hint.
- **class `Artifact(ABC)`** [L99-157] - Base of every typed artifact (each subclass is a frozen dataclass).
- **method `Artifact.validate`** [L119-120]: `def validate(self) -> None` - Check every invariant of this artifact. Raises ``StageFailure``.
- **method `Artifact._fail`** [L122-123]: `def _fail(self, code: ErrorCode, check: str, detail: str) -> StageFailure`
- **method `Artifact.to_payload`** [L125-142]: `def to_payload(self) -> tuple[dict[str, np.ndarray | bytes], dict[str, Any]]` - Split the artifact into ``(arrays, extra)``; blob fields appear in ``arrays`` as
- **method `Artifact.from_payload`** [L145-157]: `def from_payload(cls: type[A], arrays: Mapping[str, np.ndarray | bytes], extra: Mapping[str, Any]) -> A` decorators: @classmethod - Inverse of :meth:`to_payload`.
- **function `array_field`** [L160-162]: `def array_field() -> Any` - A dataclass field holding an array (excluded from ``__eq__``/``__repr__``).
- **function `optional_array_field`** [L165-167]: `def optional_array_field() -> Any` - An optional array field defaulting to ``None``.
- **function `payload_checksum`** [L170-185]: `def payload_checksum(arrays: Mapping[str, np.ndarray | bytes], extra: Mapping[str, Any]) -> str` - Canonical content checksum: sha256 over, for each array or blob in name order, its name,

