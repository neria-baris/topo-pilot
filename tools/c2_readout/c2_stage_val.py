"""C2 stage body S4, VAL (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §5.7, §6.6, §6.7, §7 rows
17-20): PLAN["S4"] = X1, V3x, V3y, Y1, Y1*, Y2, P1. Also the helpers S5 reuses: the C2-M patch
arms, the closed-form streams, the X1 arms and run, the bound wrapper. X1 is ephemeral; the VAL
endpoint-bearing values are sealed at P1 (§5.7, C-22). The S5 descriptive compositions (the
rotation arm, POST-DESC quantities, the C2-M intervals, the §2.12 descriptives, the opened VAL
bundles) live here too (line budget, R-0104-1)."""

from __future__ import annotations

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_endpoint
import c2_attrib as ca
import c2_code as ck
import c2_decide as cdc
import c2_driver as cdr
import c2_model as cm
import c2_oracle as co2
import c2_stage_base as sb
import c2_stats as cs
import numpy as np
from c2_stage_base import C1, EXC, X3, alive, bundle, fitb, js, orc, prob, rec, table


# ---- C2-M patch arms (§2.10; patched forwards in context H) ----------------------------------
def patched(ctx, split, j, rep, kind, rows=None) -> np.ndarray:
    X, m64 = bundle(ctx, split, j), sb.models(ctx)[j][0]
    rows = np.arange(len(X["H"]["inp"])) if rows is None else rows
    out = np.full((len(X["H"]["inp"]), cc.V), np.nan)
    out[rows] = cm.patched_logits(m64, X["H"]["inp"][rows], "resid_post_2", rep, ctx.policy, kind)
    return out


def cm_pair(ctx, split, j, kind) -> tuple:
    """C2-M x pair: F, S, C replacements of a2(H+-) in context H (§2.10); A_full."""
    X, P2 = bundle(ctx, split, j), prob(ctx, j, "M", False)["P_S"]
    h = X["H"]["a"]["resid_post_2"]
    reps = [ca.cm_replacements(h, X[r]["a"]["resid_post_2"], P2) for r in X3[1:]]
    z = {k: tuple(patched(ctx, split, j, rp[k], kind) for rp in reps) for k in "FSC"}
    d, _, A = sb.afull(ctx, split, j, "x")
    zk = {f"z_{k}{s}": z[k][i] for k in z for i, s in enumerate("pm")}
    return dict(ca.cm_quantities(d, z, A), **zk), A


def placebo_m(ctx, split, j, kind) -> tuple:
    """Y2 arms on the Y_def rows only: a2(H^Y) (F) and its P2 part (S) patched in context H;
    z_nat(H) closed (C-24)."""
    X, P2 = bundle(ctx, split, j), prob(ctx, j, "M", False)["P_S"]
    rows = np.flatnonzero(table(ctx, split)["Y_def"])
    h, hy = X["H"]["a"]["resid_post_2"][rows], X["HY"]["a"]["resid_post_2"][rows]
    rp = ca.cm_replacements(h, hy, P2)
    z = {k: patched(ctx, split, j, rp[k], kind, rows) for k in "SF"}
    d, _, AR = sb.afull(ctx, split, j, "y")
    return ca.cm_placebo(d, cm.closed_logits(X["H"]["y"], fitb(ctx, j)), z["S"], z["F"]), AR


