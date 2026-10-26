"""C2ND decisions: guards, the per-model rules of N-R, D (through c2_decide.r_model) and N-M,
the rule-6 statements, variant categories, known cases, the 2-of-3 rule, endpoint statuses,
qualifiers, licences and the union display (API.md §8, §20; protocol §4.3, §5.2, §7, §8).
`b` is one model's {stat: {"mean", "L", "U", "rank_L", "rank_U", "g"}}; a bound inside its
guard is neither > 0 nor < 0 (c2_decide.sign)."""

from __future__ import annotations

import re

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c2_decide as cdc
import nd_attrib as nat

HEADROOM, NUISANCE = cdc.HEADROOM, cdc.NUISANCE
KCC, NC, CLA = "KNOWN_CASE_CONTRADICTED", "NOT_COMPUTED", "COMPLEMENT_LOW_ALIGNED"
NR_CAT = ("NECESSARY", CLA, "CODE_DOMINANT", "NOT_NECESSARY")
NM_CAT = tuple(c + "_M" for c in NR_CAT)
D_CAT = {c: "DECOY_" + c for c in cdc.CAT}  # USED, PARTIAL, NOT_USED, LOW_ALIGNED
REASON_ORDER = cdc.REASON_ORDER + ("KNOWN_CASE_UNRESOLVED", "CONSTRUCTION")  # ND-C39
NON_EXCLUDING = ("V3y", "V3x'-g1", "KC-R", "NUM", "ENDPOINT", "REPORT", "IMPL", "ACCEPT")
UNION_DISPLAY = {"package": "0.15", "c2nd": "0.1417", "c2r_plus_c2nd": "0.1917"}
UNION_DISPLAY["all_six"] = "0.2917 (<= 0.30)"

# ---- bounds and guards (§4.1, §4.4; API.md §8.1) ---------------------------------------------
stream_bounds, guard, beta_A, beta_E = cdc.stream_bounds, cdc.guard, cdc.beta_A, cdc.beta_E
sign, model_bounds, stream_guards = cdc.sign, cdc.model_bounds, cdc.stream_guards
nr_guards, d_guards, nm_guards = nat.nr_guards, nat.d_guards, nat.nm_guards


# ---- per-model rules (§2.3, §2.4, §4.3; API.md §8.2, §20 A-6, A-7) ---------------------------
def _sg(b, stat, side) -> int:
    return sign(b[stat][side], b[stat]["g"])


def _nec(b, z1, z5, w, v, suffix="") -> str:
    """The §2.3 table: NECESSARY, COMPLEMENT_LOW_ALIGNED, CODE_DOMINANT, NOT_NECESSARY or INC."""
    l1, u1, l5, u5 = _sg(b, z1, "L"), _sg(b, z1, "U"), _sg(b, z5, "L"), _sg(b, z5, "U")
    low = u1 == -1 and u5 == -1
    if low and _sg(b, w, "L") == 1 and _sg(b, v, "U") == -1:
        return "NECESSARY" + suffix
    if low:
        return CLA + suffix
    if l1 == 1 and u5 == -1:
        return "CODE_DOMINANT" + suffix
    if l5 == 1 and l1 == 1:
        return "NOT_NECESSARY" + suffix
    return "INC/NUMERICAL" if 0 in (l1, u1, l5, u5) else "INC"


def nr_model(b, y_active) -> dict:
    """RESP, SPEC, category, coarse, rule-6 (a), nested, NEGATIVE_COMPLEMENT (§20 A-6)."""
    resp = _sg(b, "V3x", "L") == 1
    spec = bool(y_active) and "Y1" in b and _sg(b, "Y1", "U") == -1
    status = HEADROOM if not resp else NUISANCE if y_active and not spec else None
    formed = status is None
    out = {"resp": resp, "spec": spec, "coarse": {"gt010": False, "lt050": False}}
    out.update(rule6a=False, nested=False, negative=False, endpoint_formed=formed)
    if formed:
        status = _nec(b, "Zc010", "Zc050", "Wc", "Vc")
        u1, u5 = _sg(b, "Zc010", "U"), _sg(b, "Zc050", "U")
        out["coarse"] = {"gt010": _sg(b, "Zc010", "L") == 1, "lt050": u5 == -1}
        out["rule6a"] = _sg(b, "NEGc", "L") == 1 and u1 == -1 and u5 == -1
        has = "Zc090" in b and "Zc100" in b
        out["nested"] = status == "NOT_NECESSARY" and has and _sg(b, "Zc090", "L") == 1
        out["nested"] = out["nested"] and _sg(b, "Zc100", "U") == -1
        out["negative"] = _sg(b, "NEGc", "U") == -1
    return dict(out, status=status, unresolved=cdc._unresolved(b))


