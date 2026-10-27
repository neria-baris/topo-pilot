# `tests/c2_nd/test_b_dry_hs.py`

- Source: [tests/c2_nd/test_b_dry_hs.py](../../../../../tests/c2_nd/test_b_dry_hs.py)
- Kind: python
- Lines: 180

## Module docstring

> Author B, regression for D-0158-1 (job 0159): the dry-run planted circle is history-sensitive.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 23, via sys.path edit)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 26, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 27, via sys.path edit)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](../../tools/c2_nd/nd_driver.py.md) (line 28, via sys.path edit)
- `import nd_dry` -> [tools/c2_nd/nd_dry.py](../../tools/c2_nd/nd_dry.py.md) (line 29, via sys.path edit)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](../../tools/c2_nd/nd_registry.py.md) (line 30, via sys.path edit)
- `import nd_split` -> [tools/c2_nd/nd_split.py](../../tools/c2_nd/nd_split.py.md) (line 31, via sys.path edit)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](../../tools/c2_nd/nd_stage_base.py.md) (line 32, via sys.path edit)
- `import nd_stage_pre` -> [tools/c2_nd/nd_stage_pre.py](../../tools/c2_nd/nd_stage_pre.py.md) (line 33, via sys.path edit)
- `import nd_stage_val` -> [tools/c2_nd/nd_stage_val.py](../../tools/c2_nd/nd_stage_val.py.md) (line 34, via sys.path edit)

### External (third-party)

- `numpy` (lines 35)
- `pytest` (lines 36)

### Standard library

- `__future__` (lines 13)
- `json` (lines 15)
- `pathlib` (lines 17)
- `sys` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `KNOWN_D`
- `ORDER`
- `R1_MIN`
- `REPO`

## Classes and functions

- **function `at`** [L43-46]: `def at(ctx, gate)` - A fresh policy positioned at `gate` (the earlier gates counted as done).
- **function `d_null_family`** [L49-62]: `def d_null_family(ctx)` - The planted D-NULL on DVAL: d_stream arrays under the refit projector RD, bounds (C2
- **function `run`** [L66-108]: `def run(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_belief_chart_files`** [L111-118]: `def test_belief_chart_files(run)` - ND-C59: c2/charts/CHART_<j>_dry.npz holds mu (d_model) and U (2 x 128) only.
- **test `test_fixture_reaches_r1`** [L121-127]: `def test_fixture_reaches_r1(run)` - The stages before R1 record PASS on the planted models (the 0158 run stopped only at R1).
- **test `test_r1_passes_on_every_planted_model`** [L130-144]: `def test_r1_passes_on_every_planted_model(run)` - Pass criterion 2 of 10.1 / D-0158-1: the planted models are R1-history-sensitive, for every
- **test `test_d_only_is_necessary`** [L147-164]: `def test_d_only_is_necessary(run)` - KC (8.3): D0 USED, D-ONLY USED and NECESSARY, D-DOSE PARTIAL and NOT_NECESSARY. No model
- **test `test_d_null_is_not_used`** [L167-180]: `def test_d_null_is_not_used(run)` - The planted D-NULL: (a) KC-R, the coordinate decoys D-NULL-R NOT_USED and D-ID USED, never

