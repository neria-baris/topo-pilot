"""C2ND stage body S5 (API.md §10, §14.2; C2ND-DESIGN-v1 §3 rows 27-34, §4, §7, §8): ACCEPT,
REG2, T-PRE, T-PRE-MODEL, RESP-SPEC, NUM, ENDPOINT, REPORT (licences, unsealing, descriptives,
POST-DESC). Endpoint arrays exist only for admitted models and only after T-PRE; RESP/SPEC run
first on each family stream, then the endpoint arrays with the same seed and rows (T-BOOT)."""

from __future__ import annotations

import platform
import time
from fractions import Fraction
from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_endpoint
import c2_attrib as ca
import c2_config as cc
import c2_decide as cdc
import c2_model as cm
import c2_oracle as co2
import nd_attrib as nat
import nd_decide as ndc
import nd_decoy as ndy
import nd_driver as ndr
import nd_registry as nrg
import nd_split as sp
import nd_stage_base as sb
import nd_stage_pre as pre
import numpy as np
import torch
from nd_stage_base import EXC, OK, alive, js, orc, problem, put, putj, rec

TEST_GATE, SEED = EXC + "TEST_GATE", {"N-R": "test_NR", "D": "test_D", "N-M": "test_NM"}
FLAGS = {"N-R": ("rule6a", "nested"), "D": ("rule6b",), "N-M": ("rule6c",)}
T0 = time.process_time(), time.time()


def y_on(ctx, fam, j) -> bool:
    g = js(ctx, "stages/S4/gates.json") or {}
    key = {"N-R": "y_on", "D": "y_on_D"}.get(fam)
    return bool(key and (g.get(key) or {}).get(str(j)))


def tb(arrays, guards, fam) -> dict:
    return sp.bounds(arrays, guards, SEED[fam], nc.ALPHA[fam], nc.TEST_DRAWS)


def keyed(per_model) -> tuple:
    arr = {f"{k}|{j}": v for j, (a, _) in per_model.items() for k, v in a.items()}
    return arr, {f"{k}|{j}": v for j, (_, g) in per_model.items() for k, v in g.items()}


# ---- ACCEPT, REG2, T-PRE, T-PRE-MODEL (§3 rows 27-30) ----------------------------------------
def accept(ctx) -> dict:
    r, rel = ndr.release_ok(ctx, "S5"), js(ctx, "RELEASE_R5.json") or {}
    v = {k: rel.get(k) for k in ("N_test", "k", "accept_review_sha256")}
    return {"status": "PASS" if r["ok"] else "FAIL_TECHNICAL/AUTHORITY", "values": v}


def reg2(ctx) -> dict:
    """R'_ND = R_ND rebuilt now plus U_DFIT, U_DFEAS, U_DVAL (§6.4); then k DTEST blocks."""
    extra = {s: sb.table(ctx, s) for s in nc.SPLIT_BLOCKS}
    man = nrg.build("ND-REG2", ctx.store, extra=extra)
    pre.reg_files(ctx, "ND-REG2")
    if man["status"] != "PASS":
        return {"status": man["status"], "values": {"problems": man.get("problems")}}
    return sp.sample(ctx, {"test": int(js(ctx, "RELEASE_R5.json")["k"])}, "ND-REG2")


