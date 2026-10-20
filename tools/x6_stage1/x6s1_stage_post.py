"""X6S1 stage content of E1, E2, E3a/E3w and E3z (ruling R-0079-1): INGEST, LEARN, LC, LOSS-ECHO,
E3.0, DET, the wave schedule, `chunk_plan`, E3.2-E3.9, §2.8, the report and unsealing (protocol §8
rows 14-30; API.md §13 items 27-31); gates fn(ctx) -> {"status", "values"}; no I/O at import."""
# fmt: off

from __future__ import annotations

import io
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import x6s1_data as sd  # first: its import applies the API §1 sys.path convention

# isort: split
import numpy as np
import torch
import x6_model as xm
import x6s1_cloud as sc
import x6s1_decide as sdc
import x6s1_eval as se
import x6s1_ingest as si
import x6s1_pairs as sp
import x6s1_run as sr
import x6s1_stage_pre as pre
import x6s1_stats as ss

NA, SEEDS, TERMINAL = tuple(f"NA-s{s}" for s in sd.SEEDS), sd.SEEDS, ("DONE", "INVALID:NONFINITE")
BINS = ((8, 15), (16, 23), (24, 31))  # β_ord by age bin at t = 32 (§2.8)
NOT_COMPUTED = {"status": "NOT_COMPUTED", "reason": "not in the eval_chunk outputs (D-0082-2)"}
REFS, VALIDITY = ("h_rev", "h_last", "h_first"), ("S0", "PF", "SMOKE-INGEST", "G0-ORC", "SCORE",
                                                  "G0-POS", "G0-FEAS")


def _clean(v):  # canonical JSON refuses NaN and inf: a non-finite float is recorded as None
    if isinstance(v, dict):
        return {k: _clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_clean(x) for x in v]
    return (float(v) if math.isfinite(v) else None) if isinstance(v, (float, np.floating)) else v
def _r(ok, values=None, bad="FAIL") -> dict:
    return {"status": "PASS" if ok else bad, "values": _clean(values)}
def _gates(store) -> dict:  # gate → its GATES.jsonl records, in order
    out, p = {}, Path(store) / "GATES.jsonl"
    for ln in p.read_text("utf-8").splitlines() if p.is_file() else []:
        out.setdefault((r := json.loads(ln))["gate"], []).append(r)
    return out
def _last(store, gate): return (_gates(store).get(gate) or [{}])[-1]
def _vals(store, gate) -> dict: return _last(store, gate).get("values") or {}
def _e0(store) -> dict: return sr._load(Path(store) / "stages" / "E0" / "record.json")["values"]
def _bytes(path, sha) -> bytes:  # a stored file, re-verified against its recorded sha256
    if sc.sha256_bytes(data := Path(path).read_bytes()) != sha:
        raise ValueError(f"{path}: sha256 differs from its record")
    return data
def _npz(path, sha) -> dict:
    with np.load(io.BytesIO(_bytes(path, sha))) as z:
        return {k: z[k] for k in z.files}
def _tables(store, e0) -> dict:
    return _npz(Path(store) / "tables/log_tables.npz", e0["SCORE"]["tables"]["file_sha256"])
def _partners(store, e0) -> dict:
    return _npz(Path(store) / "stages/E0/partners_test_NA_t32.npz",
                e0["G0-FEAS"]["partners_sha256"])
def _tok(store, name) -> np.ndarray: return pre.load_obs(store, name).tokens
def _status(store) -> dict:  # model → its status in the last INGEST-C1 and INGEST-C2 records
    return {m: v["status"] for g in ("INGEST-C1", "INGEST-C2")
            for m, v in _vals(store, g).get("models", {}).items()}
def _pred(store, m) -> se.ModelPredictor:  # the admitted final weights, verified at load
    if (v := si.verify_admitted(store, m))["status"] != "PASS":
        raise ValueError(f"{m}: {v['detail']}")
    se.set_threads()
    return se.ModelPredictor(v["path"], v["file_sha256"], v["weights_sha256"])
def _dir(ctx) -> Path:
    d = Path(ctx["store"]) / "stages" / ctx.get("stage_dir", ctx["stage"])
    return d.mkdir(parents=True, exist_ok=True) or d
def _wjson(path, obj) -> str: return si._xwrite(Path(path), sr._cj(_clean(obj)))
def _mean(x) -> float: return math.fsum(x) / len(x) if len(x) else math.nan
def _lt(x, bound) -> bool: return sdc._fin(x) and Fraction(float(x)) < bound
def _waves(ctx) -> list: return [int(k) for k in ctx["dispatch"].get("waves", [1])]
def _iv(r) -> dict:
    lo, hi = ss.quantile(r, ss.LB_975), ss.quantile(r, ss.UB_975)
    return {"lb": lo, "ub": hi, "hw95": (hi - lo) / 2}

