"""C2ND shared stage plumbing (the extra module of job 0125, ND-C43; C2 c2_stage_base pattern,
ND-C6): store loaders and caches with the read-only C2 store, lineage records, the gate history
(the §3 scope rule), per-model split state (inputs, hooks, readout coordinates, phases) and the
split-level checks reused by S3 and T-PRE (L1, R1, N2, support, H5). It never imports nd_driver
or a stage module; nd_dry is imported lazily in a dry-run store only. Nothing runs at import."""

from __future__ import annotations

import importlib
import json
import os
from fractions import Fraction
from functools import partial
from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_chart
import c1_model
import c2_config as cc
import c2_data as cd
import c2_model as cm
import c2_oracle as co2
import chart
import nd_decide as ndc
import numpy as np
import stage_records as sr
from c1_records import C1GateFailure

OK, EXC, J1, X3 = ("PASS", "NOT_RUN"), "EXCLUDED/", nc.MODELS[0], ("H", "Hp", "Hm")
PROB_KEYS = ("alpha", "Gamma", "B", "L", "P_S", "P_G", "mtilde")
SRC = {"N-R": "R", "D": "RD", "N-M": "M"}  # the code problem whose L1/R1 gates each family
APPEND, SKIP_DIRS = ("GATES.jsonl", "STAGES.jsonl"), ("manifests", "superseded")
COORD = ("FREEZE.json", "AUTH.json", "AUTH_IMPL.json", "DRY.json", "nd_meter_bind.py")
SCHEMA = {"FREEZE.json": "c2nd-freeze-v1", "AUTH.json": "c2nd-auth-v1", "DRY.json": "c2nd-dry-v1"}
SCHEMA["AUTH_IMPL.json"] = "c2nd-auth-impl-v1"


