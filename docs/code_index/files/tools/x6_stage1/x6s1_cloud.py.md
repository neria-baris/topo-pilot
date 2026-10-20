# `tools/x6_stage1/x6s1_cloud.py`

- Source: [tools/x6_stage1/x6s1_cloud.py](../../../../../tools/x6_stage1/x6s1_cloud.py)
- Kind: python
- Lines: 540

## Module docstring

> X6S1 cloud (leaf; Colab and local): bundle check, environment and session records, the chunked
> Trainer-equivalent loop, checkpoint/record I/O, chain discovery, quarantine, run_wave, finalise and
> the six notebook cells (X6S1-FROZEN-v1 §4.3, §5.3-§5.11; API.md §5, §12). Imports only the
> standard library, numpy, torch and topo_pilot; no sys.path edit. Import performs no I/O.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 27, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 28, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 29, via package root)
- `from topo_pilot.learner.trainer import WarmupCosine, _materialise, lm_loss` -> [src/topo_pilot/learner/trainer.py](../../src/topo_pilot/learner/trainer.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 23)
- `torch` (lines 24)

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 9)
- `hashlib` (lines 10)
- `io` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 21)
- `platform` (lines 14)
- `re` (lines 15)
- `subprocess` (lines 16)
- `sys` (lines 17)
- `tarfile` (lines 18)
- `time` (lines 19)
- `uuid` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6_stage1/test_a_eval.py](../../tests/x6_stage1/test_a_eval.py.md) (line 25, import)
- [tests/x6_stage1/test_b_chain_ops.py](../../tests/x6_stage1/test_b_chain_ops.py.md) (line 25, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 26, import)
- [tests/x6_stage1/test_b_nb_s0_ops.py](../../tests/x6_stage1/test_b_nb_s0_ops.py.md) (line 25, import)
- [tests/x6_stage1/test_b_train_chain.py](../../tests/x6_stage1/test_b_train_chain.py.md) (line 26, import)
- [tools/x6_stage1/X6S1_colab.ipynb](X6S1_colab.ipynb.md) (line 29, import)
- [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 27, import)
- [tools/x6_stage1/x6s1_ingest.py](x6s1_ingest.py.md) (line 23, import)
- [tools/x6_stage1/x6s1_run.py](x6s1_run.py.md) (line 30, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 21, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 29, import)

## Top-level constants

- `CELL_TEMPLATES`
- `HASH_PLACEHOLDER`
- `MARKER_SCHEMA`
- `_CURRENT_ENV`
- `_ENV_FIELDS`
- `_MODEL_CFG`
- `_TERMINAL`

## Classes and functions

