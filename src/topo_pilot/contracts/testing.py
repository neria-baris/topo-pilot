"""Tiny, deterministic test fixtures. Importable from tests only, never from ``src`` code.

The values here are hand-chosen and documented; nothing is computed by science modules.
"""

from __future__ import annotations

from typing import Literal

import numpy as np

from .backends import MemoryBackend
from .errors import ErrorCode, StageFailure
from .schemas import ObservationSet, WorldSpec
from .ids import SeedTree
from .store import ArtifactStore

# Betti numbers of the two core surfaces (contractible square; cylinder ~ circle), any field p.
_BETTI = {"square": (1, 0, 0), "cylinder": (1, 1, 0)}


def tiny_world_spec(family: Literal["square", "cylinder"] = "cylinder", n: int = 3) -> WorldSpec:
    """An ``n x n`` square or cylinder (axis 0 periodic) built by direct enumeration.

    Vertex ``(x, y)`` has id ``x * n + y``. Edges join 4-neighbours (wrapping in x for the
    cylinder); 2-cells are the unit squares with vertex tuple
    ``((x,y), (x,y+1), (x+1,y), (x+1,y+1))`` (local lexicographic order, x wrapped).
    ``dist`` is the flat metric (periodic minimum in x for the cylinder) and ``dist_graph`` the
    Manhattan graph distance (also periodic in x). Betti numbers are the known values
    (square (1,0,0), cylinder (1,1,0)) for p = 2 and 3, stored as both expected and computed.
    For n = 3: square V/E/F = 9/12/4 (χ = 1); cylinder 9/15/6 (χ = 0). Requires n ≥ 3.
    """
    if family not in _BETTI or n < 3:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "contracts.testing", "tiny_world_spec",
                           f"family={family!r}, n={n}")
    periodic = family == "cylinder"
    xs, ys = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    coords = np.stack([xs.ravel(), ys.ravel()], axis=1).astype(np.float64)

    def vid(x: int, y: int) -> int:
        return (x % n) * n + y

    x_steps = n if periodic else n - 1
    edges = {tuple(sorted((vid(x, y), vid(x + 1, y)))) for x in range(x_steps) for y in range(n)}
    edges |= {(vid(x, y), vid(x, y + 1)) for x in range(n) for y in range(n - 1)}
    squares = [(vid(x, y), vid(x, y + 1), vid(x + 1, y), vid(x + 1, y + 1))
               for x in range(x_steps) for y in range(n - 1)]
    edge_arr = np.array(sorted(edges), dtype=np.int32)
    dx = np.abs(coords[:, None, 0] - coords[None, :, 0])
    if periodic:
        dx = np.minimum(dx, n - dx)
    dy = np.abs(coords[:, None, 1] - coords[None, :, 1])
    betti = {2: _BETTI[family], 3: _BETTI[family]}
    return WorldSpec(
        family=family, dims=(n, n), coords=coords,
        cells={0: np.arange(n * n, dtype=np.int32)[:, None], 1: edge_arr,
               2: np.array(squares, dtype=np.int32)},
        edges=edge_arr, dist=np.sqrt(dx**2 + dy**2), dist_graph=dx + dy,
        betti_expected=betti, betti_computed=dict(betti),
        identifications=("x periodic",) if periodic else (), metric="flat")


def tiny_hmm() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A hand-chosen 4-state, 3-symbol HMM: ``(T [4,4], E [4,3], pi [4])``.

    T is a lazy walk on the 4-cycle 0-1-2-3-0: stay 0.5, each ring neighbour 0.25
    (symmetric, doubly stochastic, so pi is uniform 0.25). Emission rows:
    state 0 -> (0.7, 0.2, 0.1); 1 -> (0.1, 0.7, 0.2); 2 -> (0.2, 0.1, 0.7); 3 -> (0.4, 0.4, 0.2).
    """
    T = np.array([[0.50, 0.25, 0.00, 0.25],
                  [0.25, 0.50, 0.25, 0.00],
                  [0.00, 0.25, 0.50, 0.25],
                  [0.25, 0.00, 0.25, 0.50]])
    E = np.array([[0.7, 0.2, 0.1],
                  [0.1, 0.7, 0.2],
                  [0.2, 0.1, 0.7],
                  [0.4, 0.4, 0.2]])
    pi = np.full(4, 0.25)
    return T, E, pi


def tiny_observations(R: int = 8, seed: int = 0) -> ObservationSet:
    """``R`` test-split trajectories of 33 symbols sampled from :func:`tiny_hmm`.

    Sampling: ``z_1 ~ pi``; emit ``w_t ~ E[z_t]``; then ``z_{t+1} ~ T[z_t]``. Randomness comes
    from ``SeedTree(seed).generator("tiny_observations")``. ``sequence_id = 0..R-1``, V = 3.
    """
    T, E, pi = tiny_hmm()
    rng = SeedTree(seed).generator("tiny_observations")
    tokens = np.zeros((R, 33), dtype=np.uint8)
    for r in range(R):
        z = rng.choice(4, p=pi)
        for t in range(33):
            tokens[r, t] = rng.choice(3, p=E[z])
            z = rng.choice(4, p=T[z])
    return ObservationSet(split="test", V=3, sequence_id=np.arange(R, dtype=np.int64),
                          tokens=tokens)


def memory_store() -> ArtifactStore:
    """A fresh :class:`ArtifactStore` over an in-memory backend with the default access policy."""
    return ArtifactStore(MemoryBackend())
