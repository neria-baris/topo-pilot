# `tests/c2_readout/test_b_patch.py`

- Source: [tests/c2_readout/test_b_patch.py](../../../../../tests/c2_readout/test_b_patch.py)
- Kind: python
- Lines: 375

## Module docstring

> Author B (job 0101): T-PATCH and T-X1 (C2-FROZEN-v2 §13.3; §2.1, §2.7, §7 rows 9 and 17).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 24, via sys.path edit)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](../../tools/c2_readout/c2_driver.py.md) (line 25, via sys.path edit)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 26, via sys.path edit)
- `from topo_pilot.learner import ModelConfig, TransformerLM, forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 28, via package root)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 320, via sys.path edit)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)
- `torch` (lines 18, 19)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 13)
- `hashlib` (lines 317)
- `inspect` (lines 10)
- `json` (lines 318)
- `math` (lines 11)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `REPO`
- `SITES`
- `_STAMP`
- `_V2`

## Classes and functions

- **class `_Policy(cdr.LogitPolicy)`** [L34-45] - Permissive policy stub built from cdr.LogitPolicy: records kinds, refuses nothing.
- **method `_Policy.__init__`** [L37-39]: `def __init__(self)`
- **method `_Policy.require`** [L41-42]: `def require(self, kind)`
- **method `_Policy.require_write`** [L44-45]: `def require_write(self, kind)`
- **function `_tiny_model`** [L48-60]: `def _tiny_model()`
- **function `_inputs`** [L63-66]: `def _inputs(seed, n=N_ROWS)`
- **function `tiny`** [L70-80]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **function `_scale`** [L83-84]: `def _scale(z)`
- **function `_fwp`** [L87-90]: `def _fwp(model, inputs, site, rep)`
- **function `_no_arrays`** [L93-100]: `def _no_arrays(obj) -> bool`
- **test `test_activations3_are_the_three_hooks_at_position_32`** [L104-109]: `def test_activations3_are_the_three_hooks_at_position_32(tiny)`
- **test `test_identity_patch_bitwise_at_three_sites`** [L112-122]: `def test_identity_patch_bitwise_at_three_sites(tiny)`
- **test `test_identity_patch_detects_a_one_entry_change`** [L125-129]: `def test_identity_patch_detects_a_one_entry_change(tiny)`
- **test `test_ln_final_out_patch_is_linear_and_input_independent`** [L132-147]: `def test_ln_final_out_patch_is_linear_and_input_independent(tiny)`
- **function `_attend`** [L150-156]: `def _attend(q, k, v, n_heads)`
- **function `_block3_manual`** [L159-168]: `def _block3_manual(model, x, kv_from)` - Block 3 by hand: queries from x; keys/values from kv_from at position 32 only.
- **test `test_resid_post_2_prefix_unchanged_and_own_patched_key_value`** [L171-186]: `def test_resid_post_2_prefix_unchanged_and_own_patched_key_value(tiny)`
- **function `readout`** [L191-197]: `def readout(tiny)` decorators: @pytest.fixture(scope='module')
- **function `_closed`** [L200-201]: `def _closed(basis, y)`
- **function `_arms`** [L204-208]: `def _arms(tiny, ro, z_nat=None, y_int=None)`
- **test `test_x1_signature_has_no_store_access`** [L211-212]: `def test_x1_signature_has_no_store_access()`
- **test `test_x1_closed_form_equals_patch_path_and_returns_diagnostics_only`** [L215-231]: `def test_x1_closed_form_equals_patch_path_and_returns_diagnostics_only(tiny, readout)`
- **function `_defect`** [L234-244]: `def _defect(kind, tiny, ro)`
- **test `test_x1_injected_defect_fails_by_1e6_tau`** [L248-258]: `def test_x1_injected_defect_fails_by_1e6_tau(tiny, readout, kind)` decorators: @pytest.mark.parametrize('kind', ['beta', 'Q0', 'index'])
- **test `test_x1_fail_closed_on_one_row_and_tolerance_is_relative`** [L261-270]: `def test_x1_fail_closed_on_one_row_and_tolerance_is_relative(tiny, readout)`
- **test `test_x1_non_finite_replacement_is_fail_closed`** [L273-281]: `def test_x1_non_finite_replacement_is_fail_closed(tiny, readout)`
- **test `test_readout_identity_rule`** [L284-291]: `def test_readout_identity_rule(tiny, readout)`
- **test `test_kappa_x1_matches_the_written_formula`** [L294-300]: `def test_kappa_x1_matches_the_written_formula(readout)`
- **test `test_x1_attainability_product_form_exact`** [L303-311]: `def test_x1_attainability_product_form_exact()`
- **function `_jl`** [L326-327]: `def _jl(**rec)`
- **function `_gate`** [L330-333]: `def _gate(gate)`
- **function `_g0_store`** [L336-346]: `def _g0_store(tmp_path)` - An S1 store at G0 time: coordinator files, one STARTED line, IMPL and AUTH-ADMIT.
- **function `_adm`** [L349-350]: `def _adm(store, lin)`
- **test `test_meter_active_lock_admitted_at_s1`** [L353-358]: `def test_meter_active_lock_admitted_at_s1(tmp_path)`
- **test `test_meter_active_lock_near_misses_stay_unrecognised`** [L368-375]: `def test_meter_active_lock_near_misses_stay_unrecognised(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['METER_ACTIVE.lock.bak', 'METER_ACTIVE.json', 'registry/METER_ACTIVE.lock'], ids=['lock-bak', 'json', 'registry-subdir'])

