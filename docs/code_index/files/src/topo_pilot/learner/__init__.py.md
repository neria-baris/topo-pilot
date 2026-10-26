# `src/topo_pilot/learner/__init__.py`

- Source: [src/topo_pilot/learner/__init__.py](../../../../../../src/topo_pilot/learner/__init__.py)
- Kind: python
- Lines: 11

## Module docstring

> Public API of `topo_pilot.learner` (see SPEC.md and README.md).

## Imports

### Internal (repo files)

- `from .config import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/config.py](config.py.md) (line 3, via relative)
- `from .model import HOOK_NAMES, ModelOutput, TransformerLM` -> [src/topo_pilot/learner/model.py](model.py.md) (line 4, via relative)
- `from .patch import PatchedOutput, forward_with_patch` -> [src/topo_pilot/learner/patch.py](patch.py.md) (line 5, via relative)
- `from .stage import LearnerStage, load_model, serialise_state` -> [src/topo_pilot/learner/stage.py](stage.py.md) (line 6, via relative)
- `from .trainer import Trainer, TrainSummary` -> [src/topo_pilot/learner/trainer.py](trainer.py.md) (line 7, via relative)

### External (third-party)

- none

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/activations/_extractor.py](../activations/_extractor.py.md) (line 20, import)
- [src/topo_pilot/activations/_stage.py](../activations/_stage.py.md) (line 47, import)
- [src/topo_pilot/experiment/s3.py](../experiment/s3.py.md) (line 38, import)
- [src/topo_pilot/experiment/x4_inputs.py](../experiment/x4_inputs.py.md) (line 30, import)
- [src/topo_pilot/experiment/x4f_gates.py](../experiment/x4f_gates.py.md) (line 26, import)
- [src/topo_pilot/experiment/x4f_run.py](../experiment/x4f_run.py.md) (line 30, import)
- [src/topo_pilot/experiment/x5g1_scorebench.py](../experiment/x5g1_scorebench.py.md) (line 34, import)
- [src/topo_pilot/experiment/x5g1_techbench.py](../experiment/x5g1_techbench.py.md) (line 27, import)
- [src/topo_pilot/experiment/x5g1t_checks.py](../experiment/x5g1t_checks.py.md) (line 13, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](../experiment/x5g1t_stages.py.md) (line 33, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](../experiment/x5g1t_stages_eval.py.md) (line 41, import)
- [src/topo_pilot/experiment/x5g1t_train.py](../experiment/x5g1t_train.py.md) (line 20, import)
- [tests/activations/conftest.py](../../../tests/activations/conftest.py.md) (line 54, import)
- [tests/activations/test_activations.py](../../../tests/activations/test_activations.py.md) (line 157, import)
- [tests/c2_readout/test_b_patch.py](../../../tests/c2_readout/test_b_patch.py.md) (line 28, import)
- [tests/d2a/test_a_pad.py](../../../tests/d2a/test_a_pad.py.md) (line 17, import)
- [tests/d2a/test_b_resource.py](../../../tests/d2a/test_b_resource.py.md) (line 26, import)
- [tests/experiment/test_x4f_gates_smoke.py](../../../tests/experiment/test_x4f_gates_smoke.py.md) (line 12, import)
- [tests/experiment/test_x5g1_scorebench_smoke.py](../../../tests/experiment/test_x5g1_scorebench_smoke.py.md) (line 10, import)
- [tests/experiment/test_x5g1t_checkpoint_checks.py](../../../tests/experiment/test_x5g1t_checkpoint_checks.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 26, import)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_config_synthetic.py](../../../tests/experiment/test_x5g1t_config_synthetic.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 29, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 29, import)
- [tests/learner/conftest.py](../../../tests/learner/conftest.py.md) (line 10, import)
- [tests/learner/test_checkpoint.py](../../../tests/learner/test_checkpoint.py.md) (line 17, import)
- [tests/learner/test_model.py](../../../tests/learner/test_model.py.md) (line 9, import)
- [tests/learner/test_model.py](../../../tests/learner/test_model.py.md) (line 11, import)
- [tests/learner/test_multihorizon.py](../../../tests/learner/test_multihorizon.py.md) (line 29, import)
- [tests/learner/test_patch.py](../../../tests/learner/test_patch.py.md) (line 13, import)
- [tests/learner/test_patch.py](../../../tests/learner/test_patch.py.md) (line 15, import)
- [tests/learner/test_trainer_golden.py](../../../tests/learner/test_trainer_golden.py.md) (line 24, import)
- [tests/learner/test_trainer_golden.py](../../../tests/learner/test_trainer_golden.py.md) (line 46, import)
- [tests/learner/test_training.py](../../../tests/learner/test_training.py.md) (line 10, import)
- [tests/learner/test_training.py](../../../tests/learner/test_training.py.md) (line 40, import)
- [tests/learner/test_training.py](../../../tests/learner/test_training.py.md) (line 123, import)
- [tests/x6_stage1/test_a_eval.py](../../../tests/x6_stage1/test_a_eval.py.md) (line 32, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 34, import)
- [tests/x6_stage1/test_b_train_chain.py](../../../tests/x6_stage1/test_b_train_chain.py.md) (line 32, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../../tests/x6zc/test_x6zc_dryrun.py.md) (line 312, import)
- [tools/c1prime/c1_model.py](../../../tools/c1prime/c1_model.py.md) (line 14, import)
- [tools/c2_readout/c2_model.py](../../../tools/c2_readout/c2_model.py.md) (line 24, import)
- [tools/d2a/d2a_eval.py](../../../tools/d2a/d2a_eval.py.md) (line 17, import)
- [tools/d2a/d2a_train.py](../../../tools/d2a/d2a_train.py.md) (line 50, import)
- [tools/d2a/d2a_train.py](../../../tools/d2a/d2a_train.py.md) (line 57, import)
- [tools/d2a/d2a_train.py](../../../tools/d2a/d2a_train.py.md) (line 72, import)
- [tools/d2a/d2a_train.py](../../../tools/d2a/d2a_train.py.md) (line 88, import)
- [tools/x6_stage1/x6s1_cloud.py](../../../tools/x6_stage1/x6s1_cloud.py.md) (line 29, import)
- [tools/x6_stage1/x6s1_data.py](../../../tools/x6_stage1/x6s1_data.py.md) (line 26, import)
- [tools/x6_stage1/x6s1_data.py](../../../tools/x6_stage1/x6s1_data.py.md) (line 255, import)
- [tools/x6_stage1/x6s1_ingest.py](../../../tools/x6_stage1/x6s1_ingest.py.md) (line 28, import)
- [tools/x6_stage1/x6s1_run.py](../../../tools/x6_stage1/x6s1_run.py.md) (line 446, import)
- [tools/x6zc/x6zc_dry.py](../../../tools/x6zc/x6zc_dry.py.md) (line 83, import)

## Top-level constants

- none

## Classes and functions

- none

