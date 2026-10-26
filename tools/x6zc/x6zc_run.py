"""X6ZC run: store records (exclusive create, EXPOSURE, EVALUATIONS, STAGES), the stage-1 store
no-write inventory, environment, closure and master checks, the meter binding and its template,
ledger and pause points, the pure Stage-C pipeline, the report and its schema, the stage-0 dry
run, stages A, B and C with model chunk children, and the CLI (X6ZC-DESIGN-v1 §4-§15; API.md §11,
§15, §20). Torch-heavy X6S1 modules are imported lazily inside the functions that need them."""
# fmt: off

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
import numpy as np  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6zc_census as zs  # noqa: E402

from topo_pilot.contracts import canonical_json  # noqa: E402

C, X = zc.CONTRACT, zc.CONTRACT["x6s1_store"]
FAM, VO, CO = zc.FAMILIES, zc.VARIANT_ORDER, zc.CELL_ORDER
def _utc() -> str: return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def _sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def _norm(p) -> str: return os.path.normcase(os.path.abspath(str(p)))
def _js(v):  # JSON-ready: numpy scalars and arrays, tuple keys "a|b", Fractions "p/q", NaN null
    if isinstance(v, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): _js(x)
                for k, x in v.items()}
    if isinstance(v, (list, tuple, np.ndarray)):
        return [_js(x) for x in (v.tolist() if isinstance(v, np.ndarray) else v)]
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return float(v) if math.isfinite(v) else None
    return f"{v.numerator}/{v.denominator}" if isinstance(v, Fraction) else v
def _cj(obj) -> bytes: return canonical_json(_js(obj)).encode("utf-8")

# ---- records (API §11.1-§11.2) ----
def xwrite(path, data: bytes) -> str:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as fh:  # exclusive create: FileExistsError on an existing file
        fh.write(data)
    return _sha(data)
def _append(path, obj) -> dict:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "ab") as fh:
        fh.write(_cj(obj) + b"\n")
    return obj
def _lines(path) -> list:
    p = Path(path)
    return [json.loads(x) for x in p.read_text("utf-8").splitlines() if x.strip()] if (
        p.exists()) else []
def log_exposure(store, stage, artifact, expected_sha256, purpose) -> dict:
    ex = _lines(Path(store) / "EXPOSURE.jsonl")
    k = 1 + sum(str(e.get("id", "")).startswith("X") for e in ex)
    return _append(Path(store) / "EXPOSURE.jsonl", {
        "id": f"X{k}", "stage": stage, "store": "x6-stage1-store", "artifact": artifact,
        "expected_sha256": expected_sha256, "purpose": purpose, "utc": _utc()})
def guard(stage, set_name) -> None:
    if set_name == "fresh" and stage != "C":
        raise RuntimeError(f"a model evaluation on the fresh set outside Stage C ({stage})")
def log_evaluation(store, model, kind, stage, set_name) -> dict:
    guard(stage, set_name)
    return _append(Path(store) / "EVALUATIONS.jsonl", {
        "model": model, "kind": kind, "stage": stage, "set": set_name, "utc": _utc()})
def write_stage(store, stage, record) -> Path:
    p = Path(store) / "stages" / stage / "record.json"
    sha = xwrite(p, _cj(record))
    _append(Path(store) / "STAGES.jsonl", {"stage": stage, "record_sha256": sha,
                                           "stop": record.get("stop"), "utc": _utc()})
    return p
def write_ruling(store, rid, check, stage, cause_identified, affects_beta, cause, defect_md=None,
                 setup=False) -> Path:
    p = Path(store) / "rulings" / f"{rid}.json"
    xwrite(p, _cj({"id": rid, "check": check, "stage": stage, "cause": cause, "setup": setup,
                   "cause_identified": bool(cause_identified), "affects_beta": bool(affects_beta),
                   "defect_md": defect_md, "utc": _utc()}))
    return p
def rulings(store) -> list:
    return [json.loads(p.read_text("utf-8"))
            for p in sorted((Path(store) / "rulings").glob("*.json"))]

# ---- guards and environment (API §11.3) ----
def x6s1_inventory(store=zc.X6S1_STORE) -> dict:
    root, out = Path(store), {}
    for d, dirs, files in os.walk(root):
        for s in [x for x in dirs if x == "sealed"]:  # never listed: only its own mtime (C-15)
            dirs.remove(s)
            rel = (Path(d) / s).relative_to(root).as_posix() + "/"
            out[rel] = [0, os.stat(Path(d) / s).st_mtime_ns]
        for f in files:
            st = os.stat(Path(d) / f)
            out[(Path(d) / f).relative_to(root).as_posix()] = [st.st_size, st.st_mtime_ns]
    return out
def inventory_equal(a, b) -> bool:
    return {k: list(v) for k, v in a.items()} == {k: list(v) for k, v in b.items()}
def env_check(env) -> dict:
    import x6s1_run as sr
    ref = json.loads((Path(zc.X6S1_STORE) / X["env_reference"]["path"]).read_bytes())["env_local"]
    ch = sr.env_changed(env, ref)
    return {"status": "PASS" if set(ch) <= {"commit"} else "SETUP_ERROR", "changed": ch}
def closure_diff(worktree=zc.WORKTREE) -> list:
    out = subprocess.run(["git", "-C", str(worktree), "diff", "--name-status", zc.H3, "HEAD", "--",
                          *zc.CLOSURE], capture_output=True, text=True, check=True).stdout
    return [ln for ln in out.splitlines() if ln.strip()]
def _hit(v, master) -> bool:
    if isinstance(v, dict):
        return any(_hit(x, master) for x in v.values())
    if isinstance(v, (list, tuple)):
        return any(_hit(x, master) for x in v)
    return isinstance(v, (int, np.integer)) and not isinstance(v, bool) and int(v) == master
def master_fresh(project_root=zc.PROJECT_ROOT, master=zc.X6ZC_MASTER) -> dict:
    hits = []
    for root in sorted(p for p in Path(project_root).glob("*store*") if p.is_dir()):
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x not in ("sealed", ".git", ".venv")]
            try:
                m = json.loads((Path(d) / "meta.json").read_text("utf-8")) if (
                    "meta.json" in files) else {}
            except (OSError, ValueError):
                continue
            hits += [str(Path(d) / "meta.json")] * (_hit(m.get("seed_map"), master)
                                                     or _hit(m.get("config"), master))
    import x6s1_data as sd
    return {"fresh": not hits and master not in (sd.DATA_MASTER, sd.MODEL_MASTER), "hits": hits}
def meter_bind_check(path, expected_sha256, import_dir) -> None:
    if _sha(Path(path).read_bytes()) != str(expected_sha256).strip().lower():
        raise RuntimeError(f"meter binding {path}: sha256 differs from FREEZE.json")
    if _norm(import_dir) != _norm(zc.METER_IMPORT_DIR):
        raise RuntimeError(f"meter import directory {import_dir} is not the X6ZC worktree's")
BIND_TEMPLATE = '''"""x6zc-store meter binding (BIND_TEMPLATE of tools/x6zc/x6zc_run.py): the
project meter, unchanged, with its store globals rebound to x6zc-store (--max-cpu inf)."""
import sys
from pathlib import Path
IMPORT_DIR, STORE = r"{import_dir}", Path(r"{store}")
sys.path.insert(0, IMPORT_DIR)
import meter  # noqa: E402
meter.OUT, meter.LEDGER = STORE, STORE / "cpu_ledger.json"
meter.EMERGENCY, meter.LOCK = STORE / "cpu_ledger.emergency.jsonl", STORE / "RUN.lock"
meter.ACTIVE, meter.LOG_DIR = STORE / "METER_ACTIVE.lock", STORE / "logs"
meter.WORKER_SESSION = r"{session}"
if __name__ == "__main__":
    sys.exit(meter.main())
'''
def bind_template(out, session, store=zc.STORE, import_dir=zc.METER_IMPORT_DIR) -> str:
    return xwrite(out, BIND_TEMPLATE.format(import_dir=import_dir, store=store,
                                            session=session).encode("utf-8"))
def ledger_cpu(store) -> float:
    led = json.loads((Path(store) / "cpu_ledger.json").read_text("utf-8"))
    return float(led["cumulative_cpu_s"])
def pause_check(boundary, cumulative_s, stage_s, n=None) -> dict:
    P = C["budget"]["pause"]
    key = boundary if boundary != "C" else {1024: "C_1024", 2048: "C_2048"}.get(n, "C_any")
    if key == "C_any":
        (a, b), (s,) = (map(float, re.findall(r"[\d.]+", P[key][k]))
                        for k in ("cumulative", "stage"))
        cum, st = a + b * n, s * n
    else:
        cum, st = P[key]["cumulative"], P[key]["stage"]
    return {"pause": cumulative_s > cum or stage_s > st, "cumulative_threshold": cum,
            "stage_threshold": st, "boundary": key}

