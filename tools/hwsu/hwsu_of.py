"""HWSU stage OF gates OF-P .. OF-5, outcome and report (API.md §4; protocol §4.2).

Optional ctx keys for the dry run and tests: "draws" (default 5000; the rank assertions apply
only at 5000), "block_n" (rows per block, default 4096), "decimal_rows" (default 4),
"handoff_path", "handoff_sha256".
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_oracle as uo
import hwsu_pairs as up
import hwsu_records as ur
import json
from fractions import Fraction
from pathlib import Path

import c1_means
import c2_attrib
import c2_decide
import hwsb_data
import hwsc_data
import k4b_data
import k4b_release
import numpy as np
import oracle_profile
import precision
import stage_records
from c1_records import C1GateFailure
from topo_pilot.contracts import ArtifactStore, MemoryBackend

IDENT, SAMPLER = "FAIL_TECHNICAL/IDENTITY", "FAIL_TECHNICAL/SAMPLER"
ORACLE = "FAIL_TECHNICAL/ORACLE"
FEAS = "INCONCLUSIVE/ORACLE_FEASIBILITY"


def _draws(ctx) -> int:
    return int(ctx.get("draws", uc.DRAWS))


def _bounds(arrays, seed, alpha, draws) -> tuple:
    """Gate bounds from c2_decide.stream_bounds (through its module at call time) and, from a
    second deterministic call (same seed and index rule), the draws stored in BOOT_OF.npz. The
    bounds recomputed from the stored draws must equal stream_bounds' exactly (E-4)."""
    b = c2_decide.stream_bounds(arrays, seed, alpha, draws)
    means = c1_means.bootstrap_means(arrays, seed, draws)
    for k in arrays:
        lo = c1_means.quantile_with_rank(means[k], alpha)[0]
        hi = c1_means.quantile_with_rank(means[k], 1 - alpha)[0]
        if lo != b[k]["L"] or hi != b[k]["U"]:
            raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", f"stored draws differ for {k}")
    return b, means


def _tm(x) -> float:
    return float(c1_means.tree_mean(x))


# ------------------------------------------------------------------------------- OF-P, RESERVATION
def of_p(ctx) -> dict:
    if ctx.get("dry") and not uc.dry_store_ok(ctx.get("out", "")):
        raise C1GateFailure("FAIL_TECHNICAL/BINDING", "dry context outside the dry/test scratch")
    if ctx.get("dry") and ctx.get("proc") is not None:  # DRO fixture world: no real identity
        p = ctx["proc"]
        up.check_process(p["T"], p["E_canon_shared"], p["pi"])
        return {"fixture": True, "stationarity_error": up.stationarity_error(p["T"], p["pi"])}
    W, root = uc.CONTRACT["world"], ctx["root"]
    store = ArtifactStore(MemoryBackend())
    proc = hwsb_data.build_process(store, masters=uc.MASTERS)
    r = hwsc_data.process_identity(store, proc)
    if not r["ok"]:
        raise C1GateFailure(IDENT, f"process identity: {r['checks']}")
    arts = Path(ctx["hwsc_store"]) / "artifacts"
    want = [("EmissionSpec", proc["ids"]["emission"][m], m) for m in uc.MASTERS]
    want += [("WorldSpec", proc["ids"]["world"], None), ("TransitionSpec",
                                                         proc["ids"]["transition"], None)]
    for typ, aid, master in want:
        try:
            meta = uc.read_json(arts / typ / str(aid) / "meta.json", root)
        except (OSError, ValueError) as exc:
            raise C1GateFailure(IDENT, f"{typ} {aid} meta.json: {exc!r}") from exc
        if meta.get("artifact_type") != typ or (
                master is not None and meta.get("config", {}).get("replicate") != master):
            raise C1GateFailure(IDENT, f"{typ} {aid} meta.json differs")
    T, E, pi = proc["T"], proc["E_canon_shared"], proc["pi"]
    found = oracle_profile.validate_process(T, E, pi, W["validate_tol"])
    up.check_process(T, E, pi)
    ctx["proc"] = proc
    return {"identity": r["checks"], "ids": proc["ids"],
            "stationarity_error": up.stationarity_error(T, pi), "validate": found}


def reservation_check(ctx) -> dict:
    path = Path(ctx["reservation_path"])
    if path.name != ur.reservation_file(ctx["reservation_id"]):
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", "reservation file name differs")
    v = k4b_release.verify_reservation(path, {"reservation": ctx["reservation_id"]})
    if v["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", str(v.get("reason", v["status"])))
    return {"reservation": ctx["reservation_id"]}