def nr_variant_category(b, v, primary) -> str:
    """The variant category on v:Zc010, v:Zc050 (c2_decide.variant_category pattern)."""
    if str(primary["status"]).startswith("EXCLUDED"):
        return primary["status"]
    if f"{v}:Zc010" not in b:
        return NC
    z1, z5 = f"{v}:Zc010", f"{v}:Zc050"
    l1, u1, l5, u5 = _sg(b, z1, "L"), _sg(b, z1, "U"), _sg(b, z5, "L"), _sg(b, z5, "U")
    if u1 == -1 and u5 == -1:
        return CLA
    if l1 == 1 and u5 == -1:
        return "CODE_DOMINANT"
    if l5 == 1 and l1 == 1:
        return "NOT_NECESSARY"
    return "INC/NUMERICAL" if 0 in (l1, u1, l5, u5) else "INC"


def d_model(b, y_active) -> dict:
    """c2_decide.r_model on the DNULL arrays, DECOY_ names, rule-6 (b); y_active = Y1' active."""
    r = cdc.r_model(b, y_active)
    r["status"] = D_CAT.get(r["status"], r["status"])
    r6 = _sg(b, "NEG", "L") == 1 and _sg(b, "Z010", "U") == -1 and _sg(b, "Z050", "U") == -1
    return dict(r, rule6b=bool(r["endpoint_formed"]) and r6)


def dnullr_category(b, primary) -> str:
    """The report-only D-NULL-R category on the DNULLR: arrays (feeds DECOY_LOCATION_DEPENDENT)."""
    cat = cdc.variant_category(b, "DNULLR", primary)
    return D_CAT.get(cat, cat)


def nm_model(b) -> dict:
    """RESP, ROUTED first, the four _M categories on ZMc010, ZMc050, WMc, VMc, rule-6 (c)."""
    resp = _sg(b, "V3x", "L") == 1
    out = {"resp": resp, "spec": False, "transmission": {"gt010": False, "routed": False}}
    out.update(rule6c=False, endpoint_formed=resp, status=HEADROOM)
    if resp:
        lt, ut = _sg(b, "Ztau", "L"), _sg(b, "Ztau", "U")
        if ut == -1:
            out["status"] = "ROUTED"
        elif lt == 1:
            out["status"] = _nec(b, "ZMc010", "ZMc050", "WMc", "VMc", "_M")
        else:
            out["status"] = "INC/NUMERICAL" if 0 in (lt, ut) else "INC"
        out["transmission"] = {"gt010": lt == 1, "routed": ut == -1}
        r6 = _sg(b, "NEGMc", "L") == 1 and _sg(b, "ZMc010", "U") == _sg(b, "ZMc050", "U") == -1
        out["rule6c"] = lt == 1 and r6
    return dict(out, unresolved=cdc._unresolved(b))


# ---- known cases (§3 rows 24-25, §5.2-§5.3; API.md §8.3, §20 B-4) ----------------------------
KNOWN = {
    "D0": ("USED", None),
    "DONLY": ("USED", "NECESSARY"),
    "DDOSE": ("PARTIAL", "NOT_NECESSARY"),
}
KNOWN_R = {"DNULLR": ("NOT_USED", None), "DID": ("USED", None)}


def kc_case(case, b_case, y_active) -> str:
    """PASS, CONTRADICTED (wins) or UNRESOLVED (ND-C17); the case's own RESP/SPEC (ND-C31)."""
    pre = f"{case}:"
    b = {k[len(pre) :]: v for k, v in b_case.items() if k.startswith(pre)}
    y_case = bool(y_active) and "V3y" in b and _sg(b, "V3y", "L") == 1
    known_r, known_n = {**KNOWN, **KNOWN_R}[case]
    got = [(cdc.r_model(b, y_case)["status"], known_r, cdc.CAT)]
    if known_n is not None:
        got.append((nr_model(b, y_case)["status"], known_n, NR_CAT))
    if any(s in cats and s != want for s, want, cats in got):
        return "CONTRADICTED"
    return "UNRESOLVED" if any(s not in cats for s, _, cats in got) else "PASS"