# ---- S0 and the stage directory (§13 items 29, 31) ----
def s0(ctx) -> dict:  # S0 first; the stage directory (§13 item 31)
    st, ctx["t0"] = ctx["stage"], time.perf_counter()
    if st == "E3w":
        ctx["stage_dir"] = f"E3w{_waves(ctx)[0]}"
    elif (Path(ctx["store"]) / "stages" / st / "record.json").exists():
        ctx["stage_dir"] = f"{st}-{ctx['dispatch']['job']}"
    return pre.s0(ctx)

# ---- E1/E2: INGEST, LEARN, LC with LOSS-ECHO (§4.5, §4.7, §5.7-§5.8; §8 rows 14-19) ----
def _envs(snap, store, m) -> int:  # distinct (Python, numpy, torch, CUDA, cuDNN) of m's sessions
    ids = {r["session_id"] for r in si._store_chain(store, m)[1]["chain"]}
    recs = [json.loads(p.read_bytes()) for p in (Path(snap) / "sessions").glob("*.start.json")]
    return len({tuple(r.get(k) for k in ("python", "numpy", "torch", "cuda", "cudnn"))
                for r in recs if r.get("session_id") in ids})
def _ingest(ctx, wave) -> dict:  # si.ingest; FAIL_TECHNICAL/* before HOLD (§5.8)
    store, d, fz = Path(ctx["store"]), ctx["dispatch"], pre.frozen(ctx["store"], wave)
    res = si.ingest(Path(d["snapshot"]), d["manifest_sha256"], wave, store, pre.local_digests(fz),
                    fz, redownload_ok=int(d.get("downloads", 1)) < 3)
    st = [r["status"] for r in res.values()]
    bad = [s for s in st if s.startswith("FAIL_T")] + ["HOLD" for s in st if s not in TERMINAL]
    env = {m: _envs(d["snapshot"], store, m) for m, r in res.items() if r["status"] == "DONE"}
    return _r(not bad, {"models": res, "env_versions": env}, bad[0] if bad else None)
def ingest_c2(ctx) -> dict:
    if _last(ctx["store"], "LEARN").get("status") != "PASS":
        return _r(False, {"error": "LEARN did not GO: C2 is never ingested (§4.7, S4)"}, "INVALID")
    return _ingest(ctx, "C2")
def learn(ctx) -> dict:
    """§4.7 on val: UB_0.975 of the B_GATE bootstrap of x̂ < G_8.lo; releases statuses only."""
    store, st, out = ctx["store"], _status(ctx["store"]), {}
    tab = _tables(store, _e0(store))
    for m in sd.WAVES["C1"]:  # ZC-s1 on val(ZC): computed, sealed, never gating
        arm = sd.parse_model(m)[0]
        if st.get(m) == "INVALID:NONFINITE":  # a defined FAIL (D-2a convention)
            out[m] = {"status": sdc.learned_val(None, sd.g8_lo(), nonfinite=True)}
            continue
        sr.log_evaluation(store, m, "val", ctx["stage"])
        try:
            x = se.own_arm(_pred(store, m), arm, _tok(store, f"val_{arm}"), tab)["xhat"]
        except se.QuantInvalid as exc:
            out[m] = {"status": "UNRESOLVED", "error": str(exc)}
            continue
        ub = ss.quantile(ss.boot_means(x, sd.B_GATE, ss.boot_stream("learn", m)), ss.UB_975)
        out[m] = {"mean": _mean(x), "ub": ub, "status": sdc.learned_val(ub, sd.g8_lo())}
    dec = sdc.learn_decision(out["NA-s1"]["status"], out["NA-s2"]["status"])
    sha = {"learn.json": sr.seal(store, "learn.json", _clean({**{m: out[m] for m in NA[:2]},
                                                              "decision": dec})),
           "zc_s1.json": sr.seal(store, "zc_s1.json", _clean(out["ZC-s1"]))}
    v = {**{m: out[m]["status"] for m in NA[:2]}, "decision": dec, "sealed": sha}
    return {"status": {"GO": "PASS", "NOT_LEARNED": "FAIL"}.get(dec, "UNRESOLVED"), "values": v}
