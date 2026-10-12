"""Emission builders: overlap (O), axis-permuted (P), full-permuted, identical (N), unique (U).

Conventions
-----------
* ``symbol_perm[j]`` is the public symbol id of center ``j``:
  ``E_public[:, symbol_perm[j]] = E_centers[:, j]``. ``EmissionSpec.centers[j]`` is center ``j``
  (generation order, e.g. ``j = a*k + b`` for the grid), so ``centers`` pairs with ``symbol_perm``.
* Replicate-scoped randomness (symbol names) uses ``rng_tree.generator("symbol_names", family,
  rng_tree.master)``. World-scoped randomness (center draws, P permutations) never depends on the
  replicate: it uses ``SeedTree(WORLD_SCOPE_MASTER)`` (D-012).
* Diagnostics use the uniform ``pi`` (T is doubly stochastic), so the builder never sees T.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Literal

import numpy as np
from numpy.typing import NDArray
from scipy.special import logsumexp

from topo_pilot.contracts import EmissionSpec, ErrorCode, SeedTree, WorldSpec

from ._diagnostics import check_row_multiset, check_symbols_alive, emission_diagnostics
from ._geometry import check_state_order, fail, point_distances
from .centers import CENTER_REGISTRY, check_centers_in_chart

WORLD_SCOPE_MASTER = 0
"""Master seed of the world-scoped ``SeedTree`` (permutations and centers, not replicate-scoped)."""


@dataclass(frozen=True)
class EmissionConfig:
    """Emission config. ``sigma`` is used by overlap and by the permuted modes (source sigma)."""

    mode: str
    V: int = 36
    sigma: float | None = 1.25
    center_strategy: str = "grid"
    source_mode: str | None = None
    metric: Literal["flat", "graph"] = "flat"


@dataclass(frozen=True)
class _Core:
    """Overlap matrix in center order plus the geometry that produced it."""

    E_centers: NDArray[np.float64]
    centers: NDArray[np.float64]
    dist: NDArray[np.float64]
    symbol_perm: NDArray[np.int64]


def draw_axis_permutation(world: WorldSpec) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """World-scoped ``(sigma_x, sigma_y)``: permutations of ``dims[0]`` and ``dims[1]``.

    Drawn from ``SeedTree(WORLD_SCOPE_MASTER).generator("axis_permutation", family)``: the same
    for every replicate of a world.
    """
    if len(world.dims) != 2:
        raise fail(ErrorCode.INVALID_CONFIG, "axis_permutation", "needs a 2-d chart")
    rng = SeedTree(WORLD_SCOPE_MASTER).generator("axis_permutation", world.family)
    return rng.permutation(world.dims[0]), rng.permutation(world.dims[1])


def axis_state_perm(sx: NDArray[np.int64], sy: NDArray[np.int64],
                    dims: tuple[int, ...]) -> NDArray[np.int64]:
    """State permutation of P: ``state_perm[x*n1 + y] = sx[x]*n1 + sy[y]``.

    Then ``E_P[z] = E_O[state_perm[z]]``, i.e. ``E_P[(x, y)] = E_O[(sx(x), sy(y))]``.
    """
    return (np.asarray(sx)[:, None] * dims[1] + np.asarray(sy)[None, :]).ravel().astype(np.int64)


def _check_config(world: WorldSpec, cfg: EmissionConfig) -> None:
    check_state_order(world)
    if cfg.V < 1:
        raise fail(ErrorCode.INVALID_CONFIG, "V", f"V={cfg.V}")


def _symbol_perm(world: WorldSpec, rng_tree: SeedTree, n_symbols: int) -> NDArray[np.int64]:
    rng = rng_tree.generator("symbol_names", world.family, rng_tree.master)
    return rng.permutation(n_symbols).astype(np.int64)


def _overlap_core(world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> _Core:
    """``E[z, j] = softmax_j(-d(z, c_j)^2 / 2 sigma^2)`` in float64 via log-sum-exp."""
    _check_config(world, cfg)
    sigma = cfg.sigma
    if sigma is None or not np.isfinite(sigma) or not sigma > 0:
        raise fail(ErrorCode.INVALID_SIGMA, "sigma", f"sigma={sigma} must be > 0")
    if cfg.center_strategy not in CENTER_REGISTRY:
        raise fail(ErrorCode.INVALID_CONFIG, "center_strategy", cfg.center_strategy)
    rng = SeedTree(WORLD_SCOPE_MASTER).generator("centers", world.family)
    centers = np.asarray(CENTER_REGISTRY[cfg.center_strategy]().centers(world, cfg.V, rng))
    check_centers_in_chart(world, centers)
    dist = point_distances(world, centers, cfg.metric)
    logits = -(dist**2) / (2.0 * sigma**2)
    E_centers = np.exp(logits - logsumexp(logits, axis=1, keepdims=True))
    return _Core(E_centers, centers, dist, _symbol_perm(world, rng_tree, cfg.V))


def _assemble(world: WorldSpec, mode: str, E_centers: NDArray[np.float64],
              symbol_perm: NDArray[np.int64], coverage: float, *, sigma: float | None = None,
              centers: NDArray[np.float64] | None = None, strategy: str | None = None,
              state_perm: NDArray[np.int64] | None = None) -> EmissionSpec:
    """Apply the symbol naming, compute diagnostics, check symbols, validate."""
    E = np.empty_like(E_centers)
    E[:, symbol_perm] = E_centers
    diag = emission_diagnostics(E, E_centers, tuple(world.dims), coverage)
    check_symbols_alive(np.asarray(diag["p_w"]))
    spec = EmissionSpec(E=E, symbol_perm=symbol_perm, mode=mode, sigma=sigma, centers=centers,
                        center_strategy=strategy, state_perm=state_perm, diagnostics=diag)
    spec.validate()
    return spec


class EmissionModel(ABC):
    """Variation point: one emission mode. Never receives a transition kernel."""

    mode: ClassVar[str]

    @abstractmethod
    def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec:
        """Build the ``EmissionSpec`` for ``world`` (shapes ``E [N, V]``, rows sum to 1)."""


class OverlapGaussian(EmissionModel):
    """O: ``E[z, j] = softmax_j(-d(z, c_j)^2 / 2 sigma^2)``, no truncation, symbols renamed.

    Shapes: ``E [N, V]``. Invariants: rows sum to 1 within 1e-12; ``factorizes`` True on the
    core worlds. Raises: ``INVALID_SIGMA`` (sigma <= 0, center outside chart, dead symbol),
    ``STATE_ORDER_MISMATCH``, ``INVALID_CONFIG``.
    """

    mode: ClassVar[str] = "overlap"

    def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec:
        core = _overlap_core(world, cfg, rng_tree)
        return _assemble(world, "overlap", core.E_centers, core.symbol_perm,
                         float(core.dist.min(axis=1).max()), sigma=cfg.sigma,
                         centers=core.centers, strategy=cfg.center_strategy)


class _PermutedModel(EmissionModel):
    """Shared logic of the state-permuted controls (composition over the overlap source)."""

    @abstractmethod
    def _state_perm(self, world: WorldSpec) -> NDArray[np.int64]:
        """World-scoped state permutation (``E_perm[z] = E_O[perm[z]]``)."""

    def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec:
        if cfg.source_mode not in (None, "overlap"):
            raise fail(ErrorCode.INVALID_CONFIG, "source_mode", f"{cfg.source_mode!r}")
        core = _overlap_core(world, cfg, rng_tree)
        state_perm = self._state_perm(world)
        E_centers = core.E_centers[state_perm]
        check_row_multiset(core.E_centers, E_centers)
        return _assemble(world, self.mode, E_centers, core.symbol_perm,
                         float(core.dist.min(axis=1).max()), sigma=cfg.sigma,
                         centers=core.centers, strategy=cfg.center_strategy,
                         state_perm=state_perm)


class AxisPermuted(_PermutedModel):
    """P: ``E_P[(x, y)] = E_O[(sx(x), sy(y))]`` with world-scoped ``sx, sy``.

    Preserves the row multiset, ``p_w``, ``H(W|Z)`` and the product structure; destroys
    spatial smoothness. Same symbol names as O of the same replicate.
    """

    mode: ClassVar[str] = "axis_permuted"

    def _state_perm(self, world: WorldSpec) -> NDArray[np.int64]:
        sx, sy = draw_axis_permutation(world)
        return axis_state_perm(sx, sy, tuple(world.dims))


class FullPermuted(_PermutedModel):
    """Extension: a world-scoped permutation of all N states (breaks product structure)."""

    mode: ClassVar[str] = "full_permuted"

    def _state_perm(self, world: WorldSpec) -> NDArray[np.int64]:
        rng = SeedTree(WORLD_SCOPE_MASTER).generator("full_permutation", world.family)
        return rng.permutation(world.n_states).astype(np.int64)


class Identical(EmissionModel):
    """N: ``E = 1/V`` (world-independent negative control)."""

    mode: ClassVar[str] = "identical"

    def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec:
        _check_config(world, cfg)
        E_centers = np.full((world.n_states, cfg.V), 1.0 / cfg.V)
        return _assemble(world, "identical", E_centers, _symbol_perm(world, rng_tree, cfg.V),
                         float(np.asarray(world.dist).max()))


class Unique(EmissionModel):
    """U: ``V = N`` and E is a permutation matrix (identity up to symbol names)."""

    mode: ClassVar[str] = "unique"

    def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec:
        _check_config(world, cfg)
        if cfg.V != world.n_states:
            raise fail(ErrorCode.INVALID_CONFIG, "V", f"unique needs V=N={world.n_states}")
        return _assemble(world, "unique", np.eye(cfg.V), _symbol_perm(world, rng_tree, cfg.V),
                         0.0)


EMISSION_REGISTRY: dict[str, type[EmissionModel]] = {
    cls.mode: cls for cls in (OverlapGaussian, AxisPermuted, FullPermuted, Identical, Unique)}
