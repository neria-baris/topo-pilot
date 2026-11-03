# `tools/hwsu/u2/hwsu_dry2c.py`

- Source: [tools/hwsu/u2/hwsu_dry2c.py](../../../../../../tools/hwsu/u2/hwsu_dry2c.py)
- Kind: python
- Lines: 238

## Module docstring

> HWSU model-phase dry run: the stage jobs KC, E1, REG2 and E2 through run_job on a synthetic
> store (API_U2.md section 6, DRU1; R-0223-9 part 1; the HWSC/HWSG planted-adapter precedent).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 12, via unique basename)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../hwsu_dry.py.md) (line 13, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../hwsc/hwsc_data.py.md) (line 14, via unique basename)
- `import hwsc_dry` -> [tools/hwsc/hwsc_dry.py](../../hwsc/hwsc_dry.py.md) (line 15, via unique basename)
- `import hwsu_driver` -> [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 16, via same directory)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../hwsu_oracle.py.md) (line 17, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 18, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 19, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../c1prime/c1_means.py.md) (line 25, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 27, via unique basename)
- `import topo_pilot.learner` -> [src/topo_pilot/learner/__init__.py](../../../src/topo_pilot/learner/__init__.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 26)
- `torch` (lines 29)

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 20)
- `json` (lines 21)
- `pathlib` (lines 23)
- `time` (lines 22)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md) (line 14, import)
- [tools/hwsu/u2/hwsu_dry2d.py](hwsu_dry2d.py.md) (line 12, import)

## Top-level constants

- `PLANTED_INPUTS`

## Classes and functions

- **function `_w`** [L32-33]: `def _w(path, data) -> Path`
- **function `synthetic_root_u`** [L36-46]: `def synthetic_root_u(base) -> dict` - The phase-1 synthetic root with the phase-2 authority fixtures added.
- **function `of_fixture`** [L49-85]: `def of_fixture(store, sr) -> dict` - Synthetic OF store files: FREEZE_OF, OF_ACCEPT, OF_REPORT and two blocks of OF eval pairs
- **function `registry_sources`** [L88-96]: `def registry_sources() -> dict` - Planted registry sources (hwsc_dry stubs): the stores of earlier studies are not scanned.
- **function `_kc2`** [L99-101]: `def _kc2(ctx) -> dict`
- **function `_h1u`** [L104-116]: `def _h1u(ctx) -> dict` - Three random-init 4-layer models stand in for the stage-C checkpoints.
- **function `_h5u`** [L119-121]: `def _h5u(ctx) -> dict` - H5-U headroom is a property of the production geometry; the tiny world has none.
- **function `stage_extra`** [L124-126]: `def stage_extra(sr) -> dict` - Dry-only seams of the E2 job: the stage-C loader (planted models) and the H5 floor.
- **function `planted_default`** [L129-130]: `def planted_default(sr) -> dict`
- **function `write_auth`** [L133-144]: `def write_auth(store, job, stage, sr) -> Path`
- **function `stage_ctx`** [L147-160]: `def stage_ctx(store, sr, job, stage, planted, **extra) -> dict`
- **function `prepare`** [L163-184]: `def prepare(store, stage, rid) -> None` - Coordinator-side files of a drawing job: reservation and the release record.
- **function `run_stage`** [L187-198]: `def run_stage(store, sr, job, stage, planted, reservation_id=None, dry_continue=True, **extra) -> dict`
- **function `run_stages`** [L215-238]: `def run_stages(base) -> dict` - KC, E1, REG2 and E2 through run_job on one synthetic store (R-0223-9 part 1).

