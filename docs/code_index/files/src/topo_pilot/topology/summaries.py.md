# `src/topo_pilot/topology/summaries.py`

- Source: [src/topo_pilot/topology/summaries.py](../../../../../../src/topo_pilot/topology/summaries.py)
- Kind: python
- Lines: 53

## Module docstring

> Pure summary functions on persistence diagrams.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 5, 6)

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

- [src/topo_pilot/topology/__init__.py](__init__.py.md) (line 8, import)

## Top-level constants

- none

## Classes and functions

- **function `_bars`** [L9-12]: `def _bars(diag, dim: int, finite_only: bool = True) -> NDArray[np.float64]`
- **class `Summaries`** [L15-53] - Summaries of a ``DiagramResult`` (or an ``[n, 4]`` rows array); all are pure.
- **method `Summaries.S`** [L27-32]: `def S(diag, dim: int, scale_s: float) -> float` decorators: @staticmethod - Max finite persistence in ``dim`` divided by ``scale_s``; 0.0 if none or ``s <= 0``.
- **method `Summaries.pi_max`** [L35-39]: `def pi_max(diag, dim: int) -> float` decorators: @staticmethod - Max death/birth over finite bars with birth > 0 (bars born at 0 ignored); 0.0 if none.
- **method `Summaries.top_k_persistence`** [L42-46]: `def top_k_persistence(diag, dim: int, k: int = 3) -> NDArray[np.float64]` decorators: @staticmethod - The ``k`` largest finite persistences in ``dim``, decreasing, zero padded to ``[k]``.
- **method `Summaries.betti_curve`** [L49-53]: `def betti_curve(diag, dim: int, grid: NDArray[np.float64]) -> NDArray[np.float64]` decorators: @staticmethod - Number of ``dim``-bars alive at each ``t`` in ``grid`` (birth <= t < death), float64.

