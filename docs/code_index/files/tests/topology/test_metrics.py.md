# `tests/topology/test_metrics.py`

- Source: [tests/topology/test_metrics.py](../../../../../tests/topology/test_metrics.py)
- Kind: python
- Lines: 94

## Module docstring

> T01, T02: metric hand values, metric axioms, error paths.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.topology import METRIC_REGISTRY, Chord, Euclidean, Hellinger, SqrtJS` -> [src/topo_pilot/topology/__init__.py](../../src/topo_pilot/topology/__init__.py.md) (line 8, via package root)

### External (third-party)

- `numpy` (lines 4)
- `pytest` (lines 5)

### Standard library

- `math` (lines 2)

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

- `R2`
- `X3`

## Classes and functions

- **test `test_registry_names`** [L17-21]: `def test_registry_names()`
- **test `test_euclidean_hand_values`** [L24-30]: `def test_euclidean_hand_values()`
- **test `test_chord_hand_values`** [L33-42]: `def test_chord_hand_values()`
- **test `test_hellinger_hand_values`** [L45-51]: `def test_hellinger_hand_values()`
- **test `test_sqrt_js_hand_values`** [L54-61]: `def test_sqrt_js_hand_values()`
- **test `test_metric_axioms_random`** [L65-77]: `def test_metric_axioms_random(cls)` decorators: @pytest.mark.parametrize('cls', [Euclidean, Chord, Hellinger, SqrtJS])
- **test `test_nondistribution_raises`** [L81-87]: `def test_nondistribution_raises(cls)` decorators: @pytest.mark.parametrize('cls', [Hellinger, SqrtJS])
- **test `test_chord_zero_row_raises`** [L90-94]: `def test_chord_zero_row_raises()`