def t_pre(ctx) -> dict:
    """§3 row 29 in order; FAIL_TECHNICAL ends it at once, unmet criteria give TEST_GATE; X1
    and DX failures confined to decoy arms -> FAIL_TECHNICAL/DECOY for family D."""
    v, f_val = {}, (js(ctx, "stages/S1/coverage.json") or {}).get("f", {}).get("val", {})
    h1 = co2.h1_static(sb.proc(ctx))
    v["H1"] = h1["checks"]
    if h1["status"] != "PASS":
        return {"status": h1["status"], "values": v}
    h3, v["tally"] = sp.h3_run(ctx, ("test",))
    v["H3"] = h3
    if h3["status"] != "PASS":
        st = h3["status"]
        return {"status": st if st.startswith("FAIL") else "INCONCLUSIVE/TEST_GATE", "values": v}
    f = {p: sb.frac(orc(ctx, "test")[f"E_{p}"]) for p in "xy"}
    v["drift"] = {p: abs(f[p] - Fraction(f_val[p])) for p in "xy"}
    v["H5"], bad, recs = sp.h5_bounds(orc(ctx, "test")), [], []
    for j, (m64, _) in sb.models(ctx).items():
        _, inp, acts, z, B = sp.m0_rows(ctx, "test", j)
        v[f"M0|{j}"] = cm.identity_patch(m64, inp, acts, ctx.policy)
        dec = {k: d for k, (d, _) in sp.decoys(ctx, j).items()}
        md = ndy.m0d(j, m64, dec, B, sb.c2fit(ctx, j), inp, acts, z, ctx.policy)
        v[f"M0D|{j}"] = {"status": md["status"], "checks": md["checks"]}
        bad += [] if all(v[f"M0|{j}"].values()) else ["FAIL_TECHNICAL/MODEL"]
        bad += [md["status"]] if md["status"].startswith("FAIL") else []
        x = sp.x1_model(ctx, "test", j)
        bad += [x[0]["status"]] if x[0]["status"] != "PASS" else []
        recs += [r for r in x[1:] if r["status"] != "PASS"]
        d = sp.dx_model(ctx, "test", j)
        recs += (
            []
            if d["status"] == "PASS"
            else [rec(d["status"], d, model=j, family="D", scope="family")]
        )
        X = sb.bundle(ctx, "test", j)
        hooks = {f"{r}_{cc.HOOK_KEYS[s]}": X[r]["a"][s] for r in cc.ROLES for s in cc.SITES}
        put(ctx, f"stages/S5/ACT_TEST_{j}.npz", **{f"{r}_phi": X[r]["phi"] for r in sb.X3}, **hooks)
    putj(ctx, "stages/S5/tpre.json", v)
    crit = v["H5"]["ok"] and all(d <= nc.F_DRIFT for d in v["drift"].values())
    st = bad[0] if bad else "PASS" if crit else "INCONCLUSIVE/TEST_GATE"
    return {"status": st, "records": [rec(st, v)] + recs}


def t_pre_model(ctx) -> dict:
    """§3 row 30: Sup(DTEST), L1 and R1 with the frozen decoders (C2 R, RD, M; RT report-only),
    N2 (N-M)."""

    def one(j, fam, src=None):
        s, chk = sp.support(ctx, "test", j), {}
        chk["sup"] = {"status": "PASS" if s["sup"] >= nc.SUP_MIN else "FAIL", "sup": s["sup"]}
        for name, fn in (("L1", sp.l1_check), ("R1", sp.r1_check)):
            st, val = fn(ctx, "test", j, src or sb.SRC[fam])
            chk[name] = dict(val, status=st)
        if fam == "N-M":
            st, val = sp.n2_check(ctx, "test", j)
            chk["N2"] = dict(val, status=st)
        return ("PASS" if all(c["status"] == "PASS" for c in chk.values()) else TEST_GATE), chk

    out = sb.per(ctx, nc.FAMILIES, one)
    for j in [j for j in nc.MODELS if alive(ctx, j, "D") and problem(ctx, j, "RT")["ok"]]:
        out["records"].append(rec(*one(j, "D", "RT"), model=j, family="D", problem="RT"))
    return out


# ---- the family streams (§4.2), RESP-SPEC and NUM (§3 rows 31-32) ---------------------------
def first(ctx, j, fam) -> tuple:
    """V3x and the SPEC array (Y1; Y1' for D; none for N-M): the first part of the stream."""
    Q = sp.quant(ctx, "test", j, "DNULL" if fam == "D" else None)
    Ex = Q["geo"]["x"][2]
    arr = {"V3x": ca.ind(c1_endpoint.Zfull_hat(Q["qx"]["A_full"], Q["G_x"]), Ex)}
    gd = {"V3x": cdc.guard(arr["V3x"])}
    if fam != "N-M":
        dY, dyY, Ey = Q["geo"]["y"]
        arr["Y1"] = ca.ind(Q["qy"]["A_S"] - float(nc.PLACEBO) * Q["qy"]["A_full"], Ey)
        gd["Y1"] = cdc.guard(arr["Y1"], cdc.beta_A(dY, Q["geo"]["M"], dyY, Q["P"]["delta"], 1, Ey))
    return arr, gd


