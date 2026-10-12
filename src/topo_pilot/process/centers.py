"""Center strategies for the overlap emission: where the V symbol centers sit in the chart."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, WorldSpec

from ._geometry import fail


def check_centers_in_chart(world: WorldSpec, centers: NDArray[np.float64]) -> None:
    """Require every center to lie in the chart box ``[0, dims[k]-1]`` on each axis.

    Raises
    ------
    StageFailure
        ``INVALID_SIGMA`` (check ``center_outside_chart``) otherwise.
    """
    hi = np.asarray(world.dims, dtype=np.float64) - 1.0
    if centers.ndim != 2 or centers.shape[1] != len(hi):
        raise fail(ErrorCode.INVALID_SIGMA, "centers_shape", f"centers shape {centers.shape}")
    if np.any(centers < 0.0) or np.any(centers > hi):
        raise fail(ErrorCode.INVALID_SIGMA, "center_outside_chart",
                   f"a center lies outside [0, {hi.tolist()}]")


class CenterStrategy(ABC):
    """Variation point: chooses ``n_centers`` points in the chart.

    Shapes: ``centers(...) -> [V, D] float64`` with ``V = n_centers``, ``D = len(dims)``.
    """

    name: ClassVar[str]

    @abstractmethod
    def centers(self, world: WorldSpec, n_centers: int,
                rng: np.random.Generator) -> NDArray[np.float64]:
        """Return the ``[V, D]`` center coordinates."""


class GridCenters(CenterStrategy):
    """Core grid: ``c_ab = (0.5 + 2a, 0.5 + 2b)``, ``a, b in 0..sqrt(V)-1``, index ``j = a*k + b``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if V is not a perfect square or the chart is not 2-d;
        ``INVALID_SIGMA`` if a center falls outside ``[0, dims-1]`` (e.g. any n < 12 at V=36).
    """

    name: ClassVar[str] = "grid"

    def centers(self, world: WorldSpec, n_centers: int,
                rng: np.random.Generator) -> NDArray[np.float64]:
        k = math.isqrt(n_centers)
        if k * k != n_centers or len(world.dims) != 2:
            raise fail(ErrorCode.INVALID_CONFIG, "grid_centers",
                       f"V={n_centers} must be a perfect square on a 2-d chart")
        a, b = np.meshgrid(np.arange(k), np.arange(k), indexing="ij")
        out = np.stack([0.5 + 2.0 * a.ravel(), 0.5 + 2.0 * b.ravel()], axis=1)
        check_centers_in_chart(world, out)
        return out


class FPSCenters(CenterStrategy):
    """Farthest-point sampling on ``world.dist``; the centers are vertex coordinates.

    Math: ``c_1`` = vertex 0; ``c_{m+1} = argmax_v min_{i<=m} dist[v, c_i]`` (lowest id on ties).
    Deterministic (``rng`` unused).

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if ``n_centers`` is not in ``1..N``.
    """

    name: ClassVar[str] = "fps"

    def centers(self, world: WorldSpec, n_centers: int,
                rng: np.random.Generator) -> NDArray[np.float64]:
        n = world.n_states
        if not 1 <= n_centers <= n:
            raise fail(ErrorCode.INVALID_CONFIG, "fps_centers", f"n_centers={n_centers}, N={n}")
        chosen = [0]
        nearest = np.asarray(world.dist)[0].copy()
        while len(chosen) < n_centers:
            nxt = int(np.argmax(nearest))
            chosen.append(nxt)
            nearest = np.minimum(nearest, np.asarray(world.dist)[nxt])
        return np.asarray(world.coords, dtype=np.float64)[chosen].copy()


CENTER_REGISTRY: dict[str, type[CenterStrategy]] = {"grid": GridCenters, "fps": FPSCenters}
