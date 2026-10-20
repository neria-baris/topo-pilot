# `tests/d2a/test_b_rules_decide.py`

- Source: [tests/d2a/test_b_rules_decide.py](../../../../../tests/d2a/test_b_rules_decide.py)
- Kind: python
- Lines: 319

## Module docstring

> Independent tests (author B, job 0028): T-RULES for ``d2a_decide.decide(flags)``.

## Imports

### Internal (repo files)

- `import d2a_decide` -> [tools/d2a/d2a_decide.py](../../tools/d2a/d2a_decide.py.md) (line 23, via sys.path edit)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 9)
- `copy` (lines 11)
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

- `LENGTHS`
- `REPO`

## Classes and functions

- **function `base`** [L30-42]: `def base()` - Every arm learned, nothing carried, nothing low: falls to rule 10 (INCONCLUSIVE).
- **function `loud`** [L45-52]: `def loud(flags)` - Make every qualifier source true, so an empty qualifier list is a real check.
- **function `horizon_dependent`** [L55-59]: `def horizon_dependent()`
- **function `carried`** [L62-65]: `def carried()`
- **function `predictive`** [L68-71]: `def predictive()`
- **function `not_recovered`** [L74-78]: `def not_recovered()`
- **function `run`** [L81-84]: `def run(flags)`
- **function `lengths`** [L87-88]: `def lengths(quals)`
- **test `test_rule1_stop_failures`** [L97-100]: `def test_rule1_stop_failures(s_fail, outcome)` decorators: @pytest.mark.parametrize('s_fail, outcome', [('S0', 'INVALID'), ('S1', 'INVALID'), ('S2', 'CONSTRUCTION_FAIL'), ('S3', 'FEASIBILITY_NO_GO')])
- **test `test_rule2_stage1_stops_precede_validity_and_have_no_qualifiers`** [L104-107]: `def test_rule2_stage1_stops_precede_validity_and_have_no_qualifiers(stage1)` decorators: @pytest.mark.parametrize('stage1', ['NOT_LEARNED', 'LEARNING_UNRESOLVED'])
- **test `test_rule3_pipeline_invalid_precedes_rule4_and_has_no_qualifiers`** [L110-114]: `def test_rule3_pipeline_invalid_precedes_rule4_and_has_no_qualifiers()`
- **test `test_rule4_branches`** [L130-135]: `def test_rule4_branches(h1, h2, h3, outcome)` decorators: @pytest.mark.parametrize('h1, h2, h3, outcome', [([X] * 4, [P] * 4, [P] * 4, 'MULTISTEP_ENABLES_LEARNING'), ([P, P, X, X], [P, P, P, X], [X] * 4, 'MULTISTEP_ENABLES_LEARNING'), ([P, P, None, None], [P, P, P, None], [P] * 4, 'MULTISTEP_ENABLES_LEARNING'), ([X] * 4, [X] * 4, [X] * 4, 'LEARNING_UNRESOLVED'), ([X] * 4, [P, P, X, X], [P] * 4, 'LEARNING_UNRESOLVED'), ([P, P, U, X], [P] * 4, [P] * 4, 'LEARNING_UNRESOLVED'), ([P, U, U, None], [X] * 4, [P] * 4, 'LEARNING_UNRESOLVED'), ([X] * 4, [P, P, U, None], [P] * 4, 'LEARNING_UNRESOLVED'), ([P, X, X, X], [U, U, U, X], [P] * 4, 'LEARNING_UNRESOLVED')])
- **test `test_rule4_l1_true_continues`** [L142-148]: `def test_rule4_l1_true_continues(h1, h2)` decorators: @pytest.mark.parametrize('h1, h2', [([P] * 4, [P] * 4), ([P, P, P, None], [X] * 4), ([P, P, P, X], [U, U, U, U]), ([P, P, P, U], [P, X, None, None])])
- **test `test_rule4_precedes_rule5`** [L151-154]: `def test_rule4_precedes_rule5()`
- **test `test_rule5_horizon_dependent`** [L159-160]: `def test_rule5_horizon_dependent()`
- **test `test_rule5_needs_the_same_three_seeds_for_all_conditions`** [L163-168]: `def test_rule5_needs_the_same_three_seeds_for_all_conditions()`
- **test `test_rule5_two_joint_seeds_is_not_enough`** [L171-177]: `def test_rule5_two_joint_seeds_is_not_enough()`
- **test `test_rule5_nonpositive_or_missing_delta_fails_that_seed`** [L180-186]: `def test_rule5_nonpositive_or_missing_delta_fails_that_seed()`
- **test `test_rule5_missing_h2_model_counts_as_failing`** [L189-195]: `def test_rule5_missing_h2_model_counts_as_failing()`
- **test `test_rule6_horizon_enhanced`** [L198-202]: `def test_rule6_horizon_enhanced()`
- **test `test_supported_c_hor_without_carries_is_inconclusive`** [L205-209]: `def test_supported_c_hor_without_carries_is_inconclusive()`
- **test `test_rule7_carried_without_horizon_effect`** [L214-215]: `def test_rule7_carried_without_horizon_effect()`
- **test `test_rule7_needs_both_arms`** [L219-222]: `def test_rule7_needs_both_arms(arm)` decorators: @pytest.mark.parametrize('arm', ['H1', 'H2'])
- **test `test_unresolved_c_hor_never_fires_rule7`** [L225-228]: `def test_unresolved_c_hor_never_fires_rule7()`
- **test `test_unresolved_c_hor_can_still_match_a_later_rule`** [L231-237]: `def test_unresolved_c_hor_can_still_match_a_later_rule()`
- **test `test_rule8_predictive_without_linear_posterior`** [L242-243]: `def test_rule8_predictive_without_linear_posterior()`
- **test `test_rule8_precedes_rule9`** [L246-249]: `def test_rule8_precedes_rule9()`
- **test `test_rule8_needs_three_seeds_of_each`** [L255-261]: `def test_rule8_needs_three_seeds_of_each(key, value)` decorators: @pytest.mark.parametrize('key, value', [('beta2_direct_H2', [T, T, F, None]), ('low_inc', [T, T, None, F])])
- **test `test_rule9_not_recovered`** [L264-265]: `def test_rule9_not_recovered()`
- **test `test_rule9_precision_failure_gives_inconclusive_precision_limited`** [L271-276]: `def test_rule9_precision_failure_gives_inconclusive_precision_limited(arm, slot, value)` decorators: @pytest.mark.parametrize('arm, slot, value', [('H1', 0, F), ('H1', 3, None), ('H2', 2, F), ('H2', 1, None)])
- **test `test_rule9_needs_valid_controls`** [L279-284]: `def test_rule9_needs_valid_controls()`
- **test `test_rule9_needs_low_increment_in_both_arms`** [L288-291]: `def test_rule9_needs_low_increment_in_both_arms(arm)` decorators: @pytest.mark.parametrize('arm', ['H1', 'H2'])
- **test `test_split_seeds_are_inconclusive`** [L294-299]: `def test_split_seeds_are_inconclusive()`
- **test `test_first_match_ladder`** [L302-319]: `def test_first_match_ladder()` - All of rules 5-9 hold; removing one condition at a time walks down the order.

