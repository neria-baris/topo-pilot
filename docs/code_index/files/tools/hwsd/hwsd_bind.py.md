# `tools/hwsd/hwsd_bind.py`

- Source: [tools/hwsd/hwsd_bind.py](../../../../../tools/hwsd/hwsd_bind.py)
- Kind: python
- Lines: 101

## Module docstring

> HWSD versioned binding: the hwsd binding table on hwsc_bind.bound_stage_c, the dry and identity
> tables, the audit (API.md §2; protocol §3.3; KD2, DRD3).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 6, via same directory)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../hwsc/hwsc_bind.py.md) (line 13, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 14, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 15, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `contextlib` (lines 10)
- `copy` (lines 7)
- `importlib` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 33: `dynamic: module`

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_a_bounds.py](../../tests/hwsd/test_a_bounds.py.md) (line 26, import)
- [tests/hwsd/test_a_known_bound.py](../../tests/hwsd/test_a_known_bound.py.md) (line 31, import)
- [tests/hwsd/test_b_binding.py](../../tests/hwsd/test_b_binding.py.md) (line 17, import)
- [tests/hwsd/test_b_data.py](../../tests/hwsd/test_b_data.py.md) (line 16, import)
- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 99, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 17, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 36, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 25, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 36, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 17, import)
- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 24, import)
- [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 17, import)
- [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 12, import)

## Top-level constants

- none

## Classes and functions

- **function `decode`** [L18-29]: `def decode(value, repo=None)` - hwsc_bind.decode semantics, with hwsd's contract views and this worktree's REPO.
- **function `_live`** [L32-33]: `def _live(module, name)`
- **function `load_table`** [L36-67]: `def load_table(which='hwsd', case=None, case_dir=None, process=None) -> list`
- **function `bound_hwsd`** [L71-73]: `def bound_hwsd(table=None)` decorators: @contextmanager
- **function `scope_modules`** [L76-83]: `def scope_modules() -> list`
- **function `audit`** [L86-89]: `def audit(modules=None) -> dict`
- **function `never_called`** [L92-93]: `def never_called() -> tuple`
- **function `strong_seed`** [L96-101]: `def strong_seed() -> int`

