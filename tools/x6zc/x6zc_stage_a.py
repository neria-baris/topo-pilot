"""X6ZC stage A and the model chunk children: shared stage begin/finish, the A1 records audit,
the A2 code audit, stage A (A-audit, A3, K0, the q* cache, K1-K3/F1, A4) and the Stage-B/C
chunk child (X6ZC-DESIGN-v1 §6; API.md §11.4, §20 C-52). Runs only after FREEZE and AUTH."""
# fmt: off

from __future__ import annotations

import io
import json
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
from x6zc_store import (_utc, _sha, _cj, xwrite, _append, _lines, log_exposure,  # noqa: E402
    write_stage, x6s1_inventory, inventory_equal, env_check, closure_diff,  # noqa: E402
    meter_bind_check, ledger_cpu, pause_check, _head, _frozen)  # noqa: E402
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
def _npz(data) -> dict:
    z = np.load(io.BytesIO(data), allow_pickle=False)
    return {k: z[k] for k in z.files}
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
        kids = {m: sr.launch([sys.executable, "-s", RUN, "chunk", "--stage", stage,
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
