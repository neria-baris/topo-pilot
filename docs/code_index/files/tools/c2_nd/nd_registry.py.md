# `tools/c2_nd/nd_registry.py`

- Source: [tools/c2_nd/nd_registry.py](../../../../../tools/c2_nd/nd_registry.py)
- Kind: python
- Lines: 400

## Module docstring

> C2ND exposure registry c2nd-reg-v1: the new readers c2, c2sup, c2scratch, hws and x6zc (rows
> 2-9 of protocol §6.2), the ND inventory adapter, the ND-REG1/ND-REG2 builds composing the
> unchanged c2_registry readers (row 1), loading, separation and the reservation record check
> (API.md §5, §20; C2ND-DESIGN-v1 §6.2-§6.5).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 21, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 24, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 25, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 26, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 29, via unique basename)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 44, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 28)

### Standard library

- `__future__` (lines 11)
- `fnmatch` (lines 13)
- `hashlib` (lines 14)
- `json` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 19)
- `re` (lines 17)
- `time` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_dry_hs.py](../../tests/c2_nd/test_b_dry_hs.py.md) (line 30, import)
- [tests/c2_nd/test_b_lineage.py](../../tests/c2_nd/test_b_lineage.py.md) (line 23, import)
- [tests/c2_nd/test_b_registry.py](../../tests/c2_nd/test_b_registry.py.md) (line 27, import)
- [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 24, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 30, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 27, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 26, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 26, import)

## Top-level constants

- `ARRAYS`
- `C2_COLS`
- `EXCLUDE`
- `ND_READERS`
- `NOT_READ`
- `OWN`
- `TAGS`

## Classes and functions

- **function `_xr`** [L43-46]: `def _xr()`
- **function `_new`** [L49-51]: `def _new(present=True) -> dict`
- **function `_close`** [L54-56]: `def _close(out, lineage=False) -> dict`
- **function `_hex`** [L59-60]: `def _hex(chunk) -> set`
- **function `_c2_table`** [L63-74]: `def _c2_table(path, out) -> None` - The digest columns of one C2-format history table ("" dropped; c2_data.table_digests).
- **function `source_c2`** [L78-103]: `def source_c2(store=None, bound=None) -> dict` - The bound C2 hist files (CONTRACT, or `bound` for the dry stand-in) and any further
- **function `source_c2_superseded`** [L106-118]: `def source_c2_superseded(store=None) -> dict` - A name scan of superseded/: PASS iff the bound attempt directories exist and no file has
- **function `_c2_format`** [L122-124]: `def _c2_format(path) -> bool`
- **function `source_scratch`** [L127-151]: `def source_scratch(root=None) -> dict` - Every HIST_*.npz under the scratch root outside a test_* directory (relative to the root):
- **function `_x6zc_names`** [L155-159]: `def _x6zc_names() -> list`
- **function `_read_history`** [L162-190]: `def _read_history(f, out, require) -> None` - One array file by the c2_registry._x6_member rule, integer [n, w < 32] history members
- **function `_array_files`** [L193-194]: `def _array_files(top)`
- **function `_parallel_file`** [L197-207]: `def _parallel_file(f, rel, tag, out) -> None`
- **function `source_parallel`** [L210-228]: `def source_parallel(store, tag) -> dict` - A parallel round's store: absent -> PASS (present False); unfrozen -> INCOMPLETE; else
- **function `inventory`** [L232-256]: `def inventory(root=None, readers=None) -> dict` - k4b_registry.inventory/classify of every top-level directory against the ND frozen table;
- **function `_nd_sources`** [L260-275]: `def _nd_sources(root, c2_dry=None) -> dict` - Rows 2-9; with an explicit root the stores are taken under it (API.md §20 B-5). `c2_dry`
- **function `_summary`** [L278-280]: `def _summary(r) -> dict`
- **function `build`** [L283-359]: `def build(version, store=None, root=None, extra=None, c2_dry=None) -> dict` - ND-REG1 (S1, before DFIT) or ND-REG2 (S5; R' with the DFIT/DFEAS/DVAL tables in `extra`):
- **function `load`** [L363-364]: `def load(store=None, version='ND-REG1') -> cg.Registry`
- **function `_reservation_problem`** [L371-393]: `def _reservation_problem(store, stage, root) -> str | None`
- **function `reservation_check`** [L396-400]: `def reservation_check(store, stage, root=None) -> dict` - PASS iff RESERVATION_<stage>.json records no live reservation and the parallel stores'

