"""C1' stage driver, part 2: per-split model work (activations, phases, forced and control
states, decodes, M2/M3 statistics) and the calibration stage S4 (protocol §16 rows 6-11, §5-§9).
Implemented in job 0026; never run on data in job 0026."""

from __future__ import annotations

import json

import c1_chart
import c1_config
import c1_driver as d1
import c1_endpoint
import c1_fit
import c1_gates
import c1_model
import c1_oracle as co
import chart
import numpy as np
import stage_records as sr
from c1_records import C1GateFailure, begin_stage

MODELS = c1_config.MODELS
CFG = c1_config.chart_cfg()


def load_checkpoint(ctx, model):
    from topo_pilot.contracts import ArtifactStore, Checkpoint
    from topo_pilot.contracts.backends import LocalFSBackend

    root = c1_config.Path(ctx.contract["artifacts"]["artifact_root"])
    store = ArtifactStore(LocalFSBackend(root))
    ck = ctx.contract["artifacts"]["per_model"][str(model)]["checkpoint"]
    return store.load(Checkpoint, ck, consumer="experiment")


def reload_oracle(ctx, split) -> dict:
    with np.load(ctx.out / f"ORACLE_{split}.npz", allow_pickle=False) as z:
        r = {k: z[k] for k in z.files}
    tabs = sorted(ctx.out.glob(f"HIST_{split}_b*.npz"))
    canon = np.vstack([np.load(t)["canonical"] for t in tabs])
    r["H"], r["Hp"], r["Hm"] = co.donors(canon)
    return r


def model_rows(ctx, model64, perm, r) -> dict:
    """Natural and donor activations (named tokens), logits discarded unread."""
    named = {k: perm[r[k]] for k in ("H", "Hp", "Hm")}
    inp = {k: c1_model.model_inputs(v) for k, v in named.items()}
    acts = {k: c1_model.activations(model64, inp[k]) for k in inp}
    return {"inputs": inp, "a": acts}


def phases(prod, gauge, A, timed=None):
    ext = c1_chart.extend_phase(prod, gauge, A, CFG, timed=timed)
    return ext.phase, ext.supported


def split_states(ctx, m, fit, white, prod, gauge, rows, r, elig, frames) -> dict:
    """phi, forced and control states, decodes and support for one model on one split."""
    a, ap, am = rows["a"]["H"], rows["a"]["Hp"], rows["a"]["Hm"]
    ph = {k: phases(prod, gauge, x) for k, x in (("S", a), ("p", ap), ("m", am))}
    e = np.asarray(elig, dtype=bool)
    Dp = c1_fit.forced(a, fit["B"], ph["S"][0], ph["p"][0]) - a
    Dm = c1_fit.forced(a, fit["B"], ph["S"][0], ph["m"][0]) - a
    Qt, cp = c1_fit.primary_coords(white["W"], fit["B"], Dp[e])
    _, cm = c1_fit.primary_coords(white["W"], fit["B"], Dm[e])
    return {"a": a, "ap": ap, "am": am, "ph": ph, "Dp": Dp, "Dm": Dm, "Qt": Qt, "cp": cp,
            "cm": cm, "frames": frames, "elig": e}


