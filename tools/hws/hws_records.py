"""HWS records: STAGES events, histories, look records, tree hashes, resume archive,
FREEZE.json, the REPORT and SELECTION writers (API.md §6.1, §6.3-§6.5; erratum E8-E10, E14;
ruling R-0118-6). Writes only inside the store `out`, by exclusive create (append-only:
STAGES.jsonl). Reads no payload; G0 never opens excluded paths.
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import hashlib
import json
import math
import platform
import shutil
import subprocess
import time
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

import hws_worlds as hw
import hws_select as hsel
import hws_stats as hs
import numpy as np
import scipy
import stage_records
from topo_pilot.contracts import canonical_json
from topo_pilot.process import EmissionConfig, TransitionConfig
from topo_pilot.world import WorldConfig

EFFECT_KS = (1, 2, 4, 6, 8, 12, 16, 24)
IDENT = ("key", "W", "q", "sigma", "p", "tier")
FREEZE = "FAIL_TECHNICAL/FREEZE"


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def append_stage_event(out, event: dict) -> None:
    line = json.dumps(dict(event, utc=utc()), sort_keys=True, default=str)
    Path(out).mkdir(parents=True, exist_ok=True)
    with (Path(out) / "STAGES.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def stage_events(out) -> list:
    path = Path(out) / "STAGES.jsonl"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def save_hist(out, stage, key, tok, origin=None) -> Path:
    folder = Path(out) / "hist" / stage / (origin or "")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{key}.npz"
    stage_records.save_npz(path, canon32=np.ascontiguousarray(tok, dtype=np.uint8))
    return path


def _files(out, prefixes) -> dict:
    out, found = Path(out), {}
    for pre in prefixes:
        base = out / pre
        for p in sorted(base.rglob("*")) if base.is_dir() else []:
            if p.is_file():
                found[p.relative_to(out).as_posix()] = stage_records.sha256(p)
    return found


def tree_sha(out, prefixes) -> str:
    return sha_bytes(canonical_json(_files(out, prefixes)).encode("utf-8"))


def archive_partial(out, stage):
    """RC-5 resume (choice 40): unlisted files of the interrupted stage go to superseded/."""
    out, listed = Path(out), set()
    for ev in stage_events(out):
        if ev.get("event") == "WORLD_COMPLETE" and ev.get("stage") == stage:
            listed |= set(ev.get("files", {}))
    pres = [f"stages/{stage}", f"hist/{stage}", f"hist/NULLCHK/{stage}"]
    stray = {k: v for k, v in _files(out, pres).items() if k not in listed}
    if not stray:
        return None
    stamp = utc().replace(":", "")
    dest, n = out / "superseded" / f"{stage}-{stamp}", 0
    while dest.exists():
        n += 1
        dest = out / "superseded" / f"{stage}-{stamp}-{n}"
    for rel in stray:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(out / rel), str(dest / rel))
    with (dest / "SHA256SUMS").open("x", encoding="utf-8") as handle:
        handle.write("".join(f"{sha}  {rel}\n" for rel, sha in sorted(stray.items())))
    return dest


# ------------------------------------------------------------------------------ look records


def num(x):
    """JSON-safe copy: numpy scalars to Python, Fractions to strings, keys to str."""
    if isinstance(x, dict):
        return {str(k): num(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [num(v) for v in x]
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return float(x)
    return str(x) if isinstance(x, Fraction) else x


def _ediff(kl, h4, hl) -> dict:
    s, e = hs.summary(kl), hs.entropy_diff(h4, hl)
    d = hs.summary(np.asarray(kl) - (np.asarray(h4) - np.asarray(hl)))
    return {"kl": s, "ent": e, "diff": s["mean"] - e["mean"], "diff_se": d["se"]}


def _all_finite(rows) -> bool:
    for v in rows.values():
        vals = v.values() if isinstance(v, dict) else [v]
        if not all(np.all(np.isfinite(np.asarray(a, dtype=np.float64))) for a in vals):
            return False
    return True


def boot_arrays(rows) -> dict:
    """Choice 21: D_K, B_K, V_K, G_K at the effect Ks present, G0, G4A, IZ4, IX4, Hq[L]."""
    out = {}
    for K in [k for k in EFFECT_KS if k in rows["D"]]:
        out.update({f"D{K}": rows["D"][K], f"B{K}": rows["rn"][K], f"G{K}": rows["G"][K]})
        out[f"V{K}"] = rows["rn"][K] ** 2
    out.update({k: rows[k] for k in ("G0", "G4A", "IZ4", "IX4")})
    out["Hq"] = rows["Hq"][max(rows["Hq"])]
    return out


def _ident(proc, exact, stage, n) -> dict:
    rec = {k: proc.get(k) for k in IDENT}
    rec.update(changed=exact.get("changed"), distance=exact.get("distance"), stage=stage)
    return dict(rec, n=int(n), exact=exact)


def _report(rows, exact, lh, g4_mean) -> dict:
    rep = {k: hs.summary(rows[k]) for k in ("G0", "IZ4", "IX4")}
    rep.update(H_star=hs.summary(rows["Hq"][lh]), R2=hs.summary(rows["m_sq"]))
    rep.update(p_weak=float(np.mean(rows["weak_ind"])), p_gain=float(np.mean(rows["gain_ind"])))
    rep.update(A_eff=exact.get("A_eff"), p_D2a=exact.get("p_D2a"))
    rep["perplexity_ratio"] = math.exp(g4_mean)
    ed = (("G4", rows["G"][4], "Hq"), ("G4A", rows["G4A"], "HqA"))
    ed += (("IZ4", rows["IZ4"], "Hb"), ("IX4", rows["IX4"], "Hbx"))
    rep["entropy_diff"] = {k: _ediff(x, rows[h][4], rows[h][lh]) for k, x, h in ed}
    return rep


def look_record(proc, exact, look, stage, n, floors=None, seed=None) -> dict:
    """§6.4 per-world-look aggregate. A bootstrap seed (S3: 620103, S0: 620101) adds the
    bootstrap effects; S3 bounds use them (L3). `floors` adds eligibility and class."""
    rows, lh = look["rows"], int(look["tok"].shape[1])
    ks = sorted(rows["D"])
    main = {"D4": rows["D"][4], "GC": rows["G"][1], "G4": rows["G"][4], "G4A": rows["G4A"]}
    s3b = None
    if seed is not None:
        arrs = boot_arrays(rows)
        boot = hs.bootstrap(arrs, seed)
        s3b = {k: hs.s3_bounds(x, boot[k]) for k, x in arrs.items()}
    if stage == "S3":
        bounds = {q: s3b[{"GC": "G1"}.get(q, q)] for q in main}
    else:
        bounds = {q: hs.screen_bounds(x) for q, x in main.items()}
    e5 = hs.e5(rows["m"][lh])
    nulls = {k: hs.null_z(v) for k, v in rows["nulls"].items()}
    fin = _all_finite({k: v for k, v in rows.items() if k not in ("m", "nulls")})
    e6 = {"finite": fin, "norm_err": rows["norm_err"], "gc_check": rows.get("gc_check", 0.0)}
    e6.update(pinsker_violations=hs.pinsker_violations(rows["pinsker_slack"]))
    e6["null_exceeds"] = [k for k, v in nulls.items() if v["exceeds"]]
    e6_ok = bool(fin and e6["norm_err"] <= 1e-12 and e6["gc_check"] <= 1e-12)
    cols = {"D": rows["D"], "B": rows["rn"], "G": rows["G"]}
    cols["V"] = {K: rows["rn"][K] ** 2 for K in ks}
    rec = _ident(proc, exact, stage, n)
    rec.update(Ks=ks + [lh], stream=look["stream"], hist=look.get("hist"), e5=e5, e6=e6)
    rec.update(hist_sha256=look.get("hist_sha256"), e6_ok=e6_ok, bounds=bounds, nulls=nulls)
    rec["profile"] = {name: {K: hs.summary(c[K]) for K in ks} for name, c in cols.items()}
    rec["report"] = _report(rows, exact, lh, bounds["G4"]["mean"])
    rec["annotations"] = hsel.annotations(bounds["D4"])
    if s3b is not None:
        keep = ("mean", "sd", "central95_boot", "L3")
        rec["effects"] = {k: {x: b[x] for x in keep} for k, b in s3b.items()}
    if stage == "S3":
        p4d = float(np.mean(rows["rn"][4] ** 2))
        rec["P4"] = float(np.mean(rows["P4"])) / p4d if "P4" in rows and p4d > 0 else "undefined"
        rec["L3"] = {q: b["L3"] for q, b in bounds.items()}
        rec["central95"] = {q: b["central95_boot"] for q, b in bounds.items()}
        qs = np.quantile(rows["m_norm"], [0, 0.05, 0.25, 0.5, 0.75, 0.95, 1])
        rec["m_norm_quantiles"] = [float(x) for x in qs]
    if floors is not None:
        rec["eligibility"] = hsel.eligibility(exact["status"], e5["pass"], e6_ok)
        rec.update(hsel.classify(rec, floors))
    return num(rec)


def write_look(out, rec, origin=None) -> Path:
    folder = Path(out) / "stages" / rec["stage"] / (origin or "") / "worlds"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{rec['key']}.json"
    stage_records.write_new(path, rec)
    return path


def exact_record(proc, exact, stage) -> dict:
    """Record of a world excluded by E1-E4 before sampling (never sampled; no bounds)."""
    rec = _ident(proc, exact, stage, 0)
    st = exact["status"]
    return num(dict(rec, eligibility=st, failed=[], annotations=[], **{"class": st}))


# ---------------------------------------------------------------------------- FREEZE.json


def _git(repo, *args) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def implementation_files(repo, h_exec) -> dict:
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec, "--", "tools/hws", "tests/hws")
    names = names.decode("utf-8").splitlines()
    keep = [n for n in names if n.startswith("tests/hws/") or n.endswith(".py")]
    return {n: sha_bytes(_git(repo, "show", f"{h_exec}:{n}")) for n in keep}


def _hashes(repo) -> dict:
    tools = Path(repo) / "tools" / "hws"
    names = {"protocol_sha256": "PROTOCOL_HWS_v1.md", "contract_sha256": "CONTRACT.json"}
    names.update(api_sha256="API.md", test_plan_sha256="TEST_PLAN.md")
    out = {k: stage_records.sha256(tools / v) for k, v in names.items()}
    reuse = {rel: stage_records.sha256(Path(repo) / rel) for rel in hw.CONTRACT["reuse_sha256"]}
    if out["protocol_sha256"] != hw.CONTRACT["protocol_sha256"]:
        raise hw.HwsStop(FREEZE, "protocol copy differs from CONTRACT protocol_sha256")
    bad = sorted(k for k, v in reuse.items() if v != hw.CONTRACT["reuse_sha256"][k])
    if bad:
        raise hw.HwsStop(FREEZE, f"reused files changed: {bad}")
    return dict(out, reuse_sha256=reuse)


def freeze(out, repo, h_exec, dry_report) -> dict:
    """§6.5 FREEZE.json by exclusive create, bound to h_exec and the dry-run report."""
    files = implementation_files(repo, h_exec)
    impl = sha_bytes(canonical_json(files).encode("utf-8"))
    dry = json.loads(Path(dry_report).read_text(encoding="utf-8"))
    if dry.get("implementation_sha256") != impl:
        raise hw.HwsStop(FREEZE, "dry-run report is not bound to this implementation hash")
    env = {"python": platform.python_version(), "numpy": np.__version__}
    rec = {"protocol": "HWS-FROZEN-v1", "h_exec": h_exec, "implementation_files": files}
    rec.update(implementation_sha256=impl, dry_run_report_sha256=stage_records.sha256(dry_report))
    rec.update(dry_run_report_path=str(dry_report), dry_run_all_pass=dry.get("all_pass"))
    rec.update(environment=dict(env, scipy=scipy.__version__), created_utc=utc())
    rec.update(_hashes(repo))
    Path(out).mkdir(parents=True, exist_ok=True)
    stage_records.write_new(Path(out) / "FREEZE.json", rec)
    return rec


def verify_freeze(out, repo) -> dict:
    """Every stage job checks FREEZE.json against the working tree before any sampling."""
    path = Path(out) / "FREEZE.json"
    if not path.exists():
        raise hw.HwsStop(FREEZE, "FREEZE.json missing")
    rec = json.loads(path.read_text(encoding="utf-8"))
    now = {rel: stage_records.sha256(Path(repo) / rel) for rel in rec["implementation_files"]}
    if now != rec["implementation_files"]:
        raise hw.HwsStop(FREEZE, "implementation files differ from FREEZE.json")
    bad = [k for k, v in _hashes(repo).items() if rec.get(k) != v]
    if bad:
        raise hw.HwsStop(FREEZE, f"FREEZE.json mismatch: {bad}")
    return dict(rec, freeze_sha256=stage_records.sha256(path))


# ---------------------------------------------------------------- REPORT and SELECTION writers


def report_record(state, oc, extra) -> dict:
    """§6.4 REPORT.json from the outcome state and run extras (x1, s2, cpu, nulls, hashes)."""
    recs = hsel._recs(state["records"])
    classes = {}
    for r in recs:
        classes[r["class"]] = classes.get(r["class"], 0) + 1
    worlds = {r["key"]: {"class": r["class"], "D4": r.get("bounds", {}).get("D4")} for r in recs}
    for r in recs:
        worlds[r["key"]]["annotations"] = r.get("annotations", [])
    keys = ("outcome", "licence", "selected", "fallback_list", "below_3x_worlds")
    keys += ("at_3x_fallback_only", "absence_3x_shown", "unresolved", "max_D4")
    rep = {k: oc.get(k) for k in keys}
    rep.update(finalists=state["finalists"], s3=state.get("s3", {}), classes=classes)
    rep.update(
        worlds=worlds,
        floors=state.get("floors"),
        protocol_sha256=hw.CONTRACT["protocol_sha256"],
        z={"Z1": hs.Z1, "ZW": hs.ZW, "Z3": hs.Z3, "ZNULL": hs.ZNULL},
    )
    for k in ("x1", "s2", "cpu", "nulls", "pinsker_flags", "freeze_sha256", "s0_record_sha256"):
        rep[k] = extra.get(k)
    return num(rep)


def write_report(out, report) -> Path:
    path = Path(out) / "stages" / "FINAL" / "REPORT.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, report)
    return path


def _arr_sha(a) -> str:
    return sha_bytes(np.ascontiguousarray(a, dtype=np.float64).tobytes())


def selection_record(proc, rec_s3, oc, extra) -> dict:
    """§10.1 hand-off package (written only for HWS_SELECTED, choice 32)."""
    w = proc["world_key"]
    cfg = {"WorldConfig": asdict(WorldConfig("cylinder", (w.W, 12), "flat"))}
    cfg["TransitionConfig"] = asdict(TransitionConfig(p_stay=float(w.p)))
    if proc["tier"] == 0:
        cfg["EmissionConfig"] = asdict(EmissionConfig("overlap", 36, float(w.sigma), "grid"))
    else:
        lab = np.asarray(proc["labels"], dtype=np.int64)
        cfg.update(centres=hw.centres(w.W).tolist(), alias_labels=lab.tolist())
        cfg["alias_sha256"] = sha_bytes(lab.tobytes())
    eff = dict(rec_s3.get("effects", {}))
    bits = {k: v["mean"] / math.log(2) for k, v in eff.items() if k[0] in "GIH"}
    d4 = rec_s3["bounds"]["D4"]
    sel = {"world": dict({k: proc[k] for k in IDENT}), "configs": cfg}
    sel.update(canonical_label_order="v = 6g + b", effects=eff, effects_bits=bits)
    sel["sha256"] = {k: _arr_sha(proc[k]) for k in ("T", "E", "pi", "coords")}
    for k in ("h_exec", "freeze_sha256", "streams", "search_record", "cpu"):
        sel[k] = extra.get(k)
    for k in ("m_norm_quantiles", "report", "P4"):
        sel[k] = rec_s3.get(k)
    sel.update(phase_bins=rec_s3["e5"]["bin_counts"], p_D2a=rec_s3["exact"].get("p_D2a"))
    stage_c = {"M": "1/100", "D4_over_M": d4["mean"] / 0.01, "delta_max": d4["L3"] / 3}
    sel.update(stage_c=stage_c, fallback_list=oc["fallback_list"])
    return num(sel)


def write_selection(out, sel) -> Path:
    path = Path(out) / "SELECTION.json"
    stage_records.write_new(path, sel)
    return path


def write_world_summaries(out, history) -> list:
    """worlds/<key>.json once per evaluated world: every look path and sha256, latest class."""
    paths = []
    for key, looks in sorted(history.items()):
        latest = looks[-1]["record"]
        found = [
            {"path": x["path"], "sha256": stage_records.sha256(Path(out) / x["path"])}
            for x in looks
        ]
        rec = {"key": key, "looks": found, "class": latest["class"]}
        rec.update(bounds=latest.get("bounds"), annotations=latest.get("annotations", []))
        path = Path(out) / "worlds" / f"{key}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        stage_records.write_new(path, num(rec))
        paths.append(path)
    return paths
