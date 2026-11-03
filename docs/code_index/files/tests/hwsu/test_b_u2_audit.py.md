# `tests/hwsu/test_b_u2_audit.py`

- Source: [tests/hwsu/test_b_u2_audit.py](../../../../../tests/hwsu/test_b_u2_audit.py)
- Kind: python
- Lines: 245

## Module docstring

> Author B (job 0223, phase 2): the phase-2 audit u2/hwsu_bind_u2.py (protocol 11.2; API_U2 2.6;
> DRU7; R-0223-3, R-0223-5, R-0223-6). Planted modules live under tmp_path only; planted contract
> variants are deep copies of the loaded CONTRACT.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 20, via sys.path edit)

### External (third-party)

- `psutil` (lines 192)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `importlib` (lines 8)
- `json` (lines 242)
- `os` (lines 9)
- `pathlib` (lines 13)
- `subprocess` (lines 10)
- `sys` (lines 11)
- `textwrap` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 29: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 30: `hwsu_bind_u2` -> [tools/hwsu/u2/hwsu_bind_u2.py](../../tools/hwsu/u2/hwsu_bind_u2.py.md)
- `import_module` line 213: `hwsu_bind` -> [tools/hwsu/hwsu_bind.py](../../tools/hwsu/hwsu_bind.py.md)

### sys.path additions

- line 18: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `BIND`
- `CONDITIONAL_FUNCS`
- `HEAD`
- `REPO`

## Classes and functions

- **function `_b2`** [L28-30]: `def _b2()`
- **function `_plant`** [L33-37]: `def _plant(tmp_path, body, name='hwsu_planted.py') -> Path`
- **function `_calls`** [L40-41]: `def _calls(tmp_path, body, name='hwsu_planted.py')`
- **test `test_never_called_names_fail`** [L49-57]: `def test_never_called_names_fail(tmp_path, mod, fn)` decorators: @pytest.mark.parametrize('mod,fn', [('c2_model', 'load_models'), ('c2_oracle', 'load_process'), ('c2_stats', 'p1'), ('c2_model', 'm0'), ('k4b_stats', 'write_sealed'), ('nd_decoy', 'head_edit'), ('k4b_stats', 'check_unsealed'), ('k4b_driver', 'load_checkpoint')])
- **test `test_unlisted_name_fails`** [L60-67]: `def test_unlisted_name_fails(tmp_path)`
- **test `test_from_import_outside_the_lists_fails`** [L70-77]: `def test_from_import_outside_the_lists_fails(tmp_path)`
- **test `test_allowlisted_names_pass`** [L80-91]: `def test_allowlisted_names_pass(tmp_path)`
- **test `test_c2_seed_default_reference_fails`** [L94-101]: `def test_c2_seed_default_reference_fails(tmp_path)`
- **test `test_train_and_make_train_dev_c_admitted_only_in_hwsu_dry2`** [L108-112]: `def test_train_and_make_train_dev_c_admitted_only_in_hwsu_dry2(tmp_path, body)` decorators: @pytest.mark.parametrize('body', ['import hwsb_train\n\ndef f(s, m):\n    return hwsb_train.train(s, m)\n', 'import hwsc_data\n\ndef f(s, p, m):\n    return hwsc_data.make_train_dev_c(s, p, m)\n'])
- **test `test_conditional_reads_name_exactly_the_sanctioned_functions`** [L115-122]: `def test_conditional_reads_name_exactly_the_sanctioned_functions()`
- **test `test_merged_contract_unions_tables_without_mutating_input`** [L125-136]: `def test_merged_contract_unions_tables_without_mutating_input()`
- **test `test_real_phase2_files_pass_the_audit`** [L139-142]: `def test_real_phase2_files_pass_the_audit()`
- **function `_mutate`** [L146-149]: `def _mutate(fn)`
- **test `test_unlisted_read_of_a_function_fails`** [L152-158]: `def test_unlisted_read_of_a_function_fails()` - A reused function reading a name that is not in its call_time_reads fails the read audit
- **test `test_extra_read_in_table_fails`** [L161-164]: `def test_extra_read_in_table_fails()`
- **test `test_forbidden_read_fails_closed_without_conditional_entry`** [L167-172]: `def test_forbidden_read_fails_closed_without_conditional_entry()`
- **test `test_fifth_forbidden_read_fails_closed`** [L175-180]: `def test_fifth_forbidden_read_fails_closed()` - A forbidden name recorded as a read of a function that is not a sanctioned one.
- **test `test_ast_refs_mismatch_fails`** [L183-187]: `def test_ast_refs_mismatch_fails()`
- **test `test_missing_module_without_ast_by_path_is_not_swallowed`** [L190-200]: `def test_missing_module_without_ast_by_path_is_not_swallowed()`
- **test `test_u2_files_lists_package_including_init_and_audit`** [L204-209]: `def test_u2_files_lists_package_including_init_and_audit()`
- **test `test_phase1_audit_globs_never_see_u2`** [L212-219]: `def test_phase1_audit_globs_never_see_u2()`
- **test `test_reads_by_path_does_not_import_and_equals_recorded_refs`** [L223-245]: `def test_reads_by_path_does_not_import_and_equals_recorded_refs(tmp_path)`

