# `tests/hwsc/test_b_registry.py`

- Source: [tests/hwsc/test_b_registry.py](../../../../../tests/hwsc/test_b_registry.py)
- Kind: python
- Lines: 399

## Module docstring

> Author B (job 0176): registry readers R2 (c2nd), R4 (hwsb), R5 (dry stores), R7 (own store).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 24, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 25, via sys.path edit)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 26, via sys.path edit)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../tools/hwsc/hwsc_registry.py.md) (line 27, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 28, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 29, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 30, via unique basename)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../../tools/hwsb/hwsb_registry.py.md) (line 31, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 32, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 33, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, EmissionSpec, LocalFSBackend, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 34, via package root)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 8)
- `hashlib` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 14)
- `shutil` (lines 12)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `DRY`
- `NON_HISTORY`
- `REPO`
- `SEALED`
- `_HWSC`
- `_REAL_DRY`
- `_REC`

## Classes and functions

- **function `_audit`** [L43-50]: `def _audit(event, args)`
- **function `rec`** [L57-61]: `def rec()` decorators: @pytest.fixture
- **function `_touched`** [L64-66]: `def _touched(records, fragment, events=('open',))`
- **function `_has`** [L69-71]: `def _has(entries, rel)`
- **function `_sha`** [L74-75]: `def _sha(path)`
- **function `_hexes`** [L78-79]: `def _hexes(rng, n)`
- **function `_garbage`** [L82-85]: `def _garbage(path, data=b'not an array file')`
- **function `_canon_file`** [L88-92]: `def _canon_file(path, rows=8, seed=0, key='canon32')`
- **function `c2nd`** [L104-118]: `def c2nd(tmp_path)` decorators: @pytest.fixture
- **test `test_r2_pass_digests_seq_ids_and_known_gaps`** [L121-131]: `def test_r2_pass_digests_seq_ids_and_known_gaps(c2nd, rec)`
- **test `test_r2_changed_hash_is_lineage`** [L134-140]: `def test_r2_changed_hash_is_lineage(c2nd)`
- **test `test_r2_missing_bound_file_is_incomplete`** [L143-146]: `def test_r2_missing_bound_file_is_incomplete(c2nd)`
- **test `test_r2_required_column_missing_is_incomplete`** [L149-154]: `def test_r2_required_column_missing_is_incomplete(c2nd)`
- **test `test_r2_unbound_hist_table_is_read`** [L157-164]: `def test_r2_unbound_hist_table_is_read(c2nd)`
- **test `test_r2_unexpected_array_files_are_incomplete`** [L169-173]: `def test_r2_unexpected_array_files_are_incomplete(c2nd, rel)` decorators: @pytest.mark.parametrize('rel', ['superseded/0163-a1/hist/HIST_x_b0.npz', 'misc/loose.npy', 'stages/S9/T.npz'])
- **function `_stage_b_store`** [L177-190]: `def _stage_b_store(base, with_checkpoint=True)` - A stage-B-like store: tiny-world artifacts, two ObservationSets and one hist block.
- **function `hwsb_template`** [L194-197]: `def hwsb_template(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `hwsb`** [L201-208]: `def hwsb(tmp_path, hwsb_template)` decorators: @pytest.fixture
- **function `_paths_of`** [L211-213]: `def _paths_of(s, kind)`
- **test `test_r4_pass_and_classification`** [L216-232]: `def test_r4_pass_and_classification(hwsb, rec)`
- **test `test_r4_extra_array_file_is_incomplete`** [L235-239]: `def test_r4_extra_array_file_is_incomplete(hwsb)`
- **test `test_r4_missing_or_renamed_hist_is_incomplete`** [L243-250]: `def test_r4_missing_or_renamed_hist_is_incomplete(hwsb, change)` decorators: @pytest.mark.parametrize('change', ['missing', 'renamed'])
- **function `dry_root`** [L255-277]: `def dry_root(tmp_path, hwsb_template)` decorators: @pytest.fixture
- **function `_register`** [L280-283]: `def _register(monkeypatch, planted)`
- **function `_obs_digests`** [L286-298]: `def _obs_digests(art_root, kind)` - {id: (digests, perm)}: canonical (the EmissionSpec parent's perm) or named-order rows.
- **function `_payload_opened`** [L301-303]: `def _payload_opened(records, fragment)`
- **test `test_r5_pass_file_by_file`** [L306-324]: `def test_r5_pass_file_by_file(dry_root, monkeypatch, rec)`
- **test `test_r5_unregistered_planted_file_is_incomplete`** [L327-331]: `def test_r5_unregistered_planted_file_is_incomplete(dry_root, monkeypatch)`
- **test `test_r5_observation_set_without_emission_parent_is_incomplete`** [L334-338]: `def test_r5_observation_set_without_emission_parent_is_incomplete(dry_root, monkeypatch)`
- **test `test_r5_absent_optional_and_missing_required`** [L341-345]: `def test_r5_absent_optional_and_missing_required(tmp_path)`
- **test `test_r5_default_paths_glob_hwsb_dry_star`** [L348-358]: `def test_r5_default_paths_glob_hwsb_dry_star(dry_root, monkeypatch)`
- **function `own`** [L363-376]: `def own(tmp_path)` decorators: @pytest.fixture
- **test `test_r7_six_observation_sets_and_archived_table`** [L379-388]: `def test_r7_six_observation_sets_and_archived_table(own)`
- **test `test_r7_tampered_digest_column_fails`** [L391-399]: `def test_r7_tampered_digest_column_fails(own)`

