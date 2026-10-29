# `tools/hwsc/hwsc_dry2.py`

- Source: [tools/hwsc/hwsc_dry2.py](../../../../../tools/hwsc/hwsc_dry2.py)
- Kind: python
- Lines: 247

## Module docstring

> HWSC dry-run cases DRC5-DRC14 (API.md §8; protocol §7; TEST_PLAN §4; rulings R-0176-G1..G5,
> G9, G12). Split from hwsc_dry by size; every case is synthetic and reads EXACT.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 6, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 11, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 12, via unique basename)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../hwsb/hwsb_law.py.md) (line 13, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 14, via same directory)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 15, via same directory)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 16, via same directory)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 17, via same directory)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 18, via same directory)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 19, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 22, via unique basename)
- `from hwsc_dry import _mem, case_dir` -> [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 23, via same directory)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../hwsb/hwsb_gates.py.md) (line 101, via unique basename) (inside a function)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 181, via unique basename) (inside a function)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 182, via unique basename) (inside a function)
- `from hwsc_dry import stub_sources, synthetic_root` -> [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 183, via same directory) (inside a function)
- `from hwsc_dry3 import drc10, drc11, drc12, drc13, drc14` -> [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 247, via same directory)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 9)
- `json` (lines 7)
- `math` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 204: `scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md)

### sys.path additions

- none

## Imported by

- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 298, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 27, import)

## Top-level constants

- none

## Classes and functions

- **function `_res`** [L27-29]: `def _res(ok, **details) -> dict`
- **function `_raises`** [L32-37]: `def _raises(fn, status=None) -> bool`
- **function `drc5`** [L41-84]: `def drc5(out, ctx) -> dict` - Planted endpoint fixtures: decision boundaries in exact Fractions and the annotation.
- **function `drc6`** [L88-113]: `def drc6(out, ctx) -> dict`
- **function `drc7`** [L117-147]: `def drc7(out, ctx) -> dict`
- **function `drc8`** [L151-169]: `def drc8(out, ctx) -> dict`
- **function `_c2_table`** [L173-177]: `def _c2_table(path, digests, seq)`
- **function `drc9`** [L180-244]: `def drc9(out, ctx) -> dict`

