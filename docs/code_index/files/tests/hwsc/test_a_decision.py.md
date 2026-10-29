# `tests/hwsc/test_a_decision.py`

- Source: [tests/hwsc/test_a_decision.py](../../../../../tests/hwsc/test_a_decision.py)
- Kind: python
- Lines: 370

## Module docstring

> Author A (job 0176): decision maths and the POSITIVE_BELOW_MARGIN annotation.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 24, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 25, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 26, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 27, via unique basename)

### External (third-party)

- `pytest` (lines 17)

### Standard library

- `__future__` (lines 8)
- `copy` (lines 10)
- `fractions` (lines 14)
- `math` (lines 11)
- `pathlib` (lines 15)
- `random` (lines 12)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `F_SMALL`
- `M`
- `MODELS`
- `REPO`
- `_HWSC`

## Classes and functions

- **function `bound`** [L36-38]: `def bound()` decorators: @pytest.fixture
- **function `ref_status`** [L41-56]: `def ref_status(L, U, Fm, Fp)` - Independent K4B §8.1 rule in exact rationals (L <= U assumed).
- **function `ms`** [L59-60]: `def ms(L, U, Fm, Fp)`
- **function `lower_at`** [L63-67]: `def lower_at(target, L)` - F_minus such that Fraction(L) - F_minus == target exactly (F_minus > 0).
- **function `upper_at`** [L70-74]: `def upper_at(target, U)` - F_plus such that Fraction(U) + F_plus == target exactly (F_plus > 0).
- **test `test_bound_constants`** [L80-82]: `def test_bound_constants(bound)`
- **test `test_support_and_exclude_basic`** [L85-88]: `def test_support_and_exclude_basic(bound)`
- **test `test_support_boundary_is_unresolved`** [L91-101]: `def test_support_boundary_is_unresolved(bound)`
- **test `test_exclude_upper_boundary_is_unresolved`** [L104-112]: `def test_exclude_upper_boundary_is_unresolved(bound)`
- **test `test_exclude_lower_side_boundary`** [L115-122]: `def test_exclude_lower_side_boundary(bound)`
- **test `test_unresolved_numerical_when_f_alone_blocks`** [L125-135]: `def test_unresolved_numerical_when_f_alone_blocks(bound)`
- **test `test_negative_alignment_label`** [L138-148]: `def test_negative_alignment_label(bound)`
- **test `test_random_grid_matches_reference_and_exclusive`** [L151-165]: `def test_random_grid_matches_reference_and_exclusive(bound)`
- **test `test_overall_stage_c_keys`** [L182-183]: `def test_overall_stage_c_keys(bound, statuses, expected)` decorators: @pytest.mark.parametrize('statuses, expected', [(('SUPPORT',) * 3, 'SUPPORT'), (('EXCLUDE',) * 3, 'EXCLUSION'), (('SUPPORT', 'EXCLUDE', 'UNRESOLVED'), 'MIXED'), (('SUPPORT', 'SUPPORT', 'UNRESOLVED'), 'MIXED'), (('EXCLUDE', 'EXCLUDE', 'UNRESOLVED/NUMERICAL'), 'MIXED'), (('SUPPORT', 'SUPPORT', 'EXCLUDE'), 'MIXED'), (('UNRESOLVED',) * 3, 'INCONCLUSIVE'), (('UNRESOLVED', 'UNRESOLVED/NUMERICAL', 'UNRESOLVED'), 'INCONCLUSIVE/NUMERICAL'), (('UNRESOLVED/NUMERICAL',) * 3, 'INCONCLUSIVE/NUMERICAL')])
- **function `entry`** [L189-193]: `def entry(L, U, Fm, Fp, as_str=True)`
- **function `zero_point`** [L196-201]: `def zero_point(F)` - Largest float x with Fraction(x) <= F.
- **function `pbm_kind`** [L204-206]: `def pbm_kind(res, j)`
- **function `pbm_pos`** [L209-211]: `def pbm_pos(res, j)`
- **test `test_pbm_zero_is_not_positive_next_float_is`** [L214-228]: `def test_pbm_zero_is_not_positive_next_float_is(bound)`
- **test `test_pbm_non_dyadic_F_zero_point`** [L231-243]: `def test_pbm_non_dyadic_F_zero_point(bound)`
- **test `test_pbm_kinds_and_support_never`** [L246-260]: `def test_pbm_kinds_and_support_never(bound)`
- **test `test_pbm_str_keys_accepted`** [L263-267]: `def test_pbm_str_keys_accepted(bound)`
- **function `result`** [L273-283]: `def result(pm, fresh_low=False)`
- **function `check_outcome_unchanged`** [L286-295]: `def check_outcome_unchanged(res)`
- **test `test_annotations_exclusion_all_positive`** [L298-306]: `def test_annotations_exclusion_all_positive(bound)`
- **test `test_annotations_support_never`** [L309-314]: `def test_annotations_support_never(bound)`
- **test `test_annotations_mixed_all_positive`** [L317-327]: `def test_annotations_mixed_all_positive(bound)`
- **test `test_annotations_not_all_positive`** [L330-340]: `def test_annotations_not_all_positive(bound)`
- **test `test_annotations_negative_numerical_fresh`** [L343-359]: `def test_annotations_negative_numerical_fresh(bound)`
- **test `test_annotations_no_flags_when_clean`** [L362-370]: `def test_annotations_no_flags_when_clean(bound)`

