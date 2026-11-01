# `tests/hwsd/test_b_binding.py`

- Source: [tests/hwsd/test_b_binding.py](../../../../../tests/hwsd/test_b_binding.py)
- Kind: python
- Lines: 317

## Module docstring

> Author B: the versioned binding, the audit, the never-called list, constants (§3.3; KD2, DRD3).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 16, via sys.path edit)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](../../tools/hwsd/hwsd_bind.py.md) (line 17, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 18, via same directory)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 20, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 21, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 22, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 23, via unique basename)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](../../tools/k4b/k4b_decoder.py.md) (line 94, via unique basename) (inside a function)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 95, via unique basename) (inside a function)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](../../tools/hwsd/hwsd_data.py.md) (line 230, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 24)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)
- `fractions` (lines 9)
- `importlib` (lines 6)
- `pathlib` (lines 10)
- `sys` (lines 7)
- `types` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 51: `dynamic: r['module']`
- `import_module` line 57: `dynamic: m`
- `import_module` line 226: `dynamic: mod`

### sys.path additions

- line 14: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `BIND`
- `DRY_SEEDS`
- `EXPECTED_NEW`
- `K4B_OLD_SEEDS`
- `PLANTED`
- `ROOT`
- `SEEDS`

## Classes and functions

- **function `_snapshot`** [L50-52]: `def _snapshot(rows)`
- **function `_restored`** [L55-57]: `def _restored(before)`
- **test `test_load_table_rows_and_values`** [L60-75]: `def test_load_table_rows_and_values()`
- **test `test_decode`** [L78-85]: `def test_decode()`
- **test `test_inside_the_binding_and_restoration`** [L88-114]: `def test_inside_the_binding_and_restoration()`
- **test `test_restoration_after_an_exception`** [L117-123]: `def test_restoration_after_an_exception()`
- **test `test_nesting_fails_closed`** [L126-134]: `def test_nesting_fails_closed()`
- **test `test_planted_drift_raises_and_sets_nothing`** [L137-144]: `def test_planted_drift_raises_and_sets_nothing(monkeypatch)`
- **function `_module`** [L147-155]: `def _module(name, src)`
- **test `test_audit_catches_planted_leftovers`** [L173-179]: `def test_audit_catches_planted_leftovers(which)` decorators: @pytest.mark.parametrize('which', sorted(PLANTED))
- **test `test_audit_clean_module_and_bool`** [L182-189]: `def test_audit_clean_module_and_bool(monkeypatch)`
- **test `test_audit_outside_the_binding_fails_by_design`** [L192-194]: `def test_audit_outside_the_binding_fails_by_design()`
- **test `test_left_unchanged_and_forbidden_rows`** [L197-208]: `def test_left_unchanged_and_forbidden_rows()`
- **test `test_never_called_list`** [L211-226]: `def test_never_called_list()`
- **test `test_scope_modules`** [L229-240]: `def test_scope_modules()`
- **test `test_dry_and_identity_tables`** [L243-274]: `def test_dry_and_identity_tables(tmp_path)`
- **test `test_kd2b_stream_check`** [L277-285]: `def test_kd2b_stream_check()`
- **test `test_constants`** [L288-301]: `def test_constants()`
- **test `test_dry_plans`** [L304-317]: `def test_dry_plans()`

