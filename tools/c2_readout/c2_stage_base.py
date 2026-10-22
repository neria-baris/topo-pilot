"""C2 stage helpers shared by every PLAN (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §5, §6.6, §7,
§8): the stage-entry bodies (rows 0b, 1), the store loaders and ctx caches, the gate history (the
§7 scope rule), the per-model split state, and the split-level checks that later stages and T-PRE
reuse (sampling with the Y-donor preparation, the ORACLE writer, H5, L1, R1, N2, support, X1, the
closed-form streams, the bound wrapper). No PLAN here; nothing runs at import."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_chart
import c1_gates
import c1_means
import c1_model
import c2_attrib as ca
import c2_code as ck
import c2_data as cd
import c2_decide as cdc
import c2_driver as cdr
import c2_model as cm
import c2_oracle as co2
import c2_registry as cg
import c2_stats as cs
import chart
import numpy as np
import stage_records as sr

OK, EXC, J1 = cdr.OK, "EXCLUDED/", cc.MODELS[0]
FAM = {"R": "R", "R_K1": "R", "R_K2": "R", "R_E": "R", "M": "M", "S*": "S*"}
KP = {"R": 3, "R_K1": 1, "R_K2": 2, "R_E": 3, "M": 3, "S*": 3}
BASIS, FP = ("Q0", "M", "beta", "gamma", "WU", "WUbeta"), ("alpha", "Gamma", "B")
X3, C1 = ("H", "Hp", "Hm"), float(cc.PLACEBO)


# ---- store I/O, caches, gate history (API.md §16.1, §19.2) ----------------------------------
def _abs(ctx, rel) -> Path:
    (Path(ctx.store) / rel).parent.mkdir(parents=True, exist_ok=True)
    ctx.data.setdefault("files", []).append(rel)
    return Path(ctx.store) / rel


def put(ctx, rel, **arrays) -> None:
    sr.save_npz(_abs(ctx, rel), **arrays)


def putj(ctx, rel, obj) -> None:
    sr.write_new(_abs(ctx, rel), cdr._js(obj))


def cache(ctx, key, fn):
    if key not in ctx.data:
        ctx.data[key] = fn()
    return ctx.data[key]


def npz(ctx, rel) -> dict:
    def load():
        with np.load(Path(ctx.store) / rel, allow_pickle=False) as z:
            return {k: z[k] for k in z.files}

    return cache(ctx, rel, load)


def js(ctx, rel) -> dict:
    return cache(ctx, rel, lambda: json.loads((Path(ctx.store) / rel).read_text(encoding="utf-8")))


def proc(ctx) -> dict:
    return cache(ctx, "proc", co2.load_process)


def models(ctx) -> dict:
    return cache(ctx, "models", cm.load_models)


def table(ctx, split) -> dict:
    def load():
        t = [
            npz(ctx, f"hist/{q.name}")
            for q in sorted(Path(ctx.store).glob(f"hist/HIST_{split}_b*"))
        ]
        return {k: np.concatenate([x[k] for x in t]) for k in t[0]}

    return cache(ctx, f"tab:{split}", load)


def orc(ctx, split) -> dict:
    return npz(ctx, f"oracle/ORACLE_{split}.npz")


def fitb(ctx, j) -> dict:
    return npz(ctx, f"fits/FIT_{j}.npz")


def gates(ctx) -> list:
    return sr.gates_so_far(Path(ctx.store))


def prior(ctx, j, fam):
    """The first exclusion, CNHS or stop applying to (j, fam) (§7 scope; variants never)."""
    for g in gates(ctx):
        bad = g["full_status"] not in OK and g["gate"] not in cdc.NON_EXCLUDING
        if bad and g.get("problem") not in cc.VARIANTS and cdc._applies(g, j, fam):
            return g["full_status"]
    return None


def alive(ctx, j, fam) -> bool:
    return prior(ctx, j, fam) is None


def fstop(ctx, fam):
    hit = (g for g in gates(ctx) if g.get("scope") == "family" and g.get("family") == fam)
    return next((g["full_status"] for g in hit if g["full_status"] not in OK), None)


def family_stop(ctx, fam):
    """None while >= 2 models remain, else the §6.5 rule-2 outcome (CNHS names if >= 2 CNHS)."""
    st = {j: prior(ctx, j, fam) for j in cc.MODELS}
    if sum(v is None for v in st.values()) >= 2:
        return None
    return cdc.overall(
        fam, {j: v or "INC" for j, v in st.items()}, [j for j in st if st[j] == "CNHS"]
    )


def rec(status, values=None, **who) -> dict:
    return {"status": status, "values": values or {}, **who}


def lines(recs) -> dict:
    bad = [r["status"] for r in recs if r["status"] not in OK]
    return {"status": bad[0] if bad else "PASS", "records": recs}


def per(ctx, fams, fn) -> dict:
    """One line per alive (model, family); fn(j, fam) -> (status, values)."""
    return lines(
        [rec(*fn(j, f), model=j, family=f) for j in cc.MODELS for f in fams if alive(ctx, j, f)]
    )


def frac(mask) -> Fraction:
    return Fraction(int(np.count_nonzero(mask)), len(mask))


# ---- stage entry (§7 rows 0b, 1; every PLAN) -------------------------------------------------
def auth_admit(ctx) -> dict:
    v = {"auth_sha256": sr.sha256(Path(ctx.store) / "AUTH.json"), "release": ctx.release}
    return {"status": "PASS" if cdr.auth_ok(ctx.store) else "FAIL_TECHNICAL/AUTHORITY", "values": v}


def g0_step(ctx) -> dict:
    r = cdr.g0(ctx)
    return {"status": r.pop("status"), "values": r}


ENTRY = (("AUTH-ADMIT", auth_admit, "study"), ("G0", g0_step, "study"))


# ---- per-model split state (activations, y, phases; API.md §7, §8, §19.3) --------------------
def inputs(ctx, j, H) -> np.ndarray:
    return np.asarray(c1_model.model_inputs(proc(ctx)["perm"][j][np.asarray(H)]))


def charts(ctx, j) -> tuple:
    def load():
        with np.load(Path(cc.C1P_STORE) / f"CHART_{j}_production.npz", allow_pickle=False) as z:
            return chart.chart_from_arrays({k: z[k] for k in z.files})

    return cache(ctx, f"chart:{j}", load)


def _state(ctx, j, H, rows, n, kind) -> tuple:
    """(inputs, hooks, natural logits) of one role on `rows`; elsewhere inputs -1 (never
    forwardable) and NaN (H^Y off its Y_def rows: nothing is formed there, v2 §2.2)."""
    inp, z = np.full((n, 33), -1, np.int64), np.full((n, cc.V), np.nan) if kind else None
    a = {s: np.full((n, cc.D_MODEL), np.nan) for s in cc.SITES}
    if len(rows):
        m64, x = models(ctx)[j][0], inputs(ctx, j, H)
        aa, zz = cm.natural_pass(m64, x, ctx.policy, kind) if kind else (cm.activations3(m64, x), 0)
        inp[rows] = x
        for s in cc.SITES:
            a[s][rows] = aa[s]
        if kind:
            z[rows] = zz
    return inp, a, z


def bundle(ctx, split, j, kind=None, roles=cc.ROLES) -> dict:
    """Per role: inputs, the three hooks, y, and for H, H+, H- the chart phase and support;
    natural logits z only under `kind` (cleared after X1); H^Y on its Y_def rows only."""

    def make():
        tab, out = table(ctx, split), {}
        n = len(tab["canonical"])
        for r, (H, rows) in cd.table_roles(tab).items():
            if r not in roles:
                continue
            inp, a, z = _state(ctx, j, H, rows, n, kind)
            y = cm.readout_coords(a["ln_final_out"], fitb(ctx, j))
            out[r] = {"inp": inp, "a": a, "z": z, "y": y}
            if r in X3:
                ext = c1_chart.extend_phase(*charts(ctx, j), a["resid_post_3"], cc.chart_cfg())
                out[r].update(phi=ext.phase, sup=np.asarray(ext.supported, bool))
        return out

    return cache(ctx, f"X:{split}:{j}", make)


def prob(ctx, j, p, need_alive=True) -> dict:
    """The frozen FIT projector problem p of model j ({"ok": False} unless F1 PASS and alive)."""
    F, fj = fitb(ctx, j), js(ctx, f"fits/FIT_{j}.json")
    if fj["status"].get(p) != "PASS" or (need_alive and not alive(ctx, j, FAM[p])):
        return {"ok": False}
    o = {k: F[f"{p}_{k}"] for k in FP + ("L", "P_S", "P_G", "mtilde")}
    o.update(ok=True, L_B=o["L"][5:], delta=float(fj["delta"][p]))
    return dict(o, Sigma=F[f"{p}_Sigma"] if f"{p}_Sigma" in F else F["R_Sigma"])


def w32(ctx, split) -> np.ndarray:
    return table(ctx, split)["canonical"][:, 31].astype(np.int64)


def zt(ctx, split, j) -> np.ndarray:
    F = fitb(ctx, j)
    return (orc(ctx, split)["H_nuis"] - F["zt_mu"]) / F["zt_sd"]


def Yf(fam, X, r) -> np.ndarray:
    return X[r]["a"]["resid_post_2"] if fam == "M" else X[r]["y"]


def target(fam, phi, m32) -> np.ndarray:
    return ck.fstar(m32, 1)[0] if fam == "S*" else ck.harmonics(phi, 1)


def afull(ctx, split, j, pair) -> tuple:
    """(d named, dy, A_full) of the natural x or y pair (closed form; y pair NaN off Y_def)."""
    X, ob, (a, b) = bundle(ctx, split, j), orc(ctx, split), cc.PAIRS[pair]
    d = co2.d_named(ob[f"{a}_qbar"] - ob[f"{b}_qbar"], proc(ctx)["perm"][j])
    dy = X[a]["y"] - X[b]["y"]
    return d, dy, ca.half_dot(d, dy @ fitb(ctx, j)["M"].T)


# ---- split-level checks (FEAS, reused at T-PRE on TEST) --------------------------------------
def decs(ctx, j, fam) -> dict:
    D, ff = npz(ctx, f"fits/DEC_{j}.npz"), cc.FILE_FAMILY[fam]
    return {k: cs.decoder_from_arrays({f: D[f"{ff}_{k}_{f}"] for f in cs.FIELDS}) for k in cs.KINDS}


def l1_check(ctx, split, j, fam) -> tuple:
    X, ob, P = bundle(ctx, split, j, roles=X3), orc(ctx, split), prob(ctx, j, fam)
    Y, t = Yf(fam, X, "H"), target(fam, X["H"]["phi"], ob["H_m32"])
    r = cs.l1_split(decs(ctx, j, fam), w32(ctx, split), zt(ctx, split, j), Y @ P["L_B"].T, Y, t)
    ctx.data.setdefault("preds", {})[(split, j, fam)] = (r.pop("preds"), t)
    return r.pop("status"), r


def r1_check(ctx, split, j, fam) -> tuple:
    """R1 with the zero overrides; the tally (ZERO_CODE, R1 counts) and, for R, the C1 chart-phase
    V1 of phi(a+) against phi(a-) (reported, §6.6)."""
    X, ob, P = bundle(ctx, split, j, roles=X3), orc(ctx, split), prob(ctx, j, fam)
    E, w, thr = ob["E_x"].astype(bool), w32(ctx, split), float(P["mtilde"])
    ph = {r: ck.code_phase(Yf(fam, X, r), P["alpha"], w, P["L_B"]) for r in X3[1:]}
    m = (ob["Hp_m32"], ob["Hm_m32"])
    r = ck.r1(*(x[E] for x in (ph["Hp"][0], ph["Hm"][0], ph["Hp"][1], ph["Hm"][1]) + m), thr)
    tags = (("ZERO_CODE_PLUS", ph["Hp"][1] <= thr), ("ZERO_CODE_MINUS", ph["Hm"][1] <= thr))
    r["tally"] = {k: int(v.sum()) for k, v in tags} | {
        k: r[k] for k in ("R1_ZERO", "R1_UNSELECTED")
    }
    if fam == "R":
        r["chart_v1"] = c1_gates.v1(X["Hp"]["phi"][E], X["Hm"]["phi"][E], m[0][E], m[1][E])
    return r.pop("status"), r


def n2_check(ctx, split, j) -> tuple:
    X, ob, F, fj = (
        bundle(ctx, split, j, roles=X3),
        orc(ctx, split),
        fitb(ctx, j),
        js(ctx, f"fits/FIT_{j}.json"),
    )
    if fj["n2"] != "PASS":
        return fj["n2"], {}
    E, P2 = ob["E_x"].astype(bool), prob(ctx, j, "M")["P_S"]
    fit = {"mu": F["n2_mu"], "W": F["n2_W"], "q99": float(F["n2_q99"])}
    h = X["H"]["a"]["resid_post_2"][E]
    rp = [ca.cm_replacements(h, X[r]["a"]["resid_post_2"][E], P2) for r in X3[1:]]
    r = ck.n2_gate(fit, w32(ctx, split)[E], *([x[k] for x in rp] for k in "FSC"))
    return r.pop("status"), r


def support(ctx, split, j) -> dict:
    """UNSUPPORTED_H/PLUS/MINUS counts (§5.5; rows kept and phased) and Sup(H)."""
    X = bundle(ctx, split, j, roles=X3)
    tags = dict(zip(X3, ("UNSUPPORTED_H", "UNSUPPORTED_PLUS", "UNSUPPORTED_MINUS")))
    return {tags[r]: int(np.count_nonzero(~X[r]["sup"])) for r in X3} | {"sup": frac(X["H"]["sup"])}


def h5_bounds(ob, seed) -> dict:
    L = {}
    for p in "xy":
        rng = np.random.Generator(np.random.PCG64(int(seed)))
        means = c1_means.c1_bootstrap_means(
            ob[f"G_{p}"][ob[f"E_{p}"].astype(bool)], rng, cc.VAL_DRAWS
        )
        L[p] = c1_means.quantile_with_rank(means, cc.H5_ALPHA)[0]
    return {"L": L, "ok": all(Fraction(v) > cc.H5 for v in L.values())}


def sample(ctx, blocks, version) -> dict:
    """H2 / H2': sample the splits; the Y-donor preparation (the natural-history oracle for b31(H)
    only, cached for H3 / T-PRE; k_Y, Y_def, the defined H^Y; NEW-10); hist/; separation over
    every defined donor role against `version`; first token; SYMBOL-ORDER (a)."""
    P, tabs = proc(ctx), {}
    T, E, pi, co = P["T"], P["E_canon"][J1], P["pi"], P["coords"]
    for s, nb in blocks.items():
        canon, ids, panel = cd.sample_split(T, E, pi, s, nb)
        oH = ctx.data[f"oH:{s}"] = co2.oracle_role(T, E, pi, canon, co)
        t = tabs[s] = ctx.data[f"tab:{s}"] = cd.history_table(
            canon, ids, panel, cd.k_y(oH["b31"], co)
        )
        for b in range(nb):
            sl = slice(b * cc.BLOCK, (b + 1) * cc.BLOCK)
            put(ctx, f"hist/HIST_{s}_b{b}.npz", **{k: v[sl] for k, v in t.items()})
    try:
        sep = cg.separation(cg.Registry.load(ctx.store, version), tabs)
    except cg.RegistryLineage as exc:
        return {"status": exc.status, "values": {"detail": str(exc)}}
    first = {s: cg.first_token_ok(t, T, E, pi, s) for s, t in tabs.items()}
    c = tabs["fit" if "fit" in tabs else "test"]["canonical"]
    oa = {j: cm.symbol_order_a(inputs(ctx, j, c), c, P["perm"][j]) for j in cc.MODELS}
    st = sep["status"]
    st = cd.LINEAGE if st == "PASS" and not all(first.values()) else st
    st = co2.IDENTITY if st == "PASS" and not all(oa.values()) else st
    ydef = {s: int(t["Y_def"].sum()) for s, t in tabs.items()}
    return {"status": st, "values": dict(sep, first_token=first, order_a=oa, Y_def=ydef)}


def save_oracle(ctx, split, o, el) -> None:
    k = {f"{r}_{x}": o[r][x] for r in cc.ROLES for x in ("q", "qbar", "s", "le", "m32")}
    k.update(H_b31=o["H"]["b31"], H_b32=o["H"]["b32"], H_nuis=o["nuis"], **el)
    k.update(G_x=o["G_x"], G_y=o["G_y"], Y_def=o["Y_def"], k_Y=o["k_Y"])
    put(ctx, f"oracle/ORACLE_{split}.npz", sequence_id=table(ctx, split)["sequence_id"], **k)
    ctx.data.pop(f"oracle/ORACLE_{split}.npz", None)


def reg_files(ctx, version) -> None:
    pats = (f"registry/{version}*", f"registry/runs/{version}/**/*")
    for p in (q for pat in pats for q in sorted(Path(ctx.store).glob(pat)) if q.is_file()):
        ctx.data.setdefault("files", []).append(p.relative_to(ctx.store).as_posix())
