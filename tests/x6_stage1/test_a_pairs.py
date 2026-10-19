"""Author A: T-PAIR and T-BETA (X6S1-FROZEN-v1 §2.3, §10.2 T2-T5, T7, §14.3; API.md §4.2, §7).

Independent references live here: a (v, kappa) count DP, an exhaustive path enumerator, a
backward sampler written from §2.3, and exact Fraction pair sums. Histories are synthetic random
walks on the 4x4 torus (never a real pool)."""
from __future__ import annotations

import hashlib
import math
import random
import sys
from collections import defaultdict
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

if str(REPO / "tools" / "x6_stage0") not in sys.path:  # reused code (the modules add it too)
    sys.path.append(str(REPO / "tools" / "x6_stage0"))
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
from topo_pilot.contracts import SeedTree  # noqa: E402

ANCHOR, NB = 10, (6, 9, 11, 14)
LETTERS = ("x+", "x-", "y+", "y-")
T_SHORT, NMAX_SHORT = 20, 19


# ---------------------------------------------------------------- independent references
def _bump(k, u, v, d=1):
    lt = xm.seam_letter(u, v)
    if lt is None:
        return k
    i = LETTERS.index(lt)
    if k[i] + d < 0:
        return None
    return k[:i] + (k[i] + d,) + k[i + 1:]


@lru_cache(maxsize=None)
def my_counts(n_max: int) -> tuple:
    layers = [{(ANCHOR, (0, 0, 0, 0)): 1}]
    for _ in range(n_max):
        new = defaultdict(int)
        for (v, k), c in layers[-1].items():
            for j in xm.NEIGHBOURS[v]:
                if j != ANCHOR:
                    new[(j, _bump(k, v, j))] += c
        layers.append(dict(new))
    return tuple(layers)


def enumerate_classes(n: int) -> dict:
    """Every anchor-avoiding n-step path from the anchor, grouped by (v_t, kappa)."""
    out = defaultdict(list)

    def rec(path, k):
        if len(path) == n + 1:
            out[(path[-1], k)].append(tuple(path[1:]))
            return
        for j in xm.NEIGHBOURS[path[-1]]:
            if j != ANCHOR:
                rec(path + [j], _bump(k, path[-1], j))
    rec([ANCHOR], (0, 0, 0, 0))
    return out


def my_preds(counts, m, v, k):
    out = []
    for u in xm.NEIGHBOURS[v]:
        if (u == ANCHOR) != (m - 1 == 0):
            continue
        kp = _bump(k, u, v, -1)
        w = 0 if kp is None else counts[m - 1].get((u, kp), 0)
        if w:
            out.append((u, kp, w))
    return out


def my_sample(counts, v_t, kappa, n, rnd):
    """§2.3 backward sampler: randrange(c_m) per step, cumulative weights in NEIGHBOURS order."""
    path, v, k = [v_t], v_t, tuple(kappa)
    for m in range(n, 0, -1):
        r, acc = rnd.randrange(counts[m][(v, k)]), 0
        for u, kp, w in my_preds(counts, m, v, k):
            acc += w
            if r < acc:
                v, k = u, kp
                break
        path.append(v)
    return tuple(reversed(path[:-1]))


def my_segment(row, t):
    toks = [int(w) for w in row[:t]]
    cues = [i + 1 for i, w in enumerate(toks) if w >= 15]
    if not cues:
        return None
    s = cues[-1]
    path = (ANCHOR,) + tuple(xm.vertex(w) for w in toks[s:])
    return {"s": s, "y": toks[s - 1] - 15, "n": t - s, "v_t": path[-1],
            "kappa": xm.parikh(path), "path": path}


def my_r_ord(row, t) -> bool:
    g = my_segment(row, t)
    return g is not None and g["n"] >= 8 and g["v_t"] in NB


