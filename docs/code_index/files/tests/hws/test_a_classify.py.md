# `tests/hws/test_a_classify.py`

- Source: [tests/hws/test_a_classify.py](../../../../../tests/hws/test_a_classify.py)
- Kind: python
- Lines: 387

## Module docstring

> Author A (job 0119): floors, criteria, eligibility, classes, ranking, annotations, finalists,
> the X1 trigger and the S2 worklist (TEST_PLAN §2 `test_a_classify.py`; protocol §5.1-§5.6, §6.2,
> §7.3; RC-1, RC-6, R-HWS-1). Records are planted fixtures; their class and failed list come from
> an independent classifier written here (§5.4), never from the module under test.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 21, via sys.path edit)
- `import hws_select` -> [tools/hws/hws_select.py](../../tools/hws/hws_select.py.md) (line 22, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `fractions` (lines 9)
- `json` (lines 7)
- `pathlib` (lines 10)
- `statistics` (lines 11)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `HWS_DIR` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `CASES`
- `CONTRACT`
- `CRIT`
- `F`
- `FLOORS`
- `HWS_DIR`
- `LEV`
- `P_IDX`
- `P_LEV`
- `P_MID`
- `RANK_PAIRS`
- `REPO`
- `S_IDX`
- `S_LEV`
- `S_MID`
- `X1_CASES`
- `Z1`
- `ZW`

## Classes and functions

- **class `Records(list)`** [L39-65] - API-AMBIGUITY: `records` may be read as a list of records or as {key: record}; this
- **method `Records.__init__`** [L43-45]: `def __init__(self, recs)`
- **method `Records.keys`** [L47-48]: `def keys(self)`
- **method `Records.values`** [L50-51]: `def values(self)`
- **method `Records.items`** [L53-54]: `def items(self)`
- **method `Records.get`** [L56-57]: `def get(self, k, default=None)`
- **method `Records.__getitem__`** [L59-62]: `def __getitem__(self, i)`
- **method `Records.__contains__`** [L64-65]: `def __contains__(self, k)`
- **function `key_of`** [L68-69]: `def key_of(W, q, s, p)`
- **function `tier_of`** [L72-73]: `def tier_of(W, q)`
- **function `changed_of`** [L76-77]: `def changed_of(W, q, s, p)`
- **function `dist_of`** [L80-81]: `def dist_of(W, q, s, p)`
- **function `bnd`** [L84-86]: `def bnd(mean, se=0.001)`
- **function `my_class`** [L89-98]: `def my_class(elig, b, fl=FLOORS)` - Protocol §5.4, written independently.
- **function `rec`** [L101-110]: `def rec(W, q, s, p, d4=0.05, gc=0.3, g4=0.05, g4a=0.05, elig='ELIGIBLE', over=None, se=0.001)`
- **function `my_rank`** [L113-116]: `def my_rank(r)`
- **test `test_floors_both_ways`** [L119-124]: `def test_floors_both_ways()`
- **test `test_criteria_equality_passes`** [L128-135]: `def test_criteria_equality_passes(which)` decorators: @pytest.mark.parametrize('which', ['L1', 'Uw', 'L3', 'Lw'])
- **test `test_eligibility_order_and_e6`** [L138-145]: `def test_eligibility_order_and_e6()`
- **test `test_classify_every_class`** [L163-169]: `def test_classify_every_class(name, kw, cls, failed)` decorators: @pytest.mark.parametrize('name, kw, cls, failed', CASES, ids=[c[0] for c in CASES])
- **test `test_classify_random_looks_match_the_protocol`** [L172-181]: `def test_classify_random_looks_match_the_protocol()`
- **test `test_classify_nan_bound_is_technical`** [L185-191]: `def test_classify_nan_bound_is_technical(q)` decorators: @pytest.mark.parametrize('q', ['D4', 'GC', 'G4', 'G4A'])
- **test `test_world_helpers`** [L194-206]: `def test_world_helpers()`
- **test `test_rank_key_every_tie_break_level`** [L222-225]: `def test_rank_key_every_tie_break_level(name, first, second)` decorators: @pytest.mark.parametrize('name, first, second', RANK_PAIRS, ids=[p[0] for p in RANK_PAIRS])
- **test `test_rank_key_tuple`** [L228-230]: `def test_rank_key_tuple()`
- **test `test_annotations_boundaries`** [L233-243]: `def test_annotations_boundaries()`
- **function `_tier0_tier1_records`** [L246-253]: `def _tier0_tier1_records()`
- **test `test_finalists_first_16_ordinary_never_marginal`** [L256-263]: `def test_finalists_first_16_ordinary_never_marginal()`
- **test `test_marginal_never_fills_an_ordinary_slot`** [L266-271]: `def test_marginal_never_fills_an_ordinary_slot()`
- **test `test_fallback_only_2x_set_membership`** [L274-287]: `def test_fallback_only_2x_set_membership()`
- **test `test_fallback_only_2x_set_cap_and_ties`** [L290-298]: `def test_fallback_only_2x_set_cap_and_ties()`
- **test `test_x1_trigger_condition`** [L310-320]: `def test_x1_trigger_condition(top, add_p, add_s)` decorators: @pytest.mark.parametrize('top, add_p, add_s', X1_CASES)
- **test `test_x1_trigger_ties_ineligible_and_empty`** [L323-334]: `def test_x1_trigger_ties_ineligible_and_empty()`
- **function `_keys`** [L337-338]: `def _keys(worlds)`
- **test `test_s2_worklist_edges_lowest_tier`** [L341-352]: `def test_s2_worklist_edges_lowest_tier()`
- **test `test_s2_worklist_uses_x1_levels_that_ran`** [L355-360]: `def test_s2_worklist_uses_x1_levels_that_ran()`
- **test `test_s2_worklist_cap_40_by_changed_distance_key`** [L363-377]: `def test_s2_worklist_cap_40_by_changed_distance_key()`
- **test `test_x1_worlds_counts_and_order`** [L380-387]: `def test_x1_worlds_counts_and_order()`

