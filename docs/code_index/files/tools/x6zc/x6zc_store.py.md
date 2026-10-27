# `tools/x6zc/x6zc_store.py`

- Source: [tools/x6zc/x6zc_store.py](../../../../../tools/x6zc/x6zc_store.py)
- Kind: python
- Lines: 312

## Module docstring

> X6ZC store: JSON helpers, exclusive-create records (EXPOSURE, EVALUATIONS, STAGES, rulings),
> the stage-1 store no-write inventory, environment, closure and master checks, the meter binding
> and its template, ledger and pause points, the freeze check (API.md §11.1-§11.3, §20 C-52).

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 18, via same directory)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 106, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 134, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 15)
- `hashlib` (lines 8)
- `json` (lines 9)
- `math` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 16)
- `re` (lines 12)
- `subprocess` (lines 13)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6zc/x6zc_dry.py](x6zc_dry.py.md) (line 25, import)
- [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 22, import)
- [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 252, import)
- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 18, import)
- [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 30, import)
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 31, import)

## Top-level constants

- `BIND_TEMPLATE`
- `ENV_EXEMPT`

## Classes and functions

- **function `_utc`** [L27-27]: `def _utc() -> str`
- **function `_sha`** [L28-28]: `def _sha(b: bytes) -> str`
- **function `_norm`** [L29-29]: `def _norm(p) -> str`
- **function `_js`** [L30-42]: `def _js(v)`
- **function `_cj`** [L43-43]: `def _cj(obj) -> bytes`
- **function `xwrite`** [L46-50]: `def xwrite(path, data: bytes) -> str`
- **function `_append`** [L51-55]: `def _append(path, obj) -> dict`
- **function `_lines`** [L56-59]: `def _lines(path) -> list`
- **function `log_exposure`** [L60-65]: `def log_exposure(store, stage, artifact, expected_sha256, purpose) -> dict`
- **function `guard`** [L66-68]: `def guard(stage, set_name) -> None`
- **function `log_evaluation`** [L69-72]: `def log_evaluation(store, model, kind, stage, set_name) -> dict`
- **function `write_stage`** [L73-78]: `def write_stage(store, stage, record) -> Path`
- **function `write_ruling`** [L79-85]: `def write_ruling(store, rid, check, stage, cause_identified, affects_beta, cause, defect_md=None, setup=False) -> Path`
- **function `rulings`** [L86-88]: `def rulings(store) -> list`
- **function `x6s1_inventory`** [L91-101]: `def x6s1_inventory(store=zc.X6S1_STORE) -> dict`
- **function `inventory_equal`** [L102-103]: `def inventory_equal(a, b) -> bool`
- **function `env_check`** [L105-110]: `def env_check(env) -> dict`
- **function `closure_diff`** [L111-114]: `def closure_diff(worktree=zc.WORKTREE) -> list`
- **function `_hit`** [L115-120]: `def _hit(v, master) -> bool`
- **function `master_fresh`** [L121-135]: `def master_fresh(project_root=zc.PROJECT_ROOT, master=zc.X6ZC_MASTER) -> dict`
- **function `meter_bind_check`** [L136-140]: `def meter_bind_check(path, expected_sha256, import_dir) -> None`
- **function `bind_template`** [L281-286]: `def bind_template(out, session=None, store=zc.STORE, worktree=zc.WORKTREE) -> str` - Writes the store-local binding (exclusive create); `session` is ignored (C-53: the worker
- **function `ledger_cpu`** [L287-289]: `def ledger_cpu(store) -> float`
- **function `pause_check`** [L290-300]: `def pause_check(boundary, cumulative_s, stage_s, n=None) -> dict`
- **function `_head`** [L302-304]: `def _head() -> str`
- **function `_frozen`** [L305-312]: `def _frozen(store) -> dict`