# ---- the closed-form streams, X1 and the bound wrapper (S4, S5) -------------------------------
def closed_streams(F, y, o, perm) -> dict:
    """The x/y pair quantities of every passing ln_final problem and the R and S* streams of one
    model on one split (F = {"M", "prob"}, y = {role: y}, o = ORACLE arrays; d named, RC-1)."""
    dx = co2.d_named(o["Hp_qbar"] - o["Hm_qbar"], perm)
    dY = co2.d_named(o["H_qbar"] - o["HY_qbar"], perm)
    Ex, Ey, M = np.asarray(o["E_x"], bool), np.asarray(o["E_y"], bool), F["M"]
    ok = {p: f for p, f in F["prob"].items() if f["ok"] and p != "M"}
    q = {p: ca.pair(dx, M, y["Hp"], y["Hm"], f["P_S"], f["P_G"], f["Sigma"]) for p, f in ok.items()}
    for v in q.values():
        v["G"] = np.asarray(o["G_x"], np.float64)
    qy = {}
    for p in (p for p in ("R", "S*") if p in ok):
        qy[p] = ca.pair(dY, M, y["H"], y["HY"], ok[p]["P_S"], ok[p]["P_G"], ok[p]["Sigma"])
    out = {"q": q, "qy": qy, "d_x": dx, "d_y": dY}
    if "R" in q:
        var = {v: q[v] for v in cc.VARIANTS if v in q}
        out["R"] = ca.r_arrays(q["R"], qy["R"], o["G_x"], Ex, Ey, var)
    if "S*" in q:
        out["S*"] = ca.r_arrays(q["S*"], qy["S*"], o["G_x"], Ex, Ey, y_name="Y1*")
    return out


def lowid(E, seq, n) -> np.ndarray:
    rows = np.flatnonzero(np.asarray(E, dtype=bool))
    return rows[np.argsort(np.asarray(seq)[rows], kind="stable")[: int(n)]]


def x1_arms(P, o, seq, w) -> dict:
    """X1 arms (§7 row 17): natural arms (H^Y on its Y_def rows); the R interchange arms on every
    eligible row; S*, the variants and the rotation arms on the 1,024 lowest-id eligible rows.
    Interchange arms carry arm 2's tokens (C-23)."""
    E = {"x": np.asarray(o["E_x"], bool), "y": np.asarray(o["E_y"], bool)}
    nat = {r: np.flatnonzero(o["Y_def"]) if r == "HY" else np.arange(len(seq)) for r in cc.ROLES}
    arms = {
        f"nat_{r}": (P["inp"][r][i], P["y"][r][i], P["z"][r][i], seq[i]) for r, i in nat.items()
    }
    for p, f in P["F"]["prob"].items():
        if not f["ok"] or p == "M":
            continue
        for pr, (a, b) in cc.PAIRS.items():
            rows = np.flatnonzero(E[pr]) if p == "R" else lowid(E[pr], seq, cc.X1_LOWID_ROWS)
            ys = ck.interchange(P["y"][a][rows], P["y"][b][rows], f["P_S"])
            for tag, yy in zip(("21", "12"), ys):
                arms[f"{p}_{pr}_{tag}"] = (P["inp"][b][rows], yy, None, seq[rows])
    R = P["F"]["prob"]["R"]
    if R["ok"]:
        rows = lowid(E["x"], seq, cc.X1_LOWID_ROWS)
        for m, th in cc.ROT_DOSES:
            for s, tag in ((1, "plus"), (-1, "minus")):
                yr = ca.y_rot(P["y"]["H"][rows], R["alpha"], w[rows], R["B"], R["L_B"], s * th)
                arms[f"rot_{m}_{tag}"] = (P["inp"]["H"][rows], yr, None, seq[rows])
    return arms


def x1_run(ctx, split, j) -> dict:
    """X1 (ephemeral, §5.7): identity diagnostics only; the natural logits are cleared after."""
    X, ob, T = bundle(ctx, split, j, kind="x1"), orc(ctx, split), table(ctx, split)
    F = {"M": fitb(ctx, j)["M"], "prob": {p: prob(ctx, j, p) for p in cc.PROBLEMS}}
    P = {k: {r: X[r][k] for r in cc.ROLES} for k in ("inp", "y", "z")} | {"F": F}
    arms = x1_arms(P, ob, T["sequence_id"], sb.w32(ctx, split))
    r = cm.x1(sb.models(ctx)[j][0], arms, fitb(ctx, j), ctx.policy)
    for v in X.values():
        v["z"] = None
    return r


def bounds(arrays, guards, seed, alpha=cc.VAL_ALPHA, draws=cc.VAL_DRAWS) -> dict:
    b = cdc.stream_bounds(arrays, cc.seed(seed), alpha, draws) if arrays else {}
    return {k: dict(v, g=guards[k]) for k, v in b.items()}


