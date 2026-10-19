"""X6S1 decide: learnability, C-ORD, SHARP/TARGET, readout and placebo checks, ordD, per-seed
flags, the ordered decision rules, qualifiers, licence sentences and the report (X6S1-FROZEN-v1
§2.5-§2.7, §3, §4.7, §7.6, §7.9, §11.4; API.md §9). Inputs are plain dicts; a missing or INVALID
model is None and fails every per-seed condition. Import performs no I/O."""
# fmt: off

from __future__ import annotations

import math
import sys
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_EXTRA = [REPO / p for p in ("tools/x6_stage1", "tools/x6_stage0", "tools/x4_oracle_profile",
                             "tools/d2a", "tools/k4b", "tools/c1prime_registry",
                             "tests/oracle_profile")]
sys.path[:0] = [str(p) for p in _EXTRA if str(p) not in sys.path]
import x6s1_data as sd  # noqa: E402

SEEDS = sd.SEEDS
_UNRES = ("UNRESOLVED", "NUMERICALLY_UNRESOLVED")


def _fin(x) -> bool:
    try:
        return x is not None and math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def _fr(x) -> Fraction:
    return Fraction(x) if isinstance(x, (Fraction, int)) else Fraction(Decimal(str(x))) \
        if isinstance(x, str) else Fraction(float(x))


def _dec_fr(U):
    try:
        d = Decimal(str(U))
    except (InvalidOperation, ValueError):
        return None
    return Fraction(d) if d.is_finite() else None


# ---- learnability (§4.7, E3.3) ----
def learned_val(ub, g8_lo, nonfinite=False) -> str:
    if nonfinite:
        return "FAIL"
    if not _fin(ub):
        return "UNRESOLVED"
    return "PASS" if Fraction(float(ub)) < g8_lo else "FAIL"


def learn_decision(status_s1, status_s2) -> str:
    if "PASS" in (status_s1, status_s2):
        return "GO"
    return "NOT_LEARNED" if (status_s1, status_s2) == ("FAIL", "FAIL") else "LEARNING_UNRESOLVED"


def learned_test(U, g8_lo) -> str:
    u = None if U is None else _dec_fr(U)
    if u is None:
        return "UNRESOLVED"
    return "PASS" if u < g8_lo else "FAIL"


# ---- natural criteria (§2.3-§2.4, §2.6-§2.7) ----
def ctrl(b_init, b_ab, b_zc):
    vals = [b_init, *list(b_ab or [None]), *list(b_zc or [None])]
    if not all(_fin(v) for v in vals):
        return None
    return max(float(b_init), sum(map(float, b_ab)) / len(b_ab), sum(map(float, b_zc)) / len(b_zc))


def cord(mean, lb, adjusted, tail_status, resolved) -> str:
    if not resolved or tail_status != "PASS" or not (_fin(mean) and _fin(lb)):
        return "UNRESOLVED"
    pos = sum(1 for s in SEEDS if _fin(adjusted.get(s)) and float(adjusted[s]) > 0)
    ok = _fr(mean) >= sd.CORD_MEAN and _fr(lb) > sd.CORD_LB and pos >= 3
    return "SUPPORTED" if ok else "NOT_SUPPORTED"


def sharp_target(U, g0_lo) -> dict:
    u = None if U is None else _dec_fr(U)
    sharp = u is not None and u < g0_lo
    target = sharp and u < sd.TARGET_FRAC * g0_lo
    status = "TARGET_MET" if target else "GAIN_BELOW_TARGET" if sharp else "NOT_CERTIFIED"
    return {"U": U, "SHARP": bool(sharp), "TARGET": bool(target), "status": status}


def cue_ok(median) -> bool:
    return _fin(median) and Fraction(float(median)) >= sd.CUE_MASS_MIN


