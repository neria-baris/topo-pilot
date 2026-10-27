"""C2ND exposure registry c2nd-reg-v1: the new readers c2, c2sup, c2scratch, hws and x6zc (rows
2-9 of protocol §6.2), the ND inventory adapter, the ND-REG1/ND-REG2 builds composing the
unchanged c2_registry readers (row 1), loading, separation and the reservation record check
(API.md §5, §20; C2ND-DESIGN-v1 §6.2-§6.5).

Rows 2-9 never open payload.npz, state.pt, *.pt or a path with a sealed component (§6.3, S12;
ND-C10, ND-C34). The reused readers and the ND sources are called through module attributes at
call time (API.md §20 B-5). Paths are read through nd_config at call time.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import time
from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_data
import c2_data as cd
import c2_registry as cg
import k4b_registry as kr
import numpy as np
import stage_records

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
AUTHORITY, NA = "FAIL_TECHNICAL/AUTHORITY", "NOT_APPLICABLE (dry)"
NOT_READ = "not read: payload/sealed"
OWN = "c2nd-store"
EXCLUDE = ("agent-handoff", "c1prime-store", "d2a-store", "k4b-store", "x6-stage1-store")
EXCLUDE += ("c2-readout-store", OWN, "hws-store", "x6zc-store")
ND_READERS = {"c2-readout-store": "c2", "hws-store": "hws", "x6zc-store": "x6zc"}
TAGS = ("c2", "c2sup", "c2scratch", "hws", "x6zc")
ARRAYS = (".npz", ".npy", ".pt")
C2_COLS = ("digest_H", "digest_Hp", "digest_Hm")


def _xr():
    import x6s1_registry as xr  # lazy, as c2_registry (API.md §1)

    return xr


def _new(present=True) -> dict:
    out = {"status": "PASS", "digests": set(), "files": [], "other": [], "non_c2_format": []}
    out.update(non_history=[], present=present)
    return out


def _close(out, lineage=False) -> dict:
    out["status"] = LINEAGE if lineage else INCOMPLETE if out["other"] else "PASS"
    return out


def _hex(chunk) -> set:
    return {bytes(r).hex() for r in np.asarray(chunk, dtype=np.uint8).reshape(-1, 32)}


def _c2_table(path, out) -> None:
    """The digest columns of one C2-format history table ("" dropped; c2_data.table_digests)."""
    with np.load(path, allow_pickle=False) as z:
        cols = [c for c in nc.CONTRACT["registry"]["c2_hist_columns"] if c in z.files]
        if not set(C2_COLS) <= set(cols):
            raise ValueError(f"{path}: digest columns {cols}")
        for c in cols:
            out["digests"] |= set(np.asarray(z[c]).astype(str).tolist()) - {""}
        rows = int(len(z["digest_H"]))
    out["files"].append(
        {"path": str(path), "sha256": cd.file_sha(path), "keys": cols, "rows": rows}
    )


# ---- row 2: reader c2; row 3: c2sup (API.md §5.1) --------------------------------------------
def source_c2(store=None, bound=None) -> dict:
    """The bound C2 hist files (CONTRACT, or `bound` for the dry stand-in) and any further
    HIST_*.npz."""
    store, out, bad = Path(nc.C2_STORE if store is None else store), _new(), False
    bound = nc.CONTRACT["registry"]["c2_hist"] if bound is None else bound
    for rel, want in sorted(bound.items()):
        p = store / rel
        if not p.is_file():
            out["other"].append({"path": str(p), "reason": "missing"})
        elif cd.file_sha(p) != want:
            bad = True
            out["other"].append({"path": str(p), "reason": "sha256 differs from CONTRACT"})
        else:
            try:
                _c2_table(p, out)
            except Exception as exc:  # noqa: BLE001  unreadable -> INCOMPLETE
                out["other"].append({"path": str(p), "reason": f"unreadable {exc!r}"})
    named = {(store / rel).resolve() for rel in bound}
    for p in sorted((store / "hist").glob("HIST_*.npz")):
        if p.resolve() in named:
            continue
        try:
            _c2_table(p, out)
        except Exception as exc:  # noqa: BLE001
            out["other"].append({"path": str(p), "reason": f"unreadable {exc!r}"})
    return _close(out, bad)


def source_c2_superseded(store=None) -> dict:
    """A name scan of superseded/: PASS iff the bound attempt directories exist and no file has
    an array suffix (fail closed; nothing is opened)."""
    store, out = Path(nc.C2_STORE if store is None else store), _new()
    sup, reg = store / "superseded", nc.CONTRACT["registry"]
    for d in reg["c2_superseded_dirs"]:
        if not (sup / d).is_dir():
            out["other"].append({"path": str(sup / d), "reason": "missing"})
    bad = tuple(reg["c2_superseded_forbidden_suffixes"])
    for f in cd._walk(sup) if sup.is_dir() else ():
        if f.suffix in bad:
            out["other"].append({"path": str(f), "reason": "array file in superseded/ (not read)"})
    return _close(out)


# ---- rows 4-6, 9: reader c2scratch (ND-C12, ND-C36; B-10) -----------------------------------
def _c2_format(path) -> bool:
    heads = {k: dt for k, dt, _ in _xr()._headers(path)}
    return all(k in heads and heads[k].kind == "U" for k in C2_COLS)


def source_scratch(root=None) -> dict:
    """Every HIST_*.npz under the scratch root outside a test_* directory (relative to the root):
    C2-format tables are read, other files listed as NON_C2_FORMAT (not read)."""
    root, out, reg = (
        Path(nc.SCRATCH_ROOT if root is None else root),
        _new(),
        nc.CONTRACT["registry"],
    )
    prefix, pattern = reg["scratch_exclude_prefix"], reg["scratch_name_pattern"]
    read = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(prefix))
        for name in sorted(n for n in filenames if fnmatch.fnmatchcase(n, pattern)):
            f = Path(dirpath) / name
            if "sealed" in f.relative_to(root).parts:
                out["other"].append({"path": str(f), "reason": NOT_READ})
                continue
            try:
                if not _c2_format(f):
                    out["non_c2_format"].append({"path": str(f), "bytes": f.stat().st_size})
                    continue
                _c2_table(f, out)
                read.append(f)
            except Exception as exc:  # noqa: BLE001  an unreadable header -> INCOMPLETE
                out["other"].append({"path": str(f), "reason": f"unreadable {exc!r}"})
    for r in reg["scratch_roots_expected"]:
        if not any(cd._rel(f, r) is not None for f in read):
            out["other"].append({"path": str(r), "reason": "expected root absent or no C2 table"})
    return _close(out)


# ---- rows 7-8: readers hws and x6zc (R-0116-3, R-0116-4; ND-C34, ND-C37) --------------------
def _x6zc_names() -> list:
    pats = nc.CONTRACT["registry"]["parallel"]["x6zc"]["layout"]["non_history"]
    return [re.compile("[^/]+".join(re.escape(s) for s in p.split("<model>"))) for p in pats]


def _read_history(f, out, require) -> None:
    """One array file by the c2_registry._x6_member rule; non-history-bearing files are skipped
    unless `require` (hws hist/**), when they make the source INCOMPLETE."""
    xr = _xr()
    try:
        if not xr._history_bearing(f):
            if require:
                out["other"].append({"path": str(f), "reason": "not history-bearing in hist/"})
            return
        entry = {"path": str(f), "sha256": cd.file_sha(f), "keys": [], "rows": 0}
        if f.suffix == ".npy":
            members = {"": np.load(f, allow_pickle=False)}
        else:
            with np.load(f, allow_pickle=False) as z:
                members = {k: np.asarray(z[k]) for k in z.files}
        digests = set()
        for k, a in members.items():
            for chunk in cg._x6_member(xr, k, a, entry):
                digests |= _hex(chunk)
        entry["keys"] = sorted(members)
    except Exception as exc:  # noqa: BLE001  unreadable -> other -> INCOMPLETE
        out["other"].append({"path": str(f), "reason": f"unreadable {exc!r}"})
        return
    out["digests"] |= digests
    out["files"].append(entry)


def _array_files(top):
    return sorted(p for p in Path(top).rglob("*") if p.is_file() and p.suffix in ARRAYS)


def _parallel_file(f, rel, tag, out) -> None:
    parts = rel.split("/")
    if f.suffix == ".pt" or f.name in ("payload.npz", "state.pt") or "sealed" in parts:
        out["other"].append({"path": str(f), "reason": NOT_READ})
    elif tag == "x6zc":
        if any(p.fullmatch(rel) for p in _x6zc_names()):
            out["non_history"].append({"path": str(f), "bytes": f.stat().st_size})
        else:
            out["other"].append({"path": str(f), "reason": "outside the X6ZC layout (R-0116-4)"})
    elif parts[0] != "registry":
        _read_history(f, out, require=tag == "hws" and parts[0] == "hist")


def source_parallel(store, tag) -> dict:
    """A parallel round's store: absent -> PASS (present False); unfrozen -> INCOMPLETE; else
    the hws or x6zc rule; hws also reads <SCRATCH_ROOT>/hws-dry/hist/** when present."""
    if tag not in ("hws", "x6zc"):
        raise ValueError(f"unknown parallel reader {tag!r}")
    store = Path(store)
    out = _new(present=store.exists())
    if not out["present"]:
        return out
    if not (store / nc.CONTRACT["registry"]["parallel"][tag]["frozen_marker"]).is_file():
        out["other"].append({"path": str(store), "reason": "store exists without FREEZE.json"})
        return _close(out)
    for f in _array_files(store):
        _parallel_file(f, f.relative_to(store).as_posix(), tag, out)
    if tag == "hws":
        dry = Path(nc.SCRATCH_ROOT) / nc.CONTRACT["registry"]["parallel"]["hws"]["dry_hist"]
        for f in _array_files(dry) if dry.is_dir() else ():
            rel = "hist/" + f.relative_to(dry).as_posix()
            _parallel_file(f, rel, tag, out)
    return _close(out)


# ---- the ND inventory adapter (API.md §5.2; ND-C9, ND-C38) -----------------------------------
def inventory(root=None, readers=None) -> dict:
    """k4b_registry.inventory/classify of every top-level directory against the ND frozen table;
    `readers` = the tags of the readers that succeeded (None: C2's static map plus the ND tags)."""
    root = Path(nc.PROJECT_ROOT if root is None else root)
    if readers is None:
        readers = dict(cg._static_readers(), **{k: [v] for k, v in ND_READERS.items()})
    inv = kr.inventory(root, exclude=EXCLUDE)
    inv.pop(OWN, None)
    classes = kr.classify(inv, readers)
    table = nc.CONTRACT["registry"]["inventory"]
    frozen = {k: v for k, v in table.items() if v.get("decision") != "OWN"}
    unlisted = sorted(set(inv) - set(frozen))
    violations = []
    for name in sorted(set(inv) | set(frozen)):
        entry = frozen.get(name)
        if entry is not None and entry.get("decision") == "READER_IF_PRESENT":
            if name not in inv:
                continue
            entry = dict(entry, decision="READER")
        why = cg._violation(name, entry, inv.get(name), classes.get(name), readers.get(name, []))
        if why:
            violations.append({"name": name, "reason": why})
    out = {"status": INCOMPLETE if violations else "PASS", "inv": inv, "classes": classes}
    out.update(unlisted=unlisted, violations=violations)
    return out


# ---- builds (API.md §5.3; ND-C8) -------------------------------------------------------------
def _nd_sources(root, c2_dry=None) -> dict:
    """Rows 2-9; with an explicit root the stores are taken under it (API.md §20 B-5). `c2_dry`
    (dry run): row 2 as read from the c2/ stand-in; c2real and c2sup NA (ND-C55)."""

    def at(name, attr):
        return Path(getattr(nc, attr)) if root is None else Path(root) / name

    c2s, na, dry = at("c2-readout-store", "C2_STORE"), dict(_new(None), status=NA), c2_dry
    out = {
        "c2": source_c2(c2s) if dry is None else dry,
        "c2sup": source_c2_superseded(c2s) if dry is None else na,
        "c2scratch": source_scratch(nc.SCRATCH_ROOT),
        "hws": source_parallel(at("hws-store", "HWS_STORE"), "hws"),
        "x6zc": source_parallel(at("x6zc-store", "X6ZC_STORE"), "x6zc"),
    }
    return out if dry is None else dict(out, c2real=na)


def _summary(r) -> dict:
    keys = ("status", "files", "other", "non_c2_format", "non_history", "present")
    return dict({k: r.get(k) for k in keys}, n=len(r.get("digests", ())))


def build(version, store=None, root=None, extra=None, c2_dry=None) -> dict:
    """ND-REG1 (S1, before DFIT) or ND-REG2 (S5; R' with the DFIT/DFEAS/DVAL tables in `extra`):
    the C2 recipe (row 1) plus rows 2-9 (`c2_dry`: ND-C55); status PASS, INCOMPLETE or LINEAGE."""
    if version not in nc.REG_NAMES or (extra and version != "ND-REG2"):
        raise ValueError(f"registry version {version} (extra tables only for ND-REG2)")
    explicit = root is not None
    root = Path(nc.PROJECT_ROOT if root is None else root)
    out_dir = Path(nc.STORE if store is None else store) / "registry"
    mpath, dpath = out_dir / f"{version}.json", out_dir / f"{version}_digests.npz"
    run_dir = out_dir / "runs" / version
    if mpath.exists() or dpath.exists() or run_dir.exists():
        raise FileExistsError(mpath)
    out_dir.mkdir(parents=True, exist_ok=True)
    src = cg.token_sources(root)
    problems, lineage = list(src["problems"]), list(src["lineage"])
    a_src, seqs = src["a"] if src["a"] is not None else ([], {})
    k_src = src["k"]["sources"] if src["k"] is not None else []
    tokens = a_src + src["b"] + (src["c"] or []) + src["e"]["sources"] + k_src
    x6 = cg.x6_source(root / "x6-stage1-store", run_dir)
    if x6["status"] != "PASS":
        (lineage if x6["status"] == LINEAGE else problems).append(f"x6: {x6['status']}")
    nd = _nd_sources(root if explicit else None, c2_dry)
    for tag, r in nd.items():
        if r["status"] not in ("PASS", NA):
            (lineage if r["status"] == LINEAGE else problems).append(f"{tag}: {r['status']}")
    readers = cg._ok_readers(src, x6["status"] == "PASS")
    ok = {name: nd[tag]["status"] == "PASS" for name, tag in ND_READERS.items()}
    ok["c2-readout-store"] &= nd["c2sup"]["status"] in ("PASS", NA)
    for name, tag in ND_READERS.items():
        if ok[name]:
            readers.setdefault(name, []).append(tag)
    inv = inventory(root, readers)
    tokens += cg._try(problems, "f", lambda: kr.source_f(root, inv["inv"], inv["classes"])) or []
    reg = c1_data.build_registry(tokens)
    problems += [f"unreadable: {m['name']}" for m in reg["missing"]]
    digests, seq_union = set(reg["digests"]), set()
    for s in (src["d"] or []) + k_src:
        digests |= s["digests"]
        seq_union |= s["sequence_ids"]
    for v in seqs.values():
        seq_union |= set(np.asarray(v, dtype=np.int64).tolist())
    for r in nd.values():
        digests |= set(r["digests"])
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
    x6m = cg._x6_manifest(x6, out_dir)
    canon = [s.get("meta", {}).get("canonicalisation") for s in reg["entries"]]
    sources = [cg._entry(s, "token", s.get("rows"), c) for s, c in zip(reg["entries"], canon)]
    sources += [
        cg._entry(s, "digest", len(s["digests"]), "as stored") for s in (src["d"] or []) + k_src
    ]
    e, x6sha = src["e"], x6m["digest_sha256"]
    man = {"version": version, "registry_version": nc.REG_VERSION, "status": status}
    man.update(problems=lineage + problems, n_digests=len(sorted_d), digests_sha256=dsha)
    man["seq_id_union_sha256"] = hashlib.sha256(seq_arr.tobytes()).hexdigest()
    man["x6"], man["union_sha256"] = x6m, hashlib.sha256(f"{dsha}\n{x6sha}".encode()).hexdigest()
    man.update(sources=sources, classes=inv["classes"], coverage=cov, predicates=e["predicates"])
    man["inventory"] = {k: inv[k] for k in ("status", "unlisted", "violations")}
    man.update(sealed_ranges=e["sealed_ranges"], d2a_ranges=e["ranges"])
    man["handoff_validation"] = kr.validate_handoff_json(root / "agent-handoff")
    man["k4b_store"], man["protocol_sha256"] = kr.summary(src["k"]), nc.PROTOCOL_SHA256
    man["nd_sources"] = {tag: _summary(r) for tag, r in nd.items()}
    man["built_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    stage_records.save_npz(dpath, digests=np.array(sorted_d, dtype="<U64"), seq_ids=seq_arr)
    man["digest_file_sha256"] = cd.file_sha(dpath)
    stage_records.write_new(mpath, man)
    return man


# ---- loading, separation, first tokens (API.md §5.3) -----------------------------------------
def load(store=None, version="ND-REG1") -> cg.Registry:
    return cg.Registry.load(Path(nc.STORE if store is None else store), version)


separation, first_token_ok = cg.separation, cg.first_token_ok  # unchanged (API.md §5.3)


# ---- the reservation record (§6.5; API.md §5.4) ----------------------------------------------
def _reservation_problem(store, stage, root) -> str | None:
    if stage not in ("S1", "S5"):
        return f"stage {stage!r}"
    path = Path(store) / f"RESERVATION_{stage}.json"
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return f"{path.name}: {exc!r}"
    schema = nc.CONTRACT["registry"]["reservation"]["schema"]
    if not isinstance(rec, dict) or rec.get("schema") != schema:
        return "schema"
    if rec.get("stage") != stage or rec.get("no_live_reservation") is not True:
        return "stage or live reservation"
    stores = rec.get("parallel_stores") or {}
    for name, attr in (("hws-store", "HWS_STORE"), ("x6zc-store", "X6ZC_STORE")):
        p = Path(getattr(nc, attr)) if root is None else Path(root) / name
        entry, exists = stores.get(name) or {}, p.exists()
        if entry.get("exists") is not exists:
            return f"{name}: exists flag {entry.get('exists')} but the store exists={exists}"
        fz = p / "FREEZE.json"
        if exists and (not fz.is_file() or cd.file_sha(fz) != entry.get("freeze_sha256")):
            return f"{name}: FREEZE.json does not re-hash to the recorded sha256"
    return None


def reservation_check(store, stage, root=None) -> dict:
    """PASS iff RESERVATION_<stage>.json records no live reservation and the parallel stores'
    existence and FREEZE.json sha256 as they are now; else FAIL_TECHNICAL/AUTHORITY (G0 (ix))."""
    why = _reservation_problem(store, stage, root)
    return {"status": "PASS" if why is None else AUTHORITY, "detail": why or "recorded"}
