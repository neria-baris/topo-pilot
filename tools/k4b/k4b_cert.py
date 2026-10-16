"""K4b references, moment check, row bounds, Lemma N, B_num, F and guards (API.md §7).

Protocol §5 (numerics): every certified bound, margin and comparison is an exact Fraction; a
float enters only as Fraction(float(x)). Row bounds reuse error_bound unchanged; mean-level
constants reuse c1_bounds/c1_means unchanged.
"""

from __future__ import annotations

import math
from fractions import Fraction

import c1_bounds
import c1_means
import error_bound
import k4b_config
import numpy as np
from c1_records import C1GateFailure
from k4b_config import CAP, FLOOR, KS, P2_MAX_ABS

MOMENT_TOL = error_bound.MOMENT_TOL_EXACT
NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"
D_LEMMA_N = 10**80
S_ENVELOPE = 144
CONTROL_K = {"init": 4, "delta1": 1, "delta2": 2}  # two-sided controls


def _fr(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x) if isinstance(x, int) \
        else Fraction(float(x)) if isinstance(x, (float, np.floating)) else Fraction(x)


def envelopes(Ks=KS) -> dict:
    return {int(K): error_bound.moment_envelope(error_bound.posterior_envelope(K, S_ENVELOPE),
                                                S_ENVELOPE) for K in Ks}


def references(T, E, pi, coords, canon32, cache=None) -> list:
    return error_bound.reference_moments(T, E, pi, coords, canon32, Ks=KS, cache=cache)


def moment_check(m_hat, refs) -> dict:
    """|Fraction(float(m_hat)) - Fraction(M~)| <= MOMENT_TOL for every row, K and coordinate."""
    max_gap, n_fail = Fraction(0), 0
    for K, arr in m_hat.items():
        arr = np.asarray(arr, dtype=np.float64)
        for i, ref in enumerate(refs):
            M = ref[int(K)]
            gap = max(abs(Fraction(float(arr[i, c])) - Fraction(M[c])) for c in (0, 1))
            max_gap = max(max_gap, gap)
            n_fail += gap > MOMENT_TOL
    return {"ok": n_fail == 0, "max_gap": max_gap, "n_fail": int(n_fail)}


