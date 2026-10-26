"""C2 decisions: the family bound streams, the NUM guard, the Lemma FW per-model rules (R, S*, M),
the coarse statements and their prerequisites, the 2-of-3 rule, endpoint statuses, qualifiers
and the Q-CODE licence fill (API.md §11; C2-FROZEN-v1 §3, §6.2-§6.5, §9.2, §10).

`b` is one model's {statistic: {"mean", "L", "U", "rank_L", "rank_U", "g"}} (API.md §19.1 E-6);
a bound inside its guard counts as neither > 0 nor < 0 (NUMERICALLY_UNRESOLVED).
"""

from __future__ import annotations

import re

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_means
import numpy as np

HEADROOM, NUISANCE = "EXCLUDED/MODEL_HEADROOM", "EXCLUDED/NUISANCE_IN_S"
CAT = ("USED", "PARTIAL", "NOT_USED", "LOW_ALIGNED")
M_CAT = {c: "UPSTREAM_" + c for c in CAT}
_GEN = ("USED", "NOT_USED", "PARTIAL", "LOW")
OUT = {"R": dict(zip(_GEN, ("USED", "NOT_USED", "PARTIAL", "LOW_ALIGNED_SHARE")))}
OUT["R"]["CNHS"] = "CIRCLE_NOT_HISTORY_SENSITIVE"
OUT["S*"] = {k: "X_PHASE_" + ("LOW_ALIGNED" if k == "LOW" else k) for k in _GEN}
OUT["S*"]["CNHS"] = "X_PHASE_NOT_HISTORY_SENSITIVE"
OUT["M"] = {k: "UPSTREAM_" + ("LOW_ALIGNED" if k == "LOW" else k) for k in _GEN}
OUT["M"].update(CNHS="CNHS-2", ROUTED="ROUTED_AROUND")
REASON_ORDER = tuple("CHART_UNAVAILABLE PATCH_MODEL_DEGENERATE NUMERICAL LINK".split())
REASON_ORDER += tuple("RADIAL_SUPPORT MODEL_HEADROOM NUISANCE_IN_S UNDERPOWERED TEST_GATE".split())
NON_EXCLUDING = ("V3y", "NUM", "ENDPOINT", "REPORT", "IMPL", "ACCEPT")
A_STATS = ("Z010", "Z050", "NEG", "Y1", "Y1*")
_PREFIX = (("FAIL_TECHNICAL", "FAIL"), ("INCONCLUSIVE/PRECISION", "PRECISION"))
_PREFIX += (("INCONCLUSIVE", "INCONCLUSIVE"), ("MIXED", "MIXED"))


# ---- bounds and the NUM guard (§6.2, §9.2; API.md §11) ---------------------------------------
def stream_bounds(arrays, seed, alpha, draws=20000) -> dict:
    """One shared index stream; per key the tree mean and the ranked bounds at alpha, 1 - alpha."""
    means = c1_means.bootstrap_means(arrays, seed, draws)
    out = {}
    for k, x in arrays.items():
        L, rL = c1_means.quantile_with_rank(means[k], alpha)
        U, rU = c1_means.quantile_with_rank(means[k], 1 - alpha)
        out[k] = {"mean": float(c1_means.tree_mean(x)), "L": L, "U": U, "rank_L": rL, "rank_U": rU}
    return out


def guard(s, beta=0.0) -> float:
    return float(cc.frac(cc.GUARD_REL)) * max(1.0, float(np.mean(np.abs(s)))) + float(beta)


def _rows(x, E=None):
    x = np.asarray(x, dtype=np.float64)
    return x if E is None else x[np.asarray(E, dtype=bool)]


def beta_A(d, M, dy, delta_P, coef, E=None) -> float:
    """|coef| max_i 1/2 ||M' d_i|| delta_P ||dy_i|| (A_S-type terms)."""
    md = np.linalg.norm(_rows(d, E) @ np.asarray(M), axis=1)
    b = 0.5 * md * float(delta_P) * np.linalg.norm(_rows(dy, E), axis=1)
    return abs(float(coef)) * float(np.max(b)) if b.size else 0.0


