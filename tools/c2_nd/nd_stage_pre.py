"""C2ND stage bodies S1-S3 (API.md §9.3, §10; C2ND-DESIGN-v1 §3 rows 0-18, §6) in §3 order,
the decoy builder and the split-level helpers reused by S4, S5 and T-PRE (sampling, oracle,
L1, R1, N2, support, H5). DFEAS reads no logit; DFIT logits only on the M0/M0-D rows (L2)."""

from __future__ import annotations

import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c2_attrib as ca
import c2_code as ck
import c2_config as cc
import c2_data as cd
import c2_model as cm
import c2_oracle as co2
import c2_stats as cs
import nd_attrib as nat
import nd_decoy as ndy
import nd_driver as ndr
import nd_registry as nrg
import nd_stage_base as sb
import numpy as np
from nd_split import (
    build_decoys,
    h3_run,
    h5_bounds,
    l1_check,
    m0_rows,
    move_T,
    n2_check,
    r1_check,
    sample,
    support,
    w32,
)
from nd_stage_base import EXC, bundle, c2fit, npz, orc, proc, put, putj, rec

SRC, FAMS = sb.SRC, nc.FAMILIES


# ---- stage entry and S1 (§3 rows 0-9) --------------------------------------------------------
def auth_admit(ctx) -> dict:
    name = "AUTH_IMPL.json" if ctx.dry else "AUTH.json"
    v = {"auth_sha256": cd.file_sha(Path(ctx.store) / name), "release": ctx.release}
    ok = ndr.auth_ok(ctx.store, name)
    return {"status": "PASS" if ok else "FAIL_TECHNICAL/AUTHORITY", "values": v}


def g0_step(ctx) -> dict:
    r = ndr.g0(ctx)
    return {"status": r.pop("status"), "values": r}


def impl(ctx) -> dict:
    H = (sb._jr(ndr.binding_path(ctx)) or {}).get("H")
    return {
        "status": "PASS" if sb._eq(H, ctx.head) else "FAIL_TECHNICAL/AUTHORITY",
        "values": {"H": H},
    }


SUITES = "learner dataset contracts oracle process world analysis prediction experiment"
SUITES += " circle_history c1prime c1prime_registry c2_readout c2_nd"


def pf(ctx) -> dict:
    """API.md §9.3; the basetemp has a test_ component (§20.4 row-9 trap)."""
    scratch = Path(nc.SCRATCH_ROOT) / str(ctx.job)
    tmp, base = scratch / "tmp", scratch / f"test_pt_{ctx.data.get('stage')}"
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TEMP=str(tmp), TMP=str(tmp), TMPDIR=str(tmp))
    env["PYTHONPATH"], py = str(Path(ctx.worktree) / "src"), [sys.executable, "-s"]
    kw, tests = {"cwd": ctx.worktree, "env": env}, [f"tests/{s}" for s in SUITES.split()]
    run = [py + ["-m", "pytest", *tests, "-p", "no:cacheprovider", "--basetemp", str(base)]]
    codes = [subprocess.run(c, **kw).returncode for c in run + [py + ["tools/check_imports.py"]]]
    out = subprocess.run(py + ["tools/check_file_sizes.py"], capture_output=True, text=True, **kw)
    mine = [x for x in out.stdout.splitlines() if "/c2_nd/" in x.replace("\\", "/")]
    res = {"codes": codes, "c2nd_sizes": mine, "temp": str(tmp), "basetemp": str(base)}
    putj(ctx, "stages/S1/pf.json", dict(res, sizes=out.stdout.splitlines()))
    ok = all(c == 0 for c in codes) and not mine
    return {"status": "PASS" if ok else "FAIL_TECHNICAL/PF", "values": res}


def h1(ctx) -> dict:
    r = co2.h1_static(proc(ctx))
    return {"status": r["status"], "values": {"checks": r["checks"]}}


def reg_files(ctx, version) -> None:
    pats = (f"registry/{version}*", f"registry/runs/{version}/**/*")
    for p in (q for pat in pats for q in sorted(Path(ctx.store).glob(pat)) if q.is_file()):
        ctx.data.setdefault("files", []).append(p.relative_to(ctx.store).as_posix())


