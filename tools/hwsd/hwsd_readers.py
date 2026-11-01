"""HWSD registry readers: R9 (hwsc-store layout), R10 (obligation, J11), the K4b table reader and
the superset check (API.md section 4 and section 22). Sources return the hwsc_registry._new shape
and are closed by hwsc_registry._close (looked up at call time)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import json
import os
import re
from pathlib import Path

import hwsb_data
import hwsc_registry
import numpy as np
import scores
import stage_records

from topo_pilot.contracts import ArtifactStore, EmissionSpec, ObservationSet
from topo_pilot.contracts.backends import LocalFSBackend

ARRAYS = (".npz", ".npy", ".pt")
ART_TYPES = ("WorldSpec", "TransitionSpec", "EmissionSpec", "Checkpoint")
_ART_RE = re.compile(r"(?:.*/)?artifacts/(WorldSpec|TransitionSpec|EmissionSpec|Checkpoint)"
                     r"/[0-9a-f]+/(?:payload\.npz|state\.pt)")
_OS_PAYLOAD = re.compile(r"artifacts/ObservationSet/[0-9a-f]+/payload\.npz")
_SUPER_HIST = re.compile(r"superseded/.+/stages/(S3|S7)/HIST_[^/]+\.npz")


def _obl():
    return dc.CONTRACT["obligation"]


def _merge(dst, src) -> bool:
    """Union of two sources; True when src is a lineage failure."""
    dst["digests"] |= set(src.get("digests", ()))
    dst["seq_ids"] |= set(src.get("seq_ids", ()))
    for k in ("files", "other", "non_history", "non_c2_format", "known_gaps"):
        dst[k] += list(src.get(k, ()))
    dst["present"] = bool(dst.get("present")) or bool(src.get("present"))
    return src.get("status") == hwsc_registry.LINEAGE


# ----------------------------------------------------------------------- K4b table, OS reader
def read_k4b_table(path, expected_sha256=None) -> dict:
    path = dc.guard(path)
    if expected_sha256 is not None and stage_records.sha256(path) != expected_sha256:
        raise ValueError("sha256")
    try:
        with np.load(path, allow_pickle=False) as z:
            canon, ids, dig = np.asarray(z["canon32"]), np.asarray(z["seq_ids"]), \
                np.asarray(z["digest"])
    except ValueError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"unreadable table: {exc!r}") from exc
    if canon.ndim != 2 or canon.shape[1] != 32 or canon.dtype.kind not in "iu":
        raise ValueError("canon32 is not an integer [n, 32] array")
    if ids.ndim != 1 or ids.dtype.kind not in "iu" or len(ids) != len(canon):
        raise ValueError("seq_ids")
    if dig.dtype.kind != "U" or dig.shape != (len(canon),):
        raise ValueError("digest")
    if dig.astype(str).tolist() != scores.history_digests(canon.astype(np.uint8)):
        raise ValueError("digest column differs from canon32")
    return {"digests": set(dig.astype(str).tolist()), "seq_ids": set(ids.astype(np.int64).tolist()),
            "n": int(len(canon))}


def os_digests(payload_path) -> list:
    f = Path(dc.guard(payload_path))
    root, aid = f.parent.parent.parent, f.parent.name
    st = ArtifactStore(LocalFSBackend(root))
    obs = st.load(ObservationSet, aid, consumer="experiment")
    ems = [p for p in st.meta(aid).parent_ids if st.meta(p).artifact_type == "EmissionSpec"]
    if len(ems) != 1:
        raise ValueError(f"{len(ems)} EmissionSpec parents")
    spec = st.load(EmissionSpec, ems[0], consumer="experiment")
    return scores.history_digests(hwsb_data.canonical32(obs.tokens, spec.symbol_perm))


def stage_complete_sha(stages_jsonl, rel, stage=None):
    want = None
    for line in dc.read_bytes(stages_jsonl).decode("utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("event") == "STAGE_COMPLETE" and (stage is None or r.get("stage") == stage):
            want = r.get("files", {}).get(rel, want)
    return want


def _art_type_ok(f, folder_type) -> bool:
    try:
        return dc.read_json(Path(f).parent / "meta.json").get("artifact_type") == folder_type
    except Exception:  # noqa: BLE001
        return False


# ---------------------------------------------------------------------------------- R9
def source_hwsc(store=None) -> dict:
    store = Path(dc.HWSC_STORE if store is None else store)
    r9 = dc.CONTRACT["registry"]["r9"]
    out, lineage = hwsc_registry._new(store.exists()), False
    stages = store / "STAGES.jsonl"
    # (b') OBS_INVENTORY: read_obs_inventory verified its sha256 against the CONTRACT row
    inv = dc.read_obs_inventory(store)
    sha = dc.CONTRACT["identity"]["rows"]["obs_inventory"]["sha256"]
    if sha != dc.read_json(store / "RELEASE_A.json").get("obs_inventory_sha256") or sha != \
            stage_complete_sha(stages, "stages/TRAIN/OBS_INVENTORY.json", "TRAIN_INVENTORY"):
        lineage = True
        out["other"].append({"path": "stages/TRAIN/OBS_INVENTORY.json",
                             "reason": "sha256 differs from RELEASE_A or STAGES"})
    # (a) the six ObservationSets and superseded HIST tables
    lineage |= _merge(out, hwsc_registry.source_own(store, inv))
    # (b) the four K4b history tables
    for rel in r9["b"]:
        p = store / rel
        if not p.is_file() or stage_records.sha256(p) != stage_complete_sha(stages, rel):
            lineage = True
            out["other"].append({"path": str(p), "reason": "sha256 differs from STAGES"})
            continue
        try:
            t = read_k4b_table(p)
            out["digests"] |= t["digests"]
            out["seq_ids"] |= t["seq_ids"]
            out["files"].append({"path": str(p), "sha256": stage_records.sha256(p),
                                 "rows": t["n"]})
        except Exception as exc:  # noqa: BLE001
            out["other"].append({"path": str(p), "reason": f"unreadable {exc!r}"})
    # (d), (e), (e'): names only
    rules = [(re.compile(x["regex"]), x["basis"]) for x in r9["non_history_rules"]]
    for dirpath, dirnames, filenames in os.walk(store):
        dirnames[:] = sorted(d for d in dirnames if d != "sealed")
        for name in sorted(filenames):
            f = Path(dirpath) / name
            if f.suffix not in ARRAYS:
                continue
            rel = f.relative_to(store).as_posix()
            if rel in r9["b"] or _OS_PAYLOAD.fullmatch(rel) or _SUPER_HIST.fullmatch(rel):
                continue
            if rel.startswith("stages/TRAIN/"):
                out["other"].append({"path": str(f), "reason": "array file in stages/TRAIN"})
                continue
            hit = next((b for rx, b in rules if rx.fullmatch(rel)), None)
            if hit is None:
                out["other"].append({"path": str(f), "reason": "unclassified array file"})
            elif hit.startswith("artifact"):
                m = _ART_RE.fullmatch(rel)
                if m and _art_type_ok(f, m.group(1)):
                    out["non_history"].append({"path": str(f), "basis": "artifact"})
                else:
                    out["other"].append({"path": str(f), "reason": "artifact without meta.json"})
            else:
                out["non_history"].append({"path": str(f), "basis": hit})
    return hwsc_registry._close(out, lineage)


def superset_check(reg, store=None) -> dict:
    store = Path(dc.HWSC_STORE if store is None else store)
    m = dc.read_json(store / "registry" / "K-REG2.json")
    npz = store / "registry" / "K-REG2_digests.npz"
    if stage_records.sha256(dc.guard(npz)) != m["digest_file_sha256"]:
        return {"status": "FAIL_TECHNICAL/LINEAGE", "n_kreg2": None, "missing": None,
                "n_test": None, "missing_test": None}
    with np.load(npz, allow_pickle=False) as z:
        d2 = np.asarray(z["digests"]).astype(str)
    missing = 0
    for i in range(0, len(d2), 1_000_000):
        missing += int(np.count_nonzero(~np.asarray(reg.contains(d2[i:i + 1_000_000]))))
    test = sorted(read_k4b_table(store / "stages" / "S7" / "HIST_test_b0.npz")["digests"])
    missing_test = int(np.count_nonzero(~np.asarray(reg.contains(test))))
    status = "PASS" if missing == 0 and missing_test == 0 else hwsc_registry.INCOMPLETE
    return {"status": status, "n_kreg2": int(len(d2)), "missing": missing, "n_test": len(test),
            "missing_test": missing_test}


# ---------------------------------------------------------------------------------- R10
def _check_header(o, bad) -> bool:
    c = _obl()
    if not isinstance(o, dict) or o.get("schema") != c["schema"] or \
            set(o) != set(c["fields"]):
        bad("schema or top-level keys")
        return False
    ok = o["track"] in c["tracks"] and o["rule"] == "fail closed" and \
        isinstance(o["files"], list) and isinstance(o["dry_stores"], list) and \
        (o["attempt"] is None or (isinstance(o["attempt"], int)
                                  and not isinstance(o["attempt"], bool) and o["attempt"] >= 1)) \
        and isinstance(o["written_utc"], str) and isinstance(o["name_rules"], list)
    for r in o["name_rules"] if ok else ():
        ok = ok and isinstance(r, dict) and set(r) == {"kind", "regex"} and \
            r["kind"] in c["name_kinds"] and isinstance(r["regex"], str)
    if not ok:
        bad("unknown value in the header")
    return ok


def _check_entry(store, e, rules, bad) -> bool:
    c = _obl()
    if not isinstance(e, dict) or set(e) != set(c["file_fields"]):
        bad("per-file keys")
        return False
    rel, cls, basis = e["relpath"], e["class"], e["basis"]
    ckpt = bool(_ART_RE.fullmatch(rel)) and _ART_RE.fullmatch(rel).group(1) == "Checkpoint"
    good = isinstance(rel, str) and cls in c["classes"] and e["reader"] == c["readers"].get(cls) \
        and isinstance(e["bytes"], int) and not isinstance(e["bytes"], bool)
    if good and cls != "NON_HISTORY":
        good = basis is None and isinstance(e["sha256"], str)
    elif good:
        if basis == "artifact":
            m = _ART_RE.fullmatch(rel)
            good = bool(m) and _art_type_ok(Path(store) / rel, m.group(1))
        elif basis == "registry":
            good = "registry" in rel.split("/")[:-1]
        elif basis == "name_rule":
            good = any(re.fullmatch(r["regex"], rel) for r in rules)
        else:
            good = False
        good = good and (e["sha256"] is None) == (basis == "artifact" and ckpt)
    if good and e["sha256"] is not None:
        good = isinstance(e["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", e["sha256"])
    if not good:
        bad(f"unknown basis, class, reader or sha256 for {rel}")
    return bool(good)


def obligation_check(store, kind="store") -> dict:
    if kind not in ("store", "dry"):
        raise ValueError(f"kind {kind!r}")
    store = Path(store)
    out = hwsc_registry._new(store.exists())
    arrays = []
    for dirpath, dirnames, filenames in os.walk(store):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        arrays += [(Path(dirpath) / n).relative_to(store).as_posix()
                   for n in sorted(filenames) if Path(n).suffix in ARRAYS]

    def bad(why, path=None):
        out["other"].append({"path": str(path or store), "reason": why})

    loaded = []
    for f in sorted(store.glob("REGISTRY_OBLIGATION*.json")) if store.is_dir() else ():
        try:
            o = json.loads(dc.read_bytes(f).decode("utf-8"))
            loaded.append((str(o.get("written_utc", "")) if isinstance(o, dict) else "", f.name,
                           o))
        except Exception as exc:  # noqa: BLE001
            bad(f"obligation unreadable {exc!r}", f)
    if not loaded:
        bad("store present without an obligation")
        return dict(hwsc_registry._close(out), obligation=None)
    _, name, o = max(loaded, key=lambda t: (t[0], t[1]))
    if not _check_header(o, bad):
        return dict(hwsc_registry._close(out), obligation=name)
    listed = {}
    for e in o["files"]:
        if _check_entry(store, e, o["name_rules"], bad):
            if e["relpath"] in listed:
                bad(f"duplicate entry {e['relpath']}")
            listed[e["relpath"]] = e
    for rel in arrays:
        if rel not in listed:
            bad(f"array file not listed: {rel}", store / rel)
    for rel in listed:
        if rel not in arrays:
            bad(f"listed file missing: {rel}", store / rel)
    for rel in sorted(set(arrays) & set(listed)):
        e, f = listed[rel], store / rel
        try:
            if e["class"] == "ObservationSet":
                if stage_records.sha256(f) != e["sha256"]:
                    raise ValueError("sha256")
                d = os_digests(f)
                out["digests"] |= set(d)
                out["files"].append({"path": str(f), "kind": "ObservationSet", "rows": len(d)})
            elif e["class"] == "K4b history table":
                t = read_k4b_table(f, e["sha256"])
                out["digests"] |= t["digests"]
                out["seq_ids"] |= t["seq_ids"]
                out["files"].append({"path": str(f), "rows": t["n"]})
            else:
                if e["sha256"] is not None and stage_records.sha256(f) != e["sha256"]:
                    raise ValueError("sha256")
                out["non_history"].append({"path": str(f), "basis": e["basis"]})
        except Exception as exc:  # noqa: BLE001
            bad(f"unreadable or sha256 differs {exc!r}", f)
    return dict(hwsc_registry._close(out), obligation=name)


def source_hwsu(root=None, scratch=None) -> dict:
    root = Path(dc.ROOT if root is None else root)
    scratch = Path(dc.SCRATCH if scratch is None else scratch)
    out, lineage, stores = hwsc_registry._new(False), False, []
    store = root / "hwsu-store"
    if store.is_dir():
        lineage |= _merge(out, obligation_check(store, "store"))
        stores.append("hwsu-store")
    for folder in sorted(p for p in scratch.iterdir() if p.is_dir()) if scratch.is_dir() else ():
        if not folder.name.startswith("hwsu-"):
            continue
        stores.append(folder.name)
        lineage |= _merge(out, hwsc_registry.source_dry(paths=[folder]))
        if folder.name.startswith("hwsu-dry"):
            lineage |= _merge(out, obligation_check(folder, "dry"))
    out["present"] = bool(stores)
    return dict(hwsc_registry._close(out, lineage), stores=stores)
