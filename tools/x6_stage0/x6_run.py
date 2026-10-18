"""X6 stage 0: Monte Carlo, G5-G7, PoE, labels and outcome (D), S0, store lineage, per-gate
records, preflight, run, report and CLI (X6-FROZEN-v1 sections 6-10; API.md 6). Every Decimal
operation runs in an explicit 80-, 120- or 200-digit context (x6_dp.CTX, x6_dp.C200)."""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
import time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

import x6_model as xm
import x6_dp as xd
import x6_exact as xe
from independent_reference import decimal_suffix_posterior, enumerate_posterior
from oracle_profile import suffix_posterior
from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.oracle import BayesFilter, FutureOperator
from x6_model import (ANCHOR_NB, BATCH, LADDER, MC_ARMS, MC_FLOOR, MC_K, MC_ROWS,
                      MC_STREAM, N_CHECK, THETA_ROW, TOL_DEC, TOL_LOGEV, TOL_NUM, WINDOWS)
from x6_store import (  # noqa: F401  (moved by ruling X5; re-exported, API 6.2-6.5)
    G7_DP_ITEMS, G7_ITEMS, ORDER, OUTCOMES, S8_NOT_RUN, _typed, decide, label_cert, labels,
    scratch_ok, write_preflight, ALLOWLIST, ATTEMPT_RE, GATES, KERNEL_DIFF_EXPECTED, MAILBOX,
    METER_FILES, PF_SUITES, PROTECTED_PATHS, VOLATILE_KEYS, _load, _norm, allowlist_ok,
    archive_attempt, canonical_json, compare_attempt, jsonable, kernel_diff_ok,
    lineage_precheck, read_manifest, reports_equal, s0_check, s0_lineage, sha256_file,
    strip_volatile, write_gate, write_manifest, write_marker)

C80, THIRDS = xd.CTX[80], (Fraction(1, 3),) * 3
SIG = np.array([xm.sigma_tok(w) for w in range(18)])

# ---- Monte Carlo and float helpers (API 6.1, sections 9.6, 8.7) ----
def sample(arm: str, n: int, tree):
    m = xm.model("NA", "E_nc") if arm == "NOCUE" else xm.model(arm)
    rng = tree.generator(MC_STREAM, arm)
    return HMMSampler(m["Tf"], m["Ef"], m["pif"], SequenceLayout()).sample(n, rng)
def indicator_se(p, n: int) -> float: return math.sqrt(float(Fraction(p) * (1 - Fraction(p)) / n))
def mc_check(estimate, exact, se): return bool(abs(estimate - exact) <= MC_K * se + MC_FLOOR)
def _mc(est, exact, se) -> dict:
    return {"type": "mc", "estimate": est, "exact": float(exact), "se": se,
            "pass": mc_check(est, float(exact), se)}
def indicator_check(hits: int, n: int, p) -> dict: return _mc(hits / n, p, indicator_se(p, n))
def sample_se(x) -> float: return float(np.std(np.asarray(x, float), ddof=1) / math.sqrt(len(x)))
def _mean(x, exact) -> dict: return _mc(float(np.mean(x)), exact, sample_se(x))
def _flt(value, tol) -> dict: return {"type": "float", "value": float(value), "tol": float(tol)}
def _bf(m: dict): return BayesFilter(m["Tf"], m["Ef"], m["pif"])
def _fo(m: dict): return FutureOperator(m["Tf"], m["Ef"])
def _batches(toks): return (toks[i:i + BATCH] for i in range(0, len(toks), BATCH))
def _clean(*a) -> bool: return all(bool(np.all(np.isfinite(x)) and np.all(x >= 0)) for x in a)
def _maxabs(a, b) -> float: return float(np.max(np.abs(np.asarray(a) - np.asarray(b)), initial=0))
def _kl_rows(p, q):
    with np.errstate(divide="ignore", invalid="ignore"):
        lp, lq = np.log(np.where(p > 0, p, 1.0)), np.log(np.where(p > 0, q, 1.0))
        return np.where(p > 0, p * (lp - lq), 0.0).sum(axis=1)

