# `tests/hwsd/test_b_data.py`

- Source: [tests/hwsd/test_b_data.py](../../../../../tests/hwsd/test_b_data.py)
- Kind: python
- Lines: 262

## Module docstring

> Author B: blocks, streams and sequence IDs, tables, H2-D, risk, references, controls (§2.5, §4.2).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 15, via sys.path edit)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](../../tools/hwsd/hwsd_bind.py.md) (line 16, via sys.path edit)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](../../tools/hwsd/hwsd_data.py.md) (line 17, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 18, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 20, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 21, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../../tools/hwsb/hwsb_eval.py.md) (line 22, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 23, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 24, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 28, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 29, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 26)
- `pytest` (lines 27)

### Standard library

- `__future__` (lines 3)
- `decimal` (lines 7)
- `fractions` (lines 8)
- `json` (lines 5)
- `pathlib` (lines 9)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `DTYPES`
- `PROC`

## Classes and functions

- **function `_draws`** [L38-39]: `def _draws(g, n=16)`
- **test `test_contract_stream_formulas`** [L42-48]: `def test_contract_stream_formulas()`
- **test `test_block_generator_and_ids_under_the_binding`** [L52-61]: `def test_block_generator_and_ids_under_the_binding(split)` decorators: @pytest.mark.parametrize('split', ['lgate', 'cal', 'val', 'test'])
- **test `test_split_ids_disjoint_and_differ_from_stage_c`** [L64-72]: `def test_split_ids_disjoint_and_differ_from_stage_c()`
- **function `tiny`** [L76-77]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **test `test_sample_block_d_mirror_under_the_dry_binding`** [L80-100]: `def test_sample_block_d_mirror_under_the_dry_binding(tiny, tmp_path, monkeypatch)`
- **test `test_sample_tables_hist_names_save_and_load`** [L103-139]: `def test_sample_tables_hist_names_save_and_load(tiny, tmp_path)`
- **class `_X6`** [L142-144]
- **method `_X6.contains`** [L143-144]: `def contains(self, d)`
- **function `_reg`** [L147-148]: `def _reg(digests=(), sealed=None)`
- **function `_tables`** [L151-154]: `def _tables(**over)`
- **test `test_separation_d`** [L157-172]: `def test_separation_d()`
- **test `test_registry_risk_d_exact`** [L175-183]: `def test_registry_risk_d_exact()`
- **function `_refs`** [L188-190]: `def _refs(n=3)`
- **test `test_refs_json_round_trip_and_refusals`** [L193-214]: `def test_refs_json_round_trip_and_refusals(tiny)`
- **function `_q`** [L217-222]: `def _q(n, rng)`
- **test `test_lgate_oracle_row_sums`** [L225-247]: `def test_lgate_oracle_row_sums(monkeypatch)`
- **test `test_shared_controls_bitwise`** [L250-262]: `def test_shared_controls_bitwise()`

