# `tests/hwsc/test_b_registry2.py`

- Source: [tests/hwsc/test_b_registry2.py](../../../../../tests/hwsc/test_b_registry2.py)
- Kind: python
- Lines: 374

## Module docstring

> Author B (job 0176): R6 scratch scan/check, R8 inventory, registry build, H2-FRESH.
> (H2 separation_c is in test_b_streams.py for the 400-line limit.)

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 24, via sys.path edit)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 25, via sys.path edit)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../tools/hwsc/hwsc_registry.py.md) (line 26, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 27, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 28, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 29, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 30, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 31, via unique basename)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `R6_DEFECTS`
- `REPO`
- `SOURCE_NAMES`
- `_HWSC`
- `_REC`

## Classes and functions

- **function `_audit`** [L37-39]: `def _audit(event, args)`
- **function `rec`** [L46-50]: `def rec()` decorators: @pytest.fixture
- **function `_hist`** [L53-56]: `def _hist(path, rows=5, seed=0)`
- **function `_find`** [L59-60]: `def _find(entries, suffix)`
- **function `scratch`** [L65-82]: `def scratch(tmp_path)` decorators: @pytest.fixture
- **test `test_r6_scan_classes_and_pruning`** [L85-105]: `def test_r6_scan_classes_and_pruning(scratch, rec, monkeypatch)`
- **function `_rows`** [L108-119]: `def _rows(scratch, overrides)` - A table whose frozen_files are written from the header scan, as at the freeze.
- **function `_check`** [L122-123]: `def _check(scratch, table, readers_ok=())`
- **test `test_r6_check_baseline_pass`** [L126-131]: `def test_r6_check_baseline_pass(tmp_path)`
- **test `test_r6_defects_are_incomplete`** [L142-148]: `def test_r6_defects_are_incomplete(tmp_path, name)` decorators: @pytest.mark.parametrize('name', list(R6_DEFECTS))
- **test `test_r6_reader_row_needs_its_reader`** [L151-157]: `def test_r6_reader_row_needs_its_reader(tmp_path)`
- **test `test_r6_fixture_max_rows`** [L161-165]: `def test_r6_fixture_max_rows(tmp_path, rows, status)` decorators: @pytest.mark.parametrize('rows,status', [(1000, 'PASS'), (2000, INCOMPLETE)])
- **test `test_r6_stage_b_folders_full_walk_and_empty_rows`** [L168-178]: `def test_r6_stage_b_folders_full_walk_and_empty_rows(tmp_path)`
- **test `test_r8_inventory_against_a_synthetic_table`** [L182-198]: `def test_r8_inventory_against_a_synthetic_table(tmp_path, monkeypatch)`
- **function `_hexes`** [L202-204]: `def _hexes(seed, n=3)`
- **function `_src`** [L207-211]: `def _src(digests=(), status='PASS', seq=())`
- **function `stubs`** [L218-250]: `def stubs(tmp_path, monkeypatch)` decorators: @pytest.fixture
- **function `_build`** [L253-259]: `def _build(tmp_path, version, sources, **kw)`
- **test `test_build_k_reg1_loads_unchanged`** [L262-274]: `def test_build_k_reg1_loads_unchanged(tmp_path, stubs)`
- **test `test_build_status_precedence`** [L281-283]: `def test_build_status_precedence(tmp_path, stubs, planted, status)` decorators: @pytest.mark.parametrize('planted,status', [({'c2nd': LINEAGE}, LINEAGE), ({'dry': INCOMPLETE}, INCOMPLETE), ({'scratch': INCOMPLETE, 'hwsb': LINEAGE}, LINEAGE), ({'own': INCOMPLETE}, INCOMPLETE), ({'hws': INCOMPLETE}, INCOMPLETE)])
- **test `test_build_x6_lineage_and_inventory_violation`** [L286-292]: `def test_build_x6_lineage_and_inventory_violation(tmp_path, stubs)`
- **function `_tables`** [L295-302]: `def _tables(n=600, seed=0)`
- **test `test_build_extra_only_for_k_reg2`** [L305-314]: `def test_build_extra_only_for_k_reg2(tmp_path, stubs)`
- **test `test_build_rehearsal_refusals_and_exclusivity`** [L317-328]: `def test_build_rehearsal_refusals_and_exclusivity(tmp_path, stubs)`
- **function `fresh`** [L333-351]: `def fresh(tmp_path, stubs)` decorators: @pytest.fixture
- **test `test_h2_fresh_clean_pass`** [L354-357]: `def test_h2_fresh_clean_pass(fresh)`
- **test `test_h2_fresh_test_digest_in_k_reg2_is_lineage`** [L360-364]: `def test_h2_fresh_test_digest_in_k_reg2_is_lineage(fresh)`
- **test `test_h2_fresh_interrupted_reservation_stops`** [L367-374]: `def test_h2_fresh_interrupted_reservation_stops(fresh)`

