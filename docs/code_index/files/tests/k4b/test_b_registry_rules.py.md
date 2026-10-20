# `tests/k4b/test_b_registry_rules.py`

- Source: [tests/k4b/test_b_registry_rules.py](../../../../../tests/k4b/test_b_registry_rules.py)
- Kind: python
- Lines: 400

## Module docstring

> Author B, round 2: coordinator ruling R23 (API §15), the registry classification amendments to
> `k4b_registry.inventory`/`classify`/`build`, on synthetic trees under tmp_path. Rule 1:
> ObservationSet stores with own payloads are SCANNED via source (f) (raw tokens[:, :32] when no
> EmissionSpec perm resolves); a stray history file outside the ObservationSet root → INCOMPLETE.
> Rule 2: "synthetic test fixtures" only under a basetemp segment with ≤ 1,024 header rows. Rule 3:
> main inventoried deep (tests/, .venv). Rule 4: unreadable files are fixtures only inside a
> basetemp segment. Rule 5: dedicated-reader directories are not deep-scanned; no sealed D-2a array
> is opened. Basetemp segments are judged on the path relative to the inventoried root (tmp_path
> itself lies under pytest's basetemp). `classify` gets an empty `scanned_readers` mapping (as in
> round 1); every npz is built here with numpy; header reads suffice for every expectation.

## Imports

### Internal (repo files)

