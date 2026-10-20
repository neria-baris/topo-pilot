# `src/topo_pilot/topology/__init__.py`

- Source: [src/topo_pilot/topology/__init__.py](../../../../../../src/topo_pilot/topology/__init__.py)
- Kind: python
- Lines: 14

## Module docstring

> Public API of `topo_pilot.topology` (see SPEC.md): distances and persistent homology.

## Imports

### Internal (repo files)

- `from .circular import CircularCoordinates` -> [src/topo_pilot/topology/circular.py](circular.py.md) (line 3, via relative)
- `from .distance import DistancePipeline, DistanceResult` -> [src/topo_pilot/topology/distance.py](distance.py.md) (line 4, via relative)
- `from .metrics import METRIC_REGISTRY, Chord, DistanceMetric, Euclidean, Hellinger, SqrtJS` -> [src/topo_pilot/topology/metrics.py](metrics.py.md) (line 5, via relative)
- `from .persistence import DiagramResult, PersistenceComputer, PHConfig` -> [src/topo_pilot/topology/persistence.py](persistence.py.md) (line 6, via relative)
- `from .shapes import NullClouds, SyntheticShapes` -> [src/topo_pilot/topology/shapes.py](shapes.py.md) (line 7, via relative)
- `from .summaries import Summaries` -> [src/topo_pilot/topology/summaries.py](summaries.py.md) (line 8, via relative)

### External (third-party)

- none

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/circular.py](../analysis/circular.py.md) (line 21, import)
- [src/topo_pilot/analysis/pointset.py](../analysis/pointset.py.md) (line 11, import)
- [src/topo_pilot/analysis/sensitivity.py](../analysis/sensitivity.py.md) (line 9, import)
- [src/topo_pilot/analysis/spaces.py](../analysis/spaces.py.md) (line 21, import)
- [src/topo_pilot/experiment/s1.py](../experiment/s1.py.md) (line 28, import)
- [tests/analysis/test_baselines_dynamics.py](../../../tests/analysis/test_baselines_dynamics.py.md) (line 8, import)
- [tests/topology/test_circular_pca.py](../../../tests/topology/test_circular_pca.py.md) (line 6, import)
- [tests/topology/test_metrics.py](../../../tests/topology/test_metrics.py.md) (line 8, import)
- [tests/topology/test_persistence.py](../../../tests/topology/test_persistence.py.md) (line 9, import)
- [tests/topology/test_shapes_calibration.py](../../../tests/topology/test_shapes_calibration.py.md) (line 5, import)
- [tools/x2a_stage0/x2a_ph.py](../../../tools/x2a_stage0/x2a_ph.py.md) (line 22, import)

## Top-level constants

- none

## Classes and functions

- none

