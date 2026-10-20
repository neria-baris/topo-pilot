# `tools/x4_oracle_profile/freeze.py`

- Source: [tools/x4_oracle_profile/freeze.py](../../../../../tools/x4_oracle_profile/freeze.py)
- Kind: python
- Lines: 219

## Module docstring

> Hash snapshots of protected records and the pre-profile implementation freeze (stdlib only).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 11)
- `hashlib` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 18)
- `subprocess` (lines 15)
- `sys` (lines 16)
- `time` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c1prime/c1_freeze.py](../c1prime/c1_freeze.py.md) (line 25, import)
- [tools/x4_circle_history/freeze_bind.py](../x4_circle_history/freeze_bind.py.md) (line 29, import)
- [tools/x4_oracle_profile/run_profile.py](run_profile.py.md) (line 121, import)
- [tools/x4_oracle_profile/run_tests.py](run_tests.py.md) (line 21, import)
- [tools/x4_oracle_profile/validation.py](validation.py.md) (line 182, import)

## Top-level constants

- `ARTIFACTS`
- `GIT_REFS`
- `MAILBOX_FILES`
- `OUT`
- `REPO`
- `ROOT`
- `STORES`
- `TESTS`
- `TOOL`

## Classes and functions

- **function `sha`** [L63-68]: `def sha(path: Path) -> str`
- **function `tree`** [L71-72]: `def tree(base: Path) -> dict`
- **function `git`** [L75-78]: `def git(repo: Path, *args: str) -> str`
- **function `snapshot`** [L81-98]: `def snapshot() -> dict`
- **function `write_new`** [L101-104]: `def write_new(path: Path, obj) -> None`
- **function `frozen_files`** [L107-110]: `def frozen_files() -> dict`
- **function `freeze`** [L113-156]: `def freeze() -> dict`
- **function `verify`** [L159-177]: `def verify() -> list`
- **function `main`** [L180-215]: `def main() -> int`

