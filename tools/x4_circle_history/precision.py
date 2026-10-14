"""Fixed-chart validation precision and B4 headroom gates (API.md precision.py)."""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np
from errors import Invalid


def _arrays(values: dict, models) -> list[np.ndarray]:
    arrays = [np.asarray(values[m], dtype=np.float64) for m in models]
    n = arrays[0].shape[0] if arrays else 0
    if not arrays or any(a.ndim != 1 or a.shape[0] != n for a in arrays) or n < 2:
        raise Invalid("per-model rows must be equal-length 1-d arrays with n >= 2")
    if not all(np.isfinite(a).all() for a in arrays):
        raise Invalid("non-finite precision input")
    return arrays


def sd_b4_draws(X: dict, r4n: dict, models, seed, draws, size):
    """Joint whole-trajectory resamples: ONE index per draw shared by every model."""
    xs, rs = _arrays(X, models), _arrays(r4n, models)
    if rs[0].shape[0] != xs[0].shape[0]:
        raise Invalid("X and r4 norms differ in length")
    n = xs[0].shape[0]
    rng = np.random.Generator(np.random.PCG64(seed))
    sd = np.empty((draws, len(xs)))
    b4 = np.empty((draws, len(xs)))
    for b in range(draws):
        idx = rng.integers(0, n, size=size)
        for k in range(len(xs)):
            sd[b, k] = np.std(xs[k][idx], ddof=1)
            b4[b, k] = np.mean(rs[k][idx])
    return sd, b4


def centered_draws(X: dict, models, seed, draws, size):
    xs = _arrays(X, models)
    n = xs[0].shape[0]
    means = [float(np.mean(x)) for x in xs]
    rng = np.random.Generator(np.random.PCG64(seed))
    e = np.empty((draws, len(xs)))
    for b in range(draws):
        idx = rng.integers(0, n, size=size)
        for k in range(len(xs)):
            e[b, k] = np.mean(xs[k][idx]) - means[k]
    return e


def mde(sd, cfg) -> float:
    nd = NormalDist()
    z = nd.inv_cdf(1.0 - cfg["alpha"]) + nd.inv_cdf(cfg["power"])
    return cfg["delta"] + z * float(sd) / math.sqrt(cfg["projected_N"])


def _q(values, prob) -> float:
    return float(np.quantile(np.asarray(values, dtype=np.float64), prob, method="inverted_cdf"))


def _draw_matrix(draws, models, name) -> np.ndarray:
    arr = np.asarray(draws, dtype=np.float64)
    if len(models) == 0 or len(set(models)) != len(models):
        raise Invalid("models must be a non-empty list without duplicates")
    if arr.ndim != 2 or arr.shape[0] < 1 or arr.shape[1] != len(models):
        raise Invalid(f"{name} must be [draws >= 1, len(models)], got {arr.shape}")
    if not np.isfinite(arr).all():
        raise Invalid(f"non-finite {name}")
    return arr


def precision_summary(sd, e, models, cfg) -> dict:
    sd, e = _draw_matrix(sd, models, "sd draws"), _draw_matrix(e, models, "centered draws")
    alpha = cfg["alpha"]
    per = {}
    for k, m in enumerate(models):
        lo, hi = _q(sd[:, k], alpha), _q(sd[:, k], 1.0 - alpha)
        q_alpha = _q(e[:, k], alpha)
        power = float(np.mean(cfg["alternative"] + e[:, k] + q_alpha > cfg["delta"]))
        per[m] = {
            "sd_lower": lo,
            "sd_upper": hi,
            "mde_lower": mde(lo, cfg),
            "mde_upper": mde(hi, cfg),
            "q_alpha": q_alpha,
            "power": power,
        }
    met = all(
        v["mde_upper"] <= cfg["alternative"] and v["power"] >= cfg["power"] for v in per.values()
    )
    return {"models": per, "status": "PASS" if met else "INCONCLUSIVE", "criterion_met": met}


def b4_summary(b4_draws, b4_point: dict, models, cfg) -> dict:
    draws = _draw_matrix(b4_draws, models, "B4 draws")
    if set(b4_point) != set(models) or not all(np.isfinite(b4_point[m]) for m in models):
        raise Invalid("B4 point estimates must be finite and cover exactly the models")
    per = {
        m: {
            "point": float(b4_point[m]),
            "lower": _q(draws[:, k], 0.05),
            "upper": _q(draws[:, k], 0.95),
        }
        for k, m in enumerate(models)
    }
    met = all(v["lower"] > cfg["delta"] for v in per.values())
    return {"models": per, "status": "PASS" if met else "INCONCLUSIVE", "criterion_met": met}


CONTROL_NAMES = ("m1_unit", "m4_unit", "sha256_last4")
_CONTROL_Q = {"central95": (0.025, 0.975), "bonferroni": (0.05 / 3, 1.0 - 0.05 / 3)}


def control_summary(C: dict, models, seed, draws) -> dict:
    """Validation control means with joint whole-trajectory resampling (spec v2.4 item 10).

    ONE rng.integers(0, n, size=n) call per draw, shared by every control and model (with
    seed = sd_seed this is exactly the SD/B4 index stream). Reported only: no status, no gate.
    """
    models = list(models)
    if not models or len(set(models)) != len(models):
        raise Invalid("models must be a non-empty list without duplicates")
    if set(C) - set(CONTROL_NAMES) or not C:
        raise Invalid(f"unknown or missing control names: {sorted(C)}")
    names = [name for name in CONTROL_NAMES if name in C]
    series = {name: _arrays(C[name], models) for name in names}
    n = series[names[0]][0].shape[0]
    if any(a.shape[0] != n for arrs in series.values() for a in arrs):
        raise Invalid("control arrays differ in length")
    rng = np.random.Generator(np.random.PCG64(seed))
    means = {name: np.empty((int(draws), len(models))) for name in names}
    for b in range(int(draws)):
        idx = rng.integers(0, n, size=n)
        for name in names:
            for k, a in enumerate(series[name]):
                means[name][b, k] = np.mean(a[idx])
    out = {}
    for name in names:
        out[name] = {}
        for k, m in enumerate(models):
            col = means[name][:, k]
            out[name][m] = {"point": float(np.mean(series[name][k]))} | {
                label: [_q(col, lo), _q(col, hi)] for label, (lo, hi) in _CONTROL_Q.items()
            }
    return out
