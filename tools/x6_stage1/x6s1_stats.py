"""X6S1 stats (overflow module 2): the empirical-Bernstein bound evaluated outward, certified log
tables, the quantile wrapper, the registered bootstraps and TAIL (X6S1-FROZEN-v1 §7.3-§7.5, §10.2
T14-T16; API.md §8). Import performs no I/O."""
# fmt: off

from __future__ import annotations

import hashlib
import itertools
import math
import sys
from decimal import ROUND_CEILING, Context, Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent)) if str(
    Path(__file__).resolve().parent) not in sys.path else None
import numpy as np  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_data as sd  # noqa: E402

from topo_pilot.contracts import SeedTree, canonical_json  # noqa: E402

LB_975, UB_975 = 0.025, 0.975
OUT = Context(prec=60, rounding=ROUND_CEILING)
SLACK = Decimal("1e-55")


def _dec(fr, ctx: Context) -> Decimal:
    fr = Fraction(fr)
    return ctx.divide(Decimal(fr.numerator), Decimal(fr.denominator))


# ---- Theorem EB (§7.3), outward evaluation (§7.4 item 5) ----
def _eb_parts(delta, n, B, ctx: Context, slack: Decimal) -> dict:
    m = n // 2
    L = ctx.add(_dec(Fraction(2) / Fraction(delta), ctx).ln(ctx), slack)
    a = ctx.multiply(Decimal(B), ctx.add(ctx.divide(L, Decimal(m)).sqrt(ctx), slack))
    b = ctx.divide(ctx.multiply(Decimal(B * B), L), Decimal(12 * m))
    bl3n = ctx.divide(ctx.multiply(Decimal(B), L), Decimal(3 * n))
    s2ln = ctx.add(ctx.divide(ctx.multiply(Decimal(2), L), Decimal(n)).sqrt(ctx), slack)
    return {"L": L, "a": a, "b": b, "BL3n": bl3n, "sqrt2Ln": s2ln}


def eb_constants(delta, n, B=17) -> dict:
    return {k: str(v) for k, v in _eb_parts(delta, n, B, OUT, SLACK).items()}


def _eb(xbar, zbar, n, delta, B, ctx: Context, slack: Decimal) -> Decimal:
    c = _eb_parts(delta, n, B, ctx, slack)
    a, z = c["a"], ctx.add(_dec(zbar, ctx), c["b"])
    root = ctx.add(ctx.add(ctx.multiply(a, a), ctx.multiply(Decimal(4), z)).sqrt(ctx), slack)
    sig = ctx.divide(ctx.add(a, root), Decimal(2))
    return ctx.add(ctx.add(_dec(xbar, ctx), ctx.multiply(sig, c["sqrt2Ln"])), c["BL3n"])


def eb_bound(xbar_plus, zbar_plus, n, delta, B=17) -> Decimal:
    return _eb(xbar_plus, zbar_plus, n, delta, B, OUT, SLACK)


def eb_reference(xbar, zbar, n, delta, B=17, prec=80) -> Decimal:
    return _eb(xbar, zbar, n, delta, B, Context(prec=prec), Decimal(0))


def outward_inputs(xhat, e_row=sd.E_ROW) -> tuple:
    fx = [Fraction(float(v)) for v in np.asarray(xhat, np.float64)]
    n, m, e = len(fx), len(fx) // 2, Fraction(e_row)
    xp = sum(fx, Fraction(0)) / n + e
    zp = sum(((abs(fx[2 * k] - fx[2 * k + 1]) + 2 * e) ** 2 / 2 for k in range(m)),
             Fraction(0)) / m
    return xp, zp


def eb_report(xhat, delta) -> dict:
    x = np.asarray(xhat, np.float64)
    xp, zp = outward_inputs(x)
    return {"U": str(eb_bound(xp, zp, len(x), delta)), "xbar_plus": str(_dec(xp, OUT)),
            "zbar_plus": str(_dec(zp, OUT)), "xbar": float(np.mean(x)), "n": int(len(x)),
            "delta": str(Fraction(delta))}


# ---- certified log tables (§7.4 items 1-4; T14) ----
def qvals() -> tuple:
    out = {Fraction(1, 5), Fraction(1, 15)}
    for m in range(1, sd.T_STAR + 1):
        lm = xm.lam(m)
        out |= {xm.P_MOVE * (lm + (1 - lm) / 3), xm.P_MOVE * (1 - lm) / 3}
    return (Fraction(0),) + tuple(sorted(out))


def _value(x: Fraction, kind, prec) -> Decimal:
    ctx = Context(prec=prec)
    d = _dec(x, Context(prec=prec + 10))
    ln = d.ln(ctx)
    return ln if kind == "ln" else ctx.multiply(d, ln)


def table_entry(x: Fraction, kind) -> dict:
    v80, v120 = _value(Fraction(x), kind, 80), _value(Fraction(x), kind, 120)
    return {"v80": v80, "v120": v120, "float": float(v80)}


