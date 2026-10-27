"""C2ND stage body S4, DVAL (API.md §10; C2ND-DESIGN-v1 §3 rows 19-26, §4.5, §6.7 L5): X1, DX,
V3x, V3y, Y1, V3x', Y1', V3x'-g1, KC, KC-R, P1 (p1_nd, the sealed VAL bundle, the R-0116-2
equivalence check in the dry run), and the helpers S5 reuses (quantities of the base model and
the decoys, X1, DX, the C2-M arms, the bound wrapper). KC, KC-R, V3x', V3x'-g1 and Y1' release
PASS/FAIL only; method statistics use the refit projectors only (S12)."""

from __future__ import annotations

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_endpoint
import c2_attrib as ca
import c2_config as cc
import c2_decide as cdc
import c2_stats as cs
import nd_attrib as nat
import nd_decide as ndc
import nd_driver as ndr
import nd_split as sp
import nd_stage_base as sb
import nd_stage_pre as pre
import numpy as np
import precision
from nd_stage_base import EXC, alive, bundle, orc, problem, putj, rec

C1 = float(nc.PLACEBO)
HEADROOM, NUISANCE = EXC + "MODEL_HEADROOM", EXC + "NUISANCE_IN_S"
DREF = sp.DREF


# ---- S4 gates (§3 rows 19-25) ----------------------------------------------------------------
def x1(ctx) -> dict:
    return sb.lines([r for j in nc.MODELS for r in sp.x1_model(ctx, "val", j)])


def dx(ctx) -> dict:
    recs = []
    for j in nc.MODELS:
        r = sp.dx_model(ctx, "val", j)
        recs.append(rec(r["status"], r, model=j, family="D", scope="family"))
    return sb.lines(recs)


def v3(ctx, pair, seed, fams, fail) -> dict:
    """V3x (N-R, N-M: MODEL_HEADROOM) or V3y (Y1 activity only; excludes no model), base."""
    ctx.policy.require("val_gate")
    G, Ep, arr = orc(ctx, "val")[f"G_{pair}"], sp.E(ctx, "val", pair), {}
    for j in [j for j in nc.MODELS if any(alive(ctx, j, f) for f in fams)]:
        arr[j] = ca.ind(c1_endpoint.Zfull_hat(sp.afull(ctx, "val", j, pair)[2], G), Ep)
    b = sp.bounds(arr, {j: cdc.guard(v) for j, v in arr.items()}, seed)
    ok = ctx.data.setdefault(f"V3{pair}", {})
    ok.update({j: sb.sg(v, "L") == 1 for j, v in b.items()})
    if pair == "y":
        return sb.lines([rec("PASS" if ok[j] else fail, v, model=j) for j, v in b.items()])
    fj = [(j, f) for j in b for f in fams if alive(ctx, j, f)]
    return sb.lines([rec("PASS" if ok[j] else fail, b[j], model=j, family=f) for j, f in fj])


def v3x(ctx) -> dict:
    return v3(ctx, "x", "val_V3x", ("N-R", "N-M"), HEADROOM)


def v3y(ctx) -> dict:
    return v3(ctx, "y", "val_V3y", nc.FAMILIES, "FAIL")


def y_on(ctx, j, key="V3y") -> bool:
    return bool(sb.frozen_oracle(ctx)["y_active"] and ctx.data.get(key, {}).get(j))


def _y1(Q) -> tuple:
    """Y1-type array and guard on the y pair under Q's projector (frozen C2 or RD)."""
    dY, dyY, Ey = Q["geo"]["y"]
    a = ca.ind(Q["qy"]["A_S"] - C1 * Q["qy"]["A_full"], Ey)
    return a, cdc.guard(a, cdc.beta_A(dY, Q["geo"]["M"], dyY, Q["P"]["delta"], 1, Ey))


