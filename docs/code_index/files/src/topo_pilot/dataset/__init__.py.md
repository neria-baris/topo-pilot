# `src/topo_pilot/dataset/__init__.py`

- Source: [src/topo_pilot/dataset/__init__.py](../../../../../../src/topo_pilot/dataset/__init__.py)
- Kind: python
- Lines: 9

## Module docstring

> Public API of `topo_pilot.dataset` (see SPEC.md and README.md).

## Imports

### Internal (repo files)

- `from .config import DatasetConfig` -> [src/topo_pilot/dataset/config.py](config.py.md) (line 3, via relative)
- `from .panels import PanelBuilder` -> [src/topo_pilot/dataset/panels.py](panels.py.md) (line 4, via relative)
- `from .public import PublicTokenDataset` -> [src/topo_pilot/dataset/public.py](public.py.md) (line 5, via relative)
- `from .sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](sampler.py.md) (line 6, via relative)
- `from .stage import DatasetStage` -> [src/topo_pilot/dataset/stage.py](stage.py.md) (line 7, via relative)

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

- [src/topo_pilot/experiment/s2.py](../experiment/s2.py.md) (line 41, import)
- [src/topo_pilot/experiment/s7_dev.py](../experiment/s7_dev.py.md) (line 33, import)
- [src/topo_pilot/experiment/x4b2.py](../experiment/x4b2.py.md) (line 26, import)
- [src/topo_pilot/experiment/x5g1_lineage.py](../experiment/x5g1_lineage.py.md) (line 19, import)
- [src/topo_pilot/experiment/x5g1_scorebench.py](../experiment/x5g1_scorebench.py.md) (line 33, import)
- [src/topo_pilot/experiment/x5g1_techbench.py](../experiment/x5g1_techbench.py.md) (line 26, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](../experiment/x5g1t_stages_eval.py.md) (line 40, import)
- [src/topo_pilot/experiment/x5g1t_train.py](../experiment/x5g1t_train.py.md) (line 19, import)
- [src/topo_pilot/learner/stage.py](../learner/stage.py.md) (line 20, import)
- [src/topo_pilot/learner/trainer.py](../learner/trainer.py.md) (line 15, import)
- [tests/d2a/test_a_targets.py](../../../tests/d2a/test_a_targets.py.md) (line 20, import)
- [tests/d2a/test_b_targets.py](../../../tests/d2a/test_b_targets.py.md) (line 18, import)
- [tests/dataset/conftest.py](../../../tests/dataset/conftest.py.md) (line 7, import)
- [tests/dataset/test_panels.py](../../../tests/dataset/test_panels.py.md) (line 14, import)
- [tests/dataset/test_public.py](../../../tests/dataset/test_public.py.md) (line 15, import)
- [tests/dataset/test_sampler.py](../../../tests/dataset/test_sampler.py.md) (line 7, import)
- [tests/dataset/test_stage.py](../../../tests/dataset/test_stage.py.md) (line 5, import)
- [tests/experiment/test_x5g1_lineage.py](../../../tests/experiment/test_x5g1_lineage.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 19, import)
- [tests/k4b/test_b_data.py](../../../tests/k4b/test_b_data.py.md) (line 28, import)
- [tests/learner/conftest.py](../../../tests/learner/conftest.py.md) (line 9, import)
- [tests/learner/test_multihorizon.py](../../../tests/learner/test_multihorizon.py.md) (line 28, import)
- [tests/learner/test_trainer_golden.py](../../../tests/learner/test_trainer_golden.py.md) (line 45, import)
- [tests/learner/test_training.py](../../../tests/learner/test_training.py.md) (line 9, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 32, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 30, import)
- [tests/x6_stage1/test_b_train_chain.py](../../../tests/x6_stage1/test_b_train_chain.py.md) (line 30, import)
- [tools/c1prime/c1_data.py](../../../tools/c1prime/c1_data.py.md) (line 16, import)
- [tools/c2_nd/nd_data.py](../../../tools/c2_nd/nd_data.py.md) (line 22, import)
- [tools/c2_nd/nd_dry.py](../../../tools/c2_nd/nd_dry.py.md) (line 37, import)
- [tools/c2_readout/c2_data.py](../../../tools/c2_readout/c2_data.py.md) (line 28, import)
- [tools/d2a/d2a_train.py](../../../tools/d2a/d2a_train.py.md) (line 269, import)
- [tools/d2a/d2a_world.py](../../../tools/d2a/d2a_world.py.md) (line 19, import)
- [tools/k4b/k4b_data.py](../../../tools/k4b/k4b_data.py.md) (line 19, import)
- [tools/x2a_stage0/x2a_mc.py](../../../tools/x2a_stage0/x2a_mc.py.md) (line 21, import)
- [tools/x6_stage0/x6_run.py](../../../tools/x6_stage0/x6_run.py.md) (line 24, import)
- [tools/x6_stage1/x6s1_cloud.py](../../../tools/x6_stage1/x6s1_cloud.py.md) (line 27, import)
- [tools/x6_stage1/x6s1_data.py](../../../tools/x6_stage1/x6s1_data.py.md) (line 24, import)
- [tools/x6_stage1/x6s1_run.py](../../../tools/x6_stage1/x6s1_run.py.md) (line 444, import)

## Top-level constants

- none

## Classes and functions

- none

