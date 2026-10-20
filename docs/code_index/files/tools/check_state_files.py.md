# `tools/check_state_files.py`

- Source: [tools/check_state_files.py](../../../../tools/check_state_files.py)
- Kind: python
- Lines: 78

## Module docstring

> Check state/PROGRESS.md length, state/DECISIONS.md line format, and tracked transcript files.

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `argparse` (lines 6)
- `fnmatch` (lines 7)
- `pathlib` (lines 11)
- `re` (lines 8)
- `subprocess` (lines 9)
- `sys` (lines 10)

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

- `BAD_NAMES`
- `DECISION_RE`
- `PROGRESS_MAX`
- `REPO`
- `STATE`

## Classes and functions

- **function `check_progress`** [L20-25]: `def check_progress(problems)`
- **function `check_decisions`** [L28-39]: `def check_decisions(problems)`
- **function `tracked_files`** [L42-48]: `def tracked_files()`
- **function `check_tracked`** [L51-58]: `def check_tracked(problems)`
- **function `main`** [L61-74]: `def main()`