def _arg(k, Q, eps) -> Fraction:
    return (1 - eps) * Fraction(k, Q) + eps / 18


def log_tables(Q=2**20, eps=sd.EPS) -> dict:
    eps, diag = Fraction(eps), Decimal(0)
    lnp = np.empty(Q + 1, np.float64)
    for k in range(Q + 1):
        e = table_entry(_arg(k, Q, eps), "ln")
        lnp[k], diag = e["float"], max(diag, abs(e["v80"] - e["v120"]))
    qv = qvals()
    qlnq, fl_q = np.zeros(len(qv), np.float64), np.zeros(len(qv), np.float64)
    for i, q in enumerate(qv[1:], 1):
        e = table_entry(q, "qlnq")
        qlnq[i], fl_q[i], diag = e["float"], float(q), max(diag, abs(e["v80"] - e["v120"]))
    if diag > Decimal("1e-60"):
        raise ValueError(f"log-table enclosure diagnostic {diag} exceeds 1e-60")
    strs = [str(q) for q in qv]
    h = hashlib.sha256(lnp.astype("<f8").tobytes() + qlnq.astype("<f8").tobytes()
                       + fl_q.astype("<f8").tobytes() + canonical_json(strs).encode("utf-8"))
    return {"lnp": lnp, "qlnq": qlnq, "fl_q": fl_q, "qvals": strs, "max_diag": str(diag),
            "sha256": h.hexdigest()}


def decimal_kl(q, pq, prec=80) -> Decimal:
    ctx, tot = Context(prec=prec), Decimal(0)
    for a, b in zip(q, pq):
        if Fraction(a):
            tot = ctx.add(tot, ctx.multiply(_dec(a, ctx), _dec(Fraction(a) / Fraction(b), ctx)
                                            .ln(ctx)))
    return tot


# ---- quantiles and bootstraps (§7.5; §13 items 11-12) ----
def quantile(x, level) -> float:
    return float(np.quantile(np.asarray(x, np.float64), level, method="linear"))


def boot_means(x, B, gen) -> np.ndarray:
    x, out = np.asarray(x, np.float64), np.empty(B, np.float64)
    for b in range(B):
        out[b] = x[gen.integers(0, len(x), size=len(x))].mean()
    return out


def boot_beta(num, den, B, gen) -> np.ndarray:
    num, den = np.asarray(num, np.float64), np.asarray(den, np.float64)
    out = np.empty(B, np.float64)
    for b in range(B):
        idx = gen.integers(0, len(num), size=len(num))
        out[b] = num[idx].sum() / den[idx].sum()
    return out


def cord_draws(num, den, N, B, gen) -> tuple:
    num, den = np.atleast_2d(np.asarray(num, np.float64)), np.asarray(den, np.float64)
    n_inf = len(den)
    ns, ds = np.empty((B, num.shape[0]), np.float64), np.empty(B, np.float64)
    for b in range(B):
        M = gen.binomial(N, n_inf / N)
        c = np.bincount(gen.integers(0, n_inf, size=M), minlength=n_inf)
        ns[b], ds[b] = num @ c, den @ c
    return ns, ds


def _compositions(M, k):
    for cut in itertools.combinations(range(M + k - 1), k - 1):
        edges = (-1,) + cut + (M + k - 1,)
        yield tuple(edges[i + 1] - edges[i] - 1 for i in range(k))


def two_stage_law(N, informative) -> dict:
    k = informative if isinstance(informative, int) else len(list(informative))
    p, law = Fraction(k, N), {}
    for M in range(N + 1):
        pm = math.comb(N, M) * p ** M * (1 - p) ** (N - M)
        for c in _compositions(M, k):
            mult = math.factorial(M)
            for ci in c:
                mult //= math.factorial(ci)
            law[c] = law.get(c, 0) + pm * Fraction(mult, k ** M)
    return {c: v for c, v in law.items() if v}


def tail(num_obs, den_obs, mean, lb_perc, draws_mean) -> dict:
    num = np.atleast_2d(np.asarray(num_obs, np.float64))
    bound = float(sd.TAIL_D1) * math.fsum(np.asarray(den_obs, np.float64))
    d1 = bool(np.all(np.max(np.abs(num), axis=1, initial=0.0) <= bound))
    sd_ = float(np.std(np.asarray(draws_mean, np.float64), ddof=1))
    lb_norm = float(mean) - sd.Z975 * sd_
    d2 = bool(abs(float(lb_perc) - lb_norm) <= float(sd.TAIL_D2))
    return {"D1": d1, "D2": d2, "status": "PASS" if d1 and d2 else "FAIL", "lb_norm": lb_norm}


def boot_stream(statistic_id, model=None) -> np.random.Generator:
    extra = () if model is None else (model,)
    return SeedTree(sd.DATA_MASTER).generator("x6s1", "boot", statistic_id, *extra)
