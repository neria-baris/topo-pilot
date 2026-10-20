# `tests/analysis/test_x4f_erasure_family.py`

- Source: [tests/analysis/test_x4f_erasure_family.py](../../../../../tests/analysis/test_x4f_erasure_family.py)
- Kind: python
- Lines: 237

## Module docstring

> Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
> before reading the implementation.
> (Mechanically split out of test_x4f_erasure.py by the builder to respect the 400-line limit;
> test bodies unchanged.)

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import Family, mismatch_report, random_family, whiten` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 11, via package root)

### External (third-party)

- `numpy` (lines 8)
- `pytest` (lines 9)

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

- **function `pop_cov`** [L25-28]: `def pop_cov(A, B=None)`
- **function `anisotropic_X`** [L31-36]: `def anisotropic_X(n=3000, d=6, seed=0, top=2.5)` - Correlated anisotropic features; covariance condition number about 10**(2*top).
- **function `rank_deficient_X`** [L39-41]: `def rank_deficient_X(n=600, d=8, r=5, seed=1)`
- **function `numerical_rank`** [L44-46]: `def numerical_rank(A, rel=1e-08)`
- **function `rng_for_seed`** [L49-50]: `def rng_for_seed(seed)`
- **function `ref_family_draw`** [L53-60]: `def ref_family_draw(X, wh, rank, rng)` - Spec section 2.2 draw: G in R^{k x rank}, Q from QR, E = W+ Q Q^T W, M = I - E.
- **test `test_family_matches_spec_draw_procedure_and_window`** [L66-90]: `def test_family_matches_spec_draw_procedure_and_window()`
- **test `test_family_rank_deficient_maps_live_in_retained_range`** [L93-108]: `def test_family_rank_deficient_maps_live_in_retained_range()`
- **test `test_family_rank_equal_to_k_allowed_and_rank_above_k_rejected`** [L111-121]: `def test_family_rank_equal_to_k_allowed_and_rank_above_k_rejected()`
- **test `test_family_deterministic_given_rng_for`** [L124-136]: `def test_family_deterministic_given_rng_for()`
- **test `test_family_zero_displacement_makes_no_draws`** [L139-153]: `def test_family_zero_displacement_makes_no_draws()`
- **test `test_family_degenerate_features`** [L156-160]: `def test_family_degenerate_features()`
- **test `test_family_unmatched_small_budget_returns_accepted`** [L163-171]: `def test_family_unmatched_small_budget_returns_accepted()`
- **test `test_family_unmatched_impossible_target`** [L174-181]: `def test_family_unmatched_impossible_target()`
- **class `_DuplicatingGenerator`** [L184-196] - A Generator whose standard_normal output has two identical columns (a degenerate draw).
- **method `_DuplicatingGenerator.__init__`** [L187-188]: `def __init__(self, real)`
- **method `_DuplicatingGenerator.standard_normal`** [L190-193]: `def standard_normal(self, *args, **kwargs)`
- **method `_DuplicatingGenerator.__getattr__`** [L195-196]: `def __getattr__(self, name)`
- **test `test_family_degenerate_draws_rejected_and_counted`** [L199-212]: `def test_family_degenerate_draws_rejected_and_counted()`
- **test `test_mismatch_report_hand_values_and_exclusion`** [L217-228]: `def test_mismatch_report_hand_values_and_exclusion()`
- **test `test_mismatch_report_threshold_scales_with_scale`** [L231-237]: `def test_mismatch_report_threshold_scales_with_scale()`

