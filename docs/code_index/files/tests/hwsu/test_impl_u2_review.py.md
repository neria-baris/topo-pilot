# `tests/hwsu/test_impl_u2_review.py`

- Source: [tests/hwsu/test_impl_u2_review.py](../../../../../tests/hwsu/test_impl_u2_review.py)
- Kind: python
- Lines: 142

## Module docstring

> Implementer regression tests for the real-tree path review R-0223-10 (items 1, 2, 4, 5).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)

### Standard library

- `__future__` (lines 3)
- `importlib` (lines 5)
- `json` (lines 6)
- `pathlib` (lines 9)
- `re` (lines 7)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 21: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 22: `dynamic: name`

### sys.path additions

- line 17: `str(p)` -> `tools/hwsu`, `tools/hwsu/u2`

## Imported by

- none

## Top-level constants

- `TOOLS`

## Classes and functions

- **function `mod`** [L20-22]: `def mod(name)`
- **function `_table`** [L25-26]: `def _table(path, seed=1, n=8)`
- **test `test_fixture_prefixes_from_contract`** [L30-34]: `def test_fixture_prefixes_from_contract()`
- **test `test_scratch_matcher_excludes_other_study_fixtures`** [L39-43]: `def test_scratch_matcher_excludes_other_study_fixtures(tmp_path, name, flagged)` decorators: @pytest.mark.parametrize('name,flagged', [('test_hwsg-0224', False), ('hwsg-dry-0230', False), ('otherstudy-0001', True)])
- **function `_stage_files`** [L47-52]: `def _stage_files(out)`
- **test `test_archive_previous_moves_same_stage_only`** [L55-64]: `def test_archive_previous_moves_same_stage_only(tmp_path)`
- **test `test_second_archive_gets_a2_and_obligation_lists_archived_arrays`** [L67-77]: `def test_second_archive_gets_a2_and_obligation_lists_archived_arrays(tmp_path)`
- **test `test_own_reader_follows_archived_listed_table`** [L80-87]: `def test_own_reader_follows_archived_listed_table(tmp_path)`
- **test `test_unrecorded_compares_sha_not_only_name`** [L90-98]: `def test_unrecorded_compares_sha_not_only_name(tmp_path)`
- **test `test_bind_stage_uses_the_stage_when_phase1_knows_it`** [L102-107]: `def test_bind_stage_uses_the_stage_when_phase1_knows_it()`
- **test `test_handoff_is_decoded_with_a_bom_tolerant_codec`** [L111-115]: `def test_handoff_is_decoded_with_a_bom_tolerant_codec(name)` decorators: @pytest.mark.parametrize('name', ['hwsu_driver', 'hwsu_gates', 'hwsu_known'])
- **test `test_s0_allowlist_admits_the_implementer_phase2_tests`** [L119-126]: `def test_s0_allowlist_admits_the_implementer_phase2_tests()`
- **test `test_g0u_treats_hwsg_locations_as_declarations`** [L130-142]: `def test_g0u_treats_hwsg_locations_as_declarations()`

