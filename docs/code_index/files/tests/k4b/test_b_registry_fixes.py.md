# `tests/k4b/test_b_registry_fixes.py`

- Source: [tests/k4b/test_b_registry_fixes.py](../../../../../tests/k4b/test_b_registry_fixes.py)
- Kind: python
- Lines: 248

## Module docstring

> Author B, correction round 3 (ruling R26, jobs/0051/review.md). D2: `validate_handoff_json`
> (API §3, RC7) accepts a UTF-8 BOM like the reused `utf-8-sig` reader; malformed JSON still fails
> and `source_c` refuses it (INCONCLUSIVE/REGISTRY_INCOMPLETE). D3: coverage revalidation uses the
> sequence ids the source-(a) readers populated (`seqs` is filled lazily inside each reader), via the
> pinned `revalidate_coverage(root_art, root)` and `build` on a synthetic root holding every file
> `store_sources`/`coverage` read. Unpinned: the nesting of manifest `coverage` and the item format
> of `missing`; the tests find the reused report (the dict holding `x4b_seq_in_a`) anywhere in it
> and require the missing id's decimal text. ArtifactStore.load is monkeypatched as in
> test_b_registry.

## Imports

### Internal (repo files)

- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../../tools/c1prime_registry/c1_registry_sources.py.md) (line 28, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 29, via sys.path edit)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 30, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 131, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 25)
- `pytest` (lines 26)

### Standard library

- `__future__` (lines 11)
- `hashlib` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 16)
- `sys` (lines 15)
- `types` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/k4b/test_b_store_reader.py](test_b_store_reader.py.md) (line 39, import)

## Top-level constants

- `GONE`
- `INCOMPLETE`
- `POOLS`
- `REFS`
- `REPO`
- `SEALED`
- `SEQ`
- `SEQ_MISS`

## Classes and functions

- **function `put`** [L42-45]: `def put(path: Path, **arrays) -> Path`
- **function `write_json`** [L48-52]: `def write_json(path: Path, obj, bom=False, text=None) -> Path`
- **function `mailbox`** [L57-62]: `def mailbox(base: Path, bom=False, bad=None) -> Path`
- **test `test_handoff_json_with_or_without_bom_passes`** [L66-70]: `def test_handoff_json_with_or_without_bom_passes(tmp_path, bom)` decorators: @pytest.mark.parametrize('bom', [True, False])
- **test `test_bom_json_contributes_through_source_c_like_the_reused_reader`** [L73-79]: `def test_bom_json_contributes_through_source_c_like_the_reused_reader(tmp_path)`
- **test `test_truncated_json_is_registry_incomplete`** [L83-90]: `def test_truncated_json_is_registry_incomplete(tmp_path, bad_bom)` decorators: @pytest.mark.parametrize('bad_bom', [False, True])
- **function `dig`** [L95-96]: `def dig(i) -> str`
- **function `earlier_stores`** [L99-127]: `def earlier_stores(root: Path) -> None` - Every file store_sources and coverage read, with consistent identity references.
- **function `artifacts`** [L130-151]: `def artifacts(root: Path, seq: np.ndarray, monkeypatch) -> Path`
- **function `coverage_root`** [L154-179]: `def coverage_root(tmp_path, monkeypatch, seq) -> tuple[Path, Path]`
- **function `dicts`** [L182-188]: `def dicts(obj)`
- **function `build_manifest`** [L191-200]: `def build_manifest(tmp_path, root) -> dict`
- **function `reports`** [L203-206]: `def reports(manifest) -> list`
- **test `test_revalidate_coverage_complete_when_source_a_ids_cover_refs`** [L211-214]: `def test_revalidate_coverage_complete_when_source_a_ids_cover_refs(tmp_path, monkeypatch)`
- **test `test_revalidate_coverage_reports_the_removed_id`** [L217-223]: `def test_revalidate_coverage_reports_the_removed_id(tmp_path, monkeypatch)`
- **test `test_build_coverage_complete_with_no_seq_in_a_problem`** [L228-238]: `def test_build_coverage_complete_with_no_seq_in_a_problem(tmp_path, monkeypatch)`
- **test `test_build_coverage_reports_the_missing_id`** [L241-248]: `def test_build_coverage_reports_the_missing_id(tmp_path, monkeypatch)`

