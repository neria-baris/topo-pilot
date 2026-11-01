# `tests/hwsu/test_b_of_freeze.py`

- Source: [tests/hwsu/test_b_of_freeze.py](../../../../../tests/hwsu/test_b_of_freeze.py)
- Kind: python
- Lines: 310

## Module docstring

> Author B (job 0198): FREEZE_OF.json, its verification with the append-only prefix check for
> API.md/TEST_PLAN.md (D-0, coordinator ruling on D-0), and OF-B (protocol §4.1, §4.2 OF-B; API
> §5.3-§5.4; DRO7). Every git repository is a fixture under tmp_path; the reused files are copied
> byte for byte from their blobs at r_ref = e3710d2 of this worktree's history (read-only).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 20, via sys.path edit)
- `import hwsu_bind` -> [tools/hwsu/hwsu_bind.py](../../tools/hwsu/hwsu_bind.py.md) (line 21, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 22, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `pytest` (lines 15)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 13)
- `shutil` (lines 10)
- `subprocess` (lines 11)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `C`
- `DOCS`
- `GIT`
- `REPO`
- `R_REF`
- `TESTS`

## Classes and functions

- **function `_git`** [L35-37]: `def _git(repo, *args) -> str`
- **function `_sha`** [L40-41]: `def _sha(b: bytes) -> str`
- **function `_put`** [L44-47]: `def _put(repo, rel, data: bytes)`
- **function `_reuse_blobs`** [L50-61]: `def _reuse_blobs() -> dict`
- **function `base_repo`** [L65-89]: `def base_repo(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `_clone`** [L92-98]: `def _clone(base_repo, tmp_path)`
- **function `_impl`** [L101-106]: `def _impl(repo, h) -> dict`
- **function `_canon_sha`** [L109-110]: `def _canon_sha(obj) -> str`
- **function `_report`** [L113-118]: `def _report(tmp_path, repo, h, **over) -> Path`
- **function `_jof`** [L121-124]: `def _jof(tmp_path) -> list`
- **function `_freeze`** [L127-129]: `def _freeze(tmp_path, repo, h, store, **over)`
- **function `_status`** [L132-137]: `def _status(fn, *a, **k)`
- **function `frozen_base`** [L142-145]: `def frozen_base(base_repo, tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_freeze_of_fields`** [L148-167]: `def test_freeze_of_fields(frozen_base, tmp_path)`
- **test `test_freeze_of_refuses_dro_report`** [L171-174]: `def test_freeze_of_refuses_dro_report(base_repo, tmp_path, over)` decorators: @pytest.mark.parametrize('over', [{'implementation_sha256': '0' * 64}, {'all_pass': False}])
- **test `test_freeze_of_refuses_changed_reuse_blob`** [L177-184]: `def test_freeze_of_refuses_changed_reuse_blob(base_repo, tmp_path)`
- **function `_frozen`** [L188-192]: `def _frozen(frozen_base, tmp_path)`
- **test `test_verify_passes_and_allows_appends`** [L195-200]: `def test_verify_passes_and_allows_appends(frozen_base, tmp_path)`
- **test `test_verify_refuses_byte_change_inside_prefix`** [L205-211]: `def test_verify_refuses_byte_change_inside_prefix(frozen_base, tmp_path, rel, where)` decorators: @pytest.mark.parametrize('rel', ['tools/hwsu/API.md', 'tools/hwsu/TEST_PLAN.md']) @pytest.mark.parametrize('where', ['first', 'middle', 'last'])
- **test `test_verify_refuses_truncated_document`** [L215-218]: `def test_verify_refuses_truncated_document(frozen_base, tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['tools/hwsu/API.md', 'tools/hwsu/TEST_PLAN.md'])
- **test `test_verify_refuses_any_other_change`** [L225-228]: `def test_verify_refuses_any_other_change(frozen_base, tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['tools/hwsu/hwsu_config.py', 'tools/hwsu/hwsu_records.py', 'tools/hwsu/CONTRACT_OF.json', 'tools/hwsu/PROTOCOL_HWSU_v1.md', 'tests/hwsu/test_b_of_fixture.py', 'tests/hwsu/AUTHORSHIP_A.md', 'tools/hwsb/hwsb_known.py'])
- **test `test_verify_absent_freeze`** [L231-233]: `def test_verify_absent_freeze(base_repo, tmp_path)`
- **function `_audit`** [L237-241]: `def _audit(status)` - A stub with the API §7 shape of hwsu_bind.audit.
- **function `audit_pass`** [L245-248]: `def audit_pass(monkeypatch)` decorators: @pytest.fixture
- **test `test_of_b_refuses_changed_phase1_file_after_freeze`** [L251-254]: `def test_of_b_refuses_changed_phase1_file_after_freeze(frozen_base, tmp_path, audit_pass)`
- **function `_commit_and_freeze`** [L257-270]: `def _commit_and_freeze(frozen_base, tmp_path, change)` - A freeze record at a new commit that leaves every phase-1 and test file unchanged: the
- **test `test_of_b_refuses_diff_outside_allowlist`** [L280-283]: `def test_of_b_refuses_diff_outside_allowlist(frozen_base, tmp_path, audit_pass, name, change)` decorators: @pytest.mark.parametrize('name,change', [('new file outside the allowlist', lambda r: _put(r, 'tools/hwsc/new_helper.py', b'x\n')), ('modified non-index file', lambda r: _put(r, 'notes/keep.txt', b'changed\n')), ('deleted file', lambda r: (r / 'notes' / 'keep.txt').unlink()), ('unlisted tests file', lambda r: _put(r, 'tests/hwsu/conftest.py', b'x\n')), ('unlisted hwsu module', lambda r: _put(r, 'tools/hwsu/hwsu_extra.py', b'x\n'))])
- **test `test_of_b_pass_with_code_index_changes`** [L286-295]: `def test_of_b_pass_with_code_index_changes(frozen_base, tmp_path, audit_pass)` - OF-B PASS: phase-1 and test files added, docs/code_index/** added and modified.
- **test `test_of_b_refuses_reused_file_change_in_tree`** [L298-302]: `def test_of_b_refuses_reused_file_change_in_tree(frozen_base, tmp_path, audit_pass)`
- **test `test_of_b_refuses_failed_audit_and_absent_freeze`** [L305-310]: `def test_of_b_refuses_failed_audit_and_absent_freeze(base_repo, frozen_base, tmp_path, monkeypatch)`

