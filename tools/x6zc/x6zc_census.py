"""X6ZC census: the A-audit of the stored pairs, A4 exposure matching, the K4 comparison, the K5
independent checks, B3, B4, B6, B7, B10, D2, D3 and the Stage-B descriptive tier (X6ZC-DESIGN-v1
§6-§7; API.md §10, §20). Descriptive except where a check status is returned. No I/O."""
# fmt: off

from __future__ import annotations

import math
from collections import Counter
from fractions import Fraction

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
import numpy as np  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_pairs as sp  # noqa: E402

PASS, DC = "PASS", "DEFECT_CANDIDATE"
K4_KEYS = ("beta_W2", "beta_W2_y", "R_W2", "Delta_W3", "rho_C", "rho_W2", "cue_mass_median",
           "beta_W1", "beta_W3", "beta_W3_bal", "beta_W3p")
def _st(ok) -> str: return PASS if ok else DC
def _ints(row) -> tuple: return tuple(int(w) for w in row)
def _ts(t, n) -> np.ndarray: return np.broadcast_to(np.asarray(t, np.int64), (n,)).copy()

# ---- A-audit (§6): identities from history content, never from row position ----
def _audit_row(ra, rb, t, y, family) -> str | None:
    for row in (ra, rb):
        nz = np.flatnonzero(row)
        if not len(nz) or nz[-1] + 1 != t or row[t:].any():
            return "stored t is not the unpadded length"
    ha, hb = _ints(ra[:t]), _ints(rb[:t])
    try:
        pa, pb = xm.parse(ha), xm.parse(hb)
        mem = family in sp.CONTROL_SETS or (zc.member_of(ha), zc.member_of(hb)) == ("a", "b")
    except ValueError as e:
        return f"illegal history or crossings: {e}"
    if (pa["prefix"], pa["s"], pa["y"]) != (pb["prefix"], pb["s"], pb["y"]) or pa["y"] != y:
        return "prefix, cue or cue position differs"
    if family in sp.CONTROL_SETS:
        return None
    if (pa["n"], pa["v"], xm.parikh(pa["segment"])) != (pb["n"], pb["v"], xm.parikh(pb["segment"])):
        return "n, end vertex or directed seam-crossing counts differ"
    if not mem:
        return "member a does not cross x first"
    if family == "W2" and not (Counter(ha) == Counter(hb) and ha[-8:] == hb[-8:]
                               and Counter(zip(ha, ha[1:])) == Counter(zip(hb, hb[1:]))):
        return "W2 bag, bigram or last-8 mismatch"
    if family == "W1" and not (ha[-4:] == hb[-4:] and Counter(ha) - Counter(hb) == {xm.tok(3): 1}
                               and Counter(hb) - Counter(ha) == {xm.tok(12): 1}):
        return "W1 tail or 3-vs-12 bag difference"
    return None
