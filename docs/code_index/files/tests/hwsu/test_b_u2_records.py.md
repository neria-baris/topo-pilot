# `tests/hwsu/test_b_u2_records.py`

- Source: [tests/hwsu/test_b_u2_records.py](../../../../../tests/hwsu/test_b_u2_records.py)
- Kind: python
- Lines: 289

## Module docstring

> Author B (job 0223, phase 2): sealing, records, obligations, reservations, meter binding and
> basetemps (API_U2 4.7, 4.9, 5, 9; R-0213-2; TEST_PLAN_U2 row test_b_u2_records). Everything under
> tmp_path; meter attributes are restored by monkeypatch and the meter itself is never started.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 18, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 19, via sys.path edit)
- `from c1_means import tree_mean` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 20, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 21, via unique basename)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 220, via unique basename) (inside a function)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 221, via unique basename) (inside a function)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 222, via unique basename) (inside a function)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 223, via unique basename) (inside a function)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 238, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 12)
- `pytest` (lines 13)

### Standard library

- `__future__` (lines 5)
- `hashlib` (lines 69)
- `importlib` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 30: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 31: `hwsu_gates` -> [tools/hwsu/u2/hwsu_gates.py](../../tools/hwsu/u2/hwsu_gates.py.md)
- `import_module` line 35: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 36: `hwsu_driver` -> [tools/hwsu/u2/hwsu_driver.py](../../tools/hwsu/u2/hwsu_driver.py.md)
- `import_module` line 40: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 41: `hwsu_dry2` -> [tools/hwsu/u2/hwsu_dry2.py](../../tools/hwsu/u2/hwsu_dry2.py.md)
- `import_module` line 121: `dynamic: mod`
- `import_module` line 122: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 123: `hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](../../tools/hwsu/u2/hwsu_known.py.md)
- `import_module` line 192: `hwsu_meter_bind` -> [tools/hwsu/hwsu_meter_bind.py](../../tools/hwsu/hwsu_meter_bind.py.md)
- `import_module` line 203: `hwsu_meter_bind` -> [tools/hwsu/hwsu_meter_bind.py](../../tools/hwsu/hwsu_meter_bind.py.md)

### sys.path additions

- line 16: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `GIB`
- `PROTO`
- `REPO`
- `ROOT`
- `SCRATCH`
- `SEALED`

## Classes and functions

- **function `_gates`** [L29-31]: `def _gates()`
- **function `_drv`** [L34-36]: `def _drv()`
- **function `_dry2`** [L39-41]: `def _dry2()`
- **function `_fail`** [L44-47]: `def _fail(fn, *a, **k)`
- **function `_arrays`** [L51-60]: `def _arrays()`
- **test `test_write_sealed_u_exclusive_once_with_protocol_sha_and_means_only`** [L63-81]: `def test_write_sealed_u_exclusive_once_with_protocol_sha_and_means_only(tmp_path)`
- **test `test_write_sealed_u_second_call_never_overwrites`** [L84-91]: `def test_write_sealed_u_second_call_never_overwrites(tmp_path)`
- **test `test_sealed_keys_u_constant`** [L98-99]: `def test_sealed_keys_u_constant()`
- **test `test_check_unsealed_u_refuses_each_key_at_any_depth`** [L103-107]: `def test_check_unsealed_u_refuses_each_key_at_any_depth(key)` decorators: @pytest.mark.parametrize('key', SEALED)
- **test `test_share_dropped_returns_not_run_and_computes_nothing`** [L111-113]: `def test_share_dropped_returns_not_run_and_computes_nothing()`
- **test `test_share_family_and_share_only_names_fail_closed`** [L116-124]: `def test_share_family_and_share_only_names_fail_closed()`
- **test `test_run_gates_u_continues_through_share_dropped`** [L127-138]: `def test_run_gates_u_continues_through_share_dropped(tmp_path)`
- **test `test_phase2_arrays_use_phase1_prefixes_and_obligation_lists_them`** [L142-158]: `def test_phase2_arrays_use_phase1_prefixes_and_obligation_lists_them(tmp_path)`
- **test `test_drawing_job_stopped_before_first_row_ends_reservation_and_reruns_on_a2`** [L161-177]: `def test_drawing_job_stopped_before_first_row_ends_reservation_and_reruns_on_a2(tmp_path)`
- **test `test_memory_cap_u2`** [L183-184]: `def test_memory_cap_u2(stage, cap)` decorators: @pytest.mark.parametrize('stage,cap', [('KC', 12), ('E1', 12), ('REG2', 12), ('E2', 12), ('J-U', 8), ('DRU', 8)])
- **test `test_memory_cap_u2_unknown_stage_and_phase1_cap_still_refuses`** [L187-194]: `def test_memory_cap_u2_unknown_stage_and_phase1_cap_still_refuses()`
- **test `test_job_paths_u2_dru_test_store`** [L197-207]: `def test_job_paths_u2_dru_test_store()`
- **test `test_dru_paths_lie_outside_the_project_root`** [L210-215]: `def test_dru_paths_lie_outside_the_project_root()`
- **function `_guard_attrs`** [L219-232]: `def _guard_attrs(monkeypatch)`
- **test `test_meter_main_sets_u2_memory_cap_and_measure_only_argv`** [L236-253]: `def test_meter_main_sets_u2_memory_cap_and_measure_only_argv(stage, cap, monkeypatch, tmp_path)` decorators: @pytest.mark.parametrize('stage,cap', [('DRU', 8), ('J-U', 8)])
- **test `test_meter_main_refuses_unknown_kind_stage_or_missing_flags`** [L260-269]: `def test_meter_main_refuses_unknown_kind_stage_or_missing_flags(monkeypatch, argv)` decorators: @pytest.mark.parametrize('argv', [['--job', '0223tb', '--task-sha256', 'a', '--session', 's', '--kind', 'bogus', '--stage', 'E1'], ['--job', '0223tb', '--task-sha256', 'a', '--session', 's', '--kind', 'store', '--stage', 'ZZ'], ['--job', '0223tb']])
- **test `test_no_pause_line_in_u2_contract_jobs`** [L272-275]: `def test_no_pause_line_in_u2_contract_jobs()` - Addenda 41-43: no pause check; the phase-2 job table names no PAUSE gate.
- **test `test_run_dru_refuses_out_under_the_project_root`** [L279-284]: `def test_run_dru_refuses_out_under_the_project_root(tmp_path)`
- **test `test_run_dru_refuses_out_not_named_like_a_dry_store`** [L287-289]: `def test_run_dru_refuses_out_not_named_like_a_dry_store(tmp_path)`

