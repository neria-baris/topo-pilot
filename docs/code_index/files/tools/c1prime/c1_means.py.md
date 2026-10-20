# `tools/c1prime/c1_means.py`

- Source: [tools/c1prime/c1_means.py](../../../../../tools/c1prime/c1_means.py)
- Kind: python
- Lines: 79

## Module docstring

> C1' balanced-tree means, bootstrap index streams and order-statistic ranks (API.md §6;
> protocol §15.3.2 C7, §3.5, §11, §12.3). One rng.integers(0, n, size=n) call per draw, in draw
> order, shared by every array; quantiles by inverted_cdf with a run-time rank check.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 10, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 12, via same directory)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 8)
- `math` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_b_inference.py](../../tests/c1prime/test_b_inference.py.md) (line 30, import)
- [tests/k4b/test_a_ranks_ladder.py](../../tests/k4b/test_a_ranks_ladder.py.md) (line 25, import)
- [tests/k4b/test_a_width_b4.py](../../tests/k4b/test_a_width_b4.py.md) (line 27, import)
- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 27, import)
- [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 12, import)
- [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 14, import)
- [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 28, import)
- [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 25, import)
- [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 9, import)
- [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 15, import)

## Top-level constants

- `P_THIRD`

## Classes and functions

- **function `tree_mean`** [L15-28]: `def tree_mean(X) -> np.ndarray` - Mean over the last axis: adjacent pairs added level by level (an unmatched last entry is
- **function `bootstrap_means`** [L31-43]: `def bootstrap_means(arrays, seed, draws=5000) -> dict`
- **function `c1_bootstrap_means`** [L46-54]: `def c1_bootstrap_means(x, rng, draws) -> np.ndarray` - The H5 wrapper: bootstrap_profile's index stream, the certified tree mean.
- **function `rank_for`** [L57-60]: `def rank_for(p, draws=5000) -> int` - One-based inverted_cdf rank ceil(draws * p), with p read as the exact decimal it names.
- **function `rank_check`** [L66-68]: `def rank_check(values, v, k) -> bool`
- **function `quantile_with_rank`** [L71-79]: `def quantile_with_rank(values, p) -> tuple` - np.quantile(..., method="inverted_cdf") and its verified rank (failure -> NUMERICAL).