# --------------------------------------------------------------------------------------- OF-S
def of_s(out, ctx) -> dict:
    p, scope, dry = ctx["proc"], ctx.get("scope", uc.SCOPE_OF), bool(ctx.get("dry"))
    T, E, pi = p["T"], p["E_canon_shared"], p["pi"]
    n = int(ctx.get("block_n", uc.BLOCK_OF))
    ur.begin_stage(out, "OF_S")
    ctx["rows_drawn"] = True
    try:
        fit = {b: up.sample_singles(T, E, pi, scope, "of-fit", b, n) for b in uc.BLOCKS_OF}
        ev = {b: up.sample_pairs(T, E, pi, scope, "of-eval", b, n) for b in uc.BLOCKS_OF}
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise C1GateFailure(SAMPLER, f"sampling: {exc!r}") from exc
    order = [("fit", 0, "of-fit", fit[0]["canon32"], fit[0]["ids"]),
             ("fit", 1, "of-fit", fit[1]["canon32"], fit[1]["ids"])]
    for b in uc.BLOCKS_OF:
        order += [("eval_a1", b, "of-eval-a1", ev[b]["a1"], ev[b]["ids_a1"]),
                  ("eval_a2", b, "of-eval-a2", ev[b]["a2"], ev[b]["ids_a2"])]
    files = []
    for kind, b, label, canon, ids in order:
        t = up.history_table(canon, ids, label, b)
        rel = f"stages/OF/{up.hist_name(kind, b, dry)}"
        ur.save_array(out, rel, dry=dry, **up.table_arrays(t))
        files.append(rel)
    ur.complete_stage(out, "OF_S", files)
    cat = lambda blocks, key: np.concatenate([blocks[b][key] for b in uc.BLOCKS_OF])  # noqa: E731
    ctx["fit"] = {"canon32": cat(fit, "canon32"), "ids": cat(fit, "ids")}
    ctx["eval"] = {k: cat(ev, k) for k in ("a1", "a2", "ids_a1", "ids_a2")}
    ctx["files"] = files
    return {"files": files, "n_fit": len(ctx["fit"]["ids"]), "n_pairs": len(ctx["eval"]["a1"])}


# --------------------------------------------------------------------------------------- OF-H
def of_h(ctx) -> dict:
    fit, ev = ctx["fit"]["canon32"], ctx["eval"]
    stack = np.vstack((fit, ev["a1"], ev["a2"]))
    pc = k4b_data.predicate_check(stack, ("sealed_d2a",))
    if pc["status"] != "PASS":
        return {"status": "INCONCLUSIVE/REGISTRY_INCOMPLETE", "predicate": pc}
    ho = uc.load_handoff_u(ctx.get("handoff_path", uc.HANDOFF_PATH), ctx.get("handoff_sha256"))
    h = hwsc_data.p_d2a_check(ctx["proc"], ho["p_D2a"])
    risk = ur.registry_risk_u(h["p_D2a"], 24576)
    out = {"predicate": pc, "p_d2a": h, "registry_risk": risk,
           "duplicates": k4b_data.duplicates(stack)}
    if not (h["ok"] and risk["ok"]):
        out["status"] = SAMPLER
    return out


