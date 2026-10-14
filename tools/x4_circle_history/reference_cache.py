"""Persisted exact reference moments (API.md spec v2.4 item 3; ERROR_BOUND.md v2.2 section 8).

The oracle stage writes the file once; the charts stage reloads and verifies it instead of
recomputing the all-row Decimal references in a second stage subprocess. Entries are keyed
like error_bound.reference_moments: (process digest, K, int64 history bytes). The file also
binds the feature and source identities and the per-model/split row table. Decimal values are
stored as exact strings and never pass through float.
"""

from __future__ import annotations

import hashlib
from decimal import Decimal, InvalidOperation
from pathlib import Path

import numpy as np
from errors import Invalid

SCHEMA = "x4-circle-reference-cache-v2"
HERE = Path(__file__).resolve().parent
SOURCES = {
    "independent_reference": HERE.parents[1]
    / "tests"
    / "oracle_profile"
    / "independent_reference.py",
    "error_bound": HERE / "error_bound.py",
}


def identity(T, E, pi, coords) -> dict:
    """Process, exact-feature and reference-source identities of a cache."""
    import error_bound as eb

    table = eb.exact_features(np.arange(12, dtype=np.float64).reshape(12, 1))
    text = "\n".join(f"{c}|{s}" for c, s in table) + f"|{eb.FEATURE_DIGITS}|{eb.REF_DIGITS}"
    return {
        "process_digest": eb.process_digest(T, E, pi, coords),
        "feature_identity": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "source_identity": {
            name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in SOURCES.items()
        },
    }


def history_hex(canonical32) -> list[str]:
    """int64-bytes hex per row; integer dtype, shape [n, 32] and nonnegative checked first."""
    tok = np.asarray(canonical32)
    if tok.ndim != 2 or tok.shape[1] != 32 or tok.dtype.kind not in "iu":
        raise Invalid("canonical histories must be integer [n, 32]")
    if tok.size and tok.min() < 0:
        raise Invalid("negative canonical history symbol")
    return [row.tobytes().hex() for row in tok.astype(np.int64)]


def export_cache(cache: dict, ident: dict, rows: list) -> dict:
    """JSON-able cache: identity, row table and sorted exact entries."""
    entries = [
        {"process_digest": d, "K": int(k), "history": h.hex(), "mx": str(v[0]), "my": str(v[1])}
        for (d, k, h), v in sorted(cache.items())
    ]
    return {"schema": SCHEMA, "identity": ident, "rows": list(rows), "entries": entries}


def _finite_decimal(text) -> Decimal:
    if not isinstance(text, str):
        raise Invalid(f"reference cache value {text!r} is not a string")
    try:
        value = Decimal(text)
    except (InvalidOperation, ValueError) as exc:
        raise Invalid(f"reference cache value {text!r} is not a Decimal") from exc
    if not value.is_finite():
        raise Invalid(f"reference cache value {text!r} is not finite")
    return value


def load_cache(obj: dict, ident_expected: dict) -> dict:
    """Rebuild {(digest, K, bytes): (Mx, My)} after verifying schema, identity and entries."""
    if not isinstance(obj, dict) or obj.get("schema") != SCHEMA:
        raise Invalid("reference cache schema")
    if obj.get("identity") != ident_expected:
        raise Invalid("reference cache identity differs (process, features or sources)")
    digest = ident_expected["process_digest"]
    cache: dict = {}
    for e in obj.get("entries", []):
        if e.get("process_digest") != digest:
            raise Invalid("reference cache entry bound to a different process")
        try:
            key = (digest, int(e["K"]), bytes.fromhex(e["history"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise Invalid("malformed reference cache entry") from exc
        if key in cache:
            raise Invalid("duplicate reference cache entry")
        cache[key] = (_finite_decimal(e.get("mx")), _finite_decimal(e.get("my")))
    return cache


def row_record(model, split, panel, history_id, sequence_id, canonical32) -> dict:
    """The row-table record export_cache stores for one model and split."""
    return {
        "model": int(model),
        "split": str(split),
        "panel": int(panel),
        "history_id": [str(h) for h in np.asarray(history_id).astype(str)],
        "sequence_id": [int(s) for s in np.asarray(sequence_id, dtype=np.int64)],
        "history": history_hex(canonical32),
    }


def verify_rows(obj, model, split, panel, history_id, sequence_id, canonical32, Ks=(4, 32)):
    """Invalid unless the stored row table for (model, split) equals the reloaded rows exactly
    and every (digest, K, row) entry for K in Ks is present."""
    records = [
        r for r in obj.get("rows", []) if (r.get("model"), r.get("split")) == (int(model), split)
    ]
    if len(records) != 1:
        raise Invalid(f"reference cache has {len(records)} row records for {model}/{split}")
    want = row_record(model, split, panel, history_id, sequence_id, canonical32)
    for key in ("panel", "history_id", "sequence_id", "history"):
        if records[0].get(key) != want[key]:
            raise Invalid(f"reference cache row table differs for {model}/{split}: {key}")
    digest = obj["identity"]["process_digest"]
    present = {(e["process_digest"], int(e["K"]), e["history"]) for e in obj.get("entries", [])}
    missing = [h for h in want["history"] for K in Ks if (digest, int(K), h) not in present]
    if missing:
        raise Invalid(f"reference cache misses {len(missing)} entries for {model}/{split}")