def placebo_natural(betas) -> dict:
    failed = [k for k, b in betas.items() if not _fin(b) or abs(Fraction(float(b))) > sd.PLACEBO]
    return {"failed": failed, "ok": not failed}


# ---- designed flag ordD (§2.5) ----
def _defined(d, keys) -> bool:
    return d is not None and not d.get("nonfinite") and all(
        _fin(x) for k in keys for x in (d[k] if isinstance(d[k], list) else [d[k]]))


def ord_d(na, init, ab, zc, dw2_lo) -> dict:
    def out(status, limited=False, reason=""):
        return {"status": status, "control_limited": limited, "reason": reason}
    if not _defined(na, ("beta_W2", "beta_W2_y", "R_W2", "rho_C", "cue_mass_median")):
        return out("UNRESOLVED", reason="NA model missing or non-finite")
    if not cue_ok(na["cue_mass_median"]):
        return out("UNRESOLVED", reason="READOUT_LIMITED")
    if Fraction(float(na["rho_C"])) > sd.RHO_MAX:
        return out("UNRESOLVED", reason="NA spurious order rho_C")
    for name, c in (("init", init), ("AB", ab), ("ZC", zc)):
        keys = ("beta_W2",) if name == "init" else ("beta_W2", "rho_W2")
        if not _defined(c, keys) or abs(Fraction(float(c["beta_W2"]))) > sd.PLACEBO or (
                name != "init" and Fraction(float(c["rho_W2"])) > sd.RHO_MAX):
            return out("UNRESOLVED", True, f"designed placebo {name}")
    beta, r = Fraction(float(na["beta_W2"])), Fraction(float(na["R_W2"]))
    ymin = min(Fraction(float(b)) for b in na["beta_W2_y"])
    bar, band = sd.regret_bar(dw2_lo), sd.BAND
    if beta >= sd.W2_BETA + band and r <= bar - band and ymin >= sd.W2_BETA + band:
        return out("PASS")
    if beta < sd.W2_BETA - band or r > bar + band or ymin < sd.W2_BETA - band:
        return out("FAIL")
    return out("NUMERICALLY_UNRESOLVED")


# ---- per-seed flags (§7.6) and counts ----
def seed_flags(adj, lb_adj, U025, xbar, hw95, g0_lo) -> dict:
    order = _fin(adj) and _fin(lb_adj) and Fraction(float(adj)) >= sd.CORD_MEAN and \
        Fraction(float(lb_adj)) > sd.CORD_LB
    low = _fin(adj) and Fraction(float(adj)) < sd.LOWN
    u = None if U025 is None else _dec_fr(U025)
    prec = _fin(hw95) and _fin(xbar) and u is not None and Fraction(float(hw95)) <= \
        sd.PREC_BETA and u - Fraction(float(xbar)) <= sd.PREC_FRAC * g0_lo
    return {"orderN": bool(order), "lowN": bool(low), "precision_ok": bool(prec)}


def designed_counts(statuses) -> dict:
    st = list(statuses)
    p, f = st.count("PASS"), st.count("FAIL")
    return {"PASS": p, "FAIL": f, "UNRESOLVED": len(st) - p - f}


# ---- ordered rules (§7.9) ----
_RULE1 = (("S0", "INVALID"), ("PF", "INVALID"), ("SMOKE_INGEST", "INVALID"),
          ("G0_ORC", "CONSTRUCTION_FAIL"), ("SCORE", "CONSTRUCTION_FAIL"),
          ("G0_POS", "CONSTRUCTION_FAIL"), ("G0_FEAS", "FEASIBILITY_NO_GO"),
          ("REGISTRY", None), ("INCOMPLETE", "INCOMPLETE"))
_REG = ("FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE")


