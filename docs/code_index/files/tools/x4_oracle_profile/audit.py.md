# `tools/x4_oracle_profile/audit.py`

- Source: [tools/x4_oracle_profile/audit.py](../../../../../tools/x4_oracle_profile/audit.py)
- Kind: python
- Lines: 137

## Module docstring

> Bounded independent audit of exported job-0014 statistics (post-terminal; read-only inputs).

## Imports

### Internal (repo files)

- `import inputs` -> [tools/x4_oracle_profile/inputs.py](inputs.py.md) (line 31, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](oracle_profile.py.md) (line 32, via same directory)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 44, via package root) (inside a function)
- `import validation` -> [tools/x4_oracle_profile/validation.py](validation.py.md) (line 117, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 26)

### Standard library

- `__future__` (lines 18)
- `argparse` (lines 20)
- `json` (lines 21)
- `pathlib` (lines 24)
- `sys` (lines 22)
- `time` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(HERE)` -> `tools/x4_oracle_profile`
- line 30: `str(HERE.parents[1] / 'tests' / 'oracle_profile')` -> `tests/oracle_profile`

## Imported by

- none

## Top-level constants

- `CFG`
- `HERE`
- `OUT`
- `PDIR`

## Classes and functions

- **function `compare`** [L39-40]: `def compare(a: float, b: float) -> float`
- **function `main`** [L43-133]: `def main() -> int`

