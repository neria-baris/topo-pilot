"""Deterministic artifact bundles (tar.gz) for moving artifacts between stores (internal)."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from .base import ArtifactMeta, payload_checksum
from .errors import ErrorCode, StageFailure
from .ids import make_artifact_id
from .schemas import ARTIFACT_CLASSES

if TYPE_CHECKING:
    from .store import ArtifactStore

INDEX_NAME = "bundle_index.json"
PREFIX = "artifacts/"


def _fail(code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure:
    return StageFailure(code, "contracts.bundle", check, detail, aid)


def _closure(store: ArtifactStore, ids: Sequence[str], with_parents: bool) -> list[str]:
    """Ids in dependency order (parents first)."""
    order: list[str] = []
    seen: set[str] = set()

    def visit(aid: str) -> None:
        if aid in seen:
            return
        seen.add(aid)
        meta = store.meta(aid)
        if with_parents:
            for pid in meta.parent_ids:
                visit(pid)
        order.append(aid)

    for aid in sorted(set(ids)):
        visit(aid)
    return order


def export_bundle(store: ArtifactStore, ids: Sequence[str], dest: Path, with_parents: bool) -> Path:
    """Tar every file of the selected artifacts under ``artifacts/<type>/<id>/`` plus an index.
    Entries are sorted and carry zero mtimes, so equal content gives byte-identical bundles."""
    order = _closure(store, ids, with_parents)
    files: dict[str, bytes] = {}
    for aid in order:
        meta = store.meta(aid)
        if meta.status != "complete":
            raise _fail(ErrorCode.ARTIFACT_MISSING, "incomplete", "cannot export", aid)
        for key in store.backend.list(f"{meta.artifact_type}/{aid}/"):
            files[PREFIX + key] = store.backend.get(key)
    files[INDEX_NAME] = json.dumps({"ids": order}, sort_keys=True).encode("utf-8")
    if dest.suffixes[-2:] != [".tar", ".gz"]:
        digest = hashlib.sha256("\n".join(order).encode()).hexdigest()[:16]
        dest = dest / f"artifacts_{digest}.tar.gz"
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for name in sorted(files):
            info = tarfile.TarInfo(name)
            info.size, info.mtime, info.mode = len(files[name]), 0, 0o644
            tar.addfile(info, io.BytesIO(files[name]))
    with open(dest, "wb") as handle, gzip.GzipFile(filename="", fileobj=handle, mode="wb", mtime=0) as gz:
        gz.write(raw.getvalue())
    return dest


def _read_members(src: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    try:
        with tarfile.open(src, mode="r:gz") as tar:
            for member in tar.getmembers():
                name = member.name
                if not member.isfile() or name.startswith("/") or ".." in name.split("/"):
                    raise _fail(ErrorCode.CHECKSUM_MISMATCH, "member", f"unsafe member {name!r}")
                handle = tar.extractfile(member)
                files[name] = handle.read() if handle else b""
    except (tarfile.TarError, OSError, EOFError) as exc:
        raise _fail(ErrorCode.CHECKSUM_MISMATCH, "archive", f"unreadable bundle: {exc!r}") from exc
    return files


def import_bundle(store: ArtifactStore, src: Path) -> list[str]:
    """Verify everything first, then write in dependency order; see ``ArtifactStore.import_bundle``."""
    files = _read_members(src)
    if INDEX_NAME not in files:
        raise _fail(ErrorCode.ARTIFACT_MISSING, "index", f"{INDEX_NAME} missing")
    order = json.loads(files[INDEX_NAME])["ids"]
    groups: dict[str, dict[str, bytes]] = {}
    metas: dict[str, ArtifactMeta] = {}
    for name, data in files.items():
        if name == INDEX_NAME:
            continue
        atype, aid, fname = name[len(PREFIX):].split("/", 2)
        groups.setdefault(aid, {})[fname] = data
        if fname == "meta.json":
            metas[aid] = ArtifactMeta.from_json_dict(json.loads(data))
    if sorted(metas) != sorted(order) or set(groups) != set(metas):
        raise _fail(ErrorCode.CHECKSUM_MISMATCH, "index", "index does not match the archive")
    for aid in order:
        _verify_one(store, metas[aid], groups[aid], set(order))
    imported = []
    for aid in order:
        meta = metas[aid]
        if store._is_complete(aid):
            if store.meta(aid).payload_sha256 != meta.payload_sha256:
                raise _fail(ErrorCode.CHECKSUM_MISMATCH, "existing", "differs from stored", aid)
        else:
            files_ = {k: v for k, v in groups[aid].items() if k != "meta.json"}
            store._write(meta, files_)
        imported.append(aid)
    return imported


def _verify_one(store: ArtifactStore, meta: ArtifactMeta, group: dict[str, bytes],
                bundle_ids: set[str]) -> None:
    aid = meta.artifact_id
    if meta.artifact_type not in ARTIFACT_CLASSES or meta.status != "complete":
        raise _fail(ErrorCode.CHECKSUM_MISMATCH, "meta", f"bad type/status {meta.artifact_type}", aid)
    store._check_version(meta)
    if make_artifact_id(meta.artifact_type, meta.config, meta.parent_ids,
                        meta.schema_version) != aid:
        raise _fail(ErrorCode.CHECKSUM_MISMATCH, "artifact_id", "id does not recompute", aid)
    for pid in meta.parent_ids:
        if pid not in bundle_ids and not store._is_complete(pid):
            raise _fail(ErrorCode.MISSING_PARENT, "parents", f"parent {pid} missing", aid)
    cls = ARTIFACT_CLASSES[meta.artifact_type]
    try:
        with np.load(io.BytesIO(group["payload.npz"]), allow_pickle=False) as npz:
            arrays: dict = {k: npz[k] for k in npz.files}
        extra = json.loads(group["extra.json"])
        for field_name, file_name in cls.BLOB_FILES.items():
            arrays[field_name] = group[file_name]
    except Exception as exc:
        raise _fail(ErrorCode.CHECKSUM_MISMATCH, "payload_read", repr(exc), aid) from exc
    if payload_checksum(arrays, extra) != meta.payload_sha256:
        raise _fail(ErrorCode.CHECKSUM_MISMATCH, "payload_sha256", "payload was modified", aid)
    cls.from_payload(arrays, extra).validate()
