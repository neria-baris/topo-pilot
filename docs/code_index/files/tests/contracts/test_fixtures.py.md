# `tests/contracts/test_fixtures.py`

- Source: [tests/contracts/test_fixtures.py](../../../../../tests/contracts/test_fixtures.py)
- Kind: python
- Lines: 70

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 5, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 6, via package root)

### External (third-party)

- `numpy` (lines 1)
- `pytest` (lines 2)

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

- **test `test_C14_tiny_world_spec_valid_and_counts`** [L15-23]: `def test_C14_tiny_world_spec_valid_and_counts(family, n, vef, betti)` decorators: @pytest.mark.parametrize('family,n,vef,betti', [('square', 3, (9, 12, 4), (1, 0, 0)), ('cylinder', 3, (9, 15, 6), (1, 1, 0))])
- **test `test_C14_tiny_world_spec_deterministic_and_sizes`** [L26-35]: `def test_C14_tiny_world_spec_deterministic_and_sizes()`
- **test `test_C14_tiny_hmm_is_a_valid_hmm`** [L38-48]: `def test_C14_tiny_hmm_is_a_valid_hmm()`
- **test `test_C14_tiny_observations_valid_and_deterministic`** [L51-61]: `def test_C14_tiny_observations_valid_and_deterministic()`
- **test `test_C14_memory_store_is_fresh_and_works`** [L64-70]: `def test_C14_memory_store_is_fresh_and_works()`

