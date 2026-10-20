# `tests/experiment/test_x5g1t_config_checks.py`

- Source: [tests/experiment/test_x5g1t_config_checks.py](../../../../../tests/experiment/test_x5g1t_config_checks.py)
- Kind: python
- Lines: 299

## Module docstring

> Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
> (docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
> modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
> full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import X5_GRID` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 20, via package root)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.contracts.testing import tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 22, via package root)
- `from topo_pilot.experiment import x5g1t_lineage, x5g1t_train` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md), [src/topo_pilot/experiment/x5g1t_train.py](../../src/topo_pilot/experiment/x5g1t_train.py.md) (line 23, via package root)
- `from topo_pilot.experiment.x5g1t_fixture import E0, T0, _emission` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 24, via package root)
- `from topo_pilot.experiment.x5g1t_lineage import CODES, NAMESPACE` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md) (line 25, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 26, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 9)
- `hashlib` (lines 10)
- `importlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)
- `types` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 31: `topo_pilot.experiment.x5g1t_config` -> [src/topo_pilot/experiment/x5g1t_config.py](../../src/topo_pilot/experiment/x5g1t_config.py.md)

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `KEYS`
- `MODEL`
- `PRODUCER`

## Classes and functions

- **function `_cm`** [L30-31]: `def _cm()`
- **function `_rt`** [L43-44]: `def _rt(obj)`
- **function `_sha_file`** [L47-48]: `def _sha_file(p: Path) -> str`
- **function `_snapshot`** [L51-56]: `def _snapshot(root: Path) -> dict`
- **function `_save_sources`** [L60-70]: `def _save_sources(root: Path, tag: str, producer: str)`
- **function `_sources`** [L73-77]: `def _sources(st: ArtifactStore, ids: dict) -> dict`
- **function `_save_stored_ckpt`** [L80-84]: `def _save_stored_ckpt(st: ArtifactStore, model: dict, train: dict, tag: str = 'e3') -> str`
- **function `_cfg_from_spec`** [L87-98]: `def _cfg_from_spec(spec, mode: str = 'production') -> dict`
- **function `spies`** [L102-114]: `def spies(monkeypatch)` decorators: @pytest.fixture
- **function `prod`** [L118-151]: `def prod(tmp_path, monkeypatch, spies)` decorators: @pytest.fixture - A synthetic stand-in for PRODUCTION: dataclasses.replace(PRODUCTION, ...) pointed at three
- **function `_write`** [L154-157]: `def _write(env, d: dict, name: str = 'cfg.json') -> Path`
- **function `_load`** [L160-161]: `def _load(env, d: dict, name: str = 'cfg.json')`
- **function `_assert_accepts`** [L164-172]: `def _assert_accepts(env, d: dict, spec=None) -> dict`
- **function `_assert_rejects`** [L175-188]: `def _assert_rejects(env, d: dict, spec=None) -> None` - Rejected by load_config or by validate_config with ConfigInvalid; nothing created and no
- **test `test_production_spec_holds_frozen_v4_values`** [L192-225]: `def test_production_spec_holds_frozen_v4_values()`
- **test `test_load_config_valid_is_frozen_exact_keys_and_root`** [L229-235]: `def test_load_config_valid_is_frozen_exact_keys_and_root(prod)`
- **test `test_load_config_unknown_key`** [L238-240]: `def test_load_config_unknown_key(prod)`
- **test `test_load_config_missing_key`** [L244-248]: `def test_load_config_missing_key(prod, key)` decorators: @pytest.mark.parametrize('key', sorted(KEYS))
- **test `test_load_config_wrong_type`** [L259-261]: `def test_load_config_wrong_type(prod, key, value)` decorators: @pytest.mark.parametrize('key,value', [('steps', '5000'), ('threads', 1.5), ('masters', '310001'), ('sizes', [131072, 4096, 4096]), ('gc', '0.27'), ('read_roots', 'C:/single'), ('check_stored_ids', 'yes'), ('env', ['OMP_NUM_THREADS=1']), ('protocol', 4), ('grid', '0,50'), ('stored_checkpoint', 'c3358e3cb9c352fb'), ('model_config', [1, 2]), ('cap_s', '21600'), ('bootstrap_draws', '2000'), ('protocol_doc_sha256', 'not-a-hex-sha'), ('sources', ['world'])])
- **test `test_load_config_malformed_json`** [L265-269]: `def test_load_config_malformed_json(prod, text)` decorators: @pytest.mark.parametrize('text', ['{"mode": "production",', 'not json', '[]', '', 'null'])
- **test `test_unknown_mode_rejected`** [L273-274]: `def test_unknown_mode_rejected(prod, mode)` decorators: @pytest.mark.parametrize('mode', ['prod', 'PRODUCTION', 'synthetic', 'fixture', '', 'test'])
- **test `test_production_correct_config_passes_read_only`** [L278-282]: `def test_production_correct_config_passes_read_only(prod)`
- **test `test_production_paths_compared_after_resolve_and_normcase`** [L285-291]: `def test_production_paths_compared_after_resolve_and_normcase(prod)`
- **test `test_rejection_before_sampler_leaves_no_study_root`** [L294-299]: `def test_rejection_before_sampler_leaves_no_study_root(prod)` - Rejection happens before any sampler/model: spies record nothing, study root absent.

