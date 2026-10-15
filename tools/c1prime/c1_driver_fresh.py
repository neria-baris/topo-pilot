"""C1' stage driver, part 4: the fresh stage S7 (protocol §16 rows 20-22, §12.3, §13, §15.3.11).
T-PRE runs every pre-scoring check on the fresh rows before any fresh primary/control A, Y or Z
exists; NUM certifies; ENDPOINT decides. Implemented in job 0026; never run on data in job 0026."""

from __future__ import annotations

import json

import c1_bounds as cb
import c1_cert
import c1_config
import c1_data
import c1_driver as d1
import c1_driver_cal as dc
import c1_driver_late as dl
import c1_endpoint as ce
import c1_fit
import c1_oracle as co
import numpy as np
import stage_records as sr
from c1_records import begin_stage

MODELS = c1_config.MODELS


class _SubStop(Exception):
    def __init__(self, name, status):
        super().__init__(f"{name}: {status}")
        self.name, self.status = name, status


def flat_oracle(r) -> dict:
    flat = {k: r[k] for k in ("G", "d", "lam", "lp", "lm", "seq", "H", "Hp", "Hm", "elig")}
    for k in ("H", "Hp", "Hm"):
        flat.update({f"{k}_b32": r["o"][k]["b32"], f"{k}_q": r["o"][k]["q"],
                     f"{k}_s": r["o"][k]["s"]})
    return flat


def _check(sub, name, res) -> None:
    sub[name] = res
    if res["status"] != "PASS":
        raise _SubStop(name, res["status"])


def tpre(ctx, H) -> dict:
    sub = {}
    try:
        _check(sub, "H1", d1.h1(ctx))
        for b in range(int(ctx.rel["k"])):
            canon, seq = c1_data.sample_block(ctx.data["T"], ctx.data["E"], ctx.data["pi"],
                                              "test", b)
            table = c1_data.history_table(canon, seq, c1_data.panels(seq, b))
            sr.save_npz(ctx.out / f"HIST_test_b{b}.npz", **table)
            ctx.data[("test", b)] = table
        reg2 = json.loads(open(ctx.rel["registry_v2"]["path"], encoding="utf-8").read())
        U = set()
        for (s, _), t in [(k, v) for k, v in ctx.data.items() if isinstance(k, tuple)]:
            if s == "test":
                U |= c1_data.table_union(t)
        hits = len(U & set(reg2["digests"]))
        pE = ctx.data["pi"] @ ctx.data["E"]
        first = all(c1_data.first_token_ok(t["canonical"][:, 0], pE, "test")
                    for (s, _), t in [(k, v) for k, v in ctx.data.items() if isinstance(k, tuple)]
                    if s == "test")
        _check(sub, "H2", {"status": "PASS" if not hits and first else "FAIL_TECHNICAL/LINEAGE",
                           "collisions": hits, "first_token_ok": first})
        r = d1.oracle_split(ctx, "test")
        frozen = json.loads((ctx.out / "ORACLE_FROZEN.json").read_text(encoding="utf-8"))
        r["elig"] = co.eligible(r["o"]["Hp"]["s"], r["o"]["Hm"]["s"], frozen["s_max"],
                                *(r["o"][k]["log_evidence"] for k in ("H", "Hp", "Hm")))
        _check(sub, "H3", d1.h3(ctx, splits=("test",)))
        cert = cb.row_certificate(ctx, r, np.flatnonzero(r["elig"]))
        _check(sub, "N0", {"status": cert["status"], "route_F": cert["route_F_count"]})
        f_val = float(np.load(ctx.out / "ORACLE_val.npz")["elig"].mean())
        f_test = co.eligible_fraction(r["elig"])
        ok = ce.fresh_fraction_ok(f_test, f_val)
        _check(sub, "fraction", {"status": "PASS" if ok else "INCONCLUSIVE/TEST_GATE",
                                 "f_test": f_test, "f_val": f_val})
        _check(sub, "H5", ce.h5(r["G"][r["elig"]], cert["B_H"], 520506))
        ctx.data["oracle_test"] = flat_oracle(r)
        S = H["S"] = dl.setup_split(ctx, "test")
        S["coords"] = ctx.data["coords"]
        ident = dl.identity_checks_split(ctx, S, tail=False)
        _check(sub, "M0", {"status": "PASS" if ident["ok"] else "FAIL_TECHNICAL/MODEL",
                           "models": ident["models"]})
        dl.states(ctx, S)
        _check(sub, "M1", _m1(S))
        stats = dl.m23(ctx, S)
        _check(sub, "M2", dc._per_model(stats, "m2"))
        _check(sub, "M3", dc._per_model(stats, "m3"))
        _check(sub, "M4", dl.m4_gate(S))
        _check(sub, "V1", dl.v12(S, "V1"))
        _check(sub, "V2", dl.v12(S, "V2"))
        rc = {"bG": np.asarray(cert["bG"]), "rho_p": np.array([c1_cert.up(x)
                                                                for x in cert["rho_p"]]),
              "rho_m": np.array([c1_cert.up(x) for x in cert["rho_m"]]),
              "e_l": np.array([float(x) for x in cert["e_l"]])}
        H["cert"] = rc
        _check(sub, "V3", dl._strip(dl.donor_contrast(ctx, S, rc, 520507), S))
        tail = dl.identity_checks_split(ctx, S, tail=True)
        _check(sub, "tail", {"status": "PASS" if tail["ok"] else "FAIL_TECHNICAL",
                             "models": tail["models"]})
    except _SubStop as stop:
        s = stop.status
        if not (s.startswith("FAIL_TECHNICAL") or s == "INCONCLUSIVE/NUMERICAL"):
            s = "INCONCLUSIVE/TEST_GATE"
        return {"status": s, "reason": f"{stop.name}: {stop.status}", "sub": _summ(sub)}
    return {"status": "PASS", "sub": _summ(sub)}


