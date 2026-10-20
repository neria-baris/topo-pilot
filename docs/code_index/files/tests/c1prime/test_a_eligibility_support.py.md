# `tests/c1prime/test_a_eligibility_support.py`

- Source: [tests/c1prime/test_a_eligibility_support.py](../../../../../tests/c1prime/test_a_eligibility_support.py)
- Kind: python
- Lines: 198

## Module docstring

> Independent tests, author A (job 0026): eligibility, kappa_nu and the covariates (TEST_PLAN
> A-4; protocol sections 3.3 and 4), and the support gate M3 (TEST_PLAN A-5; protocol section 9).

## Imports

### Internal (repo files)

- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 25, via sys.path edit)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](../../tools/c1prime/c1_gates.py.md) (line 26, via sys.path edit)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 27, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 28, via sys.path edit)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 29, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 11)
- `pathlib` (lines 12)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 23: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `GRID`
- `REPO`

## Classes and functions

- **test `test_s_max_inverted_cdf_rank`** [L37-43]: `def test_s_max_inverted_cdf_rank(n, expected)` decorators: @pytest.mark.parametrize('n, expected', [(1000, 998.0), (8192, 8183.0), (10, 9.0)]) - Ranks: 1000 * 0.999 = 999 exactly in float -> 999th smallest (value 998);
- **test `test_s_max_with_ties_at_the_boundary_returns_an_input_value`** [L46-51]: `def test_s_max_with_ties_at_the_boundary_returns_an_input_value()` - n = 1000: the 999th smallest value (sorted index 998) is returned, never interpolated.
- **test `test_eligibility_rule_boundaries`** [L54-64]: `def test_eligibility_rule_boundaries()`
- **test `test_eligible_fraction_and_the_h4_threshold`** [L67-73]: `def test_eligible_fraction_and_the_h4_threshold()`
- **test `test_kappa_nu_population_covariance_and_eligible_mean`** [L76-89]: `def test_kappa_nu_population_covariance_and_eligible_mean()`
- **test `test_leakage_trigger_at_001`** [L92-95]: `def test_leakage_trigger_at_001()`
- **test `test_y_marginal_m32_and_nuisance`** [L98-114]: `def test_y_marginal_m32_and_nuisance()`
- **test `test_q99_inverted_cdf_rank`** [L120-123]: `def test_q99_inverted_cdf_rank(n, expected)` decorators: @pytest.mark.parametrize('n, expected', [(100, 98.0), (8192, 8110.0)]) - 100 * 0.99 = 99 exactly in float -> 99th smallest (98); ceil(8110.08) = 8111 -> 8110.
- **test `test_frac_beyond_is_strict`** [L126-127]: `def test_frac_beyond_is_strict()`
- **function `whitened_fixture`** [L130-139]: `def whitened_fixture(d=128, n=3000, seed=5)`
- **test `test_mahalanobis_with_source_or_donor_nuisance`** [L142-155]: `def test_mahalanobis_with_source_or_donor_nuisance()`
- **function `m3`** [L158-163]: `def m3(F_T, F_C, F_D=0.0, F_S=0.0, sup=(0.995, 0.985, 0.985, 0.985))`
- **test `test_m3_primary_ceiling`** [L170-174]: `def test_m3_primary_ceiling()`
- **test `test_m3_family_ceiling`** [L177-180]: `def test_m3_family_ceiling()`
- **test `test_m3_matching_within_002`** [L183-189]: `def test_m3_matching_within_002()`
- **test `test_m3_support_fractions`** [L193-198]: `def test_m3_support_fractions(which, edge)` decorators: @pytest.mark.parametrize('which, edge', [(0, 0.99), (1, 0.98), (2, 0.98), (3, 0.98)])

