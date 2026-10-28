"""HWSB gates: B4 orchestration, the pilot ladder (B6), capture (B5), B7, B9a, the outcome
precedence, licences and HANDOFF (API.md §6; protocol §4, §5, §6.1).
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import math
from collections import defaultdict
from fractions import Fraction

import c1_means
import hwsb_data
import k4b_charts
import k4b_config
import numpy as np
import precision
from hwsb_config import ALPHA_C, M

NOT_CHARTED = "NOT_RUN/NO_CHART"
UNDERPOWERED = "INCONCLUSIVE/UNDERPOWERED"
SIDES = ("-", "+")

# ---------------------------------------------------------------------------------------- B4


def _cfg(cfg):
    return k4b_config.chart_cfg() if cfg is None else cfg


def b4_cal(out, X_cal, ids, m32_land, cfg=None) -> dict:
    trained, _ = k4b_charts.open_ledgers(out)
    per = {
        j: k4b_charts.build_chart(X_cal[j], ids, m32_land, trained, j, "production", _cfg(cfg))
        for j in X_cal
    }
    return {"per_model": per, "status": {j: r["status"] for j, r in per.items()}}


def b4_init(out, X_init, ids, m32_land, cfg=None) -> dict:
    return k4b_charts.init_charts(list(X_init), X_init, ids, m32_land, out, _cfg(cfg))


def b4_freeze(out, cal, init) -> dict:
    charts = {j: r for j, r in cal["per_model"].items() if r["status"] == "PASS"}
    return k4b_charts.freeze_production(out, charts, init, {})


def b4_val(out, cal, X_val, ids_val, cfg=None) -> dict:
    per = {}
    for j in X_val:
        if cal["per_model"].get(j, {}).get("status") == "PASS":
            res = k4b_charts.c0_val_gate(
                [j], cal["per_model"], {j: X_val[j]}, ids_val, out, _cfg(cfg)
            )
            per[j] = res["per_model"][j]
        else:
            per[j] = {"status": NOT_CHARTED}
    return {"per_model": per, "status": {j: r["status"] for j, r in per.items()}}


def _st(rec, j):
    s = rec.get("status", rec) if isinstance(rec, dict) else rec
    s = s.get(j) if isinstance(s, dict) else s
    return s.get("status") if isinstance(s, dict) else s


def b4_status(cal, val, masters) -> dict:
    per, failing, criterion, technical = {}, [], None, None
    for j in masters:
        c, v = _st(cal, j), _st(val, j)
        ok = c == "PASS" and v == "PASS"
        per[j] = {"c0_cal": c, "c0_val": v, "pass": ok}
        for s in (c, v):
            if technical is None and isinstance(s, str) and s.startswith("FAIL_TECHNICAL"):
                technical = s
        if not ok:
            failing.append(j)
            if criterion is None:
                criterion = "C0_CAL" if c != "PASS" else "C0_VAL"
    return {
        "per_model": per,
        "pass": not failing,
        "failing": failing,
        "criterion": criterion,
        "technical": technical,
    }


# ---------------------------------------------------------------------------------------- B6


def _q(col, p) -> float:
    return c1_means.quantile_with_rank(col, p)[0]


def _projection(e, keys, models, F_plan) -> dict:
    f, e = float(F_plan), np.asarray(e, dtype=np.float64)
    res = {n: {"per_model": {}, "joint": None} for n in ("support", "exclusion")}
    js, jx = np.ones(e.shape[0], bool), np.ones(e.shape[0], bool)
    for j in models:
        em, ep = e[:, keys.index((j, "-"))], e[:, keys.index((j, "+"))]
        s = 0.02 + em + _q(em, ALPHA_C) - f > 0.01
        x = (ep + _q(ep, 1 - ALPHA_C) + f < 0.01) & (em + _q(em, ALPHA_C) - f > -0.01)
        res["support"]["per_model"][j], res["exclusion"]["per_model"][j] = (
            int(s.sum()),
            int(x.sum()),
        )
        js &= s
        jx &= x
    res["support"]["joint"], res["exclusion"]["joint"] = int(js.sum()), int(jx.sum())
    res["ok"] = all(
        min(min(r["per_model"].values()), r["joint"]) >= hc.MIN_SUCCESSES
        for r in (res["support"], res["exclusion"])
    )
    return res


def _width(D_bar, e, keys, models, F_plan) -> dict:
    f, e = float(F_plan), np.asarray(e, dtype=np.float64)
    per, joint = {}, np.ones(e.shape[0], bool)
    for j in models:
        em, ep = e[:, keys.index((j, "-"))], e[:, keys.index((j, "+"))]
        d = float(D_bar[j])
        w = (d + ep + _q(ep, 1 - ALPHA_C) + f < 0.01) & (-d + em + _q(em, ALPHA_C) - f > -0.01)
        per[j] = int(w.sum())
        joint &= w
    return {"per_model": per, "joint": int(joint.sum())}


def _mde_ok(sdU, N, F_plan) -> bool:
    cfg = {
        "delta": float(M + F_plan),
        "alpha": float(ALPHA_C),
        "power": 0.80,
        "projected_N": int(N),
    }
    return all(precision.mde(sd, cfg) <= 0.02 for sd in sdU.values())


def ladder_pilot(
    X_minus,
    X_plus,
    r4n,
    F_plan,
    models=hc.MASTERS,
    seeds=(hc.SEEDS["sd_upper"], hc.SEEDS["projection"]),
    D_bar=None,
    ladder=hc.LADDER,
) -> dict:
    """k4b_stats.ladder with the model list as an argument (DRB9 bitwise on K4b keys)."""
    models = list(models)
    sdU = {}
    for side, X in (("-", X_minus), ("+", X_plus)):
        Xd = {j: np.asarray(X[j], dtype=np.float64) for j in models}
        rd = {j: np.asarray(r4n[j], dtype=np.float64) for j in models}
        sd, _ = precision.sd_b4_draws(Xd, rd, models, seeds[0], hc.DRAWS, len(Xd[models[0]]))
        for i, j in enumerate(models):
            sdU[(j, side)] = c1_means.quantile_with_rank(sd[:, i], 1 - ALPHA_C)[0]
    keys = [(j, s) for j in models for s in SIDES]
    X = {}
    for j in models:
        X[(j, "-")] = np.asarray(X_minus[j], dtype=np.float64)
        X[(j, "+")] = np.asarray(X_plus[j], dtype=np.float64)
    cands, chosen = {}, None
    for N in ladder:
        e = precision.centered_draws(X, list(keys), seeds[1], hc.DRAWS, int(N))
        cands[N] = {
            "mde_ok": _mde_ok(sdU, N, F_plan),
            "projection": _projection(e, keys, models, F_plan),
            "width_diagnostic": None if D_bar is None else _width(D_bar, e, keys, models, F_plan),
        }
        if cands[N]["mde_ok"] and cands[N]["projection"]["ok"]:
            chosen = N
            break
    return {
        "status": "PASS" if chosen else UNDERPOWERED,
        "N": chosen,
        "k": chosen // k4b_config.BLOCK if chosen else None,
        "sdU": sdU,
        "candidates": cands,
    }


def b5_N(ladder_result) -> int:
    n = ladder_result.get("N") if ladder_result else None
    return int(n) if n is not None else hc.C_MIN_FALLBACK_N


# ---------------------------------------------------------------------------------------- B5


def c_min(sdU_minus, N_C, F_plan, D4hat) -> float:
    cfg = {
        "delta": float(M + F_plan),
        "alpha": float(ALPHA_C),
        "power": 0.80,
        "projected_N": int(N_C),
    }
    return precision.mde(sdU_minus, cfg) / D4hat


def c_min_literal(sdU_minus, N_C, F_plan, D4hat) -> float:
    return (float(M + F_plan) + hc.Z_C * float(sdU_minus) / math.sqrt(N_C)) / D4hat


def capture_pass(c_hat, c_min_value) -> bool:
    return bool(c_hat >= c_min_value)


def b5(X_minus, D4_rows, sdU_minus, N_C, F_plan, models, seed=hc.SEEDS["capture_ci"]) -> dict:
    models = list(models)
    D4hat = float(c1_means.tree_mean(np.asarray(D4_rows, dtype=np.float64)))
    if not (math.isfinite(D4hat) and D4hat > 0):
        raise hc.HwsbStop("FAIL_TECHNICAL/NUMERICAL", f"D4hat = {D4hat!r} is not positive")
    arrays = {f"X_minus_{j}": np.asarray(X_minus[j], dtype=np.float64) for j in models}
    arrays["D4"] = np.asarray(D4_rows, dtype=np.float64)
    draws = c1_means.bootstrap_means(arrays, seed, hc.DRAWS)
    per = {}
    for j in models:
        mean_x = float(c1_means.tree_mean(arrays[f"X_minus_{j}"]))
        c_hat = mean_x / D4hat
        cm = c_min(sdU_minus[j], N_C, F_plan, D4hat)
        ratio = draws[f"X_minus_{j}"] / draws["D4"]
        per[j] = {
            "mean_X_minus": mean_x,
            "c_hat": c_hat,
            "c_min": cm,
            "c_min_literal": c_min_literal(sdU_minus[j], N_C, F_plan, D4hat),
            "pass": capture_pass(c_hat, cm),
            "ci95": (_q(ratio, 0.025), _q(ratio, 0.975)),
            "lower_rank125_mean_X_minus": _q(draws[f"X_minus_{j}"], 0.025),
        }
    return {
        "D4hat": D4hat,
        "N_C": int(N_C),
        "per_model": per,
        "status": "PASS" if all(r["pass"] for r in per.values()) else "FAIL",
        "positive_below_planning": all(r["lower_rank125_mean_X_minus"] > 0 for r in per.values()),
    }


# --------------------------------------------------------------------------------- B7, B9a


def b7(cpu_by_model, N_C) -> dict:
    cpu = {j: float(v) for j, v in (cpu_by_model or {}).items()}
    if not cpu:
        return {
            "model_count": 3,
            "training_forecast_s": "unavailable",
            "evaluation_forecast_s": "unavailable",
            "cpu_by_model": {},
        }
    return {
        "model_count": 3,
        "training_forecast_s": 3 * max(cpu.values()),
        "evaluation_forecast_s": 1280.5 + 1720.1 * int(N_C) / 3072,
        "cpu_by_model": cpu,
    }


def b9a(store, N_C, p_d2a, p_d2a_ref, eval_blocks) -> dict:
    """B9a; (i)/(ii) hash and read stage B's OWN history payloads (ruling c7)."""
    import k4b_data

    inv = hwsb_data.history_inventory(store)
    reg = hwsb_data.registry_digests(store, expected=inv)
    value = Fraction(float(p_d2a)) * (3072 + 3072 + int(N_C))
    rel = abs(float(p_d2a) - float(p_d2a_ref)) / abs(float(p_d2a_ref))
    ok = reg["status"] == "PASS" and value <= hc.REGISTRY_CAP and rel <= 1e-12
    hits = {
        r: int(np.sum(k4b_data.sealed_d2a_predicate(b["canon32"]))) for r, b in eval_blocks.items()
    }
    return {
        "status": "PASS" if ok else "FAIL_TECHNICAL/REGISTRY",
        "inventory": inv,
        "registry": {k: v for k, v in reg.items() if k != "digests"},
        "value": str(value),
        "value_ok": value <= hc.REGISTRY_CAP,
        "p_D2a": float(p_d2a),
        "p_D2a_ref": float(p_d2a_ref),
        "rel_diff": rel,
        "predicate_hits": hits,
        "own_payloads_hashed": True,
    }


