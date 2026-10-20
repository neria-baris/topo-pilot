# `src/topo_pilot/world/stage.py`

- Source: [src/topo_pilot/world/stage.py](../../../../../../src/topo_pilot/world/stage.py)
- Kind: python
- Lines: 37

## Module docstring

> The only I/O class of `world`: builds a WorldSpec and saves it to the artifact store.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)
- `from .config import WorldConfig` -> [src/topo_pilot/world/config.py](config.py.md) (line 10, via relative)
- `from .registry import build_world` -> [src/topo_pilot/world/registry.py](registry.py.md) (line 11, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 6)
- `logging` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/world/__init__.py](__init__.py.md) (line 9, import)

## Top-level constants

- `_LOG`

## Classes and functions

- **class `WorldStage`** [L16-37] - Build and persist a world (deterministic; no RNG, empty seed map, no parents).
- **method `WorldStage.run`** [L19-37]: `def run(self, cfg: WorldConfig, store: ArtifactStore) -> str` - Build ``cfg``, save the :class:`WorldSpec` and return its artifact id.

