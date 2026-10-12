"""Transition kernel builder: max-degree lazy walk on the world's 1-skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from topo_pilot.contracts import ErrorCode, TransitionSpec, WorldSpec

from ._geometry import check_state_order, fail


@dataclass(frozen=True)
class TransitionConfig:
    """Config of the transition kernel: ``kind`` and the self-loop floor ``p_stay`` in [0, 1)."""

    kind: Literal["max_degree_lazy_walk"] = "max_degree_lazy_walk"
    p_stay: float = 0.2


def adjacency(world: WorldSpec) -> np.ndarray:
    """Symmetric 0/1 adjacency ``A [N, N]`` of the world's edge list."""
    n = world.n_states
    A = np.zeros((n, n))
    e = np.asarray(world.edges, dtype=np.int64)
    A[e[:, 0], e[:, 1]] = 1.0
    A[e[:, 1], e[:, 0]] = 1.0
    return A


def check_support(T: np.ndarray, world: WorldSpec) -> None:
    """Require ``supp(T)`` within edges and diagonal (contracts cannot check this, D-011).

    Raises
    ------
    StageFailure
        ``NONSTOCHASTIC`` with detail ``illegal_support`` otherwise.
    """
    allowed = (adjacency(world) > 0) | np.eye(T.shape[0], dtype=bool)
    if np.any((np.asarray(T) > 0) & ~allowed):
        raise fail(ErrorCode.NONSTOCHASTIC, "support", "illegal_support")


class TransitionBuilder:
    """Builds ``TransitionSpec`` from a world; never sees an emission matrix."""

    def build(self, world: WorldSpec, cfg: TransitionConfig) -> TransitionSpec:
        """Max-degree lazy walk.

        Math
        ----
        ``T_ij = (1 - p_stay)/D_max`` for neighbours, ``T_ii = 1 - deg(i)(1 - p_stay)/D_max``,
        ``D_max = max_i deg(i)``, ``pi = 1/N`` (T is symmetric hence doubly stochastic).

        Shapes
        ------
        ``T [N, N] float64``, ``pi [N]``, rows sum to 1.

        Invariants
        ----------
        Symmetric; ``pi T = pi``; support within edges and the diagonal.

        Raises
        ------
        StageFailure
            ``INVALID_CONFIG`` (bad kind or ``p_stay`` outside [0, 1)),
            ``STATE_ORDER_MISMATCH``, ``NONSTOCHASTIC`` (``illegal_support``, or from
            ``validate``), ``STATIONARITY_FAILURE``.
        """
        if cfg.kind != "max_degree_lazy_walk":
            raise fail(ErrorCode.INVALID_CONFIG, "kind", f"unknown kind {cfg.kind!r}")
        if not 0.0 <= cfg.p_stay < 1.0:
            raise fail(ErrorCode.INVALID_CONFIG, "p_stay", f"p_stay={cfg.p_stay} not in [0, 1)")
        check_state_order(world)
        A = adjacency(world)
        deg = A.sum(axis=1)
        d_max = int(deg.max())
        T = (1.0 - cfg.p_stay) / d_max * A
        T[np.diag_indices_from(T)] = 1.0 - deg * (1.0 - cfg.p_stay) / d_max
        check_support(T, world)
        n = T.shape[0]
        spec = TransitionSpec(T=T, pi=np.full(n, 1.0 / n), p_stay=float(cfg.p_stay), d_max=d_max)
        spec.validate()
        return spec
