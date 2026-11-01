# `tools/hwsu/hwsu_freeze.py`

- Source: [tools/hwsu/hwsu_freeze.py](../../../../../tools/hwsu/hwsu_freeze.py)
- Kind: python
- Lines: 167

## Module docstring

> HWSU freeze and OF-B (API.md §5.3, §5.4; split from hwsu_records by size, re-exported there).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 5, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 13, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 15, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 16, via unique basename)
- `import hwsu_bind` -> [tools/hwsu/hwsu_bind.py](hwsu_bind.py.md) (line 137, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 14)

### Standard library

- `__future__` (lines 3)
- `fnmatch` (lines 6)
- `json` (lines 7)
- `pathlib` (lines 11)
- `platform` (lines 8)
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

- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 9, import)

## Top-level constants

- `FREEZE`

## Classes and functions

- **function `_canon_sha`** [L22-23]: `def _canon_sha(obj) -> str`
- **function `_git`** [L27-31]: `def _git(repo, *args) -> bytes`
- **function `_blob`** [L34-35]: `def _blob(repo, ref, path) -> bytes`
- **function `_blobs`** [L38-58]: `def _blobs(repo, ref, paths) -> dict` - {path: bytes} of the blobs at ref in one git cat-file --batch call.
- **function `_test_files`** [L61-64]: `def _test_files(names) -> list`
- **function `implementation_files`** [L67-71]: `def implementation_files(repo, h_exec, contract=None) -> dict`
- **function `freeze_of`** [L74-105]: `def freeze_of(store, repo, h_exec, dro_report, j_of_records, written_by) -> dict`
- **function `verify_freeze_of`** [L108-133]: `def verify_freeze_of(store, repo) -> dict`
- **function `of_b`** [L136-165]: `def of_b(store, repo, r_ref=None) -> dict`

