# `tests/d2a/test_a_world.py`

- Source: [tests/d2a/test_a_world.py](../../../../../tests/d2a/test_a_world.py)
- Kind: python
- Lines: 238

## Module docstring

> Independent tests of tools/d2a/d2a_world.py, part 1 (job 0028, author A): T-SEED, the pool
> table, processes, decision rows, padding, bin positions, master collisions and the test-pool
> guard. Written from D2A-FROZEN-v1 and tools/d2a/API.md only, before the module existed.
> Expected values come from d1_seam, SeedTree and hand computation; no pool is ever sampled.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 24, via sys.path edit)
- `import d2a_world` -> [tools/d2a/d2a_world.py](../../tools/d2a/d2a_world.py.md) (line 25, via sys.path edit)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 7)
- `json` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO_ROOT.joinpath(*_parts))` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `EXPECTED`
- `ORDER`
- `REPO_ROOT`

## Classes and functions

- **function `_expected_pools`** [L36-51]: `def _expected_pools()` - (proc, n, split, seed or None) and stream scope per pool, from API section 2.1.
- **test `test_constants`** [L58-64]: `def test_constants()`
- **test `test_pool_table_follows_api`** [L67-73]: `def test_pool_table_follows_api()`
- **test `test_T_SEED_pool_streams_follow_api_and_are_deterministic`** [L77-81]: `def test_T_SEED_pool_streams_follow_api_and_are_deterministic()`
- **test `test_T_SEED_streams_pairwise_distinct`** [L84-90]: `def test_T_SEED_streams_pairwise_distinct()`
- **test `test_T_SEED_sequence_ids_disjoint_across_pools`** [L93-102]: `def test_T_SEED_sequence_ids_disjoint_across_pools()`
- **function `_meta`** [L105-110]: `def _meta(path: Path, seed_map, config)`
- **test `test_T_SEED_master_collisions`** [L113-125]: `def test_T_SEED_master_collisions(tmp_path)`
- **test `test_process_blocks`** [L129-140]: `def test_process_blocks()`
- **test `test_world_kernels`** [L143-151]: `def test_world_kernels()`
- **test `test_decision_rows`** [L155-163]: `def test_decision_rows()`
- **test `test_pad`** [L166-170]: `def test_pad()`
- **function `_bin_tokens`** [L174-180]: `def _bin_tokens()`
- **test `test_bin_positions_follow_api_rule`** [L183-198]: `def test_bin_positions_follow_api_rule()`
- **test `test_bin_positions_are_deterministic`** [L201-203]: `def test_bin_positions_are_deterministic()`
- **test `test_test_pools_need_stage3`** [L209-217]: `def test_test_pools_need_stage3(pool, stage, tmp_path, monkeypatch)` decorators: @pytest.mark.parametrize('pool', ['test', 'testN']) @pytest.mark.parametrize('stage', [None, '0', '1', '2', '33'])
- **function `_code_or_none`** [L220-227]: `def _code_or_none(fn)`
- **test `test_guard_admits_stage3_and_ignores_other_pools`** [L230-238]: `def test_guard_admits_stage3_and_ignores_other_pools(tmp_path, monkeypatch)`

