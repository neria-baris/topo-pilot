# `tests/learner/test_training.py`

- Source: [tests/learner/test_training.py](../../../../../tests/learner/test_training.py)
- Kind: python
- Lines: 131

## Module docstring

> L04, L05, L07, L08, L10: training loop contracts.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 9, via package root)
- `from topo_pilot.learner import TrainConfig, Trainer` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 10, via package root)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 40, via package root) (inside a function)
- `from topo_pilot.learner.trainer import WarmupCosine` -> [src/topo_pilot/learner/trainer.py](../../src/topo_pilot/learner/trainer.py.md) (line 115, via package root) (inside a function)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 123, via package root) (inside a function)

### External (third-party)

- `pytest` (lines 5)
- `torch` (lines 6)

### Standard library

- `dataclasses` (lines 3)

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

- **function `_fit`** [L15-22]: `def _fit(model_cfg, train_cfg, ds, seed=1729, key=('r', 0))`
- **test `test_L04_overfit_eight_sequences`** [L25-36]: `def test_L04_overfit_eight_sequences(model_cfg, tiny_obs)`
- **test `test_L05_step0_is_initial_weights_and_runs_repeat`** [L39-56]: `def test_L05_step0_is_initial_weights_and_runs_repeat(model_cfg, train_cfg, tiny_ds)`
- **test `test_L05b_global_rng_untouched`** [L59-64]: `def test_L05b_global_rng_untouched(model_cfg, train_cfg, tiny_ds)`
- **test `test_L07_non_public_dataset_is_leakage`** [L67-75]: `def test_L07_non_public_dataset_is_leakage(model_cfg, train_cfg, tiny_ds, tiny_obs)`
- **test `test_L08_nan_loss_raises`** [L78-91]: `def test_L08_nan_loss_raises(monkeypatch, model_cfg, train_cfg, tiny_ds)`
- **test `test_L10_schedule_and_optimizer_only_at_final`** [L94-103]: `def test_L10_schedule_and_optimizer_only_at_final(model_cfg, tiny_ds)`
- **test `test_L10b_invalid_schedules_rejected`** [L106-111]: `def test_L10b_invalid_schedules_rejected(model_cfg, tiny_ds)`
- **test `test_lr_schedule_known_values`** [L114-119]: `def test_lr_schedule_known_values()`
- **test `test_weight_decay_groups`** [L122-130]: `def test_weight_decay_groups(model_cfg, train_cfg)`

