"""Process-law bound Z_bound (ERROR_BOUND.md v2.2 sections 6 and 9; API.md spec v2.4 item 4).

Exact rationals and a trapping 60-digit Decimal context only; stored float arrays are read as
exact reals. Q is the IDEALIZED sampling law (independent uniform 53-bit draws across sampler
calls and trajectories, independent panel assignment): Z_bound covers the parameter, CDF and
grid discrepancy under that idealization, never PRNG bias or correlation, and is never an
exact zero for fixed saved data. It is reported beside the controls and is not a gate.

Reported Fractions are rounded UP to the 1e-40 grid (valid upper bounds, finite strings); kappa
is rounded up before the power, which only enlarges rho.
"""

from __future__ import annotations

import decimal
import importlib.util
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
from errors import Invalid

LAW = {
    "dims": (12, 12),
    "x_period": 12,
    "neighbour": Fraction(1, 5),
    "grid": 6,
    "sigma": Fraction(5, 4),
    "L": 32,
    "draws": {"pi": 1, "emission": 32, "transition": 31},
}
GRID = 2**53
REPORT_GRID = 10**40
SAMPLER_FILE = Path(__file__).resolve().parents[2] / "src" / "topo_pilot" / "dataset" / "sampler.py"
_SAMPLER = None


class Mismatch(Exception):
    """A documented-law condition fails: the bound is UNAVAILABLE (not a defect)."""


