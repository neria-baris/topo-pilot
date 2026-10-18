"""X6 stage 0: exact Fraction filter (G2), witness families, beta, challenge, 4x8 comparator
(G3), O1/O2 (X6-FROZEN-v1 sections 4, 6.1, 8.3, 9.2; API.md 5)."""

from __future__ import annotations

import itertools
from collections import Counter
from decimal import Decimal
from fractions import Fraction

from x6_dp import (CTX, certify, certify_mass, classes, entropy_decimal, kl_decimal,  # noqa: F401
                   segment_dp)
from x6_model import (ANCHOR, ARMS, ARMS_SEAM, BETA_MAX, G_MIN, LADDER, M_MIN, S3_E, S3_LIST,
                      TOL_LOG, TV_MIN, closed_form, edge_labels, holonomy, lam, model, parikh,
                      parse, perm_name, point_law, seam_letter, statistic, tok)

# ---- Fraction forward filter and G2 (API 5.1, section 9.2) ----
_SPARSE: dict = {}

def _rows(T) -> list:
    if id(T) not in _SPARSE:
        _SPARSE[id(T)] = (T, [[(j, v) for j, v in enumerate(r) if v] for r in T])
    return _SPARSE[id(T)][1]
def _step(Ts, E, pred: dict, w: int):
    """Condition the predictive state law on w: (belief, normaliser, next predictive)."""
    a = {s: v * E[s][w] for s, v in pred.items() if E[s][w]}
    z = sum(a.values())
    if not z:
        return None, z, None
    b, nxt = {s: v / z for s, v in a.items()}, {}
    for s, v in b.items():
        for j, tv in Ts[s]:
            nxt[j] = nxt.get(j, 0) + v * tv
    return b, z, nxt

def _q(pred: dict, E) -> list:
    return [sum((v * E[s][k] for s, v in pred.items()), Fraction(0)) for k in range(len(E[0]))]
def _dense(b: dict, n: int) -> list:
    return [b.get(s, Fraction(0)) for s in range(n)]
def fraction_filter(T, E, pi, tokens) -> dict:
    Ts, pred, P, bs = _rows(T), {s: v for s, v in enumerate(pi) if v}, Fraction(1), []
    qs = [_q(pred, E)]
    for w in tokens:
        b, z, pred = _step(Ts, E, pred, int(w))
        if not z:
            raise ValueError("zero-probability history")
        P *= z
        bs.append(_dense(b, len(T)))
        qs.append(_q(pred, E))
    return {"b": bs, "q": qs, "P": P}

def gate_G2(arms=ARMS_SEAM, t_max: int = 6) -> dict:
    out = {"nodes": {}, "mass": {}, "mismatch": {}, "tables_equal": {}, "A": None}
    for arm in arms:
        m, labels = model(arm), edge_labels(arm)
        Ts, E, n_v = _rows(m["T"]), m["E"], len(m["E"][0])
        mass, stats, layers = Counter(), Counter(), [Counter() for _ in range(t_max)]

        def dfs(pred, P, hist):
            for w in range(n_v):
                b, z, nxt = _step(Ts, E, pred, w)
                if not z:
                    continue
                h, Ph = hist + (w,), P * z
                cf, mass[len(h)] = closed_form(arm, h), mass[len(h)] + Ph
                stats["nodes"] += 1
                bad = cf["b"] != _dense(b, 48) or cf["q"] != _q(nxt, E) or cf["P"] != Ph
                stats["mismatch"] += bad
                if h[0] == 15 and all(x < 15 for x in h[1:]):  # y = 0, one cue: n = t - 1
                    path = (ANCHOR,) + tuple(parse(h)["path"][1:])
                    layers[len(h) - 1][(path[-1], parikh(path), holonomy(path, labels))] += 1
                if len(h) < t_max:
                    dfs(nxt, Ph, h)
        dfs({s: v for s, v in enumerate(m["pi"]) if v}, Fraction(1), ())
        dp = [dict(layer) for _, layer in segment_dp(arm, t_max - 1)]
        out["tables_equal"][arm] = all(
            dict(layers[n]) == dp[n] and
            all(classes(layers[n], S) == classes(dp[n], S) for S in LADDER)
            for n in range(1, t_max))
        out["nodes"][arm], out["mismatch"][arm] = stats["nodes"], stats["mismatch"]
        out["mass"][arm] = {t: mass[t] for t in range(1, t_max + 1)}
        out["A"] = [sum(layers[n].values()) for n in range(1, t_max)]
    ok = all(v == 0 for v in out["mismatch"].values()) and all(out["tables_equal"].values())
    ok &= all(p == 1 for d in out["mass"].values() for p in d.values())
    ok &= out["A"][:5] == [4, 16, 76, 352, 1684]
    return {"status": "PASS" if ok else "FAIL", **out}

