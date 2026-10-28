# `tests/hwsb/test_b_streams.py`

- Source: [tests/hwsb/test_b_streams.py](../../../../../tests/hwsb/test_b_streams.py)
- Kind: python
- Lines: 399

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_streams.py`: streams and sequence IDs
> (section 2.3, RC-3, RC-12; DRB4, DRB16), sampling, canonical/named maps, hist blocks, H2-B.
> Written from the protocol, API.md, CONTRACT.json and TEST_PLAN.md only; tools/hwsb/*.py unread.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 18, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 19, via sys.path edit)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 20, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 21, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend, ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 22, via package root)
- `from topo_pilot.dataset import DatasetConfig, DatasetStage, HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 24, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 25, via package root)
- `from topo_pilot.process.emission import EmissionConfig` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 26, via package root)

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)

### Standard library

- `__future__` (lines 5)
- `dataclasses` (lines 8)
- `pathlib` (lines 9)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `DRY`
- `KEY`
- `PERM3`
- `REAL`
- `REFUSALS`
- `REPO`
- `TINY`

## Classes and functions

- **function `draw`** [L31-32]: `def draw(g)`
- **function `stop_status`** [L34-35]: `def stop_status(excinfo)`
- **test `test_real_train_dev_streams_match_contract`** [L40-46]: `def test_real_train_dev_streams_match_contract(role, master)` decorators: @pytest.mark.parametrize('master', [620201, 620202]) @pytest.mark.parametrize('role', ['train', 'dev'])
- **test `test_real_block_streams_match_contract`** [L50-52]: `def test_real_block_streams_match_contract(role)` decorators: @pytest.mark.parametrize('role', ['LGATE', 'CAL', 'VAL'])
- **test `test_dry_streams_match_contract`** [L56-65]: `def test_dry_streams_match_contract(kind)` decorators: @pytest.mark.parametrize('kind', ['dry_tiny', 'dry_e4'])
- **test `test_dry_plan_rejects_unknown_kind`** [L68-70]: `def test_dry_plan_rejects_unknown_kind()`
- **test `test_data_generator_refusals`** [L88-90]: `def test_data_generator_refusals(name, call)` decorators: @pytest.mark.parametrize('name,call', REFUSALS, ids=[r[0] for r in REFUSALS])
- **test `test_foreign_tree_is_refused`** [L93-95]: `def test_foreign_tree_is_refused()`
- **test `test_sequence_ids_refusals`** [L99-101]: `def test_sequence_ids_refusals(name, call)` decorators: @pytest.mark.parametrize('name,call', REFUSALS, ids=[r[0] for r in REFUSALS])
- **test `test_sequence_ids_follow_contract_replicates`** [L104-115]: `def test_sequence_ids_follow_contract_replicates()`
- **test `test_dry_sequence_ids_follow_contract_replicates`** [L118-124]: `def test_dry_sequence_ids_follow_contract_replicates()`
- **test `test_real_tables_have_pairwise_disjoint_ids`** [L127-136]: `def test_real_tables_have_pairwise_disjoint_ids()`
- **test `test_stream_record_lists_the_scope`** [L139-144]: `def test_stream_record_lists_the_scope()`
- **function `w0`** [L148-151]: `def w0()` decorators: @pytest.fixture(scope='module')
- **test `test_sample_observations_equals_dataset_stage_bitwise`** [L154-165]: `def test_sample_observations_equals_dataset_stage_bitwise(w0)`
- **function `named_tiny`** [L173-176]: `def named_tiny()`
- **function `spy`** [L180-188]: `def spy(monkeypatch)` decorators: @pytest.fixture
- **test `test_sample_block_one_call_contiguous_uint8_without_w33`** [L191-196]: `def test_sample_block_one_call_contiguous_uint8_without_w33(spy)`
- **test `test_sample_observations_one_call_named_tokens`** [L199-204]: `def test_sample_observations_one_call_named_tokens(spy)`
- **function `planted`** [L207-216]: `def planted(monkeypatch, edit)`
- **function `bad_range`** [L219-220]: `def bad_range(tokens, states)`
- **function `biased_first`** [L223-224]: `def biased_first(tokens, states)`
- **test `test_sampler_defects_fail_technical`** [L228-235]: `def test_sampler_defects_fail_technical(monkeypatch, edit)` decorators: @pytest.mark.parametrize('edit', [bad_range, biased_first])
- **test `test_canonical32_and_named32_invert_exactly`** [L238-247]: `def test_canonical32_and_named32_invert_exactly()`
- **test `test_model_inputs_have_bos_36_and_width_33`** [L250-257]: `def test_model_inputs_have_bos_36_and_width_33()`
- **test `test_lowest_rows_picks_the_lowest_ids`** [L260-268]: `def test_lowest_rows_picks_the_lowest_ids()`
- **function `tiny_proc`** [L271-272]: `def tiny_proc()`
- **function `small_plan`** [L275-277]: `def small_plan()`
- **test `test_make_block_matches_independent_sampling`** [L280-291]: `def test_make_block_matches_independent_sampling()`
- **test `test_block_round_trip_and_exclusive_create`** [L294-312]: `def test_block_round_trip_and_exclusive_create(tmp_path)`
- **test `test_tampered_digest_fails_load_block`** [L315-323]: `def test_tampered_digest_fails_load_block(tmp_path)`
- **function `rows`** [L326-327]: `def rows(seed, n)`
- **function `blk`** [L330-332]: `def blk(canon, start)`
- **function `tables`** [L335-344]: `def tables(**edit)`
- **test `test_separation_clean_tables_pass`** [L347-352]: `def test_separation_clean_tables_pass()`
- **test `test_separation_eval_train_collision_fails_lineage`** [L355-361]: `def test_separation_eval_train_collision_fails_lineage()`
- **test `test_separation_eval_eval_collision_fails_lineage`** [L364-369]: `def test_separation_eval_eval_collision_fails_lineage()`
- **test `test_separation_id_overlap_fails_lineage`** [L372-376]: `def test_separation_id_overlap_fails_lineage()`
- **test `test_duplicates_are_counted_and_kept`** [L379-390]: `def test_duplicates_are_counted_and_kept()`
- **test `test_hws_collisions_are_reported_not_gating`** [L393-399]: `def test_hws_collisions_are_reported_not_gating()`

