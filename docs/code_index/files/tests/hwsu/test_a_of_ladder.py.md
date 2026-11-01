# `tests/hwsu/test_a_of_ladder.py`

- Source: [tests/hwsu/test_a_of_ladder.py](../../../../../tests/hwsu/test_a_of_ladder.py)
- Kind: python
- Lines: 146

## Module docstring

> Author A (job 0198): the OF-4 proxy ladder (protocol §2.9 P1 rule, §4.2 OF-4; DRO4) with the
> real precision kernels on planted oracle arrays, against a test-side re-computation.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 12, via sys.path edit)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 13, via sys.path edit)
- `import hwsu_driver_of` -> [tools/hwsu/hwsu_driver_of.py](../../tools/hwsu/hwsu_driver_of.py.md) (line 14, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 15, via unique basename)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 16, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 18, via unique basename)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 4)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 10: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `LADDER`
- `ORDER`
- `REPO`
- `SEEDS`

## Classes and functions

- **function `planted`** [L26-34]: `def planted(shift=0.0)` - The oracle as a model: A°_full = G (Lemma D2); A°_S = 0.3 G + noise. Designed so that the
- **function `make_ctx`** [L37-44]: `def make_ctx(tmp_path, G, A_full, A_S, prior='PASS')`
- **function `status`** [L47-52]: `def status(ctx)`
- **function `my_ladder`** [L55-77]: `def my_ladder(G, A_full, A_S)` - §2.9 P1 rule, single model "oracle", written out with the reused kernels.
- **function `reference`** [L81-82]: `def reference()` decorators: @pytest.fixture(scope='module')
- **test `test_design_of_the_planted_arrays`** [L85-91]: `def test_design_of_the_planted_arrays(reference)`
- **test `test_of_4_ladder_equals_independent_recomputation`** [L94-116]: `def test_of_4_ladder_equals_independent_recomputation(tmp_path, reference)`
- **test `test_shift_of_mean_A_full_changes_nothing`** [L119-139]: `def test_shift_of_mean_A_full_changes_nothing(tmp_path, monkeypatch)` - P1 reads no model mean: shifting A_full (SDs fixed) leaves the alternatives (mean G only)
- **test `test_share_dropped_at_of_3_keeps_response_rule`** [L142-146]: `def test_share_dropped_at_of_3_keeps_response_rule(tmp_path)`

