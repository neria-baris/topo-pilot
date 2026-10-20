# `src/topo_pilot/contracts/ids.py`

- Source: [src/topo_pilot/contracts/ids.py](../../../../../../src/topo_pilot/contracts/ids.py)
- Kind: python
- Lines: 134

## Module docstring

> Canonical JSON, content-addressed artifact ids, history ids, and the seed tree.

## Imports

### Internal (repo files)

- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 15, via relative)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 9)
- `dataclasses` (lines 5)
- `enum` (lines 10)
- `hashlib` (lines 6)
- `json` (lines 7)
- `math` (lines 8)
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

- [src/topo_pilot/contracts/__init__.py](__init__.py.md) (line 9, import)
- [src/topo_pilot/contracts/_bundle.py](_bundle.py.md) (line 18, import)
- [src/topo_pilot/contracts/_schemas_data.py](_schemas_data.py.md) (line 14, import)
- [src/topo_pilot/contracts/base.py](base.py.md) (line 18, import)
- [src/topo_pilot/contracts/store.py](store.py.md) (line 18, import)
- [src/topo_pilot/contracts/testing.py](testing.py.md) (line 14, import)

## Top-level constants

- `SCHEMA_VERSION`
- `_MASK_63`

## Classes and functions

- **function `_normalise`** [L22-47]: `def _normalise(obj: Any) -> Any` - Map ``obj`` to plain JSON types (dict with str keys, list, str, int, float, bool, None).
- **function `canonical_json`** [L50-70]: `def canonical_json(obj: Any) -> str` - Serialise ``obj`` to a canonical JSON string.
- **function `make_artifact_id`** [L73-84]: `def make_artifact_id(artifact_type: str, config: Mapping[str, Any], parent_ids: Sequence[str], schema_version: str = SCHEMA_VERSION) -> str` - Content address of an artifact.
- **function `tokens_hash`** [L87-90]: `def tokens_hash(history: np.ndarray) -> str` - Hash of a token history ``w_1..w_p``: ``sha1(int64 little-endian bytes)[:16]``.
- **function `make_history_id`** [L93-96]: `def make_history_id(dataset_id: str, sequence_id: int, end: int, history_hash: str) -> str` - History id: ``sha1(f"{dataset_id}|{sequence_id}|{end}|{history_hash}")[:16]``.
- **class `SeedTree`** [L99-134] - Deterministic, platform-independent seed derivation (the only source of randomness).
- **method `SeedTree.__init__`** [L115-120]: `def __init__(self, master: int) -> None`
- **method `SeedTree.seed`** [L122-127]: `def seed(self, name: str, *scope: str | int) -> int` - Derived 63-bit seed for ``(master, name, *scope)``; identical on every OS.
- **method `SeedTree.generator`** [L129-131]: `def generator(self, name: str, *scope: str | int) -> np.random.Generator` - A fresh ``np.random.Generator(PCG64(seed(name, *scope)))``.
- **method `SeedTree.__repr__`** [L133-134]: `def __repr__(self) -> str`

