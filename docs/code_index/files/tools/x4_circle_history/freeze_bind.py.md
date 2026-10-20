# `tools/x4_circle_history/freeze_bind.py`

- Source: [tools/x4_circle_history/freeze_bind.py](../../../../../tools/x4_circle_history/freeze_bind.py)
- Kind: python
- Lines: 222

## Module docstring

> Protected-record snapshots and implementation freeze for job 0016 (standard library only).

## Imports

### Internal (repo files)

- `import freeze` -> [tools/x4_oracle_profile/freeze.py](../x4_oracle_profile/freeze.py.md) (line 29, via sys.path edit)

### External (third-party)

- none

### Standard library

- `__future__` (lines 16)
- `hashlib` (lines 18)
- `json` (lines 19)
- `pathlib` (lines 23)
- `subprocess` (lines 20)
- `sys` (lines 21)
- `time` (lines 22)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(HERE.parent / 'x4_oracle_profile')` -> `tools/x4_oracle_profile`

## Imported by

- [tests/circle_history/test_builder_guards.py](../../tests/circle_history/test_builder_guards.py.md) (line 166, import)
- [tests/circle_history/test_builder_v24_runtime.py](../../tests/circle_history/test_builder_v24_runtime.py.md) (line 193, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 49, import)
- [tools/x4_circle_history/run_tests_bind.py](run_tests_bind.py.md) (line 22, import)

## Top-level constants

- `CONTRACT`
- `DIST_PREFIXES`
- `GIT_REFS`
- `HERE`
- `OUT`
- `PROJECT_DEPENDENCIES`
- `REPO`
- `REUSED_0014`
- `ROOT`
- `STORES`
- `TESTS`
- `VENV_PYTHON`

## Classes and functions

- **function `snapshot`** [L57-78]: `def snapshot() -> dict`
- **function `frozen_files`** [L81-91]: `def frozen_files() -> dict`
- **function `numerical_identity`** [L94-105]: `def numerical_identity() -> dict` - env_identity.record() from a fresh venv probe process (metered with this run).
- **function `archive_superseded`** [L108-129]: `def archive_superseded() -> dict | None` - Keep an existing FREEZE.json as freezes/FREEZE_superseded_NN.json (exclusive create).
- **function `reused_unchanged`** [L132-136]: `def reused_unchanged() -> dict`
- **function `environment`** [L139-155]: `def environment() -> dict`
- **function `freeze`** [L158-185]: `def freeze() -> dict`
- **function `main`** [L188-218]: `def main() -> int`

