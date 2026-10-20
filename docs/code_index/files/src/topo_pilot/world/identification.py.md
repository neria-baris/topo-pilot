# `src/topo_pilot/world/identification.py`

- Source: [src/topo_pilot/world/identification.py](../../../../../../src/topo_pilot/world/identification.py)
- Kind: python
- Lines: 27

## Module docstring

> Gluing rule for one lattice axis.

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)
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

- [src/topo_pilot/world/__init__.py](__init__.py.md) (line 5, import)
- [src/topo_pilot/world/lattice.py](lattice.py.md) (line 14, import)
- [src/topo_pilot/world/metrics.py](metrics.py.md) (line 17, import)

## Top-level constants

- none

## Classes and functions

- **class `Identification`** [L10-27] decorators: @dataclass(frozen=True) - Gluing rule for a lattice axis: kind in {'none','periodic','flipped'}; for 'flipped' the

