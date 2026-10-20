# `tests/c1prime/test_b_gates.py`

- Source: [tests/c1prime/test_b_gates.py](../../../../../tests/c1prime/test_b_gates.py)
- Kind: python
- Lines: 212

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-3 part 3: damage, leakage, M2, V1, V2, M4.

## Imports

### Internal (repo files)

- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 24, via sys.path edit)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](../../tools/c1prime/c1_gates.py.md) (line 25, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 10)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `FAM`
- `NUIS`
- `REPO`
- `TWO_PI`

## Classes and functions

- **function `_status`** [L34-35]: `def _status(res) -> str`
- **test `test_D_w_counts_both_arms_over_2n`** [L41-47]: `def test_D_w_counts_both_arms_over_2n()`
- **test `test_D_y_and_leakage`** [L50-59]: `def test_D_y_and_leakage()`
- **function `_m2`** [L65-68]: `def _m2(Dw_T=0.0, Dy_T=0.0, Dw_C=None, Dy_C=None, L_T=None, active=False)`
- **test `test_m2_primary_ceilings_are_inclusive`** [L71-75]: `def test_m2_primary_ceilings_are_inclusive()`
- **test `test_m2_matching_bounds_are_inclusive`** [L78-82]: `def test_m2_matching_bounds_are_inclusive()`
- **test `test_m2_family_ceiling_fails_even_when_dispersion_holds`** [L85-87]: `def test_m2_family_ceiling_fails_even_when_dispersion_holds()`
- **test `test_m2_dispersion_needs_28_of_32_frames`** [L90-96]: `def test_m2_dispersion_needs_28_of_32_frames()`
- **test `test_m2_leakage_only_when_active_and_after_family`** [L99-103]: `def test_m2_leakage_only_when_active_and_after_family()`
- **test `test_wrap_maps_into_minus_pi_exclusive_pi_inclusive`** [L109-120]: `def test_wrap_maps_into_minus_pi_exclusive_pi_inclusive()`
- **function `_m32`** [L123-124]: `def _m32(theta)`
- **function `_v1_fixture`** [L127-137]: `def _v1_fixture(row4_agrees)`
- **test `test_v1_counts_median_ties_wraps_and_treats_sign_zero_as_disagreement`** [L140-142]: `def test_v1_counts_median_ties_wraps_and_treats_sign_zero_as_disagreement()`
- **test `test_v1_sign_zero_on_both_sides_is_still_disagreement`** [L145-150]: `def test_v1_sign_zero_on_both_sides_is_still_disagreement()`
- **function `_v2`** [L153-164]: `def _v2(flips=(), scale=1.0, base=3.0, zero_arms=())`
- **test `test_v2_kappa_agreement_wrap_and_sign_zero`** [L176-177]: `def test_v2_kappa_agreement_wrap_and_sign_zero(kwargs, expected)` decorators: @pytest.mark.parametrize('kwargs,expected', [({}, 'PASS'), ({'flips': (9, 10)}, 'PASS'), ({'flips': (9, 10, 11)}, 'INCONCLUSIVE/MANIPULATION_FAILED'), ({'scale': 0.52}, 'PASS'), ({'scale': 0.48}, 'INCONCLUSIVE/MANIPULATION_FAILED'), ({'scale': 1.48}, 'PASS'), ({'scale': 1.52}, 'INCONCLUSIVE/MANIPULATION_FAILED'), ({'scale': 0.6, 'base': 6.2}, 'PASS'), ({'zero_arms': tuple(range(11))}, 'INCONCLUSIVE/MANIPULATION_FAILED')])
- **test `test_m4_boundaries`** [L183-198]: `def test_m4_boundaries()`
- **class `_FixedDecoder`** [L201-206]
- **method `_FixedDecoder.__init__`** [L202-203]: `def __init__(self, scores)`
- **method `_FixedDecoder.predict`** [L205-206]: `def predict(self, a)`
- **test `test_w_hat_breaks_ties_to_the_lowest_index`** [L209-212]: `def test_w_hat_breaks_ties_to_the_lowest_index()`

