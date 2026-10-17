"""X6 stage 0 independent tests (X6-FROZEN-v1 section 10.4: tests 1-5, 9, 13, 14), written from
the protocol and API.md only; references use the protocol's formulas (Fractions, ints, Decimal),
never a module kernel. test_x6_stage0_dp.py reuses the helpers below."""

from __future__ import annotations

import itertools
import sys
from collections import Counter
from decimal import Context, Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools" / "x6_stage0"
for _p in (TOOLS, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
from topo_pilot.world import CubicalComplex  # noqa: E402

# ---- independent reference (protocol sections 0, 2.3-2.6 and 4) ----
E0, A, B, C, C2, TT = (0, 1, 2), (1, 0, 2), (0, 2, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0)
S3 = (E0, A, B, C, C2, TT)
NAME = dict(zip(S3, ("e", "a", "b", "c", "c2", "t")))
ETA, ANC, NB = F(1, 50), 10, {6, 9, 11, 14}
ARMS = ("NA", "AB", "ZC", "TRIV", "ETA1", "GAUGE-NA", "GAUGE-TRIV", "GAUGE-COV")
SEAM_ARMS = ARMS[:4]  # the eta = 1/50 seam-supported arms
SEAM = {"NA": (A, B), "AB": (A, A), "ZC": (C, C), "TRIV": (E0, E0), "ETA1": (A, B)}
H_COV = tuple(S3[i % 6] for i in range(16))
H_FIX = H_COV[:10] + (E0,) + H_COV[11:]
GAUGE = {"GAUGE-NA": ("NA", H_FIX), "GAUGE-TRIV": ("TRIV", H_FIX), "GAUGE-COV": ("NA", H_COV)}
LOOPS = {"A+": (9, 13, 1, 5), "A-": (1, 13, 9, 5), "B+": (6, 7, 4, 5), "B-": (4, 7, 6, 5)}
ORDS = list(itertools.permutations(("A+", "A-", "B+", "B-")))
FACETS = ((0, 1), (2, 3), (0, 2), (1, 3))  # vertex pairs of a local-lexicographic square


def comp(g, h):
    return tuple(g[h[x]] for x in range(3))

def inv(g):
    return tuple(g.index(x) for x in range(3))

def nbrs(i):  # (+x, -x, +y, -y, stay)
    x, y = divmod(i, 4)
    return (4 * ((x + 1) % 4) + y, 4 * ((x - 1) % 4) + y, 4 * x + (y + 1) % 4,
            4 * x + (y - 1) % 4, i)

def letter(i, j):
    (xi, yi), (xj, yj) = divmod(i, 4), divmod(j, 4)
    if yi == yj and {xi, xj} == {0, 3}:
        return "x+" if xi == 3 else "x-"
    if xi == xj and {yi, yj} == {0, 3}:
        return "y+" if yi == 3 else "y-"
    return None

def labels(arm):
    base, h = GAUGE.get(arm, (arm, None))
    gx, gy = SEAM[base]
    lab = {"x+": gx, "x-": inv(gx), "y+": gy, "y-": inv(gy), None: E0}
    out = {(i, j): lab[letter(i, j)] for i in range(16) for j in nbrs(i)}
    return out if h is None else {(i, j): comp(h[j], comp(g, inv(h[i])))
                                  for (i, j), g in out.items()}

def tok(i):
    return i if i < 10 else i - 1

def lam(m, eta=ETA):
    return (1 - eta) ** m

def mu(m, z, eta=ETA):
    return [(1 - lam(m, eta)) / 3 + (lam(m, eta) if k == z else 0) for k in range(3)]

def hol(path, lab):
    g = E0
    for u, v in zip(path, path[1:]):
        g = comp(lab[(u, v)], g)
    return g

def lift(arm):
    eta, T = (F(1) if arm == "ETA1" else ETA), [[F(0)] * 48 for _ in range(48)]
    for (i, j), g in labels(arm).items():
        for x, x2 in itertools.product(range(3), range(3)):
            T[3 * i + x][3 * j + x2] = F(1, 5) * ((1 - eta) * int(x2 == g[x]) + eta / 3)
    return T

def emis(kind="E"):
    M = [[F(0)] * (16 if kind == "E_nc" else 18) for _ in range(48)]
    for s in range(48):
        i, x = divmod(s, 3)
        xx = inv(H_COV[i])[x] if kind == "E_cov" else x
        w = i if kind == "E_nc" else (15 + xx if i == ANC else tok(i))
        M[s][(w + 7) % 15 if kind == "E_sigma" and w <= 14 else w] = F(1)
    return M

def filt(T, E, toks):
    """Exact forward filter (emit, then transition; pi = 1/48): ([q_0..q_t], P, [b_1..b_t])."""
    pred, P, qs, bs = [F(1, 48)] * 48, F(1), [], []
    for w in list(toks) + [None]:
        qs.append([sum(pred[s] * E[s][k] for s in range(48) if pred[s]) for k in range(len(E[0]))])
        if w is None:
            return qs, P, bs
        a = [pred[s] * E[s][w] for s in range(48)]
        if (z := sum(a)) == 0:
            return qs, F(0), bs
        P, b = P * z, [v / z for v in a]
        bs.append(b)
        pred = [sum(b[i] * T[i][j] for i in range(48) if b[i]) for j in range(48)]

def w_path(fam, mem):  # vertices v_2..v_t after the cue (section 4)
    if fam == "W1":
        return (14, 15, 3 if mem == "U" else 12, 0, 4, 5, 6)
    if fam == "W2":
        x, y = ("A+", "B+") if mem == "AB" else ("B+", "A+")
        return (9, 5) + LOOPS[x] + LOOPS[y] + (1, 2, 3, 7, 11, 15, 14)
    return (6, 5) + (5,) * 5 + sum((LOOPS[k] for k in mem), ()) + (5,) * 7 + (6,)

def w_tokens(fam, mem, y):
    return (15 + y,) + tuple(tok(v) for v in w_path(fam, mem))

def dec(fr, prec=90):
    with localcontext() as ctx:
        ctx.prec = prec
        return Decimal(F(fr).numerator) / Decimal(F(fr).denominator)

def dkl(p, q, prec=80):
    with localcontext() as ctx:
        ctx.prec = p10 = prec + 10
        return sum((dec(a, p10) * dec(F(a) / F(b), p10).ln() for a, b in zip(p, q) if a),
                   Decimal(0))

def dent(p):
    with localcontext() as ctx:
        ctx.prec = 90
        return -sum((dec(a) * dec(a).ln() for a in p if a), Decimal(0))


@pytest.fixture(scope="module")
def spec():
    return xm.build_world()


def test_01_literal_conventions():  # section 10.4 test 1
    assert (xm.S3_E, xm.S3_A, xm.S3_B, xm.S3_C, xm.S3_C2, xm.S3_T) == S3 == tuple(xm.S3_LIST)
    assert comp(A, B) == C and comp(B, A) == C2  # a o b = c, b o a = c^2 (section 0)
    for g, h in itertools.product(S3, S3):
        assert tuple(xm.compose(g, h)) == comp(g, h)
    assert all(tuple(xm.inverse(g)) == inv(g) and xm.perm_name(g) == NAME[g] for g in S3)
    table = {0: (4, 12, 1, 3, 0), 5: (9, 1, 6, 4, 5), 10: (14, 6, 11, 9, 10),
             15: (3, 11, 12, 14, 15)}  # literal rows of the section 2.5 table
    assert all(nbrs(i) == row for i, row in table.items())
    assert tuple(tuple(r) for r in xm.NEIGHBOURS) == tuple(nbrs(i) for i in range(16))
    for i in range(16):
        assert all(xm.state(i, x) == 3 * i + x for x in range(3))
        assert all(tuple(xm.split_state(3 * i + x)) == (i, x) for x in range(3))
        assert all(xm.seam_letter(i, j) == letter(i, j) for j in nbrs(i))
        if i != ANC:
            assert xm.tok(i) == tok(i) and xm.vertex(tok(i)) == i
    for bad in (ANC, -1, 16):
        with pytest.raises(ValueError):
            xm.tok(bad)
    assert all(xm.cue(x) == 15 + x and xm.vertex(15 + x) == ANC for x in range(3))
    plus = {lt: {(i, j) for i in range(16) for j in nbrs(i) if letter(i, j) == lt}
            for lt in ("x+", "y+")}
    assert plus == {"x+": {(12, 0), (13, 1), (14, 2), (15, 3)},
                    "y+": {(3, 0), (7, 4), (11, 8), (15, 12)}}
    assert xm.ANCHOR == 10 and set(xm.ANCHOR_NB) == NB and xm.V == 18 and xm.N_S == 48
    assert xm.ETA == ETA and xm.P_MOVE == F(1, 5) and tuple(xm.F_STAR_ROW) == (15, 12, 3, 0)


def cover_cells(spec, lab):  # Lemma 0' lifting, coded independently
    c1 = [[3 * i + x, 3 * j + lab[(i, j)][x]] for i, j in spec.cells[1].tolist()
          for x in range(3)]
    c2 = [[3 * r0 + x, 3 * r1 + lab[(r0, r1)][x], 3 * r2 + lab[(r0, r2)][x],
           3 * r3 + lab[(r2, r3)][lab[(r0, r2)][x]]]
          for r0, r1, r2, r3 in spec.cells[2].tolist() if sorted((r0, r1, r2, r3)) != [0, 3, 12, 15]
          for x in range(3)]
    return c1, c2

def edge_use(squares):
    return Counter(frozenset((sq[a], sq[b])) for sq in squares for a, b in FACETS)

def boundary_components(c1, c2):
    use, parent = edge_use(c2), {}
    def root(v):
        while parent.setdefault(v, v) != v:
            v = parent[v]
        return v
    for u, v in (e for e in c1 if use[frozenset(e)] == 1):
        parent[root(u)] = root(v)
    return len({root(v) for v in list(parent)})


def test_02_kernel_lift_complexes_covers(spec):  # section 10.4 test 2
    tb = [[F(1, 5) if j in nbrs(i) else F(0) for j in range(16)] for i in range(16)]
    assert xm.t_base_exact() == tb
    kf = np.asarray(xm.kernel(spec))
    assert np.max(np.abs(kf - np.array(tb, dtype=float))) <= 1e-15
    assert np.array_equal(kf > 0, np.array([[v > 0 for v in r] for r in tb]))
    for arm in ARMS:
        T = lift(arm)
        assert all(sum(r) == 1 for r in T) and all(sum(col) == 1 for col in zip(*T))
        assert xm.model(arm)["T"] == T
        assert xm.lift(tb, xm.edge_labels(arm), F(1) if arm == "ETA1" else ETA) == T
    T = lift("NA")  # states 3i + x: 0 -> 4 (+x, e), 0 -> 1 (+y, e), stay (e), 12 -> 0 (x+, a)
    assert [T[0][12], T[0][3], T[0][0], T[36][1]] == [F(74, 375)] * 4 and T[0][6] == 0
    assert [T[0][13], T[0][2], T[36][0], lift("ETA1")[0][13] / 50] == [F(1, 750)] * 4
    assert xm.model("NA")["pi"] == [F(1, 48)] * 48
    assert [len(spec.cells[k]) for k in (0, 1, 2)] == [16, 32, 16]
    assert CubicalComplex(16, spec.cells).betti(2) == (1, 2, 1) == CubicalComplex(
        16, spec.cells).betti(3)
    rows = [r for r in spec.cells[2].tolist() if sorted(r) != [0, 3, 12, 15]]
    pc = xm.punctured_complex(spec)
    assert [len(pc.cells[k]) for k in (0, 1, 2)] == [16, 32, 15]
    assert sorted(map(tuple, pc.cells[2].tolist())) == sorted(map(tuple, rows))
    assert pc.euler_characteristic() == -1 and pc.betti(2) == (1, 2, 0) == pc.betti(3)
    assert {e for e, c in edge_use(rows).items() if c == 1} == {
        frozenset(p) for p in ((15, 3), (3, 0), (0, 12), (12, 15))}  # one boundary cycle
    expect = {"NA": ((1, 4, 0), 1), "ZC": ((1, 4, 0), 3), "AB": ((2, 5, 0), 3),
              "TRIV": ((3, 6, 0), 3)}  # Lemma 0'
    g0 = xm.gate_G0(spec)
    for arm, (betti, circ) in expect.items():
        c1, c2 = cover_cells(spec, labels(arm))
        ref = CubicalComplex(48, {1: np.array(c1), 2: np.array(c2)})
        assert (len(c1), len(c2), ref.euler_characteristic()) == (96, 45, -3)
        assert ref.betti(2) == betti == ref.betti(3) and boundary_components(c1, c2) == circ
        mod = xm.cover_complex(spec, xm.edge_labels(arm))
        assert mod.cells[1].tolist() == c1 and mod.cells[2].tolist() == c2
        assert {k: tuple(v) for k, v in xm.cover_betti(mod).items()} == {2: betti, 3: betti}
        assert xm.boundary_circles(mod) == circ
        cov = g0["cover"][arm]
        assert tuple(cov["counts"]) == (48, 96, 45) and cov["circles"] == circ
        assert {k: tuple(v) for k, v in cov["betti"].items()} == {2: betti, 3: betti}
    assert g0["status"] == "PASS" and tuple(g0["counts"]) == (16, 32, 16)
    assert {k: tuple(v) for k, v in g0["betti"].items()} == {2: (1, 2, 1), 3: (1, 2, 1)}
    pu = g0["punctured"]
    assert (tuple(pu["counts"]), pu["chi"], pu["boundary_cycles"]) == ((16, 32, 15), -1, 1)
    assert {k: tuple(v) for k, v in pu["betti"].items()} == {2: (1, 2, 0), 3: (1, 2, 0)}
    assert g0["t_base_max_err"] <= 1e-15 and g0["t_base_support_ok"] is True
    assert all(g0["lift_ok"][a] and g0["validate_process"][a] for a in ARMS)
    assert all(g0["lift_max_err"][a] <= 1e-15 for a in ARMS)


def test_03_faces_flux_fstar(spec):  # section 10.4 test 3
    rows = [tuple(r) for r in spec.cells[2].tolist()]
    fs = xm.f_star_index(spec)
    assert [k for k, r in enumerate(rows) if sorted(r) == [0, 3, 12, 15]] == [fs]
    assert rows[fs] == (15, 12, 3, 0)
    cyc = tuple(xm.face_cycle((15, 12, 3, 0)))
    assert cyc == (15, 3, 0, 12, 15)
    assert [letter(u, v) for u, v in zip(cyc, cyc[1:])] == ["x+", "y+", "x-", "y-"]
    flux = {}
    for arm in ARMS:
        lab = labels(arm)
        assert {k: tuple(v) for k, v in xm.edge_labels(arm).items()} == lab
        mine = [hol((r0, r2, r3, r1, r0), lab) for r0, r1, r2, r3 in rows]
        assert [tuple(g) for g in xm.face_holonomies(spec, xm.edge_labels(arm))] == mine
        assert all(g == E0 for k, g in enumerate(mine) if k != fs)
        flux[arm] = mine[fs]
        assert tuple(xm.flux(spec, xm.edge_labels(arm))) == flux[arm]
        assert xm.eta(arm) == (F(1) if arm == "ETA1" else ETA)
    assert {a: flux[a] for a in ("NA", "AB", "ZC", "TRIV", "ETA1", "GAUGE-TRIV")} == {
        "NA": C, "AB": E0, "ZC": E0, "TRIV": E0, "ETA1": C, "GAUGE-TRIV": E0}
    assert flux["GAUGE-NA"] in (C, C2) and flux["GAUGE-COV"] in (C, C2)
    for arm, (gx, gy) in SEAM.items():  # Lemma 0(2): g_y^-1 o g_x^-1 o g_y o g_x
        assert comp(inv(gy), comp(inv(gx), comp(gy, gx))) == flux[arm]
        sl = {k: tuple(v) for k, v in xm.seam_labels(arm).items()}
        assert sl == {"x+": gx, "x-": inv(gx), "y+": gy, "y-": inv(gy)}
    with pytest.raises(ValueError):
        xm.seam_labels("GAUGE-NA")


def test_04_witness_path_sums():  # section 10.4 test 4
    T, E, lab = lift("NA"), emis(), labels("NA")
    assert w_tokens("W2", "AB", 0) == (15, 9, 5, 9, 12, 1, 5, 6, 7, 4, 5, 1, 2, 3, 7, 10, 14, 13)
    assert w_tokens("W1", "D", 2) == (17, 13, 14, 11, 0, 4, 5, 6)
    for fam, mems, n, gap in (("W1", ("U", "D"), 7, "0.092701"),
                              ("W2", ("AB", "BA"), 17, "0.061119")):
        fv = xe.family_values("NA", fam)
        assert (fv["t"], fv["n"], fv["equal_P"], fv["tv_min"]) == (n + 1, n, True, lam(n + 1))
        hols = [hol((ANC,) + w_path(fam, m), lab) for m in mems]
        assert hols == [C2, C]  # U, AB: b o a = c^2; D, BA: a o b = c
        for y in range(3):
            laws = []
            for mem, rho in zip(mems, hols):
                toks = w_tokens(fam, mem, y)
                assert tuple(xe.witness_tokens(fam, mem, y)) == toks
                qs, P, _ = filt(T, E, toks)
                assert P == F(1, 48) / 5 ** n and qs[-1][15:] == [m / 5 for m in mu(n + 1, rho[y])]
                rec = fv["members"][mem]
                assert (rec["P"][y], list(rec["q"][y]), rec["holonomy"]) == (P, qs[-1], NAME[rho])
                laws.append(qs[-1])
            tv = sum(abs(a - b) for a, b in zip(laws[0][15:], laws[1][15:])) * 5 / 2
            assert tv == lam(n + 1)  # cue-normalised (the cue mass is 1/5)
            mix, got = [(a + b) / 2 for a, b in zip(*laws)], xe.set_gap(laws)
            bar = [(1 - lam(n + 1)) / 3 + (lam(n + 1) / 2 if k else 0) for k in range(3)]
            with localcontext(Context(prec=100)):  # every reference Decimal op at 100 digits
                ref = (dkl(laws[0], mix) + dkl(laws[1], mix)) / 2
                assert abs(ref - (dent(bar) - dent(mu(n + 1, 0))) / 5) < Decimal("1e-40")
                assert abs(got - ref) < Decimal("1e-40")
                assert abs(ref - Decimal(gap)) < Decimal("1e-6")
    hs = [hol((ANC,) + w_path("W3", o), lab) for o in ORDS]
    mult = Counter(NAME[h] for h in hs)
    assert mult == {"e": 16, "c": 4, "c2": 4} and F(mult["c"] + mult["c2"], 24) == F(1, 3)
    assert hs[ORDS.index(("A+", "B+", "A-", "B-"))] == C
    assert hs[ORDS.index(("B+", "A+", "B-", "A-"))] == C2
    fv = xe.family_values("NA", "W3")
    assert {k: fv["multiplicity"][k] for k in ("e", "c", "c2")} == {"e": 16, "c": 4, "c2": 4}
    assert (fv["tv_min"], fv["equal_P"], fv["t"]) == (lam(32), True, 32)
    for o, h in zip(ORDS, hs):
        assert fv["members"][o]["holonomy"] == NAME[h]
        for y in range(3):
            assert list(fv["members"][o]["q"][y])[15:] == [m / 5 for m in mu(32, h[y])]
            assert fv["members"][o]["P"][y] == F(1, 48) / 5 ** 31


def test_05_kgram_locality():  # section 10.4 test 5
    T, E = lift("NA"), emis()
    ref2 = {w: p for w in itertools.product(range(18), repeat=2) if (p := filt(T, E, w)[1])}
    models = {a: xm.model(a) for a in SEAM_ARMS}
    for k in (1, 2, 3, 4):
        laws = [dict(xm.kgram_law(models[a], k)) for a in SEAM_ARMS]
        assert all(law == laws[0] for law in laws) and sum(laws[0].values()) == 1
        assert all(v > 0 for v in laws[0].values()) and (k != 2 or laws[0] == ref2)
    l4 = lam(4)
    grams = [(15 + y, 10, 8, 9, 15 + y2) for y in range(3) for y2 in range(3)]
    five = {a: dict(xm.kgram_law(models[a], 5)) for a in SEAM_ARMS}
    for a in SEAM_ARMS:
        gy = SEAM[a][1]
        for y, y2 in itertools.product(range(3), range(3)):
            assert tuple(xm.five_gram(y, y2)) == (15 + y, 10, 8, 9, 15 + y2)
            exp = F(1, 48) / 5 ** 4 * (l4 * int(y2 == gy[y]) + (1 - l4) / 3)
            assert five[a][(15 + y, 10, 8, 9, 15 + y2)] == exp
    for a, b in itertools.combinations(SEAM_ARMS, 2):
        ratio = max(max(five[a][g], five[b][g]) / min(five[a][g], five[b][g]) for g in grams)
        assert five[a] != five[b] and ratio == (1 + 2 * l4) / (1 - l4) and ratio > 2  # ~36.6


def test_09_block_comparator():  # section 10.4 test 9
    prior = {"e": F(2, 3), "c": F(1, 6), "c2": F(1, 6)}
    toks = {o: w_tokens("W3", o, 0) for o in ORDS}
    truth = {o: NAME[hol((ANC,) + w_path("W3", o), labels("NA"))] for o in ORDS}
    nz = Counter(truth.values())
    cnt = Counter((j, toks[o][8 * j:8 * j + 8], truth[o]) for o in ORDS for j in range(4))
    assert len({toks[o][:8] for o in ORDS}) == 1 and len({toks[o][24:] for o in ORDS}) == 1
    post = {}
    for o in ORDS:
        un = dict(prior)
        for j, z in itertools.product(range(4), prior):
            un[z] *= F(cnt[(j, toks[o][8 * j:8 * j + 8], z)], nz[z])
        post[o] = {z: v / sum(un.values()) for z, v in un.items()}
        exp = (1, 1) if truth[o] == "e" else (F(1, 5), F(4, 5))  # r_add(e), r_add(truth)
        assert (post[o]["e"], post[o][truth[o]]) == exp
    bc, q_rot, q_id = xe.block_comparator(0), mu(32, 1), mu(32, 0)
    assert {o: {z: p.get(z, 0) for z in prior} for o, p in bc["posteriors"].items()} == post
    assert dict(bc["truth"]) == truth and bc["accuracy"] == 1
    with localcontext(Context(prec=100)):  # every reference Decimal op at 100 digits
        logloss = dec(F(5, 4)).ln() / 3  # mean -ln r_add(truth): 16 x 0 and 8 x ln(5/4)
        regret = dkl(q_rot, [F(4, 5) * a + F(1, 5) * b for a, b in zip(q_rot, q_id)]) / 15
        assert abs(bc["holonomy_logloss"] - logloss) < Decimal("1e-40")
        assert abs(bc["regret"] - regret) < Decimal("1e-40")
        assert abs(logloss - Decimal("0.0743812")) < Decimal("1e-6")
        assert abs(regret - Decimal("0.0022197")) < Decimal("1e-6")
    assert bc["accuracy"] == 1 and bc["regret"] > 0  # exact classification, imperfect calibration
    r = xe.block_posterior(prior, [{"e": F(1, 16), "c": F(1, 4), "c2": F(0)}] * 2)
    assert {z: r.get(z, 0) for z in prior} == {"e": F(1, 5), "c": F(4, 5), "c2": 0}


def test_13_registry_and_geometry_guards(monkeypatch):  # section 10.4 test 13
    import topo_pilot.process._geometry as geo
    import topo_pilot.process.emission as emi
    from topo_pilot.world import WORLD_REGISTRY, QuotientLatticeBuilder
    before = dict(WORLD_REGISTRY)

    def forbidden(*args, **kwargs):
        raise AssertionError("forbidden geometry call")
    monkeypatch.setattr(geo, "point_distances", forbidden)
    monkeypatch.setattr(emi, "point_distances", forbidden)
    monkeypatch.setattr(geo, "is_x_periodic", forbidden)
    s = xm.build_world()
    assert xm.kernel(s).shape == (16, 16) and xm.gate_G0(s)["status"] == "PASS"
    assert dict(WORLD_REGISTRY) == before and xm.FAMILY == "_x6_torus_local" not in before
    assert all(c.__module__.startswith("topo_pilot.") for c in WORLD_REGISTRY.values())
    cls = xm._X6TorusBuilder
    assert issubclass(cls, QuotientLatticeBuilder) and cls.family == "_x6_torus_local"
    assert {k: tuple(v) for k, v in cls.expected_betti.items()} == {2: (1, 2, 1), 3: (1, 2, 1)}
    assert [(i.axis, i.kind) for i in cls.identifications] == [(0, "periodic"), (1, "periodic")]


def test_14_file_line_limits():  # section 10.4 test 14
    names = ("x6_model.py", "x6_dp.py", "x6_exact.py", "x6_run.py", "x6_store.py")
    assert {p.name for p in TOOLS.glob("*.py")} == set(names)
    here = Path(__file__).resolve().parent
    for p in [TOOLS / n for n in names] + sorted(here.glob("*.py")):
        assert len(p.read_bytes().splitlines()) <= 400, p.name
