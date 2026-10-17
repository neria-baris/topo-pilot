"""K4b registry, reader k for K4b's own store (API.md §16, ruling R28, defect D5).

Also holds the identity-only npz header helpers that k4b_registry re-exports (footprint split,
API.md §13.2). Derived registry lineage records are listed and contribute nothing; history-bearing
stage tables (current and superseded) are token/digest sources; anything else history-bearing,
identity-bearing or unreadable is `other`, which makes the k4b-store class INCOMPLETE.
"""

from __future__ import annotations

import fnmatch
import hashlib
import zipfile
from pathlib import Path

import numpy as np

INCOMPLETE = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
HISTORY_KEYS = ("tokens", "canon32", "named32", "H", "canonical32", "canonical_tokens")
IDENTITY_KEYS = ("sequence_id", "seq_ids", "ids", "history_id", "canonical_ids")
DERIVED = ("K-REG*.json", "K-REG*_digests.npz")  # §16 (a), in registry/ or superseded/*/registry/
GROUPS = ("derived", "sources", "other")


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _npz_header(path) -> dict:
    """{key: (dtype, shape)} from the .npy headers only (no array data, no pickle)."""
    out = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                version = np.lib.format.read_magic(f)
                read = (np.lib.format.read_array_header_1_0 if version == (1, 0)
                        else np.lib.format.read_array_header_2_0)
                shape, _, dtype = read(f)
            out[name[:-4] if name.endswith(".npy") else name] = (dtype, shape)
    return out


def _history_arrays(header) -> dict:
    """{key: shape} of the history arrays of one npz header (§3.4 history detection)."""
    return {k: list(shape) for k, (dtype, shape) in header.items()
            if k in HISTORY_KEYS or k.startswith("digest_")
            or (dtype.kind in "iu" and len(shape) >= 2 and shape[-1] in (32, 33))}


def _derived(parts) -> bool:
    where = parts[:-1] == ("registry",) or (
        len(parts) == 4 and parts[0] == "superseded" and parts[2] == "registry")
    return where and any(fnmatch.fnmatchcase(parts[-1], p) for p in DERIVED)


def _staged(parts) -> bool:
    return (len(parts) > 1 and parts[0] == "stages") or (
        len(parts) > 3 and parts[0] == "superseded" and parts[2] == "stages")


def _stage_source(f, rel, hist) -> dict:
    """One own stage table, read in full here (a partial read raises, §16 item 3): every history
    array's first 32 columns as uint8 tokens, plus its digest and sequence-id columns."""
    digests, seqs, rows = set(), set(), []
    with np.load(f, allow_pickle=False) as z:
        for k in z.files:
            a = np.asarray(z[k])
            if k == "digest" or k.startswith("digest_"):
                digests |= set(a.astype(str).tolist())
            elif k in hist:
                rows.append(np.ascontiguousarray(a.reshape(-1, a.shape[-1])[:, :32]))
            if k in ("seq_ids", "sequence_id"):
                seqs |= set(a.astype(np.int64).tolist())
    tokens = np.concatenate(rows).astype(np.uint8) if rows else np.zeros((0, 32), np.uint8)
    return {"name": f"k:{rel}", "path": str(f), "sha256": _sha(f), "rows": int(len(tokens)),
            "reader": lambda _p, t=tokens: t, "digests": digests, "sequence_ids": seqs,
            "meta": {"source": "k", "keys": sorted(hist),
                     "canonicalisation": "as stored (K4b's own stage table)"}}


def source_k(store_root) -> dict:
    """Classifies every file under k4b-store (§16 item 2 a-d); other non-empty -> INCOMPLETE."""
    store = Path(store_root)
    res = {g: [] for g in GROUPS}
    for f in sorted(p for p in store.rglob("*") if p.is_file()):
        parts = f.relative_to(store).parts
        rel = "/".join(parts)
        if _derived(parts):  # (a) unions of other scanned sources: listed, contribute nothing
            res["derived"].append({"path": str(f), "sha256": _sha(f)})
            continue
        if f.name == "meta.json" and f.parent.parent.name == "ObservationSet":
            res["other"].append({"path": str(f), "sha256": _sha(f),
                                 "reason": "ObservationSet root without a reader"})
            continue
        if f.suffix != ".npz":
            continue  # (c) free files: freeze, tests, logs, operations, records, SHA256SUMS
        try:
            header = _npz_header(f)
        except Exception as exc:  # noqa: BLE001  unreadable -> (d)
            res["other"].append({"path": str(f), "sha256": _sha(f),
                                 "reason": f"unreadable {exc!r}"})
            continue
        hist = _history_arrays(header)
        if hist and _staged(parts):  # (b) own stage tables, superseded attempts included
            res["sources"].append(_stage_source(f, rel, hist))
        elif hist or any(k in IDENTITY_KEYS for k in header):  # (d)
            res["other"].append({"path": str(f), "sha256": _sha(f), "reason": "history-bearing "
                                 f"{sorted(hist)}" if hist else "identity-bearing"})
    res["status"] = INCOMPLETE if res["other"] else "PASS"
    return res


def summary(res) -> dict:
    """Manifest `k4b_store` (§16 item 4): counts and sha256s per group; None -> not read."""
    if res is None:
        return {"status": "NOT_READ (k4b-store absent, or reader k failed: see problems)"}
    out = {"status": res["status"]}
    for g in GROUPS:
        out[g] = {"n": len(res[g]), "files": [
            {k: v for k, v in it.items() if k in ("path", "sha256", "rows", "reason")}
            for it in res[g]]}
    return out
