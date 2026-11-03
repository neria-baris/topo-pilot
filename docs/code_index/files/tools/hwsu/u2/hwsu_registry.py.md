# `tools/hwsu/u2/hwsu_registry.py`

- Source: [tools/hwsu/u2/hwsu_registry.py](../../../../../../tools/hwsu/u2/hwsu_registry.py)
- Kind: python
- Lines: 300

## Module docstring

> HWSU exposure registry: K-REG mirror, tables, U7 inventory, separation (API_U2.md section 3;
> protocol 8.2-8.3). The readers live in hwsu_regsrc (split by size) and stay reachable here.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 11, via unique basename)
- `import hwsu_regsrc` -> [tools/hwsu/u2/hwsu_regsrc.py](hwsu_regsrc.py.md) (line 12, via same directory)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 13, via unique basename)
- `import c1_data` -> [tools/c1prime/c1_data.py](../../c1prime/c1_data.py.md) (line 21, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../c2_readout/c2_registry.py.md) (line 22, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../hwsc/hwsc_registry.py.md) (line 23, via unique basename)
- `import hwsc_registry_build` -> [tools/hwsc/hwsc_registry_build.py](../../hwsc/hwsc_registry_build.py.md) (line 24, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../k4b/k4b_data.py.md) (line 25, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../k4b/k4b_registry.py.md) (line 26, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 28, via unique basename)

### External (third-party)

- `numpy` (lines 27)
- `psutil` (lines 181)

### Standard library

- `__future__` (lines 9)
- `fnmatch` (lines 14)
- `hashlib` (lines 15)
- `importlib` (lines 16)
- `pathlib` (lines 19)
- `re` (lines 17)
- `time` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 299: `hwsu_regsrc` -> [tools/hwsu/u2/hwsu_regsrc.py](hwsu_regsrc.py.md)

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_hwsd.py](../../../tests/hwsu/test_b_u2_hwsd.py.md) (line 30, dynamic)
- [tests/hwsu/test_b_u2_registry.py](../../../tests/hwsu/test_b_u2_registry.py.md) (line 29, dynamic)
- [tests/hwsu/test_impl_u2_mirror.py](../../../tests/hwsu/test_impl_u2_mirror.py.md) (line 6, import)
- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 17, import)
- [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md) (line 20, import)
- [tools/hwsu/u2/hwsu_dry2d.py](hwsu_dry2d.py.md) (line 14, import)
- [tools/hwsu/u2/hwsu_e2.py](hwsu_e2.py.md) (line 16, import)
- [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 18, import)
- [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 15, import)

## Top-level constants

- `COUNT_KEYS`
- `ND_TAGS`
- `TAGS`
- `_SPLIT`

## Classes and functions

- **function `_r`** [L39-40]: `def _r(contract=None) -> dict`
- **function `_hwsc_json`** [L43-44]: `def _hwsc_json(rel) -> dict`
- **function `_hwsc_reg`** [L47-48]: `def _hwsc_reg() -> dict`
- **function `scratch_table_u`** [L52-56]: `def scratch_table_u(contract=None) -> dict`
- **function `fixture_prefixes`** [L59-65]: `def fixture_prefixes(contract=None) -> tuple` - Scratch prefixes of other studies' synthetic test/dry fixtures (EXCLUSION rows with the
- **function `root_table_u`** [L68-71]: `def root_table_u(contract=None) -> dict`
- **function `_tags`** [L74-82]: `def _tags(rec, readers) -> list`
- **function `_violation`** [L85-100]: `def _violation(name, entry, rec, cls, readers)`
- **function `inventory_u`** [L103-122]: `def inventory_u(root, readers, contract=None) -> dict`
- **function `_scratch_u`** [L125-136]: `def _scratch_u(scratch, readers_ok) -> dict`
- **function `sources_u`** [L139-147]: `def sources_u(root, scratch, store, own_expected, contract=None) -> dict`
- **function `separation_u`** [L150-166]: `def separation_u(reg, tables, seq_union) -> dict`
- **function `load_registry_sets`** [L169-175]: `def load_registry_sets(reg_dir, version) -> tuple`
- **function `_peak_memory`** [L179-186]: `def _peak_memory()`
- **function `build_u`** [L189-290]: `def build_u(version, out_dir, root, scratch, handoff, own=None, extra=None, sources=None, contract=None) -> dict`
- **function `__getattr__`** [L297-300]: `def __getattr__(name)`

