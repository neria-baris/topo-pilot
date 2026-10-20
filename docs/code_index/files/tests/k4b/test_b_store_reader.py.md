# `tests/k4b/test_b_store_reader.py`

- Source: [tests/k4b/test_b_store_reader.py](../../../../../tests/k4b/test_b_store_reader.py)
- Kind: python
- Lines: 294

## Module docstring

> Author B, correction round 4: coordinator ruling R28 (API §16, defect D5). K4b's own store
> `k4b-store` gets the dedicated reader "k": `source_k(store_root) -> {"sources", "derived", "other",
> "status"}`. Derived registry lineage records (registry/K-REG*.json, registry/K-REG*_digests.npz,
> the same under superseded/*/registry/) are listed in `derived` with their sha256, contribute
> nothing and are never INCOMPLETE. History-bearing npz under stages/ and superseded/*/stages/ are
> `sources`, with their sha256. Any other history-bearing, identity-bearing or unreadable file is
> `other` and makes the k4b-store class INCOMPLETE through `build`. `OWN_READERS["k4b-store"] == "k"`
> keeps it out of the generic deep scan. A raising `source_k` makes k4b-store INCOMPLETE, never an
> empty contribution.

## Imports

### Internal (repo files)

- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 38, via sys.path edit)
- `import test_b_registry_fixes` -> [tests/k4b/test_b_registry_fixes.py](test_b_registry_fixes.py.md) (line 39, via same directory)

### External (third-party)

- `numpy` (lines 35)
- `pytest` (lines 36)

### Standard library

- `__future__` (lines 18)
- `builtins` (lines 20)
- `hashlib` (lines 21)
- `io` (lines 22)
- `json` (lines 23)
- `os` (lines 24)
- `pathlib` (lines 26)
- `sys` (lines 25)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 33: `str(_p)` -> `tests/k4b`, `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CLEAN`
- `HERE`
- `INCOMPLETE`
- `KS`
- `REPO`
- `STRAYS`

## Classes and functions

- **function `put`** [L46-49]: `def put(path: Path, **arrays) -> Path`
- **function `sha`** [L52-53]: `def sha(path: Path) -> str`
- **function `text`** [L56-59]: `def text(path: Path, body: str) -> Path`
- **function `derived_files`** [L62-72]: `def derived_files(store: Path) -> list` - The three D5 lineage records: K-REG1 manifest and digests, and the superseded digests.
- **function `free_files`** [L75-80]: `def free_files(store: Path) -> None` - Category (c): not history files, ignored.
- **function `stage_tables`** [L83-88]: `def stage_tables(store: Path) -> list`
- **function `stray`** [L91-99]: `def stray(path: Path, kind: str) -> Path`
- **function `names_file`** [L102-116]: `def names_file(item, store: Path, path: Path) -> bool`
- **function `find`** [L119-120]: `def find(items, store: Path, path: Path) -> list`
- **function `has_sha`** [L123-124]: `def has_sha(item, path: Path) -> bool`
- **function `is_under`** [L127-132]: `def is_under(path, base: Path) -> bool`
- **function `entry`** [L135-139]: `def entry(mapping, root: Path, name: str)`
- **test `test_derived_registry_records_are_listed_with_sha256`** [L144-157]: `def test_derived_registry_records_are_listed_with_sha256(tmp_path)`
- **test `test_stage_history_tables_are_sources_with_sha256`** [L160-173]: `def test_stage_history_tables_are_sources_with_sha256(tmp_path)`
- **test `test_stray_file_is_other_and_not_clean`** [L184-192]: `def test_stray_file_is_other_and_not_clean(tmp_path, rel, kind)` decorators: @pytest.mark.parametrize('rel,kind', STRAYS)
- **function `spy`** [L197-214]: `def spy(mp, seen: list) -> None`
- **test `test_own_readers_excludes_k4b_store_from_the_deep_scan`** [L217-234]: `def test_own_readers_excludes_k4b_store_from_the_deep_scan(tmp_path, monkeypatch)`
- **function `k4b_class`** [L239-243]: `def k4b_class(manifest, root: Path) -> dict`
- **test `test_build_with_only_derived_records_is_not_incomplete`** [L246-255]: `def test_build_with_only_derived_records_is_not_incomplete(tmp_path, monkeypatch)`
- **test `test_build_with_stray_file_makes_k4b_store_incomplete`** [L259-268]: `def test_build_with_stray_file_makes_k4b_store_incomplete(tmp_path, monkeypatch, kind)` decorators: @pytest.mark.parametrize('kind', ['ids', 'tokens'])
- **test `test_raising_source_k_makes_k4b_store_incomplete`** [L272-294]: `def test_raising_source_k_makes_k4b_store_incomplete(tmp_path, monkeypatch, exc)` decorators: @pytest.mark.parametrize('exc', [OSError, RuntimeError])

