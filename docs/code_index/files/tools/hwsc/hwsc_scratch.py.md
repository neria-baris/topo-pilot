# `tools/hwsc/hwsc_scratch.py`

- Source: [tools/hwsc/hwsc_scratch.py](../../../../../tools/hwsc/hwsc_scratch.py)
- Kind: python
- Lines: 145

## Module docstring

> HWSC R6 scratch inventory: header scan and the fail-closed check against the frozen table
> (API.md §4, §20; rulings R-0176-G9, R-0176-R6). Split from hwsc_registry by size; re-exported
> there. A row may hold reader-covered files (`covered`: {relpath: reader tag}) and HASH_FROZEN
> files (`hash_frozen`: {relpath: {sha256, bytes, reason_class}}), re-hashed at every check.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 8, via same directory)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 12, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 13, via unique basename)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 14, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 18, via same directory) (inside a function)
- `import hwsc_drystore` -> [tools/hwsc/hwsc_drystore.py](hwsc_drystore.py.md) (line 139, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `os` (lines 9)
- `pathlib` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_r_0178_dry_store_rule.py](../../tests/hwsc/test_r_0178_dry_store_rule.py.md) (line 18, import)
- [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 239, import)
- [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 331, import)

## Top-level constants

- `HASH_CLASSES`

## Classes and functions

- **function `_cr`** [L16-20]: `def _cr()` - hwsc_registry, imported lazily (it re-exports this module; no import-time cycle).
- **function `_classify`** [L26-41]: `def _classify(f) -> tuple`
- **function `scratch_scan`** [L44-68]: `def scratch_scan(scratch=None) -> dict`
- **function `_row_for`** [L71-77]: `def _row_for(name, table)`
- **function `_fixture_ok`** [L80-86]: `def _fixture_ok(rel, rec, row) -> bool`
- **function `_hash_ok`** [L89-92]: `def _hash_ok(path, want) -> bool`
- **function `_check_row`** [L95-114]: `def _check_row(name, listed, row, ok_tags, scratch, out) -> None`
- **function `scratch_check`** [L117-145]: `def scratch_check(scratch=None, table=None, readers_ok=None) -> dict`

