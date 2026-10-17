"""X6 stage 0: integer segment DP, Decimal enclosures, natural quantities, K-blk, gate G4
(X6-FROZEN-v1 sections 5-6.2; API.md 4). Counts are Python ints; logs are certified enclosures."""

from __future__ import annotations

import itertools
from collections import defaultdict
from decimal import Context, Decimal
from fractions import Fraction

from x6_model import (ANCHOR, ANCHOR_NB, ARMS_SEAM, G_MIN, LADDER, NEIGHBOURS, S3_A, S3_B,  # noqa: F401
                      S3_E, THETA_ROW, WINDOWS, compose, edge_labels, lam, model, perm_name,
                      point_law, seam_letter, statistic)

_LETTERS = ("x+", "x-", "y+", "y-")

# ---- integer DP and aggregation (API 4.1) ----
def segment_dp(arm: str, n_max: int = 31):
    """Yield (n, {(v, kappa, g): count}) for n = 0..n_max (anchor-avoiding paths from ANCHOR)."""
    lab = edge_labels(arm)
    step = {v: [(j, _LETTERS.index(lt) if (lt := seam_letter(v, j)) else -1, lab[(v, j)])
                for j in NEIGHBOURS[v] if j != ANCHOR] for v in range(16)}
    layer = {(ANCHOR, (0, 0, 0, 0), S3_E): 1}
    for n in range(n_max + 1):
        yield n, layer
        if n == n_max:
            return
        new = {}
        for (v, k, g), c in layer.items():
            for j, li, lg in step[v]:
                key = (j, k if li < 0 else k[:li] + (k[li] + 1,) + k[li + 1:],
                       g if lg == S3_E else compose(lg, g))
                new[key] = new.get(key, 0) + c
        layer = new

def classes(layer: dict, S: str) -> dict:
    out = {}
    for (v, k, g), c in layer.items():
        cls = out.setdefault((v, statistic(S, k)), {})
        cls[g] = cls.get(g, 0) + c
    return out
def _image_counts(cls: dict, y: int) -> list:
    W = [0, 0, 0]
    for g, c in cls.items():
        W[g[y]] += c
    return W
def weights(cls: dict, y: int) -> tuple:
    W = _image_counts(cls, y)
    return tuple(Fraction(x, sum(W)) for x in W)
def ambiguous(cls: dict, y: int) -> bool:
    return sum(1 for x in _image_counts(cls, y) if x) >= 2
def avoid_counts(n_max: int = 31) -> dict:
    cnt, A, B = {ANCHOR: 1}, [1], [0]
    for _ in range(n_max):
        new = defaultdict(int)
        for v, c in cnt.items():
            for j in NEIGHBOURS[v]:
                if j != ANCHOR:
                    new[j] += c
        cnt = dict(new)
        A.append(sum(cnt.values()))
        B.append(sum(c for v, c in cnt.items() if v in ANCHOR_NB))
    D = [{v: 1 for v in range(16) if v != ANCHOR}]
    for _ in range(n_max):
        D.append({v: sum(D[-1][j] for j in NEIGHBOURS[v] if j != ANCHOR) for v in D[-1]})
    return {"A": A, "B": B, "D": D}

def total_mass(t: int, counts: dict) -> Fraction:
    tot = Fraction(1, 16) + sum(Fraction(counts["A"][n], 16 * 5**n) for n in range(1, t))
    return tot + Fraction(sum(counts["D"][t - 1].values()), 16 * 5 ** (t - 1))

# ---- Decimal arithmetic and the memo (API 4.2) ----
DIV_PREC, PRECS = {80: 90, 120: 130}, (80, 120)
CTX = {80: Context(prec=80), 120: Context(prec=120)}
C200 = Context(prec=200)
MEMO: dict = {}
_PYTH: dict = {}
_LN: dict = {}  # (prec, exact ratio) -> the identical ln value; cleared with MEMO

