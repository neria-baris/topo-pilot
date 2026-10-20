# `src/topo_pilot/world/metrics.py`

- Source: [src/topo_pilot/world/metrics.py](../../../../../../src/topo_pilot/world/metrics.py)
- Kind: python
- Lines: 143

## Module docstring

> Metrics on a world: flat quotient metric (deck-transformation lifts) and graph geodesic.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)
- `from .complex import CubicalComplex` -> [src/topo_pilot/world/complex.py](complex.py.md) (line 16, via relative)
- `from .identification import Identification` -> [src/topo_pilot/world/identification.py](identification.py.md) (line 17, via relative)

### External (third-party)

- `numpy` (lines 9)
- `scipy` (lines 10, 11, 12)

### Standard library

- `__future__` (lines 3)
- `abc` (lines 6)
- `itertools` (lines 5)
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

- [src/topo_pilot/world/__init__.py](__init__.py.md) (line 7, import)
- [src/topo_pilot/world/lattice.py](lattice.py.md) (line 15, import)
- [src/topo_pilot/world/registry.py](registry.py.md) (line 12, import)
- [tools/d1_seam/d1_seam.py](../../../tools/d1_seam/d1_seam.py.md) (line 21, import)
- [tools/x2a_stage0/x2a_model.py](../../../tools/x2a_stage0/x2a_model.py.md) (line 28, import)
- [tools/x6_stage0/x6_model.py](../../../tools/x6_stage0/x6_model.py.md) (line 26, import)

## Top-level constants

- `METRICS`

## Classes and functions

- **class `Metric(ABC)`** [L20-33] - Pairwise distance on the vertices of a world.
- **method `Metric.pairwise`** [L31-33]: `def pairwise(self, coords: np.ndarray, complex_: CubicalComplex, identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray` decorators: @abstractmethod - Return the symmetric ``[N, N]`` distance matrix.
- **function `_generators`** [L36-53]: `def _generators(identifications: Sequence[Identification], dims: tuple[int, ...]) -> list[tuple[np.ndarray, np.ndarray]]` - Deck generators as affine maps ``x -> a * x + b`` (``a`` a +-1 vector), one per glued axis.
- **function `_deck_elements`** [L56-68]: `def _deck_elements(gens: list[tuple[np.ndarray, np.ndarray]], n_dim: int) -> list[tuple[np.ndarray, np.ndarray]]` - All products ``g_1^{m_1} ... g_r^{m_r}``, ``m_i in {-1, 0, 1}`` (3^r copies).
- **class `FlatQuotientMetric(Metric)`** [L71-98] - Minimum Euclidean distance over deck-transformation lifts.
- **method `FlatQuotientMetric.pairwise`** [L89-98]: `def pairwise(self, coords: np.ndarray, complex_: CubicalComplex, identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray`
- **class `GraphGeodesicMetric(Metric)`** [L101-125] - Unit-length-edge shortest-path distance on the 1-skeleton.
- **method `GraphGeodesicMetric.pairwise`** [L116-125]: `def pairwise(self, coords: np.ndarray, complex_: CubicalComplex, identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray`
- **function `check_flat_bounds`** [L132-143]: `def check_flat_bounds(dist: np.ndarray, dist_graph: np.ndarray, n_axes: int, tol: float = 1e-09) -> None` - Require ``dist <= dist_graph + tol`` and ``dist >= dist_graph / sqrt(D)``.

