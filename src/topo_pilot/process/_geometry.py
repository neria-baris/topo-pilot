"""Pure geometry helpers shared by the process builders (no I/O, no randomness)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec

COMPONENT = "process"


def fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    """Build a ``StageFailure`` attributed to the process module."""
    return StageFailure(code, COMPONENT, check, detail)


def is_x_periodic(world: WorldSpec) -> bool:
    """True if axis 0 is glued with period ``dims[0]``, read from the complex, not the name.

    Math
    ----
    With ``P = dims[0] >= 3``, axis 0 is periodic iff the 1-skeleton contains the straight wrap
    edge ``{(0, r), (P - 1, r)}`` for every index ``r`` of the other axes (vertex ids in
    row-major order). A flipped gluing (Möbius, Klein) has crossed wrap edges and is not
    periodic. For ``P <= 2`` the periodic and plain x distances coincide, so False is exact.

    Raises
    ------
    StageFailure
        ``INVALID_GLUE`` if the wrap edges are only partly present, or if the description
        declares ``'x periodic'`` but the complex has no wrap edges.
    """
    dims = tuple(int(d) for d in world.dims)
    period = dims[0]
    declared = any("x periodic" in s for s in world.identifications)
    if period < 3:
        return False
    rest = int(np.prod(dims[1:], dtype=np.int64))
    first = np.arange(rest, dtype=np.int64)
    wrap = {(int(a), int(b)) for a, b in zip(first, first + (period - 1) * rest)}
    present = {(int(min(a, b)), int(max(a, b))) for a, b in np.asarray(world.edges)}
    n_wrap = len(wrap & present)
    if 0 < n_wrap < len(wrap) or (declared and n_wrap == 0):
        raise fail(ErrorCode.INVALID_GLUE, "x_periodic",
                   f"{n_wrap}/{len(wrap)} wrap edges in axis 0; declared periodic: {declared}")
    return n_wrap == len(wrap)


def check_state_order(world: WorldSpec) -> None:
    """Require ``coords[x * dims[1] + y] == (x, y)`` (state order equals vertex-id order).

    Raises
    ------
    StageFailure
        ``STATE_ORDER_MISMATCH`` if the chart coordinates are not in vertex-id order.
    """
    coords = np.asarray(world.coords)
    if coords.shape[1] != len(world.dims):
        return
    expected = np.stack(np.unravel_index(np.arange(coords.shape[0]), world.dims), axis=1)
    if coords.shape[0] != expected.shape[0] or not np.array_equal(coords, expected.astype(float)):
        raise fail(ErrorCode.STATE_ORDER_MISMATCH, "state_order",
                   "world.coords are not in vertex-id order")


def point_distances(world: WorldSpec, points: NDArray[np.float64],
                    metric: str = "flat") -> NDArray[np.float64]:
    """Distances ``d(z, p)`` from every state to every point of ``points``.

    Math
    ----
    flat: ``sqrt(sum_k dk^2)``; graph: ``sum_k dk`` (Manhattan, the graph geodesic extended to
    non-vertex points), with ``d0 = min(|dx| mod P, P - |dx| mod P)``, ``P = dims[0]``, when
    axis 0 is periodic.

    Shapes
    ------
    points ``[V, D]`` -> result ``[N, V]`` float64.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` for an unknown metric.
    """
    if metric not in ("flat", "graph"):
        raise fail(ErrorCode.INVALID_CONFIG, "metric", f"unknown metric {metric!r}")
    diff = np.abs(np.asarray(world.coords)[:, None, :] - np.asarray(points)[None, :, :])
    if is_x_periodic(world):
        period = float(world.dims[0])
        wrapped = np.mod(diff[..., 0], period)
        diff[..., 0] = np.minimum(wrapped, period - wrapped)
    if metric == "graph":
        return diff.sum(axis=2)
    return np.sqrt((diff**2).sum(axis=2))
