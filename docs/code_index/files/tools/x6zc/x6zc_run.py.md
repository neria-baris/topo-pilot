# `tools/x6zc/x6zc_run.py`

- Source: [tools/x6zc/x6zc_run.py](../../../../../tools/x6zc/x6zc_run.py)
- Kind: python
- Lines: 989

## Module docstring

> X6ZC run: store records (exclusive create, EXPOSURE, EVALUATIONS, STAGES), the stage-1 store
> no-write inventory, environment, closure and master checks, the meter binding and its template,
> ledger and pause points, the pure Stage-C pipeline, the report and its schema, the stage-0 dry
> run, stages A, B and C with model chunk children, and the CLI (X6ZC-DESIGN-v1 §4-§15; API.md §11,
> §15, §20). Torch-heavy X6S1 modules are imported lazily inside the functions that need them.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 23, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 27, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 28, via unique basename)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 29, via same directory)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 113, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 139, via unique basename) (inside a function)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 304, via unique basename) (inside a function)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 313, via unique basename) (inside a function)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../x6_stage1/x6s1_cloud.py.md) (line 331, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 332, via unique basename) (inside a function)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 334, via package root) (inside a function)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../x6_stage1/x6s1_stats.py.md) (line 504, via unique basename) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 554, via unique basename) (inside a function)
- `import x6s1_decide` -> [tools/x6_stage1/x6s1_decide.py](../x6_stage1/x6s1_decide.py.md) (line 588, via unique basename) (inside a function)
- `import x6s1_stage_pre` -> [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 629, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 704, via unique basename) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 705, via unique basename) (inside a function)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 759, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 26)
- `torch` (lines 330)

### Standard library

- `__future__` (lines 8)
- `argparse` (lines 10)
- `fractions` (lines 20)
- `hashlib` (lines 11)
- `io` (lines 12)
- `json` (lines 13)
- `math` (lines 14)
- `os` (lines 15)
- `pathlib` (lines 21)
- `re` (lines 16)
- `subprocess` (lines 17)
- `sys` (lines 18)
- `time` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6zc/test_x6zc_decide.py](../../tests/x6zc/test_x6zc_decide.py.md) (line 18, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 20, import)

## Top-level constants

- `BIND_TEMPLATE`
- `CELL_KEYS`
- `TOP`
- `_A2_ROW`
- `_OUTS`

## Classes and functions

