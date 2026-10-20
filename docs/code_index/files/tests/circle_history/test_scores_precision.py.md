# `tests/circle_history/test_scores_precision.py`

- Source: [tests/circle_history/test_scores_precision.py](../../../../../tests/circle_history/test_scores_precision.py)
- Kind: python
- Lines: 344

## Module docstring

> Independent tests (author B) for scores.py: TEST_PLAN items B1-B4 and B8 (spec v2.2).

## Imports

### Internal (repo files)

- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 26, via sys.path edit)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 27, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 28, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 29, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 15)
- `hashlib` (lines 11)
- `itertools` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CONTROLS`
- `COORDS`
- `COORDS_RATIONAL`
- `E`
- `E_EXACT`
- `F`
- `FEAT_EXACT`
- `L_ENUM`
- `PI`
- `PI_EXACT`
- `REPO_ROOT`
- `T`
- `T_EXACT`

## Classes and functions

- **function `_stationary`** [L40-54]: `def _stationary(trans: list[list[Fraction]]) -> list[Fraction]` - Exact stationary law: pi (T - I) = 0 and sum(pi) = 1, Gauss-Jordan in Fractions.
- **function `_rows`** [L64-67]: `def _rows(n: int, width: int = 32) -> np.ndarray` - Deterministic canonical histories (every token sequence is possible under the HMM).
- **test `test_fixture_hmm_is_exactly_stationary_and_asymmetric`** [L70-74]: `def test_fixture_hmm_is_exactly_stationary_and_asymmetric() -> None`
- **test `test_canonical_from_named_inverse_permutation`** [L78-84]: `def test_canonical_from_named_inverse_permutation() -> None`
- **test `test_canonical_from_named_round_trips_contract_formula`** [L87-92]: `def test_canonical_from_named_round_trips_contract_formula() -> None`
- **test `test_canonical_from_named_rejects_non_permutations`** [L96-99]: `def test_canonical_from_named_rejects_non_permutations(perm: list[int]) -> None` decorators: @pytest.mark.parametrize('perm', [[0, 0, 1, 2], [0, 1, 2, 4], [-1, 0, 1, 2], [1, 2, 3, 4]])
- **test `test_canonical_from_named_round_trip_check_catches_negative_named`** [L102-105]: `def test_canonical_from_named_round_trip_check_catches_negative_named() -> None`
- **test `test_history_digests_known_values_and_shape`** [L108-117]: `def test_history_digests_known_values_and_shape() -> None`
- **test `test_oracle_moments_equals_posterior_means_and_decimal_reference`** [L121-133]: `def test_oracle_moments_equals_posterior_means_and_decimal_reference() -> None`
- **test `test_oracle_moments_rejects_any_width_but_32`** [L137-140]: `def test_oracle_moments_rejects_any_width_but_32(width: int) -> None` decorators: @pytest.mark.parametrize('width', [33, 31])
- **function `_forward`** [L150-156]: `def _forward(word: tuple[int, ...]) -> list[Fraction]` - Exact unnormalised forward vector of a window started at pi (emit first).
- **function `_posterior`** [L159-162]: `def _posterior(word: tuple[int, ...]) -> tuple[list[Fraction], Fraction]`
- **function `_moment`** [L165-166]: `def _moment(post: list[Fraction]) -> tuple[Fraction, Fraction]`
- **function `exact_enum`** [L170-173]: `def exact_enum()` decorators: @pytest.fixture(scope='module')
- **function `float_enum`** [L177-184]: `def float_enum()` decorators: @pytest.fixture(scope='module')
- **function `_expect_score`** [L187-196]: `def _expect_score(enum, k: int, g) -> Fraction` - Exact E[g(suffix_k) . (m_L - m_k)] over every history of length L_ENUM.
- **test `test_zero_identity_exact_per_suffix`** [L200-215]: `def test_zero_identity_exact_per_suffix(exact_enum, k: int) -> None` decorators: @pytest.mark.parametrize('k', [2, 4]) - sum_prefix P(prefix + s) (P_L - P_k(s)) == 0 for every suffix s: by linearity this is the
- **test `test_zero_identity_exact_for_rational_suffix_functions`** [L219-227]: `def test_zero_identity_exact_for_rational_suffix_functions(exact_enum, k: int) -> None` decorators: @pytest.mark.parametrize('k', [2, 4])
- **test `test_zero_identity_exact_for_the_three_controls`** [L231-237]: `def test_zero_identity_exact_for_the_three_controls(exact_enum, float_enum, name: str) -> None` decorators: @pytest.mark.parametrize('name', CONTROLS)
- **test `test_zero_identity_float_controls_within_1e12`** [L241-248]: `def test_zero_identity_float_controls_within_1e12(exact_enum, float_enum, name: str) -> None` decorators: @pytest.mark.parametrize('name', CONTROLS)
- **test `test_unit_vectors_scores_and_r4_norms_known_answers`** [L252-261]: `def test_unit_vectors_scores_and_r4_norms_known_answers() -> None`
- **function `_hand_phase`** [L264-266]: `def _hand_phase(last4: np.ndarray) -> float`
- **test `test_sha256_phase_hand_derived_from_hashlib`** [L269-273]: `def test_sha256_phase_hand_derived_from_hashlib() -> None`
- **test `test_control_vectors_zero_maps_to_unit_x_and_others_unit_norm`** [L276-299]: `def test_control_vectors_zero_maps_to_unit_x_and_others_unit_norm() -> None`
- **test `test_angular_instability_boundaries`** [L302-308]: `def test_angular_instability_boundaries() -> None`
- **test `test_control_vectors_tiny_and_subnormal_vectors`** [L312-325]: `def test_control_vectors_tiny_and_subnormal_vectors() -> None`
- **test `test_angular_instability_uses_stable_magnitude_for_subnormals`** [L328-332]: `def test_angular_instability_uses_stable_magnitude_for_subnormals() -> None`
- **test `test_angular_instability_rejects_nonfinite_input`** [L336-338]: `def test_angular_instability_rejects_nonfinite_input(bad_m) -> None` decorators: @pytest.mark.parametrize('bad_m', [[[np.nan, 0.0]], [[0.0, np.inf]], [[-np.inf, 1.0]]])
- **test `test_angular_instability_rejects_bad_bound`** [L342-344]: `def test_angular_instability_rejects_bad_bound(bound: float) -> None` decorators: @pytest.mark.parametrize('bound', [-1.0, -1e-300, np.nan, np.inf])

