# `tools/hwsb/hwsb_dry2.py`

- Source: [tools/hwsb/hwsb_dry2.py](../../../../../tools/hwsb/hwsb_dry2.py)
- Kind: python
- Lines: 334

## Module docstring

> HWSB dry-run cases DRB8-DRB16 and DRB13b (API.md §9; TEST_PLAN §4); split from hwsb_dry
> by size. Same rules: DRY streams and masters only; planted fixtures labelled "fixture": true.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 7, via same directory)
- `import hws_driver` -> [tools/hws/hws_driver.py](../hws/hws_driver.py.md) (line 14, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 15, via same directory)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 16, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](hwsb_eval.py.md) (line 17, via same directory)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 18, via same directory)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 19, via same directory)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](hwsb_law.py.md) (line 20, via same directory)
- `import hwsb_meter_bind` -> [tools/hwsb/hwsb_meter_bind.py](hwsb_meter_bind.py.md) (line 21, via same directory)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](hwsb_train.py.md) (line 22, via same directory)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 23, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 25, via unique basename)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../x4_circle_history/process_law.py.md) (line 26, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from hwsb_dry import FIX, _dir, _mem, _res, _tiny_store` -> [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 29, via same directory)
- `from topo_pilot.activations import ActivationExtractor` -> [src/topo_pilot/activations/__init__.py](../../src/topo_pilot/activations/__init__.py.md) (line 31, via package root)
- `from topo_pilot.contracts import Checkpoint, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 32, via package root)
- `from topo_pilot.dataset import DatasetConfig, PanelBuilder` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 33, via package root)
- `from topo_pilot.process import EmissionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 34, via package root)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 11)
- `json` (lines 8)
- `pathlib` (lines 12)
- `shutil` (lines 9)
- `types` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 155, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 344, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 19, import)

## Top-level constants

- none

## Classes and functions

- **function `e4_eval_check`** [L37-57]: `def e4_eval_check(store, ckpt_id, ids, proc, m, plan) -> dict` - DRB2 extension: the real 36-symbol EVAL path (model_inputs BOS 36, model_predictive,
- **function `drb8`** [L60-85]: `def drb8(out, ctx) -> dict`
- **function `drb9`** [L88-115]: `def drb9(out, ctx) -> dict`
- **function `drb10`** [L118-126]: `def drb10(out, ctx) -> dict`
- **function `drb11`** [L129-155]: `def drb11(out, ctx) -> dict`
- **function `drb12`** [L158-187]: `def drb12(out, ctx) -> dict`
- **function `drb13`** [L190-218]: `def drb13(out, ctx) -> dict`
- **function `drb13b`** [L221-234]: `def drb13b(out, ctx) -> dict`
- **function `drb14`** [L237-292]: `def drb14(out, ctx) -> dict`
- **function `drb15`** [L295-315]: `def drb15(out, ctx) -> dict`
- **function `drb16`** [L318-334]: `def drb16(out, ctx) -> dict`

