# `tests/hwsu/test_b_of_meter.py`

- Source: [tests/hwsu/test_b_of_meter.py](../../../../../tests/hwsu/test_b_of_meter.py)
- Kind: python
- Lines: 195

## Module docstring

> Author B (job 0198): meter binding, basetemps and the output cap (protocol §8.4, §10.3;
> API §8; the hwsc_meter_bind pattern). TEST_PLAN §3 row test_b_of_bind_meter (meter part).
> Every meter/winjob/k4b_meter_bind attribute that bind() sets is restored by monkeypatch.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 18, via sys.path edit)
- `import hwsu_meter_bind` -> [tools/hwsu/hwsu_meter_bind.py](../../tools/hwsu/hwsu_meter_bind.py.md) (line 19, via sys.path edit)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 20, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 21, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 22, via unique basename)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 38, via unique basename) (inside a function)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `C`
- `GIB8`
- `REPO`
- `ROOT`
- `SCRATCH`
- `STORE`

## Classes and functions

- **function `_guard_attrs`** [L31-41]: `def _guard_attrs(monkeypatch)`
- **test `test_job_paths_test`** [L45-48]: `def test_job_paths_test()`
- **test `test_job_paths_dry`** [L51-55]: `def test_job_paths_dry()`
- **test `test_job_paths_store`** [L58-62]: `def test_job_paths_store()`
- **test `test_job_paths_unknown`** [L66-68]: `def test_job_paths_unknown(kind)` decorators: @pytest.mark.parametrize('kind', ['meter', '', 'Test', 'e1'])
- **test `test_placement_ok_contract_paths`** [L72-74]: `def test_placement_ok_contract_paths(kind)` decorators: @pytest.mark.parametrize('kind', ['test', 'dry', 'store'])
- **test `test_placement_rejects_bad_test_paths`** [L85-87]: `def test_placement_rejects_bad_test_paths(key, value)` decorators: @pytest.mark.parametrize('key,value', [('basetemp', ROOT / 'topo-pilot' / 'pytest'), ('basetemp', ROOT / 'hwsu-store' / 'tmp' / 'pytest'), ('temp_root', ROOT / 'tmp'), ('temp_root', SCRATCH / 'other-0300'), ('temp_root', SCRATCH / 'x' / 'test_hwsu-0300'), ('out', ROOT / 'hwsu-dry-of-0300')])
- **test `test_placement_rejects_bad_store_paths`** [L90-93]: `def test_placement_rejects_bad_store_paths()`
- **test `test_placement_against_synthetic_root`** [L96-99]: `def test_placement_against_synthetic_root(tmp_path)`
- **test `test_this_suite_runs_outside_the_project_root`** [L102-105]: `def test_this_suite_runs_outside_the_project_root(tmp_path)` - §8.4 (the K4b registry trap): this run's basetemp and TEMP are outside the project root.
- **test `test_memory_cap`** [L109-114]: `def test_memory_cap()`
- **test `test_bind_sets_caps_from_contract`** [L118-132]: `def test_bind_sets_caps_from_contract(tmp_path, monkeypatch)`
- **test `test_bind_temp_root_defaults_to_out`** [L135-139]: `def test_bind_temp_root_defaults_to_out(tmp_path, monkeypatch)`
- **test `test_bind_output_cap_never_hard_coded`** [L142-150]: `def test_bind_output_cap_never_hard_coded(tmp_path, monkeypatch)`
- **test `test_bind_real_k4b_bind_then_overrides`** [L153-163]: `def test_bind_real_k4b_bind_then_overrides(tmp_path, monkeypatch)` - With the unchanged k4b_meter_bind.bind (which sets 4 GiB / 12 GiB), the HWSU values win.
- **test `test_child_env_u`** [L166-173]: `def test_child_env_u(tmp_path, monkeypatch)`
- **test `test_main_refuses_missing_or_unknown_flags`** [L185-195]: `def test_main_refuses_missing_or_unknown_flags(monkeypatch, argv)` decorators: @pytest.mark.parametrize('argv', [[], ['--job', '0300'], ['--job', '0300', '--task-sha256', 'a', '--session', 's', '--kind', 'test'], ['--job', '0300', '--task-sha256', 'a', '--session', 's', '--stage', 'OF'], ['--job', '0300', '--task-sha256', 'a', '--session', 's', '--kind', 'bogus', '--stage', 'OF'], ['--job', '0300', '--task-sha256', 'a', '--session', 's', '--kind', 'test', '--stage', 'E1']])

