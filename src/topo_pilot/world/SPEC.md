# SPEC: `world` (wave W1, critical, independent tests)

## Purpose

Builds latent worlds:
- states;
- the cubical complex that **defines the surface** (not just the transition graph);
- identifications (gluings);
- metrics;
- exact homology over GF(p).

It knows nothing about symbols, sequences, or models.

## Public API

```python
@dataclass(frozen=True)
class WorldConfig:
    family: str                     # registry key: "square" | "cylinder" (core); extensions add more
    dims: tuple[int, ...] = (12, 12)
    metric: Literal["flat", "graph"] = "flat"
    params: Mapping[str, Any] = field(default_factory=dict)   # family-specific (e.g. cube size)

class CubicalComplex:
    """Cells of dim 0..3 as ordered vertex tuples (k-cube has 2**k vertices, local lexicographic order)."""
    def __init__(self, n_vertices: int, cells: Mapping[int, np.ndarray]): ...
    def boundary_matrix(self, k: int) -> scipy.sparse.csr_matrix: ...   # integer signs, shape [n_{k-1}, n_k]
    def betti(self, p: int = 2) -> tuple[int, ...]: ...                   # ranks over GF(p), p prime
    def euler_characteristic(self) -> int: ...
    def one_skeleton(self) -> np.ndarray: ...                             # int32[E,2], canonical (lo,hi)

@dataclass(frozen=True)
class Identification:
    """Gluing rule for a lattice axis: kind in {'none','periodic','flipped'}; for 'flipped' the
    listed other axis is reversed when crossing (Möbius/Klein)."""
    axis: int; kind: Literal["none", "periodic", "flipped"]; flip_axis: int | None = None

class Metric(ABC):
    name: ClassVar[str]
    @abstractmethod
    def pairwise(self, coords: np.ndarray, complex_: CubicalComplex,
                 identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray: ...
class FlatQuotientMetric(Metric): ...   # min Euclidean distance over deck-transformation lifts
class GraphGeodesicMetric(Metric): ...  # unit-length edges, scipy shortest paths

class WorldBuilder(ABC):
    family: ClassVar[str]
    expected_betti: ClassVar[Mapping[int, tuple[int, ...]]]   # keyed by field p
    @abstractmethod
    def build(self, cfg: WorldConfig) -> WorldSpec: ...

class QuotientLatticeBuilder(WorldBuilder):
    """Generic: product lattice + per-axis Identification; builds vertices, all k-cubes (k≤len(dims)),
    including cubes crossing seams, with consistent vertex order."""
class SquareBuilder(QuotientLatticeBuilder): family = "square"     # no identifications
class CylinderBuilder(QuotientLatticeBuilder): family = "cylinder" # axis 0 periodic

WORLD_REGISTRY: dict[str, type[WorldBuilder]]
def register_world(cls: type[WorldBuilder]) -> type[WorldBuilder]: ...  # decorator
def build_world(cfg: WorldConfig) -> WorldSpec: ...                     # registry dispatch + validation

class WorldStage:                       # the only I/O class
    def run(self, cfg: WorldConfig, store: ArtifactStore) -> str: ...   # returns artifact id
```

## Logic requirements

- **Vertices:** vertex `(x, y)` gets the id `x * dims[1] + y`. Coordinates are stored as floats.
- **Cells:** a k-cube is listed once, by its vertex tuple in local lexicographic order. Cubes crossing a periodic or flipped seam use the identified vertex ids.
- **Boundary signs:** the boundary uses the standard cubical signs relative to each cell's own vertex order. Edges are canonicalised to (lo, hi), and the sign is adjusted when the canonical order reverses the local order.
- **Homology:** β_k over GF(p) equals `n_k − rank_p ∂_k − rank_p ∂_{k+1}`. Implement modular rank by Gaussian elimination on dense `int64 mod p`; matrices are at most a few hundred square.
- **Flat metric:** take the minimum over images of the target point under the deck group, restricted to the 3^D neighbouring copies of the fundamental domain. Flipped axes apply the reflection. Validate that `dist ≤ dist_graph + 1e-9` and that `dist ≥ dist_graph / sqrt(D)`.
- **Core worlds:**
  - `square` uses `dims = (12, 12)` with no identifications;
  - `cylinder` makes axis 0 periodic;
  - expected β is (1,0,0) for the square and (1,1,0) for the cylinder, for p = 2 and p = 3.
- **Extension hooks:** extensions register new builders (e.g. Möbius, Klein, cube-surface, RP², torus3, union, connected-sum; see `docs/EXTENSIONS.md`). Only the registry and new files are added; existing classes are not edited.

## Invariants and errors

| Condition | Error |
|---|---|
| ∂_{k-1} ∂_k ≠ 0 over ℤ | `BETTI_MISMATCH` (detail: `boundary_not_closed`) |
| computed β ≠ expected β | `BETTI_MISMATCH` |
| a cell repeats a vertex, or a gluing is inconsistent | `INVALID_GLUE` |
| the metric is asymmetric, has a nonzero diagonal, or violates the triangle inequality (tolerance 1e-9) | `NON_METRIC` |

The graph must be connected, except for families that declare `disjoint = True`.

## Dependencies and forbidden information

numpy, scipy, and `contracts` only. **Must not** receive emissions, tokens, models, or results.

## Persisted

`WorldSpec` via `WorldStage`. The seed is `none`, because world building is deterministic.

## Done when

The TEST_PLAN passes, and the README Logic section explains the cubical boundary signs and the lift-based flat metric with a small worked example (n = 3).
