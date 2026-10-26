"""C2 stage body S5 (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §3, §5.7, §6.2-§6.5, §7 rows
21-28, §8 S4/S5/S8): ACCEPT, REG2, T-PRE, T-PRE-MODEL, RESP-SPEC, NUM, ENDPOINT, REPORT (with the
§2.12 descriptives and POST-DESC). Endpoint arrays exist only for admitted models and only after
T-PRE (NEW-6); the sealed VAL values are opened only in REPORT, after every outcome."""

from __future__ import annotations

from fractions import Fraction

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_endpoint
import c2_attrib as ca
import c2_data as cd
import c2_decide as cdc
import c2_driver as cdr
import c2_model as cm
import c2_oracle as co2
import c2_registry as cg
import c2_stage_base as sb
import c2_stage_pre as pre
import c2_stage_val as sv
import numpy as np
from c2_stage_base import EXC, FAM, OK, X3, alive, bundle, fitb, js, orc, prob, rec
from c2_stage_val import sg

SEED = {"R": "test_R", "M": "test_M", "S*": "test_S"}
SPEC = {"R": "Y1", "S*": "Y1*", "M": "Y2"}
TEST_GATE = EXC + "TEST_GATE"


def _on(ctx, fam, j) -> bool:
    g = js(ctx, "stages/S4/gates.json")
    return bool(g["y2_on" if fam == "M" else "y_on"].get(str(j)))


def _E(ctx, p, split="test") -> np.ndarray:
    return orc(ctx, split)[f"E_{p}"].astype(bool)


def tb(arrays, guards, fam, draws=cc.TEST_DRAWS) -> dict:
    return sv.bounds(arrays, guards, SEED[fam], cc.ALPHA[fam], draws)


# ---- ACCEPT, REG2, T-PRE, T-PRE-MODEL (§7 rows 21-24) ----------------------------------------
def accept(ctx) -> dict:
    r, rel = cdr.release_ok(ctx, "S5"), js(ctx, "RELEASE_R5.json")
    v = {k: rel.get(k) for k in ("N_test", "k", "accept_review_sha256")}
    return {"status": "PASS" if r["ok"] else "FAIL_TECHNICAL/AUTHORITY", "values": v}


def reg2(ctx) -> dict:
    """R' = R u U_FIT u U_FEAS u U_VAL rebuilt (C-10); then k TEST blocks sampled once, with the
    Y-donor preparation (H2', NEW-10) and separation against C2-REG2."""
    man = cg.build("C2-REG2", ctx.store, extra={s: sb.table(ctx, s) for s in cc.SPLIT_BLOCKS})
    sb.reg_files(ctx, "C2-REG2")
    if man["status"] != "PASS":
        return {"status": man["status"], "values": {"problems": man.get("problems")}}
    return sb.sample(ctx, {"test": int(js(ctx, "RELEASE_R5.json")["k"])}, "C2-REG2")


def t_pre(ctx) -> dict:
    """§7 row 23 in order; FAIL_TECHNICAL ends it at once, unmet criteria give TEST_GATE."""
    P, fz, T, v = sb.proc(ctx), js(ctx, "oracle/ORACLE_FROZEN.json"), sb.table(ctx, "test"), {}
    h1 = co2.h1_static(P)
    v["H1"] = h1["checks"]
    if h1["status"] != "PASS":
        return {"status": h1["status"], "values": v}
    o, el, lam, _ = pre.oracle_splits(ctx, ("test",), float(fz["s_max"]))
    o, el = o["test"], el["test"]
    sb.save_oracle(ctx, "test", o, el)
    ctx.data["cov"] = {"tally": cd.coverage_tally(co2.reason_flags(o, float(fz["s_max"])))}
    ctx.data["cov"]["lambda_x"] = v["lambda_x"] = lam["test"]
    sp = {"test": (T["canonical"], o, el["E_x"], el["E_y"], T["sequence_id"])}
    h3 = v["H3"] = co2.h3(
        P["T"], P["E_canon"][sb.J1], P["pi"], P["coords"], P["perm"], P["E_named"], sp
    )
    if h3["status"] != "PASS":
        st = h3["status"]
        return {"status": st if st.startswith("FAIL") else "INCONCLUSIVE/TEST_GATE", "values": v}
    f = {p: sb.frac(el[f"E_{p}"]) for p in "xy"}
    v["drift"] = {p: abs(f[p] - Fraction(fz["f"]["val"][p])) for p in "xy"}
    v["H5"] = sb.h5_bounds(orc(ctx, "test"), cc.seed("test_H5"))
    rows, bad = cd.lowest(T["sequence_id"], cc.M0_ROWS), []
    for j in cc.MODELS:
        X = bundle(ctx, "test", j, kind="x1")
        a = {s: X["H"]["a"][s][rows] for s in cc.SITES}
        v[f"M0|{j}"] = cm.identity_patch(sb.models(ctx)[j][0], X["H"]["inp"][rows], a, ctx.policy)
        x = v[f"X1|{j}"] = sv.x1_run(ctx, "test", j)
        hooks = {f"{r}_{cc.HOOK_KEYS[s]}": X[r]["a"][s] for r in cc.ROLES for s in cc.SITES}
        sb.put(ctx, f"stages/S5/ACT_TEST_{j}.npz", **{f"{r}_phi": X[r]["phi"] for r in X3}, **hooks)
        bad += [] if all(v[f"M0|{j}"].values()) else ["FAIL_TECHNICAL/MODEL"]
        bad += [] if x["status"] == "PASS" else [x["status"]]
    sb.putj(ctx, "stages/S5/tpre.json", v)
    crit = v["H5"]["ok"] and all(d <= cc.F_DRIFT for d in v["drift"].values())
    return {"status": bad[0] if bad else "PASS" if crit else "INCONCLUSIVE/TEST_GATE", "values": v}


