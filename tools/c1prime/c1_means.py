"""C1' balanced-tree means, bootstrap index streams and order-statistic ranks (API.md §6;
protocol §15.3.2 C7, §3.5, §11, §12.3). One rng.integers(0, n, size=n) call per draw, in draw
order, shared by every array; quantiles by inverted_cdf with a run-time rank check."""

from __future__ import annotations

import math
from fractions import Fraction

import c1_config  # noqa: F401  (sys.path)
import numpy as np
from c1_records import C1GateFailure


def tree_mean(X) -> np.ndarray:
    """Mean over the last axis: adjacent pairs added level by level (an unmatched last entry is
    carried), then one division by n (exactly representable)."""
    level = np.asarray(X, dtype=np.float64)
    n = level.shape[-1]
    if n < 1:
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "tree_mean of an empty array")
    while level.shape[-1] > 1:
        m = (level.shape[-1] // 2) * 2
        pairs = level[..., 0:m:2] + level[..., 1:m:2]
        if level.shape[-1] % 2:
            pairs = np.concatenate((pairs, level[..., m:]), axis=-1)
        level = pairs
    return level[..., 0] / float(n)


def bootstrap_means(arrays, seed, draws=5000) -> dict:
    names = list(arrays)
    data = {k: np.asarray(arrays[k], dtype=np.float64) for k in names}
    n = data[names[0]].shape[0]
    if any(a.shape != (n,) for a in data.values()):
        raise C1GateFailure("FAIL_TECHNICAL", "bootstrap arrays must share one 1-d length")
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    out = {k: np.empty(int(draws)) for k in names}
    for d in range(int(draws)):
        idx = rng.integers(0, n, size=n)
        for k in names:
            out[k][d] = tree_mean(data[k][idx])
    return out


def c1_bootstrap_means(x, rng, draws) -> np.ndarray:
    """The H5 wrapper: bootstrap_profile's index stream, the certified tree mean."""
    x = np.asarray(x, dtype=np.float64)
    n = x.shape[0]
    out = np.empty(int(draws))
    for d in range(int(draws)):
        idx = rng.integers(0, n, size=n)
        out[d] = tree_mean(x[idx])
    return out


def rank_for(p, draws=5000) -> int:
    """One-based inverted_cdf rank ceil(draws * p), with p read as the exact decimal it names."""
    p = p if isinstance(p, Fraction) else Fraction(repr(float(p)))
    return max(1, math.ceil(Fraction(int(draws)) * p))


P_THIRD = Fraction(5, 300)  # 0.05/3 as an exact rational


def rank_check(values, v, k) -> bool:
    values = np.asarray(values, dtype=np.float64)
    return int(np.count_nonzero(values < v)) < int(k) <= int(np.count_nonzero(values <= v))


def quantile_with_rank(values, p) -> tuple:
    """np.quantile(..., method="inverted_cdf") and its verified rank (failure -> NUMERICAL)."""
    values = np.asarray(values, dtype=np.float64)
    pf = float(p) if not isinstance(p, Fraction) else float(p)
    v = float(np.quantile(values, pf, method="inverted_cdf"))
    k = rank_for(p, len(values))
    if not rank_check(values, v, k):
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", f"rank check failed (rank {k})")
    return v, k
