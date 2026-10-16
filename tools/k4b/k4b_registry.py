"""K4b exposure registry (API.md §3; protocol §3.4, RC6, RC7). Identity-only access.

Sources: (a) ObservationSets, (b) the C1' store list, (c) the mailbox (JSON pre-validated),
(d) C1' digest list and digest columns, (e) permitted D-2a pools (sealed pools by predicate and
derived sequence-id ranges, never opened), (f) other ObservationSet stores under the root.
"""

from __future__ import annotations

import hashlib
import json
import time
import zipfile
from pathlib import Path

import c1_data
import c1_registry_sources as crs
import k4b_config
import numpy as np
import stage_records
from c1_records import C1GateFailure

ROOT = k4b_config.ROOT
ART = crs.ART
INCOMPLETE = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
LINEAGE = "FAIL_TECHNICAL/LINEAGE"
VERSIONS = ("K-REG1", "K-REG2")
HISTORY_KEYS = ("tokens", "canon32", "named32", "H", "canonical32", "canonical_tokens")
IDENTITY_KEYS = ("sequence_id", "seq_ids", "ids", "history_id", "canonical_ids")
OWN_READERS = {"agent-handoff": "c", "c1prime-store": "d", "d2a-store": "e"}


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _npz_header(path) -> dict:
    """{key: (dtype, shape)} from the .npy headers only (no array data, no pickle)."""
    out = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                version = np.lib.format.read_magic(f)
                read = (
                    np.lib.format.read_array_header_1_0
                    if version == (1, 0)
                    else np.lib.format.read_array_header_2_0
                )
                shape, _, dtype = read(f)
            out[name[:-4] if name.endswith(".npy") else name] = (dtype, shape)
    return out


def _history_bearing(header) -> bool:
    for key, (dtype, shape) in header.items():
        if key in HISTORY_KEYS or key.startswith("digest_"):
            return True
        if dtype.kind in "iu" and len(shape) >= 2 and shape[-1] in (32, 33):
            return True
    return False


def inventory(root=ROOT, exclude=()) -> dict:
    """Every top-level directory of root, recursively: history files, identity refs, OS roots.
    Directories in `exclude` are listed but not opened (their dedicated reader covers them)."""
    inv = {}
    for top in sorted(p for p in Path(root).iterdir() if p.is_dir()):
        rec = {
            "history_files": [],
            "identity_refs": [],
            "observation_set_roots": [],
            "unreadable": [],
            "excluded": top.name in exclude,
        }
        if not rec["excluded"]:
            for f in sorted(top.rglob("meta.json")):
                if f.parent.parent.name == "ObservationSet":
                    rec["observation_set_roots"].append(str(f.parent.parent.parent))
            rec["observation_set_roots"] = sorted(set(rec["observation_set_roots"]))
            for f in sorted(top.rglob("*.npz")):
                try:
                    header = _npz_header(f)
                except Exception as exc:  # noqa: BLE001  unreadable -> INCOMPLETE
                    rec["unreadable"].append({"path": str(f), "error": repr(exc)})
                    continue
                if _history_bearing(header):
                    rec["history_files"].append(str(f))
                elif any(k in IDENTITY_KEYS for k in header):
                    rec["identity_refs"].append(str(f))
        inv[top.name] = rec
    return inv


def classify(inv, scanned_readers) -> dict:
    """SCANNED (a reader covers it), NOT_SCANNED (inventory found nothing), else INCOMPLETE."""
    out = {}
    for name, rec in inv.items():
        found = (
            len(rec["history_files"]),
            len(rec["identity_refs"]),
            len(rec["observation_set_roots"]),
            len(rec.get("unreadable", [])),
        )
        if name in scanned_readers:
            out[name] = {"class": "SCANNED", "reason": f"reader(s) {scanned_readers[name]}"}
        elif not any(found) and not rec.get("excluded"):
            out[name] = {
                "class": "NOT_SCANNED",
                "reason": "inventory: 0 history-bearing files, "
                "0 identity references, 0 ObservationSet roots, 0 unreadable files",
            }
        else:
            out[name] = {
                "class": "INCOMPLETE",
                "reason": "history-bearing source without a "
                "reader (history, identity, OS roots, unreadable) = %s" % (found,),
            }
    return out


