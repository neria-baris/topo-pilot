"""Output checks shared by all executors: type whitelist, bundle peeking, failure lookup."""

from __future__ import annotations

import tarfile
from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, ErrorCode, RunManifest

from .base import executor_error

ALWAYS_ALLOWED = ("RunManifest",)


def check_types(types: Sequence[str], expected: Sequence[str], where: str) -> None:
    """Reject any artifact type outside ``expected`` (``RunManifest`` is always allowed)."""
    bad = sorted({t for t in types if t not in expected and t not in ALWAYS_ALLOWED})
    if bad:
        raise executor_error("output_type", f"{where}: unexpected output types {bad}; "
                                            f"expected {sorted(expected)}")


def peek_bundle_types(path: Path) -> dict[str, str]:
    """``artifact_id -> artifact_type`` read from the member names of a bundle, without writing
    anything. A damaged archive raises ``CHECKSUM_MISMATCH``."""
    found: dict[str, str] = {}
    try:
        with tarfile.open(path, mode="r:gz") as tar:
            for member in tar.getmembers():
                parts = member.name.split("/")
                if member.isfile() and parts[-1] == "meta.json" and len(parts) == 4:
                    found[parts[2]] = parts[1]
    except (tarfile.TarError, OSError, EOFError) as exc:
        raise executor_error("archive", f"unreadable bundle {path.name}: {exc!r}",
                             ErrorCode.CHECKSUM_MISMATCH) from exc
    return found


def import_outputs(store: ArtifactStore, outputs_path: Path,
                   expected: Sequence[str]) -> tuple[list[str], list[str]]:
    """Check types, then verify-and-import an outputs tarball.

    Returns ``(stage output ids, manifest ids)``. Raises ``EXECUTOR_ERROR`` for a missing file or
    an unexpected type, and (from ``ArtifactStore.import_bundle``) ``CHECKSUM_MISMATCH`` or
    ``MISSING_PARENT``.
    """
    outputs_path = Path(outputs_path)
    if not outputs_path.is_file():
        raise executor_error("outputs_missing", f"no outputs file at {outputs_path}")
    types = peek_bundle_types(outputs_path)
    check_types(list(types.values()), expected, outputs_path.name)
    ids = store.import_bundle(outputs_path)
    manifests = [i for i in ids if types.get(i) == "RunManifest"]
    return [i for i in ids if i not in manifests], manifests


def raise_if_failed(store: ArtifactStore, manifest_ids: Sequence[str], job_id: str) -> None:
    """``EXECUTOR_ERROR`` wrapping the failures recorded in the job's RunManifest(s)."""
    for mid in manifest_ids:
        manifest = store.load(RunManifest, mid, consumer="executors")
        if manifest.failures:
            first = manifest.failures[0]
            raise executor_error("job_failed", f"job {job_id} failed: [{first.get('code')}] "
                                               f"{first.get('check')}: {first.get('detail')}",
                                 artifact_id=mid)
