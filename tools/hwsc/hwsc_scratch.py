"""HWSC R6 scratch inventory: header scan and the fail-closed check against the frozen table
(API.md §4, §20; rulings R-0176-G9, R-0176-R6). Split from hwsc_registry by size; re-exported
there. A row may hold reader-covered files (`covered`: {relpath: reader tag}) and HASH_FROZEN
files (`hash_frozen`: {relpath: {sha256, bytes, reason_class}}), re-hashed at every check."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import os
from pathlib import Path

import k4b_registry
import stage_records
import x6s1_registry

def _cr():
    """hwsc_registry, imported lazily (it re-exports this module; no import-time cycle)."""
    import hwsc_registry

    return hwsc_registry


HASH_CLASSES = ("PYTEST_FIXTURE_LARGE", "FIXTURE_STORE", "OTHER_PROCESS_TRAINING", "CHECKPOINT")


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
                                   if p.is_file() and p.suffix in _cr().ARRAYS)}
    for top in sorted(p for p in scratch.iterdir() if p.is_dir()):
        full = top.name.startswith(_cr().STAGE_B)
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
                rel = _cr()._rel(top, f)
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


def _hash_ok(path, want) -> bool:
    return (path.is_file() and path.stat().st_size == int(want["bytes"])
            and stage_records.sha256(path) == want["sha256"]
            and want.get("reason_class") in HASH_CLASSES)


def _check_row(name, listed, row, ok_tags, scratch, out) -> None:
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


def scratch_check(scratch=None, table=None, readers_ok=None) -> dict:
    scratch = Path(cc.SCRATCH if scratch is None else scratch)
    table = _cr().REG["scratch_inventory"] if table is None else table
    ok_tags = set(readers_ok or ())
    scan, out = _cr().scratch_scan(scratch), _cr()._new()
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
        if name.startswith("hwsc-dry"):  # D-0178-1: the type rule, for these stores only
            import hwsc_drystore

            hwsc_drystore.check_store(scratch / name, listed, ok_tags, out)
            continue
        _check_row(name, listed, row, ok_tags, scratch, out)
    out["scan_counts"] = counts
    return _cr()._close(out)
