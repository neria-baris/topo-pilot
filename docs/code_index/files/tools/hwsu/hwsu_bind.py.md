# `tools/hwsu/hwsu_bind.py`

- Source: [tools/hwsu/hwsu_bind.py](../../../../../tools/hwsu/hwsu_bind.py)
- Kind: python
- Lines: 234

## Module docstring

> HWSU call allowlist and constant-read audit (API.md §7; protocol §11.2; run by OF-B, RC-10).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 5, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `ast` (lines 6)
- `fnmatch` (lines 7)
- `importlib` (lines 8)
- `inspect` (lines 9)
- `pathlib` (lines 11)
- `types` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 164: `dynamic: obj.__module__`
- `import_module` line 184: `dynamic: imports[base]`
- `import_module` line 195: `dynamic: module`
- `import_module` line 210: `dynamic: mod`

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_of_bind.py](../../tests/hwsu/test_b_of_bind.py.md) (line 20, import)
- [tests/hwsu/test_b_of_freeze.py](../../tests/hwsu/test_b_of_freeze.py.md) (line 21, import)
- [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 143, import)
- [tools/hwsu/hwsu_freeze.py](hwsu_freeze.py.md) (line 137, import)

## Top-level constants

- `EXPLICIT`
- `MISSING`

## Classes and functions

- **function `module_imports`** [L16-25]: `def module_imports(tree) -> dict`
- **function `references`** [L28-40]: `def references(path) -> list`
- **function `_never`** [L43-45]: `def _never(module, name, patterns) -> bool`
- **function `_default_files`** [L48-51]: `def _default_files() -> list`
- **function `argument_less`** [L59-72]: `def argument_less(path) -> list` - Calls of the accepted conditional-read functions without their explicit arguments.
- **function `audit_calls`** [L75-95]: `def audit_calls(files=None, contract=None) -> dict`
- **function `_tools_path`** [L99-101]: `def _tools_path(f) -> bool`
- **function `_under_tools`** [L104-109]: `def _under_tools(obj) -> bool`
- **function `_tool_module`** [L112-114]: `def _tool_module(mod) -> bool`
- **function `_locals`** [L117-132]: `def _locals(tree) -> set`
- **function `_resolve`** [L135-139]: `def _resolve(mod, qualname)`
- **function `function_reads`** [L142-197]: `def function_reads(module, qualname) -> dict`
- **function `audit_reads`** [L200-228]: `def audit_reads(contract=None) -> dict`
- **function `audit`** [L231-234]: `def audit(files=None, contract=None) -> dict`