def beta_E(M, dy, P_S, delta_P, coef, E=None) -> float:
    """|coef| max_i (2 ||C M P_S dy_i|| + ||CM|| delta_P ||dy_i||) ||CM|| delta_P ||dy_i||."""
    CM, dy = np.asarray(M, dtype=np.float64), _rows(dy, E)
    CM = CM - CM.mean(axis=0)
    nCM, ndy = float(np.linalg.norm(CM, 2)), np.linalg.norm(dy, axis=1)
    v = np.linalg.norm((dy @ np.asarray(P_S).T) @ CM.T, axis=1)
    t = nCM * float(delta_P) * ndy
    return abs(float(coef)) * float(np.max((2 * v + t) * t)) if t.size else 0.0


def sign(b, g) -> int:
    return 1 if b > g else -1 if b < -g else 0


def stream_guards(arrays, geo) -> dict:
    """Guards of one R/S* stream; geo: M, x/y = (d, dy, E), proj = {prefix: (P_S, delta_P)}."""
    M, (d, dy, Ex), (dR, dyR, Ey) = geo["M"], geo["x"], geo["y"]
    out = {}
    for name, s in arrays.items():
        prefix, _, stat = name.rpartition(":")
        P, dP = geo["proj"][prefix + ":" if prefix else ""]
        if stat in ("Vabs", "Vrand"):
            beta = beta_E(M, dy, P, dP, 1, Ex)
        else:
            dd, yy, EE = (dR, dyR, Ey) if stat in ("Y1", "Y1*") else (d, dy, Ex)
            beta = beta_A(dd, M, yy, dP, 1, EE) if stat in A_STATS else 0.0
        out[name] = guard(s, beta)
    return out


def model_bounds(res, guards, model) -> dict:
    """The stream_bounds entries of one model keyed by statistic, each with its guard."""
    tail = f"|{model}"
    n = len(tail)
    return {k[:-n]: dict(v, g=guards[k[:-n]]) for k, v in res.items() if k.endswith(tail)}


# ---- per-model rules (§6.3, §6.4; API.md §11.2) ----------------------------------------------
def _sg(b, stat, side) -> int:
    return sign(b[stat][side], b[stat]["g"])


def _category(b, z1, z5, energy) -> str:
    l1, u1, l5, u5 = _sg(b, z1, "L"), _sg(b, z1, "U"), _sg(b, z5, "L"), _sg(b, z5, "U")
    if l5 == 1 and l1 == 1:
        return "USED"
    if l1 == 1 and u5 == -1:
        return "PARTIAL"
    if u1 == -1 and u5 == -1:
        return "NOT_USED" if all(_sg(b, e, "U") == -1 for e in energy) else "LOW_ALIGNED"
    return "INC/NUMERICAL" if 0 in (l1, u1, l5, u5) else "INC"


def _unresolved(b) -> list:
    return [f"{s}:{side}" for s in b for side in ("L", "U") if _sg(b, s, side) == 0]


RES_KEYS = ("status", "resp", "spec", "coarse", "negative", "unresolved", "endpoint_formed")


def _result(b, status, resp, spec, coarse, formed) -> dict:
    neg = formed and _sg(b, "NEG", "U") == -1
    return dict(zip(RES_KEYS, (status, resp, spec, coarse, neg, _unresolved(b), formed)))


def _gate(b, spec_stat, y_active) -> tuple:
    resp = _sg(b, "V3x", "L") == 1
    spec = bool(y_active) and spec_stat in b and _sg(b, spec_stat, "U") == -1
    status = HEADROOM if not resp else NUISANCE if y_active and not spec else None
    return resp, spec, status


def r_model(b, y_active) -> dict:
    """R and S* rules 1-5; NEGATIVE and the coarse statements only after RESP and SPEC."""
    spec_stat = "Y1" if "Y1" in b else "Y1*"
    resp, spec, status = _gate(b, spec_stat, y_active)
    formed = status is None
    if formed:
        status = _category(b, "Z010", "Z050", ("Vabs", "Vrand"))
    gt, lt = formed and _sg(b, "Z010", "L") == 1, formed and _sg(b, "Z050", "U") == -1
    return _result(b, status, resp, spec, {"gt010": gt, "lt050": lt}, formed)


def m_model(b, y2_active) -> dict:
    """M rules 1-7: RESP, Y2, ROUTED first, the UPSTREAM categories, INC (E-7)."""
    resp, spec, status = _gate(b, "Y2", y2_active)
    formed = status is None
    if formed:
        lt, ut = _sg(b, "Ztau", "L"), _sg(b, "Ztau", "U")
        if ut == -1:
            status = "ROUTED"
        elif lt == 1:
            cat = _category(b, "ZM010", "ZM050", ("VM",))
            status = M_CAT.get(cat, cat)
        else:
            status = "INC/NUMERICAL" if 0 in (lt, ut) else "INC"
    return _result(b, status, resp, spec, {}, formed)


