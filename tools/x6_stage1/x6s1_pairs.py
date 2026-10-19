"""X6S1 pairs: Parikh class tables, segment parse, the exact backward partner sampler and its
exhaustive check, the designed set D, and the oracle laws of the references (X6S1-FROZEN-v1
§2.3, §2.5, §6.3, §8 G0-ORC (c)-(d), (g); API.md §4). Import performs no I/O."""
# fmt: off

from __future__ import annotations

import hashlib
import random
import sys
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent)) if str(
    Path(__file__).resolve().parent) not in sys.path else None
import numpy as np  # noqa: E402
import x6_dp as xd  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_data as sd  # noqa: E402

from topo_pilot.contracts import SeedTree, canonical_json  # noqa: E402

ANCHOR, NB, LETTERS = xm.ANCHOR, xm.ANCHOR_NB, ("x+", "x-", "y+", "y-")
FLAT_FACE = (4, 8, 9, 5)
CONTROL_SETS = {"C1": (("A+", "A-"), ("A-", "A+")), "C2": (("A+", "F"), ("F", "A+")),
                "C3": (("B+", "B-"), ("B-", "B+")), "C4": (("B+", "F"), ("F", "B+"))}
W2_LETTERS = (("A+", "B+"), ("B+", "A+"))
STAGE0_PREFIXES = ("P0", "P1", "P3", "P6")
STAGE0_NAMED = (("P0", 0), ("P1", 0), ("P3", 0), ("P6", 0), ("P6", 1), ("P6", 2))
_S7 = (1, 2, 3, 7, 11, 15, 14)  # W2 scaffolding tail (x6_exact, S0 §4.3)
PAIR_FAMILIES = ("W2", "C1", "C2", "C3", "C4", "W1")


# ---- class tables (API 4.1; G0-ORC (c)) ----
@lru_cache(maxsize=None)
def class_tables(arm="NA", n_max=31) -> dict:
    tables = {}
    for m, layer in xd.segment_dp(arm, n_max):
        acc = defaultdict(int)
        for (v, k, _g), c in layer.items():
            acc[(v, k)] += c
        tables[m] = dict(acc)
    return tables


def tables_bytes(tables) -> bytes:
    rows = sorted([m, v, list(k), c] for m, layer in tables.items() for (v, k), c in layer.items())
    return canonical_json(rows).encode("utf-8")


def save_tables(path, tables) -> str:
    data = tables_bytes(tables)
    with open(path, "xb") as fh:
        fh.write(data)
    return hashlib.sha256(data).hexdigest()


def load_tables(path, sha256) -> dict:
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != str(sha256).lower():
        raise ValueError(f"class table hash mismatch: {path}")
    import json

    out = defaultdict(dict)
    for m, v, k, c in json.loads(data):
        out[m][(v, tuple(k))] = c
    return dict(out)


def validate_tables(tables) -> dict:
    """Σ_{v ≠ a★, κ} c_m equals x6_dp.avoid_counts totals for every layer m ≥ 1 present."""
    A = xd.avoid_counts(31)["A"]
    bad = [m for m, layer in tables.items() if m >= 1 and
           sum(c for (v, _k), c in layer.items() if v != ANCHOR) != A[m]]
    ok = not bad and tables.get(0) == {(ANCHOR, (0, 0, 0, 0)): 1}
    return {"status": "PASS" if ok else "FAIL", "totals_ok": not bad, "detail": {"bad": bad}}


# ---- segment parse and partner sampler (API 4.2; §2.3) ----
def segment(tokens, t):
    toks = [int(w) for w in tokens[:t]]
    cues = [i + 1 for i, w in enumerate(toks) if w >= 15]
    if not cues:
        return None
    s = cues[-1]
    path = (ANCHOR,) + tuple(xm.vertex(w) for w in toks[s:])
    return {"s": s, "y": toks[s - 1] - 15, "n": t - s, "v_t": path[-1],
            "kappa": xm.parikh(path), "path": path}


def in_r_ord(tokens, t) -> bool:
    g = segment(tokens, t)
    return g is not None and g["n"] >= sd.N_MIN and g["v_t"] in NB


def _bump(k, u, v, d):
    lt = xm.seam_letter(u, v)
    if lt is None:
        return k
    i = LETTERS.index(lt)
    return None if k[i] + d < 0 else k[:i] + (k[i] + d,) + k[i + 1:]


def predecessors(tables, m, v, kappa) -> list:
    out, k = [], tuple(kappa)
    for u in xm.NEIGHBOURS[v]:
        kp = _bump(k, u, v, -1)
        w = 0 if kp is None else tables[m - 1].get((u, kp), 0)
        if w:
            out.append((u, kp, w))
    return out


