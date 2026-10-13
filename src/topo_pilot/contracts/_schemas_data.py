"""Data, oracle and baseline artifacts (DATA_SCHEMAS §3–§4)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar

import numpy as np

from . import _checks as ck
from .base import Artifact, array_field, optional_array_field
from .errors import ErrorCode
from .ids import make_history_id

SPLITS = ("train", "dev", "test")
N_OBS = 33


def _token_dtype_ok(tokens: np.ndarray, V: int) -> bool:
    return tokens.dtype == (np.uint8 if V <= 255 else np.uint16)


@dataclass(frozen=True, eq=False)
class ObservationSet(Artifact):
    """Public token data for one split.

    Fields: ``split`` in {train, dev, test}; ``sequence_id: int64[R]`` globally unique;
    ``tokens: uint8[R, 33]`` (``uint16`` if V > 255) holding ``w_1..w_33``; ``V``;
    ``layout_version``. Contains **no** latent information.

    Invariants: shapes and dtypes, all tokens < V (``ALIGNMENT_ERROR``); unique ids
    (``SAMPLE_ID_MISMATCH``).
    """

    ARTIFACT_TYPE: ClassVar[str] = "ObservationSet"

    split: str
    V: int
    sequence_id: np.ndarray = array_field()
    tokens: np.ndarray = array_field()
    layout_version: str = "1"

    @property
    def n_sequences(self) -> int:
        """Number of trajectories R."""
        return int(self.tokens.shape[0])

    def validate(self) -> None:
        name = "ObservationSet"
        if self.split not in SPLITS:
            raise self._fail(ErrorCode.INVALID_CONFIG, "split", f"unknown split {self.split!r}")
        tokens = ck.require_array(name, "tokens", self.tokens, 2, "u")
        ids = ck.require_array(name, "sequence_id", self.sequence_id, 1, "i")
        ck.require_dtype(name, "sequence_id", ids, ["int64"])
        if tokens.shape[1] != N_OBS or not _token_dtype_ok(tokens, self.V):
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "tokens_layout",
                             f"tokens {tokens.dtype} {tokens.shape} for V={self.V}")
        ck.require_len(name, "sequence_id", ids, tokens.shape[0])
        if tokens.size and int(tokens.max()) >= self.V:
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "token_range", "token id >= V")
        ck.require_unique(name, "sequence_id", ids, ErrorCode.SAMPLE_ID_MISMATCH)


@dataclass(frozen=True, eq=False)
class EvalSidecar(Artifact):
    """Privileged latent states for dev/test: ``z: int16[R, 33]``; ``z[:, t]`` emitted
    ``tokens[:, t]``.

    Loading is restricted by ``DEFAULT_ACCESS_POLICY`` (``learner``/``activations`` -> ``LEAKAGE``).
    Invariants: ``split`` in {dev, test}; states in ``0..N-1``; ids unique and aligned.
    """

    ARTIFACT_TYPE: ClassVar[str] = "EvalSidecar"

    split: str
    N: int
    sequence_id: np.ndarray = array_field()
    z: np.ndarray = array_field()

    def validate(self) -> None:
        name = "EvalSidecar"
        if self.split not in ("dev", "test"):
            raise self._fail(ErrorCode.INVALID_CONFIG, "split", "sidecars exist for dev/test only")
        z = ck.require_array(name, "z", self.z, 2, "i")
        ck.require_dtype(name, "z", z, ["int16"])
        ids = ck.require_array(name, "sequence_id", self.sequence_id, 1, "i")
        if z.shape[1] != N_OBS:
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "z_layout", f"z shape {z.shape}")
        ck.require_len(name, "sequence_id", ids, z.shape[0])
        if z.size and (int(z.min()) < 0 or int(z.max()) >= self.N):
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "state_range", "state id outside 0..N-1")
        ck.require_unique(name, "sequence_id", ids, ErrorCode.SAMPLE_ID_MISMATCH)


@dataclass(frozen=True, eq=False)
class HistoryIndex(Artifact):
    """Analysis histories, one per trajectory, grouped into disjoint panels.

    ``history_id[i] = make_history_id(dataset_id, sequence_id[i], end[i], tokens_hash[i])``
    with ``tokens_hash = contracts.tokens_hash(w_1..w_end)``. Arrays are length M; string arrays
    use fixed-width unicode (``<U16``); ``panel`` is in ``1..n_panels``.

    Invariants: aligned lengths (``ALIGNMENT_ERROR``); ids recompute and are unique
    (``SAMPLE_ID_MISMATCH``); a trajectory appears at most once overall, so panels are
    disjoint (``SPLIT_OVERLAP``); every panel ``1..n_panels`` has exactly ``panel_size`` rows
    (``JOIN_CARDINALITY``).
    """

    ARTIFACT_TYPE: ClassVar[str] = "HistoryIndex"

    dataset_id: str
    history_id: np.ndarray = array_field()
    sequence_id: np.ndarray = array_field()
    end: np.ndarray = array_field()
    panel: np.ndarray = array_field()
    tokens_hash: np.ndarray = array_field()
    panel_size: int = 512
    n_panels: int = 8

    def validate(self) -> None:
        name = "HistoryIndex"
        hid = ck.require_array(name, "history_id", self.history_id, 1, "U")
        m = hid.shape[0]
        for key in ("sequence_id", "end", "panel"):
            ck.require_len(name, key, ck.require_array(name, key, getattr(self, key), 1, "iu"), m)
        ck.require_len(name, "tokens_hash", ck.require_array(name, "tokens_hash",
                                                             self.tokens_hash, 1, "U"), m)
        expected = [make_history_id(self.dataset_id, s, e, h) for s, e, h in
                    zip(self.sequence_id.tolist(), self.end.tolist(), self.tokens_hash.tolist())]
        if hid.tolist() != expected:
            raise self._fail(ErrorCode.SAMPLE_ID_MISMATCH, "history_id", "ids do not recompute")
        ck.require_unique(name, "history_id", hid, ErrorCode.SAMPLE_ID_MISMATCH)
        ck.require_unique(name, "sequence_id", self.sequence_id, ErrorCode.SPLIT_OVERLAP)
        panels, counts = np.unique(self.panel, return_counts=True)
        if (panels.tolist() != list(range(1, self.n_panels + 1))
                or np.any(counts != self.panel_size)):
            raise self._fail(ErrorCode.JOIN_CARDINALITY, "panels",
                             f"need panels 1..{self.n_panels} of {self.panel_size} rows each")


@dataclass(frozen=True, eq=False)
class OracleOutputs(Artifact):
    """Exact-filter quantities per history (rows aligned with ``history_id``, float64 unless noted).

    ``b32, b1: [M, N]`` beliefs b^(32) and b^(1) = r_{w_32}; ``q, q_last: [M, V]`` next-symbol
    predictive under the full and last-symbol posteriors; ``F2: [M, V, V] float32`` (panels only,
    flattened as ``i*V + j`` = (next1, next2)); ``belief_entropy, log_evidence: [M]``;
    ``ce_oracle_all_positions: [R_test, 33] float32`` (optional).

    Invariants: aligned shapes (``ALIGNMENT_ERROR``); distributions are finite, ≥ 0, and sum to 1
    within 1e-9 (1e-4 for float32 ``F2``) (``NUMERICAL_FAILURE``); unique ids.
    """

    ARTIFACT_TYPE: ClassVar[str] = "OracleOutputs"

    history_id: np.ndarray = array_field()
    b32: np.ndarray = array_field()
    b1: np.ndarray = array_field()
    q: np.ndarray = array_field()
    q_last: np.ndarray = array_field()
    belief_entropy: np.ndarray = array_field()
    log_evidence: np.ndarray = array_field()
    F2: np.ndarray | None = optional_array_field()
    ce_oracle_all_positions: np.ndarray | None = optional_array_field()

    def validate(self) -> None:
        name = "OracleOutputs"
        m = ck.require_array(name, "history_id", self.history_id, 1, "U").shape[0]
        ck.require_unique(name, "history_id", self.history_id, ErrorCode.SAMPLE_ID_MISMATCH)
        for key in ("b32", "b1", "q", "q_last"):
            arr = ck.require_array(name, key, getattr(self, key), 2, "f")
            ck.require_len(name, key, arr, m)
            ck.require_distribution_rows(name, key, arr, 1e-9)
        if self.b32.shape != self.b1.shape or self.q.shape != self.q_last.shape:
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "widths",
                             "belief or predictive widths differ")
        for key in ("belief_entropy", "log_evidence"):
            arr = ck.require_array(name, key, getattr(self, key), 1, "f")
            ck.require_len(name, key, arr, m)
            ck.require_finite(name, key, arr)
        if self.F2 is not None:
            v = self.q.shape[1]
            F2 = ck.require_array(name, "F2", self.F2, 3, "f")
            if F2.shape != (m, v, v):
                raise self._fail(ErrorCode.ALIGNMENT_ERROR, "F2_shape", f"F2 {F2.shape}")
            ck.require_distribution_rows(name, "F2", F2.astype(np.float64), 1e-4)
        if self.ce_oracle_all_positions is not None:
            ce = ck.require_array(name, "ce_oracle_all_positions",
                                  self.ce_oracle_all_positions, 2, "f")
            if ce.shape[1] != N_OBS:
                raise self._fail(ErrorCode.ALIGNMENT_ERROR, "ce_shape", f"ce {ce.shape}")
            ck.require_finite(name, "ce_oracle_all_positions", ce)


@dataclass(frozen=True, eq=False)
class ProcessDiagnostics(Artifact):
    """Process-level diagnostics: context gain ``G_C`` (nats), mean entropy of b^(1) (nats),
    singular values of the observability matrices ``O_k`` (k ≤ 3), and the σ calibration table
    (one mapping per σ candidate). Invariants: finite, ``G_C ≥ -1e-12``, ``mean_H_b1 ≥ 0``."""

    ARTIFACT_TYPE: ClassVar[str] = "ProcessDiagnostics"

    G_C: float
    mean_H_b1: float
    O_singular_values: tuple[tuple[float, ...], ...] = ()
    sigma_table: tuple[Mapping[str, Any], ...] = ()
    sigma: float | None = None
    world_family: str = ""

    def validate(self) -> None:
        values = np.array([self.G_C, self.mean_H_b1], dtype=np.float64)
        if not np.all(np.isfinite(values)) or self.G_C < -1e-12 or self.mean_H_b1 < 0:
            raise self._fail(ErrorCode.NUMERICAL_FAILURE, "values",
                             f"G_C={self.G_C}, mean_H_b1={self.mean_H_b1}")


@dataclass(frozen=True, eq=False)
class BaselineOutputs(Artifact):
    """n-gram baseline predictive ``probs: [M, V] float64`` aligned to ``history_id``.
    Invariants: aligned; rows are distributions within 1e-9 (``NUMERICAL_FAILURE``)."""

    ARTIFACT_TYPE: ClassVar[str] = "BaselineOutputs"

    ngram_order: int
    smoothing: str
    history_id: np.ndarray = array_field()
    probs: np.ndarray = array_field()
    extra_info: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        name = "BaselineOutputs"
        m = ck.require_array(name, "history_id", self.history_id, 1, "U").shape[0]
        probs = ck.require_array(name, "probs", self.probs, 2, "f")
        ck.require_len(name, "probs", probs, m)
        ck.require_distribution_rows(name, "probs", probs, 1e-9)
        if self.ngram_order < 0:
            raise self._fail(ErrorCode.INVALID_CONFIG, "ngram_order", str(self.ngram_order))
