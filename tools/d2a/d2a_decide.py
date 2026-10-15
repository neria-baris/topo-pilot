"""D-2a flags, ordered decision rules and the stage-1 / stage-3 drivers; the bootstrap primitives
live in d2a_world and are re-exported (D2A-FROZEN-v1 §6, §10; tools/d2a/API.md §2.5, §4, §5)."""

from __future__ import annotations

import os
import sys

if __name__ == "__main__":  # analysis threads (≤ 6) before numpy/torch load; parent of nothing
    os.environ.update({v: "6" for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS",
                                        "OPENBLAS_NUM_THREADS")})

import re  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d2a_train as TR  # noqa: E402  (standard library only)
import d2a_world as W  # noqa: E402
from d2a_world import boot_counts, interval, quantiles, r2_from_sums  # noqa: E402, F401  (API §2.5)

SEEDS, BOOT = (1, 2, 3, 4), ("test", "B2000")


def licences(protocol=W.PROTOCOL) -> dict:
    """§1.4 quoted licensed sentences, verbatim from the hash-bound frozen protocol (gate 1)."""
    rows = re.findall(r'^\| \w+ \| ([A-Z_]+) \| "([^"]+)"', protocol.read_text("utf-8"), re.M)
    return {**dict(rows), "INCONCLUSIVE": "Descriptive reporting only."}


def _ok(v) -> bool:
    return v is not None and bool(np.isfinite(v))


def _n(xs) -> int:
    return sum(bool(x) for x in xs)


def learned(beta1, beta1_lo, kappa1, diff_lo, *, model_status="PRESENT") -> str:
    """MISSING/INVALID model → FAIL; a present model with any undefined value → UNRESOLVED (Q6)."""
    if model_status in ("MISSING", "INVALID"):
        return "FAIL"
    if model_status != "PRESENT":
        raise ValueError(f"model_status {model_status!r}")
    if not all(map(_ok, (beta1, beta1_lo, kappa1, diff_lo))):
        return "UNRESOLVED"
    ok = beta1 >= 0.30 and beta1_lo >= 0.15 and kappa1 >= 0.20 and diff_lo > 0
    return "PASS" if ok else "FAIL"


def stage1_decision(v1, v2) -> str:
    vs = ["FAIL" if v is None else v for v in (v1, v2)]  # missing/INVALID: defined FAIL (S5)
    if "PASS" in vs:
        return "GO"
    return "NOT_LEARNED" if vs == ["FAIL", "FAIL"] else "LEARNING_UNRESOLVED"


def arm_value(values) -> str:
    vs = ["FAIL" if v is None else v for v in values]
    passes, unres = vs.count("PASS"), vs.count("UNRESOLVED")
    return "TRUE" if passes >= 3 else "FALSE" if passes + unres < 3 else "UNRESOLVED"


def carries(d, d_lo) -> bool:
    return _ok(d) and _ok(d_lo) and d >= 0.15 and d_lo > 0.05


def low_increment(d) -> bool:
    return _ok(d) and d < 0.05


def beta2_pass(b, lo) -> bool:
    return _ok(b) and _ok(lo) and b >= 0.30 and lo >= 0.15


def precision_ok(hw_r_pi_16, hw_r_pi_28, hw_c8_16, hw_c8_28) -> bool:
    hw = (hw_r_pi_16, hw_r_pi_28, hw_c8_16, hw_c8_28)
    return all(map(_ok, hw)) and max(hw[:2]) <= 0.03 and max(hw[2:]) <= 0.05


def _seeds_ok(per_seed) -> bool:
    return per_seed is not None and len(per_seed) == 4 and all(map(_ok, per_seed))


def c_hor(mean, p2_5, per_seed) -> str:
    if not (_ok(mean) and _ok(p2_5) and _seeds_ok(per_seed)):
        return "UNRESOLVED"
    ok = mean >= 0.10 and p2_5 > 0 and _n(v > 0 for v in per_seed) >= 3
    return "SUPPORTED" if ok else "NOT_SUPPORTED"


