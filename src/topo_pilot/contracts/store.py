"""Content-addressed artifact store with an access policy (DATA_SCHEMAS §1, §7)."""

from __future__ import annotations

import io
import json
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypeVar

import numpy as np

from . import _bundle
from .backends import ArtifactBackend
from .base import Artifact, ArtifactMeta, payload_checksum
from .errors import ErrorCode, StageFailure
from .ids import SCHEMA_VERSION, canonical_json, make_artifact_id
from .schemas import ARTIFACT_CLASSES

A = TypeVar("A", bound=Artifact)

MODULES = frozenset({"contracts", "world", "process", "dataset", "oracle", "learner",
                     "activations", "prediction", "topology", "analysis", "experiment",
                     "executors"})

_SPEC_READERS = frozenset({"process", "dataset", "oracle", "analysis", "experiment"})


class AccessPolicy:
    """Which consumers may load which artifact types.

    Parameters
    ----------
    rules : mapping artifact_type -> frozenset of allowed consumer names. Types without a rule
        are readable by every consumer.
    """

    def __init__(self, rules: Mapping[str, frozenset[str]]) -> None:
        self.rules = {k: frozenset(v) for k, v in rules.items()}

    def check(self, artifact_type: str, consumer: str) -> None:
        """Raise ``LEAKAGE`` if ``consumer`` may not load ``artifact_type``."""
        allowed = self.rules.get(artifact_type)
        if allowed is not None and consumer not in allowed:
            raise StageFailure(ErrorCode.LEAKAGE, "contracts.AccessPolicy", "check",
                               f"consumer {consumer!r} may not load {artifact_type}")


DEFAULT_ACCESS_POLICY = AccessPolicy({
    "EvalSidecar": frozenset({"analysis", "prediction", "experiment"}),
    "WorldSpec": _SPEC_READERS,
    "TransitionSpec": _SPEC_READERS,
    "EmissionSpec": _SPEC_READERS,
    "ObservationSet": MODULES - {"world"},
    "Checkpoint": frozenset({"learner", "activations", "experiment"}),
})