def variant_category(b, variant, primary) -> str:
    """The R category rule on the variant arrays, with the primary RESP/SPEC prerequisites."""
    if str(primary["status"]).startswith("EXCLUDED"):
        return primary["status"]
    if f"{variant}:Z010" not in b:
        return "NOT_COMPUTED"
    v = f"{variant}:"
    return _category(b, v + "Z010", v + "Z050", (v + "Vabs", v + "Vrand"))


# ---- overall rules, endpoint statuses, qualifiers (§6.5, §3.1, §10) --------------------------
def _generic(family, status) -> str | None:
    s = str(status)
    if family == "M":
        s = {v: k for k, v in M_CAT.items()}.get(s, s)
    return {"LOW_ALIGNED": "LOW"}.get(s, s) if s in CAT or s == "ROUTED" else None


def overall(family, statuses, cnhs) -> str:
    """§6.5: study failure; >= 2 CNHS; fewer than 2 valid models -> INCONCLUSIVE/<the reason of
    the exclusion that left fewer than 2>; the categories (M: ROUTED first); MIXED; PRECISION."""
    names, vals = OUT[family], [str(s) for s in statuses.values()]
    fatal = [s for s in vals if s.startswith(("FAIL_TECHNICAL", "INCONCLUSIVE", "INVALID"))]
    if fatal:
        return fatal[0]
    cn = {int(j) for j in cnhs} | {int(j) for j, s in statuses.items() if s == "CNHS"}
    if len(cn) >= 2:
        return names["CNHS"]
    excl = [s.split("/", 1)[1] for s in vals if s.startswith("EXCLUDED/")]
    if len(vals) - len(excl) - len(cn) < 2:
        order = sorted(excl, key=lambda r: REASON_ORDER.index(r) if r in REASON_ORDER else 99)
        return "INCONCLUSIVE/" + (order[min(1, len(order) - 1)] if order else "PRECISION")
    gen = [_generic(family, s) for s in vals]
    for cat in (("ROUTED",) if family == "M" else ()) + ("USED", "NOT_USED", "PARTIAL"):
        if gen.count(cat) >= 2:
            return names[cat]
    if gen.count("NOT_USED") + gen.count("LOW") >= 2:
        return names["LOW"]
    return "MIXED" if sum(g is not None for g in gen) >= 2 else "INCONCLUSIVE/PRECISION"


def _applies(rec, model, family) -> bool:
    prob = rec.get("problem")
    fam = rec.get("family") or (prob if prob in cc.FAMILIES else None)
    m = rec.get("model")
    return (m is None or int(m) == int(model)) and (fam is None or fam == family)


def endpoint_status(model, family, gate_history) -> str:
    """SCORED; NOT_RUN/<gate> for the first applicable stop (exclusion before ACCEPT, T-PRE,
    T-PRE-MODEL as "T-PRE", RESP-SPEC, a stopped family or study); SEALED_UNSCORED/<gate> only
    after the endpoint arrays were formed (NEW-6). POST-DESC never changes it."""
    formed = False
    for rec in gate_history:
        if not _applies(rec, model, family):
            continue
        full = str(rec.get("full_status") or rec.get("status"))
        if rec["gate"] == "ENDPOINT" and full != "NOT_RUN":
            formed = formed or bool((rec.get("values") or {}).get("formed", True))
        if full in ("PASS", "NOT_RUN") or rec["gate"] in NON_EXCLUDING:
            continue
        if rec.get("problem") in cc.VARIANTS:
            continue
        gate = "T-PRE" if rec["gate"] == "T-PRE-MODEL" else rec["gate"]
        return ("SEALED_UNSCORED/" if formed else "NOT_RUN/") + gate
    return "SCORED"


CLAIM = {k: (k,) for k in ("USED", "NOT_USED", "PARTIAL", "ROUTED")}
CLAIM["LOW"] = ("NOT_USED", "LOW")