def c_len(mean, p1_25, p98_75, per_seed, precision_all) -> str:
    if not (precision_all and all(map(_ok, (mean, p1_25, p98_75))) and _seeds_ok(per_seed)):
        return "LENGTH_UNRESOLVED"
    if mean >= 0.10 and p1_25 > 0 and _n(v > 0 for v in per_seed) >= 3:
        return "LENGTH_GAIN"
    if mean <= -0.10 and p98_75 < 0 and _n(v < 0 for v in per_seed) >= 3:
        return "LENGTH_LOSS"
    return "LENGTH_NOT_DETECTED"


def pipeline_null_ok(upper: dict) -> bool:
    return len(upper) == 4 and all(_ok(v) and v <= 0.02 for v in upper.values())


def decide(flags: dict) -> dict:
    """§10.5 ordered rules (first match) and the outcome-4–10 qualifiers."""
    prec, low, car = flags.get("precision_ok"), flags.get("low_inc"), flags.get("carries")

    def out(outcome, rule, quals=True):
        q = []
        if quals:
            q.append(flags["c_len"])
            arms = ("H2",) if rule == 8 else ("H1", "H2")  # models entering the rule (6a)
            if not all(bool(x) for arm in arms for x in prec[arm]):
                q.append("PRECISION_LIMITED")
            if _ok(flags.get("world_ceiling_28")) and flags["world_ceiling_28"] >= 0.30:
                q.append("WORLD_CONDITIONAL_CEILING")
            if _n(low["H1"]) >= 3 and _n(flags["beta2_ar_H1"]) >= 3:
                q.append("CAVEAT_REREAD")
            q += [f"BEHAVIOUR({H},{t})" for H, cells in sorted(flags["behaviour"].items())
                  for t, v in sorted(cells.items()) if v]
        return {"outcome": outcome, "rule": rule, "qualifiers": q}

    s = flags.get("s_fail")
    if s in ("S0", "S1", "S2", "S3"):
        return out({"S2": "CONSTRUCTION_FAIL", "S3": "FEASIBILITY_NO_GO"}.get(s, "INVALID"), 1,
                   False)
    if flags["stage1"] != "GO":
        return out(flags["stage1"], 2, False)
    if not flags["validity_ok"]:
        return out("PIPELINE_INVALID", 3, False)
    L1, L2 = (arm_value(flags["learned"][a]) for a in ("H1", "H2"))
    if L1 == "FALSE" and L2 == "TRUE":
        return out("MULTISTEP_ENABLES_LEARNING", 4)
    if L1 != "TRUE":
        return out("LEARNING_UNRESOLVED", 4)
    ch, dh = flags["c_hor"], flags["delta_h"]
    if ch == "SUPPORTED" and _n(_ok(dh[i]) and dh[i] > 0 and car["H2"][i] and low["H1"][i]
                                for i in range(4)) >= 3:
        return out("HORIZON_DEPENDENT", 5)
    if ch == "SUPPORTED" and _n(car["H2"]) >= 3:
        return out("HORIZON_ENHANCED", 6)
    if ch == "NOT_SUPPORTED" and _n(car["H1"]) >= 3 and _n(car["H2"]) >= 3:
        return out("CARRIED_WITHOUT_HORIZON_EFFECT", 7)
    if _n(low["H2"]) >= 3 and _n(flags["beta2_direct_H2"]) >= 3:
        return out("PREDICTIVE_WITHOUT_LINEAR_POSTERIOR", 8)
    if _n(low["H1"]) >= 3 and _n(low["H2"]) >= 3 and all(map(bool, prec["H1"] + prec["H2"])) \
            and flags["controls_valid"]:
        return out("NOT_RECOVERED_WITH_REGISTERED_PROBES", 9)
    return out("INCONCLUSIVE", 10)


