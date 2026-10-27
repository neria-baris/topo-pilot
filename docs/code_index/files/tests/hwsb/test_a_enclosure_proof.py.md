# `tests/hwsb/test_a_enclosure_proof.py`

- Source: [tests/hwsb/test_a_enclosure_proof.py](../../../../../tests/hwsb/test_a_enclosure_proof.py)
- Kind: python
- Lines: 339

## Module docstring

> HWSB author A: the B8a enclosure proof steps (protocol §4 B8a with delta as in RC-1; KB4 at
> sigma 5/4; DRB12; the proof note obligation of OPEN-3).

## Imports

### Internal (repo files)

- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 34, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 35, via sys.path edit)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 36, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 39, via sys.path edit)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../../tools/hwsb/hwsb_law.py.md) (line 40, via sys.path edit)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 13)
- `decimal` (lines 15, 18)
- `fractions` (lines 19)
- `math` (lines 16)
- `pathlib` (lines 20)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 30: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 32: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CENTRES`
- `MISSING`
- `REPO`
- `STATES`
- `U60`

## Classes and functions

- **function `need`** [L53-55]: `def need()`
- **function `logits_ref`** [L58-67]: `def logits_ref(sigma)`
- **function `round60`** [L70-85]: `def round60(q: Fraction) -> Fraction` - q rounded to 60 significant decimal digits, ties to even (exact integer arithmetic).
- **function `lo_hi0`** [L88-92]: `def lo_hi0()`
- **function `dec`** [L95-97]: `def dec(fr: Fraction, prec: int) -> Decimal`
- **function `softmax_dec`** [L100-104]: `def softmax_dec(row, prec)`
- **function `ref74`** [L108-114]: `def ref74()` decorators: @pytest.fixture(scope='module')
- **function `enc74`** [L118-122]: `def enc74()` decorators: @pytest.fixture(scope='module')
- **test `test_reference_states_are_the_documented_lattice`** [L127-130]: `def test_reference_states_are_the_documented_lattice()`
- **test `test_reference_round60_agrees_with_decimal_division`** [L133-138]: `def test_reference_round60_agrees_with_decimal_division(ref74)`
- **test `test_reference_sigma_5_4_logits_terminate`** [L141-143]: `def test_reference_sigma_5_4_logits_terminate()`
- **test `test_reference_step3_inequalities_for_u_qmax`** [L146-150]: `def test_reference_step3_inequalities_for_u_qmax(ref74)`
- **test `test_exact_logits_equal_independent_fractions`** [L155-164]: `def test_exact_logits_equal_independent_fractions()`
- **test `test_centres_in_softmax_enclosure_order`** [L167-169]: `def test_centres_in_softmax_enclosure_order()`
- **test `test_sigma_5_4_delta_zero_and_identical_to_old_enclosure`** [L174-189]: `def test_sigma_5_4_delta_zero_and_identical_to_old_enclosure()`
- **test `test_sigma_7_4_rounding_delta`** [L194-205]: `def test_sigma_7_4_rounding_delta(ref74)`
- **test `test_sigma_7_4_rounded_logits_are_q_tilde`** [L208-213]: `def test_sigma_7_4_rounded_logits_are_q_tilde(ref74)`
- **test `test_sigma_7_4_widened_lo_hi`** [L216-223]: `def test_sigma_7_4_widened_lo_hi(ref74, enc74)`
- **test `test_sigma_7_4_e_dec_computed_from_q_tilde`** [L226-237]: `def test_sigma_7_4_e_dec_computed_from_q_tilde(ref74, enc74)` - Step (1): the existing analysis applies to the exact inputs q~ (process_law.py:117-124).
- **test `test_step2_ratio_bound_at_200_digits`** [L240-252]: `def test_step2_ratio_bound_at_200_digits(ref74)`
- **test `test_step3_on_actual_delta`** [L255-263]: `def test_step3_on_actual_delta(ref74)`
- **test `test_enclosure_contains_exact_entries_on_sampled_rows`** [L266-275]: `def test_enclosure_contains_exact_entries_on_sampled_rows(ref74, enc74)` - Steps (1)-(3) combined: E*_j in [E_dec (1 - 2 delta)/hi0, E_dec/(lo0 (1 - 2 delta))].
- **test `test_digits_other_than_60_raise_invalid`** [L280-285]: `def test_digits_other_than_60_raise_invalid()`
- **function `entries_with_extremes`** [L288-294]: `def entries_with_extremes(ref74, k=58, seed=616601)`
- **test `test_decimal_check_passes_on_true_enclosure`** [L297-304]: `def test_decimal_check_passes_on_true_enclosure(ref74, enc74)`
- **test `test_decimal_check_catches_planted_narrow_enclosure`** [L307-314]: `def test_decimal_check_catches_planted_narrow_enclosure(ref74, enc74)`
- **test `test_bound_law_restores_process_law_state`** [L317-330]: `def test_bound_law_restores_process_law_state()`
- **test `test_proof_note_exists_and_names_delta_and_rounding`** [L333-339]: `def test_proof_note_exists_and_names_delta_and_rounding()` - OPEN-3: the reviewed proof note is in tools/hwsb (content reviewed elsewhere).

