# `tests/x6_stage1/test_b_nb_s0_ops.py`

- Source: [tests/x6_stage1/test_b_nb_s0_ops.py](../../../../../tests/x6_stage1/test_b_nb_s0_ops.py)
- Kind: python
- Lines: 400

## Module docstring

> Author B: T-BUNDLE (C0 build), T-NB, T-ENV (GPU refusal), T-S0, T-SIZE, T-RESOURCE (protocol
> §4.6, §5.3, §5.11, §8, §13.4, §14). Synthetic fixtures; controls rebound to a tmp mailbox.

## Imports

### Internal (repo files)

- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../../tools/x6_stage1/x6s1_cloud.py.md) (line 25, via sys.path edit)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 26, via sys.path edit)
- `import x6s1_ingest` -> [tools/x6_stage1/x6s1_ingest.py](../../tools/x6_stage1/x6s1_ingest.py.md) (line 27, via sys.path edit)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../../tools/x6_stage1/x6s1_run.py.md) (line 28, via sys.path edit)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 303, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)
- `torch` (lines 20)

### Standard library

- `__future__` (lines 3)
- `ctypes` (lines 361)
- `dataclasses` (lines 5)
- `fractions` (lines 15)
- `hashlib` (lines 6)
- `json` (lines 7)
- `math` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 16)
- `re` (lines 10)
- `shutil` (lines 11)
- `subprocess` (lines 12)
- `sys` (lines 13)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`

## Imported by

- none

## Top-level constants

- `GOOD`
- `NB_EDITS`
- `REPO`

## Classes and functions

- **function `_sha`** [L36-36]: `def _sha(b)`
- **function `_fsha`** [L37-37]: `def _fsha(p)`
- **function `_head`** [L38-38]: `def _head()`
- **function `_git`** [L41-42]: `def _git(*args) -> bytes`
- **function `_api_cells`** [L45-48]: `def _api_cells()`
- **function `_norm`** [L51-53]: `def _norm(src)`
- **function `c0`** [L58-69]: `def c0(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_c0_bundle_sums_ticket_and_chain_parameters`** [L72-102]: `def test_c0_bundle_sums_ticket_and_chain_parameters(c0)`
- **test `test_check_bundle_refuses_forbidden_classes`** [L109-118]: `def test_check_bundle_refuses_forbidden_classes(c0, tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['data/val_NA.npy', 'data/test_NA.npy', 'data/gate_NA.npy', 'data/prefix.npy', 'data/dev_NA_s1.npy', 'sealed/learn.json', 'registry/X6-REG2.json', 'data/train_AB_s1.npy', 'init/init_s3.pt', 'data/latent_states.npy'])
- **test `test_cell_templates_verbatim_from_api`** [L122-127]: `def test_cell_templates_verbatim_from_api()`
- **test `test_notebook_static_independent_and_nb_static`** [L130-138]: `def test_notebook_static_independent_and_nb_static()`
- **test `test_nb_static_refuses`** [L153-159]: `def test_nb_static_refuses(tmp_path, case)` decorators: @pytest.mark.parametrize('case', [*NB_EDITS, 'json'])
- **function `_exec_bootstrap`** [L162-171]: `def _exec_bootstrap(root, sha)`
- **test `test_inline_bootstrap_refuses_modified_bundle`** [L175-186]: `def test_inline_bootstrap_refuses_modified_bundle(tmp_path, case)` decorators: @pytest.mark.parametrize('case', ['ok', 'upper', 'sums', 'tar'])
- **test `test_environment_refuses_cpu_runtime`** [L190-192]: `def test_environment_refuses_cpu_runtime(tmp_path)` decorators: @pytest.mark.skipif(torch.cuda.is_available(), reason='a CUDA device is present')
- **test `test_allowlist`** [L209-210]: `def test_allowlist(extra, ok)` decorators: @pytest.mark.parametrize('extra,ok', [([], True), ([A + 'tests/x6_stage1/test_b_n4.py'], True), ([A + 'tests/x6_stage1/test_b_n4.py', A + 'tests/x6_stage1/test_b_n5.py'], False), ([A + 'tests/x6_stage1/test_b_Bad.py'], False), ([A + 'tests/x6_stage1/conftest.py'], False), (['M\tsrc/topo_pilot/learner/trainer.py'], False), (['M\ttools/x6_stage1/API.md'], False), ([A + 'tools/x6_stage1/x6s1_extra.py'], False), (['D\ttools/d2a/d2a_train.py'], False)])
- **test `test_repair_blob_hashes_at_head`** [L214-218]: `def test_repair_blob_hashes_at_head(path)` decorators: @pytest.mark.parametrize('path', sorted(sd.REPAIR_BLOBS))
- **test `test_repair_ancestry_and_d2a_unchanged`** [L221-225]: `def test_repair_ancestry_and_d2a_unchanged()`
- **test `test_protocol_and_stage0_hash_bindings`** [L228-234]: `def test_protocol_and_stage0_hash_bindings()`
- **function `_report`** [L237-245]: `def _report(edit=None)`
- **test `test_stage0_constants_exact_string_equality`** [L248-257]: `def test_stage0_constants_exact_string_equality()`
- **test `test_notebook_sha_binding`** [L260-264]: `def test_notebook_sha_binding()`
- **test `test_module_set_line_limits_and_test_files`** [L268-280]: `def test_module_set_line_limits_and_test_files()`
- **class `FakeTree`** [L284-299]
- **method `FakeTree.__init__`** [L285-287]: `def __init__(self, cpu=1.0, mem=2 ** 28, polls=2)`
- **method `FakeTree.cpu_s`** [L289-289]: `def cpu_s(self)`
- **method `FakeTree.memory_bytes`** [L290-290]: `def memory_bytes(self)`
- **method `FakeTree.terminate`** [L291-291]: `def terminate(self)`
- **method `FakeTree.close`** [L292-292]: `def close(self)`
- **method `FakeTree.wait`** [L293-293]: `def wait(self, timeout=None)`
- **method `FakeTree.poll`** [L295-299]: `def poll(self)`
- **function `_quiet_controls`** [L302-316]: `def _quiet_controls(monkeypatch, tmp_path, states=())`
- **test `test_limits_and_resource_constants`** [L319-327]: `def test_limits_and_resource_constants()`
- **test `test_supervise_enforces_s6_limits`** [L332-339]: `def test_supervise_enforces_s6_limits(tmp_path, monkeypatch, kind, status)` decorators: @pytest.mark.parametrize('kind,status', [('ok', 'DONE'), ('cpu', 'INCOMPLETE:MODEL_CPU'), ('mem', 'INCOMPLETE:PROCESS_MEMORY')])
- **test `test_supervise_stop_propagates_and_closes_children`** [L342-350]: `def test_supervise_stop_propagates_and_closes_children(tmp_path, monkeypatch)`
- **test `test_supervise_hold_waits_then_continues`** [L353-357]: `def test_supervise_hold_waits_then_continues(tmp_path, monkeypatch)`
- **function `_alive`** [L360-369]: `def _alive(pid)`
- **test `test_tree_accounting_reads_interpreter_and_kill_reaches_it`** [L373-400]: `def test_tree_accounting_reads_interpreter_and_kill_reaches_it(tmp_path, monkeypatch)` decorators: @pytest.mark.skipif(os.name != 'nt', reason='Windows Job Objects')

