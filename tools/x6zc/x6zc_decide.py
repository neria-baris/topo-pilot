"""X6ZC decision: the paired cluster bootstrap, ratio intervals, B9 sizing, the §9 decision,
licences, qualifiers and the reuse verdict (X6ZC-DESIGN-v1 §5, §7-§9; API.md §8-§9, §20 C-52).
Re-exported by x6zc_core. No I/O."""
# fmt: off

from __future__ import annotations

import math
from fractions import Fraction

# isort: off
from x6zc_const import (CONTRACT, KC, NA_DIR, VARIANT_ORDER,  # noqa: E402
    CELLS, CELL_ORDER, T, N_FLOOR, N_D, N_LADDER, _fl)  # noqa: E402
# isort: on

# isort: split
import numpy as np  # noqa: E402
import x6s1_stats as ss  # noqa: E402


# ---- paired cluster bootstrap, ratios and B9 sizing (API §8) ----
def cluster_sums(values, cluster, P) -> np.ndarray:
    v, c = np.asarray(values, np.float64), np.asarray(cluster, np.int64)
    o = np.argsort(c, kind="stable")
    b = np.searchsorted(c[o], np.arange(P + 1))
    return np.array([math.fsum(v[o[b[i]:b[i + 1]]]) for i in range(P)], np.float64)
