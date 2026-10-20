# `tests/topology/test_circular_pca.py`

- Source: [tests/topology/test_circular_pca.py](../../../../../tests/topology/test_circular_pca.py)
- Kind: python
- Lines: 55

## Module docstring

> T12 (circular coordinates), T13 (PCA contract).

## Imports

### Internal (repo files)

- `from topo_pilot.topology import CircularCoordinates, DistancePipeline, Euclidean` -> [src/topo_pilot/topology/__init__.py](../../src/topo_pilot/topology/__init__.py.md) (line 6, via package root)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)
- `scipy` (lines 4)

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

- **function `circular_agreement`** [L11-13]: `def circular_agreement(a, b)` - Resultant length of (a -+ b): 1 means equal up to rotation, sign allowed.
- **test `test_T12_circular_coordinates_recover_angle`** [L17-27]: `def test_T12_circular_coordinates_recover_angle()` decorators: @pytest.mark.slow
- **test `test_T13_pca_fit_on_one_set_applied_to_another`** [L30-49]: `def test_T13_pca_fit_on_one_set_applied_to_another()`
- **test `test_T13_pca_none_is_noop`** [L52-55]: `def test_T13_pca_none_is_noop()`