- **function `_utc`** [L35-35]: `def _utc() -> str`
- **function `_sha`** [L36-36]: `def _sha(b: bytes) -> str`
- **function `_norm`** [L37-37]: `def _norm(p) -> str`
- **function `_js`** [L38-50]: `def _js(v)`
- **function `_cj`** [L51-51]: `def _cj(obj) -> bytes`
- **function `xwrite`** [L54-58]: `def xwrite(path, data: bytes) -> str`
- **function `_append`** [L59-63]: `def _append(path, obj) -> dict`
- **function `_lines`** [L64-67]: `def _lines(path) -> list`
- **function `log_exposure`** [L68-73]: `def log_exposure(store, stage, artifact, expected_sha256, purpose) -> dict`
- **function `guard`** [L74-76]: `def guard(stage, set_name) -> None`
- **function `log_evaluation`** [L77-80]: `def log_evaluation(store, model, kind, stage, set_name) -> dict`
- **function `write_stage`** [L81-86]: `def write_stage(store, stage, record) -> Path`
- **function `write_ruling`** [L87-93]: `def write_ruling(store, rid, check, stage, cause_identified, affects_beta, cause, defect_md=None, setup=False) -> Path`
- **function `rulings`** [L94-96]: `def rulings(store) -> list`
- **function `x6s1_inventory`** [L99-109]: `def x6s1_inventory(store=zc.X6S1_STORE) -> dict`
- **function `inventory_equal`** [L110-111]: `def inventory_equal(a, b) -> bool`
- **function `env_check`** [L112-116]: `def env_check(env) -> dict`
- **function `closure_diff`** [L117-120]: `def closure_diff(worktree=zc.WORKTREE) -> list`
- **function `_hit`** [L121-126]: `def _hit(v, master) -> bool`
- **function `master_fresh`** [L127-140]: `def master_fresh(project_root=zc.PROJECT_ROOT, master=zc.X6ZC_MASTER) -> dict`
- **function `meter_bind_check`** [L141-145]: `def meter_bind_check(path, expected_sha256, import_dir) -> None`
- **function `bind_template`** [L160-162]: `def bind_template(out, session, store=zc.STORE, import_dir=zc.METER_IMPORT_DIR) -> str`
- **function `ledger_cpu`** [L163-165]: `def ledger_cpu(store) -> float`
- **function `pause_check`** [L166-176]: `def pause_check(boundary, cumulative_s, stage_s, n=None) -> dict`
- **function `predict_variants`** [L179-182]: `def predict_variants(pred, arrays_by_family) -> dict`
- **function `stage_c_statistics`** [L183-220]: `def stage_c_statistics(outputs, arrays_by_family, qstar_fn, gen, drop_pairs=None, drop_clusters=None) -> dict`
- **function `_f4`** [L221-221]: `def _f4(x) -> str`
- **function `licence_values`** [L222-245]: `def licence_values(cell, stats, dc, ev) -> dict`
- **function `decide_report`** [L246-255]: `def decide_report(stats, ev_base, census=None) -> dict`
- **function `_outcome_ok`** [L264-266]: `def _outcome_ok(o) -> bool`
- **function `validate_report`** [L267-281]: `def validate_report(report) -> list`
- **class `Planted`** [L284-302] - p = Z + sum_k f_k(prefix) (P_k - Z), Z = q*_ZC, P_k a SyntheticPredictor selected by
- **method `Planted.__init__`** [L288-289]: `def __init__(self, name, comps, paths)`
- **method `Planted.__call__`** [L290-299]: `def __call__(self, tokens, t)`
- **method `Planted._info`** [L300-302]: `def _info(self, row, t)`
- **function `sd_parse`** [L303-305]: `def sd_parse(row) -> dict`
- **function `_jitter`** [L306-311]: `def _jitter(prefixes, fid) -> dict`
- **function `_pool`** [L312-320]: `def _pool(gen, rows=4096) -> np.ndarray`
- **function `_ev`** [L321-327]: `def _ev(**kw) -> dict`
- **function `dry`** [L328-528]: `def dry(scratch=zc.DRY_STORE, fixtures=None, faults=None) -> dict` - Stage 0: every CONTRACT dry-run fixture through the pipeline on synthetic data only.
- **function `se_qstar`** [L529-529]: `def se_qstar(tok, t)`
- **function `_x6`** [L532-532]: `def _x6(rel) -> Path`
- **function `_payload`** [L533-538]: `def _payload(store, stage, rel, sha, purpose) -> bytes`
- **function `_npz`** [L539-541]: `def _npz(data) -> dict`
- **function `_head`** [L542-544]: `def _head() -> str`
- **function `_dirs`** [L545-549]: `def _dirs(store, stage) -> list`
- **function `_record`** [L550-552]: `def _record(store, stage) -> tuple`
- **function `_begin`** [L553-564]: `def _begin(store, stage) -> dict`
- **function `_finish`** [L565-579]: `def _finish(store, ctx, stop=None, n=None) -> int`
- **function `_find`** [L580-583]: `def _find(obj, key) -> list`
- **function `_passes`** [L584-586]: `def _passes(obj, name) -> bool`
- **function `a1_check`** [L587-616]: `def a1_check(closure) -> dict`
- **function `a2_check`** [L618-627]: `def a2_check() -> dict`
- **function `stage_a`** [L628-686]: `def stage_a(store=zc.STORE) -> int`
- **function `_cache`** [L687-690]: `def _cache(store) -> zc.QStarCache`
- **function `_spec`** [L691-696]: `def _spec(m) -> tuple`
- **function `_predictor`** [L697-699]: `def _predictor(m) -> se.ModelPredictor`
- **class `_Memo`** [L700-702]
- **method `_Memo.__init__`** [L701-701]: `def __init__(self, rows)`
- **method `_Memo.__call__`** [L702-702]: `def __call__(self, tokens, t)`
- **function `_children`** [L703-716]: `def _children(store, stage, names, out_dir) -> dict`
- **function `chunk`** [L717-739]: `def chunk(stage, model, out, store=zc.STORE) -> int`
- **function `_terms`** [L740-747]: `def _terms(pa, pb, A, key, qfn) -> dict`
- **function `_boot`** [L748-756]: `def _boot(terms_by_key, gen, P) -> dict`
- **function `_arm`** [L757-757]: `def _arm(m) -> str`
- **function `stage_b`** [L758-849]: `def stage_b(store=zc.STORE) -> int`
- **function `_ev_base`** [L850-858]: `def _ev_base(store) -> dict`
- **function `stage_c`** [L859-935]: `def stage_c(store=zc.STORE) -> int`
- **function `_frozen`** [L938-945]: `def _frozen(store) -> dict`
- **function `main`** [L946-987]: `def main(argv=None) -> int`

