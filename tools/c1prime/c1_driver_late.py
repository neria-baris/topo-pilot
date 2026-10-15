"""C1' stage driver, part 3: shared split evaluation (C0-val, M4, M2, M3, V1, V2, V3, P1
statistics) and the validation stage S5 (protocol §16 rows 12-19, §10-§12). Implemented in job
0026; never run on data in job 0026. Validation means are written sealed and never read here."""

from __future__ import annotations

import json

import c1_bounds as cb
import c1_cert
import c1_chart
import c1_config
import c1_driver as d1
import c1_driver_cal as dc
import c1_endpoint as ce
import c1_fit
import c1_gates
import c1_model
import c1_oracle as co
import numpy as np
import stage_records as sr
from c1_records import begin_stage

MODELS, CFG = c1_config.MODELS, dc.CFG


def setup_split(ctx, split) -> dict:
    """Models, frozen fits and split rows (activations only) for validation or fresh."""
    ctx.data["proc"] = p = d1._process(ctx)
    ctx.data.update(T=p["T"], E=p["canon"][MODELS[0]], pi=p["pi"], coords=p["coords"])
    r = ctx.data.get(f"oracle_{split}") or dc.reload_oracle(ctx, split)
    frozen = json.loads((ctx.out / "ORACLE_FROZEN.json").read_text(encoding="utf-8"))
    cal = dc.reload_oracle(ctx, "cal")
    per = {}
    for m in MODELS:
        model64, sha = c1_model.load_model64(dc.load_checkpoint(ctx, m))
        per[m] = dict(dc.load_fit(ctx, m), model64=model64, sha=sha,
                      rows=dc.model_rows(ctx, model64, p["perm"][m], r))
    z_raw = {k: co.nuisance(r[f"{k}_b32"] if f"{k}_b32" in r else r["o"][k]["b32"],
                            p["coords"]) for k in ("H", "Hp", "Hm")}
    first = per[MODELS[0]]
    zt = {k: (v - first["z_mean"]) / first["z_scale"] for k, v in z_raw.items()}
    nu = {k: co.y_marginal(_b32(r, k), p["coords"]) for k in ("H", "Hp", "Hm")}
    nu_cal_mean = co.y_marginal(cal["H_b32"], p["coords"]).mean(axis=0)
    return {"r": r, "per": per, "zt": zt, "nu": nu, "nu_cal_mean": nu_cal_mean,
            "active": co.leakage_active(frozen["kappa_nu"]), "frozen": frozen}


def _b32(r, k):
    return r[f"{k}_b32"] if f"{k}_b32" in r else r["o"][k]["b32"]


def c0_val_gate(ctx, S) -> dict:
    r, out = S["r"], {}
    ledger = c1_chart.ConstructionLedger(ctx.out / "CHART_CONSTRUCTIONS.json")
    panel = np.concatenate([np.load(t)["panel"] for t in sorted(ctx.out.glob("HIST_val_b*.npz"))])
    b0 = np.flatnonzero(panel < 4)
    land = b0[np.argsort(r["seq"][b0], kind="stable")[:512]]
    for m in MODELS:
        mm = S["per"][m]
        ledger.claim(m, "direct")
        persist = (lambda name, obj, m=m: sr.write_new(  # noqa: E731
            ctx.out / f"CHART_{m}_direct_{name}.json", obj))
        X = mm["rows"]["a"]["H"][land]
        direct = c1_chart.fit_chart_lcc(X, c1_chart.landmark_ids(r["seq"][land]), CFG,
                                        guard=ctx.guard, timed=ctx.timed, persist=persist)
        sr.save_npz(ctx.out / f"CHART_{m}_direct.npz",
                    **c1_chart.serialise(direct, c1_chart.IDENTITY_CARRIER, "direct"))
        out[m] = c1_chart.c0_val(mm["prod"], mm["gauge"], X, direct, CFG)
    bad = [v["status"] for v in out.values() if v["status"] != "PASS"]
    return {"status": bad[0] if bad else "PASS", "models": out}


def states(ctx, S) -> None:
    for m in MODELS:
        mm = S["per"][m]
        mm["st"] = dc.split_states(ctx, m, mm["fit"], mm["white"], mm["prod"], mm["gauge"],
                                   mm["rows"], S["r"], S["r"]["elig"], c1_fit.haar_frames(m))


def m4_gate(S) -> dict:
    r, e, out = S["r"], S["r"]["elig"], {}
    for m in MODELS:
        dec, a = S["per"][m]["dec"], S["per"][m]["rows"]["a"]["H"][e]
        out[m] = c1_gates.m4(c1_fit.w_hat(dec["w32"], a), r["H"][e, 31],
                             dec["ymarg"].predict(a), S["nu"]["H"][e], S["nu_cal_mean"])
    return dc._per_model({m: {"m4": v} for m, v in out.items()}, "m4")