def y1(ctx) -> dict:
    ctx.policy.require("val_gate")
    arr, gd, recs = {}, {}, []
    for j in [j for j in nc.MODELS if alive(ctx, j, "N-R")]:
        if not y_on(ctx, j):
            recs.append(rec("NOT_RUN", {"active": False}, model=j, family="N-R"))
            continue
        arr[j], gd[j] = _y1(sp.quant(ctx, "val", j))
    b = sp.bounds(arr, gd, "val_Y1")
    st = {j: "PASS" if sb.sg(v, "U") == -1 else NUISANCE for j, v in b.items()}
    return sb.lines(recs + [rec(st[j], v, model=j, family="N-R") for j, v in b.items()])


def _d_alive(ctx) -> list:
    return [j for j in nc.MODELS if alive(ctx, j, "D") and problem(ctx, j, "RD")["ok"]]


def v3x_d(ctx) -> dict:
    """V3x' and V3y' (one call, seed 630514; ND-C4) for DNULL under RD; PASS/FAIL release."""
    ctx.policy.require("val_gate")
    arr, keep = {}, ctx.data.setdefault("sealD", {})
    for j in _d_alive(ctx):
        Q = keep.setdefault(j, {"Q": sp.quant(ctx, "val", j, "DNULL")})["Q"]
        arr[f"V3x'|{j}"] = ca.ind(
            c1_endpoint.Zfull_hat(Q["qx"]["A_full"], Q["G_x"]), Q["geo"]["x"][2]
        )
        arr[f"V3y'|{j}"] = ca.ind(
            c1_endpoint.Zfull_hat(Q["qy"]["A_full"], Q["G_y"]), Q["geo"]["y"][2]
        )
    b, recs = sp.bounds(arr, {k: cdc.guard(v) for k, v in arr.items()}, "val_V3xD"), []
    for j in _d_alive(ctx):
        bj = sp.split_b(b, j)
        keep[j].update(arrays={k: arr[f"{k}|{j}"] for k in bj}, bounds=bj)
        ok, oky = sb.sg(bj["V3x'"], "L") == 1, sb.sg(bj["V3y'"], "L") == 1
        ctx.data.setdefault("V3yD", {})[j] = oky
        v = {"result": "PASS" if ok else "FAIL", "cases": {"V3y'": "PASS" if oky else "FAIL"}}
        recs.append(rec("PASS" if ok else HEADROOM, v, model=j, family="D"))
    return sb.lines(recs)


def y1_d(ctx) -> dict:
    ctx.policy.require("val_gate")
    arr, gd, recs, keep = {}, {}, [], ctx.data.get("sealD", {})
    for j in _d_alive(ctx):
        if not y_on(ctx, j, "V3yD"):
            recs.append(rec("NOT_RUN", {"result": "NOT_RUN"}, model=j, family="D"))
            continue
        arr[j], gd[j] = _y1(keep[j]["Q"])
    for j, v in sp.bounds(arr, gd, "val_Y1D").items():
        keep[j]["arrays"]["Y1'"], keep[j]["bounds"]["Y1'"] = arr[j], v
        ok = sb.sg(v, "U") == -1
        recs.append(
            rec(
                "PASS" if ok else NUISANCE,
                {"result": "PASS" if ok else "FAIL"},
                model=j,
                family="D",
            )
        )
    return sb.lines(recs)


def v3x_g1(ctx) -> dict:
    """V3x'-g1 (report-only): the unamplified decoy DNULL1 under RD; never excludes."""
    ctx.policy.require("val_gate")
    arr = {}
    for j in _d_alive(ctx):
        Q = sp.quant(ctx, "val", j, "DNULL1")
        arr[j] = ca.ind(c1_endpoint.Zfull_hat(Q["qx"]["A_full"], Q["G_x"]), Q["geo"]["x"][2])
    b, recs = sp.bounds(arr, {j: cdc.guard(v) for j, v in arr.items()}, "val_V3xD_g1"), []
    for j, v in b.items():
        keep = ctx.data["sealD"][j]
        keep["arrays"]["V3x'-g1"], keep["bounds"]["V3x'-g1"] = arr[j], v
        res = "PASS" if sb.sg(v, "L") == 1 else "FAIL"
        recs.append(rec(res, {"result": res}, model=j, family="D"))
    return sb.lines(recs)


