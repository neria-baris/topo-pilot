"""All typed artifacts (one frozen dataclass each); field docs in ``docs/DATA_SCHEMAS.md``."""

from __future__ import annotations

from ._schemas_data import (
                            BaselineOutputs,
                            EvalSidecar,
                            HistoryIndex,
                            ObservationSet,
                            OracleOutputs,
                            ProcessDiagnostics,
)
from ._schemas_results import (
                            ActivationSet,
                            Checkpoint,
                            Diagrams,
                            DistanceArtifact,
                            GateCheck,
                            GateReport,
                            MetricRecords,
                            MetricRow,
                            RunManifest,
)
from ._schemas_world import EmissionSpec, TransitionSpec, WorldSpec
from .base import Artifact

ARTIFACT_CLASSES: dict[str, type[Artifact]] = {
    cls.ARTIFACT_TYPE: cls
    for cls in (WorldSpec, TransitionSpec, EmissionSpec, ObservationSet, EvalSidecar, HistoryIndex,
                OracleOutputs, ProcessDiagnostics, BaselineOutputs, Checkpoint, ActivationSet,
                DistanceArtifact, Diagrams, MetricRecords, GateReport, RunManifest)
}

__all__ = [
    "ARTIFACT_CLASSES", "ActivationSet", "BaselineOutputs", "Checkpoint", "Diagrams",
    "DistanceArtifact", "EmissionSpec", "EvalSidecar", "GateCheck", "GateReport", "HistoryIndex",
    "MetricRecords", "MetricRow", "ObservationSet", "OracleOutputs", "ProcessDiagnostics",
    "RunManifest", "TransitionSpec", "WorldSpec",
]
