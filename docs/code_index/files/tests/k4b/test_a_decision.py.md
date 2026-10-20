# `tests/k4b/test_a_decision.py`

- Source: [tests/k4b/test_a_decision.py](../../../../../tests/k4b/test_a_decision.py)
- Kind: python
- Lines: 289

## Module docstring

> K4b author A, TEST_PLAN A6, A10, A11 (protocol §5.4, §5.5, §7.1, §8.1-§8.3).

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../../tools/c1prime/c1_bounds.py.md) (line 30, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 31, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 32, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 33, via sys.path edit)

### External (third-party)

- `pytest` (lines 21)

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 16)
- `itertools` (lines 17)
- `math` (lines 13, 18)
- `pathlib` (lines 19)
- `random` (lines 14)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 28: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `ALPHA`
- `CAP`
- `DELTA`
- `FLOOR`
- `HALF_W`
- `M`
- `MODELS`
- `MU`
- `REPO`
- `TINY`
- `U53`
- `ZETA`

## Classes and functions

- **function `F`** [L45-46]: `def F(x)`
- **function `gamma`** [L49-50]: `def gamma(m)`
- **function `ref_B_constant`** [L53-57]: `def ref_B_constant(max_b, max_abs, n)`
- **function `status`** [L60-61]: `def status(L, U, Fm, Fp)`
- **function `ref_status`** [L64-74]: `def ref_status(L, U, Fm, Fp)`
- **test `test_threshold_constants`** [L79-83]: `def test_threshold_constants()`
- **test `test_b_num_matches_B_constant_and_closed_form`** [L88-94]: `def test_b_num_matches_B_constant_and_closed_form(n, d)` decorators: @pytest.mark.parametrize('n,d', [(1, 0), (2, 1), (3, 2), (3072, 12), (4096, 12), (4097, 13), (6144, 13), (8192, 13), (8193, 14), (12288, 14)])
- **test `test_b_num_is_monotone`** [L97-102]: `def test_b_num_is_monotone()`
- **test `test_margin_floor_and_transport`** [L105-111]: `def test_margin_floor_and_transport()`
- **test `test_support_boundary_is_strict`** [L116-122]: `def test_support_boundary_is_strict()`
- **test `test_exclude_upper_boundary_is_strict`** [L125-130]: `def test_exclude_upper_boundary_is_strict()`
- **test `test_exclude_lower_boundary_is_strict`** [L133-138]: `def test_exclude_lower_boundary_is_strict()`
- **test `test_plain_support_exclude_unresolved`** [L141-147]: `def test_plain_support_exclude_unresolved()`
- **test `test_negative_alignment_label`** [L150-159]: `def test_negative_alignment_label()`
- **test `test_status_table_and_exclusivity`** [L162-176]: `def test_status_table_and_exclusivity()`
- **test `test_overall_table`** [L179-193]: `def test_overall_table()`
- **function `_events`** [L203-213]: `def _events(law)` - law: {offset k: probability}; estimate = MU + k*DELTA, L = est - HALF_W, U = est + HALF_W.
- **test `test_truth_is_neither_support_nor_exclude`** [L216-217]: `def test_truth_is_neither_support_nor_exclude()`
- **test `test_rc1_binomial_tails_add`** [L220-233]: `def test_rc1_binomial_tails_add()`
- **test `test_rc1_three_point_law_attains_two_alpha`** [L236-244]: `def test_rc1_three_point_law_attains_two_alpha()`
- **test `test_rc1_family_arithmetic`** [L247-249]: `def test_rc1_family_arithmetic()`
- **test `test_F_plan_exact`** [L255-260]: `def test_F_plan_exact(Z)` decorators: @pytest.mark.parametrize('Z', [Fr(0), Fr(212, 10 ** 14), Fr(1, 10 ** 6)])
- **test `test_F_plan_desk_values`** [L263-266]: `def test_F_plan_desk_values()`
- **test `test_F_test_never_exceeds_F_plan_under_cap_and_p2`** [L269-278]: `def test_F_test_never_exceeds_F_plan_under_cap_and_p2()`
- **test `test_F_plan_conditions_are_needed`** [L281-289]: `def test_F_plan_conditions_are_needed()`

