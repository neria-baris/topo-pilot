# `tools/hwsd/hwsd_dry3.py`

- Source: [tools/hwsd/hwsd_dry3.py](../../../../../tools/hwsd/hwsd_dry3.py)
- Kind: python
- Lines: 399

## Module docstring

> hwsd dry-run cases DRD2, DRD3, DRD6, DRD7, DRD12, DRD13, DRD14 (API.md §12; TEST_PLAN §4).
> Split from hwsd_dry by size; DRD2, DRD3, DRD6 are re-exported from hwsd_dry by its lazy __getattr__.
> Fixtures live under test_hwsd-<job>/dry/<case>/ (decision 6); nothing real is opened.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 14, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 15, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../hwsb/hwsb_dry.py.md) (line 16, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../hwsb/hwsb_train.py.md) (line 17, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../hwsc/hwsc_bind.py.md) (line 18, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 19, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 20, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 21, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 22, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 23, via unique basename)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 24, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 25, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 26, via unique basename)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](../k4b/k4b_decoder.py.md) (line 27, via unique basename)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 28, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 29, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 30, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 32, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 33, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 34, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 36, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 37, via same directory)
- `import hwsd_known` -> [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 38, via same directory)
- `import hwsd_meter_bind` -> [tools/hwsd/hwsd_meter_bind.py](hwsd_meter_bind.py.md) (line 39, via same directory)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 40, via same directory)
- `from hwsd_dry import KD4_DEFAULT, _job, _res, case_dir, fresh_fixture, plant_acts, proc_star, in_memory_rows` -> [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 41, via same directory)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 44, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 45, via package root)
- `import hwsc_dry` -> [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 303, via unique basename) (inside a function)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 304, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 31)

### Standard library

- `__future__` (lines 5)
- `builtins` (lines 8)
- `importlib` (lines 100)
- `io` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 12)
- `types` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 103: `dynamic: r['module']`
- `import_module` line 131: `dynamic: m_`

### sys.path additions

- none

## Imported by

- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 364, import)

## Top-level constants

- none

## Classes and functions

- **function `_raises`** [L48-53]: `def _raises(fn, status=None) -> bool`
- **function `_tops`** [L56-57]: `def _tops(a) -> set`
- **function `drd2`** [L60-96]: `def drd2(out, ctx) -> dict` - Real E4 architecture, 20-step checkpoints of one master on 2,048 in-memory w* rows.
- **function `drd3`** [L99-133]: `def drd3(out, ctx) -> dict`
- **function `drd6`** [L136-187]: `def drd6(out, ctx) -> dict`
- **function `drd12`** [L190-219]: `def drd12(out, ctx) -> dict`
- **function `_raises_value`** [L222-227]: `def _raises_value(fn) -> bool`
- **class `_OpenHook`** [L230-253] - Records every open() of a path containing one of the blinded tokens.
- **method `_OpenHook.__init__`** [L233-234]: `def __init__(self, tokens)`
- **method `_OpenHook.__enter__`** [L236-250]: `def __enter__(self)`
- **method `_OpenHook.__exit__`** [L252-253]: `def __exit__(self, *e)`
- **function `drd13`** [L256-298]: `def drd13(out, ctx) -> dict`
- **function `_repro_stage_c`** [L301-342]: `def _repro_stage_c(fx) -> dict` - (1) A fresh stage-C DRC1 case: its recorded C0-CAL outcome reproduced by chart_one.
- **function `drd14`** [L345-399]: `def drd14(out, ctx) -> dict`