# ---- witnesses (API 5.2, section 4) ----
LOOPS = {"A+": (9, 13, 1, 5), "A-": (1, 13, 9, 5), "B+": (6, 7, 4, 5), "B-": (4, 7, 6, 5)}
P_LOOP = 5
ORDERINGS = tuple(itertools.permutations(("A+", "A-", "B+", "B-")))
FAMILIES = ("W1", "W2", "W3", "W3p")
_S7 = (1, 2, 3, 7, 11, 15, 14)

def members(family: str) -> tuple:
    return {"W1": ("U", "D"), "W2": ("AB", "BA")}.get(family, ORDERINGS)
def witness_path(family: str, member) -> tuple:
    if family == "W1":
        return (14, 15, 3 if member == "U" else 12, 0, 4, 5, 6)
    if family == "W2":
        first, second = ("A+", "B+") if member == "AB" else ("B+", "A+")
        return (9, 5) + LOOPS[first] + LOOPS[second] + _S7
    loops = sum((LOOPS[k] for k in member), ())
    return (6, 5) + (5,) * 5 + loops + (5,) * 7 + (6,) if family == "W3" else (9, 5) + loops + _S7
def prefix_tokens(name: str, y0: int = 0) -> tuple:
    return {"P0": (), "P1": (10,), "P3": (6, 5, 9), "P6": (15 + y0, 13, 12, 9, 5, 9)}[name]
def witness_tokens(family, member, y, prefix="P0", y0=0) -> tuple:
    path = witness_path(family, member)
    return prefix_tokens(prefix, y0) + (15 + y,) + tuple(tok(v) for v in path)
def _cue_tv(q1, q2) -> Fraction:
    c1, c2 = q1[15:18], q2[15:18]
    return sum(abs(a / sum(c1) - b / sum(c2)) for a, b in zip(c1, c2)) / 2
def family_values(arm: str, family: str, prefix: str = "P0", y0: int = 0) -> dict:
    m, labels = model(arm), edge_labels(arm)
    rec, tvs, spread = {}, [], Fraction(0)
    for mem in members(family):
        rho = holonomy((ANCHOR,) + witness_path(family, mem), labels)
        rec[mem] = {"holonomy": perm_name(rho), "P": {}, "q": {}}
        for y in range(3):
            f = fraction_filter(m["T"], m["E"], m["pi"], witness_tokens(family, mem, y, prefix, y0))
            rec[mem]["P"][y], rec[mem]["q"][y] = f["P"], f["q"][-1]
    for y in range(3):
        for a, b in itertools.combinations(members(family), 2):
            qa, qb = rec[a]["q"][y], rec[b]["q"][y]
            spread = max(spread, sum(abs(u - v) for u, v in zip(qa, qb)) / 2)
            if rec[a]["holonomy"] != rec[b]["holonomy"]:
                tvs.append(_cue_tv(qa, qb))
    out = {"t": len(witness_tokens(family, members(family)[0], 0, prefix, y0)),
           "n": len(witness_path(family, members(family)[0])), "members": rec,
           "equal_P": all(len({r["P"][y] for r in rec.values()}) == 1 for y in range(3)),
           "tv_min": min(tvs) if tvs else None, "spread": spread}
    if family in ("W3", "W3p"):
        cnt = Counter(r["holonomy"] for r in rec.values())
        out["multiplicity"] = {k: cnt.get(k, 0) for k in ("e", "c", "c2")}
    return out