def sg(b, side) -> int:
    return cdc.sign(b[side], b["g"])


# ---- descriptive compositions used by ENDPOINT and REPORT (S5; descriptive only) -------------
def _E(ctx, p, split="test") -> np.ndarray:
    return orc(ctx, split)[f"E_{p}"].astype(bool)


def rotation(ctx, js_) -> dict:
    """Report only: A_rot, G_rot on every TEST E_x row, theta_rot with its 95 % interval (seed
    620517, 5,000 draws), s_rot; R-admitted models."""
    P, ob, E, w = sb.proc(ctx), orc(ctx, "test"), _E(ctx, "x"), sb.w32(ctx, "test")
    nums, dens, out = {}, {}, {}
    for m, th in cc.ROT_DOSES:
        ro = co2.rotation_oracle(ob["H_b31"], P["T"], P["E_canon"][sb.J1], w, P["coords"], m)
        for j in js_:
            Pr, y = prob(ctx, j, "R"), bundle(ctx, "test", j)["H"]["y"]
            yp, ym = (ca.y_rot(y, Pr["alpha"], w, Pr["B"], Pr["L_B"], s * th) for s in (1, -1))
            arm = ca.rotation_arm(
                co2.d_named(ro["d"], P["perm"][j]), fitb(ctx, j)["M"], yp, ym, ro["G"], E
            )
            nums[f"A|{m}|{j}"], dens[f"G|{m}|{j}"] = ca.ind(arm["A_rot"], E), ca.ind(ro["G"], E)
            out.setdefault(j, {})[m] = {k: arm[k] for k in ("theta_rot", "s_rot")}
    pairs = [(k, "G" + k[1:]) for k in nums]
    iv = ca.ratio_intervals(nums, dens, pairs, cc.seed("test_rot"), cc.DESC_DRAWS) if nums else {}
    for a, g in pairs:
        _, m, j = a.split("|")
        out[int(j)][int(m)]["interval"] = iv[f"{a}/{g}"]
    return out


def cm_intervals(ctx) -> dict:
    """C2-M descriptive intervals after the M outcome (seed 620518; 24 arrays; NEW-5)."""
    S, E, nums, dens, pairs = ctx.data.get("bnd:M") or {"q": {}}, _E(ctx, "x"), {}, {}, []
    for j, q in S["q"].items():
        X, M = bundle(ctx, "test", j), fitb(ctx, j)["M"]
        ef = ca.energy((X["Hp"]["y"] - X["Hm"]["y"]) @ M.T)
        dens.update({f"A_full|{j}": ca.ind(q["A_full"], E), f"e_full|{j}": ca.ind(ef, E)})
        for k, den in (
            ("A_S", "A"),
            ("A_C", "A"),
            ("I_M", "A"),
            ("e_S", "e"),
            ("e_C", "e"),
            ("e_F", "e"),
        ):
            nums[f"{k}|{j}"] = ca.ind(q[k], E)
            pairs.append((f"{k}|{j}", f"{den}_full|{j}" if den == "e" else f"A_full|{j}"))
    return ca.desc_intervals(nums, dens, pairs) if nums else {}


def describe(ctx, fam, j, q) -> dict:
    """The §2.12 descriptives of one admitted model (TEST; descriptive only)."""
    F, P, X, E = fitb(ctx, j), prob(ctx, j, fam, False), bundle(ctx, "test", j), _E(ctx, "x")
    fr = (
        ck.haar_frames(j, cc.CONTRACT["streams"]["frames_R"]["count"], cc.N_READ, P["Sigma"])
        if fam == "R"
        else ()
    )
    zpm = tuple(cm.closed_logits(X[r]["y"], F) for r in X3[1:])
    ys, aff = (X["Hp"]["y"], X["Hm"]["y"]), {"w": F["aff_w"], "nu": F["aff_nu"]}
    out = ca.descriptives(q, q["d"], F["M"], P["P_S"], P["P_G"], F["J"], E, fr, aff, zpm, ys)
    out["y_partition"] = ca.shares(q["qy"], _E(ctx, "y"))
    out["partial_r2"] = {
        p: v.get("partial_r2") for p, v in js(ctx, f"fits/FIT_{j}.json")["values"].items()
    }
    return dict(out, **js(ctx, "stages/S3/L1_DESC.json").get(f"{fam}|{j}", {}))


