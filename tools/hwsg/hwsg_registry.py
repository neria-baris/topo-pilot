"""HWSG registry: composition adapter, readers (b)-(d),(f), inventory, certificate (API.md §6;
protocol §6; N6). Reuses hwsc_registry_build.build / hwsc_registry readers through overrides."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import contextlib
import fnmatch
import hashlib
import io
import json
import os
import re
import time
from itertools import combinations
from pathlib import Path

import hwsb_registry
import hwsc_data
import hwsc_registry
import hwsc_registry_build
import numpy as np
import stage_records
from c1_records import C1GateFailure

INCOMPLETE, LINEAGE = "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
REG = gc.CONTRACT["registry"]
ARRAYS = (".npz", ".npy", ".pt")
METADATA = (".json", ".jsonl", ".md", ".lock", ".txt", ".log")
SINCE = time.mktime(time.strptime(REG["scratch_since"], "%Y-%m-%d"))
ADDED_ROWS = ("hwsc-store", "hwsu-store", "hwsd-store", "hwsg-store", "topo-pilot-hwsu",
              "topo-pilot-hwsd", "topo-pilot-hwsg")


_new, _close = hwsc_registry._new, hwsc_registry._close


def _merge(dst, src) -> dict:
    dst["digests"] |= set(src.get("digests", ()))
    dst["seq_ids"] |= set(src.get("seq_ids", ()))
    for k in ("files", "other", "non_history", "non_c2_format", "known_gaps"):
        dst[k] += list(src.get(k, ()))
    dst["present"] = dst["present"] and src.get("present", True)
    if src.get("status") not in (None, "PASS", INCOMPLETE):
        dst["status"] = src["status"]
    return dst


# ------------------------------------------------------------------------- reader (c)
def read_k4b_history_table(path, entry, out, opener=None) -> None:
    op = opener or (lambda p, m="rb": open(p, m))
    with op(path, "rb") as fh:
        data = fh.read()
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise C1GateFailure(LINEAGE, f"{entry['relpath']}: sha256 differs from the obligation")
    with np.load(io.BytesIO(data), allow_pickle=False) as z:
        if not {"canon32", "seq_ids", "digest"} <= set(z.files):
            out["other"].append({"path": str(path), "reason": "history table keys missing"})
            return
        dig = np.asarray(z["digest"]).astype(str)
        ids = np.asarray(z["seq_ids"], dtype=np.int64)
    out["digests"] |= set(dig.tolist()) - {""}
    out["seq_ids"] |= set(ids.tolist())
    out["files"].append({"path": str(path), "rows": int(len(dig))})


CLASS_TO_READER = {(r["class"], r["reader"]): (read_k4b_history_table if r["function"] else None)
                   for r in REG["class_to_reader"]}


def obligation_files(store) -> list:
    return sorted(n for n in os.listdir(store)
                  if fnmatch.fnmatchcase(n, "REGISTRY_OBLIGATION*.json"))


def _load_obligation(store, bound=None) -> tuple:
    store = Path(store)
    if isinstance(bound, dict) and bound.get("path"):
        p = store / bound["path"] if not Path(bound["path"]).is_absolute() else Path(bound["path"])
        data = gc.guard(p).read_bytes() if p.is_file() else None
        if data is None or hashlib.sha256(data).hexdigest() != bound.get("sha256"):
            raise C1GateFailure(INCOMPLETE, "obligation differs from the frozen path and sha256")
        return json.loads(data.decode("utf-8")), p, bound["sha256"]
    cands = []
    for n in obligation_files(store):
        data = gc.guard(store / n).read_bytes()
        cands.append((json.loads(data.decode("utf-8")), store / n,
                      hashlib.sha256(data).hexdigest()))
    if not cands:
        raise C1GateFailure(INCOMPLETE, "missing phase-2 obligation")
    return max(cands, key=lambda c: str(c[0].get("written_utc", "")))


def latest_obligation(store, bound=None) -> dict:
    obl, _, _ = _load_obligation(store, bound)
    if obl.get("schema") != "hws-registry-obligation-v1":
        raise C1GateFailure(INCOMPLETE, "obligation schema")
    return obl


def array_listing(store) -> list:
    store, out = Path(store), []
    for folder, dirs, files in os.walk(store):
        here = Path(folder)
        dirs[:] = sorted(d for d in dirs if not gc.public_summary(here / d))
        for n in sorted(files):
            if Path(n).suffix in ARRAYS:
                out.append({"relpath": (here / n).relative_to(store).as_posix(),
                            "bytes": (here / n).stat().st_size})
    return out


def _metadata(store) -> list:
    return [(Path(f) / n).relative_to(store).as_posix() for f, _, ns in os.walk(store)
            for n in sorted(ns) if Path(n).suffix in METADATA and not gc.public_summary(f)]


def source_obligation(store, bound=None, opener=None) -> dict:
    store, out = Path(store), _new()
    try:
        obl = latest_obligation(store, bound)
    except C1GateFailure as exc:
        out["other"].append({"path": str(store), "reason": exc.reason})
        return _close(out)
    lineage = False
    listing = {e["relpath"]: e for e in array_listing(store)}
    entries = {e["relpath"]: e for e in obl["files"]}
    for rel in sorted(set(listing) - set(entries)):
        out["other"].append({"path": rel, "reason": "new array file not in the obligation"})
    for rel in sorted(set(entries) - set(listing)):
        out["other"].append({"path": rel, "reason": "missing array file listed in the obligation"})
    for rel in sorted(set(entries) & set(listing)):
        e = entries[rel]
        if int(e["bytes"]) != int(listing[rel]["bytes"]):
            out["other"].append({"path": rel, "reason": "resized"})
            continue
        key = (e.get("class"), e.get("reader"))
        if key not in CLASS_TO_READER:
            out["other"].append({"path": rel, "reason": f"unknown class/reader {key}"})
        elif CLASS_TO_READER[key] is None:
            out["non_history"].append({"path": rel, "bytes": e["bytes"], "sha256": e["sha256"]})
        else:
            try:
                CLASS_TO_READER[key](store / rel, e, out, opener)
            except C1GateFailure as exc:
                out["other"].append({"path": rel, "reason": exc.reason})
                lineage = lineage or exc.status == LINEAGE
            except Exception as exc:  # noqa: BLE001
                out["other"].append({"path": rel, "reason": f"unreadable {exc!r}"})
    out["metadata"] = _metadata(store)
    return _close(out, lineage)


# ------------------------------------------------------------------------- reader (b)
def _glob_re(g) -> re.Pattern:
    return re.compile(re.escape(g).replace(r"\*\*", ".*").replace(r"\*", "[^/]*") + "$")


def source_hwsc(store=None, expected=None) -> dict:
    store = Path(gc.HWSC_STORE if store is None else store)
    out = _new(store.is_dir())
    if not store.is_dir():
        return _close(out)
    if expected is None:
        expected = gc.read_json(store / "stages/TRAIN/OBS_INVENTORY.json")
    reg = hwsb_registry.registry_digests(store, expected=dict(expected))
    out["digests"] |= set(reg["digests"])
    out["files"] += reg["sources"]
    out["other"] += [{"path": f["path"], "reason": f["error"]} for f in reg["failures"]]
    nh = [_glob_re(g) for g in REG["hwsc_store"]["non_history_by_name"]]
    assigned = re.compile(r"stages/(hwsd-dry-|hwsd-run-|hwsu-dry-of-)[^/]*/")
    for f in hwsc_registry._walk_arrays(store, None):
        rel = f.relative_to(store).as_posix()
        if rel.startswith("artifacts/ObservationSet/") or assigned.match(rel):
            continue
        if rel.startswith("sealed/"):
            out["non_history"].append({"path": rel, "name_only": True})
        elif any(r.match(rel) for r in nh):
            out["non_history"].append({"path": rel, "bytes": f.stat().st_size})
        elif f.name.startswith("HIST_") and f.suffix == ".npz" and (
                re.match(r"stages/(S3|S7)/", rel) or rel.startswith("superseded/")):
            try:
                hwsc_registry._token_file(f, out)
            except Exception as exc:  # noqa: BLE001
                out["other"].append({"path": rel, "reason": f"unreadable {exc!r}"})
        else:
            out["other"].append({"path": rel, "reason": "unassigned array file"})
    return _close(out)


# ------------------------------------------------------------------------- reader (d)
def source_scratch_g(scratch=None, table=None) -> dict:
    scratch = Path(gc.SCRATCH if scratch is None else scratch)
    out = _merge(_new(), hwsc_registry.source_scratch_c(scratch))
    rows = {r["name"]: r for r in (table or []) if isinstance(r, dict)}
    rules = REG["scratch_prefix_rules"]
    for d in sorted(p for p in scratch.iterdir() if p.is_dir()) if scratch.is_dir() else ():
        if d.stat().st_mtime < SINCE:
            continue
        row = rows.get(d.name)
        if row is None:
            row = next((r for r in rules if fnmatch.fnmatchcase(d.name, r["glob"])), None)
        dec = (row or {}).get("decision")
        if dec == "EXCLUSION":
            out["non_history"].append({"path": d.name, "excluded": True})
        elif dec == "READER":
            for f in hwsc_registry._walk_arrays(d, None):
                try:
                    hwsc_registry._token_file(f, out)
                except Exception as exc:  # noqa: BLE001
                    out["other"].append({"path": str(f), "reason": f"unreadable {exc!r}"})
        else:
            out["other"].append({"path": d.name, "reason": "no frozen decision for scratch dir"})
    return _close(out)


# ------------------------------------------------------------------------- reader (f)
def source_own(store, worlds) -> dict:
    out = _new()
    for w in worlds:
        wd = gc.world_dir(store, w)
        inv = wd / "stages/TRAIN/OBS_INVENTORY.json"
        if inv.is_file():
            _merge(out, hwsc_registry.source_own(wd, gc.read_json(inv)))
        elif (wd / "artifacts/ObservationSet").is_dir():
            out["other"].append({"path": str(wd), "reason": "ObservationSets without inventory"})
    return _close(out)


# ----------------------------------------------------------------------------- inventory
def inventory_g(root=None, readers=None) -> dict:
    root = Path(gc.ROOT if root is None else root)
    r = hwsc_registry.inventory_c(root, readers)
    viol = [v for v in r["violations"] if v["name"] not in ADDED_ROWS]
    return dict(r, violations=viol, unlisted=[n for n in r["unlisted"] if n not in ADDED_ROWS],
                status=INCOMPLETE if viol else "PASS")


def _canon(o) -> str:
    return json.dumps(o, sort_keys=True, default=str, separators=(",", ":"))


def _sha(o) -> str:
    return hashlib.sha256(_canon(o).encode("utf-8")).hexdigest()


def _obligations(root, bound=None) -> dict:
    out = {}
    for name in ("hwsu-store", "hwsd-store"):
        s = Path(root) / name
        if not s.is_dir():
            continue
        try:
            _, p, sha = _load_obligation(s, (bound or {}).get(name))
            out[name] = {"path": p.name, "sha256": sha, "listing": array_listing(s)}
        except C1GateFailure as exc:
            out[name] = {"error": exc.reason}
    return out


def certificate(manifest) -> str:
    return _sha({"inventory_sha256": manifest["inventory_sha256"],
                 "readers_version": manifest["readers_version"],
                 "sources_sha256": manifest["sources_sha256"]})


def _inv_sha(root, inv, bound=None) -> tuple:
    obl = _obligations(root, bound)
    return _sha({"inv": inv["inv"], "obligations": obl}), obl


def recheck(manifest, root=None) -> dict:
    root = Path(gc.ROOT if root is None else root)
    inv = inventory_g(root)
    bound = {k: v for k, v in manifest.get("obligations", {}).items()}
    sha, _ = _inv_sha(root, inv, bound)
    same = certificate(dict(manifest, inventory_sha256=sha)) == manifest["certificate"]
    if not same:
        raise C1GateFailure(INCOMPLETE, "registry certificate no longer holds")
    return {"status": "PASS", "certificate": manifest["certificate"]}


# ---------------------------------------------------------------------------------- build
def sources(root, scratch, worlds, extra=None, table=None) -> dict:
    root, tbl = Path(root), REG["scratch_dirs_at_0224"]
    table = table if table is not None else (tbl if isinstance(tbl, list) else None)
    spec = {"hwsc": lambda: source_hwsc(root / "hwsc-store"),
            "hwsu": lambda: source_obligation(root / "hwsu-store"),
            "hwsd": lambda: source_obligation(root / "hwsd-store"),
            "scratch_g": lambda: source_scratch_g(scratch, table),
            "own": lambda: source_own(root / "hwsg-store", worlds)}
    return spec


@contextlib.contextmanager
def _certify(mpath, root, bound):
    real = hwsc_registry_build.stage_records.write_new

    def write_new(path, obj):
        if Path(path) == Path(mpath):
            inv = inventory_g(root)
            sha, obl = _inv_sha(root, inv, bound)
            obj = dict(obj, inventory_sha256=sha, readers_version=_sha(REG),
                       sources_sha256=_sha([obj.get("sources"), obj.get("hwsc_sources"),
                                            obj.get("nd_sources")]),
                       obligations={k: {"path": v.get("path"), "sha256": v.get("sha256")}
                                    for k, v in obl.items()})
            obj["certificate"] = certificate(obj)
        real(path, obj)

    hwsc_registry_build.stage_records.write_new = write_new
    try:
        yield
    finally:
        hwsc_registry_build.stage_records.write_new = real


def build(version, out_dir, root=None, scratch=None, worlds=gc.TAGS, extra=None,
          sources_fn=None) -> dict:
    if version not in REG["versions"]:
        raise ValueError(f"registry version {version}")
    root = Path(gc.ROOT if root is None else root)
    scratch = Path(gc.SCRATCH if scratch is None else scratch)
    out_dir = Path(out_dir) / ("rehearsal" if version == "REHEARSAL" else "")
    spec = sources(root, scratch, worlds, extra)

    def union(r_dry):
        res = _merge(_new(), r_dry)
        for k in ("hwsc", "hwsu", "hwsd", "scratch_g"):
            _merge(res, spec[k]())
        res["status"] = _close(res)["status"]
        return res

    over = {"dry": lambda: union(hwsc_registry.source_dry()),
            "inventory": lambda readers: inventory_g(root, readers),
            "scratch": lambda readers_ok: {"status": "PASS", "digests": set(), "seq_ids": set()},
            "own": spec["own"]}
    if callable(sources_fn):
        over.update(sources_fn(root, scratch, worlds) or {})
    elif isinstance(sources_fn, dict):
        over.update(sources_fn)
    hand = gc.read_json(gc.HWSB_STORE / "HANDOFF.json")
    own_expected = None if version == "REHEARSAL" else {}
    with _certify(out_dir / f"{version}.json", root, None):
        man = hwsc_registry_build.build(version, out_dir, root=root, scratch=scratch,
                                        handoff=hand, own_expected=own_expected,
                                        extra=extra if version == "K-REG2" else None,
                                        sources=over)
    man.update(json.loads((out_dir / f"{version}.json").read_text(encoding="utf-8")))
    return man


# -------------------------------------------------------------------------- separation
class _RegView:
    def __init__(self, d):
        self.digests, self.seq_ids = set(d.get("digests", ())), set(d.get("seq_ids", ()))
        self.sealed_ranges, self.predicates = d.get("sealed_ranges", {}), d.get("predicates", {})

    def contains(self, digest):
        return np.isin(np.asarray(digest).astype(str), sorted(self.digests))


def _table(t) -> dict:
    if isinstance(t, (tuple, list)):
        import scores

        canon = np.asarray(t[0], dtype=np.uint8)
        return {"canon32": canon, "seq_ids": np.asarray(t[1], dtype=np.int64),
                "digest": np.array(scores.history_digests(canon), dtype="<U64")}
    return t


def separation_g(reg, tables_by_world) -> dict:
    res, coll, seq_coll = {}, {}, {}
    reg = _RegView(reg) if isinstance(reg, dict) else reg
    tables_by_world = {w: {s: _table(t) for s, t in tabs.items()}
                       for w, tabs in tables_by_world.items()}
    flat = [(f"{w}:{s}", t) for w, tabs in tables_by_world.items() for s, t in tabs.items()]
    for (a, ta), (b, tb) in combinations(flat, 2):
        if a.split(":")[0] == b.split(":")[0]:
            continue
        da = set(np.asarray(ta["digest"]).astype(str).tolist())
        db = set(np.asarray(tb["digest"]).astype(str).tolist())
        coll[f"{a}_{b}"] = len(da & db)
        seq_coll[f"{a}_{b}"] = len(set(np.asarray(ta["seq_ids"]).tolist())
                                   & set(np.asarray(tb["seq_ids"]).tolist()))
    if any(coll.values()) or any(seq_coll.values()):
        return {"status": LINEAGE, "per_world": res, "cross_collisions": coll,
                "cross_seq_collisions": seq_coll}
    for w, tabs in tables_by_world.items():
        res[w] = hwsc_data.separation_c(reg, tabs)
    st = [r["status"] for r in res.values()]
    if any(coll.values()) or any(seq_coll.values()) or LINEAGE in st:
        status = LINEAGE
    elif any(s != "PASS" for s in st):
        status = next(s for s in st if s != "PASS")
    else:
        status = "PASS"
    return {"status": status, "per_world": res, "cross_collisions": coll,
            "cross_seq_collisions": seq_coll}
