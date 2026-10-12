"""Error codes, result statuses, and the single project exception ``StageFailure``."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass, fields
from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """Codes carried by :class:`StageFailure`. The value equals the name."""

    INVALID_CONFIG = "INVALID_CONFIG"
    SCHEMA_VERSION_MISMATCH = "SCHEMA_VERSION_MISMATCH"
    ARTIFACT_MISSING = "ARTIFACT_MISSING"
    CHECKSUM_MISMATCH = "CHECKSUM_MISMATCH"
    LEAKAGE = "LEAKAGE"
    INVALID_GLUE = "INVALID_GLUE"
    BETTI_MISMATCH = "BETTI_MISMATCH"
    NON_METRIC = "NON_METRIC"
    NONSTOCHASTIC = "NONSTOCHASTIC"
    STATIONARITY_FAILURE = "STATIONARITY_FAILURE"
    INVALID_SIGMA = "INVALID_SIGMA"
    STATE_ORDER_MISMATCH = "STATE_ORDER_MISMATCH"
    SPLIT_OVERLAP = "SPLIT_OVERLAP"
    ALIGNMENT_ERROR = "ALIGNMENT_ERROR"
    IMPOSSIBLE_HISTORY = "IMPOSSIBLE_HISTORY"
    NUMERICAL_FAILURE = "NUMERICAL_FAILURE"
    NONFINITE_LOSS = "NONFINITE_LOSS"
    CAUSAL_MASK_FAILED = "CAUSAL_MASK_FAILED"
    UNKNOWN_HOOK = "UNKNOWN_HOOK"
    JOIN_CARDINALITY = "JOIN_CARDINALITY"
    PH_RESOURCE_LIMIT = "PH_RESOURCE_LIMIT"
    SAMPLE_ID_MISMATCH = "SAMPLE_ID_MISMATCH"
    GATE_FAILED = "GATE_FAILED"
    MISSING_PARENT = "MISSING_PARENT"
    CONFIG_DRIFT = "CONFIG_DRIFT"
    EXECUTOR_ERROR = "EXECUTOR_ERROR"


class Status(str, Enum):
    """Non-exception outcomes stored in results ("cannot decide" is a status, not an error)."""

    OK = "ok"
    COLLAPSED = "collapsed"
    CENSORED = "censored"
    NONSEPARABLE = "nonseparable"
    INCONCLUSIVE = "inconclusive"
    NOT_RUN = "not_run"
    APPROXIMATE = "approximate"


@dataclass(frozen=True, eq=False)
class StageFailure(Exception):
    """The only exception type raised for invariant violations anywhere in the project.

    Parameters
    ----------
    code : ErrorCode
        Machine-readable failure class.
    component : str
        Module or class that detected the failure, e.g. ``"contracts.ArtifactStore"``.
    check : str
        Name of the violated check, e.g. ``"rows_sum_to_one"``.
    detail : str
        Human-readable detail (never an array dump).
    artifact_id : str or None
        The artifact concerned, if any.
    recoverable : bool
        True if a retry or a different input could succeed.

    Notes
    -----
    The instance is frozen; only interpreter-managed dunder attributes (``__traceback__``,
    ``__context__``, ``__cause__``, ``__notes__``) may be set, so it can be raised, chained,
    and pickled across processes.
    """

    code: ErrorCode
    component: str
    check: str
    detail: str
    artifact_id: str | None = None
    recoverable: bool = False

    def __post_init__(self) -> None:
        Exception.__init__(self, self.code, self.component, self.check, self.detail)

    def __str__(self) -> str:
        code = self.code.value if isinstance(self.code, ErrorCode) else str(self.code)
        where = f" (artifact {self.artifact_id})" if self.artifact_id else ""
        return f"[{code}] {self.component}.{self.check}: {self.detail}{where}"

    def __reduce__(self) -> tuple[Any, tuple[Any, ...]]:
        return (type(self), tuple(getattr(self, f.name) for f in fields(self)))


def _stage_failure_setattr(self: StageFailure, name: str, value: Any) -> None:
    if name.startswith("__") and name.endswith("__"):
        object.__setattr__(self, name, value)
        return
    raise FrozenInstanceError(f"cannot assign to field {name!r}")


StageFailure.__setattr__ = _stage_failure_setattr  # type: ignore[method-assign]
