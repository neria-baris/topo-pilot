# `tests/experiment/test_x5g1_lineage.py`

- Source: [tests/experiment/test_x5g1_lineage.py](../../../../../tests/experiment/test_x5g1_lineage.py)
- Kind: python
- Lines: 280

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 16, via package root)
- `from topo_pilot.contracts.testing import tiny_hmm` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 24, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 25, via package root)
- `from topo_pilot.experiment.x5g1_lineage import ARMS, N_POOL, NAMESPACE_CODE, STREAM, calibration_obs, paired_generators, sample_named, sequence_ids` -> [src/topo_pilot/experiment/x5g1_lineage.py](../../src/topo_pilot/experiment/x5g1_lineage.py.md) (line 26, via package root)
- `from topo_pilot.experiment.x5g1_oracle import bootstrap_means, gate_quantities` -> [src/topo_pilot/experiment/x5g1_oracle.py](../../src/topo_pilot/experiment/x5g1_oracle.py.md) (line 36, via package root)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)

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

- `E5`
- `INV`
- `KEYS`
- `PERM`
- `T2`

## Classes and functions

- **function `_named`** [L51-52]: `def _named(n=300, seed=5, T=T1)`
- **function `_code`** [L55-57]: `def _code(arm: str) -> int`
- **test `test_frozen_constants`** [L63-65]: `def test_frozen_constants()`
- **test `test_paired_generators_distinct_objects_identical_draws`** [L68-74]: `def test_paired_generators_distinct_objects_identical_draws()`
- **test `test_paired_arms_share_first_symbol_and_misuse_is_detected`** [L77-89]: `def test_paired_arms_share_first_symbol_and_misuse_is_detected()`
- **test `test_sample_named_is_perm_of_canonical`** [L95-104]: `def test_sample_named_is_perm_of_canonical()`
- **test `test_sample_named_shape_dtype_and_no_states`** [L107-111]: `def test_sample_named_shape_dtype_and_no_states()`
- **test `test_sample_named_one_call_deterministic`** [L114-115]: `def test_sample_named_one_call_deterministic()`
- **test `test_sequence_ids_namespace_and_disjoint`** [L121-129]: `def test_sequence_ids_namespace_and_disjoint()`
- **test `test_sequence_ids_unknown_arm`** [L132-135]: `def test_sequence_ids_unknown_arm()`
- **test `test_calibration_obs_dev_v36`** [L138-146]: `def test_calibration_obs_dev_v36()`
- **function `_ref_row`** [L152-172]: `def _ref_row(T, E, pi, w)` - Independent forward filter for one 33-token row (reads w[:32] only).
- **test `test_gate_quantities_match_reference_filter`** [L175-184]: `def test_gate_quantities_match_reference_filter()`
- **test `test_gate_quantities_lawful_nonnegative`** [L187-192]: `def test_gate_quantities_lawful_nonnegative()`
- **test `test_gate_quantities_permutation_equivalence`** [L195-202]: `def test_gate_quantities_permutation_equivalence()`
- **test `test_w33_isolation`** [L205-214]: `def test_w33_isolation()`
- **test `test_gate_quantities_batching_is_rowwise`** [L217-224]: `def test_gate_quantities_batching_is_rowwise()`
- **test `test_impossible_history_sets_invalid_without_raising`** [L227-232]: `def test_impossible_history_sets_invalid_without_raising()`
- **test `test_bootstrap_matches_definition_and_is_deterministic`** [L238-246]: `def test_bootstrap_matches_definition_and_is_deterministic()`
- **test `test_bootstrap_guard_before_and_after_each_batch`** [L249-263]: `def test_bootstrap_guard_before_and_after_each_batch()`
- **class `_Halt(RuntimeError)`** [L266-267]
- **test `test_bootstrap_guard_exception_propagates`** [L270-280]: `def test_bootstrap_guard_exception_propagates()`

