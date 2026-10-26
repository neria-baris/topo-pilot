# `tests/c2_readout/test_b_screens.py`

- Source: [tests/c2_readout/test_b_screens.py](../../../../../tests/c2_readout/test_b_screens.py)
- Kind: python
- Lines: 347

## Module docstring

> Author B (job 0101): T-R1 (RC-14, NEW-3), T-N2 (RC-6), T-CMODE (RC-5, RC-6).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 20, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 21, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 22, via sys.path edit)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 23, via sys.path edit)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../../tools/c2_readout/c2_oracle.py.md) (line 24, via sys.path edit)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 25, via unique basename)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](../../tools/c1prime/c1_gates.py.md) (line 26, via unique basename)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 11)
- `pathlib` (lines 12)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `RADIAL`
- `REPO`

## Classes and functions

- **function `_m`** [L33-35]: `def _m(angle, r=0.5)`
- **function `_r1`** [L38-44]: `def _r1(pp, pm, ap, am, mod_p=None, mod_m=None, thr=1e-12, mp=None, mm=None)`
- **test `test_r1_without_overrides_reproduces_c1_gates_v1_bitwise`** [L48-62]: `def test_r1_without_overrides_reproduces_c1_gates_v1_bitwise()`
- **test `test_r1_wraps_at_plus_minus_pi`** [L65-70]: `def test_r1_wraps_at_plus_minus_pi()`
- **test `test_r1_sign_zero_is_disagreement_and_three_quarters_passes`** [L73-80]: `def test_r1_sign_zero_is_disagreement_and_three_quarters_passes()`
- **test `test_r1_median_ties_use_inverted_cdf`** [L83-89]: `def test_r1_median_ties_use_inverted_cdf()`
- **test `test_r1_zero_modulus_override_before_median_and_no_row_deleted`** [L92-110]: `def test_r1_zero_modulus_override_before_median_and_no_row_deleted()`
- **test `test_zero_code_threshold_and_override`** [L113-126]: `def test_zero_code_threshold_and_override()`
- **test `test_r1_failure_routes_to_cnhs`** [L129-136]: `def test_r1_failure_routes_to_cnhs()`
- **test `test_masked_oracle_phase_features`** [L139-150]: `def test_masked_oracle_phase_features()`
- **test `test_s_star_fit_uses_masked_regressors_and_is_deterministic`** [L153-167]: `def test_s_star_fit_uses_masked_regressors_and_is_deterministic()`
- **test `test_n2_fit_class_mean_mahalanobis_and_q99`** [L171-186]: `def test_n2_fit_class_mean_mahalanobis_and_q99()`
- **function `_states`** [L189-190]: `def _states(norms)`
- **function `_fixed_fit`** [L193-194]: `def _fixed_fit()`
- **test `test_n2_fraction_rule_and_cap_exact`** [L199-210]: `def test_n2_fraction_rule_and_cap_exact(d_beyond, s_beyond, status)` decorators: @pytest.mark.parametrize('d_beyond, s_beyond, status', [(4, 6, 'PASS'), (4, 7, RADIAL), (0, 5, 'PASS'), (0, 6, RADIAL)])
- **test `test_n2_paired_gaussian_counterexample_passes_the_radial_screen`** [L213-233]: `def test_n2_paired_gaussian_counterexample_passes_the_radial_screen()`
- **function `_oblique`** [L237-239]: `def _oblique(rng, p=128, k=6)`
- **test `test_cm_replacements_F_S_C`** [L242-250]: `def test_cm_replacements_F_S_C()`
- **function `_cancellation`** [L253-261]: `def _cancellation()`
- **function `_bounds`** [L264-267]: `def _bounds(arr, g=None)`
- **function `_m_bounds`** [L270-273]: `def _m_bounds(stats)`
- **test `test_cm_quantities_and_cancellation_fixture_is_routed_around`** [L276-305]: `def test_cm_quantities_and_cancellation_fixture_is_routed_around()`
- **function `_m_licence_common`** [L308-314]: `def _m_licence_common(text)`
- **function `_upstream_used_stats`** [L317-320]: `def _upstream_used_stats(n=32)`
- **test `test_upstream_used_licence_names_the_residual_skip_and_no_block3_claim`** [L323-331]: `def test_upstream_used_licence_names_the_residual_skip_and_no_block3_claim()`
- **test `test_y2_activity_and_resp_in_the_m_stream`** [L334-347]: `def test_y2_activity_and_resp_in_the_m_stream()`

