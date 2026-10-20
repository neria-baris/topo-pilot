# `tests/k4b/test_b_data.py`

- Source: [tests/k4b/test_b_data.py](../../../../../tests/k4b/test_b_data.py)
- Kind: python
- Lines: 355

## Module docstring

> Author B, K4b TEST_PLAN B1, B3 and B17 (data side): seed streams, fixed 3,072-row blocks
> whose content does not depend on k, sequence IDs, int-keyed maps, history tables, duplicates,
> separation (every collision -> FAIL_TECHNICAL/LINEAGE) and the sealed-D-2a predicate.

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 22, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 23, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 24, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 25, via sys.path edit)
- `from c1_registry_sources import canonical32` -> [tools/c1prime_registry/c1_registry_sources.py](../../tools/c1prime_registry/c1_registry_sources.py.md) (line 26, via sys.path edit)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 28, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 29, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 7)
- `hashlib` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `INCOMPLETE`
- `LINEAGE`
- `PROCESS`
- `REASON`
- `REPO`
- `SCOPE`

## Classes and functions

- **function `synthetic_process`** [L38-45]: `def synthetic_process(seed=7, n_states=4, n_symbols=36)`
- **function `proc`** [L49-50]: `def proc()` decorators: @pytest.fixture(scope='module')
- **function `ref_ids`** [L53-55]: `def ref_ids(split, block)`
- **function `expected_block`** [L58-64]: `def expected_block(T, E, pi, split, block)` - The protocol §3.1 recipe, written out independently of k4b_data.
- **test `test_constants_match_contract`** [L69-77]: `def test_constants_match_contract()`
- **test `test_require_int_keys_returns_the_same_dict`** [L80-82]: `def test_require_int_keys_returns_the_same_dict()`
- **test `test_require_int_keys_rejects_str_missing_or_extra`** [L91-94]: `def test_require_int_keys_rejects_str_missing_or_extra(bad)` decorators: @pytest.mark.parametrize('bad', [{'1729': 0, '2718': 0, '3141': 0}, {1729: 0, 2718: 0, '3141': 0}, {1729: 0, 2718: 0}, {1729: 0, 2718: 0, 3141: 0, 9999: 0}])
- **test `test_history_generator_is_the_registered_seedtree_stream`** [L99-104]: `def test_history_generator_is_the_registered_seedtree_stream()`
- **test `test_history_streams_differ_by_split_and_block`** [L107-113]: `def test_history_streams_differ_by_split_and_block()`
- **test `test_sequence_ids_follow_the_registered_rule`** [L117-121]: `def test_sequence_ids_follow_the_registered_rule(split, block)` decorators: @pytest.mark.parametrize('split,block', [('cal', 0), ('val', 0), ('test', 0), ('test', 3)])
- **test `test_sequence_ids_disjoint_across_k4b_blocks`** [L124-130]: `def test_sequence_ids_disjoint_across_k4b_blocks()`
- **test `test_sample_block_is_one_sampler_call_sorted_by_id`** [L135-143]: `def test_sample_block_is_one_sampler_call_sorted_by_id(proc)`
- **test `test_block_content_invariant_to_k`** [L146-157]: `def test_block_content_invariant_to_k(proc)`
- **test `test_named_from_canonical_round_trip`** [L162-169]: `def test_named_from_canonical_round_trip()`
- **test `test_digests_are_sha256_of_uint8_rows`** [L172-176]: `def test_digests_are_sha256_of_uint8_rows()`
- **test `test_lowest_rows_are_the_512_lowest_ids_ascending`** [L179-184]: `def test_lowest_rows_are_the_512_lowest_ids_ascending()`
- **function `shuffled_table_inputs`** [L187-192]: `def shuffled_table_inputs(seed=6)`
- **test `test_history_table_cal_columns_by_sequence_id`** [L195-214]: `def test_history_table_cal_columns_by_sequence_id()`
- **test `test_history_table_val_landmarks`** [L217-224]: `def test_history_table_val_landmarks()`
- **test `test_duplicates_counted_never_removed`** [L229-240]: `def test_duplicates_counted_never_removed()`
- **test `test_duplicates_none`** [L243-247]: `def test_duplicates_none()`
- **function `digest_sets`** [L250-254]: `def digest_sets(seed=11)`
- **test `test_separation_cal_val_every_collision_is_lineage`** [L258-272]: `def test_separation_cal_val_every_collision_is_lineage(case)` decorators: @pytest.mark.parametrize('case', ['none', 'cal_R1', 'val_R1', 'cal_val'])
- **test `test_separation_fresh_collision_is_lineage`** [L275-280]: `def test_separation_fresh_collision_is_lineage()`
- **function `two_blocks`** [L283-284]: `def two_blocks()`
- **test `test_seq_disjoint_pass`** [L287-289]: `def test_seq_disjoint_pass()`
- **test `test_seq_disjoint_overlap_between_blocks_is_lineage`** [L292-296]: `def test_seq_disjoint_overlap_between_blocks_is_lineage()`
- **test `test_seq_disjoint_frozen_union_hit_is_lineage`** [L300-305]: `def test_seq_disjoint_frozen_union_hit_is_lineage(as_array)` decorators: @pytest.mark.parametrize('as_array', [False, True])
- **test `test_seq_disjoint_ranges_are_half_open`** [L308-319]: `def test_seq_disjoint_ranges_are_half_open()`
- **function `predicate_rows`** [L324-332]: `def predicate_rows()`
- **test `test_sealed_d2a_predicate`** [L335-338]: `def test_sealed_d2a_predicate()`
- **test `test_predicate_hit_is_registry_incomplete_and_rows_kept`** [L341-348]: `def test_predicate_hit_is_registry_incomplete_and_rows_kept()`
- **test `test_predicate_pass_without_hits`** [L351-355]: `def test_predicate_pass_without_hits()`