# ---- JSON, hashing, loaders and caches (API.md §9.2) -----------------------------------------
def _jr(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _eq(a, b) -> bool:
    return a is not None and b is not None and str(a).lower() == str(b).lower()


def _sha_ok(path, want) -> bool:
    return Path(path).is_file() and _eq(cd.file_sha(path), want)


def _js(v):
    if isinstance(v, dict):
        return {str(k): _js(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set)):
        return [_js(x) for x in (sorted(v) if isinstance(v, set) else v)]
    if isinstance(v, np.ndarray):
        return _js(v.tolist()) if v.size <= 64 else f"<array {list(v.shape)}>"
    v = v.item() if isinstance(v, np.generic) else v
    if isinstance(v, float) and not np.isfinite(v):
        return str(v)
    if isinstance(v, Fraction):
        return f"{v.numerator}/{v.denominator}"
    return str(v) if isinstance(v, Path) or type(v).__name__ == "Decimal" else v


def _npz(path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def cache(ctx, key, fn):
    if key not in ctx.data:
        ctx.data[key] = fn()
    return ctx.data[key]


def c2_store(ctx) -> tuple:
    """(root, {rel: sha256}): the C2 store and its CONTRACT table, or in a dry-run store its c2/
    stand-in and c2/TABLE.json (written by nd_dry.prepare; ND-C42)."""
    if ctx.dry:
        root = Path(ctx.store) / "c2"
        return root, dict((_jr(root / "TABLE.json") or {}).get("files") or {})
    return Path(nc.C2_STORE), dict(nc.CONTRACT["c2_store"]["files"])


def c2_rehash(ctx) -> list:
    root, table = c2_store(ctx)
    return [r for r, s in table.items() if not _sha_ok(root / r, s)]


def _load(ctx, rel, kind, c2):
    def load():
        root, table = c2_store(ctx) if c2 else (Path(ctx.store), None)
        if c2 and not _sha_ok(root / rel, table.get(rel)):
            raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"C2 store file {rel} does not re-hash")
        return (_npz if kind == "npz" else _jr)(root / rel)

    return cache(ctx, ("c2:" if c2 else "") + rel, load)


def npz(ctx, rel, c2=False) -> dict:
    return _load(ctx, rel, "npz", c2)


def js(ctx, rel, c2=False) -> dict:
    return _load(ctx, rel, "js", c2)


def c2npz(ctx, rel) -> dict:
    return npz(ctx, rel, True)


def c2js(ctx, rel) -> dict:
    return js(ctx, rel, True)


def _abs(ctx, rel) -> Path:
    (Path(ctx.store) / rel).parent.mkdir(parents=True, exist_ok=True)
    ctx.data.setdefault("files", []).append(rel)
    return Path(ctx.store) / rel


def put(ctx, rel, **arrays) -> None:
    sr.save_npz(_abs(ctx, rel), **arrays)


def putj(ctx, rel, obj) -> None:
    sr.write_new(_abs(ctx, rel), _js(obj))


# ---- lineage (API.md §9.5, §15) --------------------------------------------------------------
def _skip(rel) -> bool:
    coord = rel in COORD or rel.startswith(("RELEASE_R", "RESERVATION_"))
    return rel in APPEND or cd._meter_file(rel) or rel.split("/")[0] in SKIP_DIRS or coord


def manifest_stem(ctx, stage) -> str:
    """manifests/<job>.json; a dry-run store runs every stage in one job: <job>-<stage>."""
    return f"{ctx.job}-{stage}" if ctx.dry else str(ctx.job)


def write_manifest(ctx, stage) -> Path:
    store, stem = Path(ctx.store), manifest_stem(ctx, stage)
    path = store / "manifests" / f"{stem}.json"
    if path.exists():
        raise FileExistsError(path)
    files = {cd._rel(f, store): cd.file_sha(f) for f in cd._walk(store)}
    man = {"schema": "c2nd-manifest-v1", "job": stem, "stage": stage, "head": ctx.head}
    man.update(files={k: x for k, x in files.items() if not _skip(k)}, utc=sr._utc())
    man["append_only"] = {k: files[k] for k in APPEND if k in files}
    path.parent.mkdir(parents=True, exist_ok=True)
    sr.write_new(path, man)
    return path


def _coord_ok(p) -> bool:
    r, name = _jr(p), Path(p).name
    if not isinstance(r, dict):
        return False
    if name.startswith("RESERVATION_"):
        return r.get("schema") == "c2nd-reservation-v1"
    proto = _eq(r.get("protocol_sha256"), nc.PROTOCOL_SHA256)
    return r.get("schema") == SCHEMA.get(name, "c2nd-release-v1") and proto


def recognised(store) -> dict:
    """{rel: sha256}: coordinator records, the bound meter file, every accepted manifest's files
    and append-only prefixes, and the superseded copies."""
    store, out, app = Path(store), {}, {}
    coord = [store / n for n in COORD[:4]] + sorted(store.glob("RELEASE_R*.json"))
    for p in coord + sorted(store.glob("RESERVATION_S*.json")):
        out.update({p.name: sr.sha256(p)} if _coord_ok(p) else {})
    mb, fz = store / "nd_meter_bind.py", _jr(store / "FREEZE.json") or _jr(store / "DRY.json")
    if mb.exists() and _eq(sr.sha256(mb), (fz or {}).get("meter_bind_sha256")):
        out[mb.name] = sr.sha256(mb)
    for acc in sorted(store.glob("manifests/*.accepted.json")):
        a = _jr(acc) or {}
        man = store / "manifests" / f"{a.get('job')}.json"
        if man.exists() and _eq(sr.sha256(man), a.get("manifest_sha256")):
            m = _jr(man)
            out.update(m["files"], **{f"manifests/{man.name}": sr.sha256(man)})
            out[f"manifests/{acc.name}"], app = sr.sha256(acc), m.get("append_only", {})
    out.update(app)
    for sums in sorted(store.glob("superseded/*/SHA256SUMS")):
        d = sums.parent.relative_to(store).as_posix()
        for line in sums.read_text(encoding="utf-8").splitlines():
            sha, _, rel = line.partition("  ")
            out[f"{d}/{rel}"] = sha
        for p in (sums, sums.parent / "SUPERSEDED.json"):
            out.update({f"{d}/{p.name}": sr.sha256(p)} if p.exists() else {})
    return out


def supersede(ctx, job, attempt, paths, ruling) -> Path:
    store = Path(ctx.store)
    dest = store / "superseded" / f"{job}-a{int(attempt)}"
    dest.mkdir(parents=True, exist_ok=False)
    lines = []
    for rel in paths:
        lines.append(f"{sr.sha256(store / rel)}  {rel}")
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        os.replace(store / rel, dest / rel)
    with (dest / "SHA256SUMS").open("x", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    rec = {k: ruling.get(k) for k in ("defect", "ruling_path", "ruling_sha256")}
    sr.write_new(dest / "SUPERSEDED.json", dict(rec, job=job, attempt=int(attempt), moved=paths))
    return dest


def regen_compare(ctx, path, archived_sha256) -> bool:
    return _eq(sr.sha256(path), archived_sha256)


# ---- gate history: the §3 scope rule ----------------------------------------------------------
def gates(ctx) -> list:
    return sr.gates_so_far(Path(ctx.store))


def _applies(g, j, fam) -> bool:
    m, f = g.get("model"), g.get("family") or ndc._family_of(g)
    return (m is None or int(m) == int(j)) and (f is None or f == fam)


def prior(ctx, j, fam):
    """The first exclusion, CNHS or stop for (j, fam); report-only records never apply
    (variant and RT problems, the coordinate decoys, the non-excluding gates)."""
    for g in gates(ctx):
        bad = g["full_status"] not in OK and g["gate"] not in ndc.NON_EXCLUDING
        ro = g.get("problem") in nc.VARIANTS + ("RT",) or g.get("decoy") in nc.KCR_CASES
        if bad and not ro and _applies(g, j, fam):
            return g["full_status"]
    return None


def alive(ctx, j, fam) -> bool:
    return prior(ctx, j, fam) is None


def fstop(ctx, fam):
    hit = (g for g in gates(ctx) if g.get("scope") == "family" and g.get("family") == fam)
    return next((g["full_status"] for g in hit if g["full_status"] not in OK), None)


def family_stop(ctx, fam):
    """None while >= 2 models remain, else the 2-of-3 rule's outcome (C2 §6.5 rule 2)."""
    st = {j: prior(ctx, j, fam) for j in nc.MODELS}
    if sum(v is None for v in st.values()) >= 2:
        return None
    cn = [j for j in st if st[j] == "CNHS"]
    return ndc.overall(fam, {j: v or "INC" for j, v in st.items()}, cn)


def rec(status, values=None, **who) -> dict:
    return {"status": status, "values": values or {}, **who}


def lines(recs) -> dict:
    bad = [r["status"] for r in recs if r["status"] not in OK]
    return {"status": bad[0] if bad else "PASS", "records": recs}


def per(ctx, fams, fn) -> dict:
    """One line per alive (model, family); fn(j, fam) -> (status, values)."""
    js_ = [(j, f) for j in nc.MODELS for f in fams if alive(ctx, j, f)]
    return lines([rec(*fn(j, f), model=j, family=f) for j, f in js_])


def frac(mask) -> Fraction:
    return Fraction(int(np.count_nonzero(mask)), len(mask))


# ---- per-model split state (API.md §9.2; ND-C6) ----------------------------------------------
def dry(ctx):
    """nd_dry, only in a dry-run store (its functions refuse otherwise; G0 (x))."""
    return importlib.import_module("nd_dry")


def proc(ctx) -> dict:
    return cache(ctx, "proc", co2.load_process)


def models(ctx) -> dict:
    """{j: (model64, state_sha)}: the C2 checkpoints, or the planted dry-run models."""
    return cache(ctx, "models", partial(_models, ctx))


def _models(ctx) -> dict:
    return dry(ctx).planted_models(ctx) if ctx.dry else cm.load_models()


def table(ctx, split) -> dict:
    def load():
        q = sorted(Path(ctx.store).glob(f"hist/HIST_{split}_b*"))
        t = [npz(ctx, f"hist/{x.name}") for x in q]
        return {k: np.concatenate([x[k] for x in t]) for k in t[0]}

    return cache(ctx, f"tab:{split}", load)


def orc(ctx, split) -> dict:
    return npz(ctx, f"oracle/ORACLE_{split}.npz")


def c2fit(ctx, j) -> dict:
    return c2npz(ctx, f"fits/FIT_{j}.npz")


def frozen_oracle(ctx) -> dict:
    return c2js(ctx, "oracle/ORACLE_FROZEN.json")


def inputs(ctx, j, H) -> np.ndarray:
    return np.asarray(c1_model.model_inputs(proc(ctx)["perm"][j][np.asarray(H)]))


def phase(ctx, j, a3) -> tuple:
    """(phi, supported) of resid_post_3 rows: the frozen production chart (C2), or the dry-run
    synthetic phase (§10.1; refused outside a dry-run store)."""
    if ctx.dry:
        return dry(ctx).synthetic_phase(ctx, j, a3)

    def load():
        with np.load(Path(cc.C1P_STORE) / f"CHART_{j}_production.npz", allow_pickle=False) as z:
            return chart.chart_from_arrays({k: z[k] for k in z.files})

    ext = c1_chart.extend_phase(*cache(ctx, f"chart:{j}", load), a3, cc.chart_cfg())
    return np.asarray(ext.phase), np.asarray(ext.supported, bool)


def _state(ctx, j, H, rows, n, kind) -> tuple:
    inp, z = np.full((n, 33), -1, np.int64), np.full((n, cc.V), np.nan) if kind else None
    a = {s: np.full((n, cc.D_MODEL), np.nan) for s in cc.SITES}
    if len(rows):
        m64, x = models(ctx)[j][0], inputs(ctx, j, H)
        aa, zz = cm.natural_pass(m64, x, ctx.policy, kind) if kind else (cm.activations3(m64, x), 0)
        inp[rows] = x
        for s in cc.SITES:
            a[s][rows] = aa[s]
        if kind:
            z[rows] = zz
    return inp, a, z


def bundle(ctx, split, j, kind=None, roles=cc.ROLES) -> dict:
    """Per role: inputs, the three hooks, y (frozen C2 basis), for H, H+, H- the phase and
    support; natural logits only under `kind`; H^Y on its Y_def rows only (C2 API §19.3)."""

    def make():
        tab, out = table(ctx, split), {}
        n = len(tab["canonical"])
        for r, (H, rows) in cd.table_roles(tab).items():
            if r in roles:
                inp, a, z = _state(ctx, j, H, rows, n, kind)
                y = cm.readout_coords(a["ln_final_out"], c2fit(ctx, j))
                out[r] = {"inp": inp, "a": a, "z": z, "y": y}
                if r in X3:
                    out[r]["phi"], out[r]["sup"] = phase(ctx, j, a["resid_post_3"])
        return out

    return cache(ctx, f"X:{split}:{j}:{kind}:{','.join(roles)}", make)


# ---- code problems: the frozen C2 FIT problems and the ND refits RD, RT (§2.8) ----------------
def problem(ctx, j, p) -> dict:
    """The projector problem p of model j: C2's frozen R, R_E, R_K1, R_K2, M, or the refit RD,
    RT ("problem" tag for nd_attrib.check_refit); {"ok": False} when it is not PASS."""
    ref = p in nc.REFITS
    F = npz(ctx, f"fits/REFIT_{j}.npz") if ref else c2fit(ctx, j)
    info = js(ctx, f"fits/REFIT_{j}.json") if ref else c2js(ctx, f"fits/FIT_{j}.json")
    if (info or {}).get("status", {}).get(p) != "PASS":
        return {"ok": False, "problem": p}
    o = {k: F[f"{p}_{k}"] for k in PROB_KEYS}
    o.update(ok=True, problem=p, L_B=o["L"][cc.N_NUIS :], delta=float(info["delta"][p]))
    return dict(o, Sigma=F[f"{p}_Sigma"] if f"{p}_Sigma" in F else F["R_Sigma"])