def unsealed(name, a, E) -> dict:
    """Point values of one opened VAL bundle (secondary; API.md §15.2 val_unsealed)."""
    fam = {"R": "R", "M": "M", "Sstar": "S*"}.get(name.split("_")[1])
    if name.startswith("VAL_ROT"):
        return {
            k[6:]: {
                "theta_rot": float(np.mean(a[k][E]) / np.mean(a["G_rot" + k[5:]][E])),
                "s_rot": float(np.mean(a[k][E] > 0)),
            }
            for k in a
            if k.startswith("A_rot")
        }
    out = ca.point_ratios(fam, a, E)
    if fam == "M":
        r = a["haar_rows"]
        out["psi_M_R"] = [float(np.mean(x) / np.mean(a["A_F"][r])) for x in a["haar_A"]]
        out["ln_scale_ratio"] = {
            k: [float(np.mean(a[k])), float(np.max(a[k]))] for k in a if k.startswith("lnr_")
        }
    return out


# ---- S4 gates (§7 rows 17-19; VAL) -----------------------------------------------------------
def x1(ctx) -> dict:
    out = [x1_run(ctx, "val", j) for j in cc.MODELS]
    return sb.lines([rec(r.pop("status"), r, model=j) for j, r in zip(cc.MODELS, out)])


def v3(ctx, pair, seed, fail) -> dict:
    ctx.policy.require("val_gate")
    ob, arr = orc(ctx, "val"), {}
    for j in [j for j in cc.MODELS if any(alive(ctx, j, f) for f in cc.FAMILIES)]:
        A = sb.afull(ctx, "val", j, pair)[2]
        arr[j] = ca.ind(c1_endpoint.Zfull_hat(A, ob[f"G_{pair}"]), ob[f"E_{pair}"].astype(bool))
    b = bounds(arr, {j: cdc.guard(v) for j, v in arr.items()}, seed)
    ok = ctx.data.setdefault(f"V3{pair}", {})
    ok.update({j: sg(v, "L") == 1 for j, v in b.items()})
    return sb.lines([rec("PASS" if ok[j] else fail, v, model=j) for j, v in b.items()])


def v3x(ctx) -> dict:
    return v3(ctx, "x", "val_V3x", EXC + "MODEL_HEADROOM")


def v3y(ctx) -> dict:
    return v3(ctx, "y", "val_V3y", "FAIL")  # Y1/Y1*/Y2 inactive; excludes no model


def y_on(ctx, j) -> bool:
    return bool(js(ctx, "oracle/ORACLE_FROZEN.json")["y_active"] and ctx.data["V3y"].get(j))


def yplac(ctx, fam, seed) -> dict:
    """Y1 (R) / Y1* (S*): U(A^Y_S - 0.10 A^Y_full) < -g on VAL E_y rows, if active."""
    ctx.policy.require("val_gate")
    E, arr, gd, recs = orc(ctx, "val")["E_y"].astype(bool), {}, {}, []
    for j in [j for j in cc.MODELS if alive(ctx, j, fam)]:
        if not y_on(ctx, j):
            recs.append(rec("NOT_RUN", {"active": False}, model=j, family=fam))
            continue
        P, M = prob(ctx, j, fam), fitb(ctx, j)["M"]
        d, dy, A = sb.afull(ctx, "val", j, "y")
        arr[j] = ca.ind(ca.partition(d, M, dy, P["P_S"], P["P_G"])["A_S"] - C1 * A, E)
        gd[j] = cdc.guard(arr[j], cdc.beta_A(d, M, dy, P["delta"], 1, E))
    b = bounds(arr, gd, seed)
    st = {j: "PASS" if sg(v, "U") == -1 else EXC + "NUISANCE_IN_S" for j, v in b.items()}
    return sb.lines(recs + [rec(st[j], v, model=j, family=fam) for j, v in b.items()])


