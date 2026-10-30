# `tools/k4b/k4b_charts.py`

- Source: [tools/k4b/k4b_charts.py](../../../../../tools/k4b/k4b_charts.py)
- Kind: python
- Lines: 215

## Module docstring

> K4b ledgers, chart construction wrappers, C0 gates, freeze and determinism (API.md §6).

## Imports

### Internal (repo files)

- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 13, via unique basename)
- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 14, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 15, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 17, via unique basename)
- `from c1_records import C1GateFailure, adapt_chart_exception, classify_exception` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 18, via unique basename)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 130, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 8)
- `json` (lines 10)
- `pathlib` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 25, import)
- [tools/hwsb/hwsb_gates.py](../hwsb/hwsb_gates.py.md) (line 14, import)
- [tools/hwsb/hwsb_stages.py](../hwsb/hwsb_stages.py.md) (line 22, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 182, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 17, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 17, import)

## Top-level constants

- `FROZEN`
- `INIT_LEDGER`
- `LINEAGE`
- `TRAINED_LEDGER`
- `UNAVAILABLE`

## Classes and functions

- **class `InitLedger`** [L27-40] - The step-0 ledger: production claims only (at most 3, one per model).
- **method `InitLedger.__init__`** [L30-32]: `def __init__(self, path)`
- **method `InitLedger.claim`** [L34-37]: `def claim(self, model, role) -> None`
- **method `InitLedger.claims`** [L39-40]: `def claims(self) -> list`
- **function `open_ledgers`** [L43-45]: `def open_ledgers(out) -> tuple`
- **function `_status_of_exception`** [L48-53]: `def _status_of_exception(exc) -> tuple`
- **function `_diagnostics`** [L56-62]: `def _diagnostics(ch, gauge) -> dict`
- **function `build_chart`** [L65-88]: `def build_chart(X, ids, m32, ledger, model, role, cfg, guard=None, timed=None, persist=None) -> dict` - Claim (model, role) first, then fit once; never retried.
- **function `_m32_for`** [L91-92]: `def _m32_for(m32_land, j)`
- **function `c0_cal`** [L95-104]: `def c0_cal(models, X_cal, ids, m32_land, out, cfg, guard=None, timed=None, persist=None) -> dict`
- **function `init_charts`** [L107-121]: `def init_charts(models, X_cal_init, ids, m32_land, out, cfg, guard=None, timed=None, persist=None) -> dict` - Step-0 charts: a valid CHART_UNAVAILABLE is INIT_UNAVAILABLE (non-gating); any
- **function `_sha`** [L124-125]: `def _sha(path) -> str`
- **function `freeze_production`** [L128-153]: `def freeze_production(out, charts, init, decoders) -> dict` - Writes every production chart, step-0 chart and decoder, then PRODUCTION_FROZEN.json.
- **function `require_frozen`** [L156-165]: `def require_frozen(out) -> dict`
- **function `extend`** [L168-173]: `def extend(prod, gauge, Q, cfg, timed=None)`
- **function `c0_val_gate`** [L176-197]: `def c0_val_gate(models, prod, val_X, ids_val, out, cfg, guard=None, timed=None, persist=None) -> dict` - require_frozen; one direct chart per model; c1_chart.c0_val unchanged.
- **function `init_val_diagnostics`** [L200-204]: `def init_val_diagnostics(prod_init, gauge_init, val_X_panel, cfg) -> dict`
- **function `determinism_check`** [L207-215]: `def determinism_check(stored, recomputed) -> dict`

