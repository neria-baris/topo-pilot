"""X5 G1 training-study lineage (x5g1-train-v3 §3): masters, streams, codes 9/10/11, paired
pool draws (named = perm[canon], latents dropped) and disjointness counts."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, StageFailure

from .x4b2 import process_code
from .x5g1_lineage import sample_named

NAMESPACE = "x5g1-train-v1"
PROTOCOL = "x5g1-train-v3"
MASTERS = (310001, 310002, 310003)
ARMS = ("a0", "a020")
CODES = {"train": 9, "dev": 10, "test": 11}
SIZES = {"train": 131_072, "dev": 4096, "test": 4096}
TEST_MASTER = "shared"


def _bad(check: str, detail: str) -> StageFailure:
    return StageFailure(ErrorCode.INVALID_CONFIG, "experiment.X5G1T", check, detail)


def stream(split: str) -> tuple[str, ...]:
    if split not in CODES:
        raise _bad("split", f"unknown split {split!r}")
    return (NAMESPACE, split, "cylinder", "overlap", "1.25")


def _seed_master(split: str, master) -> int:
    stream(split)
    if split == "test":
        if master != TEST_MASTER:
            raise _bad("master", f"test pools use master {TEST_MASTER!r}, got {master!r}")
        return 0
    if isinstance(master, bool) or not isinstance(master, (int, np.integer)):
        raise _bad("master", f"train/dev master must be an int, got {master!r}")
    return int(master)


def paired_generators(split: str, master) -> tuple[np.random.Generator, np.random.Generator]:
    """Two separately created generators with the same frozen seed (common randomness)."""
    seed = _seed_master(split, master)
    return SeedTree(seed).generator(*stream(split)), SeedTree(seed).generator(*stream(split))


def sequence_ids(split: str, arm: str, master, n: int) -> NDArray[np.int64]:
    """``(process_code(..., f"{NAMESPACE}:{split}:{arm}:{master}") << 32) | (code << 28) | i``."""
    stream(split)
    if arm not in ARMS:
        raise _bad("arm", f"unknown arm {arm!r}")
    if not 1 <= int(n) <= 2**28:
        raise _bad("n", f"n={n} outside 1..2**28")
    code = process_code("cylinder", "overlap", "1.25", f"{NAMESPACE}:{split}:{arm}:{master}")
    return ((np.int64(code) << 32) | (np.int64(CODES[split]) << 28)) + np.arange(n,
                                                                                 dtype=np.int64)


def draw_pair(kernels: dict, E: NDArray, perm: NDArray, pi: NDArray, split: str, master,
              n: int) -> dict[str, NDArray]:
    """``{arm: named tokens [n, 33]}``; one sampler call per arm with the paired generators."""
    rngs = dict(zip(ARMS, paired_generators(split, master)))
    return {arm: sample_named(kernels[arm], E, perm, pi, rngs[arm], n) for arm in ARMS}


def pool_observation(split: str, named: NDArray, ids: NDArray, V: int) -> ObservationSet:
    obs = ObservationSet(split=split, V=int(V), sequence_id=np.asarray(ids, dtype=np.int64),
                         tokens=np.asarray(named))
    obs.validate()
    return obs


def pool_config(split: str, arm: str, master) -> dict:
    return {"role": f"x5g1t-{split}", "protocol": PROTOCOL, "arm": arm, "master": master,
            "stream": "/".join(stream(split)), "namespace_code": CODES[split]}


def study_pool_config(split: str, arm: str, master, execution_protocol: str) -> dict:
    """Metadata of a NEW study pool (API v4.1 §A): ``lineage_protocol`` names the frozen
    stream/namespace/seed/ID construction (``PROTOCOL``, API v3 §2); ``execution_protocol`` names
    the validated run contract. ``pool_config`` stays for historical records."""
    if arm not in ARMS:
        raise _bad("arm", f"unknown arm {arm!r}")
    return {"role": f"x5g1t-{split}", "lineage_protocol": PROTOCOL,
            "execution_protocol": execution_protocol, "arm": arm, "master": master,
            "stream": "/".join(stream(split)), "namespace_code": CODES[split]}


def collisions(new: dict[str, NDArray], stored: NDArray) -> dict[str, int]:
    """Per new id set: how many ids are in ``stored``; ``internal``: duplicates across all new."""
    st = np.asarray(stored, dtype=np.int64)
    out = {k: int(np.isin(np.asarray(v, dtype=np.int64), st).sum()) for k, v in new.items()}
    allnew = np.concatenate([np.asarray(v, dtype=np.int64) for v in new.values()]) \
        if new else np.zeros(0, dtype=np.int64)
    out["internal"] = int(allnew.size - np.unique(allnew).size)
    return out
