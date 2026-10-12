"""Canonical JSON, content-addressed artifact ids, history ids, and the seed tree."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Any

import numpy as np

from .errors import ErrorCode, StageFailure

SCHEMA_VERSION: str = "1.0.0"

_MASK_63 = (1 << 63) - 1


def _normalise(obj: Any) -> Any:
    """Map ``obj`` to plain JSON types (dict with str keys, list, str, int, float, bool, None)."""
    if obj is None or isinstance(obj, (bool, str)):
        return obj
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, (int, np.integer)):
        return int(obj)
    if isinstance(obj, (float, np.floating)):
        value = float(obj)
        if not math.isfinite(value):
            raise StageFailure(ErrorCode.INVALID_CONFIG, "contracts.canonical_json",
                               "finite_floats", f"non-finite float {value!r} is not canonical")
        return value
    if isinstance(obj, Mapping):
        return {str(k): _normalise(v) for k, v in obj.items()}
    if isinstance(obj, np.ndarray):
        return _normalise(obj.tolist())
    if isinstance(obj, (list, tuple)):
        return [_normalise(v) for v in obj]
    if isinstance(obj, Enum):
        return _normalise(obj.value)
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: _normalise(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
    raise StageFailure(ErrorCode.INVALID_CONFIG, "contracts.canonical_json", "json_type",
                       f"type {type(obj).__name__} has no canonical JSON form")


def canonical_json(obj: Any) -> str:
    """Serialise ``obj`` to a canonical JSON string.

    Rules (these define artifact identity, so they are frozen):

    - dict keys are converted with ``str(k)`` and sorted; no whitespace (``","`` and ``":"``);
    - tuples and lists serialise identically (as JSON arrays);
    - numpy scalars become Python scalars; numpy arrays become nested lists;
    - floats use ``repr`` (shortest round-trip form), so ``0.1 -> 0.1`` and ``1.0 -> 1.0``;
      ``np.float32(0.1)`` becomes the float64 value ``0.10000000149011612``;
    - booleans stay ``true``/``false`` (never ``1``/``0``); str-valued enums use their value;
    - dataclass instances become objects keyed by field name;
    - non-ASCII text is kept as UTF-8 (``ensure_ascii=False``).

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` for NaN/inf floats or values with no JSON form.
    """
    return json.dumps(_normalise(obj), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def make_artifact_id(artifact_type: str, config: Mapping[str, Any], parent_ids: Sequence[str],
                     schema_version: str = SCHEMA_VERSION) -> str:
    """Content address of an artifact.

    Math: ``sha256(canonical_json([artifact_type, config, sorted(parent_ids), schema_version]))``
    as a lowercase hex digest, truncated to its first 16 characters.

    The id depends on the generating config and lineage, not on the payload, so a job run on
    another machine yields the same id. ``created_utc`` is never part of it.
    """
    blob = canonical_json([artifact_type, config, sorted(parent_ids), schema_version])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def tokens_hash(history: np.ndarray) -> str:
    """Hash of a token history ``w_1..w_p``: ``sha1(int64 little-endian bytes)[:16]``."""
    data = np.ascontiguousarray(np.asarray(history), dtype="<i8").tobytes()
    return hashlib.sha1(data).hexdigest()[:16]


def make_history_id(dataset_id: str, sequence_id: int, end: int, history_hash: str) -> str:
    """History id: ``sha1(f"{dataset_id}|{sequence_id}|{end}|{history_hash}")[:16]``."""
    text = f"{dataset_id}|{int(sequence_id)}|{int(end)}|{history_hash}"
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


class SeedTree:
    """Deterministic, platform-independent seed derivation (the only source of randomness).

    Math: ``seed(name, *scope) = int(sha256(canonical_json([master, name, *scope]))[:8 bytes],
    big-endian) & (2**63 - 1)``. For example ``seed`` for master 1729 and name ``"init"`` hashes
    the UTF-8 string ``[1729,"init"]``. ``generator`` wraps that seed in ``PCG64``.

    Every issued seed is recorded (per instance, never globally) in :attr:`issued`, keyed by
    ``"name/scope1/scope2"``, so stages can store it as the artifact ``seed_map``.

    Parameters
    ----------
    master : int
        Master seed (replicate seed, e.g. 1729), a non-negative integer.
    """

    def __init__(self, master: int) -> None:
        if isinstance(master, bool) or not isinstance(master, (int, np.integer)) or master < 0:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "contracts.SeedTree", "master",
                               f"master seed must be a non-negative int, got {master!r}")
        self.master = int(master)
        self.issued: dict[str, int] = {}

    def seed(self, name: str, *scope: str | int) -> int:
        """Derived 63-bit seed for ``(master, name, *scope)``; identical on every OS."""
        blob = canonical_json([self.master, name, *scope]).encode("utf-8")
        value = int.from_bytes(hashlib.sha256(blob).digest()[:8], "big") & _MASK_63
        self.issued["/".join([name, *map(str, scope)])] = value
        return value

    def generator(self, name: str, *scope: str | int) -> np.random.Generator:
        """A fresh ``np.random.Generator(PCG64(seed(name, *scope)))``."""
        return np.random.Generator(np.random.PCG64(self.seed(name, *scope)))

    def __repr__(self) -> str:
        return f"SeedTree(master={self.master})"
