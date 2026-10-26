# `src/topo_pilot/world/registry.py`

- Source: [src/topo_pilot/world/registry.py](../../../../../../src/topo_pilot/world/registry.py)
- Kind: python
- Lines: 63

## Module docstring

> World builder ABC, registry, and the validated `build_world` entry point.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)
- `from .complex import CubicalComplex, check_boundary_closed` -> [src/topo_pilot/world/complex.py](complex.py.md) (line 10, via relative)
- `from .config import WorldConfig` -> [src/topo_pilot/world/config.py](config.py.md) (line 11, via relative)
- `from .metrics import check_flat_bounds` -> [src/topo_pilot/world/metrics.py](metrics.py.md) (line 12, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `abc` (lines 5)
- `typing` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/world/__init__.py](__init__.py.md) (line 8, import)
- [src/topo_pilot/world/lattice.py](lattice.py.md) (line 16, import)
- [src/topo_pilot/world/stage.py](stage.py.md) (line 11, import)
- [tests/hws/test_a_identities.py](../../../tests/hws/test_a_identities.py.md) (line 84, import)

## Top-level constants

- `WORLD_REGISTRY`

## Classes and functions

- **class `WorldBuilder(ABC)`** [L15-29] - Builds a :class:`WorldSpec` for one family.
- **method `WorldBuilder.build`** [L28-29]: `def build(self, cfg: WorldConfig) -> WorldSpec` decorators: @abstractmethod - Return the world for ``cfg`` (deterministic; no RNG).
- **function `register_world`** [L35-38]: `def register_world(cls: type[WorldBuilder]) -> type[WorldBuilder]` - Class decorator registering ``cls`` under ``cls.family``; returns ``cls``.
- **function `build_world`** [L41-63]: `def build_world(cfg: WorldConfig) -> WorldSpec` - Registry dispatch followed by full validation.

