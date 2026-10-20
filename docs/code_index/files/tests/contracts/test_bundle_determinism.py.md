# `tests/contracts/test_bundle_determinism.py`

- Source: [tests/contracts/test_bundle_determinism.py](../../../../../tests/contracts/test_bundle_determinism.py)
- Kind: python
- Lines: 15

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.contracts.testing import memory_store, tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 3, via package root)

### External (third-party)

- `pytest` (lines 1)

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

- **test `test_C12b_bundle_bytes_are_deterministic`** [L8-15]: `def test_C12b_bundle_bytes_are_deterministic(tmp_path)` - Equal content exported twice (to different file names) gives byte-identical bundles.

