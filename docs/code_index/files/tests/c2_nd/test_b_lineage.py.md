# `tests/c2_nd/test_b_lineage.py`

- Source: [tests/c2_nd/test_b_lineage.py](../../../../../tests/c2_nd/test_b_lineage.py)
- Kind: python
- Lines: 399

## Module docstring

> Author B, T-NAMESPACE-ND (protocol §6.6, RC-11; split here from test_b_registry.py),
> T-G0-ND (§3 row 1), T-METER (§9, §6.8) and T-SIZE (§11.3); API.md §4.2-§4.3, §9.3, §9.5,
> §9.8, §12. Synthetic worktrees, stores and project roots under pytest's tmp_path only.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 17, via sys.path edit)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 20, via unique basename)
- `import nd_data` -> [tools/c2_nd/nd_data.py](../../tools/c2_nd/nd_data.py.md) (line 21, via sys.path edit)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](../../tools/c2_nd/nd_driver.py.md) (line 22, via sys.path edit)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](../../tools/c2_nd/nd_registry.py.md) (line 23, via sys.path edit)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 24)
- `pytest` (lines 25)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `hashlib` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 15: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `C2`
- `HWS`
- `ND`
- `PKG`
- `REPO`

## Classes and functions

- **function `sha`** [L37-38]: `def sha(path)`
- **function `put`** [L41-44]: `def put(path, data)`
- **function `world`** [L48-62]: `def world(tmp_path, monkeypatch)` decorators: @pytest.fixture
- **function `classes`** [L66-67]: `def classes(res)`
- **test `test_namespace_scan`** [L70-81]: `def test_namespace_scan(world)`
- **test `test_namespace_hit_in_a_parallel_store_is_foreign`** [L84-90]: `def test_namespace_hit_in_a_parallel_store_is_foreign(world)`
- **test `test_hygiene_check`** [L101-109]: `def test_hygiene_check(world, where, needle, want)` decorators: @pytest.mark.parametrize('where, needle, want', [('WORKTREE/tools/c2_nd/CONTRACT.json', C2, LIN), ('STORE/stages/S1/record.json', C2, LIN), ('STORE/GATES.jsonl', C2, LIN), ('STORE/stages/S1/notes.json', HWS, LIN), ('WORKTREE/tools/c2_nd/PROTOCOL_C2ND_v1.md', C2, 'PASS'), ('STORE/stages/S1/record.json', ND, 'PASS')])
- **test `test_needles_and_the_real_contract`** [L112-118]: `def test_needles_and_the_real_contract()`
- **test `test_store_admission_payload_at_first_sampling`** [L121-130]: `def test_store_admission_payload_at_first_sampling(world)`
- **function `fit_keys`** [L134-141]: `def fit_keys()`
- **function `dec_keys`** [L144-146]: `def dec_keys()`
- **function `c2_store_files`** [L149-166]: `def c2_store_files(world, monkeypatch, drop=None)` - A synthetic C2 store whose files re-hash to the (in-place patched) CONTRACT table.
- **function `g0_world`** [L169-180]: `def g0_world(world, monkeypatch, drop=None, dry=False, freeze_ok=True)`
- **function `loads`** [L184-192]: `def loads(monkeypatch)` decorators: @pytest.fixture
- **test `test_g0_items_on_a_synthetic_world`** [L197-204]: `def test_g0_items_on_a_synthetic_world(world, monkeypatch, loads)`
- **test `test_g0_protocol_contract_and_c2_store_failures`** [L207-215]: `def test_g0_protocol_contract_and_c2_store_failures(world, monkeypatch)`
- **test `test_g0_fit_key_set`** [L218-220]: `def test_g0_fit_key_set(world, monkeypatch)`
- **test `test_g0_store_admission_and_dry_guard`** [L223-228]: `def test_g0_store_admission_and_dry_guard(world, monkeypatch)`
- **function `auth_record`** [L231-240]: `def auth_record(schema, **change)`
- **test `test_auth_ok`** [L243-253]: `def test_auth_ok(tmp_path)`
- **test `test_contract_values`** [L256-275]: `def test_contract_values()`
- **test `test_sequence_ids_and_streams`** [L278-302]: `def test_sequence_ids_and_streams()`
- **test `test_meter_bind_check`** [L306-316]: `def test_meter_bind_check(world)`
- **test `test_measure_only_caps`** [L321-322]: `def test_measure_only_caps()`
- **function `lineage_ctx`** [L325-333]: `def lineage_ctx(tmp_path)`
- **test `test_write_manifest`** [L336-347]: `def test_write_manifest(tmp_path)`
- **test `test_supersede_and_regen_compare`** [L350-365]: `def test_supersede_and_regen_compare(tmp_path)`
- **test `test_parallel_x6zc_non_history_names`** [L373-387]: `def test_parallel_x6zc_non_history_names(tmp_path, monkeypatch, loads, names, bad)` decorators: @pytest.mark.parametrize('names, bad', [(('stages/A-r1/qstar_NA.npz', 'stages/B-r2/m1/pairs.npz'), ('stages/A-rx/qstar_NA.npz', 'stages/A-r1/other.npz')), (('stages/B/AB-s1/p.npz', 'stages/C-r1/ZC-s1/p.npz'), ('stages/B/AB-s1/q.npz',))]) - X6ZC NON_HISTORY names in any attempt directory: listed, never opened; others fail.
- **test `test_module_files_and_sizes`** [L391-399]: `def test_module_files_and_sizes()`

