"""LocalExecutor: run ``python -m topo_pilot.executors.entry`` in a subprocess."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from topo_pilot.contracts import ArtifactStore

from ._outputs import check_types, raise_if_failed
from .base import (
    Executor,
    JobHandle,
    JobSpec,
    Status,
    default_repo_root,
    executor_error,
    git_sha,
    job_to_dict,
    local_root,
    register_executor,
)
from .entry import result_path_for


def write_job_json(path: Path, job: JobSpec, *, store_root: str, repo_root: str,
                   executor: str, sha: str, stages_yaml: str = "configs/stages.yaml") -> Path:
    """Write the ``job.json`` that ``entry`` reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "job": job_to_dict(job), "store_root": store_root, "repo_root": repo_root,
        "stages_yaml": stages_yaml, "executor": executor, "git_sha": sha}, indent=1),
        encoding="utf-8")
    return path


@register_executor
class LocalExecutor(Executor):
    """Runs the job in a subprocess of the same Python environment, on the same store.

    Parameters
    ----------
    work_dir : folder for ``<job_id>/job.json`` and logs (default: a fresh temp folder).
    repo_root : repository holding ``configs/`` (default: found from this file).
    env : extra environment variables for the subprocess (e.g. ``PYTHONPATH``).
    """

    name = "local"

    def __init__(self, work_dir: Path | None = None, repo_root: Path | None = None,
                 env: Mapping[str, str] | None = None) -> None:
        self.work_dir = Path(work_dir) if work_dir else Path(tempfile.mkdtemp(prefix="tp_jobs_"))
        self.repo_root = Path(repo_root) if repo_root else default_repo_root()
        self.env = dict(env or {})
        self._procs: dict[str, subprocess.Popen] = {}
        self._jobs: dict[str, JobSpec] = {}

    def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle:
        """Start the subprocess; ``store`` must be a ``LocalFSBackend`` store."""
        root = local_root(store)
        job_json = write_job_json(self.work_dir / job.job_id / "job.json", job,
                                  store_root=str(root), repo_root=str(self.repo_root.resolve()),
                                  executor=self.name, sha=git_sha(self.repo_root))
        env = {**os.environ, **self.env}
        with open(job_json.with_name("run.log"), "wb") as log:
            try:
                self._procs[job.job_id] = subprocess.Popen(
                    [sys.executable, "-m", "topo_pilot.executors.entry", str(job_json)],
                    env=env, stdout=log, stderr=subprocess.STDOUT, cwd=self.repo_root)
            except OSError as exc:
                raise executor_error("spawn", repr(exc)) from exc
        self._jobs[job.job_id] = job
        return JobHandle(job.job_id, self.name, str(job_json))

    def _proc(self, handle: JobHandle) -> subprocess.Popen:
        if handle.job_id not in self._procs:
            raise executor_error("handle", f"unknown job {handle.job_id!r}")
        return self._procs[handle.job_id]

    def status(self, handle: JobHandle) -> Status:
        """``running`` while the subprocess lives, then ``done`` (exit 0) or ``failed``."""
        code = self._proc(handle).poll()
        if code is None:
            return "running"
        return "done" if code == 0 else "failed"

    def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]:
        """Wait for the subprocess; return the output ids (already in the shared store)."""
        proc = self._proc(handle)
        proc.wait()
        result: dict[str, Any] = {}
        result_file = result_path_for(Path(handle.location))
        if result_file.is_file():
            result = json.loads(result_file.read_text(encoding="utf-8"))
        if proc.returncode != 0 or not result.get("ok"):
            if result.get("manifest"):
                raise_if_failed(store, [result["manifest"]], handle.job_id)
            log = Path(handle.location).with_name("run.log")
            tail = log.read_text(errors="replace")[-500:] if log.is_file() else ""
            raise executor_error("job_failed",
                                 f"job {handle.job_id} exit {proc.returncode}: {tail}")
        outputs: list[str] = result["outputs"]
        check_types([store.meta(i).artifact_type for i in outputs],
                    self._jobs[handle.job_id].expected_output_types, handle.job_id)
        return outputs
