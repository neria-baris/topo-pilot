# `tools/x4_oracle_profile/run_profile.py`

- Source: [tools/x4_oracle_profile/run_profile.py](../../../../../tools/x4_oracle_profile/run_profile.py)
- Kind: python
- Lines: 211

## Module docstring

> Job-0014 driver: numerical validation (pre-freeze) and the frozen full profile.

## Imports

### Internal (repo files)

- `import inputs` -> [tools/x4_oracle_profile/inputs.py](inputs.py.md) (line 25, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](oracle_profile.py.md) (line 26, via same directory)
- `from runtime import Stopped, guard, save_npz` -> [tools/x4_oracle_profile/runtime.py](runtime.py.md) (line 33, via same directory)
- `from validation import validate` -> [tools/x4_oracle_profile/validation.py](validation.py.md) (line 34, via same directory)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 49, via package root) (inside a function)
- `import freeze` -> [tools/x4_oracle_profile/freeze.py](freeze.py.md) (line 121, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 11)
- `csv` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 17)
- `sys` (lines 15)
- `time` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(HERE)` -> `tools/x4_oracle_profile`
- line 23: `str(HERE.parents[1] / 'tests' / 'oracle_profile')` -> `tests/oracle_profile`

## Imported by

- none

## Top-level constants

- `CFG`
- `HERE`
- `OUT`
- `SPLITS`

## Classes and functions

- **function `split_profile`** [L37-45]: `def split_profile(proc, split, tokens) -> dict`
- **function `bootstrap`** [L48-62]: `def bootstrap(split, rows) -> tuple[dict, dict]`
- **function `summarise`** [L65-76]: `def summarise(point: float, draws: np.ndarray) -> dict`
- **function `diagnostics`** [L79-106]: `def diagnostics(res: dict) -> dict`
- **function `write_tables`** [L109-117]: `def write_tables(table: list, diff: list) -> None`
- **function `profile`** [L120-202]: `def profile() -> int`

