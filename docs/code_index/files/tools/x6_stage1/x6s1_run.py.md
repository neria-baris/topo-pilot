# `tools/x6_stage1/x6s1_run.py`

- Source: [tools/x6_stage1/x6s1_run.py](../../../../../tools/x6_stage1/x6s1_run.py)
- Kind: python
- Lines: 563

## Module docstring

> X6S1 run (local): S0 and bindings, NB-STATIC, environment, sealing, lineage, gate and stage
> records, local waves under the repaired D-2a supervisor, RUNTIME-ACCT, TRAIN-EQUIV, the stage
> runner and CLI (X6S1-FROZEN-v1 §4.6, §5.11, §8, §12, §14.5; API.md §11, §13 items 27-28). Gate
> content: x6s1_stage_pre/_post via a lazy import (R-0079-1); no import-time I/O (§13 item 24).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 23, via same directory)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 26, via unique basename)
- `import x6_store` -> [tools/x6_stage0/x6_store.py](../x6_stage0/x6_store.py.md) (line 29, via unique basename)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](x6s1_cloud.py.md) (line 30, via same directory)
- `import x6s1_ingest` -> [tools/x6_stage1/x6s1_ingest.py](x6s1_ingest.py.md) (line 31, via same directory)
- `from d2a_train import D2AStop, Limits, Supervisor, bound_controls, boundary, disk_reason` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 32, via unique basename)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 34, via package root)
- `from process_tree import TrainingProcess` -> [tools/d2a/process_tree.py](../d2a/process_tree.py.md) (line 304, via unique basename) (inside a function)
- `from process_tree import wave_lease` -> [tools/d2a/process_tree.py](../d2a/process_tree.py.md) (line 347, via unique basename) (inside a function)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 390, via unique basename) (inside a function)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 420, via package root) (inside a function)
- `from topo_pilot.contracts import ObservationSet, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 443, via package root) (inside a function)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 444, via package root) (inside a function)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 445, via package root) (inside a function)
- `from topo_pilot.learner import Trainer` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 446, via package root) (inside a function)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 548, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 27)
- `torch` (lines 28)

### Standard library

- `__future__` (lines 7)
- `argparse` (lines 536)
- `dataclasses` (lines 9)
- `hashlib` (lines 10)
- `importlib` (lines 495)
- `io` (lines 11)
- `json` (lines 12)
- `math` (lines 13)
- `os` (lines 14)
- `pathlib` (lines 21)
- `platform` (lines 15)
- `re` (lines 16)
- `shutil` (lines 17)
- `subprocess` (lines 18)
- `sys` (lines 19)
- `time` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 496: `dynamic: 'x6s1_stage_pre' if stage in STAGES[:2] else 'x6s1_stage_post'`

### sys.path additions

- none

## Imported by

- [tests/x6_stage1/test_b_chain_ops.py](../../tests/x6_stage1/test_b_chain_ops.py.md) (line 28, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 29, import)
- [tests/x6_stage1/test_b_nb_s0_ops.py](../../tests/x6_stage1/test_b_nb_s0_ops.py.md) (line 28, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 24, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 26, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 34, import)
- [tools/x6zc/x6zc_guard.py](../x6zc/x6zc_guard.py.md) (line 245, import)
- [tools/x6zc/x6zc_guard.py](../x6zc/x6zc_guard.py.md) (line 251, import)
- [tools/x6zc/x6zc_stage_a.py](../x6zc/x6zc_stage_a.py.md) (line 238, import)
- [tools/x6zc/x6zc_store.py](../x6zc/x6zc_store.py.md) (line 106, import)

## Top-level constants

- `ALLOWLIST`
- `AUTH_FIELDS`
- `FROZEN`
- `GATES`
- `K_ACCT`
- `METER_VALUES`
- `MODULES`
- `PROTECTED`
- `REQUEST`
- `STAGES`
- `STORE_FILES`
- `STUDY_ROWS`
- `VOLATILE_KEYS`
- `_CTX`
- `_FIXED`
- `_TEST_RE`

## Classes and functions

- **function `_sha`** [L74-74]: `def _sha(b: bytes) -> str`
- **function `_cj`** [L75-75]: `def _cj(obj) -> bytes`
- **function `_load`** [L76-76]: `def _load(p)`
- **function `_utc`** [L77-77]: `def _utc() -> str`
- **function `_st`** [L78-78]: `def _st(ok, detail=None) -> dict`
- **function `_norm`** [L79-79]: `def _norm(p) -> str`
- **function `_git`** [L80-82]: `def _git(wt, *args, text=True)`
- **function `_lines`** [L83-83]: `def _lines(wt, *args) -> list`
- **function `_blob`** [L84-84]: `def _blob(wt, head, rel) -> bytes`
- **function `allowlist_ok`** [L87-94]: `def allowlist_ok(lines) -> bool`
- **function `repair_ok`** [L95-111]: `def repair_ok(worktree, head, freeze=None) -> dict` - §8 S0 (iv): P ancestor of R; blobs at H = REPAIR_BLOBS (= FREEZE's); tools/d2a P = H.
- **function `notebook_sha_ok`** [L112-117]: `def notebook_sha_ok(worktree, head, freeze) -> bool`
- **function `seed_fresh`** [L118-126]: `def seed_fresh(seed_maps) -> bool`
- **function `_seed_maps`** [L127-138]: `def _seed_maps(project_root, store) -> list` - §6.2: seed maps and configs of the project's other ArtifactStores (D-2a pattern).
- **function `auth_ok`** [L139-146]: `def auth_ok(store, protocol_sha256) -> bool`
- **function `meter_bind_check`** [L147-151]: `def meter_bind_check(path, expected_sha256, import_dir) -> None`
- **function `dispatch_identities`** [L152-153]: `def dispatch_identities(mailbox, job_id, task_sha256, session, lock_path) -> None`
- **function `store_lineage`** [L154-162]: `def store_lineage(store, accepted=None) -> dict` - §12 item 8: x6_store lineage + static files + earlier accepted outputs (relpath → sha).
- **function `s0_check`** [L163-204]: `def s0_check(worktree, head, store, dispatch, freeze) -> dict`
- **function `nb_static`** [L207-221]: `def nb_static(path) -> dict`
- **function `bootstrap_check`** [L222-228]: `def bootstrap_check(bundle_dir, bundle_sha256) -> str`
- **function `env_local`** [L231-242]: `def env_local() -> dict`
- **function `env_changed`** [L243-245]: `def env_changed(a, b) -> list`
- **function `_strip`** [L246-249]: `def _strip(obj)`
- **function `reports_equal`** [L250-250]: `def reports_equal(a, b) -> bool`
- **function `_released`** [L251-254]: `def _released(store) -> bool`
- **function `study_stop`** [L255-259]: `def study_stop(store, row, stage, reason) -> str`
- **function `seal`** [L260-262]: `def seal(store, name, obj) -> str`
- **function `unseal`** [L263-269]: `def unseal(store, name, sha256) -> dict`
- **function `log_evaluation`** [L270-273]: `def log_evaluation(store, model, kind, stage) -> None` - Write-ahead evaluation log (§12 item 9): appended before any local evaluation.
- **function `evaluations`** [L274-277]: `def evaluations(store, model) -> list`
- **function `retrain_route_ok`** [L278-279]: `def retrain_route_ok(store, model) -> bool`
- **function `write_gate`** [L282-288]: `def write_gate(store, gate, status, values) -> dict`
- **function `write_stage`** [L289-296]: `def write_stage(store, stage, record) -> Path`
- **function `limits`** [L299-302]: `def limits(model_cpu_s=math.inf) -> Limits`
- **function `launch`** [L303-309]: `def launch(args, log_path)`
- **function `supervise`** [L310-343]: `def supervise(children, limits, stage, clock=time.monotonic) -> dict` - Poll every `poll_s` until every child has exited (§4.6, S6); STOP/HOLD at each poll.
- **function `eval_wave`** [L344-361]: `def eval_wave(store, wave_name, names) -> dict` - E3.A: ≤ MAX_CHILDREN `eval-chunk` children under the wave lease; outputs under
- **function `_smoke_root`** [L364-384]: `def _smoke_root(root, smoke, cfg, k) -> dict` - A local C0-shaped root for the chunked trainer with the recipe (cfg, k) on the stored smoke
- **function `_child`** [L385-388]: `def _child(root, max_chunks=None) -> list`
- **function `_job_cpu_s`** [L389-391]: `def _job_cpu_s() -> float`
- **function `runtime_acct`** [L392-411]: `def runtime_acct(scratch, smoke) -> dict` - §4.6 RUNTIME-ACCT items 1-5 (two normal children, one at 5 CPU-s; metered job).
- **class `_RecGen`** [L412-417]
- **method `_RecGen.__init__`** [L413-413]: `def __init__(self, gen)`
- **method `_RecGen.integers`** [L415-417]: `def integers(self, *a, **k)`
- **class `_Seeds`** [L418-427]
- **method `_Seeds.__init__`** [L419-422]: `def __init__(self, master)`
- **method `_Seeds.seed`** [L423-423]: `def seed(self, name, *scope)`
- **method `_Seeds.generator`** [L424-427]: `def generator(self, name, *scope)`
- **function `_diff`** [L428-440]: `def _diff(a, b, path='$') -> list`
- **function `_reference`** [L441-467]: `def _reference(toks, cfg) -> dict` - §4.6 item 1: the unchanged Trainer.fit on CPU with 2 intra-op threads.
- **function `train_equiv`** [L468-491]: `def train_equiv(scratch, smoke) -> dict` - §4.6 TRAIN-EQUIV: chunked training (K = 20, two fresh-process resumes) = Trainer.fit.
- **function `_stage`** [L494-496]: `def _stage(stage)`
- **function `run_stage`** [L497-534]: `def run_stage(stage, store, dispatch) -> dict` - PLAN[stage] (step, fn(ctx), validity) in §8 order after the disk floor and boundary; the
- **function `main`** [L535-559]: `def main(argv=None) -> int`