def audit_pairs(D_arrays, family, n_prefixes=zc.N_D) -> dict:
    a, b, t, y = (D_arrays[f"{family}_{s}"] for s in ("a", "b", "t", "y"))
    cex, n = None, len(a)
    if not n == len(b) == len(t) == len(y) == 3 * n_prefixes:
        cex = {"row": None, "detail": f"{n} pairs for {n_prefixes} prefixes"}
    pre = {}
    for r in range(n if cex is None else 0):
        why = _audit_row(a[r], b[r], int(t[r]), int(y[r]), family)
        p = xm.parse(_ints(a[r, :int(t[r])]))["prefix"] if why is None else None
        if why is None and (pre.setdefault(r // 3, p) != p or int(y[r]) != r % 3):
            why = "the three cues of a prefix entry are not rows 3i..3i+2"
        if why:
            cex = {"row": r, "detail": why}
            break
    return {"status": _st(cex is None), "counts": {"pairs": n, "prefixes": len(pre)},
            "counterexample": cex}

# ---- A4 exposure check ----
def exposure_matches(hist, t, pool_tokens, sets=None) -> np.ndarray:
    """`sets`: an optional dict caching one row-prefix set per (pool, t) across calls (F-17)."""
    ts, out, sets = _ts(t, len(hist)), np.zeros(len(hist), bool), {} if sets is None else sets
    for L in np.unique(ts):
        key = (id(pool_tokens), int(L))
        if key not in sets:
            sets[key] = {bytes(r[:L]) for r in np.asarray(pool_tokens, np.uint8)}
        rows, idx = sets[key], np.flatnonzero(ts == L)
        out[idx] = [bytes(np.asarray(hist[i, :L], np.uint8)) in rows for i in idx]
    return out
def exposure_report(variant_arrays_by_family, pools) -> dict:
    out, sets = {"matches": {}, "pair_mask": {}, "total": 0}, {}  # sets: built once per (pool, t)
    for F, A in variant_arrays_by_family.items():
        out["matches"][F], out["pair_mask"][F] = {}, {}
        for v in zc.VARIANT_ORDER:
            hit = {m: np.zeros(len(A[f"{v}_{m}"]), bool) for m in "ab"}
            for m, pool in ((m, p) for m in "ab" for p in pools.values()):
                hit[m] |= exposure_matches(A[f"{v}_{m}"], A[f"{v}_t"], pool, sets)
            out["matches"][F][v] = {m: int(h.sum()) for m, h in hit.items()}
            out["pair_mask"][F][v] = hit["a"] | hit["b"]
            out["total"] += int(hit["a"].sum() + hit["b"].sum())
    return out

# ---- B1 / K4 comparison ----
def _rel(g, s) -> float:
    g, s = (math.nan if x is None else float(x) for x in (g, s))
    if g == s or (math.isnan(g) and math.isnan(s)):
        return 0.0
    return abs(g - s) / max(abs(g), abs(s)) if math.isfinite(g) and math.isfinite(s) else math.inf
def k4_compare(stored, got) -> dict:
    rel = {}
    for k in K4_KEYS:
        g, s = got[k], stored[k]
        pairs = list(zip(g, s)) if isinstance(s, (list, tuple)) else [(g, s)]
        bad = isinstance(s, (list, tuple)) and len(g) != len(s)
        rel[k] = math.inf if bad else max(_rel(a, b) for a, b in pairs)
    mx, nf = max(rel.values()), bool(got["nonfinite"]) == bool(stored["nonfinite"])
    tier = ("PASS" if nf and mx == 0 else "ENV_DRIFT" if nf and mx <= float(zc.T["k4_rel"])
            else DC)
    return {"tier": tier, "max_rel": mx, "keys": rel, "nonfinite_equal": nf}

# ---- B2 / K5 independent checks ----
def _fcn(row) -> list:
    c = [Fraction(float(x)) for x in row[15:18]]
    return [x / sum(c) for x in c]
def k5_independent(terms, beta_prod, tok_a=None, tok_b=None) -> dict:
    """(a) members rebuilt from content (§20 E-3); exact q*, exact cue normalisation and sums."""
    A = terms["tok_a"] if tok_a is None else tok_a
    B = terms["tok_b"] if tok_b is None else tok_b
    num = den = Fraction(0)
    rows, ts = [], terms["t"]
    try:
        for i, t in enumerate(ts):
            hs, ps = (_ints(A[i, :t]), _ints(B[i, :t])), (terms["p_a"][i], terms["p_b"][i])
            mem, pr = [zc.member_of(h) for h in hs], [xm.parse(h) for h in hs]
            if sorted(mem) != ["a", "b"] or (pr[0]["prefix"], pr[0]["y"]) != (pr[1]["prefix"],
                                                                            pr[1]["y"]):
                return {"status": DC, "row": i, "detail": "members not rebuilt from content"}
            (hx, px), (hy, py) = sorted(zip(hs, ps), key=lambda z: zc.member_of(z[0]))
            qx_, qy_ = (zc._cn(sp.q_exact("NA", h, len(h))) for h in (hx, hy))
            cx, cy = _fcn(px), _fcn(py)
            dp, dq = [a - b for a, b in zip(cx, cy)], [a - b for a, b in zip(qx_, qy_)]
            num, den = num + sum(a * b for a, b in zip(dp, dq)), den + sum(b * b for b in dq)
            rows += [(i, 1, qx_, cx), (i, 1, qy_, cy)]
    except (ValueError, ZeroDivisionError) as e:
        return {"status": DC, "detail": f"not computable: {e}"}
    be = num / den if den else None
    xb, d = xe.beta(rows), abs(float(be) - beta_prod) if be is not None else math.inf
    ok, drift = xb == be and d <= float(zc.T["k5a_ok"]), xb == be and d <= float(zc.T["k5a_drift"])
    return {"status": PASS if ok else "NUMERIC_DRIFT" if drift else DC, "beta_exact": str(be),
            "beta_prod": beta_prod, "abs_diff": d, "xe_beta_equal": xb == be}
def k5_swap(terms) -> dict:
    joint = se.pair_terms(terms["p_b"], terms["p_a"], terms["q_b"], terms["q_a"])[0]
    pred_only = se.pair_terms(terms["p_b"], terms["p_a"], terms["q_a"], terms["q_b"])[0]
    j, p = np.array_equal(joint, terms["num"]), np.array_equal(pred_only, -terms["num"])
    return {"status": _st(j and p), "joint_unchanged": j, "predictor_only_negated": p}
def _maxdiff(a, b) -> float: return float(np.abs(np.asarray(a) - np.asarray(b)).max(initial=0))
def k5_padding(pred, tok, t) -> dict:
    tok, ts = np.asarray(tok), _ts(t, len(tok))
    alt = tok.copy()
    for i, k in enumerate(ts):
        alt[i, k:] = int(zc.T["k5_padding_token"])
    d = _maxdiff(pred(tok, ts), pred(alt, ts))
    return {"status": _st(d <= float(zc.T["padding_abs"])), "max_abs": d}
def k5_batch(pred, tok, t) -> dict:
    tok, ts = np.asarray(tok), _ts(t, len(tok))
    one = np.concatenate([pred(tok[i:i + 1], ts[i:i + 1]) for i in range(len(tok))])
    d = _maxdiff(one, pred(tok, ts))
    return {"status": _st(d <= float(zc.T["repeat_abs"])), "max_abs": d}
def k5_readout_index(pred, arrays, family) -> dict:
    t = np.asarray(arrays[f"{family}_t"], np.int64)
    tok = np.concatenate([arrays[f"{family}_a"], arrays[f"{family}_b"]])
    t2 = np.concatenate([t, t])
    mt, mt1 = (float(np.median(se.cue_mass(pred(tok, x)))) for x in (t2, t2 - 1))
    q0 = all(sum(sp.q_exact("NA", r, int(k))[15:18]) == 0 for r, k in zip(tok, t2 - 1))
    lo, hi = (float(x) for x in zc.T["cue_mass_t"])
    ok = mt1 <= float(zc.T["cue_mass_tm1_max"]) and q0 and (family != "W2" or lo <= mt <= hi)
    return {"status": _st(ok), "median_t": mt, "median_t_minus_1": mt1, "qstar_tm1_zero": q0}
def k5_two_loads(pred1, pred2, tok, t) -> dict:
    d = _maxdiff(pred1(tok, t), pred2(tok, t))
    return {"status": _st(d <= float(zc.T["repeat_abs"])), "max_abs": d}
def k5_scalar_vector(pred, tok, t) -> dict:
    tok, ts = np.asarray(tok), _ts(t, len(tok))
    one = np.concatenate([pred(tok[i:i + 1], int(ts[i])) for i in range(len(tok))])
    d = _maxdiff(one, pred(tok, ts))
    return {"status": _st(d <= float(zc.T["repeat_abs"])), "max_abs": d}
def _rows(terms, idx) -> dict:
    n = len(terms["num"])
    return {k: (np.asarray(v)[idx] if isinstance(v, np.ndarray) and len(v) == n else v)
            for k, v in terms.items()}
def k5_permutation(terms, gen=None) -> dict:
    perm = (gen or zc.stream("perm_K5i")).permutation(len(terms["num"]))
    base, per, back = (zc.pair_stats(x) for x in (terms, _rows(terms, perm),
                                                   _rows(_rows(terms, perm), np.argsort(perm))))
    ok = all(base[k] == per[k] == back[k] for k in ("beta", "rho", "beta_y"))
    return {"status": _st(ok), "beta": base["beta"], "beta_permuted": per["beta"]}
def k5_bos(model, tok, t) -> dict:
    import torch
    m, tok = getattr(model, "model", model), np.asarray(tok)
    ts = _ts(t, len(tok))
    x = np.concatenate([np.full((len(tok), 1), 18, np.int64), tok[:, :32].astype(np.int64)], 1)
    with torch.no_grad():
        lg = m(torch.from_numpy(np.ascontiguousarray(x))).logits
        p = torch.softmax(lg[torch.arange(len(tok)), torch.from_numpy(ts)], -1).numpy()
    d = _maxdiff(p, se.ModelPredictor._run(m, tok, ts))
    return {"status": _st(d <= float(zc.T["repeat_abs"])), "max_abs": d}
def structural_subset(t, y) -> np.ndarray:
    first = {}
    for i, key in enumerate(zip(np.asarray(t).tolist(), np.asarray(y).tolist())):
        first.setdefault(key, i)
    return np.array(sorted(first.values()), np.int64)

# ---- B3 decomposition, B4 profile, D2, D3 ----
_LEVELS = (0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)
def _q(x, lv=_LEVELS) -> list: return [float(np.quantile(x, q)) for q in lv] if len(x) else []
def _diffs(terms) -> tuple:
    dp = se.cue_normalise(terms["p_a"]) - se.cue_normalise(terms["p_b"])
    return dp, se.cue_normalise(terms["q_a"]) - se.cue_normalise(terms["q_b"])
def decompose(terms) -> dict:
    dp, dq = _diffs(terms)
    st, eye, n = zc.pair_stats(terms), np.eye(3), len(dp)
    na, nb = dq.argmax(1), dq.argmin(1)
    e1 = (eye[na] - eye[nb]) / math.sqrt(2)
    e2 = (2 * eye[3 - na - nb] - eye[na] - eye[nb]) / math.sqrt(6)
    c1, c2, cl = (dp * e1).sum(1), (dp * e2).sum(1), np.asarray(terms["cluster"])
    b, rho, y = st["beta"], st["rho"], np.asarray(terms["y"])
    tot = math.fsum((dp * dp).sum(1))
    return {"beta": b, "rho": rho, "cos_agg": b / math.sqrt(rho) if rho > 0 else math.nan,
            "beta2_over_rho": b * b / rho if rho > 0 else math.nan,
            "phi1": math.fsum(c1 * c1) / tot if tot else math.nan,
            "e1_mean": float(c1.mean()), "e1_sd": float(c1.std(ddof=1)) if n > 1 else math.nan,
            "e2_mean": float(c2.mean()), "e2_sd": float(c2.std(ddof=1)) if n > 1 else math.nan,
            "frac_pos": float(((dp * dq).sum(1) > 0).mean()),
            "diff_quantiles": {"full": _q(np.abs(terms["p_a"] - terms["p_b"]).max(1)),
                               "cue": _q(np.abs(dp).max(1))},
            "num_by_prefix": zc.cluster_sums(terms["num"], cl, int(cl.max()) + 1),
            "num_by_cue": [math.fsum(terms["num"][y == z]) for z in range(3)]}
def zc_profile(terms, tables, arm) -> dict:
    y, out = np.asarray(terms["y"]), {}
    G = (xm.S3_E, xm.S3_A) if arm == "AB" else (xm.S3_E, xm.S3_C, xm.S3_C2)
    for m in "ab":
        c, rows = se.cue_normalise(terms[f"p_{m}"]), np.arange(len(y))
        sh = [c[rows, [g[int(k)] for k in y]] for g in G]
        if arm == "AB":  # shares on y, a·y and the remaining cue (C-24)
            sh.append(1 - sh[0] - np.where(np.array([xm.S3_A[int(k)] for k in y]) == y, 0, sh[1]))
        codes = se.qstar(arm, terms[f"tok_{m}"], terms["t"])[1]
        reg = se.score(codes, se.quantise(terms[f"p_{m}"]), tables)
        out[m] = {"shares": [float(np.mean(s)) for s in sh], "regret": math.fsum(reg) / len(reg)}
    return out
def crosses(x, y, bar=0.1, band=1e-9) -> bool:
    ax, ay, lo, hi = abs(x), abs(y), bar - band, bar + band
    return (ax < lo and ay > hi) or (ay < lo and ax > hi)
def _sens(b, alt) -> bool: return abs(b - alt) >= float(zc.T["material_change"]) and crosses(b, alt)
def d2_decompose(terms) -> dict:
    pa, pb = np.asarray(terms["p_a"])[:, 15:18], np.asarray(terms["p_b"])[:, 15:18]
    ma, mb = pa.sum(1), pb.sum(1)
    mbar, d = (ma + mb) / 2, _diffs(terms)[1]
    t1 = (pa - pb) / mbar[:, None]
    t2 = -((ma - mb) / (2 * mbar))[:, None] * (pa / ma[:, None] + pb / mb[:, None])
    c1, c2, den = (t1 * d).sum(1), (t2 * d).sum(1), math.fsum((d * d).sum(1))
    b, bf = se.beta_fsum(terms["num"], terms["den"]), math.fsum((5 * (pa - pb) * d).sum(1)) / den
    m = np.concatenate([ma, mb])
    return {"identity_max_abs": float(np.abs(c1 + c2 - terms["num"]).max(initial=0)),
            "contrib_norm": math.fsum(c1), "contrib_mass": math.fsum(c2), "beta": b,
            "beta_fixed": bf, "min": float(m.min()), "median": float(np.median(m)),
            **dict(zip(("p01", "p05", "p10"), _q(m, (0.01, 0.05, 0.1)))),
            "frac_below_0.10": float((m < 0.1).mean()), "readout_amplified": _sens(b, bf)}
def _wbeta(num, den, w) -> float: return math.fsum(w * num) / math.fsum(w * den)
def weighting_summaries(terms, prefixes, named_mask) -> dict:
    num, den = np.asarray(terms["num"]), np.asarray(terms["den"])
    cl, nm = np.asarray(terms["cluster"]), np.asarray(named_mask, bool)
    s, L = [tuple(prefixes[i]) for i in cl], np.array([len(prefixes[i]) for i in cl])
    grp, lc, b = Counter(s), Counter(L.tolist()), se.beta_fsum(num, den)
    nat = np.flatnonzero(~nm)
    def sub(mask): return se.beta_fsum(num[mask], den[mask]) if mask.any() else math.nan
    keys = sorted(grp)
    loo = [sub(np.array([x != k for x in s])) for k in keys]
    absn = np.abs(num)
    ps = np.sort([math.fsum(absn[cl == i]) for i in range(len(prefixes))])[::-1]
    gs = np.sort([math.fsum(absn[[x == k for x in s]]) for k in keys])[::-1]
    bd = _wbeta(num, den, np.array([1 / grp[x] for x in s]))
    bl = _wbeta(num, den, np.array([1 / lc[x] for x in L.tolist()]))
    return {"beta": b, "named": sub(nm[cl]), "natural": sub(~nm[cl]),
            "by_length": {str(k): sub(L == k) for k in sorted(lc)},
            "by_bin": {f"{a}-{z}": sub((L >= a) & (L <= z)) for a, z in ((1, 4), (5, 9), (10, 14))},
            "blocks": [sub(np.isin(cl, nat[256 * k:256 * (k + 1)])) for k in range(4)],
            "beta_distinct": bd, "beta_length": bl,
            "loo": {"min": min(loo), "max": max(loo), "argmin": list(keys[int(np.argmin(loo))]),
                    "argmax": list(keys[int(np.argmax(loo))])},
            "top5_prefix_share": math.fsum(ps[:math.ceil(0.05 * len(ps))]) / math.fsum(ps),
            "top10_group_share": math.fsum(gs[:math.ceil(0.10 * len(gs))]) / math.fsum(gs),
            "multiplicities": {str(k): v for k, v in sorted(Counter(
                Counter(prefixes[i] for i in range(len(prefixes))).values()).items())},
            "multiplicity_sensitive": _sens(b, bd), "length_weight_sensitive": _sens(b, bl)}

# ---- B6, B7, B10 and the descriptive tier ----
def similarity(dp) -> dict:
    ms = list(dp)
    X = np.stack([np.asarray(dp[m], np.float64).ravel() for m in ms])
    nrm = np.sqrt((X * X).sum(1))
    with np.errstate(divide="ignore", invalid="ignore"):
        cos = (X @ X.T) / np.outer(nrm, nrm)
    return {"models": ms, "cos": cos.tolist()}
def control_families(stats_by_family) -> dict:
    """{"terms": {family: pair_arrays output}, "designed": designed_stats dict} -> B7 values."""
    T, ds = stats_by_family["terms"], stats_by_family.get("designed", {})
    dq2 = math.fsum((_diffs(T["W2"])[1] ** 2).sum(1)) / len(T["W2"]["num"])
    rho = {c: math.fsum((_diffs(T[c])[0] ** 2).sum(1)) / len(T[c]["num"]) / dq2
           for c in ("C1", "C2", "C3", "C4") if c in T}
    w1 = zc.pair_stats(T["W1"]) if "W1" in T else {}
    return {"rho_C": rho, "beta_W1_y": w1.get("beta_y"), "rho_W1": w1.get("rho"),
            **{k: ds.get(k) for k in ("beta_W3", "beta_W3_bal", "beta_W3p")}}
def float32_replay(beta32, beta64) -> dict:
    d = abs(beta32 - beta64)
    return {"diff": d, "precision_sensitive": d > float(zc.T["precision_sensitive"])}
_FLAGS = ("READOUT_AMPLIFIED", "MULTIPLICITY_SENSITIVE", "LENGTH_WEIGHT_SENSITIVE",
          "PRECISION_SENSITIVE")
def descriptive_tier(model, family, k4_tier, k1_ok, k5_ok, max_pair_diff, flags, betas) -> dict:
    on = (k4_tier in ("PASS", "ENV_DRIFT") and k1_ok and k5_ok
          and max_pair_diff > float(zc.T["census_pair_diff"]))
    q = [f"{f}({model}, {family})" for f in _FLAGS if flags.get(f)] + ["ORIGIN_UNRESOLVED"]
    q += ["BAG_UNMATCHED"] * (family == "W1") + [
        f"FAMILY_PATTERN(beta_W1={betas['W1']:.4f}, beta_W2={betas['W2']:.4f})"]
    return {"model": model, "family": family, "trained_control": model[:2] in ("AB", "ZC"),
            "tier": f"CENSUS_NON_INVARIANT({model}, {family})" if on else None, "qualifiers": q}
