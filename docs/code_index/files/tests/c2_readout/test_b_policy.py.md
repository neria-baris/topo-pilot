# `tests/c2_readout/test_b_policy.py`

- Source: [tests/c2_readout/test_b_policy.py](../../../../../tests/c2_readout/test_b_policy.py)
- Kind: python
- Lines: 397

## Module docstring

> Author B (job 0101): T-POLICY (RC-13, NEW-2), T-SEED, T-SIZE, T-METER.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 23, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 24, via sys.path edit)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 25, via sys.path edit)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](../../tools/c2_readout/c2_driver.py.md) (line 26, via sys.path edit)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 14)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `ALLOWED`
- `MODULES`
- `ORDER`
- `PROTO`
- `REFUSED`
- `REPO`
- `SEQ`

## Classes and functions

- **function `_name`** [L44-49]: `def _name(g)`
- **function `_at`** [L52-55]: `def _at(gate)`
- **function `_refused`** [L58-62]: `def _refused(fn, word=None)`
- **test `test_gate_order_equals_protocol_section_7`** [L66-68]: `def test_gate_order_equals_protocol_section_7()`
- **test `test_full_walk_in_order`** [L71-79]: `def test_full_walk_in_order()`
- **test `test_require_table_over_every_gate`** [L83-89]: `def test_require_table_over_every_gate(gate)` decorators: @pytest.mark.parametrize('gate', [g for g in ORDER if g != 'ACCEPT'])
- **test `test_no_fit_logit_outside_m0_and_no_feas_logit`** [L92-97]: `def test_no_fit_logit_outside_m0_and_no_feas_logit()`
- **test `test_test_endpoint_refused_before_t_pre_and_t_pre_model`** [L100-108]: `def test_test_endpoint_refused_before_t_pre_and_t_pre_model()`
- **test `test_x1_and_t_pre_cannot_write_endpoint_arrays`** [L111-118]: `def test_x1_and_t_pre_cannot_write_endpoint_arrays()`
- **test `test_out_of_order_gates_are_refused`** [L121-129]: `def test_out_of_order_gates_are_refused()`
- **test `test_same_gate_again_and_stage_entry_keep_the_position`** [L132-142]: `def test_same_gate_again_and_stage_entry_keep_the_position()`
- **function `_gates_file`** [L145-150]: `def _gates_file(out, seq)`
- **test `test_check_sequence`** [L153-160]: `def test_check_sequence(tmp_path)`
- **function `_ctx`** [L163-165]: `def _ctx(store, pol)`
- **test `test_val_sealed_arrays_refused_before_the_outcome`** [L168-188]: `def test_val_sealed_arrays_refused_before_the_outcome(tmp_path)`
- **test `test_y_donor_preparation_order_new10`** [L191-202]: `def test_y_donor_preparation_order_new10()`
- **function `_sha`** [L209-210]: `def _sha(path)`
- **function `_write`** [L213-216]: `def _write(path, data)`
- **function `_rctx`** [L219-221]: `def _rctx(store)`
- **function `_released`** [L224-232]: `def _released(ctx, stage)`
- **function `_release`** [L235-241]: `def _release(store, ctx, k, **over)`
- **test `test_release_binding_refusals`** [L248-255]: `def test_release_binding_refusals(tmp_path, over)` decorators: @pytest.mark.parametrize('over', [{'job': '0198'}, {'task_sha256': 'b' * 64}, {'head': '2' * 40}, {'protocol_sha256': '0' * 64}, {'freeze_sha256': '0' * 64}, {'stages': ['S2']}, {'schema': 'c2-release-v0'}])
- **test `test_release_r5_must_carry_n_test_and_k`** [L258-263]: `def test_release_r5_must_carry_n_test_and_k(tmp_path)`
- **test `test_k_y_sign_rule`** [L268-274]: `def test_k_y_sign_rule()`
- **test `test_v2_coverage_reasons_and_h4`** [L277-283]: `def test_v2_coverage_reasons_and_h4()`
- **test `test_scope_and_history_streams`** [L287-301]: `def test_scope_and_history_streams()`
- **test `test_sequence_id_codes`** [L314-327]: `def test_sequence_id_codes()`
- **test `test_seed_map_620501_to_620518`** [L330-338]: `def test_seed_map_620501_to_620518()`
- **test `test_haar_frames_streams`** [L342-354]: `def test_haar_frames_streams(j, count, p)` decorators: @pytest.mark.parametrize('j, count, p', [(1729, 2, 127), (3141, 8, 128)])
- **test `test_module_set_and_400_line_limit`** [L363-381]: `def test_module_set_and_400_line_limit()`
- **test `test_meter_binding_sha_and_import_directory`** [L385-397]: `def test_meter_binding_sha_and_import_directory(tmp_path)`

