# `tests/experiment/test_x5g1t_lineage_oracle.py`

- Source: [tests/experiment/test_x5g1t_lineage_oracle.py](../../../../../tests/experiment/test_x5g1t_lineage_oracle.py)
- Kind: python
- Lines: 315

## Module docstring

> Independent contract tests, written from the API contract (X5_G1_TRAINING_API.md §2-§4, §8
> "Lineage and oracle") and protocol x5g1-train-v3 §2-§4, without reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 15, via package root)
- `from topo_pilot.contracts.testing import tiny_hmm` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 22, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 23, via package root)
- `from topo_pilot.experiment import x5g1_lineage` -> [src/topo_pilot/experiment/x5g1_lineage.py](../../src/topo_pilot/experiment/x5g1_lineage.py.md) (line 24, via package root)
- `from topo_pilot.experiment import x5g1t_lineage` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md) (line 25, via package root)
- `from topo_pilot.experiment.x4b2 import process_code` -> [src/topo_pilot/experiment/x4b2.py](../../src/topo_pilot/experiment/x4b2.py.md) (line 26, via package root)
- `from topo_pilot.experiment.x5g1t_oracle import oracle_q32` -> [src/topo_pilot/experiment/x5g1t_oracle.py](../../src/topo_pilot/experiment/x5g1t_oracle.py.md) (line 27, via package root)
- `from topo_pilot.experiment.x5g1t_score import kl_from_log_probs, p32_log_probs, regret_rows` -> [src/topo_pilot/experiment/x5g1t_score.py](../../src/topo_pilot/experiment/x5g1t_score.py.md) (line 28, via package root)
- `from topo_pilot.learner import ModelConfig, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 29, via package root)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)
- `torch` (lines 13)

### Standard library

- `__future__` (lines 9)

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

- `KERNELS`
- `PERM`
- `TINY_MODEL`
- `T_OTHER`

## Classes and functions

- **function `_code`** [L42-43]: `def _code(exc: pytest.ExceptionInfo) -> ErrorCode`
- **test `test_constants_frozen`** [L49-56]: `def test_constants_frozen()`
- **test `test_stream`** [L60-61]: `def test_stream(split)` decorators: @pytest.mark.parametrize('split', ['train', 'dev', 'test'])
- **test `test_stream_unknown_split`** [L64-67]: `def test_stream_unknown_split()`
- **test `test_sequence_ids_formula_and_bits`** [L75-84]: `def test_sequence_ids_formula_and_bits(split, arm, master)` decorators: @pytest.mark.parametrize('split,arm,master', [('train', 'a0', 310001), ('dev', 'a020', 310003), ('test', 'a020', 'shared')])
- **test `test_sequence_ids_invalid`** [L89-92]: `def test_sequence_ids_invalid(split, arm, n)` decorators: @pytest.mark.parametrize('split,arm,n', [('calibration', 'a0', 4), ('train', 'a1', 4), ('dev', 'a0', 0), ('dev', 'a0', 2 ** 28 + 1)])
- **test `test_paired_generators_separate_and_identical`** [L98-105]: `def test_paired_generators_separate_and_identical()`
- **test `test_paired_generators_test_split_uses_seed_zero`** [L108-112]: `def test_paired_generators_test_split_uses_seed_zero()`
- **test `test_paired_generators_invalid`** [L117-120]: `def test_paired_generators_invalid(split, master)` decorators: @pytest.mark.parametrize('split,master', [('test', 310001), ('test', 0), ('train', 'shared'), ('dev', 'shared'), ('calibration', 310001)])
- **test `test_draw_pair_matches_sample_named_per_arm`** [L123-130]: `def test_draw_pair_matches_sample_named_per_arm()`
- **test `test_draw_pair_first_symbol_identical_across_arms`** [L133-141]: `def test_draw_pair_first_symbol_identical_across_arms()`
- **test `test_draw_pair_test_split_is_master_independent`** [L144-147]: `def test_draw_pair_test_split_is_master_independent()`
- **test `test_pool_observation_valid`** [L154-163]: `def test_pool_observation_valid(split)` decorators: @pytest.mark.parametrize('split', ['train', 'dev', 'test'])
- **test `test_pool_observation_rejects_invalid`** [L166-173]: `def test_pool_observation_rejects_invalid()`
- **test `test_pool_config_contents`** [L176-182]: `def test_pool_config_contents()`
- **function `_all_planned`** [L188-195]: `def _all_planned(n: int) -> dict[str, np.ndarray]`
- **test `test_disjoint_across_splits_arms_masters`** [L198-205]: `def test_disjoint_across_splits_arms_masters()`
- **test `test_collisions_counts`** [L208-218]: `def test_collisions_counts()`
- **function `_named_and_canon`** [L224-227]: `def _named_and_canon(n: int) -> tuple[np.ndarray, np.ndarray]`
- **test `test_oracle_equals_bayes_filter_on_w1_to_w32`** [L230-235]: `def test_oracle_equals_bayes_filter_on_w1_to_w32()`
- **test `test_oracle_ignores_column_33`** [L238-245]: `def test_oracle_ignores_column_33()`
- **test `test_oracle_named_equals_canonical_under_perm`** [L248-254]: `def test_oracle_named_equals_canonical_under_perm()`
- **test `test_oracle_guard_and_batch_invariance`** [L257-262]: `def test_oracle_guard_and_batch_invariance()`
- **function `_model_and_inputs`** [L268-274]: `def _model_and_inputs(r: int) -> tuple[TransformerLM, torch.Tensor, np.ndarray]`
- **test `test_regret_zero_on_own_softmax_and_nonnegative`** [L277-285]: `def test_regret_zero_on_own_softmax_and_nonnegative()`
- **test `test_regret_batch_invariant_and_training_flag_restored`** [L288-297]: `def test_regret_batch_invariant_and_training_flag_restored()`
- **test `test_kl_hand_value_and_invalid_q`** [L300-309]: `def test_kl_hand_value_and_invalid_q()`
- **test `test_p32_requires_33_inputs`** [L312-315]: `def test_p32_requires_33_inputs()`

