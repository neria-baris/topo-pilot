"""Author A (job 0197): an independent reference reading of HWSD-DESIGN-v1 §5 (no hwsd code).

Pure Python: the per-checkpoint notation (§5.1), onsets (§5.2), ORDER (§5.3), D1-D6 (§5.4),
the aggregate rule and the diagnostics, written from the protocol text and API.md §7 only.
Other author-A files compare `hwsd_statements` against these functions and against hand
values. The tests at the bottom check this reference on the protocol's own worked examples
(the KD4 sequences of API.md §17.3), so the oracle itself is pinned to the protocol.
"""

from __future__ import annotations

import random
from fractions import Fraction

M = Fraction(1, 100)
F9 = Fraction(1, 10**9)
STEPS = (0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000)
SC, SU, CU, UC = "SCORED", "SCORED_UNVALIDATED", "CHART_UNAVAILABLE", "UNCERTIFIED"
MASTERS = (620301, 620302, 620303)


def fr(x):
    return x if isinstance(x, Fraction) else Fraction(float(x))


def ref_model_status(L, U, Fm, Fp) -> dict:
    """K4B §8.1 as stated in tools/k4b/API.md (model_status), in exact rationals."""

    def core(fm, fp):
        if fr(L) - fm > M:
            return "SUPPORT"
        if fr(U) + fp < M and fr(L) - fm > -M:
            return "EXCLUDE"
        return "UNRESOLVED"

    s, s0 = core(fr(Fm), fr(Fp)), core(Fraction(0), Fraction(0))
    if s == "UNRESOLVED" and s0 != "UNRESOLVED":
        s = "UNRESOLVED/NUMERICAL"
    labels = ["NEGATIVE_ALIGNMENT"] if fr(U) + fr(Fp) < -M else []
    return {"status": s, "labels": labels, "status_without_F": s0}


# ---- planted rows (API.md §7 row fields) ----
def row(status, valid=None, L=None, U=None, L_S=None, U_S=None, F=F9, learn=False, b2=None,
        step=0, Fm=None, Fp=None):
    if valid is None:
        valid = status in (SC, UC)
    has = status != CU
    return {"status": status, "valid": bool(valid),
            "L": L if has else None, "U": U if has else None,
            "L_S": L_S if has else None, "U_S": U_S if has else None,
            "F_minus": (Fm if Fm is not None else F) if has else None,
            "F_plus": (Fp if Fp is not None else F) if has else None,
            "learn_pass": bool(learn), "B2_L_zS": b2, "step": step}


def NOC(**k):  # no chart: KD4 case (i)
    return row(CU, **k)


def EXC(status=SC, **k):  # certified below: sigma EXCLUDE, below_s; KD4 (ii)/(v)
    return row(status, L=-0.002, U=0.002, L_S=-0.003, U_S=0.003, **k)


def SUP(status=SC, **k):  # certified above: sigma SUPPORT, above_s; KD4 (iii)
    return row(status, L=0.04, U=0.05, L_S=0.039, U_S=0.051, **k)


def UNR(status=SC, **k):  # straddles the margin: sigma UNRESOLVED, neither above nor below
    return row(status, L=0.005, U=0.02, L_S=0.004, U_S=0.021, **k)


def UNV(**k):  # unvalidated chart carrying it: KD4 (iv)
    return SUP(status=SU, **k)


def seq(*rows):
    out = []
    for i, r in enumerate(rows):
        r = dict(r)
        r["step"] = STEPS[i] if i < len(STEPS) else 5000 + i
        out.append(r)
    return out


# ---- §5.1 notation ----
def est(r):
    return r["status"] in (SC, SU)


def ok(r):
    return r["status"] == SC


def sigma(r):
    return ref_model_status(r["L"], r["U"], r["F_minus"], r["F_plus"])["status"] if ok(r) else "NA"


def above_s(r):
    return est(r) and fr(r["L_S"]) - r["F_minus"] > M


def below_s(r):
    return ok(r) and fr(r["U_S"]) + r["F_plus"] < M


def above_s_ok(r):
    return ok(r) and fr(r["L_S"]) - r["F_minus"] > M


def _first(rows, pred):
    for i, r in enumerate(rows):
        if pred(i, r):
            return i + 1
    return None


# ---- §5.2 onsets ----
def onsets(rows):
    K = len(rows)
    v = [bool(r["valid"]) for r in rows]
    return {
        "k_C": _first(rows, lambda i, r: v[i]),
        "k_C_star": _first(rows, lambda i, r: all(v[i:K])),
        "k_C_plus": _first(rows, lambda i, r: i >= 1 and v[i] and not v[i - 1]),
        "k_L": _first(rows, lambda i, r: r["learn_pass"]),
        "k_P": _first(rows, lambda i, r: r["B2_L_zS"] is not None and r["B2_L_zS"] > 0),
        "k_B": _first(rows, lambda i, r: sigma(r) == "SUPPORT"),
        "k_B_S": _first(rows, lambda i, r: above_s(r)),
    }


