"""Metrics on a world: flat quotient metric (deck-transformation lifts) and graph geodesic."""

from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import ClassVar, Sequence

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from scipy.spatial.distance import cdist

from topo_pilot.contracts import ErrorCode, StageFailure

from .complex import CubicalComplex
from .identification import Identification


class Metric(ABC):
    """Pairwise distance on the vertices of a world.

    Shapes
    ------
    ``coords: [N, D] float64``; ``pairwise`` returns ``[N, N] float64``.
    """

    name: ClassVar[str]

    @abstractmethod
    def pairwise(self, coords: np.ndarray, complex_: CubicalComplex,
                 identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray:
        """Return the symmetric ``[N, N]`` distance matrix."""


def _generators(identifications: Sequence[Identification],
                dims: tuple[int, ...]) -> list[tuple[np.ndarray, np.ndarray]]:
    """Deck generators as affine maps ``x -> a * x + b`` (``a`` a +-1 vector), one per glued axis.

    Periodic axis ``i``: ``b = n_i e_i``. Flipped axis ``i`` with flip axis ``f``:
    ``b = n_i e_i + (n_f - 1) e_f`` and ``a_f = -1`` (the glide reflection).
    """
    gens = []
    for ident in identifications:
        if ident.kind == "none":
            continue
        a, b = np.ones(len(dims)), np.zeros(len(dims))
        b[ident.axis] = dims[ident.axis]
        if ident.kind == "flipped":
            f = int(ident.flip_axis)
            a[f], b[f] = -1.0, dims[f] - 1.0
        gens.append((a, b))
    return gens


def _deck_elements(gens: list[tuple[np.ndarray, np.ndarray]],
                   n_dim: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """All products ``g_1^{m_1} ... g_r^{m_r}``, ``m_i in {-1, 0, 1}`` (3^r copies)."""
    elems = []
    for powers in itertools.product((-1, 0, 1), repeat=len(gens)):
        a, b = np.ones(n_dim), np.zeros(n_dim)
        for (ga, gb), m in zip(gens, powers):
            if m == 0:
                continue
            ha, hb = (ga, gb) if m == 1 else (ga, -ga * gb)
            a, b = a * ha, a * hb + b
        elems.append((a, b))
    return elems


class FlatQuotientMetric(Metric):
    """Minimum Euclidean distance over deck-transformation lifts.

    Math
    ----
    ``d(p, q) = min_{g in G'} || p - g(q) ||_2`` where ``G'`` is the set of products of the
    glued-axis generators with exponents in ``{-1, 0, 1}`` (the 3^r neighbouring copies of the
    fundamental domain); flipped axes apply the reflection. The result is symmetrised by
    ``min(d, d^T)`` (the truncated word set is not closed under inverses when gluings do not
    commute).

    Shapes
    ------
    ``coords: [N, D]`` -> ``[N, N]``.
    """

    name: ClassVar[str] = "flat"

    def pairwise(self, coords: np.ndarray, complex_: CubicalComplex,
                 identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray:
        coords = np.asarray(coords, dtype=np.float64)
        elems = _deck_elements(_generators(identifications, dims), coords.shape[1])
        dist = np.full((len(coords), len(coords)), np.inf)
        for a, b in elems:
            dist = np.minimum(dist, cdist(coords, coords * a + b))
        dist = np.minimum(dist, dist.T)
        np.fill_diagonal(dist, 0.0)
        return dist


class GraphGeodesicMetric(Metric):
    """Unit-length-edge shortest-path distance on the 1-skeleton.

    Math
    ----
    ``d(u, v) = `` minimal number of edges on a path from ``u`` to ``v``.

    Raises
    ------
    StageFailure
        ``NON_METRIC`` if the graph is disconnected and a distance is infinite.
    """

    name: ClassVar[str] = "graph"

    def pairwise(self, coords: np.ndarray, complex_: CubicalComplex,
                 identifications: Sequence[Identification], dims: tuple[int, ...]) -> np.ndarray:
        n = len(coords)
        edges = complex_.one_skeleton()
        adj = sp.coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])), shape=(n, n))
        dist = shortest_path(adj.tocsr(), method="D", directed=False, unweighted=True)
        if not np.all(np.isfinite(dist)):
            raise StageFailure(ErrorCode.NON_METRIC, "world.GraphGeodesicMetric", "finite",
                               "graph is disconnected (infinite distances)")
        return dist.astype(np.float64)


METRICS: dict[str, type[Metric]] = {FlatQuotientMetric.name: FlatQuotientMetric,
                                    GraphGeodesicMetric.name: GraphGeodesicMetric}


def check_flat_bounds(dist: np.ndarray, dist_graph: np.ndarray, n_axes: int,
                      tol: float = 1e-9) -> None:
    """Require ``dist <= dist_graph + tol`` and ``dist >= dist_graph / sqrt(D)``.

    Raises ``NON_METRIC`` (check ``flat_le_graph`` / ``flat_ge_graph_over_sqrtD``).
    """
    if np.any(dist > dist_graph + tol):
        raise StageFailure(ErrorCode.NON_METRIC, "world.metrics", "flat_le_graph",
                           "dist exceeds dist_graph")
    if np.any(dist < dist_graph / np.sqrt(n_axes) - tol):
        raise StageFailure(ErrorCode.NON_METRIC, "world.metrics", "flat_ge_graph_over_sqrtD",
                           "dist below dist_graph / sqrt(D)")