def t_pre_model(ctx) -> dict:
    """§7 row 24: Sup(TEST), L1 and R1 with the frozen FIT decoders, N2 (M); TEST tallies."""
    tally = ctx.data.setdefault("cov", {}).setdefault("models", {})

    def one(j, fam):
        chk, s = {}, sb.support(ctx, "test", j)
        if fam in ("R", "M"):
            chk["sup"] = {"status": "PASS" if s["sup"] >= cc.SUP_MIN else "FAIL", "sup": s["sup"]}
        for name, fn in (("L1", sb.l1_check), ("R1", sb.r1_check)):
            st, val = fn(ctx, "test", j, fam)
            chk[name] = dict(val, status=st)
        if fam == "M":
            st, val = sb.n2_check(ctx, "test", j)
            chk["N2"] = dict(val, status=st)
        un = {k: v for k, v in s.items() if k != "sup"} if fam in ("R", "M") else {}
        tally[f"{fam}|{j}"] = dict(chk["R1"]["tally"], **un)
        return ("PASS" if all(c["status"] == "PASS" for c in chk.values()) else TEST_GATE), chk

    return sb.per(ctx, cc.FAMILIES, one)


# ---- RESP-SPEC, NUM: the family streams (§6.2, §6.3, §9.2) ----------------------------------
def first(ctx, j, fam) -> tuple:
    """V3x and the SPEC array (first part of the family stream; no endpoint array)."""
    ob, (Ex, Ey) = orc(ctx, "test"), (_E(ctx, "x"), _E(ctx, "y"))
    arr = {"V3x": ca.ind(c1_endpoint.Zfull_hat(sb.afull(ctx, "test", j, "x")[2], ob["G_x"]), Ex)}
    if fam == "M":
        q, AR = sv.placebo_m(ctx, "test", j, "test_endpoint")
        arr["Y2"], beta = ca.ind(q["AR_S"] - sb.C1 * q["AR_F"], Ey), 0.0
    else:
        P, M = prob(ctx, j, fam), fitb(ctx, j)["M"]
        d, dy, AR = sb.afull(ctx, "test", j, "y")
        AS = ca.partition(d, M, dy, P["P_S"], P["P_G"])["A_S"]
        arr[SPEC[fam]] = ca.ind(AS - sb.C1 * AR, Ey)
        beta = cdc.beta_A(d, M, dy, P["delta"], 1, Ey)
    return arr, {"V3x": cdc.guard(arr["V3x"]), SPEC[fam]: cdc.guard(arr[SPEC[fam]], beta)}


def keyed(per_model) -> tuple:
    arr = {f"{k}|{j}": v for j, (a, _) in per_model.items() for k, v in a.items()}
    return arr, {f"{k}|{j}": v for j, (_, g) in per_model.items() for k, v in g.items()}


def _split(b, j) -> dict:
    return {k.split("|")[0]: v for k, v in b.items() if k.endswith(f"|{j}")}