# --------------------------------------------------------------------------------------- OF-1
def of_1(ctx) -> dict:
    p, fit, ev = ctx["proc"], ctx["fit"]["canon32"], ctx["eval"]
    T, E, pi, co = p["T"], p["E_canon_shared"], p["pi"], p["coords"]
    a1, a2 = ev["a1"], ev["a2"]
    ctx["of"], ctx["o1"], ctx["o2"] = (uo.arm_oracle(T, E, pi, x, co) for x in (fit, a1, a2))
    s1, s2 = uo.suffix_oracle(T, E, pi, [a1, a2], co)
    ctx["s1"], ctx["s2"] = s1, s2
    ctx["sf"] = uo.suffix_oracle(T, E, pi, [fit], co)[0]
    o1, o2 = ctx["o1"], ctx["o2"]
    pc = ctx["pc"] = uo.pair_core(o1, o2)
    if not up.suffix_equal(a1, a2).all():
        raise C1GateFailure(SAMPLER, "OF-1 (i): arm suffixes differ")
    m4c = uo.m4_check(T, E, pi, a1, co, s1["m4"])
    if not (np.array_equal(s1["q4bar"], s2["q4bar"]) and np.array_equal(s1["m4"], s2["m4"])
            and m4c["ok"]):
        raise C1GateFailure(SAMPLER, f"OF-1 (ii): q4/m4 differ across arms or m4 check {m4c}")
    if not all(np.all(np.isfinite(o["le"])) for o in (ctx["of"], o1, o2)):
        raise C1GateFailure(SAMPLER, "OF-1 (iii): non-finite log evidence")
    N = uo.helmert(36)
    ctx["A_KO"] = {k: uo.readout_A(pc["d"], uo.ko_logits(o1, s1, k), uo.ko_logits(o2, s2, k), N)
                   for k in uo.CASES}
    ids = uo.ko_identities(pc["G"], ctx["A_KO"])
    cats = uo.ko_categories(pc["G"], ctx["A_KO"], ctx["seeds"]["share"], draws=_draws(ctx))
    ctx["ko"] = {"identities": ids, "categories": cats}
    if not (all(v["ok"] for v in ids.values()) and cats["ok"]):
        raise C1GateFailure(ORACLE, f"OF-1 (iv): KO identities/categories {ids} {cats}")
    dec = ctx["decimal"] = uo.decimal_rows(T, E, pi, a1, a2, o1, o2, s1, pc,
                                           k=ctx.get("decimal_rows", uc.DECIMAL_ROWS))
    if not dec["ok"]:
        raise C1GateFailure(ORACLE, "OF-1 (v): Decimal rows differ")
    return {"suffix_equal": True, "m4_check": m4c, "ko": ctx["ko"], "decimal": dec}


# ------------------------------------------------------------------------------ OF-2, OF-3
def of_2(ctx) -> dict:
    G, draws = ctx["pc"]["G"], _draws(ctx)
    b, means = _bounds({"G": G}, ctx["seeds"]["headroom"], uc.ALPHA_HEADROOM, draws)
    ctx.setdefault("boot", {})["headroom_G"] = means["G"]
    ctx["EG"] = {"point": b["G"]["mean"], "L": b["G"]["L"], "rank_L": b["G"]["rank_L"]}
    if draws == uc.DRAWS and b["G"]["rank_L"] != 250:
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "OF-2 rank_L != 250")
    out = {"EG": ctx["EG"], "U": b["G"]["U"]}
    if not Fraction(float(b["G"]["L"])) > uc.HEADROOM:
        out["status"] = FEAS
    return out


def _psi(ctx, K=None, euclidean=False):
    o1, o2, pc = ctx["o1"], ctx["o2"], ctx["pc"]
    pr = uo.problem_o(ctx["of"], ctx["fit"]["canon32"][:, 31], K=K, euclidean=euclidean)
    if pr["status"] != "PASS":
        return pr, None, "NOT_COMPUTED"
    sa = uo.share_arrays(pr, pc, o1, o2)
    return pr, sa, _tm(sa["A_S"]) / _tm(pc["G"])


def of_3(ctx) -> dict:
    pc, seeds, draws = ctx["pc"], ctx["seeds"], _draws(ctx)
    G = pc["G"]
    pr, sa, psi = _psi(ctx)
    ctx["pr"], ctx["sa"], ctx["psi"] = pr, sa, psi
    if sa is None:
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", f"OF-3 primary fit {pr['status']}")
    A_S = sa["A_S"]
    arrays = {"Z020": A_S - 0.2 * G, "Z050": A_S - 0.5 * G, "AS": A_S, "G": G}
    b, means = _bounds(arrays, seeds["share"], uc.ALPHA_VAL, draws)
    ctx.setdefault("boot", {}).update({f"share_{k}": v for k, v in means.items()
                                       if k in ("Z020", "Z050", "AS", "G")})
    if draws == uc.DRAWS and b["Z020"]["rank_L"] != 84:
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "OF-3 rank_L != 84")
    g = c2_decide.guard(arrays["Z020"], uo.share_guard_beta(pr, pc, sa["dy"]))
    ci = c2_attrib.ratio_intervals({"AS": A_S}, {"G": G}, [("AS", "G")], seeds["share"], draws)
    var = {}
    for name, kw in (("K1", {"K": 1}), ("E", {"euclidean": True})):
        v = _psi(ctx, **kw)
        ctx[f"pr_{name}"], ctx[f"sa_{name}"] = v[0], v[1]
        var[name] = v[2]
    gc = uo.label_share(ctx["o1"]["qbar"], ctx["o2"]["qbar"])
    ctx["G_circ"] = gc
    ctx["share"] = {"psi_orc": psi, "interval95": ci["AS/G"],
                    "Z020": {"L": b["Z020"]["L"], "rank_L": b["Z020"]["rank_L"], "g": g},
                    "Z050": {"L": b["Z050"]["L"], "U": b["Z050"]["U"]}, "variants": var,
                    "circular_label_share": _tm(gc) / _tm(G)}
    out = dict(ctx["share"])
    if not c2_decide.sign(b["Z020"]["L"], g) == 1:
        out.update(status="SHARE_DROPPED", share_outcome=FEAS)
    return out


