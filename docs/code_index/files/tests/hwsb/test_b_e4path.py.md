# `tests/hwsb/test_b_e4path.py`

- Source: [tests/hwsb/test_b_e4path.py](../../../../../tests/hwsb/test_b_e4path.py)
- Kind: python
- Lines: 267

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_e4path.py`: recipe check (DRB3), the
> Trainer composition against `LearnerStage` (DRB2-type, tiny sizes), the checkpoint saver and
> SentinelStop, logits/activation equalities (DRB6), thread settings and the torch lock line.
> Tiny models and a few steps only; MemoryBackend stores. tools/hwsb/*.py unread.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 22, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 23, via sys.path edit)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 24, via sys.path edit)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../../tools/hwsb/hwsb_eval.py.md) (line 25, via sys.path edit)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../../tools/hwsb/hwsb_train.py.md) (line 26, via sys.path edit)
- `import c1_model` -> [tools/c1prime/c1_model.py](../../tools/c1prime/c1_model.py.md) (line 27, via unique basename)
- `from topo_pilot.activations import ActivationExtractor` -> [src/topo_pilot/activations/__init__.py](../../src/topo_pilot/activations/__init__.py.md) (line 28, via package root)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, HistoryIndex, MemoryBackend, ObservationSet, SeedTree, SequenceLayout, make_history_id, payload_checksum, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 29, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 32, via package root)
- `from topo_pilot.learner import LearnerStage, ModelConfig, Trainer, TrainConfig, TransformerLM, load_model, serialise_state` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)
- `torch` (lines 16)

### Standard library

- `__future__` (lines 6)
- `dataclasses` (lines 8)
- `json` (lines 9)
- `os` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CHANGES`
- `CONTRACT`
- `E4_MODEL`
- `E4_TRAIN`
- `MASTER`
- `RECIPE`
- `REPO`
- `TINY_MODEL`
- `TRAIN_CHANGES`

## Classes and functions

- **test `test_recipe_equals_contract_and_passes`** [L46-49]: `def test_recipe_equals_contract_and_passes()`
- **test `test_recipe_equals_the_e4_checkpoint_extra_json`** [L52-61]: `def test_recipe_equals_the_e4_checkpoint_extra_json()`
- **test `test_recipe_model_field_change_is_refused`** [L75-78]: `def test_recipe_model_field_change_is_refused(field, value)` decorators: @pytest.mark.parametrize('field,value', list(CHANGES.items()))
- **test `test_recipe_train_field_change_is_refused`** [L82-85]: `def test_recipe_train_field_change_is_refused(field, value)` decorators: @pytest.mark.parametrize('field,value', list(TRAIN_CHANGES.items()))
- **function `tiny_plan`** [L89-95]: `def tiny_plan()`
- **function `world`** [L98-101]: `def world(plan)`
- **function `stores`** [L105-109]: `def stores()` decorators: @pytest.fixture(scope='module')
- **test `test_identical_observation_sets_in_both_stores`** [L112-114]: `def test_identical_observation_sets_in_both_stores(stores)`
- **function `trained`** [L118-124]: `def trained(stores)` decorators: @pytest.fixture(scope='module')
- **test `test_train_equals_learner_stage_bitwise`** [L127-135]: `def test_train_equals_learner_stage_bitwise(stores, trained)`
- **test `test_sentinel_stop_keeps_in_memory_checkpoints`** [L138-156]: `def test_sentinel_stop_keeps_in_memory_checkpoints(stores, trained)`
- **test `test_build_checkpoint_is_the_learner_stage_save_body`** [L159-172]: `def test_build_checkpoint_is_the_learner_stage_save_body()`
- **function `history`** [L176-184]: `def history(obs, dataset_id='drb6')`
- **test `test_logits32_equals_activation_extractor_bitwise`** [L187-197]: `def test_logits32_equals_activation_extractor_bitwise()`
- **function `small_checkpoint`** [L200-208]: `def small_checkpoint(n_layers, seed=3, vocab=(37, 36))`
- **test `test_activations_at_site_equal_c1_model_bitwise`** [L211-228]: `def test_activations_at_site_equal_c1_model_bitwise()`
- **test `test_model_predictive_is_canonical_softmax`** [L231-244]: `def test_model_predictive_is_canonical_softmax()`
- **test `test_set_threads_records_values`** [L248-259]: `def test_set_threads_records_values(monkeypatch)`
- **test `test_torch_versions_reads_the_lock_line`** [L262-267]: `def test_torch_versions_reads_the_lock_line(tmp_path)`

