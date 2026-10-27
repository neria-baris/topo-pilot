"""HWS statistics: means, SEs, bounds, z constants, bootstrap, E5, nulls (API.md §2).

Protocol §5.3 items 1-5 (nominal screening bounds, widened bound, S3 decision bound, null rule),
§2.5 (E5 legibility), §2.3 (Pinsker count, entropy-difference cross-checks).
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import math
from fractions import Fraction
from statistics import NormalDist

import hws_worlds as hw
import c1_means
import k4b_scores
import numpy as np
import scores

_Z = hw.CONTRACT["z"]


def z_of(alpha: Fraction) -> float:
    return NormalDist().inv_cdf(float(1 - Fraction(alpha)))


Z1 = z_of(Fraction(_Z["Z1"]["alpha"]))
ZW = z_of(Fraction(_Z["ZW"]["alpha"]))
Z3 = z_of(Fraction(_Z["Z3"]["alpha"]))
ZNULL = z_of(Fraction(_Z["ZNULL"]["alpha"]))
Z975 = z_of(Fraction(_Z["central95"]["alpha_each_side"]))
ALPHA_F = Fraction(hw.CONTRACT["bootstrap"]["alpha_f"])
DRAWS = int(hw.CONTRACT["bootstrap"]["draws"])
RANK_F = c1_means.rank_for(ALPHA_F, DRAWS)
if RANK_F != int(hw.CONTRACT["bootstrap"]["rank_alpha_f"]):
    raise hw.HwsStop("FAIL_TECHNICAL/NUMERICAL", f"rank_for(1/320, 5000) = {RANK_F} != 16")


def _finite(x) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float64)
    if arr.ndim != 1 or arr.size < 2 or not np.all(np.isfinite(arr)):
        raise hw.HwsStop("FAIL_TECHNICAL/NUMERICAL", f"summary: need finite 1-d n >= 2 {arr.shape}")
    return arr


def summary(x) -> dict:
    arr = _finite(x)
    n = int(arr.shape[0])
    sd = float(np.std(arr, ddof=1))
    return {"n": n, "mean": float(c1_means.tree_mean(arr)), "sd": sd, "se": sd / math.sqrt(n)}


def screen_bounds(x) -> dict:
    s = summary(x)
    m, se = s["mean"], s["se"]
    return dict(s, L1=m - Z1 * se, U1=m + Z1 * se, Lw=m - ZW * se, Uw=m + ZW * se)


def s3_bounds(x, boot) -> dict:
    b = screen_bounds(x)
    boot = np.asarray(boot, dtype=np.float64)
    l3n = b["mean"] - Z3 * b["se"]
    l3b = c1_means.quantile_with_rank(boot, ALPHA_F)[0]
    lo = c1_means.quantile_with_rank(boot, Fraction(1, 40))[0]
    hi = c1_means.quantile_with_rank(boot, Fraction(39, 40))[0]
    return dict(b, L3_normal=l3n, L3_boot=l3b, L3=min(l3n, l3b), central95_boot=[lo, hi])


def normal95(s) -> tuple:
    return s["mean"] - Z975 * s["se"], s["mean"] + Z975 * s["se"]


def bootstrap(arrays: dict, seed: int) -> dict:
    return c1_means.bootstrap_means(arrays, int(seed), DRAWS)


def null_z(x) -> dict:
    s = summary(x)
    if s["se"] == 0.0:
        z = 0.0 if s["mean"] == 0.0 else math.inf
    else:
        z = abs(s["mean"]) / s["se"]
    return {"mean": s["mean"], "se": s["se"], "z": z, "exceeds": bool(z > ZNULL)}


def e5(m32) -> dict:
    """§2.5 on point values (choice 11): 95 % norm >= 0.2, 12 bins >= n/64, resultant <= 0.30."""
    m = np.asarray(m32, dtype=np.float64)
    n = int(m.shape[0])
    norm = np.sqrt(np.sum(m * m, axis=1))
    phase = k4b_scores.oracle_phase(m)
    bins = np.minimum(np.floor(phase * 12 / (2 * np.pi)).astype(np.int64), 11)
    counts = np.bincount(bins, minlength=12)
    u = scores.unit_vectors(phase)
    mean_u = c1_means.tree_mean(np.asarray(u, dtype=np.float64).T)
    resultant = math.hypot(float(mean_u[0]), float(mean_u[1]))
    n_ok = int(np.count_nonzero(norm >= 0.2))
    ok = 100 * n_ok >= 95 * n and 64 * int(counts.min()) >= n and resultant <= 0.30
    return {
        "frac_norm_ge_0.2": n_ok / n,
        "bin_counts": [int(c) for c in counts],
        "min_bin": int(counts.min()),
        "resultant": resultant,
        "pass": bool(ok),
    }


def pinsker_violations(slack, tol=1e-12) -> int:
    return int(np.count_nonzero(np.asarray(slack, dtype=np.float64) < -tol))


def entropy_diff(ha, hb) -> dict:
    return summary(np.asarray(ha, dtype=np.float64) - np.asarray(hb, dtype=np.float64))
