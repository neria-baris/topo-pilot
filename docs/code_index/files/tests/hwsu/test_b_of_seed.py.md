# `tests/hwsu/test_b_of_seed.py`

- Source: [tests/hwsu/test_b_of_seed.py](../../../../../tests/hwsu/test_b_of_seed.py)
- Kind: python
- Lines: 356

## Module docstring

> Author B (job 0198): the J9 seed-search mirror, the declaration fragments, the namespace
> overlap check (D-16) and G0-OF (protocol §4.2 OF-0; RC-3, J3, J5, J9, J10; API §6). TEST_PLAN §3
> row test_b_of_seed; DRO6. Synthetic roots and a synthetic mailbox under tmp_path only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 26, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 27, via sys.path edit)
- `import hwsu_seed` -> [tools/hwsu/hwsu_seed.py](../../tools/hwsu/hwsu_seed.py.md) (line 28, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 29, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 30, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via unique basename)

### External (third-party)

- `pytest` (lines 21)

### Standard library

- `__future__` (lines 10)
- `builtins` (lines 12)
- `copy` (lines 13)
- `hashlib` (lines 14)
- `io` (lines 15)
- `json` (lines 16)
- `os` (lines 17)
- `pathlib` (lines 19)
- `sys` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `AUTH_CASES`
- `C`
- `FAKE`
- `REPO`

## Classes and functions

- **function `_norm`** [L37-38]: `def _norm(p) -> str`
- **function `_hook`** [L41-59]: `def _hook(monkeypatch) -> list`
- **function `_w`** [L62-66]: `def _w(p, text) -> Path`
- **function `_sha`** [L69-70]: `def _sha(p) -> str`
- **function `_rebase`** [L73-74]: `def _rebase(hits, root)`
- **function `_plain_root`** [L78-85]: `def _plain_root(root)`
- **test `test_seed_search_equals_stage_c_mirror`** [L88-97]: `def test_seed_search_equals_stage_c_mirror(tmp_path)`
- **test `test_digit_needles_whole_tokens`** [L100-104]: `def test_digit_needles_whole_tokens(tmp_path)`
- **function `_blinded_fixtures`** [L107-117]: `def _blinded_fixtures(root)`
- **test `test_blinded_files_pruned_unopened`** [L120-132]: `def test_blinded_files_pruned_unopened(tmp_path, monkeypatch)`
- **test `test_search_root_for_guard`** [L135-139]: `def test_search_root_for_guard(tmp_path)`
- **function `_decl_root`** [L143-151]: `def _decl_root(root)`
- **test `test_classify_declarations`** [L154-161]: `def test_classify_declarations(tmp_path)`
- **test `test_classify_unclassified`** [L168-175]: `def test_classify_unclassified(tmp_path, rel, text)` decorators: @pytest.mark.parametrize('rel,text', [('topo-pilot/src/x.py', 'seed = 640101\n'), ('topo-pilot/src/y.py', "s = 'hwsd-v1'\n"), ('other-store/r.json', '"629999"\n'), ('topo-pilot/tools/hwsc/x.md', 'hwsu-store\n')])
- **test `test_classify_explicit_lists_never_read_stage_b_contract`** [L178-187]: `def test_classify_explicit_lists_never_read_stage_b_contract(monkeypatch)` - Ruling (conditional reads): HWSU always passes both lists, so hwsb_config.CONTRACT
- **test `test_needles_are_contract_lists`** [L190-194]: `def test_needles_are_contract_lists()`
- **test `test_contract_fragments_are_j9_list`** [L197-204]: `def test_contract_fragments_are_j9_list()`
- **function `_ns`** [L208-214]: `def _ns()`
- **test `test_namespace_real_record_disjoint`** [L217-220]: `def test_namespace_real_record_disjoint()`
- **test `test_namespace_overlap_detected`** [L233-237]: `def test_namespace_overlap_detected(change)` decorators: @pytest.mark.parametrize('change', [lambda d: d['scopes'].append('hwsu-v1'), lambda d: d['scopes'].append('HWSU-DRY-V1'), lambda d: d['scopes'].append('x-hwsu-of-v1-y'), lambda d: d.update(seed_blocks=[[620400, 620499], [640120, 640130]]), lambda d: d.update(seed_blocks=[[649000, 649901]]), lambda d: d.update(store='X:/Downloads/projects/topo-pilot/hwsu-store-x'), lambda d: d.update(dry_store_glob='X:/Downloads/topo-scratch/hwsu-dry*'), lambda d: d.update(test_root_glob='X:/Downloads/topo-scratch/test_hwsu-*')])
- **test `test_namespace_adjacent_seed_blocks_disjoint`** [L240-243]: `def test_namespace_adjacent_seed_blocks_disjoint()`
- **function `_g0_world`** [L247-282]: `def _g0_world(tmp_path, d_track=None, u_track=None)`
- **function `_g0`** [L285-291]: `def _g0(monkeypatch, c, ctx)`
- **test `test_g0_of_pass_writes_record`** [L294-300]: `def test_g0_of_pass_writes_record(tmp_path, monkeypatch)`
- **test `test_g0_of_authority_failures`** [L319-324]: `def test_g0_of_authority_failures(tmp_path, monkeypatch, case)` decorators: @pytest.mark.parametrize('case', sorted(AUTH_CASES))
- **test `test_g0_of_namespace_u_differs`** [L327-330]: `def test_g0_of_namespace_u_differs(tmp_path, monkeypatch)`
- **test `test_g0_of_overlap_is_seed_scope`** [L333-337]: `def test_g0_of_overlap_is_seed_scope(tmp_path, monkeypatch)`
- **test `test_g0_of_store_lineage`** [L340-343]: `def test_g0_of_store_lineage(tmp_path, monkeypatch)`
- **test `test_g0_of_unclassified_hit`** [L346-356]: `def test_g0_of_unclassified_hit(tmp_path, monkeypatch)`

