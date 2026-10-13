"""X4 Phase B adapter (M1/M2): frozen inputs, float64 future maps and reachable pools.

Protocol x4b-v1 (docs/proposals/X4_FEASIBILITY_PROTOCOL.md). Reads existing artifacts only (no
checkpoint, ActivationSet or EvalSidecar) and reuses the oracle kernels unchanged. Outputs go
to an independent store through :class:`ReadThroughBackend`, which never writes to the main one.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.analysis import joint_marginals
from topo_pilot.contracts import (
    ArtifactBackend,
    ArtifactStore,
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    StageFailure,
    TransitionSpec,
    tokens_hash,
)
from topo_pilot.oracle import BayesFilter, FutureOperator

from .config import ResolvedConfig
from .s2 import child_of
from .s3 import find_run_inputs, selected_sigma

CONS = "experiment"
END = 32
PROTOCOL_VERSION = "x4b-v1"
SEEDS = (1729, 2718, 3141)
SIGMA = 1.25
EXPECTED = {
    1729: {"emission": "3633ac27dab50cf4", "obs_test": "2a67b2c947e293ba",
           "history_index": "afb6e7120c9477b1", "oracle": "efebc05165d4f7bc",
           "diagnostics": "2cd84acf8e3897b2", "obs_dev": "096f9b6dbe8536cd",
           "dev_index": "d9fe461a56797514"},
    2718: {"emission": "97838b9e13a26f74", "obs_test": "95c4d118517ecd92",
           "history_index": "908cb61ffbd956c6", "oracle": "d9c6defcc7a9d803",
           "diagnostics": "c904849c3b3ba6d7", "obs_dev": "d6d3eeb32dfa40ac",
           "dev_index": "880c3e8ec8347b72"},
    3141: {"emission": "8c29c329c197c79e", "obs_test": "2e2cf22bb4820155",
           "history_index": "7e7d27bd143ebeb5", "oracle": "1731629d61077e96",
           "diagnostics": "07a9775b7c0eae63", "obs_dev": "6da65c49fac77b30",
           "dev_index": "d5e64c5398ef4c25"},
}
SHARED = {"world": "21feee1d8ee5422e", "transition": "e4dafc7b9785c172"}
S7_RECORDS = {"dev_extract": "13be28a051ce15b1", "probes": "63ebd7ec1ba5f38a",
              "circular": "a7a60592e32b26fb", "sensitivity": "baff2c7a1e5294c9"}


def _missing(check: str, detail: str) -> StageFailure:
    return StageFailure(ErrorCode.MISSING_PARENT, "experiment.X4B", check, detail)


class ReadThroughBackend(ArtifactBackend):
    """Reads from ``writable`` then ``read_only``; writes only to ``writable``."""

    def __init__(self, read_only: ArtifactBackend, writable: ArtifactBackend) -> None:
        self.read_only, self.writable = read_only, writable

    def put(self, key: str, data: bytes) -> None:
        self.writable.put(key, data)

    def get(self, key: str) -> bytes:
        return self.writable.get(key) if self.writable.exists(key) else self.read_only.get(key)

    def exists(self, key: str) -> bool:
        return self.writable.exists(key) or self.read_only.exists(key)

    def list(self, prefix: str) -> list[str]:
        return sorted(set(self.writable.list(prefix)) | set(self.read_only.list(prefix)))


def ancestors(store: ArtifactStore, artifact_id: str) -> set[str]:
    """Every transitive parent id of ``artifact_id``."""
    seen: set[str] = set()
    frontier = [artifact_id]
    while frontier:
        nxt = []
        for aid in frontier:
            for pid in store.meta(aid).parent_ids:
                if pid not in seen:
                    seen.add(pid)
                    nxt.append(pid)
        frontier = nxt
    return seen


def resolve_inputs(cfg: ResolvedConfig, store: ArtifactStore) -> dict[int, dict[str, str]]:
    """Resolve the cylinder-O inputs of each seed and check them against the frozen table.

    Raises
    ------
    StageFailure
        ``MISSING_PARENT`` if σ, any id or the S7 dev lineage differs from protocol x4b-v1.
    """
    sigma = selected_sigma(store)
    if sigma != SIGMA:
        raise _missing("sigma", f"selected sigma {sigma} != {SIGMA}")
    lineage = ancestors(store, S7_RECORDS["dev_extract"])
    out = {}
    for seed in SEEDS:
        inp = dict(find_run_inputs(store, cfg, "cylinder", "O", sigma, seed))
        inp["transition"] = child_of(store, TransitionSpec, inp["world"])
        inp["dev_index"] = child_of(store, HistoryIndex, inp["obs_dev"], split="dev")
        want = {**EXPECTED[seed], **SHARED}
        bad = {k: (inp.get(k), v) for k, v in want.items() if inp.get(k) != v}
        if bad:
            raise _missing("frozen_inputs", f"seed {seed}: {bad}")
        if not {inp["dev_index"], inp["obs_dev"]} <= lineage:
            raise _missing("s7_lineage", f"seed {seed}: dev pool not under S7 dev extraction")
        out[seed] = inp
    return out


def provenance_row(store: ArtifactStore, artifact_id: str, role: str) -> dict:
    """Identity of one input artifact (type, producer commit, checksum, parents)."""
    meta = store.meta(artifact_id)
    return {"role": role, "artifact_id": artifact_id, "type": meta.artifact_type,
            "producer_version": meta.producer_version, "payload_sha256": meta.payload_sha256,
            "created_utc": meta.created_utc, "parents": list(meta.parent_ids)}


@dataclass(frozen=True, eq=False)
class FutureMaps:
    """``G1 [N, V]``, joint ``G2 [N, V*V]`` (lexicographic) and the checks of protocol §3."""

    G1: NDArray[np.float64]
    G2: NDArray[np.float64]
    O_singular_values: tuple[NDArray[np.float64], NDArray[np.float64]]
    checks: dict[str, float]


MAP_LIMITS = {"route_diff": 1e-12, "lexicographic_diff": 1e-12, "O1_vs_G1T": 0.0,
              "O2_head_vs_O1": 0.0, "G1_row_sum": 1e-10, "G2_row_sum": 1e-10,
              "first_marginal_diff": 1e-12, "second_marginal_vs_T2E": 1e-12}


def future_maps(T: NDArray, E: NDArray) -> FutureMaps:
    """Float64 one-step and joint two-step maps by two FutureOperator routes, cross-checked.

    Math
    ----
    Route A: ``observability_matrices(2) = [O1, O2]``, ``G2 = O2[V:]^T``. Route B: ``F2`` on the
    identity beliefs. Explicit: block ``i`` of G2 is ``T diag(E[:, i]) T E``.
    """
    fut = FutureOperator(T, E)
    n, v = fut.E.shape
    O1, O2 = fut.observability_matrices(2)
    G1 = fut.TE
    G2 = O2[v:].T.copy()
    route_b = fut.F2(np.eye(n)).reshape(n, v * v)
    explicit = np.hstack([(fut.T * fut.E[:, i][None, :]) @ G1 for i in range(v)])
    first, second = joint_marginals(G2, v)
    checks = {
        "route_diff": float(np.max(np.abs(G2 - route_b))),
        "lexicographic_diff": float(np.max(np.abs(G2 - explicit))),
        "O1_vs_G1T": float(np.max(np.abs(O1 - G1.T))),
        "O2_head_vs_O1": float(np.max(np.abs(O2[:v] - O1))),
        "G1_row_sum": float(np.max(np.abs(G1.sum(1) - 1))),
        "G2_row_sum": float(np.max(np.abs(G2.sum(1) - 1))),
        "G2_min": float(G2.min()),
        "first_marginal_diff": float(np.max(np.abs(first - G1))),
        "second_marginal_vs_T2E": float(np.max(np.abs(second - fut.T @ G1))),
        "second_marginal_vs_G1": float(np.max(np.abs(second - G1))),
    }
    svs = (np.linalg.svd(O1, compute_uv=False), np.linalg.svd(O2, compute_uv=False))
    return FutureMaps(G1, G2, svs, checks)


def map_failures(maps: FutureMaps) -> list[str]:
    """Names of protocol §3 checks that fail (empty when all pass)."""
    bad = [k for k, lim in MAP_LIMITS.items() if not maps.checks[k] <= lim]
    if maps.checks["G2_min"] < -1e-14:
        bad.append("G2_min")
    return bad


def canonical_tokens(tokens: NDArray, symbol_perm: NDArray) -> NDArray[np.int64]:
    """Canonical indices ``j`` with ``token = symbol_perm[j]`` (D-019)."""
    return np.argsort(np.asarray(symbol_perm))[np.asarray(tokens, dtype=np.int64)]


def index_tokens(store: ArtifactStore, index_id: str, obs_id: str) -> tuple[HistoryIndex, NDArray]:
    """HistoryIndex and its ``[M, 32]`` run-vocabulary tokens (checked against tokens_hash)."""
    index = store.load(HistoryIndex, index_id, consumer=CONS)
    obs = store.load(ObservationSet, obs_id, consumer=CONS)
    row = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
    tok = np.asarray(obs.tokens[[row[int(s)] for s in index.sequence_id.tolist()], :END],
                     dtype=np.int64)
    if [tokens_hash(t) for t in tok] != [str(h) for h in index.tokens_hash]:
        raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.X4B", "tokens_hash",
                           f"index {index_id} does not match {obs_id}")
    return index, tok


@dataclass(frozen=True, eq=False)
class Pool:
    """One reachable pool in the canonical vocabulary (rows in the first run's index order)."""

    name: str
    canonical_ids: tuple[str, ...]
    history_keys: tuple[str, ...]
    canonical: NDArray[np.int64]
    last_symbol: NDArray[np.int64]
    b32: NDArray[np.float64]
    Q1: NDArray[np.float64]
    Q2: NDArray[np.float64]
    run_history_ids: dict[int, tuple[str, ...]]
    sequence_id: NDArray[np.int64]


def build_pool(name: str, split: str, runs: list[tuple[int, HistoryIndex, NDArray, NDArray]],
               T: NDArray, E_canon: NDArray, pi: NDArray, maps: FutureMaps) -> Pool:
    """Canonical pool from one or more runs sharing trajectories (``(seed, index, tokens,
    symbol_perm)`` each); runs are joined on sequence id and must give equal canonical tokens.

    Raises
    ------
    StageFailure
        ``SAMPLE_ID_MISMATCH`` if runs disagree on sequence ids or canonical tokens.
    """
    seed0, index0, tok0, perm0 = runs[0]
    seq = np.asarray(index0.sequence_id, dtype=np.int64)
    canon = canonical_tokens(tok0, perm0)
    hist_ids = {seed0: tuple(str(h) for h in index0.history_id)}
    for seed, index, tok, perm in runs[1:]:
        pos = {int(s): i for i, s in enumerate(index.sequence_id.tolist())}
        rows = [pos.get(int(s), -1) for s in seq.tolist()]
        if min(rows) < 0 or not np.array_equal(canonical_tokens(tok, perm)[rows], canon):
            raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.X4B", "canonical",
                               f"{name}: run {seed} disagrees with run {seed0}")
        hist_ids[seed] = tuple(str(index.history_id[r]) for r in rows)
    keys = tuple(tokens_hash(c) for c in canon)
    ids = tuple(f"{split}|{int(s)}|{k}" for s, k in zip(seq.tolist(), keys))
    b32 = BayesFilter(T, E_canon, pi).run(canon).b[:, END - 1]
    return Pool(name, ids, keys, canon, canon[:, -1], b32, b32 @ maps.G1, b32 @ maps.G2,
                hist_ids, seq)


def pool_checks(pool: Pool, V: int) -> dict[str, float]:
    """Row sums, minimum entries and Σ_j Q2 = Q1 for a pool (protocol §5)."""
    first, _ = joint_marginals(pool.Q2, V)
    return {"Q1_row_sum": float(np.max(np.abs(pool.Q1.sum(1) - 1))),
            "Q2_row_sum": float(np.max(np.abs(pool.Q2.sum(1) - 1))),
            "Q1_min": float(pool.Q1.min()), "Q2_min": float(pool.Q2.min()),
            "marginal_diff": float(np.max(np.abs(first - pool.Q1)))}


def pool_failures(checks: dict[str, float]) -> list[str]:
    """Names of failed pool checks."""
    lim = {"Q1_row_sum": 1e-10, "Q2_row_sum": 1e-10, "marginal_diff": 1e-12}
    bad = [k for k, v in lim.items() if not checks[k] <= v]
    return bad + [k for k in ("Q1_min", "Q2_min") if checks[k] < -1e-14]