def qualifiers(family, per_model, variants, y_active, p1) -> list:
    """The §3.1 qualifiers in the API.md §2 order, models ascending within each kind."""
    js = sorted(per_model)
    out = [] if y_active else ["SPECIFICITY_NOT_ESTABLISHED"]
    out += [f"NEGATIVE_ALIGNED_CONTRIBUTION({j})" for j in js if per_model[j].get("negative")]
    if family == "R":
        variants = variants or {}

        def differs(j, v):
            got = variants.get(j, {}).get(v)
            return got not in (None, "NOT_COMPUTED") and got != per_model[j]["status"]

        out += [f"PROJECTOR_DEPENDENT({j})" for j in js if differs(j, "R_E")]
        jk = [(j, K) for j in js for K in (1, 2) if differs(j, f"R_K{K}")]
        out += [f"HARMONIC_DEPENDENT({j}, {K})" for j, K in jk]
    out += [f"PRECISION_LIMITED({j})" for j in sorted((p1 or {}).get("precision_limited", []))]
    statuses = {j: per_model[j]["status"] for j in js}
    outcome = overall(family, statuses, [])
    cat = next((k for k, v in OUT[family].items() if v == outcome and k in CLAIM), None)
    if cat is not None:
        dissent = [j for j in js if _generic(family, statuses[j]) not in CLAIM[cat]]
        out += [f"DISSENT({j}: {statuses[j]})" for j in dissent]
    return out


# ---- licences (§3; API.md §11.2, §19.1 E-2, E-12) --------------------------------------------
_TEXT = """
Q|These outcomes concern the frozen, nuisance-excluding linear code defined by {} fit and
projector. They do not exclude predictive use of phase information in excluded directions,
higher harmonics, interactions, or other encodings.

CNHS|In models [list], the registered {} coordinate failed the specified directional
registration criterion on FEAS (sign agreement [registration] < 0.75 on the larger half of the
oracle phase changes; L1 passed: R²_code|0 [R2_code_0], incremental ratio [rho_inc]); this is an
assay-registration finding, not evidence that the representation carries no history.

LOW|In [k] models the signed oracle-aligned contribution of the registered {} interchange is
below 10% of {}, but its total logit-change energy was not shown to be below the bound, so
movement of the logits in other directions, or per-row cancellation, is not excluded. This is
not a {} result.

FAIL|No statement about the models: an identity, lineage, oracle, model or numerical-integrity
defect was found at gate [gate] ([values]).

INCONCLUSIVE|The assay was infeasible as specified at gate [gate] ([values]; per model
[statuses]; endpoints NOT_RUN for [models]).

PRECISION|The fresh test could not resolve ψ against 0.10 and 0.50 in two models ([intervals]).

MIXED|Per-model statuses [statuses]; no 2-of-3 claim is supported.

USED|In [k] of the 3 models ([list]; the other: [other]), the registered code interchange
carries more than half of the signed oracle-aligned response: setting the six circle-code
coordinates of the final LayerNorm output at position 32 to their values under the
counterfactual history, with every other coordinate held fixed, gives ψ̂ = [psi_hat] (one-sided
lower bounds [lower]) of the model's signed oracle-aligned response to a ±2-cell rotation of
the x-history with the last symbol kept. The models respond to this counterfactual (θ_full >
0.30).

NOT_USED|In [k] of the 3 models, the registered interchange has a low signed oracle-aligned
share and a bounded mean-square centred-logit effect: the circle code moves with the
counterfactual on FEAS (registration [registration]) and the model responds (θ_full > 0.30),
yet setting the code to its counterfactual value gives a signed oracle-aligned contribution
below 0.10 of the model's signed oracle-aligned response (the contribution may be negative,
i.e. opposing; NEGATIVE_ALIGNED_CONTRIBUTION in models [models]), and its total effect on the
centred logits has less than 10% of the mean-square energy of the full natural response and
less than 127/60 times the energy that a Σ_ε-whitened random six-dimensional subspace carries
in expectation on the same rows. The position-32 readout does not use this registered code
interchange beyond this bound.

PARTIAL|In [k] models the registered code interchange carries more than 10% and less than 50%
of the signed oracle-aligned response (ψ̂ [psi_hat], bounds ([lower], [upper])); ψ̂_Γ, ψ̂_rest
are reported descriptively.

PLACEBO|The mean signed placebo contribution is below 0.10 times the mean full placebo
contrast.

M_ROUTED|In [k] models, the signed oracle-aligned effect of the full layer-2 final-position
interchange, in the fixed source context, is below 10% of the natural contrast (τ̂_M
[tau_hat]). This does not distinguish weak transfer, opposition, cancellation, interaction,
context incompatibility, or compensation, and does not establish routing around the circle.

M_USED|In [k] models, the full layer-2 final-position interchange carries more than 10% of the
natural contrast (τ̂_M [tau_hat]), and the registered layer-2 code interchange, in the source
context, carries more than half of the signed oracle-aligned effect of the full interchange
(ψ̂_M [psi_M_hat]). The layer-2 code intervention changes the final output after the remaining
computation, including the residual skip.

M_NOT_USED|In [k] models, the full interchange carries more than 10% (τ̂_M [tau_hat]), but the
registered layer-2 code interchange has a low signed oracle-aligned share (below 0.10 of the
full interchange's, possibly negative) and a bounded mean-square centred-logit effect (below
10% of the full interchange's energy).

M_PARTIAL|In [k] models the registered layer-2 code interchange carries between 10% and 50% of
the full interchange's signed oracle-aligned effect (ψ̂_M [psi_M_hat]).

M_CAVEAT|Caveats: a patched final-position state combined with a context from H is never
produced naturally (it is the intended interchange counterfactual); N2 is a radial support
screen, which assesses neither the joint law of the interchanged state nor its compatibility
with the source prefix's keys and values; the residual skip is part of every M effect; only
position 32 is tested; self-repair can lower τ_M.

ROT|Rotating the six-dimensional circle code within its own coordinates by ±θ (harmonic k by
kθ, frozen orientation §2.11), with every other coordinate held fixed, moved the model's
prediction in the direction of the prediction of the belief obtained by rotating the
pre-last-symbol belief by ±[m] cells and re-applying the last symbol, by θ̂_rot = [theta_rot]
of that belief contrast (95% interval [interval], descriptive; sign agreement s_rot =
[s_rot]). The dose names a latent pre-observation rotation. The code-coordinate rotation is a
descriptive proxy whose posterior phase and shape need not match that oracle counterfactual.

S_SUB|the circle code=the six-dimensional code of the oracle x-phase (harmonics 1–3 of arg m32
of the exact belief);registered code interchange=registered oracle-phase code interchange;six
circle-code=six oracle-phase code;first-harmonic phase coordinate=first-harmonic oracle-phase
coordinate
"""
T = {k: " ".join(v.split()) for k, v in (e.split("|", 1) for e in _TEXT.strip().split("\n\n"))}
QCODE = {f: T["Q"].format(w) for f, w in (("R", "this"), ("M", "the layer-2"))}
QCODE["S*"] = T["Q"].format("the oracle x-phase")
S_SUB = [tuple(x.split("=")) for x in T["S_SUB"].split(";")]
_R_LOW = ("code", "the model's signed oracle-aligned response", "NOT_USED")
_M_LOW = ("layer-2 code", "the signed oracle-aligned effect of the full layer-2 interchange")
T["M_LOW"] = T["LOW"].format(*_M_LOW, "UPSTREAM_NOT_USED")
T["LOW"] = T["LOW"].format(*_R_LOW)
T["M_CNHS"] = T["CNHS"].format("layer-2 first-harmonic phase")
T["CNHS"] = T["CNHS"].format("first-harmonic phase")


