"""Artifact envelope (``ArtifactMeta``) and the ``Artifact`` base class with generic serialisation."""

from __future__ import annotations

import dataclasses
import hashlib
import types
import typing
from abc import ABC
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar, TypeVar

import numpy as np

from .errors import ErrorCode, StageFailure
from .ids import _normalise, canonical_json

A = TypeVar("A", bound="Artifact")

META_STATUSES = ("complete", "incomplete")


@dataclass(frozen=True)
class ArtifactMeta:
    """Envelope stored as ``meta.json`` next to every payload (DATA_SCHEMAS §1).

    ``artifact_id = make_artifact_id(artifact_type, config, parent_ids, schema_version)``;
    ``created_utc`` is informational and never part of the identity. ``payload_sha256`` is the
    canonical content checksum computed by the store (array names, dtypes, shapes and bytes,
    the JSON extra, and any blobs), so it does not depend on zip timestamps.
    """

    artifact_type: str
    artifact_id: str
    schema_version: str
    parent_ids: tuple[str, ...]
    config: Mapping[str, Any]
    seed_map: Mapping[str, int]
    producer_version: str
    created_utc: str
    shapes: Mapping[str, tuple[int, ...]]
    dtypes: Mapping[str, str]
    payload_sha256: str
    status: str = "incomplete"
    consumer: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        """Plain-JSON form for ``meta.json``."""
        return _normalise(dataclasses.asdict(self))

    @classmethod
    def from_json_dict(cls, data: Mapping[str, Any]) -> ArtifactMeta:
        """Inverse of :meth:`to_json_dict`; unknown keys are ignored (forward compatibility)."""
        names = {f.name for f in dataclasses.fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in names}
        kwargs["parent_ids"] = tuple(kwargs.get("parent_ids", ()))
        kwargs["shapes"] = {k: tuple(v) for k, v in kwargs.get("shapes", {}).items()}
        return cls(**kwargs)


def _coerce(value: Any, hint: Any) -> Any:
    """Convert a JSON-decoded value back to the type named by a dataclass field hint."""
    if value is None or hint is Any:
        return value
    origin = typing.get_origin(hint)
    args = typing.get_args(hint)
    if origin in (typing.Union, types.UnionType):
        for option in (a for a in args if a is not type(None)):
            try:
                return _coerce(value, option)
            except (TypeError, ValueError):
                continue
        return value
    if origin is tuple:
        items = list(value)
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(_coerce(v, args[0]) for v in items)
        if args:
            return tuple(_coerce(v, a) for v, a in zip(items, args))
        return tuple(items)
    if origin in (dict, Mapping, typing.Mapping) or hint in (dict, Mapping):
        key_t, val_t = args if args else (Any, Any)
        return {_coerce(k, key_t) if key_t is not str else k: _coerce(v, val_t)
                for k, v in value.items()}
    if origin is list:
        return [_coerce(v, args[0]) if args else v for v in value]
    if hint is int and not isinstance(value, bool):
        return int(value)
    if hint is float:
        return float(value)
    if dataclasses.is_dataclass(hint) and isinstance(value, Mapping):
        sub = typing.get_type_hints(hint)
        return hint(**{k: _coerce(v, sub.get(k, Any)) for k, v in value.items()})
    return value


class Artifact(ABC):
    """Base of every typed artifact (each subclass is a frozen dataclass).

    Serialisation is generic and driven by the dataclass fields:

    - ``np.ndarray`` fields go to the ``.npz`` payload (no pickle; ``allow_pickle=False``);
    - ``bytes`` fields are opaque blobs stored as separate files named by ``BLOB_FILES``
      (e.g. ``Checkpoint.state -> "state.pt"``);
    - ``dict[int, np.ndarray]`` fields listed in ``ARRAY_DICT_FIELDS`` are stored as arrays
      named ``"<field>__<key>"``;
    - every other field goes to the JSON ``extra`` and is coerced back by its type hint
      (so tuples survive the round trip).

    Subclasses implement :meth:`validate`, raising :class:`StageFailure`.
    """

    ARTIFACT_TYPE: ClassVar[str] = ""
    BLOB_FILES: ClassVar[Mapping[str, str]] = {}
    ARRAY_DICT_FIELDS: ClassVar[tuple[str, ...]] = ()

    def validate(self) -> None:
        """Check every invariant of this artifact. Raises ``StageFailure``."""

    def _fail(self, code: ErrorCode, check: str, detail: str) -> StageFailure:
        return StageFailure(code, f"contracts.{type(self).__name__}", check, detail)

    def to_payload(self) -> tuple[dict[str, np.ndarray | bytes], dict[str, Any]]:
        """Split the artifact into ``(arrays, extra)``; blob fields appear in ``arrays`` as bytes."""
        arrays: dict[str, np.ndarray | bytes] = {}
        extra: dict[str, Any] = {}
        for f in dataclasses.fields(self):  # type: ignore[arg-type]
            value = getattr(self, f.name)
            if f.name in self.ARRAY_DICT_FIELDS:
                extra[f.name] = sorted(int(k) for k in value)
                for key, arr in value.items():
                    arrays[f"{f.name}__{int(key)}"] = np.asarray(arr)
            elif isinstance(value, np.ndarray):
                arrays[f.name] = value
            elif isinstance(value, (bytes, bytearray)):
                arrays[f.name] = bytes(value)
            else:
                extra[f.name] = _normalise(value)
        return arrays, extra

    @classmethod
    def from_payload(cls: type[A], arrays: Mapping[str, np.ndarray | bytes],
                     extra: Mapping[str, Any]) -> A:
        """Inverse of :meth:`to_payload`."""
        hints = typing.get_type_hints(cls)
        kwargs: dict[str, Any] = {}
        for f in dataclasses.fields(cls):  # type: ignore[arg-type]
            if f.name in cls.ARRAY_DICT_FIELDS:
                kwargs[f.name] = {int(k): arrays[f"{f.name}__{int(k)}"] for k in extra[f.name]}
            elif f.name in arrays:
                kwargs[f.name] = arrays[f.name]
            elif f.name in extra:
                kwargs[f.name] = _coerce(extra[f.name], hints.get(f.name, Any))
        return cls(**kwargs)


def array_field() -> Any:
    """A dataclass field holding an array (excluded from ``__eq__``/``__repr__``)."""
    return field(compare=False, repr=False)


def optional_array_field() -> Any:
    """An optional array field defaulting to ``None``."""
    return field(default=None, compare=False, repr=False)


def payload_checksum(arrays: Mapping[str, np.ndarray | bytes], extra: Mapping[str, Any]) -> str:
    """Canonical content checksum: sha256 over, for each array or blob in name order, its name,
    dtype, shape and raw C-order bytes; then ``canonical_json(extra)``. Independent of file
    container details (zip timestamps), so identical content always gives the same checksum."""
    h = hashlib.sha256()
    for name in sorted(arrays):
        value = arrays[name]
        if isinstance(value, (bytes, bytearray)):
            h.update(f"blob:{name}:{len(value)}\n".encode())
            h.update(bytes(value))
        else:
            arr = np.ascontiguousarray(value)
            h.update(f"array:{name}:{arr.dtype.str}:{list(arr.shape)}\n".encode())
            h.update(arr.tobytes())
    h.update(b"extra:" + canonical_json(extra).encode("utf-8"))
    return h.hexdigest()
