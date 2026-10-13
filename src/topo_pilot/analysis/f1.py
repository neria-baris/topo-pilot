"""F1Decision: the pre-registered F1 decision rule (RESEARCH_SUMMARY 7.4), pure functions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.F1Decision"
_WORLDS = ("cylinder", "square")
_CKPTS = ("init", "final")


@dataclass(frozen=True)
class F1Verdict:
    """Outcome of the F1 rule.

    ``status`` in ``SUPPORTED | REJECTED | INCONCLUSIVE``; ``reasons`` name every failed gate or
    condition; ``details`` has one dict per replicate with ``n_positive, median_D, u, cond1,
    cond2``.
    """

    status: str
    reasons: tuple[str, ...]
    details: tuple[dict, ...]


def _fail(check: str, detail: str) -> StageFailure:
    return StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, check, detail)


def _panels(S: Mapping[tuple[str, str, int], float]) -> list[int]:
    panels = sorted({int(k[2]) for k in S})
    for world in _WORLDS:
        for ckpt in _CKPTS:
            for p in panels:
                if (world, ckpt, p) not in S:
                    raise _fail("missing_cell", f"S has no entry for {(world, ckpt, p)}")
    return panels


@dataclass(frozen=True)
class F1Decision:
    """The F1 rule: contrasts D_i, noise envelope u, and the replicate-level verdict.

    Math
    ----
    ``D_i = (S[cyl,final,i] - S[cyl,init,i]) - (S[sq,final,i] - S[sq,init,i])``;
    ``u = max_c percentile_{100 q}({|S_{c,i} - S_{c,j}| : i < j})`` over the four cells
    (numpy linear interpolation). Per replicate: cond1 = ``#{D_i > 0} >= min_positive_panels``,
    cond2 = ``median(D) > u`` (strict). SUPPORTED iff both hold in every replicate.

    Shapes
    ------
    ``S``: mapping ``(world in {"cylinder","square"}, ckpt in {"init","final"}, panel) -> float``.
    ``D``: float64 ``[n_panels]`` ordered by sorted panel id.

    Invariants
    ----------
    Verdict precedence: learning gate, input status, replicate count (all INCONCLUSIVE), then
    REJECTED / SUPPORTED. Statuses are returned, never raised.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` for a missing S key or gate / replicate length mismatch.
    """

    min_positive_panels: int = 7
    envelope_quantile: float = 0.95
    min_replicates: int = 3

    def contrasts(self, S: Mapping[tuple[str, str, int], float]) -> NDArray[np.float64]:
        """Return D (see class docstring)."""
        panels = _panels(S)
        return np.array([
            (S[("cylinder", "final", p)] - S[("cylinder", "init", p)])
            - (S[("square", "final", p)] - S[("square", "init", p)]) for p in panels],
            dtype=np.float64)

    def noise_envelope(self, S: Mapping[tuple[str, str, int], float]) -> float:
        """Return u, the largest cell-wise quantile of pairwise panel differences."""
        panels = _panels(S)
        iu = np.triu_indices(len(panels), k=1)
        best = 0.0
        for world in _WORLDS:
            for ckpt in _CKPTS:
                v = np.array([S[(world, ckpt, p)] for p in panels], dtype=np.float64)
                diffs = np.abs(v[:, None] - v[None, :])[iu]
                if diffs.size:
                    best = max(best, float(np.percentile(diffs, 100.0 * self.envelope_quantile)))
        return best

    def _detail(self, D: NDArray[np.float64], u: float) -> dict:
        D = np.asarray(D, dtype=np.float64)
        n_pos = int(np.sum(D > 0.0))
        med = float(np.median(D))
        return {"n_positive": n_pos, "median_D": med, "u": float(u),
                "cond1": n_pos >= self.min_positive_panels, "cond2": bool(med > u)}

    def verdict(self, per_replicate: Sequence[tuple[NDArray[np.float64], float]],
                learning_gate_passed: Sequence[bool],
                input_statuses: Sequence[str] = ()) -> F1Verdict:
        """Apply the rule to ``[(D_r, u_r)]`` with one learning-gate flag per replicate."""
        if len(learning_gate_passed) != len(per_replicate):
            raise _fail("gate_length", "one learning-gate flag per replicate is required")
        details = tuple(self._detail(D, u) for D, u in per_replicate)
        reasons: list[str] = []
        for r, ok in enumerate(learning_gate_passed):
            if not ok:
                reasons.append(f"learning_gate failed for replicate {r}")
        bad = [s for s in input_statuses if s != "ok"]
        if bad:
            reasons.append(f"input status not ok: {sorted(set(bad))}")
        if len(per_replicate) < self.min_replicates:
            reasons.append(f"replicates: {len(per_replicate)} < {self.min_replicates}")
        if reasons:
            return F1Verdict("INCONCLUSIVE", tuple(reasons), details)
        for r, d in enumerate(details):
            if not d["cond1"]:
                reasons.append(f"replicate {r}: cond1 failed ({d['n_positive']} positive panels)")
            if not d["cond2"]:
                reasons.append(f"replicate {r}: cond2 failed (median D {d['median_D']:.4g} "
                               f"<= u {d['u']:.4g})")
        return F1Verdict("REJECTED" if reasons else "SUPPORTED", tuple(reasons), details)