def _lo(ci):
    return None if ci is None else ci[0]


def learned_stats(be: dict, n: int, B: int, scope) -> dict:
    """β₁, its interval, β₁⁽⁸⁾, κ₁ and the paired lower bound of β₁ − β₁⁽⁸⁾ (§6)."""
    st = W.beta_draws(be["ep"], be["rm"], be["d"], n, B, scope, extra=be["r8"])
    b1, b8 = (v if _ok(v) else None for v in (st["point"], st["point8"]))
    ci, diff = interval(st["draws"]), interval(st["draws"] - st["draws8"])
    kappa = (b1 - b8) / (1 - b8) if b1 is not None and b8 is not None and b8 < 1 else None
    return {"beta1": b1, "beta1_ci": ci, "beta1_w8": b8, "kappa1": kappa, "diff_ci": diff,
            "diff_lo": _lo(diff), "learned": learned(b1, _lo(ci), kappa, _lo(diff))}


def stage1_main(store_root=W.STORE) -> str:
    """CLI ``stage1``: learnability gate on val for H3-s1, H3-s2 (§6) plus descriptive R_π."""
    import d2a_eval as EV
    import d2a_targets as TG
    import torch

    torch.set_num_threads(6)
    root = Path(store_root)
    rec = {"S0": W.s0_bindings(TR.JOB_ID, TR.TASK_SHA256, TR.SESSION, root), "models": {}}
    if rec["S0"]["status"] != "PASS":
        rec["decision"] = "INVALID"
    else:
        val, cal = W.load_tokens("val", root), W.load_tokens("cal", root)
        runs = {r: TR._read(root / "runs" / f"{r}.json") for r in TR.WAVES["W1"]}
        if any(v["status"].startswith("INCOMPLETE") for v in runs.values()):
            rec["decision"] = "INCOMPLETE"
        vals = []
        for run, info in runs.items():
            if info["status"] != "COMPLETE":
                rec["models"][run] = {"status": info["status"], "learned": "FAIL"}
                vals.append(None)
                continue
            model, cid = EV.load_run(run, 10000, root)
            be = TG.band_edge_table(val, EV.next_symbol_probs(model, val))
            st = learned_stats(be, val.shape[0], 2000, ("val", "B2000", run))
            m = {"status": info["status"], "checkpoint_id": cid, **st, "R_pi": {},
                 "beta2_direct": {}, "dev_ce": info.get("checkpoints", [])}
            for t in W.POSITIONS:
                rc, rv = W.decision_rows(cal, t), W.decision_rows(val, t)
                pos_c, pos_v = np.full(rc.size, t), np.full(rv.size, t)
                yc, yv = EV.targets_for(cal, rc, pos_c), EV.targets_for(val, rv, pos_v)
                Xc, Xv = (EV.position_activations(model, tk, r_, p_, (EV.PRIMARY_HOOK,))
                          [EV.PRIMARY_HOOK] for tk, r_, p_ in ((cal, rc, pos_c), (val, rv, pos_v)))
                m["R_pi"][t] = EV.fit(Xc, yc["pi"], 1 + rc % 6, Xv, yv["pi"], "linear")["r2"]
                r, d = EV.contrasts(EV.direct_two_step(model, val, rv, pos_v), yv["J2_half"],
                                    yv["T2_full"])
                m["beta2_direct"][t] = TG.beta(r, d)[0]
            rec["models"][run] = m
            vals.append(st["learned"])
        rec.setdefault("decision", stage1_decision(*vals))
    (root / "stage1").mkdir(exist_ok=True)
    TR.write_json(root / "stage1" / "STAGE1.json", rec)
    return rec["decision"]


