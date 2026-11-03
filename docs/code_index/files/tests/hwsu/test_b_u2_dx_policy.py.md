# `tests/hwsu/test_b_u2_dx_policy.py`

- Source: [tests/hwsu/test_b_u2_dx_policy.py](../../../../../tests/hwsu/test_b_u2_dx_policy.py)
- Kind: python
- Lines: 207

## Module docstring

> Author B (job 0223, phase 2): the logit policy and the M0 mirror (API_U2 1.3-1.4; protocol 2.10,
> 6 rows 11-12). Synthetic: a float64 TransformerLM (4 layers, d_model 128, random init, a few
> rows), no checkpoint, no store. x1_gate's input layout is not fixed by API_U2 (see AUTHORSHIP).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 17, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 18, via unique basename)
- `from topo_pilot.learner import ModelConfig, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 120, via package root) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 142, via unique basename) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 157, via unique basename) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 168, via unique basename) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 176, via unique basename) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 184, via unique basename) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 195, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)

### Standard library

- `__future__` (lines 5)
- `importlib` (lines 7)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 26: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 27: `hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](../../tools/hwsu/u2/hwsu_model.py.md)

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `BIND`
- `J`
- `MODEL`
- `REPO`

## Classes and functions

- **function `_m`** [L25-27]: `def _m()`
- **function `_fail`** [L30-33]: `def _fail(fn, *a, **k)`
- **test `test_gate_order_and_allowed_kinds`** [L37-42]: `def test_gate_order_and_allowed_kinds()`
- **test `test_policy_refuses_unknown_gate`** [L46-48]: `def test_policy_refuses_unknown_gate()`
- **test `test_policy_refuses_out_of_order_gate_and_nested_begin`** [L51-60]: `def test_policy_refuses_out_of_order_gate_and_nested_begin()`
- **test `test_require_allows_only_the_listed_gates`** [L67-76]: `def test_require_allows_only_the_listed_gates(kind, ok, bad)` decorators: @pytest.mark.parametrize('kind,ok,bad', [('basis', ['BASIS'], ['M0', 'X1', 'T-PRE']), ('m0', ['M0', 'T-PRE'], ['BASIS', 'X1', 'NUM']), ('x1', ['X1', 'T-PRE'], ['BASIS', 'M0', 'NUM'])])
- **test `test_require_without_a_current_gate_refused`** [L79-84]: `def test_require_without_a_current_gate_refused()`
- **test `test_test_endpoint_needs_t_pre_pass`** [L87-100]: `def test_test_endpoint_needs_t_pre_pass()`
- **test `test_test_endpoint_refused_at_other_gates_even_after_t_pre`** [L103-107]: `def test_test_endpoint_refused_at_other_gates_even_after_t_pre()`
- **test `test_policy_done_argument_does_not_grant_pass_by_itself`** [L110-113]: `def test_policy_done_argument_does_not_grant_pass_by_itself()`
- **function `tiny`** [L118-137]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **function `_run_m0`** [L140-153]: `def _run_m0(tiny, sha='sha-A', ck=None, state='sha-A')`
- **test `test_m0_u_true_identity_passes_when_attainable`** [L156-164]: `def test_m0_u_true_identity_passes_when_attainable(tiny, monkeypatch)`
- **test `test_m0_u_wrong_state_sha_is_model_failure`** [L167-172]: `def test_m0_u_wrong_state_sha_is_model_failure(tiny, monkeypatch)`
- **test `test_m0_u_wrong_checkpoint_id_is_model_failure`** [L175-180]: `def test_m0_u_wrong_checkpoint_id_is_model_failure(tiny, monkeypatch)`
- **test `test_m0_u_only_attainability_failing_is_inconclusive_numerical`** [L183-190]: `def test_m0_u_only_attainability_failing_is_inconclusive_numerical(tiny, monkeypatch)`
- **test `test_m0_u_refused_outside_m0_or_t_pre`** [L193-207]: `def test_m0_u_refused_outside_m0_or_t_pre(tiny)`

