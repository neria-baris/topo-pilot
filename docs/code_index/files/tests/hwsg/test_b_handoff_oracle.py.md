# `tests/hwsg/test_b_handoff_oracle.py`

- Source: [tests/hwsg/test_b_handoff_oracle.py](../../../../../tests/hwsg/test_b_handoff_oracle.py)
- Kind: python
- Lines: 176

## Module docstring

> Author B: WORLD_HANDOFF and oracle identity/reproduction (protocol 2.6, O1, O3, O4).

## Imports

### Internal (repo files)

- `from test_b_common import CONTRACT, TAGS, expect_fail, mod, sha_bytes` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 15, via same directory)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 119, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)

### Standard library

- `__future__` (lines 2)
- `copy` (lines 4)
- `fractions` (lines 8)
- `importlib` (lines 5)
- `json` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 23: `k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md)

### sys.path additions

- line 14: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- `Z`

## Classes and functions

- **function `_handoff`** [L20-29]: `def _handoff(tag='hi', **over)`
- **function `_put`** [L32-39]: `def _put(tmp_path, h, tag='hi')` - Write bytes directly (bypasses write()) and return (store, sha).
- **test `test_contract_key_set_is_the_handoff_key_set`** [L42-43]: `def test_contract_key_set_is_the_handoff_key_set()`
- **test `test_write_load_round_trip`** [L47-60]: `def test_write_load_round_trip(tmp_path, tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **function `_bad_cases`** [L63-74]: `def _bad_cases()`
- **test `test_defective_handoff_fails_identity`** [L78-81]: `def test_defective_handoff_fails_identity(tmp_path, name)` decorators: @pytest.mark.parametrize('name', list(_bad_cases()))
- **test `test_sha_mismatch_and_absent_binding_fail_identity`** [L84-89]: `def test_sha_mismatch_and_absent_binding_fail_identity(tmp_path)`
- **test `test_default_sha_comes_from_o_stage_complete`** [L92-98]: `def test_default_sha_comes_from_o_stage_complete(tmp_path)`
- **test `test_as_hwsc_view`** [L101-113]: `def test_as_hwsc_view()`
- **function `lo_proc`** [L117-121]: `def lo_proc()` decorators: @pytest.fixture(scope='module')
- **test `test_process_sigma_neighbour_are_exact`** [L124-130]: `def test_process_sigma_neighbour_are_exact(lo_proc)`
- **test `test_identity_fails_on_planted_id_difference`** [L133-143]: `def test_identity_fails_on_planted_id_difference(lo_proc)`
- **test `test_identity_checker_compares_handoff_identities`** [L146-164]: `def test_identity_checker_compares_handoff_identities(lo_proc, monkeypatch)`
- **test `test_reproduce_wrong_table_fails_oracle`** [L167-176]: `def test_reproduce_wrong_table_fails_oracle(tmp_path)` - A synthetic stored table that is not the stage-A table cannot pass O4 (OPEN-2).