_CF: dict = {}  # (arm, w_t, fibre) -> float (b_t, q_t); Theorem 1 depends on v_t and the fibre
def _cf_float(arm: str, h) -> tuple:
    cf = xm.closed_form(arm, h)
    key = (arm, h[-1], cf["fibre"])
    if key not in _CF:
        _CF[key] = (xm.to_float(cf["b"]), xm.to_float(cf["q"]))
    return _CF[key]
def _filter_check(arm: str, toks, hook=None) -> dict:
    """Unchanged BayesFilter b_t, q_t (t <= 32, and q_0) against the closed form (Theorem 1)."""
    m = xm.model(arm)
    bf, e, ok = _bf(m), [0.0, 0.0], True
    q0 = xm.to_float(xe.fraction_filter(m["T"], m["E"], m["pi"], [])["q"][0])
    for tk in _batches(toks[:, :32]):
        res, cf = bf.run(tk), [[_cf_float(arm, r[:t]) for t in range(1, 33)] for r in tk.tolist()]
        Q = np.array([[c[1] for c in r] for r in cf])
        e = [max(e[0], _maxabs(res.b, [[c[0] for c in r] for r in cf])),
             max(e[1], _maxabs(res.q[:, 1:], Q), _maxabs(res.q[:, 0], q0))]
        ok &= _clean(res.b, res.q) and bool(np.all(np.isfinite(res.log_evidence)))
        if hook:
            hook(tk, res, Q)
    return {"b": _flt(e[0], TOL_NUM), "q": _flt(e[1], TOL_NUM), "clean": ok,
            "pass": ok and max(e) <= TOL_NUM}

# ---- G5 (sections 8.2, 9.5) ----
def _decimal_reference(na) -> dict:
    """Section 9.5 reference set: Decimal (80 digits; edge cases also 120) against Fractions."""
    m, v = xm.model("NA"), xm.vertex
    bi = [(a, b) for a in range(18) for b in range(18) if v(b) in xm.NEIGHBOURS[v(a)]]
    first = next(tuple(r) for r in na.tolist() if sum(w >= 15 for w in r) >= 3)
    edge = [(5,) * 32, tuple(15 + k % 3 for k in range(32)), xe.witness_tokens("W2", "AB", 1, "P6"),
            xe.witness_tokens("W1", "U", 0) + (17,), first]
    hist = [(w,) for w in range(18)] + bi + [xe.witness_tokens(f, o, y) for f in ("W1", "W2", "W3")
                                             for o in xe.members(f) for y in range(3)]
    hist += edge + [tuple(r) for r in na[:64].tolist()]
    dm, bf, err = {p: xd.decimal_model("NA", p) for p in xd.PRECS}, _bf(m), {}
    for h in hist:
        cf, res = xm.closed_form("NA", h), bf.run([h])
        d80 = decimal_suffix_posterior(*dm[80], h, 80)
        ex = [cf["b"]] + ([xe.fraction_filter(m["T"], m["E"], m["pi"], h)["b"][-1]]
                          if len(h) <= 6 else [])
        ln_p = C80.ln(xd.to_decimal(cf["P"], xd.DIV_PREC[80]))
        new = {"decimal": max(abs(Fraction(d) - f) for e in ex for d, f in zip(d80, e)),
               "float": max(_maxabs(res.b[0, -1], xm.to_float(cf["b"])),
                            _maxabs(res.q[0, -1], xm.to_float(cf["q"]))),
               "log_evidence": abs(Fraction(float(res.log_evidence[0])) - Fraction(ln_p))}
        if h in edge:
            d120 = decimal_suffix_posterior(*dm[120], h, 120)
            new["repeat_120"] = max(abs(Fraction(a) - Fraction(b)) for a, b in zip(d80, d120))
        err.update({k: max(x, err.get(k, x)) for k, x in new.items()})
    h30 = [(w,) for w in range(18)] + bi[:12]
    enum = all(enumerate_posterior(m["T"], m["E"], m["pi"], h) ==
               xe.fraction_filter(m["T"], m["E"], m["pi"], h)["b"][-1] for h in h30)
    tol = {"decimal": TOL_DEC, "repeat_120": TOL_DEC, "float": TOL_NUM, "log_evidence": TOL_LOGEV}
    return {"n_histories": len(hist), "n_repeat_120": len(edge), "enumerate": {
            "n": len(h30), "equal": enum}, "errors": {k: _flt(x, tol[k]) for k, x in err.items()},
            "pass": enum and all(Fraction(err[k]) <= Fraction(tol[k]) for k in tol)}

