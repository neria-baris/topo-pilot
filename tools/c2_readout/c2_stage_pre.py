"""C2 stage bodies S1-S3 (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §5, §6.6, §7 rows 0-16, §8):
PLAN["S1"], PLAN["S2"], PLAN["S3"] in §7 order. A step fn(ctx) returns {"status", "values"} or
per-line "records"; c2_driver records them through run_gate inside the policy. FEAS reads no
logit; FIT logits only on the M0 rows (§5.7)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_chart
import c1_fit
import c1_oracle
import c2_attrib as ca
import c2_code as ck
import c2_data as cd
import c2_model as cm
import c2_oracle as co2
import c2_registry as cg
import c2_stage_base as sb
import c2_stats as cs
import numpy as np
from c1_records import C1GateFailure
from c2_stage_base import EXC, FAM, J1, X3, alive, frac, js, orc, proc, put, putj, rec, table

KP, BASIS, FP, cache = sb.KP, sb.BASIS, sb.FP, sb.cache


# ---- S1 (§7 rows 0, 2-8) ---------------------------------------------------------------------
def impl(ctx) -> dict:
    fz = js(ctx, "FREEZE.json")
    ok = str(fz.get("H", "")).lower() == str(ctx.head).lower()
    return {"status": "PASS" if ok else "FAIL_TECHNICAL/AUTHORITY", "values": {"H": fz.get("H")}}


SUITES = "learner dataset contracts oracle process world analysis prediction experiment"
SUITES += " circle_history c1prime c1prime_registry c2_readout"


def pf(ctx) -> dict:
    """§12.3 unchanged (moved from c2_driver, API.md §19.2); the E-0102-2 file-size scope."""
    scratch = Path(cc.SCRATCH_ROOT) / str(ctx.job)
    tmp, base = scratch / "tmp", scratch / "pt"
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TEMP=str(tmp), TMP=str(tmp), TMPDIR=str(tmp))
    env["PYTHONPATH"] = str(Path(ctx.worktree) / "src")
    py, kw = [sys.executable, "-s"], {"cwd": ctx.worktree, "env": env}
    tests = [f"tests/{s}" for s in SUITES.split()]
    run = [py + ["-m", "pytest", *tests, "-p", "no:cacheprovider", "--basetemp", str(base)]]
    codes = [subprocess.run(c, **kw).returncode for c in run + [py + ["tools/check_imports.py"]]]
    out = subprocess.run(py + ["tools/check_file_sizes.py"], capture_output=True, text=True, **kw)
    lines_ = out.stdout.splitlines()
    mine = [x for x in lines_ if "/c2_readout/" in x.replace("\\", "/")]
    ok = all(c == 0 for c in codes) and not mine
    res = {"codes": codes, "c2_sizes": mine, "temp": str(tmp), "basetemp": str(base)}
    putj(ctx, "stages/S1/pf.json", dict(res, pre_existing_sizes=lines_))
    return {"status": "PASS" if ok else "FAIL_TECHNICAL/PF", "values": res}


def h1(ctx) -> dict:
    r = co2.h1_static(proc(ctx))
    return {"status": r["status"], "values": {"checks": r["checks"]}}


def reg(ctx) -> dict:
    man = cg.build("C2-REG1", ctx.store)
    sb.reg_files(ctx, "C2-REG1")
    keep = ("n_digests", "union_sha256", "problems", "inventory", "digest_file_sha256")
    return {"status": man["status"], "values": {k: man.get(k) for k in keep}}


def h2(ctx) -> dict:
    return sb.sample(ctx, cc.SPLIT_BLOCKS, "C2-REG1")


def oracle_splits(ctx, splits, smax=None) -> tuple:
    """The four-role oracle of each split from the H2 / H2' cache (H^Y on Y_def rows only),
    s_max (FIT, unless given), eligibility and lambda_x; ORACLE_<split>.npz written."""
    P = proc(ctx)
    T, E, pi, co = P["T"], P["E_canon"][J1], P["pi"], P["coords"]
    o, el, lam = {}, {}, {}
    for s in splits:
        k, oH = table(ctx, s)["k_Y"], ctx.data.pop(f"oH:{s}")
        o[s] = co2.oracle_split(T, E, pi, co, table(ctx, s)["canonical"], k, o_H=oH)
    smax = co2.s_max(o["fit"]["H"]["s"]) if smax is None else smax
    for s in splits:
        el[s] = co2.eligibility(o[s], smax)
        lam[s] = co2.x_leakage(o[s], el[s]["E_x"], el[s]["E_y"], co)
    return o, el, lam, smax


def h3(ctx) -> dict:
    P = proc(ctx)
    T, E, pi, co = P["T"], P["E_canon"][J1], P["pi"], P["coords"]
    o, el, lam, smax = oracle_splits(ctx, tuple(cc.SPLIT_BLOCKS))
    t = {s: table(ctx, s) for s in o}
    sp = {s: (t[s]["canonical"], o[s], el[s]["E_x"], el[s]["E_y"], t[s]["sequence_id"]) for s in o}
    r = co2.h3(T, E, pi, co, P["perm"], P["E_named"], sp)
    for s in o:
        sb.save_oracle(ctx, s, o[s], el[s])
    ctx.data.update(o1=o, smax=smax, lam=lam)
    return {"status": r["status"], "values": dict(r, s_max=smax, lambda_x=lam)}


def h4(ctx) -> dict:
    """f_x >= 9/10 and f_y >= 17/20 on FIT, FEAS, VAL (OFF_GRID_Y rows ineligible); tally."""
    o, smax = ctx.data["o1"], ctx.data["smax"]
    f = ctx.data["f"] = {s: {p: frac(orc(ctx, s)[f"E_{p}"]) for p in "xy"} for s in o}
    tally = {s: cd.coverage_tally(co2.reason_flags(o[s], smax)) for s in o}
    putj(ctx, "stages/S1/coverage.json", {"tally": tally, "lambda_x": ctx.data["lam"]})
    ok = all(v[p] >= cc.H4[p] for v in f.values() for p in "xy")
    st = "PASS" if ok else "INCONCLUSIVE/ELIGIBILITY"
    return {"status": st, "values": {"f": f, "tally": tally, "lambda_x": ctx.data["lam"]}}


def h5(ctx) -> dict:
    b, F = sb.h5_bounds(orc(ctx, "val"), cc.seed("val_H5")), orc(ctx, "fit")
    km = co2.kappa_m(F["H_m32"], F["HY_m32"], F["E_y"], F["H_m32"])
    kn = co2.kappa_nu(ctx.data["o1"]["fit"], F["E_x"], proc(ctx)["coords"])
    fz = {"s_max": ctx.data["smax"], "kappa_nu": kn, "kappa_m": km, "y_active": co2.y_active(km)}
    putj(ctx, "oracle/ORACLE_FROZEN.json", dict(fz, f=ctx.data["f"]))
    return {"status": "PASS" if b["ok"] else "INCONCLUSIVE/HEADROOM", "values": dict(b, **fz)}


# ---- S2 (§7 rows 9-11) -----------------------------------------------------------------------
def m0(ctx) -> dict:
    T, ob, recs = table(ctx, "fit"), orc(ctx, "fit"), []
    rows = cd.lowest(T["sequence_id"], cc.M0_ROWS)
    for j, (m64, sha) in sb.models(ctx).items():
        inp = sb.inputs(ctx, j, T["canonical"][rows])
        acts, z = cm.natural_pass(m64, inp, ctx.policy, "m0")
        B = ctx.data[f"basis:{j}"] = cm.readout_basis(m64)
        d, cj = ob["Hp_qbar"][rows] - ob["Hm_qbar"][rows], cc.CONTRACT["models"][str(j)]
        r = cm.m0(m64, sha, cj, inp, acts, z, B, d, proc(ctx)["perm"][j], ctx.policy)
        recs.append(rec(r["status"], dict(r["values"], checks=r["checks"]), model=j))
    return sb.lines(recs)


def c0c(ctx) -> dict:
    T, recs, want = table(ctx, "fit"), [], cc.CONTRACT["hashes"]["charts"]
    for j, (m64, _) in sb.models(ctx).items():
        name = f"CHART_{j}_production.npz"
        sha = next(s for p, s in want.items() if Path(p).name == name)
        if cd.file_sha(Path(cc.C1P_STORE) / name) != sha:
            recs.append(rec("FAIL_TECHNICAL/AUTHORITY", {"chart": name}, model=j, scope="study"))
            continue
        a = cm.activations3(m64, sb.inputs(ctx, j, T["canonical"]))
        ext = c1_chart.extend_phase(*sb.charts(ctx, j), a["resid_post_3"], cc.chart_cfg())
        ctx.data[f"act:{j}"] = {"a": a, "phi": ext.phase}
        hooks = {f"H_{cc.HOOK_KEYS[s]}": a[s] for s in cc.SITES}
        put(ctx, f"stages/S2/ACT_FIT_{j}.npz", H_phi=ext.phase, **hooks)
        st = "PASS" if frac(ext.supported) >= cc.SUP_MIN else EXC + "CHART_UNAVAILABLE"
        recs += [rec(st, {"sup": frac(ext.supported)}, model=j, family=f) for f in ("R", "M")]
    return sb.lines(recs)


def f1_model(ctx, j, recs) -> None:
    """The six problems of one model, decoders, m-tilde, N2 fit, J and the affine readouts."""
    T, ob = table(ctx, "fit"), orc(ctx, "fit")
    w, nu = sb.w32(ctx, "fit"), c1_oracle.y_marginal(ob["H_b32"], proc(ctx)["coords"])
    mu, sd = ck.standardise(ob["H_nuis"])
    z, A, B = (ob["H_nuis"] - mu) / sd, ctx.data[f"act:{j}"], ctx.data[f"basis:{j}"]
    y, a2 = cm.readout_coords(A["a"]["ln_final_out"], B), A["a"]["resid_post_2"]
    aff, n2 = ca.affine_readouts(y, w, nu), ck.n2_fit(a2, w)
    arr = {k: B[k] for k in BASIS} | {"zt_mu": mu, "zt_sd": sd, "J": ca.null_projector(B["M"])}
    W = n2["W"] if n2["W"] is not None else np.zeros((a2.shape[1],) * 2)
    arr.update(aff_w=aff["R_w"], aff_nu=aff["R_nu"], n2_mu=n2["mu"], n2_W=W, n2_q99=n2["q99"])
    info, dec, prs = {"status": {}, "values": {}, "delta": {}, "n2": n2["status"]}, {}, {}
    for p in cc.PROBLEMS:
        fam = FAM[p]
        if not alive(ctx, j, fam):
            recs.append(rec("NOT_RUN", model=j, family=fam, problem=p))
            continue
        Y = a2 if p == "M" else y
        f = ck.fstar(ob["H_m32"], 3)[0] if p == "S*" else ck.harmonics(A["phi"], KP[p])
        base = prs["R"]["fit"] if p == "R_E" and "R" in prs else None
        pr = prs[p] = cs.f1_problem(Y, w, z, f, euclidean=p == "R_E", fit=base)
        st, fit, g = pr["status"].replace("INCONCLUSIVE/", EXC), pr["fit"], pr["g"]
        if p == fam and st == "PASS":
            t = sb.target(fam, A["phi"], ob["H_m32"])
            dec[fam] = cs.fit_decoders(w, z, Y @ g["L_B"].T, Y, t, T["panel"])
            st = st if all(d.ok for d in dec[fam].values()) else EXC + "NUMERICAL"
        arr.update({f"{p}_{k}": fit[k] for k in FP})
        arr.update({f"{p}_{k}": g[k] for k in ("L", "P_S", "P_G")})
        arr.update({f"{p}_Sigma": pr["Sigma"]} if p != "R_E" else {})
        mod = ck.code_phase(Y, fit["alpha"], w, g["L_B"])[1]
        arr[f"{p}_mtilde"] = np.float64(ck.zero_code_threshold(mod))
        v = {k: fit[k] for k in ("rank", "cond")} | {k: g[k] for k in ("rank_Xt", "cond_Xt")}
        v.update(ids=pr["ids"], ref=pr["ref"], partial_r2=ck.partial_r2(Y, w, z, f))
        info["status"][p], info["values"][p] = st, v
        info["delta"][p] = cs.delta_p(pr["ref"]) if pr["ref"] else float("inf")
        recs.append(rec(st, v, model=j, family=fam, problem=p))
    put(ctx, f"fits/FIT_{j}.npz", **arr)
    putj(ctx, f"fits/FIT_{j}.json", info)
    da = {}
    for f, ds in dec.items():
        for k, d in ds.items():
            da.update({f"{cc.FILE_FAMILY[f]}_{k}_{x}": v for x, v in cs.decoder_arrays(d).items()})
    put(ctx, f"fits/DEC_{j}.npz", **da)


def f1(ctx) -> dict:
    recs = []
    for j in cc.MODELS:
        f1_model(ctx, j, recs)
    return sb.lines(recs)


# ---- S3 (§7 rows 12-16; FEAS: activations only, no logit) -----------------------------------
def c0v(ctx) -> dict:
    T, recs, cfg = table(ctx, "feas"), [], cc.chart_cfg()
    led = c1_chart.ConstructionLedger(sb._abs(ctx, "CHART_CONSTRUCTIONS.json"))
    land = cd.lowest(T["sequence_id"], cc.C0V_ROWS)
    for j in cc.MODELS:
        X = sb.bundle(ctx, "feas", j, roles=X3)
        hooks = {f"{r}_{cc.HOOK_KEYS[s]}": X[r]["a"][s] for r in X3 for s in cc.SITES}
        ph = {f"{r}_{k}": X[r][x] for r in X3 for k, x in (("phi", "phi"), ("supported", "sup"))}
        put(ctx, f"stages/S3/ACT_FEAS_{j}.npz", **hooks, **ph)
        fams = [f for f in ("R", "M") if alive(ctx, j, f)]
        if not fams:
            continue
        led.claim(j, "direct")
        Xl, ids = X["H"]["a"]["resid_post_3"][land], c1_chart.landmark_ids(T["sequence_id"][land])
        direct = c1_chart.fit_chart_lcc(Xl, ids, cfg)
        put(ctx, f"stages/S3/DIRECT_{j}.npz", **c1_chart.serialise(direct, None, "direct"))
        r = dict(c1_chart.c0_val(*sb.charts(ctx, j), Xl, direct, cfg), sup_feas=frac(X["H"]["sup"]))
        st = (
            "PASS" if r["status"] == "PASS" and r["sup_feas"] >= cc.SUP_MIN else "CHART_UNAVAILABLE"
        )
        st = st if st == "PASS" else EXC + st
        recs += [rec(st, r, model=j, family=f) for f in fams]
    return sb.lines(recs)


def _fit_target(ctx, j, fam) -> np.ndarray:
    F = sb.npz(ctx, f"stages/S2/ACT_FIT_{j}.npz")
    return sb.target(fam, F["H_phi"], orc(ctx, "fit")["H_m32"])


def _rff_rest(ctx, j) -> dict:
    """The descriptive RFF decoder of f1 from P_rest y (C-27): FIT fit, FEAS score."""
    P, F, B = sb.prob(ctx, j, "R"), sb.npz(ctx, f"stages/S2/ACT_FIT_{j}.npz"), sb.fitb(ctx, j)
    Pr = np.eye(cc.N_READ) - P["P_S"] - P["P_G"]
    yF = cm.readout_coords(F["H_ln"], B) @ Pr.T
    X = sb.bundle(ctx, "feas", j, roles=X3)
    t, tF = sb.target("R", X["H"]["phi"], None), _fit_target(ctx, j, "R")
    try:
        dec = c1_fit.fit_decoder(
            yF, tF, table(ctx, "fit")["panel"], j, cc.CONTRACT["streams"]["rff_rest_target"]
        )
    except C1GateFailure as exc:
        return {"status": exc.status, "reason": str(exc)}
    e = t - dec.predict(X["H"]["y"] @ Pr.T)
    return {"R2": 1.0 - float(np.sum(e**2)) / float(np.sum((t - t.mean(0)) ** 2)), "lam": dec.lam}


def l1(ctx) -> dict:
    """L1 per (model, family) on FEAS; L1_DESC.json: the complete-decoder scores and the RFF
    decoder of f1 from P_rest y (descriptive, §6.6)."""
    out = sb.per(ctx, cc.FAMILIES, lambda j, f: sb.l1_check(ctx, "feas", j, f))
    desc, w, wF = {}, sb.w32(ctx, "feas"), sb.w32(ctx, "fit")
    for (_, j, fam), (preds, t) in ctx.data.get("preds", {}).items():
        tF = _fit_target(ctx, j, fam)
        means = np.array(
            [tF[wF == c].mean(0) if np.any(wF == c) else 0 * tF[0] for c in range(cc.V)]
        )
        desc[f"{fam}|{j}"] = {"l1_complete": cs.l1_complete_scores(t, preds, w, means)}
        if fam == "R":
            desc[f"{fam}|{j}"]["rff_rest"] = _rff_rest(ctx, j)
    putj(ctx, "stages/S3/L1_DESC.json", desc)
    return out


def r1(ctx) -> dict:
    def one(j, f):
        st, v = sb.r1_check(ctx, "feas", j, f)
        ctx.data.setdefault("tally", {})[f"{f}|{j}"] = dict(v["tally"])
        return ("PASS" if st == "PASS" else "CNHS"), v

    return sb.per(ctx, cc.FAMILIES, one)


def n2(ctx) -> dict:
    return sb.per(ctx, ("M",), lambda j, f: sb.n2_check(ctx, "feas", j))


def survival(ctx) -> dict:
    """Each family needs >= 2 ok models; the FEAS per-model, per-family coverage tally."""
    tally = ctx.data.get("tally", {})
    for j in cc.MODELS:
        s = sb.support(ctx, "feas", j)
        for f in ("R", "M"):
            tally.setdefault(f"{f}|{j}", {}).update({k: v for k, v in s.items() if k != "sup"})
    putj(ctx, "stages/S3/coverage.json", tally)
    return sb.lines([rec(sb.family_stop(ctx, f) or "PASS", family=f) for f in cc.FAMILIES])


S1 = (("PF", pf), ("H1", h1), ("REG", reg), ("H2", h2), ("H3", h3), ("H4", h4), ("H5", h5))
S3 = (("C0v", c0v), ("L1", l1), ("R1", r1), ("N2", n2))
PLAN = {"S1": (("IMPL", impl, "study"),) + sb.ENTRY + tuple((g, f, "study") for g, f in S1)}
PLAN["S2"] = sb.ENTRY + (("M0", m0, "study"), ("C0c", c0c, "model"), ("F1", f1, "model"))
PLAN["S3"] = sb.ENTRY + tuple((g, f, "model") for g, f in S3) + (("SURVIVAL", survival, "family"),)