def lattice_states(coords) -> list[tuple[int, int]]:
    c = np.asarray(coords, dtype=np.float64)
    nx, ny = LAW["dims"]
    if c.ndim != 2 or c.shape[0] != nx * ny or c.shape[1] < 2:
        raise Mismatch(f"coords shape {c.shape} is not the documented {nx}x{ny} lattice")
    states = []
    for s in range(nx * ny):
        if (c[s, 0], c[s, 1]) != (float(s // ny), float(s % ny)):
            raise Mismatch(f"coords of state {s} are not (s // {ny}, s % {ny})")
        states.append((s // ny, s % ny))
    return states


def _neighbours(states, s, t) -> bool:
    (x1, y1), (x2, y2) = states[s], states[t]
    dx = (x1 - x2) % LAW["x_period"]
    return (y1 == y2 and dx in (1, LAW["x_period"] - 1)) or (x1 == x2 and abs(y1 - y2) == 1)


def documented_transition(states) -> list[list[Fraction]]:
    n, w = len(states), LAW["neighbour"]
    T = [[Fraction(0)] * n for _ in range(n)]
    for s in range(n):
        deg = 0
        for t in range(n):
            if t != s and _neighbours(states, s, t):
                T[s][t] = w
                deg += 1
        T[s][s] = 1 - deg * w
    return T


def ideal_identities(T_star, S) -> None:
    n = len(T_star)
    if n != S or any(len(row) != n for row in T_star):
        raise Mismatch("T* is not S x S")
    pi = Fraction(1, S)
    for s in range(n):
        if sum(T_star[s]) != 1 or any(not 0 <= v <= 1 for v in T_star[s]):
            raise Mismatch(f"T* row {s} is not a probability row")
        if any(T_star[s][t] != T_star[t][s] for t in range(n)):
            raise Mismatch("T* is not symmetric")
    for t in range(n):
        if sum(pi * T_star[s][t] for s in range(n)) != pi:
            raise Mismatch("pi* T* != pi*")


def _ctx() -> decimal.Context:
    import error_bound

    return error_bound.trapping_context(60)


def softmax_enclosure(states, digits=60):
    """(E_dec, lo, hi): every exact E*[s][j] lies in [E_dec/hi, E_dec/lo] (positive)."""
    from error_bound import u_digits

    if int(digits) != 60:
        raise Invalid("softmax enclosure is proved for 60 digits only")
    k, period = LAW["grid"], LAW["x_period"]
    centres = [(Fraction(1, 2) + 2 * a, Fraction(1, 2) + 2 * b) for a in range(k) for b in range(k)]
    scale = 2 * LAW["sigma"] ** 2
    exact = _ctx().copy()
    exact.traps[decimal.Inexact] = True
    E_dec = []
    for x, y in states:
        logits = []
        for cx, cy in centres:
            dx = abs(Fraction(x) - cx) % period
            d2 = min(dx, period - dx) ** 2 + (Fraction(y) - cy) ** 2
            q = -d2 / scale
            with decimal.localcontext(exact):
                logits.append(Decimal(q.numerator) / Decimal(q.denominator))
        with decimal.localcontext(_ctx()):
            num = [lg.exp() for lg in logits]
            den = sum(num, Decimal(0))
            E_dec.append([v / den for v in num])
    u = u_digits(60)
    n_add = len(centres)
    lo = (1 - 2 * u) * (1 - u) / ((1 + 2 * u) * (1 + u) ** n_add)
    hi = (1 + 2 * u) * (1 + u) / ((1 - 2 * u) * (1 - u) ** n_add)
    return E_dec, lo, hi


def _sampler():
    global _SAMPLER
    if _SAMPLER is None:
        spec = importlib.util.spec_from_file_location("x4c_frozen_dataset_sampler", SAMPLER_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _SAMPLER = module
    return _SAMPLER


def sampler_cdf(P) -> np.ndarray:
    """The ACTUAL sampler thresholds (_cumulative_rows of the frozen dataset/sampler.py)."""
    return _sampler()._cumulative_rows(np.asarray(P, dtype=np.float64))


def _G(x: Fraction) -> int:
    return min(max(math.ceil(x * GRID), 0), GRID)


def threshold_law(c_row) -> dict:
    """Exact law of j = min(#{i: c'_i <= u}, V-1) for u on the 2^-53 grid, c' clamped to [0, 1]."""
    clamped = [min(max(Fraction(float(c)), Fraction(0)), Fraction(1)) for c in c_row]
    V = len(clamped)
    s = sorted(clamped)
    counts = [_G(s[0])] + [_G(s[j]) - _G(s[j - 1]) for j in range(1, V)] + [GRID - _G(s[V - 1])]
    q = [Fraction(c, GRID) for c in counts[: V - 1]] + [Fraction(counts[V - 1] + counts[V], GRID)]
    monotone = all(clamped[j] <= clamped[j + 1] for j in range(V - 1)) and clamped[-1] == 1
    return {"q": q, "clamped": clamped, "monotone": monotone}


def row_tv(p_hat_row, dev_row, c_row) -> dict:
    law = threshold_law(c_row)
    p = [Fraction(float(v)) for v in p_hat_row]
    grid = sum(abs(qj - pj) + d for qj, pj, d in zip(law["q"], p, dev_row)) / 2
    documented = None
    if law["monotone"]:
        e, partial = [], Fraction(0)
        for cj, pj in zip(law["clamped"], p):
            partial += pj
            e.append(cj - partial)
        prev = [Fraction(0)] + e[:-1]
        half_ulp = Fraction(1, GRID)
        documented = sum(abs(a) + abs(b) + half_ulp + d for a, b, d in zip(e, prev, dev_row)) / 2
    return {"grid": grid, "documented": documented}


def _up(x: Fraction) -> Fraction:
    return Fraction(math.ceil(x * REPORT_GRID), REPORT_GRID)


def _report(x):
    return None if x is None else {"exact_upper": str(x), "float": float(x)}


def _arrays(T, E, pi, coords):
    arrs = [np.asarray(a, dtype=np.float64) for a in (T, E, pi, coords)]
    T, E, pi, coords = arrs
    S = pi.shape[0] if pi.ndim == 1 else -1
    shapes_ok = T.shape == (S, S) and E.ndim == 2 and E.shape[0] == S and coords.shape[:1] == (S,)
    if not shapes_ok or not all(np.isfinite(a).all() for a in arrs):
        raise Invalid("process law needs finite T [S,S], E [S,V], pi [S], coords [S,d]")
    return T, E, pi, coords


def _kappas(T, E, pi, T_star, E_dec, lo, hi):
    S = len(T_star)
    kT, devT = Fraction(0), []
    for s in range(S):
        row = []
        for t in range(S):
            th, ts = Fraction(float(T[s, t])), T_star[s][t]
            if (th > 0) != (ts > 0) or th < 0:
                raise Mismatch(f"T zero support differs from T* at ({s}, {t})")
            row.append(abs(th - ts))
            if ts > 0:
                kT = max(kT, abs(th - ts) / ts)
        devT.append(row)
    if np.any(E <= 0) or np.any(pi <= 0):
        raise Mismatch("a stored E or pi entry is not strictly positive")
    kE, devE = Fraction(0), []
    for s in range(S):
        row = []
        for j in range(E.shape[1]):
            ed, eh = Fraction(E_dec[s][j]), Fraction(float(E[s, j]))
            dev = max(abs(eh - ed / hi), abs(eh - ed / lo))
            row.append(dev)
            kE = max(kE, dev / (ed / hi))
        devE.append(row)
    pi_star = Fraction(1, S)
    devP = [abs(Fraction(float(v)) - pi_star) for v in pi]
    kP = max(devP) * S
    return {"T": kT, "E": kE, "pi": kP}, devT, devE, devP


def process_law_bound(T, E, pi, coords) -> dict:
    T, E, pi, coords = _arrays(T, E, pi, coords)
    try:
        states = lattice_states(coords)
        if E.shape[1] != LAW["grid"] ** 2:
            raise Mismatch(f"V = {E.shape[1]} is not {LAW['grid'] ** 2}")
        T_star = documented_transition(states)
        ideal_identities(T_star, len(states))
        E_dec, lo, hi = softmax_enclosure(states)
        kap, devT, devE, devP = _kappas(T, E, pi, T_star, E_dec, lo, hi)
        kappa = max(kap.values())
        if kappa >= 1:
            raise Mismatch(f"kappa {float(kappa)} >= 1")
        tv_pi = row_tv(pi, devP, sampler_cdf(pi[None, :])[0])
        cum_E, cum_T = sampler_cdf(E), sampler_cdf(T)
        tvE = [row_tv(E[s], devE[s], cum_E[s]) for s in range(len(states))]
        tvT = [row_tv(T[s], devT[s], cum_T[s]) for s in range(len(states))]
    except Mismatch as exc:
        return {"status": "UNAVAILABLE", "reason": str(exc), "claim": "no process-law bound"}
    d = LAW["draws"]
    k_up = _up(kappa)
    rho_minus_1 = _up(((1 + k_up) / (1 - k_up)) ** (2 * LAW["L"] + 1) - 1)
    tv_E, tv_T = max(r["grid"] for r in tvE), max(r["grid"] for r in tvT)
    TV = _up(tv_pi["grid"] + d["emission"] * tv_E + d["transition"] * tv_T)
    docs = [tv_pi["documented"]] + [r["documented"] for r in tvE + tvT]
    TV_doc = None
    if all(v is not None for v in docs):
        TV_doc = _up(
            tv_pi["documented"]
            + d["emission"] * max(r["documented"] for r in tvE)
            + d["transition"] * max(r["documented"] for r in tvT)
        )
    return {
        "status": "BOUNDED",
        "kappa_T": _report(_up(kap["T"])),
        "kappa_E": _report(_up(kap["E"])),
        "kappa_pi": _report(_up(kap["pi"])),
        "kappa": _report(k_up),
        "rho_minus_1": _report(rho_minus_1),
        "tv_pi": _report(_up(tv_pi["grid"])),
        "tv_E_max": _report(_up(tv_E)),
        "tv_T_max": _report(_up(tv_T)),
        "TV": _report(TV),
        "TV_documented": _report(TV_doc),
        "Z_bound": _report(_up(2 * rho_minus_1 + 4 * TV)),
        "monotone": {
            "pi": threshold_law(sampler_cdf(pi[None, :])[0])["monotone"],
            "E": all(r["documented"] is not None for r in tvE),
            "T": all(r["documented"] is not None for r in tvT),
        },
        "claim": "bound on |E_Q[g·(M32-M4)]| under the IDEALIZED sampling law; not an exact "
        "zero for the fixed saved data",
    }