def m23(ctx, S) -> dict:
    stats = {}
    for m in MODELS:
        mm = S["per"][m]
        stats[m] = dc.damage_support(ctx, mm["st"], mm["dec"], mm["fit"], mm["white"],
                                     S["zt"]["H"], S["zt"]["Hp"], S["zt"]["Hm"], S["r"]["H"][:, 31],
                                     S["nu"]["Hp"], S["nu"]["Hm"], mm["q99"], mm["trcov"],
                                     mm["prod"], mm["gauge"], S["active"])
    return stats


def v12(S, which) -> dict:
    r, e, out, coords = S["r"], S["r"]["elig"], {}, S["coords"]
    for m in MODELS:
        st, mm = S["per"][m]["st"], S["per"][m]
        ph = st["ph"]
        if which == "V1":
            out[m] = c1_gates.v1(ph["p"][0][e], ph["m"][0][e], co.m32(_b32(r, "Hp")[e], coords),
                                 co.m32(_b32(r, "Hm")[e], coords))
        else:
            phT = [dc.phases(mm["prod"], mm["gauge"], st["a"][e] + D[e])[0]
                   for D in (st["Dp"], st["Dm"])]
            out[m] = c1_gates.v2(ph["S"][0][e], [ph["p"][0][e], ph["m"][0][e]], phT)
    return dc._per_model({m: {"v": v} for m, v in out.items()}, "v")


def donor_contrast(ctx, S, cert, seed) -> dict:
    """V3: A_full from the model's own donor logits, Z_full, b^Zf, B^V3 and the guard."""
    ctx.policy.require("donor")
    r, e = S["r"], S["r"]["elig"]
    p0 = ctx.data.get("p0") or c1_cert.p0(ctx.data["T"], [ctx.data["E"]], ctx.data["pi"])
    c, Zf, B = cb.bound_constants(), {}, {}
    d, qp, qm, G = r["d"][e], r["Hp_q"][e], r["Hm_q"][e], r["G"][e]
    for m in MODELS:
        mm, perm = S["per"][m], ctx.data["proc"]["perm"][m]
        z = {k: co.canonical_from_named_cols(c1_model.natural_logits(
            mm["model64"], mm["rows"]["inputs"][k][e]), perm) for k in ("Hp", "Hm")}
        A_full = ce.A_hat(d, z["Hp"], z["Hm"])
        Zf[m] = ce.Zfull_hat(A_full, G)
        Delta = np.abs(z["Hp"] - z["Hm"])
        V = d.shape[1]
        bA = cb.b_A([np.abs(d[:, v]) for v in range(V)], [Delta[:, v] for v in range(V)],
                    [qp[:, v] for v in range(V)], [qm[:, v] for v in range(V)], cert["rho_p"],
                    cert["rho_m"], Delta.max(axis=1), c1_cert.up(p0["omega_TE"]), c)
        bZf = cb.b_Zf(np.abs(Zf[m]), bA, np.abs(G), cert["bG"], c)
        ok2 = c1_cert.p2_leaves(logits=(z["Hp"], z["Hm"]), scores=(A_full, Zf[m]),
                                leaves=(Delta, Delta.max(axis=1), np.abs(Zf[m])))
        if not ok2:
            return {"status": "FAIL_TECHNICAL/NUMERICAL", "reason": f"P2 at V3, model {m}"}
        B[m] = cb.B_constant(float(np.max(bZf)), float(np.max(np.abs(Zf[m]))), int(e.sum()))
    res = ce.v3(Zf, B, seed)
    return dict(res, B_V3={m: str(v) for m, v in B.items()}, _Zf=Zf)


def endpoint_arrays(ctx, S) -> dict:
    """Primary and control logits (reference and tail paths), A_T, A_C, Y and Z per model."""
    ctx.policy.require("endpoint")
    r, e = S["r"], S["r"]["elig"]
    d, G, out = r["d"][e], r["G"][e], {}
    for m in MODELS:
        mm, perm, st = S["per"][m], ctx.data["proc"]["perm"][m], S["per"][m]["st"]
        inp, a = mm["rows"]["inputs"]["H"][e], st["a"][e]
        canon = (lambda z: co.canonical_from_named_cols(z, perm))  # noqa: E731
        zT = [canon(c1_model.patched_logits(mm["model64"], inp, a + D[e]))
              for D in (st["Dp"], st["Dm"])]
        A_T = ce.A_hat(d, zT[0], zT[1])
        A_C, zC = [], []
        for Q in st["frames"]:
            arms = [canon(c1_model.tail_logits(mm["model64"], a + c1_fit.control_delta(
                mm["white"]["W_inv"], Q, cc))) for cc in (st["cp"], st["cm"])]
            zC.append(arms)
            A_C.append(ce.A_hat(d, arms[0], arms[1]))
        Y = ce.Y_hat(A_T, A_C)
        out[m] = {"A_T": A_T, "A_C": A_C, "Y": Y, "Z": ce.Z_hat(Y, G), "zT": zT, "zC": zC}
    return out


