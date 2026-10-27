"""X6ZC stage A and the model chunk children: the A1 records audit, the A2 code audit, stage A
(A-audit, A3, K0, the q* cache, K1-K3/F1, A4) and the Stage-B/C chunk child (X6ZC-DESIGN-v1 §6;
API.md §11.4, §20 C-52, C-54). Stage begin/finish live in x6zc_guard. Runs only after FREEZE
and AUTH."""
# fmt: off

from __future__ import annotations

import io
import json
import math
import re
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

# isort: off
from x6zc_pipeline import (predict_variants)  # noqa: E402
# isort: on
# isort: off
from x6zc_store import (_utc, _sha, _cj, xwrite, _append, _lines, log_exposure)  # noqa: E402
# isort: on
# isort: off
from x6zc_guard import (_dirs, _record, _begin, _finish, run_guarded)  # noqa: E402, F401
# isort: on

C, X = zc.CONTRACT, zc.CONTRACT["x6s1_store"]
FAM, VO, CO = zc.FAMILIES, zc.VARIANT_ORDER, zc.CELL_ORDER
# ---- stages A, B, C (§6-§8; API §11.4): only after FREEZE.json and AUTH.json ----
RUN = str(zc.HERE / "x6zc_run.py")  # the CLI script of the chunk children
def _x6(rel) -> Path: return Path(zc.X6S1_STORE) / rel
def _payload(store, stage, rel, sha, purpose) -> bytes:
    log_exposure(store, stage, rel, sha, purpose)  # written before the payload is opened
    data = _x6(rel).read_bytes()
    if sha and _sha(data) != str(sha).lower():
        raise ValueError(f"{rel}: sha256 differs from the CONTRACT binding")
    return data
def _checked(r) -> bytes:  # a payload re-read by a chunk child, sha-checked (F-15)
    data = _x6(r["path"]).read_bytes()
    if _sha(data) != str(r["file_sha256"]).lower():
        raise ValueError(f"{r['path']}: sha256 differs from the CONTRACT binding")
    return data
def _npz(data) -> dict:
    z = np.load(io.BytesIO(data), allow_pickle=False)
    return {k: z[k] for k in z.files}
def _x6json(rel) -> tuple:  # (object, sha256) of a stage-1 JSON record (never a payload)
    b = _x6(rel).read_bytes()
    return json.loads(b), _sha(b)
def _latest(lines, gate) -> dict:
    return next((r for r in reversed(lines) if r.get("gate") == gate), {})
def _prov(m, rep, gl, pools, echo) -> dict:  # A1 item 3 of one focal model (F-3)
    R, ad, s = X["records"], X["admitted"][m], int(m.split("-s")[1])
    wave = ad["bundle_id"].split("-")[0]  # C1 or C2
    d, tp, el = f"cloud/{wave}/{m}", X["train_pools_A4"][f"train_ZC_s{s}"], (
        "stages/E1/loss_echo.json" if wave == "C1" else "stages/E2/loss_echo.json")
    lock, (man, msh) = _x6json(ad["lock"])[0], _x6json(f"{d}/MANIFEST.json")
    smf = _x6json(f"{d}/STORE_MANIFEST.json")[0]
    ing = _latest(gl, f"INGEST-{wave}").get("values", {}).get("models", {}).get(m, {})
    gst = {g.get("gate"): g.get("status") for g in ing.get("gates", []) if g.get("model") == m}
    e = next((y for y in man.get("models", []) if y.get("model") == m), {})
    (le, lsh), ch = echo[el], e.get("chain") or [{}]
    x, pe = (le.get(m) or {}).get("max_abs_32"), pools[0].get(f"train_ZC_s{s}") or {}
    chk = {
        "lock": all(lock.get(k) == ad[k] for k in ("final_file_sha256", "final_weights_sha256",
                                                    "bundle_id")),
        "gates": ing.get("status") == "DONE" and ing.get("admitted") is True and all(
            gst.get(g) == "PASS" for g in X["gates_required_pass"]),  # absent gate = FAIL
        "loss_echo": lsh == R[el]["sha256"] and isinstance(x, (int, float))
        and math.isfinite(x) and float(x) <= float(X["loss_echo_max_abs_32"]),  # no vacuous pass
        "learn_test": (rep.get("learn_test") or {}).get(m) == "PASS",  # E3z report learn_test
        "manifest": msh == smf.get("MANIFEST.json") and e.get("final_file_sha256") == ad[
            "final_file_sha256"] and [r.get("record_sha256") for r in ch] == lock.get(
            "chain_record_sha256"),
        "data": e.get("data_stream") == ["x6s1", "train", "ZC", s] and e.get("data_sha256") == tp[
            "file_sha256"] and pools[1] == R["pools/POOLS.json"]["sha256"] and all(
            pe.get(k) == tp[k] for k in ("file_sha256", "token_sha256")),
        "ckpt_path": f"{d}/{ch[-1].get('file')}" == ad["ckpt"]}  # A1 item 4
    return {"checks": chk, "max_abs_32": x, "devices": e.get("devices"), "gates": gst,
            "sessions": sorted({str(r.get("session_id")) for r in ch})}