# ---- pure pipeline (API §11.4; no I/O) ----
def predict_variants(pred, arrays_by_family) -> dict:
    return {F: {v: (pred(A[f"{v}_a"], t), pred(A[f"{v}_b"], t))
                for v in VO for t in [np.asarray(A[f"{v}_t"], np.int64)]}
            for F, A in arrays_by_family.items()}
def stage_c_statistics(outputs, arrays_by_family, qstar_fn, gen, drop_pairs=None,
                       drop_clusters=None) -> dict:
    P0 = 1 + max(int(np.max(A["prefix"], initial=-1)) for A in arrays_by_family.values())
    keep = np.ones(P0, bool) if drop_clusters is None else ~np.asarray(drop_clusters, bool)
    new, P, Q = np.cumsum(keep) - 1, int(keep.sum()), {}
    for F, A in arrays_by_family.items():
        for v in VO:
            t, cl = np.asarray(A[f"{v}_t"], np.int64), np.asarray(A["prefix"], np.int64)
            mk = keep[cl] & ~(np.zeros(len(cl), bool) if drop_pairs is None else drop_pairs[F][v])
            Q[F, v] = (qstar_fn(A[f"{v}_a"], t)[0], qstar_fn(A[f"{v}_b"], t)[0], new[cl][mk],
                       np.asarray(A[f"{v}_y"], np.int64)[mk], mk)
    point, beta_y, rho, num_d, den_d = {}, {}, {}, {}, {}
    for (name, out), (F, v) in ((x, k) for x in outputs.items() for k in Q):
        qa, qb, cl, y, mk = Q[F, v]
        pa, pb = out[F][v]
        num, den = (x[mk] for x in se.pair_terms(pa, pb, qa, qb))
        dp2 = ((se.cue_normalise(pa) - se.cue_normalise(pb)) ** 2).sum(1)[mk]
        key = (name, F, v)
        point[key], beta_y[key] = se.beta_fsum(num, den), [se.beta_fsum(num[y == z], den[y == z])
                                                            for z in range(3)]
        rho[key] = math.fsum(dp2) / math.fsum(den) if math.fsum(den) else math.nan
        for st, (nn, dd) in [("beta", (num, den)), ("rho", (dp2, den))] + [
                (f"beta_y{z}", (num * (y == z), den * (y == z))) for z in range(3)]:
            num_d[f"{name}|{F}|{v}|{st}"] = zc.cluster_sums(nn, cl, P)
            den_d[f"{name}|{F}|{v}|{st}"] = zc.cluster_sums(dd, cl, P)
    draws, cells, errs = zc.paired_cluster_boot(num_d, den_d, zc.B_DRAWS, gen), {}, {}
    for c in CO:
        try:
            cells[c] = zc.cell_statistics(point, draws, c) if (
                zc.CELLS[c]["model"] in outputs) else None
        except ValueError as e:  # non-finite draws: no interval (C-21 -> G-R1)
            cells[c], errs[c] = None, str(e)
    vals = {F: {m: point[(m, F, "PP")] for m in zc.K6_CONTROLS[F] if (m, F, "PP") in point}
            for F in FAM}
    k6 = {F: sum(abs(x) <= float(zc.T["placebo"]) for x in vals[F].values()) >= zc.K6_MIN[F]
          for F in FAM}
    return {"point": point, "beta_y": beta_y, "rho": rho, "draws": draws, "cells": cells,
            "k6": {**k6, "values": vals}, "n_clusters": P, "cell_errors": errs}
def _f4(x) -> str: return "n/a" if x is None or (isinstance(x, float) and x != x) else f"{x:.4f}"
def licence_values(cell, stats, dc, ev) -> dict:
    s, c, pt = (stats.get("cells") or {}).get(cell) or {}, zc.CELLS[cell], stats.get("point", {})
    r = s.get("r") or {}
    seven = [m for m in ("AB-s1", "AB-s2", "AB-s3", "AB-s4", "ZC-s2", "ZC-s3", "ZC-s4")
             if (m, "W2", "PP") in pt]
    exc = [m for m in seven if not abs(pt[(m, "W2", "PP")]) <= float(zc.T["placebo"])]
    his = [r[v]["hi"] for v in r if r[v].get("hi") is not None]
    cause = "; ".join(x["cause"] for x in ev.get("rulings", []) if x.get("affects_beta"))
    return {"model": c["model"], "family": c["family"], "cell": cell, "n": stats.get("n_clusters"),
            "beta_d3": f"{c['beta_D']:.3f}", "b_label": "β_PP" if c["sign"] > 0 else "−β_PP",
            "b": _f4(s.get("b")), "beta_pp": _f4(s.get("beta_pp")), "lo": _f4(s.get("b_lo")),
            "hi": _f4(s.get("b_hi")), "level": c["b_level"], "k": len(seven) - len(exc),
            "exceptions": f"; exception: {', '.join(exc)}" if exc else "",
            **{f"r_{v.lower()}": _f4((r.get(v) or {}).get("point")) for v in VO[1:]},
            "r_values": ", ".join(f"{v} {_f4((r.get(v) or {}).get('point'))}" for v in VO[1:]),
            "intervals": "; ".join(f"{v} [{_f4(r[v]['lo'])}, {_f4(r[v]['hi'])}]" for v in r),
            "upper": _f4(max(his) * s["beta_pp"] if his and s.get("beta_pp") is not None else None),
            "predictor": ev.get("k1_predictor", "an exactly commutative predictor"),
            "value": f"{c['beta_D']:.4f}", "defect": cause or "the identified defect",
            "corrected": "not computed here (§10)", "outcome": dc["outcome"],
            "descriptive": " (descriptive)" if dc["descriptive"] else "",
            "numbers": f"b = {_f4(s.get('b'))}, interval [{_f4(s.get('b_lo'))}, "
                       f"{_f4(s.get('b_hi'))}], undefined ratio draws "
                       f"{_f4(s.get('undefined_frac'))}"}
def decide_report(stats, ev_base, census=None) -> dict:
    ev = {**ev_base, "k6": {F: stats["k6"][F] for F in FAM}, "cells": stats["cells"]}
    ev["incomplete"] = bool(ev.get("incomplete") or stats.get("cell_errors"))
    d = zc.decide_x6zc(ev)
    lic = {c: zc.licence(d["cells"][c]["outcome"], licence_values(c, stats, d["cells"][c], ev),
                         d["cells"][c]["licence_case"]) for c in CO}
    return {"decision": d, "qualifiers": zc.qualifiers(ev, d, census), "licences": lic,
            "not_licensed": {c: zc.not_licensed(d["cells"][c]["outcome"],
                                                d["cells"][c]["licence_case"]) for c in CO},
            "reuse_verdict": zc.reuse_verdict(ev, d), "ev": ev}
TOP = ("schema", "protocol_id", "protocol_sha256", "head", "x6zc_master", "outcome", "global_rule",
       "cells", "r_w1_p", "k6", "f1", "k0", "coupling", "stage_b", "reuse_verdict",
       "x6s1_statement", "descriptive", "exposure", "sensitivity", "follow_up", "budget", "n",
       "n_avail", "r_star", "stages", "env")
CELL_KEYS = ("model", "family", "rule", "outcome", "licence", "not_licensed", "qualifiers", "b",
             "b_interval", "beta_pp", "r", "undefined_frac", "beta_sb", "n", "descriptive")
_OUTS = set(C["outcomes"]["global"].values()) | {o["P"] for o in C["outcomes"]["cell"].values()} | {
    o["S"] for o in C["outcomes"]["cell"].values()}
def _outcome_ok(o) -> bool:
    return isinstance(o, str) and (o in _OUTS or bool(re.fullmatch(
        r"UNEXPLAINED/NOT_DISCRIMINABLE\(M[0-9a-z+]+(, M[0-9a-z+]+)*\)", o)))
def validate_report(report) -> list:
    err = [f"missing key {k}" for k in TOP if k not in report]
    err += [] if report.get("schema", "x6zc-report-v1") == "x6zc-report-v1" else ["schema"]
    err += [] if "outcome" not in report or _outcome_ok(report["outcome"]) else ["outcome"]
    cells = report.get("cells") if isinstance(report.get("cells"), dict) else {}
    for c in CO:
        x = cells.get(c)
        if not isinstance(x, dict):
            err += [f"cell {c} missing"] * ("cells" in report)
            continue
        err += [f"cell {c}: missing {k}" for k in CELL_KEYS if k not in x]
        err += [] if _outcome_ok(x.get("outcome")) else [f"cell {c}: outcome {x.get('outcome')}"]
        err += [f"cell {c}: licence for {x.get('outcome')}"] * bool(
            x.get("outcome") in ("STOP_REPLAN", "INVALID") and x.get("licence"))
    return err