def kc_gate(results) -> dict:
    """KC per model: PASS/FAIL per case only (§6.7 L5); CONTRADICTED wins over UNRESOLVED."""
    vals = set(results.values())
    full = KCC if "CONTRADICTED" in vals else "PASS" if vals <= {"PASS"} else None
    full = full or "EXCLUDED/KNOWN_CASE_UNRESOLVED"
    cases = {c: "PASS" if r == "PASS" else "FAIL" for c, r in results.items()}
    return {"status": "PASS" if full == "PASS" else "FAIL", "full_status": full, "cases": cases}


def kcr_gate(results) -> dict:
    """KC-R per model (report-only): MOVE_CASE_CONTRADICTED, NOT_COMPUTED, UNRESOLVED or PASS."""
    vals = set(results.values())
    if "CONTRADICTED" in vals:
        status, full = "FAIL", "MOVE_CASE_CONTRADICTED"
    elif NC in vals:
        status, full = "NOT_RUN", NC
    else:
        status, full = ("PASS", "PASS") if vals <= {"PASS"} else ("FAIL", "UNRESOLVED")
    cases = {c: r if r in ("PASS", NC) else "FAIL" for c, r in results.items()}
    return {"status": status, "full_status": full, "cases": cases}


# ---- overall rules, statement counts, endpoint statuses (§4.3; API.md §8.4) ------------------
def _cats(family, gen) -> str | None:
    n = {c: gen.count(c) for c in set(gen)}
    if family == "D":
        if n.get("DECOY_NOT_USED", 0) >= 2:
            return "DECOY_NOT_USED"
        if n.get("DECOY_NOT_USED", 0) + n.get("DECOY_LOW_ALIGNED", 0) >= 2:
            return "DECOY_LOW_ALIGNED"
        return next((c for c in ("DECOY_PARTIAL", "DECOY_USED") if n.get(c, 0) >= 2), None)
    s = "_M" if family == "N-M" else ""
    if family == "N-M" and n.get("ROUTED", 0) >= 2:
        return "ROUTED_AROUND"
    if n.get("NECESSARY" + s, 0) >= 2:
        return "NECESSARY" + s
    if n.get("NECESSARY" + s, 0) + n.get(CLA + s, 0) >= 2:
        return CLA + s
    return next((c + s for c in NR_CAT[2:] if n.get(c + s, 0) >= 2), None)


RESOLVED = {"N-R": NR_CAT, "D": tuple(D_CAT.values()), "N-M": NM_CAT + ("ROUTED",)}


def overall(family, statuses, cnhs, kc_contradicted=False) -> str:
    """§4.3 / C2 §6.5 (fatal, D: KNOWN_CASE_CONTRADICTED, CNHS, exclusions, categories)."""
    vals = [str(s) for s in statuses.values()]
    fatal = [s for s in vals if s.startswith(("FAIL_TECHNICAL", "INCONCLUSIVE", "INVALID"))]
    if fatal:
        return fatal[0]
    if family == "D" and (kc_contradicted or KCC in vals):
        return KCC
    cn = {int(j) for j in cnhs} | {int(j) for j, s in statuses.items() if s == "CNHS"}
    if len(cn) >= 2:
        return "CNHS-2" if family == "N-M" else "CIRCLE_NOT_HISTORY_SENSITIVE"
    excl = [s.split("/", 1)[1] for s in vals if s.startswith("EXCLUDED/")]
    if len(vals) - len(excl) - len(cn) < 2:
        order = sorted(excl, key=lambda r: REASON_ORDER.index(r) if r in REASON_ORDER else 99)
        return "INCONCLUSIVE/" + (order[min(1, len(order) - 1)] if order else "PRECISION")
    cat = _cats(family, vals)
    if cat is not None:
        return cat
    return "MIXED" if sum(s in RESOLVED[family] for s in vals) >= 2 else "INCONCLUSIVE/PRECISION"