def resp_spec(ctx) -> dict:
    ctx.policy.require("test_endpoint")
    recs = []
    for fam in cc.FAMILIES:
        got = {j: first(ctx, j, fam) for j in cc.MODELS if alive(ctx, j, fam)}
        b = tb(*keyed(got), fam)
        for j in got:
            resp, spec, st = cdc._gate(_split(b, j), SPEC[fam], _on(ctx, fam, j))
            recs.append(
                rec(
                    st or "PASS",
                    {"resp": resp, "spec": spec, "bounds": _split(b, j)},
                    model=j,
                    family=fam,
                )
            )
    return sb.lines(recs)


def stream(ctx, j, fam) -> tuple:
    """The whole family stream of one admitted model (§11.1), its guards (§9.2; M: C-44) and the
    quantities kept for REPORT."""
    ob, X, (Ex, Ey) = orc(ctx, "test"), bundle(ctx, "test", j), (_E(ctx, "x"), _E(ctx, "y"))
    if fam == "M":
        q, A = sv.cm_pair(ctx, "test", j, "test_endpoint")
        qR, AR = sv.placebo_m(ctx, "test", j, "test_endpoint")
        arr = ca.m_arrays(q, qR, A, AR, ob["G_x"], Ex, Ey)
        arr.pop("Y2act")
        return arr, {k: cdc.guard(v) for k, v in arr.items()}, dict(q, A_full=A)
    ps = {p: prob(ctx, j, p) for p in cc.PROBLEMS if FAM[p] == fam}
    F, y = {"M": fitb(ctx, j)["M"], "prob": ps}, {r: X[r]["y"] for r in cc.ROLES}
    s = sv.closed_streams(F, y, ob, sb.proc(ctx)["perm"][j])
    proj = {(f"{p}:" if p != fam else ""): (v["P_S"], v["delta"]) for p, v in ps.items() if v["ok"]}
    geo = {
        "M": F["M"],
        "x": (s["d_x"], y["Hp"] - y["Hm"], Ex),
        "y": (s["d_y"], y["H"] - y["HY"], Ey),
    }
    q = dict(s["q"][fam], qy=s["qy"][fam], d=s["d_x"])
    return s[fam], cdc.stream_guards(s[fam], dict(geo, proj=proj)), q


def num(ctx) -> dict:
    """Form the admitted models' endpoint arrays (policy: test_endpoint) and record every
    bound inside its guard (INC_j/NUMERICAL for the affected statement, §6.4 rule 3)."""
    ctx.policy.require_write("test_endpoint")
    recs = []
    for fam in cc.FAMILIES:
        got = {j: stream(ctx, j, fam) for j in cc.MODELS if alive(ctx, j, fam)}
        b = tb(*keyed({j: g[:2] for j, g in got.items()}), fam)
        bj = {j: _split(b, j) for j in got}
        ctx.data[f"bnd:{fam}"] = {
            "b": bj,
            "arr": {j: g[0] for j, g in got.items()},
            "q": {j: g[2] for j, g in got.items()},
        }
        for j in got:
            un = [f"{s}:{x}" for s, v in bj[j].items() for x in "LU" if sg(v, x) == 0]
            recs.append(
                rec("INC/NUMERICAL" if un else "PASS", {"unresolved": un}, model=j, family=fam)
            )
    return sb.lines(recs)


# ---- ENDPOINT (§6.3-§6.5, §3.1) and the rotation arm (§2.11) --------------------------------
def endpoint(ctx) -> dict:
    ctx.policy.require_write("test_endpoint")
    recs, fz, p1 = [], js(ctx, "oracle/ORACLE_FROZEN.json"), js(ctx, "stages/S4/P1.json")
    rep = ctx.data.setdefault("report", {})
    for fam in cc.FAMILIES:
        S, st, per, var = ctx.data.get(f"bnd:{fam}") or {"b": {}}, {}, {}, {}
        for j in cc.MODELS:
            b = S["b"].get(j)
            if b is None:
                st[j] = sb.prior(ctx, j, fam) or "INC"
                per[j] = {"status": st[j], "negative": False}
                continue
            r = per[j] = (cdc.m_model if fam == "M" else cdc.r_model)(b, _on(ctx, fam, j))
            st[j] = r["status"]
            if fam == "R":
                var[j] = {v: cdc.variant_category(b, v, r) for v in cc.VARIANTS}
            sb.put(ctx, f"stages/S5/ENDPOINT_{cc.FILE_FAMILY[fam]}_{j}.npz", **S["arr"][j])
        out = sb.fstop(ctx, fam) or cdc.overall(fam, st, [j for j, s in st.items() if s == "CNHS"])
        act = fz["y_active"] and all(_on(ctx, fam, j) for j in S["b"])
        q = cdc.qualifiers(fam, per, var, act, p1["families"].get(fam)) if S["b"] else []
        v = {
            "outcome": out,
            "formed": bool(S["b"]),
            "statuses": st,
            "qualifiers": q,
            "y_active": act,
        }
        rep[fam] = dict(v, per_model=per, variants=var)
        recs.append(rec(out if S["b"] else "NOT_RUN", v, family=fam))
    js_ = [j for j in cc.MODELS if j in (ctx.data.get("bnd:R") or {"b": {}})["b"]]
    rep["rotation"] = sv.rotation(ctx, js_)
    bnd = {f: (ctx.data.get(f"bnd:{f}") or {}).get("b", {}) for f in cc.FAMILIES}
    sb.putj(ctx, "stages/S5/bounds.json", {"bounds": bnd, "rotation": rep["rotation"]})
    return sb.lines(recs)


