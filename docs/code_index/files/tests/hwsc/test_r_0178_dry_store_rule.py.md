# `tests/hwsc/test_r_0178_dry_store_rule.py`

- Source: [tests/hwsc/test_r_0178_dry_store_rule.py](../../../../../tests/hwsc/test_r_0178_dry_store_rule.py)
- Kind: python
- Lines: 110

## Module docstring

> Coordinator-commissioned regression test for defect D-0178-1 (API.md §22): the hwsc-dry type
> rule of the R6 scratch check. A synthetic dry store under tmp_path holds one file of each allowed
> class; scratch_check passes it, and an unexpected array fails closed. Only hwsc-dry* folders are
> ruled by type; the same unexpected array in another folder still needs the frozen table.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 15, via sys.path edit)
- `import hwsc_drystore` -> [tools/hwsc/hwsc_drystore.py](../../tools/hwsc/hwsc_drystore.py.md) (line 16, via sys.path edit)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../tools/hwsc/hwsc_registry.py.md) (line 17, via sys.path edit)
- `import hwsc_scratch` -> [tools/hwsc/hwsc_scratch.py](../../tools/hwsc/hwsc_scratch.py.md) (line 18, via sys.path edit)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 6)
- `json` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `OK`
- `REPO`
- `UTC`

## Classes and functions

- **function `_meta`** [L25-28]: `def _meta(d: Path, art_type: str, parents=())`
- **function `_dry_store`** [L31-58]: `def _dry_store(root: Path) -> Path`
- **function `_check`** [L61-62]: `def _check(scratch, readers=OK)`
- **test `test_every_allowed_class_passes`** [L65-73]: `def test_every_allowed_class_passes(tmp_path)`
- **test `test_unexpected_array_fails_closed`** [L76-81]: `def test_unexpected_array_fails_closed(tmp_path)`
- **test `test_registry_npz_with_extra_key_fails_closed`** [L84-89]: `def test_registry_npz_with_extra_key_fails_closed(tmp_path)`
- **test `test_changed_planted_fixture_fails_closed`** [L92-95]: `def test_changed_planted_fixture_fails_closed(tmp_path)`
- **test `test_reader_classes_need_their_reader`** [L98-102]: `def test_reader_classes_need_their_reader(tmp_path)`
- **test `test_rule_applies_only_to_hwsc_dry_folders`** [L105-110]: `def test_rule_applies_only_to_hwsc_dry_folders(tmp_path)`

