"""HWSU name rule, reservations, W2 attestation, obligations, root inventory (API.md §5.1,
§5.5, §5.6, §10; split from hwsu_records by size, re-exported there)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import fnmatch
import hashlib
import json
import os
import re
from pathlib import Path

import hwsu_records as ur
import stage_records
from c1_records import C1GateFailure

ARRAY_SUFFIXES = (".npz", ".npy", ".pt")
ARTIFACT_TYPES = ("WorldSpec", "TransitionSpec", "EmissionSpec", "Checkpoint")


# --------------------------------------------------------------------------- name rule, arrays
def _prefixes(contract=None) -> list:
    c = uc.CONTRACT if contract is None else contract
    out = []
    for blk in c["name_rule"].values():
        out += [p for p in blk.get("prefixes", []) if p not in out]
    return out


def name_class(relpath, contract=None, dry=False):
    rel = str(relpath).replace("\\", "/")
    if not rel.lower().endswith(ARRAY_SUFFIXES):
        raise ValueError(f"not an array file: {relpath!r}")
    parts = rel.split("/")
    base = parts[-1]
    if base.endswith(".npz") and base.startswith("DRYHIST_" if dry else "HIST_"):
        return "K4b history table"
    if parts[0] == "stages" and base.startswith(tuple(_prefixes(contract))):
        return "NON_HISTORY"
    if parts[0] == "registry":
        return "NON_HISTORY_REGISTRY"
    if (len(parts) == 4 and parts[0] == "artifacts" and parts[1] in ARTIFACT_TYPES
            and base in ("payload.npz", "state.pt")):
        return "NON_HISTORY_ARTIFACT"
    return None


def save_array(out, relpath, dry=False, **arrays) -> Path:
    if name_class(relpath, dry=dry) not in ("K4b history table", "NON_HISTORY"):
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"array name outside the rule: {relpath}")
    p = Path(out) / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(p, **arrays)
    return p



# ------------------------------------------------------------------ reservations (J2, J8)
_RES = re.compile(r"^RES-HWSU-(OF|U)(?:-a([0-9]+))?$")


def reservation_file(reservation_id) -> str:
    m = _RES.match(str(reservation_id))
    if not m or (m.group(2) is not None and int(m.group(2)) < 2):
        raise ValueError(f"unknown reservation id {reservation_id!r}")
    return f"RESERVATION_{m.group(1)}" + (f"-a{m.group(2)}" if m.group(2) else "") + ".json"


def write_reservation(store, reservation_id, scope, start_utc, written_by) -> Path:
    p = Path(store) / reservation_file(reservation_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(p, {"id": reservation_id, "scope": scope, "state": "ACTIVE",
                                "start_utc": start_utc, "end_utc": None, "interruptions": [],
                                "job_states": {}, "written_by": written_by})
    return p


def _rel(path, root) -> str:
    return Path(os.path.relpath(Path(path).resolve(), Path(root).resolve())).as_posix()


def end_reservation(store, reservation_id, utc, obligation_path,
                    written_by="hwsu_records.end_reservation") -> Path:
    store = Path(store)
    rf = store / reservation_file(reservation_id)
    end = store / "reservations" / f"{reservation_id}.END.json"
    fail = "FAIL_TECHNICAL/LINEAGE"
    if not rf.is_file() or json.loads(rf.read_text(encoding="utf-8")).get("state") != "ACTIVE":
        raise C1GateFailure(fail, "reservation absent or not ACTIVE")
    if not Path(obligation_path).is_file():
        raise C1GateFailure(fail, "obligation absent")
    if end.exists():
        raise C1GateFailure(fail, "end record exists")
    root = store.resolve().parent
    end.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(end, {
        "schema": "hws-reservation-end-v1", "reservation_id": reservation_id,
        "reservation_file": _rel(rf, root), "reservation_sha256": stage_records.sha256(rf),
        "end_utc": utc, "obligation_file": _rel(obligation_path, root),
        "obligation_sha256": stage_records.sha256(obligation_path), "written_by": written_by})
    return end


def _ended(rec, f, root, w2_end, w2_sha) -> str | None:
    rid, sha = rec.get("id"), stage_records.sha256(f)
    if rid == "RES-HWSC-W2":
        try:
            if uc.sha256_file(w2_end) == w2_sha and uc.read_json(w2_end).get(
                    "reservation_file_sha256") == sha:
                return "a"
        except (OSError, ValueError, C1GateFailure):
            pass
    store = f.parent.parent if f.parent.name == "reservations" else f.parent
    e = store / "reservations" / f"{rid}.END.json"
    try:
        r = uc.read_json(e, root)
        ob = Path(root) / r["obligation_file"]
        if (r.get("schema") == "hws-reservation-end-v1" and r.get("reservation_sha256") == sha
                and r.get("obligation_sha256") == uc.sha256_file(ob, root)):
            return "b"
    except (OSError, ValueError, KeyError, C1GateFailure):
        pass
    return None


def w2_attestation(root, own=None, w2_end=None, w2_end_sha256=None) -> dict:
    root = Path(root)
    w2_end = uc.MAILBOX / "records" / "HWSC_W2_END.json" if w2_end is None else w2_end
    w2_sha = (uc.CONTRACT["authority"]["records"]["HWSC_W2_END"]["sha256"]
              if w2_end_sha256 is None else w2_end_sha256)
    files = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        files += sorted(d.glob("RESERVATION*.json")) + sorted((d / "reservations").glob("*.json"))
    active, ended, live = [], {}, []
    for f in files:
        if f.name.endswith(".END.json") or uc.blinded(f, root):
            continue
        try:
            rec = uc.read_json(f, root)
        except (OSError, ValueError):
            live.append(str(f))
            continue
        if not isinstance(rec, dict) or rec.get("state") != "ACTIVE" or (
                own is not None and rec.get("id") == own):
            continue
        rid = rec.get("id", str(f))
        active.append(rid)
        how = _ended(rec, f, root, w2_end, w2_sha)
        if how:
            ended[rid] = how
        else:
            live.append(rid)
    return {"status": "PASS" if not live else "INCONCLUSIVE/AUTHORITY", "active": active,
            "ended": ended, "live": live}


# ------------------------------------------------------------------ obligations (J10)
def obligation_name(job, attempt=None, final=False) -> str:
    if final:
        return "REGISTRY_OBLIGATION.json"
    if job == "OF" and attempt is None:
        return "REGISTRY_OBLIGATION_OF.json"
    if not isinstance(attempt, int) or attempt < 1:
        raise ValueError(f"attempt must be an int >= 1, got {attempt!r}")
    return f"REGISTRY_OBLIGATION_{job}-a{attempt}.json"


def write_obligation(store, name, job, written_by, dry=False, contract=None, attempt=None,
                     reservation_id=None, dry_stores=()) -> Path:
    c = uc.CONTRACT if contract is None else contract
    ob, store = c["obligation"], Path(store)
    arrays = sorted(p.relative_to(store).as_posix() for p in store.rglob("*")
                    if p.is_file() and p.suffix in ARRAY_SUFFIXES)
    files = []
    for rel in arrays:
        cls = name_class(rel, c, dry)
        if cls is None:
            raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"array outside the name rule: {rel}")
        f = store / rel
        ckpt = cls == "NON_HISTORY_ARTIFACT" and rel.split("/")[1] == "Checkpoint"
        e = {"relpath": rel, "sha256": None if ckpt else uc.sha256_file(f),
             "bytes": f.stat().st_size, "class": "NON_HISTORY", "reader": None}
        if cls == "K4b history table":
            e.update({"class": cls, "reader": ob["readers"][cls], "basis": None})
        else:
            e["basis"] = {"NON_HISTORY_ARTIFACT": "artifact", "NON_HISTORY_REGISTRY": "registry",
                          "NON_HISTORY": "name_rule"}[cls]
        files.append(e)
    rec = {"schema": ob["schema"], "store": store.resolve().as_posix(), "track": ob["track"],
           "job": job, "attempt": attempt, "written_utc": ur.utc(), "written_by": written_by,
           "reservation_id": reservation_id, "name_rules": [dict(r) for r in ob["name_rules"]],
           "dry_stores": [Path(d).as_posix() for d in dry_stores], "files": files,
           "rule": ob["rule"]}
    p = store / name
    stage_records.write_new(p, rec)
    return p


def read_obligation(store, contract=None) -> dict:
    """J11 reader rule: the newest obligation by written_utc governs (API.md J11 erratum)."""
    c = (uc.CONTRACT if contract is None else contract)["obligation"]
    store, probs = Path(store), []
    arrays = sorted(p.relative_to(store).as_posix() for p in store.rglob("*")
                    if p.is_file() and p.suffix in ARRAY_SUFFIXES)
    recs = []
    for f in sorted(store.glob("REGISTRY_OBLIGATION*.json")):
        try:
            recs.append(json.loads(f.read_text(encoding="utf-8")))
        except ValueError:
            probs.append(f"unreadable {f.name}")
    incomplete = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
    if not recs:
        return {"status": incomplete if arrays or probs else "PASS",
                "problems": probs + (["no obligation"] if arrays else [])}
    rec = max(recs, key=lambda r: str(r.get("written_utc")) if isinstance(r, dict) else "")
    if not isinstance(rec, dict) or set(rec) != set(c["top_level"]) or not isinstance(
            rec["files"], list) or rec["schema"] != c["schema"] or rec["rule"] != c["rule"]:
        return {"status": incomplete, "problems": probs + ["top-level keys or values"]}
    try:
        rules = [re.compile(r["regex"]) for r in rec["name_rules"]
                 if set(r) == {"kind", "regex"} and r["kind"] in c["name_rule_kinds"]]
    except (re.error, TypeError):
        rules = []
    if len(rules) != len(rec["name_rules"]):
        probs.append("name_rules")
    listed = {}
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
        f = store / e["relpath"]
        if e["sha256"] is not None and (not f.is_file() or uc.sha256_file(f) != e["sha256"]):
            probs.append(f"sha256: {e['relpath']}")
    probs += [f"unlisted: {a}" for a in arrays if a not in listed]
    return {"status": incomplete if probs else "PASS", "problems": probs}


# ------------------------------------------------------------------ root inventory (§8.4)
def root_inventory(root=uc.ROOT) -> dict:
    root = Path(root)
    rule = uc.CONTRACT["hygiene"]["root_rule"]
    rel_prunes = tuple(rule["prune_paths"])

    def pruned(rel: str, name: str) -> bool:
        low = name.lower()
        return (name in rule["prune_names"] or low.startswith("00_read_me_first")
                or any(rel == q or rel.startswith(q + "/") for q in rel_prunes)
                or any(fnmatch.fnmatchcase(name, g) for g in rule["prune_components"]))

    out = {}
    for top in sorted(p for p in os.listdir(root) if (root / p).is_dir()):
        if pruned(top, top):
            out[top] = {"listed": False, "reason": "pruned unlisted (blinded/track-D)"}
            continue
        arrays, prot, obs, sealed = [], 0, 0, 0
        for folder, dirs, files in os.walk(root / top, topdown=True):
            rel_f = Path(folder).relative_to(root).as_posix()
            keep = []
            for d in sorted(dirs):
                if d == "sealed":
                    sealed += 1
                if not pruned(f"{rel_f}/{d}", d):
                    keep.append(d)
            dirs[:] = keep
            if Path(folder).parent.name == "ObservationSet" and "meta.json" in files:
                obs += 1
            hist = "hist" in rel_f.split("/")
            for f in files:
                if f.lower().endswith(ARRAY_SUFFIXES):
                    arrays.append(f"{rel_f}/{f}")
                if hist or f in ("payload.npz", "state.pt") or f.startswith("HIST_"):
                    prot += 1
        digest = hashlib.sha256("\n".join(sorted(arrays)).encode()).hexdigest()
        out[top] = {"listed": True, "n_array_files": len(arrays), "n_protected_names": prot,
                    "n_observationset_roots": obs, "n_sealed_dirs_pruned": sealed,
                    "array_relpaths_sha256": digest}
    return out
