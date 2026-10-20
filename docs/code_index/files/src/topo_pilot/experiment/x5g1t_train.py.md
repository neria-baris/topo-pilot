# `src/topo_pilot/experiment/x5g1t_train.py`

- Source: [src/topo_pilot/experiment/x5g1t_train.py](../../../../../../src/topo_pilot/experiment/x5g1t_train.py)
- Kind: python
- Lines: 127

## Module docstring

> X5 G1 training-study composition (x5g1-train-v3 §2, §8): the public ``Trainer`` with an
> experiment-side checkpoint callback that mirrors the ``LearnerStage`` identity, controls before
> and after every checkpoint write, one model per lock, and an outcome recorded on every exit.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import X5_GRID` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 11, via package root)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 19, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig, Trainer, serialise_state` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 20, via package root)
- `from .x5g1t_runtime import EST, RunLock, assert_can_start, interval_estimate, record_outcome` -> [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 22, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)
- `collections` (lines 8)
- `dataclasses` (lines 7)
- `pathlib` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 17, import)
- [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 30, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 59, import)
- [tests/experiment/test_x5g1t_checkpoint_checks.py](../../../tests/experiment/test_x5g1t_checkpoint_checks.py.md) (line 21, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_config_synthetic.py](../../../tests/experiment/test_x5g1t_config_synthetic.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 23, import)

## Top-level constants

- `LOCK_NAME`

## Classes and functions

- **function `study_train_config`** [L33-35]: `def study_train_config(steps: int = 5000, grid=X5_GRID) -> TrainConfig` - Stored E3 values except ``checkpoint_steps`` = the grid and ``device = "cpu"``.
- **function `study_run_key`** [L38-40]: `def study_run_key(master) -> tuple` - The same for both arms of a pair: identical init and batch order.
- **function `checkpoint_callback`** [L43-66]: `def checkpoint_callback(store: ArtifactStore, obs_train_id: str, obs_dev_id: str, model_cfg: ModelConfig, train_cfg: TrainConfig, seeds: SeedTree, run_key: tuple, before: Callable[[int], None], after: Callable[[int], None], record: list) -> Callable` - ``on_checkpoint(step, model, info)``: ``before`` -> LearnerStage-identical save ->
- **function `_next_updates`** [L69-71]: `def _next_updates(grid: tuple[int, ...], step: int) -> int`
- **function `train_one`** [L74-127]: `def train_one(store: ArtifactStore, obs_train_id: str, obs_dev_id: str, model_cfg: ModelConfig, train_cfg: TrainConfig, master, arm: str, root: Path, controls, reserve_s: float = 0.0, est: dict = EST) -> dict` - Train one model under a run lock; always record COMPLETE or INCOMPLETE, then re-raise.

