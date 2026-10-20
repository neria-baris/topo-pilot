# `tools/check_file_sizes.py`

- Source: [tools/check_file_sizes.py](../../../../tools/check_file_sizes.py)
- Kind: python
- Lines: 64

## Module docstring

> Fail on .py files over 400 lines (outside .venv) and tracked files over 5 MB.

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `argparse` (lines 6)
- `os` (lines 7)
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

- [tasks.ps1](../tasks.ps1.md) (line 13, invoke)

## Top-level constants

- `FALLBACK_PRUNE`
- `MAX_BYTES`
- `MAX_LINES`
- `PRUNE`
- `REPO`

## Classes and functions

- **function `display`** [L19-23]: `def display(path)`
- **function `walk`** [L26-30]: `def walk(prune)`
- **function `tracked_files`** [L33-39]: `def tracked_files()`
- **function `main`** [L42-60]: `def main()`

