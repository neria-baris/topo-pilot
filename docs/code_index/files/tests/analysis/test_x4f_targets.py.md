# `tests/analysis/test_x4f_targets.py`

- Source: [tests/analysis/test_x4f_targets.py](../../../../../tests/analysis/test_x4f_targets.py)
- Kind: python
- Lines: 154

## Module docstring

> Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import PCMap, circle_expectation, leading_components, pc_scores` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 9, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 6)
- `pytest` (lines 7)

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **function `_code`** [L15-18]: `def _code(fn)`
- **test `test_delta_belief_gives_unit_vector_at_state_angle`** [L24-31]: `def test_delta_belief_gives_unit_vector_at_state_angle(s)` decorators: @pytest.mark.parametrize('s', range(12))
- **test `test_uniform_belief_over_full_period_is_zero`** [L34-38]: `def test_uniform_belief_over_full_period_is_zero()`
- **test `test_hand_values_mixed_beliefs_and_non_integer_positions`** [L41-48]: `def test_hand_values_mixed_beliefs_and_non_integer_positions()`
- **test `test_linear_in_belief_and_bounded`** [L51-59]: `def test_linear_in_belief_and_bounded()`
- **test `test_circle_expectation_errors`** [L62-67]: `def test_circle_expectation_errors()`
- **function `_flip_to_convention`** [L72-78]: `def _flip_to_convention(V)`
- **function `_anisotropic`** [L81-84]: `def _anisotropic(n=4000, seed=0)`
- **test `test_leading_components_hand_case`** [L87-92]: `def test_leading_components_hand_case()`
- **test `test_leading_components_match_eigh_of_population_covariance`** [L95-107]: `def test_leading_components_match_eigh_of_population_covariance()`
- **test `test_eigen_order_is_descending`** [L110-114]: `def test_eigen_order_is_descending()`
- **test `test_sign_convention_largest_abs_entry_positive_and_stable_under_negation`** [L117-124]: `def test_sign_convention_largest_abs_entry_positive_and_stable_under_negation()`
- **test `test_leading_components_errors`** [L127-131]: `def test_leading_components_errors()`
- **test `test_pc_scores_definition_on_new_rows`** [L136-142]: `def test_pc_scores_definition_on_new_rows()`
- **test `test_pc_scores_hand_case_and_decorrelation`** [L145-154]: `def test_pc_scores_hand_case_and_decorrelation()`