# --------------------------------------------------------------------- outcome and licence


def outcome(state) -> dict:
    oc = {"k": None, "models": None, "criterion": None, "annotations": []}
    b1 = state.get("b1") or {}
    b4 = state.get("b4") or {}
    b5 = state.get("b5") or {}

    def done(o, **kw):
        return dict(oc, outcome=o, **kw)

    fail = state.get("fail")
    if fail:
        return done(fail if str(fail).startswith("FAIL_TECHNICAL/") else f"FAIL_TECHNICAL/{fail}")
    if any(v == "INCONCLUSIVE" for v in b1.values()):
        return done("FAIL_TECHNICAL/NUMERICAL")
    if state.get("b8a") is not None and state.get("b8a") != "PASS":
        return done("FAIL_TECHNICAL/LAW_BOUND")
    if state.get("b9a") is not None and state.get("b9a") != "PASS":
        return done("FAIL_TECHNICAL/REGISTRY")
    if state.get("incomplete"):
        return done("INCONCLUSIVE/RESOURCE_OR_AUTHORITY")
    bad1 = [j for j in hc.MASTERS if b1.get(j) == "FAIL"] + [
        j for j in b1 if j not in hc.MASTERS and b1[j] == "FAIL"
    ]
    if bad1:
        return done("HWSB_NOT_LEARNED", k=len(bad1), models=bad1)
    order = [j for j in hc.MASTERS if j in b4] + [j for j in b4 if j not in hc.MASTERS]
    bad4 = [j for j in order if b4[j] != "PASS"]
    if bad4:
        crit = b4[bad4[0]]
        return done(f"HWSB_NO_CIRCLE/{crit}", models=bad4, criterion=crit)
    if state.get("b6") == "FAIL":
        return done("HWSB_UNDERPOWERED/LADDER")
    if any(v == "FAIL" for v in b5.values()):
        ann = ["POSITIVE_BELOW_PLANNING"] if state.get("b5_positive") else []
        return done("HWSB_UNDERPOWERED/CAPTURE", annotations=ann)
    if (
        b1
        and b4
        and b5
        and all(v == "PASS" for v in list(b1.values()) + list(b4.values()) + list(b5.values()))
        and all(state.get(k) == "PASS" for k in ("b6", "b8a", "b9a"))
    ):
        return done("HWSB_PASS")
    return done("FAIL_TECHNICAL/OUTCOME")