# ---- matched statistics and constancy (API 5.3, section 4.7) ----
def matched(family: str, y: int = 0) -> dict:
    toks = [witness_tokens(family, mem, y) for mem in members(family)]
    paths = [(ANCHOR,) + witness_path(family, mem) for mem in members(family)]
    grams = lambda t, k: Counter(t[i:i + k] for i in range(len(t) - k + 1))  # noqa: E731
    stat = {"length": [len(t) for t in toks], "n": [len(p) - 1 for p in paths],
            "end": [p[-1] for p in paths], "prefix": [parse(t)["prefix"] for t in toks],
            "cue": [t[0] for t in toks], "parikh": [parikh(p) for p in paths],
            "h1": [statistic("H1", parikh(p)) for p in paths],
            "counts": [statistic("counts", parikh(p)) for p in paths],
            "parity": [statistic("parity", parikh(p)) for p in paths],
            "bag": [Counter(t) for t in toks], "bigram": [grams(t, 2) for t in toks],
            "trigram": [grams(t, 3) for t in toks]}
    out = {k: "equal" if all(v == vals[0] for v in vals) else "differs" for k, vals in stat.items()}
    tail = 0
    while tail < len(toks[0]) and len({t[len(t) - tail - 1:] for t in toks}) == 1:
        tail += 1
    tri = set().union(*stat["trigram"])
    out["tail"] = tail
    out["trigram_diff"] = sorted(g for g in tri if len({c[g] for c in stat["trigram"]}) > 1)
    return out

def rs_key(S: str, tokens) -> tuple:
    p = parse(tokens)
    if p["s"] is None:
        return (True, tuple(int(w) for w in tokens), None, None, p["v"], None)
    return (False, p["prefix"], p["n"], p["y"], p["v"], statistic(S, parikh(p["segment"])))
def constant_by_keys(keys) -> bool:
    keys = list(keys)
    return bool(keys) and all(k == keys[0] for k in keys)

# ---- beta table (API 5.4, section 4.9) ----
def competitor_holonomy(kind: str, letters) -> tuple:
    if not letters:
        return S3_E
    if kind == "last":
        return tuple(letters[-1])
    if kind == "first":
        return tuple(letters[0])
    g = S3_E
    for lt in letters:  # "rev": the first letter is applied last
        g = tuple(g[lt[x]] for x in range(3))
    return g

def beta(rows):
    rows, sets = list(rows), {}
    for sid, w, qs, qa in rows:
        sets.setdefault(sid, []).append((Fraction(w), qs, qa))
    num = den = Fraction(0)
    for items in sets.values():
        tw = sum(w for w, _, _ in items)
        ms = [sum(w * q[k] for w, q, _ in items) / tw for k in range(3)]
        ma = [sum(w * q[k] for w, _, q in items) / tw for k in range(3)]
        for w, qs, qa in items:
            cs, ca = [qs[k] - ms[k] for k in range(3)], [qa[k] - ma[k] for k in range(3)]
            num += w * sum(a * b for a, b in zip(ca, cs))
            den += w * sum(a * a for a in cs)
    return num / den if den else None

def beta_table() -> dict:
    lab, out = edge_labels("NA"), {}
    for fam in ("W1", "W2", "W3"):
        n, out[fam] = len(witness_path(fam, members(fam)[0])), {}
        for kind in ("rev", "last", "first", "set_constant"):
            rows = {"eq": [], "bal": []}
            for y, mem in itertools.product(range(3), members(fam)):
                path = (ANCHOR,) + witness_path(fam, mem)
                rho = holonomy(path, lab)
                lets = [lab[(u, v)] for u, v in zip(path, path[1:]) if seam_letter(u, v)]
                alt = competitor_holonomy(kind, lets)
                qs = point_law(n + 1, rho[y])
                qa = (Fraction(1, 3),) * 3 if kind == "set_constant" else point_law(n + 1, alt[y])
                rows["eq"].append((y, 1, qs, qa))
                rows["bal"].append((y, Fraction(1, 4) if rho == S3_E else 1, qs, qa))
            per_y = [beta([r for r in rows["eq"] if r[0] == y]) for y in range(3)]
            out[fam][kind] = {"pooled": beta(rows["eq"]), "per_y": per_y}
            if fam == "W3":
                out[fam][kind]["balanced"] = beta(rows["bal"])
    return out

