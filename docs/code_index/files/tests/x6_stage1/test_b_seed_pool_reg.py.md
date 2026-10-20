# `tests/x6_stage1/test_b_seed_pool_reg.py`

- Source: [tests/x6_stage1/test_b_seed_pool_reg.py](../../../../../tests/x6_stage1/test_b_seed_pool_reg.py)
- Kind: python
- Lines: 398

## Module docstring

> Author B (operations): T-SEED, T-POOL, T-REG (X6S1-FROZEN-v1 §6.1-§6.6, §14.3; API.md §3, §10).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 21, via sys.path edit)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../../tools/x6_stage1/x6s1_pairs.py.md) (line 22, via sys.path edit)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../../tools/x6_stage1/x6s1_registry.py.md) (line 23, via sys.path edit)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../../tools/x6_stage1/x6s1_run.py.md) (line 24, via sys.path edit)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../../tools/x6_stage1/x6s1_stats.py.md) (line 25, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 26, via unique basename)
- `import x6_run` -> [tools/x6_stage0/x6_run.py](../../tools/x6_stage0/x6_run.py.md) (line 27, via unique basename)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 28, via unique basename)
- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 29, via package root)
- `from topo_pilot.dataset import HMMSampler, PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 30, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 31, via package root)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 354, via unique basename) (inside a function)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 387, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 5)
- `dataclasses` (lines 7)
- `fractions` (lines 11)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 10)
- `types` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`

## Imported by

- none

## Top-level constants

- `REPO`
- `ROWS`

## Classes and functions

