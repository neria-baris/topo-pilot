"""World and process artifacts: WorldSpec, TransitionSpec, EmissionSpec (DATA_SCHEMAS §2)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar

import numpy as np

from . import _checks as ck
from .base import Artifact, array_field, optional_array_field
from .errors import ErrorCode

EMISSION_MODES = ("overlap", "axis_permuted", "full_permuted", "identical", "unique")
EMISSION_DIAGNOSTIC_KEYS = ("H_W_given_Z", "H_W", "p_w", "coverage_radius",
                            "row_entropy_quantiles", "factorizes")
MIN_SYMBOL_PROB = 1e-4


@dataclass(frozen=True, eq=False)
class WorldSpec(Artifact):
    """A latent world: states, the cubical complex defining the surface, metrics, homology.

    Fields
    ------
    family : registry key (``"square"``, ``"cylinder"``, ...).
    dims : lattice size, e.g. ``(12, 12)``; vertex ``(x, y)`` has id ``x * dims[1] + y``.
    coords : ``[N, D] float64`` chart coordinates (generator and analysis only).
    cells : ``{k: int32[n_k, 2**k]}`` k-cubes as vertex tuples in local lexicographic order;
        ``cells[0]`` is ``[[0], [1], ..., [N-1]]``.
    edges : ``int32[E, 2]`` the 1-skeleton, canonical ``(lo, hi)``, equal to ``cells[1]`` as sets.
    dist : ``[N, N] float64`` primary metric d_M. ``dist_graph`` : graph geodesic distance.
    betti_expected, betti_computed : ``{p: (b_0, b_1, ...)}`` over GF(p).
    identifications : human-readable gluing description. metric : name of ``dist``.
    disjoint : True only for declared disjoint-union families (exempt from connectivity).

    Invariants checked here: shapes; cells use valid ids, never repeat a vertex within a cell,
    and are not listed twice (``INVALID_GLUE``); edges match ``cells[1]`` (``INVALID_GLUE``);
    ``dist`` and ``dist_graph`` are metrics (``NON_METRIC``); computed β equals expected β
    (``BETTI_MISMATCH``); the 1-skeleton is connected unless ``disjoint`` (``INVALID_GLUE``).
    ``∂∂ = 0`` needs the cubical sign convention and is enforced by ``world`` when building.
    """

    ARTIFACT_TYPE: ClassVar[str] = "WorldSpec"
    ARRAY_DICT_FIELDS: ClassVar[tuple[str, ...]] = ("cells",)

    family: str
    dims: tuple[int, ...]
    coords: np.ndarray = array_field()
    cells: dict[int, np.ndarray] = array_field()
    edges: np.ndarray = array_field()
    dist: np.ndarray = array_field()
    dist_graph: np.ndarray = array_field()
    betti_expected: dict[int, tuple[int, ...]] = field(default_factory=dict)
    betti_computed: dict[int, tuple[int, ...]] = field(default_factory=dict)
    identifications: tuple[str, ...] = ()
    metric: str = "flat"
    disjoint: bool = False

    @property
    def n_states(self) -> int:
        """Number of states N."""
        return int(self.coords.shape[0])

    def validate(self) -> None:
        name = "WorldSpec"
        coords = ck.require_array(name, "coords", self.coords, 2, "f")
        ck.require_finite(name, "coords", coords)
        n = coords.shape[0]
        self._validate_cells(n)
        for key, D in (("dist", self.dist), ("dist_graph", self.dist_graph)):
            ck.require_array(name, key, D, 2, "f", ErrorCode.NON_METRIC)
            if D.shape != (n, n):
                raise self._fail(ErrorCode.NON_METRIC, f"{key}_shape", f"{key} is not [{n}, {n}]")
            ck.require_metric_matrix(name, key, D, positive=True)
        if not self.betti_expected or self.betti_computed != self.betti_expected:
            raise self._fail(ErrorCode.BETTI_MISMATCH, "betti",
                             f"computed {self.betti_computed} != expected {self.betti_expected}")
        if not self.disjoint and _n_components(n, self.edges) != 1:
            raise self._fail(ErrorCode.INVALID_GLUE, "connected", "the 1-skeleton is disconnected")

    def _validate_cells(self, n: int) -> None:
        keys = sorted(self.cells)
        if keys != list(range(len(keys))) or not keys:
            raise self._fail(ErrorCode.INVALID_GLUE, "cell_dims", f"cell dims {keys} not 0..k")
        if not np.array_equal(np.asarray(self.cells[0]).ravel(), np.arange(n)):
            raise self._fail(ErrorCode.INVALID_GLUE, "vertices", "cells[0] must be 0..N-1")
        for k in keys:
            c = ck.require_array("WorldSpec", f"cells_{k}", np.asarray(self.cells[k]), 2, "iu",
                                 ErrorCode.INVALID_GLUE)
            if c.shape[1] != 2**k or (c.size and (c.min() < 0 or c.max() >= n)):
                raise self._fail(ErrorCode.INVALID_GLUE, f"cells_{k}", "bad width or vertex id")
            srt = np.sort(c, axis=1)
            if k > 0 and np.any(srt[:, 1:] == srt[:, :-1]):
                raise self._fail(ErrorCode.INVALID_GLUE, f"cells_{k}_repeat",
                                 f"a {k}-cell repeats a vertex")
            if np.unique(srt, axis=0).shape[0] != c.shape[0]:
                raise self._fail(ErrorCode.INVALID_GLUE, f"cells_{k}_duplicate",
                                 f"a {k}-cell is listed twice")
        edges = ck.require_array("WorldSpec", "edges", self.edges, 2, "iu", ErrorCode.INVALID_GLUE)
        if edges.shape[1] != 2 or np.any(edges[:, 0] >= edges[:, 1]):
            raise self._fail(ErrorCode.INVALID_GLUE, "edges_canonical", "edges must be (lo, hi)")
        if 1 in self.cells:
            as_set = {tuple(e) for e in np.sort(self.cells[1], axis=1).tolist()}
            if as_set != {tuple(e) for e in edges.tolist()} or len(as_set) != edges.shape[0]:
                raise self._fail(ErrorCode.INVALID_GLUE, "edges_match_cells",
                                 "edges differ from cells[1]")


def _n_components(n: int, edges: np.ndarray) -> int:
    parent = list(range(n))

    def root(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b in np.asarray(edges).tolist():
        parent[root(a)] = root(b)
    return len({root(i) for i in range(n)})


@dataclass(frozen=True, eq=False)
class TransitionSpec(Artifact):
    """Transition kernel ``T[i, j] = P(z_{t+1} = j | z_t = i)`` (``[N, N] float64``) and ``pi [N]``.

    Invariants: entries ≥ 0 and rows sum to 1 ± 1e-12 (``NONSTOCHASTIC``); ``T`` symmetric
    (``NONSTOCHASTIC``, detail ``asymmetric``); ``pi`` a distribution with ``|pi T - pi|∞ ≤ 1e-12``
    (``STATIONARITY_FAILURE``). Support on edges and self-loops needs the world and is checked
    by ``process`` at build time.
    """

    ARTIFACT_TYPE: ClassVar[str] = "TransitionSpec"

    T: np.ndarray = array_field()
    pi: np.ndarray = array_field()
    p_stay: float = 0.2
    d_max: int = 4
    event_order: str = "emit_then_transition"

    def validate(self) -> None:
        name = "TransitionSpec"
        T = ck.require_array(name, "T", self.T, 2, "f", ErrorCode.NONSTOCHASTIC)
        pi = ck.require_array(name, "pi", self.pi, 1, "f", ErrorCode.NONSTOCHASTIC)
        n = T.shape[0]
        if T.shape != (n, n) or pi.shape != (n,):
            raise self._fail(ErrorCode.NONSTOCHASTIC, "shape", f"T {T.shape}, pi {pi.shape}")
        ck.require_distribution_rows(name, "T", T, 1e-12, ErrorCode.NONSTOCHASTIC)
        if np.max(np.abs(T - T.T)) > 1e-12:
            raise self._fail(ErrorCode.NONSTOCHASTIC, "symmetric", "asymmetric")
        ck.require_distribution_rows(name, "pi", pi[None, :], 1e-12, ErrorCode.STATIONARITY_FAILURE)
        if np.max(np.abs(pi @ T - pi)) > 1e-12:
            raise self._fail(ErrorCode.STATIONARITY_FAILURE, "stationary", "pi T != pi")
        if self.event_order != "emit_then_transition":
            raise self._fail(ErrorCode.INVALID_CONFIG, "event_order", self.event_order)


@dataclass(frozen=True, eq=False)
class EmissionSpec(Artifact):
    """Emission matrix ``E[z, w] = P(w_t = w | z_t = z)`` (``[N, V] float64``).

    ``diagnostics`` holds ``H_W_given_Z, H_W`` (nats), ``p_w`` (length-V list, = pi E),
    ``coverage_radius, row_entropy_quantiles, factorizes``.

    Invariants: rows ≥ 0 summing to 1 ± 1e-12 (``NONSTOCHASTIC``); every ``p_w ≥ 1e-4`` and no
    all-zero column (``INVALID_SIGMA``, detail ``dead_symbol``); ``overlap`` needs σ > 0
    (``INVALID_SIGMA``); ``identical`` has equal rows; ``unique`` is a permutation matrix with
    ``V = N``; permutations are valid (``INVALID_CONFIG``). The same-row-multiset property of
    permuted modes needs the source spec and is checked by ``process``.
    """

    ARTIFACT_TYPE: ClassVar[str] = "EmissionSpec"

    E: np.ndarray = array_field()
    symbol_perm: np.ndarray = array_field()
    mode: str = "overlap"
    sigma: float | None = None
    centers: np.ndarray | None = optional_array_field()
    center_strategy: str | None = None
    state_perm: np.ndarray | None = optional_array_field()
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        name = "EmissionSpec"
        E = ck.require_array(name, "E", self.E, 2, "f", ErrorCode.NONSTOCHASTIC)
        n, v = E.shape
        ck.require_distribution_rows(name, "E", E, 1e-12, ErrorCode.NONSTOCHASTIC)
        if self.mode not in EMISSION_MODES:
            raise self._fail(ErrorCode.INVALID_CONFIG, "mode", f"unknown mode {self.mode!r}")
        if self.mode == "overlap" and (self.sigma is None or not self.sigma > 0):
            raise self._fail(ErrorCode.INVALID_SIGMA, "sigma", f"sigma={self.sigma} must be > 0")
        ck.require_permutation(name, "symbol_perm", self.symbol_perm, v)
        if self.state_perm is not None:
            ck.require_permutation(name, "state_perm", self.state_perm, n)
        if self.centers is not None and (self.centers.ndim != 2 or self.centers.shape[0] != v):
            raise self._fail(ErrorCode.INVALID_SIGMA, "centers", f"centers {self.centers.shape}")
        missing = [k for k in EMISSION_DIAGNOSTIC_KEYS if k not in self.diagnostics]
        if missing:
            raise self._fail(ErrorCode.INVALID_CONFIG, "diagnostics", f"missing {missing}")
        p_w = np.asarray(self.diagnostics["p_w"], dtype=np.float64)
        if p_w.shape != (v,) or np.any(p_w < MIN_SYMBOL_PROB) or np.any(E.max(axis=0) <= 0):
            raise self._fail(ErrorCode.INVALID_SIGMA, "p_w", "dead_symbol")
        if self.mode == "identical" and np.max(np.abs(E - E[:1])) > 1e-12:
            raise self._fail(ErrorCode.INVALID_CONFIG, "identical_rows", "rows differ")
        if self.mode == "unique" and (n != v or not np.array_equal(np.sort(E, axis=1)[:, -1], np.ones(n))
                                      or not np.array_equal(E.sum(axis=0), np.ones(v))):
            raise self._fail(ErrorCode.INVALID_CONFIG, "unique_permutation",
                             "E is not a permutation matrix")
