# `tests/hwsg/test_b_train_meter.py`

- Source: [tests/hwsg/test_b_train_meter.py](../../../../../tests/hwsg/test_b_train_meter.py)
- Kind: python
- Lines: 97

## Module docstring

> Author B: training children, meter caps, ledgers, basetemps (G7, 10.3, DRG12, DRG13, KG4).

## Imports

### Internal (repo files)

- `from test_b_common import GIB, mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 11, via same directory)

### External (third-party)

- `pytest` (lines 8)

### Standard library

- `__future__` (lines 2)
- `json` (lines 4)
- `pathlib` (lines 6)
- `sys` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 10: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- `THREADS`

## Classes and functions

- **test `test_child_env_one_thread_and_temp_under_out`** [L16-23]: `def test_child_env_one_thread_and_temp_under_out(tmp_path)`
- **test `test_child_env_distinct_per_job`** [L26-29]: `def test_child_env_distinct_per_job(tmp_path)`
- **test `test_child_argv_names_world_master_and_attempt`** [L32-39]: `def test_child_argv_names_world_master_and_attempt(tmp_path)`
- **test `test_ram_ok_threshold`** [L42-47]: `def test_ram_ok_threshold()`
- **function `_child_records`** [L50-56]: `def _child_records(wd, tag, job, statuses)`
- **test `test_aggregate_one_ledger_entry_per_child_with_unique_labels`** [L59-73]: `def test_aggregate_one_ledger_entry_per_child_with_unique_labels(tmp_path)`
- **test `test_meter_caps_and_output_caps`** [L76-84]: `def test_meter_caps_and_output_caps()`
- **test `test_basetemp_and_tmp_outside_project_root`** [L87-92]: `def test_basetemp_and_tmp_outside_project_root(tmp_path)`
- **test `test_no_array_or_hist_name_inside_project_tests_dir`** [L95-97]: `def test_no_array_or_hist_name_inside_project_tests_dir()`

