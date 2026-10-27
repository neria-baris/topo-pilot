"""HWSB law enclosure for non-terminating logits (API.md §5; protocol §4 B8a, RC-1, OPEN-3).

The 60-digit enclosure of `process_law.softmax_enclosure` assumes every logit converts to a
Decimal exactly. At sigma = 7/4 the logits -d^2/(2 sigma^2) have the factor 49 in their
denominator and do not terminate. Here each logit q is rounded once to qt (round half even,
60 digits), delta = max |qt - q| is computed exactly, and the returned lo/hi are widened by
(1 - 2 delta). Proof: ENCLOSURE_PROOF.md. When every logit terminates, delta = 0 and every
returned object equals the original enclosure. `process_law_bound` itself is unchanged; it is
called inside `bound_law`, which rebinds LAW and `softmax_enclosure` and restores them.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import contextlib
import decimal
from decimal import Decimal
from fractions import Fraction

import error_bound
import process_law
from errors import Invalid

DIGITS = 60
CHECK_DIGITS = 200
SLACK = Fraction(1, 10**190)


def centres() -> list:
    k = int(process_law.LAW["grid"])
    return [(Fraction(1, 2) + 2 * a, Fraction(1, 2) + 2 * b) for a in range(k) for b in range(k)]


def exact_logits(states) -> list:
    """q[s][j] = -d^2/(2 sigma^2) as exact Fractions (process_law.py:112-115)."""
    period, sigma = process_law.LAW["x_period"], Fraction(process_law.LAW["sigma"])
    scale = 2 * sigma**2
    cen = centres()
    rows = []
    for x, y in states:
        row = []
        for cx, cy in cen:
            dx = abs(Fraction(x) - cx) % period
            d2 = min(dx, period - dx) ** 2 + (Fraction(y) - cy) ** 2
            row.append(-d2 / scale)
        rows.append(row)
    return rows


def rounded_logits(q_rows, digits=DIGITS) -> list:
    with decimal.localcontext(error_bound.trapping_context(int(digits))):
        return [[Decimal(q.numerator) / Decimal(q.denominator) for q in row] for row in q_rows]


def _delta(q_rows, qt_rows, digits) -> dict:
    delta, q_max, n_inexact = Fraction(0), Fraction(0), 0
    for qr, tr in zip(q_rows, qt_rows):
        for q, t in zip(qr, tr):
            gap = abs(Fraction(t) - q)
            n_inexact += gap != 0
            delta = max(delta, gap)
            q_max = max(q_max, abs(q))
    u = error_bound.u_digits(int(digits))
    return {"delta": delta, "Q_max": q_max, "u": u, "bound": u * q_max, "n_inexact": n_inexact}


def rounding_delta(states, digits=DIGITS) -> dict:
    q = exact_logits(states)
    return _delta(q, rounded_logits(q, digits), digits)


def softmax_enclosure_rounded(states, digits=DIGITS):
    """(E_dec, lo, hi): every exact E*[s][j] lies in [E_dec/hi, E_dec/lo] (ENCLOSURE_PROOF)."""
    if int(digits) != DIGITS:
        raise Invalid("softmax enclosure is proved for 60 digits only")
    q = exact_logits(states)
    qt = rounded_logits(q, DIGITS)
    r = _delta(q, qt, DIGITS)
    delta = r["delta"]
    if not (delta <= r["bound"] and 2 * delta < 1):
        raise hc.HwsbStop(
            "FAIL_TECHNICAL/LAW_BOUND",
            f"rounding delta {float(delta)!r} outside u*Q_max = {float(r['bound'])!r}",
        )
    E_dec = []
    with decimal.localcontext(error_bound.trapping_context(DIGITS)):
        for row in qt:
            num = [lg.exp() for lg in row]
            den = sum(num, Decimal(0))
            E_dec.append([v / den for v in num])
    u = error_bound.u_digits(DIGITS)
    n_add = len(centres())
    lo = (1 - 2 * u) * (1 - u) / ((1 + 2 * u) * (1 + u) ** n_add)
    hi = (1 + 2 * u) * (1 + u) / ((1 - 2 * u) * (1 - u) ** n_add)
    return E_dec, lo * (1 - 2 * delta), hi / (1 - 2 * delta)


@contextlib.contextmanager
def bound_law(sigma, neighbour):
    """Bind LAW sigma/neighbour and the rounded enclosure; restore all three in finally."""
    law = process_law.LAW
    saved = (law["sigma"], law["neighbour"], process_law.softmax_enclosure)
    try:
        law["sigma"], law["neighbour"] = Fraction(sigma), Fraction(neighbour)
        process_law.softmax_enclosure = softmax_enclosure_rounded
        yield
    finally:
        law["sigma"], law["neighbour"] = saved[0], saved[1]
        process_law.softmax_enclosure = saved[2]


def _exact(rep):
    if rep is None:
        return None
    if isinstance(rep, dict):
        rep = rep.get("exact_upper")
    return Fraction(rep) if isinstance(rep, (str, Fraction, int)) else None


def law_bound(T, E, pi, coords, sigma=hc.SIGMA, neighbour=hc.NEIGHBOUR) -> dict:
    """process_law_bound (unchanged) under the rounded enclosure; exceptions propagate."""
    with bound_law(sigma, neighbour):
        res = process_law.process_law_bound(T, E, pi, coords)
        r = None
        if res.get("status") == "BOUNDED":
            r = rounding_delta(process_law.lattice_states(coords))
    bounded = res.get("status") == "BOUNDED"
    return {
        "status": res.get("status"),
        "Z_bound": _exact(res.get("Z_bound")) if bounded else None,
        "kappa": _exact(res.get("kappa")) if bounded else None,
        "delta": r["delta"] if r else None,
        "Q_max": r["Q_max"] if r else None,
        "u": r["u"] if r else None,
        "n_inexact": r["n_inexact"] if r else None,
        "sigma": Fraction(sigma),
        "neighbour": Fraction(neighbour),
        "reason": res.get("reason"),
        "raw": res,
    }


def reference_entry(q_row, j, digits=CHECK_DIGITS) -> Decimal:
    """Independent softmax entry from the exact logits at `digits` digits."""
    ctx = decimal.Context(
        prec=int(digits), rounding=decimal.ROUND_HALF_EVEN, Emin=-999999, Emax=999999
    )
    with decimal.localcontext(ctx):
        ex = [(Decimal(q.numerator) / Decimal(q.denominator)).exp() for q in q_row]
        return ex[int(j)] / sum(ex, Decimal(0))


def decimal_check(states, enclosure, entries, digits=CHECK_DIGITS) -> dict:
    E_dec, lo, hi = enclosure
    entries = list(entries)
    q = exact_logits(states)
    n_fail, worst = 0, {"s": None, "j": None, "excess": "0"}
    best = Fraction(0)
    for s, j in entries:
        ref = Fraction(reference_entry(q[s], j, digits))
        e = Fraction(E_dec[s][j])
        lower, upper = e / Fraction(hi) - SLACK, e / Fraction(lo) + SLACK
        excess = max(lower - ref, ref - upper)
        if excess > 0:
            n_fail += 1
            if excess > best:
                best = excess
                worst = {"s": int(s), "j": int(j), "excess": str(excess)}
    return {"n": len(entries), "n_fail": n_fail, "worst": worst, "pass": n_fail == 0}
