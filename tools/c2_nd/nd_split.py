"""C2ND split-level helpers (the second extra module of job 0125, ND-C44; split out of
nd_stage_pre by function group): sampling with the Y-donor preparation, the oracle writer and
H3, H5 bounds, the decoy builder and its S4/S5 rebuild check, the M0 rows, and the L1, R1, N2
and support checks of DFEAS that T-PRE reuses on DTEST (API.md §10)."""

from __future__ import annotations

from fractions import Fraction

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_means
import c2_attrib as ca
import c2_code as ck
import c2_config as cc
import c2_data as cd
import c2_decide as cdc
import c2_model as cm
import c2_oracle as co2
import c2_registry as cg
import c2_stats as cs
import nd_attrib as nat
import nd_data as nda
import nd_decide as ndc
import nd_decoy as ndy
import nd_registry as nrg
import nd_stage_base as sb
import numpy as np
import torch
from c1_records import C1GateFailure
from nd_stage_base import EXC, J1, OK, X3, bundle, c2fit, js, npz, orc, problem, proc, put, rec

KINDS, X2 = cs.KINDS, ("Hp", "Hm")
DREF = {k: "RT" if k in nc.COORD_DECOYS else "RD" for k in nc.DECOYS}


# ---- helpers reused by S4, S5 (API.md §10) ---------------------------------------------------
def w32(ctx, split) -> np.ndarray:
    return sb.table(ctx, split)["canonical"][:, 31].astype(np.int64)


def afull(ctx, split, j, pair, M=None) -> tuple:
    """(d named, dy, A_full) of the natural x or y pair under the readout M (base default)."""
    X, ob, (a, b) = bundle(ctx, split, j), orc(ctx, split), cc.PAIRS[pair]
    d = co2.d_named(ob[f"{a}_qbar"] - ob[f"{b}_qbar"], proc(ctx)["perm"][j])
    dy = X[a]["y"] - X[b]["y"]
    return d, dy, ca.half_dot(d, dy @ (c2fit(ctx, j)["M"] if M is None else M).T)


def move_T(ctx, j):
    H = npz(ctx, f"decoys/HEAD_{j}.npz")
    return H["T"] if "T" in H and np.all(np.isfinite(H["T"])) else None


def Yof(src, X, r, T=None) -> np.ndarray:
    if src == "M":
        return X[r]["a"]["resid_post_2"]
    return X[r]["y"] @ T.T if src == "RT" else X[r]["y"]


def zt(ctx, split, j, src) -> np.ndarray:
    F = npz(ctx, f"fits/REFIT_{j}.npz") if src in nc.REFITS else c2fit(ctx, j)
    return (orc(ctx, split)["H_nuis"] - F["zt_mu"]) / F["zt_sd"]


def decs(ctx, j, src) -> dict:
    ref = src in nc.REFITS
    D = npz(ctx, f"fits/DEC_{j}.npz") if ref else sb.c2npz(ctx, f"fits/DEC_{j}.npz")
    tag = src if ref else cc.FILE_FAMILY[src]
    load = cs.decoder_from_arrays
    return {k: load({f: D[f"{tag}_{k}_{f}"] for f in cs.FIELDS}) for k in KINDS}


def build_decoys(ctx, j) -> tuple:
    """({kind: decoy}, move map, base basis) from the frozen C2 problem R (§2.6, Lemma DC4)."""
    m64, F = sb.models(ctx)[j][0], c2fit(ctx, j)
    B = cm.readout_basis(m64)
    i, out = ndy.base_inputs(F, B), {}
    for k in nc.HEAD_EDITS:
        out[k] = ndy.make_head_decoy(m64, ndy.head_edit(k, i["WU"], i["Q0"], i["P_S"]))
    mm = ndy.move_map(i["B"], i["L_B"], i["M"])
    for k in nc.COORD_DECOYS if mm["ok"] else ():
        out[k] = ndy.make_coord_decoy(m64, k, i["Q0"], i["beta"], mm["T"], mm["Tinv"], i["WU"])
    return out, mm, B


