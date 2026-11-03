# `tests/hwsu/test_b_of_records.py`

- Source: [tests/hwsu/test_b_of_records.py](../../../../../tests/hwsu/test_b_of_records.py)
- Kind: python
- Lines: 306

## Module docstring

> Author B (job 0198): the gate runner, status mapping, stage events, lineage, the study ledger
> and pauses (protocol §4.1, §6 convention, §10.2-§10.3; API §5.1-§5.2). TEST_PLAN §3 row
> test_b_of_records (the freeze and OF-B parts are in test_b_of_freeze.py). tmp_path only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 21, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 22, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 23, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 12)
- `hashlib` (lines 7)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 13)
- `sys` (lines 10)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `C`
- `EXEMPT`
- `REPO`

## Classes and functions

- **function `_lines`** [L30-32]: `def _lines(p) -> list`
- **function `_sha`** [L35-36]: `def _sha(p) -> str`
- **test `test_status_of_mapping`** [L40-49]: `def test_status_of_mapping()`
- **function `_steps`** [L53-61]: `def _steps(calls, spec)`
- **test `test_run_gates_stops_after_failure`** [L64-75]: `def test_run_gates_stops_after_failure(tmp_path)`
- **test `test_run_gates_share_dropped_continues`** [L78-85]: `def test_run_gates_share_dropped_continues(tmp_path)`
- **test `test_run_gates_inconclusive_stops`** [L88-92]: `def test_run_gates_inconclusive_stops(tmp_path)`
- **test `test_run_gates_dry_continue_calls_every_fn`** [L95-102]: `def test_run_gates_dry_continue_calls_every_fn(tmp_path)`
- **test `test_run_gates_pause_recorded_then_reraised`** [L105-112]: `def test_run_gates_pause_recorded_then_reraised(tmp_path)`
- **test `test_run_gates_details_json_safe_and_reason_capped`** [L115-125]: `def test_run_gates_details_json_safe_and_reason_capped(tmp_path)`
- **test `test_contract_gate_order_and_continuing`** [L128-135]: `def test_contract_gate_order_and_continuing()`
- **test `test_begin_and_complete_stage`** [L139-155]: `def test_begin_and_complete_stage(tmp_path)`
- **function `_store`** [L159-165]: `def _store(tmp_path)`
- **test `test_lineage_absent_and_recorded`** [L168-172]: `def test_lineage_absent_and_recorded(tmp_path)`
- **test `test_lineage_exemptions`** [L184-191]: `def test_lineage_exemptions(tmp_path)`
- **test `test_lineage_unrecorded_file`** [L196-203]: `def test_lineage_unrecorded_file(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['stages/OF/ORACLE_x.npz', 'stages/OF/OF_REPORT.json', 'NOTES.json', 'reservations/sub/x.json', 'stages/OF/HIST_OF_fit_b0.npz'])
- **test `test_lineage_changed_recorded_file`** [L206-211]: `def test_lineage_changed_recorded_file(tmp_path)`
- **test `test_lineage_superseded`** [L214-224]: `def test_lineage_superseded(tmp_path)`
- **test `test_central_and_cumulative`** [L228-236]: `def test_central_and_cumulative()`
- **test `test_ledger_read_absent`** [L239-241]: `def test_ledger_read_absent(tmp_path)`
- **test `test_ledger_append_unique_atomic`** [L244-264]: `def test_ledger_append_unique_atomic(tmp_path, monkeypatch)`
- **test `test_pause_check_thresholds_strict`** [L269-276]: `def test_pause_check_thresholds_strict(stage, s_th, c_th)` decorators: @pytest.mark.parametrize('stage,s_th,c_th', [('J-OF', 2700, 2700), ('DRO', 600, 3300), ('OF', 2100, 5400)])
- **test `test_running_cpu`** [L279-284]: `def test_running_cpu(tmp_path)`
- **test `test_pause_or_raise_disabled_without_ledger`** [L287-289]: `def test_pause_or_raise_disabled_without_ledger(tmp_path)`
- **test `test_pause_or_raise_records_cpu_fields_only`** [L292-306]: `def test_pause_or_raise_records_cpu_fields_only(tmp_path)`

