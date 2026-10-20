# `tests/learner/test_multihorizon.py`

- Source: [tests/learner/test_multihorizon.py](../../../../../tests/learner/test_multihorizon.py)
- Kind: python
- Lines: 399

## Module docstring

> Independent tests of learner/multihorizon.py and the Trainer injection (job 0028, author A).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import Checkpoint, ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 28, via package root)
- `from topo_pilot.learner import ModelConfig, ModelOutput, TrainConfig, Trainer, TransformerLM, load_model, serialise_state` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 29, via package root)
- `from topo_pilot.learner.multihorizon import MultiHorizonLM, MultiHorizonOutput, check_causal_joint, joint_index, load_multi_horizon, multi_horizon_loss` -> [src/topo_pilot/learner/multihorizon.py](../../src/topo_pilot/learner/multihorizon.py.md) (line 38, via package root)
- `from topo_pilot.learner.trainer import lm_loss` -> [src/topo_pilot/learner/trainer.py](../../src/topo_pilot/learner/trainer.py.md) (line 46, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)
- `torch` (lines 17, 18)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `functools` (lines 13)
- `io` (lines 11)
- `math` (lines 12)

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

- `AUX`
- `DEEP`
- `JOINT`
- `STEP0`
- `TINY`

## Classes and functions

- **function `_x`** [L58-59]: `def _x(n=3, seed=2, vocab=6)`
- **function `_mh`** [L62-64]: `def _mh(horizon, aux=AUX, cfg=TINY, seed=11)`
- **function `_ds`** [L67-71]: `def _ds(split, n, seed)`
- **function `data`** [L75-76]: `def data()` decorators: @pytest.fixture(scope='module')
- **function `_trainer`** [L79-85]: `def _trainer(horizon, train_cfg=STEP0, cfg=TINY)`
- **function `_fit`** [L88-96]: `def _fit(horizon, data, train_cfg=STEP0)`
- **test `test_T_TRUNK_model_level_trunk_and_logits_bitwise`** [L100-109]: `def test_T_TRUNK_model_level_trunk_and_logits_bitwise(horizon)` decorators: @pytest.mark.parametrize('horizon', [2, 3])
- **test `test_T_TRUNK_trainer_step0_trunks_equal_across_horizons`** [L112-126]: `def test_T_TRUNK_trainer_step0_trunks_equal_across_horizons(data)`
- **test `test_trainer_uses_loss_fn_for_joint_heads`** [L129-134]: `def test_trainer_uses_loss_fn_for_joint_heads(data)`
- **test `test_T_HEAD_init_shared_between_horizons_and_matches_spec`** [L137-147]: `def test_T_HEAD_init_shared_between_horizons_and_matches_spec()`
- **test `test_heads_read_ln_final_out_and_forward_returns_requested_hooks`** [L151-168]: `def test_heads_read_ln_final_out_and_forward_returns_requested_hooks(horizon)` decorators: @pytest.mark.parametrize('horizon', [2, 3])
- **test `test_horizon_outside_2_3_is_invalid_config`** [L172-175]: `def test_horizon_outside_2_3_is_invalid_config(horizon)` decorators: @pytest.mark.parametrize('horizon', [0, 1, 4])
- **test `test_T_CAUS_next_symbol_and_joint_logits`** [L179-189]: `def test_T_CAUS_next_symbol_and_joint_logits(horizon)` decorators: @pytest.mark.parametrize('horizon', [2, 3])
- **test `test_T_TARGET_tokens_after_p_change_nothing_at_p`** [L193-206]: `def test_T_TARGET_tokens_after_p_change_nothing_at_p(horizon)` decorators: @pytest.mark.parametrize('horizon', [2, 3])
- **class `_Leak(nn.Module)`** [L209-211]
- **method `_Leak.forward`** [L210-211]: `def forward(self, z)`
- **function `_rng_untouched`** [L214-220]: `def _rng_untouched(fn)`
- **test `test_check_causal_joint_passes_clean_model_and_catches_a_leak`** [L223-229]: `def test_check_causal_joint_passes_clean_model_and_catches_a_leak()`
- **function `_y`** [L232-235]: `def _y()`
- **function `_hand_ce`** [L238-242]: `def _hand_ce(logits, targets)`
- **test `test_T_LOSS_joint_index_hand_values`** [L245-257]: `def test_T_LOSS_joint_index_hand_values()`
- **function `_fake_out`** [L260-264]: `def _fake_out()`
- **test `test_T_LOSS_multi_horizon_loss_hand_values_and_exclusion`** [L267-285]: `def test_T_LOSS_multi_horizon_loss_hand_values_and_exclusion()`
- **test `test_T_LOSS_horizon_one_is_lm_loss_exactly`** [L288-294]: `def test_T_LOSS_horizon_one_is_lm_loss_exactly()`
- **test `test_T_GRAD_ce2_alone_reaches_trunk_through_position_p`** [L297-309]: `def test_T_GRAD_ce2_alone_reaches_trunk_through_position_p()`
- **test `test_T_RNG_global_rng_untouched_by_fit_with_factory`** [L313-315]: `def test_T_RNG_global_rng_untouched_by_fit_with_factory(horizon, data)` decorators: @pytest.mark.parametrize('horizon', [2, 3])
- **function `_ckpt`** [L318-321]: `def _ckpt(model, cfg=TINY, state=None)`
- **function `_blob`** [L324-327]: `def _blob(state_dict)`
- **test `test_T_LOAD_round_trip`** [L331-343]: `def test_T_LOAD_round_trip(horizon)` decorators: @pytest.mark.parametrize('horizon', [2, 3])
- **function `_bad_checkpoints`** [L346-365]: `def _bad_checkpoints()`
- **test `test_T_LOAD_rejections_are_invalid_config`** [L368-372]: `def test_T_LOAD_rejections_are_invalid_config()`
- **test `test_T_LOAD_horizon1_checkpoint_uses_load_model`** [L375-381]: `def test_T_LOAD_horizon1_checkpoint_uses_load_model()`
- **test `test_T_DECAY_groups_equal_transformer_plus_joint_matrices`** [L385-399]: `def test_T_DECAY_groups_equal_transformer_plus_joint_matrices(horizon)` decorators: @pytest.mark.parametrize('horizon', [2, 3])