def decoys(ctx, j) -> dict:
    """{kind: (decoy, basis)} rebuilt at S4/S5; decoy_sha64 must equal the S2 record."""

    def make():
        dec, _, B = build_decoys(ctx, j)
        recs = js(ctx, f"decoys/DECOY_{j}.json")
        for k, d in dec.items():
            if ndy.construction_record(j, k, d)["decoy_sha64"] != recs[k]["decoy_sha64"]:
                raise C1GateFailure("FAIL_TECHNICAL/DECOY", f"decoy {k} of {j} changed")
        return {k: (d, ndy.decoy_basis(d, B)) for k, d in dec.items()}

    return sb.cache(ctx, f"decoys:{j}", make)


# ---- split-level checks (DFEAS; T-PRE on DTEST) ----------------------------------------------
def l1_check(ctx, split, j, src) -> tuple:
    X, P, T = bundle(ctx, split, j, roles=X3), sb.problem(ctx, j, src), move_T(ctx, j)
    Y, t, w = Yof(src, X, "H", T), ck.harmonics(X["H"]["phi"], 1), w32(ctx, split)
    r = cs.l1_split(decs(ctx, j, src), w, zt(ctx, split, j, src), Y @ P["L_B"].T, Y, t)
    r.pop("preds", None)
    return r.pop("status"), r


def r1_check(ctx, split, j, src) -> tuple:
    X, ob, P = bundle(ctx, split, j, roles=X3), orc(ctx, split), sb.problem(ctx, j, src)
    E, w, thr, T = ob["E_x"].astype(bool), w32(ctx, split), float(P["mtilde"]), move_T(ctx, j)
    ph = {r: ck.code_phase(Yof(src, X, r, T), P["alpha"], w, P["L_B"]) for r in X3[1:]}
    args = (ph["Hp"][0], ph["Hm"][0], ph["Hp"][1], ph["Hm"][1], ob["Hp_m32"], ob["Hm_m32"])
    r = ck.r1(*(x[E] for x in args), thr)
    r["zero_code"] = [int(np.sum(ph[k][1] <= thr)) for k in ("Hp", "Hm")]
    return ("PASS" if r.pop("status") == "PASS" else "CNHS"), r


def n2_check(ctx, split, j) -> tuple:
    X, ob, F = bundle(ctx, split, j, roles=X3), orc(ctx, split), c2fit(ctx, j)
    if sb.c2js(ctx, f"fits/FIT_{j}.json")["n2"] != "PASS":
        return EXC + "RADIAL_SUPPORT", {"n2": "C2 N2 fit not PASS"}
    E, P2 = ob["E_x"].astype(bool), sb.problem(ctx, j, "M")["P_S"]
    fit = {"mu": F["n2_mu"], "W": F["n2_W"], "q99": float(F["n2_q99"])}
    h = X["H"]["a"]["resid_post_2"][E]
    rp = [ca.cm_replacements(h, X[r]["a"]["resid_post_2"][E], P2) for r in X3[1:]]
    r = ck.n2_gate(fit, w32(ctx, split)[E], *([x[k] for x in rp] for k in "FSC"))
    st = r.pop("status")
    return (st if st in OK else EXC + "RADIAL_SUPPORT"), r


def support(ctx, split, j) -> dict:
    X = bundle(ctx, split, j, roles=X3)
    out = {f"UNSUPPORTED_{r}": int(np.count_nonzero(~X[r]["sup"])) for r in X3}
    return dict(out, sup=sb.frac(X["H"]["sup"]))


def h5_bounds(ob, level=nc.H5) -> dict:
    """Rank-250 lower bounds (5,000 draws, seed 630518, one call per pair) of mean G | E."""
    L = {}
    for p in "xy":
        rng, g = np.random.Generator(np.random.PCG64(nc.seed("h5"))), ob[f"G_{p}"]
        means = c1_means.c1_bootstrap_means(g[ob[f"E_{p}"].astype(bool)], rng, nc.H5_DRAWS)
        L[p] = c1_means.quantile_with_rank(means, nc.H5_ALPHA)[0]
    return {"L": L, "ok": all(Fraction(v) > level for v in L.values())}