def to_decimal(fr, prec: int) -> Decimal:
    fr = Fraction(fr)
    return Context(prec=prec).divide(Decimal(fr.numerator), Decimal(fr.denominator))
def kl_decimal(p, q, prec: int) -> Decimal:
    ctx, dp, tot = CTX.get(prec) or Context(prec=prec), DIV_PREC[prec], Decimal(0)
    for a, b in zip(p, q):
        if a > 0:
            if b == 0:
                raise ValueError("KL undefined: q_i = 0 where p_i > 0")
            key = (prec, Fraction(a) / Fraction(b))
            r = _LN[key] if key in _LN else _LN.setdefault(key, ctx.ln(to_decimal(key[1], dp)))
            tot = ctx.add(tot, ctx.multiply(to_decimal(a, dp), r))
    return tot

def entropy_decimal(p, prec: int) -> Decimal:
    ctx, dp, tot = CTX.get(prec) or Context(prec=prec), DIV_PREC[prec], Decimal(0)
    for a in p:
        if a > 0:
            tot = ctx.subtract(tot, ctx.multiply(to_decimal(a, dp), ctx.ln(to_decimal(a, dp))))
    return tot
def memo_key(prec, kind, n, w, z) -> tuple:
    return (prec, kind, n, tuple(Fraction(x) for x in w), z)
def _mix(m: int, w) -> list:
    lm = lam(m)
    return [lm * Fraction(a) + (1 - lm) / 3 for a in w]
def kl_term_uncached(prec, kind, n, w, z) -> Decimal:
    m = n + 1 if kind == "next" else n
    if kind not in ("next", "fibre"):
        raise ValueError(kind)
    return kl_decimal(point_law(m, z), _mix(m, w), prec)
def kl_term(prec, kind, n, w, z) -> Decimal:
    key = memo_key(prec, kind, n, w, z)
    if key not in MEMO:
        MEMO[key] = kl_term_uncached(prec, kind, n, w, z)
    return MEMO[key]
def memo_clear() -> None:
    MEMO.clear()
    _PYTH.clear()
    _LN.clear()
def _pyth_kl(prec, n, w_fine, w_coarse) -> Decimal:
    key = (prec, n, w_fine, w_coarse)
    if key not in _PYTH:
        _PYTH[key] = kl_decimal(_mix(n + 1, w_fine), _mix(n + 1, w_coarse), prec)
    return _PYTH[key]
def decimal_model(arm: str, prec: int) -> tuple:
    m, dp = model(arm), DIV_PREC[prec]
    return ([[to_decimal(v, dp) for v in r] for r in m["T"]],
            [[to_decimal(v, dp) for v in r] for r in m["E"]], [to_decimal(v, dp) for v in m["pi"]])

# ---- enclosures and certification (API 4.3) ----
def enclosure(v80, v120, abs_sum, n_terms) -> dict:
    eps = C200.multiply(Decimal("1e-60"), max(Decimal(1), Decimal(abs_sum)))
    return {"type": "enclosure", "v80": v80, "v120": v120, "abs_sum": abs_sum, "N": n_terms,
            "eps": eps, "lo": C200.subtract(v80, eps), "hi": C200.add(v80, eps),
            "consistent": C200.abs(C200.subtract(v80, v120)) <= eps, "n_ok": n_terms + 10 <= 10**17}
def enclose_sum(pairs) -> dict:
    s80, s120, a, n = Decimal(0), Decimal(0), Decimal(0), 0
    for t80, t120 in pairs:
        s80, s120 = CTX[80].add(s80, t80), CTX[120].add(s120, t120)
        a, n = CTX[80].add(a, C200.abs(t80)), n + 1
    return enclosure(s80, s120, a, n)
def certify(enc: dict, theta) -> str:
    th = Fraction(theta)
    return ("PASS" if Fraction(enc["lo"]) >= th else
            "FAIL" if Fraction(enc["hi"]) < th else "UNCERTIFIED")
