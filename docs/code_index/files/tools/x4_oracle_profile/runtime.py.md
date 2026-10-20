# `tools/x4_oracle_profile/runtime.py`

- Source: [tools/x4_oracle_profile/runtime.py](../../../../../tools/x4_oracle_profile/runtime.py)
- Kind: python
- Lines: 71

## Module docstring

> Shared job-0014 runtime helpers: safe-boundary control guard and immutable NPZ export.

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](controls.py.md) (line 17, via same directory)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](inputs.py.md) (line 18, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](oracle_profile.py.md) (line 19, via same directory)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 3)
- `io` (lines 5)
- `json` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 7)
- `time` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 14: `str(HERE)` -> `tools/x4_oracle_profile`
- line 15: `str(HERE.parents[1] / 'tests' / 'oracle_profile')` -> `tests/oracle_profile`

## Imported by

- [tools/x4_oracle_profile/run_profile.py](run_profile.py.md) (line 33, import)
- [tools/x4_oracle_profile/validation.py](validation.py.md) (line 24, import)

## Top-level constants

- `CFG`
- `HERE`
- `OUT`
- `SPLITS`

## Classes and functions

- **class `Stopped(RuntimeError)`** [L26-27]
- **function `guard`** [L30-55]: `def guard(where: str) -> None` - Safe-boundary runtime control check (HOLD waits here; STOP/INVALID raise).
- **function `headroom`** [L58-61]: `def headroom(extra: int) -> None`
- **function `save_npz`** [L64-71]: `def save_npz(path: Path, **arrays) -> str`