def y1(ctx) -> dict:
    return yplac(ctx, "R", "val_Y1")


def y1s(ctx) -> dict:
    return yplac(ctx, "S*", "val_Y1s")


def y2(ctx) -> dict:
    """Y2 (M): activity L(A^Y_M,F - 0.10 A^Y_full) > g, then U(A^Y_M,S - 0.10 A^Y_M,F) < -g."""
    ctx.policy.require("val_gate")
    E, arr, recs = orc(ctx, "val")["E_y"].astype(bool), {}, []
    on = ctx.data.setdefault("Y2on", {})
    for j in [j for j in cc.MODELS if alive(ctx, j, "M")]:
        if not y_on(ctx, j):
            recs.append(rec("NOT_RUN", {"active": False}, model=j, family="M"))
            continue
        q, AR = placebo_m(ctx, "val", j, "val_gate")
        arr[f"Y2|{j}"] = ca.ind(q["AR_S"] - C1 * q["AR_F"], E)
        arr[f"act|{j}"] = ca.ind(q["AR_F"] - C1 * AR, E)
    b = bounds(arr, {k: cdc.guard(v) for k, v in arr.items()}, "val_Y2")
    for j in sorted({int(k.split("|")[1]) for k in b}):
        on[j], yb = sg(b[f"act|{j}"], "L") == 1, b[f"Y2|{j}"]
        st = ("PASS" if sg(yb, "U") == -1 else EXC + "NUISANCE_IN_S") if on[j] else "NOT_RUN"
        recs.append(rec(st, {"active": on[j], "Y2": yb, "act": b[f"act|{j}"]}, model=j, family="M"))
    return sb.lines(recs)


# ---- P1 and the sealed VAL bundle (§6.7, §5.7; row 20) ---------------------------------------
def m_extras(ctx, j) -> dict:
    """VAL report-only C2-M (§2.10): 8 Sigma_e2-whitened Haar frames in place of P2 on the 1,024
    lowest-id eligible rows (psi_M,R), and the block-3 LayerNorm scale ratios (C-30)."""
    X, ob, P = bundle(ctx, "val", j), orc(ctx, "val"), prob(ctx, j, "M", False)
    rows = lowid(ob["E_x"], table(ctx, "val")["sequence_id"], cc.X1_LOWID_ROWS)
    h, d = X["H"]["a"]["resid_post_2"], sb.afull(ctx, "val", j, "x")[0]
    out, A = {"haar_rows": rows}, []
    for PR in ck.haar_frames(
        j, cc.CONTRACT["streams"]["frames_M"]["count"], cc.D_MODEL, P["Sigma"]
    ):
        rp = [ca.cm_replacements(h[rows], X[r]["a"]["resid_post_2"][rows], PR)["S"] for r in X3[1:]]
        zp, zm = (patched(ctx, "val", j, x, "val_sealed", rows)[rows] for x in rp)
        A.append(ca.half_dot(d[rows], zp - zm))
    out["haar_A"], eps = np.array(A), float(sb.models(ctx)[j][0].blocks[3].ln1.eps)
    for r in X3[1:]:
        rp = ca.cm_replacements(h, X[r]["a"]["resid_post_2"], P["P_S"])
        out.update({f"lnr_{k}_{r}": ca.ln_scale_ratio(rp[k], h, eps) for k in "SC"})
    return out


def rot_val(ctx, j) -> dict:
    """The VAL rotation arm (report only; sealed until the fresh outcome, §5.7)."""
    P, ob, w, out = sb.proc(ctx), orc(ctx, "val"), sb.w32(ctx, "val"), {}
    Pr, y, E = prob(ctx, j, "R"), bundle(ctx, "val", j)["H"]["y"], ob["E_x"].astype(bool)
    for m, th in cc.ROT_DOSES:
        ro = co2.rotation_oracle(ob["H_b31"], P["T"], P["E_canon"][sb.J1], w, P["coords"], m)
        yp, ym = (ca.y_rot(y, Pr["alpha"], w, Pr["B"], Pr["L_B"], s * th) for s in (1, -1))
        arm = ca.rotation_arm(
            co2.d_named(ro["d"], P["perm"][j]), fitb(ctx, j)["M"], yp, ym, ro["G"], E
        )
        out.update({f"A_rot_{m}": arm["A_rot"], f"G_rot_{m}": ro["G"]})
    return out


