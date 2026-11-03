"""HWSU exposure registry: K-REG mirror, tables, U7 inventory, separation (API_U2.md section 3;
protocol 8.2-8.3). The readers live in hwsu_regsrc (split by size) and stay reachable here.

build_u mirrors hwsc_registry_build.build (which is called only by the DRU-REG dry-run case);
the stage-C source callables come from hwsc_registry_build._default_sources unchanged except
'own', 'scratch' and 'inventory', and the U readers are added (U2, U2', U5, U6, U7, U8).
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_regsrc as rs
import u2  # noqa: F401
import fnmatch
import hashlib
import importlib
import re
import time
from pathlib import Path

import c1_data
import c2_registry
import hwsc_registry
import hwsc_registry_build
import k4b_data
import k4b_registry
import numpy as np
import stage_records

INC, LIN = "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
COUNT_KEYS = ("history_files", "identity_refs", "observation_set_roots", "unreadable")
TAGS = ["c2", "c2sup", "c2scratch", "hws", "x6zc", "c2nd", "hwsb", "dry", "hwsc", "hwsu_dry",
        "hwsd"]
ND_TAGS = {"c2-readout-store": "c2", "hws-store": "hws", "x6zc-store": "x6zc",
           "c2nd-store": "c2nd", "hwsb-store": "hwsb"}



def _r(contract=None) -> dict:
    return (uc.CONTRACT if contract is None else contract)["registry_u2"]


def _hwsc_json(rel) -> dict:
    return uc.read_json(uc.REPO / "tools" / "hwsc" / rel)


def _hwsc_reg() -> dict:
    return _hwsc_json("CONTRACT.json")["registry"]


# ---------------------------------------------------------------- tables, U7, separation
def scratch_table_u(contract=None) -> dict:
    table = dict(_hwsc_reg()["scratch_inventory"])
    rows = _r(contract)["scratch_u2"].get("rows")
    table.update(rows if isinstance(rows, dict) else {})
    return table


def fixture_prefixes(contract=None) -> tuple:
    """Scratch prefixes of other studies' synthetic test/dry fixtures (EXCLUSION rows with the
    fixture rule J4 in CONTRACT scratch_u2.rows; R-0223-10 item 1)."""
    rows = _r(contract)["scratch_u2"].get("rows")
    rows = rows if isinstance(rows, dict) else {}
    return tuple(r["prefix"] for r in rows.values() if r.get("decision") == "EXCLUSION"
                 and r.get("rule") == "J4 fixture" and r.get("prefix"))


def root_table_u(contract=None) -> dict:
    t = dict(_hwsc_reg()["inventory"])
    t.update(_r(contract)["root_table_u2"]["add"])
    return t


def _tags(rec, readers) -> list:
    art = uc.ROOT / "topo-pilot" / "artifacts"
    f = []
    for r in rec.get("observation_set_roots", []):
        try:
            Path(r).resolve().relative_to(art.resolve())
        except (ValueError, OSError):
            f = ["f"]
    return sorted(set(readers) | set(f))


def _violation(name, entry, rec, cls, readers):
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


def inventory_u(root, readers, contract=None) -> dict:
    root = Path(root)
    excl = tuple(_hwsc_reg()["deep_scan_exclude"]) + tuple(
        _r(contract)["root_table_u2"]["deep_scan_exclude_add"])
    inv = k4b_registry.inventory(root, exclude=tuple(dict.fromkeys(excl)))
    inv.pop("hwsu-store", None)
    classes = k4b_registry.classify(inv, readers)
    frozen = {k: v for k, v in root_table_u(contract).items() if v.get("decision") != "OWN"}
    violations = []
    for name in sorted(set(inv) | set(frozen)):
        entry = frozen.get(name)
        if entry is not None and entry.get("decision") == "READER_IF_PRESENT":
            if name not in inv:
                continue
            entry = dict(entry, decision="READER")
        why = _violation(name, entry, inv.get(name), classes.get(name), readers.get(name, []))
        if why:
            violations.append({"name": name, "reason": why})
    return {"status": INC if violations else "PASS", "inv": inv, "classes": classes,
            "unlisted": sorted(set(inv) - set(frozen)), "violations": violations}


def _scratch_u(scratch, readers_ok) -> dict:
    res = hwsc_registry.scratch_check(scratch, table=scratch_table_u(), readers_ok=readers_ok)
    routed = _r()["scratch_u2"]["reserved_globs"]
    fixture = fixture_prefixes()
    keep = []
    for o in res["other"]:
        first = re.split(r"[\\/]", str(o["path"]).replace(str(scratch), "").lstrip("\\/"))[0]
        if not any(fnmatch.fnmatchcase(first, g) for g in routed) and not first.startswith(
                fixture):
            keep.append(o)
    res["other"] = keep
    return rs._close(res)


def sources_u(root, scratch, store, own_expected, contract=None) -> dict:
    root, scratch = Path(root), Path(scratch)
    return {"hwsc": lambda: rs.source_hwsc(root / "hwsc-store", contract),
            "hwsu_dry": lambda: rs.source_own_dry(scratch, contract),
            "hwsd": lambda: rs.source_hwsd(root, scratch, contract),
            "own": lambda: rs.source_own_u(store, own_expected, contract),
            "kreg2_c": lambda: rs.source_kreg2_c(root / "hwsc-store", contract),
            "scratch": lambda readers_ok: _scratch_u(scratch, readers_ok),
            "inventory": lambda readers: inventory_u(root, readers, contract)}


def separation_u(reg, tables, seq_union) -> dict:
    def hit(dig):
        if hasattr(reg, "contains"):
            return int(np.count_nonzero(reg.contains(np.array(dig, "<U64"))))
        return sum(1 for d in dig if d in reg)

    names = list(tables)
    dig = {n: k4b_data.digests(tables[n]["canon32"]) for n in names}
    ids = {n: set(np.asarray(tables[n]["seq_ids"], dtype=np.int64).tolist()) for n in names}
    coll = {f"{n}_R": hit(sorted(set(dig[n]))) for n in names}
    seq = {f"{n}_R": len(ids[n] & set(seq_union)) for n in names}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            coll[f"{a}_{b}"] = len(set(dig[a]) & set(dig[b]))
            seq[f"{a}_{b}"] = len(ids[a] & ids[b])
    return {"collisions": coll, "seq_overlap": seq,
            "ok": not (any(coll.values()) or any(seq.values()))}


def load_registry_sets(reg_dir, version) -> tuple:
    d = Path(reg_dir)
    man = uc.read_json(d / f"{version}.json")
    if stage_records.sha256(d / f"{version}_digests.npz") != man.get("digest_file_sha256"):
        raise ValueError(f"{version} digest file does not re-hash")
    with np.load(d / f"{version}_digests.npz", allow_pickle=False) as z:
        return set(z["digests"].astype(str).tolist()), set(np.asarray(z["seq_ids"]).tolist()), man


# ----------------------------------------------------------------------------- build_u
def _peak_memory():
    try:
        import psutil

        info = psutil.Process().memory_info()
        return int(getattr(info, "peak_wset", 0) or getattr(info, "rss", 0))
    except Exception:  # noqa: BLE001  report only
        return None


def build_u(version, out_dir, root, scratch, handoff, own=None, extra=None, sources=None,
            contract=None) -> dict:
    if version not in _r(contract)["versions"] or (extra and version != "K-REG2"):
        raise ValueError(f"registry version {version} (extra tables only for K-REG2)")
    if (version == "REHEARSAL") == (own is not None):
        raise ValueError("own is required for K-REG1/K-REG2 and refused for REHEARSAL")
    t0, root, scratch, out_dir = time.process_time(), Path(root), Path(scratch), Path(out_dir)
    mpath, dpath = out_dir / f"{version}.json", out_dir / f"{version}_digests.npz"
    run_dir = out_dir / "runs" / version
    if mpath.exists() or dpath.exists() or run_dir.exists():
        raise FileExistsError(mpath)
    out_dir.mkdir(parents=True, exist_ok=True)
    src_fn = hwsc_registry_build._default_sources(root, scratch, run_dir, handoff,
                                                  out_dir.parent, None)
    src_fn.update(sources_u(root, scratch, out_dir.parent, own, contract))
    src_fn.update(sources or {})
    src = src_fn["token_sources"]()
    problems, lineage = list(src["problems"]), list(src["lineage"])
    a_src, seqs = src["a"] if src["a"] is not None else ([], {})
    k_src = src["k"]["sources"] if src["k"] is not None else []
    tokens = a_src + src["b"] + (src["c"] or []) + src["e"]["sources"] + k_src
    x6 = src_fn["x6_source"]()
    if x6["status"] != "PASS":
        (lineage if x6["status"] == LIN else problems).append(f"x6: {x6['status']}")
    tags = TAGS + ([] if version == "REHEARSAL" else ["own"])
    nd = {t: src_fn[t]() for t in tags}
    ok_tags = {t for t in ("c2scratch", "hws") if nd[t]["status"] == "PASS"}
    ok_tags |= {"R5"} if nd["dry"]["status"] == "PASS" else set()
    ok_tags |= {u for u, t in (("U2", "hwsc"), ("U2prime", "hwsu_dry"), ("U5", "hwsd"))
                if nd[t]["status"] == "PASS"}
    nd["scratch"] = src_fn["scratch"](ok_tags)
    for tag, r in nd.items():
        if r["status"] != "PASS":
            (lineage if r["status"] == LIN else problems).append(f"{tag}: {r['status']}")
    readers = c2_registry._ok_readers(src, x6["status"] == "PASS")
    for name, tag in ND_TAGS.items():
        if nd[tag]["status"] == "PASS" and (tag != "c2" or nd["c2sup"]["status"] == "PASS"):
            readers.setdefault(name, []).append(tag)
    for name, tag, u in (("hwsc-store", "hwsc", "U2"), ("hwsd-store", "hwsd", "U5")):
        if nd[tag]["status"] == "PASS" and (tag != "hwsd" or nd[tag]["present"]):
            readers.setdefault(name, []).append(u)
    inv = src_fn["inventory"](readers)
    tokens += c2_registry._try(problems, "f", lambda: k4b_registry.source_f(
        root, inv["inv"], inv["classes"])) or []
    reg = c1_data.build_registry(tokens)
    problems += [f"unreadable: {m['name']}" for m in reg["missing"]]
    digests, seq_union = set(reg["digests"]), set()
    for s in (src["d"] or []) + k_src:
        digests |= s["digests"]
        seq_union |= s["sequence_ids"]
    for v in seqs.values():
        seq_union |= set(np.asarray(v, dtype=np.int64).tolist())
    for r in nd.values():
        digests |= set(r.get("digests", ()))
        seq_union |= set(r.get("seq_ids", ()))
    for tab in (extra or {}).values():
        digests |= set(np.asarray(tab["digest"]).astype(str).tolist())
        seq_union |= set(np.asarray(tab["seq_ids"], dtype=np.int64).tolist())
    k2 = src_fn["kreg2_c"]()  # U8; the S-2 diagnostic is taken before it joins the union
    diag = rs.superset_diagnostic(np.array(sorted(digests), dtype="<U64"), k2["digests"])
    if k2["status"] != "PASS":
        problems.append(f"kreg2_c: {k2['status']}")
    digests |= set(k2["digests"].tolist())
    seq_union |= set(np.asarray(k2["seq_ids"], dtype=np.int64).tolist())
    cov = src_fn["coverage"](src, seqs)
    problems += [] if cov["ok"] else [f"coverage: {cov['missing']}"]
    problems += [f"inventory {v['name']}: {v['reason']}" for v in inv["violations"]]
    status = LIN if lineage else INC if problems else "PASS"
    sorted_d = sorted(digests)
    seq_arr = np.array(sorted(seq_union), dtype=np.int64)
    dsha = hashlib.sha256("\n".join(sorted_d).encode()).hexdigest()
    x6m = c2_registry._x6_manifest(x6, out_dir)
    canon = [s.get("meta", {}).get("canonicalisation") for s in reg["entries"]]
    srcs = [c2_registry._entry(s, "token", s.get("rows"), c) for s, c in zip(reg["entries"], canon)]
    srcs += [c2_registry._entry(s, "digest", len(s["digests"]), "as stored")
             for s in (src["d"] or []) + k_src]
    e = src["e"]
    man = {"version": version, "registry_version": "hwsu-reg-v1", "status": status,
           "problems": lineage + problems, "n_digests": len(sorted_d), "digests_sha256": dsha,
           "seq_id_union_sha256": hashlib.sha256(seq_arr.tobytes()).hexdigest(), "x6": x6m,
           "union_sha256": hashlib.sha256(f"{dsha}\n{x6m['digest_sha256']}".encode()).hexdigest(),
           "sources": srcs, "classes": inv["classes"], "coverage": cov,
           "predicates": e["predicates"], "superset_diagnostic": diag,
           "inventory": {k: inv[k] for k in ("status", "unlisted", "violations")},
           "sealed_ranges": e["sealed_ranges"], "d2a_ranges": e["ranges"],
           "handoff_validation": k4b_registry.validate_handoff_json(root / "agent-handoff"),
           "k4b_store": k4b_registry.summary(src["k"]), "protocol_sha256": uc.CONTRACT[
               "protocol_sha256"],
           "nd_sources": {t: hwsc_registry_build._summary(nd[t])
                          for t in ("c2", "c2sup", "c2scratch", "hws", "x6zc")},
           "hwsc_sources": {t: hwsc_registry_build._summary(r) for t, r in nd.items()
                            if t in ("c2nd", "hwsb", "dry", "own", "scratch")},
           "hwsu_sources": {t: hwsc_registry_build._summary(nd[t])
                            for t in ("hwsc", "hwsu_dry", "hwsd")},
           "known_gaps": [g for r in nd.values() for g in r.get("known_gaps", [])],
           "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    stage_records.save_npz(dpath, digests=np.array(sorted_d, dtype="<U64"), seq_ids=seq_arr)
    man["digest_file_sha256"] = stage_records.sha256(dpath)
    man["cpu_s"] = time.process_time() - t0
    man["peak_memory_bytes"] = _peak_memory()
    stage_records.write_new(mpath, man)
    return man


_SPLIT = ("INC", "read_hist_table", "source_hwsc", "source_kreg2_c", "superset_diagnostic",
          "source_own_u", "read_obligation_u2", "source_hwsd", "source_own_dry")


def __getattr__(name):
    if name in _SPLIT:
        return getattr(importlib.import_module("hwsu_regsrc"), name)
    raise AttributeError(f"module 'hwsu_registry' has no attribute {name!r}")
