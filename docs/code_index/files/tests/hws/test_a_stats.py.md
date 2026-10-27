# `tests/hws/test_a_stats.py`

- Source: [tests/hws/test_a_stats.py](../../../../../tests/hws/test_a_stats.py)
- Kind: python
- Lines: 286

## Module docstring

> Author A (job 0119): z constants, bounds, ranks, nulls, E5 and the Pinsker count.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 23, via sys.path edit)
- `import hws_stats` -> [tools/hws/hws_stats.py](../../tools/hws/hws_stats.py.md) (line 24, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 25, via unique basename)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `fractions` (lines 11)
- `json` (lines 8)
- `math` (lines 9)
- `pathlib` (lines 12)
- `statistics` (lines 13)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `HWS_DIR` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `CENTRES`
- `CONTRACT`
- `HWS_DIR`
- `KC9_CASES`
- `KC9_EXACT`
- `KC9_ULP_UP`
- `REPO`
- `TWO_PI`
- `ZCASES`

## Classes and functions

- **function `_z`** [L32-33]: `def _z(alpha)`
- **function `_tree_mean`** [L36-44]: `def _tree_mean(x)`
- **function `_m32`** [L47-49]: `def _m32(phases, norms=1.0)`
- **test `test_alpha_derivations`** [L57-68]: `def test_alpha_derivations()`
- **test `test_z_constants`** [L72-78]: `def test_z_constants(name, ckey, alpha, approx)` decorators: @pytest.mark.parametrize('name, ckey, alpha, approx', ZCASES)
- **test `test_rank_f_is_16`** [L81-82]: `def test_rank_f_is_16()`
- **test `test_summary_tree_mean_and_ddof1`** [L85-95]: `def test_summary_tree_mean_and_ddof1()`
- **test `test_screen_bounds_formulas`** [L98-107]: `def test_screen_bounds_formulas()`
- **test `test_s3_bounds_l3_is_the_smaller_side`** [L111-130]: `def test_s3_bounds_l3_is_the_smaller_side(winner)` decorators: @pytest.mark.parametrize('winner', ['bootstrap', 'normal'])
- **test `test_normal95_and_bootstrap_kernel`** [L133-146]: `def test_normal95_and_bootstrap_kernel()`
- **test `test_null_z_se_zero_cases`** [L149-153]: `def test_null_z_se_zero_cases()`
- **test `test_null_z_threshold_is_strict`** [L156-167]: `def test_null_z_threshold_is_strict()`
- **test `test_e5_norm_fraction_boundary`** [L170-180]: `def test_e5_norm_fraction_boundary()`
- **function `_bins`** [L183-184]: `def _bins(counts)`
- **test `test_e5_bin_count_boundary`** [L187-198]: `def test_e5_bin_count_boundary()`
- **function `_patch_unit_vectors`** [L201-208]: `def _patch_unit_vectors(monkeypatch, planted)`
- **test `test_e5_resultant_boundary`** [L212-220]: `def test_e5_resultant_boundary(monkeypatch, plus, minus, ok)` decorators: @pytest.mark.parametrize('plus, minus, ok', [(33, 15, True), (34, 14, False)])
- **test `test_e5_phase_conventions`** [L223-229]: `def test_e5_phase_conventions()`
- **test `test_pinsker_violations_counts_only_below_minus_tol`** [L232-236]: `def test_pinsker_violations_counts_only_below_minus_tol()`
- **function `_kc9_floor`** [L247-248]: `def _kc9_floor()`
- **function `_kc9_pass`** [L251-252]: `def _kc9_pass(exact, mean, se)`
- **test `test_kc9_float_floor_contract_key`** [L255-262]: `def test_kc9_float_floor_contract_key()`
- **test `test_kc9_float_floor_rule`** [L273-277]: `def test_kc9_float_floor_rule(name, exact, mean, se, ok)` decorators: @pytest.mark.parametrize('name, exact, mean, se, ok', KC9_CASES)
- **test `test_kc9_row_constant_summary`** [L280-286]: `def test_kc9_row_constant_summary()`