def decide(ev) -> dict:
    def res(outcome, rule):
        return {"outcome": outcome, "rule": rule}
    for key, outcome in _RULE1:
        st = ev["validity"].get(key)
        if st not in ("PASS", "NOT_RUN"):
            return res(outcome or (st if st in _REG else _REG[0]), "1")
    if ev["learn"] != "GO":
        return res(ev["learn"] if ev["learn"] == "NOT_LEARNED" else "LEARNING_UNRESOLVED", "2")
    if any(v != "PASS" for v in ev["pipeline"].values()):
        return res("PIPELINE_INVALID", "3")
    lt = [ev["learn_test"].get(f"NA-s{s}") for s in SEEDS]
    p, u = lt.count("PASS"), lt.count("UNRESOLVED")
    if p < 3:
        return res("LEARNING_NOT_ROBUST" if p + u < 3 else "LEARNING_UNRESOLVED", "4")
    od = [ev["ord_d"].get(s) for s in SEEDS]
    od_pass, cord_ = od.count("PASS"), ev["cord"]
    if cord_ == "SUPPORTED":
        if not ev["placebo_natural_ok"]:
            return res("INCONCLUSIVE", "6'")
        return res("ORDER_USE_NATURAL_AND_DESIGNED", "5") if od_pass >= 3 else \
            res("ORDER_USE_NATURAL", "6")
    if cord_ == "NOT_SUPPORTED":
        if od_pass >= 3:
            return res("ORDER_USE_DESIGNED_ONLY", "7")
        low = sum(1 for s in SEEDS if ev["lowN"].get(s) is True)
        resolved = all(x in ("PASS", "FAIL") for x in od)
        prec = all(ev["precision_ok"].get(s) is True for s in SEEDS)
        if low >= 3 and resolved and od_pass <= 1 and prec and ev["checks_ok"] is True:
            return res("ORDER_NOT_DETECTED", "8")
    return res("INCONCLUSIVE", "9")


# ---- qualifiers (§3, §7.9; optional ev keys, §13 item 20) ----
def _models(d, pred) -> list:
    return [m for m, v in sorted((d or {}).items()) if pred(v)]


def qualifiers(ev) -> list:
    out, st = [], ev.get("sharp_target") or {}
    k = len(_models(st, lambda v: v.get("SHARP")))
    t = len(_models(st, lambda v: v.get("TARGET")))
    if k:
        out.append(f"SHARP_NATURAL({k}/4)")
    if t:
        out.append(f"NATURAL_TARGET({t}/4)")
    if k - t:
        out.append(f"GAIN_BELOW_REGISTERED_TARGET({k - t}/4)")
    for key, name in (("w2_gap_beaten", "W2_GAP_BEATEN"), ("challenge_beaten",
                                                          "CHALLENGE_BEATEN")):
        n = len(_models(ev.get(key), bool))
        if n:
            out.append(f"{name}({n}/4)")
    for dom, items in sorted((ev.get("control_limited") or {}).items()):
        if items:
            out.append(f"CONTROL_LIMITED({dom}, {', '.join(map(str, items))})")
    if ev.get("readout_limited"):
        out.append(f"READOUT_LIMITED({', '.join(ev['readout_limited'])})")
    if ev.get("controls_learned"):
        cl = ev["controls_learned"]
        out.append(f"CONTROLS_LEARNED(AB {cl['AB']}/4, ZC {cl['ZC']}/4)")
    if ev.get("ladder"):
        out.append(f"LADDER({', '.join(map(str, ev['ladder']))})")
    if ev.get("precision_limited"):
        out.append("PRECISION_LIMITED")
    unres = sum(1 for s in SEEDS if ev["ord_d"].get(s) in _UNRES)
    if unres:
        out.append(f"DESIGNED_UNRESOLVED({unres})")
    if ev.get("length_profile"):
        out.append("LENGTH_PROFILE")
    for key, name in (("mixed_device", "MIXED_DEVICE"), ("mixed_env", "MIXED_ENV")):
        if ev.get(key):
            out.append(f"{name}({', '.join(ev[key])})")
    return out


