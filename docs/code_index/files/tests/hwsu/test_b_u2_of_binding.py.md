# `tests/hwsu/test_b_u2_of_binding.py`

- Source: [tests/hwsu/test_b_u2_of_binding.py](../../../../../tests/hwsu/test_b_u2_of_binding.py)
- Kind: python
- Lines: 142

## Module docstring

> Author B (job 0223, phase 2): R-0206-1 and the share outcome (API_U2 section 2.1;
> TEST_PLAN_U2 row test_b_u2_of_binding). Fixture stores live under tmp_path; the real OF_ACCEPT.json
> and FREEZE_OF.json are read (JSON/hash only) for the 'real' checks.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 19, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 20, via unique basename)

### External (third-party)

- `pytest` (lines 14)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `hashlib` (lines 8)
- `importlib` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 28: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 29: `hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](../../tools/hwsu/u2/hwsu_known.py.md)

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `AUTH`
- `KEYS`
- `REPO`
- `SHARE`

## Classes and functions

- **function `_known`** [L27-29]: `def _known()`
- **function `_sha`** [L32-33]: `def _sha(b: bytes) -> str`
- **function `_acc`** [L36-41]: `def _acc(**over) -> dict`
- **function `_fixture`** [L44-58]: `def _fixture(tmp_path, acc_over=None, freeze_bytes=b'{"fixture": "freeze_of"}', bind_freeze=None)`
- **function `_fail`** [L61-64]: `def _fail(fn, *a, **k)`
- **test `test_pass_for_response_only_with_matching_freeze_of`** [L67-73]: `def test_pass_for_response_only_with_matching_freeze_of(tmp_path)`
- **test `test_freeze_of_sha_mismatch_in_accept_refused`** [L76-79]: `def test_freeze_of_sha_mismatch_in_accept_refused(tmp_path)` - R-0206-1: OF_ACCEPT freeze_of_sha256 differs from the sha256 of FREEZE_OF.json.
- **test `test_freeze_of_file_changed_refused`** [L82-85]: `def test_freeze_of_file_changed_refused(tmp_path)`
- **test `test_contract_freeze_of_copy_differs_refused`** [L88-90]: `def test_contract_freeze_of_copy_differs_refused(tmp_path)`
- **test `test_of_accept_bytes_differ_from_contract_refused`** [L93-96]: `def test_of_accept_bytes_differ_from_contract_refused(tmp_path)`
- **test `test_wrong_outcome_verdict_or_size_refused`** [L102-104]: `def test_wrong_outcome_verdict_or_size_refused(tmp_path, over)` decorators: @pytest.mark.parametrize('over', [{'outcome': 'OF_PASS'}, {'outcome': 'OF_FAIL'}, {'outcome': 'OF_PASS_SHARE_ONLY'}, {'verdict': 'REJECT'}, {'verdict': 'accept'}, {'N_resp': 8192}])
- **test `test_missing_key_or_missing_file_refused`** [L107-113]: `def test_missing_key_or_missing_file_refused(tmp_path)`
- **test `test_extra_keys_do_not_matter_and_share_outcome_is_fixed`** [L116-124]: `def test_extra_keys_do_not_matter_and_share_outcome_is_fixed(tmp_path)` - Only keys_read are used: an unlisted key (e.g. a planted EG value) changes nothing.
- **test `test_keys_read_in_contract`** [L127-128]: `def test_keys_read_in_contract()`
- **test `test_real_of_accept_and_freeze_of_satisfy_the_rule`** [L131-142]: `def test_real_of_accept_and_freeze_of_satisfy_the_rule()`

