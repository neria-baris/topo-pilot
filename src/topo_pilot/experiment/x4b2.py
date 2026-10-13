"""X4 Phase B2 lineage adapter (protocol x4b2-v1): fresh oracle-only pools from the same process.

Draws new canonical-vocabulary trajectories with the existing ``HMMSampler`` under frozen named
streams and a new sequence-ID namespace, discards latent states at once, and builds p32 belief
pools for the unchanged x4b-v1 screen. No model, checkpoint or fitting is involved.
"""

from __future__ import annotations

import hashlib

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
    canonical_json,
    tokens_hash,
)
from topo_pilot.dataset import HMMSampler
from topo_pilot.oracle import BayesFilter

from .x4b import END, FutureMaps, Pool

PROTOCOL_VERSION = "x4b2-v1"
ROLES = ("reference", "repetition1", "repetition2", "repetition3")
TEST_ROLE = "reference"
N_POOL = 16_384
NAMESPACE_CODE = 5
STREAM = ("x4b2-v1", "pool", "cylinder", "overlap", "1.25")
FROZEN_SEEDS = {"reference": 4472965773301758267, "repetition1": 9041520877900685805,
                "repetition2": 1190608976536703855, "repetition3": 264034718665583389}
FROZEN_CODES = {"reference": 2076810545, "repetition1": 662554568, "repetition2": 31366180,
                "repetition3": 2024988825}
CHUNK = 4096
CHI2_MIN_P = 1e-4


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, "experiment.X4B2", check, detail)


def process_code(family: str, mode: str, sigma: str, replicate: str) -> int:
    """First 31 bits of ``sha256(canonical_json([family, mode, sigma, replicate]))`` (the
    documented dataset rule, dataset/README)."""
    digest = hashlib.sha256(canonical_json([family, mode, sigma, replicate]).encode()).digest()
    return int.from_bytes(digest[:4], "big") >> 1


def sequence_ids(role: str, n: int = N_POOL) -> NDArray[np.int64]:
    """``(process_code << 32) | (5 << 28) | index`` in namespace ``x4b2-v1:<role>``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if the code differs from the frozen value or ``n >= 2**28``.
    """
    code = process_code("cylinder", "overlap", "1.25", f"{PROTOCOL_VERSION}:{role}")
    if code != FROZEN_CODES.get(role) or n >= 1 << 28:
        raise _fail(ErrorCode.INVALID_CONFIG, "namespace", f"{role}: code {code}, n {n}")
    return ((code << 32) | (NAMESPACE_CODE << 28)) + np.arange(n, dtype=np.int64)


def sample_pool(role: str, T: NDArray, E_canon: NDArray, pi: NDArray,
                n: int = N_POOL) -> tuple[NDArray[np.uint8], dict]:
    """Canonical tokens ``[n, 33]`` from the frozen stream of ``role``; states are discarded.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if the derived seed differs from the frozen value;
        ``ALIGNMENT_ERROR`` on out-of-range draws; ``NUMERICAL_FAILURE`` (``sampler_bias``) if
        the first-token chi-square p-value against ``pi E`` is below 1e-4.
    """
    tree = SeedTree(0)
    rng = tree.generator(*STREAM, role)
    seed = tree.issued["/".join([*STREAM, role])]
    if seed != FROZEN_SEEDS.get(role):
        raise _fail(ErrorCode.INVALID_CONFIG, "seed", f"{role}: derived seed {seed}")
    tokens, states = HMMSampler(T, E_canon, pi, SequenceLayout()).sample(n, rng)
    N, V = np.asarray(E_canon).shape
    if int(tokens.max()) >= V or int(states.min()) < 0 or int(states.max()) >= N:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "range", f"{role}: draw out of range")
    del states  # latent states are never persisted or passed on
    p = first_token_p(tokens[:, 0], np.asarray(pi) @ np.asarray(E_canon))
    if p < CHI2_MIN_P:
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "sampler_bias", f"{role}: p={p:.3g}")
    return tokens, {"role": role, "stream": "/".join([*STREAM, role]), "seed": seed,
                    "n": n, "first_token_chi2_p": p}


def first_token_p(first: NDArray, p_w: NDArray) -> float:
    """Chi-square p-value of first-token counts against ``n p_w`` (cells < 5 expected pooled)."""
    obs = np.bincount(np.asarray(first, dtype=np.int64), minlength=p_w.size).astype(float)
    exp = first.size * p_w / p_w.sum()
    small = exp < 5.0
    obs = np.append(obs[~small], obs[small].sum())
    exp = np.append(exp[~small], exp[small].sum())
    keep = exp > 0
    return float(stats.chisquare(obs[keep], exp[keep]).pvalue)


def beliefs_p32(T: NDArray, E: NDArray, pi: NDArray, tokens32: NDArray,
                chunk: int = CHUNK) -> NDArray[np.float64]:
    """``b32 [R, N]`` by the existing BayesFilter, in row chunks to bound memory."""
    filt = BayesFilter(T, E, pi)
    tok = np.asarray(tokens32, dtype=np.int64)
    return np.vstack([filt.run(tok[i:i + chunk]).b[:, END - 1]
                      for i in range(0, tok.shape[0], chunk)])


def build_b2_pool(role: str, tokens: NDArray, seq: NDArray, T: NDArray, E_canon: NDArray,
                  pi: NDArray, maps: FutureMaps) -> Pool:
    """Pool (canonical vocabulary) for the x4b-v1 screen; history = first 32 symbols."""
    canon = np.asarray(tokens[:, :END], dtype=np.int64)
    keys = tuple(tokens_hash(c) for c in canon)
    ids = tuple(f"x4b2-{role}|{int(s)}|{k}" for s, k in zip(np.asarray(seq).tolist(), keys))
    b32 = beliefs_p32(T, E_canon, pi, canon)
    return Pool(role, ids, keys, canon, canon[:, -1], b32, b32 @ maps.G1, b32 @ maps.G2, {},
                np.asarray(seq, dtype=np.int64))


def windows(tokens32: NDArray) -> NDArray:
    """Unique 32-symbol windows as fixed-width byte records (for overlap counting)."""
    arr = np.ascontiguousarray(np.asarray(tokens32, dtype=np.uint8))
    return np.unique(arr.view(np.dtype((np.void, arr.shape[1]))).ravel())


def stored_sequence_ids(store: ArtifactStore) -> NDArray[np.int64]:
    """Every sequence id of every ObservationSet in ``store``."""
    return np.concatenate([np.asarray(store.load(ObservationSet, a, consumer="experiment")
                                      .sequence_id, dtype=np.int64)
                           for a in store.find(ObservationSet)])


def ambient_match(audit, reference: dict, tol: float = 1e-12) -> dict:
    """Compare a recomputed tangent audit with Phase B's ``ambient.json['canonical']``."""
    def diff(a, b) -> float:
        a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        return float(np.max(np.abs(a - b))) if a.shape == b.shape else float("inf")
    out = {"verdict_equal": audit.verdict == reference["verdict"],
           "H_spectrum_diff": diff(audit.H_singular_values, reference["H_singular_values"]),
           "G2_spectrum_diff": diff(audit.G2_singular_values, reference["G2_singular_values"]),
           "rho_diff": diff([r.rho for r in audit.rows], [r["rho"] for r in reference["rows"]])}
    out["ok"] = out["verdict_equal"] and all(out[k] <= tol for k in
                                             ("H_spectrum_diff", "G2_spectrum_diff", "rho_diff"))
    return out