def mass_bounds(rows, theta) -> tuple:
    lo, up = Fraction(0), Fraction(0)
    for mass, enc in rows:
        cert = certify(enc, theta)
        lo, up = lo + (mass if cert == "PASS" else 0), up + (mass if cert != "FAIL" else 0)
    return lo, up
def certify_mass(m_lower, m_upper, threshold) -> str:
    return ("PASS" if m_lower >= threshold else
            "FAIL" if m_upper < threshold else "UNCERTIFIED")

# ---- per-layer Decimal sums (API 7 choice 17) ----
def _rec() -> dict:
    return {80: Decimal(0), 120: Decimal(0), "abs": Decimal(0), "N": 0}
def _add(rec: dict, mult: int, vals: dict) -> None:
    for p in PRECS:
        rec[p] = CTX[p].add(rec[p], CTX[p].multiply(Decimal(mult), vals[p]))
    rec["N"] += 1
def _scale(rec: dict, coef) -> dict:
    out = {p: CTX[p].multiply(rec[p], to_decimal(coef, DIV_PREC[p])) for p in PRECS}
    return {**out, "abs": C200.abs(out[80]), "N": rec["N"]}
def _enc(recs, signs=None) -> dict:
    v = {80: Decimal(0), 120: Decimal(0)}
    a, n = Decimal(0), 0
    for k, r in enumerate(recs):
        s = 1 if signs is None else signs[k]
        for p in PRECS:
            v[p] = (CTX[p].add if s > 0 else CTX[p].subtract)(v[p], r[p])
        a, n = CTX[80].add(a, r["abs"]), n + r["N"]
    return enclosure(v[80], v[120], a, n)

def _both(fn, *args) -> dict:
    return {p: fn(p, *args) for p in PRECS}
def _mass(cnt: list, t: int) -> Fraction:
    return sum((Fraction(cnt[n], 48 * 5**n) for n in range(1, t)), Fraction(0))
def _row_enc(vals: dict) -> dict:
    r = {p: CTX[p].divide(vals[p], Decimal(5)) for p in PRECS}
    return enclosure(r[80], r[120], C200.abs(r[80]), 1)

