# `tests/circle_history/test_process_law.py`

- Source: [tests/circle_history/test_process_law.py](../../../../../tests/circle_history/test_process_law.py)
- Kind: python
- Lines: 279

## Module docstring

> Independent tests (author B) for process_law.py: TEST_PLAN items B13 and B14 (spec v2.4).

## Imports

### Internal (repo files)

- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 30, via sys.path edit)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 14)
- `decimal` (lines 18)
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

- line 28: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CLAIM`
- `COORDS144`
- `F`
- `P_ROWS`
- `REPO_ROOT`
- `SCALE`
- `STATES`

## Classes and functions

- **function `_cumulative_rows`** [L43-49]: `def _cumulative_rows(P: np.ndarray) -> np.ndarray` - Replica of the frozen dataset/sampler.py `_cumulative_rows` (read, not imported).
- **function `_sweep_q`** [L52-63]: `def _sweep_q(c_row) -> list[Fraction]` - Direct comparison-count law of j = min(#{i: c_i <= k 2^-53}, V-1), k = 0..2^53-1, from the
- **function `_clamp`** [L66-67]: `def _clamp(c_row) -> list[Fraction]`
- **function `_monotone`** [L70-72]: `def _monotone(c_row) -> bool`
- **test `test_sampler_cdf_matches_frozen_cumulative_rows`** [L79-83]: `def test_sampler_cdf_matches_frozen_cumulative_rows() -> None`
- **test `test_threshold_law_equals_direct_counting`** [L93-99]: `def test_threshold_law_equals_direct_counting(c_row, monotone: bool) -> None` decorators: @pytest.mark.parametrize('c_row, monotone', [(_cumulative_rows(P_ROWS)[0], True), (_cumulative_rows(P_ROWS)[1], True), (np.array([0.6, 0.3, 1.0]), False), (np.array([-0.25, 0.5, 1.0]), True), (np.array([0.3, 0.7, 0.9]), False)])
- **test `test_threshold_law_hand_values`** [L102-106]: `def test_threshold_law_hand_values() -> None`
- **function `_row_tv`** [L109-120]: `def _row_tv(p_hat, dev, c_row) -> tuple[Fraction, Fraction | None]`
- **test `test_row_tv_grid_and_documented`** [L123-133]: `def test_row_tv_grid_and_documented() -> None`
- **function `_neighbours`** [L137-140]: `def _neighbours(x: int, y: int) -> set[tuple[int, int]]`
- **function `_t_star`** [L143-153]: `def _t_star() -> list[list[Fraction]]`
- **function `_d2`** [L156-160]: `def _d2(x: int, y: int, j: int) -> Fraction`
- **test `test_lattice_states_and_rejections`** [L163-170]: `def test_lattice_states_and_rejections() -> None`
- **test `test_documented_transition_degrees_wrap_and_identities`** [L173-186]: `def test_documented_transition_degrees_wrap_and_identities() -> None`
- **test `test_softmax_enclosure_contains_80_digit_values`** [L189-207]: `def test_softmax_enclosure_contains_80_digit_values() -> None`
- **function `_value`** [L211-215]: `def _value(out: dict, key: str) -> float`
- **function `_float_law`** [L218-222]: `def _float_law() -> tuple[np.ndarray, np.ndarray, np.ndarray]`
- **function `float_law`** [L226-227]: `def float_law()` decorators: @pytest.fixture(scope='module')
- **test `test_law_constants`** [L230-233]: `def test_law_constants() -> None`
- **test `test_process_law_bound_on_the_rounded_documented_law`** [L236-245]: `def test_process_law_bound_on_the_rounded_documented_law(float_law) -> None`
- **function `_unavailable_cases`** [L248-261]: `def _unavailable_cases(float_law) -> dict`
- **test `test_process_law_bound_unavailable_with_reason`** [L266-269]: `def test_process_law_bound_unavailable_with_reason(float_law, case: str) -> None` decorators: @pytest.mark.parametrize('case', ['zero_support', 'zero_E', 'kappa_ge_1', 'permuted_coords', 'S_143'])
- **test `test_process_law_bound_invalid_only_for_nonfinite_or_misshaped`** [L272-279]: `def test_process_law_bound_invalid_only_for_nonfinite_or_misshaped(float_law) -> None`

