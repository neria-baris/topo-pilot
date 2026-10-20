# `tests/topology/test_shapes_calibration.py`

- Source: [tests/topology/test_shapes_calibration.py](../../../../../tests/topology/test_shapes_calibration.py)
- Kind: python
- Lines: 87

## Module docstring

> T06, T07, T11 (gate G-A), plus shape / null-cloud contracts.

## Imports

### Internal (repo files)

- `from topo_pilot.topology import DistancePipeline, Euclidean, NullClouds, PersistenceComputer, PHConfig, Summaries, SyntheticShapes` -> [src/topo_pilot/topology/__init__.py](../../src/topo_pilot/topology/__init__.py.md) (line 5, via package root)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)

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

- none

## Top-level constants

- none

## Classes and functions

- **function `s_of`** [L18-22]: `def s_of(X)` - H1 signal S of a point cloud under the Euclidean pipeline.
- **test `test_shape_generators_contract`** [L25-35]: `def test_shape_generators_contract()`
- **test `test_null_clouds_contract`** [L38-46]: `def test_null_clouds_contract()`
- **test `test_T06_circle_above_gaussian_floor`** [L49-54]: `def test_T06_circle_above_gaussian_floor()`
- **test `test_T07_disk_and_gaussian_below_threshold`** [L57-75]: `def test_T07_disk_and_gaussian_below_threshold()`
- **test `test_T11_gate_GA_circle_vs_disk`** [L79-87]: `def test_T11_gate_GA_circle_vs_disk()` decorators: @pytest.mark.slow

