# `tests/experiment/test_runner.py`

- Source: [tests/experiment/test_runner.py](../../../../../tests/experiment/test_runner.py)
- Kind: python
- Lines: 152

## Module docstring

> Runner contracts: gate requirements (X02), idempotent re-runs, prereg refusal (X07).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, ErrorCode, GateCheck, GateReport, LocalFSBackend, MetricRecords, MetricRow, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.experiment import load_config, run_stage` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 19, via package root)
- `from topo_pilot.experiment.config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](../../src/topo_pilot/experiment/config.py.md) (line 20, via package root)
- `from topo_pilot.experiment.prereg import write_prereg` -> [src/topo_pilot/experiment/prereg.py](../../src/topo_pilot/experiment/prereg.py.md) (line 21, via package root)
- `from topo_pilot.experiment.s3 import TrainingRun, activation_ids` -> [src/topo_pilot/experiment/s3.py](../../src/topo_pilot/experiment/s3.py.md) (line 22, via package root)
- `from topo_pilot.experiment.s4_analysis import _row` -> [src/topo_pilot/experiment/s4_analysis.py](../../src/topo_pilot/experiment/s4_analysis.py.md) (line 23, via package root)
- `from topo_pilot.experiment.stages import latest_gate_verdicts, save_tool_gate, tool_line` -> [src/topo_pilot/experiment/stages.py](../../src/topo_pilot/experiment/stages.py.md) (line 24, via package root)

### External (third-party)

- `pytest` (lines 6)

### Standard library

- `json` (lines 2)
- `math` (lines 3)
- `pathlib` (lines 4)

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

## Classes and functions

- **function `store`** [L32-33]: `def store(tmp_path)` decorators: @pytest.fixture
- **function `cfg`** [L37-38]: `def cfg()` decorators: @pytest.fixture
- **function `_gate`** [L41-53]: `def _gate(store, stage, gate_id, verdict, created=None, tag='')`
- **test `test_X02_required_stage_needs_every_gate`** [L56-63]: `def test_X02_required_stage_needs_every_gate(store, cfg)`
- **test `test_X02_missing_gate_blocks`** [L66-70]: `def test_X02_missing_gate_blocks(store, cfg)`
- **test `test_latest_report_per_gate_wins`** [L73-76]: `def test_latest_report_per_gate_wins(store)`
- **test `test_waiver_in_the_same_second_as_a_failure_counts`** [L79-82]: `def test_waiver_in_the_same_second_as_a_failure_counts(store)`
- **test `test_tool_line_strips_pytest_wall_time`** [L92-93]: `def test_tool_line_strips_pytest_wall_time(raw, line)` decorators: @pytest.mark.parametrize('raw, line', [('95 passed in 3.73s', '95 passed'), ('x\n363 passed, 5 deselected in 113.08s (0:01:53)\n', '363 passed, 5 deselected'), ('===== 2 failed, 3 passed in 1.2s =====', '2 failed, 3 passed'), ('check_imports: ok (91 files)', 'check_imports: ok (91 files)'), ('', '')])
- **test `test_tool_gate_rerun_never_collides`** [L96-101]: `def test_tool_gate_rerun_never_collides(store)`
- **test `test_activation_ids_missing_run_is_empty_not_an_error`** [L104-106]: `def test_activation_ids_missing_run_is_empty_not_an_error(store)`
- **test `test_nonfinite_analysis_value_is_stored_as_inconclusive`** [L109-113]: `def test_nonfinite_analysis_value_is_stored_as_inconclusive(store)`
- **function `_timing_record`** [L116-125]: `def _timing_record(store, run_key, ckpt, wall)`
- **function `_ckpt`** [L128-130]: `def _ckpt(store, tag)`
- **test `test_stored_timing_is_read_from_a_record_of_the_same_checkpoints`** [L133-143]: `def test_stored_timing_is_read_from_a_record_of_the_same_checkpoints(store, cfg)`
- **test `test_X07_prereg_refuses_to_overwrite`** [L146-152]: `def test_X07_prereg_refuses_to_overwrite(store, tmp_path)`

