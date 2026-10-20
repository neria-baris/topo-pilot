# `tests/oracle_profile/test_oracle_profile_kernels.py`

- Source: [tests/oracle_profile/test_oracle_profile_kernels.py](../../../../../tests/oracle_profile/test_oracle_profile_kernels.py)
- Kind: python
- Lines: 263

## Module docstring

> Independent tests of x4_oracle_profile helper kernels (job 0014; API.md section 4 items 7-11):
> validate_process, circle_features, residual_rows, profile_point, bootstrap_profile and
> percentile_interval. Written from ``tools/x4_oracle_profile/API.md`` only: production is imported,
> never read. Randomness only through explicitly seeded np.random.Generator(np.random.PCG64(seed)).

## Imports

### Internal (repo files)

- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 23, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 7)
- `math` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `_path` -> `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BASE`
- `E3`
- `E4`
- `KEYS`
- `N_ROWS`
- `PI3`
- `PI4`
- `REJECT`
- `REPO_ROOT`
- `T3`
- `T4`

## Classes and functions

- **function `replaced`** [L38-41]: `def replaced(arr, index, value)`
- **function `seeded`** [L44-45]: `def seeded(seed: int) -> np.random.Generator`
- **test `test_validate_process_accepts_valid_models`** [L49-55]: `def test_validate_process_accepts_valid_models()`
- **test `test_validate_process_reports_known_maxima`** [L58-71]: `def test_validate_process_reports_known_maxima()` - Dyadic perturbations: row error 2^-10 in T, 2^-11 in E, pi sum error 2^-9.
- **test `test_validate_process_rejects`** [L93-96]: `def test_validate_process_rejects(name)` decorators: @pytest.mark.parametrize('name', sorted(REJECT))
- **test `test_circle_features_known_answers`** [L100-109]: `def test_circle_features_known_answers()`
- **test `test_circle_features_all_twelve_positions`** [L112-117]: `def test_circle_features_all_twelve_positions()`
- **test `test_circle_features_rejects_bad_coordinates`** [L121-124]: `def test_circle_features_rejects_bad_coordinates(value)` decorators: @pytest.mark.parametrize('value', [1.5, 12, -1, np.nan, np.inf], ids=str)
- **function `hand_means`** [L128-133]: `def hand_means()`
- **test `test_residual_rows_and_profile_point_known_answer`** [L136-153]: `def test_residual_rows_and_profile_point_known_answer()` - r_1 = ((3, 4), (0, 1)) -> norm (5, 1), sq (25, 1); r_4 = ((0, 2), (0, 0)) -> (2, 0), (4, 0).
- **test `test_residual_rows_custom_full_and_errors`** [L156-167]: `def test_residual_rows_custom_full_and_errors()`
- **test `test_jensen_bias_at_most_root_variance`** [L170-180]: `def test_jensen_bias_at_most_root_variance()`
- **function `boot_inputs`** [L188-192]: `def boot_inputs()` - norm differs by K (norm_4 = 2 norm_1 + 1); sq_1 = norm_1 so B and V share idx visibly.
- **function `manual_bootstrap`** [L195-204]: `def manual_bootstrap(norm, sq, Ks, rng, draws)` - Re-implementation of the documented order: one rng.integers(0, n, size=n) call per draw.
- **test `test_bootstrap_reproduces_documented_sampling_order`** [L208-227]: `def test_bootstrap_reproduces_documented_sampling_order(Ks)` decorators: @pytest.mark.parametrize('Ks', [[1, 4, 32], [32, 1, 4]])
- **test `test_bootstrap_error_paths`** [L230-247]: `def test_bootstrap_error_paths()`
- **test `test_percentile_interval_equals_inverted_cdf_quantile`** [L251-256]: `def test_percentile_interval_equals_inverted_cdf_quantile()`
- **test `test_percentile_interval_hand_case`** [L259-263]: `def test_percentile_interval_hand_case()` - n = 4: inverted CDF picks x_(ceil(n p)): p = .25 -> 1, .3 -> 2, .5 -> 2, 1 -> 4.

