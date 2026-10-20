# `tests/analysis/test_x4f_erasure.py`

- Source: [tests/analysis/test_x4f_erasure.py](../../../../../tests/analysis/test_x4f_erasure.py)
- Kind: python
- Lines: 316

## Module docstring

> Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import Eraser, Whitening, apply_map, displacements, eraser_from_basis, fit_oblique_eraser, whiten` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 7)
- `pytest` (lines 8)

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

- `CHECK_KEYS`

## Classes and functions

- **function `pop_cov`** [L27-30]: `def pop_cov(A, B=None)`
- **function `anisotropic_X`** [L33-38]: `def anisotropic_X(n=3000, d=6, seed=0, top=2.5)` - Correlated anisotropic features; covariance condition number about 10**(2*top).
- **function `rank_deficient_X`** [L41-43]: `def rank_deficient_X(n=600, d=8, r=5, seed=1)`
- **function `numerical_rank`** [L46-48]: `def numerical_rank(A, rel=1e-08)`
- **function `rng_for_seed`** [L51-52]: `def rng_for_seed(seed)`
- **function `ref_family_draw`** [L55-62]: `def ref_family_draw(X, wh, rank, rng)` - Spec section 2.2 draw: G in R^{k x rank}, Q from QR, E = W+ Q Q^T W, M = I - E.
- **test `test_whiten_anisotropic_correlated`** [L67-85]: `def test_whiten_anisotropic_correlated()`
- **test `test_whiten_rank_deficient_keeps_exact_rank`** [L88-96]: `def test_whiten_rank_deficient_keeps_exact_rank()`
- **function `_diag_cov_X`** [L99-102]: `def _diag_cov_X(variances)` - Four rows whose population covariance is exactly diag(variances).
- **test `test_whiten_floor_is_relative_to_lambda_max`** [L106-110]: `def test_whiten_floor_is_relative_to_lambda_max(floor, k)` decorators: @pytest.mark.parametrize('floor,k', [(0.1, 1), (0.0001, 2), (1e-08, 3), (None, 3)])
- **test `test_whiten_degenerate`** [L115-120]: `def test_whiten_degenerate(X)` decorators: @pytest.mark.parametrize('X', [np.zeros((20, 4)), np.tile([1.0, -2.0, 3.0, 0.5], (20, 1)), 1e-07 * np.random.default_rng(0).normal(size=(20, 4))])
- **test `test_apply_map_batch_convention_non_symmetric`** [L125-135]: `def test_apply_map_batch_convention_non_symmetric()`
- **test `test_eraser_from_basis_formula`** [L138-146]: `def test_eraser_from_basis_formula()`
- **test `test_displacements_known_answer`** [L149-152]: `def test_displacements_known_answer()`
- **function `_planted_2d`** [L157-163]: `def _planted_2d(seed=5, n=3000)`
- **test `test_oblique_eraser_planted_2d_target`** [L166-184]: `def test_oblique_eraser_planted_2d_target()`
- **test `test_oblique_eraser_keeps_orthogonal_signal`** [L187-206]: `def test_oblique_eraser_keeps_orthogonal_signal()`
- **test `test_two_column_target_in_one_direction_has_rank_one`** [L209-220]: `def test_two_column_target_in_one_direction_has_rank_one()`
- **test `test_noise_free_scalar_target_has_rho_one`** [L223-228]: `def test_noise_free_scalar_target_has_rho_one()`
- **function `_two_scale_target`** [L231-235]: `def _two_scale_target(seed=10)`
- **test `test_rank_tolerance_is_relative_and_used`** [L238-244]: `def test_rank_tolerance_is_relative_and_used()`
- **test `test_eraser_invalid_keeps_computed_map`** [L247-256]: `def test_eraser_invalid_keeps_computed_map()`
- **test `test_constant_target_zero_variance`** [L261-267]: `def test_constant_target_zero_variance(Z)` decorators: @pytest.mark.parametrize('Z', [np.full((800, 2), 3.0), 5.0 + 1e-08 * np.random.default_rng(11).normal(size=(800, 2))])
- **test `test_exactly_uncorrelated_target`** [L270-282]: `def test_exactly_uncorrelated_target()`
- **test `test_degenerate_whitening_propagates`** [L285-292]: `def test_degenerate_whitening_propagates()`
- **test `test_rank_deficient_X_erasure_stays_in_retained_range`** [L295-314]: `def test_rank_deficient_X_erasure_stays_in_retained_range()`

