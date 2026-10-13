"""Predictive metrics, learning gate, and join helper (part b). Pure numpy."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, GateCheck, StageFailure, Status

_COMPONENT = "prediction.PredictiveMetrics"
_NORM_TOL = 1e-6
_G_C_FLOOR = 1e-6


def _fail(code: ErrorCode, check: str, detail: str, comp: str = _COMPONENT) -> StageFailure:
    return StageFailure(code, comp, check, detail)


def _check_dist(name: str, arr: np.ndarray) -> NDArray[np.float64]:
    arr = np.asarray(arr, dtype=np.float64)
    ok = (arr.ndim == 2 and np.all(np.isfinite(arr)) and arr.min(initial=0.0) >= 0.0
          and np.all(np.abs(arr.sum(axis=1) - 1.0) <= _NORM_TOL))
    if not ok:
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "normalised",
                    f"{name} is not a [M, V] distribution within {_NORM_TOL}")
    return arr


class PredictiveMetrics:
    """Pure functions on aligned arrays; all quantities in nats.

    Invariants
    ----------
    Inputs ``[M, V]`` are finite, >= 0, rows sum to 1 within 1e-6.

    Raises
    ------
    NUMERICAL_FAILURE : inputs not normalised, or ``p > 0`` where ``q = 0`` in a KL.
    INVALID_CONFIG : bad bootstrap arguments.
    """

    @staticmethod
    def nll(probs: np.ndarray, targets: np.ndarray) -> np.ndarray:
        """Per-row ``-log probs[i, targets[i]]`` -> ``[M]`` (``inf`` if the probability is 0)."""
        probs = _check_dist("probs", probs)
        idx = np.asarray(targets, dtype=np.int64)
        if idx.shape != (probs.shape[0],):
            raise _fail(ErrorCode.NUMERICAL_FAILURE, "targets", f"targets shape {idx.shape}")
        with np.errstate(divide="ignore"):
            return -np.log(probs[np.arange(len(idx)), idx])

    @staticmethod
    def kl(p: np.ndarray, q: np.ndarray) -> np.ndarray:
        """Rowwise ``KL(p||q) = sum_i p_i log(p_i/q_i)`` with ``0 log 0 = 0``; ``[M, V] -> [M]``."""
        p, q = _check_dist("p", p), _check_dist("q", q)
        if p.shape != q.shape:
            raise _fail(ErrorCode.NUMERICAL_FAILURE, "shape", f"{p.shape} vs {q.shape}")
        if np.any((p > 0) & (q <= 0)):
            raise _fail(ErrorCode.NUMERICAL_FAILURE, "support", "p > 0 where q = 0")
        pos = p > 0
        ratio = np.where(pos, p / np.where(pos, q, 1.0), 1.0)
        return np.maximum(np.sum(np.where(pos, p * np.log(ratio), 0.0), axis=1), 0.0)

    @staticmethod
    def regret(q_oracle: np.ndarray, p_model: np.ndarray) -> float:
        """Mean ``KL(q_C || p_model)`` over rows (exact, not a difference of sampled NLLs)."""
        return float(np.mean(PredictiveMetrics.kl(q_oracle, p_model)))

    @staticmethod
    def captured(regret: float, G_C: float) -> float:
        """``1 - regret / G_C``; ``nan`` when ``G_C <= 1e-6`` (the gate maps it to INCONCLUSIVE)."""
        if not G_C > _G_C_FLOOR:
            return float("nan")
        return float(1.0 - regret / G_C)

    @staticmethod
    def bootstrap_ci(values: np.ndarray, groups: np.ndarray, n: int,
                     rng: np.random.Generator) -> tuple[float, float]:
        """2.5/97.5 percentile CI of the mean from ``n`` resamples of whole groups.

        Each draw samples G groups with replacement and averages all rows of the drawn groups
        (never resamples tokens). ``rng`` is injected.
        """
        values = np.asarray(values, dtype=np.float64)
        groups = np.asarray(groups)
        if values.ndim != 1 or groups.shape != values.shape or n < 1 or values.size == 0:
            raise _fail(ErrorCode.INVALID_CONFIG, "bootstrap", "bad values/groups/n")
        _, inverse = np.unique(groups, return_inverse=True)
        sums = np.bincount(inverse, weights=values)
        counts = np.bincount(inverse).astype(np.float64)
        draws = rng.integers(0, len(sums), size=(n, len(sums)))
        means = sums[draws].sum(axis=1) / counts[draws].sum(axis=1)
        lo, hi = np.percentile(means, [2.5, 97.5])
        return float(lo), float(hi)


class LearningGate:
    """Gate ``captured >= threshold`` (RESEARCH_SUMMARY §6).

    ``evaluate`` returns the ``GateCheck(name="learning_gate", ...)``; ``evaluate_with_status``
    also returns the ``Status``: ``INCONCLUSIVE`` when ``captured`` is NaN (``G_C ~ 0``; check
    has ``passed=False, value=None``), else ``OK`` (a failing gate is still ``OK``).
    """

    def __init__(self, threshold: float = 0.8) -> None:
        self.threshold = float(threshold)

    def evaluate_with_status(self, captured: float) -> tuple[GateCheck, Status]:
        """Return ``(GateCheck, Status)`` for a captured fraction."""
        if captured is None or math.isnan(captured):
            return GateCheck("learning_gate", False, None, self.threshold), Status.INCONCLUSIVE
        passed = bool(captured >= self.threshold)
        return GateCheck("learning_gate", passed, float(captured), self.threshold), Status.OK

    def evaluate(self, captured: float) -> GateCheck:
        """Return the ``GateCheck`` only (see :meth:`evaluate_with_status`)."""
        return self.evaluate_with_status(captured)[0]


def join_by_history_id(ids_a: np.ndarray, ids_b: np.ndarray) -> np.ndarray:
    """One-to-one join: returns ``idx`` with ``ids_b[idx[i]] == ids_a[i]``.

    Raises
    ------
    JOIN_CARDINALITY : different lengths, duplicates, or different id sets (R08).
    """
    a, b = np.asarray(ids_a).astype(str), np.asarray(ids_b).astype(str)
    comp = "prediction.join_by_history_id"
    if a.shape != b.shape or a.ndim != 1:
        raise _fail(ErrorCode.JOIN_CARDINALITY, "length", f"{a.shape} vs {b.shape}", comp)
    if len(set(a.tolist())) != len(a) or len(set(b.tolist())) != len(b):
        raise _fail(ErrorCode.JOIN_CARDINALITY, "duplicates", "duplicate history_id", comp)
    if set(a.tolist()) != set(b.tolist()):
        raise _fail(ErrorCode.JOIN_CARDINALITY, "id_sets", "history_id sets differ", comp)
    position = {h: i for i, h in enumerate(b.tolist())}
    return np.array([position[h] for h in a.tolist()], dtype=np.int64)
