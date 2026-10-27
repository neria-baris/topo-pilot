"""X6ZC stage 0: the synthetic dry run of every CONTRACT fixture through the pipeline
(X6ZC-DESIGN-v1 §12; API.md §15, §20 C-52). Synthetic data only."""
# fmt: off

from __future__ import annotations

import io
import math
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
from x6zc_pipeline import (predict_variants, stage_c_statistics, decide_report)  # noqa: E402
# isort: on
# isort: off
from x6zc_store import (_utc, _sha, _norm, _cj, xwrite, ledger_cpu,  # noqa: E402
    pause_check)  # noqa: E402
# isort: on

C, X = zc.CONTRACT, zc.CONTRACT["x6s1_store"]
FAM, VO, CO = zc.FAMILIES, zc.VARIANT_ORDER, zc.CELL_ORDER

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
