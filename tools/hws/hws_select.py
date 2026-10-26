"""HWS selection rule: criteria, classes, ranking, finalists, X1/S2, outcomes, licences, budget
(API.md §5 and erratum E1, E2, E5, E6, E15; protocol §5, §6.2, §7, §9).

Functions taking records read each record's stored class and failed list (classify under the
frozen floors); no D4 value is used by ranking steps 2-6 (§5.5).
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import math
from fractions import Fraction

import hws_worlds as hw
import hws_stats as hs

C1_MIN, C2_MIN = Fraction(3, 100), Fraction(1, 10)
G4_FLOOR_MIN, BELOW_3X_MIN = Fraction(39, 5000), Fraction(1, 50)
TAU_D2A = Fraction(1, 2000000)
CRITERIA = (("C1", "D4"), ("C2", "GC"), ("C3", "G4"), ("C4", "G4A"))
CONFIDENT, POSSIBLE, MARGINAL = "CANDIDATE/CONFIDENT", "CANDIDATE/POSSIBLE", "CANDIDATE/MARGINAL"
LIC = hw.CONTRACT["licences"]
RATES = hw.CONTRACT["cpu"]["rates_s"]
NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"


def floors(g4_w0: float, g4A_w0: float) -> dict:
    g4 = max(float(g4_w0), float(G4_FLOOR_MIN))
    return {"D4": float(C1_MIN), "GC": float(C2_MIN), "G4": g4, "G4A": float(g4A_w0)}


def criteria(bounds: dict, floors: dict, which: str) -> dict:
    out = {}
    for c, q in CRITERIA:
        x = float(bounds[q][which])
        if not math.isfinite(x):
            raise hw.HwsStop(NUMERICAL, f"non-finite bound {q}.{which} = {x}")
        out[c] = x >= floors[q]
    return out


def eligibility(exact_status, e5_pass, e6_ok) -> str:
    if not e6_ok:
        raise hw.HwsStop("FAIL_TECHNICAL/E6", "numerical integrity (E6) failed on this look")
    if exact_status != "PASS":
        return exact_status
    return "ELIGIBLE" if e5_pass else "INELIGIBLE/E5"


def classify(look, floors) -> dict:
    """§5.4 classes on screening data (R-HWS-1)."""
    if look["eligibility"] != "ELIGIBLE":
        return {"class": look["eligibility"], "failed": []}
    b = look["bounds"]
    uw = criteria(b, floors, "Uw")
    failed = [c for c, _ in CRITERIA if not uw[c]]
    if failed:
        return {"class": "EXCLUDED/" + failed[0], "failed": failed}
    if all(criteria(b, floors, "L1").values()):
        return {"class": CONFIDENT, "failed": []}
    mean = float(b["D4"]["mean"])
    if not math.isfinite(mean):
        raise hw.HwsStop(NUMERICAL, "non-finite D4 point estimate")
    return {"class": POSSIBLE if mean >= floors["D4"] else MARGINAL, "failed": []}


def annotations(D4_bounds) -> list:
    lw, uw = float(D4_bounds["Lw"]), float(D4_bounds["Uw"])
    out = []
    if 0 < lw <= uw < 0.01:
        out.append("ORACLE_POSITIVE_BELOW_C_MARGIN")
    if lw > 0 and uw < 0.03:
        out.append("ORACLE_POSITIVE_BELOW_SWEEP_REQUIREMENT")
    return out


def _recs(records) -> list:
    return list(records.values()) if isinstance(records, dict) else list(records)


def _eligible(r) -> bool:
    return not str(r["class"]).startswith("INELIGIBLE")


def _is_cand(r) -> bool:
    return str(r["class"]).startswith("CANDIDATE")


def _world(r):
    return hw.World(int(r["W"]), int(r["q"]), Fraction(r["sigma"]), Fraction(r["p"]))


def rank_key(rec) -> tuple:
    head = (0 if rec["class"] == CONFIDENT else 1, rec["tier"], rec["changed"])
    return head + (Fraction(rec["distance"]), -rec["bounds"]["G4"]["L1"], rec["key"])


def _top_d4(recs) -> list:
    return sorted(recs, key=lambda r: (-r["bounds"]["D4"]["mean"], r["key"]))


def finalists(records) -> dict:
    """§5.6 items 1-2 (RC-1): ordinary slots never take a MARGINAL world."""
    recs = _recs(records)
    ordinary = sorted([r for r in recs if r["class"] in (CONFIDENT, POSSIBLE)], key=rank_key)
    if ordinary:
        return {"ordinary": [r["key"] for r in ordinary[:16]], "fallback_only": []}
    lo = float(BELOW_3X_MIN)
    pool = [
        r
        for r in recs
        if _eligible(r) and set(r.get("failed", [])) <= {"C1"} and r["bounds"]["D4"]["Uw"] >= lo
    ]
    return {"ordinary": [], "fallback_only": [r["key"] for r in _top_d4(pool)[:16]]}


def x1_trigger(records) -> dict:
    """§6.2 item 1 (RC-6, choice 41)."""
    recs = _recs(records)
    elig = _top_d4([r for r in recs if _eligible(r)])
    if not elig:
        return {"fire": False, "world": None, "add_p": False, "add_sigma": False}
    w = _world(elig[0])
    add_p, add_s = w.p == hw.P_LEVELS[-1], w.sigma == hw.SIGMA_LEVELS[-1]
    fire = not any(_is_cand(r) for r in recs) and (add_p or add_s)
    return {"fire": bool(fire), "world": elig[0]["key"], "add_p": add_p, "add_sigma": add_s}


def _levels(base, extra, present) -> list:
    return list(base) + [x for x in extra if x in present]


def s2_worklist(records, cap=40) -> list:
    """§6.2 item 2 (RC-6 frozen p midpoints; choice 14)."""
    recs = _recs(records)
    cands = [r for r in recs if _is_cand(r)]
    if not cands:
        return []
    low = min(r["tier"] for r in cands)
    by_world = {_world(r): r for r in recs if r["tier"] == low and _eligible(r)}
    ps = _levels(hw.P_LEVELS, hw.X1_P, {w.p for w in by_world})
    ss = _levels(hw.SIGMA_LEVELS, hw.X1_SIGMA, {w.sigma for w in by_world})
    mids = set()
    for w, r in by_world.items():
        for levels, attr, table in ((ps, "p", hw.S2_P_MID), (ss, "sigma", hw.S2_SIGMA_MID)):
            v = getattr(w, attr)
            if v not in levels or levels.index(v) + 1 >= len(levels):
                continue
            hi = levels[levels.index(v) + 1]
            other = by_world.get(hw.World(w.W, w.q, *((w.sigma, hi) if attr == "p" else (hi, w.p))))
            if other is None or _is_cand(other) == _is_cand(r):
                continue
            m = table[(v, hi)]
            mids.add(hw.World(w.W, w.q, *((w.sigma, m) if attr == "p" else (m, w.p))))
    order = sorted(mids, key=lambda w: (hw.changed_factors(w), hw.distance(w), w.key))
    return order[: int(cap)]


def s3_evaluate(rec_s3, floors, kind) -> dict:
    """§5.6 item 3, §7.1 BELOW_3X (erratum E5)."""
    ok = rec_s3["eligibility"] == "ELIGIBLE" and bool(rec_s3["e6_ok"])
    out = {"kind": kind, "ok": ok, "qualifies": False, "below_3x": False, "at_3x": False}
    if not ok:
        return dict(out, criteria_L3={}, L3={})
    crit = criteria(rec_s3["bounds"], floors, "L3")
    l3 = {q: float(rec_s3["bounds"][q]["L3"]) for _, q in CRITERIA}
    below = all(crit[c] for c in ("C2", "C3", "C4")) and l3["D4"] >= float(BELOW_3X_MIN)
    qual = kind == "ordinary" and all(crit.values())
    at3 = below and l3["D4"] >= float(C1_MIN)
    return dict(out, qualifies=qual, below_3x=below, at_3x=at3, criteria_L3=crit, L3=l3)


def selection(finalists, s3) -> dict:
    """§5.6 item 4: first ordinary qualifier in the frozen order; next two are the fallbacks."""
    quals = [k for k in finalists.get("ordinary", []) if s3.get(k, {}).get("qualifies")]
    return {"selected": quals[0] if quals else None, "fallback_list": quals[1:3]}


def absence_shown(records) -> bool:
    """Choice 34: every evaluated, not-INELIGIBLE world is EXCLUDED on its latest look."""
    return all(str(r["class"]).startswith("EXCLUDED") for r in _recs(records) if _eligible(r))


def _max_d4(recs) -> dict:
    top = _top_d4([r for r in recs if "bounds" in r])
    return (
        {"value": top[0]["bounds"]["D4"]["mean"], "key": top[0]["key"]}
        if top
        else {"value": None, "key": None}
    )


def outcome(state) -> dict:
    """§7.1 precedence (RC-1, RC-7, R-HWS-1; choice 35; erratum E6)."""
    recs, fin, s3 = _recs(state["records"]), state["finalists"], state.get("s3", {})
    by_key = {r["key"]: r for r in recs}
    sel = selection(fin, s3)
    order = list(fin.get("ordinary", [])) + list(fin.get("fallback_only", []))
    below = [k for k in order if s3.get(k, {}).get("below_3x")]
    at3 = [k for k in fin.get("fallback_only", []) if s3.get(k, {}).get("at_3x")]
    unresolved = [r["key"] for r in recs if _is_cand(r)]
    res = {
        "selected": None,
        "fallback_list": [],
        "below_3x_worlds": below,
        "at_3x_fallback_only": at3,
        "absence_3x_shown": absence_shown(recs),
        "unresolved": unresolved,
        "max_D4": _max_d4(recs),
    }
    fill = {}
    if state.get("fail"):
        f = str(state["fail"])
        oc = f if f.startswith("FAIL_TECHNICAL") else "FAIL_TECHNICAL/" + f
    elif not state.get("complete"):
        oc = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    elif sel["selected"]:
        res.update(sel)
        oc = f"HWS_SELECTED/T{by_key[sel['selected']]['tier']}"
        fill = _selected_fill(by_key[sel["selected"]], s3[sel["selected"]], state["floors"])
    elif below:
        oc = "HWS_BELOW_3X"
        fill = {
            "worlds": ", ".join(below),
            "fallback_at_3x": ", ".join(at3) or "none",
            "absence": "shown" if res["absence_3x_shown"] else "not shown",
        }
    elif unresolved:
        oc, fill = "HWS_NO_WORLD_CONFIRMED", {"unresolved": ", ".join(unresolved)}
    elif recs and all(not _eligible(r) or r["class"].startswith("EXCLUDED") for r in recs):
        excl = [r for r in recs if _eligible(r)]
        head = bool(excl) and all("C1" in r.get("failed", []) for r in excl)
        sub = "HEADROOM" if head else "FILTER"
        oc = "HWS_NO_SUITABLE_WORLD/" + sub
        fill = {
            "z_w": round(hs.ZW, 2),
            "sub_reason": sub,
            "max_D4": res["max_D4"]["value"],
            "max_D4_key": res["max_D4"]["key"],
        }
    else:
        oc = "FAIL_TECHNICAL/OUTCOME"
    return dict(res, outcome=oc, licence=licence(oc, fill))


def _selected_fill(rec, s3e, fl) -> dict:
    l3 = s3e.get("L3", {})
    fill = {
        "W": rec["W"],
        "q": rec["q"],
        "sigma": float(Fraction(rec["sigma"])),
        "p": float(Fraction(rec["p"])),
        "g4_star": fl.get("G4"),
        "g4A_star": fl.get("G4A"),
    }
    fill.update({f"L3_{q}": l3.get(q, "n/a") for _, q in CRITERIA})
    return fill


class _Fill(dict):
    def __missing__(self, key):
        return "n/a"


def licence(outcome, fill) -> str:
    head = outcome.split("/")[0]
    key = outcome if outcome in LIC else ("HWS_SELECTED" if head == "HWS_SELECTED" else head)
    text = LIC[key].format_map(_Fill(fill))
    if outcome in ("HWS_SELECTED/T1", "HWS_SELECTED/T2"):
        text += " " + LIC["HWS_SELECTED_T1_T2_addendum"]
    return text


# ----------------------------------------------------------------------- budget (§9)


def rate(stage, w) -> int:
    if stage in ("S1", "X1", "S2"):
        return int(RATES["screening"][str(w.W)])
    if stage == "S3":
        if w.W == 12:
            return int(RATES["S3"]["12_tier0" if hw.tier(w) == 0 else "12_tier1"])
        return int(RATES["S3"][str(w.W)])
    raise ValueError(f"no per-world rate for stage {stage!r}")


def forecast(stage, worklist) -> int:
    if stage == "S0":
        return int(hw.CONTRACT["cpu"]["S0_forecast_s"])
    if stage == "J1":
        return int(hw.CONTRACT["cpu"]["J1_forecast_s"])
    return sum(rate(stage, w) for w in worklist)


def pause_check(stage_cpu, stage_fc, cum_cpu, cum_fc) -> dict:
    st, cu = stage_cpu > 3 * stage_fc, cum_cpu > 3 * cum_fc
    trig = "BOTH" if st and cu else "STAGE" if st else "CUMULATIVE" if cu else None
    return {
        "pause": bool(st or cu),
        "trigger": trig,
        "stage_cpu": stage_cpu,
        "stage_fc": stage_fc,
        "cum_cpu": cum_cpu,
        "cum_fc": cum_fc,
    }
