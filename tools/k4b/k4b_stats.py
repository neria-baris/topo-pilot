"""K4b joint bootstrap, ranks, statuses, the precision ladder and sealing (API.md §8).

Protocol §5.4 (ranks), §7 (ladder: MDE, projection, width diagnostic; sealing), §8.1-§8.2
(per-model status in exact rationals with strict inequalities; overall outcome).
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import c1_means
import k4b_config
import numpy as np
import precision
from c1_records import C1GateFailure
from k4b_config import ALPHA, DRAWS, LADDER, MARGIN, MODELS, RANKS, SEEDS

NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"
SEALED_KEYS = ("mean_X_minus", "mean_X_plus", "control_means", "init_means", "decoder_means",
               "delta1_mean", "delta2_mean", "delta4_orc_mean", "supported_contribution",
               "supported_conditional_mean", "endpoint_ratios")
SEALED_FILE = "SEALED_VALIDATION.json"
MIN_SUCCESSES = 4000


def joint_bootstrap(arrays, seed, draws=DRAWS) -> dict:
    return c1_means.bootstrap_means(arrays, seed, draws)


def _q(values, p, rank) -> tuple:
    values = np.asarray(values, dtype=np.float64)
    if not np.all(np.isfinite(values)):
        raise C1GateFailure(NUMERICAL, "non-finite bootstrap draws")
    v, k = c1_means.quantile_with_rank(values, p)
    if k != rank or not c1_means.rank_check(values, v, k):
        raise C1GateFailure(NUMERICAL, f"rank check failed (rank {k}, expected {rank})")
    return v, k


def bounds(draws_minus, draws_plus) -> dict:
    """L (rank 84) of the X- draws, U (rank 4,917) of the X+ draws, central 95% of both."""
    L = _q(draws_minus, ALPHA, RANKS["alpha"])
    U = _q(draws_plus, 1 - ALPHA, RANKS["one_minus_alpha"])
    central = {}
    for name, d in (("central95_minus", draws_minus), ("central95_plus", draws_plus)):
        central[name] = (_q(d, 0.025, RANKS["central_lo"]), _q(d, 0.975, RANKS["central_hi"]))
    return dict({"L": L, "U": U, "L_rank": L[1], "U_rank": U[1]}, **central)


def _fr(x) -> Fraction:
    if isinstance(x, (tuple, list)):
        x = x[0]
    return x if isinstance(x, Fraction) else Fraction(x) if isinstance(x, int) \
        else Fraction(float(x))


def _status(L, U, Fm, Fp) -> str:
    if L - Fm > MARGIN:
        return "SUPPORT"
    if U + Fp < MARGIN and L - Fm > -MARGIN:
        return "EXCLUDE"
    return "UNRESOLVED"


def model_status(L, U, F_minus, F_plus) -> dict:
    """§8.1 in exact rationals, strict inequalities; UNRESOLVED/NUMERICAL when F alone blocks."""
    L, U, Fm, Fp = _fr(L), _fr(U), _fr(F_minus), _fr(F_plus)
    s, s0 = _status(L, U, Fm, Fp), _status(L, U, Fraction(0), Fraction(0))
    if s == "UNRESOLVED" and s0 != "UNRESOLVED":
        s = "UNRESOLVED/NUMERICAL"
    labels = ["NEGATIVE_ALIGNMENT"] if U + Fp < -MARGIN else []
    return {"status": s, "labels": labels, "status_without_F": s0}


def overall(per_model) -> str:
    st = [per_model[j] for j in MODELS] if set(per_model) == set(MODELS) \
        else list(per_model.values())
    definite = [s for s in st if s in ("SUPPORT", "EXCLUDE")]
    if len(definite) == len(st) and set(definite) == {"SUPPORT"}:
        return "SUPPORT"
    if len(definite) == len(st) and set(definite) == {"EXCLUDE"}:
        return "EXCLUSION"
    if definite:
        return "MIXED"
    return "INCONCLUSIVE/NUMERICAL" if "UNRESOLVED/NUMERICAL" in st else "INCONCLUSIVE"


def sd_upper(X_minus, X_plus, r4n, seed=SEEDS["val_sd"]) -> dict:
    """SD^U per (model, side): rank-4,917 quantile of the sd draws (precision.sd_b4_draws)."""
    out = {}
    for side, X in (("-", X_minus), ("+", X_plus)):
        Xd = {j: np.asarray(X[j], dtype=np.float64) for j in MODELS}
        rd = {j: np.asarray(r4n[j], dtype=np.float64) for j in MODELS}
        sd, _ = precision.sd_b4_draws(Xd, rd, list(MODELS), seed, DRAWS, len(Xd[MODELS[0]]))
        for i, j in enumerate(MODELS):
            out[(j, side)] = c1_means.quantile_with_rank(sd[:, i], 1 - ALPHA)[0]
    return out


def mde_ok(sdU, N, F_plan) -> bool:
    cfg = {"delta": float(MARGIN + F_plan), "alpha": float(ALPHA), "power": 0.80,
           "projected_N": int(N)}
    return all(precision.mde(sd, cfg) <= 0.02 for sd in sdU.values())


def centered(X_dict, keys, N, seed=SEEDS["val_projection"]) -> np.ndarray:
    return precision.centered_draws(X_dict, list(keys), seed, DRAWS, int(N))


def _cols(e, keys, j) -> tuple:
    keys = list(keys)
    return e[:, keys.index((j, "-"))], e[:, keys.index((j, "+"))]


def _qa(col) -> float:
    return c1_means.quantile_with_rank(col, ALPHA)[0]


def _qb(col) -> float:
    return c1_means.quantile_with_rank(col, 1 - ALPHA)[0]


def projection(e, keys, F_plan) -> dict:
    """§7.2(2) in float: SUPPORT and EXCLUSION success counts, per model and joint."""
    f, e = float(F_plan), np.asarray(e, dtype=np.float64)
    res = {n: {"per_model": {}, "joint": None} for n in ("support", "exclusion")}
    js, jx = np.ones(e.shape[0], bool), np.ones(e.shape[0], bool)
    for j in MODELS:
        em, ep = _cols(e, keys, j)
        s = 0.02 + em + _qa(em) - f > 0.01
        x = (ep + _qb(ep) + f < 0.01) & (em + _qa(em) - f > -0.01)
        res["support"]["per_model"][j], res["exclusion"]["per_model"][j] = int(s.sum()), \
            int(x.sum())
        js &= s
        jx &= x
    res["support"]["joint"], res["exclusion"]["joint"] = int(js.sum()), int(jx.sum())
    res["ok"] = all(min(min(r["per_model"].values()), r["joint"]) >= MIN_SUCCESSES
                    for r in (res["support"], res["exclusion"]))
    return res


def width_diagnostic(D_bar, e, keys, F_plan) -> dict:
    """§7.6 (report only): [D + e+ + q(e+) + F < 0.01] and [-D + e- + q(e-) - F > -0.01]."""
    f, e = float(F_plan), np.asarray(e, dtype=np.float64)
    per, joint = {}, np.ones(e.shape[0], bool)
    for j in MODELS:
        em, ep = _cols(e, keys, j)
        d = float(D_bar[j])
        w = (d + ep + _qb(ep) + f < 0.01) & (-d + em + _qa(em) - f > -0.01)
        per[j] = int(w.sum())
        joint &= w
    return {"per_model": per, "joint": int(joint.sum())}


def ladder(X_minus, X_plus, r4n, F_plan, D_bar) -> dict:
    """First N of LADDER with mde_ok and projection ok; else INCONCLUSIVE/UNDERPOWERED."""
    keys = [(j, s) for j in MODELS for s in ("-", "+")]
    X = {}
    for j in MODELS:
        X[(j, "-")] = np.asarray(X_minus[j], dtype=np.float64)
        X[(j, "+")] = np.asarray(X_plus[j], dtype=np.float64)
    sdU = sd_upper(X_minus, X_plus, r4n)
    cands, chosen = {}, None
    for N in LADDER:
        e = centered(X, keys, N)
        cands[N] = {"mde_ok": mde_ok(sdU, N, F_plan), "projection": projection(e, keys, F_plan),
                    "width_diagnostic": width_diagnostic(D_bar, e, keys, F_plan)}
        if cands[N]["mde_ok"] and cands[N]["projection"]["ok"]:
            chosen = N
            break
    return {"status": "PASS" if chosen else "INCONCLUSIVE/UNDERPOWERED", "N": chosen,
            "k": chosen // k4b_config.BLOCK if chosen else None, "sdU": sdU, "candidates": cands}


def _means(x):
    if isinstance(x, dict):
        return {str(k): _means(v) for k, v in x.items()}
    return float(c1_means.tree_mean(np.asarray(x, dtype=np.float64)))


def write_sealed(out, arrays) -> str:
    """The only writer of SEALED_VALIDATION.json (exclusive create, once); returns its sha256."""
    path = Path(out) / SEALED_FILE
    body = {"protocol_sha256": k4b_config.CONTRACT["protocol_sha256"],
            "means": {str(k): _means(v) for k, v in arrays.items()}}
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(body, sort_keys=True) + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsealed(report) -> None:
    """Refuse any SEALED_KEYS key anywhere in a validation report (recursive)."""
    if isinstance(report, dict):
        for k, v in report.items():
            if str(k) in SEALED_KEYS:
                raise C1GateFailure("FAIL_TECHNICAL/SEALING", str(k))
            check_unsealed(v)
    elif isinstance(report, (list, tuple)):
        for v in report:
            check_unsealed(v)
