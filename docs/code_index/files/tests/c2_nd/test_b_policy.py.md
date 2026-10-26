# `tests/c2_nd/test_b_policy.py`

- Source: [tests/c2_nd/test_b_policy.py](../../../../../tests/c2_nd/test_b_policy.py)
- Kind: python
- Lines: 314

## Module docstring

> Author B, T-POLICY-ND (protocol §3, §6.7, §10.1, §12) and T-SEAL-ND (§6.7 L5, §12 S12);
> API.md §8.3, §9.1, §9.4, §9.6, §14.1. Synthetic stores under pytest's tmp_path only.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 15, via sys.path edit)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 18, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 19, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `nd_driver` (lines 20)
- `numpy` (lines 21)
- `pytest` (lines 22)

### Standard library

- `__future__` (lines 4)
- `hashlib` (lines 6)
- `json` (lines 7)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `ALLOWED`
- `ORDER`
- `RELEASE_ONLY`
- `REPO`

## Classes and functions

- **function `at_gate`** [L36-39]: `def at_gate(gate)`
- **function `status_of`** [L42-43]: `def status_of(exc_info)`
- **function `sha`** [L46-47]: `def sha(path)`
- **function `ctx_for`** [L50-54]: `def ctx_for(store, policy=None, job='0130')`
- **function `gates_file`** [L57-65]: `def gates_file(store, rows)`
- **test `test_gate_order_is_the_protocol_list`** [L69-74]: `def test_gate_order_is_the_protocol_list()`
- **test `test_begin_in_order_and_out_of_order`** [L77-92]: `def test_begin_in_order_and_out_of_order()`
- **test `test_stage_entry_repeats_are_allowed`** [L95-101]: `def test_stage_entry_repeats_are_allowed()`
- **test `test_require_matrix`** [L105-113]: `def test_require_matrix(gate)` decorators: @pytest.mark.parametrize('gate', ORDER)
- **test `test_no_feas_logit_and_no_endpoint_before_t_pre`** [L116-124]: `def test_no_feas_logit_and_no_endpoint_before_t_pre()`
- **test `test_no_write_during_identity_gates`** [L128-132]: `def test_no_write_during_identity_gates(gate)` decorators: @pytest.mark.parametrize('gate', ('X1', 'DX', 'T-PRE'))
- **test `test_require_write_outside_allowed`** [L135-141]: `def test_require_write_outside_allowed()`
- **test `test_dtest_sampling_needs_release_r5`** [L144-167]: `def test_dtest_sampling_needs_release_r5(tmp_path)`
- **function `d_inputs`** [L170-175]: `def d_inputs(n=8)`
- **test `test_d_stream_refuses_the_construction_projector`** [L179-185]: `def test_d_stream_refuses_the_construction_projector(problem)` decorators: @pytest.mark.parametrize('problem', ('construction', 'R'))
- **function `s_sequence`** [L188-194]: `def s_sequence()`
- **test `test_check_sequence`** [L197-205]: `def test_check_sequence(tmp_path)`
- **test `test_releases_carry_pass_fail_only`** [L212-221]: `def test_releases_carry_pass_fail_only(gate)` decorators: @pytest.mark.parametrize('gate', RELEASE_ONLY)
- **test `test_kc_gate_full_statuses`** [L224-236]: `def test_kc_gate_full_statuses()`
- **test `test_kcr_gate_full_statuses`** [L241-254]: `def test_kcr_gate_full_statuses()`
- **test `test_seal_exclusive_and_p1_only`** [L257-274]: `def test_seal_exclusive_and_p1_only(tmp_path)`
- **function `sealed_store`** [L277-283]: `def sealed_store(tmp_path, name)`
- **function `endpoint`** [L286-287]: `def endpoint(fam)`
- **test `test_unseal_needs_every_alive_endpoint`** [L290-300]: `def test_unseal_needs_every_alive_endpoint(tmp_path)`
- **test `test_unseal_after_family_or_study_stop`** [L303-314]: `def test_unseal_after_family_or_study_stop(tmp_path)`