def a1_provenance(rep) -> dict:  # an unreadable or malformed record fails the model's checks
    gl, pools = _lines(_x6("GATES.jsonl")), _x6json("pools/POOLS.json")
    echo, out = {f"stages/{s}/loss_echo.json": _x6json(f"stages/{s}/loss_echo.json")
                 for s in ("E1", "E2")}, {}
    for m in zc.FOCAL:
        try:
            out[m] = _prov(m, rep, gl, pools, echo)
        except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
            out[m] = {"checks": {"readable": False, "ckpt_path": False}, "error": repr(exc)}
    return out
def a1_check(store, closure) -> dict:
    import x6s1_decide as sdc
    SD, it, dj, rows = X["stored_designed"], {}, {}, {}
    rep, rsh = _x6json("stages/E3z/report.json")
    for m, r in SD.items():  # all 16 stored designed results (F-15)
        (ch, csh), (dj[m], dsh) = (_x6json(f"{r['dir']}/{f}.json") for f in ("chunk", "designed"))
        rd = (rep.get("designed") or {}).get(m) or {}
        pd = ((rep.get("placebo") or {}).get("designed") or {}).get(m)
        rows[m] = {"chunk": csh == r["chunk_sha256"], "contract": dj[m] == r["values"],
                   "file": dsh == r["designed_json_sha256"] == (ch.get("files") or {}).get(
                       "designed.json"),
                   "report_designed": bool(rd) and all(dj[m].get(k) == v for k, v in rd.items()),
                   "placebo_designed": pd is None and m not in zc.FOCAL or bool(pd) and all(
                       dj[m].get(k) == v for k, v in pd.items())}
    it["1"] = rsh == X["records"]["stages/E3z/report.json"]["sha256"] and all(
        all(rows[m].values()) for m in zc.FOCAL)
    lo = Fraction(X["dw2_lo"])
    o = [sdc.ord_d(*(dj[f"{a}-s{s}"] for a in ("NA", "init", "AB", "ZC")), lo)
         for s in (1, 2, 3, 4)]
    it["2"] = (o[0]["status"], o[0]["control_limited"], o[0]["reason"]) == (
        "UNRESOLVED", True, "designed placebo ZC") and all(x["status"] == "FAIL" for x in o[1:])
    it["2"] &= all(all(r.values()) for r in rows.values())  # the ord_d inputs, re-verified
    prov = a1_provenance(rep)
    it["3"] = all(all(v for k, v in p["checks"].items() if k != "ckpt_path") for p in prov.values())
    it["4"], w = all(p["checks"]["ckpt_path"] for p in prov.values()), {}
    for m in zc.FOCAL:  # F-10: file and weights sha at A1 (logged payload reads), not in Stage B
        log_exposure(store, "A", _spec(m)[0], _spec(m)[1], f"A1 item 4 {m}")
        try:
            _predictor(m)
            w[m] = "PASS"
        except (ValueError, OSError) as exc:
            w[m] = f"FAIL: {exc}"
    it["4"] &= all(v == "PASS" for v in w.values())
    kinds = {e.get("kind") for e in _lines(_x6("EVALUATIONS.jsonl"))}
    sites = sorted([f"tools/x6_stage1/{p.name}", i] for p in (zc.REPO / "tools/x6_stage1").glob(
        "*.py") for i, ln in enumerate(p.read_text("utf-8").splitlines(), 1) if '"prefix"' in ln)
    it["5"] = kinds <= set(X["evaluation_kinds_seen"]) and sites == sorted(X["a1_prefix_sites"])
    it["6"] = not closure
    return {"status": "PASS" if all(it.values()) else "FAIL", "items": it, "designed": rows,
            "provenance": prov, "weights": w, "ord_d": o,
            "evaluation_kinds": sorted(map(str, kinds))}
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
def stage_a(store=zc.STORE, dispatch=None, job=None) -> int:
    return run_guarded(store, "A", _stage_a, dispatch, job)
