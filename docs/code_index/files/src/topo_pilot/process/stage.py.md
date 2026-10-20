# `src/topo_pilot/process/stage.py`

- Source: [src/topo_pilot/process/stage.py](../../../../../../src/topo_pilot/process/stage.py)
- Kind: python
- Lines: 65

## Module docstring

> ProcessStage: the single place where the process module touches the artifact store.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, SeedTree, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)
- `from ._geometry import fail` -> [src/topo_pilot/process/_geometry.py](_geometry.py.md) (line 11, via relative)
- `from .conductance import ConductanceConfig, conductance_kernel` -> [src/topo_pilot/process/conductance.py](conductance.py.md) (line 12, via relative)
- `from .emission import EMISSION_REGISTRY, WORLD_SCOPE_MASTER, EmissionConfig` -> [src/topo_pilot/process/emission.py](emission.py.md) (line 13, via relative)
- `from .transition import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/transition.py](transition.py.md) (line 14, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 6)
- `logging` (lines 5)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/process/__init__.py](__init__.py.md) (line 15, import)

## Top-level constants

- `CONSUMER`
- `_WORLD_SCOPED_MODES`

## Classes and functions

- **class `ProcessStage`** [L21-65] - Loads a stored world, builds a spec, stores it with the world as parent.
- **method `ProcessStage.run_transition`** [L24-31]: `def run_transition(self, world_id: str, cfg: TransitionConfig, store: ArtifactStore) -> str` - Build and save the ``TransitionSpec`` of ``world_id``; returns its artifact id.
- **method `ProcessStage.run_conductance_transition`** [L33-41]: `def run_conductance_transition(self, world_id: str, cfg: ConductanceConfig, store: ArtifactStore) -> str` - Build and save the metric-conductance ``TransitionSpec`` of ``world_id`` (X5 G1); the
- **method `ProcessStage.run_emission`** [L43-65]: `def run_emission(self, world_id: str, cfg: EmissionConfig, seeds: SeedTree, store: ArtifactStore) -> str` - Build and save the ``EmissionSpec`` of ``world_id`` for replicate ``seeds.master``.