def statement_count(per_model, flag) -> dict:
    models = sorted(j for j, r in per_model.items() if r.get(flag))
    return {"models": models, "licensed": len(models) >= 2}


def _family_of(rec) -> str | None:
    prob = rec.get("problem")
    by_prob = {"RD": "D", "RT": "D", "R": "N-R", "M": "N-M"}.get(prob)
    return rec.get("family") or by_prob


def endpoint_status(model, family, gate_history) -> str:
    """C2's rule with the ND names: SCORED, NOT_RUN/<gate>, SEALED_UNSCORED/<gate> (ND-C40)."""
    formed = False
    for rec in gate_history:
        m, fam = rec.get("model"), _family_of(rec)
        if (m is not None and int(m) != int(model)) or (fam is not None and fam != family):
            continue
        full = str(rec.get("full_status") or rec.get("status"))
        if rec["gate"] == "ENDPOINT" and full != "NOT_RUN":
            formed = formed or bool((rec.get("values") or {}).get("formed", True))
        if full in ("PASS", "NOT_RUN") or rec["gate"] in NON_EXCLUDING:
            continue
        if rec.get("problem") in nc.VARIANTS + ("RT",) or rec.get("decoy") in nc.KCR_CASES:
            continue
        gate = "T-PRE" if rec["gate"] == "T-PRE-MODEL" else rec["gate"]
        return ("SEALED_UNSCORED/" if formed else "NOT_RUN/") + gate
    return "SCORED"


# ---- qualifiers (§2.3, §7.2-§7.4; API.md §2, §8.4) -------------------------------------------
CLAIM = {c: (c,) for c in NR_CAT + NM_CAT + tuple(D_CAT.values()) + ("ROUTED",)}
CLAIM.update({CLA: ("NECESSARY", CLA), CLA + "_M": ("NECESSARY_M", CLA + "_M")})
CLAIM.update(ROUTED_AROUND=("ROUTED",), DECOY_LOW_ALIGNED=("DECOY_NOT_USED", "DECOY_LOW_ALIGNED"))


def qualifiers(family, per_model, extra, y_active, p1) -> list:
    """The qualifiers in the API.md §2 order, models ascending within each kind (ND-C19, C29)."""
    js, extra = sorted(per_model), extra or {}
    st = {j: per_model[j]["status"] for j in js}
    out = [] if family == "N-M" or y_active else ["SPECIFICITY_NOT_ESTABLISHED"]
    neg = {"N-R": "NEGATIVE_COMPLEMENT", "D": "NEGATIVE_ALIGNED_CONTRIBUTION"}.get(family)
    out += [f"{neg}({j})" for j in js if neg and per_model[j].get("negative")]

    def differs(got, prim):
        return got not in (None, NC) and got != prim

    if family == "N-R":
        var = extra.get("variants", {})
        prim = {j: CLA if s == "NECESSARY" else s for j, s in st.items()}
        dep = [(j, v) for j in js for v in nc.VARIANTS if differs(var.get(j, {}).get(v), prim[j])]
        out += [f"PROJECTOR_DEPENDENT_NR({j})" for j, v in dep if v == "R_E"]
        out += [f"HARMONIC_DEPENDENT_NR({j}, {v[-1]})" for j, v in dep if v != "R_E"]
    if family == "D":
        dn = extra.get("dnullr", {})
        out += [f"DECOY_LOCATION_DEPENDENT({j})" for j in js if differs(dn.get(j), st[j])]
        for key, name in (("kcr", "MOVE_CASE_CONTRADICTED"), ("kc_test", "KC_TEST_DISAGREES")):
            got = extra.get(key, {})
            out += [f"{name}({j}, {c})" for j in sorted(got) for c in got[j]]
    out += [f"PRECISION_LIMITED({j})" for j in sorted((p1 or {}).get("precision_limited", []))]
    claim = CLAIM.get(overall(family, st, []))
    out += [f"DISSENT({j}: {st[j]})" for j in js if claim and st[j] not in claim]
    return out


