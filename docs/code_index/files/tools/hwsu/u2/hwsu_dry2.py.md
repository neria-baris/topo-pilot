# `tools/hwsu/u2/hwsu_dry2.py`

- Source: [tools/hwsu/u2/hwsu_dry2.py](../../../../../../tools/hwsu/u2/hwsu_dry2.py)
- Kind: python
- Lines: 247

## Module docstring

> HWSU model-phase dry run DRU, response family (API_U2.md section 6; protocol 9).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 12, via unique basename)
- `import hwsu_dry2b` -> [tools/hwsu/u2/hwsu_dry2b.py](hwsu_dry2b.py.md) (line 13, via same directory)
- `import hwsu_freeze` -> [tools/hwsu/hwsu_freeze.py](../hwsu_freeze.py.md) (line 14, via unique basename)
- `import hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 15, via same directory)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 16, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 17, via unique basename)
- `import hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 18, via same directory)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../hwsu_dry.py.md) (line 19, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 20, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../../c1prime/c1_model.py.md) (line 24, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../c2_readout/c2_model.py.md) (line 25, via unique basename)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../hwsb/hwsb_config.py.md) (line 26, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../hwsb/hwsb_dry.py.md) (line 27, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../../hwsb/hwsb_train.py.md) (line 28, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../hwsc/hwsc_data.py.md) (line 29, via unique basename)
- `import hwsc_dry` -> [tools/hwsc/hwsc_dry.py](../../hwsc/hwsc_dry.py.md) (line 30, via unique basename)
- `import hwsc_registry_build` -> [tools/hwsc/hwsc_registry_build.py](../../hwsc/hwsc_registry_build.py.md) (line 31, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 33, via unique basename)
- `import topo_pilot.contracts` -> [src/topo_pilot/contracts/__init__.py](../../../src/topo_pilot/contracts/__init__.py.md) (line 34, via package root)
- `import topo_pilot.contracts.backends` -> [src/topo_pilot/contracts/backends.py](../../../src/topo_pilot/contracts/backends.py.md) (line 35, via package root)
- `import topo_pilot.learner` -> [src/topo_pilot/learner/__init__.py](../../../src/topo_pilot/learner/__init__.py.md) (line 36, via package root)

### External (third-party)

- `numpy` (lines 32)
- `torch` (lines 37)

### Standard library

- `__future__` (lines 10)
- `json` (lines 21)
- `pathlib` (lines 22)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_records.py](../../../tests/hwsu/test_b_u2_records.py.md) (line 41, dynamic)
- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 258, dynamic)
- [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 316, dynamic)

## Top-level constants

- `CASES`
- `DRU_SITE`
- `EQ_KEYS`

## Classes and functions

- **function `tiny_plan`** [L47-57]: `def tiny_plan(case='DRU1')` - The tiny training plan: CONTRACT dry_run_u2 tiny_model / tiny_train / tiny_masters, sizes
- **function `_train_one`** [L60-69]: `def _train_one(store, proc, plan, m) -> dict` - hwsb_data admits only hwsb_config.DRY_MASTERS for a dry plan; U's tiny masters (OPEN-6)
- **function `tiny_models`** [L72-82]: `def tiny_models(store, proc, plan=None) -> dict` - Three tiny models trained by hwsb_train.train on make_train_dev_c ObservationSets under
- **function `dru1`** [L85-112]: `def dru1(base, ctx=None) -> dict` - The tiny world with real training: three tiny models, their checkpoints, TRAIN_RECORD
- **function `dru2`** [L115-153]: `def dru2(base, ctx=None) -> dict` - Real architecture, random init (seed 649910), 2,048 in-memory w* DRY pairs: BASIS, M0, X1
- **function `_build_equality`** [L161-188]: `def _build_equality(base) -> dict` - build_u equals hwsc_registry_build.build on a synthetic root with stage C's source map
- **function `dru_reg`** [L191-212]: `def dru_reg(base, ctx=None) -> dict`
- **function `run_dru`** [L215-247]: `def run_dru(out, only=None) -> dict`

