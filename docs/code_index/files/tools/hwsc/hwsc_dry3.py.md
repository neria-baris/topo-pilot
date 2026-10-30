# `tools/hwsc/hwsc_dry3.py`

- Source: [tools/hwsc/hwsc_dry3.py](../../../../../tools/hwsc/hwsc_dry3.py)
- Kind: python
- Lines: 198

## Module docstring

> HWSC dry-run cases DRC10-DRC14 (sealing and D6, blindness, records/budget/hold, meter,
> G0c needles; API.md §8; rulings R-0176-G1, G2, G5, G12). Split from hwsc_dry2 by size.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 6, via same directory)
- `import hws_driver` -> [tools/hws/hws_driver.py](../hws/hws_driver.py.md) (line 11, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../hwsb/hwsb_train.py.md) (line 12, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 13, via same directory)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 14, via same directory)
- `import hwsc_meter_bind` -> [tools/hwsc/hwsc_meter_bind.py](hwsc_meter_bind.py.md) (line 15, via same directory)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 16, via same directory)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 17, via same directory)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 20, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 23, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 24, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 25, via unique basename)
- `from hwsc_dry import _mem, build_tiny_process_c, case_dir` -> [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 26, via same directory)
- `from hwsc_dry2 import _res` -> [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 27, via same directory)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 29, via package root)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 93, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 4)
- `dataclasses` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 247, import)

## Top-level constants

- none

## Classes and functions

- **function `drc10`** [L33-53]: `def drc10(out, ctx) -> dict`
- **function `drc11`** [L57-88]: `def drc11(out, ctx) -> dict`
- **function `_tiny_train`** [L92-97]: `def _tiny_train(store, proc, plan, m, hold=None)`
- **function `drc12`** [L100-149]: `def drc12(out, ctx) -> dict`
- **function `drc13`** [L153-177]: `def drc13(out, ctx) -> dict`
- **function `drc14`** [L181-198]: `def drc14(out, ctx) -> dict`

