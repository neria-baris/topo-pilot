# `tests/oracle/test_oracle.py`

- Source: [tests/oracle/test_oracle.py](../../../../../tests/oracle/test_oracle.py)
- Kind: python
- Lines: 319

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot import oracle` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 6, via package root)
- `from topo_pilot.contracts import EvalSidecar, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.contracts.testing import memory_store, tiny_hmm, tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 8, via package root)
- `from topo_pilot.oracle import BayesFilter, FutureOperator, LastSymbolPosterior, context_gain` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)

### Standard library

- `itertools` (lines 1)

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

- **function `joint_over_paths`** [L15-25]: `def joint_over_paths(T, E, pi, seq)` - Array [N]*len(seq) of P(w_1..w_P, z_1..z_P) under the generation model.
- **function `brute_marginal`** [L28-33]: `def brute_marginal(T, E, pi, seq)` - (evidence, posterior of last state) for a sequence.
- **function `code_name`** [L36-38]: `def code_name(exc)`
- **function `hmm`** [L42-43]: `def hmm()` decorators: @pytest.fixture(scope='module')
- **test `test_O01_bruteforce_all_length4_sequences`** [L47-79]: `def test_O01_bruteforce_all_length4_sequences(hmm)`
- **test `test_O01_belief_at_matches_run`** [L82-89]: `def test_O01_belief_at_matches_run(hmm)`
- **test `test_O01_evidence_is_sum_of_ce`** [L92-96]: `def test_O01_evidence_is_sum_of_ce(hmm)`
- **test `test_filter_inputs_untouched_and_rows_independent`** [L99-110]: `def test_filter_inputs_untouched_and_rows_independent(hmm)`
- **test `test_O02_q0_is_pi_E`** [L114-124]: `def test_O02_q0_is_pi_E(hmm)`
- **test `test_O03_unique_emission_belief_is_delta`** [L128-145]: `def test_O03_unique_emission_belief_is_delta()`
- **test `test_O04_uniform_emission_beliefs_stay_pi`** [L149-156]: `def test_O04_uniform_emission_beliefs_stay_pi()`
- **test `test_O05_F1_F2`** [L160-176]: `def test_O05_F1_F2(hmm)`
- **test `test_O05_F2_from_prior_matches_brute_force`** [L179-184]: `def test_O05_F2_from_prior_matches_brute_force(hmm)`
- **test `test_O06_last_symbol_posterior`** [L188-203]: `def test_O06_last_symbol_posterior(hmm)`
- **test `test_O07_context_gain_nonneg_and_zero`** [L207-224]: `def test_O07_context_gain_nonneg_and_zero(hmm)`
- **test `test_O08_impossible_history_raises`** [L228-247]: `def test_O08_impossible_history_raises()`
- **test `test_alignment_errors`** [L250-259]: `def test_alignment_errors(hmm)`
- **test `test_O09_long_near_deterministic_no_underflow`** [L263-282]: `def test_O09_long_near_deterministic_no_underflow()`
- **test `test_O10_observability_ranks`** [L286-300]: `def test_O10_observability_ranks()`
- **test `test_O11_policy_refuses_sidecar_for_oracle`** [L304-313]: `def test_O11_policy_refuses_sidecar_for_oracle()`
- **test `test_public_api_exports`** [L316-319]: `def test_public_api_exports()`

