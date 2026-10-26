# `tools/c2_nd/store_template/nd_meter_bind.py`

- Source: [tools/c2_nd/store_template/nd_meter_bind.py](../../../../../../tools/c2_nd/store_template/nd_meter_bind.py)
- Kind: python
- Lines: 137

## Module docstring

> Store-local binding of the unchanged job-0014 meter for the C2ND runs (C2ND API.md 9.8; the
> C2 c2_meter_bind.py pattern). Template: the coordinator copies it into c2nd-store (or into a
> dry-run store) and binds its sha256 in FREEZE.json (DRY.json) "meter_bind_sha256".

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](../../x4_oracle_profile/controls.py.md) (line 65, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../x4_oracle_profile/meter.py.md) (line 66, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../x4_oracle_profile/winjob.py.md) (line 67, via unique basename)

### External (third-party)

- none

### Standard library

- `hashlib` (lines 22)
- `json` (lines 23)
- `os` (lines 24)
- `pathlib` (lines 27)
- `shutil` (lines 25)
- `sys` (lines 26)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 63: `str(IMPORT_DIR)` -> not statically determinable

## Imported by

- none

## Top-level constants

- `DISK_MIN_FREE`
- `GIB`
- `IMPORT_DIR`
- `METER_FILES`
- `OUT`
- `RECORD`
- `WORKTREE`

## Classes and functions

- **function `_norm`** [L41-42]: `def _norm(p)`
- **function `_sha`** [L45-46]: `def _sha(p)`
- **function `_fail`** [L49-50]: `def _fail(why)`
- **function `disk_reason`** [L84-92]: `def disk_reason(usage=shutil.disk_usage)`
- **function `make_limiter`** [L95-105]: `def make_limiter(disk=disk_reason, legacy=None)`
- **function `_drop`** [L108-111]: `def _drop(args, flag)`
- **function `rewrite_argv`** [L114-120]: `def rewrite_argv(argv)`
- **function `main`** [L123-133]: `def main()`

