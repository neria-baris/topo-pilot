# `src/topo_pilot/topology/distance.py`

- Source: [src/topo_pilot/topology/distance.py](../../../../../../src/topo_pilot/topology/distance.py)
- Kind: python
- Lines: 126

## Module docstring

> Distance pipeline: optional PCA, pairwise metric, deduplication, scale ``s``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, Status` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)
- `from .metrics import DistanceMetric` -> [src/topo_pilot/topology/metrics.py](metrics.py.md) (line 13, via relative)

### External (third-party)

- `numpy` (lines 8, 9)

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

- [src/topo_pilot/topology/__init__.py](__init__.py.md) (line 4, import)

## Top-level constants

- `DEDUP_TOL`

## Classes and functions

- **class `DistanceResult`** [L19-37] decorators: @dataclass(frozen=True, eq=False) - Deduplicated distance matrix (pure result; persisted later as ``DistanceArtifact``).
- **function `scale_of`** [L40-44]: `def scale_of(D: NDArray[np.float64]) -> float` - 95th percentile (linear interpolation) of the positive upper-triangle distances.
- **function `deduplicate`** [L47-63]: `def deduplicate(D: NDArray[np.float64]) -> tuple[NDArray[np.int64], NDArray[np.int64]]` - Merge points at distance <= 1e-12 (first occurrence is the representative).
- **class `DistancePipeline`** [L66-126] - ``X -> (optional PCA) -> metric -> dedup -> DistanceResult``.
- **method `DistancePipeline.__init__`** [L85-89]: `def __init__(self, metric: DistanceMetric, pca_dims: int | None = None)`
- **method `DistancePipeline.fit_pca`** [L91-102]: `def fit_pca(self, X_fit: NDArray[np.float64]) -> 'DistancePipeline'` - Fit PCA on ``X_fit`` (the caller passes dev data only). No-op if ``pca_dims`` is None.
- **method `DistancePipeline._project`** [L104-113]: `def _project(self, X: NDArray[np.float64]) -> NDArray[np.float64]`
- **method `DistancePipeline.compute`** [L115-126]: `def compute(self, X: NDArray[np.float64], ids: Sequence[str]) -> DistanceResult` - Return the deduplicated distance matrix, ids, dedup map, scale and status.