def damage_support(ctx, st, dec, fit, white, zt, zt_p, zt_m, w32, nu_p, nu_m, q99_, trcov,
                   prod, gauge, active) -> dict:
    """M2 and M3 statistics on the eligible rows of one split (activations only, no logits)."""
    e = st["elig"]
    a, ap, am = st["a"][e], st["ap"][e], st["am"][e]
    Tp, Tm = a + st["Dp"][e], a + st["Dm"][e]
    wn, yn = c1_fit.w_hat(dec["w32"], a), dec["ymarg"].predict(a)
    wT = [c1_fit.w_hat(dec["w32"], x) for x in (Tp, Tm)]
    yT = [dec["ymarg"].predict(x) for x in (Tp, Tm)]
    DM = (lambda x, z: c1_gates.mahalanobis(x, w32[e], z, fit, white))  # noqa: E731
    F_S = c1_gates.frac_beyond(DM(a, zt[e]), q99_)
    F_D = c1_gates.frac_beyond(np.r_[DM(ap, zt_p[e]), DM(am, zt_m[e])], q99_)
    F_T = c1_gates.frac_beyond(np.r_[DM(Tp, zt[e]), DM(Tm, zt[e])], q99_)
    sup = lambda X: float(np.mean(phases(prod, gauge, X)[1]))  # noqa: E731
    Sup = {"S": sup(a), "D": sup(np.vstack((ap, am))), "T": sup(np.vstack((Tp, Tm)))}
    Dw_C, Dy_C, F_C, Sup_C = [], [], [], []
    for Q in st["frames"]:
        Cp = a + c1_fit.control_delta(white["W_inv"], Q, st["cp"])
        Cm = a + c1_fit.control_delta(white["W_inv"], Q, st["cm"])
        Dw_C.append(c1_gates.D_w(wn, [c1_fit.w_hat(dec["w32"], x) for x in (Cp, Cm)]))
        Dy_C.append(c1_gates.D_y(yn, [dec["ymarg"].predict(x) for x in (Cp, Cm)], trcov))
        F_C.append(c1_gates.frac_beyond(np.r_[DM(Cp, zt[e]), DM(Cm, zt[e])], q99_))
        Sup_C.append(sup(np.vstack((Cp, Cm))))
    Sup["C"] = float(np.mean(Sup_C))
    L_T = c1_gates.leakage(yT[0], yT[1], nu_p[e], nu_m[e])
    m2 = c1_gates.m2(c1_gates.D_w(wn, wT), c1_gates.D_y(yn, yT, trcov), Dw_C, Dy_C, L_T, active)
    m3 = c1_gates.m3(F_S, F_D, F_T, F_C, Sup)
    return {"m2": m2, "m3": m3}


def decoder_targets(r, coords) -> dict:
    w = r["H"][:, 31]
    return {"w32": (w[:, None] == np.arange(36)[None, :]).astype(np.float64),
            "ymarg": co.y_marginal(r["H_b32"], coords), "m32": co.m32(r["H_b32"], coords)}