# ---- natural quantities (API 4.4, section 5.3-5.4) ----
def natural(arm: str, t_max: int = 32) -> dict:
    if arm not in ARMS_SEAM:
        raise ValueError(f"natural quantities undefined for {arm}")
    nmax, counts = t_max - 1, avoid_counts(t_max - 1)
    Q = defaultdict(lambda: [_rec() for _ in range(t_max)])
    amb = {S: [0] * t_max for S in LADDER}
    amb_nb = {S: [0] * t_max for S in LADDER}
    m_lo, m_up, null = [0] * t_max, [0] * t_max, {S: True for S in LADDER}
    nmin, amb_y = {"any": None, "nb": None}, {y: False for y in range(3)}
    tables = {S: {} for S in LADDER}
    a_dp, b_dp, zcw = [], [], {}
    for n, layer in segment_dp(arm, nmax):
        a_dp.append(sum(layer.values()))
        b_dp.append(sum(c for (v, _, _), c in layer.items() if v in ANCHOR_NB))
        memo_clear()  # keys carry n: entries of other layers are never reused
        if n == 0:
            continue
        wts = {}
        for S in LADDER:
            cl = classes(layer, S)
            if S == "counts" and n == 7:
                zcw = {perm_name(g): c for g, c in cl.get((6, (1, 0)), {}).items()}
            for (v, sig), cls in cl.items():
                nb, tot = v in ANCHOR_NB, sum(cls.values())
                if S == "Parikh" or nb:
                    tables[S][(n, v, sig)] = cls
                for y in range(3):
                    W = _image_counts(cls, y)
                    w = wts[(S, v, sig, y)] = tuple(Fraction(x, tot) for x in W)
                    if S == "Parikh" and nb:
                        for S2 in ("empty", "H1"):
                            wc = wts[(S2, v, statistic(S2, sig), y)]
                            if wc != w:
                                _add(Q[("PY", S2)][n], tot, _both(_pyth_kl, n, w, wc))
                    if sum(1 for x in W if x) < 2:
                        continue  # one image: the competitor equals q*, every KL term is 0
                    amb[S][n], null[S] = amb[S][n] + tot, False
                    if nb:
                        amb_nb[S][n] += tot
                        amb_y[y] |= S == "empty"
                    if S == "Parikh":
                        nmin["any"] = nmin["any"] or n
                        nmin["nb"] = nmin["nb"] or (n if nb else None)
                    for z in (z for z in range(3) if W[z]):
                        if nb:
                            kn = _both(kl_term, "next", n, w, z)
                            _add(Q[("G", S)][n], W[z], kn)
                            if S == "empty":
                                _add(Q[("Gy", y)][n], W[z], kn)
                            if S == "Parikh":
                                cert = certify(_row_enc(kn), THETA_ROW)
                                m_lo[n] += W[z] if cert == "PASS" else 0
                                m_up[n] += W[z] if cert != "FAIL" else 0
                        if S == "Parikh":
                            _add(Q[("Jfib",)][n], W[z], _both(kl_term, "fibre", n, w, z))
    g = {k: [_scale(r, Fraction(1, (48 if k == ("Jfib",) else 240) * 5**n))
             for n, r in enumerate(v)] for k, v in Q.items()}
    for k in [("G", S) for S in LADDER] + [("PY", "empty"), ("PY", "H1"), ("Jfib",)] + [
            ("Gy", y) for y in range(3)]:
        g.setdefault(k, [_rec() for _ in range(t_max)])
    ts = range(1, t_max + 1)
    rng = lambda key, hi: _enc(g[key][1:hi])  # noqa: E731  (n = 1..hi-1)
    ln3 = {p: CTX[p].ln(Decimal(3)) for p in PRECS}
    hmu = [{p: entropy_decimal(point_law(m, 0), p) for p in PRECS} for m in range(t_max + 1)]
    pn = [Fraction(1, 16)] + [Fraction(counts["A"][n], 16 * 5**n) for n in range(1, t_max)]

    def info(coef, m):
        return _scale({**{p: CTX[p].subtract(ln3[p], hmu[m][p]) for p in PRECS}, "N": 1}, coef)
    ifib = [info(pn[n], n) for n in range(t_max)]
    gk = [info(Fraction(counts["B"][n], 80 * 5**n), n + 1) for n in range(t_max)]
    out = {"G": {S: {t: rng(("G", S), t) for t in ts} for S in LADDER},
           "pyth": {t: {} for t in ts},
           "J": {k: {t: rng(("G", "Parikh"), min(k, t)) for t in ts} for k in WINDOWS},
           "J_fib": {k: {t: rng(("Jfib",), min(k, t)) for t in ts} for k in WINDOWS},
           "J_fib_full": {t: rng(("Jfib",), t) for t in ts},
           "I_fib": {k: {t: _enc(ifib[:min(k, t)]) for t in ts} for k in WINDOWS},
           "I_fib_full": {t: _enc(ifib[:t]) for t in ts},
           "G_k": {k: {t: _enc(gk[k:t]) for t in ts} for k in WINDOWS}}
    for t, S2 in itertools.product(ts, ("empty", "H1")):  # G_S - G_Parikh - E KL(q_P || q_S)
        recs = g[("G", S2)][1:t] + g[("G", "Parikh")][1:t] + g[("PY", S2)][1:t]
        out["pyth"][t][S2] = _enc(recs, [1] * (t - 1) + [-1] * (2 * t - 2))
    masses = {}
    for t in ts:
        no_cue = Fraction(sum(counts["D"][t - 1].values()), 16 * 5 ** (t - 1))
        nb_nc = Fraction(sum(c for v, c in counts["D"][t - 1].items() if v in ANCHOR_NB),
                         16 * 5 ** (t - 1))
        masses[t] = {"E_cue": 1 - no_cue, "age": pn[:t], "no_cue": no_cue,
                     "E_nb": nb_nc + sum(Fraction(counts["B"][n], 16 * 5**n) for n in range(1, t)),
                     "amb": {S: _mass(amb[S], t) for S in LADDER},
                     "amb_nb": {S: _mass(amb_nb[S], t) for S in LADDER}}
    lo, up = _mass(m_lo, t_max), _mass(m_up, t_max)
    gp = g[("G", "Parikh")]
    mean = [{**{p: CTX[p].multiply(gp[n][p], to_decimal(Fraction(t_max - n, t_max), DIV_PREC[p]))
                for p in PRECS}, "abs": C200.abs(gp[n][80]), "N": gp[n]["N"] * (t_max - n)}
            for n in range(1, t_max)]
    return {**out, "masses": masses, "M32": {"lower": lo, "upper": up,
                                             "cert": certify_mass(lo, up, Fraction(1, 32))},
            "n_min": nmin, "null": {S: null[S] for S in LADDER},
            "theorem4": (nmin["nb"] or 99) >= 7 and (nmin["any"] or 99) >= 4,
            "tables": tables, "mean_G_parikh": _enc(mean), "A_dp": a_dp, "B_dp": b_dp,
            "fixed_point": {"amb_y": amb_y,
                            "G_empty_y": {y: rng(("Gy", y), t_max) for y in range(3)}},
            "zc_witness": zcw}

