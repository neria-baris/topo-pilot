"""K4b oracle moments, X-/X+ assembly, control and descriptive phases (API.md §4).

Protocol §1.4 (every row kept: supported rows score the extension phase, unsupported rows take
the bounds -/+ ||r4||), §9 (controls), §10 (support reporting; sealed form, §7.5).
"""

from __future__ import annotations

import c1_means
import k4b_config
import numpy as np
import scores
from c1_records import C1GateFailure
from k4b_config import KS

TWO_PI = 2.0 * np.pi
NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"


def oracle_moments(T, E_canon, pi, canon32, features) -> dict:
    import oracle_profile

    means = oracle_profile.posterior_means(T, E_canon, pi, np.asarray(canon32), KS, features)
    return {int(K): np.asarray(means[K], dtype=np.float64) for K in KS}


def wrap_phase(phi) -> np.ndarray:
    phi = np.asarray(phi, dtype=np.float64)
    if not np.all(np.isfinite(phi)):
        raise C1GateFailure(NUMERICAL, "non-finite phase")
    out = np.mod(phi, TWO_PI)
    return np.where(out >= TWO_PI, 0.0, out)


def vector_phase(m) -> np.ndarray:
    m = np.asarray(m, dtype=np.float64)
    zero = (m[:, 0] == 0.0) & (m[:, 1] == 0.0)
    return np.where(zero, 0.0, wrap_phase(np.arctan2(m[:, 1], m[:, 0])))


def m4_phase(m4) -> np.ndarray:
    return vector_phase(m4)


def oracle_phase(m32) -> np.ndarray:
    return vector_phase(m32)


def sha_phase(canon32) -> np.ndarray:
    c = np.asarray(canon32, dtype=np.uint8)
    return wrap_phase(np.array([scores.sha256_phase(row[28:32]) for row in c], dtype=np.float64))


def phase_scores(phi, m32, mK) -> np.ndarray:
    return scores.scores(scores.unit_vectors(phi), m32, mK)


def _bounded(phi, supported, m32, mK) -> dict:
    sup = np.asarray(supported, dtype=bool)
    r = scores.r4_norms(m32, mK)
    x = phase_scores(np.where(sup, phi, 0.0), m32, mK)
    xm = np.where(sup, x, -r)
    xp = np.where(sup, x, r)
    if not np.all(xm <= xp):
        raise C1GateFailure(NUMERICAL, "X- > X+ on some row")
    return {"X_minus": xm, "X_plus": xp, "r4n": r}


def endpoint_arrays(phi, supported, m32, m4) -> dict:
    """§1.4: X- = X+ = u(phi).r4 on supported rows; -/+ ||r4|| on unsupported rows."""
    return _bounded(phi, supported, m32, m4)


def secondary_arrays(phi, supported, m, K) -> dict:
    return _bounded(phi, supported, m[32], m[K])


def naive_scores(phi, m32, m4) -> np.ndarray:
    return phase_scores(phi, m32, m4)


def support_reasons(ext, R) -> dict:
    sup = np.asarray(ext.supported, dtype=bool)
    low = np.asarray(ext.resultant) < 0.2
    far = np.asarray(ext.eighth_distance) > R
    un = ~sup
    return {"resultant_only": int(np.sum(un & low & ~far)), "distance_only": int(np.sum(un & far
            & ~low)), "both": int(np.sum(un & low & far)),
            "duplicate_queries": int(np.sum(np.asarray(ext.duplicate, dtype=bool)))}


def _summary(x) -> dict:
    x = np.asarray(x, dtype=np.float64)
    q = np.quantile(x, [0.0, 0.25, 0.5, 0.75, 1.0]) if x.size else [None] * 5
    return dict(zip(("min", "q25", "median", "q75", "max"), (None if v is None else float(v)
                                                              for v in q)))


def _mean(x) -> float | None:
    x = np.asarray(x, dtype=np.float64)
    return float(c1_means.tree_mean(x)) if x.size else None


def support_report(ext, R, r4n, phi, m32, m4, sealed) -> dict:
    """§10 support report; the sealed form omits the supported contribution (§7.5)."""
    A = np.asarray(ext.supported, dtype=bool)
    r4n = np.asarray(r4n, dtype=np.float64)
    missing = _mean((1.0 - A) * r4n)
    rep = {"n": int(A.size), "n_supported": int(A.sum()), "fraction": float(A.mean()),
           "reasons": support_reasons(ext, R), "resultant_summary": _summary(ext.resultant),
           "d8_summary": _summary(ext.eighth_distance), "missing_mass": missing,
           "width": 2.0 * missing, "mean_r4_supported": _mean(r4n[A]),
           "mean_r4_unsupported": _mean(r4n[~A])}
    if not sealed:
        x = phase_scores(phi, m32, m4)
        rep["supported_contribution"] = _mean(A * x)
        rep["supported_conditional_mean"] = _mean(x[A])
    return rep


def _one(phi, m32, m4) -> dict:
    return {"X": phase_scores(phi, m32, m4), "phi": phi}


def control_arrays(m, canon32, ext, init_ext, decoders) -> dict:
    """API.md §14.2: the eight control families (two-sided: init, delta1, delta2)."""
    import k4b_decoder  # k4b_decoder imports this module

    m32, m4 = m[32], m[4]

    def two(e, K):
        if isinstance(e, dict):
            return {"unavailable": str(e.get("unavailable", e.get("reason", "unavailable")))}
        return dict(secondary_arrays(e.phase, e.supported, m, K), phi=e.phase,
                    supported=np.asarray(e.supported, dtype=bool))

    def dec(d):
        if d.get("status") != "AVAILABLE":
            return {"unavailable": str(d.get("reason", ""))}
        return _one(k4b_decoder.predict_phase(d, canon32), m32, m4)

    return {"m4_phase": {"all": _one(m4_phase(m4), m32, m4)},
            "sha_suffix": {"all": _one(sha_phase(canon32), m32, m4)},
            "init": {j: two(init_ext[j], 4) for j in k4b_config.MODELS},
            "decoder": {j: dec(decoders[j]) for j in k4b_config.MODELS},
            "delta1": {j: two(ext[j], 1) for j in k4b_config.MODELS},
            "delta2": {j: two(ext[j], 2) for j in k4b_config.MODELS},
            "delta4_orc": {"all": _one(oracle_phase(m32), m32, m4)},
            "naive": {j: {"X": naive_scores(ext[j].phase, m32, m4),
                          "phi": ext[j].phase} for j in k4b_config.MODELS}}


def _radius(R, j) -> float:
    return float(R[j]) if isinstance(R, dict) else float(R)


def support_entries(ext, R, arrays, m) -> dict:
    return {j: support_report(ext[j], _radius(R, j), arrays[j]["r4n"], ext[j].phase,
                                         m[32], m[4], False) for j in k4b_config.MODELS}