def stream(ctx, j, fam) -> tuple:
    """(arrays, guards, quantities) of the whole family stream of one admitted model."""
    E = {p: sp.E(ctx, "test", p) for p in "xy"}
    if fam == "N-M":
        q = sp.cm_pair(ctx, "test", j, "test_endpoint")
        a = nat.nm_stream(q, q["A_full"], orc(ctx, "test")["G_x"], E["x"])
        return a, nat.nm_guards(a), q
    if fam == "N-R":
        Q, var, yb = sp.quant(ctx, "test", j), {}, sp.ys(ctx, "test", j)
        for v in [v for v in nc.VARIANTS if problem(ctx, j, v)["ok"]]:
            Pv = problem(ctx, j, v)
            var[v] = nat.nr_quantities(
                Q["geo"]["x"][0], Q["geo"]["M"], yb["Hp"], yb["Hm"], Pv["P_S"]
            )
            var[v]["delta"] = Pv["delta"]
        a = nat.nr_stream(Q["qx"], Q["qy"], Q["G_x"], E["x"], E["y"], var)
        geo = dict(Q["geo"], P_S=Q["P"]["P_S"], delta_P=Q["P"]["delta"])
        geo["variants"] = {v: (problem(ctx, j, v)["P_S"], q["delta"]) for v, q in var.items()}
        return a, nat.nr_guards(a, geo), dict(Q["qx"], variants=var)
    Q = sp.quant(ctx, "test", j, "DNULL")
    R = sp.quant(ctx, "test", j, "DNULLR") if "DNULLR" in sp.decoys(ctx, j) else None
    R = R if R is not None and R["P"]["ok"] else None
    qr, pr = (R["qx"], R["P"]) if R else (None, None)
    a = nat.d_stream(Q["qx"], Q["qy"], Q["G_x"], E["x"], E["y"], qr, Q["P"], pr)
    gD = dict(Q["geo"], proj={"": (Q["P"]["P_S"], Q["P"]["delta"])})
    gR = dict(R["geo"], proj={"DNULLR:": (R["P"]["P_S"], R["P"]["delta"])}) if R else None
    return a, nat.d_guards(a, gD, gR), dict(Q["qx"], G=Q["G_x"])


def resp_spec(ctx) -> dict:
    ctx.policy.require("test_endpoint")
    recs = []
    for fam in nc.FAMILIES:
        got = {j: first(ctx, j, fam) for j in nc.MODELS if alive(ctx, j, fam)}
        b = tb(*keyed(got), fam)
        for j in got:
            bj = sp.split_b(b, j)
            resp, spec, st = cdc._gate(bj, "Y1", y_on(ctx, fam, j))
            v = {"resp": resp, "spec": spec, "bounds": bj}
            recs.append(rec(st or "PASS", v, model=j, family=fam))
    return sb.lines(recs)


def num(ctx) -> dict:
    """Form the admitted models' endpoint arrays; record every bound inside its guard."""
    ctx.policy.require_write("test_endpoint")
    recs = []
    for fam in nc.FAMILIES:
        got = {j: stream(ctx, j, fam) for j in nc.MODELS if alive(ctx, j, fam)}
        b = tb(*keyed({j: g[:2] for j, g in got.items()}), fam)
        bj = {j: sp.split_b(b, j) for j in got}
        q = {j: g[2] for j, g in got.items()}
        ctx.data[f"bnd:{fam}"] = {"b": bj, "arr": {j: g[0] for j, g in got.items()}, "q": q}
        for j in got:
            un = [f"{s}:{x}" for s, v in bj[j].items() for x in "LU" if sb.sg(v, x) == 0]
            st = "INC/NUMERICAL" if un else "PASS"
            recs.append(rec(st, {"unresolved": un}, model=j, family=fam))
    return sb.lines(recs)


