# `tools/c2_readout/c2_driver.py`

- Source: [tools/c2_readout/c2_driver.py](../../../../../tools/c2_readout/c2_driver.py)
- Kind: python
- Lines: 400

## Module docstring

> C2 driver (API.md §12, §19.2-§19.3; C2-FROZEN-v2 §5.7, §7, §11): gate order, LogitPolicy,
> sealing, records, lineage, release, G0, meter check, lazy stage dispatch, CLI. Gate bodies:
> c2_stage_pre (S1-S3), c2_stage_val (S4), c2_stage_post (S5), helpers c2_stage_base (R-0104-1).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 19, via same directory)
- `import c2_data` -> [tools/c2_readout/c2_data.py](c2_data.py.md) (line 22, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 24, via unique basename)
- `from c1_records import C1GateFailure, classify_exception` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 25, via unique basename)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 5)
- `argparse` (lines 7)
- `dataclasses` (lines 14)
- `decimal` (lines 15)
- `fractions` (lines 16)
- `hashlib` (lines 8)
- `importlib` (lines 9)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 17)
- `subprocess` (lines 12)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 361: `dynamic: STAGE_MODULE[stage]`

### sys.path additions

- none

## Imported by

- [tests/c2_readout/test_b_lineage.py](../../tests/c2_readout/test_b_lineage.py.md) (line 25, import)
- [tests/c2_readout/test_b_patch.py](../../tests/c2_readout/test_b_patch.py.md) (line 25, import)
- [tests/c2_readout/test_b_policy.py](../../tests/c2_readout/test_b_policy.py.md) (line 26, import)
- [tests/c2_readout/test_b_registry.py](../../tests/c2_readout/test_b_registry.py.md) (line 24, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 24, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 17, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 17, import)

## Top-level constants

- `ALLOWED`
- `GATE_ORDER`
- `GATE_STAGE`
- `OK`
- `PREREQ`
- `STAGE_ENTRY`
- `STAGE_MODULE`
- `STATE_SHA`
- `_ST`

## Classes and functions

- **class `LogitPolicy`** [L50-73]
- **method `LogitPolicy.__init__`** [L51-52]: `def __init__(self, done=())`
- **method `LogitPolicy.begin`** [L54-61]: `def begin(self, gate) -> None`
- **method `LogitPolicy.end`** [L63-64]: `def end(self, gate) -> None`
- **method `LogitPolicy.require`** [L66-69]: `def require(self, kind) -> None`
- **method `LogitPolicy.require_write`** [L71-73]: `def require_write(self, kind) -> None`
- **function `check_sequence`** [L76-86]: `def check_sequence(gates_jsonl) -> bool`
- **class `Ctx`** [L90-99] decorators: @dataclass
- **function `_js`** [L103-116]: `def _js(v)`
- **function `run_gate`** [L119-134]: `def run_gate(ctx, gate, fn, scope, model=None, family=None, problem=None) -> dict` - One GATES.jsonl line, or one per entry of res["records"] (API.md §19.2); an exception is
- **function `_jr`** [L137-141]: `def _jr(path)`
- **function `_eq`** [L144-145]: `def _eq(a, b) -> bool`
- **function `seal`** [L149-158]: `def seal(ctx, name, arrays) -> str`
- **function `unseal`** [L161-172]: `def unseal(ctx, name, sha256) -> dict`
- **function `auth_ok`** [L175-183]: `def auth_ok(store) -> bool`
- **function `_release_why`** [L186-197]: `def _release_why(ctx, stage, r) -> str`
- **function `release_ok`** [L200-207]: `def release_ok(ctx, stage) -> dict`
- **function `meter_bind_check`** [L210-215]: `def meter_bind_check(path, expected_sha256, import_dir) -> None`
- **function `_blob`** [L219-221]: `def _blob(wt, head, rel) -> str`
- **function `_item`** [L224-228]: `def _item(fn) -> dict`
- **function `g0`** [L231-265]: `def g0(ctx, stage=None) -> dict` - Items (i)-(viii), never raising (E-25); LINEAGE iff only (vi)-(vii) fail (R-0100-2).
- **function `_skip`** [L268-270]: `def _skip(rel) -> bool`
- **function `write_manifest`** [L273-284]: `def write_manifest(ctx, stage) -> Path`
- **function `recognised`** [L287-313]: `def recognised(store) -> dict`
- **function `supersede`** [L316-329]: `def supersede(ctx, job, attempt, paths, ruling) -> Path`
- **function `regen_compare`** [L332-333]: `def regen_compare(ctx, path, archived_sha256) -> bool`
- **function `begin_stage`** [L336-350]: `def begin_stage(ctx, stage) -> None`
- **function `complete_stage`** [L353-354]: `def complete_stage(ctx, stage, files) -> None`
- **function `run_stage`** [L357-379]: `def run_stage(stage, ctx) -> dict` - Lazy dispatch (API.md §19.2-§19.3): PLAN steps in order; NOT_RUN after a study stop.
- **function `main`** [L382-396]: `def main(argv=None) -> int`

