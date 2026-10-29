# `tests/hwsc/test_b_binding.py`

- Source: [tests/hwsc/test_b_binding.py](../../../../../tests/hwsc/test_b_binding.py)
- Kind: python
- Lines: 368

## Module docstring

> Author B (job 0176): the versioned binding, its audit and the KC7-type stream check.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 24, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 25, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 26, via unique basename)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 80, via unique basename) (inside a function)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 168, via unique basename) (inside a function)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 169, via unique basename) (inside a function)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 170, via unique basename) (inside a function)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 171, via unique basename) (inside a function)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 172, via unique basename) (inside a function)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 216, via unique basename) (inside a function)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 224, via unique basename) (inside a function)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 225, via unique basename) (inside a function)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 309, via unique basename) (inside a function)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 336, via unique basename) (inside a function)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 360, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 7)
- `copy` (lines 9)
- `fractions` (lines 13)
- `importlib` (lines 10)
- `pathlib` (lines 14)
- `sys` (lines 11)
- `types` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 45: `dynamic: r['module']`

### sys.path additions

- line 22: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `C`
- `NEW_MODELS`
- `OLD_MODELS`
- `PLANTS`
- `REPO`
- `ROOT`
- `STAGE_C_SEEDS`
- `_HWSC`

## Classes and functions

- **function `_status`** [L39-40]: `def _status(exc_info)`
- **function `_live`** [L43-46]: `def _live(rows)` - (module, name, object) for every row, read from the live modules.
- **function `_by_name`** [L49-50]: `def _by_name(rows)`
- **test `test_config_constants_equal_contract`** [L54-76]: `def test_config_constants_equal_contract()`
- **test `test_config_margin_matches_k4b`** [L79-84]: `def test_config_margin_matches_k4b()`
- **test `test_decode_each_encoding`** [L88-99]: `def test_decode_each_encoding(tmp_path)`
- **test `test_load_table_has_the_21_contract_rows`** [L102-119]: `def test_load_table_has_the_21_contract_rows()`
- **test `test_check_old_is_empty_on_live_modules`** [L122-123]: `def test_check_old_is_empty_on_live_modules()`
- **function `synth`** [L127-134]: `def synth(monkeypatch)` decorators: @pytest.fixture
- **test `test_check_old_rules_on_a_synthetic_module`** [L137-150]: `def test_check_old_rules_on_a_synthetic_module(synth)`
- **test `test_bound_stage_c_on_a_synthetic_table`** [L153-159]: `def test_bound_stage_c_on_a_synthetic_table(synth)`
- **test `test_bound_stage_c_sets_every_name_and_restores_identity`** [L163-196]: `def test_bound_stage_c_sets_every_name_and_restores_identity()`
- **test `test_exception_inside_restores_everything`** [L199-206]: `def test_exception_inside_restores_everything()`
- **test `test_entering_twice_fails_with_binding`** [L209-220]: `def test_entering_twice_fails_with_binding()`
- **test `test_planted_drift_refuses_and_sets_nothing`** [L223-233]: `def test_planted_drift_refuses_and_sets_nothing(monkeypatch)`
- **test `test_audit_outside_the_binding_fails`** [L236-240]: `def test_audit_outside_the_binding_fails()`
- **function `_module`** [L262-266]: `def _module(monkeypatch, name, src)`
- **test `test_planted_defect_is_a_hit`** [L270-280]: `def test_planted_defect_is_a_hit(monkeypatch, src, top)` decorators: @pytest.mark.parametrize('src,top', PLANTS, ids=[p[1] for p in PLANTS])
- **test `test_clean_module_and_bool_and_foreign_functions`** [L283-290]: `def test_clean_module_and_bool_and_foreign_functions(monkeypatch)`
- **test `test_wrong_top_name_does_not_cover`** [L293-296]: `def test_wrong_top_name_does_not_cover(monkeypatch)`
- **test `test_identity_table_is_a_no_op`** [L300-313]: `def test_identity_table_is_a_no_op()`
- **test `test_dry_table_binds_the_dry_values`** [L316-341]: `def test_dry_table_binds_the_dry_values(tmp_path)`
- **test `test_dry_table_requires_case_and_dir`** [L345-347]: `def test_dry_table_requires_case_and_dir(kw)` decorators: @pytest.mark.parametrize('kw', [{}, {'case': 'DRC1'}, {'case_dir': 'x'}])
- **test `test_table_is_not_mutated_by_binding`** [L350-355]: `def test_table_is_not_mutated_by_binding()`
- **test `test_kc7_cal_stream_inside_the_binding`** [L359-368]: `def test_kc7_cal_stream_inside_the_binding()`

