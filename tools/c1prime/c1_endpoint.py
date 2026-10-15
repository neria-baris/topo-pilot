"""C1' crossed contrast, inference and decision (API.md §11; protocol §11-§13; §15.3.2 C4-C7).
A, Y, Z and Z_full use the prescribed ordered elementwise kernels; bootstrap means use the tree
kernel with one shared index draw per bootstrap replicate; ranks are verified at run time."""

from __future__ import annotations

import math
from fractions import Fraction

import c1_bounds
import c1_config
import c1_means
import numpy as np
import precision
from oracle_profile import percentile_interval

P_LOW = c1_means.P_THIRD
P_HIGH = 1 - c1_means.P_THIRD


def _osum_dot(x, y) -> np.ndarray:
    acc = x[:, 0] * y[:, 0]
    for v in range(1, x.shape[1]):
        acc = acc + x[:, v] * y[:, v]
    return acc


def A_hat(d, z_plus, z_minus) -> np.ndarray:
    """C4: Delta = z+ - z-, A = 0.5 * osum_v(d_v * Delta_v) (canonical order, caller-gathered)."""
    d = np.asarray(d, dtype=np.float64)
    Delta = np.asarray(z_plus, dtype=np.float64) - np.asarray(z_minus, dtype=np.float64)
    return 0.5 * _osum_dot(d, Delta)


def Y_hat(A_T, A_C_list) -> np.ndarray:
    acc = np.asarray(A_C_list[0], dtype=np.float64)
    for a in A_C_list[1:]:
        acc = acc + np.asarray(a, dtype=np.float64)
    return np.asarray(A_T, dtype=np.float64) - acc * 2.0 ** -5


def Z_hat(Y, G) -> np.ndarray:
    return np.asarray(Y, dtype=np.float64) - 0.1 * np.asarray(G, dtype=np.float64)


def Zfull_hat(A_full, G) -> np.ndarray:
    return np.asarray(A_full, dtype=np.float64) - 0.3 * np.asarray(G, dtype=np.float64)


def A_logsoftmax(qp, qm, lp_plus, lp_minus) -> np.ndarray:
    """The log-softmax definition (secondary quantities and checks only)."""
    d = np.asarray(qp) - np.asarray(qm)
    return 0.5 * np.sum(d * (np.asarray(lp_plus) - np.asarray(lp_minus)), axis=1)


def endpoint_bounds(Z_by_model, seed=520503, draws=5000) -> dict:
    means = c1_means.bootstrap_means(Z_by_model, seed, draws)
    out = {"means": means, "per_model": {}}
    for j, m in means.items():
        L, kL = c1_means.quantile_with_rank(m, P_LOW)
        U, kU = c1_means.quantile_with_rank(m, P_HIGH)
        out["per_model"][j] = {"L": L, "U": U, "rank_L": kL, "rank_U": kU}
    return out


def per_model_status(L, U) -> str:
    if L > 0:
        return "PASS_j"
    return "FAIL_j" if U < 0 else "INC_j"


def overall(statuses) -> str:
    vals = list(statuses.values()) if isinstance(statuses, dict) else list(statuses)
    if all(s == "PASS_j" for s in vals):
        return "PASS"
    return "FAIL" if all(s == "FAIL_j" for s in vals) else "MIXED"


def v3(Zfull_by_model, B_V3, seed) -> dict:
    means = c1_means.bootstrap_means(Zfull_by_model, seed, 5000)
    lows = {j: c1_means.quantile_with_rank(m, P_LOW) for j, m in means.items()}
    order = list(Zfull_by_model)
    status = c1_bounds.guard_V3([lows[j][0] for j in order], [B_V3[j] for j in order])
    return {"lower": {j: lows[j][0] for j in order}, "rank": {j: lows[j][1] for j in order},
            "status": status}


def h5(G, B_H, seed) -> dict:
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    means = c1_means.c1_bootstrap_means(np.asarray(G, dtype=np.float64), rng, 5000)
    lower = float(percentile_interval(means, [0.05])[0])
    k = c1_means.rank_for(Fraction(1, 20), len(means))
    if not c1_means.rank_check(means, lower, k):
        return {"lower": lower, "rank": k, "status": "FAIL_TECHNICAL/NUMERICAL"}
    return {"lower": lower, "rank": k, "status": c1_bounds.guard_H5(lower, B_H)}


def ladder(Z_val, G_val, models=c1_config.MODELS) -> dict:
    models = list(models)
    n_val = len(np.asarray(G_val))
    G_val = np.asarray(G_val, dtype=np.float64)
    sd, _ = precision.sd_b4_draws(X={j: Z_val[j] for j in models}, r4n={j: G_val for j in models},
                                  models=models, seed=520501, draws=5000, size=n_val)
    alternative = (0.20 - 0.10) * float(np.mean(G_val))
    summaries, N_test = {}, None
    for N in (4096, 8192, 16384):
        e = precision.centered_draws(X={j: Z_val[j] for j in models}, models=models, seed=520502,
                                     draws=5000, size=N)
        cfg = {"alpha": 0.05 / 3, "power": 0.80, "delta": 0.0, "alternative": alternative,
               "projected_N": N}
        summaries[N] = precision.precision_summary(sd, e, models, cfg)
        if N_test is None and summaries[N]["status"] == "PASS":
            N_test = N
    status = "PASS" if N_test is not None else "INCONCLUSIVE/UNDERPOWERED"
    return {"summaries": summaries, "N_test": N_test, "status": status}


def k_blocks(N_test, f_val) -> int:
    denom = (Fraction(float(f_val)) - Fraction(2, 100)) * 4096
    return math.ceil(Fraction(int(N_test)) / denom)


def fresh_fraction_ok(f_test, f_val) -> bool:
    ft, fv, slack = Fraction(float(f_test)), Fraction(float(f_val)), Fraction(2, 100)
    return abs(ft - fv) <= slack and ft >= fv - slack


def ratio_reduction(meanY, meanG, c) -> bool:
    if not meanG > 0:
        raise ValueError("ratio reduction needs E[G] > 0")
    return meanY - c * meanG > 0
