# `tools/c1prime/c1_env.py`

- Source: [tools/c1prime/c1_env.py](../../../../../tools/c1prime/c1_env.py)
- Kind: python
- Lines: 28

## Module docstring

> C1' numerical-environment identity (API.md §14; protocol §18 field 2, review RC8): rebind
> env_identity.SCIENTIFIC_IMPORTS to the C1 set (adds torch and the c1prime modules), then call
> import_scientific(), then record(). record() itself does not consult SCIENTIFIC_IMPORTS.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 7, via same directory)
- `import env_identity` -> [tools/x4_circle_history/env_identity.py](../x4_circle_history/env_identity.py.md) (line 8, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c1prime/c1_freeze.py](c1_freeze.py.md) (line 148, import)
- [tools/c1prime/c1_freeze.py](c1_freeze.py.md) (line 205, import)

## Top-level constants

- `SCIENTIFIC_IMPORTS`

## Classes and functions

- **function `record`** [L23-28]: `def record() -> dict`

