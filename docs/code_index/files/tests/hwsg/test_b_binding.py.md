# `tests/hwsg/test_b_binding.py`

- Source: [tests/hwsg/test_b_binding.py](../../../../../tests/hwsg/test_b_binding.py)
- Kind: python
- Lines: 192

## Module docstring

> Author B: binding and rebinding (protocol 2.3, G3, KG1, DRG3). Black-box on API.md section 2.

## Imports

### Internal (repo files)

- `from test_b_common import CONTRACT, TAGS, expect_fail, mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 13, via same directory)

### External (third-party)

- `pytest` (lines 10)

### Standard library

- `__future__` (lines 2)
- `fractions` (lines 7)
- `importlib` (lines 4)
- `pathlib` (lines 8)
- `sys` (lines 5)
- `textwrap` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 23: `dynamic: m`
- `import_module` line 45: `hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md)
- `import_module` line 47: `hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md)
- `import_module` line 47: `hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md)
- `import_module` line 48: `k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md)
- `import_module` line 49: `k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md)
- `import_module` line 68: `dynamic: r['module']`
- `import_module` line 71: `hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md)
- `import_module` line 96: `hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md)
- `import_module` line 103: `hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md)
- `import_module` line 111: `hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md)
- `import_module` line 112: `hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md)
- `import_module` line 115: `hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md)
- `import_module` line 124: `hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md)
- `import_module` line 130: `hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md)
- `import_module` line 141: `hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md)
- `import_module` line 148: `dynamic: name`

### sys.path additions

- line 12: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`
- line 146: `str(tmp_path)` -> not statically determinable

## Imported by

- none

## Top-level constants

- `ADAPTERS`
- `NON_PLAIN`
- `ROW_NAMES`

## Classes and functions

- **function `_res`** [L21-23]: `def _res(dotted)`
- **function `_snapshot`** [L26-28]: `def _snapshot()`
- **test `test_rows_listing`** [L32-35]: `def test_rows_listing(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_values_inside_and_restored_after`** [L39-73]: `def test_values_inside_and_restored_after(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_restored_after_exception_including_adapters`** [L77-87]: `def test_restored_after_exception_including_adapters(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_nested_world_refused_and_state_intact`** [L90-98]: `def test_nested_world_refused_and_state_intact()`
- **test `test_refused_inside_active_bound_stage_c`** [L101-106]: `def test_refused_inside_active_bound_stage_c()`
- **test `test_drifted_row_refused_and_nothing_set`** [L109-116]: `def test_drifted_row_refused_and_nothing_set(monkeypatch)`
- **test `test_constants_differ_between_worlds`** [L119-132]: `def test_constants_differ_between_worlds()`
- **test `test_kg1_wstar_import_time_values_are_stage_c`** [L135-141]: `def test_kg1_wstar_import_time_values_are_stage_c()`
- **function `_planted_module`** [L144-150]: `def _planted_module(tmp_path, name, body)`
- **test `test_audit_catches_planted_w_star_constants`** [L153-170]: `def test_audit_catches_planted_w_star_constants(tmp_path)`
- **test `test_audit_mid_own_value_is_not_a_hit`** [L173-182]: `def test_audit_mid_own_value_is_not_a_hit(tmp_path)`
- **test `test_check_explicit_stale_default_trap`** [L185-192]: `def test_check_explicit_stale_default_trap()`