def sample(ctx, blocks, version) -> dict:
    """H2 / REG2: the splits (scope c2nd-v1, or c2nd-dry-v1 in a dry-run store), the Y-donor
    preparation, hist/, separation from `version`, first token, SYMBOL-ORDER (a)."""
    P, tabs, scope = proc(ctx), {}, nc.DRY_SCOPE if ctx.dry else nc.SCOPE
    T, E, pi, co = P["T"], P["E_canon"][J1], P["pi"], P["coords"]
    for s, nb in blocks.items():
        canon, ids, panel = nda.sample_split(T, E, pi, s, nb, scope)
        oH = ctx.data[f"oH:{s}"] = co2.oracle_role(T, E, pi, canon, co)
        t = cd.history_table(canon, ids, panel, cd.k_y(oH["b31"], co))
        tabs[s] = ctx.data[f"tab:{s}"] = t
        for b in range(nb):
            sl = slice(b * nc.BLOCK, (b + 1) * nc.BLOCK)
            put(ctx, f"hist/HIST_{s}_b{b}.npz", **{k: v[sl] for k, v in t.items()})
    try:
        sep = nrg.separation(nrg.load(ctx.store, version), tabs)
    except cg.RegistryLineage as exc:
        return {"status": exc.status, "values": {"detail": str(exc)}}
    first = {s: nrg.first_token_ok(t, T, E, pi, s) for s, t in tabs.items()}
    c = tabs["fit" if "fit" in tabs else "test"]["canonical"]
    oa = {j: cm.symbol_order_a(sb.inputs(ctx, j, c), c, P["perm"][j]) for j in nc.MODELS}
    st = sep["status"]
    st = cd.LINEAGE if st == "PASS" and not all(first.values()) else st
    st = co2.IDENTITY if st == "PASS" and not all(oa.values()) else st
    return {"status": st, "values": dict(sep, first_token=first, order_a=oa)}


def h3_run(ctx, splits) -> tuple:
    """The four-role oracle per split from the sampling cache, eligibility with the frozen C2
    s_max (ND-C23), ORACLE_<split>.npz, then C2 H3; returns (h3 result, coverage tally)."""
    P, smax, o, sp, tally = proc(ctx), float(sb.frozen_oracle(ctx)["s_max"]), {}, {}, {}
    T, E, pi, co = P["T"], P["E_canon"][J1], P["pi"], P["coords"]
    for s in splits:
        tab = sb.table(ctx, s)
        o[s] = co2.oracle_split(
            T, E, pi, co, tab["canonical"], tab["k_Y"], o_H=ctx.data.pop(f"oH:{s}")
        )
        el = co2.eligibility(o[s], smax)
        ks = {f"{r}_{x}": o[s][r][x] for r in cc.ROLES for x in ("q", "qbar", "s", "le", "m32")}
        ks.update(H_b31=o[s]["H"]["b31"], H_b32=o[s]["H"]["b32"], H_nuis=o[s]["nuis"], **el)
        ks.update(G_x=o[s]["G_x"], G_y=o[s]["G_y"], Y_def=o[s]["Y_def"], k_Y=o[s]["k_Y"])
        put(ctx, f"oracle/ORACLE_{s}.npz", sequence_id=tab["sequence_id"], **ks)
        sp[s] = (tab["canonical"], o[s], el["E_x"], el["E_y"], tab["sequence_id"])
        tally[s] = cd.coverage_tally(co2.reason_flags(o[s], smax))
    return co2.h3(T, E, pi, co, P["perm"], P["E_named"], sp), tally


def m0_rows(ctx, split, j) -> tuple:
    """(rows, inputs, hooks, natural logits, basis) on the 1,024 lowest-id rows (M0, M0-D)."""

    def make():
        T, m64 = sb.table(ctx, split), sb.models(ctx)[j][0]
        rows = cd.lowest(T["sequence_id"], nc.M0_ROWS)
        inp = sb.inputs(ctx, j, T["canonical"][rows])
        acts, z = cm.natural_pass(m64, inp, ctx.policy, "m0")
        return rows, inp, acts, z, cm.readout_basis(m64)

    return sb.cache(ctx, f"m0:{split}:{j}", make)


