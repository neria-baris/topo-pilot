# `tools/hwsu/u2/hwsu_regsrc.py`

- Source: [tools/hwsu/u2/hwsu_regsrc.py](../../../../../../tools/hwsu/u2/hwsu_regsrc.py)
- Kind: python
- Lines: 289

## Module docstring

> HWSU registry readers: U2 (stage C), U2', U5, U6, U8 and the J10 obligation reader
> (API_U2.md section 3; protocol 8.2-8.3). Split from hwsu_registry by size (API erratum); every
> name stays reachable as hwsu_registry.<name>.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 7, via unique basename)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 8, via same directory)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../hwsu_pairs.py.md) (line 9, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 10, via unique basename)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../../hwsb/hwsb_registry.py.md) (line 16, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../hwsc/hwsc_registry.py.md) (line 17, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../k4b/k4b_data.py.md) (line 18, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 20, via unique basename)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 5)
- `json` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 14)
- `re` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 288, dynamic)
- [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 12, import)

## Top-level constants

- `ARR`
- `ART_T`

## Classes and functions

- **function `_new`** [L27-29]: `def _new(present=True) -> dict`
- **function `_close`** [L32-34]: `def _close(out, lineage=False) -> dict`
- **function `read_hist_table`** [L37-44]: `def read_hist_table(path) -> tuple` - K4b history table: digest column re-derived from canon32 (k4b_data.digests).
- **function `_take`** [L47-51]: `def _take(out, f, rel) -> None`
- **function `_class_c`** [L56-78]: `def _class_c(rel, store) -> str | None`
- **function `source_hwsc`** [L81-117]: `def source_hwsc(store, contract=None) -> dict`
- **function `source_kreg2_c`** [L120-131]: `def source_kreg2_c(store, contract=None) -> dict`
- **function `superset_diagnostic`** [L134-146]: `def superset_diagnostic(union_sorted, kreg2_sorted, chunk=1000000) -> dict`
- **function `source_own_u`** [L150-173]: `def source_own_u(store, expected, contract=None) -> dict`
- **function `read_obligation_u2`** [L176-222]: `def read_obligation_u2(store, root=uc.ROOT, contract=None) -> dict`
- **function `_read_store`** [L225-240]: `def _read_store(store, root, out, tag) -> None`
- **function `source_hwsd`** [L243-253]: `def source_hwsd(root, scratch, contract=None) -> dict`
- **function `_registered_ids`** [L256-263]: `def _registered_ids() -> set`
- **function `source_own_dry`** [L266-289]: `def source_own_dry(scratch, contract=None) -> dict`