def reg(ctx) -> dict:
    c2_dry = sb.dry(ctx).registry_c2(ctx) if ctx.dry else None  # ND-C55
    man = nrg.build("ND-REG1", ctx.store, c2_dry=c2_dry)
    reg_files(ctx, "ND-REG1")
    keep = ("n_digests", "union_sha256", "problems", "inventory", "nd_sources")
    return {"status": man["status"], "values": {k: man.get(k) for k in keep}}


def h2(ctx) -> dict:
    return sample(ctx, dict(nc.SPLIT_BLOCKS), "ND-REG1")


def h3(ctx) -> dict:
    r, ctx.data["tally"] = h3_run(ctx, tuple(nc.SPLIT_BLOCKS))
    return {"status": r["status"], "values": r}


def h4(ctx) -> dict:
    """f_x >= 9/10, f_y >= 17/20 on DFIT, DFEAS, DVAL (frozen s_max); the coverage tally."""
    f = {s: {p: sb.frac(orc(ctx, s)[f"E_{p}"]) for p in "xy"} for s in nc.SPLIT_BLOCKS}
    putj(ctx, "stages/S1/coverage.json", {"tally": ctx.data["tally"], "f": f})
    ok = all(v[p] >= nc.H4[p] for v in f.values() for p in "xy")
    return {"status": "PASS" if ok else "INCONCLUSIVE/ELIGIBILITY", "values": {"f": f}}


def h5(ctx) -> dict:
    b = ctx.data["h5"] = h5_bounds(orc(ctx, "val"))
    return {"status": "PASS" if b["ok"] else "INCONCLUSIVE/HEADROOM", "values": b}


def oracle_feas(ctx) -> dict:
    """(i) the oracle's own log-predictive gives G per DVAL row under each model's symbol
    order (ND-C24); (ii) the H5 bounds clear 1/50 nat."""
    ob, P, ident = orc(ctx, "val"), proc(ctx), {}
    for j in nc.MODELS:
        d = co2.d_named(ob["Hp_qbar"] - ob["Hm_qbar"], P["perm"][j])
        ident[j] = nat.oracle_identity(ob["Hp_qbar"], ob["Hm_qbar"], d, P["perm"][j], ob["G_x"])
    head = all(Fraction(v) > nc.ORACLE_HEADROOM for v in ctx.data["h5"]["L"].values())
    v = {"identity": ident, "headroom": {"L": ctx.data["h5"]["L"], "ok": head}}
    putj(ctx, "stages/S1/oracle_feas.json", v)
    st = "PASS" if head else "INCONCLUSIVE/ORACLE_FEASIBILITY"
    return {
        "status": st if all(x["ok"] for x in ident.values()) else "FAIL_TECHNICAL/ORACLE",
        "values": v,
    }


# ---- S2 (§3 rows 10-13) ----------------------------------------------------------------------
def m0(ctx) -> dict:
    ob, recs = orc(ctx, "fit"), []
    for j, (m64, sha) in sb.models(ctx).items():
        rows, inp, acts, z, B = m0_rows(ctx, "fit", j)
        d, cj = ob["Hp_qbar"][rows] - ob["Hm_qbar"][rows], nc.CONTRACT["models"][str(j)]
        r = cm.m0(m64, sha, cj, inp, acts, z, B, d, proc(ctx)["perm"][j], ctx.policy)
        if ctx.dry:  # a planted model has no C2 checkpoint identity (§10.1)
            r["checks"].update(ids=True, state_sha=True)
            ok = all(v for k, v in r["checks"].items() if k != "attainable")
            r["status"] = "PASS" if ok and r["checks"]["attainable"] else r["status"]
        recs.append(rec(r["status"], dict(r["values"], checks=r["checks"]), model=j))
    return sb.lines(recs)