def gate_G5(rows) -> dict:
    toks, m = rows["NA"][0][:N_CHECK], xm.model("NA")
    fo, acc = _fo(m), {"F1": 0.0, "clean": True, **{k: 0.0 for k in WINDOWS}}

    def hook(tk, res, Q):
        f1 = fo.F1(res.b[:, 31])
        acc["F1"], acc["clean"] = max(acc["F1"], _maxabs(f1, Q[:, 31])), acc["clean"] and _clean(f1)
        for k in WINDOWS:  # stationary restart: the closed form of the window itself
            sp = suffix_posterior(m["Tf"], m["Ef"], m["pif"], tk, k)
            ref = [_cf_float("NA", row[32 - k:])[0] for row in tk.tolist()]
            acc[k], acc["clean"] = max(acc[k], _maxabs(sp, ref)), acc["clean"] and _clean(sp)
    filt, dec = _filter_check("NA", toks, hook), _decimal_reference(rows["NA"][0][:, :32])
    ok = filt["pass"] and dec["pass"] and acc["clean"] and max(acc[k] for k in WINDOWS) <= TOL_NUM
    return {"status": "PASS" if ok and acc["F1"] <= TOL_NUM else "FAIL", "rows": len(toks),
            "filter": filt, "F1": _flt(acc["F1"], TOL_NUM), "decimal": dec,
            "suffix": {k: _flt(acc[k], TOL_NUM) for k in WINDOWS},
            "finite_nonnegative": acc["clean"]}

# ---- G6 (section 8.2, OS 1) ----
@lru_cache(maxsize=None)
def _cue_part(m: int, w) -> np.ndarray:
    lm = xm.lam(m)
    return np.array([float(xm.P_MOVE * (lm * a + (1 - lm) / 3)) for a in w])
@lru_cache(maxsize=None)
def _row_certified(n: int, w, z: int) -> bool:
    """The row's exact class (n, y, v_32, kappa, z) is certified row-KL >= THETA_ROW."""
    return xd.certify(xd._row_enc(xd._both(xd.kl_term, "next", n, w, z)), THETA_ROW) == "PASS"
def _row_info(toks, labels) -> list:
    out = []
    for p in map(xm.parse, toks.tolist()):
        seg = p["segment"]
        out.append(seg and (p["n"], p["y"], p["v"], xm.parikh(seg), xm.holonomy(seg, labels)))
    return out