# ---- K-blk (API 4.4, section 6.2, Theorem 8) ----
def kblk(arm: str) -> dict:
    if arm not in ARMS_SEAM:
        raise ValueError(f"K-blk undefined for {arm}")
    lab, recs, states_max, amb_any, wit = edge_labels(arm), [], 0, False, False
    step = {v: [(j, lab[(v, j)]) for j in NEIGHBOURS[v] if j != ANCHOR] for v in range(16)}
    for s in range(1, 32):  # cue position s, n = 32 - s; transitions land on s+1..32
        n, st, rec = 32 - s, {(ANCHOR, S3_E, ()): 1}, _rec()
        memo_clear()
        for p in range(s + 1, 33):
            new, fresh = {}, p > s + 1 and (p - 1) // 8 != (p - 2) // 8
            for (v, cur, done), c in st.items():
                if fresh:
                    cur, done = S3_E, done + (cur,)
                for j, lg in step[v]:
                    key = (j, compose(lg, cur), done)
                    new[key] = new.get(key, 0) + c
            st, states_max = new, max(states_max, len(new))
        cls = defaultdict(dict)
        for (v, cur, done), c in st.items():
            g, blocks = S3_E, done + (cur,)
            for b in blocks:
                g = compose(b, g)
            d = cls[(v, tuple(sorted(blocks)))]
            d[g] = d.get(g, 0) + c
        if n == 16:
            d = cls.get((6, tuple(sorted((S3_A, S3_B)))))
            wit = d is not None and all(ambiguous(d, y) for y in range(3))
        for (v, _ms), d in cls.items():
            tot = sum(d.values())
            for y in range(3):
                W = _image_counts(d, y)
                if sum(1 for x in W if x) < 2:
                    continue
                amb_any = True
                if v in ANCHOR_NB:
                    w = tuple(Fraction(x, tot) for x in W)
                    for z in (z for z in range(3) if W[z]):
                        _add(rec, W[z], _both(kl_term, "next", n, w, z))
        recs.append(_scale(rec, Fraction(1, 240 * 5**n)))
    return {"D_blk": _enc(recs), "ambiguous_any": amb_any, "witness_ambiguous": wit,
            "states_max": states_max}

# ---- gate G4 (section 8.2) ----
G4_CHECKS = ("dp_counts", "total_mass", "E_nb", "ladder", "pythagorean", "theorem4", "n_min",
             "abelian_nulls", "windows_identical", "kblk_zero", "kblk_witness", "enclosures")