def run_calibration(ctx) -> None:
    begin_stage(ctx.out, "calibration", MODELS)
    ctx.data["proc"] = d1._process(ctx)
    p, frozen = ctx.data["proc"], json.loads((ctx.out / "ORACLE_FROZEN.json").read_text())
    r = reload_oracle(ctx, "cal")
    coords, active = p["coords"], co.leakage_active(frozen["kappa_nu"])
    panel = np.concatenate([np.load(t)["panel"] for t in sorted(ctx.out.glob("HIST_cal_b*.npz"))])
    m0_rows = np.sort(np.argsort(r["seq"], kind="stable")[:1024])
    b0 = np.flatnonzero(panel < 4)
    land = b0[np.argsort(r["seq"][b0], kind="stable")[:512]]
    ledger = c1_chart.ConstructionLedger(ctx.out / "CHART_CONSTRUCTIONS.json")
    z_raw = {k: co.nuisance(r[f"{k}_b32"], coords) for k in ("H", "Hp", "Hm")}
    mean, scale = c1_fit.standardise_nuisance(z_raw["H"])
    zt = {k: (v - mean) / scale for k, v in z_raw.items()}
    targets = decoder_targets(r, coords)
    nu = {k: co.y_marginal(r[f"{k}_b32"], coords) for k in ("H", "Hp", "Hm")}
    trcov = float(np.trace(np.cov(nu["H"].T, ddof=0)))
    per = ctx.data["cal"] = {}
    for m in MODELS:
        model64, sha = c1_model.load_model64(load_checkpoint(ctx, m))
        rows = model_rows(ctx, model64, p["perm"][m], r)
        per[m] = {"model64": model64, "sha": sha, "rows": rows}

    def m0():
        out = {}
        for m in MODELS:
            ctx.policy.require("identity_check")
            mm, inp = per[m], per[m]["rows"]["inputs"]["H"][m0_rows]
            a0 = mm["rows"]["a"]["H"][m0_rows]
            ident = c1_model.identity_patch_ok(mm["model64"], inp, a0)
            zp, zm = (c1_model.patched_logits(mm["model64"], inp, a0) for _ in range(2))
            perm = p["perm"][m]
            A0 = c1_endpoint.A_hat(r["d"][m0_rows], co.canonical_from_named_cols(zp, perm),
                                   co.canonical_from_named_cols(zm, perm))
            zero = bool(np.all(A0 == 0.0))
            out[m] = {"sha_f32": mm["sha"], "identity": ident, "zero_patch": zero}
        ok = all(v["identity"] and v["zero_patch"] for v in out.values())
        return {"status": "PASS" if ok else "FAIL_TECHNICAL/MODEL", "models": out}

    d1.gate(ctx, "M0", m0)

    def c0_cal():
        out = {}
        for m in MODELS:
            ledger.claim(m, "production")
            persist = (lambda name, obj, m=m: sr.write_new(  # noqa: E731
                ctx.out / f"CHART_{m}_production_{name}.json", obj))
            ids = c1_chart.landmark_ids(r["seq"][land])
            prod = c1_chart.fit_chart_lcc(per[m]["rows"]["a"]["H"][land], ids, CFG,
                                          guard=ctx.guard, timed=ctx.timed, persist=persist)
            cstar = np.asarray(prod.info["cstar"])
            gauge = c1_chart.fit_production_gauge(prod, co.m32(r["H_b32"][land][cstar], coords))
            sr.save_npz(ctx.out / f"CHART_{m}_production.npz",
                        **c1_chart.serialise(prod, gauge, "production"))
            per[m].update(prod=prod, gauge=gauge)
            out[m] = {"m": prod.info["m"], "alignment": gauge.alignment,
                      "sha256": sr.sha256(ctx.out / f"CHART_{m}_production.npz")}
        return {"status": "PASS", "models": out}

    d1.gate(ctx, "C0-cal", c0_cal, chart=True)

    def f1():
        out = {}
        for m in MODELS:
            a = per[m]["rows"]["a"]["H"]
            phi = phases(per[m]["prod"], per[m]["gauge"], a)[0]
            fit = c1_fit.fit_fwl(a, r["H"][:, 31], zt["H"], phi)
            st1 = c1_fit.f1_check(fit)
            white = c1_fit.whitening(c1_fit.residual(a, r["H"][:, 31], zt["H"], fit))
            decs = {t: c1_fit.fit_decoder(a, y, panel, m, t) for t, y in targets.items()}
            per[m].update(fit=fit, white=white, dec=decs)
            out[m] = {"f1": st1, "whitening": white["status"], "cond": fit["cond"],
                      "partial_r2": c1_fit.partial_r2(a, r["H"][:, 31], zt["H"], phi)}
            if st1 != "PASS" or white["status"] != "PASS":
                return {"status": st1 if st1 != "PASS" else white["status"], "models": out}
        return {"status": "PASS", "models": out}

    d1.gate(ctx, "F1", f1)

    def m1():
        out = {}
        for m in MODELS:
            mm = per[m]
            st = split_states(ctx, m, mm["fit"], mm["white"], mm["prod"], mm["gauge"],
                              mm["rows"], r, r["elig"], c1_fit.haar_frames(m))
            mm["st"] = st
            rep = c1_fit.m1_report(mm["white"]["W"], [st["Dp"][st["elig"]],
                                                      st["Dm"][st["elig"]]], st["Qt"],
                                   st["frames"], [st["cp"], st["cm"]], mm["white"]["W_inv"])
            decs = mm["dec"].values()
            eq = max(d.equivalence for d in decs)
            eq_ok = all(d.equivalence <= d.eq_tol for d in decs)  # ruling R13 (job 0042)
            out[m] = dict(rep, ridge_equivalence=eq, ridge_equivalence_ok=eq_ok,
                          ridge_tol={t: d.eq_tol for t, d in mm["dec"].items()},
                          ridge_kappa={t: d.kappa for t, d in mm["dec"].items()},
                          ridge_lam={t: d.lam for t, d in mm["dec"].items()})
            if rep["status"] != "PASS" or not eq_ok:
                return {"status": "FAIL_TECHNICAL", "models": out}
        return {"status": "PASS", "models": out}

    d1.gate(ctx, "M1", m1)
    DMcal = {m: c1_gates.mahalanobis(per[m]["rows"]["a"]["H"], r["H"][:, 31], zt["H"],
                                     per[m]["fit"], per[m]["white"]) for m in MODELS}
    q99s = {m: c1_gates.q99(DMcal[m]) for m in MODELS}
    stats = {}

    def m2():
        stats.update({m: damage_support(ctx, per[m]["st"], per[m]["dec"], per[m]["fit"],
                                        per[m]["white"], zt["H"], zt["Hp"], zt["Hm"],
                                        r["H"][:, 31], nu["Hp"], nu["Hm"], q99s[m], trcov,
                                        per[m]["prod"], per[m]["gauge"], active)
                      for m in MODELS})
        return _per_model(stats, "m2")

    d1.gate(ctx, "M2-cal", m2)
    d1.gate(ctx, "M3-cal", lambda: _per_model(stats, "m3"))
    for m in MODELS:
        save_fit(ctx, m, per[m], q99s[m], mean, scale, trcov)
    sr.complete(ctx.out, "calibration", [f"FIT_{m}.npz" for m in MODELS]
                + [f"CHART_{m}_production.npz" for m in MODELS])


