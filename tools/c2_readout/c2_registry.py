"""C2 exposure registry c2-reg-v1: the R and R' sources (the reused C1'/K4b readers a-f, k and
the X6S1 reader x6), the run-time inventory against the frozen table, builds, loading and the
split separation (API.md §5, §18; C2-FROZEN-v1 §5.3, §7 rows 4, 5, 22). Identity-only access.

Paths are read through c2_config at call time (API.md §19.1 E-24). x6s1_registry is imported
lazily inside the reader-x6 functions (API.md §1).
"""

from __future__ import annotations

import hashlib
import json
import time
from itertools import combinations
from pathlib import Path

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_data
import c1_registry_sources as crs
import c2_data as cd
import k4b_data
import k4b_registry as kr
import numpy as np
import stage_records

from topo_pilot.dataset.checks import check_disjoint

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
VERSIONS = ("C2-REG1", "C2-REG2")
OWN = "c2-readout-store"
EXCLUDE = ("agent-handoff", "c1prime-store", "d2a-store", "k4b-store", "x6-stage1-store", OWN)
OWN_READERS = {"topo-pilot": "a", "agent-handoff": "c", "c1prime-store": "d", "d2a-store": "e"}
OWN_READERS.update({"k4b-store": "k", "x6-stage1-store": "x6"})
COUNT_KEYS = ("history_files", "identity_refs", "observation_set_roots", "unreadable")
SRC_KEYS = ("name", "path", "sha256", "kind", "n", "canonicalisation")
INVENTORY = cc.CONTRACT["registry"]["inventory"]


class RegistryLineage(RuntimeError):
    """A registry binding or re-hash mismatch; `.status` is FAIL_TECHNICAL/LINEAGE."""

    def __init__(self, detail: str):
        super().__init__(f"{LINEAGE}: {detail}")
        self.status = LINEAGE


def _root(root) -> Path:
    return Path(cc.PROJECT_ROOT if root is None else root)


def _try(problems, tag, fn):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001  a failed source makes the registry INCOMPLETE
        problems.append(f"{tag}: {exc!r}")
        return None


# ---- reader x6 (API.md §5.1) -----------------------------------------------------------------
def _x6_member(xr, key, arr, entry):
    """Digest chunks of one history-bearing member (token columns 0..31, or hex digests)."""
    a = np.asarray(arr)
    if key.startswith("digest"):
        yield xr.hex_to_digests(a)
        entry["rows"] += int(a.size)
    elif key in kr.HISTORY_KEYS or (
        a.dtype.kind in "iu" and a.ndim >= 2 and a.shape[-1] in (32, 33)
    ):
        tokens = a.reshape(-1, a.shape[-1])[:, :32]
        yield from xr._chunks(tokens)
        entry["rows"] += int(len(tokens))


def _x6_chunks(xr, store, files, other):
    for f in sorted(p for p in store.rglob("*") if p.is_file() and p.suffix in (".npz", ".npy")):
        if f.relative_to(store).parts[0] == "registry":
            continue
        try:
            if not xr._history_bearing(f):
                continue
            entry = {"path": str(f), "sha256": cd.file_sha(f), "keys": [], "rows": 0}
            if f.suffix == ".npy":
                members = {"": np.load(f, allow_pickle=False)}
            else:
                with np.load(f, allow_pickle=False) as z:
                    members = {k: np.asarray(z[k]) for k in z.files}
            chunks = [c for k, a in members.items() for c in _x6_member(xr, k, a, entry)]
            entry["keys"] = sorted(members)
        except Exception as exc:  # noqa: BLE001  an unreadable array file -> other -> INCOMPLETE
            other.append({"path": str(f), "reason": f"unreadable {exc!r}"})
            continue
        files.append(entry)
        yield from chunks


