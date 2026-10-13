"""X5 G1 calibration lineage (x5g1-feas-v2 §4): paired generators, named tokens, namespace 8.

Canonical draws use ``E[:, perm]`` and are remapped to the stored E vocabulary as
``named = perm[canon]`` (D-019) before any persistence or oracle use. Latent states are dropped.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import (
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
)
from topo_pilot.dataset import HMMSampler

from .x4b2 import process_code

STREAM = ("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")
N_POOL = 16_384
NAMESPACE_CODE = 8
ARMS = ("a0", "a020")


def paired_generators() -> tuple[np.random.Generator, np.random.Generator]:
    """Two separately created generators with the identical frozen seed (common randomness)."""
    return SeedTree(0).generator(*STREAM), SeedTree(0).generator(*STREAM)


def sample_named(T: NDArray, E: NDArray, perm: NDArray, pi: NDArray, rng: np.random.Generator,
                 n: int = N_POOL) -> NDArray:
    """One sampler call on ``E[:, perm]``; returns ``perm[canon]`` ``[n, 33]``; states dropped.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if a drawn symbol or state is out of range.
    """
    p = np.asarray(perm, dtype=np.int64)
    canon, states = HMMSampler(T, np.asarray(E)[:, p], pi, SequenceLayout()).sample(n, rng)
    N, V = np.asarray(E).shape
    if int(canon.max()) >= V or int(states.min()) < 0 or int(states.max()) >= N:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "experiment.X5G1", "range", "draw range")
    del states
    return p[canon.astype(np.int64)].astype(canon.dtype)


def sequence_ids(arm: str, n: int = N_POOL) -> NDArray[np.int64]:
    """``(process_code(..., "x5g1-v1:calibration:" + arm) << 32) | (8 << 28) | index``."""
    if arm not in ARMS:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.X5G1", "arm", f"arm {arm!r}")
    code = process_code("cylinder", "overlap", "1.25", f"x5g1-v1:calibration:{arm}")
    return ((code << 32) | (NAMESPACE_CODE << 28)) + np.arange(n, dtype=np.int64)


def calibration_obs(named: NDArray, seq: NDArray) -> ObservationSet:
    """Public calibration pool: ``split="dev"`` (schema literal); the role lives in the config."""
    obs = ObservationSet(split="dev", V=36, sequence_id=np.asarray(seq, dtype=np.int64),
                         tokens=np.asarray(named))
    obs.validate()
    return obs