def _per_model(stats, key) -> dict:
    out = {m: s[key] for m, s in stats.items()}
    bad = [v["status"] for v in out.values() if v["status"] != "PASS"]
    return {"status": bad[0] if bad else "PASS", "models": out}


def save_fit(ctx, m, mm, q99_, mean, scale, trcov) -> None:
    arrays = {"alpha": mm["fit"]["alpha"], "Gamma": mm["fit"]["Gamma"], "B": mm["fit"]["B"],
              "W": mm["white"]["W"], "W_inv": mm["white"]["W_inv"], "r_mean": mm["white"]["mean"],
              "q99": np.array(q99_), "z_mean": mean, "z_scale": scale, "trcov": np.array(trcov)}
    for t, dec in mm["dec"].items():
        arrays.update({f"{t}_{k}": v for k, v in c1_fit.decoder_arrays(dec).items()})
    sr.save_npz(ctx.out / f"FIT_{m}.npz", **arrays)


def load_fit(ctx, m) -> dict:
    with np.load(ctx.out / f"FIT_{m}.npz", allow_pickle=False) as z:
        a = {k: z[k] for k in z.files}
    fit = {"alpha": a["alpha"], "Gamma": a["Gamma"], "B": a["B"]}
    white = {"W": a["W"], "W_inv": a["W_inv"], "mean": a["r_mean"], "status": "PASS"}
    decs = {t: c1_fit.decoder_from_arrays({k[len(t) + 1:]: v for k, v in a.items()
                                           if k.startswith(t + "_")})
            for t in ("w32", "ymarg", "m32")}
    with np.load(ctx.out / f"CHART_{m}_production.npz", allow_pickle=False) as z:
        prod, gauge = chart.chart_from_arrays({k: z[k] for k in z.files})
    if not gauge.alignment > 0:
        raise C1GateFailure("FAIL_TECHNICAL", "frozen production gauge missing")
    return {"fit": fit, "white": white, "dec": decs, "prod": prod, "gauge": gauge,
            "q99": float(a["q99"]), "z_mean": a["z_mean"], "z_scale": a["z_scale"],
            "trcov": float(a["trcov"])}
