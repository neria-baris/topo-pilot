# `tools/c1prime/c1_freeze.py`

- Source: [tools/c1prime/c1_freeze.py](../../../../../tools/c1prime/c1_freeze.py)
- Kind: python
- Lines: 215

## Module docstring

> C1' accepted test run, protected-record snapshots, implementation freeze and fresh-venv pin
> check (API.md §14; K4 freeze_bind / run_tests_bind / live_context._pin_modules pattern).

## Imports

### Internal (repo files)

- `import freeze` -> [tools/x4_oracle_profile/freeze.py](../x4_oracle_profile/freeze.py.md) (line 25, via sys.path edit)
- `import c1_env` -> [tools/c1prime/c1_env.py](c1_env.py.md) (line 148, via same directory) (inside a function)
- `import env_identity` -> [tools/x4_circle_history/env_identity.py](../x4_circle_history/env_identity.py.md) (line 149, via sys.path edit) (inside a function)
- `import c1_env` -> [tools/c1prime/c1_env.py](c1_env.py.md) (line 205, via same directory) (inside a function)

### External (third-party)

- `pytest` (lines 162)

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 12)
- `json` (lines 13)
- `os` (lines 14)
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

- line 22: `[p for p in (str(HERE), str(HERE.parent / 'x4_oracle_profile'), str(HERE.parent / 'x4_circle_history')) if p not in sys.path]` -> `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 53, import)

## Top-level constants

- `CONTRACT`
- `DIST_PREFIXES`
- `HERE`
- `OUT`
- `PROTECTED_STORES`
- `REPO`
- `REUSED_0014`
- `REUSED_K4`
- `ROOT`
- `TESTS`
- `VENV_PYTHON`

## Classes and functions

- **function `_listing`** [L44-47]: `def _listing(base: Path) -> dict` - Listing hash material (relative path -> size) without reading payload bytes.
- **function `snapshot`** [L50-60]: `def snapshot() -> dict`
- **function `_hash_json`** [L63-64]: `def _hash_json(obj) -> str`
- **function `compare`** [L67-73]: `def compare(a: dict, b: dict) -> dict`
- **function `frozen_files`** [L76-84]: `def frozen_files() -> dict`
- **function `reused_unchanged`** [L87-94]: `def reused_unchanged() -> dict`
- **function `environment`** [L97-102]: `def environment() -> dict`
- **function `numerical_identity`** [L105-110]: `def numerical_identity() -> dict`
- **function `freeze`** [L113-135]: `def freeze() -> dict`
- **function `pin_check`** [L138-158]: `def pin_check() -> dict` - Fresh venv process: frozen hashes, file set, dists, loaded modules and env identity.
- **function `accept`** [L161-182]: `def accept() -> int`
- **function `main`** [L185-211]: `def main() -> int`

