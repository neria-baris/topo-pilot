# `tools/c2_nd/nd_driver.py`

- Source: [tools/c2_nd/nd_driver.py](../../../../../tools/c2_nd/nd_driver.py)
- Kind: python
- Lines: 398

## Module docstring

> C2ND driver (API.md §9, §14, §15, §20; C2ND-DESIGN-v1 §3, §6.7, §10, §12): gate order, the ND
> LogitPolicy, records, sealing, AUTH and release binding, G0 (i)-(x), the meter check, lazy stage
> dispatch (no stage module at import time) and the CLI. Loaders, caches and lineage records live
> in nd_stage_base (ND-C43) and are re-exported here under their API.md §9 names.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 18, via same directory)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 21, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 22, via unique basename)
- `import nd_data` -> [tools/c2_nd/nd_data.py](nd_data.py.md) (line 23, via same directory)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](nd_registry.py.md) (line 24, via same directory)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 25, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 26, via unique basename)
- `from c1_records import C1GateFailure, classify_exception` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 27, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `argparse` (lines 8)
- `dataclasses` (lines 15)
- `hashlib` (lines 9)
- `importlib` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 16)
- `subprocess` (lines 12)
- `sys` (lines 13)
- `zipfile` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 356: `nd_dry` -> [tools/c2_nd/nd_dry.py](nd_dry.py.md)
- `import_module` line 357: `dynamic: STAGE_MODULE[stage]`

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_decoy_maths.py](../../tests/c2_nd/test_a_decoy_maths.py.md) (line 27, import)
- [tests/c2_nd/test_b_decoy_model.py](../../tests/c2_nd/test_b_decoy_model.py.md) (line 28, import)
- [tests/c2_nd/test_b_lineage.py](../../tests/c2_nd/test_b_lineage.py.md) (line 22, import)
- [tests/c2_nd/test_b_policy.py](../../tests/c2_nd/test_b_policy.py.md) (line 20, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 29, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 25, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 25, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 19, import)

## Top-level constants

- `ALLOWED`
- `GATE_ORDER`
- `GATE_STAGE`
- `META`
- `PREREQ`
- `STAGE_MODULE`
- `STATE_SHA`
- `_ST`

## Classes and functions

- **class `LogitPolicy`** [L63-91]
- **method `LogitPolicy.__init__`** [L64-65]: `def __init__(self, done=())`
- **method `LogitPolicy.begin`** [L67-74]: `def begin(self, gate) -> None`
- **method `LogitPolicy.end`** [L76-77]: `def end(self, gate) -> None`
- **method `LogitPolicy.require`** [L79-82]: `def require(self, kind) -> None`
- **method `LogitPolicy.require_write`** [L84-86]: `def require_write(self, kind) -> None`
- **method `LogitPolicy.require_release`** [L88-91]: `def require_release(self, gate, values) -> None`
- **function `require_release`** [L94-95]: `def require_release(policy, gate, values) -> None`
- **function `check_sequence`** [L98-107]: `def check_sequence(gates_jsonl) -> bool`
- **class `Ctx`** [L111-121] decorators: @dataclass
- **function `run_gate`** [L125-144]: `def run_gate(ctx, gate, fn, scope, model=None, family=None, problem=None) -> dict` - One GATES.jsonl line per record (C2 API §19.2) plus the key `decoy`; a release-only gate
- **function `seal`** [L148-159]: `def seal(ctx, name, arrays) -> str`
- **function `unseal`** [L162-172]: `def unseal(ctx, name, sha256) -> dict`
- **function `auth_ok`** [L176-184]: `def auth_ok(store, name='AUTH.json') -> bool`
- **function `is_dry_store`** [L187-191]: `def is_dry_store(store) -> bool` - A FREEZE-free scratch store under SCRATCH_ROOT holding a valid AUTH_IMPL.json (§10.1).
- **function `binding_path`** [L194-196]: `def binding_path(ctx) -> Path` - FREEZE.json; in a dry-run store DRY.json (H, contract and meter bindings, ND-C42).
- **function `_release_why`** [L199-210]: `def _release_why(ctx, stage, r) -> str`
- **function `release_ok`** [L213-220]: `def release_ok(ctx, stage) -> dict`
- **function `meter_bind_check`** [L223-228]: `def meter_bind_check(path, expected_sha256, import_dir) -> None`
- **function `_git`** [L232-233]: `def _git(wt, *args) -> bytes`
- **function `_blobs_ok`** [L236-247]: `def _blobs_ok(wt, head) -> bool`
- **function `_c2_store_ok`** [L250-265]: `def _c2_store_ok(ctx) -> bool` - (iv): every C2 store file re-hashes; 0115.accepted names the 0115 manifest; the FIT/DEC
- **function `_item`** [L268-272]: `def _item(fn) -> dict`
- **function `g0`** [L275-318]: `def g0(ctx, stage=None) -> dict` - Items "i"-"x", never raising; FAIL_TECHNICAL/LINEAGE iff only (vi)-(vii) fail.
- **function `_same`** [L321-322]: `def _same(a, b) -> bool`
- **function `begin_stage`** [L326-341]: `def begin_stage(ctx, stage) -> None`
- **function `complete_stage`** [L344-347]: `def complete_stage(ctx, stage, files) -> list` - sr.complete, then the C2 store re-hash of G0 (iv) at the end of every stage (L7).
- **function `run_stage`** [L350-376]: `def run_stage(stage, ctx) -> dict` - Lazy dispatch (C2 API §19.2): PLAN steps in order, NOT_RUN after a study stop, REPORT
- **function `main`** [L379-394]: `def main(argv=None) -> int`