def isqrt_bracket(s, D=D_LEMMA_N) -> int:
    """k with k/D <= sqrt(s) < (k+1)/D, for a non-negative Fraction s = a/b."""
    s = _fr(s)
    if s < 0:
        raise C1GateFailure(NUMERICAL, "isqrt_bracket of a negative value")
    return math.isqrt(s.numerator * D * D // s.denominator)


def norm_bound(n_hat, M32, M4, eps4, eps32, D=D_LEMMA_N) -> Fraction:
    """Lemma N: B_N = max(|n - k/D|, |n - (k+1)/D|) + (3/2)(eps_K + eps32)."""
    rx = Fraction(M32[0]) - Fraction(M4[0])
    ry = Fraction(M32[1]) - Fraction(M4[1])
    k = isqrt_bracket(rx * rx + ry * ry, D)
    n = Fraction(float(n_hat))
    lo, hi = Fraction(k, D), Fraction(k + 1, D)
    return max(abs(n - lo), abs(n - hi)) + Fraction(3, 2) * (_fr(eps4) + _fr(eps32))


def phase_bound(x_hat, phi, MK, M32, epsK, eps32) -> Fraction:
    return _fr(error_bound.row_bound(x_hat, phi, MK, M32, epsK, eps32)["B"])


def endpoint_bounds(arrays, supported, phi, refs, eps, K=4) -> dict:
    """Supported rows: phase bound; unsupported rows (X-/+ = -/+ n_hat): Lemma N; B4: Lemma N."""
    sup = np.asarray(supported, dtype=bool)
    out = {"B_minus": [], "B_plus": [], "B_norm": []}
    for i, ref in enumerate(refs):
        MK, M32 = ref[K], ref[32]
        bn = norm_bound(arrays["r4n"][i], M32, MK, eps[K], eps[32])
        out["B_norm"].append(bn)
        if sup[i]:
            for side, key in (("B_minus", "X_minus"), ("B_plus", "X_plus")):
                out[side].append(phase_bound(float(arrays[key][i]), float(phi[i]), MK, M32,
                                             eps[K], eps[32]))
        else:
            out["B_minus"].append(bn)
            out["B_plus"].append(bn)
    out["max"] = {"minus": max(out["B_minus"], default=Fraction(0)),
                  "plus": max(out["B_plus"], default=Fraction(0)),
                  "norm": max(out["B_norm"], default=Fraction(0))}
    return out


def control_bounds(x, phi, refs, eps, K=4) -> dict:
    B = [phase_bound(float(x[i]), float(phi[i]), ref[K], ref[32], eps[K], eps[32])
         for i, ref in enumerate(refs)]
    mx = max(B, default=Fraction(0))
    return {"B": B, "max": mx, "certified": cap_ok(mx)}


def cap_ok(max_b) -> bool:
    return _fr(max_b) <= CAP


def p2_ok(X) -> bool:
    X = np.asarray(X, dtype=np.float64)
    return bool(np.all(np.isfinite(X)) and np.all(np.abs(X) <= P2_MAX_ABS))


def certify(primary: dict, controls: dict) -> dict:
    """primary/controls: {name: {"X": array, "max_B": Fraction}}. Primary defects raise
    FAIL_TECHNICAL/NUMERICAL; a primary max above CAP -> INCONCLUSIVE/NUMERICAL. Controls are
    certified and reported only ("uncertified" above CAP)."""
    max_B, certified, status = {}, {}, "PASS"
    for name, entry in primary.items():
        if not p2_ok(entry["X"]):
            raise C1GateFailure(NUMERICAL, f"{name}: non-finite or |X| > {P2_MAX_ABS}")
        max_B[name] = _fr(entry["max_B"])
        certified[name] = cap_ok(max_B[name])
        if not certified[name]:
            status = "INCONCLUSIVE/NUMERICAL"
    for name, entry in controls.items():
        max_B[name] = _fr(entry["max_B"])
        certified[name] = cap_ok(max_B[name]) and p2_ok(entry["X"])
    return {"status": status, "max_B": max_B, "certified": certified,
            "labels": {n: "uncertified" for n in controls if not certified[n]}}


def b_num(max_b, max_abs, n) -> Fraction:
    return c1_bounds.B_constant(_fr(max_b), max_abs, n)


def margin(B_num, Z_bound) -> Fraction:
    return max(_fr(B_num), FLOOR) + _fr(Z_bound)


def F_plan(Z_bound) -> Fraction:
    """§7.1: max(B_constant(1e-4, 4, 12288), FLOOR) + Z_bound."""
    return max(c1_bounds.B_constant(CAP, P2_MAX_ABS, k4b_config.LADDER[-1]), FLOOR) \
        + _fr(Z_bound)


def b4_guard(r4n, B_norm_max, Z_bound, seed, n) -> dict:
    r4n = np.asarray(r4n, dtype=np.float64)
    B_H = b_num(B_norm_max, float(np.max(r4n)), n)
    draws = c1_means.bootstrap_means({"r4n": r4n}, seed)["r4n"]
    lower, k = c1_means.quantile_with_rank(draws, 0.05)
    Z = _fr(Z_bound)
    return {"lower": lower, "rank": k, "B_H": B_H, "Z_bound": Z,
            "status": c1_bounds.guard_H5(lower, B_H + Z),
            "point": float(c1_means.tree_mean(r4n))}


def transport_bound(T, E, pi, coords) -> dict:
    import process_law

    res = process_law.process_law_bound(T, E, pi, coords)
    if res.get("status") != "BOUNDED":
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"process law: {res.get('status')}")
    return dict(res, Z_bound=_fr(res["Z_bound"]))


def control_bounds_all(controls, refs, eps) -> dict:
    """Row certificates of every control entry (reported, never gating; R22 per side)."""
    out = {}
    for name, entries in controls.items():
        out[name] = {}
        for key, e in entries.items():
            if "unavailable" in e:
                out[name][key] = dict(e)
            elif name in CONTROL_K:
                b = endpoint_bounds(e, e["supported"], e["phi"], refs, eps,
                                             CONTROL_K[name])["max"]
                mx = max(b.values())
                out[name][key] = {"max_B": mx, "max_B_minus": b["minus"], "max_B_plus": b["plus"],
                                  "certified": cap_ok(mx) and p2_ok(
                                      e["X_minus"]) and p2_ok(e["X_plus"])}
            else:
                mx = control_bounds(e["X"], e["phi"], refs, eps, K=4)["max"]
                out[name][key] = {"max_B": mx, "certified": cap_ok(mx)
                                  and p2_ok(e["X"])}
    return out