def sample_segment(tables, v_t, kappa, n, rnd: random.Random) -> tuple:
    path, v, k = [v_t], v_t, tuple(kappa)
    for m in range(n, 0, -1):
        r, acc = rnd.randrange(tables[m][(v, k)]), 0
        for u, kp, w in predecessors(tables, m, v, k):
            acc += w
            if r < acc:
                v, k = u, kp
                break
        path.append(v)
    return tuple(reversed(path[:-1]))


def partner_seed(pool, t, row) -> int:
    return SeedTree(sd.DATA_MASTER).seed("x6s1", "partner", pool, t, row)


def partner(tables, tokens, t, pool, row):
    if not in_r_ord(tokens, t):
        return None
    g = segment(tokens, t)
    seg = sample_segment(tables, g["v_t"], g["kappa"], g["n"],
                         random.Random(partner_seed(pool, t, int(row))))
    return tuple(int(w) for w in tokens[:g["s"]]) + tuple(xm.tok(v) for v in seg)


def partners(tables, pool_tokens, t, pool, rows=None) -> dict:
    rows = range(len(pool_tokens)) if rows is None else rows
    keep, out = [], []
    for i in rows:
        hp = partner(tables, pool_tokens[i], t, pool, i)
        if hp is not None:
            keep.append(int(i))
            out.append(hp)
    toks = np.zeros((len(out), sd.N_OBS), np.uint8)
    for r, hp in enumerate(out):
        toks[r, :t] = hp
    return {"rows": np.asarray(keep, np.int64), "tokens": toks}


def sampler_law(tables, v_t, kappa, n) -> dict:
    law = {}

    def rec(m, v, k, suffix, p):
        if m == 0:
            law[tuple(suffix)] = law.get(tuple(suffix), 0) + p
            return
        c = tables[m][(v, k)]
        for u, kp, w in predecessors(tables, m, v, k):
            rec(m - 1, u, kp, ([u] if m > 1 else []) + suffix, p * Fraction(w, c))
    rec(n, v_t, tuple(kappa), [v_t], Fraction(1))
    return law


def exhaustive_check(n_max=6) -> dict:
    tables, bad, classes = class_tables("NA", n_max), [], 0
    for n in range(1, n_max + 1):
        for (v, k), c in tables[n].items():
            law, classes = sampler_law(tables, v, k, n), classes + 1
            if len(law) != c or sum(law.values()) != 1 or any(
                    p != Fraction(1, c) for p in law.values()):
                bad.append([n, v, list(k)])
    return {"status": "FAIL" if bad else "PASS", "classes": classes, "detail": {"bad": bad}}


# ---- designed set D (API 4.3; §2.5, §6.3) ----
def natural_prefixes(prefix_tokens, rnd_len: np.random.Generator) -> list:
    out = []
    for row in prefix_tokens:
        lmax = int(rnd_len.integers(1, 15))  # one call per row, skipped rows included
        ok = [L for L in range(1, lmax + 1) if xm.vertex(int(row[L - 1])) in NB | {ANCHOR}]
        if ok and len(out) < 1024:
            out.append(tuple(int(w) for w in row[:ok[-1]]))
    return out


def _loops(letters) -> tuple:
    return sum((FLAT_FACE if lt == "F" else xe.LOOPS[lt] for lt in letters), ())


def designed_history(prefix, letters, y) -> tuple:
    path = (9, 5) + _loops(letters) + _S7
    return tuple(int(w) for w in prefix) + (15 + int(y),) + tuple(xm.tok(v) for v in path)


def _w1_history(prefix, member, y) -> tuple:
    path = xe.witness_path("W1", member)
    return tuple(int(w) for w in prefix) + (15 + int(y),) + tuple(xm.tok(v) for v in path)


def designed_set(prefix_pool) -> dict:
    rnd = SeedTree(sd.DATA_MASTER).generator("x6s1", "prefix_len")
    named = [(f"{p}|{y0}", xe.prefix_tokens(p, y0)) for p, y0 in STAGE0_NAMED]
    nat = [(f"N{i}", p) for i, p in enumerate(natural_prefixes(prefix_pool, rnd))]
    pres, D = named + nat, {}
    D["prefixes"] = pres
    for fam, (la, lb) in (("W2", W2_LETTERS),) + tuple(CONTROL_SETS.items()):
        D[fam] = [{"a": designed_history(pre, la, y), "b": designed_history(pre, lb, y), "y": y,
                   "prefix": i, "t": len(pre) + 18} for i, (_, pre) in enumerate(pres)
                  for y in range(3)]
    D["W1"] = [{"a": _w1_history(pre, "U", y), "b": _w1_history(pre, "D", y), "y": y,
                "prefix": i, "t": len(pre) + 8} for i, (_, pre) in enumerate(pres)
               for y in range(3)]
    for fam in ("W3", "W3p"):
        D[fam] = [xe.witness_tokens(fam, o, y) for o in xe.ORDERINGS for y in range(3)]
    return D