# ---- the stage-0 dry run (§12; API §15) ----
class Planted:
    """p = Z + sum_k f_k(prefix) (P_k - Z), Z = q*_ZC, P_k a SyntheticPredictor selected by
    "family" or "family|variant"; f_k = 1 + u (centred jitter, |u| <= 1/5) or a given map."""
    _Z = zc.oracle("ZC", "qstar")
    def __init__(self, name, comps, paths):
        self.name, self.comps, self.paths = name, comps, paths
    def __call__(self, tokens, t):
        tok = np.asarray(tokens)
        ts = np.broadcast_to(np.asarray(t, np.int64), (len(tok),))
        z, info = self._Z(tok, ts), [self._info(r, k) for r, k in zip(tok, ts)]
        out = z.copy()
        for sel, pred, wt in self.comps:
            f = np.array([wt(i[3]) if {i[0], f"{i[0]}|{i[1]}"} & sel else 0.0 for i in info])
            idx = np.flatnonzero(f)
            out[idx] += f[idx, None] * (pred(tok[idx], ts[idx]) - z[idx]) if len(idx) else 0
        return out
    def _info(self, row, t):
        p = sd_parse(row[:t])
        return self.paths[tuple(p["segment"][1:])] + (tuple(int(w) for w in p["prefix"]),)
def sd_parse(row) -> dict:
    import x6_model as xm
    return xm.parse([int(w) for w in row])
def _jitter(prefixes, fid) -> dict:
    keys = sorted(set(prefixes))
    u = zc.dry_stream("jitter", fid).uniform(-0.1, 0.1, len(keys))
    cnt = np.array([prefixes.count(k) for k in keys], np.float64)
    u -= (cnt * u).sum() / cnt.sum()  # centred over the prefix rows: |u| <= 1/5 (C-14)
    return {k: 1.0 + float(x) for k, x in zip(keys, u)}
def _pool(gen, rows=4096) -> np.ndarray:
    import x6_model as xm
    out = np.zeros((rows, 33), np.uint8)
    for r in range(rows):
        v = int(gen.choice([i for i in range(16) if i != xm.ANCHOR]))
        for k in range(33):
            v = xm.NEIGHBOURS[v][int(gen.integers(0, 5))] if k else v
            out[r, k] = 15 + int(gen.integers(0, 3)) if v == xm.ANCHOR else xm.tok(v)
    return out
def _ev(**kw) -> dict:
    return {"k0": "PASS", "incomplete": False, "rulings": [], "k1": "PASS", "a2_k5_pass": True,
            "checks": dict.fromkeys(("A1", "A2", "A_audit", "K2", "K4", "K5"), "PASS"),
            "n_avail": 2400, "k6": {F: True for F in FAM}, "b9": {
                "n": 1024, "status": "OK", "candidates": [1024], "h": {},
                "underpowered": dict.fromkeys(CO, False), "low_feasibility": ["S3"]},
            "f1": {F: {"m0_ok": True, "passed": True, "failed": []} for F in FAM}, **kw}