def walks(n_rows: int, seed: int) -> np.ndarray:
    """Synthetic positive-probability histories: random walk, a random cue at the anchor."""
    rng, out = np.random.default_rng(seed), np.zeros((n_rows, 33), np.uint8)
    for i in range(n_rows):
        v = int(rng.integers(16))
        for c in range(33):
            out[i, c] = 15 + int(rng.integers(3)) if v == ANCHOR else xm.tok(v)
            v = xm.NEIGHBOURS[v][int(rng.integers(5))]
    return out


@lru_cache(maxsize=None)
def pool():
    return walks(1500, 20261019)


@lru_cache(maxsize=None)
def short_tables():
    return sp.class_tables("NA", n_max=NMAX_SHORT)


def ord_rows(tokens, t):
    return [i for i in range(len(tokens)) if my_r_ord(tokens[i], t)]


def cue_frac(q):
    c = [Fraction(x) for x in q[15:18]]
    return tuple(x / sum(c) for x in c)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


# ---------------------------------------------------------------- T-PAIR
def test_tables_equal_independent_dp_and_validate():
    tables, ref = short_tables(), my_counts(NMAX_SHORT)
    assert tables[0] == {(10, (0, 0, 0, 0)): 1}
    for m in range(NMAX_SHORT + 1):
        got = {(int(v), tuple(int(x) for x in k)): int(c) for (v, k), c in tables[m].items()}
        assert got == ref[m], m
    assert [sum(ref[m].values()) for m in range(1, 6)] == [4, 16, 76, 352, 1684]
    # API-AMBIGUITY: validate_tables read as checking the layers present (n_max = 19 here)
    assert sp.validate_tables(tables)["status"] == "PASS"
    bad = {m: dict(layer) for m, layer in tables.items()}
    bad[3][next(iter(bad[3]))] += 1
    assert sp.validate_tables(bad)["status"] != "PASS"


def test_sampler_law_exhaustively_uniform_n_le_6():
    tables = short_tables()
    for n in range(1, 7):
        for (v, k), members in enumerate_classes(n).items():
            assert tables[n][(v, k)] == len(members)
            law = sp.sampler_law(tables, v, k, n)
            assert set(tuple(p) for p in law) == set(members), (n, v, k)
            assert all(p == Fraction(1, len(members)) for p in law.values())
            assert sum(law.values()) == 1
    assert sp.exhaustive_check(6)["status"] == "PASS"


def test_predecessors_sum_to_class_count():
    tables, ref = short_tables(), my_counts(NMAX_SHORT)
    rnd = random.Random(7)
    for m in (1, 2, 5, 9, 14, 19):
        for v, k in rnd.sample(sorted(ref[m]), min(25, len(ref[m]))):
            got = [(int(u), tuple(kp), int(w)) for u, kp, w in sp.predecessors(tables, m, v, k)]
            assert got == my_preds(ref, m, v, k)
            assert sum(w for _, _, w in got) == ref[m][(v, k)]


def test_sample_segment_equals_independent_backward_sampler():
    tables, ref = short_tables(), my_counts(NMAX_SHORT)
    rnd = random.Random(11)
    for n in (1, 3, 8, 12, 19):
        for v, k in rnd.sample(sorted(ref[n]), min(6, len(ref[n]))):
            for seed in range(5):
                got = tuple(sp.sample_segment(tables, v, k, n, random.Random(seed)))
                assert got == my_sample(ref, v, k, n, random.Random(seed))
                path = (ANCHOR,) + got
                assert len(got) == n and got[-1] == v and ANCHOR not in got
                assert all(b in xm.NEIGHBOURS[a] for a, b in zip(path, path[1:]))
                assert xm.parikh(path) == tuple(k)


