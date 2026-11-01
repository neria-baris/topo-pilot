"""HWSD SUMMARY: bootstraps, bounds, F, the 36-row table, outcome, report (API.md section 8).
Reused functions are called through their module attributes at call time."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import hashlib
from fractions import Fraction
from pathlib import Path

import c1_means
import hwsd_bind
import hwsd_readers
import hwsd_score
import hwsd_statements as dst
import k4b_cert
import k4b_config
import k4b_driver
import k4b_fresh
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure

NUMERICAL, LINEAGE = "FAIL_TECHNICAL/NUMERICAL", "FAIL_TECHNICAL/LINEAGE"
SHARED = ("m4_phase", "sha_suffix", "delta4_orc")


def _tm(x) -> float:
    return float(c1_means.tree_mean(np.asarray(x, dtype=np.float64)))


def _checked(out, rel, stage):
    f = Path(out) / rel
    want = hwsd_readers.stage_complete_sha(Path(out) / "STAGES.jsonl", rel, stage)
    if want is None or not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != want:
        raise C1GateFailure(LINEAGE, f"{rel} does not re-hash to its record")
    return f


def load_scores(out, masters=dc.MASTERS) -> dict:
    out, res = Path(out), {}
    for j in masters:
        for step in dc.STEPS:
            base = f"stages/SCORE/{j}/s{step}/"
            st = f"SCORE_{j}"
            rec = dc.read_json(_checked(out, base + "CHECKPOINT_RECORD.json", st))
            learn = dc.read_json(_checked(out, base + "LEARN.json", st))
            arrays = None
            if rec.get("arrays_sha256") is not None or (out / (base + "ARRAYS.npz")).exists():
                with np.load(_checked(out, base + "ARRAYS.npz", st), allow_pickle=False) as z:
                    arrays = {k: z[k] for k in z.files}
            res[(int(j), int(step))] = {"record": rec, "learn": learn, "arrays": arrays}
    return res


def _order(scores):
    return sorted(scores, key=lambda t: (dc.MASTERS.index(t[0]) if t[0] in dc.MASTERS else t[0],
                                         t[1]))


def bootstrap_inputs_d(scores, shared) -> dict:
    d = {}
    for j, s in _order(scores):
        a = scores[(j, s)]["arrays"]
        if a is None:
            continue
        d[f"X:{j}:{s}:-"], d[f"X:{j}:{s}:+"] = a["X_minus"], a["X_plus"]
        if "decoder_X" in a:
            d[f"decoder:{j}:{s}"] = a["decoder_X"]
        for n in ("delta1", "delta2"):
            d[f"{n}:{j}:{s}:-"], d[f"{n}:{j}:{s}:+"] = a[f"{n}_X_minus"], a[f"{n}_X_plus"]
        d[f"naive:{j}:{s}"] = a["naive_X"]
    for n in SHARED:
        d[f"{n}:all"] = shared[n]["all"]["X"]
    return {k: np.asarray(v, dtype=np.float64) for k, v in d.items()}


def main_bootstrap(inputs, seed=None) -> dict:
    return k4b_stats.joint_bootstrap(
        inputs, seed if seed is not None else k4b_config.SEEDS["endpoint"])


def strong_bootstrap(scores, seed=None) -> dict:
    keys = {}
    for j, s in _order(scores):
        a = scores[(j, s)]["arrays"]
        if a is not None:
            keys[f"X:{j}:{s}:-"], keys[f"X:{j}:{s}:+"] = a["X_minus"], a["X_plus"]
    return c1_means.bootstrap_means(
        keys, seed if seed is not None else hwsd_bind.strong_seed(), dc.STRONG_DRAWS)


def strong_bounds(draws_minus, draws_plus) -> dict:
    out = {}
    for tag, d, p, rank in (("L_S", draws_minus, dc.P_LO, dc.STRONG_RANKS["lo"]),
                            ("U_S", draws_plus, dc.P_HI, dc.STRONG_RANKS["hi"])):
        d = np.asarray(d, dtype=np.float64)
        if not np.all(np.isfinite(d)):
            raise C1GateFailure(NUMERICAL, "non-finite strong bootstrap draws")
        v, k = c1_means.quantile_with_rank(d, p)
        if k != rank or not c1_means.rank_check(d, v, k):
            raise C1GateFailure(NUMERICAL, f"strong rank check failed (rank {k}, expected {rank})")
        out[tag], out[tag + "_rank"] = v, rank
    return out


def f_sides(record, Z, n=dc.N) -> tuple:
    cert = record.get("certificate") or {}
    if record.get("planted") or cert.get("planted"):
        return dc.F_PLANTED, dc.F_PLANTED
    return tuple(k4b_cert.margin(k4b_cert.b_num(Fraction(cert["max_B"][s]), cert["max_abs"][s], n),
                                 Z) for s in ("X_minus", "X_plus"))


def control_summary_d(draws, controls, bounds) -> dict:
    return k4b_fresh.control_summary(draws, controls, bounds)


def checkpoint_row(j, step, item, draws, sdraws, Z, controls_summary) -> dict:
    rec, learn, a = item["record"], item["learn"], item["arrays"]
    row = {"status": rec["status"], "label": rec["label"], "valid": rec["valid"],
           "step": int(step), "k": dc.K_OF[int(step)], "master": int(j),
           "captured": learn["captured"], "regret": learn["regret"],
           "regret_se": learn["regret_se"], "learn_pass": bool(learn["learn_pass"]),
           "B2_z": learn["B2_z"], "B2_zS": learn["B2_zS"], "B2_L_zS": learn["B2_L_zS"],
           "chart": {"c0_cal": rec["c0_cal"], "c0_val": rec["c0_val"]},
           "L": None, "U": None, "L_S": None, "U_S": None, "F_minus": None, "F_plus": None}
    if a is None:
        return row
    km, kp = f"X:{j}:{step}:-", f"X:{j}:{step}:+"
    bd = k4b_stats.bounds(draws[km], draws[kp])
    sb = strong_bounds(sdraws[km], sdraws[kp])
    fm, fp = f_sides(rec, Z)
    pm, pp = _tm(a["X_minus"]), _tm(a["X_plus"])
    row.update(L=bd["L"][0], U=bd["U"][0], central95_minus=bd["central95_minus"],
               central95_plus=bd["central95_plus"], L_S=sb["L_S"], U_S=sb["U_S"],
               F_minus=fm, F_plus=fp, point_minus=pm, point_plus=pp)
    if rec["status"] == "SCORED":
        ms = k4b_stats.model_status(row["L"], row["U"], fm, fp)
        row.update(sigma=ms["status"], labels=ms["labels"],
                   status_without_F=ms["status_without_F"])
    sup = rec.get("support") or {}
    row["support"] = {k: sup.get(k) for k in ("fraction", "width", "missing_mass")}
    row["positive"] = bool(dst.est(row) and dst.fr(row["L"]) - fm > 0)
    b4 = (controls_summary.get("B4_TEST") or {}).get("point")
    d4 = ((controls_summary.get("delta4_orc") or {}).get("all") or {}).get("point")
    row["ratios"] = k4b_stats.ratios(pm, b4, d4)
    key = f"{j}:{step}"
    row["controls"] = {n: e[key] for n, e in controls_summary.items()
                       if isinstance(e, dict) and key in e}
    row["decoder_agreement"] = rec.get("decoder_agreement")
    return row


def outcome_d(state) -> dict:
    if state.get("fail"):
        f = str(state["fail"])
        f = f if f.startswith("FAIL_TECHNICAL") else "FAIL_TECHNICAL/" + f
        return {"outcome": f, "detail": f}
    if state.get("resource"):
        return {"outcome": "INCONCLUSIVE/RESOURCE_OR_AUTHORITY",
                "detail": {"reason": state["resource"], "partial": state.get("partial")}}
    if state.get("registry"):
        return {"outcome": "INCONCLUSIVE/REGISTRY_INCOMPLETE", "detail": state["registry"]}
    if state.get("headroom"):
        return {"outcome": "INCONCLUSIVE/HEADROOM", "detail": state["headroom"]}
    return {"outcome": "HWSD_REPORT", "detail": None}


class _Default(dict):
    def __missing__(self, key):
        return "n/a"


def _step(table, j, k):
    return table[j][k - 1]["step"] if k else None


def fill_templates(evaluation, table) -> dict:
    T, st, on = dc.CONTRACT["statements"]["templates"], evaluation["statements"], \
        evaluation["onsets"]
    out, fmt = {}, lambda key, **kw: T[key].format_map(_Default(kw))  # noqa: E731

    def ne(s):
        r = st[s]["reasons"]
        return fmt("NOT_EVALUABLE", statement=s, reasons="; ".join(
            f"{k} ({', '.join(str(m) for m in v)})" for k, v in r.items()))

    for s in ("D1", "D2", "D3", "D4", "D5", "D6"):
        a, per = st[s], st[s]["per_model"]
        if a["reading"] == "NOT_EVALUABLE":
            out[s] = ne(s)
        elif s == "D1":
            out[s] = "D1: the covariance was certified above 0.01 at step 5000 in each model." \
                if a["reading"] == "TRUE" else "D1: FALSE."
        elif s == "D2" and a["reading"] == "TRUE":
            out[s] = fmt("D2_TRUE", n_pre=", ".join(f"{j}: {evaluation['n_pre'][j]}" for j in per),
                         max_upper=", ".join(f"{j}: {evaluation['pre_chart_max'][j]}" for j in per),
                         qualifiers=", ".join(f"{j}: {per[j]['qualifier'] or per[j]['reading']}"
                                              for j in per))
        elif a["reading"] == "FALSE" and s in ("D2", "D3", "D4", "D5"):
            lines = []
            for j, v in per.items():
                if v["reading"] != "FALSE":
                    continue
                rows, kc = table[j], on[j]["k_C"]
                if s == "D2":
                    kb = next((k for k in range(1, (kc or 1)) if dst.above_s(rows[k - 1])), None)
                    lines.append(fmt("D2_FALSE", model=j, step=_step(table, j, kb),
                                     chart_step=_step(table, j, kc)))
                elif s == "D3":
                    lines.append(fmt("D3_FALSE", model=j, step=_step(table, j, kc)))
                elif s == "D5":
                    kp = _step(table, j, on[j]["k_P"])
                    lines.append(f"[{j}] " + fmt("D5_FALSE", steps=kp))
                else:
                    lines.append(f"D4: in model {j}, the covariance was already above 0.01 "
                                 f"when captured first reached 0.8.")
            out[s] = " ".join(lines)
        elif a["reading"] == "FALSE":
            out[s] = "D6: a model showed a certified loss after a certified gain."
        else:
            key = {"D3": "D3_TRUE", "D4": "D4_TRUE", "D5": "D5_TRUE", "D6": "D6_TRUE"}[s]
            src = {"D3": "k_C", "D4": "k_L", "D5": "k_P"}.get(s)
            steps = ", ".join(f"{j}: {_step(table, j, on[j][src])}" for j in per) if src else ""
            out[s] = fmt(key, steps=steps)
    if any(v["reason"] == "CHART_AT_INIT" for v in st["D3"]["per_model"].values()):
        out["D3_CHART_AT_INIT"] = fmt("D3_CHART_AT_INIT")
    return out


def _fracs(e) -> dict:
    return {k: (Fraction(v) if k.startswith("max_B") else v) for k, v in e.items()}


def _shared_inputs(out, shared):
    rel = "stages/S4/SHARED_CONTROLS.json"
    f = _checked(out, rel, "S4")
    meta = dc.read_json(f)
    return meta, {n: {"all": _fracs(meta[n])}
                  for n in SHARED}


def _controls_for(out, scores, shared_bounds):
    controls = {n: {} for n in ("decoder", "delta1", "delta2", "naive")}
    bounds = {n: {} for n in controls}
    for j, s in _order(scores):
        it = scores[(j, s)]
        a, key = it["arrays"], f"{j}:{s}"
        if a is None:
            continue
        rel = f"stages/SCORE/{j}/s{s}/CONTROLS_B.json"
        cb = dc.read_json(_checked(out, rel, f"SCORE_{j}")) \
            if (Path(out) / rel).exists() else {}
        z = {"max_B": "0", "certified": True}  # planted: no bound
        if "decoder_X" in a:
            controls["decoder"][key] = {"X": a["decoder_X"], "phi": a["decoder_phi"]}
            bounds["decoder"][key] = _fracs(cb.get("decoder", z))
        else:
            controls["decoder"][key] = {"unavailable": str(
                (it["record"].get("decoder") or {}).get("reason", ""))}
        for n in ("delta1", "delta2"):
            controls[n][key] = {"X_minus": a[f"{n}_X_minus"], "X_plus": a[f"{n}_X_plus"]}
            bounds[n][key] = _fracs(cb.get(n, z))
        controls["naive"][key] = {"X": a["naive_X"]}
        bounds["naive"][key] = _fracs(cb.get("naive", z))
    bounds.update(shared_bounds)
    return controls, bounds


def report(out, Z, shared, b4, stage_c=None) -> dict:
    out, Z = Path(out), (Z if isinstance(Z, Fraction) else Fraction(Z))
    scores = load_scores(out)
    draws = main_bootstrap(bootstrap_inputs_d(scores, shared))
    sdraws = strong_bootstrap(scores)
    meta, shared_bounds = _shared_inputs(out, shared)
    controls, bounds = _controls_for(out, scores, shared_bounds)
    controls.update({n: shared[n] for n in SHARED})
    cs = control_summary_d(draws, controls, bounds)
    cs_rows = dict(cs, B4_TEST={"point": (b4 or {}).get("point")})
    rows = {j: [checkpoint_row(j, s, scores[(j, s)], draws, sdraws, Z, cs_rows)
                for s in dc.STEPS] for j in dc.MASTERS}
    headroom_ok = (b4 or {}).get("status") == "PASS"
    ev = dst.evaluate(rows, headroom_ok=headroom_ok)
    state = {"headroom": None if headroom_ok else (b4 or {}).get("status", "HEADROOM")}
    oc = outcome_d(state)
    C = dc.CONTRACT["statements"]
    sha = lambda p: stage_records.sha256(p) if Path(p).is_file() else None  # noqa: E731
    ref = None
    if stage_c is not None:
        ref = {"label": "stage C, other rows",
               "per_model": {j: {"L": stage_c["per_model"][str(j)]["L"],
                                 "U": stage_c["per_model"][str(j)]["U"]} for j in dc.MASTERS
                             if str(j) in stage_c.get("per_model", {})}}
    rep = {"outcome": oc["outcome"], "outcome_detail": oc["detail"],
           "per_checkpoint": [r for j in dc.MASTERS for r in rows[j]],
           "onsets": ev["onsets"], "n_pre": ev["n_pre"], "pre_chart_max": ev["pre_chart_max"],
           "order": ev["order"], "statements": ev["statements"],
           "onset_order_line": ev["onset_order_line"], "diagnostics": ev["diagnostics"],
           "readings_text": fill_templates(ev, rows), "error_statements": C["error_statements"],
           "multiplicity": C["multiplicity"], "does_not_establish": C["does_not_establish"],
           "disclosure": dc.DISCLOSURE, "stage_c_reference": ref, "B4_TEST": b4,
           "seeds": {"main": k4b_config.SEEDS["endpoint"], "strong": hwsd_bind.strong_seed()},
           "ranks": {"main": dict(dc.RANKS), "strong": dict(dc.STRONG_RANKS)},
           "protocol_sha256": dc.PROTOCOL_SHA256, "freeze_sha256": sha(out / "FREEZE.json"),
           "registry_obligation_sha256": sha(out / "REGISTRY_OBLIGATION.json")}
    d = out / "stages" / "SUMMARY"
    d.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(d / "REPORT.json", hwsd_score._jsonable(rep))
    k4b_driver.complete_stage(out, "SUMMARY", [d / "REPORT.json"])
    return rep
