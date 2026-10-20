# `tests/experiment/test_x5g1t_integration.py`

- Source: [tests/experiment/test_x5g1t_integration.py](../../../../../tests/experiment/test_x5g1t_integration.py)
- Kind: python
- Lines: 393

## Module docstring

> Independent integration regressions for the X5 G1 v4 stage integration (API v4 §2, §4, §6, §7).

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x5g1t_exports, x5g1t_lineage, x5g1t_runtime, x5g1t_stages_eval` -> [src/topo_pilot/experiment/x5g1t_exports.py](../../src/topo_pilot/experiment/x5g1t_exports.py.md), [src/topo_pilot/experiment/x5g1t_lineage.py](../../src/topo_pilot/experiment/x5g1t_lineage.py.md), [src/topo_pilot/experiment/x5g1t_runtime.py](../../src/topo_pilot/experiment/x5g1t_runtime.py.md), [src/topo_pilot/experiment/x5g1t_stages_eval.py](../../src/topo_pilot/experiment/x5g1t_stages_eval.py.md) (line 19, via package root)
- `from topo_pilot.experiment.x5g1t_exports import ExportIncomplete, verify_export_complete` -> [src/topo_pilot/experiment/x5g1t_exports.py](../../src/topo_pilot/experiment/x5g1t_exports.py.md) (line 20, via package root)
- `from topo_pilot.experiment.x5g1t_fixture import build_fixture` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 21, via package root)
- `from topo_pilot.experiment.x5g1t_main import main` -> [src/topo_pilot/experiment/x5g1t_main.py](../../src/topo_pilot/experiment/x5g1t_main.py.md) (line 22, via package root)

### External (third-party)

- `pytest` (lines 17)

### Standard library

- `__future__` (lines 8)
- `hashlib` (lines 10)
- `json` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 15)
- `shutil` (lines 13)
- `types` (lines 14)

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
- `_REAL_DUMPS`

## Classes and functions

- **function `_cli`** [L32-33]: `def _cli(cfg, *args) -> int`
- **function `_tables`** [L36-37]: `def _tables(root: Path) -> Path`
- **function `_ledger_last`** [L40-41]: `def _ledger_last(root: Path) -> dict`
- **function `_snapshot`** [L44-52]: `def _snapshot(root: Path) -> dict`
- **function `_clone`** [L55-73]: `def _clone(src: Path, dst: Path) -> Path` - Copy a fixture root and re-point its config's absolute paths at the copy.
- **function `_on_first_export_write`** [L76-88]: `def _on_first_export_write(monkeypatch, action)` - Run ``action`` while the first export file is being serialised (the write in flight).
- **function `_write_json`** [L91-92]: `def _write_json(path: Path, obj) -> None`
- **function `pools_root`** [L98-102]: `def pools_root(tmp_path_factory) -> Path` decorators: @pytest.fixture(scope='module')
- **function `trained_root`** [L106-112]: `def trained_root(pools_root, tmp_path_factory) -> Path` decorators: @pytest.fixture(scope='module')
- **function `dev_done`** [L116-141]: `def dev_done(trained_root, tmp_path_factory)` decorators: @pytest.fixture(scope='module') - dev-analysis on a clone of the trained state, with the oracle/score guards recorded.
- **function `_stop_worker_control`** [L146-147]: `def _stop_worker_control(mb: Path)`
- **function `_stop_request`** [L150-151]: `def _stop_request(mb: Path)`
- **function `_stop_file`** [L154-155]: `def _stop_file(mb: Path)`
- **function `_clear_stops`** [L158-162]: `def _clear_stops(mb: Path)`
- **test `test_stop_during_pools_export_writes_no_further_file`** [L167-190]: `def test_stop_during_pools_export_writes_no_further_file(tmp_path, monkeypatch, caplog, source)` decorators: @pytest.mark.parametrize('source', [_stop_worker_control, _stop_request, _stop_file], ids=['worker_control', 'request', 'stop_file'])
- **test `test_hold_released_by_sleep_completes`** [L196-222]: `def test_hold_released_by_sleep_completes(tmp_path, monkeypatch, when)` decorators: @pytest.mark.parametrize('when', ['stage_start', 'during_export'])
- **function `_draw_spy`** [L227-236]: `def _draw_spy(monkeypatch)`
- **function `_final_done`** [L239-240]: `def _final_done(root: Path) -> bool`
- **test `test_final_test_control_draws_once`** [L243-251]: `def test_final_test_control_draws_once(dev_done, tmp_path, monkeypatch)` - Positive control: the draw spy sees the fresh draw when nothing stops it.
- **test `test_stop_before_fresh_draw_never_draws`** [L254-263]: `def test_stop_before_fresh_draw_never_draws(dev_done, tmp_path, monkeypatch)`
- **test `test_stop_during_collision_check_never_draws`** [L266-283]: `def test_stop_during_collision_check_never_draws(dev_done, tmp_path, monkeypatch)` - The STOP appears after the stage started, while the fresh IDs are being planned.
- **test `test_fresh_id_collision_refuses_without_draw`** [L286-303]: `def test_fresh_id_collision_refuses_without_draw(dev_done, tmp_path, monkeypatch, caplog)`
- **test `test_dev_analysis_calls_batch_and_oracle_guards`** [L308-321]: `def test_dev_analysis_calls_batch_and_oracle_guards(dev_done)`
- **test `test_scoring_guard_is_a_real_boundary`** [L324-344]: `def test_scoring_guard_is_a_real_boundary(trained_root, tmp_path, monkeypatch)` - A STOP that appears at 'score batch 1' stops dev-analysis with no result export.
- **test `test_tampered_pools_export_refuses_train`** [L350-365]: `def test_tampered_pools_export_refuses_train(pools_root, tmp_path, caplog, tamper)` decorators: @pytest.mark.parametrize('tamper', ['mutate_pools_json', 'extra_file'])
- **test `test_extra_file_in_train_export_refuses_dev_analysis`** [L368-378]: `def test_extra_file_in_train_export_refuses_dev_analysis(trained_root, tmp_path, caplog)`
- **test `test_validate_is_read_only`** [L383-393]: `def test_validate_is_read_only(tmp_path, capsys)`

