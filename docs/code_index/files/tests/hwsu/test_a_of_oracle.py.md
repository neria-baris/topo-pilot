# `tests/hwsu/test_a_of_oracle.py`

- Source: [tests/hwsu/test_a_of_oracle.py](../../../../../tests/hwsu/test_a_of_oracle.py)
- Kind: python
- Lines: 310

## Module docstring

> Author A (job 0198): oracle quantities on the tiny world (protocol §2.3, §2.6 problem O,
> §4.2 OF-1, §5.2 KO1-KO3; DRO3). Expected values come from a test-side forward filter, the
> protocol's formulas and the reused kernels called directly, never from the function under test.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 13, via sys.path edit)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../../tools/hwsu/hwsu_pairs.py.md) (line 14, via sys.path edit)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../../tools/hwsu/hwsu_oracle.py.md) (line 15, via sys.path edit)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 16, via sys.path edit)
- `import hwsu_driver_of` -> [tools/hwsu/hwsu_driver_of.py](../../tools/hwsu/hwsu_driver_of.py.md) (line 17, via sys.path edit)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../../tools/hwsu/hwsu_dry.py.md) (line 18, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 19, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 20, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 21, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../../tools/c2_readout/c2_oracle.py.md) (line 22, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 23, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 28, via package root)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 119, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 25)
- `pytest` (lines 26)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 27)
- `pathlib` (lines 8)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `KO`
- `REPO`

## Classes and functions

- **function `world`** [L35-36]: `def world()` decorators: @pytest.fixture(scope='module')
- **function `pairs`** [L40-42]: `def pairs(world)` decorators: @pytest.fixture(scope='module')
- **function `orc`** [L46-51]: `def orc(world, pairs)` decorators: @pytest.fixture(scope='module')
- **function `feats`** [L54-56]: `def feats(coords)`
- **function `my_filter`** [L59-68]: `def my_filter(T, E, pi, tok)` - Test-side forward filter: last belief b_L and the normalised predictive q̄.
- **test `test_tiny_world_matches_d18`** [L71-82]: `def test_tiny_world_matches_d18(world)`
- **test `test_arm_oracle_against_test_side_filter`** [L85-96]: `def test_arm_oracle_against_test_side_filter(world, pairs, orc)`
- **test `test_suffix_oracle_bitwise_across_arms_and_correct`** [L99-115]: `def test_suffix_oracle_bitwise_across_arms_and_correct(world, pairs, orc)`
- **test `test_helmert_mirror`** [L118-123]: `def test_helmert_mirror()`
- **function `_ko_A`** [L126-133]: `def _ko_A(o1, o2, s1, s2, pc, lam=None)`
- **test `test_ko_logits_and_identities`** [L136-155]: `def test_ko_logits_and_identities(orc)`
- **function `_my_categories`** [L158-180]: `def _my_categories(G, A, seed)` - Protocol §2.9 table and rule 6 with the reused bounds/guard, written out test-side.
- **test `test_ko_categories`** [L183-193]: `def test_ko_categories(orc)`
- **test `test_decimal_rows`** [L196-208]: `def test_decimal_rows(world, pairs, orc)`
- **function `fit`** [L213-216]: `def fit(world)` decorators: @pytest.fixture(scope='module')
- **function `_my_problem`** [L219-225]: `def _my_problem(o, w32, K, euclidean)`
- **test `test_problem_o_is_the_f1_composition`** [L229-243]: `def test_problem_o_is_the_f1_composition(fit, K, euclidean)` decorators: @pytest.mark.parametrize('K,euclidean', [(3, False), (1, False), (3, True)])
- **test `test_problem_o_degenerate_fit_is_not_pass`** [L246-250]: `def test_problem_o_degenerate_fit_is_not_pass(fit)`
- **test `test_share_arrays_and_guard`** [L253-272]: `def test_share_arrays_and_guard(fit, orc)`
- **function `_ctx`** [L276-285]: `def _ctx(tmp_path, world, a1, a2, fit)`
- **function `_status`** [L288-293]: `def _status(fn, ctx)`
- **test `test_of_1_passes_and_fills_ctx`** [L296-303]: `def test_of_1_passes_and_fills_ctx(tmp_path, world, pairs, fit)`
- **test `test_of_1_suffix_defect_is_a_sampler_failure`** [L306-310]: `def test_of_1_suffix_defect_is_a_sampler_failure(tmp_path, world, pairs, fit)`

