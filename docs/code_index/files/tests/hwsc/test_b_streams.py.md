# `tests/hwsc/test_b_streams.py`

- Source: [tests/hwsc/test_b_streams.py](../../../../../tests/hwsc/test_b_streams.py)
- Kind: python
- Lines: 320

## Module docstring

> Author B (job 0176): streams, sequence IDs, the train/dev mirror (DRC4) and evaluation blocks.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 22, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 23, via sys.path edit)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 24, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 25, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 26, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 27, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 28, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend, ObservationSet, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 31, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `DRY`
- `REPO`
- `W_STAR`
- `_HWSC`

## Classes and functions

- **function `_ids`** [L38-39]: `def _ids(rep, split, n, process=W_STAR)`
- **function `_draws`** [L42-43]: `def _draws(gen, n=32)`
- **function `dry_binding`** [L47-51]: `def dry_binding(tmp_path)` decorators: @pytest.fixture
- **test `test_hwsc_plan_fields`** [L55-62]: `def test_hwsc_plan_fields()`
- **test `test_dry_plan`** [L67-71]: `def test_dry_plan(kind, sizes)` decorators: @pytest.mark.parametrize('kind,sizes', [('dry_tiny', {'train': 4096, 'dev': 512}), ('dry_e4', {'train': 2048, 'dev': 256})])
- **test `test_dry_plan_refuses_other_kinds`** [L74-76]: `def test_dry_plan_refuses_other_kinds()`
- **test `test_run_key_real_and_dry`** [L79-85]: `def test_run_key_real_and_dry()`
- **test `test_sequence_ids_real`** [L91-95]: `def test_sequence_ids_real(split, master)` decorators: @pytest.mark.parametrize('master', cc.MASTERS) @pytest.mark.parametrize('split', ['train', 'dev'])
- **test `test_sequence_ids_dry_replicates`** [L98-105]: `def test_sequence_ids_dry_replicates()`
- **test `test_block_roles_refused`** [L109-111]: `def test_block_roles_refused(role)` decorators: @pytest.mark.parametrize('role', ['lgate', 'cal', 'val', 'test', 'LGATE', 'CAL'])
- **test `test_master_outside_plan_refused`** [L115-117]: `def test_master_outside_plan_refused(master)` decorators: @pytest.mark.parametrize('master', [620201, 1729, 629911])
- **function `_obs`** [L121-122]: `def _obs(store, oid)`
- **test `test_drc4_mirror_equals_stage_b_unbound`** [L125-139]: `def test_drc4_mirror_equals_stage_b_unbound()`
- **test `test_drc4_hwsc_scope_differs_and_is_disjoint`** [L142-168]: `def test_drc4_hwsc_scope_differs_and_is_disjoint(dry_binding)`
- **test `test_block_generator_formula_explicit_and_default`** [L172-180]: `def test_block_generator_formula_explicit_and_default()`
- **test `test_block_ids_formula`** [L183-189]: `def test_block_ids_formula()`
- **test `test_sample_block_c_equals_k4b_sample_block_under_dry_binding`** [L192-199]: `def test_sample_block_c_equals_k4b_sample_block_under_dry_binding(dry_binding)`
- **test `test_sample_block_c_one_sampler_call_and_shape`** [L202-220]: `def test_sample_block_c_one_sampler_call_and_shape(dry_binding, monkeypatch)`
- **test `test_hist_names`** [L223-228]: `def test_hist_names()`
- **test `test_save_table_six_keys_and_exclusive`** [L231-248]: `def test_save_table_six_keys_and_exclusive(tmp_path)`
- **function `_tables`** [L251-258]: `def _tables(n=600, seed=0)`
- **function `_reg`** [L265-267]: `def _reg(digests=(), seq=(), ranges=None)`
- **function `_retable`** [L270-271]: `def _retable(t, split, canon)`
- **test `test_h2_clean_pass_and_keys`** [L274-279]: `def test_h2_clean_pass_and_keys()`
- **test `test_h2_planted_registry_digest_is_lineage`** [L282-285]: `def test_h2_planted_registry_digest_is_lineage()`
- **test `test_h2_cross_split_collision_is_lineage`** [L288-294]: `def test_h2_cross_split_collision_is_lineage()`
- **test `test_h2_seq_id_overlaps_are_lineage`** [L297-302]: `def test_h2_seq_id_overlaps_are_lineage()`
- **test `test_h2_d2a_predicate_row_is_incomplete`** [L305-310]: `def test_h2_d2a_predicate_row_is_incomplete()`
- **test `test_h2_duplicates_counted_and_kept`** [L313-320]: `def test_h2_duplicates_counted_and_kept()`

