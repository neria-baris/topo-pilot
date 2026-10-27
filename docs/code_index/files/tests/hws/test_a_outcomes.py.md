# `tests/hws/test_a_outcomes.py`

- Source: [tests/hws/test_a_outcomes.py](../../../../../tests/hws/test_a_outcomes.py)
- Kind: python
- Lines: 318

## Module docstring

> Author A (job 0119): S3 evaluation, selection, every outcome branch and the licences.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 23, via sys.path edit)
- `import hws_select` -> [tools/hws/hws_select.py](../../tools/hws/hws_select.py.md) (line 24, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `fractions` (lines 11)
- `json` (lines 9)
- `pathlib` (lines 12)
- `statistics` (lines 13)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `HWS_DIR` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `CRIT`
- `F`
- `FIN`
- `FLOORS`
- `HEAD`
- `HWS_DIR`
- `KEYS`
- `LIC`
- `REPO`
- `S3_CASES`
- `SEL_CASES`
- `SEL_FILL`
- `Z1`
- `ZW`

## Classes and functions

- **class `Records(list)`** [L35-61] - API-AMBIGUITY: `records` may be read as a list of records or as {key: record}; this
- **method `Records.__init__`** [L39-41]: `def __init__(self, recs)`
- **method `Records.keys`** [L43-44]: `def keys(self)`
- **method `Records.values`** [L46-47]: `def values(self)`
- **method `Records.items`** [L49-50]: `def items(self)`
- **method `Records.get`** [L52-53]: `def get(self, k, default=None)`
- **method `Records.__getitem__`** [L55-58]: `def __getitem__(self, i)`
- **method `Records.__contains__`** [L60-61]: `def __contains__(self, k)`
- **function `bnd`** [L64-66]: `def bnd(mean, se=0.001)`
- **function `my_class`** [L69-77]: `def my_class(elig, b)`
- **function `rec`** [L80-91]: `def rec(W, q, s, p, d4=0.05, gc=0.3, g4=0.05, g4a=0.05, elig='ELIGIBLE', stage='S1')`
- **function `s3e`** [L94-96]: `def s3e(kind='ordinary', qual=False, below=False, at=False)`
- **function `state`** [L99-102]: `def state(recs, ordinary=(), fallback=(), s3=None, complete=True, fail=None)`
- **function `_sel_state`** [L116-118]: `def _sel_state(quals, **kw)`
- **test `test_selected_first_ordinary_qualifier_in_finalist_order`** [L122-133]: `def test_selected_first_ordinary_qualifier_in_finalist_order(name, quals, out, sel, fb)` decorators: @pytest.mark.parametrize('name, quals, out, sel, fb', SEL_CASES, ids=[c[0] for c in SEL_CASES])
- **test `test_fail_technical_first_then_inconclusive`** [L136-142]: `def test_fail_technical_first_then_inconclusive()`
- **test `test_fallback_only_worlds_give_below_3x_never_selected`** [L145-155]: `def test_fallback_only_worlds_give_below_3x_never_selected()`
- **function `_below_state`** [L158-165]: `def _below_state(extra=())`
- **test `test_below_3x_absence_shown`** [L168-175]: `def test_below_3x_absence_shown()`
- **test `test_below_3x_absence_not_shown`** [L178-185]: `def test_below_3x_absence_not_shown()`
- **test `test_absence_shown_ignores_ineligible_worlds`** [L188-192]: `def test_absence_shown_ignores_ineligible_worlds()`
- **function `_nwc_state`** [L195-198]: `def _nwc_state(extra)`
- **test `test_no_world_confirmed_needs_an_unresolved_world`** [L201-206]: `def test_no_world_confirmed_needs_an_unresolved_world()`
- **test `test_ineligible_world_with_passing_bounds_is_not_unresolved`** [L209-213]: `def test_ineligible_world_with_passing_bounds_is_not_unresolved()`
- **test `test_no_suitable_world_headroom`** [L220-227]: `def test_no_suitable_world_headroom()`
- **test `test_no_suitable_world_filter`** [L230-237]: `def test_no_suitable_world_filter()`
- **test `test_paused_search_never_gets_the_no_world_licence`** [L240-245]: `def test_paused_search_never_gets_the_no_world_licence()`
- **test `test_outcome_fallthrough_is_fail_technical_outcome`** [L248-257]: `def test_outcome_fallthrough_is_fail_technical_outcome()`
- **function `_s3rec`** [L260-265]: `def _s3rec(d4=0.03, gc=0.1, g4=0.0078, g4a=0.004, elig='ELIGIBLE')`
- **test `test_s3_evaluate`** [L281-286]: `def test_s3_evaluate(kind, kw, qual, below, at)` decorators: @pytest.mark.parametrize('kind, kw, qual, below, at', S3_CASES)
- **test `test_licence_selected`** [L294-303]: `def test_licence_selected(tier)` decorators: @pytest.mark.parametrize('tier', [0, 1, 2])
- **test `test_licence_other_outcomes`** [L306-318]: `def test_licence_other_outcomes()`