def dry(scratch=zc.DRY_STORE, fixtures=None, faults=None) -> dict:
    """Stage 0: every CONTRACT dry-run fixture through the pipeline on synthetic data only."""
    import torch
    import x6s1_cloud as sc
    import x6s1_data as sd

    from topo_pilot.learner import TransformerLM
    if faults and not _norm(scratch).startswith(_norm(zc.SCRATCH_ROOT)):
        raise RuntimeError("fault injection is accepted only under SCRATCH_ROOT")
    cpu0, S, FX = time.process_time(), Path(scratch), C["dry_run"]["fixtures"]
    want = {f["id"]: f for f in FX if fixtures is None or f["id"] in fixtures}
    paths = {}
    for v, m in ((v, m) for v in VO for m in "ab"):
        paths.update({zc.variant_path(F, v, m): (F, v, m) for F in FAM})
    pool = _pool(zc.dry_stream("pool"))
    D = sp.designed_set(pool)
    fr = zc.fresh_prefixes(pool, D["prefixes"])
    fresh = [p for _, p in fr["fresh"]][:int(C["dry_run"]["model_fresh_n"])]
    VA = {F: zc.variant_arrays(fresh, F) for F in FAM}
    cache, got, n_hist = zc.QStarCache.build(list(VA.values())), {}, 0
    zc_out = predict_variants(Planted("ZC", [], paths), VA)
    def stats(planted, va=VA, qf=cache, seed="stats"):
        if (seed, va is VA) in memo:
            return memo[seed, va is VA]
        base = zc_out if va is VA else predict_variants(Planted("ZC", [], paths), va)
        outs = {m: predict_variants(planted[m], va) if m in planted else base
                for m in zc.STAGE_B_ORDER}
        memo[seed, va is VA] = stage_c_statistics(outs, va, qf, zc.dry_stream(seed))
        return memo[seed, va is VA]
    memo = {}
    def pl(fid, model, *comps):
        J = _jitter(fresh, fid)
        def wt(j): return (lambda q: J.get(q, 1.0)) if j else (lambda q: 1.0)
        return {model: Planted(model, [(sel, zc.SyntheticPredictor(k, **p), wt(j))
                                       for sel, k, j, p in comps], paths)}
    F5, F20 = Fraction(1, 5), Fraction(1, 20)
    plants = {
        "DR01": pl("DR01", "ZC-s1", ({"W2|PP", "W2|MM", "W2|MP"}, "M0", 1, {"w": F5}),
                   ({"W2|PM"}, "M0", 1, {"w": 2 * F5})),
        "DR02": pl("DR02", "ZC-s1", (set(FAM), "M0", 1, {"w": F5})),
        "DR03": pl("DR03", "ZC-s1", ({"W2"}, "M2a", 1, {"pi_a": F20, "pi_b": F5 + F20})),
        "DR04": pl("DR04", "ZC-s3", ({"W1"}, "M2a", 1, {"pi_a": F5 + F20, "pi_b": F20})),
        "DR05": pl("DR05", "ZC-s1", ({"W2"}, "M1", 1, {"kappa_a": Fraction(17, 20),
                                                       "kappa_b": Fraction(11, 20)})),
        "DR06": {"ZC-s1": Planted("DR06", [({"W2"}, zc.SyntheticPredictor("M0", w=F5), (
            lambda q, s={zc._ints(p) for _, p in D["prefixes"]} - set(fresh): float(q in s)))],
            paths)},
        "DR07": pl("DR07", "ZC-s1", ({"W2"}, "M0", 1, {"w": F20})),
        "DR08": {"ZC-s1": Planted("DR08", [*pl("DR08", "ZC-s1", ({"W2"}, "M0", 1, {
            "w": 3 * F20}))["ZC-s1"].comps, *pl("DR08b", "ZC-s1", ({"W2"}, "M2a", 1, {
                "pi_a": Fraction(0), "pi_b": F20}))["ZC-s1"].comps], paths)},
        "DR10": {**pl("DR03", "ZC-s1", ({"W2"}, "M2a", 1, {"pi_a": F20, "pi_b": F5 + F20})),
                 **pl("x", "AB-s1", ({"W2"}, "M0", 0, {"w": F5})),
                 **pl("x", "ZC-s2", ({"W2"}, "M0", 0, {"w": F5}))}}
    for fid in (f for f in plants if f in want):
        rep = decide_report(stats(plants[fid], seed=fid), _ev())
        dc = rep["decision"]["cells"]["S3" if fid == "DR04" else "P"]
        got[fid], got[f"{fid}_licence_case"] = dc["outcome"], dc["licence_case"]
    if "DR09" in want:  # statistics-level plant (C-50, R-0117-1)
        pp = np.r_[-9.8, np.full(127, 0.3)]
        plant = {("ZC-s1", "W2"): (pp, .3, .3, .3), ("ZC-s1", "W1"): (.3,) * 4,
                 ("ZC-s3", "W1"): (-.3, .3, -.15, .15), ("ZC-s4", "W1"): (-.3, .3, -.15, .15)}
        num = {f"{m}|{F}|{v}|beta": np.broadcast_to(np.asarray(x, np.float64), (128,)).copy()
               for (m, F), vals in plant.items() for v, x in zip(VO, vals)}
        dr = zc.paired_cluster_boot(num, {k: np.ones(128) for k in num}, 5000,
                                    zc.dry_stream("DR09"))
        pt = {tuple(k.split("|")[:3]): math.fsum(num[k]) / 128 for k in num}
        st = {"point": pt, "draws": dr, "cells": {c: zc.cell_statistics(pt, dr, c) for c in CO},
              "k6": {"W2": True, "W1": True}, "n_clusters": 128}
        got["DR09"] = decide_report(st, _ev())["decision"]["cells"]["P"]["outcome"]
    if want.keys() & {"DR11", "DR12"}:
        rows = [r for r, _ in zc.prefix_yields(pool, zc.SeedTree(sd.DATA_MASTER).generator(
            *zc._X["prefix_len_stream"]))]
        short = pool[:rows[1279] + 1]
        fr2 = zc.fresh_prefixes(short, sp.designed_set(short)["prefixes"])
        b9 = zc.choose_n(fr2["n_avail"], dict.fromkeys(CO, 0.01))
        va2 = {F: zc.variant_arrays([p for _, p in fr2["fresh"]], F) for F in FAM}
        st = stats(plants["DR02"], va2, zc.QStarCache.build(list(va2.values())), "DR11")
        got["DR11"] = decide_report(st, _ev(n_avail=fr2["n_avail"], b9=b9))["decision"]["cells"][
            "P"]["outcome"] if fr2["not_enough_data"] else "N_AVAIL>=512"
        b9 = zc.choose_n(2400, {"P": 0.05, "S3": 0.001, "S4": 0.001})
        got["DR12"] = decide_report(stats(plants["DR02"], seed="DR02"), _ev(b9=b9))[
            "decision"]["cells"]["P"]["outcome"]
    A = {F: zc.variant_arrays(fresh[:4], F) for F in FAM}
    if "DR13" in want:  # a pipeline that swaps a and b on the predictor side (§20 E-3)
        sw = {}
        for k in ("qstar", "h_last", "h_first", "h_rev"):
            t = zc.pair_arrays(zc.oracle("NA", k), A["W2"], "PP", cache)
            sw[k] = {**t, "num": se.pair_terms(t["p_b"], t["p_a"], t["q_a"], t["q_b"])[0]}
        k2 = zc.k2_check(sw, "W2")
        k5 = zs.k5_independent(sw["qstar"], se.beta_fsum(sw["qstar"]["num"], sw["qstar"]["den"]))
        fails = {"K2": k2["status"], "K5": "FAIL" if k5["status"] != "PASS" else "PASS"}
        rul = [{"id": f"DR13-{c}", "check": c, "cause_identified": True, "affects_beta": True,
                "cause": "a/b swapped between p and q*"} for c, s in fails.items() if s == "FAIL"]
        got["DR13"] = decide_report(stats(plants["DR02"], seed="DR02"), _ev(
            checks={**_ev()["checks"], **fails}, rulings=rul))["decision"]["global_outcome"]
        got["DR13_k5_flags"] = k5["status"]
    if "DR14" in want:
        def nudge(tok, ts):
            p = Planted._Z(tok, ts)
            p[[zc.member_of(r[:k]) == "a" for r, k in zip(tok, ts)], 15] += 1e-6
            return p / p.sum(1)[:, None]
        k1 = zc.k1_check(zc.pair_arrays(nudge, A["W2"], "PP", cache))
        got["DR14"] = decide_report(stats(plants["DR02"], seed="DR02"), _ev(
            k1=k1["status"], a2_k5_pass=True))["decision"]["global_outcome"]
    if "DR15" in want:
        g = zc.oracle_geometry({**A["W1"], "PM_b": A["W1"]["PM_a"].copy()}, "W1")
        got["DR15"] = decide_report(stats(plants["DR02"], seed="DR02"), _ev(k0=g["status"]))[
            "decision"]["global_outcome"]
    checks = {}
    if "DR16" in want:
        checks["DR16"] = all(zc.beta_exact_pi0(p.exact, F, "PP") == d and abs(se.beta_fsum(
            *(lambda t: (t["num"], t["den"]))(zc.pair_arrays(p, A[F], "PP", cache))) - float(d))
            <= 1e-12 for d in (0, F20, 2 * F20, F5, 5 * F20, 1) for F in FAM
            for p in [zc.SyntheticPredictor("mixture", S="Parikh", delta=d)])
    if "DR17" in want:
        t = zc.pair_arrays(zc.SyntheticPredictor("M0+M2a", w=3 * F20, pi_a=0, pi_b=F20), A["W2"],
                           "PM", cache)
        dup = {k: np.concatenate([v, v]) for k, v in A["W2"].items()}
        t2 = zc.pair_arrays(zc.SyntheticPredictor("M0+M2a", w=3 * F20, pi_a=0, pi_b=F20), dup,
                            "PM", cache)
        s1, s2 = zc.pair_stats(t), zc.pair_stats(t2)
        checks["DR17"] = (zs.k5_swap(t)["status"] == zs.k5_permutation(t)["status"] == "PASS"
                          and abs(s1["beta"] - s2["beta"]) <= 1e-15)
    if "DR18" in want:
        rej = 0
        for bad in ({**A["W2"], "PP_b": A["W2"]["PP_b"][:-3]},
                    {**A["W2"], "PP_y": A["W2"]["PP_y"][:-1]}):
            try:
                zc.pair_arrays(zc.oracle("NA", "qstar"), bad, "PP", cache)
            except ValueError:
                rej += 1
        g = zc.oracle_geometry({**A["W2"], "PP_t": (A["W2"]["PP_t"] - 1).astype(np.int16)}, "W2",
                               ("PP",))
        checks["DR18"] = rej == 2 and g["status"] == "FAIL" and g["counterexample"]["item"] == 2
    if "DR19" in want:
        def no_cue(tok, ts): return np.pad(np.full((len(tok), 15), 1 / 15), ((0, 0), (0, 3)))
        st0 = zc.pair_stats(zc.pair_arrays(no_cue, A["W2"], "PP", cache))
        tz = zc.pair_arrays(zc.oracle("NA", "qstar"), A["W2"], "PP", lambda tk, u: se.qstar(
            "ZC", tk, u))
        try:
            zc.interval(np.full(50, np.nan), (0.025, 0.975))
            inv = False
        except ValueError:
            inv = True
        checks["DR19"] = st0["nonfinite"] and math.isnan(st0["beta"]) and inv and math.isnan(
            se.beta_fsum(tz["num"], tz["den"]))
    if "DR20" in want:
        A5 = zc.variant_arrays([(), (10,), (10,), (6, 5, 9), ()], "W2")
        rng = zc.dry_stream("DR20")
        def rp(tok, ts):
            m = rng.uniform(0.1, 0.3, len(tok))
            return np.c_[rng.dirichlet(np.ones(15), len(tok)) * (1 - m)[:, None],
                         rng.dirichlet(np.ones(3), len(tok)) * m[:, None]]
        checks["DR20"] = zs.d2_decompose(zc.pair_arrays(rp, A5, "PP", se_qstar))[
            "identity_max_abs"] <= 1e-12
    if "DR21" in want:
        checks["DR21"] = (zs.crosses(0.0999999, 0.1000001) and not zs.crosses(0.1 - 5e-10, 0.2)
                          and zs.crosses(-0.2, 0.05))
    if "DR22" in want:
        led = S / "dr22" / "cpu_ledger.json"
        if not led.exists():
            xwrite(led, _cj({"cumulative_cpu_s": 3 * 720 + 1}))
        checks["DR22"] = pause_check("0", ledger_cpu(led.parent), 0.0)["pause"]
    models = {}  # two random-init models as fake checkpoints with fake locks (sha checks)
    for k in (1, 2):
        torch.manual_seed(int(zc.dry_stream("model", k).integers(2**31)))
        sd_, buf = TransformerLM(sd.MODEL_CFG).state_dict(), io.BytesIO()
        torch.save({"model": sd_, "step": 0}, buf)
        p = S / "ckpt" / f"init-dry{k}.pt"
        if not p.exists():
            xwrite(p, buf.getvalue())
        models[k] = se.ModelPredictor(p, _sha(p.read_bytes()), sc.weights_digest(sd_))
    sub = {k: v if k.startswith("W3") else v[:3 * int(C["dry_run"]["model_prefixes_D"])]
           for k, v in sp.designed_arrays(D).items()}
    kq, eps = np.arange(sd.Q + 1, dtype=np.float64), float(sd.EPS)
    import x6s1_stats as ss
    qv = np.array([float(q) for q in ss.qvals()])
    tables = {"lnp": np.log((1 - eps) * kq / sd.Q + eps / 18), "fl_q": qv,
              "qlnq": np.where(qv > 0, qv * np.log(np.where(qv > 0, qv, 1.0)), 0.0)}
    cD, ok_models = zc.QStarCache.build([sub]), True
    for m in models.values():
        ds = se.designed_stats(m, sub, cD, tables)
        o = predict_variants(m, VA)
        n_hist += sum(len(x) for k, x in sub.items() if k[-2:] in ("_a", "_b")) + sum(
            len(p) for F in FAM for v in VO for p in o[F][v])
        ok_models &= not ds["nonfinite"] and all(np.isfinite(p).all() for F in FAM for v in VO
                                                 for p in o[F][v])
    checks["models"] = bool(ok_models)
    res = []
    for f in want.values():
        g = got.get(f["id"], checks.get(f["id"]))
        res.append({"id": f["id"], "expected": f["expected"], "got": g,
                    "pass": g is True or g == f["expected"]})
    rep = {"schema": "x6zc-dry-v1", "fixtures": res, "all_pass": all(r["pass"] for r in res)
           and ok_models, "cpu_per_history_s": (time.process_time() - cpu0) / max(n_hist, 1),
           "dr13_k5": got.get("DR13_k5_flags"), "models_ok": bool(ok_models),
           "n_avail": fr["n_avail"], "r_star": fr["r_star"], "utc": _utc()}
    k = sum(1 for _ in S.glob("report*.json"))
    rep["sha256"] = xwrite(S / (f"report-r{k}.json" if k else "report.json"), _cj(rep))
    return rep
