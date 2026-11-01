# `tests/hwsd/test_b_guard_search.py`

- Source: [tests/hwsd/test_b_guard_search.py](../../../../../tests/hwsd/test_b_guard_search.py)
- Kind: python
- Lines: 242

## Module docstring

> Author B: blindness guard, J9 search pruning, G0d needles and declarations (§9.2, J5, J9).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 13, via sys.path edit)
- `import hwsd_known` -> [tools/hwsd/hwsd_known.py](../../tools/hwsd/hwsd_known.py.md) (line 14, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 15, via same directory)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 17, via unique basename)

### External (third-party)

- `pytest` (lines 18)

### Standard library

- `__future__` (lines 3)
- `json` (lines 5)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `BLIND`
- `DECLARED`
- `FALSE_REL`
- `PRUNED`
- `PRUNED_FILES`
- `SEARCHABLE`
- `TP`
- `TRUE_REL`

## Classes and functions

- **function `roots`** [L44-45]: `def roots(tmp_path)` decorators: @pytest.fixture
- **test `test_blinded_true`** [L49-53]: `def test_blinded_true(roots, rel)` decorators: @pytest.mark.parametrize('rel', TRUE_REL)
- **test `test_blinded_false`** [L57-59]: `def test_blinded_false(roots, rel)` decorators: @pytest.mark.parametrize('rel', FALSE_REL)
- **test `test_blinded_scratch_job_folders`** [L62-69]: `def test_blinded_scratch_job_folders(roots)`
- **test `test_search_pruned_hwsu_searchable`** [L81-84]: `def test_search_pruned_hwsu_searchable(roots, rel)` decorators: @pytest.mark.parametrize('rel', SEARCHABLE)
- **test `test_search_pruned_true`** [L88-90]: `def test_search_pruned_true(roots, rel)` decorators: @pytest.mark.parametrize('rel', PRUNED + TRUE_REL[:4])
- **test `test_public_summary`** [L93-96]: `def test_public_summary()`
- **test `test_guard_refuses_before_any_open`** [L99-111]: `def test_guard_refuses_before_any_open(tmp_path, monkeypatch)`
- **function `_root`** [L114-138]: `def _root(tmp_path) -> tuple[Path, Path]`
- **test `test_seed_search_d_prunes_before_opening`** [L147-161]: `def test_seed_search_d_prunes_before_opening(tmp_path, monkeypatch)`
- **test `test_seed_search_d_equals_stage_c_search_without_pruned_paths`** [L164-176]: `def test_seed_search_d_equals_stage_c_search_without_pruned_paths(tmp_path, monkeypatch)`
- **function `_ns`** [L179-182]: `def _ns() -> dict`
- **test `test_needles_d_from_the_namespace_record`** [L185-191]: `def test_needles_d_from_the_namespace_record()`
- **test `test_overlap_check`** [L194-205]: `def test_overlap_check()`
- **function `_classify`** [L224-226]: `def _classify(hits)`
- **test `test_j9_fragments_classify_declarations`** [L229-233]: `def test_j9_fragments_classify_declarations()`
- **test `test_j9_tokens_elsewhere_are_unclassified`** [L239-242]: `def test_j9_tokens_elsewhere_are_unclassified(path)` decorators: @pytest.mark.parametrize('path', [f'{TP}/topo-pilot/src/x.py', f'{TP}/topo-pilot/tools/hwsc/x.py', 'X:/Downloads/topo-scratch/0089/a.json', f'{TP}/hwsc-store/stages/S8/RESULT.json'])

