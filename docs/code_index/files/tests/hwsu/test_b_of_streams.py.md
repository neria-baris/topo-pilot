# `tests/hwsu/test_b_of_streams.py`

- Source: [tests/hwsu/test_b_of_streams.py](../../../../../tests/hwsu/test_b_of_streams.py)
- Kind: python
- Lines: 172

## Module docstring

> Author B (job 0198): streams, sequence ids, history tables and names (protocol §2.1 S2, §2.8;
> API §2.3). TEST_PLAN §3 row test_b_of_streams. Sampling only in the dry scope `hwsu-dry-v1` on a
> synthetic 3-state world (V = 36); real-scope generators are created and compared but never
> sampled from.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 17, via sys.path edit)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../../tools/hwsu/hwsu_pairs.py.md) (line 18, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 19, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 21, via package root)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 22, via package root)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 166, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)

### Standard library

- `__future__` (lines 6)
- `json` (lines 94)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `DRY`
- `PROC`
- `REPO`

## Classes and functions

- **function `_world`** [L28-32]: `def _world()`
- **function `_first`** [L35-36]: `def _first(g, k=64)`
- **test `test_generator_equals_seedtree`** [L42-45]: `def test_generator_equals_seedtree(scope, split, block)` decorators: @pytest.mark.parametrize('scope,split,block', [('hwsu-of-v1', 'of-fit', 0), ('hwsu-of-v1', 'of-eval', 1), ('hwsu-of-v1', 'of-eval/cf', 0), (DRY, 'of-fit', 1)])
- **test `test_generator_block_cast_and_process_argument`** [L48-55]: `def test_generator_block_cast_and_process_argument()`
- **test `test_streams_distinct_across_scope_split_block`** [L58-62]: `def test_streams_distinct_across_scope_split_block()`
- **test `test_seq_ids_rule`** [L70-74]: `def test_seq_ids_rule(scope, split, block, arm)` decorators: @pytest.mark.parametrize('scope,split,block,arm', [('hwsu-of-v1', 'of-fit', 0, 's'), ('hwsu-of-v1', 'of-eval', 1, 'a1'), ('hwsu-of-v1', 'of-eval', 1, 'a2'), (DRY, 'of-eval', 0, 'a2')])
- **test `test_seq_ids_distinct_across_arms_blocks_scopes`** [L77-84]: `def test_seq_ids_distinct_across_arms_blocks_scopes()`
- **test `test_seq_ids_unknown_arm`** [L88-90]: `def test_seq_ids_unknown_arm(arm)` decorators: @pytest.mark.parametrize('arm', ['a3', 'S', '', 'a'])
- **test `test_contract_stream_and_id_rules`** [L93-98]: `def test_contract_stream_and_id_rules()`
- **test `test_sample_singles_stream_and_ids`** [L102-110]: `def test_sample_singles_stream_and_ids()`
- **test `test_sample_pairs_streams_rows_and_ids`** [L113-127]: `def test_sample_pairs_streams_rows_and_ids()`
- **test `test_sampling_deterministic`** [L130-135]: `def test_sampling_deterministic()`
- **test `test_history_table`** [L140-154]: `def test_history_table(label)` decorators: @pytest.mark.parametrize('label', ['of-fit', 'of-eval-a1', 'of-eval-a2'])
- **test `test_hist_name`** [L161-162]: `def test_hist_name(kind, block, dry, name)` decorators: @pytest.mark.parametrize('kind,block,dry,name', [('fit', 0, False, 'HIST_OF_fit_b0.npz'), ('eval_a1', 1, False, 'HIST_OF_eval_a1_b1.npz'), ('eval_a2', 0, False, 'HIST_OF_eval_a2_b0.npz'), ('fit', 1, True, 'DRYHIST_OF_fit_b1.npz'), ('eval_a2', 1, True, 'DRYHIST_OF_eval_a2_b1.npz')])
- **test `test_hist_names_follow_name_rule`** [L165-172]: `def test_hist_names_follow_name_rule()`