def test_segment_parse_and_r_ord():
    toks = pool()
    for i in range(200):
        for t in (1, 9, 20, 32, 33):
            got, want = sp.segment(toks[i], t), my_segment(toks[i], t)
            if want is None:
                assert got is None
                continue
            assert all(got[k] == want[k] for k in ("s", "y", "n", "v_t"))
            assert tuple(got["kappa"]) == want["kappa"] and tuple(got["path"]) == want["path"]
            assert bool(sp.in_r_ord(toks[i], t)) == my_r_ord(toks[i], t)
    # hand case: cue y=1 at s=1, then 8 steps 9,5,1,13(seam x-),9,5,6,6 -> v_t = 6, n = 8
    h = (16,) + tuple(xm.tok(v) for v in (9, 5, 1, 13, 9, 5, 6, 6))
    row = np.array(h + (0,) * 24, np.uint8)
    g = sp.segment(row, 9)
    assert (g["s"], g["y"], g["n"], g["v_t"], tuple(g["kappa"])) == (1, 1, 8, 6, (0, 1, 0, 0))
    assert sp.in_r_ord(row, 9) and not sp.in_r_ord(row, 8)          # n = 7 < 8 at t = 8


def test_partner_seed_is_registered_stream():
    for pool_name, t, row in (("test_NA", 32, 0), ("test_NA", 16, 5), ("val_NA", 32, 77)):
        want = SeedTree(sd.DATA_MASTER).seed("x6s1", "partner", pool_name, t, row)
        assert sp.partner_seed(pool_name, t, row) == want


def test_partner_key_probability_validity_and_determinism():
    toks, tables, ref, t = pool(), short_tables(), my_counts(NMAX_SHORT), T_SHORT
    rows = ord_rows(toks, t)
    assert len(rows) >= 20
    for i in range(60):
        if i not in rows:
            assert sp.partner(tables, toks[i], t, "test_NA", i) is None
    for i in rows[:40]:
        h = tuple(int(w) for w in toks[i][:t])
        hp = tuple(int(w) for w in sp.partner(tables, toks[i], t, "test_NA", i))
        g = my_segment(toks[i], t)
        seed = SeedTree(sd.DATA_MASTER).seed("x6s1", "partner", "test_NA", t, i)
        seg = my_sample(ref, g["v_t"], g["kappa"], g["n"], random.Random(seed))
        assert hp == h[:g["s"]] + tuple(xm.tok(v) for v in seg)
        assert len(hp) == t and hp[:g["s"]] == h[:g["s"]] and max(hp[g["s"]:]) < 15
        xm.parse(hp)  # adjacency (raises on an illegal step)
        assert xe.rs_key("Parikh", hp) == xe.rs_key("Parikh", h)
        assert xm.closed_form("NA", hp)["P"] == xm.closed_form("NA", h)["P"]   # T2
        assert tuple(int(w) for w in sp.partner(tables, toks[i], t, "test_NA", i)) == hp


def test_partners_batch_rows_and_padding():
    toks, tables, t = pool()[:400], short_tables(), T_SHORT
    out = sp.partners(tables, toks, t, "test_NA")
    rows = ord_rows(toks, t)
    assert out["rows"].dtype == np.int64 and out["rows"].tolist() == rows
    assert out["tokens"].dtype == np.uint8 and out["tokens"].shape == (len(rows), 33)
    for r, i in enumerate(rows):
        hp = tuple(int(w) for w in sp.partner(tables, toks[i], t, "test_NA", i))
        assert tuple(int(w) for w in out["tokens"][r, :t]) == hp
        assert not out["tokens"][r, t:].any()


@pytest.mark.slow
def test_partner_full_tables_t32():
    toks, tables, ref = pool(), sp.class_tables("NA"), my_counts(31)
    for m in range(32):
        got = {(int(v), tuple(int(x) for x in k)): int(c) for (v, k), c in tables[m].items()}
        assert got == ref[m]
    for i in ord_rows(toks, 32)[:30]:
        h = tuple(int(w) for w in toks[i][:32])
        hp = tuple(int(w) for w in sp.partner(tables, toks[i], 32, "test_NA", i))
        assert xe.rs_key("Parikh", hp) == xe.rs_key("Parikh", h)
        assert xm.closed_form("NA", hp)["P"] == xm.closed_form("NA", h)["P"]


