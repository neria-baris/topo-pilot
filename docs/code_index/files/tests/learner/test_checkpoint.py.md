# `tests/learner/test_checkpoint.py`

- Source: [tests/learner/test_checkpoint.py](../../../../../tests/learner/test_checkpoint.py)
- Kind: python
- Lines: 84

## Module docstring

> L06 and stage-level checkpoint contracts.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import Checkpoint, ErrorCode, ObservationSet, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 9, via package root)
- `from topo_pilot.contracts.testing import memory_store, tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 16, via package root)
- `from topo_pilot.learner import LearnerStage, TransformerLM, load_model` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 17, via package root)
- `from topo_pilot.learner.stage import serialise_state` -> [src/topo_pilot/learner/stage.py](../../src/topo_pilot/learner/stage.py.md) (line 67, via package root) (inside a function)

### External (third-party)

- `pytest` (lines 6)
- `torch` (lines 7)

### Standard library

- `dataclasses` (lines 3)
- `io` (lines 4)

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

- **function `store_ids`** [L23-30]: `def store_ids(tiny_obs)` decorators: @pytest.fixture()
- **function `_run`** [L33-37]: `def _run(store_ids, model_cfg, train_cfg)`
- **test `test_L06_save_load_reproduces_logits`** [L40-54]: `def test_L06_save_load_reproduces_logits(store_ids, model_cfg, train_cfg)`
- **test `test_L06b_optimizer_flags_and_byte_determinism`** [L57-70]: `def test_L06b_optimizer_flags_and_byte_determinism(store_ids, model_cfg, train_cfg)`
- **test `test_L06c_load_model_rejects_bad_checkpoint`** [L73-79]: `def test_L06c_load_model_rejects_bad_checkpoint(store_ids, model_cfg, train_cfg)`
- **test `test_stage_reads_observations_only_with_learner_policy`** [L82-84]: `def test_stage_reads_observations_only_with_learner_policy(store_ids)`