# ---- REPORT (§7 row 28; §15.2): descriptives, licences, unsealing, POST-DESC (§5.7) ---------
def quantities(ctx, j, fam) -> dict:
    """x-pair quantities of one model for POST-DESC (formed only now, after every outcome)."""
    if fam == "M":
        q, A = sv.cm_pair(ctx, "test", j, "test_endpoint")
        return {"tau_M": (q["A_F"], A), "psi_M": (q["A_S"], q["A_F"])}
    P, X, (d, _, A) = (
        prob(ctx, j, fam, False),
        bundle(ctx, "test", j),
        sb.afull(ctx, "test", j, "x"),
    )
    q = ca.pair(d, fitb(ctx, j)["M"], X["Hp"]["y"], X["Hm"]["y"], P["P_S"], P["P_G"], P["Sigma"])
    return {"psi": (q["A_S"], A), "theta_full": (A, orc(ctx, "test")["G_x"])}


def post_desc(ctx, G, stop):
    if stop is not None and stop["full_status"] != "INCONCLUSIVE/TEST_GATE":
        return None  # never after a FAIL_TECHNICAL or an INVALID (§5.7)
    arrays, E = {}, _E(ctx, "x")
    for fam in cc.FAMILIES:
        for j in cc.MODELS:
            es = cdc.endpoint_status(j, fam, G)
            if es in ("NOT_RUN/T-PRE", "NOT_RUN/RESP-SPEC") and prob(ctx, j, fam, False)["ok"]:
                for k, (n, d) in quantities(ctx, j, fam).items():
                    arrays[f"{fam}|{j}|{k}"] = {"num": n, "den": d, "E": E, "gate": es[8:]}
    return ca.post_desc(arrays) if arrays else None


def lic_values(ctx, fam, outcome, pm, G, act) -> dict:
    """The §3 bracket values (B3): the claim models and their count from the generic category,
    dissent, point values, the declared bounds, FEAS registration and L1, statuses."""
    cat = next((k for k, v in cdc.OUT[fam].items() if v == outcome and k in cdc.CLAIM), None)
    claim = [j for j in pm if cat and cdc._generic(fam, pm[j]["status"]) in cdc.CLAIM[cat]]
    gv = {(g["gate"], g.get("model")): g.get("values") or {} for g in G if g.get("family") == fam}
    pt = {j: pm[j]["point"] or {} for j in claim}
    bz = {j: (pm[j]["bounds"] or {}).get("ZM050" if fam == "M" else "Z050", {}) for j in claim}
    v = {"k": len(claim), "list": ", ".join(map(str, claim)), "y_active": act}
    v["other"] = ", ".join(f"{j}: {pm[j]['status']}" for j in pm if j not in claim)
    v["psi_hat"] = [pt[j].get("psi") for j in claim]
    v["tau_hat"], v["psi_M_hat"] = (
        [pt[j].get("tau_M") for j in claim],
        [pt[j].get("psi_M") for j in claim],
    )
    z = "Z_M^0.50" if fam == "M" else "Z^0.50"  # the declared statement's bounds, labelled
    v["lower"] = [f"L({z}) = {bz[j]['L']:.4g}" for j in claim if bz[j].get("L") is not None]
    v["upper"] = [f"U({z}) = {bz[j]['U']:.4g}" for j in claim if bz[j].get("U") is not None]
    zt = (ctx.data.get("cov") or {}).get("tally", {})
    v["zero_mod"] = {k: zt.get(k) for k in ("ZERO_MOD_H", "ZERO_MOD_PLUS", "ZERO_MOD_MINUS")}
    v["registration"] = [gv.get(("R1", j), {}).get("agreement") for j in claim]
    v["R2_code_0"] = [gv.get(("L1", j), {}).get("R2_code_0") for j in claim]
    v["rho_inc"] = [gv.get(("L1", j), {}).get("rho_inc") for j in claim]
    v["statuses"] = str({j: pm[j]["status"] for j in pm})
    neg = [j for j in pm if pm[j].get("negative")]
    v["models"] = ", ".join(
        map(str, neg if cat else [j for j in pm if pm[j]["endpoint_status"] != "SCORED"])
    )
    stop = next((g for g in G if g["full_status"] == outcome), None)
    v.update(gate=(stop or {}).get("gate", "[ ]"), values=(stop or {}).get("reason") or "[ ]")
    return v


