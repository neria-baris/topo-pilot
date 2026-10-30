# `tools/hwsc/hwsc_drystore.py`

- Source: [tools/hwsc/hwsc_drystore.py](../../../../../tools/hwsc/hwsc_drystore.py)
- Kind: python
- Lines: 129

## Module docstring

> HWSC type rule for the stage-C dry stores `hwsc-dry*` (defect D-0178-1; API.md §22).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 12, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 18, via unique basename)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 19, via unique basename)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 10)
- `json` (lines 13)
- `pathlib` (lines 15)
- `re` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_r_0178_dry_store_rule.py](../../tests/hwsc/test_r_0178_dry_store_rule.py.md) (line 16, import)
- [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 238, import)
- [tools/hwsc/hwsc_scratch.py](hwsc_scratch.py.md) (line 139, import)

## Top-level constants

- `PLANTED`
- `PREFIX`
- `RULE`
- `_ARTS`
- `_RUN`

## Classes and functions

- **function `is_dry_store`** [L29-30]: `def is_dry_store(name) -> bool`
- **function `_meta`** [L33-37]: `def _meta(path)`
- **function `_os_parent_ok`** [L40-47]: `def _os_parent_ok(os_dir) -> bool` - An ObservationSet whose single EmissionSpec parent lies in the same artifacts dir.
- **function `_heads`** [L50-51]: `def _heads(f) -> dict`
- **function `_registry_npz`** [L54-56]: `def _registry_npz(f) -> bool`
- **function `_digest_run`** [L59-62]: `def _digest_run(f) -> bool`
- **function `_c2_table`** [L65-67]: `def _c2_table(f) -> bool`
- **function `_tokens`** [L70-72]: `def _tokens(f) -> bool`
- **function `dry_class`** [L75-106]: `def dry_class(store, rel, rec)` - The class of one listed file of a hwsc-dry* store, or None (fails closed).
- **function `_planted`** [L109-117]: `def _planted(f, parts)`
- **function `check_store`** [L120-129]: `def check_store(store, listed, ok_tags, out) -> None` - scratch_check for one hwsc-dry* store: every listed file needs an allowed class.

