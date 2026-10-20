# `src/topo_pilot/analysis/discriminability.py`

- Source: [src/topo_pilot/analysis/discriminability.py](../../../../../../src/topo_pilot/analysis/discriminability.py)
- Kind: python
- Lines: 68

## Module docstring

> DiscriminabilityTable: S for every reference space (stage S2).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 7, via package root)
- `from .pointset import PointSet, ph_summary` -> [src/topo_pilot/analysis/pointset.py](pointset.py.md) (line 9, via relative)
- `from .spaces import SpaceBuilder` -> [src/topo_pilot/analysis/spaces.py](spaces.py.md) (line 10, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `typing` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 6, import)

## Top-level constants

- `_RUN_ID`

## Classes and functions

- **class `DiscriminabilityTable`** [L15-68] - Compute S (H1 signal) and the scale s for world, emission, beliefs and futures.
- **method `DiscriminabilityTable.__init__`** [L36-37]: `def __init__(self, store: ArtifactStore)`
- **method `DiscriminabilityTable._rows`** [L40-46]: `def _rows(ps: PointSet, world: str, condition: str | None, panel: int | None, parents: tuple[str, ...]) -> list[MetricRow]` decorators: @staticmethod
- **method `DiscriminabilityTable.compute`** [L48-68]: `def compute(self, refs: Mapping[tuple[str, str], Mapping[str, str]], panels: Sequence[int]) -> MetricRecords` - Build the table (see class docstring); never saves.

