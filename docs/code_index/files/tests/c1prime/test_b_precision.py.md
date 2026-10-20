# `tests/c1prime/test_b_precision.py`

- Source: [tests/c1prime/test_b_precision.py](../../../../../tests/c1prime/test_b_precision.py)
- Kind: python
- Lines: 206

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-2 part 2: ladder, k rule, H5 and V3.

## Imports

### Internal (repo files)

- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../../tools/c1prime/c1_endpoint.py.md) (line 28, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 29, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 13)
- `fractions` (lines 16)
- `pathlib` (lines 17)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `LADDER`
- `MODELS`
- `REPO`

## Classes and functions

- **function `_status`** [L38-39]: `def _status(res) -> str`
- **function `_tree_mean`** [L42-50]: `def _tree_mean(values) -> float`
- **function `_reference_ladder`** [L56-68]: `def _reference_ladder(Z, G)`
- **function `_unit_sd_rows`** [L71-77]: `def _unit_sd_rows(seed, n=400)`
- **function `middle_case`** [L81-84]: `def middle_case()` decorators: @pytest.fixture(scope='module')
- **function `_summary_for`** [L87-93]: `def _summary_for(res, N)`
- **function `_underpowered`** [L96-97]: `def _underpowered(res) -> bool`
- **test `test_ladder_picks_the_smallest_passing_N`** [L100-113]: `def test_ladder_picks_the_smallest_passing_N(middle_case)`
- **test `test_ladder_underpowered_when_no_N_passes`** [L116-121]: `def test_ladder_underpowered_when_no_N_passes()`
- **test `test_k_blocks`** [L128-131]: `def test_k_blocks(N, f_val, k)` decorators: @pytest.mark.parametrize('N,f_val,k', [(4096, 0.92, 2), (8192, 0.92, 3), (16384, 0.92, 5), (16384, 1.0, 5), (4096, 1.0, 2), (8192, 0.95, 3), (16384, 0.9, 5), (8192, 0.99, 3), (4096, 0.9, 2)])
- **test `test_k_blocks_never_exceeds_five_for_admissible_fractions`** [L134-137]: `def test_k_blocks_never_exceeds_five_for_admissible_fractions()`
- **test `test_fresh_fraction_rule`** [L144-145]: `def test_fresh_fraction_rule(f_test, f_val, ok)` decorators: @pytest.mark.parametrize('f_test,f_val,ok', [(0.93, 0.92, True), (0.91, 0.92, True), (0.92, 0.92, True), (0.95, 0.92, False), (0.89, 0.92, False), (0.97, 0.96, True), (0.93, 0.96, False)])
- **function `_h5_lower`** [L151-155]: `def _h5_lower(G, seed)`
- **test `test_h5_pass_headroom_and_guard_band`** [L158-170]: `def test_h5_pass_headroom_and_guard_band()`
- **function `_v3_lowers`** [L176-184]: `def _v3_lowers(Zf, seed)`
- **function `_zf`** [L187-189]: `def _zf(seed, centres)`
- **test `test_v3_pass_and_model_headroom`** [L192-196]: `def test_v3_pass_and_model_headroom()`
- **test `test_v3_guard_band_is_numerical_and_uses_rank_84_of_shared_draws`** [L199-206]: `def test_v3_guard_band_is_numerical_and_uses_rank_84_of_shared_draws()`

