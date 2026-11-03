# `tools/hwsu/u2/hwsu_bind_u2.py`

- Source: [tools/hwsu/u2/hwsu_bind_u2.py](../../../../../../tools/hwsu/u2/hwsu_bind_u2.py)
- Kind: python
- Lines: 130

## Module docstring

> HWSU phase-2 call allowlist and constant-read audit (API_U2.md section 2.6; protocol 11.2).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 11, via unique basename)
- `import hwsu_bind` -> [tools/hwsu/hwsu_bind.py](../hwsu_bind.py.md) (line 12, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 13, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 9)
- `ast` (lines 14)
- `copy` (lines 15)
- `importlib` (lines 16)
- `pathlib` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 71: `dynamic: m`
- `import_module` line 76: `dynamic: mod`
- `import_module` line 97: `dynamic: m`

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_audit.py](../../../tests/hwsu/test_b_u2_audit.py.md) (line 30, dynamic)
- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 254, dynamic)
- [tools/hwsu/u2/hwsu_dry2b.py](hwsu_dry2b.py.md) (line 10, import)
- [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 9, import)

## Top-level constants

- `BIND`
- `DRY_ONLY`

## Classes and functions

- **function `u2_files`** [L25-26]: `def u2_files() -> list`
- **function `merged_contract`** [L29-37]: `def merged_contract(contract=None) -> dict`
- **function `_find_module`** [L40-44]: `def _find_module(module)`
- **function `reads_by_path`** [L47-64]: `def reads_by_path(module, qualname) -> dict` - alias.name references of one top-level function, parsed without importing the module.
- **function `function_reads_u2`** [L67-72]: `def function_reads_u2(module, qualname, entry) -> dict`
- **function `_resolve`** [L75-79]: `def _resolve(mod, qualname)`
- **function `_audit_reads`** [L82-116]: `def _audit_reads(c) -> tuple`
- **function `audit_u2`** [L119-130]: `def audit_u2(files=None, contract=None) -> dict`

