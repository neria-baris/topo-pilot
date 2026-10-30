"""HWSC outcome precedence, POSITIVE_BELOW_MARGIN annotation and licences (API.md §6, §12;
protocol §6.1-§6.4). Split from hwsc_gates by size (API erratum); re-exported by hwsc_gates."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
from fractions import Fraction

LIC = cc.CONTRACT["licences"]
K4B_REASONS = tuple(cc.CONTRACT["outcomes"]["k4b_reasons"])
RESOURCE = ("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "INCONCLUSIVE/AUTHORITY",
            "INCONCLUSIVE/RESOURCE")
ENDPOINT = ("SUPPORT", "EXCLUSION", "MIXED", "INCONCLUSIVE", "INCONCLUSIVE/NUMERICAL")


def _fr(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    return Fraction(float(x))


def positive_below_margin(per_model) -> dict:
    kinds, pos = {}, {}
    for j, r in per_model.items():
        p = Fraction(float(r["L"])) - _fr(r["F_minus"]) > 0
        pos[j] = p
        st = r["status"]
        kinds[j] = ("EXCLUDE" if p and st == "EXCLUDE" else
                    "UNRESOLVED" if p and st in ("UNRESOLVED", "UNRESOLVED/NUMERICAL") else None)
    return {"per_model": kinds, "positive": pos,
            "models": [j for j, k in kinds.items() if k],
            "all_positive": bool(pos) and all(pos.values())}


def annotations(result) -> list:
    per = result.get("per_model", {})
    pbm = positive_below_margin(per)
    out = [f"POSITIVE_BELOW_MARGIN_{j}" for j in pbm["models"]]
    if pbm["all_positive"] and result.get("overall") != "SUPPORT":
        out.append("POSITIVE_BELOW_MARGIN")
    for j, r in per.items():
        out += [f"{lab}_{j}" for lab in r.get("labels", [])]
        if r.get("status") == "UNRESOLVED/NUMERICAL":
            out.append(f"UNRESOLVED/NUMERICAL_{j}")
    if (result.get("fresh_B4") or {}).get("FRESH_B4_LOW"):
        out.append("FRESH_B4_LOW")
    for j, q in (result.get("init_qualifier") or {}).items():
        if isinstance(q, str):
            out.append(f"INIT_UNAVAILABLE_{j}")
        elif q is True:
            out.append(f"STEP0_QUALIFIER_{j}")
    return out


def _ft(status) -> str:
    return status if str(status).startswith("FAIL_TECHNICAL/") else f"FAIL_TECHNICAL/{status}"


def outcome(state) -> dict:
    oc = {"outcome": None, "label": None, "k": None, "models": state.get("models"),
          "criterion": state.get("criterion"), "annotations": [], "pbm": None}

    def done(o, **kw):
        oc.update(outcome=o, **kw)
        oc["label"] = oc["label"] or o
        return oc

    if state.get("fail"):
        return done(_ft(state["fail"]))
    if state.get("resource"):
        return done("INCONCLUSIVE/RESOURCE_OR_AUTHORITY")
    l1 = state.get("l1")
    if l1 and int(l1.get("k", 0)) >= 1:
        k = int(l1["k"])
        return done("INCONCLUSIVE/NOT_LEARNED", k=k, models=list(l1.get("models", [])),
                    label=f"INCONCLUSIVE/NOT_LEARNED ({k}/3)")
    k4 = state.get("k4b")
    if k4:
        reason = str(k4).partition("/")[2]
        if str(k4).startswith("INCONCLUSIVE/") and reason in K4B_REASONS:
            return done(str(k4))
        if k4 in RESOURCE:
            return done("INCONCLUSIVE/RESOURCE_OR_AUTHORITY")
        return done("FAIL_TECHNICAL/OUTCOME")
    ep = state.get("endpoint")
    if ep and ep.get("overall") in ENDPOINT:
        return done(ep["overall"], annotations=annotations(ep),
                    pbm=positive_below_margin(ep.get("per_model", {})))
    return done("FAIL_TECHNICAL/OUTCOME")


def state_from_gates(records, l1_record=None, result=None) -> dict:
    st = {"fail": None, "resource": None, "l1": None, "k4b": None, "endpoint": result,
          "criterion": None, "models": None}
    for r in records:
        s = str(r.get("status", ""))
        if s.startswith("FAIL_TECHNICAL") and st["fail"] is None:
            st["fail"] = s
        elif s in RESOURCE and st["resource"] is None:
            st["resource"] = s
        elif r.get("gate") == "L1" and s == "INCONCLUSIVE/NOT_LEARNED":
            src = l1_record or r
            st["l1"] = {"k": int(src.get("k", 1)), "models": src.get("failing",
                                                                     src.get("models", []))}
        elif s.startswith("INCONCLUSIVE/") and st["k4b"] is None:
            st["k4b"] = s
            st["criterion"] = r.get("criterion", r.get("gate"))
            st["models"] = r.get("models")
    return st


class _Fill(dict):
    def __missing__(self, key):
        return "n/a"


def _head(o) -> str:
    if o.startswith("FAIL_TECHNICAL"):
        return "FAIL_TECHNICAL"
    if o in ("INCONCLUSIVE", "INCONCLUSIVE/NUMERICAL"):
        return "INCONCLUSIVE"
    if o in ("SUPPORT", "EXCLUSION", "MIXED", "INCONCLUSIVE/RESOURCE_OR_AUTHORITY",
             "INCONCLUSIVE/NOT_LEARNED", "INCONCLUSIVE/CHART_UNAVAILABLE"):
        return o
    return "INCONCLUSIVE/<K4b reason>"


def licence(oc, fill) -> str:
    f = _Fill(fill or {})
    for k in ("k", "models", "criterion"):
        if oc.get(k) is not None:
            f[k] = oc[k]
    text = LIC[_head(oc["outcome"])].format_map(f)
    if oc["outcome"] == "EXCLUSION":
        lower = fill.get("delta4_orc_lower") if fill else None
        if fill and fill.get("delta4_orc_certified") is True and lower is not None \
                and float(lower) > 0.01:
            text += " " + LIC["EXCLUSION_ORACLE_SENTENCE"]
        text += " " + LIC["EXCLUSION_TAIL"]
    pbm = oc.get("pbm") or {}
    if pbm.get("models"):
        text += " " + LIC["POSITIVE_BELOW_MARGIN"].format_map(
            _Fill(f, models=", ".join(str(m) for m in pbm["models"])))
        for kind in ("EXCLUDE", "UNRESOLVED"):
            if kind in pbm["per_model"].values():
                text += " " + LIC[f"POSITIVE_BELOW_MARGIN_{kind}"]
    return text
