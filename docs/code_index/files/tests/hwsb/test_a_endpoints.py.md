# `tests/hwsb/test_a_endpoints.py`

- Source: [tests/hwsb/test_a_endpoints.py](../../../../../tests/hwsb/test_a_endpoints.py)
- Kind: python
- Lines: 257

## Module docstring

> HWSB author A: B4-B6 inputs on planted moments and support (protocol §4 B4, B5, B6; DRB8).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 29, via sys.path edit)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 30, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 33, via sys.path edit)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../../tools/hwsb/hwsb_eval.py.md) (line 34, via sys.path edit)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../../tools/hwsb/hwsb_gates.py.md) (line 35, via sys.path edit)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 10)
- `math` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)
- `types` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 27: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `MISSING`
- `NO_CHART`
- `REPO`
- `UNAV`

## Classes and functions

- **function `need`** [L45-47]: `def need()`
- **function `tree_mean_ref`** [L50-59]: `def tree_mean_ref(x) -> float` - Own balanced-tree mean: adjacent pairs level by level (odd last entry carried), / n.
- **function `planted`** [L62-72]: `def planted(n=41, seed=616201, n_sup=27)`
- **function `endpoints_ref`** [L75-79]: `def endpoints_ref(phi, sup, m32, m4)`
- **test `test_reference_tree_mean_matches_reused`** [L84-88]: `def test_reference_tree_mean_matches_reused()`
- **test `test_reference_endpoints_match_reused`** [L91-96]: `def test_reference_endpoints_match_reused()`
- **test `test_endpoints_partial_support_exact`** [L101-114]: `def test_endpoints_partial_support_exact()`
- **test `test_endpoints_no_or_full_support`** [L118-128]: `def test_endpoints_no_or_full_support(n_sup)` decorators: @pytest.mark.parametrize('n_sup', [0, 41])
- **test `test_endpoints_supported_rows_use_the_extension_phase_only`** [L131-139]: `def test_endpoints_supported_rows_use_the_extension_phase_only()`
- **test `test_support_missing_mass_and_width_exact`** [L144-163]: `def test_support_missing_mass_and_width_exact()`
- **test `test_support_reasons_count_unsupported_rows`** [L166-175]: `def test_support_reasons_count_unsupported_rows()`
- **test `test_d4_rows_equal_k4b_delta4_orc`** [L180-192]: `def test_d4_rows_equal_k4b_delta4_orc()`
- **function `_maps`** [L197-205]: `def _maps(cal_val)` - cal_val: {j: (c0_cal status, c0_val status)} -> the b4_cal-like and b4_val-like dicts.
- **test `test_b4_status_both_pass`** [L212-218]: `def test_b4_status_both_pass()`
- **test `test_b4_status_cal_failure_is_c0_cal`** [L221-228]: `def test_b4_status_cal_failure_is_c0_cal()`
- **test `test_b4_status_first_failing_model_in_master_order`** [L231-237]: `def test_b4_status_first_failing_model_in_master_order()`
- **test `test_b4_status_no_chart_counts_against_c0_val`** [L240-244]: `def test_b4_status_no_chart_counts_against_c0_val()`
- **test `test_b4_status_technical_status_reported`** [L247-257]: `def test_b4_status_technical_status_reported()`

