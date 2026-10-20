# `src/topo_pilot/experiment/x5g1t_stages_eval.py`

- Source: [src/topo_pilot/experiment/x5g1t_stages_eval.py](../../../../../../src/topo_pilot/experiment/x5g1t_stages_eval.py)
- Kind: python
- Lines: 246

## Module docstring

> X5 G1 training-study stages, part 2 (x5g1-train-v4 §10-§11; API v4 §6): ``dev-analysis`` and
> the separately authorised ``final-test``.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import PairEvidence, cohort_verdict, dev_auc, difference_bounds, grid_event, paired_bootstrap_endpoint, pass_sequence, ratio_curve` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 23, via package root)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 33, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 40, via package root)
- `from topo_pilot.learner import load_model` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 41, via package root)
- `from .x5g1_safety import ensure_new_output_dir` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 43, via relative)
- `from .x5g1t_checks import validate_checkpoints, validate_pool, verify_full` -> [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 44, via relative)
- `from .x5g1t_config import StudyConfig, validate_config` -> [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 45, via relative)
- `from .x5g1t_exports import study_export, verify_export_complete` -> [src/topo_pilot/experiment/x5g1t_exports.py](x5g1t_exports.py.md) (line 46, via relative)
- `from .x5g1t_lineage import ARMS, NAMESPACE, TEST_MASTER, collisions, draw_pair, pool_observation, sequence_ids, stream, study_pool_config` -> [src/topo_pilot/experiment/x5g1t_lineage.py](x5g1t_lineage.py.md) (line 47, via relative)
- `from .x5g1t_oracle import oracle_q32` -> [src/topo_pilot/experiment/x5g1t_oracle.py](x5g1t_oracle.py.md) (line 58, via relative)
- `from .x5g1t_runtime import EST, StudyControls, evaluation_reserve` -> [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 59, via relative)
- `from .x5g1t_score import regret_rows` -> [src/topo_pilot/experiment/x5g1t_score.py](x5g1t_score.py.md) (line 60, via relative)
- `from .x5g1t_stages import StudyFailed, _controls, _meta, _sources, _study, collision_inputs, complete_outcome, complete_pools, stores, tables, validate_pools` -> [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 61, via relative)

### External (third-party)

- `numpy` (lines 20)
- `torch` (lines 21)

### Standard library

- `__future__` (lines 15)
- `dataclasses` (lines 17)
- `pathlib` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 30, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 21, import)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 19, import)

## Top-level constants

- none

## Classes and functions

- **function `_inputs`** [L76-78]: `def _inputs(obs: ObservationSet) -> torch.Tensor`
- **function `_guard`** [L81-82]: `def _guard(sc: StudyControls, reserve: float)`
- **function `_regret_curve`** [L85-93]: `def _regret_curve(rw: ArtifactStore, sc: StudyControls, ckpts: list, inputs, q, reserve: float) -> np.ndarray` - Regret per row and checkpoint; checkpoints were validated by ``validate_checkpoints``.
- **function `_complete`** [L96-97]: `def _complete(o) -> bool`
- **function `run_dev_analysis`** [L100-169]: `def run_dev_analysis(cfg: StudyConfig, repo: Path) -> dict` - Dense dev regret curves, grid events, paired bootstrap and the cohort verdict.
- **function `_pool_ids`** [L172-175]: `def _pool_ids(rw: ArtifactStore, pools: dict) -> np.ndarray` - Sequence IDs of the study's (already identity-checked) train and dev pools.
- **function `run_final_test`** [L178-246]: `def run_final_test(cfg: StudyConfig, repo: Path, authorized: bool) -> dict` - Fresh test (generated here only), step-final checkpoints only; needs authorisation.