def x6_source(store=None, run_dir=None) -> dict:
    """X6-REG2 (re-hashed, manifest bound by CONTRACT.json) as base plus every other history-
    bearing array of the X6S1 store, as one bounded-memory DigestSet written into run_dir."""
    import x6s1_registry as xr

    store = Path(cc.X6S1_STORE if store is None else store)
    out = {"status": "PASS", "digestset": None, "files": [], "other": [], "base": None}
    man = store / "registry" / "X6-REG2.json"
    try:
        msha = cd.file_sha(man)
        recorded = json.loads(man.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        out["other"].append({"path": str(man), "reason": f"unreadable {exc!r}"})
        out["status"] = INCOMPLETE
        return out
    got = recorded.get
    out["base"] = {"manifest_sha256": msha, "n": got("n"), "digest_sha256": got("digest_sha256")}
    if msha != cc.CONTRACT["registry"]["x6_reg2_manifest_sha256"]:
        out["status"] = LINEAGE
        return out
    try:
        base = xr.open_reg(store, "X6-REG2")
    except xr.RegistryError as exc:
        out["other"].append({"path": str(man), "reason": repr(exc)})
        out["status"] = LINEAGE
        return out
    chunks = _x6_chunks(xr, store, out["files"], out["other"])
    out["digestset"] = xr.DigestSet.build(chunks, run_dir, base=base)
    out["status"] = INCOMPLETE if out["other"] else "PASS"
    return out


# ---- token and digest sources a-e, k (API.md §5.1) -------------------------------------------
def token_sources(root=None) -> dict:
    """Readers a, b, c, d, e, k through the reused K4b/C1' functions; failures become problems
    (a binding mismatch of reader d is also recorded under "lineage")."""
    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    root, problems, lineage = _root(root), [], []
    art = root / "topo-pilot" / "artifacts"
    store_a = ArtifactStore(LocalFSBackend(art))
    res = {"art": art, "store_a": store_a, "problems": problems, "lineage": lineage}
    res["a"] = _try(problems, "a", lambda: kr.source_a(art, store_a))
    res["b"] = kr.source_b(root)
    res["c"] = _try(problems, "c", lambda: kr.source_c(root / "agent-handoff"))
    try:
        res["d"] = kr.source_d(root / "c1prime-store")
    except Exception as exc:  # noqa: BLE001  unreadable -> INCOMPLETE; binding -> LINEAGE
        res["d"] = None
        problems.append(f"d: {exc!r}")
        if getattr(exc, "status", None) == LINEAGE:
            lineage.append(f"d: {exc}")
    res["e"] = kr.source_e(root / "d2a-store")
    problems += [f"e: {p}" for p in res["e"]["problems"]]
    ks = root / "k4b-store"
    res["k"] = _try(problems, "k", lambda: kr.source_k(ks)) if ks.is_dir() else None
    if res["k"] is not None and res["k"]["other"]:
        problems.append(f"k: {len(res['k']['other'])} unclassified file(s)")
    return res


# ---- inventory against the frozen table (API.md §5.2, §18) -----------------------------------
def _static_readers() -> dict:
    out = {s: ["b"] for s in crs.SCANNED_STORES}
    out.update({name: [tag] for name, tag in OWN_READERS.items()})
    return out


def _tags(rec, readers) -> list:
    roots = rec.get("observation_set_roots", [])
    f = ["f"] if any(not kr._under(r, crs.ART) for r in roots) else []
    return sorted(set(readers) | set(f))


def _violation(name, entry, rec, cls, readers) -> str | None:
    decision = entry.get("decision") if entry else None
    if decision == "READER":
        if rec is None:
            return "frozen READER directory absent"
        if cls["class"] != "SCANNED" or _tags(rec, readers) != sorted(entry["readers"]):
            return f"READER expected tags {entry['readers']}; classed {cls['class']}"
    elif decision == "EXCLUSION" and rec is not None and cls["class"] != "NOT_SCANNED":
        return f"EXCLUSION classed {cls['class']}: {cls['reason']}"
    elif decision is None:
        counts = sum(len(rec[k]) for k in COUNT_KEYS)
        if cls["class"] != "NOT_SCANNED" or counts:
            return f"unlisted directory classed {cls['class']} with {counts} item(s)"
    if cls is not None and cls["class"] == "INCOMPLETE":
        return f"class INCOMPLETE: {cls['reason']}"
    return None


def inventory(root=None, readers=None) -> dict:
    """k4b_registry.inventory/classify of every top-level directory, checked against the frozen
    INVENTORY by rules (i)-(iv); `readers` = the tags of the readers that succeeded."""
    readers = _static_readers() if readers is None else readers
    inv = kr.inventory(_root(root), exclude=EXCLUDE)
    inv.pop(OWN, None)
    classes = kr.classify(inv, readers)
    frozen = {k: v for k, v in cc.CONTRACT["registry"]["inventory"].items() if k != OWN}
    unlisted = sorted(set(inv) - set(frozen))
    violations = []
    for name in sorted(set(inv) | set(frozen)):
        why = _violation(
            name, frozen.get(name), inv.get(name), classes.get(name), readers.get(name, [])
        )
        if why:
            violations.append({"name": name, "reason": why})
    status = INCOMPLETE if violations else "PASS"
    out = {"status": status, "inv": inv, "classes": classes}
    out.update(unlisted=unlisted, violations=violations)
    return out


# ---- builds (API.md §5.3, §16.3) -------------------------------------------------------------
def _ok_readers(src, x6_ok) -> dict:
    readers = {s: ["b"] for s in crs.SCANNED_STORES}
    ok = {"topo-pilot": src["a"] is not None, "agent-handoff": src["c"] is not None}
    ok.update({"c1prime-store": src["d"] is not None, "d2a-store": not src["e"]["problems"]})
    ok.update({"k4b-store": src["k"] is not None, "x6-stage1-store": x6_ok})
    for name, tag in OWN_READERS.items():
        if ok[name]:
            readers.setdefault(name, []).append(tag)
    return readers


def _x6_manifest(res, out_dir) -> dict:
    ds = res["digestset"]
    own = [p for p in (ds.paths if ds is not None else []) if cd._rel(p, out_dir) is not None]
    out = {"status": res["status"], "n": ds.n if ds is not None else 0}
    out["digest_sha256"] = ds.sha256() if ds is not None else None
    out["base_manifest_sha256"] = (res["base"] or {}).get("manifest_sha256")
    out["runs"] = [{"file": cd._rel(p, out_dir), "sha256": ds.shas[str(p)]} for p in own]
    out.update(files=res["files"], other=res["other"])
    return out


def _entry(s, kind, n, canon) -> dict:
    return dict(zip(SRC_KEYS, (s["name"], str(s["path"]), s.get("sha256"), kind, n, canon)))


def build(version, store=None, root=None, extra=None) -> dict:
    """C2-REG1 (before FIT) or C2-REG2 (R' with the FIT/FEAS/VAL tables in `extra`, keyed by
    split); written by exclusive create; status PASS, INCOMPLETE or LINEAGE."""
    if version not in VERSIONS or (extra and version != "C2-REG2"):
        raise ValueError(f"registry version {version} (extra tables only for C2-REG2)")
    root, out_dir = _root(root), Path(cc.STORE if store is None else store) / "registry"
    mpath, dpath = out_dir / f"{version}.json", out_dir / f"{version}_digests.npz"
    run_dir = out_dir / "runs" / version
    if mpath.exists() or dpath.exists() or run_dir.exists():
        raise FileExistsError(mpath)
    out_dir.mkdir(parents=True, exist_ok=True)
    src = token_sources(root)
    problems, lineage = src["problems"], src["lineage"]
    a_src, seqs = src["a"] if src["a"] is not None else ([], {})
    k_src = src["k"]["sources"] if src["k"] is not None else []
    tokens = a_src + src["b"] + (src["c"] or []) + src["e"]["sources"] + k_src
    x6 = x6_source(root / "x6-stage1-store", run_dir)
    if x6["status"] != "PASS":
        (lineage if x6["status"] == LINEAGE else problems).append(f"x6: {x6['status']}")
    inv = inventory(root, _ok_readers(src, x6["status"] == "PASS"))
    tokens += _try(problems, "f", lambda: kr.source_f(root, inv["inv"], inv["classes"])) or []
    reg = c1_data.build_registry(tokens)
    problems += [f"unreadable: {m['name']}" for m in reg["missing"]]
    digests, seq_union = set(reg["digests"]), set()
    for s in (src["d"] or []) + k_src:
        digests |= s["digests"]
        seq_union |= s["sequence_ids"]
    for v in seqs.values():
        seq_union |= set(np.asarray(v, dtype=np.int64).tolist())
    for tab in (extra or {}).values():
        digests |= cd.table_digests(tab)
        seq_union |= set(np.asarray(tab["sequence_id"], dtype=np.int64).tolist())
    cov = kr.revalidate_coverage(
        src["art"], root, store=src["store_a"], seqs_a=seqs if src["a"] is not None else None
    )
    problems += [] if cov["ok"] else [f"coverage: {cov['missing']}"]
    problems += [f"inventory {v['name']}: {v['reason']}" for v in inv["violations"]]
    status = LINEAGE if lineage else INCOMPLETE if problems else "PASS"
    sorted_d = sorted(digests)
    seq_arr = np.array(sorted(seq_union), dtype=np.int64)
    dsha = hashlib.sha256("\n".join(sorted_d).encode()).hexdigest()
    x6m = _x6_manifest(x6, out_dir)
    canon = [s.get("meta", {}).get("canonicalisation") for s in reg["entries"]]
    sources = [_entry(s, "token", s.get("rows"), c) for s, c in zip(reg["entries"], canon)]
    digest_src = (src["d"] or []) + k_src
    sources += [_entry(s, "digest", len(s["digests"]), "as stored") for s in digest_src]
    e, x6sha = src["e"], x6m["digest_sha256"]
    man = {"version": version, "registry_version": cc.REG_VERSION, "status": status}
    man.update(problems=lineage + problems, n_digests=len(sorted_d), digests_sha256=dsha)
    man["seq_id_union_sha256"] = hashlib.sha256(seq_arr.tobytes()).hexdigest()
    man["x6"], man["union_sha256"] = x6m, hashlib.sha256(f"{dsha}\n{x6sha}".encode()).hexdigest()
    man.update(sources=sources, classes=inv["classes"], coverage=cov, predicates=e["predicates"])
    man["inventory"] = {k: inv[k] for k in ("status", "unlisted", "violations")}
    man.update(sealed_ranges=e["sealed_ranges"], d2a_ranges=e["ranges"])
    man["handoff_validation"] = kr.validate_handoff_json(root / "agent-handoff")
    man["k4b_store"], man["protocol_sha256"] = kr.summary(src["k"]), cc.PROTOCOL_SHA256
    man["built_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest = man
    stage_records.save_npz(dpath, digests=np.array(sorted_d, dtype="<U64"), seq_ids=seq_arr)
    manifest["digest_file_sha256"] = cd.file_sha(dpath)
    stage_records.write_new(mpath, manifest)
    return manifest


# ---- loading and separation (API.md §5.3) ----------------------------------------------------
class Registry:
    def __init__(self, digests, x6, sealed_ranges, predicates, manifest, seq_ids=()):
        self.digests, self.x6, self.manifest = set(digests), x6, manifest
        self.sealed_ranges = {k: tuple(v) for k, v in dict(sealed_ranges).items()}
        self.predicates, self.seq_ids = list(predicates), set(seq_ids)

    @classmethod
    def load(cls, store=None, version="C2-REG1") -> Registry:
        """Re-hashes the digest file and the own x6 runs; the base runs via X6-REG2."""
        reg = Path(cc.STORE if store is None else store) / "registry"
        man = json.loads((reg / f"{version}.json").read_text(encoding="utf-8"))
        dpath = reg / f"{version}_digests.npz"
        if cd.file_sha(dpath) != man.get("digest_file_sha256"):
            raise RegistryLineage(f"{dpath.name} does not re-hash to its manifest")
        with np.load(dpath, allow_pickle=False) as z:
            digests = set(z["digests"].astype(str).tolist())
            seqs = set(np.asarray(z["seq_ids"], dtype=np.int64).tolist())
        x6 = cls._x6(reg, man.get("x6") or {})
        ranges, preds = man.get("sealed_ranges", {}), man.get("predicates", ["sealed_d2a"])
        return cls(digests, x6, ranges, preds, man, seqs)

    @staticmethod
    def _x6(reg, x6m):
        import x6s1_registry as xr

        runs = x6m.get("runs", [])
        for r in runs:
            if cd.file_sha(reg / r["file"]) != r["sha256"]:
                raise RegistryLineage(f"x6 run {r['file']} re-hash mismatch")
        base = None
        if x6m.get("base_manifest_sha256"):
            man = Path(cc.X6S1_STORE) / "registry" / "X6-REG2.json"
            if cd.file_sha(man) != x6m["base_manifest_sha256"]:
                raise RegistryLineage("X6-REG2 manifest differs from the recorded base")
            try:
                base = xr.open_reg(cc.X6S1_STORE, "X6-REG2")
            except xr.RegistryError as exc:
                raise RegistryLineage(repr(exc)) from exc
        if base is None and not runs:
            return None
        paths = (base.paths if base is not None else []) + [reg / r["file"] for r in runs]
        shas = {str(reg / r["file"]): r["sha256"] for r in runs}
        return xr.DigestSet(paths, base=base, shas={**(base.shas if base else {}), **shas})

    def contains(self, hex_digests) -> np.ndarray:
        h = np.asarray(hex_digests).astype(str).reshape(-1)
        out = np.array([d in self.digests for d in h.tolist()], dtype=bool)
        if self.x6 is not None and len(h):
            import x6s1_registry as xr

            out |= self.x6.contains(xr.hex_to_digests(h))
        return out


def separation(reg, tables) -> dict:
    """Every split's four-role union disjoint from R and from every other split; sequence ids
    pairwise disjoint and outside the sealed D-2a ranges; duplicates counted and kept; a
    sealed_d2a predicate hit -> INCONCLUSIVE/REGISTRY_INCOMPLETE (API.md C-11)."""
    names = list(tables)
    U = {s: sorted(cd.table_digests(tables[s])) for s in names}
    coll = {f"{s}_R": int(np.count_nonzero(reg.contains(np.array(U[s], "<U64")))) for s in names}
    coll.update({f"{a}_{b}": len(set(U[a]) & set(U[b])) for a, b in combinations(names, 2)})
    dup = {s: 4 * len(tables[s]["sequence_id"]) - len(U[s]) for s in names}
    ids = {s: np.asarray(tables[s]["sequence_id"], dtype=np.int64) for s in names}
    problems = []
    try:
        check_disjoint(**ids)
    except Exception as exc:  # noqa: BLE001  SPLIT_OVERLAP -> lineage
        problems.append(repr(exc))
    rng = reg.sealed_ranges.values()
    in_ranges = sum(int(((v >= lo) & (v < hi)).sum()) for v in ids.values() for lo, hi in rng)
    if in_ranges:
        problems.append(f"{in_ranges} sequence id(s) inside the sealed D-2a ranges")
    roles = [H for s in names for H in cd.donors4(tables[s]["canonical"])]
    hits = sum(sum(k4b_data.predicate_check(H, reg.predicates)["hits"].values()) for H in roles)
    lineage = any(coll.values()) or problems
    status = LINEAGE if lineage else INCOMPLETE if hits else "PASS"
    out = {"status": status, "collisions": coll, "duplicates": dup, "sealed_ranges": in_ranges}
    out.update(seq_ids="; ".join(problems) or "PASS", predicate={"hits": int(hits)})
    return out


def first_token_ok(table, T, E_canon, pi, split) -> bool:
    """c1_data.first_token_ok on the first symbols of every 4096-row block."""
    first = np.asarray(table["canonical"])[:, 0]
    pE = np.asarray(pi, dtype=np.float64) @ np.asarray(E_canon, dtype=np.float64)
    starts = range(0, len(first), cc.BLOCK)
    return all(c1_data.first_token_ok(first[s : s + cc.BLOCK], pE, split) for s in starts)
