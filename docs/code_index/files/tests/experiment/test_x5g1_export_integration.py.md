# `tests/experiment/test_x5g1_export_integration.py`

- Source: [tests/experiment/test_x5g1_export_integration.py](../../../../../tests/experiment/test_x5g1_export_integration.py)
- Kind: python
- Lines: 272

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_REPAIR_API.md §4 before
> reading the implementation.

## Imports

### Internal (repo files)

- `import topo_pilot.contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 18, via package root)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, ObservationSet, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 19, via package root)
- `from topo_pilot.experiment.x5g1_controls import LedgerCorrupt, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 26, via package root)
- `from topo_pilot.experiment.x5g1_main import _export` -> [src/topo_pilot/experiment/x5g1_main.py](../../src/topo_pilot/experiment/x5g1_main.py.md) (line 27, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 9)
- `contextlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 13)

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

- `INVALID_LEDGERS`
- `REPO`
- `TABLE_FILES`
- `_OK_ENTRY`

## Classes and functions

- **function `_spec`** [L38-39]: `def _spec() -> TransitionSpec`
- **function `_obs`** [L42-45]: `def _obs(offset: int) -> ObservationSet`
- **function `_build_main`** [L48-59]: `def _build_main(main_root: Path) -> dict` - Lawful parents in a LocalFS main store; returns the ids used by ``res``.
- **function `_res`** [L62-73]: `def _res(ids: dict, global_failed=None) -> dict`
- **function `env`** [L77-100]: `def env(tmp_path, monkeypatch)` decorators: @pytest.fixture() - Main store, output dirs, controls paths, and a counting spy on ArtifactStore.save.
- **function `_ctl`** [L103-104]: `def _ctl(env) -> RunControls`
- **function `_last_entry`** [L107-108]: `def _last_entry(env) -> dict`
- **function `_status`** [L111-112]: `def _status(env) -> dict`
- **function `_metric_dir`** [L115-116]: `def _metric_dir(env) -> Path`
- **function `_metric_ids`** [L119-121]: `def _metric_ids(env) -> list[str]`
- **function `_expected_parents`** [L124-125]: `def _expected_parents(ids: dict) -> set[str]`
- **test `test_stop_before_export_saves_nothing`** [L131-146]: `def test_stop_before_export_saves_nothing(env)`
- **test `test_normal_export_single_save_and_manifest`** [L149-174]: `def test_normal_export_single_save_and_manifest(env)`
- **test `test_stop_created_during_save_skips_remaining_steps`** [L177-194]: `def test_stop_created_during_save_skips_remaining_steps(env)`
- **test `test_global_failed_writes_tables_without_save`** [L197-207]: `def test_global_failed_writes_tables_without_save(env)`
- **test `test_missing_parent_id_gives_no_save`** [L210-220]: `def test_missing_parent_id_gives_no_save(env)`
- **test `test_invalid_ledger_raises_at_construction_and_keeps_bytes`** [L242-250]: `def test_invalid_ledger_raises_at_construction_and_keeps_bytes(tmp_path, text)` decorators: @pytest.mark.parametrize('text', list(INVALID_LEDGERS.values()), ids=list(INVALID_LEDGERS))
- **test `test_valid_ledger_survives_run_that_raises`** [L253-272]: `def test_valid_ledger_survives_run_that_raises(tmp_path)`

