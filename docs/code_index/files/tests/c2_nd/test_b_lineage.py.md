# `tests/c2_nd/test_b_lineage.py`

- Source: [tests/c2_nd/test_b_lineage.py](../../../../../tests/c2_nd/test_b_lineage.py)
- Kind: python
- Lines: 374

## Module docstring

> Author B, T-NAMESPACE-ND (protocol §6.6, RC-11; split here from test_b_registry.py),
> T-G0-ND (§3 row 1), T-METER (§9, §6.8) and T-SIZE (§11.3); API.md §4.2-§4.3, §9.3, §9.5,
> §9.8, §12. Synthetic worktrees, stores and project roots under pytest's tmp_path only.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 17, via sys.path edit)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 20, via unique basename)
- `import nd_data` -> [tools/c2_nd/nd_data.py](../../tools/c2_nd/nd_data.py.md) (line 21, via sys.path edit)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 27, via package root)

### External (third-party)

- `nd_driver` (lines 22)
- `numpy` (lines 23)
- `pytest` (lines 24)

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

- **function `sha`** [L36-37]: `def sha(path)`
- **function `put`** [L40-43]: `def put(path, data)`
- **function `world`** [L47-61]: `def world(tmp_path, monkeypatch)` decorators: @pytest.fixture
- **function `classes`** [L65-66]: `def classes(res)`
- **test `test_namespace_scan`** [L69-80]: `def test_namespace_scan(world)`
- **test `test_namespace_hit_in_a_parallel_store_is_foreign`** [L83-89]: `def test_namespace_hit_in_a_parallel_store_is_foreign(world)`
- **test `test_hygiene_check`** [L100-108]: `def test_hygiene_check(world, where, needle, want)` decorators: @pytest.mark.parametrize('where, needle, want', [('WORKTREE/tools/c2_nd/CONTRACT.json', C2, LIN), ('STORE/stages/S1/record.json', C2, LIN), ('STORE/GATES.jsonl', C2, LIN), ('STORE/stages/S1/notes.json', HWS, LIN), ('WORKTREE/tools/c2_nd/PROTOCOL_C2ND_v1.md', C2, 'PASS'), ('STORE/stages/S1/record.json', ND, 'PASS')])
- **test `test_needles_and_the_real_contract`** [L111-117]: `def test_needles_and_the_real_contract()`
- **test `test_store_admission_payload_at_first_sampling`** [L120-129]: `def test_store_admission_payload_at_first_sampling(world)`
- **function `fit_keys`** [L133-140]: `def fit_keys()`
- **function `dec_keys`** [L143-145]: `def dec_keys()`
- **function `c2_store_files`** [L148-165]: `def c2_store_files(world, monkeypatch, drop=None)` - A synthetic C2 store whose files re-hash to the (in-place patched) CONTRACT table.
- **function `g0_world`** [L168-179]: `def g0_world(world, monkeypatch, drop=None, dry=False, freeze_ok=True)`
- **function `loads`** [L183-191]: `def loads(monkeypatch)` decorators: @pytest.fixture
- **test `test_g0_items_on_a_synthetic_world`** [L196-203]: `def test_g0_items_on_a_synthetic_world(world, monkeypatch, loads)`
- **test `test_g0_protocol_contract_and_c2_store_failures`** [L206-214]: `def test_g0_protocol_contract_and_c2_store_failures(world, monkeypatch)`
- **test `test_g0_fit_key_set`** [L217-219]: `def test_g0_fit_key_set(world, monkeypatch)`
- **test `test_g0_store_admission_and_dry_guard`** [L222-227]: `def test_g0_store_admission_and_dry_guard(world, monkeypatch)`
- **function `auth_record`** [L230-239]: `def auth_record(schema, **change)`
- **test `test_auth_ok`** [L242-252]: `def test_auth_ok(tmp_path)`
- **test `test_contract_values`** [L255-274]: `def test_contract_values()`
- **test `test_sequence_ids_and_streams`** [L277-301]: `def test_sequence_ids_and_streams()`
- **test `test_meter_bind_check`** [L305-315]: `def test_meter_bind_check(world)`
- **test `test_measure_only_caps`** [L320-321]: `def test_measure_only_caps()`
- **function `lineage_ctx`** [L324-332]: `def lineage_ctx(tmp_path)`
- **test `test_write_manifest`** [L335-346]: `def test_write_manifest(tmp_path)`
- **test `test_supersede_and_regen_compare`** [L349-364]: `def test_supersede_and_regen_compare(tmp_path)`
- **test `test_module_files_and_sizes`** [L368-374]: `def test_module_files_and_sizes()`