def gate_G6(rows, g4) -> dict:
    nat, tables, (toks, states) = g4["natural"]["NA"], g4["tables"], rows["NA"]
    m, W = xm.model("NA"), {}
    bf, fo, st = _bf(m), _fo(m), {k: [] for k in LADDER + ("W8", "ifib", "lab_next", "lab_fib")}
    hits = {"E_cue": 0, "amb_nb": 0, "M32": 0}

    def wts(S, n, y, v, kappa):
        if (S, n, y, v, kappa) not in W:
            W[(S, n, y, v, kappa)] = xd.weights(tables[S][(n, v, xm.statistic(S, kappa))], y)
        return W[(S, n, y, v, kappa)]
    for tk, sx in zip(_batches(toks), _batches(states[:, 31].astype(np.int64))):
        res, info, rr = bf.run(tk[:, :32]), _row_info(tk[:, :32], m["labels"]), np.arange(len(tk))
        qs, b, w33 = res.q[:, 32], res.b[:, 31], tk[:, 32].astype(np.int64)
        fib = b.reshape(-1, 16, 3).sum(axis=1)
        st["ifib"].append(math.log(3) - _kl_rows(fib, np.ones_like(fib)))  # ln 3 - H(fibre)
        sp8 = suffix_posterior(m["Tf"], m["Ef"], m["pif"], tk[:, :32], 8)
        st["W8"].append(_kl_rows(qs, fo.F1(sp8)))
        for S in LADDER:
            qS = qs.copy()
            for r, f in enumerate(info):
                if f and f[0] >= 1 and f[2] in ANCHOR_NB:
                    qS[r, 15:18] = _cue_part(f[0] + 1, wts(S, *f[:4]))
            st[S].append(_kl_rows(qs, qS))
        st["lab_next"].append(np.log(qs[rr, w33]) - np.log(qS[rr, w33]))  # qS: Parikh (last S)
        pstar = b[rr, sx]
        ppar = pstar.copy()
        for r, f in enumerate(info):
            hits["E_cue"] += bool(f)
            if f and f[0] >= 1:  # no cue: both fibre laws uniform; n = 0: both the point mass at y
                (n, y, v, kappa, g), w, lm = f, wts("Parikh", *f[:4]), xm.lam(f[0])
                ppar[r] = float(lm * w[int(sx[r]) % 3] + (1 - lm) / 3)
                if v in ANCHOR_NB:
                    hits["amb_nb"] += xd.ambiguous(tables["Parikh"][(n, v, kappa)], y)
                    hits["M32"] += _row_certified(n, w, g[y])
        st["lab_fib"].append(np.log(pstar) - np.log(ppar))
    xd.memo_clear()
    x, n, G = {k: np.concatenate(v) for k, v in st.items()}, len(toks), nat["G"]
    ms = nat["masses"][32]
    comp = {f"G_{S}": _mean(x[S], G[S][32]["v80"]) for S in LADDER}
    comp.update({"G_8": _mean(x["W8"], nat["G_k"][8][32]["v80"]),
                 "E_cue": indicator_check(hits["E_cue"], n, ms["E_cue"]),
                 "E_amb_nb": indicator_check(hits["amb_nb"], n, ms["amb_nb"]["Parikh"]),
                 "M32": indicator_check(hits["M32"], n, nat["M32"]["lower"]),
                 "I_fib": _mean(x["ifib"], nat["I_fib_full"][32]["v80"]),
                 "label_next": _mean(x["lab_next"], G["Parikh"][32]["v80"]),
                 "label_fibre": _mean(x["lab_fib"], nat["J_fib_full"][32]["v80"])})
    ok = len(comp) == 12 and all(c["pass"] for c in comp.values())
    return {"status": "PASS" if ok else "FAIL", "rows": n, "comparisons": comp, "hits": hits,
            "hoeffding_halfwidth": math.sqrt(math.log(2 / 1e-6) / (2 * n))}

# ---- G7 (section 7) and PoE (section 6.3) ----
def _zero(enc) -> bool: return enc["v80"] == 0 and enc["v120"] == 0
def _pos(enc) -> bool: return Fraction(enc["lo"]) > 0
def _q_diffs(toks, base: str, others) -> dict:
    fb, fo = _bf(xm.model(base)), {a: _bf(xm.model(a)) for a in others}
    err = dict.fromkeys(others, 0.0)
    for tk in _batches(toks[:, :32]):
        q = fb.run(tk).q
        err = {a: max(err[a], _maxabs(fo[a].run(tk).q, q)) for a in others}
    return err
