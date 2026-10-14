"""Per-row numerical certificate (ERROR_BOUND.md v2.1; API.md error_bound.py).

The float pipeline is compared with an independent high-precision reference: the job-0014
`independent_reference.decimal_suffix_posterior`, reused UNCHANGED. A proven reference envelope
is added, and the bound is evaluated in exact rational arithmetic. There is no float64 error
model.
"""

from __future__ import annotations

import decimal
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests" / "oracle_profile"))

import independent_reference  # noqa: E402
from errors import Invalid, require_scoring  # noqa: E402

TAYLOR_N = 48
X_MAX = Fraction(6284, 1000)
TERM_SUM_BOUND = Fraction(270)
TAIL_LIMIT = Fraction(1, 10**75)
MOMENT_TOL = 1e-10
REF_DIGITS, FEATURE_DIGITS = 60, 80
_TRAPS = (
    decimal.Underflow,
    decimal.Subnormal,
    decimal.Overflow,
    decimal.Clamped,
    decimal.InvalidOperation,
    decimal.DivisionByZero,
)
_WATCHED_FLAGS = (decimal.Underflow, decimal.Subnormal, decimal.Overflow)


def u_digits(n) -> Fraction:
    return Fraction(1, 2) * Fraction(10) ** (1 - int(n))


def gamma_digits(k, n) -> Fraction:
    ku = int(k) * u_digits(n)
    if ku >= 1:
        raise ValueError("gamma undefined: k*u >= 1")
    return ku / (1 - ku)


def trapping_context(prec) -> decimal.Context:
    traps = {sig: True for sig in _TRAPS}
    traps.update({decimal.Inexact: False, decimal.Rounded: False, decimal.FloatOperation: False})
    return decimal.Context(
        prec=int(prec),
        rounding=decimal.ROUND_HALF_EVEN,
        Emin=-999999,
        Emax=999999,
        clamp=0,
        traps=traps,
        flags=[],
    )


def _factorial_fraction(x: Fraction, n: int) -> Fraction:
    return x**n / math.factorial(n)


def _verify_taylor_constants() -> tuple[Fraction, Fraction]:
    n = TAYLOR_N
    tail_cos = _factorial_fraction(X_MAX, 2 * n + 2)
    tail_sin = _factorial_fraction(X_MAX, 2 * n + 3)
    ratio_cos = X_MAX**2 / ((2 * n + 3) * (2 * n + 4))
    ratio_sin = X_MAX**2 / ((2 * n + 4) * (2 * n + 5))
    partial = sum(_factorial_fraction(X_MAX, k) for k in range(2 * n + 4))
    if not (
        tail_cos < TAIL_LIMIT
        and tail_sin < TAIL_LIMIT
        and ratio_cos < 1
        and ratio_sin < 1
        and partial + tail_cos <= 2 * TERM_SUM_BOUND
    ):
        raise Invalid("Taylor constants fail their exact verification")
    return tail_cos, tail_sin


_TAIL_COS, _TAIL_SIN = _verify_taylor_constants()


def _eps_v() -> Fraction:
    g3n, gn1 = (
        gamma_digits(3 * TAYLOR_N, FEATURE_DIGITS),
        gamma_digits(TAYLOR_N + 1, FEATURE_DIGITS),
    )
    return max(_TAIL_COS, _TAIL_SIN) + g3n * TERM_SUM_BOUND + gn1 * (1 + g3n) * TERM_SUM_BOUND


EPS_V = _eps_v()


def decimal_cos_sin(x: float, digits=FEATURE_DIGITS) -> tuple[Decimal, Decimal, Fraction]:
    """(cos, sin, eps_v) of Decimal(x) exactly by fixed N-term Taylor sums (ERROR_BOUND §4)."""
    if int(digits) != FEATURE_DIGITS:
        raise Invalid("decimal_cos_sin envelope is proved for 80 digits only")
    xf = float(x)
    if not math.isfinite(xf) or xf < 0 or Fraction(xf) > X_MAX:
        raise Invalid(f"phase {x!r} outside the analytic interval [0, 6.284]")
    with decimal.localcontext(trapping_context(FEATURE_DIGITS)):
        xd = Decimal(xf)
        x2 = xd * xd
        cos_term, sin_term = Decimal(1), xd
        cos_sum, sin_sum = Decimal(0), Decimal(0)
        for k in range(TAYLOR_N + 1):
            cos_sum += cos_term
            sin_sum += sin_term
            cos_term = -(cos_term * x2) / ((2 * k + 1) * (2 * k + 2))
            sin_term = -(sin_term * x2) / ((2 * k + 2) * (2 * k + 3))
        return +cos_sum, +sin_sum, EPS_V


