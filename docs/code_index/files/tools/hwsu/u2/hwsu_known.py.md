# `tools/hwsu/u2/hwsu_known.py`

- Source: [tools/hwsu/u2/hwsu_known.py](../../../../../../tools/hwsu/u2/hwsu_known.py)
- Kind: python
- Lines: 400

## Module docstring

> HWSU binding, freeze, S0, authority, attestation, G0U and the known cases KC0-KC6
> (API_U2.md section 2; protocol 4.1, 6 rows KC and 0). Response family only: the KU
> constructions are not implemented (R-0223-1) and fail closed.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 8, via unique basename)
- `import hwsu_bind_u2` -> [tools/hwsu/u2/hwsu_bind_u2.py](hwsu_bind_u2.py.md) (line 9, via same directory)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../hwsu_dry.py.md) (line 10, via unique basename)
- `import hwsu_freeze` -> [tools/hwsu/hwsu_freeze.py](../hwsu_freeze.py.md) (line 11, via unique basename)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 12, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../hwsu_of.py.md) (line 13, via unique basename)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../hwsu_oracle.py.md) (line 14, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 15, via unique basename)
- `import hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 16, via same directory)
- `import hwsu_seed` -> [tools/hwsu/hwsu_seed.py](../hwsu_seed.py.md) (line 17, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 18, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../c1prime/c1_means.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 29, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 30, via unique basename)

### External (third-party)

- `numpy` (lines 28)

### Standard library

- `__future__` (lines 6)
- `fnmatch` (lines 19)
- `importlib` (lines 20)
- `json` (lines 21)
- `os` (lines 22)
- `pathlib` (lines 25)
- `platform` (lines 23)
- `sys` (lines 24)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 316: `hwsu_dry2` -> [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md)

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_freeze.py](../../../tests/hwsu/test_b_u2_freeze.py.md) (line 30, dynamic)
- [tests/hwsu/test_b_u2_hwsd.py](../../../tests/hwsu/test_b_u2_hwsd.py.md) (line 35, dynamic)
- [tests/hwsu/test_b_u2_of_binding.py](../../../tests/hwsu/test_b_u2_of_binding.py.md) (line 29, dynamic)
- [tests/hwsu/test_b_u2_records.py](../../../tests/hwsu/test_b_u2_records.py.md) (line 123, dynamic)
- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 12, import)
- [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md) (line 15, import)
- [tools/hwsu/u2/hwsu_dry2b.py](hwsu_dry2b.py.md) (line 13, import)
- [tools/hwsu/u2/hwsu_e2.py](hwsu_e2.py.md) (line 11, import)
- [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 12, import)

## Top-level constants

- `SHARE_OUTCOME`
- `TEST_PATTERNS`

## Classes and functions

- **function `_C`** [L38-39]: `def _C(contract=None) -> dict`
- **function `of_binding`** [L42-62]: `def of_binding(store=uc.STORE, contract=None) -> dict`
- **function `_tables`** [L66-68]: `def _tables(contract=None) -> dict`
- **function `implementation_files_u`** [L71-76]: `def implementation_files_u(repo, h_exec, contract=None) -> dict`
- **function `freeze_u`** [L79-118]: `def freeze_u(store, repo, h_exec, dru_report, j_u_records, written_by) -> dict`
- **function `verify_freeze_u`** [L121-135]: `def verify_freeze_u(store, repo) -> dict`
- **function `_allowed_s0`** [L138-141]: `def _allowed_s0(status, path, contract=None) -> bool`
- **function `s0_u`** [L144-164]: `def s0_u(store, repo, r_ref=None) -> dict`
- **function `auth_u`** [L168-181]: `def auth_u(store, job, stage, mailbox=uc.MAILBOX, contract=None) -> dict`
- **function `end_obligation_path`** [L184-199]: `def end_obligation_path(end_rec, end_path, root)` - R-0213-1: first existing of <store>/<rel> and <root>/<rel>, bounded to that store.
- **function `_ended_u2`** [L202-222]: `def _ended_u2(rec, f, root, w2_end, w2_sha)`
- **function `w2_attestation_u2`** [L225-253]: `def w2_attestation_u2(root, own=None, w2_end=None, w2_end_sha256=None) -> dict`
- **function `g0_u`** [L257-294]: `def g0_u(out, ctx, stage) -> dict`
- **function `kc0`** [L297-298]: `def kc0(out, ctx) -> dict`
- **function `kc1`** [L301-302]: `def kc1(ctx) -> dict`
- **function `kc2`** [L305-308]: `def kc2(ctx) -> dict`
- **function `_need_pass`** [L311-313]: `def _need_pass(name, r) -> None`
- **function `kc3`** [L314-323]: `def kc3(ctx) -> dict`
- **function `kc4`** [L326-330]: `def kc4(ctx=None) -> dict`
- **function `_bytes`** [L333-334]: `def _bytes(root) -> int`
- **function `kc5`** [L337-357]: `def kc5(out, ctx) -> dict`
- **function `kc6`** [L360-381]: `def kc6(out, ctx) -> dict`
- **function `kc_report`** [L384-394]: `def kc_report(out, records) -> Path`
- **function `ku_cases`** [L397-398]: `def ku_cases(*args, **kwargs)`

