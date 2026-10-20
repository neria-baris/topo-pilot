# `tests/experiment/test_x5g1t_training.py`

- Source: [tests/experiment/test_x5g1t_training.py](../../../../../tests/experiment/test_x5g1t_training.py)
- Kind: python
- Lines: 300

## Module docstring

> Independent contract tests, written from the API contract (X5_G1_TRAINING_API.md §5-§6, §8
> "Training composition") and protocol x5g1-train-v3 §2, without reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import Checkpoint, ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.contracts.testing import memory_store, tiny_hmm` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 18, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 19, via package root)
- `from topo_pilot.experiment import x5g1t_lineage` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md) (line 20, via package root)
- `from topo_pilot.experiment.x5g1_controls import StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 21, via package root)
- `from topo_pilot.experiment.x5g1t_runtime import RunLocked, outcome_path, read_outcome` -> [src/topo_pilot/experiment/x5g1t_runtime.py](../../src/topo_pilot/experiment/x5g1t_runtime.py.md) (line 22, via package root)
- `from topo_pilot.experiment.x5g1t_train import checkpoint_callback, study_run_key, study_train_config, train_one` -> [src/topo_pilot/experiment/x5g1t_train.py](../../src/topo_pilot/experiment/x5g1t_train.py.md) (line 23, via package root)
- `from topo_pilot.learner import LearnerStage, ModelConfig, TrainConfig, Trainer` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 29, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 10)
- `dataclasses` (lines 12)

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
- `MASTER`
- `MODEL`
- `PERM`
- `STUDY_GRID`
- `TRAIN`
- `T_OTHER`

## Classes and functions

- **function `_add_pools`** [L43-53]: `def _add_pools(store, master: int = MASTER) -> dict[str, tuple[str, str]]` - Save train (n=32) and dev (n=8) pools per arm; returns {arm: (train_id, dev_id)}.
- **function `_datasets`** [L56-59]: `def _datasets(store, train_id: str, dev_id: str)`
- **function `_ckpts`** [L62-63]: `def _ckpts(store) -> list[str]`
- **class `FakeControls`** [L66-76] - ``.boundary(what, next_estimate, reserve, audit=...)``; raises STOP at call ``stop_at``.
- **method `FakeControls.__init__`** [L69-71]: `def __init__(self, stop_at: int | None = None) -> None`
- **method `FakeControls.boundary`** [L73-76]: `def boundary(self, what, next_estimate, reserve, audit=None)`
- **function `root`** [L80-83]: `def root(tmp_path)` decorators: @pytest.fixture
- **test `test_study_train_config_defaults`** [L89-98]: `def test_study_train_config_defaults()`
- **test `test_study_train_config_custom_grid`** [L101-105]: `def test_study_train_config_custom_grid()`
- **test `test_study_run_key`** [L109-111]: `def test_study_run_key(m)` decorators: @pytest.mark.parametrize('m', [310001, 310002, 310003])
- **function `_callback_run`** [L117-123]: `def _callback_run(store, train_id, dev_id, before, after)`
- **test `test_callback_identical_to_learner_stage`** [L126-159]: `def test_callback_identical_to_learner_stage()`
- **test `test_stop_in_before_writes_no_artifact_for_that_step`** [L162-181]: `def test_stop_in_before_writes_no_artifact_for_that_step()`
- **test `test_stop_before_first_write_leaves_store_empty`** [L184-193]: `def test_stop_before_first_write_leaves_store_empty()`
- **function `_train`** [L199-201]: `def _train(store, pools, arm, root, controls, master=MASTER)`
- **test `test_train_one_complete_matches_learner_stage`** [L204-226]: `def test_train_one_complete_matches_learner_stage(root)`
- **test `test_arms_share_step0_weights_and_seeds_but_not_ids`** [L229-248]: `def test_arms_share_step0_weights_and_seeds_but_not_ids(root)`
- **test `test_train_one_incomplete_recorded_and_reraised`** [L252-266]: `def test_train_one_incomplete_recorded_and_reraised(root, stop_at)` decorators: @pytest.mark.parametrize('stop_at', [1, 3])
- **test `test_second_start_refused_after_complete`** [L269-277]: `def test_second_start_refused_after_complete(root)`
- **test `test_second_start_refused_after_incomplete`** [L280-289]: `def test_second_start_refused_after_incomplete(root)`
- **test `test_existing_lock_refuses_start`** [L292-300]: `def test_existing_lock_refuses_start(root)`

