"""X6ZC pipeline: the pure Stage-C functions shared by Stage C, the sensitivity lines and the dry
run, the licence values, decide_report and the report schema (API.md §11.4, §11.6, §20 C-52)."""
# fmt: off

from __future__ import annotations

import math
import re

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
import numpy as np  # noqa: E402
import x6s1_eval as se  # noqa: E402

C, X = zc.CONTRACT, zc.CONTRACT["x6s1_store"]
FAM, VO, CO = zc.FAMILIES, zc.VARIANT_ORDER, zc.CELL_ORDER

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
