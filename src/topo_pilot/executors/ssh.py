"""SSHExecutor: the same bundle, copied and run with the system ``ssh`` and ``scp``."""

from __future__ import annotations

import logging
import shlex
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from topo_pilot.contracts import ArtifactStore

from ._outputs import import_outputs, raise_if_failed
from .base import (
    Executor,
    JobHandle,
    JobSpec,
    Status,
    default_repo_root,
    executor_error,
    register_executor,
)
from .bundle import build_bundle

LOG = logging.getLogger("topo_pilot.executors")


@register_executor
class SSHExecutor(Executor):
    """Runs a bundle on a reachable machine. Credentials come from the user's SSH config
    (``~/.ssh/config``, agent); nothing secret is read from or written to the repository.

    Parameters
    ----------
    local : the ``local`` mapping of the resolved config (``configs/local.yaml``), holding
        ``ssh: {host, user, remote_dir, python, install}``. ``user`` and ``python``
        (default ``python3``) are optional; ``install: false`` passes ``--no-install``.
    out_dir : where the bundle is built and the outputs are downloaded (default ``./bundles``).
    repo_root : repository to pack (default: found from this file).
    """

    name = "ssh"

    def __init__(self, local: Mapping[str, Any], out_dir: Path | None = None,
                 repo_root: Path | None = None) -> None:
        cfg = (local or {}).get("ssh") or {}
        missing = [k for k in ("host", "remote_dir") if not cfg.get(k)]
        if missing:
            raise executor_error("ssh_config", f"configs/local.yaml ssh: missing {missing}")
        self.host = str(cfg["host"])
        self.user = cfg.get("user")
        self.remote_dir = str(cfg["remote_dir"]).rstrip("/")
        self.python = str(cfg.get("python", "python3"))
        self.install = bool(cfg.get("install", True))
        self.out_dir = Path(out_dir) if out_dir else Path("bundles")
        self.repo_root = Path(repo_root) if repo_root else default_repo_root()
        self._jobs: dict[str, JobSpec] = {}

    @property
    def target(self) -> str:
        """``user@host`` or ``host``."""
        return f"{self.user}@{self.host}" if self.user else self.host

    def _remote_job_dir(self, job_id: str) -> str:
        return f"{self.remote_dir}/bundle_{job_id}"

    # ---- command lines (pure; unit-tested without a network) -------------------------------
    def upload_cmd(self, bundle: Path) -> list[str]:
        """``scp`` of the bundle into ``remote_dir``."""
        return ["scp", str(bundle), f"{self.target}:{self.remote_dir}/"]

    def run_cmd(self, job_id: str) -> list[str]:
        """``ssh`` command that unpacks the bundle and starts ``run_bundle.py`` detached;
        the exit code lands in ``exit_code`` and the log in ``run.log``."""
        flag = "" if self.install else " --no-install"
        inner = f"{shlex.quote(self.python)} run_bundle.py{flag}; echo $? > exit_code"
        script = (f"mkdir -p {shlex.quote(self.remote_dir)} && cd {shlex.quote(self.remote_dir)} "
                  f"&& tar xzf bundle_{job_id}.tar.gz && cd bundle_{job_id} && rm -f exit_code "
                  f"&& (nohup sh -c {shlex.quote(inner)} > run.log 2>&1 &)")
        return ["ssh", self.target, script]

    def status_cmd(self, job_id: str) -> list[str]:
        """``ssh`` command printing the exit code, or ``running``."""
        path = shlex.quote(f"{self._remote_job_dir(job_id)}/exit_code")
        return ["ssh", self.target, f"if [ -f {path} ]; then cat {path}; else echo running; fi"]

    def download_cmd(self, job_id: str, dest: Path) -> list[str]:
        """``scp`` of ``outputs_<job>.tar.gz`` back to ``dest``."""
        remote = f"{self._remote_job_dir(job_id)}/outputs_{job_id}.tar.gz"
        return ["scp", f"{self.target}:{remote}", str(dest)]

    # ---- Executor API ---------------------------------------------------------------------
    def _exec(self, cmd: Sequence[str]) -> str:
        try:
            proc = subprocess.run(list(cmd), capture_output=True, text=True, timeout=3600)
        except (OSError, subprocess.SubprocessError) as exc:
            raise executor_error("ssh", f"{cmd[0]} failed: {exc!r}") from exc
        if proc.returncode != 0:
            raise executor_error("ssh", f"{cmd[0]} exit {proc.returncode}: {proc.stderr[-300:]}")
        return proc.stdout

    def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle:
        """Build the bundle, copy it over, and start it remotely."""
        bundle = build_bundle(job, store, self.repo_root, self.out_dir)
        self._exec(["ssh", self.target, f"mkdir -p {shlex.quote(self.remote_dir)}"])
        self._exec(self.upload_cmd(bundle))
        self._exec(self.run_cmd(job.job_id))
        self._jobs[job.job_id] = job
        LOG.info("job %s started on %s", job.job_id, self.target)
        return JobHandle(job.job_id, self.name, f"{self.target}:{self._remote_job_dir(job.job_id)}")

    def status(self, handle: JobHandle) -> Status:
        """``running`` until the remote ``exit_code`` file exists, then ``done`` or ``failed``."""
        out = self._exec(self.status_cmd(handle.job_id)).strip()
        if out == "running":
            return "running"
        return "done" if out == "0" else "failed"

    def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]:
        """Download the outputs and import them (same checks as ``BundleExecutor``)."""
        job = self._jobs.get(handle.job_id)
        if job is None:
            raise executor_error("handle", f"unknown job {handle.job_id!r}")
        self.out_dir.mkdir(parents=True, exist_ok=True)
        dest = self.out_dir / f"outputs_{handle.job_id}.tar.gz"
        self._exec(self.download_cmd(handle.job_id, dest))
        outputs, manifests = import_outputs(store, dest, job.expected_output_types)
        raise_if_failed(store, manifests, handle.job_id)
        return outputs
