"""Null clouds and synthetic shapes with known topology (all randomness injected)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "topology.SyntheticShapes"


def _require_rng(rng: np.random.Generator | None, component: str) -> np.random.Generator:
    if rng is None:
        raise StageFailure(ErrorCode.INVALID_CONFIG, component, "rng",
                           "an np.random.Generator must be injected")
    return rng


class NullClouds:
    """Gaussian null clouds for the noise floor (RESEARCH_SUMMARY 7.3). Shapes: ``[M, F]``."""

    @staticmethod
    def isotropic(M: int, F: int, rng: np.random.Generator) -> NDArray[np.float64]:
        """``M`` draws of ``N(0, I_F)``."""
        return _require_rng(rng, "topology.NullClouds").standard_normal((M, F))

    @staticmethod
    def covariance_matched(X: NDArray[np.float64], rng: np.random.Generator) -> NDArray[np.float64]:
        """``M`` draws of ``N(mean(X), cov(X))`` (sample covariance, ddof=1), same shape as ``X``.

        Sampled through the SVD ``Xc = U S V^T``: ``x = mu + z (S / sqrt(M-1)) V^T`` with
        ``z ~ N(0, I_r)``, so no ``F x F`` matrix is formed (``F > M`` is fine).
        """
        rng = _require_rng(rng, "topology.NullClouds")
        X = np.asarray(X, dtype=np.float64)
        M = X.shape[0]
        mu = X.mean(axis=0)
        _, s, vt = np.linalg.svd(X - mu, full_matrices=False)
        z = rng.standard_normal((M, len(s)))
        return mu + (z * (s / np.sqrt(max(M - 1, 1)))) @ vt


def _embed(core: NDArray[np.float64], ambient: int, noise: float,
           rng: np.random.Generator) -> NDArray[np.float64]:
    """Place ``core [M, k]`` in the first ``k`` axes of R^ambient and add N(0, noise^2) per axis."""
    if ambient < core.shape[1]:
        raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "ambient",
                           f"ambient={ambient} < intrinsic embedding dim {core.shape[1]}")
    X = np.zeros((core.shape[0], ambient))
    X[:, : core.shape[1]] = core
    return X + noise * rng.standard_normal(X.shape)


class SyntheticShapes:
    """Samples of shapes with known Betti numbers, embedded in ``R^ambient``.

    Math
    ----
    Clean points lie on the unit circle / unit disk / Clifford torus ``(cos a, sin a, cos b,
    sin b)/sqrt 2`` / unit sphere ``S^dim`` in the first coordinates; i.i.d. Gaussian noise of
    standard deviation ``noise`` is added **per ambient coordinate**.

    Shapes
    ------
    Each method returns ``[M, ambient] float64``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if ``rng`` is None or ``ambient`` is too small.
    """

    @staticmethod
    def circle(M: int, ambient: int = 128, noise: float = 0.05,
               rng: np.random.Generator | None = None) -> NDArray[np.float64]:
        """Uniform angles on the unit circle (beta_1 = 1)."""
        rng = _require_rng(rng, _COMPONENT)
        a = rng.uniform(0.0, 2 * np.pi, M)
        return _embed(np.column_stack([np.cos(a), np.sin(a)]), ambient, noise, rng)

    @staticmethod
    def disk(M: int, ambient: int = 128, noise: float = 0.05,
             rng: np.random.Generator | None = None) -> NDArray[np.float64]:
        """Uniform points of the unit disk (contractible)."""
        rng = _require_rng(rng, _COMPONENT)
        a = rng.uniform(0.0, 2 * np.pi, M)
        r = np.sqrt(rng.uniform(0.0, 1.0, M))
        return _embed(np.column_stack([r * np.cos(a), r * np.sin(a)]), ambient, noise, rng)

    @staticmethod
    def flat_torus(M: int, ambient: int = 128, noise: float = 0.05,
                   rng: np.random.Generator | None = None) -> NDArray[np.float64]:
        """Uniform angles on the Clifford torus in R^4 (beta_1 = 2)."""
        rng = _require_rng(rng, _COMPONENT)
        a, b = rng.uniform(0.0, 2 * np.pi, (2, M))
        core = np.column_stack([np.cos(a), np.sin(a), np.cos(b), np.sin(b)]) / np.sqrt(2.0)
        return _embed(core, ambient, noise, rng)

    @staticmethod
    def sphere(M: int, dim: int = 2, ambient: int = 128, noise: float = 0.05,
               rng: np.random.Generator | None = None) -> NDArray[np.float64]:
        """Uniform points of the unit sphere ``S^dim`` in R^(dim+1)."""
        rng = _require_rng(rng, _COMPONENT)
        g = rng.standard_normal((M, dim + 1))
        return _embed(g / np.linalg.norm(g, axis=1, keepdims=True), ambient, noise, rng)