def _lc(ctx, wave, part) -> dict:  # LOSS-ECHO and a sealed learning-curve part
    store, st = ctx["store"], _status(ctx["store"])
    ms = [m for m in sd.WAVES[wave] if st.get(m) == "DONE"]
    for m in ms:
        for kind in ("loss_echo", "dev_curve"):
            sr.log_evaluation(store, m, kind, ctx["stage"])
    echo = {m: si.loss_echo(store, wave, m, _tok(store, "train_" + m.replace("-", "_")))
            for m in ms}
    curve = si.learning_curve(store, ms, {m: _tok(store, "dev_" + m.replace("-", "_")) for m in ms})
    p = _dir(ctx) / "loss_echo.json"
    return _r(True, {"sealed": {part: sr.seal(store, part, curve)}, "loss_echo": {
        "path": p.relative_to(store).as_posix(), "sha256": _wjson(p, echo)}})

# ---- E3a/E3w: E3.0, E3.1, the wave schedule, chunk_plan and E3.A (§8 rows 20-22; §13.3) ----
def schedule(store) -> list:  # E3.A waves: INITS, MODELS; ≤ MAX_CHILDREN each
    names = [n for n in sd.INITS + sd.MODELS if _status(store).get(n) != "INVALID:NONFINITE"]
    return [tuple(names[i:i + sd.MAX_CHILDREN]) for i in range(0, len(names), sd.MAX_CHILDREN)]
def _regen(ctx) -> dict:  # §12 item 6 after an environment change
    store = Path(ctx["store"])
    ch = sr.env_changed(sr._load(store / "stages/E3a/record.json")["env_local"], sr.env_local())
    if not ch:
        return {"status": "PASS", "changed": []}
    n, w = schedule(store)[0][0], f"E3r{_waves(ctx)[0]}"
    for kind in ("test", "designed"):
        sr.log_evaluation(store, n, kind, ctx["stage"])
    sr.eval_wave(store, w, [n])
    old, new = (sr._load(store / "stages" / x / n / "chunk.json")["files"] for x in ("E3w1", w))
    return {"status": "PASS" if old == new else "FAIL", "changed": ch, "regenerated": n}
def bind(ctx) -> dict:  # E3.0: model locks, pool and table hashes
    store, e0, st = Path(ctx["store"]), _e0(ctx["store"]), _status(ctx["store"])
    models = {m: si.verify_admitted(store, m)["status"] if st.get(m) == "DONE" else st.get(m)
              for m in sd.MODELS}
    idx, g = pre.pools_index(store), e0["G0-ORC"]
    tabs = {"class_tables_NA.json": g["c"]["tables_sha256"], "designed.npz": g["designed"][
        "file_sha256"], "log_tables.npz": e0["SCORE"]["tables"]["file_sha256"]}
    for n in idx:  # the token digest of every pool (a mismatch raises: INVALID)
        pre.load_obs(store, n)
    v = {"models": models, "pools": len(idx) == 35 and all(sc.sha256_file(store / r["npy"]) == r[
        "file_sha256"] for r in idx.values() if "npy" in r), "POOLS.json": sc.sha256_file(
        store / "pools/POOLS.json") == e0["REG"]["POOLS.json"], "tables": all(
        sc.sha256_file(store / "tables" / f) == h for f, h in tabs.items())}
    ok = all(s in ("PASS", "INVALID:NONFINITE") for s in models.values()) and pre._ok(v)
    if ok and ctx["stage"] == "E3w":
        ok = (v.update(env=_regen(ctx)) or v["env"])["status"] == "PASS"
    return _r(ok, v, "INVALID")
def det(ctx) -> dict:  # E3.1 (T8): two loads, N_DET test(NA) rows
    store = ctx["store"]
    m = next(m for m in sd.MODELS if _status(store).get(m) == "DONE")
    sr.log_evaluation(store, m, "test", ctx["stage"])
    tok = _tok(store, "test_NA")[:sd.N_DET]
    a, b = (_pred(store, m)(tok, 32) for _ in range(2))
    d, same = float(np.max(np.abs(a - b))), bool(np.array_equal(se.quantise(a), se.quantise(b)))
    return _r(d <= sd.DET_TOL and same, {"model": m, "max_abs": d, "counts_equal": same})
def _spec(store, name, e0) -> dict:  # eval_chunk's predictor spec, verified
    arm, s = sd.parse_model(name)
    if arm != "init":
        if (v := si.verify_admitted(store, name))["status"] != "PASS":
            raise ValueError(f"{name}: {v['detail']}")
        return {k: v[k] for k in ("file_sha256", "weights_sha256")} | {"ckpt_path": v["path"]}
    st = torch.load(Path(store) / "stages/E0/init" / f"init_s{s}.pt", map_location="cpu",
                    weights_only=True)["model"]
    if sc.weights_digest(st) != e0["CLOUD-PREP"]["inits"][f"NA-s{s}"]["weights_sha256"]:
        raise ValueError(f"{name}: the init weights digest differs from CLOUD-PREP")
    return {"state": st}