def exact_features(coords) -> list[tuple[Decimal, Decimal]]:
    """Exact (cos, sin)(pi*x/6) at 80 digits for integer x in 0..11: 0, +-1, +-1/2, +-sqrt(3)/2."""
    arr = np.asarray(coords, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[1] < 1 or not np.isfinite(arr).all():
        raise Invalid("coords must be finite [S, >=1]")
    with decimal.localcontext(trapping_context(FEATURE_DIGITS)):
        r = Decimal(3).sqrt() / 2
        h, one, zero = Decimal(1) / 2, Decimal(1), Decimal(0)
        table = [
            (one, zero),
            (r, h),
            (h, r),
            (zero, one),
            (-h, r),
            (-r, h),
            (-one, zero),
            (-r, -h),
            (-h, -r),
            (zero, -one),
            (h, -r),
            (r, -h),
        ]
    out = []
    for value in arr[:, 0]:
        if value != round(value) or not 0 <= value <= 11:
            raise Invalid("feature coordinate must be an integer in 0..11")
        out.append(table[int(value)])
    return out


def feature_envelope() -> Fraction:
    return 2 * u_digits(FEATURE_DIGITS)


def posterior_envelope(L, S) -> Fraction:
    """beta of ERROR_BOUND §3(a): N = 1 + (L-1)(2S+2) positive-path operations at 60 digits."""
    n_ops = 1 + (int(L) - 1) * (2 * int(S) + 2)
    h, t, v = (
        gamma_digits(n_ops, REF_DIGITS),
        gamma_digits(int(S), REF_DIGITS),
        u_digits(REF_DIGITS),
    )
    ell = (1 - h) * (1 - v) / ((1 + h) * (1 + t))
    q = (1 + h) * (1 + v) / ((1 - h) * (1 - t))
    return max(1 - ell, q - 1)


def moment_envelope(beta, S) -> Fraction:
    eps_c = feature_envelope()
    g = gamma_digits(2 * int(S) + 2, FEATURE_DIGITS)
    return beta + (1 + beta) * eps_c + (1 + beta) * (1 + eps_c) * g


def _reference_posterior(T, E, pi, suffix) -> list[Decimal]:
    ctx = trapping_context(REF_DIGITS)
    with decimal.localcontext(ctx):
        try:
            post = independent_reference.decimal_suffix_posterior(T, E, pi, suffix, REF_DIGITS)
        except (decimal.DecimalException, ValueError) as exc:
            raise Invalid(f"reference posterior failed: {exc!r}") from exc
        raised = [sig.__name__ for sig in _WATCHED_FLAGS if decimal.getcontext().flags[sig]]
    if raised:
        raise Invalid(f"reference raised flags {raised}")
    return post


def reference_moments(T, E, pi, coords, canonical32, Ks=(4, 32), cache=None) -> list[dict]:
    """Per row {K: (Mx, My)} Decimal moments with exact features (cached by row bytes)."""
    feats = exact_features(coords)
    tok = np.asarray(canonical32)
    if tok.ndim != 2 or tok.shape[1] != 32:
        raise Invalid("canonical histories must be [n, 32]")
    cache = {} if cache is None else cache
    out = []
    for row in tok:
        per = {}
        for K in Ks:
            key = (int(K), row.astype(np.uint8).tobytes())
            if key not in cache:
                post = _reference_posterior(T, E, pi, row[32 - int(K) :])
                with decimal.localcontext(trapping_context(FEATURE_DIGITS)):
                    mx = sum((p * c for p, (c, _) in zip(post, feats)), Decimal(0))
                    my = sum((p * s for p, (_, s) in zip(post, feats)), Decimal(0))
                cache[key] = (mx, my)
            per[int(K)] = cache[key]
        out.append(per)
    return out


def row_bound(x_hat, phi, M4, M32, eps_M4, eps_M32) -> dict:
    """Exact-rational R, Delta, E_ref and B for one row (ERROR_BOUND §2-3)."""
    vc, vs, eps_v = decimal_cos_sin(float(phi))
    r = [Fraction(M32[0]) - Fraction(M4[0]), Fraction(M32[1]) - Fraction(M4[1])]
    R = Fraction(vc) * r[0] + Fraction(vs) * r[1]
    xh = float(x_hat)
    if not math.isfinite(xh):
        raise Invalid("non-finite operational score")
    delta = abs(Fraction(Decimal(xh)) - R)
    e_ref = eps_v * (abs(r[0]) + abs(r[1])) + 2 * (Fraction(eps_M4) + Fraction(eps_M32))
    return {"R": R, "Delta": delta, "E_ref": e_ref, "B": delta + e_ref}


def _deny_scoring(split, scoring_release):
    if split not in ("calibration", "validation", "scoring"):
        raise Invalid(f"unknown split {split!r}")
    if split == "scoring":
        require_scoring(scoring_release)


def _moment_gap(m_hat_row, ref) -> float:
    return max(abs(Fraction(float(m_hat_row[j])) - Fraction(ref[j])) for j in (0, 1))


def reference_check_rows(
    T, E, pi, coords, canonical32, m_hat: dict, Ks, split, scoring_release=None, cache=None
) -> dict:
    """Early gate: every row and K in Ks, |m_hat - M_ref| <= 1e-10 (no phase needed)."""
    _deny_scoring(split, scoring_release)
    refs = reference_moments(T, E, pi, coords, canonical32, tuple(Ks), cache)
    worst = {}
    for K in Ks:
        mh = np.asarray(m_hat[K], dtype=np.float64)
        if mh.shape != (len(refs), 2) or not np.isfinite(mh).all():
            raise Invalid(f"m_hat[{K}] must be finite [n, 2]")
        worst[int(K)] = float(max(_moment_gap(mh[i], refs[i][int(K)]) for i in range(len(refs))))
    ok = all(v <= MOMENT_TOL for v in worst.values())
    return {
        "status": "PASS" if ok else "FAIL_TECHNICAL",
        "moment_check_max": worst,
        "rows": len(refs),
    }


def certify_rows(
    T,
    E,
    pi,
    coords,
    canonical32,
    phi,
    x_hat,
    m4_hat,
    m32_hat,
    split,
    scoring_release=None,
    cap=1e-4,
    cache=None,
) -> dict:
    """Per-row score certificate; CERTIFIED / INCONCLUSIVE / FAIL_TECHNICAL (ERROR_BOUND §7)."""
    _deny_scoring(split, scoring_release)
    cache = {} if cache is None else cache
    phi = np.asarray(phi, dtype=np.float64)
    x_hat = np.asarray(x_hat, dtype=np.float64)
    n = phi.shape[0] if phi.ndim == 1 else -1
    base = {"rows": n, "bounds": [], "max_bound": None, "moment_check_max": None}
    aligned = phi.ndim == 1 and x_hat.shape == (n,) and np.asarray(canonical32).shape[:1] == (n,)
    if not aligned or not (np.isfinite(phi).all() and np.isfinite(x_hat).all()):
        return dict(base, status="FAIL_TECHNICAL", reason="non-finite or misaligned inputs")
    if np.any(phi < 0) or np.any(phi >= 2 * np.pi):
        return dict(base, status="FAIL_TECHNICAL", reason="operational phase outside [0, 2pi)")
    try:
        check = reference_check_rows(
            T,
            E,
            pi,
            coords,
            canonical32,
            {4: m4_hat, 32: m32_hat},
            (4, 32),
            split,
            scoring_release,
            cache,
        )
        if check["status"] != "PASS":
            return dict(
                base,
                status="FAIL_TECHNICAL",
                moment_check_max=check["moment_check_max"],
                reason="moment check above 1e-10",
            )
        refs = reference_moments(T, E, pi, coords, canonical32, (4, 32), cache)
        S = int(np.asarray(pi).shape[0])
        eps = {K: moment_envelope(posterior_envelope(K, S), S) for K in (4, 32)}
        bounds = [
            row_bound(x_hat[i], phi[i], refs[i][4], refs[i][32], eps[4], eps[32])["B"]
            for i in range(n)
        ]
    except Invalid as exc:
        return dict(base, status="FAIL_TECHNICAL", reason=str(exc))
    worst = max(bounds) if bounds else Fraction(0)
    status = "CERTIFIED" if worst <= Fraction(str(cap)) else "INCONCLUSIVE"
    return dict(
        base,
        status=status,
        bounds=[float(b) for b in bounds],
        max_bound=float(worst),
        max_bound_exact=str(worst),
        moment_check_max=check["moment_check_max"],
        reason="all rows within cap" if status == "CERTIFIED" else "some bound exceeds cap",
    )
