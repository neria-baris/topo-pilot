"""Quotient-lattice world builder: product lattice + per-axis gluings (square, cylinder)."""

from __future__ import annotations

import itertools
from typing import ClassVar, Sequence

import numpy as np

from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec

from .complex import CubicalComplex, check_boundary_closed
from .config import WorldConfig
from .identification import Identification
from .metrics import METRICS, GraphGeodesicMetric
from .registry import WorldBuilder, register_world

_COMPONENT = "world.QuotientLatticeBuilder"
_AXIS_NAMES = "xyz"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def _check_identifications(idents: Sequence[Identification], dims: tuple[int, ...]) -> None:
    seen = set()
    for ident in idents:
        if not 0 <= ident.axis < len(dims) or ident.axis in seen:
            raise _fail(ErrorCode.INVALID_GLUE, "axis", f"bad or repeated axis {ident.axis}")
        seen.add(ident.axis)
        if ident.kind not in ("none", "periodic", "flipped"):
            raise _fail(ErrorCode.INVALID_GLUE, "kind", f"unknown gluing kind {ident.kind!r}")
        if ident.kind == "none":
            continue
        if dims[ident.axis] < 3:
            raise _fail(ErrorCode.INVALID_GLUE, "glued_size", "a glued axis needs length >= 3")
        if ident.kind == "flipped":
            f = ident.flip_axis
            if f is None or not 0 <= f < len(dims) or f == ident.axis:
                raise _fail(ErrorCode.INVALID_GLUE, "flip_axis", "flipped needs another axis")
        elif ident.flip_axis is not None:
            raise _fail(ErrorCode.INVALID_GLUE, "flip_axis", "flip_axis only with 'flipped'")


def _wrap(corner: list[int], idents: Sequence[Identification], dims: tuple[int, ...]) -> list[int]:
    """Map a lattice corner (coordinates may equal ``n_a``) to its representative vertex.

    Crossing a glued axis ``a`` subtracts ``n_a`` and, if flipped, reflects the flip axis
    ``f -> n_f - 1 - f``; glued axes are finally reduced mod ``n``.
    """
    c = list(corner)
    glued = [i for i in idents if i.kind != "none"]
    for ident in glued:
        if c[ident.axis] >= dims[ident.axis]:
            c[ident.axis] -= dims[ident.axis]
            if ident.kind == "flipped":
                c[ident.flip_axis] = dims[ident.flip_axis] - 1 - c[ident.flip_axis]
    for ident in glued:
        c[ident.axis] %= dims[ident.axis]
    if any(not 0 <= v < n for v, n in zip(c, dims)):
        raise _fail(ErrorCode.INVALID_GLUE, "corner", "cube corner leaves the lattice")
    return c


def lattice_cells(dims: tuple[int, ...], idents: Sequence[Identification]) -> dict[int, np.ndarray]:
    """All k-cubes of the glued lattice, ``k = 0..len(dims)``, as local-lexicographic tuples.

    Shapes
    ------
    ``{k: int32 [n_k, 2**k]}``; ``cells[1]`` rows are canonical ``(lo, hi)``, sorted.

    Raises
    ------
    StageFailure
        ``INVALID_GLUE`` if a cube repeats a vertex or is generated twice.
    """
    glued = {i.axis for i in idents if i.kind != "none"}
    strides = np.cumprod((1,) + tuple(reversed(dims[1:])))[::-1]
    n_vertices = int(np.prod(dims))
    cells: dict[int, np.ndarray] = {0: np.arange(n_vertices, dtype=np.int32)[:, None]}
    for k in range(1, len(dims) + 1):
        rows, keys = [], set()
        for axes in itertools.combinations(range(len(dims)), k):
            ranges = [range(n - 1 if (a in axes and a not in glued) else n)
                      for a, n in enumerate(dims)]
            for base in itertools.product(*ranges):
                tup = []
                for j in range(2**k):
                    c = list(base)
                    for t, a in enumerate(axes):
                        c[a] += (j >> (k - 1 - t)) & 1
                    tup.append(int(np.dot(_wrap(c, idents, dims), strides)))
                key = tuple(sorted(tup))
                if len(set(key)) != len(key) or key in keys:
                    raise _fail(ErrorCode.INVALID_GLUE, f"cells_{k}", "repeated vertex or cube")
                keys.add(key)
                rows.append(key if k == 1 else tuple(tup))
        arr = np.array(rows, dtype=np.int32)
        cells[k] = arr[np.lexsort(arr.T[::-1])] if k == 1 else arr
    return cells


