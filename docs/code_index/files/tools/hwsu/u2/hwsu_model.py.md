# `tools/hwsu/u2/hwsu_model.py`

- Source: [tools/hwsu/u2/hwsu_model.py](../../../../../../tools/hwsu/u2/hwsu_model.py)
- Kind: python
- Lines: 299

## Module docstring

> HWSU model part: stage-C loading, readout, response arrays, M0/X1 mirrors, logit policy
> (API_U2.md section 1; protocol 2.3-2.5, 2.10, 3.1, 6 rows 6, 11, 12).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 10, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 11, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../../c1prime/c1_model.py.md) (line 15, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../c1prime/c1_oracle.py.md) (line 16, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../c2_readout/c2_attrib.py.md) (line 17, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../c2_readout/c2_model.py.md) (line 18, via unique basename)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../hwsc/hwsc_gates.py.md) (line 19, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../k4b/k4b_config.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `import topo_pilot.contracts` -> [src/topo_pilot/contracts/__init__.py](../../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)
- `import topo_pilot.contracts.backends` -> [src/topo_pilot/contracts/backends.py](../../../src/topo_pilot/contracts/backends.py.md) (line 24, via package root)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 26, via unique basename)

### External (third-party)

- `numpy` (lines 21)
- `torch` (lines 25)

### Standard library

- `__future__` (lines 8)
- `json` (lines 12)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_binding.py](../../../tests/hwsu/test_b_u2_binding.py.md) (line 29, dynamic)
- [tests/hwsu/test_b_u2_dx_policy.py](../../../tests/hwsu/test_b_u2_dx_policy.py.md) (line 27, dynamic)
- [tools/hwsu/u2/hwsu_decide.py](hwsu_decide.py.md) (line 9, import)
- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 14, import)
- [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md) (line 16, import)
- [tools/hwsu/u2/hwsu_dry2b.py](hwsu_dry2b.py.md) (line 14, import)
- [tools/hwsu/u2/hwsu_e2.py](hwsu_e2.py.md) (line 13, import)
- [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 13, import)
- [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 12, import)
- [tools/hwsu/u2/hwsu_regsrc.py](hwsu_regsrc.py.md) (line 8, import)

## Top-level constants

- `ALLOWED_U`
- `GATE_ORDER_U`
- `TRAIN_KEYS`

## Classes and functions

- **function `_c`** [L36-37]: `def _c(contract=None) -> dict`
- **class `_Pairs(list)`** [L41-42] - Inert object body: nothing is looked up by key until the whitelist is applied.
- **function `_plain`** [L45-50]: `def _plain(x)`
- **function `read_train_record`** [L53-62]: `def read_train_record(path, root=uc.ROOT) -> dict`
- **function `stage_complete_sha`** [L65-73]: `def stage_complete_sha(store, stage, relpath)`
- **function `checkpoint_meta_u`** [L76-83]: `def checkpoint_meta_u(artifact_root, artifact_id) -> dict`
- **function `load_checkpoint_u`** [L86-88]: `def load_checkpoint_u(artifact_root, artifact_id)`
- **function `identity_c`** [L91-112]: `def identity_c(hwsc_store, handoff, contract=None) -> dict`
- **function `charts_identity`** [L115-129]: `def charts_identity(hwsc_store, contract=None) -> dict`
- **function `load_stage_c`** [L132-141]: `def load_stage_c(hwsc_store, ident, contract=None) -> dict`
- **function `named_inputs`** [L145-146]: `def named_inputs(canon32, perm)`
- **function `basis_u`** [L149-150]: `def basis_u(model64) -> dict`
- **function `readout_y`** [L153-157]: `def readout_y(model64, canon32, perm, basis, batch=1024) -> np.ndarray`
- **function `a_full`** [L160-161]: `def a_full(d_named, M, y1, y2) -> np.ndarray`
- **function `response_arrays`** [L164-166]: `def response_arrays(A, G) -> dict`
- **function `row_cross_check`** [L169-171]: `def row_cross_check(q1bar_named, q4bar_named, y1, basis) -> np.ndarray`
- **function `named_d`** [L174-175]: `def named_d(d_canon, perm)`
- **class `UPolicy`** [L179-201]
- **method `UPolicy.__init__`** [L180-181]: `def __init__(self, done=())`
- **method `UPolicy.begin`** [L183-190]: `def begin(self, gate) -> None`
- **method `UPolicy.end`** [L192-193]: `def end(self, gate) -> None`
- **method `UPolicy.mark_pass`** [L195-196]: `def mark_pass(self, gate) -> None`
- **method `UPolicy.require`** [L198-201]: `def require(self, kind) -> None`
- **function `basis_gate`** [L205-224]: `def basis_gate(models, fit_canon, perm_of, policy) -> dict`
- **function `m0_u`** [L227-249]: `def m0_u(model64, sha, ident_j, inputs, acts, z_net, basis, d_canon, perm, policy, contract=None) -> dict`
- **function `m0_gate`** [L252-269]: `def m0_gate(models, ident, val_a1, perm_of, d_canon, policy) -> dict`
- **function `x1_gate`** [L272-292]: `def x1_gate(models, val, perm_of, basis_of, policy) -> dict`
- **function `write_json`** [L295-299]: `def write_json(path, obj) -> Path`