# ---------------------------------------------------------------- T-BETA
def _law(cue3, rest=0.0625):
    return np.concatenate([np.full(12, rest), np.zeros(3), np.array(cue3, np.float64)])


def test_pair_terms_hand_values():
    # dyadic laws: cue-normalised vectors are exact; num and den are exact by hand
    ph = np.array([_law((0.125, 0.0625, 0.0625)), _law((0.0625, 0.0625, 0.125))])
    ph2 = np.array([_law((0.0625, 0.125, 0.0625)), _law((0.0625, 0.0625, 0.125))])
    qh = np.array([_law((0.25, 0.0, 0.0)), _law((0.0, 0.125, 0.125))])
    qh2 = np.array([_law((0.0, 0.25, 0.0)), _law((0.125, 0.0, 0.125))])
    num, den = se.pair_terms(ph, ph2, qh, qh2)
    # row 0: dp = (1/4, -1/4, 0), dq = (1, -1, 0): num 1/2, den 2
    # row 1: dp = 0, dq = (-1/2, 1/2, 0): num 0, den 1/2
    assert num.dtype == np.float64 and num.tolist() == [0.5, 0.0]
    assert den.tolist() == [2.0, 0.5]
    assert se.beta_fsum(num, den) == 0.5 / 2.5
    # x6_exact.beta on the same pairs as two-member sets (centring halves num and den alike)
    rows = [(i, 1, cue_frac(q[i]), cue_frac(p[i]))
            for i in range(2) for q, p in ((qh, ph), (qh2, ph2))]
    assert xe.beta(rows) == Fraction(1, 5)
    assert se.beta_exact(num, den) == Fraction(1, 5)


def test_beta_fsum_and_exact_agree_t7():
    rng = np.random.default_rng(3)
    den = rng.uniform(0.5, 2.0, 5000)
    den[::7] = 0.0
    num = rng.uniform(-1.0, 1.0, 5000) * den
    want = sum(map(Fraction, num[den > 0])) / sum(map(Fraction, den[den > 0]))
    assert se.beta_exact(num, den) == want
    assert abs(se.beta_fsum(num, den) - float(want)) <= 1e-9
    assert se.beta_fsum(num, den) == math.fsum(num) / math.fsum(den)
    assert math.isnan(se.beta_fsum(np.zeros(3), np.zeros(3)))


def _parikh_function_law(tokens, t):
    """A synthetic predictor that is a function of the R_Parikh key only (Lemma P1)."""
    key = xe.rs_key("Parikh", tuple(int(w) for w in tokens[:t]))
    d = hashlib.sha256(repr(key).encode()).digest()
    p = np.full(18, 0.03)
    p[15:18] = [(d[0] + 1) / 2000, (d[1] + 1) / 2000, (d[2] + 1) / 2000]
    return p / p.sum()


def test_lemma_p1_exact_zero_and_oracle_normalisation():
    toks, tables, t = pool(), short_tables(), T_SHORT
    out = sp.partners(tables, toks, t, "test_NA")
    h, hp = toks[out["rows"]], out["tokens"]
    ph = np.array([_parikh_function_law(r, t) for r in h])
    ph2 = np.array([_parikh_function_law(r, t) for r in hp])
    qs = se.OraclePredictor("NA", "qstar")
    qh, qh2 = qs(h, t), qs(hp, t)
    num, den = se.pair_terms(ph, ph2, qh, qh2)
    assert np.all(num == 0.0)                                   # Lemma P1, exact
    num_q, den_q = se.pair_terms(qh, qh2, qh, qh2)
    assert np.array_equal(num_q, den_q)
    assert abs(se.beta_fsum(num_q, den_q) - 1.0) <= 1e-12                 # T3
    for i, r in enumerate(out["rows"][:10]):
        want = [float(x) for x in xm.closed_form("NA", tuple(int(w) for w in toks[r][:t]))["q"]]
        assert qh[i].tolist() == want


