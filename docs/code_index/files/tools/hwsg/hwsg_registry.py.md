# `tools/hwsg/hwsg_registry.py`

- Source: [tools/hwsg/hwsg_registry.py](../../../../../tools/hwsg/hwsg_registry.py)
- Kind: python
- Lines: 401

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
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 366, via unique basename) (inside a function)

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

- [tests/hwsg/test_impl_review.py](../../tests/hwsg/test_impl_review.py.md) (line 16, import)
- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 10, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 12, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 297, import)

## Top-level constants

- `ADDED_ROWS`
- `ARRAYS`
- `CLASS_TO_READER`
- `METADATA`
- `REG`
- `SINCE`

## Classes and functions

- **function `_merge`** [L38-46]: `def _merge(dst, src) -> dict`
- **function `read_k4b_history_table`** [L50-64]: `def read_k4b_history_table(path, entry, out, opener=None) -> None`
- **function `obligation_files`** [L71-73]: `def obligation_files(store) -> list`
- **function `_load_obligation`** [L76-91]: `def _load_obligation(store, bound=None) -> tuple`
- **function `latest_obligation`** [L94-98]: `def latest_obligation(store, bound=None) -> dict`
- **function `array_listing`** [L101-110]: `def array_listing(store) -> list`
- **function `_metadata`** [L113-115]: `def _metadata(store) -> list`
- **function `source_obligation`** [L118-151]: `def source_obligation(store, bound=None, opener=None) -> dict`
- **function `_glob_re`** [L155-156]: `def _glob_re(g) -> re.Pattern`
- **function `source_hwsc`** [L159-188]: `def source_hwsc(store=None, expected=None) -> dict`
- **function `source_scratch_g`** [L192-214]: `def source_scratch_g(scratch=None, table=None) -> dict`
- **function `source_own`** [L218-227]: `def source_own(store, worlds) -> dict`
- **function `inventory_g`** [L231-236]: `def inventory_g(root=None, readers=None) -> dict`
- **function `_canon`** [L239-240]: `def _canon(o) -> str`
- **function `_sha`** [L243-244]: `def _sha(o) -> str`
- **function `_obligations`** [L247-258]: `def _obligations(root, bound=None) -> dict`
- **function `certificate`** [L261-264]: `def certificate(manifest) -> str`
- **function `_inv_sha`** [L267-269]: `def _inv_sha(root, inv, bound=None) -> tuple`
- **function `recheck`** [L272-280]: `def recheck(manifest, root=None) -> dict`
- **function `sources`** [L284-293]: `def sources(root, scratch, worlds, extra=None, table=None) -> dict`
- **function `_certify`** [L297-316]: `def _certify(mpath, root, bound)` decorators: @contextlib.contextmanager
- **function `build`** [L319-351]: `def build(version, out_dir, root=None, scratch=None, worlds=gc.TAGS, extra=None, sources_fn=None) -> dict`
- **class `_RegView`** [L355-361]
- **method `_RegView.__init__`** [L356-358]: `def __init__(self, d)`
- **method `_RegView.contains`** [L360-361]: `def contains(self, digest)`
- **function `_table`** [L364-371]: `def _table(t) -> dict`
- **function `separation_g`** [L374-401]: `def separation_g(reg, tables_by_world) -> dict`

