# `tests/c1prime/test_b_registry.py`

- Source: [tests/c1prime/test_b_registry.py](../../../../../tests/c1prime/test_b_registry.py)
- Kind: python
- Lines: 177

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-5: histories, registry digests, separation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)
- `from topo_pilot.dataset.checks import check_first_token, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 24, via package root)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 25, via package root)
- `import c1_data` -> [tools/c1prime/c1_data.py](../../tools/c1prime/c1_data.py.md) (line 33, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 34, via sys.path edit)

### External (third-party)

- `numpy` (lines 21)
- `pytest` (lines 22)

### Standard library

- `__future__` (lines 16)
- `pathlib` (lines 19)
- `sys` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 31: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `LINEAGE`
- `REPO`

## Classes and functions

- **function `_status`** [L41-42]: `def _status(res) -> str`
- **function `_stream`** [L45-46]: `def _stream(split, block)`
- **function `_process`** [L49-53]: `def _process(N=6, V=36, seed=1)`
- **function `_tau`** [L56-58]: `def _tau(canon, k)`
- **function `_donor`** [L61-64]: `def _donor(canon32, k)`
- **test `test_history_stream_and_sequence_ids`** [L67-77]: `def test_history_stream_and_sequence_ids()`
- **test `test_sample_block_is_one_fixed_4096_row_stream_with_w33_dropped`** [L80-87]: `def test_sample_block_is_one_fixed_4096_row_stream_with_w33_dropped()`
- **test `test_panels_follow_rank_in_block`** [L90-97]: `def test_panels_follow_rank_in_block()`
- **test `test_lowest_selects_the_n_lowest_ids_in_ascending_id_order`** [L100-106]: `def test_lowest_selects_the_n_lowest_ids_in_ascending_id_order()`
- **test `test_history_table_digests_of_H_and_both_donors`** [L109-124]: `def test_history_table_digests_of_H_and_both_donors()`
- **test `test_registry_digests_are_the_history_digest_set`** [L127-129]: `def test_registry_digests_are_the_history_digest_set()`
- **function `_three_sets`** [L132-136]: `def _three_sets(seed)`
- **test `test_separation_passes_when_all_three_intersections_are_empty`** [L139-141]: `def test_separation_passes_when_all_three_intersections_are_empty()`
- **test `test_separation_collision_is_lineage_failure`** [L146-157]: `def test_separation_collision_is_lineage_failure(collision)` decorators: @pytest.mark.parametrize('collision', ['cal_H_vs_R1', 'val_donor_vs_R1', 'cal_Hp_vs_val_Hm', 'cal_Hm_vs_val_H'])
- **test `test_first_token_ok_is_check_first_token_not_raising`** [L160-177]: `def test_first_token_ok_is_check_first_token_not_raising()`

