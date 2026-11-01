"""HWSD K-REG-D: the scratch scan and check mirrors, the hwsd-dry type rule, inventory_d, build_d
and load_d (API.md section 5; DRD8). Mirrors hwsc_scratch / hwsc_registry.inventory_c with the
hwsd changes; reused functions are looked up at call time."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import os
import re
import time
from pathlib import Path

import c2_registry
import hwsc_config
import hwsc_drystore
import hwsc_registry
import hwsc_registry_build
import hwsc_scratch
import hwsd_readers
import k4b_registry
import numpy as np
import stage_records
import x6s1_registry
from c1_records import C1GateFailure

BLINDED_TOP = "hwsc-job-"
_CASE, _UTC = re.compile(r"DRD\d+"), re.compile(r"\d{8}T\d{6}Z")
_RUN = re.compile(r"run_\d{5}\.npy")
_SPLIT_FILE = re.compile(r"DRYHIST_(lgate|cal|val|test)_b0\.npz")
_PATTERNS = (("hwsc-dry-<job>", "hwsc-dry-"), ("test_hwsc-<job>", "test_hwsc-"),
             ("hwsd-dry-<job>", "hwsd-dry-"), ("hwsd-kd-<job>", "hwsd-kd-"),
             ("test_hwsd-<job>", "test_hwsd-"), ("test_hwsu-<job>", "test_hwsu-"),
             ("hwsu-*", "hwsu-"))


# --------------------------------------------------------------------------- scratch scan
def scratch_scan_d(scratch=None) -> dict:
    scratch = Path(dc.SCRATCH if scratch is None else scratch)
    res = {"__top_level__": sorted(str(p) for p in scratch.iterdir()
                                   if p.is_file() and p.suffix in hwsc_registry.ARRAYS)}
    for top in sorted(p for p in scratch.iterdir() if p.is_dir()):
        blind = top.name.startswith(BLINDED_TOP)
        full = top.name.startswith(hwsc_registry.STAGE_B)
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
                rel = hwsc_registry._rel(top, f)
                if blind:
                    if f.suffix in hwsc_registry.ARRAYS:
                        listed[rel] = {"class": "blinded_array", "shape": None}
                elif name == "meta.json" and here.parent.name == "ObservationSet":
                    listed[rel] = {"class": "os_root", "shape": None}
                elif f.suffix in hwsc_registry.ARRAYS:
                    cls, shape = hwsc_scratch._classify(f)
                    if cls:
                        listed[rel] = {"class": cls, "shape": shape}
        res[top.name] = listed
    return res


def row_for_d(name, table):
    if name in table:
        return table[name]
    for pat, prefix in _PATTERNS:
        if name.startswith(prefix) and pat in table:
            return table[pat]
    return None


# ------------------------------------------------------------------- hwsd-dry type rule
def _heads(f) -> dict:
    return {k: (dt, tuple(sh)) for k, dt, sh in x6s1_registry._headers(f)}


def _os_parent_ok(os_dir) -> bool:
    def meta(p):
        try:
            return dc.read_json(p)
        except Exception:  # noqa: BLE001
            return {}

    os_dir = Path(os_dir)
    arts = os_dir.parent.parent
    ems = [p for p in meta(os_dir / "meta.json").get("parent_ids", [])
           if meta(arts / "EmissionSpec" / p / "meta.json").get("artifact_type") == "EmissionSpec"]
    return len(ems) == 1


def dry_class_d(store, rel, rec):
    parts = rel.split("/")
    if len(parts) < 3 or not _CASE.fullmatch(parts[0]) or not _UTC.fullmatch(parts[1]):
        return None
    f, tail, cls = Path(store) / rel, parts[2:], rec["class"]
    try:
        if len(tail) == 4 and tail[0] == "artifacts":
            if tail[1] == "ObservationSet" and tail[3] in ("meta.json", "payload.npz") and \
                    cls in ("os_root", "history") and _os_parent_ok(f.parent):
                return "R5"
            if tail[1] == "Checkpoint" and (tail[3] == "payload.npz" or (
                    tail[3] == "state.pt" and cls == "pt")):
                return "CHECKPOINT"
            return None
        if len(tail) == 3 and tail[:2] == ["stages", "S3"] and _SPLIT_FILE.fullmatch(tail[2]) \
                and cls == "history":
            dt, sh = _heads(f)["canon32"]
            return "R5" if dt.kind in "iu" and sh and sh[-1] == 32 else None
        if tail == ["registry", "K-REG1_digests.npz"]:
            h = _heads(f)
            return "REGISTRY_FIXTURE" if set(h) == {"digests", "seq_ids"} and \
                h["digests"][0].kind == "U" else None
        if len(tail) == 4 and tail[:3] == ["registry", "runs", "K-REG1"] and \
                _RUN.fullmatch(tail[3]):
            dt, sh = _heads(f)[""]
            return "REGISTRY_FIXTURE" if dt == np.uint8 and len(sh) == 2 and sh[1] == 32 \
                else None
    except Exception:  # noqa: BLE001  an unreadable header is not an allowed class
        return None
    return None


# ------------------------------------------------------------------------ scratch check
def _fixture_ok(rel, rec, row) -> bool:
    parts = rel.split("/")[:-1]
    comps = set(row.get("fixture_components", []))
    seg = any(p.startswith(("pt-", "pt2-", "bt", "pytest-of-")) or p in comps for p in parts)
    if rec["class"] == "history":
        return seg and rec["shape"] is not None and rec["shape"][0] <= row["fixture_max_rows"]
    return seg


def _hash_ok(path, want) -> bool:
    return (path.is_file() and path.stat().st_size == int(want["bytes"])
            and stage_records.sha256(path) == want["sha256"]
            and want.get("reason_class") in hwsc_scratch.HASH_CLASSES)


def _check_row_d(name, listed, row, ok_tags, scratch, out) -> None:
    frozen = row.get("frozen_files") or {}
    covered, hashed = row.get("covered") or {}, row.get("hash_frozen") or {}
    for rel, rec in listed.items():
        where = f"{name}/{rel}"
        if frozen.get(rel) != rec["class"]:
            out["other"].append({"path": where, "reason": "not in frozen_files"})
        elif rel in hashed:
            if not _hash_ok(Path(scratch) / name / rel, hashed[rel]):
                out["other"].append({"path": where, "reason": "HASH_FROZEN sha256 differs"})
        elif rel in covered:
            if covered[rel] not in ok_tags:
                out["other"].append({"path": where, "reason": f"reader {covered[rel]} not PASS"})
        elif row["decision"] == "EXCLUSION" and "fixture_max_rows" in row and not \
                _fixture_ok(rel, rec, row):
            out["other"].append({"path": where, "reason": "not a fixture"})
    if row["decision"] in ("READER", "READER_IF_PRESENT") and listed:
        missing = [t for t in row.get("readers", []) if t not in ok_tags]
        if missing:
            out["other"].append({"path": name, "reason": f"readers not PASS: {missing}"})


def scratch_check_d(scratch=None, table=None, readers_ok=None) -> dict:
    scratch = Path(dc.SCRATCH if scratch is None else scratch)
    table = dc.scratch_table() if table is None else table
    ok_tags = set(readers_ok or ())
    scan, out = scratch_scan_d(scratch), hwsc_registry._new()
    out["other"] += [{"path": p, "reason": "array file directly under the scratch root"}
                     for p in scan.pop("__top_level__")]
    counts = {}
    for name, listed in scan.items():
        counts[name] = {}
        for rec in listed.values():
            counts[name][rec["class"]] = counts[name].get(rec["class"], 0) + 1
        row = row_for_d(name, table)
        if row is None:
            if listed:
                out["other"].append({"path": name, "reason": "no inventory row"})
            continue
        if row["decision"] == "TO_FREEZE" or row.get("frozen_files") == "TO_FREEZE":
            if listed or row["decision"] == "TO_FREEZE":
                out["other"].append({"path": name, "reason": "row not frozen"})
            continue
        if name.startswith("hwsc-dry"):
            hwsc_drystore.check_store(scratch / name, listed, ok_tags, out)
        elif name.startswith("hwsd-dry"):
            for rel, rec in listed.items():
                cls = dry_class_d(scratch / name, rel, rec)
                if cls is None:
                    out["other"].append({"path": f"{name}/{rel}", "reason":
                                         "not allowed by the hwsd-dry type rule"})
                elif cls == "R5" and "R5" not in ok_tags:
                    out["other"].append({"path": f"{name}/{rel}", "reason": "reader R5 not PASS"})
        elif name.startswith("hwsu-"):
            for rel in listed:
                if "R10" not in ok_tags:
                    out["other"].append({"path": f"{name}/{rel}", "reason": "reader R10 not PASS"})
        else:
            _check_row_d(name, listed, row, ok_tags, scratch, out)
    out["scan_counts"] = counts
    return hwsc_registry._close(out)


# --------------------------------------------------------------------------- inventory
def inventory_d(root=None, readers=None, table=None) -> dict:
    root = Path(dc.ROOT if root is None else root)
    readers = {} if readers is None else readers
    table = dc.root_table() if table is None else table
    inv = k4b_registry.inventory(
        root, exclude=tuple(dc.CONTRACT["registry"]["deep_scan_exclude"]))
    for name, row in table.items():
        if row.get("decision") == "OWN":
            inv.pop(name, None)
    classes = k4b_registry.classify(inv, readers)
    frozen = {k: v for k, v in table.items() if v.get("decision") != "OWN"}
    violations = []
    for name in sorted(set(inv) | set(frozen)):
        entry = frozen.get(name)
        if entry is not None and entry.get("decision") == "TO_FREEZE":
            violations.append({"name": name, "reason": "row not frozen"})
            continue
        if entry is not None and entry.get("decision") == "READER_IF_PRESENT":
            if name not in inv:
                continue
            entry = dict(entry, decision="READER")
        why = c2_registry._violation(name, entry, inv.get(name), classes.get(name),
                                     readers.get(name, []))
        if why:
            violations.append({"name": name, "reason": why})
    return {"status": hwsc_registry.INCOMPLETE if violations else "PASS", "inv": inv,
            "classes": classes, "unlisted": sorted(set(inv) - set(frozen)),
            "violations": violations}


# ------------------------------------------------------------------------ build, load
def _summary(r) -> dict:
    keys = ("status", "files", "other", "non_c2_format", "non_history", "present", "known_gaps")
    return dict({k: r.get(k) for k in keys}, n=len(r.get("digests", ())))


def _merged(*srcs) -> dict:
    out, lineage = hwsc_registry._new(), False
    for s in srcs:
        lineage |= hwsd_readers._merge(out, s)
    bad = [s for s in srcs if s["status"] != "PASS"]
    out["status"] = hwsc_registry.LINEAGE if lineage else \
        (hwsc_registry.INCOMPLETE if bad else "PASS")
    return out


def build_d(out_dir, root=None, scratch=None, handoff=None, sources=None) -> dict:
    out_dir = Path(out_dir)
    if out_dir.name != "registry":
        raise ValueError("out_dir must be <store>/registry")
    wrapper = out_dir / "K-REG-D.json"
    if wrapper.exists():
        raise FileExistsError(wrapper)
    root = Path(dc.ROOT if root is None else root)
    scratch = Path(dc.SCRATCH if scratch is None else scratch)
    handoff = hwsc_config.load_handoff() if handoff is None else handoff
    t0, state, given = time.process_time(), {}, dict(sources or {})

    def own():
        r9 = hwsd_readers.source_hwsc(root / "hwsc-store")
        r10 = hwsd_readers.source_hwsu(root, scratch)
        state["r9"], state["r10"] = r9, r10
        return _merged(r9, r10)

    def dry():
        return _merged(hwsc_registry.source_dry(),
                       hwsc_registry.source_dry(paths=sorted(scratch.glob("hwsd-dry*"))))

    def ok(key):
        return key in state and state[key]["status"] == "PASS"

    def scr(ok_tags):
        tags = set(ok_tags) | ({"R10"} if ok("r10") else set())
        return scratch_check_d(scratch, readers_ok=tags)

    def inv(readers):
        extra = {}
        if ok("r9"):
            extra["hwsc-store"] = ["R9"]
        if ok("r10"):
            extra["hwsu-store"] = ["R10"]
        return inventory_d(root, dict(readers, **extra))

    overrides = {"own": own, "dry": dry, "scratch": scr, "inventory": inv}
    superset = given.pop("superset", None)
    overrides.update(given)
    inner = hwsc_registry_build.build("K-REG1", out_dir, root=root, scratch=scratch,
                                      handoff=handoff, own_expected={"hwsd": "R9+R10"},
                                      sources=overrides)
    reg = c2_registry.Registry.load(out_dir.parent, "K-REG1")
    sup = superset(reg) if superset else hwsd_readers.superset_check(reg, root / "hwsc-store")
    rec = {"registry_version": "hwsd-reg-v1", "protocol_sha256": dc.PROTOCOL_SHA256,
           "inner_version": "K-REG1",
           "inner_manifest_sha256": stage_records.sha256(out_dir / "K-REG1.json"),
           "inner_digest_file_sha256": inner["digest_file_sha256"],
           "inner_status": inner["status"],
           "status": inner["status"] if inner["status"] != "PASS" else sup["status"],
           "problems": inner["problems"], "superset": sup,
           "r9": _summary(state["r9"]) if "r9" in state else None,
           "r10": _summary(state["r10"]) if "r10" in state else None,
           "known_label": dc.CONTRACT["registry"]["known_label"],
           "cpu_s": time.process_time() - t0,
           "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    stage_records.write_new(wrapper, rec)
    return rec


def load_d(store=None):
    store = Path(dc.STORE if store is None else store)
    reg_dir = store / "registry"
    w = reg_dir / "K-REG-D.json"
    if not w.is_file():
        raise C1GateFailure(hwsc_registry.LINEAGE, "K-REG-D.json missing")
    rec = dc.read_json(w)
    inner = reg_dir / "K-REG1.json"
    if not inner.is_file() or stage_records.sha256(inner) != rec.get("inner_manifest_sha256"):
        raise C1GateFailure(hwsc_registry.LINEAGE, "K-REG1.json differs from the wrapper")
    if rec.get("status") != "PASS":
        raise C1GateFailure(rec.get("status"), "K-REG-D status")
    return c2_registry.Registry.load(store, "K-REG1")
