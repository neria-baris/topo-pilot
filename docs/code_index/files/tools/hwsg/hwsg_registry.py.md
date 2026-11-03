# `tools/hwsg/hwsg_registry.py`

- Source: [tools/hwsg/hwsg_registry.py](../../../../../tools/hwsg/hwsg_registry.py)
- Kind: python
- Lines: 413

## Module docstring

> HWSG registry: composition adapter, readers (b)-(d),(f), inventory, certificate (API.md §6;
> protocol §6; N6). Reuses hwsc_registry_build.build / hwsc_registry readers through overrides.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 6, via same directory)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../hwsb/hwsb_registry.py.md) (line 18, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 19, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../hwsc/hwsc_registry.py.md) (line 20, via unique basename)
- `import hwsc_registry_build` -> [tools/hwsc/hwsc_registry_build.py](../hwsc/hwsc_registry_build.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 23, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 24, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 378, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 4)
- `contextlib` (lines 7)
- `fnmatch` (lines 8)
- `hashlib` (lines 9)
- `io` (lines 10)
- `itertools` (lines 15)
- `json` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 16)
- `re` (lines 13)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 10, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 12, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 286, import)

## Top-level constants

- `ADDED_ROWS`
- `ARRAYS`
- `CLASS_TO_READER`
- `METADATA`
- `REG`
- `SINCE`

## Classes and functions

- **function `_new`** [L35-36]: `def _new(present=True) -> dict`
- **function `_close`** [L39-40]: `def _close(out, lineage=False) -> dict`
- **function `_merge`** [L43-51]: `def _merge(dst, src) -> dict`
- **function `read_k4b_history_table`** [L55-69]: `def read_k4b_history_table(path, entry, out, opener=None) -> None`
- **function `obligation_files`** [L76-78]: `def obligation_files(store) -> list`
- **function `_load_obligation`** [L81-96]: `def _load_obligation(store, bound=None) -> tuple`
- **function `latest_obligation`** [L99-103]: `def latest_obligation(store, bound=None) -> dict`
- **function `array_listing`** [L106-115]: `def array_listing(store) -> list`
- **function `_metadata`** [L118-125]: `def _metadata(store) -> list`
- **function `source_obligation`** [L128-161]: `def source_obligation(store, bound=None, opener=None) -> dict`
- **function `_glob_re`** [L165-166]: `def _glob_re(g) -> re.Pattern`
- **function `source_hwsc`** [L169-198]: `def source_hwsc(store=None, expected=None) -> dict`
- **function `source_scratch_g`** [L202-224]: `def source_scratch_g(scratch=None, table=None) -> dict`
- **function `source_own`** [L228-237]: `def source_own(store, worlds) -> dict`
- **function `inventory_g`** [L241-246]: `def inventory_g(root=None) -> dict`
- **function `_canon`** [L249-250]: `def _canon(o) -> str`
- **function `_sha`** [L253-254]: `def _sha(o) -> str`
- **function `_obligations`** [L257-268]: `def _obligations(root, bound=None) -> dict`
- **function `readers_version`** [L271-272]: `def readers_version() -> str`
- **function `certificate`** [L275-278]: `def certificate(manifest) -> str`
- **function `_inv_sha`** [L281-283]: `def _inv_sha(root, inv, bound=None) -> tuple`
- **function `recheck`** [L286-294]: `def recheck(manifest, root=None) -> dict`
- **function `sources`** [L298-305]: `def sources(root, scratch, worlds, extra=None, table=None) -> dict`
- **function `_certify`** [L309-328]: `def _certify(mpath, root, bound)` decorators: @contextlib.contextmanager
- **function `build`** [L331-363]: `def build(version, out_dir, root=None, scratch=None, worlds=gc.TAGS, extra=None, sources_fn=None) -> dict`
- **class `_RegView`** [L367-373]
- **method `_RegView.__init__`** [L368-370]: `def __init__(self, d)`
- **method `_RegView.contains`** [L372-373]: `def contains(self, digest)`
- **function `_table`** [L376-383]: `def _table(t) -> dict`
- **function `separation_g`** [L386-413]: `def separation_g(reg, tables_by_world) -> dict`

