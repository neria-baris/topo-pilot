# `tools/hwsu/u2/hwsu_dry2d.py`

- Source: [tools/hwsu/u2/hwsu_dry2d.py](../../../../../../tools/hwsu/u2/hwsu_dry2d.py)
- Kind: python
- Lines: 222

## Module docstring

> HWSU dry run DRU-REG: the planted-defect registry fixtures of API_U2.md section 6
> (R-0223-9 part 3): renamed, missing, unreadable and re-hashed S3 tables of the stage-C store,
> the planted Checkpoint payload.npz and sealed/ never opened (an audit hook records zero opens),
> the S-2 superset diagnostic and the K-REG2 digest file, the hwsd-store READER fixtures and the
> obligation fixtures (DRO9 through read_obligation_u2, a stopped E1, the KC obligation).
> Synthetic stores under the helper folder only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 11, via unique basename)
- `import hwsu_dry2c` -> [tools/hwsu/u2/hwsu_dry2c.py](hwsu_dry2c.py.md) (line 12, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 13, via unique basename)
- `import hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 14, via same directory)
- `import hwsu_regsrc` -> [tools/hwsu/u2/hwsu_regsrc.py](hwsu_regsrc.py.md) (line 15, via same directory)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 16, via unique basename)
- `import hwsc_dry` -> [tools/hwsc/hwsc_dry.py](../../hwsc/hwsc_dry.py.md) (line 21, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../k4b/k4b_data.py.md) (line 22, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 24, via unique basename)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 9)
- `json` (lines 17)
- `pathlib` (lines 19)
- `sys` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md) (line 15, import)

## Top-level constants

- `HIST`
- `INC`
- `OPENS`
- `WATCH`
- `WATCHED`

## Classes and functions

- **function `_audit`** [L32-34]: `def _audit(event, args)`
- **function `_table`** [L40-45]: `def _table(path, n=16, seed=1) -> None`
- **function `_contract`** [L48-53]: `def _contract(hist) -> dict`
- **function `hwsc_fixture`** [L60-89]: `def hwsc_fixture(base, mutate=None, extra=None)` - A synthetic stage-C store with the four U2 tables and the observation inventory.
- **function `s3_defects`** [L92-100]: `def s3_defects(base) -> dict`
- **function `never_opened`** [L103-121]: `def never_opened(base) -> dict`
- **function `kreg2`** [L124-154]: `def kreg2(base) -> dict` - S-2: the K-REG2 digest file holds a digest the reader-built union lacks.
- **function `hwsd_reader`** [L157-168]: `def hwsd_reader(base) -> dict` - A conforming hwsd-store obligation is read (READER U5); a stray array is not.
- **function `obligations`** [L171-214]: `def obligations(base) -> dict` - DRO9 through read_obligation_u2, a stopped E1 and the KC obligation.
- **function `fixtures`** [L217-222]: `def fixtures(base) -> dict`

