# `src/topo_pilot/world/lattice.py`

- Source: [src/topo_pilot/world/lattice.py](../../../../../../src/topo_pilot/world/lattice.py)
- Kind: python
- Lines: 178

## Module docstring

> Quotient-lattice world builder: product lattice + per-axis gluings (square, cylinder).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from .complex import CubicalComplex, check_boundary_closed` -> [src/topo_pilot/world/complex.py](complex.py.md) (line 12, via relative)
- `from .config import WorldConfig` -> [src/topo_pilot/world/config.py](config.py.md) (line 13, via relative)
- `from .identification import Identification` -> [src/topo_pilot/world/identification.py](identification.py.md) (line 14, via relative)
- `from .metrics import METRICS, GraphGeodesicMetric` -> [src/topo_pilot/world/metrics.py](metrics.py.md) (line 15, via relative)
- `from .registry import WorldBuilder, register_world` -> [src/topo_pilot/world/registry.py](registry.py.md) (line 16, via relative)

### External (third-party)

- `numpy` (lines 8)

### Standard library

- `__future__` (lines 3)
- `itertools` (lines 5)
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

- [src/topo_pilot/world/__init__.py](__init__.py.md) (line 6, import)

## Top-level constants

- `_AXIS_NAMES`
- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L22-23]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `_check_identifications`** [L26-43]: `def _check_identifications(idents: Sequence[Identification], dims: tuple[int, ...]) -> None`
- **function `_wrap`** [L46-63]: `def _wrap(corner: list[int], idents: Sequence[Identification], dims: tuple[int, ...]) -> list[int]` - Map a lattice corner (coordinates may equal ``n_a``) to its representative vertex.
- **function `lattice_cells`** [L66-101]: `def lattice_cells(dims: tuple[int, ...], idents: Sequence[Identification]) -> dict[int, np.ndarray]` - All k-cubes of the glued lattice, ``k = 0..len(dims)``, as local-lexicographic tuples.
- **function `describe_identifications`** [L104-112]: `def describe_identifications(idents: Sequence[Identification]) -> tuple[str, ...]` - Human-readable gluing strings, e.g. ``'x periodic'``, ``'x flipped(y)'``.
- **class `QuotientLatticeBuilder(WorldBuilder)`** [L115-161] - Generic: product lattice + per-axis Identification; builds vertices and all k-cubes
- **method `QuotientLatticeBuilder.build`** [L138-161]: `def build(self, cfg: WorldConfig) -> WorldSpec`
- **class `SquareBuilder(QuotientLatticeBuilder)`** [L165-169] decorators: @register_world - Plain grid, no identifications: contractible, beta = (1, 0, 0), chi = 1.
- **class `CylinderBuilder(QuotientLatticeBuilder)`** [L173-178] decorators: @register_world - Axis 0 periodic: beta = (1, 1, 0), chi = 0.

