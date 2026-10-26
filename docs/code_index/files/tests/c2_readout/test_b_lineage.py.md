# `tests/c2_readout/test_b_lineage.py`

- Source: [tests/c2_readout/test_b_lineage.py](../../../../../tests/c2_readout/test_b_lineage.py)
- Kind: python
- Lines: 395

## Module docstring

> Author B (job 0101): T-G0 (RC-16), T-LINEAGE and T-NAMESPACE (RC-11; three tests)
> (C2-FROZEN-v2 §13.3, §4, §5.2, §7 row 1, §11, §13.1; API.md §3.1, §4.4, §12, §16, §19.3).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 23, via sys.path edit)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 24, via sys.path edit)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](../../tools/c2_readout/c2_driver.py.md) (line 25, via sys.path edit)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 26, via sys.path edit)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 27, via unique basename)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `BLOBS`
- `CHARTS`
- `LINEAGE`
- `PATHS`
- `PROTO`
- `REPO`
- `STATE_SHA`
- `SYN_AUTH`
- `V1`

## Classes and functions

- **function `_sha`** [L77-78]: `def _sha(path)`
- **function `_write`** [L81-84]: `def _write(path, data)`
- **function `_isolate`** [L87-93]: `def _isolate(monkeypatch, root)`
- **function `_ctx`** [L96-98]: `def _ctx(store, worktree=REPO, job='0199', task='a' * 64)`
- **test `test_protocol_and_authority_bindings`** [L102-114]: `def test_protocol_and_authority_bindings()`
- **test `test_state_sha_chart_and_freeze_hashes_equal_the_contract`** [L117-125]: `def test_state_sha_chart_and_freeze_hashes_equal_the_contract()`
- **test `test_reused_blob_hashes_equal_section_13_1_and_the_files`** [L128-139]: `def test_reused_blob_hashes_equal_section_13_1_and_the_files()`
- **test `test_load_contract_refuses_a_protocol_mismatch`** [L142-151]: `def test_load_contract_refuses_a_protocol_mismatch(tmp_path)`
- **function `_g0_env`** [L154-169]: `def _g0_env(tmp_path, monkeypatch, alter)`
- **test `test_g0_refuses_a_protocol_copy_mismatch`** [L172-180]: `def test_g0_refuses_a_protocol_copy_mismatch(tmp_path, monkeypatch)`
- **test `test_g0_item_i_accepts_the_exact_copy`** [L183-187]: `def test_g0_item_i_accepts_the_exact_copy(tmp_path, monkeypatch)`
- **function `bound_auth`** [L195-204]: `def bound_auth(monkeypatch)` decorators: @pytest.fixture - The v2 AUTH is pending (CONTRACT protocol.auth null); bind a synthetic one for the test.
- **function `_auth`** [L207-220]: `def _auth(**over)`
- **test `test_auth_ok`** [L227-229]: `def test_auth_ok(tmp_path, bound_auth, over, ok)` decorators: @pytest.mark.parametrize('over, ok', [({}, True), ({'protocol_sha256': PROTO.upper()}, True), ({'schema': 'c2-auth-v0'}, False), ({'protocol_sha256': '0' * 64}, False), ({'owner_sha256': '0' * 64}, False), ({'owner_owner_verbatim': ''}, False), ({'coordinator': ''}, False)])
- **test `test_auth_ok_refuses_while_the_v2_auth_is_pending`** [L232-236]: `def test_auth_ok_refuses_while_the_v2_auth_is_pending(tmp_path)`
- **test `test_auth_ok_missing_or_unparsable_never_raises`** [L239-242]: `def test_auth_ok_missing_or_unparsable_never_raises(tmp_path, bound_auth)`
- **function `_store`** [L246-252]: `def _store(tmp_path)`
- **test `test_write_manifest_exclusive_and_hashes`** [L255-270]: `def test_write_manifest_exclusive_and_hashes(tmp_path)`
- **test `test_supersede_moves_append_only_and_records`** [L273-296]: `def test_supersede_moves_append_only_and_records(tmp_path)`
- **test `test_regen_compare_bit_identical`** [L299-308]: `def test_regen_compare_bit_identical(tmp_path)`
- **function `_ns_root`** [L312-323]: `def _ns_root(tmp_path, monkeypatch)`
- **test `test_namespace_initial_admission`** [L326-336]: `def test_namespace_initial_admission(tmp_path, monkeypatch)`
- **test `test_namespace_legitimate_continuation`** [L339-367]: `def test_namespace_legitimate_continuation(tmp_path, monkeypatch)`
- **test `test_namespace_unrelated_collision_is_lineage`** [L376-383]: `def test_namespace_unrelated_collision_is_lineage(tmp_path, monkeypatch, rel, data)` decorators: @pytest.mark.parametrize('rel, data', [('x9-research-store/notes.json', b'{"scope": "c2-v1"}'), ('other-dir/FREEZE_old.json', b'{"scope": "c2-v1"}'), ('c2-readout-store/extra.json', b'{"tag": "c2-v1"}'), ('big-store/big.txt', b'x' * (2 ** 20 - 2) + b'c2-v1' + b'y' * 9)], ids=['foreign-store', 'freeze-anywhere', 'store-unlisted', 'chunk-boundary'])
- **test `test_measure_only_caps_in_the_contract`** [L387-395]: `def test_measure_only_caps_in_the_contract()`