class ArtifactStore:
    """Typed, content-addressed, immutable artifact storage.

    Layout: ``<ArtifactType>/<artifact_id>/{meta.json, payload.npz, extra.json, <blob files>}``.
    Writes are ordered meta(incomplete) -> payload -> meta(complete), so an interrupted write
    leaves ``status = incomplete``, which ``load`` refuses.

    Parameters
    ----------
    backend : bytes storage.
    policy : access policy applied on ``load``.
    producer_version : recorded in every meta (the caller passes the git SHA + dirty flag).
    """

    def __init__(self, backend: ArtifactBackend, policy: AccessPolicy = DEFAULT_ACCESS_POLICY,
                 producer_version: str = "unknown") -> None:
        self.backend = backend
        self.policy = policy
        self.producer_version = producer_version

    # ---- keys -----------------------------------------------------------------------------
    @staticmethod
    def _key(artifact_type: str, artifact_id: str, name: str) -> str:
        return f"{artifact_type}/{artifact_id}/{name}"

    def _fail(self, code: ErrorCode, check: str, detail: str,
              aid: str | None = None) -> StageFailure:
        return StageFailure(code, "contracts.ArtifactStore", check, detail, aid)

    # ---- write ----------------------------------------------------------------------------
    def save(self, artifact: Artifact, *, config: Mapping[str, Any], parents: Sequence[str],
             seed_map: Mapping[str, int], consumer: str) -> str:
        """Validate, derive the id, and write; idempotent for identical content.

        Raises ``MISSING_PARENT`` if a parent is not stored, and ``CHECKSUM_MISMATCH`` if the id
        exists with different (or tampered) content.
        """
        artifact.validate()
        atype = artifact.ARTIFACT_TYPE
        cfg = json.loads(canonical_json(config))
        parent_ids = tuple(sorted(set(parents)))
        for pid in parent_ids:
            if not self._is_complete(pid):
                raise self._fail(ErrorCode.MISSING_PARENT, "parents", f"parent {pid} not stored")
        aid = make_artifact_id(atype, cfg, parent_ids)
        arrays, extra = artifact.to_payload()
        checksum = payload_checksum(arrays, extra)
        if self.backend.exists(self._key(atype, aid, "meta.json")):
            old = self._read_meta(atype, aid)
            if old.status == "complete":
                self._verify_stored(old)
                if old.payload_sha256 != checksum:
                    raise self._fail(ErrorCode.CHECKSUM_MISMATCH, "save",
                                     "same id, different content", aid)
                return aid
        meta = ArtifactMeta(
            artifact_type=atype, artifact_id=aid, schema_version=SCHEMA_VERSION,
            parent_ids=parent_ids, config=cfg, seed_map=dict(seed_map),
            producer_version=self.producer_version,
            created_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            shapes={k: tuple(v.shape) for k, v in arrays.items() if isinstance(v, np.ndarray)},
            dtypes={k: v.dtype.str for k, v in arrays.items() if isinstance(v, np.ndarray)},
            payload_sha256=checksum, status="incomplete", consumer=consumer)
        self._write(meta, self._encode_files(artifact, arrays, extra))
        return aid

    def _encode_files(self, artifact: Artifact, arrays: Mapping[str, np.ndarray | bytes],
                      extra: Mapping[str, Any]) -> dict[str, bytes]:
        files: dict[str, bytes] = {"extra.json": canonical_json(extra).encode("utf-8")}
        plain = {k: v for k, v in arrays.items() if isinstance(v, np.ndarray)}
        if any(v.dtype.hasobject for v in plain.values()):
            raise self._fail(ErrorCode.INVALID_CONFIG, "object_arrays", "object arrays not allowed")
        buf = io.BytesIO()
        np.savez(buf, **plain)
        files["payload.npz"] = buf.getvalue()
        for name, blob in arrays.items():
            if isinstance(blob, (bytes, bytearray)):
                files[artifact.BLOB_FILES.get(name, f"{name}.bin")] = bytes(blob)
        return files

    def _write(self, meta: ArtifactMeta, files: Mapping[str, bytes]) -> None:
        def put_meta(status: str) -> None:
            data = dict(meta.to_json_dict(), status=status)
            self.backend.put(self._key(meta.artifact_type, meta.artifact_id, "meta.json"),
                             json.dumps(data, sort_keys=True, indent=1).encode("utf-8"))
        put_meta("incomplete")
        for name, data in files.items():
            self.backend.put(self._key(meta.artifact_type, meta.artifact_id, name), data)
        put_meta("complete")

    # ---- read -----------------------------------------------------------------------------
    def _read_meta(self, atype: str, aid: str) -> ArtifactMeta:
        key = self._key(atype, aid, "meta.json")
        if not self.backend.exists(key):
            raise self._fail(ErrorCode.ARTIFACT_MISSING, "meta", f"no {atype} {aid}", aid)
        return ArtifactMeta.from_json_dict(json.loads(self.backend.get(key)))

    def _read_files(self, meta: ArtifactMeta) -> tuple[dict[str, np.ndarray | bytes], dict]:
        atype, aid = meta.artifact_type, meta.artifact_id
        cls = ARTIFACT_CLASSES[atype]
        try:
            with np.load(io.BytesIO(self.backend.get(self._key(atype, aid, "payload.npz"))),
                         allow_pickle=False) as npz:
                arrays: dict[str, np.ndarray | bytes] = {k: npz[k] for k in npz.files}
            extra = json.loads(self.backend.get(self._key(atype, aid, "extra.json")))
        except StageFailure:
            raise
        except Exception as exc:  # corrupt container: treat as tampered content
            raise self._fail(ErrorCode.CHECKSUM_MISMATCH, "payload_read", repr(exc), aid) from exc
        for field_name, file_name in cls.BLOB_FILES.items():
            arrays[field_name] = self.backend.get(self._key(atype, aid, file_name))
        return arrays, extra

    def _verify_stored(self, meta: ArtifactMeta) -> tuple[dict[str, np.ndarray | bytes], dict]:
        arrays, extra = self._read_files(meta)
        if payload_checksum(arrays, extra) != meta.payload_sha256:
            raise self._fail(ErrorCode.CHECKSUM_MISMATCH, "payload_sha256",
                             "stored payload does not match its checksum", meta.artifact_id)
        return arrays, extra

    def _check_version(self, meta: ArtifactMeta) -> None:
        if meta.schema_version.split(".")[0] != SCHEMA_VERSION.split(".")[0]:
            raise self._fail(ErrorCode.SCHEMA_VERSION_MISMATCH, "schema_version",
                             f"{meta.schema_version} vs {SCHEMA_VERSION}", meta.artifact_id)

    def load(self, cls: type[A], artifact_id: str, *, consumer: str) -> A:
        """Load and re-validate an artifact. Order of checks: access policy (``LEAKAGE``),
        existence (``ARTIFACT_MISSING``), completeness (``ARTIFACT_MISSING``, check
        ``incomplete``), major schema version (``SCHEMA_VERSION_MISMATCH``), checksum
        (``CHECKSUM_MISMATCH``), then ``validate()``."""
        self.policy.check(cls.ARTIFACT_TYPE, consumer)
        meta = self._read_meta(cls.ARTIFACT_TYPE, artifact_id)
        if meta.status != "complete":
            raise self._fail(ErrorCode.ARTIFACT_MISSING, "incomplete",
                             "artifact write was not completed", artifact_id)
        self._check_version(meta)
        arrays, extra = self._verify_stored(meta)
        artifact = cls.from_payload(arrays, extra)
        artifact.validate()
        return artifact

    def meta(self, artifact_id: str) -> ArtifactMeta:
        """The envelope of any stored artifact (no access check: metadata is not privileged)."""
        for atype in ARTIFACT_CLASSES:
            if self.backend.exists(self._key(atype, artifact_id, "meta.json")):
                return self._read_meta(atype, artifact_id)
        raise self._fail(ErrorCode.ARTIFACT_MISSING, "meta", f"unknown id {artifact_id}",
                         artifact_id)

    def _is_complete(self, artifact_id: str) -> bool:
        try:
            return self.meta(artifact_id).status == "complete"
        except StageFailure:
            return False

    def find(self, cls: type[Artifact], **config_filter: Any) -> list[str]:
        """Ids (sorted) of complete artifacts of ``cls`` whose top-level config entries equal
        ``config_filter`` (compared in canonical JSON form)."""
        want = {k: canonical_json(v) for k, v in config_filter.items()}
        found = []
        for key in self.backend.list(f"{cls.ARTIFACT_TYPE}/"):
            if not key.endswith("/meta.json"):
                continue
            meta = ArtifactMeta.from_json_dict(json.loads(self.backend.get(key)))
            if meta.status == "complete" and all(
                    k in meta.config and canonical_json(meta.config[k]) == v
                    for k, v in want.items()):
                found.append(meta.artifact_id)
        return sorted(found)

    # ---- bundles --------------------------------------------------------------------------
    def export_bundle(self, ids: Sequence[str], dest: Path, *, with_parents: bool = True) -> Path:
        """Write a deterministic ``.tar.gz`` holding ``ids`` (and, by default, all ancestors)."""
        return _bundle.export_bundle(self, ids, Path(dest), with_parents)

    def import_bundle(self, src: Path) -> list[str]:
        """Import a bundle; verifies schema versions, ids, checksums and parents first
        (``SCHEMA_VERSION_MISMATCH``, ``CHECKSUM_MISMATCH``, ``MISSING_PARENT``). Returns the
        imported ids in dependency order. Already-present identical artifacts are skipped."""
        return _bundle.import_bundle(self, Path(src))
