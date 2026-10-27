"""X6ZC stages B and C: B1-B10 on the opened D, the Stage-B gate, and the registered Stage C
with its sensitivity lines and report (X6ZC-DESIGN-v1 §7-§9; API.md §11.4, §11.6, §20 C-52)."""
# fmt: off

from __future__ import annotations

import json
from pathlib import Path

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
import numpy as np  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6zc_census as zs  # noqa: E402

# isort: off
from x6zc_pipeline import (predict_variants, stage_c_statistics, decide_report,  # noqa: E402
    validate_report)  # noqa: E402
# isort: on
# isort: off
from x6zc_stage_a import (_payload, _npz, _record, _begin, _finish,  # noqa: E402
    _cache, _spec, _predictor, _children)  # noqa: E402
# isort: on
# isort: off
from x6zc_store import (_cj, xwrite, _lines, log_exposure,  # noqa: E402
    log_evaluation, rulings, ledger_cpu, _head)  # noqa: E402
# isort: on

C, X = zc.CONTRACT, zc.CONTRACT["x6s1_store"]
FAM, VO, CO = zc.FAMILIES, zc.VARIANT_ORDER, zc.CELL_ORDER
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
    ro = {(f"init-s1|{F}", "e") for F in ("W2", "W1")}  # R-0134-1: recorded, report-only (F-4)
    bad = {x["status"] for k, r in k5.items() for i, x in r.items() if (k, i) not in ro} - {
        "PASS", "NUMERIC_DRIFT"}
    G["K5"] = {"status": "DEFECT_CANDIDATE" if bad else "PASS", "results": k5,
               "report_only": sorted(f"{k}|{i}" for k, i in ro)}
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
            "checks": {k: st(k) for k in ("A1", "A2", "A_audit", "A3", "K2", "K4", "K5")},
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
        "K3:" + k + ":" + ",".join(f"{a}={b}" for a, b in sorted(p.items())):
            predict_variants(zc.SyntheticPredictor(k, **p), VA)
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