def family_label(beta_row: dict) -> str:
    ok = all(r["pooled"] is not None and r["pooled"] <= BETA_MAX for r in beta_row.values())
    return "DISCRIMINATING" if ok else "NOT_DISCRIMINATING"

# ---- challenge and the 4x8 comparator (API 5.5, sections 4.8, 6.1) ----
def set_gap(laws, prec: int = 80) -> Decimal:
    laws = [list(map(Fraction, q)) for q in laws]
    mix = [sum(c) / len(laws) for c in zip(*laws)]
    tot = Decimal(0)
    for q in laws:
        tot = CTX[prec].add(tot, kl_decimal(q, mix, prec))
    return CTX[prec].divide(tot, Decimal(len(laws)))
def _w3_laws(y: int) -> dict:
    fv = family_values("NA", "W3")
    return {o: (fv["members"][o]["holonomy"], fv["members"][o]["q"][y]) for o in ORDERINGS}
def challenge_values() -> dict:
    hol = [h for h, _ in _w3_laws(0).values()]
    prior = {z: Fraction(hol.count(z), len(hol)) for z in ("e", "c", "c2")}
    toks = [witness_tokens("W3", o, 0) for o in ORDERINGS]
    out = {"prior": prior, "z_information": entropy_decimal(list(prior.values()), 80),
           "z_information_window": {k: Fraction(0) if len({t[-k:] for t in toks}) == 1 else None
                                    for k in range(1, 10)},
           "q_bar": {}, "delta_challenge": {}, "delta_cue": {}}
    for y in range(3):
        laws = [q for _, q in _w3_laws(y).values()]
        cue = [[v / sum(q[15:18]) for v in q[15:18]] for q in laws]
        out["q_bar"][y] = tuple(sum(c) / len(cue) for c in zip(*cue))
        out["delta_challenge"][y], out["delta_cue"][y] = set_gap(laws), set_gap(cue)
    return out

def block_posterior(prior: dict, likelihoods) -> dict:
    un = dict(prior)
    for lik in likelihoods:
        un = {z: v * lik.get(z, 0) for z, v in un.items()}
    tot = sum(un.values())
    if not tot:
        raise ValueError("zero total block evidence")
    return {z: v / tot for z, v in un.items()}
def block_comparator(y: int = 0) -> dict:
    laws = _w3_laws(y)
    truth = {o: h for o, (h, _) in laws.items()}
    q_of = {h: q for h, q in laws.values()}
    toks = {o: witness_tokens("W3", o, y) for o in ORDERINGS}
    nz = Counter(truth.values())
    prior = {z: Fraction(nz[z], len(ORDERINGS)) for z in ("e", "c", "c2")}
    lik = [{} for _ in range(4)]
    for o, j in itertools.product(ORDERINGS, range(4)):
        d = lik[j].setdefault(toks[o][8 * j:8 * j + 8], {z: Fraction(0) for z in prior})
        d[truth[o]] += Fraction(1, nz[truth[o]])
    post = {o: block_posterior(prior, [lik[j][toks[o][8 * j:8 * j + 8]] for j in range(4)])
            for o in ORDERINGS}
    ctx, ll, reg = CTX[80], Decimal(0), Decimal(0)
    for o in ORDERINGS:
        r = post[o]
        q_add = [sum(r[z] * q_of[z][k] for z in r if r[z]) for k in range(18)]
        ll = ctx.subtract(ll, ctx.ln(ctx.divide(Decimal(r[truth[o]].numerator),
                                                Decimal(r[truth[o]].denominator))))
        reg = ctx.add(reg, kl_decimal(q_of[truth[o]], q_add, 80))
    n = Decimal(len(ORDERINGS))
    acc = Fraction(sum(max(post[o], key=post[o].get) == truth[o] for o in ORDERINGS), 24)
    return {"block_likelihoods": lik, "posteriors": post, "truth": truth, "accuracy": acc,
            "holonomy_logloss": ctx.divide(ll, n), "regret": ctx.divide(reg, n)}