def model_flags(mid, P, data, B=2000) -> dict:
    """Primary per-model statistics with paired draws: R_X, ctrl_X, R_X − ctrl_X (§10.1-10.3)."""
    s, n = int(mid.split("-s")[1][0]), data["tok_test"].shape[0]
    out, cols, idx = {}, [], {}
    for t in W.POSITIONS:
        for X in ("pi", "r8"):
            key = f"t{t}|{X}|resid_post_3|linear"
            terms = {"model": P[mid].get("model|" + key), "shuffle": P[mid].get("shuffle|" + key),
                     "init": P.get(f"init-s{s}", {}).get("model|" + key),
                     "window8": P.get("window8", {}).get(f"window8|t{t}|{X}"),
                     "N1": P.get("d2a-s1-N", {}).get("model|" + key),
                     "N2": P.get("d2a-s2-N", {}).get("model|" + key)}
            dt, mean = data["test"][f"t{t}"], data["cal"][f"t{t}"]["y"][X].mean(0)
            for name, pred in terms.items():
                if pred is not None:
                    idx[(t, X, name)] = len(cols)
                    cols.append(W.r2_columns(n, dt["rows"], dt["y"][X], pred, mean))
    pt, bt = W.pooled_r2(cols, B, BOOT)
    for t in W.POSITIONS:
        for X in ("pi", "r8"):
            have = {k[2]: v for k, v in idx.items() if k[:2] == (t, X)}
            R, Rb = (pt(have["model"]), bt(have["model"])) if "model" in have else (None, None)
            terms = [have.get(k) for k in ("init", "shuffle", "window8")]
            ctrl = ctrl_b = None
            if R is not None and None not in terms and {"N1", "N2"} <= set(have):
                ctrl = max([pt(i) for i in terms] + [0.5 * (pt(have["N1"]) + pt(have["N2"]))])
                ctrl_b = np.max(np.stack([bt(i) for i in terms]
                                         + [0.5 * (bt(have["N1"]) + bt(have["N2"]))]), axis=0)
            ci = None if Rb is None else interval(Rb)
            out[(t, X)] = {"R": R, "R_ci": ci, "hw": None if ci is None else (ci[1] - ci[0]) / 2,
                           "ctrl": ctrl, "d": R - ctrl if _ok(R) and _ok(ctrl) else None,
                           "d_ci": None if ctrl_b is None else interval(Rb - ctrl_b),
                           "shuffle": pt(have["shuffle"]) if "shuffle" in have else None}
    be = {k[3:]: v for k, v in P[mid].items() if k.startswith("be|")}
    out["learned"] = learned_stats(be, n, B, BOOT)
    for t in W.POSITIONS:
        for route in ("direct", "ar"):
            r = P[mid].get(f"b2|{route}|t{t}|r")
            if r is not None:
                st = W.beta_draws(data["test"][f"t{t}"]["rows"], r, P[mid][f"b2|{route}|t{t}|d"],
                                  n, B, BOOT)
                ci = interval(st["draws"])
                out[(t, "beta2", route)] = {"beta2": st["point"], "ci": ci,
                                            "pass": beta2_pass(st["point"], _lo(ci))}
    return out