def chunk_plan(store, name) -> dict:  # the E3.A inputs, re-verified (§13 item 31)
    store, e0 = Path(store), _e0(store)
    arm, test, P, g = sd.parse_model(name)[0], _tok(store, "test_NA"), _partners(store, e0), e0[
        "G0-ORC"]
    plan = {"predictor": _spec(store, name, e0), "arm": "NA" if arm == "init" else arm,
            "own_tokens": test[:0] if arm == "init" else _tok(store, f"test_{arm}"),
            "test_tokens": test, "partner_tokens": P["tokens"], "rows": P["rows"],
            "designed": _npz(store / "tables/designed.npz", g["designed"]["file_sha256"]),
            "tables": _tables(store, e0), "env_local": sr.env_local()}
    if arm == "NA":  # the profile partners (t = 16, 24; first N_PROFILE rows), emergence, val
        ct = sp.load_tables(store / "tables/class_tables_NA.json", g["c"]["tables_sha256"])
        d, e, _ = si._store_chain(store, name)
        by, prof = {r["step"]: r for r in e["chain"]}, {}
        for t in sd.PROFILE_T:
            q = sp.partners(ct, test[:sd.N_PROFILE], t, "test_NA")
            prof[t] = {"rows": q["rows"], "partner_tokens": q["tokens"], "n_rows": sd.N_PROFILE}
        plan.update(profile=prof, emergence_rows=sd.N_EMERGE, val_tokens=_tok(store, "val_NA"),
                    emergence={k: {"ckpt_path": d / by[k]["file"], "file_sha256": by[k][
                        "file_sha256"], "weights_sha256": by[k]["weights_sha256"]}
                        for k in sd.EMERGENCE_STEPS})
    return plan
def e3a(ctx) -> dict:  # E3.A: the dispatch's waves (default [1])
    store, sch, out = Path(ctx["store"]), schedule(ctx["store"]), {}
    for k in _waves(ctx):
        for n in sch[k - 1]:
            for kind in ("test", "designed") + (("emergence", "val") if n in NA else ()):
                sr.log_evaluation(store, n, kind, ctx["stage"])
        w = sr.eval_wave(store, f"E3w{k}", sch[k - 1])
        for n in sch[k - 1]:
            c, logs = store / "stages" / f"E3w{k}" / n / "chunk.json", sorted(
                (store / "logs").glob(f"eval_{n}_*.txt"))
            out[n] = {"wave": k, "status": w["children"][n]["status"], "quant": any(
                "QuantInvalid" in p.read_text("utf-8", "replace") for p in logs[-1:]),
                "chunk_sha256": sc.sha256_file(c) if c.is_file() else None}
    quant = any(v["quant"] for v in out.values())
    ok = all(v["status"] == "DONE" and v["chunk_sha256"] for v in out.values())
    return _r(ok, {"chunks": out, "QUANT": ("PASS", "FAIL")[quant]}, ("INVALID", "FAIL")[quant])

# ---- E3z: E3.2-E3.9 (§2.3-§2.8, §7; §8 rows 23-30) ----
def _chunk(store, name, rec):  # the verified chunk directory (chunk.json = E3.A record) or None
    if not rec or not rec.get("chunk_sha256"):
        return None
    d = Path(store) / "stages" / f"E3w{rec['wave']}" / name
    for f, h in json.loads(_bytes(d / "chunk.json", rec["chunk_sha256"]))["files"].items():
        _bytes(d / f, h)
    return d
def learn_test(ctx) -> dict:  # loads the chunks; E3.2 U_0.025 and U_0.00625
    store, recs, eb, lt = Path(ctx["store"]), {}, {}, {}
    for r in _gates(store).get("E3.A", []):
        recs.update((r.get("values") or {}).get("chunks") or {})
    dirs = ctx["dirs"] = {n: _chunk(store, n, recs.get(n)) for n in sd.PREDICTORS}
    for m in sd.MODELS:
        if dirs[m] is None:  # a missing or INVALID model fails every per-seed condition
            lt[m] = "FAIL"
            continue
        z = np.load(dirs[m] / "own.npz")
        x, n = z["xhat"], len(z["xhat"])
        xp, zp = ss.outward_inputs(x)
        eb[m] = {"U025": str(ss.eb_bound(xp, zp, n, sd.DELTA_LEARN)), "xbar": _mean(x), "U_sharp":
                 str(ss.eb_bound(xp, zp, n, sd.DELTA_SHARP)), "raw_kl": _mean(z["raw_kl"])}
        lt[m] = sdc.learned_test(eb[m]["U025"], sd.g8_lo())
    cl = ctx["controls_learned"] = {a: sum(lt[f"{a}-s{s}"] == "PASS" for s in SEEDS)
                                    for a in ("AB", "ZC")}
    ctx.update(eb=eb, learn_test=lt)
    p = [lt[m] for m in NA]
    st = "PASS" if p.count("PASS") >= 3 else "FAIL" if p.count("PASS") + p.count(
        "UNRESOLVED") < 3 else "UNRESOLVED"
    return {"status": st, "values": _clean({"learn_test": lt, "eb": eb, "controls_learned": cl})}
