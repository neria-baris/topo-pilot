"""hwsd_statements: notation, onsets, ORDER and statements D1-D6 (API.md section 7).

Pure logic over per-model sequences of checkpoint rows; no file access.
"""
from __future__ import annotations  # noqa: I001

from fractions import Fraction

import hwsd_config as dc  # noqa: F401  (puts the reused tool folders on sys.path)
import k4b_stats  # noqa: E402

M = Fraction(1, 100)
STATEMENTS = ("D1", "D2", "D3", "D4", "D5", "D6")


def est(row) -> bool:
    return row["status"] in ("SCORED", "SCORED_UNVALIDATED")


def ok(row) -> bool:
    return row["status"] == "SCORED"


def fr(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(float(x))


def sigma(row) -> str:
    if not ok(row):
        return "NA"
    return k4b_stats.model_status(row["L"], row["U"], row["F_minus"], row["F_plus"])["status"]


def above_s(row) -> bool:
    return bool(est(row) and fr(row["L_S"]) - fr(row["F_minus"]) > M)


def below_s(row) -> bool:
    return bool(ok(row) and fr(row["U_S"]) + fr(row["F_plus"]) < M)


def above_s_ok(row) -> bool:
    return bool(ok(row) and fr(row["L_S"]) - fr(row["F_minus"]) > M)


def _first(rows, pred, start=1):
    for i, r in enumerate(rows):
        if i + 1 >= start and pred(i + 1, r):
            return i + 1
    return None


def onsets(rows) -> dict:
    n = len(rows)
    valid = [bool(r.get("valid")) for r in rows]
    k_star = None
    for k in range(n, 0, -1):
        if valid[k - 1]:
            k_star = k
        else:
            break
    if k_star is not None and not valid[-1]:
        k_star = None
    return {
        "k_C": _first(rows, lambda k, r: valid[k - 1]),
        "k_C_star": k_star,
        "k_C_plus": _first(rows, lambda k, r: valid[k - 1] and not valid[k - 2], 2),
        "k_L": _first(rows, lambda k, r: bool(r.get("learn_pass"))),
        "k_P": _first(rows, lambda k, r: r.get("B2_L_zS") is not None and r["B2_L_zS"] > 0),
        "k_B": _first(rows, lambda k, r: sigma(r) == "SUPPORT"),
        "k_B_S": _first(rows, lambda k, r: above_s(r)),
    }


def n_pre(rows) -> int:
    kc = onsets(rows)["k_C"]
    lim = len(rows) + 1 if kc is None else kc
    return sum(1 for i, r in enumerate(rows) if i + 1 < lim and est(r))


def pre_chart_max(rows):
    kc = onsets(rows)["k_C"]
    lim = len(rows) + 1 if kc is None else kc
    vals = [fr(r["U_S"]) + fr(r["F_plus"]) for i, r in enumerate(rows) if i + 1 < lim and est(r)]
    return str(max(vals)) if vals else None


def order(rows, anchor, A=None) -> dict:
    on = onsets(rows)
    if A is None:
        A = on["k_C"] if anchor == "chart" else on["k_L"]
    K = len(rows)

    def res(cat):
        return {"anchor": anchor, "A": A, "category": cat}

    if A is None:
        return res("NO_CHART" if anchor == "chart" else "NO_LEARNING")
    if anchor == "chart" and A == 1:
        return res("CHART_AT_INIT")
    if any(above_s(rows[k - 1]) for k in range(1, A)):
        return res("BEFORE")
    sa, sk = sigma(rows[A - 1]), sigma(rows[K - 1])
    if sa == "NA":
        if anchor == "learning" and (on["k_C"] is None or on["k_C"] > A):
            return res("LEARNING_BEFORE_CHART")
        return res("UNCERTIFIED_AT_ANCHOR")
    if sa == "SUPPORT":
        return res("WITH")
    if sa == "EXCLUDE" and sk == "SUPPORT":
        return res("AFTER")
    if sk == "EXCLUDE":
        return res("NEVER")
    if sk == "NA":
        return res("FINAL_NA")
    return res("UNRESOLVED")


def _rd(reading, reason=None, qualifier=None) -> dict:
    return {"reading": reading, "reason": reason, "qualifier": qualifier}


def _ne(reason):
    return _rd("NOT_EVALUABLE", reason)


def d1(rows) -> dict:
    s = sigma(rows[-1])
    if s == "SUPPORT":
        return _rd("TRUE")
    if s == "EXCLUDE":
        return _rd("FALSE")
    return _ne("FINAL_NA" if s == "NA" else "UNRESOLVED")


def d2(rows) -> dict:
    on = onsets(rows)
    kc = on["k_C"]
    if kc == 1:
        return _ne("CHART_AT_INIT")
    if kc is None:
        return _ne("NO_CHART")
    if order(rows, "chart")["category"] == "BEFORE":
        return _rd("FALSE", "BEFORE")
    if sigma(rows[-1]) != "SUPPORT":
        return _ne("FINAL_NOT_SUPPORT")
    if n_pre(rows) >= 1:
        inf = any(est(r) and fr(r["U_S"]) + fr(r["F_plus"]) < M for r in rows[:kc - 1])
        return _rd("TRUE", None, "INFORMATIVE" if inf else "UNINFORMATIVE")
    return _rd("BY_CONSTRUCTION")


def _by_order(rows, anchor) -> dict:
    c = order(rows, anchor)["category"]
    if c == "AFTER":
        return _rd("TRUE")
    if c in ("WITH", "BEFORE"):
        return _rd("FALSE", c)
    return _ne(c)


def d3(rows) -> dict:
    return _by_order(rows, "chart")


def d4(rows) -> dict:
    return _by_order(rows, "learning")


def d5(rows) -> dict:
    on = onsets(rows)
    kp, kc = on["k_P"], on["k_C"]
    if kp is None:
        return _ne("NO_PREDICTIVE_ONSET")
    if kc is None or kc > kp:
        return _rd("FALSE", "CHART_AFTER_PREDICTIVE_ONSET")
    s = sigma(rows[kp - 1])
    if s == "EXCLUDE":
        return _rd("FALSE", "EXCLUDE_AT_PREDICTIVE_ONSET")
    if s == "SUPPORT":
        return _rd("TRUE")
    if s == "NA":
        return _ne("NA_AT_PREDICTIVE_ONSET")
    return _ne("UNRESOLVED")


def d6(rows) -> dict:
    K = len(rows)
    a = [k for k in range(1, K + 1) if above_s_ok(rows[k - 1])]
    for k1 in a:
        if any(below_s(rows[k2 - 1]) for k2 in range(k1 + 1, K + 1)):
            return _rd("FALSE", "LOSS")
    if any(k1 < K for k1 in a):
        return _rd("TRUE")
    return _ne("NO_STRONG_CROSSING")


_FN = {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5, "D6": d6}


def aggregate(statement, per_model) -> dict:
    rd = {j: v["reading"] for j, v in per_model.items()}
    vals = list(rd.values())
    reasons = {}

    def out(reading):
        return {"statement": statement, "reading": reading, "reasons": reasons,
                "per_model": per_model}

    if "FALSE" in vals:
        return out("FALSE")
    if statement == "D2":
        good = all(v in ("TRUE", "BY_CONSTRUCTION") for v in vals)
        informative = any(v["reading"] == "TRUE" and v["qualifier"] == "INFORMATIVE"
                          for v in per_model.values())
        if good and informative:
            return out("TRUE")
    elif all(v == "TRUE" for v in vals):
        return out("TRUE")
    for j, v in per_model.items():
        if v["reading"] == "NOT_EVALUABLE":
            reasons.setdefault(v["reason"], []).append(j)
    if statement == "D2" and vals:
        if all(v == "BY_CONSTRUCTION" for v in vals):
            reasons["BY_CONSTRUCTION"] = list(per_model)
        elif all(v in ("TRUE", "BY_CONSTRUCTION") for v in vals):
            reasons["UNINFORMATIVE_PRE_CHART"] = list(per_model)
    return out("NOT_EVALUABLE")


def onset_order_line(table) -> dict:
    def c(a, b):
        if a is None or b is None:
            return "undefined"
        return "<" if a < b else ("=" if a == b else ">")

    out = {}
    for j, rows in table.items():
        o = onsets(rows)
        out[j] = {"k_L_vs_k_C": c(o["k_L"], o["k_C"]), "k_P_vs_k_C": c(o["k_P"], o["k_C"])}
    return out


def diagnostics(table) -> dict:
    out = {}
    for j, rows in table.items():
        K = len(rows)
        on = onsets(rows)

        def step(k):
            return rows[k - 1].get("step")

        mc = [step(k) for k in range(1, K + 1)
              if rows[k - 1].get("L") is not None
              and (rows[k - 1]["L_S"] > rows[k - 1]["L"] or rows[k - 1]["U_S"] < rows[k - 1]["U"])]
        pos = [step(k) for k in range(1, K + 1)
               if est(rows[k - 1]) and fr(rows[k - 1]["L"]) - fr(rows[k - 1]["F_minus"]) > 0]
        loss = [[k1, k2] for k1 in range(1, K + 1) for k2 in range(k1 + 1, K + 1)
                if above_s(rows[k1 - 1]) and rows[k1 - 1]["status"] == "SCORED_UNVALIDATED"
                and below_s(rows[k2 - 1])]
        d = {"mc": mc, "positive": pos, "est_loss": loss, "chart_at_init": None}
        if on["k_C"] == 1:
            kp = on["k_C_plus"]
            d["chart_at_init"] = {
                "sigma_step0": sigma(rows[0]),
                "order_at_k_C_plus": order(rows, "chart", A=kp)["category"] if kp else "NO_CHART"}
        out[j] = d
    return out


def evaluate(table, headroom_ok=True, resource_ok=True) -> dict:
    models = list(table)
    per = {s: {j: _FN[s](table[j]) for j in models} for s in STATEMENTS}
    stm = {s: aggregate(s, per[s]) for s in STATEMENTS}
    why = None if (headroom_ok and resource_ok) else ("RESOURCE" if not resource_ok else "HEADROOM")
    if why:
        for s in STATEMENTS:
            stm[s] = {"statement": s, "reading": "NOT_EVALUABLE", "reasons": {why: list(models)},
                      "per_model": per[s]}
    return {
        "onsets": {j: onsets(table[j]) for j in models},
        "n_pre": {j: n_pre(table[j]) for j in models},
        "pre_chart_max": {j: pre_chart_max(table[j]) for j in models},
        "order": {j: {"chart": order(table[j], "chart"), "learning": order(table[j], "learning")}
                  for j in models},
        "statements": stm,
        "onset_order_line": onset_order_line(table),
        "diagnostics": diagnostics(table),
    }
