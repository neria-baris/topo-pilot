# `tests/c1prime/test_a_oracle_named.py`

- Source: [tests/c1prime/test_a_oracle_named.py](../../../../../tests/c1prime/test_a_oracle_named.py)
- Kind: python
- Lines: 232

## Module docstring

> Independent tests, author A (job 0026): the operational oracle wrapper, G (C3), named /
> canonical joins, the cross-model G identity and the Decimal reference (TEST_PLAN A-3; protocol
> sections 3.3, 3.4 and 15.3.2 C3).

## Imports

### Internal (repo files)

- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 28, via sys.path edit)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 29, via package root)

### External (third-party)

- `numpy` (lines 18)

### Standard library

- `__future__` (lines 10)
- `decimal` (lines 12, 14)
- `fractions` (lines 15)
- `pathlib` (lines 16)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 26: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `COORDS`
- `N`
- `PERMS`
- `REPO`
- `U`

## Classes and functions

- **function `state`** [L38-39]: `def state(x, y)`
- **function `make_T`** [L42-51]: `def make_T()`
- **function `make_E`** [L54-66]: `def make_E()`
- **function `histories`** [L72-73]: `def histories(rows, seed)`
- **function `ordered_half_dot`** [L76-81]: `def ordered_half_dot(d, x)` - 0.5 * osum_v fl(d_v * x_v), left to right in column order (protocol C3/C4).
- **function `to_named`** [L84-87]: `def to_named(x, perm)`
- **function `gamma`** [L90-91]: `def gamma(n)`
- **function `donor_predictives`** [L94-98]: `def donor_predictives(rows=10, seed=4)`
- **test `test_run_oracle_is_bayesfilter_with_the_section_3_3_indices`** [L101-107]: `def test_run_oracle_is_bayesfilter_with_the_section_3_3_indices()`
- **test `test_G_hat_is_the_ordered_C3_kernel`** [L110-120]: `def test_G_hat_is_the_ordered_C3_kernel()`
- **test `test_G_named_uses_the_permuted_canonical_arrays`** [L123-134]: `def test_G_named_uses_the_permuted_canonical_arrays()`
- **test `test_cross_model_G_identity_within_1e_12`** [L137-143]: `def test_cross_model_G_identity_within_1e_12()`
- **test `test_named_canonical_column_permutations_round_trip`** [L146-152]: `def test_named_canonical_column_permutations_round_trip()`
- **test `test_named_space_filter_agrees_with_canonical_within_4e_12`** [L155-169]: `def test_named_space_filter_agrees_with_canonical_within_4e_12()` - Section 3.3: q_named[perm[j]] = q_canon[j], checked against direct named-space filtering
- **function `exact_forward`** [L172-181]: `def exact_forward(seq)` - Unnormalised exact forward pass with the stored float weights read as rationals.
- **function `exact_predictive`** [L184-187]: `def exact_predictive(b, TF, EF)`
- **function `rel_gap`** [L190-191]: `def rel_gap(dec_list, exact_list)`
- **function `exact_ln`** [L194-196]: `def exact_ln(value, digits=90)`
- **test `test_decimal_reference_against_exact_rationals`** [L199-214]: `def test_decimal_reference_against_exact_rationals()`
- **test `test_decimal_predictive_is_b_T_E`** [L217-225]: `def test_decimal_predictive_is_b_T_E()`
- **test `test_decimal_posterior60_matches_the_exact_posterior`** [L228-232]: `def test_decimal_posterior60_matches_the_exact_posterior()`

