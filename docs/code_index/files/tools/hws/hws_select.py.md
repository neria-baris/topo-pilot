# `tools/hws/hws_select.py`

- Source: [tools/hws/hws_select.py](../../../../../tools/hws/hws_select.py)
- Kind: python
- Lines: 304

## Module docstring

> HWS selection rule: criteria, classes, ranking, finalists, X1/S2, outcomes, licences, budget
> (API.md §5 and erratum E1, E2, E5, E6, E15; protocol §5, §6.2, §7, §9).

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 13, via same directory)
- `import hws_stats` -> [tools/hws/hws_stats.py](hws_stats.py.md) (line 14, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 11)
- `math` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_a_budget.py](../../tests/hws/test_a_budget.py.md) (line 19, import)
- [tests/hws/test_a_classify.py](../../tests/hws/test_a_classify.py.md) (line 22, import)
- [tests/hws/test_a_outcomes.py](../../tests/hws/test_a_outcomes.py.md) (line 24, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 20, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 19, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 20, import)
- [tools/hws/hws_records.py](hws_records.py.md) (line 21, import)

## Top-level constants

- `CRITERIA`
- `LIC`
- `NUMERICAL`
- `RATES`
- `TAU_D2A`

## Classes and functions

- **function `floors`** [L26-28]: `def floors(g4_w0: float, g4A_w0: float) -> dict`
- **function `criteria`** [L31-38]: `def criteria(bounds: dict, floors: dict, which: str) -> dict`
- **function `eligibility`** [L41-46]: `def eligibility(exact_status, e5_pass, e6_ok) -> str`
- **function `classify`** [L49-63]: `def classify(look, floors) -> dict` - §5.4 classes on screening data (R-HWS-1).
- **function `annotations`** [L66-73]: `def annotations(D4_bounds) -> list`
- **function `_recs`** [L76-77]: `def _recs(records) -> list`
- **function `_eligible`** [L80-81]: `def _eligible(r) -> bool`
- **function `_is_cand`** [L84-85]: `def _is_cand(r) -> bool`
- **function `_world`** [L88-89]: `def _world(r)`
- **function `rank_key`** [L92-94]: `def rank_key(rec) -> tuple`
- **function `_top_d4`** [L97-98]: `def _top_d4(recs) -> list`
- **function `finalists`** [L101-113]: `def finalists(records) -> dict` - §5.6 items 1-2 (RC-1): ordinary slots never take a MARGINAL world.
- **function `x1_trigger`** [L116-125]: `def x1_trigger(records) -> dict` - §6.2 item 1 (RC-6, choice 41).
- **function `_levels`** [L128-129]: `def _levels(base, extra, present) -> list`
- **function `s2_worklist`** [L132-155]: `def s2_worklist(records, cap=40) -> list` - §6.2 item 2 (RC-6 frozen p midpoints; choice 14).
- **function `s3_evaluate`** [L158-169]: `def s3_evaluate(rec_s3, floors, kind) -> dict` - §5.6 item 3, §7.1 BELOW_3X (erratum E5).
- **function `selection`** [L172-175]: `def selection(finalists, s3) -> dict` - §5.6 item 4: first ordinary qualifier in the frozen order; next two are the fallbacks.
- **function `absence_shown`** [L178-180]: `def absence_shown(records) -> bool` - Choice 34: every evaluated, not-INELIGIBLE world is EXCLUDED on its latest look.
- **function `_max_d4`** [L183-189]: `def _max_d4(recs) -> dict`
- **function `outcome`** [L192-242]: `def outcome(state) -> dict` - §7.1 precedence (RC-1, RC-7, R-HWS-1; choice 35; erratum E6).
- **function `_selected_fill`** [L245-256]: `def _selected_fill(rec, s3e, fl) -> dict`
- **class `_Fill(dict)`** [L259-261]
- **method `_Fill.__missing__`** [L260-261]: `def __missing__(self, key)`
- **function `licence`** [L264-270]: `def licence(outcome, fill) -> str`
- **function `rate`** [L276-283]: `def rate(stage, w) -> int`
- **function `forecast`** [L286-291]: `def forecast(stage, worklist) -> int`
- **function `pause_check`** [L294-304]: `def pause_check(stage_cpu, stage_fc, cum_cpu, cum_fc) -> dict`

