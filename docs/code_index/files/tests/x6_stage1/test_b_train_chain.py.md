# `tests/x6_stage1/test_b_train_chain.py`

- Source: [tests/x6_stage1/test_b_train_chain.py](../../../../../tests/x6_stage1/test_b_train_chain.py)
- Kind: python
- Lines: 400

## Module docstring

> Author B (cloud): T-TRAIN-EQUIV, T-CHAIN (X6S1-FROZEN-v1 §4.3, §4.6, §5.4, §5.5; API.md §5).

## Imports

### Internal (repo files)

- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../../tools/x6_stage1/x6s1_cloud.py.md) (line 26, via sys.path edit)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 27, via sys.path edit)
- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 28, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 30, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 31, via package root)
- `from topo_pilot.learner import TrainConfig, Trainer, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 32, via package root)
- `from topo_pilot.learner.trainer import _materialise` -> [src/topo_pilot/learner/trainer.py](../../src/topo_pilot/learner/trainer.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)
- `torch` (lines 21)

### Standard library

- `__future__` (lines 6)
- `copy` (lines 8)
- `dataclasses` (lines 9)
- `hashlib` (lines 10)
- `io` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 17)
- `subprocess` (lines 14)
- `sys` (lines 15)
- `tarfile` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`

## Imported by

- none

## Top-level constants

- `CLOUD`
- `REPO`

## Classes and functions

- **function `_sha`** [L39-40]: `def _sha(b: bytes) -> str`
- **function `_head`** [L43-48]: `def _head() -> str`
- **function `_tokens`** [L51-52]: `def _tokens(n, seed=7)`
- **function `_cfg`** [L55-56]: `def _cfg(steps, warmup)`
- **function `_ds`** [L59-62]: `def _ds(toks)`
- **function `make_bundle`** [L65-103]: `def make_bundle(root, steps, k, n=256, warmup=2, wrong_stream=False)` - A C0-shaped bundle (§5.3, API §5.1/§5.6) with the ticket's steps/K set by the caller.
- **function `run_child`** [L106-111]: `def run_child(root, max_chunks=None)`
- **function `main_in_process`** [L114-116]: `def main_in_process(root, max_chunks=None)`
- **class `_RecGen`** [L119-132] - Delegates to the real PCG64 generator and records every batch-index array.
- **method `_RecGen.__init__`** [L122-123]: `def __init__(self, gen)`
- **method `_RecGen.bit_generator`** [L126-127]: `def bit_generator(self)` decorators: @property
- **method `_RecGen.integers`** [L129-132]: `def integers(self, *args, **kwargs)`
- **class `_Seeds`** [L135-150] - Test-only delegating SeedTree wrapper exposing the reference generator (RC11).
- **method `_Seeds.__init__`** [L138-140]: `def __init__(self, master)`
- **method `_Seeds.seed`** [L142-143]: `def seed(self, name, *scope)`
- **method `_Seeds.generator`** [L145-150]: `def generator(self, name, *scope)`
- **function `reference`** [L153-173]: `def reference(toks, cfg)` - The unchanged Trainer.fit on CPU with 2 intra-op threads (§4.6 item 1).
- **function `trainer_init`** [L176-179]: `def trainer_init()`
- **function `same`** [L182-195]: `def same(a, b, path='$')`
- **function `_batch_sha`** [L198-199]: `def _batch_sha(arrays)`
- **test `test_chunked_equals_trainer_bitwise_with_two_fresh_process_resumes`** [L207-230]: `def test_chunked_equals_trainer_bitwise_with_two_fresh_process_resumes(tmp_path, steps, k, warmup)` decorators: @pytest.mark.parametrize('steps,k,warmup', [pytest.param(6, 2, 2, id='small'), pytest.param(60, 20, 10, id='equiv-cfg', marks=pytest.mark.slow)])
- **test `test_init_and_batch_order_identical_across_arms`** [L233-242]: `def test_init_and_batch_order_identical_across_arms()`
- **test `test_weights_digest_definition_and_pickling_independence`** [L246-257]: `def test_weights_digest_definition_and_pickling_independence()`
- **test `test_expected_digests_independent`** [L261-270]: `def test_expected_digests_independent(steps, k)` decorators: @pytest.mark.parametrize('steps,k', [(4, 2), (6, 3), (200, 100)])
- **test `test_checkpoint_write_single_buffer_fsync_and_duplicate_refusal`** [L273-285]: `def test_checkpoint_write_single_buffer_fsync_and_duplicate_refusal(tmp_path, monkeypatch)`
- **test `test_checkpoint_not_published_when_reread_differs`** [L288-300]: `def test_checkpoint_not_published_when_reread_differs(tmp_path, monkeypatch)`
- **test `test_json_atomic_canonical_and_exclusive`** [L303-310]: `def test_json_atomic_canonical_and_exclusive(tmp_path)`
- **function `_marker`** [L314-318]: `def _marker(mdir, recs)`
- **test `test_resume_restores_state_and_checks_internal_consistency`** [L321-360]: `def test_resume_restores_state_and_checks_internal_consistency(tmp_path)`
- **test `test_cli_resume_marker_and_batch_precheck`** [L363-383]: `def test_cli_resume_marker_and_batch_precheck(tmp_path)`
- **test `test_record_published_only_after_checkpoint_verifies`** [L386-400]: `def test_record_published_only_after_checkpoint_verifies(tmp_path, monkeypatch)`

