# `tests/hwsd/test_a_hwsd_ref.py`

- Source: [tests/hwsd/test_a_hwsd_ref.py](../../../../../tests/hwsd/test_a_hwsd_ref.py)
- Kind: python
- Lines: 353

## Module docstring

> Author A (job 0197): an independent reference reading of HWSD-DESIGN-v1 §5 (no hwsd code).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 13)
- `random` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_a_evaluate.py](test_a_evaluate.py.md) (line 23, import)
- [tests/hwsd/test_a_evaluate.py](test_a_evaluate.py.md) (line 24, import)
- [tests/hwsd/test_a_kd4.py](test_a_kd4.py.md) (line 33, import)
- [tests/hwsd/test_a_known_bound.py](test_a_known_bound.py.md) (line 37, import)
- [tests/hwsd/test_a_onsets_order.py](test_a_onsets_order.py.md) (line 24, import)
- [tests/hwsd/test_a_onsets_order.py](test_a_onsets_order.py.md) (line 25, import)
- [tests/hwsd/test_a_statements.py](test_a_statements.py.md) (line 24, import)
- [tests/hwsd/test_a_statements.py](test_a_statements.py.md) (line 25, import)

## Top-level constants

- `F9`
- `KD4_EXPECTED`
- `KD4_ROWS`
- `M`
- `MASTERS`
- `PER_MODEL`
- `STEPS`

## Classes and functions

- **function `fr`** [L22-23]: `def fr(x)`
- **function `ref_model_status`** [L26-40]: `def ref_model_status(L, U, Fm, Fp) -> dict` - K4B §8.1 as stated in tools/k4b/API.md (model_status), in exact rationals.
- **function `row`** [L44-54]: `def row(status, valid=None, L=None, U=None, L_S=None, U_S=None, F=F9, learn=False, b2=None, step=0, Fm=None, Fp=None)`
- **function `NOC`** [L57-58]: `def NOC(**k)`
- **function `EXC`** [L61-62]: `def EXC(status=SC, **k)`
- **function `SUP`** [L65-66]: `def SUP(status=SC, **k)`
- **function `UNR`** [L69-70]: `def UNR(status=SC, **k)`
- **function `UNV`** [L73-74]: `def UNV(**k)`
- **function `seq`** [L77-83]: `def seq(*rows)`
- **function `est`** [L87-88]: `def est(r)`
- **function `ok`** [L91-92]: `def ok(r)`
- **function `sigma`** [L95-96]: `def sigma(r)`
- **function `above_s`** [L99-100]: `def above_s(r)`
- **function `below_s`** [L103-104]: `def below_s(r)`
- **function `above_s_ok`** [L107-108]: `def above_s_ok(r)`
- **function `_first`** [L111-115]: `def _first(rows, pred)`
- **function `onsets`** [L119-130]: `def onsets(rows)`
- **function `_pre`** [L133-136]: `def _pre(rows)`
- **function `n_pre`** [L139-140]: `def n_pre(rows)`
- **function `pre_chart_max`** [L143-145]: `def pre_chart_max(rows)`
- **function `order`** [L149-170]: `def order(rows, anchor, A=None)`
- **function `_ne`** [L174-175]: `def _ne(reason)`
- **function `d1`** [L178-184]: `def d1(rows)`
- **function `d2`** [L187-200]: `def d2(rows)`
- **function `_d34`** [L203-209]: `def _d34(rows, anchor)`
- **function `d3`** [L212-213]: `def d3(rows)`
- **function `d4`** [L216-217]: `def d4(rows)`
- **function `d5`** [L220-232]: `def d5(rows)`
- **function `d6`** [L235-242]: `def d6(rows)`
- **function `aggregate`** [L248-270]: `def aggregate(statement, per)` - per: {j: (reading, reason, qualifier)} -> (reading, {reason: sorted models}).
- **function `evaluate`** [L273-275]: `def evaluate(table)`
- **function `cmp_line`** [L278-281]: `def cmp_line(a, b)`
- **function `est_loss`** [L284-287]: `def est_loss(rows)`
- **function `random_row`** [L291-298]: `def random_row(rng: random.Random)`
- **function `random_table`** [L301-303]: `def random_table(rng: random.Random, K=None)`
- **function `kd4_table`** [L324-325]: `def kd4_table(cases)`
- **test `test_reference_reproduces_api_17_3`** [L328-336]: `def test_reference_reproduces_api_17_3()`
- **test `test_reference_model_status_boundaries`** [L339-345]: `def test_reference_model_status_boundaries()`
- **test `test_reference_planted_presets`** [L348-353]: `def test_reference_planted_presets()`