def case_guards(arrays, Q) -> dict:
    """KC / KC-R case guards: C2 stream_guards on the R keys; beta_A (coef 1) on the
    A_comp-type N-R keys, beta_E with I - P_hat for Vc (ND-C16); V3y none."""
    g, P = Q["geo"], Q["P"]
    geo, nr = dict(g, proj={"": (P["P_S"], P["delta"])}), dict(g, P_S=P["P_S"], delta_P=P["delta"])
    out = {}
    for k, s in arrays.items():
        st = k.split(":", 1)[1]
        if st in nat.NEC_KEYS:
            out[k] = nat.nr_guards({st: s}, dict(nr, variants={}))[st]
        else:
            out[k] = cdc.stream_guards({st: s}, geo)[st] if st != "V3y" else cdc.guard(s)
    return out


def kc_arrays(ctx, split, j, cases) -> tuple:
    """(arrays, guards) keyed "<case>:<stat>|<j>" of the given cases of model j."""
    arr, gd = {}, {}
    for case in cases:
        Q = sp.quant(ctx, split, j, None if case == "D0" else case, problem(ctx, j, DREF[case]))
        Ex, Ey = Q["geo"]["x"][2], Q["geo"]["y"][2]
        a = nat.case_arrays(case, Q["qx"], Q["qy"], Q["G_x"], Q["G_y"], Ex, Ey, refit=Q["P"])
        for k, v in case_guards(a, Q).items():
            arr[f"{k}|{j}"], gd[f"{k}|{j}"] = a[k], v
    return arr, gd


def kc_eval(ctx, split, seed, cases, alpha=nc.VAL_ALPHA, draws=nc.VAL_DRAWS) -> dict:
    """{j: {case: PASS | CONTRADICTED | UNRESOLVED | NOT_COMPUTED}} (one bootstrap call)."""
    arr, gd, ok = {}, {}, {}
    for j in _d_alive(ctx):
        dec = sp.decoys(ctx, j)
        ok[j] = [c for c in cases if c == "D0" or (c in dec and problem(ctx, j, DREF[c])["ok"])]
        a, g = kc_arrays(ctx, split, j, ok[j])
        arr.update(a)
        gd.update(g)
    b = sp.bounds(arr, gd, seed, alpha, draws)
    keep = ctx.data.setdefault("sealKC", {})
    keep.update({(split, cases, j): (sp.split_b(arr, j), sp.split_b(b, j)) for j in ok})
    act = sb.frozen_oracle(ctx)["y_active"]
    nc_ = "NOT_COMPUTED"
    return {
        j: {c: ndc.kc_case(c, sp.split_b(b, j), act) if c in ok[j] else nc_ for c in cases}
        for j in ok
    }


def kc(ctx) -> dict:
    ctx.policy.require("val_kc")
    recs = []
    for j, r in kc_eval(ctx, "val", "val_KC", nc.KC_CASES).items():
        g = ndc.kc_gate(r)
        recs.append(rec(g["full_status"], {"cases": g["cases"]}, model=j, family="D"))
    return sb.lines(recs)


def kc_r(ctx) -> dict:
    ctx.policy.require("val_kc")
    recs = []
    for j, r in kc_eval(ctx, "val", "val_KC", nc.KCR_CASES).items():
        g = ndc.kcr_gate(r)
        recs.append(rec(g["status"], {"cases": g["cases"]}, model=j, family="D", problem="RT"))
    return sb.lines(recs)


# ---- P1 (§4.5; ND-C20, ND-C21) and the sealed VAL bundle (§6.7 L5) ---------------------------
def summaries(arrays, r4n, models, seeds, alpha, alternative) -> dict:
    """The c2_stats._summaries loop with explicit integer seeds (kernels called directly)."""
    out = {}
    for name, X in arrays.items():
        X, r4 = {j: X[j] for j in models}, {j: r4n[j] for j in models}
        kw = {"X": X, "models": models, "draws": nc.VAL_DRAWS}
        sd, _ = precision.sd_b4_draws(r4n=r4, seed=seeds[0], size=nc.BLOCK, **kw)
        out[name] = {}
        for N in nc.N_LADDER:
            e = precision.centered_draws(seed=seeds[1], size=N, **kw)
            out[name][N] = precision.precision_summary(
                sd, e, models, cs._cfg(alpha, alternative, N)
            )
    return out