def _fmt(x) -> str:
    if isinstance(x, (float, np.floating)):
        return format(float(x), ".4g")
    if isinstance(x, tuple) and len(x) == 2:
        return f"({_fmt(x[0])}, {_fmt(x[1])})"
    return ", ".join(_fmt(v) for v in x) if isinstance(x, (list, tuple)) else str(x)


def _key(family, outcome) -> str:
    gen = {v: k for k, v in OUT[family].items()}.get(outcome)
    if gen is not None:
        return gen
    for prefix, key in _PREFIX:
        if str(outcome).startswith(prefix):
            return key
    raise ValueError(f"no licence for {family} {outcome}")


def licence(family, outcome, values) -> str:
    """The §3 sentence, [name] filled (absent: "[ ]"), then the §3.2 caveats (M) and Q-CODE."""
    if family == "ROT":
        text = T["ROT"]
    else:
        key = _key(family, outcome)
        text = T["M_" + key] if family == "M" and "M_" + key in T else T[key]
        if family == "S*":
            for a, b in S_SUB:
                text = text.replace(a, b)
            text += " ZERO_MOD counts: [zero_mod]."
        if key == "USED" and family != "M" and values.get("y_active"):
            text += " " + T["PLACEBO"]
        text += (" " + T["M_CAVEAT"] if family == "M" else "") + " " + QCODE[family]
    return re.sub(
        r"\[(\w+)\]", lambda m: _fmt(values[m.group(1)]) if m.group(1) in values else "[ ]", text
    )
