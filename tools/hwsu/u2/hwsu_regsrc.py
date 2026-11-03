"""HWSU registry readers: U2 (stage C), U2', U5, U6, U8 and the J10 obligation reader
(API_U2.md section 3; protocol 8.2-8.3). Split from hwsu_registry by size (API erratum); every
name stays reachable as hwsu_registry.<name>."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_model as um
import hwsu_pairs as up
import u2  # noqa: F401
import json
import os
import re
from pathlib import Path

import hwsb_registry
import hwsc_registry
import k4b_data
import numpy as np
import stage_records

INC, LIN = "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
ARR = (".npz", ".npy", ".pt")
ART_T = ("WorldSpec", "TransitionSpec", "EmissionSpec", "Checkpoint")


def _new(present=True) -> dict:
    return {"status": "PASS", "digests": set(), "seq_ids": set(), "files": [], "other": [],
            "non_history": [], "non_c2_format": [], "present": present, "known_gaps": []}


def _close(out, lineage=False) -> dict:
    out["status"] = LIN if lineage else INC if out["other"] else "PASS"
    return out


def read_hist_table(path) -> tuple:
    """K4b history table: digest column re-derived from canon32 (k4b_data.digests)."""
    with np.load(path, allow_pickle=False) as z:
        canon, dig = np.asarray(z["canon32"]), np.asarray(z["digest"]).astype(str).tolist()
        ids = np.asarray(z["seq_ids"], dtype=np.int64)
    if dig != k4b_data.digests(canon) or len(ids) != len(dig):
        raise ValueError("digest column differs from canon32")
    return dig, ids.tolist()


def _take(out, f, rel) -> None:
    dig, ids = read_hist_table(f)
    out["digests"] |= set(dig)
    out["seq_ids"] |= set(ids)
    out["files"].append({"path": rel, "rows": len(dig)})



# ----------------------------------------------------------------------- U2, U8, S-2
def _class_c(rel, store) -> str | None:
    p = rel.split("/")
    name = p[-1]
    if p[0] == "superseded" and len(p) >= 4 and p[2] == "stages" and p[3] in ("S3", "S7") \
            and name.startswith("HIST_"):
        return "covered"
    if p[0] == "superseded" and len(p) >= 4 and p[2] == "artifacts":
        p = p[2:]
    if p[0] == "artifacts" and len(p) == 4 and p[1] == "ObservationSet":
        return "covered"
    if p[0] == "artifacts" and len(p) == 4 and p[1] in ART_T:
        try:
            meta = uc.read_json(store / "/".join(rel.split("/")[:-1]) / "meta.json")
        except (OSError, ValueError):
            return None
        return "NON_HISTORY_ARTIFACT" if meta.get("artifact_type") == p[1] else None
    if p[0] == "registry":
        return "NON_HISTORY_REGISTRY"
    if p[0] == "stages" and len(p) >= 3 and (
            (p[1] == "S4" and name.startswith("ORACLE_"))
            or (p[1] == "S4a" and name.startswith(("ACTS_", "CHART_", "DECODER_", "INIT_CHART_")))):
        return "NON_HISTORY"
    return "NON_HISTORY" if p[0] in ("logs", "tmp") else None


def source_hwsc(store, contract=None) -> dict:
    C, store, out = um._c(contract), Path(store), _new()
    oi = C["obs_inventory"]
    try:
        p = store / oi["relpath"]
        sha = uc.sha256_file(p)
        if sha != oi["sha256"] or sha != um.stage_complete_sha(store, oi["stage"], oi["relpath"]):
            raise ValueError("OBS_INVENTORY.json does not re-hash")
        own = hwsc_registry.source_own(store, uc.read_json(p))
        for k in ("digests", "seq_ids"):
            out[k] |= own[k]
        out["files"] += own["files"]
        out["other"] += own["other"]
    except Exception as exc:  # noqa: BLE001  fail closed
        out["other"].append({"path": oi["relpath"], "reason": f"U2 own inventory: {exc!r}"})
    for rel, stage in C["u2_hist"].items():
        try:
            f = store / rel
            if stage_records.sha256(f) != um.stage_complete_sha(store, stage, rel):
                raise ValueError("sha256 differs from STAGE_COMPLETE")
            _take(out, f, rel)
        except Exception as exc:  # noqa: BLE001
            out["other"].append({"path": rel, "reason": f"U2 history table: {exc!r}"})
    for dirpath, dirnames, filenames in os.walk(store):
        dirnames[:] = sorted(d for d in dirnames
                             if d != "sealed" and not uc.blinded(Path(dirpath) / d))
        for name in sorted(filenames):
            f = Path(dirpath) / name
            rel = f.relative_to(store).as_posix()
            if f.suffix not in ARR or rel in C["u2_hist"]:
                continue
            c = _class_c(rel, store)
            if c is None:
                out["other"].append({"path": rel, "reason": "unclassified array file"})
            elif c != "covered":
                out["non_history"].append(rel)
    return _close(out)


def source_kreg2_c(store, contract=None) -> dict:
    k = um._c(contract)["k_reg2"]
    p = Path(store) / k["digest_file"]
    try:
        if stage_records.sha256(p) != k["digest_file_sha256"]:
            raise ValueError("K-REG2 digest file does not re-hash")
        with np.load(p, allow_pickle=False) as z:
            dig, ids = np.asarray(z["digests"]).astype("<U64"), np.asarray(z["seq_ids"])
        return {"status": "PASS", "digests": dig, "seq_ids": ids, "n": int(len(dig))}
    except Exception as exc:  # noqa: BLE001
        return {"status": INC, "digests": np.array([], dtype="<U64"), "seq_ids": np.array([]),
                "n": 0, "reason": repr(exc)}


def superset_diagnostic(union_sorted, kreg2_sorted, chunk=1_000_000) -> dict:
    u, k = np.asarray(union_sorted).astype("<U64"), np.asarray(kreg2_sorted).astype("<U64")
    n, head = 0, []
    for s in range(0, len(k), int(chunk)):
        c = k[s:s + int(chunk)]
        if len(u):
            idx = np.minimum(np.searchsorted(u, c), len(u) - 1)
            miss = c[u[idx] != c]
        else:
            miss = c
        n += int(len(miss))
        head += miss.tolist()[:max(0, 100 - len(head))]
    return {"n_missing": n, "missing_head": head}


# ------------------------------------------------------------------ U6 own, J10 readers
def source_own_u(store, expected, contract=None) -> dict:
    store, out = Path(store), _new()
    listed = {}
    for e in stage_records.stages_so_far(store):
        if e.get("event") == "STAGE_COMPLETE":
            listed.update({r: h for r, h in e.get("files", {}).items()
                           if Path(r).name.startswith(("HIST_", "DRYHIST_"))})
    for rel in expected or ():
        if rel not in listed:
            out["other"].append({"path": rel, "reason": "required history table not listed"})
    for rel, want in listed.items():
        try:
            f = store / rel
            if stage_records.sha256(f) != want:
                raise ValueError("sha256 differs from STAGE_COMPLETE")
            _take(out, f, rel)
        except Exception as exc:  # noqa: BLE001
            out["other"].append({"path": rel, "reason": repr(exc)})
    for f in sorted(store.rglob("*")):
        rel = f.relative_to(store).as_posix()
        if f.is_file() and f.suffix in ARR and f.name.startswith(("HIST_", "DRYHIST_")) \
                and rel not in listed and not rel.startswith("superseded/"):
            out["other"].append({"path": rel, "reason": "unlisted history table"})
    return _close(out)


def read_obligation_u2(store, root=uc.ROOT, contract=None) -> dict:
    c = (uc.CONTRACT if contract is None else contract)["obligation"]
    store, probs, recs = Path(store), [], []
    arrays = sorted(p.relative_to(store).as_posix() for p in store.rglob("*")
                    if p.is_file() and p.suffix in ARR)
    for f in sorted(store.glob("REGISTRY_OBLIGATION*.json")):
        try:
            recs.append(json.loads(f.read_text(encoding="utf-8")))
        except ValueError:
            probs.append(f"unreadable {f.name}")
    if not recs:
        return {"status": INC if arrays or probs else "PASS",
                "problems": probs + (["no obligation"] if arrays else []), "history": []}
    rec = max(recs, key=lambda r: str(r.get("written_utc")) if isinstance(r, dict) else "")
    if not isinstance(rec, dict) or set(rec) != set(c["top_level"]) or not isinstance(
            rec["files"], list) or rec["schema"] != c["schema"] or rec["rule"] != c["rule"] \
            or rec["track"] not in ("U", "D"):
        return {"status": INC, "problems": probs + ["top-level keys or values"], "history": []}
    try:
        rules = [re.compile(r["regex"]) for r in rec["name_rules"]
                 if set(r) == {"kind", "regex"} and r["kind"] in c["name_rule_kinds"]]
    except (re.error, TypeError):
        rules = []
    if len(rules) != len(rec["name_rules"]):
        probs.append("name_rules")
    listed, hist = {}, []
    for e in rec["files"]:
        if not isinstance(e, dict) or set(e) != set(c["file_keys"]):
            probs.append(f"file keys: {e!r}"[:120])
            continue
        listed[e["relpath"]] = e
        if e["class"] not in c["classes"] or e["reader"] != c["readers"].get(e["class"]):
            probs.append(f"class/reader: {e['relpath']}")
        if (e["class"] == "NON_HISTORY") != (e["basis"] is not None) or (
                e["basis"] is not None and e["basis"] not in c["bases"]):
            probs.append(f"basis: {e['relpath']}")
        elif e["basis"] == "name_rule" and not any(r.fullmatch(e["relpath"]) for r in rules):
            probs.append(f"no name rule matches: {e['relpath']}")
        sha, f = e["sha256"], store / e["relpath"]
        if sha is None and not e["relpath"].startswith("artifacts/Checkpoint/"):
            probs.append(f"sha256: {e['relpath']}")
        elif sha is not None and (not f.is_file() or stage_records.sha256(f) != sha):
            probs.append(f"sha256: {e['relpath']}")
        if e["class"] != "NON_HISTORY":
            hist.append({"relpath": e["relpath"], "class": e["class"], "reader": e["reader"]})
    probs += [f"unlisted: {a}" for a in arrays if a not in listed]
    return {"status": INC if probs else "PASS", "problems": probs, "history": hist}


def _read_store(store, root, out, tag) -> None:
    r = read_obligation_u2(store, root)
    if r["status"] != "PASS":
        out["other"].append({"path": str(store), "reason": f"{tag}: {r['problems'][:5]}"})
        return
    for h in r["history"]:
        try:
            if h["class"] == "ObservationSet":
                reg = hwsb_registry.registry_digests(store)
                if reg["status"] != "PASS":
                    raise ValueError(f"ObservationSets: {reg['failures'][:3]}")
                out["digests"] |= set(reg["digests"])
            else:
                _take(out, Path(store) / h["relpath"], h["relpath"])
        except Exception as exc:  # noqa: BLE001
            out["other"].append({"path": str(Path(store) / h["relpath"]), "reason": repr(exc)})


def source_hwsd(root, scratch, contract=None) -> dict:
    root, scratch = Path(root), Path(scratch)
    store = root / "hwsd-store"
    out = _new(present=store.is_dir())
    if store.is_dir():
        _read_store(store, root, out, "U5")
    dirs = sorted(scratch.glob("hwsd-dry*")) + sorted(scratch.glob("test_hwsd-*"))
    for d in (d for d in dirs if d.is_dir()):
        if any(p.suffix in ARR for p in d.rglob("*") if p.is_file()):
            _read_store(d, root, out, "U5")
    return _close(out)


def _registered_ids() -> set:
    ids = set()
    for split, blocks, arms in (("fit", (0, 1), ("s",)), ("val", (0,), ("a1", "a2")),
                                ("test", tuple(range(8)), ("a1", "a2"))):
        for b in blocks:
            for a in arms:
                ids |= set(int(x) for x in up.seq_ids(uc.SCOPE_U, split, b, a, uc.BLOCK_OF))
    return ids


def source_own_dry(scratch, contract=None) -> dict:
    scratch, out = Path(scratch), _new()
    for d in sorted(p for p in scratch.glob("hwsu-dry*") if p.is_dir()):
        _read_store(d, uc.ROOT, out, "U2prime")
    reg_ids = None
    for d in sorted(p for p in scratch.glob("test_hwsu-*") if p.is_dir()):
        for f in sorted(d.rglob("*")):
            rel = f"{d.name}/{f.relative_to(d).as_posix()}"
            if f.is_file() and f.name.startswith(("HIST_", "DRYHIST_")) and f.suffix in ARR:
                out["other"].append({"path": rel, "reason": "HIST-named file in a fixture root"})
            elif f.is_file() and f.name == "meta.json" and f.parent.parent.name == "ObservationSet":
                out["other"].append({"path": rel, "reason": "ObservationSet root in a fixture"})
            elif f.is_file() and f.suffix == ".npz":
                try:
                    with np.load(f, allow_pickle=False) as z:
                        key = next((k for k in ("seq_ids", "sequence_id", "ids") if k in z.files),
                                   None)
                        got = set(np.asarray(z[key]).ravel().tolist()) if key else set()
                    reg_ids = _registered_ids() if reg_ids is None and got else reg_ids
                    if got & (reg_ids or set()):
                        out["other"].append({"path": rel, "reason": "registered-scope ids"})
                except Exception:  # noqa: BLE001  not a table; fixture arrays are not history
                    pass
    return _close(out)