def readout(ctx) -> dict:  # E3.3 (§2.6); loads the natural pair arrays
    store = Path(ctx["store"])
    P = ctx["P"] = _partners(store, _e0(store))
    test = _tok(store, "test_NA")
    inf = ctx["inf"] = P["informative"]
    ctx["qh"] = [se.qstar("NA", h, 32)[0] for h in (test[P["rows"][inf]], P["tokens"][inf])]
    dq, nat, des, out, lim = ctx["qh"][0] - ctx["qh"][1], {}, {}, {}, []
    for n, d in ctx["dirs"].items():
        if d is None:
            out[n], lim = dict.fromkeys(("natural", "designed")), lim + [f"{n} missing"]
            continue
        z, des[n] = dict(np.load(d / "pairs.npz")), sr._load(d / "designed.json")
        if not np.array_equal(z["rows"], P["rows"]):
            raise ValueError(f"chunk {n}: pair rows differ from the E0 partners")
        cn, dp = se.cue_normalise(z["p_h"]) - se.cue_normalise(z["p_h2"]), z["p_h"] - z["p_h2"]
        nf = not (np.isfinite(z["p_h"]).all() and np.isfinite(z["p_h2"]).all())
        out[n] = {"natural": float(np.median(z["cue_mass_h"])),
                  "designed": des[n]["cue_mass_median"]}
        nat[n] = {"num": z["num"], "den": z["den"], "nonfinite": nf, "beta": se.beta_fsum(
            z["num"], z["den"]), "spur": _mean((cn * cn).sum(1)[~inf]) / _mean(z["den"][inf]),
                  "raw": math.fsum((dp[inf] * dq).sum(1)) / math.fsum((dq * dq).sum(1)),
                  "ok": not nf and sdc.cue_ok(out[n]["natural"])}
        lim += [f"{n} {k}" for k, ok in (("natural", nat[n]["ok"]), ("designed", sdc.cue_ok(
            out[n]["designed"]) and not des[n]["nonfinite"])) if not ok]
    ctx.update(nat=nat, des=des, readout=out, readout_limited=lim)
    return _r(not lim, {"medians": out, "READOUT_LIMITED": lim}, "UNRESOLVED")
def placebo(ctx) -> dict:  # E3.4: natural |β_ord(c)| ≤ 0.10 (§2.7)
    nat, des, ctl = ctx["nat"], ctx["des"], [c for c in sd.PREDICTORS if c not in NA]
    pn = ctx["placebo"] = sdc.placebo_natural({c: nat[c]["beta"] if c in nat else None
                                               for c in ctl})
    dv = {c: {k: des[c][k] for k in ("beta_W2", "rho_W2")} if c in des else None for c in ctl}
    return _r(pn["ok"], {"natural": pn, "designed": dv})
def xcheck(ctx) -> dict:  # E3.5 (T7): fsum β vs x6_exact.beta
    diff = {n: None if a["nonfinite"] else abs(a["beta"] - float(se.beta_exact(a["num"], a["den"])))
            for n, a in ctx["nat"].items()}
    ok = all(v <= sd.XCHECK_TOL for v in diff.values() if v is not None)
    ctx["xcheck"] = "PASS" if ok else "FAIL"
    return _r(ok, {"abs_diff": diff})
def _draws(ctx, names, B, gen) -> tuple:  # informative num and full-row bootstrap ratios (§7.5)
    inf, N = ctx["inf"], pre.pools_index(ctx["store"])["test_NA"]["n_rows"]
    num = np.stack([ctx["nat"][n]["num"][inf] for n in names])
    ns, ds = ss.cord_draws(num, ctx["P"]["den"][inf], N, B, gen)
    return num, ns / ds[:, None]
