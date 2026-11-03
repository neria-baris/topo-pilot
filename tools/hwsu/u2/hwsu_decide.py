"""HWSU decision side: P1 ladder, family stream, per-model statements, aggregation, outcomes,
licences, descriptives, sealing (API_U2.md sections 4.2, 4.4-4.7). Split from hwsu_gates by size
(API erratum); every name stays reachable as hwsu_gates.<name>. Response family only.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_model as um
import hwsu_of as uof
import u2  # noqa: F401
import json
import re
from fractions import Fraction
from pathlib import Path

import c1_means
import c2_attrib
import c2_decide
import numpy as np
import precision
import stage_records
from c1_records import C1GateFailure

SHARE_OUTCOME = "INCONCLUSIVE/ORACLE_FEASIBILITY"
NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"
SEALED_KEYS_U = {"A_full", "AF", "ZR010", "ZR030", "theta", "theta_hat", "mean_A", "mean_ZR010",
                 "mean_ZR030", "sign_agreement", "row_cross_check", "family_bounds",
                 "per_model_status"}
_SEALED_RE = re.compile(r"^(A|ZR010|ZR030|theta|AF)_[0-9A-Za-z]+$")
_CAT = {"USED": "RESPONDS_j", "PARTIAL": "WEAK_RESPONSE_j", "NOT_USED": "LOW_RESPONSE_j",
        "LOW_ALIGNED": "LOW_RESPONSE_j", "INC": "INC_j", "INC/NUMERICAL": "INC_j/NUMERICAL"}


def _tm(x) -> float:
    return float(c1_means.tree_mean(x))


# ------------------------------------------------------------------------------- P1
def p1_u(A, G, models, seeds, ladder=uc.LADDER) -> dict:
    models, G = list(models), np.asarray(G, dtype=np.float64)
    alt = float(uc.ALT_RESP * Fraction(_tm(G)))
    passes, prec, mde = {}, {}, {}
    for X in ("ZR010", "ZR030"):
        Xd = {j: um.response_arrays(A[j], G)[X] for j in models}
        sd, _ = precision.sd_b4_draws(Xd, {j: G for j in models}, models, seeds["p1_sd"],
                                      uc.DRAWS, len(G))
        prec[f"sd_{X}"], passes[X] = sd, {}
        for N in ladder:
            e = precision.centered_draws(Xd, models, seeds["p1_centred"], uc.DRAWS, N)
            cfg = {"alpha": float(uc.ALPHA_FAMILY), "power": uc.POWER, "delta": 0.0,
                   "alternative": alt, "projected_N": N}
            s = precision.precision_summary(sd, e, models, cfg)
            prec[f"e_{X}_{N}"] = e
            passes[X][N] = {j: bool(s["models"][j]["mde_upper"] <= alt
                                    and s["models"][j]["power"] >= uc.POWER) for j in models}
            mde.setdefault(X, {})[N] = {
                j: {"mde_upper": s["models"][j]["mde_upper"], "power": s["models"][j]["power"]}
                for j in models}
    both = {N: [j for j in models if passes["ZR010"][N][j] and passes["ZR030"][N][j]]
            for N in ladder}
    n_resp = next((N for N in ladder if len(both[N]) == len(models)), None)
    if n_resp is None:
        n_resp = next((N for N in ladder if len(both[N]) >= 2), None)
    limited = [] if n_resp is None else [f"PRECISION_LIMITED({j})" for j in models
                                         if j not in both[n_resp]]
    k = None if n_resp is None else (n_resp // uc.BLOCK_OF if n_resp % uc.BLOCK_OF == 0
                                     else n_resp / uc.BLOCK_OF)
    return {"N_RESP": n_resp, "N": n_resp, "k": k, "mde": mde, "passes": passes, "precision_limited": limited, "prec": prec, "alt": alt}


# ------------------------------------------------------------ family stream, statements
def family_bounds(A, G, models, seed=640111, alpha=Fraction(1, 300), draws=20000) -> dict:
    arrays = {}
    for j in models:
        for name, arr in um.response_arrays(A[j], G).items():
            arrays[f"{j}:{name}"] = arr
    b = c2_decide.stream_bounds(arrays, seed, float(alpha), draws)
    if draws == 20000 and not all(v["rank_L"] == 67 and v["rank_U"] == 19934 for v in b.values()):
        raise C1GateFailure(NUMERICAL, "family stream rank check (67 / 19934) failed")
    return {k: {"L": v["L"], "U": v["U"], "mean": v["mean"], "rank_L": v["rank_L"],
                "rank_U": v["rank_U"], "g": c2_decide.guard(arrays[k], 0.0)}
            for k, v in b.items()}


def model_status(bj) -> dict:
    cat = c2_decide._category({s: dict(bj[s]) for s in ("ZR010", "ZR030")}, "ZR010", "ZR030", ())
    sg = c2_decide.sign
    af, z1, z3 = bj["AF"], bj["ZR010"], bj["ZR030"]
    rule6 = sg(af["L"], af["g"]) == 1 and sg(z3["U"], z3["g"]) == -1
    coarse = []
    if sg(z1["L"], z1["g"]) == 1:
        coarse.append("theta > 0.10")
    if sg(z3["U"], z3["g"]) == -1:
        coarse.append("theta < 0.30")
    return {"status": _CAT[cat], "rule6": bool(rule6), "coarse": coarse, "bounds": bj}


_REGIONS = {"<=0": 2, "0<<=0.1": 2, "0.1<<0.3": 2, "=0.3": 2, ">0.3": 1}


def _region(x) -> str:
    if isinstance(x, str):
        s = x.lower().replace("\u03b8", "").replace("theta", "").replace(" ", "")
        return s.replace("\u2264", "<=").replace("0.10", "0.1").replace("0.30", "0.3")
    t = Fraction(x)
    return ("<=0" if t <= 0 else "0<<=0.1" if t <= Fraction(1, 10) else "0.1<<0.3"
            if t < Fraction(3, 10) else "=0.3" if t == Fraction(3, 10) else ">0.3")


def fw_events(theta_region) -> int:
    """Lemma FW-U, response part: events whose union holds 'a declared statement is false'.
    With G >= 0 elementwise the draw means satisfy ZR030 <= ZR010 <= AF, so L(ZR030) <= L(ZR010)
    <= L(AF) and U(ZR030) <= U(ZR010): every false positive statement is inside the event
    F^L(ZR010) and F^L(AF) (theta <= 0), every false negative one inside F^U(ZR030) (theta > 0.30)."""
    r = _region(theta_region)
    if r not in _REGIONS:
        raise ValueError(f"unknown truth region {theta_region!r}")
    return _REGIONS[r]


# ---------------------------------------------------------- aggregation, outcomes
_ST = re.compile(r"^(RESPONDS|WEAK_RESPONSE|LOW_RESPONSE|INC|EXCLUDED|NOT_RUN)(?:_[0-9A-Za-z]*)?"
                 r"(/.*)?$")


def _base(st) -> str:
    m = _ST.match(str(st["status"] if isinstance(st, dict) else st))
    return m.group(1) if m else "INC"


def response_outcome(per_model, rule6=None) -> dict:
    sts = {j: (v["status"] if isinstance(v, dict) else v) for j, v in per_model.items()}
    r6 = dict(rule6 or {j: bool(v.get("rule6")) for j, v in per_model.items()
                        if isinstance(v, dict)})
    base = {j: _base(s) for j, s in sts.items()}
    ex = [j for j, b in base.items() if b in ("EXCLUDED", "NOT_RUN")]
    cnt = {b: sum(1 for j in base if base[j] == b) for b in set(base.values())}
    if len(base) - len(ex) < 2:
        gate = str(sts[ex[0]]).split("/", 1)[1] if ex and "/" in str(sts[ex[0]]) else "PRECISION"
        out = f"INCONCLUSIVE/{gate}"
    else:
        out = next((c for c in ("RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE") if cnt.get(c, 0) >= 2),
                   None)
        if out is None:
            n_res = sum(cnt.get(c, 0) for c in ("RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE"))
            out = "MIXED" if n_res >= 2 else "INCONCLUSIVE/PRECISION"
    dissent = [] if out not in ("RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE") else [
        f"DISSENT({j}: {sts[j]})" for j in sts if base[j] not in (out, "EXCLUDED", "NOT_RUN")]
    k = sum(1 for j in r6 if r6[j])
    note = None if k < 2 else ("RESP_POSITIVE_BELOW_MARGIN in all three" if k == 3
                               else f"RESP_POSITIVE_BELOW_MARGIN in {k} models")
    return {"outcome": out, "dissent": dissent, "rule6": note, "qualifiers": dissent}


def share_outcome(of_bind) -> dict:
    return {"outcome": SHARE_OUTCOME, "source": "OF_ACCEPT.json",
            "of_accept_sha256": of_bind["of_accept_sha256"]}


def study_outcome(records, resp, share=None) -> str:
    st = [str(r["status"]) for r in records]
    fail = next((s for s in st if s.startswith("FAIL_TECHNICAL")), None)
    if fail:
        return fail
    if any(s in ("INCONCLUSIVE/AUTHORITY", "INCONCLUSIVE/RESOURCE_OR_AUTHORITY") for s in st):
        return "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    inc = next((s for s in st if s.startswith("INCONCLUSIVE")), None)
    return inc or resp["outcome"]


def licences(resp, per_model, bounds, desc, contract=None) -> dict:
    oc = (uc.CONTRACT if contract is None else contract)["outcomes_u2"]
    L, clause, out = oc["licences"], oc["scope_clause"], resp["outcome"]
    weak = "WEAK_RESPONSE / RESP_POSITIVE_BELOW_MARGIN"
    key = {"RESPONDS": "RESPONDS", "WEAK_RESPONSE": weak,
           "LOW_RESPONSE": "LOW_RESPONSE"}.get(out, "MIXED / INCONCLUSIVE")
    text = L[key]
    cat = out
    masters = [j for j, s in per_model.items() if _base(s) == cat]
    if key != "MIXED / INCONCLUSIVE":
        pts = ", ".join(f"{(desc or {}).get('theta_hat', {}).get(j)}" for j in masters)
        lows = ", ".join(f"{bounds.get(f'{j}:ZR030', {}).get('L')}" for j in masters)
        text = (text.replace("In k of the 3", f"In {len(masters)} of the 3")
                .replace("(masters ...)", f"(masters {', '.join(map(str, masters))})")
                .replace("theta-hat = ...", f"theta-hat = {pts}")
                .replace("lower bounds ....", f"lower bounds {lows}."))
    share = L["SHARE_INCONCLUSIVE_ORACLE_FEASIBILITY"]
    res = {"response": f"{text} {clause}", "share": f"{share} {clause}",
           "disclosure": oc["disclosure"], "does_not_establish": oc["does_not_establish"],
           "rule6": resp.get("rule6")}
    if out == "LOW_RESPONSE":
        res["not_licensed"] = L["LOW_RESPONSE_not_licensed"]
    return res


def descriptives(A, G, rowA, models) -> dict:
    nums = {f"A_{j}": A[j] for j in models}
    iv = c2_attrib.ratio_intervals(nums, {"G": G}, [(f"A_{j}", "G") for j in models], 640117,
                                   uc.DRAWS)
    return {"theta_hat": {j: _tm(A[j]) / _tm(G) for j in models},
            "interval95": {j: iv[f"A_{j}/G"] for j in models},
            "sign_agreement": {j: float(np.mean(np.asarray(A[j]) > 0)) for j in models},
            "cross_check": {j: {"pair": _tm(A[j]), "row": _tm(rowA[j])} for j in models},
            "tails": uof.tails(G)}


# ------------------------------------------------------------------------------ sealing
def write_sealed_u(store, arrays) -> str:
    G = np.asarray(arrays["G"], dtype=np.float64)
    means = {}
    for k, v in arrays.items():
        if k.startswith(("A_", "ZR010_", "ZR030_")):
            means[k] = repr(_tm(v))
            if k.startswith("A_"):
                means[f"theta_{k[2:]}"] = repr(_tm(v) / _tm(G))
    body = (json.dumps({"protocol_sha256": uc.CONTRACT["protocol_sha256"], "means": means},
                       sort_keys=True) + "\n").encode()
    p = Path(store) / "SEALED_VALIDATION.json"
    with open(p, "xb") as handle:
        handle.write(body)
    return stage_records.sha256(p)


def check_unsealed_u(report) -> None:
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in SEALED_KEYS_U or _SEALED_RE.match(str(k)):
                    raise C1GateFailure("FAIL_TECHNICAL/SEALING", f"sealed key {k!r} in a report")
                walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
    walk(report)

