# `tests/k4b/test_a_ranks_ladder.py`

- Source: [tests/k4b/test_a_ranks_ladder.py](../../../../../tests/k4b/test_a_ranks_ladder.py)
- Kind: python
- Lines: 272

## Module docstring

> K4b author A, TEST_PLAN A7, A9 (protocol §5.4, §7.1, §7.2).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 25, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 26, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 27, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 28, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 29, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 12)
- `math` (lines 10)
- `pathlib` (lines 13)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `ALPHA`
- `KEYS`
- `MODELS`
- `NDRAW`
- `REPO`

## Classes and functions

- **function `leaves`** [L38-48]: `def leaves(x)`
- **function `numbers`** [L51-53]: `def numbers(x)`
- **function `val`** [L56-57]: `def val(x)`
- **function `f_plan`** [L61-62]: `def f_plan()` decorators: @pytest.fixture(scope='module')
- **test `test_rank_constants`** [L67-77]: `def test_rank_constants()`
- **test `test_bounds_ranks_on_distinct_draws`** [L80-88]: `def test_bounds_ranks_on_distinct_draws()`
- **test `test_bounds_with_ties`** [L91-94]: `def test_bounds_with_ties()`
- **test `test_bounds_rank_check_failure_is_numerical`** [L97-101]: `def test_bounds_rank_check_failure_is_numerical()`
- **function `designed_e`** [L106-115]: `def designed_e(fail_minus, fail_plus)` - '-' column: -0.01 on the fail set (>= 84 draws, so q_alpha = -0.01), else 0.001.
- **function `ref_projection`** [L118-135]: `def ref_projection(e, F)`
- **function `counts`** [L138-140]: `def counts(res)`
- **test `test_projection_exact_threshold_passes`** [L143-148]: `def test_projection_exact_threshold_passes(f_plan)`
- **test `test_projection_joint_one_below_fails`** [L151-158]: `def test_projection_joint_one_below_fails(f_plan)`
- **test `test_projection_exclusion_per_model_one_below_fails`** [L161-170]: `def test_projection_exclusion_per_model_one_below_fails(f_plan)`
- **test `test_projection_support_per_model_one_below_fails`** [L173-178]: `def test_projection_support_per_model_one_below_fails(f_plan)`
- **function `_random_X`** [L181-186]: `def _random_X(seed, shift=None, n=3072)`
- **test `test_centered_is_precision_centered_draws`** [L189-194]: `def test_centered_is_precision_centered_draws()`
- **test `test_projection_matches_reference_and_is_mean_shift_invariant`** [L197-207]: `def test_projection_matches_reference_and_is_mean_shift_invariant(f_plan)`
- **test `test_mde_ok_boundary`** [L212-221]: `def test_mde_ok_boundary(f_plan)`
- **function `_alternating`** [L226-227]: `def _alternating(c, n=3072)`
- **function `_ladder_inputs`** [L230-232]: `def _ladder_inputs(c, r)`
- **test `test_ladder_passes_at_3072`** [L235-241]: `def test_ladder_passes_at_3072(f_plan)`
- **test `test_ladder_passes_at_6144`** [L244-262]: `def test_ladder_passes_at_6144(f_plan)` - SD 0.2: MDE fails at 3,072 (0.2082 > 0.02) and passes at 6,144 (0.0177).
- **test `test_ladder_underpowered`** [L265-272]: `def test_ladder_underpowered(f_plan)`

