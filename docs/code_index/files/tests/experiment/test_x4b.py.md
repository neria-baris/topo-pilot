# `tests/experiment/test_x4b.py`

- Source: [tests/experiment/test_x4b.py](../../../../../tests/experiment/test_x4b.py)
- Kind: python
- Lines: 108

## Module docstring

> X4 Phase B adapter (protocol x4b-v1): future maps, canonical remapping, store isolation,
> precision and permutation agreement flags, and an end-to-end pool screen on a tiny HMM.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import MemoryBackend, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.experiment.x4b import Pool, ReadThroughBackend, canonical_tokens, future_maps, map_failures, pool_checks, pool_failures` -> [src/topo_pilot/experiment/x4b.py](../../src/topo_pilot/experiment/x4b.py.md) (line 7, via package root)
- `from topo_pilot.experiment.x4b_audit import agreement_failures, pool_audit` -> [src/topo_pilot/experiment/x4b_audit.py](../../src/topo_pilot/experiment/x4b_audit.py.md) (line 16, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)

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

- **function `_stochastic`** [L21-23]: `def _stochastic(rng, n, m)`
- **test `test_future_maps_routes_agree_and_checks_pass`** [L26-34]: `def test_future_maps_routes_agree_and_checks_pass()`
- **test `test_future_maps_four_state_path`** [L37-42]: `def test_future_maps_four_state_path()`
- **test `test_map_failures_flag_a_corrupted_joint`** [L45-49]: `def test_map_failures_flag_a_corrupted_joint()`
- **test `test_canonical_tokens_invert_the_symbol_permutation`** [L52-56]: `def test_canonical_tokens_invert_the_symbol_permutation()`
- **test `test_read_through_backend_never_writes_to_the_main_store`** [L59-65]: `def test_read_through_backend_never_writes_to_the_main_store()`
- **function `_agreement`** [L68-73]: `def _agreement(**over)`
- **test `test_agreement_failures_flag_precision_and_permutation`** [L76-82]: `def test_agreement_failures_flag_precision_and_permutation()`
- **function `_tiny_pool`** [L85-93]: `def _tiny_pool(rng, m=600)`
- **test `test_pool_audit_end_to_end_is_deterministic`** [L96-108]: `def test_pool_audit_end_to_end_is_deterministic()`