def _stage_a(store, ctx) -> int:
    import x6s1_stage_pre as pre
    G, V, d = ctx["gates"], ctx["values"], Path(store) / "stages" / ctx["dir"]
    if not (Path(store) / "EXPOSURE.jsonl").exists():
        _append(Path(store) / "EXPOSURE.jsonl", {**C["store"]["exposure_first"], "utc": _utc()})
    G["A1"], G["A2"] = a1_check(store, ctx["closure"]), a2_check()
    D = _npz(_payload(store, "A", X["designed"]["path"], X["designed"]["file_sha256"], "A-audit"))
    au = {F: zs.audit_pairs(D, F) for F in sp.PAIR_FAMILIES}
    dsh = sp.designed_sha256(D) == X["designed"]["designed_sha256"]
    G["A_audit"] = {"status": "PASS" if dsh and all(r["status"] == "PASS" for r in au.values())
                    else "DEFECT_CANDIDATE", "families": au, "designed_sha256_equal": dsh}  # F-9
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
    a3 = {"first_1024_equal": fr["first_1024_equal"], "d_equal": fr["d_equal"],
          "d_rebuilt_equal": sp.designed_sha256(sp.designed_arrays(Ds)) == X["designed"][
              "designed_sha256"]}
    G["A3"] = {"status": "PASS" if all(a3.values()) else "DEFECT_CANDIDATE", **a3}  # F-9
    V.update(fresh=fresh, n_avail=fr["n_avail"], r_star=fr["r_star"],
             d_coincident=fr["d_coincident"], n_d_coincident=fr["n_d_coincident"],
             not_enough_data=fr["not_enough_data"], coupling=zc.coupling_table(), **a3)
    if G["K0"]["status"] == "FAIL":
        return _finish(store, ctx, "STOP_REPLAN")  # G-R0 before any model
    cache = zc.QStarCache.build([D, *VA.values()])
    V["qstar_sha256"] = cache.save(d / "qstar_NA.npz")
    k1p = [zc.oracle("ZC", "qstar"), zc.oracle("AB", "qstar"), zc.SyntheticPredictor(
        "set_constant"), zc.SyntheticPredictor("matched_key"), zc.oracle("NA", "q_8")] + [
        zc.oracle("NA", k) for k in ("q_empty", "q_parity", "q_counts", "q_H1", "q_Parikh")]
    k1 = {f"{getattr(p, 'arm', 'synthetic')}:{p.name}|{F}|{src}|{key}": zc.k1_check(  # F-11
        zc.pair_arrays(p, A, key, cache))["status"]
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
def _children(store, stage, names, out_dir, ctx) -> dict:
    """<= MAX_CHILDREN chunk children per batch under sr.supervise, which classifies the mailbox
    controls at every poll with the dispatch identities bound by _begin (F-1). Each finished
    child's CPU (its own process_time in chunk.json, or the supervisor's reading if larger) is
    added to the stage CPU (R-0134-3)."""
    import x6s1_data as sd
    import x6s1_run as sr
    if not (sr._CTX.get("job") and sr._CTX.get("task")) or str(sr._CTX["job"]) == "None":
        raise RuntimeError("no dispatch identities bound for the supervisor (F-1)")
    lim, res, todo = sr.limits(), {}, list(names)
    (Path(store) / "logs").mkdir(parents=True, exist_ok=True)
    while todo:
        batch, todo = todo[:sd.MAX_CHILDREN], todo[sd.MAX_CHILDREN:]
        kids = {m: sr.launch([sys.executable, "-s", RUN, "chunk", "--stage", stage,
                              "--model", m, "--store", store, "--out", str(out_dir / m)],
                             Path(store) / "logs" / f"{stage}_{m}_{int(time.time())}.log")
                for m in batch}
        for m, r in sr.supervise(kids, lim, "E3").items():
            cj = out_dir / m / "chunk.json"
            own = json.loads(cj.read_text("utf-8"))["cpu_s"] if cj.exists() else None
            res[m] = {**r, "chunk_cpu_s": own}
            ctx["kids_cpu"] += max(float(r.get("cpu_s") or 0.0), float(own or 0.0))
    return res
def chunk(stage, model, out, store=zc.STORE) -> int:
    import os

    import d2a_train
    import torch
    se.set_threads()  # the design's 2 intra-op / 1 inter-op threads, recorded (R-0134-4)
    thr = {"threads": {"intra": torch.get_num_threads(),
                       "interop": torch.get_num_interop_threads()},
           "thread_env": {v: os.environ.get(v) for v in d2a_train.THREAD_VARS}}
    cpu0, o, pred = time.process_time(), Path(out), _predictor(model)
    dA, A = _record(store, "A")
    cache = _cache(store)
    if stage == "B":
        D, tabs = (_npz(_checked(X[k])) for k in ("designed", "log_tables"))  # parent-logged
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
    xwrite(o / "chunk.json", _cj({"model": model, "stage": stage, "files": files, **thr,
                                  "cpu_s": time.process_time() - cpu0, "utc": _utc()}))
    return 0
