"""HWSB H2-B separation and the fail-closed registry reader (API.md §2.4, §2.5; protocol §2.3,
§6.3, B9a). Split out of hwsb_data by size; hwsb_data re-exports every name, so `hd.<name>`
keeps working.

B9a reads and hashes stage B's OWN history payloads (ObservationSet payload.npz, hist/*.npz)
inside its own store (ruling c7); no other store's payload is opened or hashed.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
from collections import Counter
from pathlib import Path

import hwsb_data as hd
import numpy as np
import scores
import stage_records
from hwsb_data import BLOCKS, LINEAGE, READER, REGISTRY, canonical32, load_block

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    ObservationSet,
    StageFailure,
)
from topo_pilot.dataset.checks import check_disjoint

__all__ = ["train_dev_canonical", "hws_store_digests", "duplicates", "separation",
           "history_inventory", "registry_digests", "hd"]


def train_dev_canonical(store, ids, perm) -> tuple:
    obs = store.load(ObservationSet, ids, consumer=READER)
    return canonical32(obs.tokens, perm), np.asarray(obs.sequence_id, dtype=np.int64)


def hws_store_digests(root=hc.HWS_STORE, key=hc.KEY) -> dict:
    root = Path(root)
    files, digests = [], set()
    for f in sorted((root / "hist").rglob(f"{key}.npz")):
        with np.load(f, allow_pickle=False) as z:
            digests |= set(scores.history_digests(z["canon32"]))
        files.append(f.relative_to(root).as_posix())
    return {"files": files, "digests": digests}


def duplicates(digests) -> dict:
    digests = list(digests)
    c = Counter(digests)
    n = len(digests)
    return {
        "n_rows": n,
        "n_unique": len(c),
        "n_duplicate_rows": n - len(c),
        "max_multiplicity": max(c.values()) if c else 0,
    }


def separation(blocks, train_dev, hws=None) -> dict:
    tables = {r: np.asarray(b["seq_ids"]) for r, b in blocks.items()}
    tables.update({name: np.asarray(v[1]) for name, v in train_dev.items()})
    overlap = None
    try:
        check_disjoint(**tables)
    except StageFailure as exc:
        overlap = str(exc)
    dig = {r: set(b["digest_canon32"]) for r, b in blocks.items()}
    td = set()
    for canon, _ in train_dev.values():
        td |= set(scores.history_digests(canon))
    roles = [r for r in BLOCKS if r in dig]
    col = {}
    for i, a in enumerate(roles):
        for b in roles[i + 1 :]:
            col[f"{a}|{b}"] = len(dig[a] & dig[b])
    for r in roles:
        col[f"{r}|train_dev"] = len(dig[r] & td)
    ok = overlap is None and all(v == 0 for v in col.values())
    return {
        "status": "PASS" if ok else LINEAGE,
        "id_overlap": overlap,
        "collisions": col,
        "duplicates": {r: duplicates(blocks[r]["digest_canon32"]) for r in roles},
        "hws_store_collisions": None if hws is None else {r: len(dig[r] & set(hws)) for r in roles},
    }


def _rel(store, f) -> str:
    return Path(f).relative_to(store).as_posix()


def history_inventory(store) -> dict:
    """{relpath: sha256} of every file under artifacts/ObservationSet/, hist/, superseded/.
    These are stage B's own payloads; they ARE hashed here (ruling c7)."""
    store = Path(store)
    out = {}
    for sub in (Path("artifacts") / "ObservationSet", Path("hist"), Path("superseded")):
        base = store / sub
        if base.is_dir():
            for f in sorted(p for p in base.rglob("*") if p.is_file()):
                out[_rel(store, f)] = stage_records.sha256(f)
    return dict(sorted(out.items()))


def _art_roots(store) -> list:
    roots = [store / "artifacts"] if (store / "artifacts").is_dir() else []
    sup = store / "superseded"
    if sup.is_dir():
        roots += sorted(p for p in sup.rglob("artifacts") if p.is_dir())
    return roots


def _os_digests(root, aid) -> list:
    st = ArtifactStore(LocalFSBackend(root))
    obs = st.load(ObservationSet, aid, consumer=READER)
    meta = st.meta(aid)
    ems = [p for p in meta.parent_ids if st.meta(p).artifact_type == "EmissionSpec"]
    if len(ems) != 1:
        raise ValueError(f"{len(ems)} EmissionSpec parents")
    spec = st.load(EmissionSpec, ems[0], consumer=READER)
    return scores.history_digests(canonical32(obs.tokens, spec.symbol_perm))


def registry_digests(store, expected=None) -> dict:
    """Fail-closed digest reader of every stage-B history (B9a ii)."""
    store = Path(store)
    sources, failures, digests, n_rows, n_dig = [], [], set(), 0, 0
    hist = sorted(f for f in (store / "hist").glob("*") if f.is_file())
    sup = store / "superseded"
    hist += sorted(f for f in sup.rglob("*.npz") if f.parent.name == "hist") if sup.is_dir() else []
    for f in hist:
        rel = _rel(store, f)
        try:
            if f.suffix != ".npz" or f.stem not in hc.HIST_NAMES:
                raise ValueError("unexpected file name in hist/")
            b = load_block(f)
            d = b["digest_canon32"]
            sources.append({"path": rel, "kind": "hist", "n_rows": len(d), "n_digests": len(d)})
            digests |= set(d)
            n_rows += int(b["canon32"].shape[0])
            n_dig += len(d)
        except Exception as exc:  # noqa: BLE001  fail closed
            failures.append({"path": rel, "error": f"{type(exc).__name__}: {exc}"})
    for root in _art_roots(store):
        base = root / "ObservationSet"
        for d in sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []:
            rel = _rel(store, d)
            try:
                dg = _os_digests(root, d.name)
                sources.append(
                    {"path": rel, "kind": "ObservationSet", "n_rows": len(dg), "n_digests": len(dg)}
                )
                digests |= set(dg)
                n_rows += len(dg)
                n_dig += len(dg)
            except Exception as exc:  # noqa: BLE001  fail closed
                failures.append({"path": rel, "error": f"{type(exc).__name__}: {exc}"})
    if expected is not None:
        found = history_inventory(store)
        for rel, sha in expected.items():
            if rel not in found:
                failures.append({"path": rel, "error": "expected file missing"})
            elif found[rel] != sha:
                failures.append({"path": rel, "error": "sha256 differs from the expected list"})
        failures += [
            {"path": rel, "error": "file not in the expected list"}
            for rel in found
            if rel not in expected
        ]
    ok = not failures and n_dig == n_rows
    return {
        "status": "PASS" if ok else REGISTRY,
        "sources": sources,
        "digests": digests,
        "n_rows": n_rows,
        "n_digests": n_dig,
        "failures": failures,
    }