def _controls_float(rows) -> dict:
    """NOCUE (NA vs TRIV under E_nc, uniform fibre, base walk) and TOKPERM maximum errors."""
    fa, ft, fe, fs = (_bf(xm.model(a, k)) for a, k in (("NA", "E_nc"), ("TRIV", "E_nc"),
                                                         ("NA", "E"), ("NA", "E_sigma")))
    tb, e = xm.to_float(xm.t_base_exact()), dict.fromkeys(("q", "fibre", "base_walk", "TOKPERM"), 0)
    for tk in _batches(rows["NOCUE"][0][:, :32]):
        ra, rt = fa.run(tk), ft.run(tk)
        fib = [_maxabs(r.b.reshape(len(tk), 32, 16, 3).sum(2), 1 / 3) for r in (ra, rt)]
        e.update(q=max(e["q"], _maxabs(ra.q, rt.q)), fibre=max(e["fibre"], *fib),
                 base_walk=max(e["base_walk"], _maxabs(ra.q[:, 1:], tb[tk])))
    for tk in _batches(rows["NA"][0][:N_CHECK, :32]):
        e["TOKPERM"] = max(e["TOKPERM"], _maxabs(fs.run(SIG[tk]).q[:, :, SIG], fe.run(tk).q))
    return e

def gate_G7(rows, g3, g4, s8: bool = False) -> dict:
    fam, nat, kb = g3["families"], g4.get("natural", {}), g4.get("kblk", {})
    filt = {a: _filter_check(a, rows[a][0]) for a in ("AB", "ZC", "TRIV", "ETA1")}
    det = {**_q_diffs(rows["NA"][0], "NA", ("GAUGE-NA", "GAUGE-COV")),
           **_q_diffs(rows["TRIV"][0], "TRIV", ("GAUGE-TRIV",)), **_controls_float(rows)}
    eta0 = all(xm.lam(k, 1) == 0 and xm.point_law(k, z, 1) == THIRDS for k in range(1, 34)
               for z in range(3))
    labs = set(xm.edge_labels("GAUGE-TRIV").values())
    ident = [r["q"] for r in fam["NA"]["W3|P0|0"]["members"].values() if r["holonomy"] == "e"]
    same = lambda a: all(r["q"] == fam["NA"][c]["members"][o]["q"]  # noqa: E731
                         for c, fv in fam[a].items() for o, r in fv["members"].items())
    item = {f"{a}.filter": f["pass"] for a, f in filt.items()}
    item.update({f"{a}.spread": all(fv["spread"] == 0 for fv in fam[a].values())
                 for a in ("AB", "ZC", "TRIV")})
    cues = [xm.cue_normalised(q) for fv in fam["ETA1"].values() for r in fv["members"].values()
            for q in r["q"].values()]
    item.update({"ETA1.cue_uniform": eta0 and all(c == THIRDS for c in cues),
                 "GAUGE-NA.exact": same("GAUGE-NA"), "GAUGE-COV.exact": same("GAUGE-COV"),
                 "GAUGE-TRIV.noncommuting": any(xm.compose(g, h) != xm.compose(h, g) for g in labs
                                                for h in labs),
                 "NOCUE": max(det[k] for k in ("q", "fibre", "base_walk")) <= TOL_NUM,
                 "SAME-HOLONOMY": len(ident) == 16 and all(q == ident[0] for q in ident),
                 "TOKPERM": det["TOKPERM"] <= TOL_NUM,
                 **{f"{k}.filter": det[k] <= TOL_NUM for k in ("GAUGE-NA", "GAUGE-TRIV",
                                                              "GAUGE-COV")}})
    if not s8:  # the DP-dependent items (section 8.5 S8)
        fp, zc = nat["AB"]["fixed_point"], nat["ZC"]

        def gs(a, Ss):
            return all(_zero(nat[a]["G"][S][t]) for S in Ss for t in range(1, 33))
        item.update({"AB.ambiguity": nat["AB"]["null"]["parity"], "ZC.ambiguity": zc["null"]["H1"],
                     "AB.G_S": gs("AB", LADDER[1:]), "TRIV.G_S": gs("TRIV", LADDER),
                     "ETA1.G_S": eta0,
                     "ZC.G_S": gs("ZC", ("H1", "Parikh")) and _pos(zc["G"]["parity"][32]) and
                     _pos(zc["G"]["counts"][32]) and min(zc["zc_witness"].get(z, 0) for z in
                                                         ("c", "c2")) > 0,
                     "FIXED-POINT": not fp["amb_y"][2] and fp["amb_y"][0] and fp["amb_y"][1] and
                     _zero(fp["G_empty_y"][2]) and _pos(fp["G_empty_y"][0]) and
                     _pos(fp["G_empty_y"][1]),
                     **{f"{a}.D_blk": _zero(kb[a]["D_blk"]) and not kb[a]["ambiguous_any"]
                        for a in ("AB", "ZC", "TRIV")}})
    items = {k: "NOT_RUN" if k not in item else "PASS" if item[k] else "FAIL" for k in G7_ITEMS}
    ok = all(v == "PASS" for k, v in items.items() if not (s8 and k in G7_DP_ITEMS))
    return {"status": "PASS" if ok else "FAIL", "items": items, "filter": filt,
            "max_err": {k: _flt(v, TOL_NUM) for k, v in det.items()}}