def validate_handoff_json(root) -> dict:
    failures, files = [], sorted(Path(root).rglob("*.json"))
    for f in files:
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001  any parse failure is recorded
            failures.append({"path": str(f), "error": repr(exc)})
    return {"ok": not failures, "n_files": len(files), "failures": failures}


def source_a(root_art, store=None) -> tuple:
    if store is None and Path(root_art).resolve() != Path(crs.ART).resolve():
        raise C1GateFailure("FAIL_TECHNICAL/REGISTRY", f"non-default root {root_art} needs a store")
    return crs.observation_set_sources(store, root_art)


def source_b(root=ROOT) -> list:
    return crs.store_sources(Path(root))


def source_c(root=ROOT / "agent-handoff") -> list:
    v = validate_handoff_json(root)
    if not v["ok"]:
        raise C1GateFailure(INCOMPLETE, f"handoff JSON parse failures: {v['failures']}")
    return crs.handoff_sources(Path(root))


def source_d(store=ROOT / "c1prime-store") -> list:
    store = Path(store)
    reg = store / "registry" / "registry_v1.json"
    sha = _sha(reg)
    if sha != k4b_config.CONTRACT["registry"]["c1prime_registry_v1_sha256"]:
        raise C1GateFailure(LINEAGE, "registry_v1 sha256 mismatch")
    d1 = json.loads(reg.read_text(encoding="utf-8"))
    out = [
        {
            "name": "d1:c1prime registry_v1",
            "path": str(reg),
            "sha256": sha,
            "digests": set(d1["digests"]),
            "sequence_ids": set(d1.get("sequence_ids", [])),
        }
    ]
    for f in sorted(store.rglob("HIST_*.npz")):
        digests, seqs = set(), set()
        with np.load(f, allow_pickle=False) as z:
            for key in ("digest_H", "digest_Hp", "digest_Hm"):
                digests |= set(np.asarray(z[key]).astype(str).tolist())
            if "sequence_id" in z.files:
                seqs = set(np.asarray(z["sequence_id"], dtype=np.int64).tolist())
        out.append(
            {
                "name": f"d2:{f.relative_to(store).as_posix()}",
                "path": str(f),
                "sha256": _sha(f),
                "digests": digests,
                "sequence_ids": seqs,
            }
        )
    return out


def _d2a_reader(store, pool, entry):
    """A permitted pool's raw tokens[:, :32] (uint8, no canonicalisation)."""
    if entry.get("id"):
        from topo_pilot.contracts import ArtifactStore, ObservationSet
        from topo_pilot.contracts.backends import LocalFSBackend

        path = store / "store" / "ObservationSet" / entry["id"] / "payload.npz"

        def reader(_path, oid=entry["id"]):
            obs = ArtifactStore(LocalFSBackend(store / "store")).load(
                ObservationSet, oid, consumer="analysis"
            )
            return np.ascontiguousarray(np.asarray(obs.tokens)[:, :32]).astype(np.uint8)

        return path, reader
    for path in (
        store / "pools" / f"{pool}.npz",
        store / f"{pool}.npz",
        store / pool / "tokens.npz",
    ):
        if path.is_file():

            def reader(p):
                with np.load(p, allow_pickle=False) as z:
                    return np.ascontiguousarray(np.asarray(z["tokens"])[:, :32]).astype(np.uint8)

            return path, reader
    return None, None


