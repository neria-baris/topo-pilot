# `tests/c2_nd/test_impl_dry_hs.py`

- Source: [tests/c2_nd/test_impl_dry_hs.py](../../../../../tests/c2_nd/test_impl_dry_hs.py)
- Kind: python
- Lines: 161

## Module docstring

> Implementer test, D-0158-1 (job 0159; API.md §20.11 ND-C59; protocol §10.1 criterion 2).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 24, via sys.path edit)
- `import c1_data` -> [tools/c1prime/c1_data.py](../../tools/c1prime/c1_data.py.md) (line 27, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 28, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../../tools/c2_readout/c2_oracle.py.md) (line 29, via unique basename)
- `import nd_data` -> [tools/c2_nd/nd_data.py](../../tools/c2_nd/nd_data.py.md) (line 30, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 31, via sys.path edit)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](../../tools/c2_nd/nd_driver.py.md) (line 32, via sys.path edit)
- `import nd_dry` -> [tools/c2_nd/nd_dry.py](../../tools/c2_nd/nd_dry.py.md) (line 33, via sys.path edit)
- `import nd_split` -> [tools/c2_nd/nd_split.py](../../tools/c2_nd/nd_split.py.md) (line 34, via sys.path edit)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](../../tools/c2_nd/nd_stage_base.py.md) (line 35, via sys.path edit)
- `import nd_stage_post` -> [tools/c2_nd/nd_stage_post.py](../../tools/c2_nd/nd_stage_post.py.md) (line 36, via sys.path edit)
- `import nd_stage_pre` -> [tools/c2_nd/nd_stage_pre.py](../../tools/c2_nd/nd_stage_pre.py.md) (line 37, via sys.path edit)
- `import nd_stage_val` -> [tools/c2_nd/nd_stage_val.py](../../tools/c2_nd/nd_stage_val.py.md) (line 38, via sys.path edit)

### External (third-party)

- `numpy` (lines 39)
- `pytest` (lines 40)

### Standard library

- `__future__` (lines 15)
- `pathlib` (lines 18)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `R1_MARGIN`
- `REPO`

## Classes and functions

- **function `panels`** [L46-51]: `def panels(seq_ids, block)` - c1_data.panels with 1,024 replaced by BLOCK / 4: four panels per block, as at 4,096.
- **function `at`** [L54-58]: `def at(ctx, gate)` - A policy opened at `gate` with every earlier gate done.
- **function `world`** [L62-104]: `def world(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_planted_code_carries_the_contrast`** [L107-112]: `def test_planted_code_carries_the_contrast(world)` - Before rescaling, the head's code part carries a substantial share of the oracle
- **test `test_r1_history_sensitive_with_margin`** [L115-122]: `def test_r1_history_sensitive_with_margin(world)` - R1 PASS on N-R (R), D (R), N-M (M) and the report-only D refit RT, every model.
- **test `test_m0d_every_decoy_passes`** [L125-133]: `def test_m0d_every_decoy_passes(world)` - No INCONCLUSIVE/NUMERICAL D-NULL-R row: (viii) holds for every decoy (D-0158-1).
- **test `test_refits_pass`** [L136-138]: `def test_refits_pass(world)`
- **test `test_known_cases_return_their_constructed_answers`** [L141-149]: `def test_known_cases_return_their_constructed_answers(world)` - KC: D0 USED; D-ONLY USED and NECESSARY; D-DOSE PARTIAL and NOT_NECESSARY. KC-R:
- **test `test_dnull_not_used_at_test_level`** [L152-161]: `def test_dnull_not_used_at_test_level(world)` - The D stream at the TEST level (alpha 1/300; VAL draw count; Y1' as at S4): no model