# ---- G3, O1, O2 (API 5.6, sections 8.2-8.3) ----
_TAILS = {"W1": 4, "W2": 8, "W3": 9}
_BAGGED = {"W1": False, "W2": True, "W3": True}
_EQUAL_ROWS = ("length", "n", "end", "prefix", "cue", "parikh", "h1", "counts", "parity")
_H, _S = Fraction(1, 2), Fraction(1, 6)
_PER_Y = {"last": {"W1": (_H, -1, _H), "W2": (_H, -1, _H), "W3": (-_S, 2 * _S, -_S)},
          "first": {"W1": (-_H, 1, -_H), "W2": (-_H, 1, -_H), "W3": (_S, -2 * _S, _S)}}
_REV = {"W1": -1, "W2": -1, "W3": Fraction(1, 3)}
_ZERO_SPREAD = ("AB", "ZC", "TRIV", "GAUGE-TRIV")

def _cases():
    for fam in ("W1", "W2"):
        yield from ((fam, p, 0) for p in ("P0", "P1", "P3"))
        yield from ((fam, "P6", y0) for y0 in range(3))
    yield from (("W3", "P0", 0), ("W3p", "P0", 0))
def _ent(p) -> Decimal:
    return entropy_decimal(p, 80)
def _close(a: Decimal, b: Decimal) -> bool:
    return CTX[80].abs(CTX[80].subtract(a, b)) <= TOL_LOG
def _window_constant(fam: str) -> bool:
    """Bayes k-window predictors (stationary restart) constant on the set for k <= n."""
    m, mems = model("NA"), members(fam)
    for y, k in itertools.product(range(3), range(1, len(witness_path(fam, mems[0])) + 1)):
        qs = [fraction_filter(m["T"], m["E"], m["pi"], witness_tokens(fam, o, y)[-k:])["q"][-1]
              for o in mems]
        if any(q != qs[0] for q in qs):
            return False
    return True

def _matched_ok(f: str, m: dict) -> bool:
    bag = "equal" if _BAGGED[f] else "differs"
    return (all(m[k] == "equal" for k in _EQUAL_ROWS) and m["tail"] >= _TAILS[f] and
            m["bag"] == m["bigram"] == bag)