# ---- per-model quantities (base, decoys) -----------------------------------------------------
def bounds(arrays, guards, seed, alpha=nc.VAL_ALPHA, draws=nc.VAL_DRAWS) -> dict:
    b = cdc.stream_bounds(arrays, nc.seed(seed), alpha, draws) if arrays else {}
    return {k: dict(v, g=guards[k]) for k, v in b.items()}


def split_b(b, j) -> dict:
    return {k.rsplit("|", 1)[0]: v for k, v in b.items() if k.endswith(f"|{j}")}


def E(ctx, split, p) -> np.ndarray:
    return orc(ctx, split)[f"E_{p}"].astype(bool)


def lowid(Ex, seq, n=nc.LOWID_ROWS) -> np.ndarray:
    rows = np.flatnonzero(Ex)
    return rows[np.argsort(np.asarray(seq)[rows], kind="stable")[: int(n)]]


def ys(ctx, split, j, kind=None) -> dict:
    """Readout coordinates per role: y, or y @ T.T for a coordinate decoy."""
    X, T = bundle(ctx, split, j), move_T(ctx, j)
    return {r: X[r]["y"] @ T.T if kind in nc.COORD_DECOYS else X[r]["y"] for r in cc.ROLES}


def readout(ctx, j, kind) -> np.ndarray:
    return c2fit(ctx, j)["M"] if kind in (None, "D0") else decoys(ctx, j)[kind][1]["M"]


def quant(ctx, split, j, kind=None, P=None) -> dict:
    """x and y pair quantities under the readout of `kind` (None: base) and the problem P
    (default: the frozen C2 R for the base, the refit RD / RT for a decoy)."""
    P = P or problem(ctx, j, DREF[kind] if kind else "R")
    y, M, ob = ys(ctx, split, j, kind), readout(ctx, j, kind), orc(ctx, split)
    dx, dY = afull(ctx, split, j, "x")[0], afull(ctx, split, j, "y")[0]
    qx = nat.nr_quantities(dx, M, y["Hp"], y["Hm"], P["P_S"])
    qx.update(ca.pair(dx, M, y["Hp"], y["Hm"], P["P_S"], P["P_G"], P["Sigma"]))
    qy = ca.pair(dY, M, y["H"], y["HY"], P["P_S"], P["P_G"], P["Sigma"])
    geo = {"M": M, "x": (dx, qx["dy"], E(ctx, split, "x"))}
    geo["y"] = (dY, qy["dy"], E(ctx, split, "y"))
    return {"qx": qx, "qy": qy, "geo": geo, "P": P, "G_x": ob["G_x"], "G_y": ob["G_y"]}


def head_logits(dec, u) -> np.ndarray:
    """The decoy's natural logits from the base ln_final_out (head-only path, §9)."""
    with torch.no_grad():
        x = torch.as_tensor(np.asarray(u, np.float64))
        x = dec.ln_final[1](x) if isinstance(dec.ln_final, torch.nn.Sequential) else x
        return dec.unembed(x).numpy().copy()


# ---- X1 and DX (ephemeral identity diagnostics; reused at T-PRE) -----------------------------
def _arms(X, y, rows, P, prefix, seq) -> dict:
    """The x interchange arms 21, 12 (arm 2's tokens, C2 C-23) on `rows`."""
    ab = ck.interchange(y["Hp"][rows], y["Hm"][rows], P)
    inp = X["Hm"]["inp"][rows]
    return {f"{prefix}_x_{t}": (inp, v, None, seq[rows]) for t, v in zip(("21", "12"), ab)}


