"""Author A: T-DESIGN (X6S1-FROZEN-v1 §2.5, §6.3, §14.3; API.md §4.3, §7 designed_stats).

Matched statistics, oracle spread, prefix invariance and the W2 beta table are recomputed here
from token tuples and exact Fractions; the natural-prefix rule has an independent implementation.
Prefix pools are synthetic random walks (never the registered prefix pool)."""
from __future__ import annotations

import functools
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_data as sd  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_stats as ss  # noqa: E402

if str(REPO / "tools" / "x6_stage0") not in sys.path:  # reused code (the modules add it too)
    sys.path.append(str(REPO / "tools" / "x6_stage0"))
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
from topo_pilot.contracts import SeedTree  # noqa: E402

ANCHOR, NB = 10, (6, 9, 11, 14)
S7 = (1, 2, 3, 7, 11, 15, 14)                     # W2 scaffolding tail (S0 §4.3)
STAGE0 = [("P0", 0), ("P1", 0), ("P3", 0), ("P6", 0), ("P6", 1), ("P6", 2)]
FAMILIES = {"W2": (("A+", "B+"), ("B+", "A+")), "C1": (("A+", "A-"), ("A-", "A+")),
            "C2": (("A+", "F"), ("F", "A+")), "C3": (("B+", "B-"), ("B-", "B+")),
            "C4": (("B+", "F"), ("F", "B+"))}
FLOOR = 1.012287e-6


def walks(n_rows: int, seed: int) -> np.ndarray:
    rng, out = np.random.default_rng(seed), np.zeros((n_rows, 33), np.uint8)
    for i in range(n_rows):
        v = int(rng.integers(16))
        for c in range(33):
            out[i, c] = 15 + int(rng.integers(3)) if v == ANCHOR else xm.tok(v)
            v = xm.NEIGHBOURS[v][int(rng.integers(5))]
    return out


@lru_cache(maxsize=None)
def prefix_pool():
    return walks(4096, 1810)


def my_natural_prefixes(tokens, rnd):
    out = []
    for row in tokens:
        lmax = int(rnd.integers(1, 15))                  # one call per row, skipped rows too
        ok = [L for L in range(1, lmax + 1) if xm.vertex(int(row[L - 1])) in NB + (ANCHOR,)]
        if ok and len(out) < 1024:
            out.append(tuple(int(w) for w in row[:ok[-1]]))
    return out


def my_history(prefix, letters, y):
    """API-AMBIGUITY: API §4.3 says 'prefix + cue + tokens of the loops ... as
    x6_exact.witness_tokens composes them'; read literally as witness_tokens does for W2,
    i.e. with the (9, 5) lead-in and the S7 tail (readout t = L + 18, protocol §2.5)."""
    loops = sum((sp.FLAT_FACE if lt == "F" else xe.LOOPS[lt] for lt in letters), ())
    return tuple(prefix) + (15 + y,) + tuple(xm.tok(v) for v in (9, 5) + loops + S7)


def segment_stats(h):
    s = max(i + 1 for i, w in enumerate(h) if w >= 15)
    path = (ANCHOR,) + tuple(xm.vertex(w) for w in h[s:])
    return {"n": len(h) - s, "v": path[-1], "kappa": xm.parikh(path), "y": h[s - 1] - 15}


def cue_frac(q):
    c = [Fraction(x) for x in q[15:18]]
    return tuple(x / sum(c) for x in c)


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def some_prefixes():
    nat = my_natural_prefixes(prefix_pool()[:64], np.random.default_rng(4))[:5]
    return [xe.prefix_tokens(p, y0) for p, y0 in STAGE0] + nat


# ---------------------------------------------------------------- constants and composition
def test_registered_constants_and_flat_face():
    assert sp.FLAT_FACE == (4, 8, 9, 5)
    assert sp.CONTROL_SETS == {k: v for k, v in FAMILIES.items() if k != "W2"}
    assert tuple(sp.STAGE0_PREFIXES) == ("P0", "P1", "P3", "P6")
    loop = (5,) + sp.FLAT_FACE                            # a closed loop at p = 5
    assert all(b in xm.NEIGHBOURS[a] and a != b for a, b in zip(loop, loop[1:]))
    assert ANCHOR not in loop and xm.parikh(loop) == (0, 0, 0, 0)


def test_designed_history_composition():
    for (p, y0), y in ((c, y) for c in STAGE0 for y in range(3)):
        pre = xe.prefix_tokens(p, y0)
        for mem, letters in zip(("AB", "BA"), FAMILIES["W2"]):
            got = tuple(int(w) for w in sp.designed_history(pre, letters, y))
            assert got == xe.witness_tokens("W2", mem, y, p, y0)
        for fam, (la, lb) in FAMILIES.items():
            for letters in (la, lb):
                got = tuple(int(w) for w in sp.designed_history(pre, letters, y))
                assert got == my_history(pre, letters, y) and len(got) == len(pre) + 18
                xm.parse(got)                             # every step legal