# --------------------------------------------------------------------------------------- OF-4
def of_4(ctx) -> dict:
    G, sa, seeds, draws = ctx["pc"]["G"], ctx["sa"], ctx["seeds"], _draws(ctx)
    eg = _tm(G)
    dropped = ctx.get("results", {}).get("OF-3") == "SHARE_DROPPED"
    arrs = [("ZR010", sa["A_full"] - 0.1 * G, "resp"), ("ZR030", sa["A_full"] - 0.3 * G, "resp")]
    if not dropped:
        arrs += [("Z010", sa["A_S"] - 0.1 * G, "share"), ("Z050", sa["A_S"] - 0.5 * G, "share")]
    prec, proxy, passed = {}, {}, {}
    for name, X, fam in arrs:
        alt = float((uc.ALT_RESP if fam == "resp" else uc.ALT_SHARE) * Fraction(eg))
        sd = precision.sd_b4_draws(X={"oracle": X}, r4n={"oracle": G}, models=["oracle"],
                                   seed=seeds["p1_sd"], draws=draws, size=len(G))[0]
        prec[f"sd_{name}"] = sd
        proxy[name] = {}
        for N in uc.LADDER:
            e = precision.centered_draws(X={"oracle": X}, models=["oracle"],
                                         seed=seeds["p1_centred"], draws=draws, size=N)
            prec[f"e_{name}_{N}"] = e
            cfg = {"alpha": float(uc.ALPHA_FAMILY), "power": uc.POWER, "delta": 0.0,
                   "alternative": alt, "projected_N": N}
            s = precision.precision_summary(sd, e, ["oracle"], cfg)
            m = s["models"]["oracle"]
            proxy[name][N] = {"mde_upper": m["mde_upper"], "power": m["power"],
                              "criterion_met": s["criterion_met"]}
            passed[(name, N)] = s["criterion_met"]

    def first(names):
        return next((N for N in uc.LADDER if all(passed[(n, N)] for n in names)), None)

    ctx["prec"], ctx["proxy"] = prec, proxy
    ctx["N_resp"] = first(("ZR010", "ZR030"))
    ctx["N_share"] = None if dropped else first(("Z010", "Z050"))
    out = {"N_resp": ctx["N_resp"], "N_share": ctx["N_share"], "proxy": proxy}
    if dropped:
        out["share"] = "NOT_RUN/SHARE_DROPPED"
    if ctx["N_resp"] is None:
        out["status"] = FEAS
    elif dropped or ctx["N_share"] is None:
        out["status"] = "SHARE_DROPPED"
    return out


# --------------------------------------------------------------------------------------- OF-5
def of_5(ctx) -> dict:
    a = uo.lemma_p_arrays(ctx["o1"], ctx["o2"], ctx["s1"], ctx["pc"])
    m = c1_means.bootstrap_means({k: a[k] for k in ("pairU", "rowU", "pairG", "rowG")},
                                 ctx["seeds"]["lemma_p"], _draws(ctx))
    ctx["lemma"] = a
    ctx.setdefault("boot", {}).update({f"lemma_{k}": v for k, v in m.items()})
    out, ok = {}, True
    for Q in ("U", "G"):
        diff = _tm(a[f"pair{Q}"]) - _tm(a[f"row{Q}"])
        se = float(np.std(m[f"pair{Q}"] - m[f"row{Q}"], ddof=1))
        good = Fraction(abs(diff)) <= uc.LEMMA_P_SE * Fraction(se)
        out[Q] = {"pair": _tm(a[f"pair{Q}"]), "row": _tm(a[f"row{Q}"]), "diff": diff, "se": se,
                  "ok": good}
        ok = ok and good
    if not ok:
        out["status"] = SAMPLER
    return out