def x1_model(ctx, split, j) -> list:
    """§3 row 19: base natural, R interchange and direct complement arms (compared with
    A_full - A_S) on every eligible row, the variant complement arms on the 1,024 lowest-id
    eligible rows; DNULL's arms on every eligible row, the other decoys' on the low-id rows."""
    X, m64 = bundle(ctx, split, j, kind="x1"), sb.models(ctx)[j][0]
    F, Ex, seq = c2fit(ctx, j), E(ctx, split, "x"), sb.table(ctx, split)["sequence_id"]
    rows, low, yd = np.flatnonzero(Ex), lowid(Ex, seq), sb.table(ctx, split)["Y_def"]
    y, P = {r: X[r]["y"] for r in cc.ROLES}, problem(ctx, j, "R")
    nr = {r: np.flatnonzero(yd) if r == "HY" else np.arange(len(seq)) for r in cc.ROLES}
    arms = {f"nat_{r}": (X[r]["inp"][i], y[r][i], X[r]["z"][i], seq[i]) for r, i in nr.items()}
    arms.update(_arms(X, y, rows, P["P_S"], "R", seq))
    yC, inp2 = nat.comp_arm(y["Hp"][rows], y["Hm"][rows], P["P_S"]), X["Hm"]["inp"][rows]
    zC = cm.patched_logits(m64, inp2, "ln_final_out", cm.placed(yC, F), ctx.policy, "x1")
    arms["comp_x"] = (inp2, yC, zC, seq[rows])
    d = afull(ctx, split, j, "x")[0][rows]
    A_comp = nat.nr_quantities(d, F["M"], y["Hp"][rows], y["Hm"][rows], P["P_S"])["A_comp"]
    dev = np.abs(nat.a_comp_direct(d, zC, X["Hm"]["z"][rows]) - A_comp)
    tol = float(nc.frac(nc.TAU_X1)) * np.maximum(1.0, np.abs(zC).max(axis=1, initial=0.0))
    comp_ok = bool(np.all(dev <= tol))  # |1/2 d'v| <= |v|_inf since |d|_1 <= 2
    for v in [v for v in nc.VARIANTS if problem(ctx, j, v)["ok"]]:
        yv = nat.comp_arm(y["Hp"][low], y["Hm"][low], problem(ctx, j, v)["P_S"])
        arms[f"{v}_comp_x"] = (X["Hm"]["inp"][low], yv, None, seq[low])
    r = cm.x1(m64, arms, F, ctx.policy)
    r["comp_direct"] = {"max_dev": float(dev.max(initial=0.0)), "ok": comp_ok}
    out, u = [rec(r["status"] if comp_ok else "FAIL_TECHNICAL/X1", r, model=j)], {}
    u = {q: X[q]["a"]["ln_final_out"] for q in X2}
    for kind, (dec, B) in decoys(ctx, j).items():
        Pk = problem(ctx, j, DREF[kind])
        if not Pk["ok"]:
            continue
        yk, rr = ys(ctx, split, j, kind), rows if kind == "DNULL" else low
        arms = {
            f"nat_{q}": (X[q]["inp"][rr], yk[q][rr], head_logits(dec, u[q][rr]), seq[rr])
            for q in X2
        }
        arms.update(_arms(X, yk, rr, Pk["P_S"], DREF[kind], seq))
        rk = cm.x1(dec, arms, B, ctx.policy)
        st = "PASS" if rk["status"] == "PASS" else "FAIL_TECHNICAL/DECOY"
        out.append(rec(st, rk, model=j, family="D", decoy=kind, scope="family"))
    for b in X.values():
        b["z"] = None
    return out


def dx_model(ctx, split, j) -> dict:
    """§3 row 20 with the construction projector (the frozen C2 R P_S) on the eligible rows."""
    F, Ex, T = c2fit(ctx, j), E(ctx, split, "x"), move_T(ctx, j)
    P_S, d, arrays, base = F["R_P_S"], afull(ctx, split, j, "x")[0][Ex], {}, ys(ctx, split, j)
    for kind, (dec, B) in decoys(ctx, j).items():
        y = ys(ctx, split, j, kind)
        P = T @ P_S @ np.linalg.inv(T) if kind in nc.COORD_DECOYS else P_S
        q = nat.nr_quantities(d, B["M"], y["Hp"][Ex], y["Hm"][Ex], P)
        if kind == "DDOSE":
            q["A_S_base"] = nat.nr_quantities(d, F["M"], base["Hp"][Ex], base["Hm"][Ex], P_S)["A_S"]
        if kind == "DID":  # logit changes: the constant head offset cancels (ND-C45)
            q = {"z": q["dy"] @ B["M"].T, "z_base": (base["Hp"][Ex] - base["Hm"][Ex]) @ F["M"].T}
        arrays[kind] = q
    return ndy.dx(arrays, ctx.policy)


