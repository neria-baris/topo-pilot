# `tests/k4b/test_b_registry.py`

- Source: [tests/k4b/test_b_registry.py](../../../../../tests/k4b/test_b_registry.py)
- Kind: python
- Lines: 368

## Module docstring

> Author B, K4b TEST_PLAN B2, B15, B16, B17 (registry side): recursive inventory and the
> NOT_SCANNED/INCOMPLETE classes, C1'-style digest columns (d1, d2 incl. superseded/), the D-2a
> reader that never opens sealed tokens, handoff-JSON pre-validation, the non-default artifact
> root with an explicit store, and the manifest/load round trip.

## Imports

### Internal (repo files)

- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../../tools/c1prime_registry/c1_registry_sources.py.md) (line 29, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 30, via sys.path edit)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 31, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 32, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 278, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 279, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 26)
- `pytest` (lines 27)

### Standard library

- `__future__` (lines 9)
- `builtins` (lines 11)
- `hashlib` (lines 12)
- `io` (lines 13)
- `json` (lines 14)
- `os` (lines 15)
- `pathlib` (lines 17)
- `sys` (lines 16)
- `types` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `INCOMPLETE`
- `POOLS`
- `REPO`
- `SEALED`

## Classes and functions

- **function `sha`** [L39-40]: `def sha(path) -> str`
- **function `dig`** [L43-44]: `def dig(i) -> str`
- **function `outcome`** [L47-53]: `def outcome(fn, *args, **kwargs)` - (status, result): a refusal raised as C1GateFailure or a returned status dict.
- **function `entry`** [L56-60]: `def entry(mapping, root, name)`
- **function `names`** [L63-64]: `def names(paths) -> set`
- **function `inventory_root`** [L69-79]: `def inventory_root(tmp_path) -> Path`
- **test `test_inventory_is_recursive_and_counts_worktrees_and_temp_dirs`** [L82-91]: `def test_inventory_is_recursive_and_counts_worktrees_and_temp_dirs(tmp_path)`
- **test `test_classify_not_scanned_only_with_inventory_reason`** [L94-105]: `def test_classify_not_scanned_only_with_inventory_reason(tmp_path)`
- **function `c1prime_store`** [L110-130]: `def c1prime_store(root: Path, with_object=True) -> tuple[Path, set]`
- **test `test_source_d_reads_digest_list_and_columns_incl_superseded`** [L133-142]: `def test_source_d_reads_digest_list_and_columns_incl_superseded(tmp_path, monkeypatch)`
- **test `test_source_d_refuses_unbound_registry_v1`** [L145-148]: `def test_source_d_refuses_unbound_registry_v1(tmp_path)`
- **function `d2a_store`** [L153-167]: `def d2a_store(root: Path, with_meta=True) -> Path`
- **test `test_source_e_never_opens_sealed_token_arrays`** [L170-203]: `def test_source_e_never_opens_sealed_token_arrays(tmp_path, monkeypatch)`
- **test `test_source_e_unresolved_pool_inventory_is_incomplete`** [L206-209]: `def test_source_e_unresolved_pool_inventory_is_incomplete(tmp_path)`
- **function `mailbox`** [L214-222]: `def mailbox(tmp_path, bad=False) -> Path`
- **test `test_validate_handoff_json_reports_parse_failure`** [L225-231]: `def test_validate_handoff_json_reports_parse_failure(tmp_path)`
- **test `test_source_c_malformed_json_refused_never_empty`** [L234-238]: `def test_source_c_malformed_json_refused_never_empty(tmp_path)`
- **test `test_source_c_valid_mailbox_delegates_unchanged`** [L241-249]: `def test_source_c_valid_mailbox_delegates_unchanged(tmp_path)`
- **function `artifact_root`** [L254-262]: `def artifact_root(tmp_path) -> Path`
- **test `test_source_a_non_default_root_without_store_refused`** [L265-274]: `def test_source_a_non_default_root_without_store_refused(tmp_path, monkeypatch)`
- **test `test_source_a_explicit_store_reads_that_root`** [L277-305]: `def test_source_a_explicit_store_reads_that_root(tmp_path, monkeypatch)`
- **function `build_root`** [L310-328]: `def build_root(tmp_path, monkeypatch) -> Path`
- **test `test_build_on_synthetic_root_is_incomplete_and_written_once`** [L331-359]: `def test_build_on_synthetic_root_is_incomplete_and_written_once(tmp_path, monkeypatch)`
- **test `test_build_refuses_unknown_version`** [L362-368]: `def test_build_refuses_unknown_version(tmp_path, monkeypatch)`

