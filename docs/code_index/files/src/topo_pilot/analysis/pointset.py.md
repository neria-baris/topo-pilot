# `src/topo_pilot/analysis/pointset.py`

- Source: [src/topo_pilot/analysis/pointset.py](../../../../../../src/topo_pilot/analysis/pointset.py)
- Kind: python
- Lines: 112

## Module docstring

> PointSet value, id alignment check and the pure PH summary helper.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, Status` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.topology import DistanceMetric, DistancePipeline, Euclidean, Hellinger, PersistenceComputer, PHConfig, Summaries` -> [src/topo_pilot/topology/__init__.py](../topology/__init__.py.md) (line 11, via package root)

### External (third-party)

- `numpy` (lines 7, 8)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 29, import)
- [src/topo_pilot/analysis/discriminability.py](discriminability.py.md) (line 9, import)
- [src/topo_pilot/analysis/dynamics.py](dynamics.py.md) (line 11, import)
- [src/topo_pilot/analysis/readout.py](readout.py.md) (line 12, import)
- [src/topo_pilot/analysis/spaces.py](spaces.py.md) (line 24, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **class `PointSet`** [L25-44] decorators: @dataclass(frozen=True, eq=False) - A labelled point cloud in one comparison space.
- **function `require_same_ids`** [L47-52]: `def require_same_ids(a: PointSet, b: PointSet) -> None` - Raise ``SAMPLE_ID_MISMATCH`` unless both sets have the identical ordered id list.
- **function `_metric`** [L55-60]: `def _metric(name: str) -> DistanceMetric`
- **function `_dedup_given_D`** [L63-71]: `def _dedup_given_D(D: NDArray[np.float64]) -> NDArray[np.float64]` - Merge points at distance <= 1e-12 in a given D (first occurrence kept).
- **function `_scale`** [L74-77]: `def _scale(D: NDArray[np.float64]) -> float`
- **function `ph_summary`** [L80-112]: `def ph_summary(pointset: PointSet, maxdim: int = 1) -> dict` - Persistent-homology summary of one point set.