# ---- C2-M arms (§2.4; patched forwards in context H) -----------------------------------------
def cm_pair(ctx, split, j, kind) -> dict:
    X, P2, m64 = bundle(ctx, split, j), problem(ctx, j, "M")["P_S"], sb.models(ctx)[j][0]
    h, inp = X["H"]["a"]["resid_post_2"], X["H"]["inp"]
    reps = [ca.cm_replacements(h, X[r]["a"]["resid_post_2"], P2) for r in X2]
    z = {
        k: tuple(
            cm.patched_logits(m64, inp, "resid_post_2", rp[k], ctx.policy, kind) for rp in reps
        )
        for k in "FSC"
    }
    d, _, A = afull(ctx, split, j, "x")
    eps = float(m64.blocks[3].ln1.eps)
    lnr = {
        f"lnr_{k}_{r}": ca.ln_scale_ratio(rp[k], h, eps) for k in "SC" for r, rp in zip(X2, reps)
    }
    return dict(ca.cm_quantities(d, z, A), A_full=A, **lnr)


# ---- REPORT helpers (DTEST point values, licence brackets, opened VAL bundles) -----------
def _m(x, E) -> float:
    return float(np.mean(np.asarray(x, np.float64)[E]))


def point(fam, q, E) -> dict:
    """Eligible-row point ratios of one model (DTEST; descriptive)."""
    if q is None:
        return {}
    if fam == "N-M":
        A = _m(q["A_F"], E)
        out = {"tau_M": A / _m(q["A_full"], E), "psi_M_comp": _m(q["A_C"], E) / A}
        return dict(out, eta_M_C=_m(q["e_C"], E) / _m(q["e_F"], E), iota_M=_m(q["I_M"], E) / A)
    A, e = _m(q["A_full"], E), _m(q["e_full"], E)
    if fam == "D":
        out = {"psi_prime": _m(q["A_S"], E) / A, "theta_prime": A / _m(q["G"], E)}
        return dict(out, eta_prime=_m(q["e_S"], E) / e, lambda_D=_m(q["A_S"], E) / A)
    out = {"psi_comp": _m(q["A_comp"], E) / A, "psi": _m(q["A_S"], E) / A}
    out.update(eta_comp=_m(q["e_comp"], E) / e, cross=_m(q["cross"], E) / e)
    return out


def lic_values(fam, outcome, pm) -> dict:
    """The bracket values of the §7 sentences: claim models, point values, declared bounds."""
    claim = [j for j in pm if pm[j]["status"] in ndc.CLAIM.get(outcome, ())]
    key = {"N-R": "psi_comp", "D": "psi_prime", "N-M": "psi_M_comp"}[fam]
    z = {"N-R": "Zc050", "D": "Z050", "N-M": "ZMc050"}[fam]
    bz = [(pm[j]["bounds"] or {}).get(z, {}) for j in claim]
    v = {
        "k": len(claim),
        "j": ", ".join(map(str, claim)),
        key: [pm[j]["point"].get(key) for j in claim],
    }
    v["bounds"] = [f"({x.get('L', float('nan')):.4g}, {x.get('U', float('nan')):.4g})" for x in bz]
    v["upper"], v["iota_M"] = v["bounds"], [pm[j]["point"].get("iota_M") for j in claim]
    v["theta_prime"] = [pm[j]["point"].get("theta_prime") for j in claim]
    return v


def _unsealed(ctx, sealed, unseal) -> dict:
    """Point means of every opened VAL bundle (secondary, after every outcome)."""
    out = {}
    for name, s in sealed.items():
        if not name.startswith("ACT_"):
            a = unseal(ctx, name, s)
            out[name] = {k: float(np.mean(v)) for k, v in a.items() if np.asarray(v).ndim <= 1}
    return out


def _c2_outcome(ctx):
    try:
        return sb.c2js(ctx, "stages/S5/report.json")["families"]["R"]["outcome"]
    except Exception:  # noqa: BLE001  the dry-run stand-in has no C2 report
        return None
