"""HWSB evaluation: logits, B1-B3, activations, oracle moments, X+- and support (API.md §4).

Protocol §2.4 (float32 logits at index 32 softmaxed in float64, E4's path; float64 activations
at resid_post_3/32 via c1_model), §4 B1-B3, B4-B6 inputs. Logits never mix with the float64
activation forwards.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import math

import c1_means
import c1_model
import hws_oracle
import k4b_scores
import numpy as np
import torch
from hwsb_data import model_inputs

from topo_pilot.contracts import Status
from topo_pilot.learner.stage import load_model
from topo_pilot.prediction.metrics import LearningGate, PredictiveMetrics

NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"


def _mean(x) -> float:
    return float(c1_means.tree_mean(np.asarray(x, dtype=np.float64)))


def load_float32(checkpoint):
    return load_model(checkpoint)


def logits32(model, inputs, batch=256) -> np.ndarray:
    """ActivationExtractor's logits path: plain forward, position 32, float32."""
    model.eval()
    parts = []
    with torch.no_grad():
        for start in range(0, int(inputs.shape[0]), int(batch)):
            out = model(inputs[start : start + int(batch)])
            parts.append(out.logits[:, hc.INDEX].float().cpu().numpy())
    return np.concatenate(parts).astype(np.float32, copy=False)


def softmax64(logits) -> np.ndarray:
    l64 = np.asarray(logits).astype(np.float64)
    p = np.exp(l64 - l64.max(axis=1, keepdims=True))
    p /= p.sum(axis=1, keepdims=True)
    return p


def to_canonical(p_named, perm) -> np.ndarray:
    return np.asarray(p_named)[:, np.asarray(perm, dtype=np.int64)]


def check_rows(p, tol=1e-6) -> np.ndarray:
    p = np.asarray(p, dtype=np.float64)
    if (
        p.ndim != 2
        or not np.all(np.isfinite(p))
        or np.any(p < 0)
        or np.any(np.abs(p.sum(axis=1) - 1.0) > tol)
    ):
        raise hc.HwsbStop(NUMERICAL, f"model predictive rows are not distributions within {tol}")
    return p


def model_predictive(checkpoint, canon32, perm, batch=256) -> np.ndarray:
    lg = logits32(load_float32(checkpoint), model_inputs(canon32, perm), batch)
    return check_rows(to_canonical(softmax64(lg), perm))


def oracle_predictives(proc, canon32, Ks=(1, 4)) -> dict:
    T, E = proc["T"], proc["E_canon_shared"]
    b = hws_oracle.beliefs({"T": T, "E": E, "pi": proc["pi"]}, np.asarray(canon32), Ks)
    keys = sorted(set(int(k) for k in Ks) | {int(np.asarray(canon32).shape[1])})
    return {K: hws_oracle.predictive(b[K], T, E) for K in keys}


def _sd_se(x) -> tuple:
    x = np.asarray(x, dtype=np.float64)
    sd = float(np.std(x, ddof=1)) if x.size > 1 else 0.0
    return sd, sd / math.sqrt(x.size) if x.size else 0.0


def b1(q, p) -> dict:
    rows = hws_oracle.kl_rows(q[32], p)
    gc_rows = hws_oracle.kl_rows(q[32], q[1])
    regret, G_C = _mean(rows), _mean(gc_rows)
    captured = PredictiveMetrics.captured(regret, G_C)
    check, st = LearningGate(float(hc.LEARN)).evaluate_with_status(captured)
    status = "INCONCLUSIVE" if st == Status.INCONCLUSIVE else ("PASS" if check.passed else "FAIL")
    sd, se = _sd_se(rows)
    return {
        "regret": regret,
        "G_C": G_C,
        "captured": captured,
        "status": status,
        "regret_sd": sd,
        "regret_se": se,
        "G_C_sd": _sd_se(gc_rows)[0],
        "n": int(rows.size),
    }


def forcing(q_full, q_base, p, z=hc.Z_B23) -> dict:
    base = hws_oracle.kl_rows(q_full, q_base)
    model = hws_oracle.kl_rows(q_full, p)
    d = base - model
    G_hat, r, d_mean = _mean(base), _mean(model), _mean(d)
    se = _sd_se(d)[1]
    L = d_mean - float(z) * se
    return {
        "G_hat": G_hat,
        "r": r,
        "ratio": r / G_hat if G_hat > 0 else "undefined",
        "d_mean": d_mean,
        "se": se,
        "L": L,
        "not_suffix_only": bool(L > 0),
    }


def b2(q, p) -> dict:
    return forcing(q[32], q[4], p)


def b3(q, p, n_axial=6) -> dict:
    def c(x):
        return hws_oracle.circ_marginal(np.asarray(x, dtype=np.float64), n_axial)

    return forcing(c(q[32]), c(q[4]), c(p))


def load64(checkpoint) -> tuple:
    return c1_model.load_model64(checkpoint)


def activations(model64, inputs, site=hc.SITE, index=hc.INDEX, batch=1024) -> np.ndarray:
    if site == hc.SITE and int(index) == hc.INDEX:
        return c1_model.activations(model64, inputs, batch)
    out = []
    with torch.no_grad():
        for s in range(0, int(inputs.shape[0]), int(batch)):
            res = model64(inputs[s : s + int(batch)], return_hooks=(site,))
            out.append(res.hooks[site][:, int(index), :].to(torch.float64).numpy().copy())
            del res  # logits discarded unread
    return np.vstack(out)


def moments(proc, canon32) -> dict:
    return k4b_scores.oracle_moments(
        proc["T"], proc["E_canon_shared"], proc["pi"], np.asarray(canon32), proc["features"]
    )


def d4_rows(m) -> np.ndarray:
    return k4b_scores.phase_scores(k4b_scores.oracle_phase(m[32]), m[32], m[4])


def endpoints(ext, m) -> dict:
    a = k4b_scores.endpoint_arrays(ext.phase, ext.supported, m[32], m[4])
    return dict(
        a,
        phi=np.asarray(ext.phase, dtype=np.float64),
        supported=np.asarray(ext.supported, dtype=bool),
    )


def support(ext, R, a, m) -> dict:
    return k4b_scores.support_report(ext, R, a["r4n"], ext.phase, m[32], m[4], False)