def confirmatory(P, data, B=20000) -> dict:
    """C-HOR and C-LEN: the four seed pairs averaged per draw, episode-cluster (§10.3-10.4)."""
    n, cols, idx = data["tok_test"].shape[0], [], {}
    for H, t, X in (("H1", 28, "pi"), ("H2", 28, "pi"), ("H2", 16, "r8"), ("H2", 28, "r8")):
        for s in SEEDS:
            pred = P.get(f"d2a-s{s}-{H}", {}).get(f"model|t{t}|{X}|resid_post_3|linear")
            if pred is None:
                return {"c_hor": {"status": "UNRESOLVED"}, "c_len": {"status": "MISSING"}}
            dt, mean = data["test"][f"t{t}"], data["cal"][f"t{t}"]["y"][X].mean(0)
            idx[(H, t, X, s)] = len(cols)
            cols.append(W.r2_columns(n, dt["rows"], dt["y"][X], pred, mean))
    pt, bt = W.pooled_r2(cols, B, ("confirmatory", "B20000"))

    def paired(a, b):  # per-seed point differences and the per-draw seed mean
        return ([pt(idx[(*a, s)]) - pt(idx[(*b, s)]) for s in SEEDS],
                np.mean([bt(idx[(*a, s)]) - bt(idx[(*b, s)]) for s in SEEDS], axis=0))

    (h_pt, h_b), (l_pt, l_b) = paired(("H2", 28, "pi"), ("H1", 28, "pi")), \
        paired(("H2", 28, "r8"), ("H2", 16, "r8"))
    hq, lq = quantiles(h_b, [0.025]) or [None], quantiles(l_b, [0.0125, 0.9875]) or [None, None]
    return {"c_hor": {"mean": float(np.mean(h_pt)) if all(map(_ok, h_pt)) else None,
                      "p2_5": hq[0], "per_seed": h_pt},
            "c_len": {"mean": float(np.mean(l_pt)) if all(map(_ok, l_pt)) else None,
                      "p1_25": lq[0], "p98_75": lq[1], "per_seed": l_pt}}


def assemble(F, oracle, R, stage1, conf) -> dict:
    """The decide() flag table from per-model statistics and validity records (API §2.5)."""
    ks = ((16, "pi"), (28, "pi"), (16, "r8"), (28, "r8"))

    def per(H, fn):
        return [F.get(f"d2a-s{s}-{H}") is not None and bool(fn(F[f"d2a-s{s}-{H}"]))
                for s in SEEDS]

    fits, key = oracle["fits"], "shuffle|t{}|pi|resid_post_3|linear"
    shuffle_r2 = [R.get(m, {}).get("fits", {}).get(key.format(t), {}).get("r2")
                  for m in R if m.startswith("d2a-") for t in W.POSITIONS]
    shuffle_ok = len(shuffle_r2) == 28 and all(_ok(v) and v <= 0.05 for v in shuffle_r2)
    upper = {(m, t): R.get(m, {}).get("pipeline_null", {}).get(t, {}).get("upper")
             for m in ("d2a-s1-N", "d2a-s2-N") for t in W.POSITIONS}
    pos_ok = all(_ok(fits.get(k, {}).get("r2")) and fits[k]["r2"] >= 0.99 for t in W.POSITIONS
                 for k in (f"positive_control_val|t{t}", f"ceiling|t{t}|full_belief"))
    valid = shuffle_ok and pipeline_null_ok(upper) and pos_ok
    c8_prec = all(per("H2", lambda m: all(_ok(m[k]["hw"]) and m[k]["hw"] <= 0.05
                                          for k in ks[2:])))
    ch, cl, beh = conf["c_hor"], conf["c_len"], {}
    for H in ("H1", "H2", "H3"):
        cells = [R.get(f"d2a-s{s}-{H}", {}).get("behaviour") for s in SEEDS]
        beh[H] = {t: _n(c and c["routes"][c["native"]]["BEHAVIOUR"][t] for c in cells) >= 3
                  for t in (11, 16, 28)}
    return {"s_fail": None, "stage1": stage1, "validity_ok": valid, "controls_valid": valid,
            "validity": {"shuffle_ok": shuffle_ok, "positive_control_ok": pos_ok,
                         "pipeline_null_upper": {f"{m}|{t}": v for (m, t), v in upper.items()}},
            "learned": {H: [F[f"d2a-s{s}-{H}"]["learned"]["learned"]
                            if f"d2a-s{s}-{H}" in F else None for s in SEEDS]
                        for H in ("H1", "H2", "H3")},
            "c_hor": c_hor(ch.get("mean"), ch.get("p2_5"), ch.get("per_seed")),
            "delta_h": ch.get("per_seed", [None] * 4),
            "carries": {H: per(H, lambda m: carries(m[(28, "pi")]["d"], _lo(m[(28, "pi")]["d_ci"])))
                        for H in ("H1", "H2")},
            "low_inc": {H: per(H, lambda m: low_increment(m[(28, "pi")]["d"]))
                        for H in ("H1", "H2")},
            "beta2_direct_H2": per("H2", lambda m: m.get((28, "beta2", "direct"), {}).get("pass")),
            "beta2_ar_H1": per("H1", lambda m: m.get((28, "beta2", "ar"), {}).get("pass")),
            "precision_ok": {H: per(H, lambda m: precision_ok(*(m[k]["hw"] for k in ks)))
                             for H in ("H1", "H2")},
            "c_len": c_len(cl.get("mean"), cl.get("p1_25"), cl.get("p98_75"),
                           cl.get("per_seed"), c8_prec),
            "world_ceiling_28": fits.get("ceiling|t28|world_conditional", {}).get("r2"),
            "behaviour": beh}


