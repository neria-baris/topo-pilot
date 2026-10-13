"""Dynamics (checkpoint-order null) and the minimal LayerSweep."""

from __future__ import annotations

import math

import numpy as np

from topo_pilot.contracts import ArtifactStore, ErrorCode, StageFailure

from .pointset import PointSet, ph_summary
from .spaces import SpaceBuilder

_COMPONENT = "analysis.Dynamics"


def _first_third_share(values: np.ndarray) -> float:
    steps = np.abs(np.diff(values))
    total = float(steps.sum())
    if total == 0.0:
        return float("nan")
    return float(steps[:math.ceil(steps.size / 3)].sum() / total)


class Dynamics:
    """Descriptive checkpoint-order permutation null (not a replicate-level test).

    Math
    ----
    ``stat = sum_{first ceil((n-1)/3) diffs} |dS| / sum |dS|`` over consecutive checkpoints;
    ``p = (1 + #{perm stat >= observed}) / (1 + n_perm)`` over ``rng.permutation`` of the order.

    Shapes
    ------
    ``values: [n_ckpt]`` (S per checkpoint, in training order), ``n_ckpt >= 2``.

    Invariants
    ----------
    Total ``|dS| = 0`` gives ``statistic = nan`` and ``p_value = 1.0``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` for fewer than 2 values or ``n_perm < 1``.
    """

    def checkpoint_order_null(self, values, n_perm: int, rng) -> dict:
        """Return ``{"statistic", "p_value"}``."""
        v = np.asarray(values, dtype=np.float64)
        if v.ndim != 1 or v.size < 2 or n_perm < 1:
            raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "args",
                               "need a 1-D series of >= 2 values and n_perm >= 1")
        observed = _first_third_share(v)
        if math.isnan(observed):
            return {"statistic": float("nan"), "p_value": 1.0}
        hits = sum(_first_third_share(rng.permutation(v)) >= observed for _ in range(n_perm))
        return {"statistic": observed, "p_value": (1.0 + hits) / (1.0 + n_perm)}


class LayerSweep:
    """Secondary analysis: S_H1 for every hook and for the concatenation of all hooks.

    Shapes
    ------
    One dict per hook plus ``"concat"``: ``{"hook", "S_H1", "scale_s", "status", "n_points"}``
    (Euclidean, via ``ph_summary``; statuses propagate).
    """

    def run(self, activation_set_id: str, panel: int, store: ArtifactStore) -> list[dict]:
        """Sweep all hooks of one ActivationSet on one panel."""
        builder = SpaceBuilder(store)
        hooks = builder.hooks(activation_set_id)
        sets = [builder.activations(activation_set_id, h, panel) for h in hooks]
        concat = PointSet("act:concat", np.hstack([s.X for s in sets]), None, list(sets[0].ids),
                          "euclidean")
        return [{"hook": name, **ph_summary(ps)}
                for name, ps in zip([*hooks, "concat"], [*sets, concat])]
