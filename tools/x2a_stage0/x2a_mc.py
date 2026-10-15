"""X2a stage 0, part 2 (X2A-FROZEN-v1; API.md): seeded sampling, batched filter statistics,
windows, blocks, additive score, credits, SE / intervals / Hoeffding, decision labels, G3, G4, D,
G5 and the descriptive Monte Carlo (N-local, P-ref, long horizon)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path[:0] = [p for p in (str(Path(__file__).resolve().parent),) if p not in sys.path]

import x2a_model as xm  # noqa: E402
from independent_reference import decimal_suffix_posterior  # noqa: E402  (unchanged)
from oracle_profile import suffix_posterior  # noqa: E402  (job-0014, unchanged)
from scipy.special import expit, log_expit, xlogy  # noqa: E402

from topo_pilot.contracts import SequenceLayout  # noqa: E402
from topo_pilot.dataset import HMMSampler  # noqa: E402
from topo_pilot.oracle import BayesFilter, LastSymbolPosterior, context_gain  # noqa: E402

TAU, Z99, LN2, NA, ALLOW = xm.TAU, xm.Z99, xm.LN2, xm.N, 2e-12
CURVE_T = (1, 2, 4, 8, 16, 24, 32)
MC_SIZES = {"main": 2**19, "N-iso": 2**15, "N-same": 2**13, "N-id": 2**12, "P-ref": 2**17,
            "N-local": 2**17}

# ---- elementary statistics (Lemma C, Lemma A, §6.3) -------------------------------------------
def entropy_b(p):
    p = np.asarray(p, dtype=np.float64)
    return -(xlogy(p, p) + xlogy(1 - p, 1 - p))

def _hb(mA, mB):
    return -(xlogy(mA, mA) + xlogy(mB, mB))

def mass_pi(b, n_A=NA):
    return np.asarray(b)[..., n_A:].sum(-1)

def mass_logit(b, n_A=NA):
    b = np.asarray(b)
    return np.log(b[..., n_A:].sum(-1)) - np.log(b[..., :n_A].sum(-1))

def expit_pi(s):
    return expit(np.asarray(s, dtype=np.float64))

def decision(pi_d, tau=TAU):
    p = np.asarray(pi_d, dtype=np.float64)
    return np.where(np.abs(p - 0.5) <= tau, -1, np.where(p > 0.5, 1, 0)).astype(np.int8)

def credit(pi_full, pi_d, tau=TAU):
    d, pf = decision(pi_d, tau), np.asarray(pi_full, dtype=np.float64)
    return np.where(d == 1, pf, np.where(d == 0, 1 - pf, 0.5))

def additive_score(Tt, Et, pit, tokens, n_A=NA, block=8, n_blocks=4):
    bf, tok = BayesFilter(Tt, Et, pit), np.asarray(tokens)
    return sum(mass_logit(bf.run(tok[:, block * i: block * (i + 1)]).b[:, block - 1], n_A)
               for i in range(n_blocks))

def strat_mean_se(x_A, x_B):
    a, b = np.asarray(x_A, dtype=np.float64), np.asarray(x_B, dtype=np.float64)
    se = np.sqrt(0.25 * (a.var(0, ddof=1) / len(a) + b.var(0, ddof=1) / len(b)))
    return 0.5 * (a.mean(0) + b.mean(0)), se

def interval(mean, se, z=Z99):
    return mean - z * se, mean + z * se

def hoeffding(R, n, delta):
    return R * math.sqrt(math.log(2 / delta) / (2 * n))

def _lu(m, se, hw):
    return (m - hw, m + hw) if hw is not None else interval(m, se)

def p3_label(d3, se, hw=None):
    lo, hi = _lu(d3, se, hw)
    return "PASS" if lo - TAU >= 0.10 else "FAIL" if hi < 0.10 else "THRESHOLD_INCONCLUSIVE"

def p4_label(i8, se8, i32, se32, hw8=None, hw32=None):
    (l8, u8), (l32, u32) = _lu(i8, se8, hw8), _lu(i32, se32, hw32)
    return ("PASS" if u8 <= 0.5 * l32 else "FAIL" if l8 > 0.5 * u32
            else "THRESHOLD_INCONCLUSIVE")

def a3_label(d_add, se, hw=None):
    return "NONADDITIVE" if _lu(d_add, se, hw)[0] >= 0.03 else "ADDITIVE"

def scientific_outcome(p3, p4, a3):
    if p3 == "PASS" and p4 == "PASS":
        return "GO_P1_NONADDITIVE" if a3 == "NONADDITIVE" else "GO_P1_ADDITIVE"
    return "STOP_P1"

def hoeffding_label(S, delta=0.01):
    hw = (lambda R: hoeffding(R, S["n"], delta))  # noqa: E731
    g = (lambda k: S[k]["est"])  # noqa: E731
    return {"P3": p3_label(g("D3"), 0, hw=hw(1.0)), "A3": a3_label(g("Dadd"), 0, hw=hw(1.0)),
            "P4": p4_label(g("Iw8"), 0, S["I_t"]["est"][31], 0, hw8=hw(LN2), hw32=hw(LN2))}

# ---- sampling and per-row statistics (§6.1, §4.2) ------------------------------------------------
def sample(T, E, n, rng, n_obs=33):
    pi = np.full(T.shape[0], 1.0 / T.shape[0])
    return HMMSampler(T, E, pi, SequenceLayout(n_obs=n_obs)).sample(n, rng)[0]

def _kl(p, r):
    return (p * (np.log(p) - np.log(r))).sum(-1)

def _batch(m, tok, label, keep):
    bf = BayesFilter(m["Tt"], m["Et"], m["pit"])
    f = bf.run(tok[:, :32])
    b = f.b
    mA, mB = b[..., :NA].sum(-1), b[..., NA:].sum(-1)
    qA = (b[..., :NA] / mA[..., None]) @ (m["T"] @ m["E1"])
    qB = (b[..., NA:] / mB[..., None]) @ (m["T"] @ m["E2"])
    q, H, lg = f.q[:, 1:], _hb(mA, mB), np.log(mB) - np.log(mA)
    win = {k: bf.run(tok[:, 32 - k:32]).b[:, k - 1] for k in xm.WINDOWS}
    blk = [mass_logit(bf.run(tok[:, 8 * i:8 * i + 8]).b[:, 7]) for i in range(3)]
    s_add = sum(blk) + mass_logit(win[8])
    pi32, pa32 = mB[:, -1], mA[:, -1]
    o = {"I": LN2 - H, "acc": np.maximum(mA, mB), "logit": lg, "s_add": s_add,
         "inc": (mA * _kl(qA, q) + mB * _kl(qB, q))[:, :31], "V": _kl(q, 0.5 * (qA + qB)),
         "cr32": np.maximum(pi32, pa32), "pi1dev": np.abs(mB[:, 0] - 0.5),
         "ILB": LN2 + pi32 * log_expit(s_add) + pa32 * log_expit(-s_add)}
    if label is not None:
        o["Ip"] = LN2 + np.log(mB if label else mA)
    for k, bw in win.items():
        wA, wB = bw[:, :NA].sum(-1), bw[:, NA:].sum(-1)
        o[f"Iw{k}"], o[f"accw{k}"] = LN2 - _hb(wA, wB), np.maximum(wA, wB)
        o[f"crw{k}"] = credit(pi32, wB)
    o["cr_add"] = credit(pi32, expit(s_add))
    o["D3"], o["Dadd"] = o["cr32"] - o["crw8"], o["cr32"] - o["cr_add"]
    o["P4row"], o["add_m8"] = o["I"][:, -1] - 2 * o["Iw8"], o["cr_add"] - o["crw8"]
    q_last = LastSymbolPosterior(m["Tt"], m["Et"], m["pit"]).q_last(tok[:, 31])
    o["cg_last"] = np.full(len(tok), context_gain(f.q[:, 32], q_last))
    o["cg8"] = np.full(len(tok), context_gain(f.q[:, 32], win[8] @ (m["Tt"] @ m["Et"])))
    if keep:
        o["b32"], o["bw8"] = b[:keep, -1], win[8][:keep]
        o["bcurve"] = b[:keep, [t - 1 for t in CURVE_T]]
    return o

def row_stats(model, tokens, batch=2048, label=None, keep=0):
    parts = []
    for s in range(0, len(tokens), batch):
        k = max(0, min(batch, keep - s))
        parts.append(_batch(model, np.asarray(tokens[s:s + batch], dtype=np.int64), label, k))
    return {key: np.concatenate([p[key] for p in parts if key in p]) for key in parts[0]}

def _ms(A, B, key, R=None, n=None, f=None):
    f = f or (lambda s: s[key])
    est, se = strat_mean_se(f(A), f(B))
    out = {"est": est, "se": se, "L99": est - Z99 * se, "U99": est + Z99 * se}
    if R is not None:
        out["hoeffding"] = hoeffding(R, n, 1e-6)
    return out

def summarise(A, B):
    n = len(A["cr32"]) + len(B["cr32"])
    S = {"n": n, "I_t": _ms(A, B, "I", LN2, n), "acc_t": _ms(A, B, "acc", 0.5, n),
         "inc": _ms(A, B, "inc"), "V_t": _ms(A, B, "V"), "cr32": _ms(A, B, "cr32", 1.0, n),
         "D3": _ms(A, B, "D3", 1.0, n), "Dadd": _ms(A, B, "Dadd", 1.0, n),
         "acc_add": _ms(A, B, "cr_add", 1.0, n), "ILB": _ms(A, B, "ILB"),
         "P4row": _ms(A, B, "P4row"), "add_m8": _ms(A, B, "add_m8"),
         "cg_last": _ms(A, B, "cg_last"), "cg8": _ms(A, B, "cg8")}
    for k in xm.WINDOWS:
        S[f"Iw{k}"], S[f"accw{k}"] = _ms(A, B, f"Iw{k}", LN2, n), _ms(A, B, f"accw{k}", 0.5, n)
        S[f"crw{k}"] = _ms(A, B, f"crw{k}", 1.0, n)
    if "Ip" in A:
        S["Ip_t"] = _ms(A, B, "Ip")
        S["pair_I_Ip"] = _ms(A, B, None, f=lambda s: s["I"] - s["Ip"])
    S["pair_steps"] = _ms(A, B, None, f=lambda s: np.diff(s["I"], axis=1))
    S["pair_chain"] = _ms(A, B, None, f=lambda s: s["inc"].sum(1) - s["I"][:, -1])
    S["pair_win"] = {k: {"I": _ms(A, B, None, f=lambda s, k=k: s[f"Iw{k}"] - s["I"][:, k - 1]),
                         "acc": _ms(A, B, None,
                                    f=lambda s, k=k: s[f"accw{k}"] - s["acc"][:, k - 1])}
                     for k in (2, 4, 8)}
    S["pair_cr_max8"] = _ms(A, B, None, f=lambda s: s["crw8"] - s["accw8"])
    pooled = np.concatenate([LN2 - A["I"], LN2 - B["I"]])
    acc = np.concatenate([A["acc"], B["acc"]])
    S["concentration"] = {"ge_0.9": (acc >= 0.9).mean(0), "ge_0.99": (acc >= 0.99).mean(0),
                          "H_quantiles": np.quantile(pooled, [0.05, 0.25, 0.5, 0.75, 0.95], 0)}
    mlA, mlB = A["logit"].mean(0), B["logit"].mean(0)
    t = np.arange(16, 33)
    S["llr"] = {"mean_logit_A": mlA, "mean_logit_B": mlB,
                "slope_A": float(np.polyfit(t, mlA[15:], 1)[0]),
                "slope_B": float(np.polyfit(t, mlB[15:], 1)[0])}
    num = (-A["s_add"]).mean() + B["s_add"].mean()
    S["rho_add"] = float(num / ((-A["logit"][:, -1]).mean() + B["logit"][:, -1].mean()))
    S["pi1dev_max"] = float(max(A["pi1dev"].max(), B["pi1dev"].max()))
    return S

# ---- gates -------------------------------------------------------------------------------------
def _max(acc, key, val):
    acc[key] = max(acc.get(key, 0.0), float(np.max(val)))

def gate_G3(m, tok_A, tok_B, exact=None, n_rows=2**13, chunk=1024):
    bf = BayesFilter(m["Tt"], m["Et"], m["pit"])
    comp = [BayesFilter(m["T"], E, np.full(NA, 1.0 / NA)) for E in (m["E1"], m["E2"])]
    err, finite, chosen = {}, True, []
    for tok in (tok_A, tok_B):
        llr32 = []
        for s in range(0, n_rows, chunk):
            t = np.asarray(tok[s:s + chunk, :32], dtype=np.int64)
            f, st = bf.run(t), xm.stencil_filter(m["E1"], m["E2"], t)
            mA, mB = f.b[..., :NA].sum(-1), f.b[..., NA:].sum(-1)
            _max(err, "belief", np.abs(f.b - st["b"]))
            _max(err, "pi", np.abs(mB - st["pi"]))
            fa, fb = comp[0].run(t), comp[1].run(t)
            llr = np.cumsum(fa.ce, 1) - np.cumsum(fb.ce, 1)
            _max(err, "expit", np.abs(expit(llr) - mB))
            mix = mA[..., None] * fa.q[:, 1:] + mB[..., None] * fb.q[:, 1:]
            _max(err, "q", np.abs(f.q[:, 1:] - mix))
            _max(err, "evidence", np.abs(np.expm1(f.log_evidence - st["log_evidence"])))
            for K in xm.WINDOWS:
                sp = suffix_posterior(m["Tt"], m["Et"], m["pit"], t, K)
                _max(err, "suffix", np.abs(sp - bf.run(t[:, 32 - K:]).b[:, -1]))
            for i in range(4):
                bl = t[:, 8 * i:8 * i + 8]
                sp = suffix_posterior(m["Tt"], m["Et"], m["pit"], bl, 8)
                _max(err, "suffix", np.abs(sp - bf.run(bl).b[:, -1]))
            arrs = (f.b, f.q, st["b"], fa.q, fb.q, llr)
            finite &= all(np.isfinite(a).all() for a in arrs)
            finite &= min(a.min() for a in arrs[:5]) >= 0
            llr32.append(llr[:, -1])
        a = np.abs(np.concatenate(llr32))
        rest = np.lexsort((np.arange(8, n_rows), -a[8:]))[:4] + 8
        chosen.append((tok, list(range(8)) + sorted(int(r) for r in rest)))
    T_l, E_l, p_l = m["Tt"].tolist(), m["Et"].tolist(), m["pit"].tolist()
    rows = []
    for tok, idx in chosen:
        for r in idx:
            ref = decimal_suffix_posterior(T_l, E_l, p_l, tok[r, :32].tolist(), digits=80)
            b32 = bf.run(np.asarray(tok[r:r + 1, :32], dtype=np.int64)).b[0, -1]
            rows.append(r)
            _max(err, "decimal", np.abs(np.array([float(x) for x in ref]) - b32))
    tol = {"belief": 1e-12, "pi": 1e-11, "expit": 1e-10, "q": 1e-12, "evidence": 1e-10,
           "suffix": 1e-12, "decimal": 1e-12}
    checks = {k: err[k] <= v for k, v in tol.items()}
    checks["finite_nonnegative"] = bool(finite)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {"status": status, "checks": checks, "max_err": err, "decimal_rows": rows}

def gate_G4(exact, S):
    Iex, acc, c = exact["main"]["I"], exact["main"]["acc"], {}
    ok = (lambda d, se: abs(d) <= 4 * se + ALLOW)  # noqa: E731
    c["I1"] = S["I_t"]["est"][0] <= 1e-14 and S["pi1dev_max"] <= 1e-14
    for k in (2, 3, 4):
        for nm, key in (("I", "I_t"), ("acc", "acc_t")):
            x, ex = S[key], (Iex if nm == "I" else acc)[k - 1]
            d = x["est"][k - 1] - ex
            c[f"{nm}{k}_exact"] = ok(d, x["se"][k - 1]) and abs(d) <= x["hoeffding"]
    for k in (2, 4, 8):
        for nm in ("I", "acc"):
            x = S["pair_win"][k][nm]
            c[f"stationary_{nm}{k}"] = ok(x["est"], x["se"])
    x = S["pair_I_Ip"]
    for t in (4, 8, 16, 32):
        c[f"I_vs_Ip_{t}"] = ok(x["est"][t - 1], x["se"][t - 1])
    c["chain"] = ok(S["pair_chain"]["est"], S["pair_chain"]["se"])
    st = S["pair_steps"]
    for t in range(31):
        c[f"monotone_{t + 1}"] = st["est"][t] >= -4 * st["se"][t] - ALLOW
    c["credit_vs_max8"] = ok(S["pair_cr_max8"]["est"], S["pair_cr_max8"]["se"])
    n4 = len(c) - 1
    return {"status": "PASS" if all(c.values()) else "FAIL", "checks": c, "n_four_se": n4}

def gate_D(S):
    v = {"D3": S["D3"], "Iw8": S["Iw8"], "I32": {k: S["I_t"][k][31] if k != "hoeffding"
                                                 else S["I_t"][k] for k in S["I_t"]},
         "Dadd": S["Dadd"], "acc_add": S["acc_add"], "ILB": S["ILB"], "rho_add": S["rho_add"],
         "P4_paired": S["P4row"], "acc_add_minus_acc8": S["add_m8"]}
    lab = {"P3": p3_label(S["D3"]["est"], S["D3"]["se"]),
           "P4": p4_label(S["Iw8"]["est"], S["Iw8"]["se"], v["I32"]["est"], v["I32"]["se"]),
           "A3": a3_label(S["Dadd"]["est"], S["Dadd"]["se"])}
    hl = hoeffding_label(S)
    return {"values": v, "labels": lab, "outcome": scientific_outcome(**{k.lower(): lab[k]
                                                                          for k in lab}),
            "hoeffding_labels": hl, "block_boundaries": [8, 16, 24],
            "bound_robustness": {k: "BOUND_SENSITIVE" if hl[k] != lab[k] else "UNCHANGED"
                                 for k in lab},
            "U99_Dadd_below_0.03": bool(S["Dadd"]["U99"] < 0.03)}

def control_tokens(models, tree):
    out = {}
    for v in ("N-iso", "N-same", "N-id", "P-ref", "N-local"):
        m = models[v]
        out[v] = [sample(m["T"], m[E], MC_SIZES[v], tree.generator("x2a0_mc", v, c))
                  for E, c in (("E1", "A"), ("E2", "B"))]
    return out

def _pi_dev(m, toks, batch=2048, full=False):
    bf, dev = BayesFilter(m["Tt"], m["Et"], m["pit"]), {"pi": 0.0, "belief": 0.0}
    for tok in toks:
        for s in range(0, len(tok), batch):
            b = bf.run(np.asarray(tok[s:s + batch, :32], dtype=np.int64)).b
            _max(dev, "pi", np.abs(b[..., NA:].sum(-1) - 0.5))
            if full:
                _max(dev, "belief", np.abs(b - 1.0 / xm.N_MIX))
    return dev

def gate_G5(models, exact, ctl, main_tok, n_swap=2**13):
    ex = {v: max(exact[v]["I"]) for v in ("N-iso", "N-same")}
    iso, same = _pi_dev(models["N-iso"], ctl["N-iso"]), _pi_dev(models["N-same"], ctl["N-same"])
    nid = _pi_dev(models["N-id"], ctl["N-id"], full=True)
    m, ms = models["main"], models["N-swap"]
    sw, inv = {"pi": 0.0}, {}
    for tok in main_tok:
        t = np.asarray(tok[:n_swap], dtype=np.int64)
        a, b = row_stats(m, t), row_stats(ms, t)
        for s in range(0, n_swap, 2048):
            pa = BayesFilter(m["Tt"], m["Et"], m["pit"]).run(t[s:s + 2048, :32]).b
            pb = BayesFilter(ms["Tt"], ms["Et"], ms["pit"]).run(t[s:s + 2048, :32]).b
            _max(sw, "pi", np.abs(pb[..., NA:].sum(-1) - pa[..., :NA].sum(-1)))
        for k in ["I", "acc"] + [f"{p}w{k}" for p in ("I", "acc") for k in xm.WINDOWS]:
            inv[k] = max(inv.get(k, 0.0), float(np.max(np.abs(a[k].mean(0) - b[k].mean(0)))))
    checks = {"N-iso_exact": ex["N-iso"] <= 1e-12, "N-iso_mc": iso["pi"] <= 1e-12,
              "N-same_exact": ex["N-same"] <= 1e-15, "N-same_mc": same["pi"] <= 1e-12,
              "N-id_beliefs": nid["belief"] <= 1e-15, "N-id_pi": nid["pi"] <= 1e-15,
              "N-swap_pi": sw["pi"] <= 1e-12, "N-swap_invariants": max(inv.values()) <= 1e-12}
    vals = {"exact_max_I": ex, "N-iso_pi_dev": iso["pi"], "N-same_pi_dev": same["pi"],
            "N-id": nid, "N-swap_pi_dev": sw["pi"], "N-swap_estimate_dev": inv}
    return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, **vals}

def descriptive_mc(models, ctl, exact, keep_pref=4096):
    out, beliefs = {}, {}
    for v in ("N-local", "P-ref"):
        m = models[v]
        A = row_stats(m, ctl[v][0], label=0)
        B = row_stats(m, ctl[v][1], label=1, keep=keep_pref if v == "P-ref" else 0)
        S = summarise(A, B)
        if v == "P-ref":
            beliefs["P-ref_B"] = B["b32"]
        d = gate_D(S)
        out[v] = {"exact": exact[v], "summary": S, "D_values": d["values"],
                  "D_labels_as_values": d["labels"]}
        if v == "N-local":
            x = S["Dadd"]
            out[v]["reading_rule"] = ("EXPECTED_BELOW_0.03" if x["U99"] < 0.03 else
                                      "QUALIFIER_REQUIRED" if x["L99"] >= 0.03 else "INDETERMINATE")
    return out, beliefs

def long_horizon(m, tree, n=2**15, ts=(32, 48, 64, 96, 128), batch=4096):
    toks = [sample(m["T"], m[E], n, tree.generator("x2a0_long", c), n_obs=128)
            for E, c in (("E1", "A"), ("E2", "B"))]
    sp = (lambda tk, K: suffix_posterior(m["Tt"], m["Et"], m["pit"], tk, K))  # noqa: E731
    res = {}
    for key, t, K in [(f"t{t}", t, t) for t in ts] + [("win8_t128", 128, 8), ("win8_t32", 32, 8)]:
        st = [[], []]
        for i, tok in enumerate(toks):
            for s in range(0, n, batch):
                b = sp(np.asarray(tok[s:s + batch, :t], dtype=np.int64), K)
                st[i].append(np.stack((b[:, :NA].sum(-1), b[:, NA:].sum(-1)), 1))
        ms = [np.concatenate(x) for x in st]  # separately accumulated masses (RC 8)
        f = (lambda g: strat_mean_se(g(ms[0]), g(ms[1])))  # noqa: E731
        mx = (lambda a: np.maximum(a[:, 0], a[:, 1]))  # noqa: E731
        Ik, acc = f(lambda a: LN2 - _hb(a[:, 0], a[:, 1])), f(mx)
        res[key] = {"I": Ik, "acc": acc, "ge_0.9": f(lambda a: mx(a) >= 0.9)[0],
                    "ge_0.99": f(lambda a: mx(a) >= 0.99)[0]}
    rel = {"stencil_pi": 0.0, "decimal": 0.0}
    for tok in toks:
        t = np.asarray(tok[:512], dtype=np.int64)
        st = xm.stencil_filter(m["E1"], m["E2"], t)
        for tt in ts:
            _max(rel, "stencil_pi", np.abs(st["pi"][:, tt - 1] - mass_pi(sp(t[:, :tt], tt))))
        full = sp(t[:2], 128)
        for r in range(2):
            ref = decimal_suffix_posterior(m["Tt"].tolist(), m["Et"].tolist(), m["pit"].tolist(),
                                           t[r].tolist(), digits=80)
            _max(rel, "decimal", np.abs(np.array([float(x) for x in ref]) - full[r]))
    res["reliability"] = {**rel, "status": "RELIABLE" if max(rel.values()) <= 1e-10
                          else "UNRELIABLE"}
    return res