- **function `_sha`** [L38-39]: `def _sha(b: bytes) -> str`
- **function `_specs`** [L42-43]: `def _specs()`
- **function `_toks`** [L46-47]: `def _toks(n, seed=3)`
- **test `test_masters_are_registered_and_fresh_against_known_lineages`** [L51-54]: `def test_masters_are_registered_and_fresh_against_known_lineages()`
- **test `test_seed_fresh_compares_values_recursively`** [L64-66]: `def test_seed_fresh_compares_values_recursively(maps, fresh)` decorators: @pytest.mark.parametrize('maps,fresh', [([{'init/x6s0/1': 5}, {'cfg': {'master': 420700}}], True), ([{'a': {'b': [1, 2026101861]}}], False), ([{'model_master': 2026101862}], False), ([{'nested': [{'deep': np.int64(2026101861)}]}], False), ([], True)])
- **test `test_data_streams_distinct_and_scoped`** [L69-76]: `def test_data_streams_distinct_and_scoped()`
- **test `test_model_streams_scope_map_and_arm_sharing`** [L79-95]: `def test_model_streams_scope_map_and_arm_sharing()`
- **test `test_partner_and_bootstrap_streams`** [L98-108]: `def test_partner_and_bootstrap_streams()`
- **test `test_parse_model`** [L113-114]: `def test_parse_model(name, want)` decorators: @pytest.mark.parametrize('name,want', [('NA-s3', ('NA', 3)), ('ZC-s1', ('ZC', 1)), ('init-s2', ('init', 2)), ('SMOKE', ('NA', 'smoke'))])
- **test `test_parse_model_refuses`** [L118-120]: `def test_parse_model_refuses(bad)` decorators: @pytest.mark.parametrize('bad', ['NA-s5', 'XX-s1', 'na-s1', 'smoke', 'NA-s0', ''])
- **test `test_pool_table_order_sizes_splits_names`** [L124-137]: `def test_pool_table_order_sizes_splits_names()`
- **test `test_pool_spec_streams_and_codes`** [L149-153]: `def test_pool_spec_streams_and_codes(args, stream, code_args)` decorators: @pytest.mark.parametrize('args,stream,code_args', [(('train', 'AB', 3), ('x6s1', 'train', 'AB', 3), ('x6s1', 'AB', 'train', 3)), (('dev', 'ZC', 1), ('x6s1', 'dev', 'ZC', 1), ('x6s1', 'ZC', 'dev', 1)), (('smoke',), ('x6s1', 'smoke', 'NA'), ('x6s1', 'NA', 'smoke', 0)), (('gate', 'AB'), ('x6s1', 'gate', 'AB'), ('x6s1', 'AB', 'gate', 0)), (('prefix',), ('x6s1', 'prefix'), ('x6s1', 'NA', 'prefix', 0)), (('val', 'NA'), ('x6s1', 'val', 'NA'), ('x6s1', 'NA', 'val', 0)), (('test', 'ZC'), ('x6s1', 'test', 'ZC'), ('x6s1', 'ZC', 'test', 0))])
- **test `test_unregistered_pool_refused`** [L158-160]: `def test_unregistered_pool_refused(args)` decorators: @pytest.mark.parametrize('args', [('smoke', 'AB'), ('train', 'NA', 5), ('train', 'NA', None), ('bogus', 'NA'), ('prefix', 'ZC'), ('test', 'XX')])
- **test `test_sequence_ids_exact_and_disjoint_across_all_pools`** [L163-171]: `def test_sequence_ids_exact_and_disjoint_across_all_pools()`
- **test `test_sample_pool_returns_tokens_only_and_matches_sampler`** [L174-188]: `def test_sample_pool_returns_tokens_only_and_matches_sampler()`
- **test `test_save_and_load_pool`** [L191-203]: `def test_save_and_load_pool(tmp_path)`
- **test `test_stage0_regeneration_count_check`** [L212-213]: `def test_stage0_regeneration_count_check(counts, status)` decorators: @pytest.mark.parametrize('counts,status', [({'E_cue': 200306, 'amb_nb': 13402}, 'PASS'), ({'E_cue': 200305, 'amb_nb': 13402}, LINEAGE), ({'E_cue': 200306, 'amb_nb': 13403}, LINEAGE)])
- **test `test_row_digests_keys_and_hex`** [L216-226]: `def test_row_digests_keys_and_hex()`
- **test `test_digest_set_runs_full_confirmation_and_hash`** [L229-238]: `def test_digest_set_runs_full_confirmation_and_hash(tmp_path)`
- **test `test_collision_mass`** [L241-243]: `def test_collision_mass()`
- **test `test_separation_collision_is_lineage`** [L247-262]: `def test_separation_collision_is_lineage(tmp_path, kind)` decorators: @pytest.mark.parametrize('kind', ['rows', 'ids'])
- **function `_x6_rows`** [L265-266]: `def _x6_rows(n)`
- **test `test_handoff_rows_malformed_json_is_incomplete`** [L269-273]: `def test_handoff_rows_malformed_json_is_incomplete(tmp_path)`
- **test `test_handoff_rows_keeps_x6_valid_lists`** [L276-283]: `def test_handoff_rows_keeps_x6_valid_lists(tmp_path)`
- **function `_scratch`** [L286-290]: `def _scratch(tmp_path)`
- **test `test_inventory_registered_copy_passes`** [L293-298]: `def test_inventory_registered_copy_passes(tmp_path)`
- **test `test_inventory_unregistered_npy_is_incomplete`** [L301-307]: `def test_inventory_unregistered_npy_is_incomplete(tmp_path)`
- **test `test_inventory_unregistered_observation_set_root_is_incomplete`** [L310-316]: `def test_inventory_unregistered_observation_set_root_is_incomplete(tmp_path)`
- **test `test_inventory_unclassified_x6_directory_is_incomplete`** [L319-323]: `def test_inventory_unclassified_x6_directory_is_incomplete(tmp_path)`
- **test `test_no_sealed_d2a_predicate`** [L326-328]: `def test_no_sealed_d2a_predicate()`
- **function `_kreg2`** [L332-349]: `def _kreg2(d, n=37, unsorted=False, edit=None)`
- **test `test_kreg2_reader_equals_k4b_load`** [L353-373]: `def test_kreg2_reader_equals_k4b_load(tmp_path, run)` decorators: @pytest.mark.parametrize('run', [1, 5, 2 ** 22])
- **test `test_kreg2_reader_refuses_mismatch`** [L377-390]: `def test_kreg2_reader_refuses_mismatch(tmp_path, case)` decorators: @pytest.mark.parametrize('case', ['file_hash', 'count', 'union', 'seq_union', 'unsorted'])
- **test `test_disk_floors`** [L396-398]: `def test_disk_floors(c, x, bad)` decorators: @pytest.mark.parametrize('c,x,bad', [(2 * 10 ** 9, 30 * 10 ** 9, None), (2 * 10 ** 9 - 1, 10 ** 12, 'C:'), (10 ** 12, 30 * 10 ** 9 - 1, 'X:')])