def identity_checks_split(ctx, S, tail) -> dict:
    """Identity patch bitwise on every eligible row (tail=False) or the tail-path identity on
    T+- within 1e-12 (tail=True)."""
    ctx.policy.require("identity_check")
    e, out = S["r"]["elig"], {}
    for m in MODELS:
        mm, st = S["per"][m], S["per"][m]["st"] if "st" in S["per"][m] else None
        inp, a = mm["rows"]["inputs"]["H"][e], mm["rows"]["a"]["H"][e]
        if tail:
            out[m] = max(c1_model.tail_identity(mm["model64"], inp, a + D[e])
                         for D in (st["Dp"], st["Dm"]))
        else:
            out[m] = c1_model.identity_patch_ok(mm["model64"], inp, a)
    ok = all(v <= 1e-12 for v in out.values()) if tail else all(out.values())
    return {"ok": bool(ok), "models": out}


def identity_checks(ctx, S) -> dict:
    ident, tail = identity_checks_split(ctx, S, False), identity_checks_split(ctx, S, True)
    return {"ok": ident["ok"] and tail["ok"], "identity": ident["models"],
            "tail": tail["models"]}


def run_validation(ctx) -> None:
    begin_stage(ctx.out, "validation", MODELS)
    S = setup_split(ctx, "val")
    S["coords"] = ctx.data["coords"]
    with np.load(ctx.out / "CERT_val.npz", allow_pickle=False) as z:
        cert = {k: z[k] for k in z.files}
    d1.gate(ctx, "C0-val", lambda: c0_val_gate(ctx, S), chart=True)
    d1.gate(ctx, "M4", lambda: m4_gate(S))
    stats = {}

    def m2():
        states(ctx, S)
        stats.update(m23(ctx, S))
        return dc._per_model(stats, "m2")

    d1.gate(ctx, "M2-val", m2)
    d1.gate(ctx, "M3-val", lambda: dc._per_model(stats, "m3"))
    d1.gate(ctx, "V1", lambda: v12(S, "V1"))
    d1.gate(ctx, "V2", lambda: v12(S, "V2"))
    v3res = d1.gate(ctx, "V3", lambda: _strip(donor_contrast(ctx, S, cert, 520504), S))

    def p1():
        ident = identity_checks(ctx, S)
        if not ident["ok"]:
            return {"status": "FAIL_TECHNICAL", "identity": ident}
        S["ep"] = endpoint_arrays(ctx, S)
        G = S["r"]["G"][S["r"]["elig"]]
        lad = ce.ladder({m: S["ep"][m]["Z"] for m in MODELS}, G)
        sr.write_new(ctx.out / "GATE_REPORT_validation.json", {"ladder": _jsonable(lad),
                                                               "identity": _jsonable(ident)})
        return {"status": lad["status"], "N_test": lad["N_test"], "identity": ident}

    d1.gate(ctx, "P1", p1)
    _seal(ctx, S, v3res)
    sr.complete(ctx.out, "validation", ["GATE_REPORT_validation.json", "SEALED_VALIDATION.json"]
                + [f"CHART_{m}_direct.npz" for m in MODELS])


def _strip(res, S) -> dict:
    S["Zf"] = res.pop("_Zf")
    return res


def _seal(ctx, S, v3res) -> None:
    """Sealed validation means (§12.5): written once, never read by the driver."""
    G = S["r"]["G"][S["r"]["elig"]]
    sealed = {m: {"Z_mean": float(np.mean(S["ep"][m]["Z"])),
                  "theta": float(np.mean(S["ep"][m]["Y"]) / np.mean(G)),
                  "theta_full": float((np.mean(S["Zf"][m]) + 0.3 * np.mean(G)) / np.mean(G)),
                  "A_T_mean": float(np.mean(S["ep"][m]["A_T"])),
                  "A_C_frame_means": [float(np.mean(x)) for x in S["ep"][m]["A_C"]]}
              for m in MODELS}
    sr.write_new(ctx.out / "SEALED_VALIDATION.json", {"sealed": True, "models": sealed})


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    return x.tolist() if isinstance(x, np.ndarray) else x


def run(ctx, stage) -> None:
    if stage == "calibration":
        dc.run_calibration(ctx)
    elif stage == "validation":
        run_validation(ctx)
    elif stage == "fresh":
        import c1_driver_fresh

        c1_driver_fresh.run_fresh(ctx)
    else:
        raise SystemExit(f"unknown stage {stage!r}")
