"""X5 G1 training endpoint (x5g1-train-v3 §4–§6): grid-defined event, infinity-safe bounds,
paired whole-curve bootstrap and the all-pair cohort rule. Pure; no I/O, no torch.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

GRID: tuple[int, ...] = tuple(range(0, 1001, 100)) + tuple(range(1250, 5001, 250))
THRESHOLD = 0.05
DELAY = 250
X5_GRID, X5_THRESHOLD, X5_DELAY = GRID, THRESHOLD, DELAY  # package-root aliases


@dataclass(frozen=True)
class GridEvent:
    """Observed: ``tau = lower = upper = t_j``. Censored: ``tau None``, ``lower = grid[-3]``
    (strict), ``upper = inf``; ``trailing_pass`` lists unconfirmed PASS steps in the last two
    positions (descriptive)."""

    tau: int | None
    lower: float
    upper: float
    censored: bool
    lower_strict: bool
    trailing_pass: tuple[int, ...] = ()


@dataclass(frozen=True)
class DiffBounds:
    """Bounds on ``Delta = tau(curved) - tau(flat)``; ``*_strict`` marks open bounds."""

    low: float
    high: float
    low_strict: bool
    high_strict: bool


@dataclass(frozen=True)
class BootstrapResult:
    d_low: NDArray[np.float64]
    d_high: NDArray[np.float64]
    censored_curved: NDArray[np.bool_]
    censored_flat: NDArray[np.bool_]
    q025_low: float
    q975_high: float
    censored_curved_frac: float
    censored_flat_frac: float


@dataclass(frozen=True)
class PairEvidence:
    point: DiffBounds
    q025_low: float
    q975_high: float
    events: tuple[GridEvent, GridEvent]


def _check_grid(grid: Sequence[int]) -> tuple[int, ...]:
    g = tuple(int(t) for t in grid)
    if len(g) < 3 or any(b <= a for a, b in zip(g, g[1:])):
        raise ValueError(f"grid must be strictly increasing with >= 3 points, got {g}")
    return g


def pass_sequence(ratios, threshold: float = THRESHOLD) -> NDArray[np.bool_]:
    """``ratios <= threshold`` element-wise; NaN is an error."""
    r = np.asarray(ratios, dtype=np.float64)
    if np.any(np.isnan(r)):
        raise ValueError("NaN ratio")
    return r <= threshold


def grid_event(passes: Sequence, grid: Sequence[int] = GRID) -> GridEvent:
    """First ``t_j`` with PASS at ``j, j+1, j+2`` (``j <= len(grid) - 3``), else censored."""
    g = _check_grid(grid)
    p = list(passes)
    if len(p) != len(g):
        raise ValueError(f"{len(p)} PASS values for a {len(g)}-point grid")
    if not all(isinstance(x, (bool, np.bool_)) for x in p):
        raise ValueError("PASS values must be bool (an incomplete curve is a failed model)")
    for j in range(len(g) - 2):
        if p[j] and p[j + 1] and p[j + 2]:
            return GridEvent(g[j], float(g[j]), float(g[j]), False, False)
    trailing = tuple(g[k] for k in (len(g) - 2, len(g) - 1) if p[k])
    return GridEvent(None, float(g[-3]), math.inf, True, True, trailing)


def difference_bounds(curved: GridEvent, flat: GridEvent) -> DiffBounds:
    """``low = Lc - Uf``, ``high = Uc - Lf``; lowers are finite, so never NaN."""
    return DiffBounds(curved.lower - flat.upper, curved.upper - flat.lower,
                      curved.censored and not flat.censored,
                      flat.censored and not curved.censored)


def ratio_curve(regret, gc: float) -> NDArray[np.float64]:
    """``regret[R, K].mean(axis=0) / gc``."""
    r = np.asarray(regret, dtype=np.float64)
    if r.ndim != 2 or r.shape[0] < 1:
        raise ValueError(f"regret must be [R >= 1, K], got {r.shape}")
    if not (math.isfinite(gc) and gc > 0):
        raise ValueError(f"gc must be finite and > 0, got {gc}")
    return r.mean(axis=0) / gc


def quantile_inverted_cdf(values, q: float) -> float:
    """The ``k``-th smallest value, ``k = max(1, ceil(q n - 1e-9))``; works with +-inf."""
    v = np.asarray(values, dtype=np.float64).ravel()
    if v.size == 0 or np.any(np.isnan(v)) or not 0.0 <= q <= 1.0:
        raise ValueError("quantile needs non-empty, NaN-free values and q in [0, 1]")
    k = max(1, math.ceil(q * v.size - 1e-9))
    return float(np.sort(v)[k - 1])


def _event_from_regret(reg: NDArray, gc: float, grid: tuple[int, ...],
                       threshold: float) -> GridEvent:
    return grid_event(list(pass_sequence(ratio_curve(reg, gc), threshold)), grid)


def paired_bootstrap_endpoint(reg_curved, reg_flat, gc_curved: float, gc_flat: float,
                              rng: np.random.Generator, n_draws: int = 2000, batch: int = 500,
                              grid: Sequence[int] = GRID, threshold: float = THRESHOLD,
                              guard: Callable[[str], None] | None = None) -> BootstrapResult:
    """One shared ``rng.integers(0, R, size=R)`` per draw, applied to whole rows of both arms."""
    g = _check_grid(grid)
    rc, rf = np.asarray(reg_curved, np.float64), np.asarray(reg_flat, np.float64)
    if rc.ndim != 2 or rc.shape != rf.shape or rc.shape[1] != len(g) or rc.shape[0] < 1:
        raise ValueError(f"regret shapes {rc.shape} / {rf.shape} vs grid {len(g)}")
    n = rc.shape[0]
    d_low, d_high = np.empty(n_draws), np.empty(n_draws)
    cc, cf = np.zeros(n_draws, dtype=bool), np.zeros(n_draws, dtype=bool)
    for start in range(0, n_draws, batch):
        if guard:
            guard(f"bootstrap {start}")
        for j in range(start, min(start + batch, n_draws)):
            idx = rng.integers(0, n, size=n)
            ec = _event_from_regret(rc[idx], gc_curved, g, threshold)
            ef = _event_from_regret(rf[idx], gc_flat, g, threshold)
            b = difference_bounds(ec, ef)
            d_low[j], d_high[j], cc[j], cf[j] = b.low, b.high, ec.censored, ef.censored
        if guard:
            guard(f"bootstrap {start} done")
    return BootstrapResult(d_low, d_high, cc, cf, quantile_inverted_cdf(d_low, 0.025),
                           quantile_inverted_cdf(d_high, 0.975), float(cc.mean()),
                           float(cf.mean()))


def pair_evidence(reg_curved, reg_flat, gc_curved: float, gc_flat: float,
                  rng: np.random.Generator, **kw) -> PairEvidence:
    """Point events from the full-sample curves; quantiles from the paired bootstrap."""
    g = _check_grid(kw.get("grid", GRID))
    thr = kw.get("threshold", THRESHOLD)
    ec = _event_from_regret(np.asarray(reg_curved, np.float64), gc_curved, g, thr)
    ef = _event_from_regret(np.asarray(reg_flat, np.float64), gc_flat, g, thr)
    boot = paired_bootstrap_endpoint(reg_curved, reg_flat, gc_curved, gc_flat, rng, **kw)
    return PairEvidence(difference_bounds(ec, ef), boot.q025_low, boot.q975_high, (ec, ef))


def pair_flags(ev: PairEvidence) -> tuple[bool, bool]:
    """``(supported, rejected)`` for one pair (protocol §6)."""
    return (ev.point.low >= DELAY and ev.q025_low > 0), ev.q975_high < DELAY


def cohort_verdict(pairs: Sequence[PairEvidence | None], failures: Sequence[str] = (),
                   n_required: int = 3) -> tuple[str, str]:
    """All-pair rule; contradiction, failures, missing or failed pairs give INCONCLUSIVE."""
    if failures:
        return "INCONCLUSIVE", "failures: " + "; ".join(map(str, failures))
    if len(pairs) != n_required:
        return "INCONCLUSIVE", f"{len(pairs)} pairs, {n_required} required"
    if any(p is None for p in pairs):
        return "INCONCLUSIVE", "a pair has a failed, incomplete or lost model"
    flags = [pair_flags(p) for p in pairs]
    supported = all(s for s, _ in flags)
    rejected = any(r for _, r in flags)
    if supported and rejected:
        return "INCONCLUSIVE", "contradiction: all pairs supported and some pair rejected"
    if supported:
        return "SUPPORTED", "every pair: D_low >= 250 and bootstrap 2.5% of D_low* > 0"
    if rejected:
        return "REJECTED", "some pair: bootstrap 97.5% of D_high* < 250"
    return "INCONCLUSIVE", "neither the support nor the rejection condition holds"


def dev_auc(ratios, grid: Sequence[int] = GRID) -> float:
    """Trapezoid area of the ratio curve over the actual step values."""
    g = np.asarray(_check_grid(grid), dtype=np.float64)
    r = np.asarray(ratios, dtype=np.float64)
    if r.shape != g.shape:
        raise ValueError(f"ratios {r.shape} vs grid {g.shape}")
    return float(np.sum((g[1:] - g[:-1]) * (r[1:] + r[:-1]) / 2.0))