def _save(out: Path, name: str, rec, preds=None) -> None:
    TR.write_json(out / "fits" / f"{name}.json", rec)
    if preds:
        with (out / "pred" / f"{name}.npz").open("xb") as fh:
            np.savez(fh, **{k.replace("|", "__"): np.asarray(v) for k, v in preds.items()})


def stage3_main(store_root=W.STORE) -> str:
    """CLI ``stage3`` (API §4): primary passes, decision, then budgeted secondary work."""
    import d2a_eval as EV
    import torch
    import winjob

    os.environ["D2A_STAGE"] = "3"
    torch.set_num_threads(6)
    root = Path(store_root)
    out = root / "stage3"
    for sub in ("fits", "pred"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    led = TR._read(root / "cpu_ledger.json")
    base, tot0 = TR.stage_spent(led, "stage3"), TR.total_spent(led)

    def can(need):
        own = winjob.own_cpu_s()
        return TR.admit("stage3", base + own, tot0 + own, TR.Limits(), need)

    rec = {"S0": W.s0_bindings(TR.JOB_ID, TR.TASK_SHA256, TR.SESSION, root), "not_run": [],
           "status": "COMPLETE"}
    if rec["S0"]["status"] != "PASS":
        rec["outcome"] = "INVALID"
    else:
        st1 = TR._read(root / "stage1" / "STAGE1.json")["decision"]
        runs = {r: TR._read(root / "runs" / f"{r}.json")["status"]
                for r in TR.RUNS if (root / "runs" / f"{r}.json").exists()}
        data, P, R = EV.stage3_data(root), {}, {}
        for mid, run, step, H in EV.model_list():
            if runs.get(run) != "COMPLETE":
                R[mid] = {"status": runs.get(run, "MISSING")}
            elif not can(1200):
                rec["not_run"].append(mid)
                rec["status"] = "INCOMPLETE:STAGE_CPU"
            else:
                res = EV.collect_model(mid, run, step, H, data, root)
                P[mid], R[mid] = res["preds"], res["record"]
                _save(out, mid, R[mid], P[mid])
        of = EV.oracle_fits(data, root)
        P["window8"] = of["preds"]
        _save(out, "oracle", of["fits"], of["preds"])
        F = {m: model_flags(m, P, data) for m in P if m.startswith("d2a-") and "-N" not in m}
        conf = confirmatory(P, data)
        flags = assemble(F, of, R, st1, conf)
        dec = decide(flags)
        dec["licensed_sentence"] = licences().get(dec["outcome"])
        rec["decision"] = dec
        TR.write_json(out / "DECISION.json", {"flags": flags, **dec, "confirmatory": conf,
                                       "model_stats": F, "runs": runs})
        rec["secondary"] = EV.secondary(data, P, R, can, root)
        rec["not_run"] += rec["secondary"].pop("not_run")
    TR.write_json(out / "STAGE3.json", rec)
    return rec.get("decision", {}).get("outcome", rec.get("outcome"))


if __name__ == "__main__":
    print({"stage1": stage1_main, "stage3": stage3_main}[sys.argv[1]]())