# ---- ENDPOINT (§4.3; §3 row 33) --------------------------------------------------------------
def _kc_extra(ctx) -> dict:
    """KC-R contradictions (S4 records) and the DTEST report-only KC / KC-R categories (seed
    630507, 5,000 draws, two-sided 95 %) for KC_TEST_DISAGREES and the report."""
    kcr = {}
    for g in sb.gates(ctx):
        if g["gate"] == "KC-R" and g["full_status"] == "MOVE_CASE_CONTRADICTED":
            cases = (g.get("values") or {}).get("cases", {})
            kcr[int(g["model"])] = [c for c, r in cases.items() if r == "FAIL"]
    cases = nc.KC_CASES + nc.KCR_CASES
    test = sp.kc_eval(ctx, "test", "test_KC", cases, nc.DESC_ALPHA, nc.KC_TEST_DRAWS)
    kt = {j: [c for c in nc.KC_CASES if r.get(c) == "CONTRADICTED"] for j, r in test.items()}
    return {"kcr": kcr, "kc_test": {j: c for j, c in kt.items() if c}, "kc_test_all": test}


def endpoint(ctx) -> dict:
    ctx.policy.require_write("test_endpoint")
    recs, p1 = [], js(ctx, "stages/S4/P1.json") or {}
    rep, kx = ctx.data.setdefault("report", {}), _kc_extra(ctx)
    for fam in nc.FAMILIES:
        S, st, per = ctx.data.get(f"bnd:{fam}") or {"b": {}}, {}, {}
        var, dn = {}, {}
        for j in nc.MODELS:
            b = S["b"].get(j)
            if b is None:
                st[j] = sb.prior(ctx, j, fam) or "INC"
                per[j] = {"status": st[j], "negative": False}
                continue
            if fam == "N-R":
                r = ndc.nr_model(b, y_on(ctx, fam, j))
                var[j] = {v: ndc.nr_variant_category(b, v, r) for v in nc.VARIANTS}
            elif fam == "D":
                r = ndc.d_model(b, y_on(ctx, fam, j))
                dn[j] = ndc.dnullr_category(b, r) if "DNULLR:Z010" in b else None
            else:
                r = ndc.nm_model(b)
            per[j], st[j] = r, r["status"]
            put(ctx, f"stages/S5/ENDPOINT_{nc.FILE_FAMILY[fam]}_{j}.npz", **S["arr"][j])
        cn = [j for j, s in st.items() if s == "CNHS"]
        out = sb.fstop(ctx, fam) or ndc.overall(fam, st, cn)
        act = sb.frozen_oracle(ctx)["y_active"] and all(y_on(ctx, fam, j) for j in S["b"])
        extra = {"variants": var, "dnullr": dn, "kcr": kx["kcr"], "kc_test": kx["kc_test"]}
        pf = (p1.get("families") or {}).get(fam)
        q = ndc.qualifiers(fam, per, extra, act, pf) if S["b"] else []
        stm = {f: ndc.statement_count(per, f) for f in FLAGS[fam]}
        v = {"outcome": out, "formed": bool(S["b"]), "statuses": st, "qualifiers": q}
        v.update(y_active=act, statements=stm)
        rep[fam] = dict(v, per_model=per, variants=var, dnullr=dn, N_F=(pf or {}).get("N_F"))
        recs.append(rec(out if S["b"] else "NOT_RUN", v, family=fam))
    rep["kc_test"] = kx["kc_test_all"]
    bnd = {f: (ctx.data.get(f"bnd:{f}") or {}).get("b", {}) for f in nc.FAMILIES}
    putj(ctx, "stages/S5/bounds.json", {"bounds": bnd, "kc_test": kx["kc_test_all"]})
    return sb.lines(recs)


