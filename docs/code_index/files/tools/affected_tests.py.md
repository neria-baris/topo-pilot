# `tools/affected_tests.py`

- Source: [tools/affected_tests.py](../../../../tools/affected_tests.py)
- Kind: python
- Lines: 118

## Module docstring

> Print the minimal pytest folders for changed paths (see tools/SPEC.md).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `argparse` (lines 6)
- `ast` (lines 7)
- `pathlib` (lines 10)
- `subprocess` (lines 8)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tasks.ps1](../tasks.ps1.md) (line 45, invoke)

## Top-level constants

- `DEPENDENTS`
- `MODULES`
- `REPO`

## Classes and functions

- **function `repo_rel`** [L30-38]: `def repo_rel(raw)` - Return the repo-relative posix path for a path given as \ or /, absolute or relative.
- **function `signature`** [L41-51]: `def signature(node)` - Return a comparable text signature of a top-level function or class.
- **function `api_of`** [L54-68]: `def api_of(source)` - Return (sorted __all__ names, {name: signature}) for a module source text.
- **function `api_changed`** [L71-82]: `def api_changed(module)` - True if the public API of <module>/__init__.py differs from HEAD (or cannot be compared).
- **function `main`** [L85-114]: `def main()`