def p1_nd(family, arrays, afull_or_G, models, alpha) -> dict:
    """§4.5: N_F = the smallest N at which every model passes every gated array, else the
    smallest N at which >= 2 pass (others PRECISION_LIMITED), else INCONCLUSIVE/UNDERPOWERED;
    alternative 1/10 min_j mean(A_full 1_E) (N-R, N-M) or 3/100 min_j mean(G_x 1_E) (D)."""
    models = list(models)
    coef = nc.P1_ALT_D if family == "D" else nc.P1_ALT_NR_NM
    alt = float(coef) * min(float(np.mean(afull_or_G[j])) for j in models)
    gated = {k: arrays[k] for k in nc.P1_GATED[family]}
    seeds = (nc.seed("val_p1_sd"), nc.seed("val_p1_c"))
    summ, passing = summaries(gated, afull_or_G, models, seeds, alpha, alt), {}
    for N in nc.N_LADDER:
        ok = set(models)
        for name in gated:
            per = summ[name][N]["models"]
            ok &= {j for j in models if per[j]["mde_upper"] <= alt and per[j]["power"] >= nc.POWER}
        passing[N] = sorted(ok)
    full = [N for N in nc.N_LADDER if len(passing[N]) == len(models)]
    two = [N for N in nc.N_LADDER if len(passing[N]) >= 2]
    N_F = full[0] if full else two[0] if two else None
    lim = [j for j in models if N_F is not None and j not in passing[N_F]]
    st = "PASS" if N_F is not None else "INCONCLUSIVE/UNDERPOWERED"
    out = {"N_F": N_F, "pass": passing, "status": st, "precision_limited": lim}
    return dict(out, summaries=summ, alternative=alt)


def _same(a, b) -> bool:
    """Bitwise equality of nested summaries (arrays by dtype, shape and bytes)."""
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    x, y = np.asarray(a), np.asarray(b)
    return x.dtype == y.dtype and x.shape == y.shape and x.tobytes() == y.tobytes()


def p1_equivalence(arrays, afull, models, alpha) -> dict:
    """R-0116-2: the direct kernel path with C2's seeds reproduces c2_stats._summaries."""
    names, alt = cs.P1_SEEDS["R"], 0.1 * min(float(np.mean(afull[j])) for j in models)
    mine = summaries(arrays, afull, list(models), tuple(cc.seed(n) for n in names), alpha, alt)
    ref = cs._summaries(arrays, afull, list(models), names, alpha, alt)
    return {"equal": _same(mine, ref), "seeds": list(names), "arrays": sorted(arrays)}


def _fam_arrays(ctx, fam, j) -> tuple:
    """(stream arrays, P1 base array, sealed quantities) of one family and model on DVAL."""
    Ex = sp.E(ctx, "val", "x")
    if fam == "N-M":
        q = sp.cm_pair(ctx, "val", j, "val_sealed")
        return nat.nm_stream(q, q["A_full"], orc(ctx, "val")["G_x"], Ex), ca.ind(q["A_full"], Ex), q
    Q = sp.quant(ctx, "val", j) if fam == "N-R" else ctx.data["sealD"][j]["Q"]
    args = (Q["qx"], Q["qy"], Q["G_x"], Ex, Q["geo"]["y"][2])
    if fam == "N-R":
        y = {f"y_{k}": v for k, v in Q["qy"].items()}
        return nat.nr_stream(*args), ca.ind(Q["qx"]["A_full"], Ex), dict(Q["qx"], **y)
    keep = {k: Q["qx"][k] for k in ("A_full", "A_S", "e_full", "e_S")}
    return nat.d_stream(*args, refit=Q["P"]), ca.ind(Q["G_x"], Ex), keep


MDE = {"N-R": ("Wc", "Vc", "NEGc"), "D": ("Vabs", "Vrand", "NEG")}
MDE["N-M"] = ("ZMc010", "ZMc050", "WMc", "VMc")


def _bnd(b) -> dict:
    return {f"bounds_{k}": np.array([v["mean"], v["L"], v["U"], v["g"]]) for k, v in b.items()}


