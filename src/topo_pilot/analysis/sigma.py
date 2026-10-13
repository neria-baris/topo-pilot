"""SigmaCalibrator: the pre-registered sigma selection rule (RESEARCH_SUMMARY section 4)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Sequence

from topo_pilot.contracts import ErrorCode, StageFailure


@dataclass(frozen=True)
class SigmaRow:
    """Calibration measurements for one (sigma, world) pair (V symbols)."""

    sigma: float
    world: str
    mean_H_b1: float
    G_C: float
    min_p_w: float
    V: int


@dataclass(frozen=True)
class SigmaDecision:
    """Outcome: ``status`` in ``ok | weak_context | stop_H3``; ``sigma`` is None on stop."""

    sigma: float | None
    status: str
    reasons: tuple[str, ...]
    table: tuple[dict[str, Any], ...]


class SigmaCalibrator:
    """Select sigma by the first-passing rule with a weak-context fallback.

    Math
    ----
    Candidates are the sigma values in order of first appearance in ``rows``. A candidate
    passes iff in every world: ``mean_H_b1 >= log 2``, ``G_C >= 0.10`` nats and
    ``min_p_w >= 0.5 / V``. If none passes, take the candidate with the largest
    ``min_world G_C`` (ties: earliest); if that value is ``>= 0.03`` the status is
    ``weak_context``, otherwise ``stop_H3`` with ``sigma = None``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if ``rows`` is empty or contains a non-finite measurement.
    """

    def __init__(self, min_entropy: float = math.log(2.0), min_gc: float = 0.10,
                 min_p_factor: float = 0.5, fallback_gc: float = 0.03):
        self.min_entropy = min_entropy
        self.min_gc = min_gc
        self.min_p_factor = min_p_factor
        self.fallback_gc = fallback_gc

    def _row_failures(self, r: SigmaRow) -> list[str]:
        fails = []
        if not r.mean_H_b1 >= self.min_entropy:
            fails.append(f"{r.world}: mean_H_b1={r.mean_H_b1:.4g} < {self.min_entropy:.4g}")
        if not r.G_C >= self.min_gc:
            fails.append(f"{r.world}: G_C={r.G_C:.4g} < {self.min_gc:.4g}")
        if not r.min_p_w >= self.min_p_factor / r.V:
            fails.append(f"{r.world}: min_p_w={r.min_p_w:.4g} < {self.min_p_factor / r.V:.4g}")
        return fails

    def select(self, rows: Sequence[SigmaRow]) -> SigmaDecision:
        """Apply the rule to rows ordered by candidate priority (see class docstring)."""
        if not rows or any(not all(map(math.isfinite, (r.mean_H_b1, r.G_C, r.min_p_w)))
                           for r in rows):
            raise StageFailure(ErrorCode.INVALID_CONFIG, "analysis.SigmaCalibrator", "rows",
                               "rows empty or containing non-finite measurements")
        order = list(dict.fromkeys(r.sigma for r in rows))
        table = []
        for s in order:
            group = [r for r in rows if r.sigma == s]
            fails = [f for r in group for f in self._row_failures(r)]
            table.append({"sigma": s, "passes": not fails, "failures": tuple(fails),
                          "min_G_C": min(r.G_C for r in group)})
        for entry in table:
            if entry["passes"]:
                return SigmaDecision(entry["sigma"], "ok",
                                     (f"sigma={entry['sigma']} passes in all worlds",),
                                     tuple(table))
        best = max(table, key=lambda e: e["min_G_C"])  # max() keeps the earliest tie
        if best["min_G_C"] >= self.fallback_gc:
            return SigmaDecision(best["sigma"], "weak_context",
                                 (f"no candidate passes; sigma={best['sigma']} has the highest "
                                  f"min-world G_C={best['min_G_C']:.4g} >= {self.fallback_gc}",),
                                 tuple(table))
        return SigmaDecision(None, "stop_H3",
                             (f"no candidate passes and the best min-world G_C="
                              f"{best['min_G_C']:.4g} < {self.fallback_gc}: go to checkpoint H3",),
                             tuple(table))