def report(ctx) -> dict:
    """Always runs (S4: values kept). Statuses, licences, unsealed VAL values, coverage,
    descriptives, POST-DESC; written to stages/S5/report.json."""
    ctx.policy.require("test_endpoint")
    G = sb.gates(ctx)
    stop = next((g for g in G if g.get("scope") == "study" and g["full_status"] not in OK), None)
    inv = [g["full_status"] for g in G if g["full_status"].startswith("INVALID")]
    rep, fams, desc = ctx.data.get("report", {}), {}, {}
    for fam in cc.FAMILIES:
        r = rep.get(fam) or {"outcome": (stop or {}).get("full_status") or sb.fstop(ctx, fam)}
        S, pm = ctx.data.get(f"bnd:{fam}") or {"b": {}, "q": {}}, {}
        for j in cc.MODELS:
            q = S["q"].get(j)
            pt = ca.point_ratios(fam, q, _E(ctx, "x")) if q is not None else None
            st = (r.get("per_model") or {}).get(j, {}).get("status") or sb.prior(ctx, j, fam)
            neg = (r.get("per_model") or {}).get(j, {}).get("negative", False)
            pm[j] = {
                "status": st,
                "endpoint_status": cdc.endpoint_status(j, fam, G),
                "negative": neg,
                "bounds": S["b"].get(j),
                "point": pt,
                "variants": (r.get("variants") or {}).get(j),
            }
            if q is not None and fam != "M":
                desc[f"{fam}|{j}"] = sv.describe(ctx, fam, j, q)
        vals = lic_values(ctx, fam, r["outcome"], pm, G, r.get("y_active"))
        lic = cdc.licence(fam, r["outcome"], vals) if r["outcome"] else None
        fams[fam] = {
            "outcome": r["outcome"],
            "qualifiers": r.get("qualifiers"),
            "licence": lic,
            "per_model": pm,
        }
    sealed, Ev = js(ctx, "stages/S4/SEALED.json"), _E(ctx, "x", "val")
    val_unsealed = {
        n: sv.unsealed(n, cdr.unseal(ctx, n, s), Ev)
        for n, s in sealed.items()
        if not n.startswith("ACT_")
    }
    pd = post_desc(ctx, G, stop)
    desc["cm_intervals"] = sv.cm_intervals(ctx) if not stop else None
    cov = {"S1": js(ctx, "stages/S1/coverage.json"), "S3": js(ctx, "stages/S3/coverage.json")}
    if ctx.data.get("cov"):
        sb.putj(ctx, "stages/S5/coverage.json", ctx.data["cov"])
        cov["S5"] = ctx.data["cov"]
    out = {"protocol_id": cc.PROTOCOL_ID, "protocol_sha256": cc.PROTOCOL_SHA256, "head": ctx.head}
    out.update(R=cc.R_COMMIT, study=inv[0] if inv else "VALID", union_bound_display="0.15")
    out.update(families=fams, rotation=rep.get("rotation"), post_desc=pd, sealed_released=sealed)
    out.update(descriptives=desc, val_unsealed=val_unsealed, coverage=cov)
    if pd is not None:
        sb.putj(ctx, "stages/S5/POST_DESC.json", pd)
    sb.putj(ctx, "stages/S5/report.json", out)
    return {"status": "PASS", "values": {"study": out["study"], "post_desc": pd is not None}}


PLAN = {"S5": sb.ENTRY + (("ACCEPT", accept, "study"), ("REG2", reg2, "study"))}
PLAN["S5"] += (("T-PRE", t_pre, "study"), ("T-PRE-MODEL", t_pre_model, "model"))
PLAN["S5"] += (("RESP-SPEC", resp_spec, "model"), ("NUM", num, "model"))
PLAN["S5"] += (("ENDPOINT", endpoint, "family"), ("REPORT", report, "study"))