def _summ(sub) -> dict:
    return {k: v.get("status") for k, v in sub.items()}


def _m1(S) -> dict:
    out = {}
    for m in MODELS:
        mm, st = S["per"][m], S["per"][m]["st"]
        e = st["elig"]
        out[m] = c1_fit.m1_report(mm["white"]["W"], [st["Dp"][e], st["Dm"][e]], st["Qt"],
                                  st["frames"], [st["cp"], st["cm"]], mm["white"]["W_inv"])
    return dc._per_model({m: {"m1": v} for m, v in out.items()}, "m1")


def num(ctx, H) -> dict:
    S, rc = H["S"], H["cert"]
    ep = H["ep"] = dl.endpoint_arrays(ctx, S)
    r, e = S["r"], S["r"]["elig"]
    d, qp, qm, G = r["d"][e], r["Hp_q"][e], r["Hm_q"][e], r["G"][e]
    p0 = c1_cert.p0(ctx.data["T"], [ctx.data["E"]], ctx.data["pi"])
    c, V, B, n = cb.bound_constants(), d.shape[1], {}, int(e.sum())
    lists = {"d": [np.abs(d[:, v]) for v in range(V)], "qp": [qp[:, v] for v in range(V)],
             "qm": [qm[:, v] for v in range(V)]}

    def bA(zp, zm):
        Dl = np.abs(zp - zm)
        return cb.b_A(lists["d"], [Dl[:, v] for v in range(V)], lists["qp"], lists["qm"],
                      rc["rho_p"], rc["rho_m"], Dl.max(axis=1), c1_cert.up(p0["omega_TE"]), c)

    for m in MODELS:
        x = ep[m]
        bT, bC = bA(*x["zT"]), [bA(*arms) for arms in x["zC"]]
        bY = cb.b_Y(np.abs(x["Y"]), bT, bC, [np.abs(a) for a in x["A_C"]], c)
        bZ = cb.b_Z(np.abs(x["Z"]), bY, np.abs(G), rc["bG"], c)
        logits = [x["zT"][0], x["zT"][1]] + [z for arms in x["zC"] for z in arms]
        if not c1_cert.p2_leaves(logits=logits, scores=[x["A_T"], x["Y"], x["Z"]] + x["A_C"],
                                 leaves=[np.abs(z) for z in logits]):
            return {"status": "FAIL_TECHNICAL/NUMERICAL", "reason": f"P2 at NUM, model {m}"}
        B[m] = cb.B_constant(float(np.max(bZ)), float(np.max(np.abs(x["Z"]))), n)
    bounds = ce.endpoint_bounds({m: ep[m]["Z"] for m in MODELS}, 520503, 5000)
    pm = bounds["per_model"]
    guard = cb.guard_endpoint({m: pm[m]["L"] for m in MODELS}, {m: pm[m]["U"] for m in MODELS}, B)
    H["bounds"] = pm
    return {"status": guard["status"], "B_num": {m: str(v) for m, v in B.items()},
            "bounds": pm, "n_test": n}


def endpoint(ctx, H) -> dict:
    pm = H["bounds"]
    statuses = {m: ce.per_model_status(pm[m]["L"], pm[m]["U"]) for m in MODELS}
    outcome = ce.overall(statuses)
    G = H["S"]["r"]["G"][H["S"]["r"]["elig"]]
    theta = {m: float(np.mean(H["ep"][m]["Y"]) / np.mean(G)) for m in MODELS}
    sr.write_new(ctx.out / "ENDPOINT.json", {"outcome": outcome, "per_model": statuses,
                                             "bounds": pm, "theta_hat": theta,
                                             "qualifier": "chart built by the LCC >= 95% rule; "
                                                          "operational"})
    return {"status": "PASS", "outcome": outcome, "per_model": statuses}


def run_fresh(ctx) -> None:
    begin_stage(ctx.out, "fresh", MODELS)
    ctx.data["proc"] = d1._process(ctx)
    H = {}
    d1.gate(ctx, "T-PRE", lambda: tpre(ctx, H))
    d1.gate(ctx, "NUM", lambda: num(ctx, H))
    d1.gate(ctx, "ENDPOINT", lambda: endpoint(ctx, H))
    sr.complete(ctx.out, "fresh", ["ENDPOINT.json"])