def p1(ctx) -> dict:
    recs, out, seals, sd = [], {}, {}, (nc.seed("val_p1_sd"), nc.seed("val_p1_c"))
    for fam in nc.FAMILIES:
        js_, ff = [j for j in nc.MODELS if alive(ctx, j, fam)], nc.FILE_FAMILY[fam]
        stop = ("NOT_RUN" if sb.fstop(ctx, fam) else None) or sb.family_stop(ctx, fam)
        if stop:
            recs.append(rec(stop, family=fam))
            continue
        arrays, base = {}, {}
        for j in js_:
            a, base[j], seals[f"VAL_{ff}_{j}"] = _fam_arrays(ctx, fam, j)
            for k, v in a.items():
                arrays.setdefault(k, {})[j] = v
            seals[f"VAL_{ff}_{j}"].update({f"arr_{k}": v for k, v in a.items()})
        r = out[fam] = p1_nd(fam, arrays, base, js_, nc.ALPHA[fam])
        sm = summaries({k: arrays[k] for k in MDE[fam]}, base, js_, sd, nc.ALPHA[fam], 0.0)
        r["mde"] = {
            k: {N: {j: s["models"][j]["mde_upper"] for j in js_} for N, s in v.items()}
            for k, v in sm.items()
        }
        if ctx.dry and fam == "N-R":
            gated = {k: arrays[k] for k in nc.P1_GATED[fam]}
            putj(
                ctx,
                "stages/S4/p1_equivalence.json",
                p1_equivalence(gated, base, js_, nc.ALPHA[fam]),
            )
        v = {k: r[k] for k in ("N_F", "pass", "precision_limited", "alternative", "mde")}
        recs.append(rec(r["status"], v, family=fam))
    for j, s in ctx.data.get("sealD", {}).items():
        a = {f"gate_{k}": v for k, v in s.get("arrays", {}).items()}
        seals.setdefault(f"VAL_D_{j}", {}).update(a, **_bnd(s.get("bounds", {})))
    for (_, _c, j), (a, b) in ctx.data.get("sealKC", {}).items():
        seals.setdefault(f"VAL_KC_{j}", {}).update({f"arr_{k}": v for k, v in a.items()}, **_bnd(b))
    for j in nc.MODELS:
        X = bundle(ctx, "val", j)
        seals[f"ACT_VAL_{j}"] = {
            f"{r}_{cc.HOOK_KEYS[s]}": X[r]["a"][s] for r in cc.ROLES for s in cc.SITES
        }
    for name, a in seals.items():
        ndr.seal(ctx, name, {k: np.asarray(v) for k, v in a.items()})
        ctx.data.setdefault("files", []).append(f"sealed/{name}.npz")
    nf = {f: r["N_F"] for f, r in out.items() if r["status"] == "PASS"}
    N, k = cs.n_test(nf) if nf else (None, None)
    fams = {f: {x: r[x] for x in ("N_F", "status", "precision_limited")} for f, r in out.items()}
    putj(ctx, "stages/S4/P1.json", {"families": fams, "N_test": N, "k": k})
    on = {"y_on": {j: y_on(ctx, j) for j in nc.MODELS}}
    putj(ctx, "stages/S4/gates.json", dict(on, y_on_D={j: y_on(ctx, j, "V3yD") for j in nc.MODELS}))
    ctx.data.setdefault("files", []).append("stages/S4/SEALED.json")
    if ctx.dry:  # §10.1: a sealed/ read before the TEST outcome is refused
        putj(ctx, "stages/S4/DRY_SEALED.json", sb.dry(ctx).sealed_check(ctx))
    return sb.lines(recs)


S4 = (("V3x", v3x), ("V3y", v3y), ("Y1", y1), ("V3x'", v3x_d), ("Y1'", y1_d))
S4 += (("V3x'-g1", v3x_g1), ("KC", kc), ("KC-R", kc_r))
PLAN = {"S4": pre.ENTRY + (("X1", x1, "study"), ("DX", dx, "study"))}
PLAN["S4"] += tuple((g, f, "model") for g, f in S4) + (("P1", p1, "family"),)