def se_qstar(tok, t): return se.qstar("NA", tok, t)

# ---- stages A, B, C (§6-§8; API §11.4): only after FREEZE.json and AUTH.json ----
def _x6(rel) -> Path: return Path(zc.X6S1_STORE) / rel
def _payload(store, stage, rel, sha, purpose) -> bytes:
    log_exposure(store, stage, rel, sha, purpose)  # written before the payload is opened
    data = _x6(rel).read_bytes()
    if sha and _sha(data) != str(sha).lower():
        raise ValueError(f"{rel}: sha256 differs from the CONTRACT binding")
    return data
def _npz(data) -> dict:
    z = np.load(io.BytesIO(data), allow_pickle=False)
    return {k: z[k] for k in z.files}
def _head() -> str:
    return subprocess.run(["git", "-C", zc.WORKTREE, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
def _dirs(store, stage) -> list:
    out, k = [], 0
    while (Path(store) / "stages" / (f"{stage}-r{k}" if k else stage) / "record.json").exists():
        out, k = out + [f"{stage}-r{k}" if k else stage], k + 1
    return out
def _record(store, stage) -> tuple:  # (directory, record) of the latest attempt (G2 reruns)
    d = _dirs(store, stage)[-1]
    return d, json.loads((Path(store) / "stages" / d / "record.json").read_text("utf-8"))
def _begin(store, stage) -> dict:
    import x6s1_run as sr
    fz = _frozen(store)
    meter_bind_check(Path(store) / "x6zc_meter_bind.py", fz["meter_bind_sha256"],
                     fz["meter_import_dir"])
    se.set_threads()
    env, k = sr.env_local(), len(_dirs(store, stage))
    ctx = {"stage": stage, "dir": f"{stage}-r{k}" if k else stage, "env": env,
           "ec": env_check(env), "closure": closure_diff(), "inv0": x6s1_inventory(),
           "cpu0": ledger_cpu(store), "gates": {}, "values": {}, "freeze": fz}
    ctx["stop"] = "SETUP_ERROR" if ctx["ec"]["status"] != "PASS" or ctx["closure"] else None
    return ctx
def _finish(store, ctx, stop=None, n=None) -> int:
    inv1, cpu, d = x6s1_inventory(), ledger_cpu(store), Path(store) / "stages" / ctx["dir"]
    sh = [xwrite(d / f"x6s1_inventory_{k}.json", _cj(v)) for k, v in (("before", ctx["inv0"]),
                                                                       ("after", inv1))]
    eq = inventory_equal(ctx["inv0"], inv1)
    pc = pause_check(ctx["stage"], cpu, cpu - ctx["cpu0"], n)
    stop = stop or ctx["stop"] or (None if eq else "SETUP_ERROR") or (
        "PAUSE" if pc["pause"] else None)
    write_stage(store, ctx["dir"], {
        "stage": ctx["stage"], "head": _head(), "env_local": ctx["env"],
        "env_diff": ctx["ec"]["changed"], "closure_diff": ctx["closure"], "gates": ctx["gates"],
        "inventory": {"before_sha256": sh[0], "after_sha256": sh[1], "equal": eq},
        "values": ctx["values"], "cpu_s": cpu - ctx["cpu0"], "cpu_cumulative_s": cpu, "pause": pc,
        "stop": stop, "utc": _utc()})
    return 2 if stop else 0
def _find(obj, key) -> list:  # every value stored under `key` anywhere in a JSON object
    if isinstance(obj, dict):
        return [obj[key]] * (key in obj) + [x for v in obj.values() for x in _find(v, key)]
    return [x for v in obj for x in _find(v, key)] if isinstance(obj, list) else []
def _passes(obj, name) -> bool:
    f = _find(obj, name)
    return bool(f) and all((x.get("status") if isinstance(x, dict) else x) == "PASS" for x in f)
def a1_check(closure) -> dict:
    import x6s1_decide as sdc
    SD, it = X["stored_designed"], {}
    rb = _x6("stages/E3z/report.json").read_bytes()
    rep, it["1"] = json.loads(rb), _sha(rb) == X["records"]["stages/E3z/report.json"]["sha256"]
    for m in zc.FOCAL:
        db = _x6(SD[m]["dir"] + "/designed.json").read_bytes()
        dj = json.loads(db)
        ds = [d for d in _find(rep, m) if isinstance(d, dict) and "beta_W2" in d]
        it["1"] &= (_sha(db) == SD[m]["designed_json_sha256"] and dj == SD[m]["values"]
                    and any(all(dj.get(k) == v for k, v in d.items()) for d in ds))
    lo = Fraction(X["dw2_lo"])
    o = [sdc.ord_d(*(SD[f"{a}-s{s}"]["values"] for a in ("NA", "init", "AB", "ZC")), lo)
         for s in (1, 2, 3, 4)]
    it["2"] = (o[0]["status"], o[0]["control_limited"], o[0]["reason"]) == (
        "UNRESOLVED", True, "designed placebo ZC") and all(x["status"] == "FAIL" for x in o[1:])
    gates = _lines(_x6("GATES.jsonl"))
    locks = {m: json.loads(_x6(X["admitted"][m]["lock"]).read_bytes()) for m in zc.FOCAL}
    it["3"] = all(locks[m].get(k) == X["admitted"][m][k] for m in zc.FOCAL
                  for k in ("final_file_sha256", "final_weights_sha256", "bundle_id"))
    it["3"] &= all(_passes(gates, g) for g in X["gates_required_pass"] + ["LEARN-TEST"])
    it["3"] &= all(float(x) <= float(X["loss_echo_max_abs_32"]) for x in _find(gates, "max_abs_32"))
    it["4"] = all(_x6(X["admitted"][m]["ckpt"]).is_file() for m in zc.FOCAL)  # stat only (C-48)
    kinds = {e.get("kind") for e in _lines(_x6("EVALUATIONS.jsonl"))}
    sites = sorted([f"tools/x6_stage1/{p.name}", i] for p in (zc.REPO / "tools/x6_stage1").glob(
        "*.py") for i, ln in enumerate(p.read_text("utf-8").splitlines(), 1) if '"prefix"' in ln)
    it["5"] = kinds <= set(X["evaluation_kinds_seen"]) and sites == sorted(X["a1_prefix_sites"])
    it["6"] = not closure
    return {"status": "PASS" if all(it.values()) else "FAIL", "items": it,
            "ord_d": o, "evaluation_kinds": sorted(map(str, kinds))}
_A2_ROW = re.compile(r"\| (\S+) \| `([^`]+?):(\d+)(?:–(\d+))?` \| `(.+?)` \| (.*) \|$")
def a2_check() -> dict:
    sec, rows = (zc.HERE / "API.md").read_text("utf-8").split("## 17.")[1].split("## 18.")[0], {}
    for m in filter(None, map(_A2_ROW.match, sec.splitlines())):
        rid, f, a, b, anchor, why = m.groups()
        got = (zc.REPO / (f if "/" in f else f"tools/x6_stage1/{f}")).read_text(
            "utf-8").splitlines()[int(a) - 1:int(b or a)]
        rows[rid] = {"file": f, "lines": [int(a), int(b or a)], "behaviour": why,
                     "found": any(anchor in x for x in got)}
    ok = len(rows) >= 20 and all(r["found"] for r in rows.values())
    return {"status": "PASS" if ok else "DEFECT_CANDIDATE", "rows": rows}
def stage_a(store=zc.STORE) -> int:
    import x6s1_stage_pre as pre
    ctx = _begin(store, "A")
    if ctx["stop"]:
        return _finish(store, ctx)
    G, V, d = ctx["gates"], ctx["values"], Path(store) / "stages" / ctx["dir"]
    if not (Path(store) / "EXPOSURE.jsonl").exists():
        _append(Path(store) / "EXPOSURE.jsonl", {**C["store"]["exposure_first"], "utc": _utc()})
    G["A1"], G["A2"] = a1_check(ctx["closure"]), a2_check()
    D = _npz(_payload(store, "A", X["designed"]["path"], X["designed"]["file_sha256"], "A-audit"))
    au = {F: zs.audit_pairs(D, F) for F in sp.PAIR_FAMILIES}
    dsh = sp.designed_sha256(D) == X["designed"]["designed_sha256"]
    G["A_audit"] = {"status": "PASS" if dsh and au["W2"]["status"] == au["W1"]["status"] == "PASS"
                    else "DEFECT_CANDIDATE", "families": au, "designed_sha256_equal": dsh}
    pp = X["prefix_pool"]
    log_exposure(store, "A", pp["dir"], pp["token_sha256"], "A3")
    pool = pre.load_obs(zc.X6S1_STORE, "prefix").tokens
    Ds = sp.designed_set(pool)
    fr = zc.fresh_prefixes(pool, Ds["prefixes"])
    fresh = [p for _, p in fr["fresh"]]
    VA = {F: zc.variant_arrays(fresh, F) for F in FAM}
    k0 = {**{f"D_{F}": zc.oracle_geometry(D, F, (F,)) for F in FAM},
          **{f"fresh_{F}": zc.oracle_geometry(VA[F], F) for F in FAM}}
    G["K0"] = {"status": "PASS" if all(r["status"] == "PASS" for r in k0.values()) else "FAIL",
               "results": k0, "controls": zc.oracle_geometry(D, "W2", ("C1", "C2", "C3", "C4"))}
    V.update(fresh=fresh, n_avail=fr["n_avail"], r_star=fr["r_star"],
             d_coincident=fr["d_coincident"], n_d_coincident=fr["n_d_coincident"],
             not_enough_data=fr["not_enough_data"], first_1024_equal=fr["first_1024_equal"],
             d_equal=fr["d_equal"], coupling=zc.coupling_table(),
             d_rebuilt_equal=sp.designed_sha256(sp.designed_arrays(Ds)) == X["designed"][
                 "designed_sha256"])
    if G["K0"]["status"] == "FAIL":
        return _finish(store, ctx, "STOP_REPLAN")  # G-R0 before any model
    cache = zc.QStarCache.build([D, *VA.values()])
    V["qstar_sha256"] = cache.save(d / "qstar_NA.npz")
    k1p = [zc.oracle("ZC", "qstar"), zc.oracle("AB", "qstar"), zc.SyntheticPredictor(
        "set_constant"), zc.SyntheticPredictor("matched_key"), zc.oracle("NA", "q_8")] + [
        zc.oracle("NA", k) for k in ("q_empty", "q_parity", "q_counts", "q_H1", "q_Parikh")]
    k1 = {f"{p.name}|{F}|{src}|{key}": zc.k1_check(zc.pair_arrays(p, A, key, cache))["status"]
          for p in k1p for F in FAM if not (p.name == "q_8" and F == "W1")
          for src, A, keys in (("D", D, (F,)), ("fresh", VA[F], VO)) for key in keys}
    G["K1"] = {"status": "PASS" if set(k1.values()) == {"PASS"} else "FAIL", "results": k1}
    refs = ("qstar", "h_last", "h_first", "h_rev")
    k2 = {f"{s}_{F}": zc.k2_check({k: zc.pair_arrays(zc.oracle("NA", k), A, key, cache)
                                   for k in refs}, F)
          for F in FAM for s, A, key in (("D", D, F), ("fresh", VA[F], "PP"))}
    G["K2"] = {"status": "PASS" if all(r["status"] == "PASS" for r in k2.values()) else "FAIL",
               "results": k2, "variants_exact": {F: zc.k2_exact_variants(F) for F in FAM}}
    k3 = {F: zc.k3_exact(F) for F in FAM}
    tid = zc.SyntheticPredictor("W1_token_identity", eps=Fraction(1, 20))
    G["K3"] = {F: {"exact": k3[F], "float": zc.k3_float_check(F, VA[F], cache)} for F in FAM}
    G["K3"]["W1_token_identity"] = {v: zc.beta_exact_pi0(tid.exact, "W1", v) for v in VO}
    G["F1"] = {F: zc.f1(k3[F]) for F in FAM}
    pools = {name: np.load(io.BytesIO(_payload(store, "A", r["npy"], r["file_sha256"], "A4")),
                           allow_pickle=False) for name, r in X["train_pools_A4"].items()}
    a4 = zs.exposure_report(VA, pools)  # A4: the 7 train pools of §4.4 (MD-7)
    G["A4"] = {"status": "RECORDED", "matches": a4["matches"], "total": a4["total"]}
    V["a4_pair_mask"] = {F: {v: np.flatnonzero(a4["pair_mask"][F][v]) for v in VO} for F in FAM}
    return _finish(store, ctx)
def _cache(store) -> zc.QStarCache:
    dA, A = _record(store, "A")
    return zc.QStarCache.load(Path(store) / "stages" / dA / "qstar_NA.npz",
                              A["values"]["qstar_sha256"])
def _spec(m) -> tuple:  # (store-relative checkpoint, file sha256, weights sha256)
    a = X["admitted"].get(m)
    if a:
        return a["ckpt"], a["final_file_sha256"], a["final_weights_sha256"]
    i = X["inits"][m] if m in X["inits"] else X["zc_s1_chain"][m.split("@")[1]]
    return i.get("path", i.get("ckpt")), i["file_sha256"], i["weights_sha256"]
def _predictor(m) -> se.ModelPredictor:
    rel, f, w = _spec(m)
    return se.ModelPredictor(_x6(rel), f, w)  # verifies the file sha256 and the weights digest
class _Memo:  # a predictor answering from precomputed rows of the same arrays (no second forward)
    def __init__(self, rows): self.rows, self.name = rows, "memo"
    def __call__(self, tokens, t): return self.rows[id(tokens)]
def _children(store, stage, names, out_dir) -> dict:
    import x6s1_data as sd
    import x6s1_run as sr
    sr._CTX["store"] = store
    lim, res, todo = sr.limits(), {}, list(names)
    (Path(store) / "logs").mkdir(parents=True, exist_ok=True)
    while todo:
        batch, todo = todo[:sd.MAX_CHILDREN], todo[sd.MAX_CHILDREN:]
        kids = {m: sr.launch([sys.executable, "-s", __file__, "chunk", "--stage", stage,
                              "--model", m, "--store", store, "--out", str(out_dir / m)],
                             Path(store) / "logs" / f"{stage}_{m}_{int(time.time())}.log")
                for m in batch}
        res.update(sr.supervise(kids, lim, "E3"))
    return res
def chunk(stage, model, out, store=zc.STORE) -> int:
    se.set_threads()
    cpu0, o, pred = time.process_time(), Path(out), _predictor(model)
    dA, A = _record(store, "A")
    cache = _cache(store)
    if stage == "B":
        D = _npz(_x6(X["designed"]["path"]).read_bytes())  # logged by the Stage-B parent
        tabs = _npz(_x6(X["log_tables"]["path"]).read_bytes())
        P = {k: pred(v, np.asarray(D[f"{k[:-2]}_t"], np.int64)) for k, v in D.items()
             if k[-2:] in ("_a", "_b")}
        ds = se.designed_stats(_Memo({id(D[k]): v for k, v in P.items()}), D, cache, tabs)
        files = {"designed.json": xwrite(o / "designed.json", _cj(ds))}
    else:
        n = _record(store, "B")[1]["values"]["b9"]["n"]
        VA = {F: zc.variant_arrays([tuple(p) for p in A["values"]["fresh"][:n]], F) for F in FAM}
        P = {f"{F}|{v}|{m}": x for F, d in predict_variants(pred, VA).items() for v, pr in d.items()
             for m, x in zip("ab", pr)}
    buf = io.BytesIO()
    np.savez(buf, **P)
    files = {**(files if stage == "B" else {}), "p.npz": xwrite(o / "p.npz", buf.getvalue())}
    xwrite(o / "chunk.json", _cj({"model": model, "stage": stage, "files": files,
                                  "cpu_s": time.process_time() - cpu0, "utc": _utc()}))
    return 0
def _terms(pa, pb, A, key, qfn) -> dict:  # pair terms of precomputed predictions (zc.pair_arrays)
    t = np.asarray(A[f"{key}_t"], np.int64)
    (qa, ca), (qb, cb) = qfn(A[f"{key}_a"], t), qfn(A[f"{key}_b"], t)
    num, den = se.pair_terms(pa, pb, qa, qb)
    cl = np.asarray(A["prefix"], np.int64) if "prefix" in A else zc.d_cluster(len(t))
    return {"p_a": pa, "p_b": pb, "q_a": qa, "q_b": qb, "codes_a": ca, "codes_b": cb, "num": num,
            "den": den, "y": np.asarray(A[f"{key}_y"], np.int64), "t": t, "cluster": cl,
            "tok_a": A[f"{key}_a"], "tok_b": A[f"{key}_b"]}
def _boot(terms_by_key, gen, P) -> dict:  # B5: one paired prefix-cluster bootstrap on D
    num, den = {}, {}
    for key, T in terms_by_key.items():
        y, cl = T["y"], T["cluster"]
        dp2 = ((se.cue_normalise(T["p_a"]) - se.cue_normalise(T["p_b"])) ** 2).sum(1)
        for st, (nn, dd) in [("beta", (T["num"], T["den"])), ("rho", (dp2, T["den"]))] + [
                (f"beta_y{z}", (T["num"] * (y == z), T["den"] * (y == z))) for z in range(3)]:
            num[f"{key}|{st}"], den[f"{key}|{st}"] = (zc.cluster_sums(x, cl, P) for x in (nn, dd))
    return zc.paired_cluster_boot(num, den, zc.B_DRAWS, gen)
def _arm(m) -> str: return "NA" if m.startswith("init") else m[:2]
def stage_b(store=zc.STORE) -> int:
    import x6_model as xm
    ctx = _begin(store, "B")
    if ctx["stop"]:
        return _finish(store, ctx)
    G, V, d, (_, A) = ctx["gates"], ctx["values"], Path(store) / "stages" / ctx["dir"], _record(
        store, "A")
    D = _npz(_payload(store, "B", X["designed"]["path"], X["designed"]["file_sha256"], "B1"))
    tabs = _npz(_payload(store, "B", X["log_tables"]["path"], X["log_tables"]["file_sha256"], "B1"))
    cache = _cache(store)
    for m in zc.STAGE_B_ORDER:  # known cases first (§7); logged before any payload is opened
        log_exposure(store, "B", _spec(m)[0], _spec(m)[1], f"B1 {m}")
        log_evaluation(store, m, "designed_D", "B", "D")
    V["children"] = _children(store, "B", zc.STAGE_B_ORDER, d)
    if any(r["status"] != "DONE" for r in V["children"].values()):
        return _finish(store, ctx, "CHUNK_FAILED")
    ds = {m: json.loads((d / m / "designed.json").read_text("utf-8")) for m in zc.STAGE_B_ORDER}
    P = {m: _npz((d / m / "p.npz").read_bytes()) for m in zc.STAGE_B_ORDER}
    T = {m: {F: _terms(P[m][f"{F}_a"], P[m][f"{F}_b"], D, F, cache) for F in sp.PAIR_FAMILIES}
         for m in zc.STAGE_B_ORDER}
    k4 = {m: zs.k4_compare(X["stored_designed"][m]["values"], ds[m]) for m in zc.STAGE_B_ORDER}
    tiers = {r["tier"] for r in k4.values()}
    G["K4"] = {"status": next(t for t in ("DEFECT_CANDIDATE", "ENV_DRIFT", "PASS") if t in tiers),
               "models": k4}
    k5, sym = {}, {}
    for m in zc.K5_MODELS:
        for _ in range(2):
            log_exposure(store, "B", _spec(m)[0], _spec(m)[1], f"K5 {m}")
        log_evaluation(store, m, "k5", "B", "D")
        p1, p2 = _predictor(m), _predictor(m)  # (g) two independent loads
        for F in ("W2", "W1"):
            Tm, tok, t = T[m][F], D[f"{F}_a"], np.asarray(D[f"{F}_t"], np.int64)
            s = zs.structural_subset(t, D[f"{F}_y"])
            k5[f"{m}|{F}"] = {
                "a": zs.k5_independent(Tm, ds[m][f"beta_{F}"]), "b": zs.k5_swap(Tm),
                "c": zs.k5_padding(p1, tok, t), "d": zs.k5_batch(p1, tok, t),
                "e": zs.k5_readout_index(p1, D, F), "g": zs.k5_two_loads(p1, p2, tok[s], t[s]),
                "h": zs.k5_scalar_vector(p1, tok[s], t[s]), "i": zs.k5_permutation(Tm),
                "j": zs.k5_bos(p1, tok[s], t[s])}
    bad = {x["status"] for r in k5.values() for x in r.values()} - {"PASS", "NUMERIC_DRIFT"}
    G["K5"] = {"status": "DEFECT_CANDIDATE" if bad else "PASS", "results": k5}
    for m, F in ((m, F) for m in zc.FOCAL for F in ("W2", "W1")):  # K1 of sym(m) (§6, B2 (f))
        sa, sb = zc.sym_arrays(T[m][F]["p_a"], T[m][F]["p_b"])
        sym[f"{m}|{F}"] = zc.k1_check(_terms(sa, sb, D, F, cache))
    G["K1_sym"] = sym
    pre = [zc._ints(xm.parse(zc._ints(D["W2_a"][3 * i, :D["W2_t"][3 * i]]))["prefix"])
           for i in range(len(D["W2_t"]) // 3)]
    named, MF = np.arange(len(pre)) < 6, [(m, F) for m in zc.STAGE_B_ORDER for F in ("W2", "W1")]
    desc = {f"{m}|{F}": {"B3": zs.decompose(T[m][F]), "B4": zs.zc_profile(T[m][F], tabs, _arm(m)),
                         "D2": zs.d2_decompose(T[m][F]),
                         "D3": zs.weighting_summaries(T[m][F], pre, named)} for m, F in MF}
    draws = _boot({f"{m}|{F}": T[m][F] for m, F in MF}, zc.stream("boot_B"), len(pre))
    V["B5"] = {k: {"sd": float(np.std(x, ddof=1)), "ci95": list(zc.interval(x, zc.T["b5_q"]))
                   if np.isfinite(x).all() else None} for k, x in draws.items()}
    V["B6"] = {F: zs.similarity({m: zs._diffs(T[m][F])[0] for m in zc.STAGE_B_ORDER})
               for F in ("W2", "W1")}
    V["B7"] = {m: zs.control_families({"terms": T[m], "designed": ds[m]}) for m in zc.STAGE_B_ORDER}
    b10 = {}
    for c in zc.CELLS.values():  # B10: float32 copy of each focal model on its focal family
        m, F = c["model"], c["family"]
        log_exposure(store, "B", _spec(m)[0], _spec(m)[1], f"B10 {m}")
        log_evaluation(store, m, "b10_float32", "B", "D")
        pm, t = _predictor(m), np.asarray(D[f"{F}_t"], np.int64)
        t32 = _terms(pm.float32(D[f"{F}_a"], t), pm.float32(D[f"{F}_b"], t), D, F, cache)
        b10[f"{m}|{F}"] = zs.float32_replay(se.beta_fsum(t32["num"], t32["den"]),
                                            ds[m][f"beta_{F}"])
    flags = {k: {"READOUT_AMPLIFIED": v["D2"]["readout_amplified"],
                 "MULTIPLICITY_SENSITIVE": v["D3"]["multiplicity_sensitive"],
                 "LENGTH_WEIGHT_SENSITIVE": v["D3"]["length_weight_sensitive"],
                 "PRECISION_SENSITIVE": b10.get(k, {}).get("precision_sensitive", False)}
             for k, v in desc.items()}
    k1A = _record(store, "A")[1]["gates"]["K1"]["status"] == "PASS"
    tier = {f"{m}|{F}": zs.descriptive_tier(
        m, F, k4[m]["tier"], k1A and all(x["status"] == "PASS" for x in sym.values()),
        not bad, zc.pair_stats(T[m][F])["max_pair_diff"], flags[f"{m}|{F}"],
        {"W1": ds[m]["beta_W1"], "W2": ds[m]["beta_W2"]}) for m, F in MF if m[:2] in ("AB", "ZC")}
    V.update(desc=desc, B10=b10, tier=tier, census={
        "qualifiers": {k: [q for q in t["qualifiers"] if q.split("(")[0] in zs._FLAGS]
                       for k, t in tier.items()},
        "numeric_drift": [k for k, r in k5.items() if r["a"]["status"] == "NUMERIC_DRIFT"]})
    se_d = {c: V["B5"][f"{x['model']}|{x['family']}|beta"]["sd"] for c, x in zc.CELLS.items()}
    V["b9"], V["se_d"] = zc.choose_n(A["values"]["n_avail"], se_d), se_d
    if ledger_cpu(store) - ctx["cpu0"] <= C["budget"]["g3_b8_max_stage_b_cpu_s"]:  # G3: B8
        V["B8"] = {}
        for step in X["zc_s1_chain"]:
            m = f"ZC-s1@{step}"
            log_exposure(store, "B", _spec(m)[0], _spec(m)[1], f"B8 {m}")
            log_evaluation(store, "ZC-s1", "b8_emergence", "B", "D")
            pm = _predictor(m)
            V["B8"][step] = {F: zc.pair_stats(_terms(*(pm(D[f"{F}_{x}"], np.asarray(D[
                f"{F}_t"], np.int64)) for x in "ab"), D, F, cache)) for F in ("W2", "W1")}
    return _finish(store, ctx)
def _ev_base(store) -> dict:
    (_, A), (_, B) = _record(store, "A"), _record(store, "B")
    g = {**A["gates"], **B["gates"]}
    def st(k): return g.get(k, {}).get("status", "NOT_RUN")
    k1 = st("K1") == "PASS" and all(x["status"] == "PASS" for x in g.get("K1_sym", {}).values())
    return {"k0": st("K0"), "incomplete": False, "rulings": rulings(store),
            "checks": {k: st(k) for k in ("A1", "A2", "A_audit", "K2", "K4", "K5")},
            "k1": "PASS" if k1 else "FAIL", "a2_k5_pass": st("A2") == st("K5") == "PASS",
            "n_avail": A["values"]["n_avail"], "b9": B["values"]["b9"], "f1": g["F1"]}
def stage_c(store=zc.STORE) -> int:
    ctx = _begin(store, "C")
    if ctx["stop"]:
        return _finish(store, ctx)
    ev, (_, A), (_, B) = _ev_base(store), _record(store, "A"), _record(store, "B")
    try:  # the Stage-B gate: no global rule, every candidate ruled (C-17)
        g = zc.decide_x6zc({**ev, "k6": dict.fromkeys(FAM, True), "cells": {},
                            "b9": {**ev["b9"], "status": "NOT_ENOUGH_DATA"}})["global_rule"]
    except ValueError as e:
        g = f"UNRULED: {e}"
    if g:
        ctx["values"]["gate"] = g
        return _finish(store, ctx, "STAGE_B_GATE")
    V, d, n, av = ctx["values"], Path(store) / "stages" / ctx["dir"], ev["b9"]["n"], A["values"]
    VA = {F: zc.variant_arrays([tuple(p) for p in av["fresh"][:n]], F) for F in FAM}
    cache = _cache(store)
    names = zc.INITS + zc.MODELS
    for m in names:
        log_exposure(store, "C", _spec(m)[0], _spec(m)[1], f"C {m}")
        log_evaluation(store, m, "fresh_variants", "C", "fresh")
    V["children"] = _children(store, "C", names, d)
    if any(r["status"] != "DONE" for r in V["children"].values()):
        return _finish(store, ctx, "CHUNK_FAILED", n)  # G2 allowed: no statistic exists yet
    outs = {m: (lambda P: {F: {v: (P[f"{F}|{v}|a"], P[f"{F}|{v}|b"]) for v in VO} for F in FAM})(
        _npz((d / m / "p.npz").read_bytes())) for m in names}
    extra = {"qstar_NA": predict_variants(zc.oracle("NA", "qstar"), VA), **{
        f"K3:{k}|{p}": predict_variants(zc.SyntheticPredictor(k, **p), VA)
        for k, p in zc.k3_grid()}}
    stats = stage_c_statistics({**outs, **extra}, VA, cache, zc.stream("boot_C"))
    mask = {F: {v: np.isin(np.arange(3 * n), av["a4_pair_mask"][F][v]) for v in VO} for F in FAM}
    sens = {"A4": stage_c_statistics(outs, VA, cache, zc.stream("sens_A4"), drop_pairs=mask),
            "DPREFIX": stage_c_statistics(outs, VA, cache, zc.stream("sens_DPREFIX"),
                                          drop_clusters=np.asarray(av["d_coincident"][:n], bool))}
    census = {**B["values"]["census"], "sensitivity": {k: {c: x["cells"][c]["outcome"] for c in CO}
              for k, s in sens.items() for x in [decide_report(s, ev)["decision"]]}}
    rep = decide_report(stats, ev, census)
    dec, sc = rep["decision"], stats["cells"]
    tabs = _npz(_payload(store, "C", X["log_tables"]["path"], X["log_tables"]["file_sha256"], "B4"))
    b34 = {f"{m}|{F}|{v}": {"B3": zs.decompose(t), "B4": zs.zc_profile(t, tabs, _arm(m))}
           for m in names for F in FAM for v in VO
           for t in [_terms(*outs[m][F][v], VA[F], v, cache)]}
    pt = stats["point"]
    report = {
        "schema": "x6zc-report-v1", "protocol_id": zc.PROTOCOL_ID, "head": _head(),
        "protocol_sha256": zc.PROTOCOL_SHA256, "x6zc_master": zc.X6ZC_MASTER,
        "outcome": dec["headline"], "global_rule": dec["global_rule"], "cells": {c: {
            "model": zc.CELLS[c]["model"], "family": zc.CELLS[c]["family"],
            **{k: dec["cells"][c][k] for k in ("rule", "outcome", "descriptive")},
            "licence": rep["licences"][c], "not_licensed": rep["not_licensed"][c],
            "qualifiers": rep["qualifiers"][c], "b": (sc[c] or {}).get("b"),
            "b_interval": [(sc[c] or {}).get("b_lo"), (sc[c] or {}).get("b_hi")],
            "beta_pp": (sc[c] or {}).get("beta_pp"), "r": (sc[c] or {}).get("r"),
            "undefined_frac": (sc[c] or {}).get("undefined_frac"),
            "beta_sb": (sc[c] or {}).get("beta_sb"), "n": n} for c in CO},
        "r_w1_p": (sc["P"] or {}).get("r_w1_p"), "k6": stats["k6"], "f1": ev["f1"],
        "k0": {"status": ev["k0"]}, "coupling": av["coupling"],
        "reuse_verdict": rep["reuse_verdict"],
        "stage_b": {"k4": B["gates"]["K4"]["status"], "k5": B["gates"]["K5"]["status"],
                    "descriptive_tier": B["values"]["tier"], "b9": ev["b9"],
                    "qualifiers": B["values"]["census"]},
        "x6s1_statement": C["x6s1_statement"], "sensitivity": census["sensitivity"],
        "descriptive": {"point": pt, "rho": stats["rho"], "beta_y": stats["beta_y"], "b3_b4": b34,
                        "r": {k[0] + "|" + k[1]: {v: pt[(k[0], k[1], v)] / pt[k] if pt[k] else None
                                                   for v in VO[1:]} for k in pt if k[2] == "PP"},
                        "na_models_w1_r": {m: {v: pt[(m, "W1", v)] / pt[(m, "W1", "PP")] if pt[
                            (m, "W1", "PP")] else None for v in VO[1:]} for m in zc.NA_MODELS}},
        "exposure": {"a4_matches": A["gates"]["A4"]["total"], "d_coincident": av["n_d_coincident"]},
        "follow_up": C["follow_up"].get(zc.NA_DIR) if any(
            dec["cells"][c]["outcome"] == zc.NA_DIR for c in CO) else None,
        "budget": {"cpu_s": {s: _record(store, s)[1]["cpu_s"] for s in ("A", "B")},
                   "pauses": [x for x in _lines(Path(store) / "STAGES.jsonl") if x.get("stop")]},
        "n": n, "n_avail": av["n_avail"], "r_star": av["r_star"], "env": ctx["env"],
        "stages": {x["stage"]: x["record_sha256"] for x in _lines(Path(store) / "STAGES.jsonl")}}
    V.update(errors=validate_report(report), report_sha256=xwrite(Path(store) / "report.json",
                                                                  _cj(report)))
    return _finish(store, ctx, "REPORT_SCHEMA" if V["errors"] else None, n)

# ---- CLI (API §11.5) ----
def _frozen(store) -> dict:
    fz, au = (Path(store) / n for n in ("FREEZE.json", "AUTH.json"))
    if not (fz.exists() and au.exists()):
        raise RuntimeError("FREEZE.json and AUTH.json are required before stages A-C")
    f = json.loads(fz.read_text("utf-8"))
    if str(f.get("protocol_sha256", "")).lower() != _sha(zc.PROTOCOL_FILE.read_bytes()):
        raise RuntimeError("protocol sha256 differs from FREEZE.json")
    return f
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="x6zc_run.py")
    ap.add_argument("command", choices=("dry", "A", "B", "C", "report", "chunk", "ruling",
                                        "master-check", "bind-template"))
    for a in ("--store", "--job", "--dispatch", "--stage", "--model", "--out", "--id", "--check",
              "--cause", "--defect-md", "--session", "--cause-identified", "--affects-beta"):
        ap.add_argument(a)
    ap.add_argument("--setup", action="store_true")
    a = ap.parse_args(argv)
    st = a.store or (zc.DRY_STORE if a.command == "dry" else zc.STORE)
    try:
        if a.command == "dry":
            cpu0, rep = time.process_time(), dry(st)
            if (Path(zc.STORE) / "cpu_ledger.json").exists():  # the stage-0 record (API §11.4)
                write_stage(zc.STORE, "0", {"stage": "0", "head": _head(), "utc": _utc(),
                                            "dry_report_sha256": rep["sha256"], "stop": None,
                                            "all_pass": rep["all_pass"], "scratch": st,
                                            "cpu_s": time.process_time() - cpu0,
                                            "cpu_cumulative_s": ledger_cpu(zc.STORE)})
            print(json.dumps(_js(rep), indent=1))
            return 0 if rep["all_pass"] else 2
        if a.command == "master-check":
            r = master_fresh()
            print(json.dumps(r))
            return 0 if r["fresh"] else 2
        if a.command == "bind-template":
            print(bind_template(a.out, a.session, st))
            return 0
        if a.command == "ruling":
            print(write_ruling(st, a.id, a.check, a.stage, a.cause_identified == "1",
                               a.affects_beta == "1", a.cause, a.defect_md, a.setup))
            return 0
        if a.command == "report":
            errs = validate_report(json.loads((Path(st) / "report.json").read_text("utf-8")))
            print(json.dumps(errs))
            return 2 if errs else 0
        if a.command == "chunk":
            return chunk(a.stage, a.model, a.out, st)
        return {"A": stage_a, "B": stage_b, "C": stage_c}[a.command](st)
    except (RuntimeError, ValueError, OSError) as e:
        print(f"x6zc_run: {e!r}", file=sys.stderr)
        return 1
if __name__ == "__main__":
    sys.exit(main())
