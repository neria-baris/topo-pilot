# `tests/hwsd/test_b_registry_build.py`

- Source: [tests/hwsd/test_b_registry_build.py](../../../../../tests/hwsd/test_b_registry_build.py)
- Kind: python
- Lines: 330

## Module docstring

> Author B: K-REG-D composition, scratch scan/check mirrors, root inventory, tables (§4.1; DRD8).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 12, via sys.path edit)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](../../tools/hwsd/hwsd_readers.py.md) (line 13, via sys.path edit)
- `import hwsd_registry` -> [tools/hwsd/hwsd_registry.py](../../tools/hwsd/hwsd_registry.py.md) (line 14, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 15, via same directory)
- `import hwsc_dry` -> [tools/hwsc/hwsc_dry.py](../../tools/hwsc/hwsc_dry.py.md) (line 17, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../tools/hwsc/hwsc_registry.py.md) (line 18, via unique basename)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 3)
- `pathlib` (lines 6)
- `sys` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 10: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `UTCDIR`

## Classes and functions

- **function `_hist`** [L26-27]: `def _hist(path, n=8)`
- **test `test_effective_tables`** [L30-43]: `def test_effective_tables()`
- **test `test_tables_refuse_a_changed_stage_c_contract`** [L46-54]: `def test_tables_refuse_a_changed_stage_c_contract(monkeypatch)`
- **test `test_row_for_d_patterns`** [L62-64]: `def test_row_for_d_patterns(name, key)` decorators: @pytest.mark.parametrize('name,key', [('hwsc-dry-0177', 'hwsc-dry-<job>'), ('test_hwsc-0190', 'test_hwsc-<job>'), ('hwsd-dry-0201', 'hwsd-dry-<job>'), ('hwsd-kd-0300', 'hwsd-kd-<job>'), ('test_hwsd-0197', 'test_hwsd-<job>'), ('test_hwsu-0198', 'test_hwsu-<job>'), ('hwsu-dry', 'hwsu-*'), ('hwsu-job-1', 'hwsu-*'), ('hwsd-dry', 'hwsd-dry')])
- **test `test_row_for_d_none`** [L67-68]: `def test_row_for_d_none()`
- **function `_scratch`** [L71-83]: `def _scratch(tmp_path, monkeypatch=None) -> Path`
- **test `test_scratch_scan_d`** [L86-101]: `def test_scratch_scan_d(tmp_path, monkeypatch)`
- **function `_dry_store`** [L104-114]: `def _dry_store(sc: Path, name='hwsd-dry') -> Path`
- **function `_recs`** [L117-118]: `def _recs(sc: Path, name: str) -> dict`
- **test `test_dry_class_d`** [L121-144]: `def test_dry_class_d(tmp_path)`
- **function `_check`** [L147-148]: `def _check(sc, **kw)`
- **test `test_scratch_check_d_clean_and_fail_closed`** [L151-159]: `def test_scratch_check_d_clean_and_fail_closed(tmp_path)`
- **test `test_scratch_check_d_incomplete`** [L164-168]: `def test_scratch_check_d_incomplete(tmp_path, plant)` decorators: @pytest.mark.parametrize('plant', ['newdir/h.npz', 'hwsd-kd-0300/x.npz', 'top.npz', 'hwsc-job-0181/a.npz', 'hwsd-dry-0202/stray/x.npz'])
- **test `test_scratch_check_d_to_freeze_row_without_files`** [L171-174]: `def test_scratch_check_d_to_freeze_row_without_files(tmp_path)`
- **test `test_scratch_check_d_hwsu_needs_r10`** [L177-181]: `def test_scratch_check_d_hwsu_needs_r10(tmp_path)`
- **test `test_scratch_check_d_blinded_rows`** [L184-192]: `def test_scratch_check_d_blinded_rows(tmp_path)`
- **function `_root_tree`** [L195-199]: `def _root_tree(tmp_path) -> Path`
- **test `test_inventory_d`** [L202-214]: `def test_inventory_d(tmp_path)`
- **function `_src`** [L220-225]: `def _src(digests=(), lineage=False, other=False)`
- **function `_sources`** [L228-237]: `def _sources(own=None, sup=PASS)`
- **function `_syn`** [L240-243]: `def _syn(tmp_path)`
- **test `test_build_d_wrapper_and_precedence`** [L249-272]: `def test_build_d_wrapper_and_precedence(tmp_path, own, sup, want)` decorators: @pytest.mark.parametrize('own,sup,want', [(None, PASS, PASS), ('lineage', PASS, LIN), ('other', PASS, INC), (None, INC, INC), ('lineage', INC, LIN)])
- **test `test_build_d_refusals_and_load_d_lineage`** [L275-288]: `def test_build_d_refusals_and_load_d_lineage(tmp_path)`
- **test `test_build_d_composite_own_and_reader_tags`** [L293-330]: `def test_build_d_composite_own_and_reader_tags(tmp_path, monkeypatch, r9, r10, want)` decorators: @pytest.mark.parametrize('r9,r10,want', [(PASS, PASS, PASS), (PASS, INC, INC), (LIN, PASS, LIN), (INC, PASS, INC)])