def _pad(rows) -> np.ndarray:
    out = np.zeros((len(rows), sd.N_OBS), np.uint8)
    for i, h in enumerate(rows):
        out[i, :len(h)] = h
    return out


def designed_arrays(D) -> dict:
    A = {}
    for fam in PAIR_FAMILIES:
        P = D[fam]
        A[f"{fam}_a"], A[f"{fam}_b"] = _pad([p["a"] for p in P]), _pad([p["b"] for p in P])
        A[f"{fam}_t"] = np.asarray([p["t"] for p in P], np.int16)
        A[f"{fam}_y"] = np.asarray([p["y"] for p in P], np.int8)
    for fam in ("W3", "W3p"):  # sets, not pairs: histories, readout t and cue y (§13 item 18)
        A[f"{fam}_a"] = _pad(D[fam])
        A[f"{fam}_t"] = np.asarray([len(h) for h in D[fam]], np.int16)
        A[f"{fam}_y"] = np.asarray([y for _o in xe.ORDERINGS for y in range(3)], np.int8)
    return A


def designed_sha256(arrays) -> str:
    h = hashlib.sha256()
    for key in sorted(arrays):
        a = np.ascontiguousarray(arrays[key])
        h.update(key.encode() + b"\x00" + a.dtype.str.encode() + b"\x00")
        h.update(np.asarray(a.shape, "<i8").tobytes() + a.tobytes())
    return h.hexdigest()


def gap_enclosures() -> dict:
    """Δ_W2 (y = 0, the two W2 members) and Δ_W3 (y = 0, the 24 W3 orderings) as 80/120-digit
    enclosures of x6_exact.set_gap over the unchanged exact laws (G0-ORC (g))."""
    sets = {"Delta_W2": [xe.witness_tokens("W2", m, 0) for m in xe.members("W2")],
            "Delta_W3": [xe.witness_tokens("W3", o, 0) for o in xe.ORDERINGS]}
    out = {}
    for name, toks in sets.items():
        laws = [xm.closed_form("NA", h)["q"] for h in toks]
        v80, v120 = xe.set_gap(laws, 80), xe.set_gap(laws, 120)
        enc = xd.enclosure(v80, v120, v80, len(laws))
        out[name] = {k: str(enc[k]) for k in ("lo", "hi", "v80", "v120")}
    return out


# ---- oracle laws for the references (API 4.4) ----
def _hist(tokens, t) -> tuple:
    return tuple(int(w) for w in tokens[:t])


def q_exact(arm, tokens, t) -> tuple:
    return tuple(xm.closed_form(arm, _hist(tokens, t))["q"])


def _with_cue(q, m, w) -> tuple:
    lm, q = xm.lam(m), list(q)
    for z in range(3):
        q[xm.cue(z)] = xm.P_MOVE * (lm * w[z] + (1 - lm) / 3)
    return tuple(q)


def q_stat(S, tokens, t) -> tuple:
    """Exact Bayes law given R_S (x6_run.gate_G6 semantics; class tables of x6_dp)."""
    h = _hist(tokens, t)
    q, p = q_exact("NA", h, t), xm.parse(h)
    if p["segment"] is None or p["n"] < 1 or p["v"] not in NB:
        return q
    key = (p["v"], xm.statistic(S, xm.parikh(p["segment"])))
    w = xd.weights(sd.holonomy_classes("NA")[S][p["n"]][key], p["y"])
    return _with_cue(q, p["n"] + 1, w)


def q_window(tokens, t, k=8) -> np.ndarray:
    from oracle_profile import suffix_posterior

    from topo_pilot.oracle import FutureOperator

    m = sd.arm_model("NA")
    toks = np.asarray(_hist(tokens, t), np.int64)[None, :]
    b = suffix_posterior(m["Tf"], m["Ef"], m["pif"], toks, min(k, t))
    return FutureOperator(m["Tf"], m["Ef"]).F1(b)[0]


def q_heuristic(kind, tokens, t) -> tuple:
    """The competitor's law: the segment holonomy replaced by competitor_holonomy(kind, seam
    labels along the segment), composed as x6_exact.beta_table does."""
    h = _hist(tokens, t)
    q, p = q_exact("NA", h, t), xm.parse(h)
    if p["segment"] is None:
        return q
    lab, path = xm.edge_labels("NA"), p["segment"]
    lets = [lab[(u, v)] for u, v in zip(path, path[1:]) if xm.seam_letter(u, v)]
    alt = xe.competitor_holonomy(kind, lets)
    if not any(j == ANCHOR for j in xm.NEIGHBOURS[p["v"]]):
        return q
    return _with_cue(q, p["n"] + 1, xm.point_law(0, alt[p["y"]]))
