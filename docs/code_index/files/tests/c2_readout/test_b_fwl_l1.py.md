# `tests/c2_readout/test_b_fwl_l1.py`

- Source: [tests/c2_readout/test_b_fwl_l1.py](../../../../../tests/c2_readout/test_b_fwl_l1.py)
- Kind: python
- Lines: 393

## Module docstring

> Author B (job 0101): T-FWL (RC-12) and T-L1 (RC-3) (C2-FROZEN-v2 §13.3; §2.4, §2.5, §6.6);
> also the D-0107-1 G0 (vii) regression (T-NAMESPACE in part; R-0107-2).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 21, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 22, via sys.path edit)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 23, via sys.path edit)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 24, via unique basename)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 26, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 27, via package root)
- `from topo_pilot.prediction.ridge import RidgeProbe` -> [src/topo_pilot/prediction/ridge.py](../../src/topo_pilot/prediction/ridge.py.md) (line 28, via package root)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 323, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 12)
- `hashlib` (lines 320)
- `json` (lines 321)
- `pathlib` (lines 13)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `DEGENERATE`
- `GRID`
- `N`
- `REPO`
- `V2`

## Classes and functions

- **function `_harm`** [L36-40]: `def _harm(phi, K)`
- **function `fwl_data`** [L44-53]: `def fwl_data()` decorators: @pytest.fixture(scope='module')
- **test `test_harmonics_column_order`** [L57-62]: `def test_harmonics_column_order()`
- **test `test_fwl_recovers_known_B_with_K3`** [L65-76]: `def test_fwl_recovers_known_B_with_K3(fwl_data)`
- **test `test_design_and_whitened_ranks`** [L80-94]: `def test_design_and_whitened_ranks(fwl_data, K)` decorators: @pytest.mark.parametrize('K', [1, 2, 3])
- **test `test_rank_failures_keep_every_column`** [L97-107]: `def test_rank_failures_keep_every_column(fwl_data)`
- **test `test_conditioning_failure_at_full_rank`** [L110-116]: `def test_conditioning_failure_at_full_rank(fwl_data)`
- **test `test_degenerate_B_singular_values`** [L119-126]: `def test_degenerate_B_singular_values(fwl_data)`
- **test `test_whitened_rank_and_conditioning_failures`** [L129-140]: `def test_whitened_rank_and_conditioning_failures(fwl_data)`
- **function `_l1_case`** [L144-152]: `def _l1_case(seed, n, code_fn, zt_fn)`
- **function `_zt_plain`** [L155-156]: `def _zt_plain(rng, f1, n)`
- **function `_zt_phase`** [L159-160]: `def _zt_phase(rng, f1, n)`
- **function `_code_snr`** [L163-164]: `def _code_snr(rng, f1, n)`
- **function `_code_half`** [L167-169]: `def _code_half(rng, f1, n)`
- **function `_code_weak`** [L172-173]: `def _code_weak(rng, f1, n)`
- **function `_run_l1`** [L176-187]: `def _run_l1(code_fn, zt_fn, seed)`
- **function `_sse`** [L190-191]: `def _sse(Y, pred)`
- **test `test_decoder_features_layout`** [L194-203]: `def test_decoder_features_layout()`
- **test `test_fit_decoder_recipe_and_equivalence`** [L206-228]: `def test_fit_decoder_recipe_and_equivalence()`
- **test `test_snr_fixture_registered_comparator_passes_where_raw_gls_fails`** [L231-243]: `def test_snr_fixture_registered_comparator_passes_where_raw_gls_fails()`
- **test `test_code_missing_half_the_circle_fails`** [L246-249]: `def test_code_missing_half_the_circle_fails()`
- **function `_flat_numbers`** [L252-257]: `def _flat_numbers(obj)`
- **test `test_nuisance_predictive_fixture_fails_the_incremental_link`** [L260-275]: `def test_nuisance_predictive_fixture_fails_the_incremental_link()`
- **function `_pred_with_sse`** [L278-286]: `def _pred_with_sse(n, sse)` - Entries 2 and 1 against Y = 0, so the SSE is the exact integer `sse` (<= 8 entries).
- **test `test_l1_thresholds_exact`** [L295-299]: `def test_l1_thresholds_exact(sse0, ssec, ssel, status)` decorators: @pytest.mark.parametrize('sse0, ssec, ssel, status', [(8.0, 4.0, 4.0, 'PASS'), (10.0, 1.0, 0.0, 'PASS'), (8.0, 2.0, 1.0, 'EXCLUDED/LINK'), (16.0, 9.0, 9.0, 'EXCLUDED/LINK')])
- **test `test_l1_denominator_fixtures_fail_link`** [L302-309]: `def test_l1_denominator_fixtures_fail_link()`
- **function `_jl`** [L328-329]: `def _jl(**rec)`
- **function `_gate`** [L332-335]: `def _gate(gate, stage='S1', scope='study')`
- **function `_event`** [L338-339]: `def _event(stage='S1', event='STARTED')`
- **function `_own_store`** [L342-350]: `def _own_store(tmp_path, gates, stages, prefix=('', ''))`
- **function `_admitted`** [L353-355]: `def _admitted(store, stage, lin, first)`
- **test `test_own_pre_g0_records_admitted_at_s1`** [L358-364]: `def test_own_pre_g0_records_admitted_at_s1(tmp_path)`
- **test `test_own_records_near_misses_are_not_admitted`** [L378-380]: `def test_own_records_near_misses_are_not_admitted(tmp_path, gates, stages)` decorators: @pytest.mark.parametrize('gates, stages', [([_gate('IMPL'), _gate('AUTH-ADMIT'), _gate('G0')], [_event()]), ([_gate('IMPL'), _gate('AUTH-ADMIT'), _gate('PF')], [_event()]), ([_gate('IMPL'), _gate('AUTH-ADMIT', stage='S2')], [_event()]), ([_gate('IMPL'), _gate('AUTH-ADMIT', scope='model')], [_event()]), ([_gate('IMPL'), _gate('AUTH-ADMIT')], [_event(), _event()]), ([_gate('IMPL'), _gate('AUTH-ADMIT')], [_event('S2')]), ([_gate('IMPL'), _gate('AUTH-ADMIT')], [_event(), _event(event='COMPLETED')]), ([_gate('IMPL'), _jl(foreign='c2-v1')], [_event()])], ids=['extra-G0', 'extra-PF', 'other-stage', 'scope', 'two-started', 'started-S2', 'completed', 'foreign'])
- **test `test_later_stage_accepted_prefix_plus_own_lines`** [L383-393]: `def test_later_stage_accepted_prefix_plus_own_lines(tmp_path)`