- **class `CloudStop(RuntimeError)`** [L85-86] - The exact `STOP: ...` line (API.md §5.2).
- **function `_req`** [L88-90]: `def _req(ok, stop: str) -> None`
- **function `utc_iso`** [L91-91]: `def utc_iso() -> str`
- **function `utc_stamp`** [L92-92]: `def utc_stamp() -> str`
- **function `sha256_bytes`** [L95-95]: `def sha256_bytes(b) -> str`
- **function `_read`** [L96-98]: `def _read(path) -> bytes`
- **function `sha256_file`** [L99-99]: `def sha256_file(path) -> str`
- **function `sha256_json`** [L100-100]: `def sha256_json(obj) -> str`
- **function `_rjson`** [L101-101]: `def _rjson(path)`
- **function `batch_digest`** [L102-103]: `def batch_digest(arrays) -> str`
- **function `pcg64_state`** [L104-104]: `def pcg64_state(gen) -> dict`
- **function `pcg64_digest`** [L105-105]: `def pcg64_digest(state) -> str`
- **function `weights_digest`** [L106-114]: `def weights_digest(state_dict) -> str`
- **function `generator_from_state`** [L115-118]: `def generator_from_state(state) -> np.random.Generator`
- **function `draw_indices`** [L119-120]: `def draw_indices(gen, n_rows, k, batch=128) -> list`
- **function `expected_digests`** [L121-127]: `def expected_digests(model_master, run_key, n_rows, steps, k, batch=128) -> list`
- **function `_groups`** [L132-136]: `def _groups(model) -> tuple`
- **function `build_optimizer`** [L137-140]: `def build_optimizer(model, train_cfg) -> torch.optim.AdamW`
- **function `build_scheduler`** [L141-142]: `def build_scheduler(opt, cfg)`
- **function `set_precision`** [L143-149]: `def set_precision(device) -> dict`
- **function `fresh_state`** [L150-157]: `def fresh_state(init_sd, model_cfg, train_cfg, gen, device)`
- **function `restore_state`** [L158-164]: `def restore_state(ckpt, model_cfg, train_cfg, device)`
- **function `check_internal`** [L165-174]: `def check_internal(ckpt, record, expected, model_cfg=None) -> list`
- **function `train_chunk`** [L175-190]: `def train_chunk(st, x, y, idx_arrays) -> dict`
- **function `snapshot_bytes`** [L191-197]: `def snapshot_bytes(st) -> bytes`
- **function `load_checkpoint`** [L198-199]: `def load_checkpoint(path, device) -> dict`
- **function `materialise`** [L200-205]: `def materialise(tokens, arm='NA', seed='smoke') -> tuple`
- **function `_publish`** [L208-219]: `def _publish(target: Path, data: bytes, stop: str) -> str`
- **function `write_checkpoint`** [L220-222]: `def write_checkpoint(model_dir, step, data: bytes) -> str`
- **function `write_json_atomic`** [L223-226]: `def write_json_atomic(path, obj) -> str`
- **function `record_sha`** [L227-228]: `def record_sha(rec) -> str`
- **function `make_record`** [L229-239]: `def make_record(model, step, file_sha, weights_sha, batch_sha, pcg_state, prev_sha, session_id, device_name, cuda_capability, loss_first, loss_last, loss_finite, wall_s) -> dict`
- **function `valid_record`** [L240-246]: `def valid_record(model_dir, rec) -> bool`
- **function `_parse`** [L247-253]: `def _parse(raw: bytes)`
- **function `_wsha`** [L254-255]: `def _wsha(path) -> str`
- **function `discover`** [L256-282]: `def discover(model_dir, entry, steps, k) -> dict`
- **function `read_marker`** [L283-294]: `def read_marker(model_dir)`
- **function `write_marker`** [L295-299]: `def write_marker(model_dir, info) -> dict`
- **function `quarantine`** [L300-311]: `def quarantine(root, model, orphans, utc) -> list`
- **function `_save`** [L312-319]: `def _save(md, st, entry, env, prev, chunk) -> dict`
- **function `_next_chunk`** [L320-326]: `def _next_chunk(entry, ticket, gen, step) -> list` - §5.4 step 6: the next chunk's index arrays, drawn from a copy and checked before use.
- **function `train_chunked`** [L327-382]: `def train_chunked(root, entry, ticket, env, device, max_chunks=None, log=print, _reenter=True)`
- **function `executed_sources`** [L385-389]: `def executed_sources() -> list`
- **function `normalise_source`** [L390-392]: `def normalise_source(src) -> str`
- **function `_cells`** [L393-393]: `def _cells() -> list`
- **function `_tar_commit`** [L394-396]: `def _tar_commit(path) -> str`
- **function `verify_bundle`** [L397-412]: `def verify_bundle(root, bundle_sha256) -> dict`
- **function `environment`** [L413-432]: `def environment(root, bundle) -> dict`
- **function `_sessions`** [L433-433]: `def _sessions(root, kind) -> list`
- **function `_model_status`** [L434-437]: `def _model_status(root, entry, ticket) -> tuple`
- **function `precheck`** [L438-455]: `def precheck(root, env) -> dict`
- **function `_start_of`** [L456-457]: `def _start_of(root, sid) -> list`
- **function `_write_start`** [L458-467]: `def _write_start(root, env, cells) -> list` - The session-start record (§5.6): by cell 5, or by cell 6 if cell 5 never ran (item 26).
- **function `run_wave`** [L468-474]: `def run_wave(root, env) -> dict`
- **function `finalise`** [L475-516]: `def finalise(root, env=None) -> dict`
- **function `main`** [L517-537]: `def main(argv=None) -> int`