def _pre(rows):
    kc = onsets(rows)["k_C"]
    lim = (kc - 1) if kc is not None else len(rows)
    return [r for r in rows[:lim] if est(r)]


def n_pre(rows):
    return len(_pre(rows))


def pre_chart_max(rows):
    p = _pre(rows)
    return max(fr(r["U_S"]) + r["F_plus"] for r in p) if p else None


# ---- §5.3 ORDER ----
def order(rows, anchor, A=None):
    o = onsets(rows)
    if A is None:
        A = o["k_C"] if anchor == "chart" else o["k_L"]
    if A is None:
        return "NO_CHART" if anchor == "chart" else "NO_LEARNING"
    if anchor == "chart" and A == 1:
        return "CHART_AT_INIT"
    if any(above_s(r) for r in rows[:A - 1]):
        return "BEFORE"
    sA, sK = sigma(rows[A - 1]), sigma(rows[-1])
    if sA == "NA":
        if anchor == "learning" and (o["k_C"] is None or o["k_C"] > A):
            return "LEARNING_BEFORE_CHART"
        return "UNCERTIFIED_AT_ANCHOR"
    if sA == "SUPPORT":
        return "WITH"
    if sA == "EXCLUDE" and sK == "SUPPORT":
        return "AFTER"
    if sK == "EXCLUDE":
        return "NEVER"
    return "FINAL_NA" if sK == "NA" else "UNRESOLVED"


# ---- §5.4 statements, per model: (reading, reason, qualifier) ----
def _ne(reason):
    return ("NOT_EVALUABLE", reason, None)


def d1(rows):
    s = sigma(rows[-1])
    if s == "SUPPORT":
        return ("TRUE", None, None)
    if s == "EXCLUDE":
        return ("FALSE", None, None)
    return _ne("FINAL_NA" if s == "NA" else "UNRESOLVED")


def d2(rows):
    kc = onsets(rows)["k_C"]
    if kc == 1:
        return _ne("CHART_AT_INIT")
    if kc is None:
        return _ne("NO_CHART")
    if order(rows, "chart") == "BEFORE":
        return ("FALSE", None, None)
    if sigma(rows[-1]) != "SUPPORT":
        return _ne("FINAL_NOT_SUPPORT")
    if n_pre(rows) >= 1:
        inf = any(fr(r["U_S"]) + r["F_plus"] < M for r in _pre(rows))
        return ("TRUE", None, "INFORMATIVE" if inf else "UNINFORMATIVE")
    return ("BY_CONSTRUCTION", None, None)


def _d34(rows, anchor):
    c = order(rows, anchor)
    if c == "AFTER":
        return ("TRUE", None, None)
    if c in ("WITH", "BEFORE"):
        return ("FALSE", None, None)
    return _ne(c)


def d3(rows):
    return _d34(rows, "chart")


def d4(rows):
    return _d34(rows, "learning")


def d5(rows):
    o = onsets(rows)
    kp, kc = o["k_P"], o["k_C"]
    if kp is None:
        return _ne("NO_PREDICTIVE_ONSET")
    if kc is None or kc > kp:
        return ("FALSE", None, None)
    s = sigma(rows[kp - 1])
    if s == "EXCLUDE":
        return ("FALSE", None, None)
    if s == "SUPPORT":
        return ("TRUE", None, None)
    return _ne("NA_AT_PREDICTIVE_ONSET" if s == "NA" else "UNRESOLVED")


def d6(rows):
    K = len(rows)
    loss = any(above_s_ok(rows[a]) and below_s(rows[b]) for a in range(K) for b in range(a + 1, K))
    if loss:
        return ("FALSE", None, None)
    if any(above_s_ok(rows[a]) for a in range(K - 1)):
        return ("TRUE", None, None)
    return _ne("NO_STRONG_CROSSING")


PER_MODEL = {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5, "D6": d6}


def aggregate(statement, per):
    """per: {j: (reading, reason, qualifier)} -> (reading, {reason: sorted models})."""
    reads = {j: p[0] for j, p in per.items()}
    models = sorted(per)
    if "FALSE" in reads.values():
        return ("FALSE", {})
    if statement == "D2":
        all_tb = all(v in ("TRUE", "BY_CONSTRUCTION") for v in reads.values())
        inf = any(p[0] == "TRUE" and p[2] == "INFORMATIVE" for p in per.values())
        if all_tb and inf:
            return ("TRUE", {})
    elif all(v == "TRUE" for v in reads.values()):
        return ("TRUE", {})
    reasons = {}
    for j in models:
        if per[j][0] == "NOT_EVALUABLE":
            reasons.setdefault(per[j][1], []).append(j)
    if statement == "D2":
        if all(v == "BY_CONSTRUCTION" for v in reads.values()):
            reasons["BY_CONSTRUCTION"] = models
        elif all(v in ("TRUE", "BY_CONSTRUCTION") for v in reads.values()):
            reasons["UNINFORMATIVE_PRE_CHART"] = models
    return ("NOT_EVALUABLE", reasons)


