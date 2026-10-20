# `tests/c1prime/test_a_oracle.py`

- Source: [tests/c1prime/test_a_oracle.py](../../../../../tests/c1prime/test_a_oracle.py)
- Kind: python
- Lines: 317

## Module docstring

> Independent tests, author A (job 0026): donors, symmetry, the closed-form donor posterior and
> the v4 comparison rules (TEST_PLAN A-3; protocol sections 3.1, 3.2, 3.4, 15.3.16 item 15).

## Imports

### Internal (repo files)

- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 30, via sys.path edit)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 31, via sys.path edit)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 11)
- `decimal` (lines 13, 15)
- `fractions` (lines 16)
- `pathlib` (lines 17)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 28: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `A_TOL`
- `COORDS`
- `DELTA`
- `N`
- `REPO`
- `ULP1`

## Classes and functions

- **function `state`** [L41-42]: `def state(x, y)`
- **function `tau_ref`** [L45-47]: `def tau_ref(j, k)`
- **function `make_T`** [L50-59]: `def make_T()`
- **function `make_E`** [L62-78]: `def make_E()`
- **function `rho_ref`** [L84-85]: `def rho_ref(k)`
- **function `histories`** [L88-89]: `def histories(rows, seed)`
- **function `exact_r_E`** [L92-100]: `def exact_r_E(Em)`
- **test `test_tau_maps_symbol_columns_and_inverts`** [L103-109]: `def test_tau_maps_symbol_columns_and_inverts()`
- **test `test_donors_shift_w1_to_w31_and_keep_w32`** [L112-122]: `def test_donors_shift_w1_to_w31_and_keep_w32()`
- **test `test_rho_index_from_coordinates`** [L125-129]: `def test_rho_index_from_coordinates()`
- **test `test_fixture_is_exactly_symmetric`** [L132-137]: `def test_fixture_is_exactly_symmetric()`
- **test `test_symmetry_report_on_the_exact_fixture`** [L140-143]: `def test_symmetry_report_on_the_exact_fixture()`
- **test `test_symmetry_report_measures_r_E_exactly_for_a_perturbed_emission`** [L146-157]: `def test_symmetry_report_measures_r_E_exactly_for_a_perturbed_emission()`
- **test `test_exact_invariance_fails_on_one_ulp`** [L161-167]: `def test_exact_invariance_fails_on_one_ulp(which)` decorators: @pytest.mark.parametrize('which', ['T', 'pi'])
- **function `my_closed_form`** [L170-174]: `def my_closed_form(b31, w32, k)`
- **test `test_closed_form_index_convention_on_a_nonsymmetric_posterior`** [L177-188]: `def test_closed_form_index_convention_on_a_nonsymmetric_posterior()`
- **test `test_closed_form_agrees_with_the_direct_donor_filter_within_t_plus_t2`** [L191-204]: `def test_closed_form_agrees_with_the_direct_donor_filter_within_t_plus_t2()`
- **test `test_closed_form_tolerance_values_and_the_three_halves_switch`** [L207-218]: `def test_closed_form_tolerance_values_and_the_three_halves_switch()`
- **test `test_rel_agree_at_the_relative_boundary`** [L225-231]: `def test_rel_agree_at_the_relative_boundary(k, ok)` decorators: @pytest.mark.parametrize('k, ok', [(9007, True), (9008, False)]) - 9007 * 2^-52 < 2e-12 < 9008 * 2^-52 (exact rationals).
- **test `test_named_canonical_four_e_minus_12_rule_boundary`** [L234-241]: `def test_named_canonical_four_e_minus_12_rule_boundary()`
- **function `dec_minus`** [L244-246]: `def dec_minus(x, text)`
- **test `test_interval_rule_three_way_at_its_boundaries`** [L249-267]: `def test_interval_rule_three_way_at_its_boundaries()`
- **test `test_h3_compare_branches_and_zero_posterior_entries`** [L270-281]: `def test_h3_compare_branches_and_zero_posterior_entries()`
- **function `decimal_closed_form`** [L284-293]: `def decimal_closed_form(b31_dec, w32, k)`
- **test `test_enclosure_branch_corrupted_float_closed_form_fails`** [L296-317]: `def test_enclosure_branch_corrupted_float_closed_form_fails()` - Section 3.2 S1 fixture: corrupted float64 closed-form values on the enclosure branch,