def _head(o) -> str:
    if o.startswith("FAIL_TECHNICAL"):
        return "FAIL_TECHNICAL"
    if o.startswith(("HWSB_NO_CIRCLE", "HWSB_UNDERPOWERED")):
        return o.split("/")[0]
    return o


def licence(oc, fill) -> str:
    L = hc.CONTRACT["licences"]
    values = defaultdict(lambda: "n/a")
    values.update({k: v for k, v in (fill or {}).items() if v is not None})
    for k in ("k", "models", "criterion"):
        if oc.get(k) is not None:
            values[k] = ", ".join(map(str, oc[k])) if isinstance(oc[k], list) else oc[k]
    text = L[_head(oc["outcome"])].format_map(values)
    if "POSITIVE_BELOW_PLANNING" in (oc.get("annotations") or []):
        text += " " + L["POSITIVE_BELOW_PLANNING"]
    return text


def check_handoff(obj, top=True) -> None:
    H = hc.CONTRACT["handoff"]
    if top and isinstance(obj, dict):
        extra = [k for k in obj if k not in H["keys"]]
        if extra:
            raise hc.HwsbStop("FAIL_TECHNICAL/BLINDNESS", f"keys outside the HANDOFF list: {extra}")
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k) in H["forbidden_keys"]:
                raise hc.HwsbStop("FAIL_TECHNICAL/BLINDNESS", str(k))
            check_handoff(v, False)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            check_handoff(v, False)


def handoff_record(fields) -> dict:
    keys = hc.CONTRACT["handoff"]["keys"]
    missing = [k for k in keys if k not in fields]
    if missing:
        raise hc.HwsbStop("FAIL_TECHNICAL/BLINDNESS", f"HANDOFF fields missing: {missing}")
    rec = {k: fields[k] for k in keys}
    check_handoff(rec)
    return rec