def _descriptive(ctx) -> dict:  # §2.8, from the chunk outputs (no model run)
    store, d, eb, nat, inf, P = (ctx[k] for k in ("store", "dirs", "eb", "nat", "inf", "P"))
    test, lp, pg = _tok(store, "test_NA"), {}, {}
    na, G = [m for m in NA if d[m] is not None], sd.CONST_MAP
    ages = np.array([sp.segment(test[r], 32)["n"] for r in P["rows"]])
    for m in na:
        z, a = np.load(d[m] / "profile.npz"), nat[m]
        lp[m] = {f"t{t}": {"beta": se.beta_fsum(z[f"num_t{t}"], z[f"den_t{t}"]), "delta_nat": _mean(
            z[f"xhat_t{t}"]), "G_Parikh_lo": G[f"G_Parikh_{t}"]["lo"]} for t in sd.PROFILE_T} | {
            f"age_{lo}_{hi}": se.beta_fsum(a["num"][k := (ages >= lo) & (ages <= hi)], a["den"][k])
            for lo, hi in BINS}
    h, h2 = test[P["rows"][inf]], P["tokens"][inf]
    keep = np.array([(g := sp.segment(r, 32)) is not None and g["n"] >= 1 and
                     g["v_t"] in xm.ANCHOR_NB for r in test])  # elsewhere q_Parikh = q*
    kl = np.zeros(len(test))
    kl[keep] = se.kl_rows(se.qstar("NA", test[keep], 32)[0],
                          se.OraclePredictor("NA", "q_Parikh")(test[keep], 32))
    hi = kl >= float(xm.THETA_ROW)  # the stage-0 M_32 rows
    for m in na:
        g = kl - np.load(d[m] / "own.npz")["xhat"]
        pg[m] = {"all": _mean(g), "M32_rows": _mean(g[hi]), "other_rows": _mean(g[~hi])}
    return {"ladder": {m: {S: sdc.learned_test(eb[m]["U025"], sd.ladder_lo(S)) == "PASS" for S in
                           xm.LADDER + ("blk",)} for m in NA if m in eb}, "length_profile": lp,
            "references": {k: se.beta_fsum(*se.pair_terms(o(h, 32), o(h2, 32), *ctx["qh"])) for
                           k, o in ((k, se.OraclePredictor("NA", k)) for k in REFS)},
            "spurious_ratio": {n: a["spur"] for n, a in nat.items()},
            "abelian_spread": NOT_COMPUTED, "paired_gain": pg | {"M32_row_share": _mean(hi)},
            "matched_excess": {m: eb[m]["xbar"] - eb[z]["xbar"] for m, z in zip(
                NA, sd.MODELS[8:]) if m in eb and z in eb} | {
                "G_Parikh_lo": G["G_Parikh_32"]["lo"]},
            "raw": {"beta_full": {n: a["raw"] for n, a in nat.items()}, "float32_vs_float64":
                    NOT_COMPUTED, "raw_kl": {m: e["raw_kl"] for m, e in eb.items()}},
            "emergence": {m: sr._load(d[m] / "emergence.json") for m in na},
            "gamma": {m: sr._load(d[m] / "gamma.json") for m in na}}
def stats(ctx) -> dict:  # E3.6: β_ord, intervals, ctrl, β̃, C_s, ordD, §2.8
    nat, des, e0 = ctx["nat"], ctx["des"], _e0(ctx["store"])
    b = ctx["beta"] = {n: a["beta"] for n, a in nat.items()}
    iv = ctx["iv"] = {n: _iv(_draws(ctx, [n], sd.B_MODEL, ss.boot_stream("beta", n))[1][:, 0])
                      for n in nat}
    ctl = ctx["ctrl"] = {s: sdc.ctrl(b.get(f"init-s{s}"), [b.get(f"AB-s{u}") for u in SEEDS],
                                     [b.get(f"ZC-s{u}") for u in SEEDS]) for s in SEEDS}
    adj = ctx["adj"] = {s: None if ctl[s] is None or not sdc._fin(b.get(f"NA-s{s}")) else
                        b[f"NA-s{s}"] - ctl[s] for s in SEEDS}
    cs = ctx["C_s"] = {}
    for s in SEEDS:
        names = [f"{a}-s{s}" for a in ("NA", "init", "AB", "ZC")]
        if all(n in nat for n in names):
            r = _draws(ctx, names, sd.B_MODEL, ss.boot_stream("cseed", f"s{s}"))[1]
            cs[s] = {"value": b[names[0]] - max(b[n] for n in names[1:]),
                     **_iv(r[:, 0] - r[:, 1:].max(1))}
    dw2, dw3 = (Fraction(e0["G0-ORC"]["lo"][k]) for k in ("Delta_W2", "Delta_W3"))
    od = ctx["ord_d"] = {s: sdc.ord_d(*(des.get(f"{a}-s{s}") for a in ("NA", "init", "AB", "ZC")),
                                      dw2) for s in SEEDS}
    ctx["w2_gap"], ctx["challenge"] = ({m: m in des and _lt(des[m][k], lo - sd.BAND) for m in NA}
                                       for k, lo in (("R_W2", dw2), ("Delta_W3", dw3)))
    ctx["desc"] = _descriptive(ctx)
    return _r(True, {"beta_ord": b, "intervals": iv, "ctrl": ctl, "adjusted": adj, "C_s": cs,
                     "ord_d": od, "rho_C": {m: des[m]["rho_C"] for m in NA if m in des},
                     "w2_gap_beaten": ctx["w2_gap"], "challenge_beaten": ctx["challenge"],
                     "descriptive": ctx["desc"]})
