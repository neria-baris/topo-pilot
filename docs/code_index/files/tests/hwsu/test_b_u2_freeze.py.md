# `tests/hwsu/test_b_u2_freeze.py`

- Source: [tests/hwsu/test_b_u2_freeze.py](../../../../../tests/hwsu/test_b_u2_freeze.py)
- Kind: python
- Lines: 224

## Module docstring

> Author B (job 0223, phase 2): the execution freeze FREEZE.json and S0 (API_U2 2.2; protocol 4.1,
> 6 row S0). The repository under test is this worktree (read-only: git ls-tree / cat-file / diff);
> the store is a tmp_path copy holding byte copies of the real OF_ACCEPT.json and FREEZE_OF.json (so
> the R-0206-1 hashes of CONTRACT hold). Nothing is written to the real store.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 21, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 22, via unique basename)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `importlib` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 14)
- `shutil` (lines 11)
- `subprocess` (lines 12)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 29: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 30: `hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](../../tools/hwsu/u2/hwsu_known.py.md)

### sys.path additions

- line 19: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `FREEZE_FAIL`
- `P2`
- `REPO`

## Classes and functions

- **function `_known`** [L28-30]: `def _known()`
- **function `_git`** [L33-35]: `def _git(*args) -> str`
- **function `_canon_sha`** [L38-39]: `def _canon_sha(obj) -> str`
- **function `_store`** [L42-50]: `def _store(tmp_path) -> Path`
- **function `_report`** [L53-59]: `def _report(tmp_path, h, **over) -> Path`
- **function `_ju`** [L62-65]: `def _ju(tmp_path) -> list`
- **function `_freeze`** [L68-71]: `def _freeze(tmp_path, store, **over)`
- **function `_status`** [L74-79]: `def _status(fn, *a, **k)`
- **function `frozen`** [L83-88]: `def frozen(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `_copy`** [L91-95]: `def _copy(frozen, tmp_path)`
- **test `test_implementation_files_u_names_phase2_files_and_tests`** [L98-109]: `def test_implementation_files_u_names_phase2_files_and_tests()`
- **test `test_freeze_u_writes_contract_fields`** [L112-127]: `def test_freeze_u_writes_contract_fields(frozen)`
- **test `test_freeze_u_is_exclusive`** [L130-135]: `def test_freeze_u_is_exclusive(frozen, tmp_path)`
- **test `test_freeze_u_refuses_other_implementation_sha256_and_writes_nothing`** [L138-141]: `def test_freeze_u_refuses_other_implementation_sha256_and_writes_nothing(tmp_path)`
- **test `test_freeze_u_refuses_all_pass_false_and_writes_nothing`** [L144-147]: `def test_freeze_u_refuses_all_pass_false_and_writes_nothing(tmp_path)`
- **test `test_freeze_u_refuses_when_verify_freeze_of_fails`** [L150-158]: `def test_freeze_u_refuses_when_verify_freeze_of_fails(tmp_path)`
- **test `test_verify_freeze_u_passes_on_the_unmodified_freeze`** [L161-163]: `def test_verify_freeze_u_passes_on_the_unmodified_freeze(frozen, tmp_path)`
- **test `test_verify_freeze_u_absent_is_invalid`** [L166-168]: `def test_verify_freeze_u_absent_is_invalid(tmp_path)`
- **function `_tamper`** [L171-178]: `def _tamper(s, table, key=None)`
- **test `test_verify_freeze_u_detects_a_changed_phase2_file`** [L181-186]: `def test_verify_freeze_u_detects_a_changed_phase2_file(frozen, tmp_path)`
- **test `test_verify_freeze_u_detects_a_changed_reused_file_in_either_table`** [L189-200]: `def test_verify_freeze_u_detects_a_changed_reused_file_in_either_table(frozen, tmp_path)`
- **test `test_s0_u_refuses_a_diff_touching_a_phase1_file`** [L203-207]: `def test_s0_u_refuses_a_diff_touching_a_phase1_file(frozen, tmp_path)` - r_ref far enough back that the diff contains phase-1 files (status A): refused.
- **test `test_s0_u_accepts_the_real_diff_once_the_tree_is_committed`** [L210-224]: `def test_s0_u_accepts_the_real_diff_once_the_tree_is_committed(frozen, tmp_path)`

