# `tests/experiment/test_x5g1t_checkpoint_checks.py`

- Source: [tests/experiment/test_x5g1t_checkpoint_checks.py](../../../../../tests/experiment/test_x5g1t_checkpoint_checks.py)
- Kind: python
- Lines: 257

## Module docstring

> Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
> (docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
> modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
> full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
> Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts.testing import tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 20, via package root)
- `from topo_pilot.experiment.x5g1t_train import study_run_key, study_train_config` -> [src/topo_pilot/experiment/x5g1t_train.py](../../src/topo_pilot/experiment/x5g1t_train.py.md) (line 21, via package root)
- `from topo_pilot.learner import ModelConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 22, via package root)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `importlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 13)
- `types` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 26: `topo_pilot.experiment.x5g1t_checks` -> [src/topo_pilot/experiment/x5g1t_checks.py](../../src/topo_pilot/experiment/x5g1t_checks.py.md)

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `MASTER`
- `MODEL`

## Classes and functions

- **function `_ck`** [L25-26]: `def _ck()`
- **function `_rt`** [L31-32]: `def _rt(obj)`
- **function `_flip`** [L35-36]: `def _flip(h: str) -> str`
- **function `_obs`** [L44-47]: `def _obs(split: str, seed: int) -> ObservationSet`
- **function `_ckstore`** [L50-56]: `def _ckstore(root: Path)`
- **function `_save_run`** [L59-75]: `def _save_run(st, train_id, dev_id, *, master=MASTER, run_master=None, grid=GRID, steps=STEPS, model=MODEL, train_cfg=None, parents=None, obs_id=None) -> dict`
- **function `_cfg`** [L78-79]: `def _cfg(grid=GRID, steps=STEPS, model=None)`
- **function `ckrun`** [L83-87]: `def ckrun(tmp_path)` decorators: @pytest.fixture
- **test `test_validate_checkpoints_real_store_passes`** [L91-100]: `def test_validate_checkpoints_real_store_passes(ckrun, grid)` decorators: @pytest.mark.parametrize('grid', [list(GRID), tuple(GRID)])
- **test `test_validate_checkpoints_model_config_compared_with_defaults_filled`** [L103-107]: `def test_validate_checkpoints_model_config_compared_with_defaults_filled(ckrun)`
- **function `_fails`** [L110-115]: `def _fails(ckrun, outcome=None, cfg=None, arm='a0', master=MASTER, train=None, dev=None, st=None)`
- **test `test_checkpoints_reordered_rejected`** [L118-121]: `def test_checkpoints_reordered_rejected(ckrun)`
- **test `test_checkpoints_swapped_ids_same_steps_rejected`** [L124-129]: `def test_checkpoints_swapped_ids_same_steps_rejected(ckrun)`
- **test `test_checkpoints_missing_one_rejected`** [L132-135]: `def test_checkpoints_missing_one_rejected(ckrun)`
- **test `test_checkpoints_grid_differs_rejected`** [L138-139]: `def test_checkpoints_grid_differs_rejected(ckrun)`
- **test `test_checkpoints_wrong_dev_parent_rejected`** [L142-143]: `def test_checkpoints_wrong_dev_parent_rejected(ckrun)`
- **test `test_checkpoints_saved_with_wrong_parents_rejected`** [L146-151]: `def test_checkpoints_saved_with_wrong_parents_rejected(tmp_path)`
- **test `test_checkpoints_wrong_model_config_rejected`** [L154-155]: `def test_checkpoints_wrong_model_config_rejected(ckrun)`
- **test `test_checkpoints_wrong_steps_rejected`** [L158-159]: `def test_checkpoints_wrong_steps_rejected(ckrun)`
- **test `test_checkpoints_saved_with_wrong_train_config_rejected`** [L162-168]: `def test_checkpoints_saved_with_wrong_train_config_rejected(tmp_path)`
- **test `test_checkpoints_outcome_arm_mismatch_rejected`** [L171-175]: `def test_checkpoints_outcome_arm_mismatch_rejected(ckrun)`
- **test `test_checkpoints_outcome_master_mismatch_rejected`** [L178-182]: `def test_checkpoints_outcome_master_mismatch_rejected(ckrun)`
- **test `test_checkpoints_of_another_master_rejected`** [L185-191]: `def test_checkpoints_of_another_master_rejected(tmp_path)` - outcome claims master 310001 but the checkpoints carry 310002's run key.
- **test `test_checkpoints_wrong_observation_id_rejected`** [L194-199]: `def test_checkpoints_wrong_observation_id_rejected(tmp_path)`
- **test `test_checkpoints_recorded_sha_wrong_rejected`** [L202-205]: `def test_checkpoints_recorded_sha_wrong_rejected(ckrun)`
- **test `test_checkpoints_not_a_checkpoint_rejected`** [L208-212]: `def test_checkpoints_not_a_checkpoint_rejected(ckrun)`
- **test `test_checkpoints_same_metadata_mutated_payload_rejected`** [L215-220]: `def test_checkpoints_same_metadata_mutated_payload_rejected(ckrun)`
- **test `test_verify_full_passes_on_lawful_artifacts`** [L224-228]: `def test_verify_full_passes_on_lawful_artifacts(ckrun)`
- **test `test_verify_full_missing_id_rejected`** [L231-234]: `def test_verify_full_missing_id_rejected(ckrun)`
- **test `test_verify_full_wrong_sha_rejected`** [L237-241]: `def test_verify_full_wrong_sha_rejected(ckrun)`
- **test `test_verify_full_wrong_class_rejected`** [L244-248]: `def test_verify_full_wrong_class_rejected(ckrun)`
- **test `test_verify_full_mutated_payload_rejected`** [L251-257]: `def test_verify_full_mutated_payload_rejected(ckrun)`

