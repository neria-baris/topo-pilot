"""HWSC exposure registry hwsc-reg-v1: K-REG1, K-REG2, REHEARSAL (API.md §4; protocol §3.3-§3.4,
RC-2..RC-4; rulings R-0176-G4, G9). Composes C2ND's frozen readers (R1, R3) unchanged with the new
readers R2, R4-R7 and the stage-C inventory adapter (R8), in nd_registry.build's C2 format."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import fnmatch
import os
from pathlib import Path

import c2_registry
import hwsb_data
import hwsb_registry
import k4b_registry
import nd_registry
import numpy as np
import scores
import stage_records
import x6s1_registry

from topo_pilot.contracts import ArtifactStore, EmissionSpec, ObservationSet
from topo_pilot.contracts.backends import LocalFSBackend

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
VERSIONS = ("K-REG1", "K-REG2", "REHEARSAL")
ARRAYS = (".npz", ".npy", ".pt")
C2_COLS = ("digest_H", "digest_Hp", "digest_Hm")
REG = cc.CONTRACT["registry"]
ART_TYPES = ("WorldSpec", "TransitionSpec", "EmissionSpec", "Checkpoint", "ObservationSet")
STAGE_B = ("hwsb-", "hwsb-dry", "test_hwsb-")


def _new(present=True) -> dict:
    return {"status": "PASS", "digests": set(), "seq_ids": set(), "files": [], "other": [],
            "non_history": [], "non_c2_format": [], "present": present, "known_gaps": []}


def _close(out, lineage=False) -> dict:
    out["status"] = LINEAGE if lineage else INCOMPLETE if out["other"] else "PASS"
    return out


def _rel(base, f) -> str:
    return Path(f).relative_to(base).as_posix()


def _walk_arrays(top, prune=None):
    for dirpath, dirnames, filenames in os.walk(top):
        here = Path(dirpath)
        dirnames[:] = sorted(d for d in dirnames if not (prune and prune(here / d)))
        for name in sorted(filenames):
            if Path(name).suffix in ARRAYS:
                yield here / name


def _meta_type(f):
    """artifact_type of <root>/<T>/<id>/payload.npz|state.pt from its meta.json, else None."""
    if f.parent.parent.name not in ART_TYPES or f.name not in ("payload.npz", "state.pt"):
        return None
    meta = f.parent / "meta.json"
    try:
        t = cc.read_json(meta).get("artifact_type")
    except Exception:  # noqa: BLE001
        return None
    return t if t == f.parent.parent.name else None


# --------------------------------------------------------------------------------- R2 c2nd
def _c2_table(path, out) -> None:
    with np.load(path, allow_pickle=False) as z:
        cols = [c for c in REG["c2nd"]["hist_columns"] if c in z.files]
        if not set(C2_COLS) <= set(cols):
            raise ValueError(f"digest columns {cols}")
        for c in cols:
            out["digests"] |= set(np.asarray(z[c]).astype(str).tolist()) - {""}
        if "sequence_id" in z.files:
            out["seq_ids"] |= set(np.asarray(z["sequence_id"], dtype=np.int64).tolist())
        else:
            out["known_gaps"].append({"path": str(path), "gap": "no sequence_id column"})
        rows = int(len(z["digest_H"]))
    out["files"].append({"path": str(path), "sha256": stage_records.sha256(path), "rows": rows})


def source_c2nd(store=None, bound=None) -> dict:
    store = Path(cc.ROOT / "c2nd-store" if store is None else store)
    bound = REG["c2nd"]["hist_bound"] if bound is None else bound
    out, bad = _new(store.exists()), False
    for rel, want in sorted(bound.items()):
        p = store / rel
        if not p.is_file():
            out["other"].append({"path": str(p), "reason": "missing"})
        elif stage_records.sha256(p) != want:
            bad = True
            out["other"].append({"path": str(p), "reason": "sha256 differs from CONTRACT"})
        else:
            try:
                _c2_table(p, out)
            except Exception as exc:  # noqa: BLE001
                out["other"].append({"path": str(p), "reason": f"unreadable {exc!r}"})
    named = {(store / rel).resolve() for rel in bound}
    pats = REG["c2nd"]["non_history_patterns"]
    for f in _walk_arrays(store) if store.is_dir() else ():
        rel = _rel(store, f)
        parts = rel.split("/")
        if f.resolve() in named:
            continue
        if "sealed" in parts:
            out["non_history"].append({"path": str(f), "bytes": f.stat().st_size,
                                       "class": "SEALED_NAME_ONLY"})
        elif parts[0] == "superseded":
            out["other"].append({"path": str(f), "reason": "array file in superseded/"})
        elif parts[0] == "hist" and fnmatch.fnmatchcase(f.name, "HIST_*.npz"):
            try:
                _c2_table(f, out)
            except Exception as exc:  # noqa: BLE001
                out["other"].append({"path": str(f), "reason": f"unreadable {exc!r}"})
        elif parts[0] == "registry" or any(fnmatch.fnmatchcase(rel, p) for p in pats):
            out["non_history"].append({"path": str(f), "bytes": f.stat().st_size})
        else:
            out["other"].append({"path": str(f), "reason": "unclassified array file"})
    return _close(out, bad)


# --------------------------------------------------------------------------------- R4 hwsb
def source_hwsb(store=None, expected=None) -> dict:
    if expected is None:
        raise ValueError("source_hwsb needs the HANDOFF store_inventory")
    store = Path(cc.HWSB_STORE if store is None else store)
    out = _new(store.exists())
    reg = hwsb_registry.registry_digests(store, expected=dict(expected))
    out["digests"] |= set(reg["digests"])
    out["files"] += reg["sources"]
    out["other"] += [{"path": f["path"], "reason": f["error"]} for f in reg["failures"]]
    hist_sub = ("artifacts/ObservationSet/", "hist/", "superseded/")
    for f in _walk_arrays(store, prune=lambda d: cc.blinded(d, store.parent)
                          or _rel(store, d).lower() == "stages/eval"):
        rel = _rel(store, f)
        if rel.startswith(hist_sub) or cc.blinded(f, store.parent):
            continue
        if _meta_type(f) in ART_TYPES[:4] or any(
                fnmatch.fnmatchcase(rel, p) for p in REG["hwsb"]["chart_patterns"]):
            out["non_history"].append({"path": str(f), "bytes": f.stat().st_size})
        else:
            out["other"].append({"path": str(f), "reason": "unclassified array file"})
    return _close(out)


# ---------------------------------------------------------------------------------- R5 dry
def _dry_paths() -> list:
    fixed = [Path(p) for p in REG["dry_stores"]["paths"] if "<job>" not in p]
    found = sorted(cc.SCRATCH.glob("hwsb-dry*")) + sorted(cc.SCRATCH.glob("hwsc-dry*"))
    return list(dict.fromkeys(fixed + [p for p in found if p.is_dir()]))


def _os_canonical(f, out) -> None:
    root, aid = f.parent.parent.parent, f.parent.name
    st = ArtifactStore(LocalFSBackend(root))
    obs = st.load(ObservationSet, aid, consumer="experiment")
    ems = [p for p in st.meta(aid).parent_ids if st.meta(p).artifact_type == "EmissionSpec"]
    if len(ems) != 1:
        raise ValueError(f"{len(ems)} EmissionSpec parents")
    spec = st.load(EmissionSpec, ems[0], consumer="experiment")
    d = scores.history_digests(hwsb_data.canonical32(obs.tokens, spec.symbol_perm))
    out["digests"] |= set(d)
    out["files"].append({"path": str(f), "kind": "ObservationSet", "rows": len(d)})


def _token_file(f, out) -> None:
    if f.suffix == ".npy":
        members = {"": np.load(f, allow_pickle=False)}
    else:
        with np.load(f, allow_pickle=False) as z:
            members = {k: np.asarray(z[k]) for k in z.files}
    n = 0
    for k, a in members.items():
        if k.startswith("digest"):
            out["digests"] |= set(np.asarray(a).astype(str).reshape(-1).tolist()) - {""}
            n += int(a.size)
        elif k in k4b_registry.HISTORY_KEYS or (a.dtype.kind in "iu" and a.ndim >= 2
                                                and a.shape[-1] in (32, 33)):
            tok = a.reshape(-1, a.shape[-1])[:, :32]
            out["digests"] |= set(scores.history_digests(tok.astype(np.uint8)))
            n += int(len(tok))
    if n:
        out["files"].append({"path": str(f), "rows": n})
    else:
        out["non_history"].append({"path": str(f), "bytes": f.stat().st_size})


def source_dry(paths=None) -> dict:
    paths = _dry_paths() if paths is None else [Path(p) for p in paths]
    must = {"hws-dry", "hwsb-dry", "hwsb-dry-0169", "hwsb-dry-0171"}
    planted = {Path(p["path"]).as_posix().lower(): p for p in
               REG["dry_stores"]["planted_fixtures"]}
    out = _new()
    for top in paths:
        if not top.is_dir():
            if top.name in must:
                out["other"].append({"path": str(top), "reason": "missing"})
            continue
        for f in _walk_arrays(top):
            rel = _rel(top, f)
            if top.name == "hws-dry" and rel.startswith("hist/"):
                continue
            fx = planted.get(f.as_posix().lower())
            if fx and f.stat().st_size == fx["bytes"] and stage_records.sha256(f) == fx["sha256"]:
                out["non_history"].append({"path": str(f), "class": "PLANTED_FIXTURE"})
                continue
            t = _meta_type(f)
            try:
                if t == "ObservationSet" and f.name == "payload.npz":
                    _os_canonical(f, out)
                elif t is not None:
                    out["non_history"].append({"path": str(f), "class": t})
                elif fnmatch.fnmatchcase(f.name, "CHART_*.npz") or fnmatch.fnmatchcase(
                        f.name, "INIT_CHART_*.npz"):
                    out["non_history"].append({"path": str(f), "class": "chart"})
                elif f.suffix == ".pt":
                    out["other"].append({"path": str(f), "reason": ".pt outside artifacts"})
                else:
                    _token_file(f, out)
            except Exception as exc:  # noqa: BLE001  unreadable -> INCOMPLETE
                out["other"].append({"path": str(f), "reason": f"unreadable {exc!r}"})
    return _close(out)


# ---------------------------------------------------------------------------------- R6 scratch
def source_scratch_c(scratch=None) -> dict:
    return nd_registry.source_scratch(cc.SCRATCH if scratch is None else scratch)


def _classify(f) -> tuple:
    if f.suffix == ".pt":
        return "pt", None
    try:
        heads = x6s1_registry._headers(f)
        if x6s1_registry._history_bearing(f):
            for k, dt, sh in heads:
                if k in k4b_registry.HISTORY_KEYS or k.startswith("digest") or (
                        dt.kind in "iu" and len(sh) >= 2 and sh[-1] in (32, 33)):
                    return "history", list(sh)
            return "history", None
        if any(k in k4b_registry.IDENTITY_KEYS for k, _, _ in heads):
            return "identity", None
    except Exception:  # noqa: BLE001
        return "unreadable", None
    return None, None


def scratch_scan(scratch=None) -> dict:
    scratch = Path(cc.SCRATCH if scratch is None else scratch)
    res = {"__top_level__": sorted(str(p) for p in scratch.iterdir()
                                   if p.is_file() and p.suffix in ARRAYS)}
    for top in sorted(p for p in scratch.iterdir() if p.is_dir()):
        full = top.name.startswith(STAGE_B)
        if top.name.startswith("test_") and not top.name.startswith("test_hwsb-"):
            continue
        listed = {}
        for dirpath, dirnames, filenames in os.walk(top):
            here = Path(dirpath)
            if not full:
                dirnames[:] = [d for d in dirnames if not d.startswith("test_")]
            dirnames.sort()
            for name in sorted(filenames):
                f = here / name
                rel = _rel(top, f)
                if name == "meta.json" and here.parent.name == "ObservationSet":
                    listed[rel] = {"class": "os_root", "shape": None}
                elif f.suffix in (".npz", ".npy", ".pt"):
                    cls, shape = _classify(f)
                    if cls:
                        listed[rel] = {"class": cls, "shape": shape}
        res[top.name] = listed
    return res


def _row_for(name, table):
    if name in table:
        return table[name]
    for pat, prefix in (("hwsc-dry-<job>", "hwsc-dry-"), ("test_hwsc-<job>", "test_hwsc-")):
        if name.startswith(prefix) and pat in table:
            return table[pat]
    return None


def _fixture_ok(rel, rec, row) -> bool:
    parts = rel.split("/")[:-1]
    comps = set(row.get("fixture_components", []))
    seg = any(p.startswith(("pt-", "pt2-", "bt", "pytest-of-")) or p in comps for p in parts)
    if rec["class"] == "history":
        return seg and rec["shape"] is not None and rec["shape"][0] <= row["fixture_max_rows"]
    return seg


def scratch_check(scratch=None, table=None, readers_ok=None) -> dict:
    table = REG["scratch_inventory"] if table is None else table
    ok_tags = set(readers_ok or ())
    scan, out = scratch_scan(scratch), _new()
    out["other"] += [{"path": p, "reason": "array file directly under the scratch root"}
                     for p in scan.pop("__top_level__")]
    counts = {}
    for name, listed in scan.items():
        counts[name] = {}
        for rec in listed.values():
            counts[name][rec["class"]] = counts[name].get(rec["class"], 0) + 1
        row = _row_for(name, table)
        if row is None:
            if listed:
                out["other"].append({"path": name, "reason": "no inventory row"})
            continue
        if row["decision"] == "TO_FREEZE" or row.get("frozen_files") == "TO_FREEZE":
            if listed or row["decision"] == "TO_FREEZE":
                out["other"].append({"path": name, "reason": "row not frozen"})
            continue
        frozen = row.get("frozen_files") or {}
        for rel, rec in listed.items():
            want = frozen.get(rel)
            if want != rec["class"]:
                out["other"].append({"path": f"{name}/{rel}", "reason": "not in frozen_files"})
            elif row["decision"] == "EXCLUSION" and "fixture_max_rows" in row and not \
                    _fixture_ok(rel, rec, row):
                out["other"].append({"path": f"{name}/{rel}", "reason": "not a fixture"})
        if row["decision"] in ("READER", "READER_IF_PRESENT") and listed:
            missing = [t for t in row.get("readers", []) if t not in ok_tags]
            if missing:
                out["other"].append({"path": name, "reason": f"readers not PASS: {missing}"})
    out["scan_counts"] = counts
    return _close(out)


# ------------------------------------------------------------------------------------ R7 own
def source_own(store, expected) -> dict:
    store, out = Path(store), _new()
    reg = hwsb_registry.registry_digests(store, expected=dict(expected))
    out["digests"] |= set(reg["digests"])
    out["files"] += reg["sources"]
    out["other"] += [{"path": f["path"], "reason": f["error"]} for f in reg["failures"]]
    sup = store / "superseded"
    for f in sorted(sup.rglob("HIST_*.npz")) if sup.is_dir() else ():
        if f.parent.name not in ("S3", "S7") or f.parent.parent.name != "stages":
            continue
        try:
            with np.load(f, allow_pickle=False) as z:
                canon, dig = np.asarray(z["canon32"]), np.asarray(z["digest"]).astype(str)
                ids = np.asarray(z["seq_ids"], dtype=np.int64)
            if dig.tolist() != scores.history_digests(canon):
                raise ValueError("digest column differs from canon32")
            out["digests"] |= set(dig.tolist())
            out["seq_ids"] |= set(ids.tolist())
            out["files"].append({"path": str(f), "rows": int(len(dig))})
        except Exception as exc:  # noqa: BLE001
            out["other"].append({"path": str(f), "reason": f"unreadable {exc!r}"})
    return _close(out)


# ----------------------------------------------------------------------------- R8 inventory
def inventory_c(root=None, readers=None) -> dict:
    root = Path(cc.ROOT if root is None else root)
    readers = {} if readers is None else readers
    inv = k4b_registry.inventory(root, exclude=tuple(REG["deep_scan_exclude"]))
    inv.pop("hwsc-store", None)
    classes = k4b_registry.classify(inv, readers)
    frozen = {k: v for k, v in REG["inventory"].items() if v.get("decision") != "OWN"}
    violations = []
    for name in sorted(set(inv) | set(frozen)):
        entry = frozen.get(name)
        if entry is not None and entry.get("decision") == "READER_IF_PRESENT":
            if name not in inv:
                continue
            entry = dict(entry, decision="READER")
        why = c2_registry._violation(name, entry, inv.get(name), classes.get(name),
                                     readers.get(name, []))
        if why:
            violations.append({"name": name, "reason": why})
    return {"status": INCOMPLETE if violations else "PASS", "inv": inv, "classes": classes,
            "unlisted": sorted(set(inv) - set(frozen)), "violations": violations}


# ---------------------------------------------------------------------------------- build
from hwsc_registry_build import build, obligation  # noqa: E402,F401  (split by size, erratum)
