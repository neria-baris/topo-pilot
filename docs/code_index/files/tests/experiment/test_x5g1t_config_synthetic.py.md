# `tests/experiment/test_x5g1t_config_synthetic.py`

- Source: [tests/experiment/test_x5g1t_config_synthetic.py](../../../../../tests/experiment/test_x5g1t_config_synthetic.py)
- Kind: python
- Lines: 288

## Module docstring

> Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
> (docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
> modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
> full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
> Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.contracts.testing import tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 22, via package root)
- `from topo_pilot.experiment import x5g1t_lineage, x5g1t_train` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md), [src/topo_pilot/experiment/x5g1t_train.py](../../src/topo_pilot/experiment/x5g1t_train.py.md) (line 23, via package root)
- `from topo_pilot.experiment.x5g1t_fixture import E0, T0, _emission` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 24, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 25, via package root)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 8)
- `copy` (lines 10)
- `dataclasses` (lines 11)
- `hashlib` (lines 12)
- `importlib` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 15)
- `types` (lines 16)

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
- `SYN_TAMPER`

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
- **function `_mutate_npz`** [L194-199]: `def _mutate_npz(path: Path) -> None`
- **function `syn`** [L204-220]: `def syn(prod)` decorators: @pytest.fixture
- **test `test_synthetic_correct_config_passes_read_only`** [L223-226]: `def test_synthetic_correct_config_passes_read_only(syn)`
- **test `test_synthetic_each_violation_rejected`** [L268-271]: `def test_synthetic_each_violation_rejected(syn, case)` decorators: @pytest.mark.parametrize('case', sorted(SYN_TAMPER))
- **test `test_synthetic_production_source_id_rejected`** [L274-283]: `def test_synthetic_production_source_id_rejected(syn)` - The synthetic store holds the production world content under the production config, so
- **test `test_synthetic_source_payload_mutated_on_disk_rejected`** [L286-288]: `def test_synthetic_source_payload_mutated_on_disk_rejected(syn)`

