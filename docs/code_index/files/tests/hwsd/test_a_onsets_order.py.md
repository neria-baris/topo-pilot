# `tests/hwsd/test_a_onsets_order.py`

- Source: [tests/hwsd/test_a_onsets_order.py](../../../../../tests/hwsd/test_a_onsets_order.py)
- Kind: python
- Lines: 273

## Module docstring

> Author A (job 0197): §5.1 notation, §5.2 onsets, §5.3 ORDER (TEST_PLAN A test_a_onsets_order).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 21, via sys.path edit)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](../../tools/hwsd/hwsd_statements.py.md) (line 22, via sys.path edit)
- `import test_a_hwsd_ref` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 24, via same directory)
- `from test_a_hwsd_ref import CU, EXC, NOC, SC, SU, SUP, UC, UNR, UNV, row, seq` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 25, via same directory)

### External (third-party)

- `pytest` (lines 23)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 12)
- `math` (lines 9)
- `pathlib` (lines 13)
- `random` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `CHART_CASES`
- `HERE`
- `LEARN_CASES`
- `M`
- `REPO`

## Classes and functions

- **function `k`** [L30-32]: `def k(o)`
- **function `cat`** [L35-37]: `def cat(rows, anchor, A=None)`
- **test `test_est_ok_and_sigma_by_status`** [L41-50]: `def test_est_ok_and_sigma_by_status()`
- **test `test_sigma_numerical_label_and_constants`** [L53-56]: `def test_sigma_numerical_label_and_constants()`
- **test `test_fr_rule`** [L59-61]: `def test_fr_rule()`
- **test `test_above_below_strict_equality`** [L64-75]: `def test_above_below_strict_equality()`
- **test `test_above_s_unvalidated_vs_ok_and_below_needs_ok`** [L78-83]: `def test_above_s_unvalidated_vs_ok_and_below_needs_ok()`
- **test `test_above_s_uses_F_minus_and_below_uses_F_plus`** [L86-90]: `def test_above_s_uses_F_minus_and_below_uses_F_plus()`
- **test `test_onsets_basic_and_undefined`** [L94-99]: `def test_onsets_basic_and_undefined()`
- **test `test_unvalidated_is_never_a_chart_onset`** [L102-105]: `def test_unvalidated_is_never_a_chart_onset()`
- **test `test_uncertified_valid_counts_for_k_C`** [L108-112]: `def test_uncertified_valid_counts_for_k_C()`
- **test `test_chart_lost_after_k_C_keeps_k_C`** [L115-120]: `def test_chart_lost_after_k_C_keeps_k_C()`
- **test `test_k_C_star_none_when_final_not_valid_and_k_C_plus_from_init`** [L123-127]: `def test_k_C_star_none_when_final_not_valid_and_k_C_plus_from_init()`
- **test `test_k_L_and_k_P_strict`** [L130-134]: `def test_k_L_and_k_P_strict()`
- **test `test_n_pre_counts_est_before_k_C_only`** [L138-141]: `def test_n_pre_counts_est_before_k_C_only()`
- **test `test_n_pre_zero_and_pre_chart_max_none`** [L144-146]: `def test_n_pre_zero_and_pre_chart_max_none()`
- **test `test_n_pre_without_chart_counts_every_est`** [L149-152]: `def test_n_pre_without_chart_counts_every_est()`
- **test `test_order_chart_categories`** [L176-178]: `def test_order_chart_categories(expected, rows)` decorators: @pytest.mark.parametrize('expected,rows', CHART_CASES)
- **test `test_order_unresolved_numerical_read_as_unresolved`** [L181-186]: `def test_order_unresolved_numerical_read_as_unresolved()`
- **test `test_order_learning_categories`** [L205-207]: `def test_order_learning_categories(expected, rows)` decorators: @pytest.mark.parametrize('expected,rows', LEARN_CASES)
- **test `test_learning_anchor_at_step0_is_not_chart_at_init`** [L210-213]: `def test_learning_anchor_at_step0_is_not_chart_at_init()`
- **test `test_order_returns_anchor_and_A`** [L216-222]: `def test_order_returns_anchor_and_A()`
- **test `test_order_explicit_A_for_k_C_plus`** [L225-231]: `def test_order_explicit_A_for_k_C_plus()`
- **test `test_onset_order_line`** [L234-243]: `def test_onset_order_line()`
- **test `test_random_sequences_match_reference`** [L247-266]: `def test_random_sequences_match_reference()`
- **test `test_categories_are_the_contract_list`** [L269-273]: `def test_categories_are_the_contract_list()`

