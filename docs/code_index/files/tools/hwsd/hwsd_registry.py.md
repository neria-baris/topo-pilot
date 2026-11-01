# `tools/hwsd/hwsd_registry.py`

- Source: [tools/hwsd/hwsd_registry.py](../../../../../tools/hwsd/hwsd_registry.py)
- Kind: python
- Lines: 327

## Module docstring

> HWSD K-REG-D: the scratch scan and check mirrors, the hwsd-dry type rule, inventory_d, build_d
> and load_d (API.md section 5; DRD8). Mirrors hwsc_scratch / hwsc_registry.inventory_c with the
> hwsd changes; reused functions are looked up at call time.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 13, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 14, via unique basename)
- `import hwsc_drystore` -> [tools/hwsc/hwsc_drystore.py](../hwsc/hwsc_drystore.py.md) (line 15, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../hwsc/hwsc_registry.py.md) (line 16, via unique basename)
- `import hwsc_registry_build` -> [tools/hwsc/hwsc_registry_build.py](../hwsc/hwsc_registry_build.py.md) (line 17, via unique basename)
- `import hwsc_scratch` -> [tools/hwsc/hwsc_scratch.py](../hwsc/hwsc_scratch.py.md) (line 18, via unique basename)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](hwsd_readers.py.md) (line 19, via same directory)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 23, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 24, via unique basename)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 5)
- `os` (lines 8)
- `pathlib` (lines 11)
- `re` (lines 9)
- `time` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_b_registry_build.py](../../tests/hwsd/test_b_registry_build.py.md) (line 14, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 21, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 29, import)

## Top-level constants

- `BLINDED_TOP`
- `_PATTERNS`
- `_RUN`
- `_SPLIT_FILE`

## Classes and functions

- **function `scratch_scan_d`** [L37-65]: `def scratch_scan_d(scratch=None) -> dict`
- **function `row_for_d`** [L68-74]: `def row_for_d(name, table)`
- **function `_heads`** [L78-79]: `def _heads(f) -> dict`
- **function `_os_parent_ok`** [L82-93]: `def _os_parent_ok(os_dir) -> bool`
- **function `dry_class_d`** [L96-125]: `def dry_class_d(store, rel, rec)`
- **function `_fixture_ok`** [L129-135]: `def _fixture_ok(rel, rec, row) -> bool`
- **function `_hash_ok`** [L138-141]: `def _hash_ok(path, want) -> bool`
- **function `_check_row_d`** [L144-163]: `def _check_row_d(name, listed, row, ok_tags, scratch, out) -> None`
- **function `scratch_check_d`** [L166-204]: `def scratch_check_d(scratch=None, table=None, readers_ok=None) -> dict`
- **function `inventory_d`** [L208-235]: `def inventory_d(root=None, readers=None, table=None) -> dict`
- **function `_summary`** [L239-241]: `def _summary(r) -> dict`
- **function `_merged`** [L244-251]: `def _merged(*srcs) -> dict`
- **function `build_d`** [L254-312]: `def build_d(out_dir, root=None, scratch=None, handoff=None, sources=None) -> dict`
- **function `load_d`** [L315-327]: `def load_d(store=None)`