- `import c1_data` -> [tools/c1prime/c1_data.py](../../tools/c1prime/c1_data.py.md) (line 31, via sys.path edit)
- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../../tools/c1prime_registry/c1_registry_sources.py.md) (line 32, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 33, via sys.path edit)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 34, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 35, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 236, via package root) (inside a function)
- `from topo_pilot.contracts.testing import tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 237, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 28)
- `pytest` (lines 29)

### Standard library

- `__future__` (lines 12)
- `builtins` (lines 14)
- `hashlib` (lines 15)
- `io` (lines 16)
- `json` (lines 17)
- `os` (lines 18)
- `pathlib` (lines 20)
- `sys` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `DEDICATED`
- `FIXTURES`
- `OUTSIDE`
- `POOLS`
- `REPO`
- `SEALED`
- `SEGMENTS`

## Classes and functions

- **function `entry`** [L43-47]: `def entry(mapping, root, name)`
- **function `names`** [L50-51]: `def names(paths) -> set`
- **function `is_under`** [L54-59]: `def is_under(path, base) -> bool`
- **function `put`** [L62-65]: `def put(path: Path, **arrays) -> Path`
- **function `hist`** [L68-69]: `def hist(path: Path, rows: int, cols: int = 33, key: str = 'tokens') -> Path`
- **function `junk`** [L72-74]: `def junk(path: Path) -> None`
- **function `truncated`** [L77-80]: `def truncated(path: Path) -> None`
- **function `note`** [L83-85]: `def note(d: Path) -> None`
- **function `classify_root`** [L88-90]: `def classify_root(root)`
- **function `klass`** [L93-94]: `def klass(root, name) -> dict`
- **function `deep`** [L97-98]: `def deep(root: Path, top: str, segs) -> Path`
- **test `test_fixtures_in_a_basetemp_segment_are_not_scanned`** [L115-124]: `def test_fixtures_in_a_basetemp_segment_are_not_scanned(tmp_path, top, segs)` decorators: @pytest.mark.parametrize('top,segs', SEGMENTS)
- **test `test_fixture_with_more_than_1024_rows_is_incomplete`** [L130-135]: `def test_fixture_with_more_than_1024_rows_is_incomplete(tmp_path, key, rows, cols, dtype)` decorators: @pytest.mark.parametrize('key,rows,cols,dtype', [('tokens', 1025, 33, np.uint8), ('x', 1025, 32, np.int64), ('canon32', 4096, 32, np.uint8)])
- **test `test_one_large_array_in_a_small_file_is_incomplete`** [L138-143]: `def test_one_large_array_in_a_small_file_is_incomplete(tmp_path)`
- **test `test_history_outside_a_basetemp_segment_is_incomplete`** [L157-162]: `def test_history_outside_a_basetemp_segment_is_incomplete(tmp_path, top, segs)` decorators: @pytest.mark.parametrize('top,segs', OUTSIDE)
- **test `test_one_file_outside_the_segment_spoils_the_directory`** [L165-169]: `def test_one_file_outside_the_segment_spoils_the_directory(tmp_path)`
- **test `test_unreadable_file_inside_a_segment_counts_as_fixture`** [L175-181]: `def test_unreadable_file_inside_a_segment_counts_as_fixture(tmp_path, make)` decorators: @pytest.mark.parametrize('make', [junk, truncated])
- **test `test_unreadable_file_outside_a_segment_is_incomplete`** [L186-190]: `def test_unreadable_file_outside_a_segment_is_incomplete(tmp_path, make, segs)` decorators: @pytest.mark.parametrize('make', [junk, truncated]) @pytest.mark.parametrize('segs', [('export',), ('sub', 'bt2')])
- **function `main_tree`** [L195-203]: `def main_tree(root: Path) -> Path`
- **test `test_main_inventory_is_deep_including_tests_and_venv`** [L206-211]: `def test_main_inventory_is_deep_including_tests_and_venv(tmp_path)`
- **test `test_main_with_only_tests_venv_and_basetemp_fixtures_is_not_incomplete`** [L214-217]: `def test_main_with_only_tests_venv_and_basetemp_fixtures_is_not_incomplete(tmp_path)`
- **test `test_main_file_failing_rule_2a_prime_makes_main_incomplete`** [L227-230]: `def test_main_file_failing_rule_2a_prime_makes_main_incomplete(tmp_path, rel, rows)` decorators: @pytest.mark.parametrize('rel,rows', [(('scripts', 'out', 'h.npz'), 5), (('results', 'x4', 'hist.npz'), 5), (('a', 'b', 'c', 'd', 'e', 'f', 'deep.npz'), 3), (('tests', 'big.npz'), 1025), (('.venv', 'Lib', 'big.npz'), 2000)])
- **function `os_store`** [L235-243]: `def os_store(store: Path) -> np.ndarray`
- **test `test_observation_set_store_is_scanned_via_source_f`** [L249-263]: `def test_observation_set_store_is_scanned_via_source_f(tmp_path, top, sub)` decorators: @pytest.mark.parametrize('top,sub', [('x5g1-research-store', ('store',)), ('x5g1t-fixture-run', ('study', 'store')), ('x9-new-research-store', ('store',))])
- **test `test_stray_history_outside_the_os_root_is_incomplete`** [L267-271]: `def test_stray_history_outside_the_os_root_is_incomplete(tmp_path, stray)` decorators: @pytest.mark.parametrize('stray', [('exports', 'hist.npz'), ('study', 'cache', 'canon.npz')])
- **test `test_history_file_inside_the_os_root_counts_as_covered`** [L274-280]: `def test_history_file_inside_the_os_root_counts_as_covered(tmp_path)`
- **function `dig`** [L285-286]: `def dig(i) -> str`
- **function `c1prime_store`** [L289-298]: `def c1prime_store(root: Path) -> Path`
- **function `d2a_store`** [L301-312]: `def d2a_store(root: Path) -> Path`
- **function `mailbox`** [L315-319]: `def mailbox(root: Path) -> Path`
- **function `sealed`** [L322-327]: `def sealed(path, d2a: Path) -> bool`
- **function `guard`** [L330-351]: `def guard(monkeypatch, d2a: Path, seen: list) -> None` - Record every opened path; refuse (raise) on any sealed D-2a pool array.
- **test `test_dedicated_dirs_are_not_deep_scanned_by_the_inventory`** [L354-371]: `def test_dedicated_dirs_are_not_deep_scanned_by_the_inventory(tmp_path, monkeypatch)`
- **test `test_build_never_opens_a_sealed_pool_array`** [L374-400]: `def test_build_never_opens_a_sealed_pool_array(tmp_path, monkeypatch)`

