# `tests/experiment/test_x5g1t_config_production.py`

- Source: [tests/experiment/test_x5g1t_config_production.py](../../../../../tests/experiment/test_x5g1t_config_production.py)
- Kind: python
- Lines: 390

## Module docstring

> Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
> (docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
> modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
> full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
> Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.contracts.testing import tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 21, via package root)
- `from topo_pilot.experiment import x5g1t_lineage, x5g1t_train` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md), [src/topo_pilot/experiment/x5g1t_train.py](../../src/topo_pilot/experiment/x5g1t_train.py.md) (line 22, via package root)
- `from topo_pilot.experiment.x5g1t_fixture import E0, T0, _emission` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 23, via package root)
- `from topo_pilot.experiment.x5g1t_lineage import CODES, NAMESPACE` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md) (line 24, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 25, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `hashlib` (lines 11)
- `importlib` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 14)
- `types` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 30: `topo_pilot.experiment.x5g1t_config` -> [src/topo_pilot/experiment/x5g1t_config.py](../../src/topo_pilot/experiment/x5g1t_config.py.md)

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `MODEL`
- `PRODUCER`
- `PROD_TAMPER`

## Classes and functions

- **function `_cm`** [L29-30]: `def _cm()`
- **function `_rt`** [L36-37]: `def _rt(obj)`
- **function `_flip`** [L40-41]: `def _flip(h: str) -> str`
- **function `_sha_file`** [L44-45]: `def _sha_file(p: Path) -> str`
- **function `_snapshot`** [L48-53]: `def _snapshot(root: Path) -> dict`
- **function `_put`** [L56-59]: `def _put(d: dict, path: tuple, value) -> None`
- **function `_save_sources`** [L63-73]: `def _save_sources(root: Path, tag: str, producer: str)`
- **function `_sources`** [L76-80]: `def _sources(st: ArtifactStore, ids: dict) -> dict`
- **function `_save_stored_ckpt`** [L83-87]: `def _save_stored_ckpt(st: ArtifactStore, model: dict, train: dict, tag: str = 'e3') -> str`
- **function `_cfg_from_spec`** [L90-101]: `def _cfg_from_spec(spec, mode: str = 'production') -> dict`
- **function `spies`** [L105-117]: `def spies(monkeypatch)` decorators: @pytest.fixture
- **function `prod`** [L121-154]: `def prod(tmp_path, monkeypatch, spies)` decorators: @pytest.fixture - A synthetic stand-in for PRODUCTION: dataclasses.replace(PRODUCTION, ...) pointed at three
- **function `_write`** [L157-160]: `def _write(env, d: dict, name: str = 'cfg.json') -> Path`
- **function `_load`** [L163-164]: `def _load(env, d: dict, name: str = 'cfg.json')`
- **function `_assert_accepts`** [L167-175]: `def _assert_accepts(env, d: dict, spec=None) -> dict`
- **function `_assert_rejects`** [L178-191]: `def _assert_rejects(env, d: dict, spec=None) -> None` - Rejected by load_config or by validate_config with ConfigInvalid; nothing created and no
- **test `test_production_each_tampered_field_rejected`** [L251-255]: `def test_production_each_tampered_field_rejected(prod, case)` decorators: @pytest.mark.parametrize('case', sorted(PROD_TAMPER))
- **test `test_production_cfg_env_matching_environ_but_not_spec_rejected`** [L258-262]: `def test_production_cfg_env_matching_environ_but_not_spec_rejected(prod, monkeypatch)`
- **test `test_production_env_missing_from_os_environ_rejected`** [L266-268]: `def test_production_env_missing_from_os_environ_rejected(prod, monkeypatch, name)` decorators: @pytest.mark.parametrize('name', ['OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS'])
- **test `test_production_env_differing_in_os_environ_rejected`** [L272-274]: `def test_production_env_differing_in_os_environ_rejected(prod, monkeypatch, name)` decorators: @pytest.mark.parametrize('name', ['OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS'])
- **test `test_production_protocol_doc_bytes_changed_rejected`** [L277-283]: `def test_production_protocol_doc_bytes_changed_rejected(prod)`
- **test `test_production_spec_doc_sha_differs_from_consistent_cfg_rejected`** [L286-289]: `def test_production_spec_doc_sha_differs_from_consistent_cfg_rejected(prod)` - cfg and the repo document agree but the spec pins another sha256.
- **function `_mutate_npz`** [L292-297]: `def _mutate_npz(path: Path) -> None`
- **test `test_production_source_payload_mutated_on_disk_rejected`** [L300-305]: `def test_production_source_payload_mutated_on_disk_rejected(prod)` - Same metadata, mutated payload: the full re-hash must catch it.
- **test `test_production_source_of_wrong_artifact_type_rejected`** [L308-313]: `def test_production_source_of_wrong_artifact_type_rejected(prod)` - cfg and spec agree, but the 'world' source is a TransitionSpec.
- **test `test_production_stored_producer_differs_from_consistent_cfg_rejected`** [L316-320]: `def test_production_stored_producer_differs_from_consistent_cfg_rejected(prod)` - cfg and spec agree on a producer that is not the stored producer_version.
- **function `_with_stored`** [L323-330]: `def _with_stored(prod, model: dict, train: dict, spec_model: dict | None = None)`
- **test `test_production_stored_train_config_differs_beyond_grid_and_device_rejected`** [L336-340]: `def test_production_stored_train_config_differs_beyond_grid_and_device_rejected(prod, field, value)` decorators: @pytest.mark.parametrize('field,value', [('lr', 0.002), ('batch_size', 64), ('warmup', 100), ('weight_decay', 0.0), ('grad_clip', 0.5), ('steps', 4000)])
- **test `test_production_stored_train_config_device_and_grid_are_replaced`** [L343-348]: `def test_production_stored_train_config_device_and_grid_are_replaced(prod)` - Only checkpoint_steps (-> grid) and device (-> "cpu") may differ from the stored dict.
- **test `test_production_stored_model_config_differs_from_cfg_rejected`** [L351-354]: `def test_production_stored_model_config_differs_from_cfg_rejected(prod)`
- **test `test_production_stored_checkpoint_not_a_checkpoint_rejected`** [L357-359]: `def test_production_stored_checkpoint_not_a_checkpoint_rejected(prod)`
- **test `test_production_lineage_constants_mismatch_rejected`** [L369-371]: `def test_production_lineage_constants_mismatch_rejected(prod, lineage)` decorators: @pytest.mark.parametrize('lineage', [{'namespace': 'x5g1-train-v9', 'codes': dict(CODES), 'stream_tail': ('cylinder', 'overlap', '1.25')}, {'namespace': NAMESPACE, 'codes': {**CODES, 'test': 12}, 'stream_tail': ('cylinder', 'overlap', '1.25')}, {'namespace': NAMESPACE, 'codes': dict(CODES), 'stream_tail': ('cylinder', 'overlap', '1.5')}])
- **test `test_production_write_root_safety`** [L377-390]: `def test_production_write_root_safety(prod, where)` decorators: @pytest.mark.parametrize('where', ['equals_read_root', 'inside_read_root', 'inside_repo', 'equals_repo', 'inside_main_repository', 'ledger_inside_study_root']) - spec and cfg agree, so only the write-root rule can reject.