def p1(ctx) -> dict:
    """§6.7 per family; the VAL endpoint bundle is sealed here (§5.7, C-22); P1.json."""
    E, recs, out, seals = orc(ctx, "val")["E_x"].astype(bool), [], {}, {}
    for fam in cc.FAMILIES:
        js_, ff = [j for j in cc.MODELS if alive(ctx, j, fam)], cc.FILE_FAMILY[fam]
        stop = ("NOT_RUN" if sb.fstop(ctx, fam) else None) or sb.family_stop(ctx, fam)
        if stop:
            recs.append(rec(stop, family=fam))
            continue
        arrays, af = {}, {}
        for j in js_:
            if fam == "M":
                q, A = cm_pair(ctx, "val", j, "val_sealed")
                arrays.setdefault("Ztau", {})[j] = ca.ind(q["A_F"] - float(cc.TAU_M) * A, E)
                q.update(m_extras(ctx, j), A_full=A)
            else:
                P, X, (d, _, A) = (
                    prob(ctx, j, fam),
                    bundle(ctx, "val", j),
                    sb.afull(ctx, "val", j, "x"),
                )
                M, (yp, ym) = fitb(ctx, j)["M"], (X["Hp"]["y"], X["Hm"]["y"])
                q = ca.pair(d, M, yp, ym, P["P_S"], P["P_G"], P["Sigma"])
                for k, v in ca.threshold_arrays(q, E).items():
                    arrays.setdefault(k, {})[j] = v
                q["G"] = orc(ctx, "val")["G_x"]
                if fam == "R":
                    seals[f"VAL_ROT_{j}"] = rot_val(ctx, j)
            af[j], seals[f"VAL_{ff}_{j}"] = ca.ind(A, E), q
        gated = {k: arrays[k] for k in cs.P1_ARRAYS[fam]}
        r = out[fam] = cs.p1(fam, gated, af, js_, cc.ALPHA[fam])
        rest = {k: v for k, v in arrays.items() if k not in cs.P1_ARRAYS[fam]}
        r["mde"] = cs.mde_report(rest, js_, *cs.P1_SEEDS[fam], cc.ALPHA[fam]) if rest else {}
        v = {k: r[k] for k in ("N_F", "pass", "precision_limited", "alternative", "mde")}
        recs.append(rec(r["status"], v, family=fam))
    for j in cc.MODELS:
        X = bundle(ctx, "val", j)
        seals[f"ACT_VAL_{j}"] = {
            f"{r}_{cc.HOOK_KEYS[s]}": X[r]["a"][s] for r in cc.ROLES for s in cc.SITES
        }
    for name, a in seals.items():
        cdr.seal(ctx, name, a)
        ctx.data.setdefault("files", []).append(f"sealed/{name}.npz")
    nf = {f: r["N_F"] for f, r in out.items() if r["status"] == "PASS"}
    N, k = cs.n_test(nf) if nf else (None, None)
    fam = {f: {x: r[x] for x in ("N_F", "status", "precision_limited")} for f, r in out.items()}
    sb.putj(ctx, "stages/S4/P1.json", {"families": fam, "N_test": N, "k": k})
    on = {"y_on": {j: y_on(ctx, j) for j in cc.MODELS}, "y2_on": ctx.data.get("Y2on", {})}
    sb.putj(ctx, "stages/S4/gates.json", dict(on, V3x=ctx.data.get("V3x"), V3y=ctx.data.get("V3y")))
    ctx.data["files"].append("stages/S4/SEALED.json")
    return sb.lines(recs)


S4 = (("V3x", v3x), ("V3y", v3y), ("Y1", y1), ("Y1*", y1s), ("Y2", y2))
PLAN = {"S4": sb.ENTRY + (("X1", x1, "study"),) + tuple((g, f, "model") for g, f in S4)}
PLAN["S4"] += (("P1", p1, "family"),)
