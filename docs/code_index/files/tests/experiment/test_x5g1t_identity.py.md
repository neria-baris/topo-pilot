# `tests/experiment/test_x5g1t_identity.py`

- Source: [tests/experiment/test_x5g1t_identity.py](../../../../../tests/experiment/test_x5g1t_identity.py)
- Kind: python
- Lines: 331

## Module docstring

> Independent pool input-identity regressions for X5 G1 API v4.1 (§A, §B, §D; §E items 1, 2, 5).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 19, via package root)
- `from topo_pilot.experiment import x5g1t_stages` -> [src/topo_pilot/experiment/x5g1t_stages.py](../../src/topo_pilot/experiment/x5g1t_stages.py.md) (line 20, via package root)
- `from topo_pilot.experiment.x4b import ReadThroughBackend` -> [src/topo_pilot/experiment/x4b.py](../../src/topo_pilot/experiment/x4b.py.md) (line 21, via package root)
- `from topo_pilot.experiment.x5g1t_checks import IntegrityFailed, validate_pool` -> [src/topo_pilot/experiment/x5g1t_checks.py](../../src/topo_pilot/experiment/x5g1t_checks.py.md) (line 22, via package root)
- `from topo_pilot.experiment.x5g1t_config import load_config, read_chain` -> [src/topo_pilot/experiment/x5g1t_config.py](../../src/topo_pilot/experiment/x5g1t_config.py.md) (line 23, via package root)
- `from topo_pilot.experiment.x5g1t_fixture import build_fixture` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 24, via package root)
- `from topo_pilot.experiment.x5g1t_lineage import CODES, MASTERS, PROTOCOL, pool_config, sequence_ids, stream, study_pool_config` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md) (line 25, via package root)
- `from topo_pilot.experiment.x5g1t_main import main` -> [src/topo_pilot/experiment/x5g1t_main.py](../../src/topo_pilot/experiment/x5g1t_main.py.md) (line 34, via package root)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `shutil` (lines 13)

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

- `REPO`
- `SIZES`
- `SUBSTITUTIONS`
- `V`

## Classes and functions

- **class `_Reached(Exception)`** [L44-45] - Raised by a spy: the stage got past every check to the guarded call.
- **function `_clone`** [L50-68]: `def _clone(src: Path, dst: Path) -> Path` - Copy a fixture root and re-point its config's absolute paths at the copy.
- **function `_out`** [L71-72]: `def _out(root: Path, *parts: str) -> Path`
- **function `_pools`** [L75-76]: `def _pools(root: Path) -> dict`
- **function `_store`** [L79-82]: `def _store(root: Path) -> ArtifactStore` - Writes into the study store; parents resolve through the fixture's read root.
- **function `_remap`** [L85-95]: `def _remap(root: Path, cfg, changes: dict) -> None` - Point pools.json keys at ``(pool_id, sha)`` and recompute the COMPLETE manifest.
- **function `_existing`** [L98-100]: `def _existing(root: Path, key: str) -> tuple[str, str]`
- **function `_resave`** [L103-117]: `def _resave(root: Path, key: str, *, config=None, parents=None, obs=None) -> tuple[str, str]` - Save a checksum-valid variant of pool ``key``. With only ``obs`` changed the artifact id
- **function `_expected_config`** [L120-124]: `def _expected_config(split: str, arm: str, master, protocol: str) -> dict` - §A, written out literally.
- **function `_parents`** [L127-128]: `def _parents(cfg, arm: str) -> tuple`
- **function `_train_spy`** [L131-139]: `def _train_spy(monkeypatch) -> list`
- **function `_assert_no_train_export`** [L142-145]: `def _assert_no_train_export(root: Path, arm: str, master) -> None`
- **function `pools_root`** [L151-155]: `def pools_root(tmp_path_factory) -> Path` decorators: @pytest.fixture(scope='module')
- **function `clone`** [L159-161]: `def clone(pools_root, tmp_path)` decorators: @pytest.fixture
- **test `test_untouched_fixture_reaches_train_one_with_intended_pools`** [L166-172]: `def test_untouched_fixture_reaches_train_one_with_intended_pools(clone, monkeypatch)`
- **test `test_root_wrong_arm_train_pool_refused_before_train_one`** [L175-182]: `def test_root_wrong_arm_train_pool_refused_before_train_one(clone, monkeypatch)`
- **test `test_root_wrong_arm_cli_exits_3`** [L185-193]: `def test_root_wrong_arm_cli_exits_3(clone, monkeypatch)`
- **function `_swap_train_dev`** [L198-200]: `def _swap_train_dev(root, cfg)`
- **function `_cfg_variant`** [L203-208]: `def _cfg_variant(edit)`
- **function `_parents_variant`** [L211-214]: `def _parents_variant(pick)`
- **function `_obs_variant`** [L217-227]: `def _obs_variant(edit)`
- **test `test_valid_substitution_refused_before_train_one`** [L266-273]: `def test_valid_substitution_refused_before_train_one(clone, monkeypatch, name)` decorators: @pytest.mark.parametrize('name', list(SUBSTITUTIONS))
- **test `test_obs_variant_helper_is_a_faithful_copy`** [L276-283]: `def test_obs_variant_helper_is_a_faithful_copy(clone, monkeypatch)` - Control for the content variants: a re-save with nothing changed still trains.
- **test `test_validate_pool_accepts_intended_and_refuses_others`** [L288-300]: `def test_validate_pool_accepts_intended_and_refuses_others(clone)`
- **test `test_study_pool_config_is_exactly_section_a`** [L305-313]: `def test_study_pool_config_is_exactly_section_a(clone)`
- **test `test_new_pools_record_lineage_and_execution_protocol`** [L316-331]: `def test_new_pools_record_lineage_and_execution_protocol(pools_root)`