_LADDER_PAIRS = (("empty", "parity"), ("parity", "counts"), ("counts", "Parikh"),
                 ("parity", "H1"), ("H1", "Parikh"))

def _encs(obj):
    if isinstance(obj, dict):
        if obj.get("type") == "enclosure":
            yield obj
        else:
            for v in obj.values():
                yield from _encs(v)
def _ge(a: dict, b: dict) -> bool:  # a >= b within the summed half-widths
    return C200.add(C200.add(a["v80"], a["eps"]), b["eps"]) >= b["v80"]
def _g4_checks(nat: dict, kb: dict, arms) -> dict:
    counts, ts = avoid_counts(31), range(1, 33)
    def run(src, need, fn):
        return ("PASS" if fn() else "FAIL") if all(a in src for a in need) else "NOT_RUN"
    same = lambda k: all(  # noqa: E731
        (e["v80"], e["v120"]) == (f["v80"], f["v120"])
        for a in arms for e, f in zip(_encs(nat[a][k]), _encs(nat[arms[0]][k])))
    abel = {"AB": "parity", "ZC": "H1", "TRIV": "empty"}
    return {
        "dp_counts": run(nat, arms, lambda: all(nat[a]["A_dp"] == counts["A"] and
                                                nat[a]["B_dp"] == counts["B"] for a in arms)),
        "total_mass": "PASS" if all(total_mass(t, counts) == 1 for t in ts) else "FAIL",
        "E_nb": run(nat, arms, lambda: all(nat[a]["masses"][t]["E_nb"] == Fraction(1, 4)
                                           for a in arms for t in ts)),
        "ladder": run(nat, arms, lambda: all(_ge(nat[a]["G"][s1][t], nat[a]["G"][s2][t]) for a in
                                             arms for t in ts for s1, s2 in _LADDER_PAIRS)),
        "pythagorean": run(nat, arms, lambda: all(C200.abs(e["v80"]) <= e["eps"] for a in arms
                                                  for t in ts for e in nat[a]["pyth"][t].values())),
        "theorem4": run(nat, arms, lambda: all(nat[a]["theorem4"] for a in arms)),
        "n_min": run(nat, ["NA"], lambda: nat["NA"]["n_min"] == {"any": 4, "nb": 7}),
        "abelian_nulls": run(nat, list(abel),
                             lambda: all(nat[a]["null"][s] for a, s in abel.items())),
        "windows_identical": run(nat, arms,
                                 lambda: all(same(k) for k in ("I_fib", "I_fib_full", "G_k"))),
        "kblk_zero": run(kb, list(abel), lambda: not any(kb[a]["ambiguous_any"] for a in abel)),
        "kblk_witness": run(kb, ["NA"], lambda: kb["NA"]["witness_ambiguous"]),
        "enclosures": run(kb, arms, lambda: all(e["consistent"] and e["n_ok"] for e in
                                                _encs({"n": nat, "k": kb}))),
    }

def gate_G4(arms=ARMS_SEAM) -> dict:
    nat, kb, tables, step = {}, {}, None, None
    try:
        for arm in arms:
            step = f"natural:{arm}"
            nat[arm] = natural(arm)
            tab = nat[arm].pop("tables")
            tables = tab if arm == "NA" else tables
        for arm in arms:
            step = f"kblk:{arm}"
            kb[arm] = kblk(arm)
        step = None
    except MemoryError:  # S8: the Job Object memory limit
        pass
    checks = _g4_checks(nat, kb, tuple(arms))
    fail = any(v == "FAIL" for v in checks.values())
    out = {"status": "FAIL" if fail else "RESOURCE_LIMIT" if step else "PASS", "natural": nat,
           "kblk": kb, "checks": checks, "tables": tables}
    if step:
        out["resource_limit"] = {"step": step,
                                 "completed": [k for k, v in checks.items() if v != "NOT_RUN"]}
    return out
