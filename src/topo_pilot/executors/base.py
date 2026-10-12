"""Job description, executor ABC, registry, and job.json (de)serialisation (internal)."""

from __future__ import annotations

import json
import subprocess
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Literal

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    LocalFSBackend,
    StageFailure,
    canonical_json,
)

Status = Literal["pending", "running", "done", "failed", "awaiting_user"]


@dataclass(frozen=True)
class JobSpec:
    """One unit of work: a stage plus the artifacts it reads.

    ``resolved_config`` may carry ``"import_modules": [<module names>]``; ``entry`` imports them
    before dispatch (this is how extensions and test stubs register stages in a subprocess).
    ``resources`` is ``{"gpu": bool, "mem_gb": float, "time_h": float}``.
    """

    job_id: str
    stage_id: str
    run_key: tuple | None
    config_hash: str
    resolved_config: Mapping[str, Any]
    input_artifact_ids: tuple[str, ...]
    expected_output_types: tuple[str, ...]
    resources: Mapping[str, Any] = field(default_factory=dict)
    env_lock_hash: str = ""


@dataclass(frozen=True)
class JobHandle:
    """Opaque reference to a submitted job (``location`` is a path, a remote path, or a pid)."""

    job_id: str
    executor: str
    location: str


class Executor(ABC):
    """Where a job runs. Stage code is executor-agnostic; the executor decides where the store
    lives during the run. Subclasses register themselves in ``EXECUTOR_REGISTRY``."""

    name: ClassVar[str]

    @abstractmethod
    def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle:
        """Start (or prepare) the job."""

    @abstractmethod
    def status(self, handle: JobHandle) -> Status:
        """Current state; ``awaiting_user`` means the user must move files by hand."""

    @abstractmethod
    def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]:
        """Import the job outputs into ``store`` and return their artifact ids."""


EXECUTOR_REGISTRY: dict[str, type[Executor]] = {}


def register_executor(cls: type[Executor]) -> type[Executor]:
    """Class decorator adding an executor to ``EXECUTOR_REGISTRY`` under ``cls.name``."""
    EXECUTOR_REGISTRY[cls.name] = cls
    return cls


def executor_error(check: str, detail: str, code: ErrorCode = ErrorCode.EXECUTOR_ERROR,
                   artifact_id: str | None = None) -> StageFailure:
    """Build a ``StageFailure`` for the executors component."""
    return StageFailure(code, "executors", check, detail, artifact_id)


def job_to_dict(job: JobSpec) -> dict[str, Any]:
    """JSON-ready dict of a JobSpec (tuples become lists)."""
    return json.loads(canonical_json({
        "job_id": job.job_id, "stage_id": job.stage_id,
        "run_key": None if job.run_key is None else list(job.run_key),
        "config_hash": job.config_hash, "resolved_config": job.resolved_config,
        "input_artifact_ids": list(job.input_artifact_ids),
        "expected_output_types": list(job.expected_output_types),
        "resources": job.resources, "env_lock_hash": job.env_lock_hash}))


def job_from_dict(data: Mapping[str, Any]) -> JobSpec:
    """Inverse of :func:`job_to_dict`."""
    run_key = data.get("run_key")
    return JobSpec(
        job_id=data["job_id"], stage_id=data["stage_id"],
        run_key=None if run_key is None else tuple(run_key), config_hash=data["config_hash"],
        resolved_config=data.get("resolved_config", {}),
        input_artifact_ids=tuple(data.get("input_artifact_ids", ())),
        expected_output_types=tuple(data.get("expected_output_types", ())),
        resources=data.get("resources", {}), env_lock_hash=data.get("env_lock_hash", ""))


def local_root(store: ArtifactStore) -> Path:
    """Directory of a ``LocalFSBackend`` store; ``EXECUTOR_ERROR`` for any other backend."""
    if not isinstance(store.backend, LocalFSBackend):
        raise executor_error("backend", "executors need a LocalFSBackend store")
    return Path(store.backend.root).resolve()


def git_sha(repo_root: Path) -> str:
    """``git rev-parse HEAD`` in ``repo_root``, or ``"unknown"``."""
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True,
                             text=True, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return out.stdout.strip() or "unknown"


def default_repo_root() -> Path:
    """The repository root, found relative to this file (``src/topo_pilot/executors``)."""
    return Path(__file__).resolve().parents[3]
