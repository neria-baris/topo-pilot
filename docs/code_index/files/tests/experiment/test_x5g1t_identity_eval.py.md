# `tests/experiment/test_x5g1t_identity_eval.py`

- Source: [tests/experiment/test_x5g1t_identity_eval.py](../../../../../tests/experiment/test_x5g1t_identity_eval.py)
- Kind: python
- Lines: 297

## Module docstring

> Independent input-identity regressions for X5 G1 API v4.1 in the evaluation paths (§D; §E items
> 3, 4 and the test-pool half of 5).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.experiment import x5g1t_stages, x5g1t_stages_eval` -> [src/topo_pilot/experiment/x5g1t_stages.py](../../src/topo_pilot/experiment/x5g1t_stages.py.md), [src/topo_pilot/experiment/x5g1t_stages_eval.py](../../src/topo_pilot/experiment/x5g1t_stages_eval.py.md) (line 21, via package root)
- `from topo_pilot.experiment.x4b import ReadThroughBackend` -> [src/topo_pilot/experiment/x4b.py](../../src/topo_pilot/experiment/x4b.py.md) (line 22, via package root)
- `from topo_pilot.experiment.x5g1t_checks import IntegrityFailed` -> [src/topo_pilot/experiment/x5g1t_checks.py](../../src/topo_pilot/experiment/x5g1t_checks.py.md) (line 23, via package root)
- `from topo_pilot.experiment.x5g1t_config import load_config, read_chain` -> [src/topo_pilot/experiment/x5g1t_config.py](../../src/topo_pilot/experiment/x5g1t_config.py.md) (line 24, via package root)
- `from topo_pilot.experiment.x5g1t_fixture import build_fixture` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 25, via package root)
- `from topo_pilot.experiment.x5g1t_lineage import CODES, MASTERS, TEST_MASTER, stream` -> [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md) (line 26, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `io` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 15)
- `shutil` (lines 14)

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

- `ARMS`
- `DEV_SUBSTITUTIONS`
- `FINAL_SUBSTITUTIONS`
- `REPO`
- `SIZES`
- `_REAL_GET`

## Classes and functions

- **class `_Reached(Exception)`** [L37-38] - Raised by a spy: the stage got past every check to the guarded call.
- **function `_clone`** [L43-49]: `def _clone(src: Path, dst: Path)`
- **function `_out`** [L52-53]: `def _out(root: Path, *parts: str) -> Path`
- **function `_pools`** [L56-57]: `def _pools(root: Path) -> dict`
- **function `_existing`** [L60-62]: `def _existing(root: Path, key: str) -> tuple[str, str]`
- **function `_remap`** [L65-75]: `def _remap(root: Path, cfg, changes: dict) -> None` - Point pools.json keys at ``(pool_id, sha)`` and recompute the COMPLETE manifest.
- **function `_reordered_ids`** [L78-92]: `def _reordered_ids(root: Path, key: str) -> tuple[str, str]` - Replace pool ``key`` in place (same id, same config and parents) by a checksum-valid copy
- **function `_old_ids_pool`** [L95-101]: `def _old_ids_pool(root: Path) -> str` - A tiny old-ID reference ObservationSet in the fixture read root (no ID overlap).
- **function `_payload`** [L104-105]: `def _payload(store_root: Path, aid: str) -> Path`
- **function `_mutate`** [L108-114]: `def _mutate(path: Path) -> None` - Reverse every array's rows: still loadable and valid, different payload checksum.
- **function `_watch`** [L117-132]: `def _watch(monkeypatch, target: Path, mutate: bool) -> dict` - Count backend reads of ``target``; with ``mutate``, change its bytes right after the first
- **function `_spy`** [L135-145]: `def _spy(monkeypatch, name: str, stop: bool = False) -> list`
- **function `_assert_no_result`** [L148-150]: `def _assert_no_result(root: Path, stage: str) -> None`
- **function `trained`** [L156-166]: `def trained(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `dev_done`** [L170-174]: `def dev_done(trained, tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_pools_collision_check_loads_the_old_id_store`** [L179-182]: `def test_pools_collision_check_loads_the_old_id_store(trained)`
- **test `test_pools_read_root_payload_mutated_after_load_refused`** [L185-193]: `def test_pools_read_root_payload_mutated_after_load_refused(tmp_path, monkeypatch)`
- **test `test_dev_analysis_control_reaches_oracle`** [L198-204]: `def test_dev_analysis_control_reaches_oracle(trained, tmp_path, monkeypatch)`
- **test `test_dev_analysis_mismatched_pool_never_scores`** [L217-225]: `def test_dev_analysis_mismatched_pool_never_scores(trained, tmp_path, monkeypatch, name)` decorators: @pytest.mark.parametrize('name', list(DEV_SUBSTITUTIONS))
- **test `test_final_test_control_draws_and_records_test_provenance`** [L230-249]: `def test_final_test_control_draws_and_records_test_provenance(dev_done, tmp_path, monkeypatch)`
- **test `test_final_test_prerequisite_identity_failure_never_draws`** [L260-270]: `def test_final_test_prerequisite_identity_failure_never_draws(dev_done, tmp_path, monkeypatch, name)` decorators: @pytest.mark.parametrize('name', list(FINAL_SUBSTITUTIONS))
- **test `test_final_test_collision_input_mutated_after_load_refused`** [L276-297]: `def test_final_test_collision_input_mutated_after_load_refused(dev_done, tmp_path, monkeypatch, target)` decorators: @pytest.mark.parametrize('target', ['read_root_old_ids', f'train:a0:{M1}', f'dev:a020:{M2}']) - The collision check runs before the fresh draw (§D), so the bytes are changed when the