# ---- licences, package statement, caveat (§7; API.md §8.4, §20 R-0121-2) ---------------------
_TEXT = """
NECESSARY|In [k] of 3 models, setting every readout coordinate except the six registered code
coordinates to its counterfactual value, with the code held, carries between −10% and 10% of the
model's signed oracle-aligned response (ψ̂_comp [psi_comp], bounds [bounds]) and less than 10% of
its centred logit-change energy. With C2's USED, the registered code is sufficient and necessary for
this readout response in this sense.
COMPLEMENT_LOW_ALIGNED|In [k] of 3 models, the complement's signed aligned share is below 10% (it
may be negative), but either its total logit-change energy was not shown below 10% or the share was
not shown above −10%. This is not a necessity result.
CODE_DOMINANT|In [k] of 3 models, the complement interchange carries between 10% and 50% of the
signed oracle-aligned response (ψ̂_comp [psi_comp], bounds [bounds]): the registered code is the
main carrier of this readout response, not the only one. At this linear readout this is the same
quantity as one minus C2's code share, replicated on fresh histories.
VARIANT|The size of the remainder depends on how 'everything except the code' is defined; under
[variant] its category is [variant_category] (ψ̂_comp^v [psi_comp_v]; below 10% only if that
category is COMPLEMENT_LOW_ALIGNED).
NOT_NECESSARY|In [k] of 3 models, the complement alone carries more than half of the signed
oracle-aligned response (ψ̂_comp [psi_comp], bounds [bounds]).
PRECISION|The fresh test could not resolve the share against 0.10 and 0.50 in two models
([intervals]).
NECESSARY_M|In [k] models, the layer-2 complement interchange in the source context carries between
−10% and 10% of the signed aligned effect of the full layer-2 interchange (ψ̂_M,comp [psi_M_comp],
bounds [bounds]) and less than 10% of its centred logit-change energy.
COMPLEMENT_LOW_ALIGNED_M|In [k] models, the layer-2 complement's signed aligned share is below 10%
of the full layer-2 interchange's (it may be negative), but either its energy was not shown below
10% or the share was not shown above −10%. This is not a necessity result.
CODE_DOMINANT_M|In [k] models, the layer-2 complement interchange in the source context carries
between 10% and 50% of the signed aligned effect of the full layer-2 interchange (ψ̂_M,comp
[psi_M_comp]); the interaction share is [iota_M] (descriptive).
NOT_NECESSARY_M|In [k] models, the layer-2 complement interchange alone carries more than half of
the signed aligned effect of the full layer-2 interchange (ψ̂_M,comp [psi_M_comp], bounds [bounds]).
KM3|The layer-2 complement includes LayerNorm-scale effects: changing the non-code coordinates
rescales the code inside block 3 and at the final LayerNorm, so a code that is the only input the
readout reads need not be shown necessary here.
DECOY_NOT_USED|In [k] of 3 models, on a decoy that keeps the circle code bitwise in the activations
(the same link and registration gates pass) but whose readout ignores it exactly, while responding
to the counterfactual at [theta_prime] of the oracle contrast through its other readout directions
(gain ×6, fixed in advance), the registered method, re-estimating the code on fresh data, returned
NOT_USED (ψ̂′ [psi_prime], upper bounds [upper]; energy share [energy]). The method also returned
the constructed answer on every core known case at validation (code-only head: used and necessary;
partial dose: partial; base model: used). Report-only cases: moved code [moved], compensated move
[compensated]. Unamplified decoy: response [unamplified] against the 0.30 gate.
DECOY_LOW_ALIGNED|In [k] of 3 models, the aligned share of the decoy's response attributed to the
code was below 10%, but its energy was not bounded (ψ̂′ [psi_prime], bounds [bounds]).
DECOY_PARTIAL|In [k] of 3 models, the method attributed between 10% and 50% of the decoy's response
to a code that the decoy provably does not read (ψ̂′ [psi_prime], bounds [bounds]).
DECOY_USED|In [k] of 3 models, the method called an unread code used (ψ̂′ [psi_prime], bounds
[bounds]).
KNOWN_CASE_CONTRADICTED|At validation the method returned [category] on [case], whose constructed
answer is [known].
QN2|At the linear readout the complement share equals one minus the code share by an exact identity;
it is not an independent measurement.
QD|These outcomes concern constructed decoys of the three models in which the readout of the
registered code is removed or rescaled by an exact head edit, while the code stays in the
activations. They show whether the frozen recipe, re-estimated on fresh data, returns NOT_USED when
the readout provably ignores the code. The decoy's remaining readout can still depend on the
upstream code through the LayerNorm scale; this is outside the registered interchange. They do not
show that every form of non-use would be detected, that NOT_USED on a natural model would be
correct, or that the C2 result excludes every alternative mechanism.
GAIN|The decoy's remaining readout is amplified by a gain of 6, fixed in advance, and the readout of
the code is removed by an exact edit of the output head.
rule6a|In [k] models the complement interchange carries a certified positive share of the signed
oracle-aligned response that is below the 10% margin (ψ̂_comp [psi_comp], bounds [bounds]): a
positive but below-margin contribution of everything except the code.
rule6b|In [k] models the method attributed a small, certified positive share (below 10%; ψ̂′
[psi_prime], bounds [bounds]) to a code the decoy does not read.
rule6c|In [k] models the layer-2 complement interchange carries a certified positive share below the
10% margin (ψ̂_M,comp [psi_M_comp], bounds [bounds]).
nested|In [k] models the complement alone carries more than half of the signed oracle-aligned
response, and the registered code's own share is certified positive but below 10% (ψ̂ [psi]).
PACKAGE|At position 32 of the final readout, setting the six registered code coordinates to the
counterfactual's values carries more than half of the model's signed aligned response (C2); setting
everything else carries between 10% and 50% (C2ND, fresh histories; the same quantity as one minus
the code share); and on decoys of the same models in which the code is present but unread, the same
method returns not used (C2ND).
"""
_ENTRY = re.compile(r"^(\w+)\|(.*?)(?=^\w+\||\Z)", re.S | re.M)
T = {k: " ".join(v.split()) for k, v in _ENTRY.findall(_TEXT)}
Q = {"N-R": cdc.QCODE["R"] + " " + T["QN2"], "D": T["QD"] + " " + T["GAIN"]}
Q["N-M"] = cdc.T["M_CAVEAT"] + " " + cdc.QCODE["M"] + " " + T["KM3"]
_GEN = (("FAIL_TECHNICAL", "FAIL"), ("INCONCLUSIVE/PRECISION", "PRECISION"))
_GEN += (("INCONCLUSIVE", "INCONCLUSIVE"), ("MIXED", "MIXED"), ("C", "CNHS"))


