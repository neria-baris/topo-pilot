# `tests/x6_stage1/test_b_ingest_bundle.py`

- Source: [tests/x6_stage1/test_b_ingest_bundle.py](../../../../../tests/x6_stage1/test_b_ingest_bundle.py)
- Kind: python
- Lines: 399

## Module docstring

> Author B: T-INGEST, T-ENV normalisation, T-S0 auth_ok (protocol §5.6-§5.8, §8 row 0b, §12;
> API.md §5.6, §5.7, §6, §11.1). A tiny CPU lineage (ticket steps 2, K 1) stands in for a Colab
> export snapshot; its records claim a CUDA device so that the provenance gate can pass.

## Imports

### Internal (repo files)

- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../../tools/x6_stage1/x6s1_cloud.py.md) (line 26, via sys.path edit)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 27, via sys.path edit)
- `import x6s1_ingest` -> [tools/x6_stage1/x6s1_ingest.py](../../tools/x6_stage1/x6s1_ingest.py.md) (line 28, via sys.path edit)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../../tools/x6_stage1/x6s1_run.py.md) (line 29, via sys.path edit)
- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 32, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 33, via package root)
- `from topo_pilot.learner import TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 34, via package root)
- `from topo_pilot.learner.trainer import _materialise` -> [src/topo_pilot/learner/trainer.py](../../src/topo_pilot/learner/trainer.py.md) (line 35, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)
- `torch` (lines 21)

### Standard library

- `__future__` (lines 4)
- `copy` (lines 6)
- `dataclasses` (lines 7)
- `hashlib` (lines 8)
- `io` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 17)
- `platform` (lines 11)
- `shutil` (lines 12)
- `subprocess` (lines 13)
- `sys` (lines 14)
- `tarfile` (lines 15)
- `time` (lines 16)

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

- `AUTH`
- `AUTH_EDITS`
- `REPO`

## Classes and functions

- **function `_sha`** [L43-43]: `def _sha(b)`
- **function `_fsha`** [L44-44]: `def _fsha(p)`
- **function `_cj`** [L45-45]: `def _cj(obj)`
- **function `_put`** [L48-51]: `def _put(root, rel, obj)`
- **function `_head`** [L54-55]: `def _head()`
- **function `_ckpt_edit`** [L58-63]: `def _ckpt_edit(path)`
- **function `build_snapshot`** [L66-163]: `def build_snapshot(root)` - §5.3 bundle files + §5.5 chain + §5.6 session records and manifest (API §5.1 layout).
- **function `base`** [L167-168]: `def base(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `snap`** [L172-175]: `def snap(base, tmp_path)` decorators: @pytest.fixture
- **function `_remanifest`** [L178-178]: `def _remanifest(s)`
- **test `test_four_gates_pass_on_consistent_snapshot`** [L182-188]: `def test_four_gates_pass_on_consistent_snapshot(snap)`
- **test `test_weights_hash_transfer_failures`** [L192-206]: `def test_weights_hash_transfer_failures(snap, case)` decorators: @pytest.mark.parametrize('case', ['byte', 'relayed', 'missing', 'extra'])
- **test `test_weights_hash_honours_explicit_exclusions`** [L209-216]: `def test_weights_hash_honours_explicit_exclusions(snap)`
- **test `test_weights_digest_mismatch_fails_even_with_redownload`** [L219-231]: `def test_weights_digest_mismatch_fails_even_with_redownload(snap)`
- **test `test_cloud_prov_failures`** [L237-259]: `def test_cloud_prov_failures(snap, case)` decorators: @pytest.mark.parametrize('case', ['missing_field', 'commit', 'protocol', 'bundle', 'edited_cell', 'extra_code', 'no_cuda', 'tf32', 'nondeterministic', 'session_field'])
- **test `test_data_id_failures`** [L264-273]: `def test_data_id_failures(snap, case)` decorators: @pytest.mark.parametrize('case', ['init', 'batch', 'pcg', 'data', 'tokens'])
- **function `_relink`** [L276-283]: `def _relink(chain, prev='e' * 64)`
- **test `test_train_complete_statuses`** [L290-314]: `def test_train_complete_statuses(case, status)` decorators: @pytest.mark.parametrize('case,status', [('full', 'PASS'), ('prefix', 'HOLD:CLOUD_INCOMPLETE'), ('gap', CHAIN), ('duplicate', CHAIN), ('badlink', CHAIN), ('order', CHAIN), ('marker', 'INVALID:NONFINITE'), ('bad_marker', 'HOLD:MARKER')])
- **test `test_admission_lock_before_import_blocks_retrain_and_restoration_rules`** [L317-344]: `def test_admission_lock_before_import_blocks_retrain_and_restoration_rules(snap, tmp_path, monkeypatch)`
- **test `test_refinalisation_creates_new_snapshot_and_preserves_earlier`** [L347-365]: `def test_refinalisation_creates_new_snapshot_and_preserves_earlier(snap)`
- **test `test_executed_cell_normalisation`** [L377-380]: `def test_executed_cell_normalisation(raw, want)` decorators: @pytest.mark.parametrize('raw,want', [('a = 1  \r\nb = 2\t\n\n\n', 'a = 1\nb = 2'), (T2.replace(sc.HASH_PLACEHOLDER, HEX), T2), (T2.replace(sc.HASH_PLACEHOLDER, HEX.upper()).replace('\n', '\r\n') + '\n', T2), ('BUNDLE_SHA256 = "' + 'g' * 64 + '"', 'BUNDLE_SHA256 = "' + 'g' * 64 + '"'), ('BUNDLE_SHA256 = "' + HEX[:63] + '"', 'BUNDLE_SHA256 = "' + HEX[:63] + '"')])
- **test `test_auth_ok`** [L393-399]: `def test_auth_ok(tmp_path, case)` decorators: @pytest.mark.parametrize('case', ['valid', *AUTH_EDITS, 'missing', 'absent', 'garbage', 'array'])

