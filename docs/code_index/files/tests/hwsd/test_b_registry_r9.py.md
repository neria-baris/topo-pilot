# `tests/hwsd/test_b_registry_r9.py`

- Source: [tests/hwsd/test_b_registry_r9.py](../../../../../tests/hwsd/test_b_registry_r9.py)
- Kind: python
- Lines: 297

## Module docstring

> Author B: R9, the stage-C layout reader, on a synthetic stage-C-like store (J1; DRD8, DRD9).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 14, via sys.path edit)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](../../tools/hwsd/hwsd_readers.py.md) (line 15, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 16, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 18, via unique basename)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../../tools/hwsb/hwsb_registry.py.md) (line 19, via unique basename)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 3)
- `json` (lines 5)
- `pathlib` (lines 8)
- `shutil` (lines 6)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 12: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `B_FILES`
- `CK`
- `IDENT`

## Classes and functions

- **function `_build`** [L30-69]: `def _build(store: Path) -> dict`
- **function `base`** [L73-75]: `def base(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `store`** [L79-84]: `def store(base, tmp_path, monkeypatch)` decorators: @pytest.fixture
- **function `_bind_obs`** [L87-96]: `def _bind_obs(store: Path, monkeypatch)` - dc.read_obs_inventory bound to the fixture's sha (TEST_PLAN B r9).
- **function `_never_opened`** [L99-106]: `def _never_opened(spy, store: Path)`
- **test `test_source_hwsc_passes_on_the_layout`** [L109-121]: `def test_source_hwsc_passes_on_the_layout(store, monkeypatch)`
- **test `test_unknown_array_is_incomplete`** [L126-133]: `def test_unknown_array_is_incomplete(store, rel, monkeypatch)` decorators: @pytest.mark.parametrize('rel', ['tmp/unknown.npz', 'stages/S5/X.npy', 'w.pt', 'logs/stray.npz', 'stages/S4/ORACLE_test.npz'])
- **test `test_array_in_train_is_incomplete_and_unopened`** [L136-142]: `def test_array_in_train_is_incomplete_and_unopened(store, monkeypatch)`
- **test `test_hist_sha_differing_from_stage_complete_is_lineage`** [L145-151]: `def test_hist_sha_differing_from_stage_complete_is_lineage(store)`
- **test `test_tampered_digest_column_is_incomplete`** [L154-163]: `def test_tampered_digest_column_is_incomplete(store)`
- **test `test_obs_inventory_not_equal_to_release_a_is_lineage`** [L166-169]: `def test_obs_inventory_not_equal_to_release_a_is_lineage(store)`
- **test `test_artifact_meta_mismatch_is_incomplete`** [L172-175]: `def test_artifact_meta_mismatch_is_incomplete(store)`
- **test `test_obs_inventory_extra_file_fails_closed`** [L178-181]: `def test_obs_inventory_extra_file_fails_closed(store)`
- **test `test_read_train_record_whitelist`** [L187-204]: `def test_read_train_record_whitelist(tmp_path)`
- **test `test_read_obs_inventory`** [L207-224]: `def test_read_obs_inventory(tmp_path)`
- **test `test_read_k4b_table`** [L227-245]: `def test_read_k4b_table(tmp_path)`
- **test `test_stage_complete_sha`** [L248-263]: `def test_stage_complete_sha(tmp_path)`
- **class `_X6`** [L266-268]
- **method `_X6.contains`** [L267-268]: `def contains(self, d)`
- **function `_reg`** [L271-272]: `def _reg(digests) -> c2_registry.Registry`
- **test `test_superset_check`** [L275-288]: `def test_superset_check(store)`
- **test `test_os_digests_independent`** [L291-297]: `def test_os_digests_independent(store)`

