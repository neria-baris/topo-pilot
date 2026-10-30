# `src/topo_pilot/learner/stage.py`

- Source: [src/topo_pilot/learner/stage.py](../../../../../../src/topo_pilot/learner/stage.py)
- Kind: python
- Lines: 106

## Module docstring

> Checkpoint serialisation and the single I/O class of the learner.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 20, via package root)
- `from .config import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/config.py](config.py.md) (line 22, via relative)
- `from .model import TransformerLM` -> [src/topo_pilot/learner/model.py](model.py.md) (line 23, via relative)
- `from .trainer import Trainer, TrainSummary` -> [src/topo_pilot/learner/trainer.py](trainer.py.md) (line 24, via relative)

### External (third-party)

- `torch` (lines 9)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)
- `io` (lines 6)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/learner/__init__.py](__init__.py.md) (line 6, import)
- [tests/learner/test_checkpoint.py](../../../tests/learner/test_checkpoint.py.md) (line 67, import)
- [tools/c1prime/c1_model.py](../../../tools/c1prime/c1_model.py.md) (line 15, import)
- [tools/hwsb/hwsb_eval.py](../../../tools/hwsb/hwsb_eval.py.md) (line 22, import)
- [tools/hwsb/hwsb_train.py](../../../tools/hwsb/hwsb_train.py.md) (line 31, import)
- [tools/hwsc/hwsc_dry.py](../../../tools/hwsc/hwsc_dry.py.md) (line 35, import)
- [tools/x6_stage1/x6s1_eval.py](../../../tools/x6_stage1/x6s1_eval.py.md) (line 33, import)

## Top-level constants

- `CONSUMER`

## Classes and functions

- **function `serialise_state`** [L29-43]: `def serialise_state(model: TransformerLM, info: dict[str, Any]) -> bytes` - ``torch.save({"model": ...[, "optimizer", "scheduler"]})`` into bytes.
- **function `load_model`** [L46-61]: `def load_model(checkpoint: Checkpoint) -> TransformerLM` - Rebuild a ``TransformerLM`` (eval mode, CPU) from ``checkpoint.model_config`` + weights.
- **class `LearnerStage`** [L64-106] - Loads the two ObservationSets (consumer ``learner``), trains, saves one Checkpoint per step.
- **method `LearnerStage.__init__`** [L72-73]: `def __init__(self) -> None`
- **method `LearnerStage.run`** [L75-106]: `def run(self, obs_train_id: str, obs_dev_id: str, model_cfg: ModelConfig, train_cfg: TrainConfig, seeds: SeedTree, run_key: tuple, store: ArtifactStore) -> list[str]` - Train and store checkpoints; returns their ids in step order.

