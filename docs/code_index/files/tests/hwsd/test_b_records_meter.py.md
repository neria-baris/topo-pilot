# `tests/hwsd/test_b_records_meter.py`

- Source: [tests/hwsd/test_b_records_meter.py](../../../../../tests/hwsd/test_b_records_meter.py)
- Kind: python
- Lines: 371

## Module docstring

> Author B: lineage, AUTH, H-1 records, ledger, pauses, archive, meter binding (§2.7, §7, §11).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 16, via sys.path edit)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](../../tools/hwsd/hwsd_records.py.md) (line 17, via sys.path edit)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](../../tools/hwsd/hwsd_score.py.md) (line 18, via sys.path edit)
- `import hwsd_meter_bind` -> [tools/hwsd/hwsd_meter_bind.py](../../tools/hwsd/hwsd_meter_bind.py.md) (line 19, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 20, via same directory)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../../tools/c1prime/c1_chart.py.md) (line 22, via unique basename)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 23, via unique basename)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../../tools/hwsb/hwsb_driver.py.md) (line 24, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 25, via unique basename)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 26, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 27, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 28, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 30, via unique basename)
- `import hwsd_driver` -> [tools/hwsd/hwsd_driver.py](../../tools/hwsd/hwsd_driver.py.md) (line 274, via sys.path edit) (inside a function)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](../../tools/hwsd/hwsd_readers.py.md) (line 275, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 29)

### Standard library

- `__future__` (lines 3)
- `json` (lines 5)
- `math` (lines 6)
- `os` (lines 7)
- `pathlib` (lines 10)
- `shutil` (lines 112)
- `sys` (lines 8)
- `tempfile` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 14: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `A37`
- `METER_ATTRS`

## Classes and functions

- **function `_recorded_store`** [L36-42]: `def _recorded_store(tmp_path) -> Path`
- **test `test_lineage_d`** [L45-64]: `def test_lineage_d(tmp_path, monkeypatch)`
- **test `test_lineage_d_foreign_reservation_name`** [L69-74]: `def test_lineage_d_foreign_reservation_name(tmp_path, name)` decorators: @pytest.mark.parametrize('name', ['RES-HWSC-W2.json', 'RES-HWSD-W2.json', 'RES-HWSD-W2-a1.txt', 'notes.json', 'RES-HWSU-OF-a1.json'])
- **test `test_archive_attempt_and_superseded_sums`** [L77-96]: `def test_archive_attempt_and_superseded_sums(tmp_path)`
- **test `test_archived_wall_record_and_newest_attempt`** [L99-116]: `def test_archived_wall_record_and_newest_attempt(tmp_path)`
- **test `test_auth_ok_d`** [L119-129]: `def test_auth_ok_d()`
- **test `test_no_value_check_refuses`** [L135-138]: `def test_no_value_check_refuses(obj)` decorators: @pytest.mark.parametrize('obj', [{'a': {'b': {'mean': 1}}}, [{'x': [{'L': 0.1}]}], ({'k': ({'captured': 0.9},)},), {'a': [{'b': {'max_B': '1'}}]}, {'statuses': []}, {'x': {'sigma': 'SUPPORT'}}])
- **test `test_no_value_check_passes_clean`** [L141-143]: `def test_no_value_check_passes_clean()`
- **function `_acc`** [L146-153]: `def _acc(**over)`
- **test `test_acceptance_check`** [L156-173]: `def test_acceptance_check()`
- **test `test_score_acceptance_record`** [L176-201]: `def test_score_acceptance_record(tmp_path)`
- **test `test_ledger`** [L204-225]: `def test_ledger(tmp_path)`
- **test `test_centrals`** [L228-234]: `def test_centrals()`
- **test `test_pause_check_d`** [L237-248]: `def test_pause_check_d(monkeypatch)`
- **test `test_pause_or_raise_d`** [L251-270]: `def test_pause_or_raise_d(tmp_path, monkeypatch)`
- **test `test_run_close_writes_its_obligation`** [L273-286]: `def test_run_close_writes_its_obligation(tmp_path)`
- **function `meter_state`** [L296-303]: `def meter_state(monkeypatch)` decorators: @pytest.fixture
- **test `test_bind_per_stage`** [L308-318]: `def test_bind_per_stage(tmp_path, meter_state, stage, gib)` decorators: @pytest.mark.parametrize('stage,gib', [('J-D1', 8), ('DRY', 12), ('KD', 12), ('SAMPLE', 12), ('SCORE', 8), ('SUMMARY', 8)])
- **test `test_bind_unknown_stage_and_temp_root`** [L321-331]: `def test_bind_unknown_stage_and_temp_root(tmp_path, meter_state)`
- **test `test_job_paths_and_placement`** [L334-354]: `def test_job_paths_and_placement()`
- **test `test_this_suite_runs_outside_the_project`** [L357-360]: `def test_this_suite_runs_outside_the_project(tmp_path)`
- **test `test_meter_main_refuses_bad_arguments`** [L369-371]: `def test_meter_main_refuses_bad_arguments(monkeypatch, meter_state, argv)` decorators: @pytest.mark.parametrize('argv', [['--job', '0197', '--task-sha256', 'ab' * 32, '--session', 's', '--kind', 'test'], ['--job', '0197', '--task-sha256', 'ab' * 32, '--session', 's', '--kind', 'test', '--stage', 'BOGUS'], ['--job', '0197', '--task-sha256', 'ab' * 32, '--session', 's', '--kind', 'elsewhere', '--stage', 'DRY']])