def source_e(store=ROOT / "d2a-store", pools_meta=None) -> dict:
    store, d2a = Path(store), k4b_config.CONTRACT["registry"]["d2a"]
    res = {
        "sources": [],
        "sealed_ranges": {},
        "ranges": {},
        "predicates": ["sealed_d2a"],
        "status": "PASS",
        "problems": [],
    }
    if list(d2a.get("predicate_alphabet", [])) != [0, 1, 2, 3, 4]:
        res["problems"].append("unresolved predicate alphabet")
    meta_path = store / "pools.json"
    if pools_meta is None:
        try:
            pools_meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001  unresolved pool inventory
            res["problems"].append(f"pools.json unreadable: {exc!r}")
            pools_meta = {}
    for code, pool in enumerate(d2a["pools"], start=1):
        entry = pools_meta.get(pool)
        if not isinstance(entry, dict) or not isinstance(entry.get("n"), int):
            res["problems"].append(f"pool {pool}: n unresolved")
            continue
        rng = (code * 2**32, code * 2**32 + int(entry["n"]))
        res["ranges"][pool] = rng
        if pool in d2a["sealed"]:
            res["sealed_ranges"][pool] = rng
            continue
        path, reader = _d2a_reader(store, pool, entry)
        if path is None:
            res["problems"].append(f"pool {pool}: token array unresolved")
            continue
        res["sources"].append(
            {
                "name": f"e:d2a/{pool}",
                "path": path,
                "reader": reader,
                "meta": {
                    "source": "e",
                    "pool": pool,
                    "n": entry["n"],
                    "canonicalisation": "none (raw tokens[:, :32])",
                },
            }
        )
    if res["problems"]:
        res["status"] = INCOMPLETE
    return res


def source_f(root, inv, classes) -> list:
    """ObservationSet stores under other directories, canonicalised by their EmissionSpec."""
    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    out = []
    for name, rec in inv.items():
        if classes.get(name, {}).get("class") != "SCANNED" or name in OWN_READERS:
            continue
        for art in rec["observation_set_roots"]:
            if Path(art).resolve() == Path(crs.ART).resolve():
                continue
            out += crs.observation_set_sources(ArtifactStore(LocalFSBackend(Path(art))), art)[0]
    return out


def revalidate_coverage(root_art, root=ROOT, extra_ids=None, store=None) -> dict:
    """crs.coverage unchanged, then every referenced id must resolve to a covered source."""
    try:
        seqs = source_a(root_art, store)[1]
        hist = crs.history_index_ids(store, root_art)
        cov = crs.coverage(seqs, hist, Path(root))
    except Exception as exc:  # noqa: BLE001  unresolvable coverage -> INCOMPLETE
        return {"ok": False, "missing": [f"coverage unresolved: {exc!r}"]}
    missing = [k for k, v in cov.items() if isinstance(v, dict) and v.get("missing")]
    covered = set().union(*(set(v.tolist()) for v in seqs.values())) if seqs else set()
    missing += [f"id {i}" for i in sorted(set(extra_ids or ()) - covered)]
    return {"ok": not missing, "missing": missing, "coverage": cov}