def poe(rows) -> dict:
    out = {}
    for arm in ("NA", "AB", "TRIV"):
        m, vals = xm.model(arm), []
        bf, fo = _bf(m), _fo(m)
        prop = [np.linalg.matrix_power(m["Tf"], 24 - 8 * k) for k in range(4)]  # T^(32 - 8 beta)
        for tk in _batches(rows[arm][0][:N_CHECK]):
            prod = np.prod([bf.run(tk[:, 8 * k:8 * k + 8]).b[:, 7] @ prop[k] for k in range(4)], 0)
            q_poe = fo.F1(prod / prod.sum(axis=1, keepdims=True))
            vals.append(_kl_rows(bf.run(tk[:, :32]).q[:, 32], q_poe))
        v = np.concatenate(vals)
        out[arm] = {"type": "mc", "estimate": float(np.mean(v)), "se": sample_se(v), "rows": len(v)}
    return out

# ---- preflight, run, report (API 6.5) ----
def _call(fn, *args) -> dict:
    try:
        return fn(*args)
    except Exception as exc:  # noqa: BLE001  (S2 in G0; otherwise a recorded defect: INVALID)
        return {"status": "INVALID", "error": f"{type(exc).__name__}: {exc}"}

def run(store, dispatch) -> dict:
    t0, store, disp = time.process_time(), Path(store), _load(dispatch)
    rdir, st, vals, res, rows = store / "run", dict.fromkeys(ORDER + ("D",), "NOT_RUN"), {}, {}, {}
    pf = _load(rdir / "preflight.json") if (rdir / "preflight.json").is_file() else {}
    pf_ok = pf.get("status") == "PASS" and pf.get("head") == disp["head"]
    pf_ok &= pf.get("job") == disp["job"]
    st["PF"], vals["PF"] = "PASS" if pf_ok else "INVALID", {"preflight": pf}
    if pf_ok:
        vals["S0"] = _call(s0_check, disp["worktree"], disp["head"], store, disp)
        st["S0"] = vals["S0"]["status"]
        for g in ("PF", "S0"):
            write_gate(rdir, g, st[g], {})
    tree, s8 = SeedTree(xm.MASTER_SEED), None

    def mc():  # the six streams, issued once, in MC_ARMS order (section 8.6)
        rows.update({} if rows else {a: sample(a, MC_ROWS[a], tree) for a in MC_ARMS})
        return rows
    steps = (("G0", xm.gate_G0), ("G1", xm.gate_G1), ("G2", xe.gate_G2), ("G3", xe.gate_G3),
             ("G4", xd.gate_G4), ("G5", lambda: gate_G5(mc())),
             ("G6", lambda: gate_G6(mc(), res["G4"])),
             ("G7", lambda: gate_G7(mc(), res["G3"], res["G4"], s8 is not None)))
    for name, fn in steps:
        if st["S0"] != "PASS" or any(st[g] in ("FAIL", "INVALID") for g in ORDER):
            break
        if name == "G6" and s8:
            continue  # S8: G6 is NOT_RUN and gets no marker
        write_marker(rdir, name)
        r = res[name] = _call(fn)
        st[name], vals[name] = r["status"], {k: v for k, v in r.items() if k != "tables"}
        if name == "G4" and r["status"] == "RESOURCE_LIMIT":
            s8 = {"completed_checks_pass": "FAIL" not in r["checks"].values(),
                  "theorem4": r["checks"].get("theorem4") == "PASS"}
        write_gate(rdir, name, st[name], vals[name])
    o1v = xe.o1(res["G3"]) if st["G3"] == "PASS" else None
    o2v = xe.o2(res["G4"]) if st["G4"] == "PASS" else None
    dec = decide({g: st[g] for g in ORDER}, o1v and o1v["status"] == "PASS",
                 o2v and o2v["status"], s8)
    lab = None
    if dec["verdict"] not in ("FAIL", "INVALID"):
        write_marker(rdir, "D")
        lab = _call(lambda: labels(res["G3"], res["G4"], poe(mc())))
        st["D"], vals["D"] = "INVALID" if lab.get("status") else "PASS", {
            "o1": o1v, "o2": o2v, "s8": s8, "outcome": dec, "labels": lab}
        write_gate(rdir, "D", st["D"], vals["D"])
    arrays = {"T_base": xm.to_float(xm.t_base_exact()),
              **{f"T_lift_{a}": xm.model(a)["Tf"] for a in xm.ARMS},
              **{k: xm.to_float(xm.emission(k)) for k in xm.EMISSIONS}}
    g3, g4 = vals.get("G3", {}), vals.get("G4", {})
    report = {"protocol": xm.PROTOCOL_ID, "protocol_sha256": xm.PROTOCOL_SHA256,
              "verdict": dec["verdict"], "first_failed": dec["first_failed"],
              "gates": {g: {**vals.get(g, {}), "status": st[g]} for g in st},
              "exact": {"G2": vals.get("G2"), "G3": {k: g3.get(k) for k in (
                  "families", "matched", "keys_constant", "beta", "set_gaps", "prefix_invariant")}},
              "natural": g4.get("natural"),
              "challenge": {k: g3.get(k) for k in ("challenge", "comparator")},
              "blocks": {"kblk": g4.get("kblk"), "PoE": (lab or {}).get("PoE")},
              "controls": vals.get("G7"),
              "mc": vals.get("G6"), "decimal": vals.get("G5"), "outcome": dec, "labels": lab,
              "seeds": dict(tree.issued),
              "cpu_s": {"type": "resource", "value": time.process_time() - t0},
              "model_sha256": {k: hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
                               for k, a in arrays.items()}}
    if rdir.is_dir():
        with open(rdir / "report.json", "xb") as fh:
            fh.write(canonical_json(_typed(report)))
        with open(rdir / "model.npz", "xb") as fh:
            np.savez(fh, **arrays)
    return report

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=("precheck", "preflight", "run"))
    for opt, default in (("--store", xm.STORE), ("--record", None), ("--dispatch", None)):
        ap.add_argument(opt, default=default)
    a = ap.parse_args(argv)
    if a.cmd == "run":
        rep = run(a.store, a.dispatch)
        print(canonical_json({k: rep[k] for k in ("verdict", "first_failed", "outcome")}).decode())
        return 0
    out = (lineage_precheck(a.store) if a.cmd == "precheck" else
           write_preflight(a.store, _load(a.record)))
    print(canonical_json(out).decode())
    return 0 if out["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