def test_q8_difference_on_r_ord_rows_t5():
    toks, tables, t = pool(), short_tables(), T_SHORT
    out = sp.partners(tables, toks[:300], t, "test_NA")
    q8 = se.OraclePredictor("NA", "q_8")
    d = q8(toks[:300][out["rows"][:8]], t) - q8(out["tokens"][:8], t)
    assert np.max(np.abs(d)) <= 1e-12


def _segment_only_f(seg):
    """Any rational function of the segment tokens alone (no cue, no prefix)."""
    a, b, c = 1 + sum(seg), 1 + seg[-2] * 3, 2 + len(set(seg))
    return tuple(Fraction(x, a + b + c) for x in (a, b, c))


def test_lemma_p2_zero_in_expectation_over_uniform_y():
    prefixes = [(), (6, 5, 9), (17, 13, 12, 9, 5, 9)]
    ref = my_counts(9)
    for n in (8, 9):
        keys = sorted(key for key, c in ref[n].items() if key[0] in NB and c > 1)
        for v, k in random.Random(n).sample(keys, 6):
            members = sorted({my_sample(ref, v, k, n, random.Random(s)) for s in range(8)})
            for g1, g2 in zip(members, members[1:3]):
                s1, s2 = (tuple(xm.tok(u) for u in g) for g in (g1, g2))
                f1, f2 = _segment_only_f(s1), _segment_only_f(s2)
                for pre in prefixes:
                    total, nums = Fraction(0), []
                    for y in range(3):
                        q1, q2 = (sp.q_exact("NA", h, len(h)) for h in
                                  (pre + (15 + y,) + s1, pre + (15 + y,) + s2))
                        total += dot(sub(f1, f2), sub(cue_frac(q1), cue_frac(q2)))
                        rows = [np.array([0.0] * 15 + [float(x) / 5 for x in f]) for f in (f1, f2)]
                        rows += [np.array([float(x) for x in q]) for q in (q1, q2)]
                        nums.append(se.pair_terms(*(r[None] for r in rows))[0][0])
                    assert total == 0                         # exact, every (gamma, gamma')
                    assert abs(math.fsum(nums)) <= 1e-14


def test_lemma_p2_scope_prefix_cue_counterexample():
    """L-E5: a predictor that combines the segment with a prefix cue is not covered by P2."""
    pre = xe.prefix_tokens("P6", 0)                          # cue y0 = 0, five steps, ends at 9
    q_pre = xm.closed_form("NA", pre)["q"]
    p_y = [q_pre[15 + y] / sum(q_pre[15:18]) for y in range(3)]
    assert len(set(p_y)) > 1                                 # y is not uniform given the prefix
    g1, g2 = xe.witness_path("W2", "AB"), xe.witness_path("W2", "BA")
    assert xm.parikh((ANCHOR,) + g1) == xm.parikh((ANCHOR,) + g2) and g1[-1] == g2[-1] == 14
    s1, s2 = tuple(xm.tok(u) for u in g1), tuple(xm.tok(u) for u in g2)

    def law(seg, y):
        h = pre + (15 + y,) + seg
        return cue_frac(sp.q_exact("NA", h, len(h)))

    def f(seg):                                              # uses prefix cue and segment only
        return tuple(sum(p_y[y] * law(seg, y)[c] for y in range(3)) for c in range(3))
    df = [a - b for a, b in zip(f(s1), f(s2))]
    dq = {y: [a - b for a, b in zip(law(s1, y), law(s2, y))] for y in range(3)}
    natural = sum(p_y[y] * dot(df, dq[y]) for y in range(3))
    uniform = sum(Fraction(1, 3) * dot(df, dq[y]) for y in range(3))
    assert natural == dot(df, df) and natural > 0           # non-zero under the natural law
    assert uniform == 0                                      # zero only for uniform y
