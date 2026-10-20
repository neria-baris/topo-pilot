# `tests/c1prime/test_a_release_meter.py`

- Source: [tests/c1prime/test_a_release_meter.py](../../../../../tests/c1prime/test_a_release_meter.py)
- Kind: python
- Lines: 263

## Module docstring

> Independent tests, author A (job 0026): the C1 release schema checks and the meter-binding
> rebindings (TEST_PLAN A-6, last two bullets; protocol sections 17 and 18 field 2; API.md
> sections 13 and 14).

## Imports

### Internal (repo files)

- `import c1_meter_bind` -> [tools/c1prime/c1_meter_bind.py](../../tools/c1prime/c1_meter_bind.py.md) (line 34, via sys.path edit)
- `import c1_release` -> [tools/c1prime/c1_release.py](../../tools/c1prime/c1_release.py.md) (line 35, via sys.path edit)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 36, via sys.path edit)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 37, via sys.path edit)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 38, via sys.path edit)

### External (third-party)

- `pytest` (lines 24)

### Standard library

- `__future__` (lines 15)
- `copy` (lines 17)
- `hashlib` (lines 18)
- `json` (lines 19)
- `pathlib` (lines 21)
- `sys` (lines 20)
- `types` (lines 22)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 30: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 32: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `BOUND`
- `BREAKS`
- `GIB`
- `HEAD`
- `JOB`
- `REPO`
- `SENTINEL`

## Classes and functions

- **function `sha`** [L45-46]: `def sha(path)`
- **function `put`** [L49-52]: `def put(path, text)`
- **function `ref`** [L55-56]: `def ref(path)`
- **function `world`** [L59-101]: `def world(tmp_path, stages=('oracle',))`
- **function `verify`** [L104-109]: `def verify(w, head=HEAD)`
- **test `test_release_constants`** [L112-114]: `def test_release_constants()`
- **test `test_valid_releases_verify`** [L118-121]: `def test_valid_releases_verify(tmp_path, stages)` decorators: @pytest.mark.parametrize('stages', [('oracle',), ('calibration', 'validation'), ('fresh',)])
- **function `_drop`** [L124-125]: `def _drop(key)`
- **test `test_each_broken_binding_is_refused`** [L151-155]: `def test_each_broken_binding_is_refused(tmp_path, name)` decorators: @pytest.mark.parametrize('name', sorted(BREAKS))
- **test `test_source_head_mismatch_is_refused`** [L158-160]: `def test_source_head_mismatch_is_refused(tmp_path)`
- **test `test_release_outside_the_dispatched_job_directory_is_refused`** [L163-167]: `def test_release_outside_the_dispatched_job_directory_is_refused(tmp_path)`
- **test `test_r3_needs_n_test_k_and_registry_v2`** [L171-176]: `def test_r3_needs_n_test_k_and_registry_v2(tmp_path, key)` decorators: @pytest.mark.parametrize('key', ['N_test', 'k', 'registry_v2'])
- **function `restore_meter`** [L187-190]: `def restore_meter(monkeypatch)` decorators: @pytest.fixture
- **test `test_bind_rebinds_every_module_level_name`** [L193-205]: `def test_bind_rebinds_every_module_level_name(tmp_path, restore_meter)`
- **test `test_k4_meter_bind_is_not_imported_by_the_c1_binding`** [L208-210]: `def test_k4_meter_bind_is_not_imported_by_the_c1_binding()`
- **function `usage_of`** [L213-219]: `def usage_of(free_c, free_x)`
- **test `test_disk_safe_stop_thresholds`** [L225-229]: `def test_disk_safe_stop_thresholds(free_c, free_x, stop)` decorators: @pytest.mark.parametrize('free_c, free_x, stop', [(2000000000, 30000000000, False), (1999999999, 30000000000, True), (2000000000, 29999999999, True), (10 ** 12, 10 ** 12, False)])
- **test `test_disk_safe_stop_fails_closed_on_unreadable_drive`** [L232-235]: `def test_disk_safe_stop_fails_closed_on_unreadable_drive()`
- **function `legacy`** [L241-242]: `def legacy(*args)`
- **test `test_limiter_checks_disk_every_eighth_poll_and_never_caps_cpu`** [L245-250]: `def test_limiter_checks_disk_every_eighth_poll_and_never_caps_cpu(tmp_path)`
- **test `test_limiter_kills_an_overdue_native_operation`** [L253-263]: `def test_limiter_kills_an_overdue_native_operation(tmp_path)`

