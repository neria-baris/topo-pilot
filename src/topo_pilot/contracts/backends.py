"""Bytes-level storage backends for the artifact store."""

from __future__ import annotations

import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

from .errors import ErrorCode, StageFailure


def _check_key(key: str) -> str:
    parts = key.split("/")
    if not key or key.startswith("/") or "\\" in key or any(p in ("", ".", "..") for p in parts):
        raise StageFailure(ErrorCode.INVALID_CONFIG, "contracts.ArtifactBackend", "key",
                           f"invalid storage key {key!r}")
    return key


class ArtifactBackend(ABC):
    """Flat key -> bytes storage. Keys are relative POSIX paths such as
    ``"WorldSpec/0123456789abcdef/meta.json"``; ``..``, empty and absolute segments are refused."""

    @abstractmethod
    def put(self, key: str, data: bytes) -> None:
        """Store ``data`` under ``key`` (atomically where the medium allows), replacing any value."""

    @abstractmethod
    def get(self, key: str) -> bytes:
        """Return the bytes at ``key``; raises ``ARTIFACT_MISSING`` if absent."""

    @abstractmethod
    def exists(self, key: str) -> bool:
        """True if ``key`` holds a value."""

    @abstractmethod
    def list(self, prefix: str) -> list[str]:
        """All keys starting with ``prefix``, sorted."""

    def _missing(self, key: str) -> StageFailure:
        return StageFailure(ErrorCode.ARTIFACT_MISSING, f"contracts.{type(self).__name__}", "get",
                            f"no value at key {key!r}")


class MemoryBackend(ArtifactBackend):
    """In-process dictionary backend for tests (``contracts.testing.memory_store``)."""

    def __init__(self) -> None:
        self._data: dict[str, bytes] = {}

    def put(self, key: str, data: bytes) -> None:
        self._data[_check_key(key)] = bytes(data)

    def get(self, key: str) -> bytes:
        try:
            return self._data[_check_key(key)]
        except KeyError:
            raise self._missing(key) from None

    def exists(self, key: str) -> bool:
        return _check_key(key) in self._data

    def list(self, prefix: str) -> list[str]:
        return sorted(k for k in self._data if k.startswith(prefix))


class LocalFSBackend(ArtifactBackend):
    """Files under ``root``; writes go to a temporary file and are moved into place atomically."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def _path(self, key: str) -> Path:
        return self.root.joinpath(*_check_key(key).split("/"))

    def put(self, key: str, data: bytes) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
            os.replace(tmp, path)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise

    def get(self, key: str) -> bytes:
        path = self._path(key)
        if not path.is_file():
            raise self._missing(key)
        return path.read_bytes()

    def exists(self, key: str) -> bool:
        return self._path(key).is_file()

    def list(self, prefix: str) -> list[str]:
        head = prefix.rsplit("/", 1)[0] if "/" in prefix else ""
        start = self.root.joinpath(*head.split("/")) if head else self.root
        if not start.is_dir():
            return []
        keys = (p.relative_to(self.root).as_posix() for p in start.rglob("*") if p.is_file())
        return sorted(k for k in keys if k.startswith(prefix) and "/.tmp-" not in f"/{k}")


class MirrorBackend(ArtifactBackend):
    """Writes to ``primary`` and to a ``LocalFSBackend`` at ``mirror_root`` (e.g. an external
    disk or a synced folder). Reads prefer ``primary`` and fall back to the mirror."""

    def __init__(self, primary: ArtifactBackend, mirror_root: Path) -> None:
        self.primary = primary
        self.mirror = LocalFSBackend(mirror_root)

    def put(self, key: str, data: bytes) -> None:
        self.primary.put(key, data)
        self.mirror.put(key, data)

    def get(self, key: str) -> bytes:
        if self.primary.exists(key):
            return self.primary.get(key)
        return self.mirror.get(key)

    def exists(self, key: str) -> bool:
        return self.primary.exists(key) or self.mirror.exists(key)

    def list(self, prefix: str) -> list[str]:
        return sorted(set(self.primary.list(prefix)) | set(self.mirror.list(prefix)))
