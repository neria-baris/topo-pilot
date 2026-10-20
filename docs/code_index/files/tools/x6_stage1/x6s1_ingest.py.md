# `tools/x6_stage1/x6s1_ingest.py`

- Source: [tools/x6_stage1/x6s1_ingest.py](../../../../../tools/x6_stage1/x6s1_ingest.py)
- Kind: python
- Lines: 498

## Module docstring

> X6S1 ingest (local): CLOUD-PREP (allowed-class guard, code.tar, tickets, bundles), the four
> integrity gates with execution-record validation, the admission lock, store import, E3.0
> verification, retrain eligibility, LOSS-ECHO and the learning-curve record (X6S1-FROZEN-v1 §4.5,
> §5.3, §5.6-§5.8, §12 items 9-10; API.md §6, §13 item 25). Import performs no I/O.

## Imports

### Internal (repo files)

- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](x6s1_cloud.py.md) (line 23, via same directory)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 24, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 25, via same directory)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.learner import ModelConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 28, via package root)
- `from topo_pilot.learner.trainer import lm_loss` -> [src/topo_pilot/learner/trainer.py](../../src/topo_pilot/learner/trainer.py.md) (line 29, via package root)

### External (third-party)

- `numpy` (lines 21)
- `torch` (lines 22)

### Standard library

- `__future__` (lines 7)
- `copy` (lines 9)
- `dataclasses` (lines 10)
- `io` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 19)
- `re` (lines 14)
- `shutil` (lines 15)
- `subprocess` (lines 16)
- `uuid` (lines 17)
- `warnings` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6_stage1/test_b_chain_ops.py](../../tests/x6_stage1/test_b_chain_ops.py.md) (line 27, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 28, import)
- [tests/x6_stage1/test_b_nb_s0_ops.py](../../tests/x6_stage1/test_b_nb_s0_ops.py.md) (line 27, import)
- [tools/x6_stage1/x6s1_run.py](x6s1_run.py.md) (line 31, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 24, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 31, import)

## Top-level constants

- `ALLOWED`
- `_ALLOWED_RE`
- `_CHUNK_ONLY`
- `_ENTRY_F`
- `_FINAL_F`
- `_FLAGS`
- `_FORBID`
- `_LOCK_KEYS`
- `_MAN_F`
- `_N`
- `_REC_F`
- `_SKIPPED`
- `_START_F`
- `_SUB`
- `_T`

## Classes and functions

- **function `_spec`** [L46-46]: `def _spec(text) -> dict`
- **function `_posix`** [L65-65]: `def _posix(rel) -> str`
- **function `_lo`** [L66-66]: `def _lo(x)`
- **function `_cj`** [L67-67]: `def _cj(obj) -> bytes`
- **function `_gate`** [L68-68]: `def _gate(g, model, status, detail)`
- **function `_xwrite`** [L69-76]: `def _xwrite(path, data: bytes) -> str`
- **function `_typed`** [L77-80]: `def _typed(obj, spec, where) -> list`
- **function `_entry`** [L81-83]: `def _entry(manifest, model)`
- **function `_weights`** [L84-85]: `def _weights(path) -> str`
- **function `_files`** [L88-92]: `def _files(model) -> tuple`
- **function `_names`** [L93-94]: `def _names(wave, models) -> set`
- **function `forbidden`** [L95-98]: `def forbidden(relpath) -> bool`
- **function `allowed_class`** [L99-100]: `def allowed_class(relpath, wave, models) -> bool`
- **function `code_tar`** [L101-105]: `def code_tar(worktree, head, out_path) -> str`
- **function `_tsha`** [L106-106]: `def _tsha() -> list`
- **function `make_ticket`** [L107-129]: `def make_ticket(wave, head, pools, inits) -> dict`
- **function `_sums`** [L130-131]: `def _sums(d: Path, files) -> bytes`
- **function `build_bundle`** [L132-163]: `def build_bundle(wave, out_root, head, worktree, pools, inits, notebook) -> dict`
- **function `check_bundle`** [L164-182]: `def check_bundle(bundle_dir, wave) -> dict`
- **function `find_manifest`** [L185-190]: `def find_manifest(snapshot, manifest_sha256) -> tuple` - (path, manifest) of the export whose MANIFEST.json bytes have the relayed sha256.
- **function `transfer_check`** [L191-206]: `def transfer_check(snapshot, manifest_sha256) -> tuple` - WEIGHTS-HASH (a)-(b) for the whole snapshot: (manifest or None, problems).
- **function `gate_weights_hash`** [L207-226]: `def gate_weights_hash(snapshot, manifest_sha256, model, redownload_ok=False, transfer=None)`
- **function `_compiles`** [L228-237]: `def _compiles(src) -> bool`
- **function `_seq`** [L238-243]: `def _seq(cells, templates)`
- **function `check_execution`** [L244-268]: `def check_execution(records, templates=sc.CELL_TEMPLATES) -> dict`
- **function `_diff`** [L269-269]: `def _diff(rows) -> list`
- **function `_prov`** [L270-322]: `def _prov(root: Path, man, model, frozen) -> list`
- **function `gate_cloud_prov`** [L323-329]: `def gate_cloud_prov(snapshot, manifest, model, frozen) -> dict`
- **function `gate_data_id`** [L330-354]: `def gate_data_id(snapshot, manifest, model, local) -> dict`
- **function `_linked`** [L355-358]: `def _linked(ch, model) -> bool`
- **function `gate_train_complete`** [L359-380]: `def gate_train_complete(manifest, model, steps, k) -> dict`
- **function `ingest`** [L381-405]: `def ingest(snapshot, manifest_sha256, wave, store, local, frozen, redownload_ok=False) -> dict`
- **function `_lock_path`** [L408-408]: `def _lock_path(store, model) -> Path`
- **function `write_admission_lock`** [L409-415]: `def write_admission_lock(store, model, info) -> Path`
- **function `admitted`** [L416-418]: `def admitted(store, model)`
- **function `import_model`** [L419-431]: `def import_model(snapshot, store, wave, model, manifest) -> dict`
- **function `_store_chain`** [L432-440]: `def _store_chain(store, model, wave=None) -> tuple`
- **function `verify_admitted`** [L441-452]: `def verify_admitted(store, model) -> dict`
- **function `retrain_eligible`** [L453-454]: `def retrain_eligible(store, model, evaluations) -> bool`
- **function `refinalised`** [L455-464]: `def refinalised(snapshots, earlier_sha256=None) -> bool`
- **function `_xy`** [L467-469]: `def _xy(tokens) -> tuple`
- **function `_model64`** [L470-471]: `def _model64(d, r)`
- **function `loss_echo`** [L472-485]: `def loss_echo(store, wave, model, pool) -> dict`
- **function `learning_curve`** [L486-498]: `def learning_curve(store, models, dev_pools) -> dict`

