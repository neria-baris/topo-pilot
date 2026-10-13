"""Metric-conductance transition kernel on a fixed lattice (X5 G1, x5g1-feas-v2 §2).

The world complex and its metric literal are unchanged; the warp profile, edge lengths and
conductances travel as explicit metadata of the TransitionSpec artifact.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, TransitionSpec, WorldSpec

from ._geometry import check_state_order, fail
from .transition import adjacency, check_support


@dataclass(frozen=True)
class ConductanceConfig:
    """Warp amplitude ``a`` (|a| < 1) and total off-diagonal mass at ``C_max`` (``move``)."""

    a: float = 0.20
    move: float = 0.8


def warp_profile(dims: tuple[int, int],
                 a: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Warped circumference profile and horizontal edge lengths.

    Math
    ----
    ``R = dims[0] / (2 pi)``; ``f(y) = R (1 + a cos(2 pi y / (ny - 1)))``;
    ``l_h(y) = f(y) 2 pi / dims[0] = 1 + a cos(2 pi y / (ny - 1))``, ``y = 0..ny-1``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if ``|a| >= 1`` or ``ny < 2``.
    """
    nx, ny = int(dims[0]), int(dims[1])
    if not abs(a) < 1.0 or ny < 2:
        raise fail(ErrorCode.INVALID_CONFIG, "warp", f"a={a}, ny={ny}")
    wave = 1.0 + a * np.cos(2.0 * np.pi * np.arange(ny) / (ny - 1))
    return nx / (2.0 * np.pi) * wave, wave


def conductance_kernel(world: WorldSpec, cfg: ConductanceConfig) -> tuple[TransitionSpec, dict]:
    """Symmetric lazy kernel from edge conductances ``c = 1 / l^2``.

    Math
    ----
    Horizontal edges (same y) have length ``l_h(y)``, vertical edges (same x) length 1;
    ``C_max = max_i sum_j c_ij``; ``T_ij = move c_ij / C_max`` (i != j),
    ``T_ii = 1 - move sum_j c_ij / C_max``; ``pi = 1/N``. At ``a = 0`` this is the
    max-degree lazy walk with ``p_stay = 1 - move``.

    Raises
    ------
    StageFailure
        ``STATE_ORDER_MISMATCH`` (state order, or an edge that is neither horizontal nor
        vertical), ``INVALID_CONFIG`` (warp), ``NONSTOCHASTIC`` / ``STATIONARITY_FAILURE``.
    """
    check_state_order(world)
    _, l_h = warp_profile(tuple(world.dims), cfg.a)
    coords = np.asarray(world.coords, dtype=np.float64)
    e = np.asarray(world.edges, dtype=np.int64)
    same_y = coords[e[:, 0], 1] == coords[e[:, 1], 1]
    same_x = coords[e[:, 0], 0] == coords[e[:, 1], 0]
    if np.any(~(same_x ^ same_y)):
        raise fail(ErrorCode.STATE_ORDER_MISMATCH, "edge_class", "edge neither horizontal nor "
                   "vertical")
    n = coords.shape[0]
    c = np.zeros((n, n))
    w = np.where(same_y, 1.0 / l_h[coords[e[:, 0], 1].astype(np.int64)] ** 2, 1.0)
    c[e[:, 0], e[:, 1]] = w
    c[e[:, 1], e[:, 0]] = w
    rows = c.sum(axis=1)
    c_max = float(rows.max())
    T = cfg.move * c / c_max
    T[np.diag_indices(n)] = 1.0 - cfg.move * rows / c_max
    check_support(T, world)
    d_max = int(adjacency(world).sum(axis=1).max())
    spec = TransitionSpec(T=T, pi=np.full(n, 1.0 / n), p_stay=float(1.0 - cfg.move), d_max=d_max)
    spec.validate()
    f, _ = warp_profile(tuple(world.dims), cfg.a)
    meta = {"kind": "metric_conductance", "a": float(cfg.a), "move": float(cfg.move),
            "f_y": [float(v) for v in f], "l_h": [float(v) for v in l_h], "C_max": c_max,
            "n_edges_h": int(same_y.sum()), "n_edges_v": int(same_x.sum())}
    return spec, meta
