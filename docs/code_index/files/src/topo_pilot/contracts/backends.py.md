# `src/topo_pilot/contracts/backends.py`

- Source: [src/topo_pilot/contracts/backends.py](../../../../../../src/topo_pilot/contracts/backends.py)
- Kind: python
- Lines: 129

## Module docstring

> Bytes-level storage backends for the artifact store.

## Imports

### Internal (repo files)

- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 10, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `abc` (lines 7)
- `os` (lines 5)
- `pathlib` (lines 8)
- `tempfile` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/__init__.py](__init__.py.md) (line 6, import)
- [src/topo_pilot/contracts/store.py](store.py.md) (line 15, import)
- [src/topo_pilot/contracts/testing.py](testing.py.md) (line 12, import)
- [tests/k4b/test_b_registry.py](../../../tests/k4b/test_b_registry.py.md) (line 279, import)
- [tools/c1prime/c1_driver_cal.py](../../../tools/c1prime/c1_driver_cal.py.md) (line 28, import)
- [tools/c1prime_registry/c1_registry_sources.py](../../../tools/c1prime_registry/c1_registry_sources.py.md) (line 54, import)
- [tools/chart_diag/chart_diag.py](../../../tools/chart_diag/chart_diag.py.md) (line 130, import)
- [tools/d2a/d2a_world.py](../../../tools/d2a/d2a_world.py.md) (line 182, import)
- [tools/k4b/k4b_driver.py](../../../tools/k4b/k4b_driver.py.md) (line 139, import)
- [tools/k4b/k4b_registry.py](../../../tools/k4b/k4b_registry.py.md) (line 191, import)
- [tools/k4b/k4b_registry.py](../../../tools/k4b/k4b_registry.py.md) (line 243, import)
- [tools/k4b/k4b_registry.py](../../../tools/k4b/k4b_registry.py.md) (line 301, import)
- [tools/x4_circle_history/live_context.py](../../../tools/x4_circle_history/live_context.py.md) (line 110, import)
- [tools/x6_stage1/x6s1_stage_pre.py](../../../tools/x6_stage1/x6s1_stage_pre.py.md) (line 38, import)

## Top-level constants

- none

## Classes and functions

- **function `_check_key`** [L13-18]: `def _check_key(key: str) -> str`
- **class `ArtifactBackend(ABC)`** [L21-44] - Flat key -> bytes storage. Keys are relative POSIX paths such as
- **method `ArtifactBackend.put`** [L26-28]: `def put(self, key: str, data: bytes) -> None` decorators: @abstractmethod - Store ``data`` under ``key``, replacing any value (atomically where the medium
- **method `ArtifactBackend.get`** [L31-32]: `def get(self, key: str) -> bytes` decorators: @abstractmethod - Return the bytes at ``key``; raises ``ARTIFACT_MISSING`` if absent.
- **method `ArtifactBackend.exists`** [L35-36]: `def exists(self, key: str) -> bool` decorators: @abstractmethod - True if ``key`` holds a value.
- **method `ArtifactBackend.list`** [L39-40]: `def list(self, prefix: str) -> list[str]` decorators: @abstractmethod - All keys starting with ``prefix``, sorted.
- **method `ArtifactBackend._missing`** [L42-44]: `def _missing(self, key: str) -> StageFailure`
- **class `MemoryBackend(ArtifactBackend)`** [L47-66] - In-process dictionary backend for tests (``contracts.testing.memory_store``).
- **method `MemoryBackend.__init__`** [L50-51]: `def __init__(self) -> None`
- **method `MemoryBackend.put`** [L53-54]: `def put(self, key: str, data: bytes) -> None`
- **method `MemoryBackend.get`** [L56-60]: `def get(self, key: str) -> bytes`
- **method `MemoryBackend.exists`** [L62-63]: `def exists(self, key: str) -> bool`
- **method `MemoryBackend.list`** [L65-66]: `def list(self, prefix: str) -> list[str]`
- **class `LocalFSBackend(ArtifactBackend)`** [L69-105] - Files under ``root``; writes go to a temporary file and are moved into place atomically.
- **method `LocalFSBackend.__init__`** [L72-73]: `def __init__(self, root: Path) -> None`
- **method `LocalFSBackend._path`** [L75-76]: `def _path(self, key: str) -> Path`
- **method `LocalFSBackend.put`** [L78-88]: `def put(self, key: str, data: bytes) -> None`
- **method `LocalFSBackend.get`** [L90-94]: `def get(self, key: str) -> bytes`
- **method `LocalFSBackend.exists`** [L96-97]: `def exists(self, key: str) -> bool`
- **method `LocalFSBackend.list`** [L99-105]: `def list(self, prefix: str) -> list[str]`
- **class `MirrorBackend(ArtifactBackend)`** [L108-129] - Writes to ``primary`` and to a ``LocalFSBackend`` at ``mirror_root`` (e.g. an external
- **method `MirrorBackend.__init__`** [L112-114]: `def __init__(self, primary: ArtifactBackend, mirror_root: Path) -> None`
- **method `MirrorBackend.put`** [L116-118]: `def put(self, key: str, data: bytes) -> None`
- **method `MirrorBackend.get`** [L120-123]: `def get(self, key: str) -> bytes`
- **method `MirrorBackend.exists`** [L125-126]: `def exists(self, key: str) -> bool`
- **method `MirrorBackend.list`** [L128-129]: `def list(self, prefix: str) -> list[str]`

