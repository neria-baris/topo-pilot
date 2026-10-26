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
import c2_model as cm
import c2_oracle as co2
import c2_registry as cg
import c2_stats as cs
import nd_data as nda
import nd_decoy as ndy
import nd_registry as nrg
import nd_stage_base as sb
import numpy as np
from c1_records import C1GateFailure
from nd_stage_base import EXC, J1, OK, X3, bundle, c2fit, js, npz, orc, proc, put

KINDS = cs.KINDS


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
