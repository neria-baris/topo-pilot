# `tests/hwsd/test_a_bounds.py`

- Source: [tests/hwsd/test_a_bounds.py](../../../../../tests/hwsd/test_a_bounds.py)
- Kind: python
- Lines: 238

## Module docstring

> Author A (job 0197): per-checkpoint bounds and F (§5.1, §5.6, §7 row 13; DRD5, S2).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 25, via sys.path edit)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](../../tools/hwsd/hwsd_bind.py.md) (line 26, via sys.path edit)
- `import hwsd_summary` -> [tools/hwsd/hwsd_summary.py](../../tools/hwsd/hwsd_summary.py.md) (line 27, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 28, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 29, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 30, via unique basename)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 13)
- `math` (lines 11)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `HERE`
- `J`
- `REPO`
- `X_KEYS`

## Classes and functions

- **function `own_draws`** [L35-44]: `def own_draws(arrays, seed, draws)` - Independent stream: one PCG64(seed); per draw one integers(0, n, size=n) for all arrays.
- **test `test_rank_constants`** [L48-61]: `def test_rank_constants()`
- **test `test_strong_bounds_ranks_70_and_49931`** [L65-71]: `def test_strong_bounds_ranks_70_and_49931()`
- **test `test_strong_bounds_refuses_bad_draws`** [L75-85]: `def test_strong_bounds_refuses_bad_draws(bad)` decorators: @pytest.mark.parametrize('bad', ['nan', 'inf', 'short'])
- **function `_arrays`** [L89-92]: `def _arrays(n=64, seed=8)`
- **test `test_main_bootstrap_equals_c1_means_and_own_stream`** [L95-104]: `def test_main_bootstrap_equals_c1_means_and_own_stream()`
- **test `test_main_bootstrap_default_seed_inside_binding_and_stream_shared`** [L107-116]: `def test_main_bootstrap_default_seed_inside_binding_and_stream_shared()`
- **function `_scores`** [L120-141]: `def _scores(n=3072, with_arrays=((620301, 100), (620302, 0)), seed=9)`
- **function `_x_arrays`** [L147-151]: `def _x_arrays(sc)`
- **test `test_strong_bootstrap_seed_draws_and_keys_spy`** [L154-172]: `def test_strong_bootstrap_seed_draws_and_keys_spy(monkeypatch, tmp_path)`
- **test `test_strong_bootstrap_bitwise_and_seed_sensitive`** [L176-188]: `def test_strong_bootstrap_bitwise_and_seed_sensitive()` decorators: @pytest.mark.slow
- **test `test_f_sides_planted_and_certified`** [L192-212]: `def test_f_sides_planted_and_certified()`
- **test `test_bootstrap_inputs_d_order_and_values`** [L216-238]: `def test_bootstrap_inputs_d_order_and_values()`

