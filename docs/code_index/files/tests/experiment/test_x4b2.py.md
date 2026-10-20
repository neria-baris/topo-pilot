# `tests/experiment/test_x4b2.py`

- Source: [tests/experiment/test_x4b2.py](../../../../../tests/experiment/test_x4b2.py)
- Kind: python
- Lines: 93

## Module docstring

> X4 Phase B2 lineage adapter (protocol x4b2-v1): frozen streams and namespaces, determinism,
> state discarding, chunked beliefs, window overlap and the Phase B ambient link.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.experiment.x4b2 import FROZEN_CODES, ROLES, ambient_match, beliefs_p32, first_token_p, sample_pool, sequence_ids, windows` -> [src/topo_pilot/experiment/x4b2.py](../../src/topo_pilot/experiment/x4b2.py.md) (line 7, via package root)

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

- **function `_hmm`** [L21-27]: `def _hmm(rng, n=6, v=3)`
- **test `test_sequence_ids_frozen_namespace_and_disjoint`** [L30-39]: `def test_sequence_ids_frozen_namespace_and_disjoint()`
- **test `test_sample_pool_is_deterministic_and_returns_no_states`** [L42-51]: `def test_sample_pool_is_deterministic_and_returns_no_states()`
- **test `test_first_token_p_detects_bias`** [L54-58]: `def test_first_token_p_detects_bias()`
- **test `test_beliefs_chunked_equal_unchunked`** [L61-66]: `def test_beliefs_chunked_equal_unchunked()`
- **test `test_windows_count_identical_histories`** [L69-72]: `def test_windows_count_identical_histories()`
- **class `_Row`** [L75-77]
- **method `_Row.__init__`** [L76-77]: `def __init__(self, rho)`
- **class `_Audit`** [L80-84]
- **test `test_ambient_match_requires_identical_result`** [L87-93]: `def test_ambient_match_requires_identical_result()`