def m0d(ctx) -> dict:
    """nd_decoy.m0d on the M0 rows; decoys/DECOY_<j>.json and decoys/HEAD_<j>.npz."""
    recs, nan = [], np.full((cc.N_READ, cc.N_READ), np.nan)
    for j, (m64, _) in sb.models(ctx).items():
        _, inp, acts, z, _ = m0_rows(ctx, "fit", j)
        (dec, mm, B), F = build_decoys(ctx, j), c2fit(ctx, j)
        r = ndy.m0d(j, m64, dec, B, F, inp, acts, z, ctx.policy)
        ub = float(np.linalg.norm(mm["U"]) / np.linalg.norm(F["R_B"]))
        ex = {"cond_T": mm["cond_T"], "sv_LBV0": mm["sv"], "k0": len(mm["V0"].T), "U_over_B": ub}
        cons = {k: ndy.construction_record(j, k, d, ex) for k, d in dec.items()}
        putj(ctx, f"decoys/DECOY_{j}.json", cons)
        arr = {f"{k}_WU": ndy._np(d.unembed.weight) for k, d in dec.items()}
        arr.update({k: mm[k] if mm["ok"] else nan for k in ("T", "Tinv")}, U=mm["U"], V0=mm["V0"])
        put(ctx, f"decoys/HEAD_{j}.npz", **arr)
        sc = "study" if r["status"].startswith("FAIL") else "model"
        v = {"checks": r["checks"], "values": r["values"]}
        recs.append(rec(r["status"], v, model=j, family="D", scope=sc))
        for k, p in r["per_decoy"].items():
            if p["status"] != "PASS" and k != "DNULL":
                v = {"items": p["items"]}
                recs.append(rec(p["status"], v, model=j, family="D", decoy=k, scope="model"))
        if ctx.dry:  # §10.1 pass criteria 3 and 5 and the forbidden accesses (diagnostic)
            putj(ctx, f"stages/S2/DRY_CHECKS_{j}.json", sb.dry(ctx).checks(ctx, j, inp, acts, z))
    return sb.lines(recs)


def c0c(ctx) -> dict:
    """Chart sha256 (a dry-run store: the c2/ stand-in table) and Sup(DFIT) >= 0.99; DFIT
    activations of every H row, no logit (stages/S2/ACT_FIT_<j>.npz)."""
    recs, want = [], nc.CONTRACT["hashes"]["charts"]
    for j in nc.MODELS:
        name = f"CHART_{j}_production.npz"
        if not ctx.dry and cd.file_sha(Path(cc.C1P_STORE) / name) != want[f"c1prime-store/{name}"]:
            recs.append(rec("FAIL_TECHNICAL/AUTHORITY", {"chart": name}, model=j, scope="study"))
            continue
        X, s = bundle(ctx, "fit", j, roles=("H",))["H"], "stages/S2"
        a = {"H_rp3": X["a"]["resid_post_3"], "H_ln": X["a"]["ln_final_out"]}
        put(ctx, f"{s}/ACT_FIT_{j}.npz", H_phi=X["phi"], H_sup=X["sup"], **a)
        u = sb.frac(X["sup"])
        st = "PASS" if u >= nc.SUP_MIN else EXC + "CHART_UNAVAILABLE"
        recs += [rec(st, {"sup": u}, model=j, family=f) for f in FAMS]
    return sb.lines(recs)


def refit(ctx, j, p, Y, aux, arr, dec) -> tuple:
    """One refit problem on DFIT natural rows: C2 F1 exactly, decoders, m-tilde (§3 row 13)."""
    w, z, panel, phi = aux
    pr = cs.f1_problem(Y, w, z, ck.harmonics(phi, 3))
    st, fit, g = pr["status"].replace("INCONCLUSIVE/", EXC), pr["fit"], pr["g"]
    if st == "PASS":
        dec[p] = cs.fit_decoders(w, z, Y @ g["L_B"].T, Y, ck.harmonics(phi, 1), panel)
        st = st if all(d.ok for d in dec[p].values()) else EXC + "NUMERICAL"
        arr.update({f"{p}_{k}": fit[k] for k in sb.FP})
        arr.update({f"{p}_{k}": g[k] for k in ("L", "P_S", "P_G")}, **{f"{p}_Sigma": pr["Sigma"]})
        mod = ck.code_phase(Y, fit["alpha"], w, g["L_B"])[1]
        arr[f"{p}_mtilde"] = np.float64(ck.zero_code_threshold(mod))
    v = {k: fit.get(k) for k in ("rank", "cond")} | {k: g.get(k) for k in ("rank_Xt", "cond_Xt")}
    return st, dict(v, ids=pr.get("ids"), ref=pr.get("ref"))


