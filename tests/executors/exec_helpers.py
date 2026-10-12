"""Plain helpers shared by the executors tests."""

import io
import json
import tarfile
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow
from topo_pilot.executors import JobSpec


def make_store(path: Path) -> ArtifactStore:
    """A LocalFS store with a fixed producer version."""
    return ArtifactStore(LocalFSBackend(path), producer_version="test")


def seed_input(store: ArtifactStore) -> str:
    """Save the MetricRecords input (value 10.0) of the stub jobs."""
    art = MetricRecords(rows=(MetricRow("in", "world", "stub_input", 10.0),))
    return store.save(art, config={"role": "input"}, parents=[], seed_map={}, consumer="experiment")


def make_job(input_id: str, job_id: str = "j1", expected=("MetricRecords",), **extra) -> JobSpec:
    """A STUB job reading ``input_id``."""
    cfg = {"import_modules": ["stub_stage"], "value": 2.5, "input_id": input_id, **extra}
    return JobSpec(job_id=job_id, stage_id="STUB", run_key=("cylinder", "O", 1),
                   config_hash="abc123", resolved_config=cfg, input_artifact_ids=(input_id,),
                   expected_output_types=tuple(expected),
                   resources={"gpu": False, "mem_gb": 1.0, "time_h": 0.1}, env_lock_hash="lock")


def tamper_tar(src: Path, dest: Path) -> Path:
    """Copy a bundle, bumping the first metric value inside every ``extra.json`` that has rows
    (the checksum and the id inputs stay as they were)."""
    with tarfile.open(src, "r:gz") as tin, tarfile.open(dest, "w:gz") as tout:
        for member in tin.getmembers():
            data = tin.extractfile(member).read()
            if member.name.endswith("/extra.json"):
                doc = json.loads(data)
                if doc.get("rows"):
                    doc["rows"][0]["value"] += 1.0
                    data = json.dumps(doc).encode()
            member.size = len(data)
            tout.addfile(member, io.BytesIO(data))
    return dest


STUB_ENV = {"PYTHONPATH": str(Path(__file__).resolve().parent)}