# ---- licence sentences (§3) ----
_NAT = ("On fresh natural histories, the models' next-symbol predictions at t = 32 varied between "
        "histories with identical prefix, last cue, cue age, end vertex and directed seam-crossing "
        "counts, in the direction of the exact oracle's order-dependent variation: mean "
        "control-adjusted alignment {beta_bar} (nominal one-sided 97.5% bootstrap lower bound "
        "{lb}; oracle 1; every function of the Parikh vector exactly 0; every function of the "
        "cue-free segment, including every function of the last 8 symbols, 0 in expectation). "
        "These models' predictors are therefore not functions of the Parikh vector or of any "
        "coarser commutative statistic of the crossing word.")
_DES = ("On the registered AB-versus-BA family, whose members share token and directed-bigram "
        "multisets, crossing counts, H1 class and their last 8 symbols, {k} of the 4 models ({k} "
        "PASS, {f} FAIL, {u} UNRESOLVED) shifted their cue predictions in the oracle direction "
        "(pooled and per-cue alignment >= 0.25) and had full-vocabulary regret <= 75 % of the best "
        "set-constant predictor's. Every function of the matched statistics, first- and "
        "last-crossing rules (pooled 0) and reversed-order composition (-1) cannot do this.")
_NONE = ("No statement about models. CONSTRUCTION_FAIL: the stage-1 oracle or scoring pipeline "
         "disagrees with stage 0. FEASIBILITY_NO_GO: this design cannot resolve the estimand. "
         "INCOMPLETE: the registered models could not all be trained and verified. None is a "
         "negative result.")
_TEXT = {
    "NOT_LEARNED": "Neither registered NA validation model's natural excess log-loss at t = 32 "
    "was credibly below the exact 8-symbol-window Bayes gap G_8(32) = 8.855e-3 nats on fresh "
    "validation histories, so neither was shown to be better than every function of the last 8 "
    "symbols (and hence not transport-blind). This recipe failed the registered learnability "
    "gate.",
    "LEARNING_UNRESOLVED": "Learnability could not be decided because a required statistic was "
    "undefined.",
    "PIPELINE_INVALID": "No conclusion from the affected analysis until a documented technical "
    "correction (no threshold change).",
    "LEARNING_NOT_ROBUST": "Fewer than three of the four registered NA models met the "
    "learnability criterion on the fresh test pool; order statistics are reported per model, "
    "descriptively.",
    "ORDER_USE_NATURAL_AND_DESIGNED": _NAT + " " + _DES,
    "ORDER_USE_NATURAL": _NAT + " The designed criterion had {k} PASS, {f} FAIL and {u} "
    "UNRESOLVED models and was not established in three models. A natural-distribution "
    "mechanism using segment token bags or a last-crossing rule remains possible.",
    "ORDER_USE_DESIGNED_ONLY": _DES + " The registered natural-distribution order criterion was "
    "not met.",
    "ORDER_NOT_DETECTED": "The models passed the transport learnability gate, but their "
    "control-adjusted within-Parikh-class order alignment was below 0.10 in at least three of "
    "four seeds, and the registered order criteria were not met.",
    "INCONCLUSIVE": "Split seeds, an UNRESOLVED confirmatory contrast, a natural placebo failure "
    "(CONTROL_LIMITED), a failed tail diagnostic, precision failure or mixed patterns. "
    "Descriptive only.",
}


def licence(outcome, values) -> str:
    return _TEXT.get(outcome, _NONE).format(**{k: values.get(k) for k in
                                                ("beta_bar", "lb", "k", "f", "u")})


def report(ev, values) -> dict:
    d = decide(ev)
    rep = {"protocol_id": sd.PROTOCOL_ID, "protocol_sha256": sd.PROTOCOL_SHA256, **d,
           "qualifiers": qualifiers(ev), "licence": licence(d["outcome"], values)}
    rep.update({k: v for k, v in values.items() if k not in rep})
    return rep