# ---------------------------------------------------------------- matched statistics
def test_matched_statistics_and_control_spread_zero():
    lam18 = xm.lam(18)
    for pre in some_prefixes():
        for y in range(3):
            for fam, (la, lb) in FAMILIES.items():
                a, b = my_history(pre, la, y), my_history(pre, lb, y)
                assert len(a) == len(b) and Counter(a) == Counter(b)            # token bag
                assert Counter(zip(a, a[1:])) == Counter(zip(b, b[1:]))         # directed bigrams
                assert segment_stats(a) == segment_stats(b)                     # n, v_t, kappa, y
                assert a[-8:] == b[-8:]                                         # last 8 symbols
                qa, qb = sp.q_exact("NA", a, len(a)), sp.q_exact("NA", b, len(b))
                if fam == "W2":
                    ca, cb = cue_frac(qa), cue_frac(qb)
                    assert sum(abs(x - z) for x, z in zip(ca, cb)) / 2 == lam18     # oracle TV
                else:
                    assert tuple(qa) == tuple(qb)                                # spread exactly 0
                    for arm in ("AB", "ZC"):
                        qa, qb = sp.q_exact(arm, a, len(a)), sp.q_exact(arm, b, len(b))
                        assert tuple(qa) == tuple(qb)
            for arm in ("AB", "ZC"):                     # abelian oracles: W2 spread exactly 0
                a, b = (my_history(pre, lt, y) for lt in FAMILIES["W2"])
                assert tuple(sp.q_exact(arm, a, len(a))) == tuple(sp.q_exact(arm, b, len(b)))


def test_prefix_invariance_of_qstar():
    pres = some_prefixes()
    for fam, pair in FAMILIES.items():
        for letters in pair:
            for y in range(3):
                laws = {tuple(sp.q_exact("NA", h, len(h))) for h in
                        (my_history(pre, letters, y) for pre in pres)}
                assert len(laws) == 1, (fam, letters, y)
                h = my_history((), letters, y)
                assert next(iter(laws)) == tuple(xm.closed_form("NA", h)["q"])


# ---------------------------------------------------------------- the W2 beta table
def _w2_beta(law_fn):
    per_y, tot_n, tot_d = [], Fraction(0), Fraction(0)
    for y in range(3):
        a, b = (my_history((), lt, y) for lt in FAMILIES["W2"])
        dq = sub(cue_frac(sp.q_exact("NA", a, len(a))), cue_frac(sp.q_exact("NA", b, len(b))))
        dp = sub(law_fn(a), law_fn(b))
        per_y.append(dot(dp, dq) / dot(dq, dq))
        tot_n, tot_d = tot_n + dot(dp, dq), tot_d + dot(dq, dq)
    return tuple(per_y), tot_n / tot_d


def test_w2_beta_table_and_per_cue_heuristics():
    h = Fraction(1, 2)                  # S0 §4.9: last (1/2, -1, 1/2), first (-1/2, 1, -1/2)
    want = {"last": ((h, -1, h), 0), "first": ((-h, 1, -h), 0), "rev": ((-1, -1, -1), -1)}
    ref = xe.beta_table()["W2"]
    for kind, (per_y, pooled) in want.items():
        got = _w2_beta(lambda tok, k=kind: cue_frac(sp.q_heuristic(k, tok, len(tok))))
        assert got == (per_y, pooled), kind
        assert tuple(ref[kind]["per_y"]) == per_y and ref[kind]["pooled"] == pooled
    assert _w2_beta(lambda tok: cue_frac(sp.q_exact("NA", tok, len(tok)))) == ((1, 1, 1), 1)
    third = (Fraction(1, 3),) * 3
    assert _w2_beta(lambda tok: third) == ((0, 0, 0), 0)            # set-constant competitor
    # x6_exact.beta with each pair as a two-member set gives the same pooled value
    rows = []
    for y in range(3):
        for lt in FAMILIES["W2"]:
            tok = my_history((), lt, y)
            rows.append((y, 1, cue_frac(sp.q_exact("NA", tok, len(tok))),
                         cue_frac(sp.q_heuristic("rev", tok, len(tok)))))
    assert xe.beta(rows) == -1


@pytest.mark.slow
def test_w2_beta_zero_for_every_ladder_statistic():
    for S in xm.LADDER:          # q_S is constant on each W2 set: matched key, beta exactly 0
        got = _w2_beta(lambda tok, s=S: cue_frac(sp.q_stat(s, tok, len(tok))))
        assert got == ((0, 0, 0), 0), S


# ---------------------------------------------------------------- natural prefixes and D
def test_natural_prefix_rule_independent():
    toks = prefix_pool()
    got = sp.natural_prefixes(toks, np.random.default_rng(99))
    want = my_natural_prefixes(toks, np.random.default_rng(99))
    assert [tuple(int(w) for w in p) for p in got] == want and len(want) == 1024
    for p in want:
        assert 1 <= len(p) <= 14 and xm.vertex(p[-1]) in NB + (ANCHOR,)


@lru_cache(maxsize=None)
def designed():
    return sp.designed_set(prefix_pool())