# ---- REPORT (§3 row 34; API.md §14.2) --------------------------------------------------------
def _descriptives(ctx) -> dict:
    """lambda_D, eta_comp, iota_M and the LN-scale shares with intervals (seed 630508)."""
    nums, dens, pairs, E = {}, {}, [], sp.E(ctx, "test", "x")
    for j, q in ((ctx.data.get("bnd:D") or {}).get("q") or {}).items():
        nums[f"AS_D|{j}"], dens[f"A_D|{j}"] = ca.ind(q["A_S"], E), ca.ind(q["A_full"], E)
        pairs.append((f"AS_D|{j}", f"A_D|{j}"))
    for j, q in ((ctx.data.get("bnd:N-R") or {}).get("q") or {}).items():
        nums[f"e_comp|{j}"], dens[f"e_full|{j}"] = ca.ind(q["e_comp"], E), ca.ind(q["e_full"], E)
        dens[f"A_full|{j}"], pairs = (
            ca.ind(q["A_full"], E),
            pairs + [(f"e_comp|{j}", f"e_full|{j}")],
        )
        X, F, eps = (
            sb.bundle(ctx, "test", j),
            sb.c2fit(ctx, j),
            float(sb.models(ctx)[j][0].ln_final.eps),
        )
        s1, s2 = (nat.sigma(X[r]["a"]["resid_post_3"], eps) for r in ("Hp", "Hm"))
        d = sp.afull(ctx, "test", j, "x")[0]
        ln = nat.ln_arrays(
            d, F["M"], problem(ctx, j, "R")["P_S"], X["Hp"]["y"], X["Hm"]["y"], s1, s2
        )
        for k, a in ln.items():
            nums[f"{k}|{j}"] = ca.ind(a, E)
            pairs.append((f"{k}|{j}", f"A_full|{j}"))
    for j, q in ((ctx.data.get("bnd:N-M") or {}).get("q") or {}).items():
        nums[f"I_M|{j}"], dens[f"A_F|{j}"] = ca.ind(q["I_M"], E), ca.ind(q["A_F"], E)
        pairs.append((f"I_M|{j}", f"A_F|{j}"))
    return nat.descriptives_nd(nums, dens, pairs, E) if pairs else {}


def post_desc(ctx, G, stop):
    """C2 §5.7: unlicensed point ratios for the models stopped at T-PRE or RESP-SPEC."""
    if stop is not None and stop["full_status"] != "INCONCLUSIVE/TEST_GATE":
        return None
    arrays, E = {}, sp.E(ctx, "test", "x")
    for fam in nc.FAMILIES:
        for j in nc.MODELS:
            es = ndc.endpoint_status(j, fam, G)
            if es in ("NOT_RUN/T-PRE", "NOT_RUN/RESP-SPEC") and fam != "N-M":
                Q = sp.quant(ctx, "test", j, "DNULL" if fam == "D" else None)
                num_ = Q["qx"]["A_S"] if fam == "D" else Q["qx"]["A_comp"]
                arrays[f"{fam}|{j}|share"] = {
                    "num": num_,
                    "den": Q["qx"]["A_full"],
                    "E": E,
                    "gate": es[8:],
                }
    return ca.post_desc(arrays) if arrays else None


