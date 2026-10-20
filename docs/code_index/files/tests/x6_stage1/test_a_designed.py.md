# `tests/x6_stage1/test_a_designed.py`

- Source: [tests/x6_stage1/test_a_designed.py](../../../../../tests/x6_stage1/test_a_designed.py)
- Kind: python
- Lines: 281

## Module docstring

> Author A: T-DESIGN (X6S1-FROZEN-v1 §2.5, §6.3, §14.3; API.md §4.3, §7 designed_stats).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 21, via sys.path edit)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../../tools/x6_stage1/x6s1_pairs.py.md) (line 22, via sys.path edit)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../../tools/x6_stage1/x6s1_eval.py.md) (line 23, via sys.path edit)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../../tools/x6_stage1/x6s1_stats.py.md) (line 24, via sys.path edit)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../../tools/x6_stage0/x6_exact.py.md) (line 28, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 29, via sys.path edit)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 6)
- `collections` (lines 10)
- `fractions` (lines 11)
- `functools` (lines 8, 12)
- `pathlib` (lines 13)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`
- line 27: `str(REPO / 'tools' / 'x6_stage0')` -> `tools/x6_stage0`

## Imported by

- none

## Top-level constants

- `FAMILIES`
- `FLOOR`
- `REPO`
- `S7`
- `STAGE0`

## Classes and functions

- **function `walks`** [L41-48]: `def walks(n_rows: int, seed: int) -> np.ndarray`
- **function `prefix_pool`** [L52-53]: `def prefix_pool()` decorators: @lru_cache(maxsize=None)
- **function `my_natural_prefixes`** [L56-63]: `def my_natural_prefixes(tokens, rnd)`
- **function `my_history`** [L66-71]: `def my_history(prefix, letters, y)` - API-AMBIGUITY: API §4.3 says 'prefix + cue + tokens of the loops ... as
- **function `segment_stats`** [L74-77]: `def segment_stats(h)`
- **function `cue_frac`** [L80-82]: `def cue_frac(q)`
- **function `sub`** [L85-86]: `def sub(a, b)`
- **function `dot`** [L89-90]: `def dot(a, b)`
- **function `some_prefixes`** [L93-95]: `def some_prefixes()`
- **test `test_registered_constants_and_flat_face`** [L99-105]: `def test_registered_constants_and_flat_face()`
- **test `test_designed_history_composition`** [L108-118]: `def test_designed_history_composition()`
- **test `test_matched_statistics_and_control_spread_zero`** [L122-143]: `def test_matched_statistics_and_control_spread_zero()`
- **test `test_prefix_invariance_of_qstar`** [L146-155]: `def test_prefix_invariance_of_qstar()`
- **function `_w2_beta`** [L159-167]: `def _w2_beta(law_fn)`
- **test `test_w2_beta_table_and_per_cue_heuristics`** [L170-188]: `def test_w2_beta_table_and_per_cue_heuristics()`
- **test `test_w2_beta_zero_for_every_ladder_statistic`** [L192-195]: `def test_w2_beta_zero_for_every_ladder_statistic()` decorators: @pytest.mark.slow
- **test `test_natural_prefix_rule_independent`** [L199-205]: `def test_natural_prefix_rule_independent()`
- **function `designed`** [L209-210]: `def designed()` decorators: @lru_cache(maxsize=None)
- **test `test_designed_set_structure`** [L213-235]: `def test_designed_set_structure()`
- **test `test_designed_arrays_and_digest`** [L238-253]: `def test_designed_arrays_and_digest()`
- **test `test_designed_stats_oracle_and_heuristic_references`** [L258-281]: `def test_designed_stats_oracle_and_heuristic_references()` decorators: @pytest.mark.slow

