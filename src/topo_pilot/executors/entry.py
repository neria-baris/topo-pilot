"""In-bundle / subprocess entry point: ``python -m topo_pilot.executors.entry <job.json>``."""

from __future__ import annotations

import importlib
import json
import logging
import os
import platform
import shutil
import sys
import time
from pathlib import Path
from typing import Any

from topo_pilot.contracts import ArtifactStore, ErrorCode, LocalFSBackend, RunManifest, StageFailure

from .base import JobSpec, executor_error, git_sha, job_from_dict, job_to_dict

LOG = logging.getLogger("topo_pilot.executors")


def result_path_for(job_json: Path) -> Path:
    """Where ``entry`` writes its result summary (next to the job file)."""
    return job_json.with_name(job_json.stem + ".result.json")


def hardware_info() -> dict[str, Any]:
    """Host description recorded in the RunManifest (stdlib only; GPU via ``nvidia-smi``)."""
    gpu = "none"
    smi = shutil.which("nvidia-smi")
    if smi:
        import subprocess
        try:
            out = subprocess.run([smi, "--query-gpu=name", "--format=csv,noheader"],
                                 capture_output=True, text=True, timeout=20)
            gpu = out.stdout.strip().replace("\n", "; ") or "none"
        except (OSError, subprocess.SubprocessError):
            gpu = "unknown"
    return {"platform": platform.platform(), "machine": platform.machine(),
            "processor": platform.processor(), "python": platform.python_version(),
            "cpu_count": os.cpu_count() or 1, "gpu": gpu}


def _failure_dict(exc: BaseException) -> dict[str, Any]:
    if isinstance(exc, StageFailure):
        return {"code": exc.code.value, "component": exc.component, "check": exc.check,
                "detail": exc.detail, "artifact_id": exc.artifact_id}
    return {"code": ErrorCode.EXECUTOR_ERROR.value, "component": "executors", "check": "stage",
            "detail": repr(exc), "artifact_id": None}


def _dispatch(job: JobSpec, store: ArtifactStore, repo_root: Path,
              stages_yaml: Path) -> list[str]:
    for module in job.resolved_config.get("import_modules", ()):
        importlib.import_module(module)
    experiment = importlib.import_module("topo_pilot.experiment")
    registry = experiment.STAGE_REGISTRY
    if job.stage_id not in registry:
        raise executor_error("stage_id", f"stage {job.stage_id!r} is not registered "
                                         f"(available: {sorted(registry)})")
    cfg = experiment.load_config(stages_yaml, repo_root)
    return list(registry[job.stage_id]().execute(job.resolved_config, cfg, store))


def _write_manifest(store: ArtifactStore, job: JobSpec, executor: str, outputs: list[str],
                    failures: list[dict[str, Any]], started_ns: int, wall: float) -> str:
    dag = {aid: tuple(store.meta(aid).parent_ids) for aid in outputs}
    manifest = RunManifest(
        run_key="|".join(map(str, job.run_key)) if job.run_key else job.job_id,
        executor=executor, config_hash=job.config_hash or "unknown",
        config=job_to_dict(job), dag=dag, seed_bundle={},
        stage_status={job.stage_id: "failed" if failures else "ok"},
        hardware=hardware_info(), wall_time_s=wall, failures=tuple(failures))
    return store.save(manifest, config={"job_id": job.job_id, "executor": executor,
                                        "started_ns": started_ns},
                      parents=outputs, seed_map={}, consumer="executors")


def _resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def entry(job_json: Path) -> int:
    """Run the job described by ``job_json``; return 0 on success, 1 after recording a failure.

    ``job.json`` holds ``job`` (a JobSpec dict), ``store_root``, ``repo_root``, ``stages_yaml``
    (relative to ``repo_root``), and optionally ``executor`` and ``git_sha``; relative paths
    resolve against the folder of ``job.json``. The stage is looked up by name in
    ``topo_pilot.experiment.STAGE_REGISTRY`` at run time. A RunManifest (executor, hardware,
    wall time, failures) is always written, and ``<job>.result.json`` lists
    ``{"ok", "outputs", "manifest"}``.

    Raises
    ------
    StageFailure
        ``EXECUTOR_ERROR`` if ``job.json`` itself is unreadable.
    """
    job_json = Path(job_json).resolve()
    try:
        data = json.loads(job_json.read_text(encoding="utf-8"))
        job = job_from_dict(data["job"])
        base = job_json.parent
        repo_root = _resolve(base, data.get("repo_root", "."))
        store = ArtifactStore(LocalFSBackend(_resolve(base, data["store_root"])),
                              producer_version=data.get("git_sha") or git_sha(repo_root))
    except (OSError, KeyError, ValueError) as exc:
        raise executor_error("job_json", f"cannot read {job_json.name}: {exc!r}") from exc
    stages_yaml = _resolve(repo_root, data.get("stages_yaml", "configs/stages.yaml"))
    started_ns, t0 = time.time_ns(), time.perf_counter()
    outputs: list[str] = []
    failures: list[dict[str, Any]] = []
    LOG.info("job %s: stage %s", job.job_id, job.stage_id)
    try:
        outputs = _dispatch(job, store, repo_root, stages_yaml)
    except Exception as exc:  # recorded in the manifest, reported through the exit code
        LOG.error("job %s failed: %s", job.job_id, exc)
        failures.append(_failure_dict(exc))
    manifest_id = _write_manifest(store, job, str(data.get("executor", "local")), outputs,
                                  failures, started_ns, time.perf_counter() - t0)
    result_path_for(job_json).write_text(json.dumps(
        {"ok": not failures, "outputs": outputs, "manifest": manifest_id,
         "failures": failures}), encoding="utf-8")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    """CLI wrapper around :func:`entry`."""
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python -m topo_pilot.executors.entry <job.json>", file=sys.stderr)
        return 2
    try:
        return entry(Path(args[0]))
    except StageFailure as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
