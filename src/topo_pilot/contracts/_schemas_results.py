"""Model, topology and result artifacts (DATA_SCHEMAS §5–§6)."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar

import numpy as np

from . import _checks as ck
from .base import Artifact, array_field, optional_array_field
from .errors import ErrorCode, Status

ACTIVATION_SOURCES = ("model", "baseline:R0", "baseline:R1", "baseline:R2", "baseline:R3")
STATUS_VALUES = tuple(s.value for s in Status)
GATE_VERDICTS = ("pass", "fail", "waived")


@dataclass(frozen=True, eq=False)
class Checkpoint(Artifact):
    """Model weights at one training step. ``state`` is an opaque ``torch.save`` blob stored as
    ``state.pt`` (contracts never imports torch). Optimizer and RNG state are included only for
    the last step (``has_optimizer_state``). Invariants: ``step ≥ 0``; non-empty state."""

    ARTIFACT_TYPE: ClassVar[str] = "Checkpoint"
    BLOB_FILES: ClassVar[Mapping[str, str]] = {"state": "state.pt"}

    run_id: str
    step: int
    observation_id: str
    state: bytes = field(repr=False)
    model_config: Mapping[str, Any] = field(default_factory=dict)
    train_config: Mapping[str, Any] = field(default_factory=dict)
    has_optimizer_state: bool = False
    layout_version: str = "1"

    def validate(self) -> None:
        if self.step < 0 or not self.run_id or not self.observation_id:
            raise self._fail(ErrorCode.INVALID_CONFIG, "fields", f"step={self.step}")
        if not isinstance(self.state, (bytes, bytearray)) or len(self.state) == 0:
            raise self._fail(ErrorCode.INVALID_CONFIG, "state", "empty or non-bytes state")


@dataclass(frozen=True, eq=False)
class ActivationSet(Artifact):
    """Activations at the analysis position for M histories.

    ``A: [M, K, d] float32`` (hooks in ``hooks`` order); ``logits: [M, V] float32`` or None (for
    representation baselines R2/R3); ``source`` in ``model, baseline:R0..R3``; ``checkpoint_id``
    is None only for baselines that use no checkpoint. Row order equals ``HistoryIndex`` order.
    Invariants: shapes (``ALIGNMENT_ERROR``); finite (``NUMERICAL_FAILURE``); unique hooks
    (``UNKNOWN_HOOK``).
    """

    ARTIFACT_TYPE: ClassVar[str] = "ActivationSet"

    hooks: tuple[str, ...]
    source: str
    history_id: np.ndarray = array_field()
    A: np.ndarray = array_field()
    logits: np.ndarray | None = optional_array_field()
    checkpoint_id: str | None = None

    def validate(self) -> None:
        name = "ActivationSet"
        if self.source not in ACTIVATION_SOURCES:
            raise self._fail(ErrorCode.INVALID_CONFIG, "source", f"unknown source {self.source!r}")
        if not self.hooks or len(set(self.hooks)) != len(self.hooks):
            raise self._fail(ErrorCode.UNKNOWN_HOOK, "hooks", "empty or duplicate hooks")
        m = ck.require_array(name, "history_id", self.history_id, 1, "U").shape[0]
        A = ck.require_array(name, "A", self.A, 3, "f")
        ck.require_dtype(name, "A", A, ["float32"])
        if A.shape[:2] != (m, len(self.hooks)):
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "A_shape", f"A {A.shape} for M={m}")
        ck.require_finite(name, "A", A)
        if self.logits is not None:
            logits = ck.require_array(name, "logits", self.logits, 2, "f")
            ck.require_dtype(name, "logits", logits, ["float32"])
            ck.require_len(name, "logits", logits, m)
            ck.require_finite(name, "logits", logits)
        if self.source in ("model", "baseline:R0", "baseline:R1") and not self.checkpoint_id:
            raise self._fail(ErrorCode.MISSING_PARENT, "checkpoint_id", "model source needs it")


@dataclass(frozen=True, eq=False)
class DistanceArtifact(Artifact):
    """Pairwise distances after deduplication.

    ``point_ids: [M'] <U``; ``D: [M', M'] float64``; ``dedup_map: int64[M]`` maps each original
    point to its row in ``D``; ``scale_s`` = 95th percentile of positive distances (0 if none);
    ``status`` in ``Status`` values (``collapsed`` when all points coincide).
    Invariants: ``D`` symmetric, zero diagonal, ≥ 0, finite (``NON_METRIC``); the map is onto.
    """

    ARTIFACT_TYPE: ClassVar[str] = "DistanceArtifact"

    metric_id: str
    scale_s: float
    point_ids: np.ndarray = array_field()
    D: np.ndarray = array_field()
    dedup_map: np.ndarray = array_field()
    pca_ref: str | None = None
    status: str = "ok"

    def validate(self) -> None:
        name = "DistanceArtifact"
        m = ck.require_array(name, "point_ids", self.point_ids, 1, "U").shape[0]
        D = ck.require_array(name, "D", self.D, 2, "f", ErrorCode.NON_METRIC)
        if D.shape != (m, m):
            raise self._fail(ErrorCode.NON_METRIC, "D_shape", f"D {D.shape} for {m} points")
        ck.require_metric_matrix(name, "D", D, triangle=False)
        dm = ck.require_array(name, "dedup_map", self.dedup_map, 1, "i")
        if dm.size and (dm.min() < 0 or set(np.unique(dm).tolist()) != set(range(m))):
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "dedup_map", "map is not onto 0..M'-1")
        scale_ok = self.scale_s >= 0 and math.isfinite(self.scale_s)
        if self.status not in STATUS_VALUES or not scale_ok:
            raise self._fail(ErrorCode.INVALID_CONFIG, "status_scale",
                             f"status={self.status}, scale_s={self.scale_s}")


@dataclass(frozen=True, eq=False)
class Diagrams(Artifact):
    """Persistence diagrams: ``rows: [n, 4] float64`` with columns (dim, birth, death, censored).

    ``death = inf`` marks a bar that never closed (expected for the H₀ essential class; flagged
    ``censored = 1`` in dim ≥ 1). Invariants: dims in ``0..maxdim``; ``birth ≤ death``; finite
    births; ``censored`` in {0, 1}; ``coeff_p`` prime (``INVALID_CONFIG``/``NUMERICAL_FAILURE``).
    """

    ARTIFACT_TYPE: ClassVar[str] = "Diagrams"

    coeff_p: int
    maxdim: int
    threshold: float
    library_version: str
    rows: np.ndarray = array_field()
    status: str = "ok"

    def validate(self) -> None:
        name = "Diagrams"
        rows = ck.require_array(name, "rows", self.rows, 2, "f")
        if rows.shape[1] != 4:
            raise self._fail(ErrorCode.ALIGNMENT_ERROR, "rows_shape", f"rows {rows.shape}")
        if self.coeff_p < 2 or any(self.coeff_p % k == 0 for k in range(2, self.coeff_p)):
            raise self._fail(ErrorCode.INVALID_CONFIG, "coeff_p", f"{self.coeff_p} is not prime")
        dims, birth, death, cens = rows.T
        if rows.size and (np.any(dims != np.round(dims)) or dims.min() < 0
                          or dims.max() > self.maxdim
                          or not np.all(np.isin(cens, (0.0, 1.0)))):
            raise self._fail(ErrorCode.INVALID_CONFIG, "dims_censored", "bad dim or censored flag")
        if not np.all(np.isfinite(birth)) or np.any(np.isnan(death)) or np.any(death < birth):
            raise self._fail(ErrorCode.NUMERICAL_FAILURE, "bars",
                             "non-finite birth or death < birth")
        if self.status not in STATUS_VALUES:
            raise self._fail(ErrorCode.INVALID_CONFIG, "status", self.status)


@dataclass(frozen=True)
class MetricRow:
    """One row of the long metric table. ``value=None`` means undefined or missing, never 0."""

    run_id: str
    space: str
    metric_id: str
    value: float | None
    status: str = "ok"
    replicate: int | None = None
    world: str | None = None
    condition: str | None = None
    checkpoint: int | None = None
    hook: str | None = None
    panel: int | None = None
    units: str = ""
    uncertainty_kind: str | None = None
    parent_ids: tuple[str, ...] = ()


@dataclass(frozen=True, eq=False)
class MetricRecords(Artifact):
    """Long table of metric values (one ``MetricRow`` per value), stored as JSON.

    Invariants: ``status`` in ``Status`` values; ``value`` finite or None; ``ok`` needs a value;
    ``not_run`` has none (``INVALID_CONFIG``/``NUMERICAL_FAILURE``).
    """

    ARTIFACT_TYPE: ClassVar[str] = "MetricRecords"

    rows: tuple[MetricRow, ...] = ()

    def validate(self) -> None:
        for i, row in enumerate(self.rows):
            if row.status not in STATUS_VALUES:
                raise self._fail(ErrorCode.INVALID_CONFIG, "status", f"row {i}: {row.status!r}")
            if row.value is not None and not math.isfinite(row.value):
                raise self._fail(ErrorCode.NUMERICAL_FAILURE, "value", f"row {i}: non-finite")
            if (row.status == "ok") == (row.value is None) and row.status in ("ok", "not_run"):
                raise self._fail(ErrorCode.INVALID_CONFIG, "value_status",
                                 f"row {i}: status {row.status} with value {row.value}")


@dataclass(frozen=True)
class GateCheck:
    """One gate check: ``value`` and ``threshold`` are JSON scalars (or None)."""

    name: str
    passed: bool
    value: Any = None
    threshold: Any = None


@dataclass(frozen=True, eq=False)
class GateReport(Artifact):
    """Verdict of one gate. Invariants (``INVALID_CONFIG``): ``pass`` needs ≥ 1 check and all
    passed; ``fail`` needs ≥ 1 failed check; ``waived`` needs a non-empty ``waiver_reason``."""

    ARTIFACT_TYPE: ClassVar[str] = "GateReport"

    stage: str
    gate_id: str
    verdict: str
    checks: tuple[GateCheck, ...] = ()
    waiver_reason: str | None = None

    def validate(self) -> None:
        ok = [c.passed for c in self.checks]
        bad = (self.verdict not in GATE_VERDICTS
               or (self.verdict == "pass" and (not ok or not all(ok)))
               or (self.verdict == "fail" and all(ok))
               or (self.verdict == "waived" and not (self.waiver_reason or "").strip()))
        if bad:
            raise self._fail(ErrorCode.INVALID_CONFIG, "verdict",
                             f"verdict {self.verdict!r} inconsistent with checks/waiver")


@dataclass(frozen=True, eq=False)
class RunManifest(Artifact):
    """What ran: the artifact DAG (``id -> parent ids``), resolved config and its hash, seeds,
    per-stage status, hardware, wall time, peak memory, executor, failures and waivers.
    Invariants: non-empty executor and config hash; ``wall_time_s ≥ 0`` (``INVALID_CONFIG``)."""

    ARTIFACT_TYPE: ClassVar[str] = "RunManifest"

    run_key: str
    executor: str
    config_hash: str
    config: Mapping[str, Any] = field(default_factory=dict)
    dag: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    seed_bundle: Mapping[str, int] = field(default_factory=dict)
    stage_status: Mapping[str, str] = field(default_factory=dict)
    hardware: Mapping[str, Any] = field(default_factory=dict)
    wall_time_s: float = 0.0
    peak_mem_mb: float | None = None
    failures: tuple[Mapping[str, Any], ...] = ()
    waivers: tuple[Mapping[str, Any], ...] = ()

    def validate(self) -> None:
        if not self.executor or not self.config_hash or not self.wall_time_s >= 0:
            raise self._fail(ErrorCode.INVALID_CONFIG, "fields",
                             f"executor={self.executor!r}, wall_time_s={self.wall_time_s}")