def gate_G3() -> dict:
    fams = {a: {f"{f}|{p}|{y0}": family_values(a, f, p, y0) for f, p, y0 in _cases()} for a in ARMS}
    keys = {f: {S: all(constant_by_keys(rs_key(S, witness_tokens(f, o, y, p, y0))
                                        for o in members(f))
                       for g, p, y0 in _cases() if g == f for y in range(3)) for S in LADDER}
            for f in ("W1", "W2", "W3", "W3p")}
    mat = {f: {y: matched(f, y) for y in range(3)} for f in ("W1", "W2", "W3")}
    bt, ch, comp = beta_table(), challenge_values(), {y: block_comparator(y) for y in range(3)}
    na, chk, gaps = fams["NA"], {}, {}
    chk["equal_P"] = all(fv["equal_P"] for d in fams.values() for fv in d.values())
    chk["tv"] = all(fv["tv_min"] == lam(fv["n"] + 1) for fv in na.values())
    chk["cue_laws"] = all(
        list(r["q"][y][15:18]) == [v / 5 for v in point_law(fv["n"] + 1, next(
            g for g in S3_LIST if perm_name(g) == r["holonomy"])[y])]
        for fv in na.values() for r in fv["members"].values() for y in range(3))
    chk["matched"] = all(_matched_ok(f, m) and m["trigram"] == "differs"
                         for f, d in mat.items() for m in d.values())
    chk["keys_constant"] = all(all(d.values()) for d in keys.values())
    for f, y in itertools.product(("W1", "W2", "W3", "W3p"), range(3)):
        fv = na[f"{f}|P0|0"]
        laws = [r["q"][y] for r in fv["members"].values()]
        cue = [[v / sum(q[15:18]) for v in q[15:18]] for q in laws]
        h_bar = _ent([sum(c) / len(cue) for c in zip(*cue)])
        closed = CTX[80].divide(CTX[80].subtract(h_bar, _ent(point_law(fv["n"] + 1, 0))), 5)
        gaps[f"{f}|{y}"] = {"value": set_gap(laws), "closed": closed}
    chk["set_gaps"] = all(_close(g["value"], g["closed"]) for g in gaps.values())
    chk["multiplicity"] = (na["W3|P0|0"]["multiplicity"] == {"e": 16, "c": 4, "c2": 4} and
                           fams["AB"]["W3|P0|0"]["multiplicity"] == {"e": 24, "c": 0, "c2": 0})
    chk["beta"] = bt["W3"]["rev"]["balanced"] == 0 and all(
        bt[f]["set_constant"]["pooled"] == 0 and bt[f]["rev"]["pooled"] == _REV[f] and
        all(bt[f][k]["pooled"] == 0 and tuple(bt[f][k]["per_y"]) == _PER_Y[k][f]
            for k in ("last", "first")) for f in _REV)
    chk["prefix_invariant"] = all(
        fams[a][f"{f}|{p}|{y0}"]["members"][o]["q"][y] == fams[a][f"{f}|P0|0"]["members"][o]["q"][y]
        for a in ARMS for f, p, y0 in _cases() for o in members(f) for y in range(3))
    chk["spread_zero"] = all(fams[a][c]["spread"] == 0 for a in _ZERO_SPREAD for c in fams[a])
    L, q_l, q_rot = lam(32), point_law(32, 0), point_law(32, 1)
    chk["challenge"] = (
        ch["prior"] == {"e": 4 * _S, "c": _S, "c2": _S} and
        all(v == 0 for v in ch["z_information_window"].values()) and
        all(list(ch["q_bar"][y]) == [(1 + L) / 3 if k == y else (2 - L) / 6 for k in range(3)] and
            _close(ch["delta_cue"][y], CTX[80].subtract(_ent(ch["q_bar"][y]), _ent(q_l))) and
            _close(ch["delta_challenge"][y], CTX[80].divide(ch["delta_cue"][y], 5))
            for y in range(3)))
    ll = CTX[80].divide(CTX[80].ln(Decimal("1.25")), 3)
    mix = [Fraction(4, 5) * a + Fraction(1, 5) * b for a, b in zip(q_rot, q_l)]
    reg = CTX[80].divide(kl_decimal(q_rot, mix, 80), 15)
    chk["comparator"] = all(
        c["accuracy"] == 1 and _close(c["holonomy_logloss"], ll) and _close(c["regret"], reg) and
        all((c["posteriors"][o]["e"], c["posteriors"][o][z]) ==
            ((1, 1) if z == "e" else (Fraction(1, 5), Fraction(4, 5)))
            for o, z in c["truth"].items())
        for c in comp.values())
    win = {f: _window_constant(f) for f in ("W1", "W2", "W3")}
    chk["window_constant"] = all(win.values())
    return {"status": "PASS" if all(chk.values()) else "FAIL", "checks": chk, "families": fams,
            "matched": mat, "keys_constant": keys, "beta": bt, "challenge": ch,
            "comparator": comp, "set_gaps": gaps, "prefix_invariant": chk["prefix_invariant"],
            "window_constant": win}

def o1(g3: dict) -> dict:
    per = {}
    for f in ("W1", "W2", "W3"):
        c = f"{f}|P0|0"
        per[f] = {"tv": g3["families"]["NA"][c]["tv_min"] >= TV_MIN,
                  "constant": all(_matched_ok(f, m) for m in g3["matched"][f].values()) and
                  all(g3["keys_constant"][f].values()) and g3["window_constant"][f],
                  "zero_spread": all(g3["families"][a][c]["spread"] == 0 for a in _ZERO_SPREAD)}
    ok = all(all(v.values()) for v in per.values())
    return {"status": "PASS" if ok else "FAIL", "per_family": per}

def o2_combine(c1: str, c2: str) -> str:
    return "PASS" if c1 == c2 == "PASS" else "FAIL" if "FAIL" in (c1, c2) else "UNCERTIFIED"
def o2(g4: dict) -> dict:
    na = g4["natural"]["NA"]
    c1 = certify(na["G"]["Parikh"][32], G_MIN)
    c2 = certify_mass(na["M32"]["lower"], na["M32"]["upper"], M_MIN)
    return {"G_parikh": c1, "M": c2, "status": o2_combine(c1, c2)}
