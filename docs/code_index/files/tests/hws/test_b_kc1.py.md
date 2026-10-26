# `tests/hws/test_b_kc1.py`

- Source: [tests/hws/test_b_kc1.py](../../../../../tests/hws/test_b_kc1.py)
- Kind: python
- Lines: 340

## Module docstring

> Author B (job 0119), TEST_PLAN §3 `test_b_kc1.py` (KC1, DR7, RC-2) plus the G0 seed-scope
> search of `test_b_records.py` (§6.6, choice 33, ruling R-0118-5), which shares the "never opened"
> proof: patched `open`/`io.open`/`Path.open`/`os.open`/`np.load` record every touched path.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 33, via sys.path edit)
- `import hws_exact` -> [tools/hws/hws_exact.py](../../tools/hws/hws_exact.py.md) (line 34, via sys.path edit)
- `import hws_driver` -> [tools/hws/hws_driver.py](../../tools/hws/hws_driver.py.md) (line 35, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, SeedTree, canonical_json, make_artifact_id` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 37, via package root)
- `from topo_pilot.process import EmissionConfig, ProcessStage, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 44, via package root)
- `from topo_pilot.world import WorldConfig, WorldStage` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 45, via package root)

### External (third-party)

- `numpy` (lines 26)
- `pytest` (lines 27)

### Standard library

- `__future__` (lines 15)
- `builtins` (lines 17)
- `hashlib` (lines 18)
- `io` (lines 19)
- `json` (lines 20)
- `os` (lines 21)
- `pathlib` (lines 24)
- `shutil` (lines 22)
- `sys` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 31: `str(REPO / 'tools' / 'hws')` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `DECLARED`
- `FAIL`
- `FORBIDDEN`
- `OUTSIDE`
- `P`
- `PLANT`
- `REPO`
- `SEEDS`
- `SKIPPED`
- `TAMPERS`

## Classes and functions

- **function `_sha`** [L53-54]: `def _sha(path) -> str`
- **function `_status`** [L57-62]: `def _status(fn, *args, **kwargs) -> str` - A KC1 failure may come back as a status or as a raised HwsStop; both are accepted.
- **function `_guard`** [L65-99]: `def _guard(monkeypatch, touched, bad)` - Record (and refuse) every open of a path for which `bad(path)` is true.
- **function `base`** [L105-115]: `def base(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `_store`** [L118-127]: `def _store(base, dest: Path, unreadable=False) -> dict`
- **function `_seal`** [L130-143]: `def _seal(st, manifest_edit=None, config_edit=None)`
- **function `_edit`** [L146-153]: `def _edit(st, index, filename, fn)`
- **function `_set`** [L156-163]: `def _set(*path_and_value)`
- **function `_run`** [L166-167]: `def _run(st)`
- **test `test_synthetic_store_reproduces_the_contract_identities`** [L198-200]: `def test_synthetic_store_reproduces_the_contract_identities(base)`
- **test `test_expected_envelope_reproduces_process_stage`** [L203-220]: `def test_expected_envelope_reproduces_process_stage(base)`
- **test `test_identity_passes_without_touching_any_payload`** [L224-242]: `def test_identity_passes_without_touching_any_payload(base, tmp_path, monkeypatch, unreadable)` decorators: @pytest.mark.parametrize('unreadable', [False, True])
- **test `test_each_tamper_fails`** [L246-254]: `def test_each_tamper_fails(base, tmp_path, monkeypatch, name)` decorators: @pytest.mark.parametrize('name', sorted(TAMPERS))
- **test `test_read_json_refuses_other_files`** [L257-273]: `def test_read_json_refuses_other_files(tmp_path, monkeypatch)`
- **test `test_seed_search_skips_and_never_opens_excluded_paths`** [L294-308]: `def test_seed_search_skips_and_never_opens_excluded_paths(tmp_path, monkeypatch)`
- **function `_hits`** [L323-324]: `def _hits(paths)`
- **test `test_classify_seed_hits_declarations_pass`** [L330-332]: `def test_classify_seed_hits_declarations_pass()`
- **test `test_classify_seed_hits_fails_closed_outside`** [L336-340]: `def test_classify_seed_hits_fails_closed_outside(outside)` decorators: @pytest.mark.parametrize('outside', OUTSIDE)

