# `tests/process/test_geometry.py`

- Source: [tests/process/test_geometry.py](../../../../../tests/process/test_geometry.py)
- Kind: python
- Lines: 46

## Module docstring

> P13: x-periodicity is read from the world's complex, not from its family name.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.process._geometry import is_x_periodic, point_distances` -> [src/topo_pilot/process/_geometry.py](../../src/topo_pilot/process/_geometry.py.md) (line 11, via package root)

### External (third-party)

- `numpy` (lines 7)
- `pytest` (lines 8)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **test `test_P13_core_worlds`** [L16-18]: `def test_P13_core_worlds(square12, cylinder12, square3, cylinder3)`
- **test `test_P13_family_name_is_ignored`** [L21-28]: `def test_P13_family_name_is_ignored(square12, cylinder12)`
- **test `test_P13_flipped_wrap_is_not_periodic`** [L31-36]: `def test_P13_flipped_wrap_is_not_periodic(square12)` - Möbius-style crossed wrap edges (11, y) ~ (0, 11 - y) do not make axis 0 periodic.
- **test `test_P13_partial_or_declared_without_edges_raises`** [L39-46]: `def test_P13_partial_or_declared_without_edges_raises(square12, cylinder12)`