def describe_identifications(idents: Sequence[Identification]) -> tuple[str, ...]:
    """Human-readable gluing strings, e.g. ``'x periodic'``, ``'x flipped(y)'``."""
    out = []
    for i in idents:
        if i.kind == "periodic":
            out.append(f"{_AXIS_NAMES[i.axis]} periodic")
        elif i.kind == "flipped":
            out.append(f"{_AXIS_NAMES[i.axis]} flipped({_AXIS_NAMES[i.flip_axis]})")
    return tuple(out)


class QuotientLatticeBuilder(WorldBuilder):
    """Generic: product lattice + per-axis Identification; builds vertices and all k-cubes
    (k <= len(dims)), including cubes crossing seams, with consistent vertex order.

    Subclasses set ``family``, ``expected_betti`` and the class attribute ``identifications``
    (a tuple of :class:`Identification`; axes not listed are unglued).

    Math
    ----
    Vertex ``x`` has id ``ravel(x, dims)`` (C order, ``x * dims[1] + y`` for D = 2); the k-cube
    with base ``b`` and direction axes ``S`` has corners ``b + sum_t e_t a_t`` wrapped through the
    gluings and listed in local lexicographic order.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (bad dims/metric), ``INVALID_GLUE``, ``BETTI_MISMATCH``,
        ``NON_METRIC`` (graph disconnected).
    """

    identifications: ClassVar[tuple[Identification, ...]] = ()
    expected_betti: ClassVar[dict[int, tuple[int, ...]]] = {}

    def build(self, cfg: WorldConfig) -> WorldSpec:
        dims = tuple(int(d) for d in cfg.dims)
        if not 1 <= len(dims) <= 3 or min(dims) < 2:
            raise _fail(ErrorCode.INVALID_CONFIG, "dims", f"dims {dims}: 1-3 axes, each >= 2")
        if cfg.metric not in METRICS:
            raise _fail(ErrorCode.INVALID_CONFIG, "metric", f"unknown metric {cfg.metric!r}")
        idents = tuple(self.identifications)
        _check_identifications(idents, dims)
        cells = lattice_cells(dims, idents)
        cx = CubicalComplex(int(np.prod(dims)), cells)
        check_boundary_closed(cx)
        betti = {int(p): cx.betti(int(p)) for p in self.expected_betti}
        expected = {int(p): tuple(v) for p, v in self.expected_betti.items()}
        if betti != expected:
            raise _fail(ErrorCode.BETTI_MISMATCH, "betti",
                        f"computed {betti} != expected {expected}")
        coords = np.stack(np.meshgrid(*[np.arange(n) for n in dims], indexing="ij"),
                          axis=-1).reshape(-1, len(dims)).astype(np.float64)
        dist_graph = GraphGeodesicMetric().pairwise(coords, cx, idents, dims)
        dist = METRICS[cfg.metric]().pairwise(coords, cx, idents, dims)
        return WorldSpec(
            family=self.family, dims=dims, coords=coords, cells=cells, edges=cx.one_skeleton(),
            dist=dist, dist_graph=dist_graph, betti_expected=expected, betti_computed=betti,
            identifications=describe_identifications(idents), metric=cfg.metric)


@register_world
class SquareBuilder(QuotientLatticeBuilder):
    """Plain grid, no identifications: contractible, beta = (1, 0, 0), chi = 1."""

    family: ClassVar[str] = "square"
    expected_betti: ClassVar[dict[int, tuple[int, ...]]] = {2: (1, 0, 0), 3: (1, 0, 0)}


@register_world
class CylinderBuilder(QuotientLatticeBuilder):
    """Axis 0 periodic: beta = (1, 1, 0), chi = 0."""

    family: ClassVar[str] = "cylinder"
    expected_betti: ClassVar[dict[int, tuple[int, ...]]] = {2: (1, 1, 0), 3: (1, 1, 0)}
    identifications: ClassVar[tuple[Identification, ...]] = (Identification(0, "periodic"),)