def prec(ctx) -> dict:  # E3.7 (§7.6): precision_ok(s)
    eb, iv = ctx["eb"], ctx["iv"]
    pk = ctx["precision_ok"] = {s: m in eb and m in iv and sdc.seed_flags(
        None, None, eb[m]["U025"], eb[m]["xbar"], iv[m]["hw95"], sd.g0_lo())["precision_ok"]
        for s, m in zip(SEEDS, NA)}
    return _r(all(pk.values()), {"precision_ok": pk})
def confirm(ctx) -> dict:  # E3.8: C-ORD with TAIL, SHARP/TARGET, flags
    nat, adj, eb, g0 = ctx["nat"], ctx["adj"], ctx["eb"], sd.g0_lo()
    mean = _mean([adj[s] for s in SEEDS]) if all(sdc._fin(adj[s]) for s in SEEDS) else None
    lb, tail, lba = None, {"status": "FAIL", "reason": "a C-ORD term is missing"}, {}
    if all(n in nat for n in sd.PREDICTORS):
        num, r = _draws(ctx, sd.PREDICTORS, sd.B_CORD, ss.boot_stream("cord"))
        a = r[:, :4] - np.maximum(r[:, 12:16], np.maximum(r[:, 4:8].mean(1, keepdims=True),
                                                          r[:, 8:12].mean(1, keepdims=True)))
        lb, lba = ss.quantile(a.mean(1), ss.LB_975), {s: ss.quantile(a[:, s - 1], ss.LB_975)
                                                      for s in SEEDS}
        tail = ss.tail(num, ctx["P"]["den"][ctx["inf"]], math.nan if mean is None else mean, lb,
                       a.mean(1))
    ok = all(n in nat and nat[n]["ok"] for n in sd.PREDICTORS) and mean is not None
    cord = ctx["cord"] = sdc.cord(mean, lb, adj, tail["status"], ok)
    ctx["sharp"] = {m: sdc.sharp_target((eb.get(m) or {}).get("U_sharp"), g0) for m in NA}
    ctx["flags"] = {s: sdc.seed_flags(adj[s], lba.get(s), *((eb.get(m) or {}).get(k) for k in (
        "U025", "xbar")), (ctx["iv"].get(m) or {}).get("hw95"), g0) for s, m in zip(SEEDS, NA)}
    ctx["natural"] = {"beta_ord": ctx["beta"], "ctrl": ctx["ctrl"], "adjusted": adj, "mean": mean,
                      "lb": lb, "lb_adjusted": lba, "tail": tail, "cord": cord, "C_s": ctx["C_s"]}
    return _r(cord != "UNRESOLVED", {**ctx["natural"], "sharp_target": ctx["sharp"],
                                     "flags": ctx["flags"]}, "UNRESOLVED")
def _released(store) -> dict:  # name → (sha256, unsealed record) of every sealed part (E3)
    v = [_vals(store, g).get("sealed", {}) for g in ("LEARN", "LC-1", "LC-2", "HEADROOM-D")]
    return {n: (h, sr.unseal(store, n, h)) for s in v for n, h in s.items()}
def _echo(store) -> dict:  # the LOSS-ECHO files of E1 and E2, re-verified
    es = [e for e in (_vals(store, g).get("loss_echo") for g in ("LC-1", "LC-2")) if e]
    return {k: v for e in es for k, v in json.loads(_bytes(Path(store) / e["path"], e[
        "sha256"])).items()}
