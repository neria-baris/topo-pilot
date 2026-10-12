"""BundleExecutor: a self-contained ``bundle_<job>.tar.gz`` to run on any machine."""

from __future__ import annotations

import fnmatch
import logging
import tarfile
import tempfile
from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore

from ._outputs import import_outputs, raise_if_failed
from .base import (
    Executor,
    JobHandle,
    JobSpec,
    Status,
    default_repo_root,
    executor_error,
    git_sha,
    register_executor,
)
from .local import write_job_json

LOG = logging.getLogger("topo_pilot.executors")

SOURCE_ENTRIES = ("src", "pyproject.toml", "requirements.lock", "configs")
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".ipynb_checkpoints"}
SKIP_SUFFIXES = (".pyc", ".pyo")
SECRET_GLOBS = ("*key*", "*token*")
SECRET_NAMES = ("local.yaml", ".env")


def is_forbidden(name: str) -> bool:
    """True for ``local.yaml``, ``.env`` (and ``.env.*``) and anything matching ``*key*`` or
    ``*token*`` (case-insensitive)."""
    low = name.lower()
    return (low in SECRET_NAMES or low.startswith(".env.")
            or any(fnmatch.fnmatch(low, pat) for pat in SECRET_GLOBS))


def _skip(path: Path) -> bool:
    return (any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.parts)
            or path.suffix in SKIP_SUFFIXES or is_forbidden(path.name))


def collect_files(repo_root: Path, extra_files: Sequence[Path] = ()) -> dict[str, Path]:
    """``bundle-relative posix path -> file`` for the source tree.

    Secrets found while walking the tree are left out. An explicit request for one
    (``extra_files``) raises ``EXECUTOR_ERROR``.
    """
    files: dict[str, Path] = {}
    for entry in SOURCE_ENTRIES:
        path = repo_root / entry
        if path.is_file():
            files[entry] = path
        elif path.is_dir():
            for sub in sorted(path.rglob("*")):
                rel = sub.relative_to(repo_root)
                if sub.is_file() and not _skip(rel):
                    files[rel.as_posix()] = sub
    for extra in extra_files:
        extra = Path(extra)
        if any(is_forbidden(part) for part in extra.parts):
            raise executor_error("secret_file", f"refusing to bundle secret file {extra.name!r}")
        files[extra.as_posix()] = repo_root / extra
    return files


def build_bundle(job: JobSpec, store: ArtifactStore, repo_root: Path, out_dir: Path,
                 extra_files: Sequence[Path] = ()) -> Path:
    """Write ``out_dir/bundle_<job_id>.tar.gz`` (layout in docs/EXECUTION.md §3).

    The archive holds ``bundle_<job_id>/{src, pyproject.toml, requirements.lock, configs,
    inputs.tar.gz, job.json, run_bundle.py}``. ``inputs.tar.gz`` is
    ``store.export_bundle(job.input_artifact_ids, with_parents=True)``.
    """
    files = collect_files(Path(repo_root), extra_files)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    top = f"bundle_{job.job_id}"
    dest = out_dir / f"{top}.tar.gz"
    with tempfile.TemporaryDirectory(prefix="tp_bundle_") as tmp:
        tmp_path = Path(tmp)
        inputs = store.export_bundle(list(job.input_artifact_ids), tmp_path / "inputs.tar.gz",
                                     with_parents=True)
        job_json = write_job_json(tmp_path / "job.json", job, store_root="work/store",
                                  repo_root=".", executor="bundle", sha=git_sha(repo_root))
        script = Path(__file__).with_name("run_bundle_script.py")
        with tarfile.open(dest, "w:gz") as tar:
            for rel, path in files.items():
                tar.add(path, arcname=f"{top}/{rel}", recursive=False)
            tar.add(inputs, arcname=f"{top}/inputs.tar.gz")
            tar.add(job_json, arcname=f"{top}/job.json")
            tar.add(script, arcname=f"{top}/run_bundle.py")
    return dest


@register_executor
class BundleExecutor(Executor):
    """Packs the job for a machine the user operates by hand (Colab, Kaggle, a rented GPU).

    ``submit`` writes the bundle and the state becomes ``awaiting_user``; ``fetch`` imports
    ``outputs_<job>.tar.gz`` (verifying checksums, ids and parents) and the state becomes ``done``.

    Parameters
    ----------
    out_dir : where bundles are written and outputs are looked for (default ``./bundles``).
    repo_root : repository to pack (default: found from this file).
    extra_files : repo-relative files to add; secrets raise ``EXECUTOR_ERROR``.
    """

    name = "bundle"

    def __init__(self, out_dir: Path | None = None, repo_root: Path | None = None,
                 extra_files: Sequence[Path] = ()) -> None:
        self.out_dir = Path(out_dir) if out_dir else Path("bundles")
        self.repo_root = Path(repo_root) if repo_root else default_repo_root()
        self.extra_files = tuple(extra_files)
        self._state: dict[str, Status] = {}
        self._jobs: dict[str, JobSpec] = {}

    def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle:
        """Write the bundle; the job is then ``awaiting_user``."""
        path = build_bundle(job, store, self.repo_root, self.out_dir, self.extra_files)
        self._state[job.job_id] = "awaiting_user"
        self._jobs[job.job_id] = job
        handle = JobHandle(job.job_id, self.name, str(path))
        LOG.info("%s", self.instructions(handle))
        return handle

    def instructions(self, handle: JobHandle) -> str:
        """What the user must upload, run and download."""
        bundle = Path(handle.location)
        return (f"Upload {bundle.name} to the remote machine, then run there: "
                f"tar xzf {bundle.name} && cd bundle_{handle.job_id} && python run_bundle.py "
                f"(add --no-install if the environment is ready). Download "
                f"outputs_{handle.job_id}.tar.gz and call fetch(handle, store, "
                f"outputs_path=<that file>).")

    def status(self, handle: JobHandle) -> Status:
        """``awaiting_user`` after submit, ``done`` after a successful fetch."""
        if handle.job_id not in self._state:
            raise executor_error("handle", f"unknown job {handle.job_id!r}")
        return self._state[handle.job_id]

    def fetch(self, handle: JobHandle, store: ArtifactStore,
              outputs_path: Path | None = None) -> list[str]:
        """Import the outputs tarball; returns the stage output ids (the RunManifest is imported
        too). Raises ``CHECKSUM_MISMATCH``, ``MISSING_PARENT`` or ``EXECUTOR_ERROR`` (unexpected
        output type, missing file, or a job that recorded a failure)."""
        job = self._jobs.get(handle.job_id)
        if job is None:
            raise executor_error("handle", f"unknown job {handle.job_id!r}")
        path = Path(outputs_path) if outputs_path else (
            Path(handle.location).with_name(f"outputs_{handle.job_id}.tar.gz"))
        outputs, manifests = import_outputs(store, path, job.expected_output_types)
        try:
            raise_if_failed(store, manifests, handle.job_id)
        except Exception:
            self._state[handle.job_id] = "failed"
            raise
        self._state[handle.job_id] = "done"
        return outputs
