# `tests/circle_history/test_scores_precision_gates.py`

- Source: [tests/circle_history/test_scores_precision_gates.py](../../../../../tests/circle_history/test_scores_precision_gates.py)
- Kind: python
- Lines: 301

## Module docstring

> Independent tests (author B) for precision.py: TEST_PLAN items B5 and B9 (spec v2.2).

## Imports

### Internal (repo files)

- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 29, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 21)
- `pytest` (lines 22)

### Standard library

- `__future__` (lines 13)
- `json` (lines 15)
- `math` (lines 16)
- `pathlib` (lines 18)
- `statistics` (lines 19)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BASE`
- `CFG`
- `E_GOOD`
- `GOOD_SD`
- `MODELS`
- `N_EVAL`
- `PREC`
- `R4N`
- `REPO_ROOT`
- `X_DICT`
- `_CONTRACT`

## Classes and functions

- **function `_record`** [L40-49]: `def _record(summary: dict, model: int) -> dict`
- **function `_verdict`** [L52-56]: `def _verdict(summary: dict) -> str`
- **function `_mde`** [L59-62]: `def _mde(sd: float) -> float`
- **test `test_cfg_comes_from_contract_values`** [L65-69]: `def test_cfg_comes_from_contract_values() -> None`
- **function `_manual_sd_b4`** [L80-89]: `def _manual_sd_b4(seed: int, draws: int, size: int) -> tuple[np.ndarray, np.ndarray]`
- **function `_manual_centered`** [L92-99]: `def _manual_centered(seed: int, draws: int, size: int) -> np.ndarray`
- **test `test_sd_b4_draws_reproduce_manual_loop_with_shared_idx`** [L103-112]: `def test_sd_b4_draws_reproduce_manual_loop_with_shared_idx(size: int) -> None` decorators: @pytest.mark.parametrize('size', [9, N_EVAL])
- **test `test_centered_draws_reproduce_manual_loop_with_shared_idx`** [L116-121]: `def test_centered_draws_reproduce_manual_loop_with_shared_idx(size: int) -> None` decorators: @pytest.mark.parametrize('size', [7, N_EVAL])
- **test `test_mde_formula_via_normal_dist`** [L124-129]: `def test_mde_formula_via_normal_dist() -> None`
- **test `test_precision_summary_inverted_cdf_quantiles_power_and_mde_fields`** [L133-155]: `def test_precision_summary_inverted_cdf_quantiles_power_and_mde_fields() -> None`
- **function `_mde_upper_at`** [L162-164]: `def _mde_upper_at(sd_value: float) -> float`
- **function `boundary_sd`** [L168-189]: `def boundary_sd() -> tuple[float, float]` decorators: @pytest.fixture(scope='module') - The float sd whose mde_upper is EXACTLY .02 in production arithmetic, and the next float
- **test `test_precision_pass_at_exact_equalities`** [L192-199]: `def test_precision_pass_at_exact_equalities(boundary_sd) -> None`
- **test `test_precision_just_over_mde_or_under_power_is_inconclusive`** [L202-217]: `def test_precision_just_over_mde_or_under_power_is_inconclusive(boundary_sd) -> None`
- **test `test_precision_summary_nonfinite_raises_invalid`** [L220-229]: `def test_precision_summary_nonfinite_raises_invalid() -> None`
- **function `_b4_column`** [L233-236]: `def _b4_column(second: float) -> np.ndarray` - 30 draws whose 2nd order statistic (the inverted_cdf 0.05 quantile) is ``second``.
- **function `_b4`** [L239-241]: `def _b4(draws: np.ndarray) -> dict`
- **test `test_b4_lower_equal_to_delta_is_not_pass`** [L244-254]: `def test_b4_lower_equal_to_delta_is_not_pass() -> None`
- **test `test_b4_lower_just_above_delta_passes`** [L257-262]: `def test_b4_lower_just_above_delta_passes() -> None`
- **test `test_precision_summary_fail_closed`** [L279-281]: `def test_precision_summary_fail_closed(models, sd, e) -> None` decorators: @pytest.mark.parametrize('models, sd, e', [((), np.zeros((10, 0)), np.zeros((10, 0))), ((1729, 1729, 2718), GOOD_SD, E_GOOD), (MODELS, GOOD_SD[:, :2], E_GOOD), (MODELS, GOOD_SD, E_GOOD[:, :2]), (MODELS, GOOD_SD[:, 0], E_GOOD), (MODELS, GOOD_SD, E_GOOD.reshape(10, 3, 1)), (MODELS, np.zeros((0, 3)), E_GOOD), (MODELS, GOOD_SD, np.zeros((0, 3)))])
- **test `test_b4_summary_fail_closed`** [L284-301]: `def test_b4_summary_fail_closed() -> None`

