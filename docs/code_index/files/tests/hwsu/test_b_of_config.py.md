# `tests/hwsu/test_b_of_config.py`

- Source: [tests/hwsu/test_b_of_config.py](../../../../../tests/hwsu/test_b_of_config.py)
- Kind: python
- Lines: 316

## Module docstring

> Author B (job 0198): hwsu_config: constants, the CONTRACT loader (D-2), the blindness guard
> (protocol §8.1, J9, D-3) and the HANDOFF mirror (D-4). TEST_PLAN §3 row test_b_of_config; DRO1 loader.
> Expected values come from CONTRACT_OF.json and the protocol, never from the code under test.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 22, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `pytest` (lines 17)

### Standard library

- `__future__` (lines 5)
- `builtins` (lines 7)
- `copy` (lines 8)
- `fractions` (lines 14)
- `hashlib` (lines 9)
- `io` (lines 10)
- `json` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `BLIND`
- `C`
- `OF`
- `OPEN`
- `REPO`

## Classes and functions

- **function `_sha`** [L28-29]: `def _sha(b: bytes) -> str`
- **function `_norm`** [L32-33]: `def _norm(p) -> str`
- **function `_hook`** [L36-54]: `def _hook(monkeypatch) -> list` - Access hook (TEST_PLAN §1): record every path opened through the usual entry points.
- **function `_fails`** [L57-61]: `def _fails(status, fn, *a, **k)`
- **test `test_constants_equal_contract`** [L65-91]: `def test_constants_equal_contract()`
- **test `test_paths_equal_contract`** [L94-106]: `def test_paths_equal_contract()`
- **test `test_import_contract_is_phase1_file`** [L109-119]: `def test_import_contract_is_phase1_file()`
- **function `_files`** [L126-134]: `def _files(tmp_path, p2=None, of=OF, raw_p2=None)`
- **test `test_loader_absent_phase2_returns_deep_copy`** [L137-143]: `def test_loader_absent_phase2_returns_deep_copy(tmp_path)`
- **test `test_loader_union_adds_top_level_and_nested_keys`** [L146-152]: `def test_loader_union_adds_top_level_and_nested_keys(tmp_path)`
- **test `test_loader_real_contract_with_nested_resource_key`** [L155-166]: `def test_loader_real_contract_with_nested_resource_key(tmp_path)`
- **test `test_loader_refuses_unbound_phase2`** [L171-173]: `def test_loader_refuses_unbound_phase2(tmp_path, p2)` decorators: @pytest.mark.parametrize('p2', [{'d': 1}, {'contract_of_sha256': '0' * 64, 'd': 1}, {'contract_of_sha256': None, 'd': 1}])
- **test `test_loader_refuses_any_override_even_equal`** [L178-181]: `def test_loader_refuses_any_override_even_equal(tmp_path, extra)` decorators: @pytest.mark.parametrize('extra', [{'a': 2}, {'a': 1}, {'b': {'c': 2}}, {'b': {'l': [3]}}, {'b': {'l': [1, 2]}}, {'b': 5}, {'s': {'t': 1}}])
- **test `test_loader_override_reason_names_dotted_key`** [L184-188]: `def test_loader_override_reason_names_dotted_key(tmp_path)`
- **test `test_loader_refuses_unreadable_of`** [L191-195]: `def test_loader_refuses_unreadable_of(tmp_path)`
- **test `test_merge_is_pure_and_lists_are_leaves`** [L198-208]: `def test_merge_is_pure_and_lists_are_leaves()`
- **test `test_blinded_true`** [L235-240]: `def test_blinded_true(tmp_path, rel, monkeypatch)` decorators: @pytest.mark.parametrize('rel', BLIND)
- **test `test_blinded_false`** [L244-246]: `def test_blinded_false(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', OPEN)
- **test `test_blinded_is_relative_to_root`** [L249-252]: `def test_blinded_is_relative_to_root(tmp_path)`
- **test `test_guard_raises_before_any_open`** [L255-269]: `def test_guard_raises_before_any_open(tmp_path, monkeypatch)`
- **test `test_read_helpers_on_open_paths`** [L272-282]: `def test_read_helpers_on_open_paths(tmp_path)`
- **function `_handoff`** [L286-291]: `def _handoff(tmp_path, **over)`
- **test `test_load_handoff_u_two_keys_only`** [L294-298]: `def test_load_handoff_u_two_keys_only(tmp_path)`
- **test `test_load_handoff_u_refusals`** [L301-308]: `def test_load_handoff_u_refusals(tmp_path)`
- **test `test_load_handoff_u_real_record`** [L313-316]: `def test_load_handoff_u_real_record()` decorators: @pytest.mark.skipif(not Path(C['resources']['project_root'], C['handoff']['path']).is_file(), reason='real HANDOFF.json absent')

