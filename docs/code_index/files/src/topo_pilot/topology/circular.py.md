# `src/topo_pilot/topology/circular.py`

- Source: [src/topo_pilot/topology/circular.py](../../../../../../src/topo_pilot/topology/circular.py)
- Kind: python
- Lines: 87

## Module docstring

> Circular coordinates (de Silva, Morozov, Vejdemo-Johansson) from the top H1 cocycle.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 5, 7)
- `ripser` (lines 6)
- `scipy` (lines 8)

### Standard library

- `__future__` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/topology/__init__.py](__init__.py.md) (line 3, import)

## Top-level constants

- `_COMPONENT`
- `_LIFETIME_FRACTION`

## Classes and functions

- **class `CircularCoordinates`** [L16-87] - Angles on S^1 from the cocycle of the most persistent H1 class.
- **method `CircularCoordinates.__init__`** [L43-47]: `def __init__(self, coeff_p: int = 47)`
- **method `CircularCoordinates._top_cocycle`** [L49-57]: `def _top_cocycle(self, D: NDArray[np.float64])`
- **method `CircularCoordinates.fit_transform`** [L59-87]: `def fit_transform(self, D: NDArray[np.float64]) -> NDArray[np.float64]` - Return circular coordinates ``[M]`` in ``[0, 2 pi)`` for the distance matrix ``D``.

