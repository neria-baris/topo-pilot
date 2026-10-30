"""HWSC registry build and obligation record (API.md §4 `build`, `obligation`; split from
hwsc_registry by size, API erratum). A mirror of nd_registry.build with the stage-C sources;
every source is looked up at call time so that the dry run and tests can replace it."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import hashlib
import time
from pathlib import Path

import c1_data
import c2_registry
import hwsc_registry as cr
import k4b_registry
import nd_registry
import numpy as np
import stage_records

ND_TAGS = {"c2-readout-store": "c2", "hws-store": "hws", "x6zc-store": "x6zc",
           "c2nd-store": "c2nd", "hwsb-store": "hwsb"}


def _peak_memory():
    try:
        import psutil

        info = psutil.Process().memory_info()
        return int(getattr(info, "peak_wset", 0) or getattr(info, "rss", 0))
    except Exception:  # noqa: BLE001  report only
        return None


def _default_sources(root, scratch, run_dir, handoff, store, own_expected) -> dict:
    return {
        "token_sources": lambda: c2_registry.token_sources(root),
        "x6_source": lambda: c2_registry.x6_source(root / "x6-stage1-store", run_dir),
        "c2": lambda: nd_registry.source_c2(root / "c2-readout-store"),
        "c2sup": lambda: nd_registry.source_c2_superseded(root / "c2-readout-store"),
        "c2scratch": lambda: cr.source_scratch_c(scratch),
        "hws": lambda: nd_registry.source_parallel(root / "hws-store", "hws"),
        "x6zc": lambda: nd_registry.source_parallel(root / "x6zc-store", "x6zc"),
        "c2nd": lambda: cr.source_c2nd(root / "c2nd-store"),
        "hwsb": lambda: cr.source_hwsb(root / "hwsb-store", handoff["store_inventory"]),
        "dry": lambda: cr.source_dry(),
        "own": lambda: cr.source_own(store, own_expected),
        "scratch": lambda readers_ok: cr.scratch_check(scratch, readers_ok=readers_ok),
        "inventory": lambda readers: cr.inventory_c(root, readers),
        "coverage": lambda src, seqs: k4b_registry.revalidate_coverage(
            src["art"], root, store=src["store_a"],
            seqs_a=seqs if src["a"] is not None else None),
    }


def _summary(r) -> dict:
    keys = ("status", "files", "other", "non_c2_format", "non_history", "present", "known_gaps")
    return dict({k: r.get(k) for k in keys}, n=len(r.get("digests", ())))


def build(version, out_dir, root=None, scratch=None, handoff=None, own_expected=None,
          extra=None, sources=None) -> dict:
    if version not in cr.VERSIONS or (extra and version != "K-REG2"):
        raise ValueError(f"registry version {version} (extra tables only for K-REG2)")
    if (version == "REHEARSAL") == (own_expected is not None):
        raise ValueError("own_expected is required for K-REG1/K-REG2 and refused for REHEARSAL")
    if handoff is None:
        raise ValueError("build needs the HANDOFF dict (store_inventory)")
    t0 = time.process_time()
    root = Path(cc.ROOT if root is None else root)
    scratch = Path(cc.SCRATCH if scratch is None else scratch)
    out_dir = Path(out_dir)
    mpath, dpath = out_dir / f"{version}.json", out_dir / f"{version}_digests.npz"
    run_dir = out_dir / "runs" / version
    if mpath.exists() or dpath.exists() or run_dir.exists():
        raise FileExistsError(mpath)
    out_dir.mkdir(parents=True, exist_ok=True)
    src_fn = _default_sources(root, scratch, run_dir, handoff, out_dir.parent, own_expected)
    src_fn.update(sources or {})
    src = src_fn["token_sources"]()
    problems, lineage = list(src["problems"]), list(src["lineage"])
    a_src, seqs = src["a"] if src["a"] is not None else ([], {})
    k_src = src["k"]["sources"] if src["k"] is not None else []
    tokens = a_src + src["b"] + (src["c"] or []) + src["e"]["sources"] + k_src
    x6 = src_fn["x6_source"]()
    if x6["status"] != "PASS":
        (lineage if x6["status"] == cr.LINEAGE else problems).append(f"x6: {x6['status']}")
    tags = ["c2", "c2sup", "c2scratch", "hws", "x6zc", "c2nd", "hwsb", "dry"]
    tags += [] if version == "REHEARSAL" else ["own"]
    nd = {t: src_fn[t]() for t in tags}
    ok_tags = {t for t in ("c2scratch", "hws") if nd[t]["status"] == "PASS"}
    ok_tags |= {"R5"} if nd["dry"]["status"] == "PASS" else set()
    nd["scratch"] = src_fn["scratch"](ok_tags)
    for tag, r in nd.items():
        if r["status"] != "PASS":
            (lineage if r["status"] == cr.LINEAGE else problems).append(f"{tag}: {r['status']}")
    readers = c2_registry._ok_readers(src, x6["status"] == "PASS")
    for name, tag in ND_TAGS.items():
        ok = nd[tag]["status"] == "PASS" and (tag != "c2" or nd["c2sup"]["status"] == "PASS")
        if ok:
            readers.setdefault(name, []).append(tag)
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
    cov = src_fn["coverage"](src, seqs)
    problems += [] if cov["ok"] else [f"coverage: {cov['missing']}"]
    problems += [f"inventory {v['name']}: {v['reason']}" for v in inv["violations"]]
    status = cr.LINEAGE if lineage else cr.INCOMPLETE if problems else "PASS"
    sorted_d = sorted(digests)
    seq_arr = np.array(sorted(seq_union), dtype=np.int64)
    dsha = hashlib.sha256("\n".join(sorted_d).encode()).hexdigest()
    x6m = c2_registry._x6_manifest(x6, out_dir)
    canon = [s.get("meta", {}).get("canonicalisation") for s in reg["entries"]]
    srcs = [c2_registry._entry(s, "token", s.get("rows"), c)
            for s, c in zip(reg["entries"], canon)]
    srcs += [c2_registry._entry(s, "digest", len(s["digests"]), "as stored")
             for s in (src["d"] or []) + k_src]
    e = src["e"]
    man = {"version": version, "registry_version": "hwsc-reg-v1", "status": status,
           "problems": lineage + problems, "n_digests": len(sorted_d), "digests_sha256": dsha,
           "seq_id_union_sha256": hashlib.sha256(seq_arr.tobytes()).hexdigest(), "x6": x6m,
           "union_sha256": hashlib.sha256(f"{dsha}\n{x6m['digest_sha256']}".encode())
           .hexdigest(), "sources": srcs, "classes": inv["classes"], "coverage": cov,
           "predicates": e["predicates"],
           "inventory": {k: inv[k] for k in ("status", "unlisted", "violations")},
           "sealed_ranges": e["sealed_ranges"], "d2a_ranges": e["ranges"],
           "handoff_validation": k4b_registry.validate_handoff_json(root / "agent-handoff"),
           "k4b_store": k4b_registry.summary(src["k"]), "protocol_sha256": cc.PROTOCOL_SHA256,
           "nd_sources": {t: _summary(nd[t]) for t in ("c2", "c2sup", "c2scratch", "hws",
                                                       "x6zc")},
           "hwsc_sources": {t: _summary(r) for t, r in nd.items()
                            if t in ("c2nd", "hwsb", "dry", "own", "scratch")},
           "known_gaps": [g for r in nd.values() for g in r.get("known_gaps", [])],
           "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    stage_records.save_npz(dpath, digests=np.array(sorted_d, dtype="<U64"), seq_ids=seq_arr)
    man["digest_file_sha256"] = stage_records.sha256(dpath)
    man["cpu_s"] = time.process_time() - t0
    man["peak_memory_bytes"] = _peak_memory()
    stage_records.write_new(mpath, man)
    return man


def obligation(store, extra_paths=()) -> dict:
    store = Path(store)
    inv = {}
    for sub in ("artifacts/ObservationSet", "stages/S3", "stages/S7", "superseded"):
        base = store / sub
        for f in sorted(p for p in base.rglob("*") if p.is_file()) if base.is_dir() else ():
            inv[f.relative_to(store).as_posix()] = stage_records.sha256(f)
    rec = {"store": str(store),
           "readers": {"ObservationSet": "hwsb_registry.registry_digests",
                       "HIST_*.npz": "K4b history-table reader (canon32, seq_ids, digest)"},
           "dry_stores": [str(cc.DRY_STORE)] + [str(p) for p in extra_paths],
           "inventory": inv,
           "rule": "every later registry lists hwsc-store, hwsc-dry and every hwsc-dry-<job>; "
                   "fail closed"}
    stage_records.write_new(store / "REGISTRY_OBLIGATION.json", rec)
    return rec