# ------------------------------------------------------------------------- outcome, report
def of_outcome(records) -> str:
    for r in records:
        if r["status"] not in ("PASS", "SHARE_DROPPED"):
            return r["status"]
    return "OF_PASS_RESPONSE_ONLY" if any(r["status"] == "SHARE_DROPPED" for r in records) \
        else "OF_PASS"


def tails(G) -> dict:
    G = np.sort(np.asarray(G, dtype=np.float64))[::-1]
    k = int(np.ceil(0.01 * len(G)))
    c = G - G.mean()
    return {"top1pct_share": float(G[:k].sum() / G.sum()),
            "kurtosis": float(np.mean(c**4) / np.mean(c**2) ** 2)}


def of_report(out, ctx, records) -> Path:
    dry, out = bool(ctx.get("dry")), Path(out)
    written = []

    def save(name, **arrs):
        written.append(f"stages/OF/{name}")
        ur.save_array(out, written[-1], dry=dry, **arrs)

    pc, sa, o1, o2 = ctx.get("pc"), ctx.get("sa"), ctx.get("o1"), ctx.get("o2")
    if pc is not None:
        ko = ctx.get("A_KO", {})
        ev = {"G": pc["G"], "le_a1": o1["le"], "le_a2": o2["le"]}
        if sa is not None:
            ev.update(A_full=sa["A_full"], A_S=sa["A_S"], A_G=sa["A_G"])
        ev.update({f"A_{k}": v for k, v in ko.items()})
        if "lemma" in ctx:
            ev.update(pairU=ctx["lemma"]["pairU"], rowU=ctx["lemma"]["rowU"],
                      rowG=ctx["lemma"]["rowG"])
        if "G_circ" in ctx:
            ev["G_circ"] = ctx["G_circ"]
        save("ORACLE_OF_eval.npz", **ev)
        save("ORACLE_OF_fit.npz", le=ctx["of"]["le"], s=ctx["of"]["s"])
    for key, name in (("pr", "FIT_OF_O.npz"), ("pr_K1", "FIT_OF_OK1.npz"),
                      ("pr_E", "FIT_OF_OE.npz")):
        pr = ctx.get(key)
        if pr is not None and pr.get("status") == "PASS":
            save(name, alpha=pr["fit"]["alpha"], Gamma=pr["fit"]["Gamma"], B=pr["fit"]["B"],
                 Sigma=pr["Sigma"], L=pr["g"]["L"], P_S=pr["g"]["P_S"], P_G=pr["g"]["P_G"],
                 mu=pr["mu"], sd=pr["sd"])
    if ctx.get("boot"):
        save("BOOT_OF.npz", **ctx["boot"])
    if ctx.get("prec"):
        save("PREC_OF.npz", **ctx["prec"])
    sh = ctx.get("share", {})
    report = {
        "schema": "hwsu-of-report-v1", "outcome": of_outcome(records),
        "gates": {r["gate"]: r["status"] for r in records}, "EG": ctx.get("EG"),
        "psi_orc": {"point": sh.get("psi_orc"), "interval95": sh.get("interval95"),
                    "Z020": sh.get("Z020"), "Z050": sh.get("Z050")},
        "psi_orc_variants": sh.get("variants"), "circular_label_share": sh.get(
            "circular_label_share"), "proxy": ctx.get("proxy"), "N_resp": ctx.get("N_resp"),
        "N_share": ctx.get("N_share"),
        "alternatives": {"response": str(uc.ALT_RESP), "share": str(uc.ALT_SHARE)},
        "tails": tails(pc["G"]) if pc is not None else None,
        "lemma_p": {r["gate"]: r for r in records}.get("OF-5"), "ko": ctx.get("ko"),
        "decimal": ctx.get("decimal"), "hygiene": {r["gate"]: r for r in records}.get("OF-H"),
        "n_rows": {"fit": len(ctx["fit"]["ids"]), "eval_pairs": len(ctx["eval"]["a1"])},
        "cpu_s": ctx.get("cpu_s"), "protocol_sha256": uc.CONTRACT["protocol_sha256"],
        "contract_of_sha256": uc.CONTRACT_SHA256["of"],
        "freeze_of_sha256": ctx.get("freeze_of_sha256"), "written_utc": ur.utc()}
    rp = out / "stages" / "OF" / "OF_REPORT.json"
    stage_records.write_new(rp, json.loads(json.dumps(report, default=str)))
    extra = ["stages/OF/G0_OF.json"] if (out / "stages" / "OF" / "G0_OF.json").is_file() else []
    ur.complete_stage(out, "OF", ["stages/OF/OF_REPORT.json", *extra, *written])
    return rp