def f1(ctx) -> dict:
    """The refits R@D (y) and R@T (y @ T.T) per model (§2.8); fits/REFIT_<j>, DEC_<j>; the
    blind leak diagnostic of R@D (construction projector; matrices only, reported)."""
    recs, ob = [], orc(ctx, "fit")
    w, (mu, sd) = w32(ctx, "fit"), ck.standardise(ob["H_nuis"])
    z, panel = (ob["H_nuis"] - mu) / sd, sb.table(ctx, "fit")["panel"]
    for j in [j for j in nc.MODELS if sb.alive(ctx, j, "D")]:
        X, F, T = bundle(ctx, "fit", j, roles=("H",))["H"], c2fit(ctx, j), move_T(ctx, j)
        arr, info, dec = {"zt_mu": mu, "zt_sd": sd}, {"status": {}, "values": {}, "delta": {}}, {}
        for p in nc.REFITS:
            if p == "RT" and T is None:
                st, v = "NOT_COMPUTED", {}
            else:
                Y = X["y"] @ T.T if p == "RT" else X["y"]
                st, v = refit(ctx, j, p, Y, (w, z, panel, X["phi"]), arr, dec)
            ref = v.get("ref")
            info["status"][p], info["values"][p] = st, v
            info["delta"][p] = cs.delta_p(ref) if ref else float("inf")
            recs.append(rec(st, v, model=j, family="D", problem=p))
        if info["status"]["RD"] == "PASS":
            ctx.policy.require("construction")
            Bh, MD = arr["RD_B"], npz(ctx, f"decoys/HEAD_{j}.npz")["DNULL_WU"] @ F["Q0"]
            ang, kap = nat.canonical_angles(Bh, F["R_B"]), nat.kappa_leak(F["M"], F["R_P_S"], Bh)
            info["leak"], arr["J_D"] = (
                {"canonical_angles": ang, "kappa_leak": kap},
                ca.null_projector(MD),
            )
        put(ctx, f"fits/REFIT_{j}.npz", **arr)
        putj(ctx, f"fits/REFIT_{j}.json", info)
        da = {
            f"{p}_{k}_{x}": a
            for p, ds in dec.items()
            for k, d in ds.items()
            for x, a in cs.decoder_arrays(d).items()
        }
        put(ctx, f"fits/DEC_{j}.npz", **da)
    return sb.lines(recs)


# ---- S3 (§3 rows 14-18; DFEAS: activations only, no logit) -----------------------------------
def sup(ctx) -> dict:
    def one(j, f):
        s = support(ctx, "feas", j)
        return ("PASS" if s["sup"] >= nc.SUP_MIN else EXC + "CHART_UNAVAILABLE"), s

    return sb.per(ctx, FAMS, one)


def _with_rt(ctx, check) -> dict:
    """The family records plus the report-only R@T records of D (problem RT; never exclude)."""
    out = sb.per(ctx, FAMS, lambda j, f: check(ctx, "feas", j, SRC[f]))
    for j in [j for j in nc.MODELS if sb.alive(ctx, j, "D") and sb.problem(ctx, j, "RT")["ok"]]:
        out["records"].append(rec(*check(ctx, "feas", j, "RT"), model=j, family="D", problem="RT"))
    return out


def l1(ctx) -> dict:
    return _with_rt(ctx, l1_check)


def r1(ctx) -> dict:
    return _with_rt(ctx, r1_check)


def n2(ctx) -> dict:
    return sb.per(ctx, ("N-M",), lambda j, f: n2_check(ctx, "feas", j))


def survival(ctx) -> dict:
    putj(ctx, "stages/S3/coverage.json", {j: support(ctx, "feas", j) for j in nc.MODELS})
    return sb.lines([rec(sb.family_stop(ctx, f) or "PASS", family=f) for f in FAMS])


ENTRY = (("AUTH-ADMIT", auth_admit, "study"), ("G0", g0_step, "study"))
S1 = (("PF", pf), ("H1", h1), ("REG", reg), ("H2", h2), ("H3", h3), ("H4", h4), ("H5", h5))
S1 += (("ORACLE-FEAS", oracle_feas),)
S2 = (("M0", m0, "study"), ("M0-D", m0d, "study"), ("C0c", c0c, "model"), ("F1", f1, "model"))
S3 = (("SUP", sup), ("L1", l1), ("R1", r1), ("N2", n2))
PLAN = {"S1": (("IMPL", impl, "study"),) + ENTRY + tuple((g, f, "study") for g, f in S1)}
PLAN["S2"], PLAN["S3"] = ENTRY + S2, ENTRY + tuple((g, f, "model") for g, f in S3)
PLAN["S3"] += (("SURVIVAL", survival, "family"),)
