# `tools/hwsb/hwsb_gates.py`

- Source: [tools/hwsb/hwsb_gates.py](../../../../../tools/hwsb/hwsb_gates.py)
- Kind: python
- Lines: 382

## Module docstring

> HWSB gates: B4 orchestration, the pilot ladder (B6), capture (B5), B7, B9a, the outcome
> precedence, licences and HANDOFF (API.md §6; protocol §4, §5, §6.1).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 7, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 12, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 13, via same directory)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 14, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 15, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 17, via unique basename)
- `from hwsb_config import ALPHA_C, M` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 18, via same directory)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 265, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 5)
- `collections` (lines 9)
- `fractions` (lines 10)
- `math` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_a_capture.py](../../tests/hwsb/test_a_capture.py.md) (line 36, import)
- [tests/hwsb/test_a_endpoints.py](../../tests/hwsb/test_a_endpoints.py.md) (line 35, import)
- [tests/hwsb/test_a_ladder.py](../../tests/hwsb/test_a_ladder.py.md) (line 38, import)
- [tests/hwsb/test_a_outcomes.py](../../tests/hwsb/test_a_outcomes.py.md) (line 29, import)
- [tests/hwsb/test_b_registry.py](../../tests/hwsb/test_b_registry.py.md) (line 25, import)
- [tests/hwsc/test_a_ladder.py](../../tests/hwsc/test_a_ladder.py.md) (line 28, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 18, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 23, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 18, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 17, import)
- [tools/hwsc/hwsc_dry2.py](../hwsc/hwsc_dry2.py.md) (line 101, import)
- [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 15, import)
- [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 200, import)

## Top-level constants

- `NOT_CHARTED`
- `SIDES`
- `UNDERPOWERED`

## Classes and functions

- **function `_cfg`** [L27-28]: `def _cfg(cfg)`
- **function `b4_cal`** [L31-37]: `def b4_cal(out, X_cal, ids, m32_land, cfg=None) -> dict`
- **function `b4_init`** [L40-41]: `def b4_init(out, X_init, ids, m32_land, cfg=None) -> dict`
- **function `b4_freeze`** [L44-46]: `def b4_freeze(out, cal, init) -> dict`
- **function `b4_val`** [L49-59]: `def b4_val(out, cal, X_val, ids_val, cfg=None) -> dict`
- **function `_st`** [L62-65]: `def _st(rec, j)`
- **function `b4_status`** [L68-87]: `def b4_status(cal, val, masters) -> dict`
- **function `_q`** [L93-94]: `def _q(col, p) -> float`
- **function `_projection`** [L97-116]: `def _projection(e, keys, models, F_plan) -> dict`
- **function `_width`** [L119-128]: `def _width(D_bar, e, keys, models, F_plan) -> dict`
- **function `_mde_ok`** [L131-138]: `def _mde_ok(sdU, N, F_plan) -> bool`
- **function `ladder_pilot`** [L141-182]: `def ladder_pilot(X_minus, X_plus, r4n, F_plan, models=hc.MASTERS, seeds=(hc.SEEDS['sd_upper'], hc.SEEDS['projection']), D_bar=None, ladder=hc.LADDER) -> dict` - k4b_stats.ladder with the model list as an argument (DRB9 bitwise on K4b keys).
- **function `b5_N`** [L185-187]: `def b5_N(ladder_result) -> int`
- **function `c_min`** [L193-200]: `def c_min(sdU_minus, N_C, F_plan, D4hat) -> float`
- **function `c_min_literal`** [L203-204]: `def c_min_literal(sdU_minus, N_C, F_plan, D4hat) -> float`
- **function `capture_pass`** [L207-208]: `def capture_pass(c_hat, c_min_value) -> bool`
- **function `b5`** [L211-240]: `def b5(X_minus, D4_rows, sdU_minus, N_C, F_plan, models, seed=hc.SEEDS['capture_ci']) -> dict`
- **function `b7`** [L246-260]: `def b7(cpu_by_model, N_C) -> dict`
- **function `b9a`** [L263-286]: `def b9a(store, N_C, p_d2a, p_d2a_ref, eval_blocks) -> dict` - B9a; (i)/(ii) hash and read stage B's OWN history payloads (ruling c7).
- **function `outcome`** [L292-335]: `def outcome(state) -> dict`
- **function `_head`** [L338-343]: `def _head(o) -> str`
- **function `licence`** [L346-356]: `def licence(oc, fill) -> str`
- **function `check_handoff`** [L359-372]: `def check_handoff(obj, top=True) -> None`
- **function `handoff_record`** [L375-382]: `def handoff_record(fields) -> dict`

