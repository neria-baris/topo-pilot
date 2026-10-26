# `src/topo_pilot/process/centers.py`

- Source: [src/topo_pilot/process/centers.py](../../../../../../src/topo_pilot/process/centers.py)
- Kind: python
- Lines: 99

## Module docstring

> Center strategies for the overlap emission: where the V symbol centers sit in the chart.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from ._geometry import fail` -> [src/topo_pilot/process/_geometry.py](_geometry.py.md) (line 14, via relative)

### External (third-party)

- `numpy` (lines 9, 10)

### Standard library

- `__future__` (lines 3)
- `abc` (lines 6)
- `math` (lines 5)
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

- [src/topo_pilot/process/__init__.py](__init__.py.md) (line 3, import)
- [src/topo_pilot/process/emission.py](emission.py.md) (line 28, import)
- [tools/hws/hws_worlds.py](../../../tools/hws/hws_worlds.py.md) (line 31, import)

## Top-level constants

- `CENTER_REGISTRY`

## Classes and functions

- **function `check_centers_in_chart`** [L17-30]: `def check_centers_in_chart(world: WorldSpec, centers: NDArray[np.float64]) -> None` - Require every center to lie in the chart box ``[0, dims[k]-1]`` on each axis.
- **class `CenterStrategy(ABC)`** [L33-44] - Variation point: chooses ``n_centers`` points in the chart.
- **method `CenterStrategy.centers`** [L42-44]: `def centers(self, world: WorldSpec, n_centers: int, rng: np.random.Generator) -> NDArray[np.float64]` decorators: @abstractmethod - Return the ``[V, D]`` center coordinates.
- **class `GridCenters(CenterStrategy)`** [L47-68] - Core grid: ``c_ab = (0.5 + 2a, 0.5 + 2b)``, ``a, b in 0..sqrt(V)-1``, index ``j = a*k + b``.
- **method `GridCenters.centers`** [L59-68]: `def centers(self, world: WorldSpec, n_centers: int, rng: np.random.Generator) -> NDArray[np.float64]`
- **class `FPSCenters(CenterStrategy)`** [L71-96] - Farthest-point sampling on ``world.dist``; the centers are vertex coordinates.
- **method `FPSCenters.centers`** [L85-96]: `def centers(self, world: WorldSpec, n_centers: int, rng: np.random.Generator) -> NDArray[np.float64]`

