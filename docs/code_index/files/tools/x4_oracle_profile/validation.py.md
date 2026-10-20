# `tools/x4_oracle_profile/validation.py`

- Source: [tools/x4_oracle_profile/validation.py](../../../../../tools/x4_oracle_profile/validation.py)
- Kind: python
- Lines: 263

## Module docstring

> Job-0014 pre-freeze numerical validation on the existing histories (via run_profile).

## Imports

### Internal (repo files)

- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 15, via sys.path edit)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](inputs.py.md) (line 16, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](oracle_profile.py.md) (line 17, via same directory)
- `from runtime import guard` -> [tools/x4_oracle_profile/runtime.py](runtime.py.md) (line 24, via same directory)
- `import freeze` -> [tools/x4_oracle_profile/freeze.py](freeze.py.md) (line 182, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 9)

### Standard library

- `__future__` (lines 3)
- `json` (lines 5)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 12: `str(HERE)` -> `tools/x4_oracle_profile`
- line 13: `str(HERE.parents[1] / 'tests' / 'oracle_profile')` -> `tests/oracle_profile`

## Imported by

- [tools/x4_oracle_profile/audit.py](audit.py.md) (line 117, import)
- [tools/x4_oracle_profile/run_profile.py](run_profile.py.md) (line 34, import)

## Top-level constants

- `CFG`
- `HERE`
- `OUT`
- `SPLITS`

## Classes and functions

- **function `reference_rows`** [L27-28]: `def reference_rows(n: int) -> list[int]`
- **function `decimal_moments`** [L31-34]: `def decimal_moments(proc, E, suffix) -> tuple[np.ndarray, np.ndarray]`
- **function `k8_reproduction`** [L37-61]: `def k8_reproduction(proc, cal) -> dict` - Recorded calibration B8/V8 from actual T/E/pi/tokens (never cached m8/r8).
- **function `stored_value_checks`** [L64-83]: `def stored_value_checks(proc, data) -> dict`
- **function `reference_checks`** [L86-159]: `def reference_checks(proc, data) -> dict` - Independent Decimal reference on fixed rows, all K; canonical/named; trap detectability.
- **function `trap_checks`** [L162-178]: `def trap_checks(proc, split, sub) -> dict` - Wrong symbol mapping and an extra trailing transition must be detectable on real rows.
- **function `source_identity`** [L181-194]: `def source_identity() -> dict`
- **function `validate`** [L197-263]: `def validate() -> int`