def paired_cluster_boot(num, den, B, gen) -> dict:
    keys = list(num)
    N, D = (np.stack([np.asarray(x[k], np.float64) for k in keys]) for x in (num, den))
    out = np.empty((len(keys), B), np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        for b in range(B):
            idx = gen.integers(0, N.shape[1], size=N.shape[1])  # one index array per draw
            G, H = N[:, idx], D[:, idx]  # each row summed as a 1-D array: the boot_beta sum
            out[:, b] = np.array([g.sum() for g in G]) / np.array([h.sum() for h in H])
    return {k: out[i] for i, k in enumerate(keys)}
def interval(draws, q) -> tuple:
    d = np.asarray(draws, np.float64)
    if not np.isfinite(d).all():
        raise ValueError("non-finite bootstrap draws: no interval (C-21)")
    return ss.quantile(d, float(q[0])), ss.quantile(d, float(q[1]))
def ratio_interval(draws_v, draws_pp, sign, q) -> dict:
    v, pp = np.asarray(draws_v, np.float64), np.asarray(draws_pp, np.float64)
    ok = sign * pp > 0
    nd = int(ok.sum())
    lo, hi = interval(v[ok] / pp[ok], q) if nd else (None, None)
    return {"lo": lo, "hi": hi, "n_defined": nd, "undefined": len(pp) - nd,
            "undefined_frac": (len(pp) - nd) / len(pp), "n_draws": len(pp)}
def _ratio(a, b): return a / b if b else None
def cell_statistics(point, draws, cell) -> dict:
    c, (lo_b, hi_b) = CELLS[cell], T["r_band"]
    m, F, s = c["model"], c["family"], c["sign"]
    pp, dpp = point[(m, F, "PP")], np.asarray(draws[f"{m}|{F}|PP|beta"], np.float64)
    out = {"model": m, "family": F, "sign": s, "b": s * pp, "beta_pp": pp, "r": {}, "r_w1_p": None}
    out["b_lo"], out["b_hi"] = interval(s * dpp, c["b_q"])
    for v in VARIANT_ORDER[1:]:
        ri = ratio_interval(draws[f"{m}|{F}|{v}|beta"], dpp, s, c["r_q"])
        out["r"][v] = {"point": _ratio(point[(m, F, v)], pp), "lo": ri["lo"], "hi": ri["hi"],
                       "n_defined": ri["n_defined"]}
        out.update({k: ri[k] for k in ("undefined", "undefined_frac", "n_draws")})
    sb = interval(0.5 * (dpp + np.asarray(draws[f"{m}|{F}|MM|beta"])), T["beta_sb_q"])
    out["beta_sb"] = {"point": 0.5 * (pp + point[(m, F, "MM")]), "lo": sb[0], "hi": sb[1]}
    if cell == "P" and (m, "W1", "PP") in point and f"{m}|W1|PP|beta" in draws:
        ri = ratio_interval(draws[f"{m}|W1|PP|beta"], dpp, s, T["r_w1_p_q"])
        lab = (None if ri["lo"] is None or Fraction(ri["undefined"], ri["n_draws"])
               > T["undefined_max"] else "W2_ONLY" if ri["hi"] < _fl(lo_b) else
               "NA_BOTH_FAMILIES" if _fl(lo_b) < ri["lo"] and ri["hi"] < _fl(hi_b) else None)
        out["r_w1_p"] = {"point": _ratio(point[(m, "W1", "PP")], pp), "lo": ri["lo"],
                         "hi": ri["hi"], "undefined_frac": ri["undefined_frac"], "label": lab}
    return out
def halfwidth(n, se_d, beta_d, z) -> float:
    return (z * math.sqrt(2) * se_d * math.sqrt(N_D / n)
            / max(abs(beta_d) - 2 * se_d, _fl(T["se_floor"])))
def choose_n(n_avail, se) -> dict:
    out = {"n": n_avail, "status": "NOT_ENOUGH_DATA", "candidates": [], "h": {},
           "underpowered": dict.fromkeys(CELL_ORDER, False),
           "low_feasibility": list(KC["feasibility_ratio"]["low_feasibility"])}
    if n_avail < N_FLOOR:
        return out
    cand, ht = sorted({n for n in (*N_LADDER, n_avail) if N_FLOOR <= n <= n_avail}), _fl(
        T["h_target"])
    h = {c: {str(n): halfwidth(n, se[c], CELLS[c]["beta_D"], CELLS[c]["z"]) for n in cand}
         for c in CELL_ORDER}
    ok = [n for n in cand if h["P"][str(n)] <= ht]
    n = ok[0] if ok else n_avail
    out.update(n=n, status="OK" if ok else "UNDERPOWERED", candidates=cand, h=h)
    out["underpowered"] = {"P": not ok, **{c: h[c][str(n)] > ht for c in CELL_ORDER[1:]}}
    return out

# ---- decision (§9.1), licences, qualifiers, reuse verdict (API §9) ----
def _ascii(rule) -> str: return rule.replace("′", "'")
def _lt(x, bar) -> bool: return x is not None and x < _fl(bar)
def _gt(x, bar) -> bool: return x is not None and x > _fl(bar)
def _unstable(s) -> bool:  # counts compared as integers when present (§20 E-1)
    if "undefined" in s and "n_draws" in s:
        return Fraction(s["undefined"], s["n_draws"]) > T["undefined_max"]
    return s["undefined_frac"] > _fl(T["undefined_max"])
def _cell_rule(ev, c) -> tuple:
    F, s, b9, (lo_b, hi_b), bm = (CELLS[c]["family"], ev["cells"].get(c), ev["b9"], T["r_band"],
                                  T["b_margin"])
    pre = ("R4a" if b9["status"] == "NOT_ENOUGH_DATA" else "R4b" if b9["underpowered"].get(c)
           else "R5" if not ev["k6"][F] else None)
    if pre:
        return pre, None
    if s is None:
        raise ValueError(f"cell {c}: no statistics")
    r = s["r"]
    if _lt(s["b_hi"], bm) and s["b_lo"] <= 0:
        return "R6", None
    if _lt(s["b"], bm) or s["b_lo"] <= _fl(T["lo_margin"]):
        return "R7", "positive" if s["b_lo"] > 0 and _lt(s["b"], bm) else "ambiguous"
    rule = ("R7b" if _unstable(s) else "R8" if _lt(r["MM"]["hi"], 0) else
            "R8b" if any(_lt(r[v]["hi"], lo_b) or _gt(r[v]["lo"], hi_b) for v in r) else
            "R10" if not all(_gt(r[v]["lo"], lo_b) and _lt(r[v]["hi"], hi_b) for v in r) else
            "R9" if ev["f1"][F]["passed"] else "R9′")
    return rule, None
def decide_x6zc(ev) -> dict:
    out = {"global_rule": None, "global_outcome": None, "cells": {}, "headline": None,
           "defect_elsewhere": [r["id"] for r in ev.get("rulings", []) if r["cause_identified"]
                                and not r["affects_beta"] and not r.get("setup")]}
    g = "G-R0" if ev["k0"] == "FAIL" else "G-R1" if ev.get("incomplete") else None
    if g is None:
        rul, failed = {}, [k for k, s in ev["checks"].items() if s in ("FAIL", "DEFECT_CANDIDATE")]
        for r in ev.get("rulings", []):
            rul.setdefault(r["check"], []).append(r)
        if any(k not in rul for k in failed):
            raise ValueError(f"failed checks without a ruling: {sorted(set(failed) - set(rul))}")
        rs = [r for k in failed for r in rul[k]]
        g = ("G-R2" if any(r["cause_identified"] and r["affects_beta"] for r in rs) else
             "G-R2′" if any(not r["cause_identified"] for r in rs) else
             "G-R3" if ev["k1"] == "FAIL" and ev["a2_k5_pass"] else None)
    if g is not None:
        o = CONTRACT["outcomes"]["global"][_ascii(g)]
        cell = {"rule": g, "outcome": o, "licence_case": None, "descriptive": False}
        return {**out, "global_rule": g, "global_outcome": o, "headline": o,
                "cells": {c: dict(cell) for c in CELL_ORDER}}
    for c in CELL_ORDER:
        rule, case = _cell_rule(ev, c)
        o = CONTRACT["outcomes"]["cell"][_ascii(rule)]["P" if c == "P" else "S"].format(
            mechanisms=", ".join(ev["f1"][CELLS[c]["family"]]["failed"]))
        out["cells"][c] = {"rule": rule, "outcome": o, "licence_case": case,
                           "descriptive": rule in ("R4a", "R4b")}
    return {**out, "headline": out["cells"]["P"]["outcome"]}
def _lkey(outcome, table, case=None) -> str:
    if outcome == "UNEXPLAINED/WEAK_REPLICATION":
        return f"{outcome}:{case or 'ambiguous'}"
    return outcome if outcome in table else "UNEXPLAINED/*"
def licence(outcome, values, case=None) -> str:
    L = CONTRACT["licences"]
    if outcome in ("STOP_REPLAN", "INVALID"):
        return ""
    txt = L[_lkey(outcome, L, case)].format(**{**values, "outcome": outcome})
    w1 = values["cell"] in ("S3", "S4") if "cell" in values else values.get("family") == "W1"
    return txt + L[NA_DIR + ":W1_suffix"] if outcome == NA_DIR and w1 else txt
def not_licensed(outcome, case=None) -> str:
    return CONTRACT["not_licensed"][_lkey(outcome, CONTRACT["not_licensed"], case)]
def qualifiers(ev, decision, census) -> dict:
    cen, out = census or {}, {}
    for c in CELL_ORDER:
        d, m, F = decision["cells"][c], CELLS[c]["model"], CELLS[c]["family"]
        q, s = [], (ev.get("cells") or {}).get(c) or {}
        if d["outcome"].startswith("ZC_NOT_COMMUTATIVE/"):
            q += ["ORIGIN_UNRESOLVED"] + list(cen.get("qualifiers", {}).get(f"{m}|{F}", []))
            q += [s["r_w1_p"]["label"]] if c == "P" and (s.get("r_w1_p") or {}).get("label") else []
            for line, name in (("A4", "SENSITIVITY_A4"), ("DPREFIX", "SENSITIVITY_D_PREFIX")):
                alt = cen.get("sensitivity", {}).get(line, {}).get(c)
                q += [f"{name}({alt})"] if alt is not None and alt != d["outcome"] else []
        q += [f"LOW_FEASIBILITY({c})"] * (c in ev["b9"].get("low_feasibility", []))
        q += [f"UNDERPOWERED({c})"] * bool(ev["b9"]["underpowered"].get(c))
        q += ["ENV_DRIFT"] * (ev["checks"].get("K4") == "ENV_DRIFT")
        q += [f"NUMERIC_DRIFT({m}, {F})"] * (f"{m}|{F}" in cen.get("numeric_drift", []))
        q += [f"DEFECT_ELSEWHERE({i})" for i in decision["defect_elsewhere"]]
        out[c] = q + ["DESCRIPTIVE"] * bool(d["descriptive"])
    return out
def reuse_verdict(ev, decision) -> dict:
    R, g, cells, h = (CONTRACT["reuse"], decision["global_outcome"], decision["cells"],
                      decision["headline"])
    a1 = ("NOT_FIT" if g in ("DEFECT_FOUND", "ESTIMATOR_ARTIFACT/NON_INVARIANT") else
          "UNDETERMINED" if g in ("UNEXPLAINED/IRREPRODUCIBLE", "INVALID", "STOP_REPLAN") else
          "VALID")
    if a1 != "VALID":
        return {"axis1": a1, "axis2": "NOT_ASSESSED", "amendments": [], "amendment_1_mark": None,
                "statement": None}
    a2, bo = ("UNDETERMINED" if cells["P"]["outcome"] == NA_DIR else "FIT_WITH_AMENDMENT",
              R["by_outcome"])
    am = {a for c in CELL_ORDER for a in bo.get(cells[c]["outcome"], bo["UNEXPLAINED/*"])}
    am |= {2, 3} if a2 == "UNDETERMINED" else set()
    gen = h.startswith("UNEXPLAINED/") and h not in ("UNEXPLAINED/NOT_NA_INVARIANT",
                                                     "UNEXPLAINED/WEAK_REPLICATION")
    return {"axis1": a1, "axis2": a2, "amendments": sorted(am), "statement": R["statement"],
            "amendment_1_mark": R["amendment_1_inconclusive_mark"] if 1 in am and gen else None}
