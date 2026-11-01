# `tools/hwsd/hwsd_statements.py`

- Source: [tools/hwsd/hwsd_statements.py](../../../../../tools/hwsd/hwsd_statements.py)
- Kind: python
- Lines: 289

## Module docstring

> hwsd_statements: notation, onsets, ORDER and statements D1-D6 (API.md section 7).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 9, via same directory)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 10, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_a_evaluate.py](../../tests/hwsd/test_a_evaluate.py.md) (line 21, import)
- [tests/hwsd/test_a_kd4.py](../../tests/hwsd/test_a_kd4.py.md) (line 31, import)
- [tests/hwsd/test_a_onsets_order.py](../../tests/hwsd/test_a_onsets_order.py.md) (line 22, import)
- [tests/hwsd/test_a_statements.py](../../tests/hwsd/test_a_statements.py.md) (line 22, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 40, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 31, import)
- [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 15, import)

## Top-level constants

- `M`
- `STATEMENTS`
- `_FN`

## Classes and functions

- **function `est`** [L16-17]: `def est(row) -> bool`
- **function `ok`** [L20-21]: `def ok(row) -> bool`
- **function `fr`** [L24-25]: `def fr(x) -> Fraction`
- **function `sigma`** [L28-31]: `def sigma(row) -> str`
- **function `above_s`** [L34-35]: `def above_s(row) -> bool`
- **function `below_s`** [L38-39]: `def below_s(row) -> bool`
- **function `above_s_ok`** [L42-43]: `def above_s_ok(row) -> bool`
- **function `_first`** [L46-50]: `def _first(rows, pred, start=1)`
- **function `onsets`** [L53-72]: `def onsets(rows) -> dict`
- **function `n_pre`** [L75-78]: `def n_pre(rows) -> int`
- **function `pre_chart_max`** [L81-85]: `def pre_chart_max(rows)`
- **function `order`** [L88-116]: `def order(rows, anchor, A=None) -> dict`
- **function `_rd`** [L119-120]: `def _rd(reading, reason=None, qualifier=None) -> dict`
- **function `_ne`** [L123-124]: `def _ne(reason)`
- **function `d1`** [L127-133]: `def d1(rows) -> dict`
- **function `d2`** [L136-150]: `def d2(rows) -> dict`
- **function `_by_order`** [L153-159]: `def _by_order(rows, anchor) -> dict`
- **function `d3`** [L162-163]: `def d3(rows) -> dict`
- **function `d4`** [L166-167]: `def d4(rows) -> dict`
- **function `d5`** [L170-184]: `def d5(rows) -> dict`
- **function `d6`** [L187-195]: `def d6(rows) -> dict`
- **function `aggregate`** [L201-228]: `def aggregate(statement, per_model) -> dict`
- **function `onset_order_line`** [L231-241]: `def onset_order_line(table) -> dict`
- **function `diagnostics`** [L244-268]: `def diagnostics(table) -> dict`
- **function `evaluate`** [L271-289]: `def evaluate(table, headroom_ok=True, resource_ok=True) -> dict`