def report(ctx) -> dict:
    """Always runs. Statuses, licences, rule-6 statements, unsealed VAL values, decoys, leak,
    descriptives, POST-DESC; stages/S5/report.json."""
    ctx.policy.require("test_endpoint")
    G = sb.gates(ctx)
    stop = next((g for g in G if g.get("scope") == "study" and g["full_status"] not in OK), None)
    inv = [g["full_status"] for g in G if g["full_status"].startswith("INVALID")]
    rep, fams, E = ctx.data.get("report", {}), {}, sp.E(ctx, "test", "x")
    for fam in nc.FAMILIES:
        r = rep.get(fam) or {"outcome": (stop or {}).get("full_status") or sb.fstop(ctx, fam)}
        S, pm = ctx.data.get(f"bnd:{fam}") or {"b": {}, "q": {}}, {}
        for j in nc.MODELS:
            st = (r.get("per_model") or {}).get(j, {})
            pm[j] = {
                "status": st.get("status") or sb.prior(ctx, j, fam),
                "endpoint_status": ndc.endpoint_status(j, fam, G),
            }
            pm[j].update(bounds=S["b"].get(j), point=sp.point(fam, S["q"].get(j), E), flags=st)
            pm[j].update(
                variants=(r.get("variants") or {}).get(j), dnullr=(r.get("dnullr") or {}).get(j)
            )
        vals = sp.lic_values(fam, r["outcome"], pm)
        lic = ndc.licence(fam, r["outcome"], vals) if r["outcome"] else None
        stm = {
            k: dict(s, licence=ndc.statement_licence(k, vals) if s["licensed"] else None)
            for k, s in (r.get("statements") or {}).items()
        }
        fams[fam] = {"outcome": r["outcome"], "licence": lic, "statements": stm, "per_model": pm}
        fams[fam].update(qualifiers=r.get("qualifiers"), N_F=r.get("N_F"))
    sealed = js(ctx, "stages/S4/SEALED.json") or {}
    dec = {
        j: js(ctx, f"decoys/DECOY_{j}.json")
        for j in nc.MODELS
        if (Path(ctx.store) / f"decoys/DECOY_{j}.json").exists()
    }
    leak = {j: (js(ctx, f"fits/REFIT_{j}.json") or {}).get("leak") for j in nc.MODELS}
    out = {"protocol_id": nc.PROTOCOL_ID, "protocol_sha256": nc.PROTOCOL_SHA256, "head": ctx.head}
    out.update(
        contract_sha256=sb.cd.file_sha(nc.CONTRACT_PATH),
        c2_h2=nc.C2_H2,
        study=inv[0] if inv else "VALID",
    )
    out.update(union_display=ndc.UNION_DISPLAY, families=fams, dry=bool(ctx.dry))
    o = {f: fams[f]["outcome"] for f in nc.FAMILIES}
    out.update(package_statement=ndc.package_statement(sp._c2_outcome(ctx), o["N-R"], o["D"]))
    out.update(c2_caveat=ndc.c2_caveat(o["D"]), kc_test=rep.get("kc_test"), leak=leak)
    out["decoys"] = {
        j: {k: {x: r.get(x) for x in ("decoy_sha64", "cond_T", "U_over_B")} for k, r in d.items()}
        for j, d in dec.items()
    }
    out["kc"] = [
        {k: g.get(k) for k in ("gate", "model", "full_status", "values")}
        for g in G
        if g["gate"] in ("KC", "KC-R")
    ]
    out["unamplified"] = [g.get("values") for g in G if g["gate"] == "V3x'-g1"]
    out.update(descriptives=_descriptives(ctx) if not stop else None, sealed_released=sealed)
    out.update(
        val_unsealed=sp._unsealed(ctx, sealed, ndr.unseal), post_desc=post_desc(ctx, G, stop)
    )
    out["env"] = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "torch": torch.__version__,
    }
    out.update(cpu_s=time.process_time() - T0[0], wall_s=time.time() - T0[1])
    out["gates"] = [{k: g.get(k) for k in ("gate", "model", "family", "full_status")} for g in G]
    if out["post_desc"] is not None:
        putj(ctx, "stages/S5/POST_DESC.json", out["post_desc"])
    putj(ctx, "stages/S5/report.json", out)
    return {"status": "PASS", "values": {"study": out["study"], "outcomes": o}}


PLAN = {"S5": pre.ENTRY + (("ACCEPT", accept, "study"), ("REG2", reg2, "study"))}
PLAN["S5"] += (("T-PRE", t_pre, "study"), ("T-PRE-MODEL", t_pre_model, "model"))
PLAN["S5"] += (("RESP-SPEC", resp_spec, "model"), ("NUM", num, "model"))
PLAN["S5"] += (("ENDPOINT", endpoint, "family"), ("REPORT", report, "study"))