def evaluate(table):
    return {s: aggregate(s, {j: f(rows) for j, rows in table.items()})
            for s, f in PER_MODEL.items()}


def cmp_line(a, b):
    if a is None or b is None:
        return "undefined"
    return "<" if a < b else ("=" if a == b else ">")


def est_loss(rows):
    K = len(rows)
    return [(a + 1, b + 1) for a in range(K) for b in range(a + 1, K)
            if above_s(rows[a]) and rows[a]["status"] == SU and below_s(rows[b])]


# ---- random planted sequences for the cross-checks ----
def random_row(rng: random.Random):
    st = rng.choice([SC, SC, SU, CU, UC])
    valid = st == SC or (st == UC and rng.random() < 0.7)
    base = rng.choice([-0.004, 0.0, 0.006, 0.0095, 0.011, 0.02, 0.04])
    w = rng.choice([0.0005, 0.003, 0.008])
    return row(st, valid=valid, L=base - w, U=base + w, L_S=base - 1.3 * w, U_S=base + 1.3 * w,
               F=rng.choice([F9, Fraction(1, 10**4)]), learn=rng.random() < 0.3,
               b2=rng.choice([None, -0.01, 0.0, 0.002]))


def random_table(rng: random.Random, K=None):
    K = K or rng.randint(1, 12)
    return {j: seq(*[random_row(rng) for _ in range(K)]) for j in MASTERS}


# ---- self-checks of the reference against the protocol's worked examples ----
KD4_ROWS = {"i": NOC, "ii": EXC, "iii": SUP, "iv": UNV, "v": EXC}
KD4_EXPECTED = {  # API.md §17.3 (ORDER at k_C, D2, D3, D6 aggregates)
    "AFTER": (("i", "ii", "ii", "iii", "iii"), "AFTER", ("NOT_EVALUABLE", "BY_CONSTRUCTION"),
              ("TRUE", None), ("TRUE", None)),
    "WITH": (("i", "i", "iii", "iii"), "WITH", ("NOT_EVALUABLE", "BY_CONSTRUCTION"),
             ("FALSE", None), ("TRUE", None)),
    "BEFORE": (("i", "iv", "iii", "iii"), "BEFORE", ("FALSE", None), ("FALSE", None),
               ("TRUE", None)),
    "NEVER": (("i", "ii", "ii"), "NEVER", ("NOT_EVALUABLE", "FINAL_NOT_SUPPORT"),
              ("NOT_EVALUABLE", "NEVER"), ("NOT_EVALUABLE", "NO_STRONG_CROSSING")),
    "NO_CHART": (("i", "i", "i"), "NO_CHART", ("NOT_EVALUABLE", "NO_CHART"),
                 ("NOT_EVALUABLE", "NO_CHART"), ("NOT_EVALUABLE", "NO_STRONG_CROSSING")),
    "STEP0_CONTROL": (("ii", "iii"), "CHART_AT_INIT", ("NOT_EVALUABLE", "CHART_AT_INIT"),
                      ("NOT_EVALUABLE", "CHART_AT_INIT"), ("NOT_EVALUABLE", "NO_STRONG_CROSSING")),
}


def kd4_table(cases):
    return {j: seq(*[KD4_ROWS[c]() for c in cases]) for j in (629951, 629952, 629953)}


def test_reference_reproduces_api_17_3():
    for name, (cases, order_c, e2, e3, e6) in KD4_EXPECTED.items():
        t = kd4_table(cases)
        assert {order(r, "chart") for r in t.values()} == {order_c}, name
        ev = evaluate(t)
        for s, e in (("D2", e2), ("D3", e3), ("D6", e6)):
            assert ev[s][0] == e[0], (name, s)
            if e[1] is not None:
                assert set(ev[s][1]) == {e[1]}, (name, s)


def test_reference_model_status_boundaries():
    assert ref_model_status(0.5, 0.6, Fraction(49, 100), 0)["status"] == "UNRESOLVED/NUMERICAL"
    assert ref_model_status(0.5, 0.6, Fraction(48, 100), 0)["status"] == "SUPPORT"
    fp = Fraction(1, 100) - Fraction(0.005)  # U + F+ = 1/100 exactly: not EXCLUDE
    assert ref_model_status(0.0, 0.005, 0, fp)["status"] == "UNRESOLVED/NUMERICAL"
    assert ref_model_status(-0.5, -0.4, 0, 0)["labels"] == ["NEGATIVE_ALIGNMENT"]
    assert ref_model_status(-0.5, -0.4, 0, 0)["status"] == "UNRESOLVED"


def test_reference_planted_presets():
    assert sigma(EXC()) == "EXCLUDE" and below_s(EXC()) and not above_s(EXC())
    assert sigma(SUP()) == "SUPPORT" and above_s(SUP()) and above_s_ok(SUP())
    assert sigma(UNR()) == "UNRESOLVED" and not above_s(UNR()) and not below_s(UNR())
    assert sigma(UNV()) == "NA" and above_s(UNV()) and not above_s_ok(UNV())
    assert sigma(NOC()) == "NA" and not est(NOC())
