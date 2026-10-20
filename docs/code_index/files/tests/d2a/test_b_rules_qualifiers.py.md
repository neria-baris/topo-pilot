# `tests/d2a/test_b_rules_qualifiers.py`

- Source: [tests/d2a/test_b_rules_qualifiers.py](../../../../../tests/d2a/test_b_rules_qualifiers.py)
- Kind: python
- Lines: 231

## Module docstring

> Independent tests (author B, job 0028): T-RULES qualifiers of ``d2a_decide.decide(flags)``.

## Imports

### Internal (repo files)

- `import d2a_decide` -> [tools/d2a/d2a_decide.py](../../tools/d2a/d2a_decide.py.md) (line 23, via sys.path edit)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 10)
- `pathlib` (lines 14)
- `re` (lines 12)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / _sub)` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BOTH_ARMS`
- `CASES`
- `FIXED`
- `LENGTHS`
- `REPO`

## Classes and functions

- **function `base`** [L30-41]: `def base()`
- **function `multistep`** [L44-47]: `def multistep()`
- **function `horizon_dependent`** [L50-54]: `def horizon_dependent()`
- **function `enhanced`** [L57-61]: `def enhanced()`
- **function `carried`** [L64-67]: `def carried()`
- **function `predictive`** [L70-73]: `def predictive()`
- **function `not_recovered`** [L76-79]: `def not_recovered()`
- **function `run`** [L88-90]: `def run(flags)`
- **function `behaviour_cells`** [L93-99]: `def behaviour_cells(quals)`
- **test `test_builders_hit_their_outcomes`** [L102-104]: `def test_builders_hit_their_outcomes()`
- **test `test_quiet_table_carries_only_the_length_qualifier`** [L108-111]: `def test_quiet_table_carries_only_the_length_qualifier(make, outcome)` decorators: @pytest.mark.parametrize('make, outcome', CASES)
- **test `test_length_qualifier_on_outcomes_4_to_10`** [L116-121]: `def test_length_qualifier_on_outcomes_4_to_10(make, outcome, c_len)` decorators: @pytest.mark.parametrize('c_len', LENGTHS) @pytest.mark.parametrize('make, outcome', CASES)
- **test `test_length_qualifier_on_rule4_learning_unresolved`** [L124-129]: `def test_length_qualifier_on_rule4_learning_unresolved()`
- **test `test_precision_limited_on_h1_or_h2_failure_when_both_arms_enter`** [L141-147]: `def test_precision_limited_on_h1_or_h2_failure_when_both_arms_enter(make, outcome, arm, slot, value)` decorators: @pytest.mark.parametrize('arm, slot, value', [('H1', 0, F), ('H1', 3, None), ('H2', 1, F), ('H2', 2, None)]) @pytest.mark.parametrize('make, outcome', BOTH_ARMS)
- **test `test_precision_limited_on_rule8_counts_only_h2_models`** [L153-158]: `def test_precision_limited_on_rule8_counts_only_h2_models(arm, slot, value, present)` decorators: @pytest.mark.parametrize('arm, slot, value, present', [('H1', 0, F, False), ('H1', 3, None, False), ('H2', 1, F, True), ('H2', 2, None, True)])
- **test `test_precision_limited_turns_outcome9_into_inconclusive`** [L161-165]: `def test_precision_limited_turns_outcome9_into_inconclusive()`
- **test `test_world_conditional_ceiling_threshold`** [L172-175]: `def test_world_conditional_ceiling_threshold(make, ceiling, present)` decorators: @pytest.mark.parametrize('ceiling, present', [(0.3, True), (0.95, True), (0.3 - 1e-09, False), (0.0, False), (None, False)]) @pytest.mark.parametrize('make', [enhanced, base, multistep])
- **test `test_caveat_reread`** [L185-188]: `def test_caveat_reread(low_h1, ar_h1, present)` decorators: @pytest.mark.parametrize('low_h1, ar_h1, present', [([T, T, T, F], [T, T, T, F], True), ([T, T, T, F], [F, T, T, T], True), ([T, T, T, T], [T, T, F, None], False), ([T, T, F, None], [T, T, T, T], False), ([F] * 4, [T] * 4, False)])
- **test `test_caveat_reread_on_not_recovered`** [L191-195]: `def test_caveat_reread_on_not_recovered()`
- **test `test_behaviour_cells_exactly_the_true_ones`** [L198-205]: `def test_behaviour_cells_exactly_the_true_ones()`
- **test `test_all_qualifiers_together`** [L208-218]: `def test_all_qualifiers_together()`
- **test `test_no_qualifiers_for_outcomes_1_to_3`** [L225-231]: `def test_no_qualifiers_for_outcomes_1_to_3(change)` decorators: @pytest.mark.parametrize('change', [{'s_fail': 'S2'}, {'s_fail': 'S0'}, {'stage1': 'NOT_LEARNED'}, {'stage1': 'LEARNING_UNRESOLVED'}, {'validity_ok': False}])

