# `tests/c2_readout/test_b_registry.py`

- Source: [tests/c2_readout/test_b_registry.py](../../../../../tests/c2_readout/test_b_registry.py)
- Kind: python
- Lines: 387

## Module docstring

> Author B (job 0101): T-REG with the v2 H^Y donor and the NEW-10 Y-donor preparation fixture
> (C2-FROZEN-v2 §13.3, §2.2, §5.2-§5.5, §7 rows 4-6; API.md §5, §16, §18, §19.3).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 22, via sys.path edit)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 23, via sys.path edit)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](../../tools/c2_readout/c2_driver.py.md) (line 24, via sys.path edit)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 25, via sys.path edit)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../../tools/c2_readout/c2_oracle.py.md) (line 26, via sys.path edit)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../../tools/x6_stage1/x6s1_registry.py.md) (line 27, via unique basename)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `EXCLUSIONS`
- `PATHS`
- `READERS`
- `REPO`
- `ROLE_KEYS`
- `TMPS`
- `WORKTREES`

## Classes and functions

- **function `_isolate`** [L36-42]: `def _isolate(monkeypatch, root)`
- **function `_sha`** [L45-46]: `def _sha(path)`
- **function `_write`** [L49-52]: `def _write(path, data)`
- **function `_hist`** [L58-61]: `def _hist(seed, n)` - y-rows 1..4 only, so both one-row shifts stay on the grid (Y_def on every row).
- **function `_k`** [L64-65]: `def _k(n)`
- **function `_table`** [L68-73]: `def _table(seed, n, id0, off=())`
- **function `_redo`** [L76-79]: `def _redo(table, canon=None, ids=None)`
- **function `_hex`** [L82-83]: `def _hex(tokens)`
- **function `_expected_hy`** [L86-90]: `def _expected_hy(canon, k)`
- **function `_digests`** [L93-94]: `def _digests(table)`
- **class `_Reg`** [L97-105] - Registry stand-in for separation (sealed_ranges {pool: (lo, hi)}, API.md 19.1 E-20).
- **method `_Reg.__init__`** [L100-102]: `def __init__(self, digests=(), ranges=None)`
- **method `_Reg.contains`** [L104-105]: `def contains(self, hex_digests)`
- **test `test_y_donor_map_and_off_grid_rows`** [L109-120]: `def test_y_donor_map_and_off_grid_rows()`
- **test `test_history_table_with_the_y_donor`** [L123-135]: `def test_history_table_with_the_y_donor()`
- **function `_tables`** [L139-141]: `def _tables()`
- **test `test_separation_pass_with_duplicates_kept`** [L144-154]: `def test_separation_pass_with_duplicates_kept()`
- **test `test_collision_with_R_is_lineage`** [L157-160]: `def test_collision_with_R_is_lineage()`
- **test `test_off_grid_rows_form_no_donor`** [L163-171]: `def test_off_grid_rows_form_no_donor()`
- **test `test_cross_split_collision_and_seq_id_overlap_are_lineage`** [L174-189]: `def test_cross_split_collision_and_seq_id_overlap_are_lineage()`
- **test `test_sealed_d2a_predicate_hit_is_incomplete`** [L192-198]: `def test_sealed_d2a_predicate_hit_is_incomplete()`
- **function `_npz`** [L202-204]: `def _npz(path, **arrays)`
- **test `test_inventory_violations_and_admitted_empty_directory`** [L207-219]: `def test_inventory_violations_and_admitted_empty_directory(tmp_path, monkeypatch)`
- **test `test_inventory_admits_an_unlisted_empty_directory_alone`** [L222-227]: `def test_inventory_admits_an_unlisted_empty_directory_alone(tmp_path, monkeypatch)`
- **function `_x6_store`** [L231-245]: `def _x6_store(store)`
- **test `test_x6_source_binding_and_history_arrays`** [L248-265]: `def test_x6_source_binding_and_history_arrays(tmp_path, monkeypatch)`
- **test `test_build_refuses_existing_output`** [L269-274]: `def test_build_refuses_existing_output(tmp_path, monkeypatch)`
- **test `test_build_unreadable_sources_incomplete_and_R_prime_has_four_roles`** [L277-295]: `def test_build_unreadable_sources_incomplete_and_R_prime_has_four_roles(tmp_path, monkeypatch)`
- **test `test_registry_load_rehash_mismatch_is_lineage`** [L298-308]: `def test_registry_load_rehash_mismatch_is_lineage(tmp_path, monkeypatch)`
- **test `test_contract_inventory_lists_every_section_18_directory`** [L328-339]: `def test_contract_inventory_lists_every_section_18_directory()`
- **test `test_c1prime_landmarks_enter_R_through_reader_d`** [L342-347]: `def test_c1prime_landmarks_enter_R_through_reader_d()`
- **test `test_pytest_basetemp_is_outside_the_project_root`** [L350-352]: `def test_pytest_basetemp_is_outside_the_project_root(tmp_path)`
- **function `_toy_process`** [L356-360]: `def _toy_process()`
- **test `test_y_donor_preparation_from_the_cached_natural_oracle`** [L363-387]: `def test_y_donor_preparation_from_the_cached_natural_oracle()`

