"""C1' stage driver, part 1: context, gate runner, G0 and the oracle stage S3 (API.md §15;
protocol §16 rows 0-5, §2-§4, §15.3). Implemented in job 0026; never run on data in job 0026.
Usage (venv, through c1_meter_bind.py --release R): python c1_driver.py <stage> <release.json>"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import c1_cert
import c1_config
import c1_data
import c1_oracle as co
import c1_release
import error_bound
import numpy as np
import op_guard
import stage_records as sr
from c1_records import C1Stop, LogitPolicy, begin_stage, run_c1_gate

ROOT = Path(r"X:\Downloads\projects\topo-pilot")
MODELS = c1_config.MODELS


@dataclass
class Ctx:
    out: Path
    contract: dict
    rel: dict
    policy: LogitPolicy
    timed: object
    guard: object
    data: dict = field(default_factory=dict)


def _guard(rel, out):
    import controls

    controls.JOB_ID, controls.TASK_SHA256 = str(rel["job_id"]), str(rel["task_sha256"]).upper()

    def guard():
        state, why = controls.classify_all([controls.MAILBOX], out)
        if state != controls.CONTINUE:
            raise C1Stop("GUARD", "INCONCLUSIVE/RESOURCE", f"{state}: {why}")

    return guard


def make_context(release_path) -> Ctx:
    import c1_freeze

    contract = c1_config.CONTRACT
    out = Path(contract["resources"]["output_root"])
    rel = c1_release.verify(Path(release_path))
    c1_freeze.pin_check()
    done = [g["gate"] for g in sr.gates_so_far(out) if g["status"] == "PASS"]
    return Ctx(out, contract, rel, LogitPolicy(done), op_guard.timed_factory(out, 600.0),
               _guard(rel, out))


def gate(ctx, name, fn, chart=False):
    ctx.guard()
    ctx.policy.begin(name)
    res = run_c1_gate(ctx.out, name, fn, chart=chart)
    ctx.policy.passed(name)
    return res


def _sha(path) -> str:
    return c1_release._sha(path)


# ---- G0 (row 0) ------------------------------------------------------------
def g0(ctx) -> dict:
    auth, a = ctx.rel["authority"], ctx.contract["authority"]
    ok_owner = auth["owner_decisions"]["sha256"].lower() == a["owner_decisions"]["sha256"].lower()
    ok_diag = auth["diag_json"]["sha256"].lower() == a["diag_json_sha256"].lower()
    verdict = json.loads(Path(auth["diag_json"]["path"]).read_text(encoding="utf-8")).get(
        "verdict")
    accept = "ACCEPT" in Path(auth["job_0023_accept"]["path"]).read_text(encoding="utf-8")
    if not (ok_owner and ok_diag and verdict == "GO" and accept):
        return {"status": "INCONCLUSIVE/CHART_UNAVAILABLE", "reason": "authority record missing "
                f"or verdict not GO (owner {ok_owner}, diag {ok_diag}, {verdict}, {accept})"}
    k4 = ROOT / a["k4_freeze"]["path"]
    if _sha(k4) != a["k4_freeze"]["sha256"]:
        return {"status": "FAIL_TECHNICAL", "reason": "K4 FREEZE.json hash"}
    frozen = json.loads(k4.read_text(encoding="utf-8"))["files"]
    bad = [f for f in a["k4_freeze"]["bound_files"] if _sha(c1_config.REPO / f) != frozen[f]]
    if bad:
        return {"status": "FAIL_TECHNICAL", "reason": f"chart code hash mismatch {bad}"}
    prior = sorted(p.name for p in ctx.out.glob("HIST_*.npz"))
    issued = [str(p) for store in ROOT.glob("*-store*") for p in store.rglob("*.json")
              if p.stat().st_size < 5_000_000 and "data/c1-sf-v1" in p.read_text(
                  encoding="utf-8", errors="ignore")]
    if prior or issued:
        return {"status": "FAIL_TECHNICAL/LINEAGE", "reason": f"prior c1-sf-v1 use {prior}{issued}"}
    return {"status": "PASS", "e4_chart_inputs": "none", "k4_bound": a["k4_freeze"]["bound_files"]}


# ---- S3: oracle stage (rows 1-5) --------------------------------------------------
def _process(ctx) -> dict:
    import inputs
    from oracle_profile import canonical_emission

    cfg14 = inputs.load_config()
    art = ctx.contract["artifacts"]
    ids_ok = (cfg14["world"]["artifact"] == art["shared"]["WorldSpec"]
              and cfg14["transition"]["artifact"] == art["shared"]["TransitionSpec"]
              and {int(k): v for k, v in cfg14["emissions"].items()}
              == {int(m): v["EmissionSpec"] for m, v in art["per_model"].items()})
    proc = inputs.load_process(cfg14)
    canon = {int(m): canonical_emission(proc["E_named"][m], proc["perm"][m])
             for m in proc["E_named"]}
    return dict(proc, ids_ok=ids_ok, canon=canon, perm={int(k): np.asarray(v)
                                                       for k, v in proc["perm"].items()},
                E_named={int(k): v for k, v in proc["E_named"].items()})  # job 0039 R11


def h1(ctx) -> dict:
    p = ctx.data["proc"] = _process(ctx)
    T, pi = p["T"], p["pi"]
    E_list = [p["canon"][m] for m in MODELS]
    perms_ok = all(sorted(p["perm"][m].tolist()) == list(range(36)) for m in MODELS)
    roundtrip = all(np.array_equal(np.argsort(p["perm"][m])[p["perm"][m][np.arange(36)]],
                                   np.arange(36)) for m in MODELS)
    p0 = c1_cert.p0(T, E_list, pi)
    a1 = c1_cert.a1_selftest()
    ctx.data.update(E=E_list[0], T=T, pi=pi, coords=p["coords"], p0=p0)
    ok = p["ids_ok"] and perms_ok and roundtrip and p0["ok"] and a1["ok"]
    return {"status": "PASS" if ok else "FAIL_TECHNICAL/IDENTITY", "ids_ok": p["ids_ok"],
            "perms_ok": perms_ok, "roundtrip": roundtrip, "process_checks": p["process_checks"],
            "p0": {k: str(v) for k, v in p0.items() if k != "E_digests"},
            "E_digests": p0["E_digests"], "a1": a1}


def sample_s3(ctx) -> None:
    T, E, pi = ctx.data["T"], ctx.data["E"], ctx.data["pi"]
    for split, block in (("cal", 0), ("cal", 1), ("val", 0)):
        canon, seq = c1_data.sample_block(T, E, pi, split, block)
        table = c1_data.history_table(canon, seq, c1_data.panels(seq, block))
        sr.save_npz(ctx.out / f"HIST_{split}_b{block}.npz", **table)
        ctx.data[(split, block)] = table


def h2(ctx) -> dict:
    from topo_pilot.dataset.checks import check_disjoint

    reg = json.loads(Path(ctx.rel["registry_v1"]["path"]).read_text(encoding="utf-8"))
    tabs = {k: v for k, v in ctx.data.items() if isinstance(k, tuple)}
    seqs = {f"{s}_b{b}": t["sequence_id"] for (s, b), t in tabs.items()}
    if reg.get("sequence_ids"):
        seqs["stored"] = np.asarray(reg["sequence_ids"], dtype=np.int64)
    check_disjoint(**seqs)
    U = {s: set() for s in ("cal", "val")}
    for (s, _), t in tabs.items():
        U[s] |= c1_data.table_union(t)
    sep = c1_data.separation(U["cal"], U["val"], set(reg["digests"]))
    pE = ctx.data["pi"] @ ctx.data["E"]
    first = all(c1_data.first_token_ok(t["canonical"][:, 0], pE, s) for (s, _), t in tabs.items())
    status = sep["status"] if first else "FAIL_TECHNICAL/LINEAGE"
    return {"status": status, "collisions": sep["collisions"], "first_token_ok": first}


def oracle_split(ctx, split) -> dict:
    tabs = [t for (s, _), t in ((k, v) for k, v in ctx.data.items() if isinstance(k, tuple))
            if s == split]
    canon = np.vstack([t["canonical"] for t in tabs])
    seq = np.concatenate([t["sequence_id"] for t in tabs])
    H, Hp, Hm = co.donors(canon)
    T, E, pi = ctx.data["T"], ctx.data["E"], ctx.data["pi"]
    o = {k: co.run_oracle(T, E, pi, h) for k, h in (("H", H), ("Hp", Hp), ("Hm", Hm))}
    G, d, lam, lp, lm = co.G_hat(o["Hp"]["q"], o["Hm"]["q"])
    res = {"canon": canon, "seq": seq, "H": H, "Hp": Hp, "Hm": Hm, "o": o, "G": G, "d": d,
           "lam": lam, "lp": lp, "lm": lm}
    ctx.data[f"oracle_{split}"] = res
    return res


def eligibility(ctx) -> None:
    cal, val = oracle_split(ctx, "cal"), oracle_split(ctx, "val")
    smax = co.s_max(cal["o"]["H"]["s"])
    for r in (cal, val):
        r["elig"] = co.eligible(r["o"]["Hp"]["s"], r["o"]["Hm"]["s"], smax,
                                *(r["o"][k]["log_evidence"] for k in ("H", "Hp", "Hm")))
    nu = {k: co.y_marginal(cal["o"][k]["b32"], ctx.data["coords"]) for k in ("H", "Hp", "Hm")}
    ctx.data.update(s_max=smax, kappa=co.kappa_nu(nu["Hp"], nu["Hm"], nu["H"], cal["elig"]))


def _rel_rows(xh, xr, tol_) -> bool:
    return all(co.rel_agree(a, b, tol_) for a, b in zip(xh, xr))


def h3(ctx, splits=("cal", "val")) -> dict:
    T, E, pi, coords = ctx.data["T"], ctx.data["E"], ctx.data["pi"], ctx.data["coords"]
    sym = co.symmetry_report(T, E, pi, coords)
    if not sym["symmetry_ok"] or not sym["exact_invariance"]:
        return {"status": "FAIL_TECHNICAL/ORACLE", "symmetry": sym}
    tolcf = co.closed_form_tolerance(sym["eps_sym"])
    checks = {"closed_form": True, "named": True, "G_cross": True, "decimal": "PASS"}
    for split in splits:
        r = ctx.data[f"oracle_{split}"]
        for k, key in ((1, "Hp"), (-1, "Hm")):
            cf = co.closed_form_b32(r["o"]["H"]["b31"], T, E, r["H"][:, 31],
                                    co.rho_index(coords, k))
            if tolcf is None:
                return {"status": "FAIL_TECHNICAL/ORACLE", "reason": "closed-form enclosure "
                        "branch required (r_E >= 1 or t > 3/2)", "symmetry": sym}
            checks["closed_form"] &= _rel_rows(r["o"][key]["b32"], cf, tolcf[1])
        for m in MODELS:
            perm = ctx.data["proc"]["perm"][m]
            Gn = co.G_named(r["d"], r["lam"], perm)
            checks["G_cross"] &= bool(np.max(np.abs(Gn - r["G"])) <= 1e-12)
            for key in ("H", "Hp", "Hm"):
                named = perm[r[key]]
                qn = co.run_oracle(T, ctx.data["proc"]["E_named"][m], pi, named)["q"]
                checks["named"] &= _rel_rows(co.canonical_from_named_cols(qn, perm),
                                             r["o"][key]["q"], 4e-12)
        checks["decimal"] = _h3_decimal(ctx, r, split, checks["decimal"])
    ok = checks["closed_form"] and checks["named"] and checks["G_cross"]
    status = "FAIL_TECHNICAL/ORACLE" if not ok else checks["decimal"]
    return {"status": status, "checks": checks, "symmetry": {k: str(v) for k, v in sym.items()}}


def _h3_decimal(ctx, r, split, prior) -> str:
    T, E, pi, p0 = ctx.data["T"], ctx.data["E"], ctx.data["pi"], ctx.data["p0"]
    from c1_bounds import row_certificate

    rows = np.flatnonzero(r["elig"])[np.argsort(r["seq"][r["elig"]], kind="stable")[:4]]
    status = prior
    beta = Fraction(error_bound.posterior_envelope(32, p0["N"]))
    for i in rows:
        for key in ("H", "Hp", "Hm"):
            ref = co.decimal_reference(T, E, pi, r[key][i])
            ref0 = c1_cert.reference_oracle(T, E, pi, r[key][i:i + 1])
            p1 = bool(c1_cert.p1(ref0["nu_min"], ref0["finite"], p0["nu0"])[0])
            for xh, xd in ((r["o"][key]["b31"][i], ref["b31"]), (r["o"][key]["b32"][i],
                                                                 ref["b32"])):
                out = co.h3_compare(xh, xd, p1, beta)
                status = out if out != "PASS" and status == "PASS" else status
            if abs(Fraction(float(r["o"][key]["s"][i])) - Fraction(ref["s"])) > Fraction(1, 10**10):
                status = "FAIL_TECHNICAL/ORACLE"
        cert = row_certificate(ctx, r, np.array([i]))
        Gt = co.decimal_G(co.decimal_reference(T, E, pi, r["Hp"][i])["q32"],
                          co.decimal_reference(T, E, pi, r["Hm"][i])["q32"])
        if abs(Fraction(float(r["G"][i])) - Fraction(Gt)) > Fraction(cert["bG"][0]) + \
                Fraction(1, 10**30):
            status = "FAIL_TECHNICAL/ORACLE"
    return status


def h4(ctx) -> dict:
    f = {s: co.eligible_fraction(ctx.data[f"oracle_{s}"]["elig"]) for s in ("cal", "val")}
    ok = f["cal"] >= 0.90 and f["val"] >= 0.90
    return {"status": "PASS" if ok else "INCONCLUSIVE/ELIGIBILITY", "fractions": f,
            "s_max": ctx.data["s_max"], "kappa_nu": ctx.data["kappa"],
            "leakage_active": co.leakage_active(ctx.data["kappa"])}


def n0(ctx) -> dict:
    from c1_bounds import row_certificate

    r = ctx.data["oracle_val"]
    idx = np.flatnonzero(r["elig"])
    cert = ctx.data["cert_val"] = row_certificate(ctx, r, idx)
    sr.write_new(ctx.out / "CERT_val.json", {k: [str(x) for x in v] if isinstance(v, list)
                                             else str(v) for k, v in cert.items()})
    sr.save_npz(ctx.out / "CERT_val.npz", rows=idx, bG=np.asarray(cert["bG"]),
                rho_p=np.array([c1_cert.up(x) for x in cert["rho_p"]]),
                rho_m=np.array([c1_cert.up(x) for x in cert["rho_m"]]),
                e_l=np.array([float(x) for x in cert["e_l"]]))
    return {"status": cert["status"], "route_F": cert["route_F_count"], "B_H": str(cert["B_H"])}


def h5(ctx) -> dict:
    import c1_endpoint

    r, cert = ctx.data["oracle_val"], ctx.data["cert_val"]
    return c1_endpoint.h5(r["G"][r["elig"]], cert["B_H"], 520505)


def run_oracle_stage(ctx) -> None:
    begin_stage(ctx.out, "oracle", MODELS)
    gate(ctx, "G0", lambda: g0(ctx))
    gate(ctx, "H1", lambda: h1(ctx))
    sample_s3(ctx)
    gate(ctx, "H2", lambda: h2(ctx))
    eligibility(ctx)
    gate(ctx, "H3", lambda: h3(ctx))
    gate(ctx, "H4", lambda: h4(ctx))
    gate(ctx, "N0", lambda: n0(ctx))
    gate(ctx, "H5", lambda: h5(ctx))
    for split in ("cal", "val"):
        r = ctx.data[f"oracle_{split}"]
        sr.save_npz(ctx.out / f"ORACLE_{split}.npz", G=r["G"], d=r["d"], lam=r["lam"],
                    lp=r["lp"], lm=r["lm"], elig=r["elig"], seq=r["seq"],
                    **{f"{k}_{f}": r["o"][k][f] for k in ("H", "Hp", "Hm")
                       for f in ("b32", "q", "s")})
    sr.write_new(ctx.out / "ORACLE_FROZEN.json", {"s_max": ctx.data["s_max"],
                                                  "kappa_nu": ctx.data["kappa"]})
    sr.complete(ctx.out, "oracle", ["ORACLE_cal.npz", "ORACLE_val.npz", "ORACLE_FROZEN.json",
                                    "CERT_val.npz", "CERT_val.json"])


def main() -> int:
    stage, release_path = sys.argv[1], sys.argv[2]
    ctx = make_context(release_path)
    try:
        if stage == "oracle":
            run_oracle_stage(ctx)
        else:
            import c1_driver_late

            c1_driver_late.run(ctx, stage)
    except C1Stop as stop:
        print(json.dumps({"stopped_at": stop.gate, "status": stop.status, "reason": stop.reason}))
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