def _fill(text, values) -> str:
    def one(m):
        return cdc._fmt(values[m.group(1)]) if m.group(1) in values else "[ ]"

    return re.sub(r"\[(\w+)\]", one, text)


def _sentence(family, outcome, values) -> str:
    key = "M_ROUTED" if outcome == "ROUTED_AROUND" else str(outcome)
    if key not in T and key not in cdc.T:
        key = next(k for p, k in _GEN if key.startswith(p))
        key = "M_CNHS" if key == "CNHS" and family == "N-M" else key
    text = T.get(key) or cdc.T[key]
    return text + (" " + T["VARIANT"] if key == "CODE_DOMINANT" and "variant" in values else "")


def licence(family, outcome, values) -> str:
    """The §7.2-§7.4 sentence, [name] filled ("[ ]" if absent), then the family's Q-CODE."""
    return _fill(_sentence(family, outcome, values) + " " + Q[family], values)


def statement_licence(kind, values) -> str:
    """rule6a, rule6b, rule6c (with the C2-M caveats and KM3) or nested (§7.2-§7.4)."""
    return _fill(T[kind] + (" " + cdc.T["M_CAVEAT"] + " " + T["KM3"]) * (kind == "rule6c"), values)


def package_statement(c2_outcome, nr, d) -> str | None:
    """§7.5, only if C2-R USED, N-R CODE_DOMINANT (or NECESSARY) and D DECOY_NOT_USED."""
    ok = c2_outcome == "USED" and nr in ("CODE_DOMINANT", "NECESSARY") and d == "DECOY_NOT_USED"
    return " ".join((T["PACKAGE"], Q["N-R"], T["QD"])) if ok else None


def c2_caveat(d_outcome) -> str | None:
    """Owner default (§7.3, Q4): every C2 statement carries this until the owner decides."""
    bad = d_outcome in ("DECOY_PARTIAL", "DECOY_USED")
    return "specificity not established on the decoy" if bad else None
