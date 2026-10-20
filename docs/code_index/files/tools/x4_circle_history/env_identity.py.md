# `tools/x4_circle_history/env_identity.py`

- Source: [tools/x4_circle_history/env_identity.py](../../../../../tools/x4_circle_history/env_identity.py)
- Kind: python
- Lines: 205

## Module docstring

> Numerical implementation identity (API.md spec v2.4 item 12; builder-tested).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 147, 149)
- `threadpoolctl` (lines 154)

### Standard library

- `__future__` (lines 17)
- `hashlib` (lines 19)
- `importlib` (lines 20)
- `json` (lines 21)
- `pathlib` (lines 24)
- `platform` (lines 22)
- `sys` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 92: `dynamic: name`

### sys.path additions

- line 86: `str(extra)` -> `src`, `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/circle_history/test_builder_v24_runtime.py](../../tests/circle_history/test_builder_v24_runtime.py.md) (line 23, import)
- [tools/c1prime/c1_env.py](../c1prime/c1_env.py.md) (line 8, import)
- [tools/c1prime/c1_freeze.py](../c1prime/c1_freeze.py.md) (line 149, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 55, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 68, import)

## Top-level constants

- `HERE`
- `LIMITATION`
- `REPO`
- `SCIENTIFIC_IMPORTS`
- `_SKIP_DIRS`

## Classes and functions

- **function `ensure_paths`** [L78-86]: `def ensure_paths() -> None`
- **function `import_scientific`** [L89-92]: `def import_scientific() -> None`
- **function `file_sha`** [L95-96]: `def file_sha(path: Path) -> str`
- **function `tree_digest`** [L99-109]: `def tree_digest(path: Path) -> str` - sha256 over sorted 'relpath:sha256' lines (a file: its own sha256).
- **function `_site_packages`** [L112-113]: `def _site_packages() -> Path`
- **function `loaded_distributions`** [L116-126]: `def loaded_distributions(modules=None) -> list[str]`
- **function `unfrozen_project_modules`** [L129-142]: `def unfrozen_project_modules(frozen_rel: set, modules=None) -> list[str]` - Loaded modules from this worktree's src/, tools/ or tests/ outside the frozen file set.
- **function `_cpu_features`** [L145-150]: `def _cpu_features() -> list[str]`
- **function `_threadpools`** [L153-159]: `def _threadpools() -> list[dict]`
- **function `record`** [L162-195]: `def record(modules=None) -> dict`
- **function `main`** [L198-201]: `def main() -> int`