def rules(ctx) -> dict:  # E3.9: §7.9, qualifiers, licence, report.json
    store, od, fl, nt = (ctx[k] for k in ("store", "ord_d", "flags", "natural"))
    G, st, lv = _gates(store), _status(store), _vals(store, "LEARN")
    last = {g: rs[-1]["status"] for g, rs in G.items()}
    val = {k.replace("-", "_"): last.get(k) for k in VALIDITY} | {"REGISTRY": last.get("REG"),
           "INCOMPLETE": "PASS" if all(st.get(m) in TERMINAL for m in sd.MODELS) else "FAIL"}
    quant = any((r.get("values") or {}).get("QUANT") == "FAIL" for r in G.get("E3.A", []))
    dl, tail = [f"s{s}" for s in SEEDS if od[s]["control_limited"]], nt["tail"]["status"] == "PASS"
    env = {m: k for g in ("INGEST-C1", "INGEST-C2") for m, k in _vals(store, g).get(
        "env_versions", {}).items()}
    lad = {m: [S for S in xm.LADDER if L[S]] for m, L in ctx["desc"]["ladder"].items()}
    ev = {"validity": val, "learn": lv.get("decision"), "learn_test": ctx["learn_test"],
          "pipeline": {"DET": last.get("E3.1"), "XCHECK": ctx["xcheck"], "QUANT": (
              "PASS", "FAIL")[quant]}, "cord": ctx["cord"],
          "placebo_natural_ok": ctx["placebo"]["ok"],
          "ord_d": {s: od[s]["status"] for s in SEEDS}, "lowN": {s: fl[s]["lowN"] for s in SEEDS},
          "precision_ok": ctx["precision_ok"], "checks_ok": ctx["placebo"]["ok"] and not dl and not
          ctx["readout_limited"] and ctx["xcheck"] == "PASS" and tail, "sharp_target": ctx["sharp"],
          "w2_gap_beaten": ctx["w2_gap"], "challenge_beaten": ctx["challenge"],
          "control_limited": {"natural": ctx["placebo"]["failed"], "designed": dl},
          "readout_limited": ctx["readout_limited"], "controls_learned": ctx["controls_learned"],
          "ladder": [f"{m}: {min(r, key=sd.ladder_lo)}" for m, r in lad.items() if r],
          "precision_limited": not (all(ctx["precision_ok"].values()) and tail),
          "length_profile": bool(ctx["desc"]["length_profile"]), "mixed_device": [
              m for m in sd.MODELS if st.get(m) == "DONE" and len(
                  si._store_chain(store, m)[1]["devices"]) > 1],
          "mixed_env": sorted(m for m, k in env.items() if k > 1)}
    cnt, rel = sdc.designed_counts([od[s]["status"] for s in SEEDS]), _released(store)
    lc = {k: v for n in ("learning_curve.json", "learning_curve_C2.json")
          for k, v in rel.get(n, (0, {}))[1].items()}
    desc = ctx["desc"] | {"headroom": rel.get("headroom.json", (0, None))[1], "learning_curve": lc,
                          "loss_echo": _echo(store), "learn_val": {
                              n: rel[n][1] for n in ("learn.json", "zc_s1.json") if n in rel}}
    rep = sdc.report(ev, _clean({
        "head": ctx["head"], "gates": last, "models": {m: st.get(m, "INVALID") for m in sd.MODELS},
        "learn": {k: lv.get(k) for k in ("NA-s1", "NA-s2", "decision")}, "flags": fl,
        "learn_test": ctx["learn_test"], "natural": nt, "sharp_target": ctx["sharp"],
        "designed": {**ctx["des"], "ord_d": od, "counts": cnt}, "readout": ctx["readout"],
        "placebo": ctx["res"]["E3.4"]["values"], "descriptive": desc, "env_local": sr.env_local(),
        "sealed_released": {n: h for n, (h, _) in rel.items()}, "cpu_s": time.process_time(),
        "wall_s": time.perf_counter() - ctx["t0"], "beta_bar": nt["mean"], "lb": nt["lb"],
        "k": cnt["PASS"], "f": cnt["FAIL"], "u": cnt["UNRESOLVED"]}))
    sha = _wjson(_dir(ctx) / "report.json", rep)
    return _r(True, {k: rep[k] for k in ("outcome", "rule", "qualifiers")} | {"report.json": sha})

PLAN = {"E1": (("S0", s0, True), ("INGEST-C1", lambda c: _ingest(c, "C1"), True),
               ("LEARN", learn, False), ("LC-1", lambda c: _lc(c, "C1", "learning_curve.json"),
                                         False),
               ("LEARN/stop", lambda c: c["res"]["LEARN"], True)),  # S4 after LC-1 (§4.7)
        "E2": (("S0", s0, True), ("INGEST-C2", ingest_c2, True),
               ("LC-2", lambda c: _lc(c, "C2", "learning_curve_C2.json"), False)),
        "E3a": (("S0", s0, True), ("E3.0", bind, True), ("E3.1", det, True), ("E3.A", e3a, True)),
        "E3w": (("S0", s0, True), ("E3.0", bind, True), ("E3.A", e3a, True)),
        "E3z": (("S0", s0, True), ("E3.2", learn_test, False), ("E3.3", readout, False),
                ("E3.4", placebo, False), ("E3.5", xcheck, False), ("E3.6", stats, False),
                ("E3.7", prec, False), ("E3.8", confirm, False), ("E3.9", rules, True))}