def test_designed_set_structure():
    D = designed()
    pres = [tuple(int(w) for w in tok) for _, tok in D["prefixes"]]
    assert len(pres) == 1030
    assert set(pres[:6]) == {xe.prefix_tokens(p, y0) for p, y0 in STAGE0}
    rnd = SeedTree(sd.DATA_MASTER).generator("x6s1", "prefix_len")
    assert pres[6:] == my_natural_prefixes(prefix_pool(), rnd)
    for fam, (la, lb) in FAMILIES.items():
        pairs = D[fam]
        assert len(pairs) == 3090, fam
        seen = set()
        for pr in pairs:
            pre, y = pres[pr["prefix"]], pr["y"]
            a, b = tuple(int(w) for w in pr["a"]), tuple(int(w) for w in pr["b"])
            assert {a, b} == {my_history(pre, la, y), my_history(pre, lb, y)}
            assert pr["t"] == len(a) == len(pre) + 18 <= 32
            seen.add((pr["prefix"], y))
        assert len(seen) == 3090
    # API-AMBIGUITY: "W3" read as 72 token histories (tuples) at t = 32
    w3 = {tuple(int(w) for w in h) for h in D["W3"]}
    assert len(D["W3"]) == 72
    assert w3 == {xe.witness_tokens("W3", o, y) for o in xe.ORDERINGS for y in range(3)}
    assert all(len(h) == 32 for h in w3)


def test_designed_arrays_and_digest():
    D = designed()
    A = sp.designed_arrays(D)
    for fam in FAMILIES:
        a, b, t, y = A[f"{fam}_a"], A[f"{fam}_b"], A[f"{fam}_t"], A[f"{fam}_y"]
        assert a.dtype == b.dtype == np.uint8 and a.shape == b.shape == (3090, 33)
        assert t.dtype == np.int16 and y.dtype == np.int8 and t.shape == y.shape == (3090,)
        for i in (0, 1, 500, 3089):
            pr = D[fam][i]
            assert tuple(a[i, :t[i]]) == tuple(int(w) for w in pr["a"]) and not a[i, t[i]:].any()
            assert tuple(b[i, :t[i]]) == tuple(int(w) for w in pr["b"]) and int(y[i]) == pr["y"]
    h1 = sp.designed_sha256(A)
    assert len(h1) == 64 and h1 == h1.lower() and h1 == sp.designed_sha256(sp.designed_arrays(D))
    B = {k: v.copy() for k, v in A.items()}
    B["W2_a"][0, 0] ^= 1
    assert sp.designed_sha256(B) != h1


# ---------------------------------------------------------------- designed statistics (oracles)
@pytest.mark.slow
def test_designed_stats_oracle_and_heuristic_references():
    A = sp.designed_arrays(designed())
    tables = ss.log_tables()
    # API-AMBIGUITY: qstar_fn read as a callable (tokens, t) -> se.qstar("NA", tokens, t)
    qfn = functools.partial(se.qstar, "NA")
    q = se.designed_stats(se.OraclePredictor("NA", "qstar"), A, qfn, tables)
    assert abs(q["beta_W2"] - 1) <= 1e-12 and all(abs(b - 1) <= 1e-12 for b in q["beta_W2_y"])
    assert q["rho_C"] == 0.0 and abs(q["rho_W2"] - 1) <= 1e-12
    assert 0 <= q["R_W2"] <= FLOOR + 1e-12 and 0 <= q["Delta_W3"] <= FLOOR + 1e-12   # T17
    assert q["cue_mass_median"] >= 0.1 and q["nonfinite"] is False
    last = se.designed_stats(se.OraclePredictor("NA", "h_last"), A, qfn, tables)
    assert [round(b, 12) for b in last["beta_W2_y"]] == [0.5, -1.0, 0.5]
    assert abs(last["beta_W2"]) <= 1e-12 and abs(last["rho_C"]) <= 1e-12
    assert abs(last["rho_W2"] - 1) <= 1e-12
    first = se.designed_stats(se.OraclePredictor("NA", "h_first"), A, qfn, tables)
    assert [round(b, 12) for b in first["beta_W2_y"]] == [-0.5, 1.0, -0.5]
    rev = se.designed_stats(se.OraclePredictor("NA", "h_rev"), A, qfn, tables)
    assert abs(rev["beta_W2"] + 1) <= 1e-12 and abs(rev["rho_C"]) <= 1e-12
    par = se.designed_stats(se.OraclePredictor("NA", "q_Parikh"), A, qfn, tables)
    assert par["beta_W2"] == 0.0 and par["rho_C"] == 0.0
    assert par["R_W2"] >= float(Fraction("0.0611193713418965")) - 1e-9   # >= set gap (S0 Thm 5)
    for arm in ("AB", "ZC"):     # abelian oracles: own within-set variance exactly 0
        ab = se.designed_stats(se.OraclePredictor(arm, "qstar"), A, qfn, tables)
        assert ab["rho_W2"] == 0.0 and ab["rho_C"] == 0.0