def build(version, out_dir, root=ROOT, extra=None) -> dict:
    """Builds K-REG1/K-REG2 from scratch; manifest and digest npz written by exclusive create."""
    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    if version not in VERSIONS:
        raise C1GateFailure("FAIL_TECHNICAL/REGISTRY", f"unknown registry version {version}")
    root, out_dir = Path(root), Path(out_dir)
    mpath, dpath = out_dir / f"{version}.json", out_dir / f"{version}_digests.npz"
    if mpath.exists() or dpath.exists():
        raise FileExistsError(mpath)
    problems, readers = [], {}
    art = root / "topo-pilot" / "artifacts"
    store = ArtifactStore(LocalFSBackend(art))
    token_sources, digest_sources, seq_union = [], [], set()
    try:
        a_src, seqs = source_a(art, store)
        token_sources += a_src
        readers.setdefault("topo-pilot", []).append("a")
    except Exception as exc:  # noqa: BLE001
        problems.append(f"a: {exc!r}")
        seqs = {}
    token_sources += source_b(root)
    for s in crs.SCANNED_STORES:
        readers.setdefault(s, []).append("b")
    try:
        token_sources += source_c(root / "agent-handoff")
        readers.setdefault("agent-handoff", []).append("c")
    except Exception as exc:  # noqa: BLE001
        problems.append(f"c: {exc!r}")
    try:
        digest_sources = source_d(root / "c1prime-store")
        readers.setdefault("c1prime-store", []).append("d")
    except Exception as exc:  # noqa: BLE001
        problems.append(f"d: {exc!r}")
    e = source_e(root / "d2a-store")
    token_sources += e["sources"]
    problems += [f"e: {p}" for p in e["problems"]]
    if not e["problems"]:
        readers.setdefault("d2a-store", []).append("e")
    inv = inventory(root, exclude=tuple(OWN_READERS))
    for name, rec in inv.items():
        if (
            name not in readers
            and rec["observation_set_roots"]
            and not rec["history_files"]
            and not rec["identity_refs"]
            and not rec["unreadable"]
        ):
            readers[name] = ["f"]
    classes = classify(inv, readers)
    token_sources += source_f(root, inv, classes)
    reg = c1_data.build_registry(token_sources)
    problems += [f"unreadable: {m['name']}" for m in reg["missing"]]
    digests = set(reg["digests"])
    for s in digest_sources:
        digests |= s["digests"]
        seq_union |= s["sequence_ids"]
    for v in seqs.values():
        seq_union |= set(np.asarray(v, dtype=np.int64).tolist())
    for tab in extra or []:
        digests |= set(np.asarray(tab["digest"]).astype(str).tolist())
        seq_union |= set(np.asarray(tab["seq_ids"], dtype=np.int64).tolist())
    hv = (
        validate_handoff_json(root / "agent-handoff")
        if (root / "agent-handoff").is_dir()
        else {"ok": False, "n_files": 0, "failures": ["mailbox absent"]}
    )
    cov = revalidate_coverage(art, root, store=store)
    problems += [] if cov["ok"] else [f"coverage: {cov['missing']}"]
    problems += [
        f"class {k}: {v['reason']}" for k, v in classes.items() if v["class"] == "INCOMPLETE"
    ]
    sorted_d = sorted(digests)
    seq_arr = np.array(sorted(seq_union), dtype=np.int64)
    sources = [
        {
            "name": s["name"],
            "path": str(s["path"]),
            "sha256": s.get("sha256"),
            "kind": "token",
            "n": s.get("rows"),
            "canonicalisation": s.get("meta", {}).get("canonicalisation"),
        }
        for s in reg["entries"]
    ]
    sources += [
        {
            "name": s["name"],
            "path": s["path"],
            "sha256": s["sha256"],
            "kind": "digest",
            "n": len(s["digests"]),
            "canonicalisation": "C1' digest columns",
        }
        for s in digest_sources
    ]
    manifest = {
        "version": version,
        "status": INCOMPLETE if problems else "PASS",
        "n_digests": len(sorted_d),
        "problems": problems,
        "digests_sha256": hashlib.sha256("\n".join(sorted_d).encode()).hexdigest(),
        "seq_id_union_sha256": hashlib.sha256(seq_arr.tobytes()).hexdigest(),
        "sealed_ranges": e["sealed_ranges"],
        "d2a_ranges": e["ranges"],
        "predicates": e["predicates"],
        "sources": sources,
        "classes": classes,
        "not_scanned": {k: v["reason"] for k, v in classes.items() if v["class"] == "NOT_SCANNED"},
        "coverage": cov,
        "handoff_validation": hv,
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "protocol_sha256": k4b_config.CONTRACT["protocol_sha256"],
    }
    stage_records.save_npz(dpath, digests=np.array(sorted_d), seq_ids=seq_arr)
    manifest["digest_file_sha256"] = _sha(dpath)
    stage_records.write_new(mpath, manifest)
    return manifest


def load(out_dir, version) -> tuple:
    out_dir = Path(out_dir)
    manifest = json.loads((out_dir / f"{version}.json").read_text(encoding="utf-8"))
    dpath = out_dir / f"{version}_digests.npz"
    if _sha(dpath) != manifest["digest_file_sha256"]:
        raise C1GateFailure(LINEAGE, f"{dpath.name} does not re-hash to its manifest")
    with np.load(dpath, allow_pickle=False) as z:
        digests = set(z["digests"].astype(str).tolist())
        seqs = set(z["seq_ids"].astype(np.int64).tolist())
    if (
        hashlib.sha256("\n".join(sorted(digests)).encode()).hexdigest()
        != manifest["digests_sha256"]
    ):
        raise C1GateFailure(LINEAGE, "digest union does not match its manifest")
    ranges = {k: tuple(v) for k, v in manifest.get("d2a_ranges", {}).items()}
    return digests, seqs, ranges, list(manifest["predicates"]), manifest
