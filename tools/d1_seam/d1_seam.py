"""D-1 seam check part 1 (D1-FROZEN-v1; API.md): model, kernels, enumerator, G0-G3. G4-G6 and run
are in d1_seam_checks.py (addendum 2). Local unregistered Möbius builder; no point_distances."""

from __future__ import annotations

import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Fr
from pathlib import Path
from typing import ClassVar

import numpy as np

REPO = Path(__file__).resolve().parents[2]
_EXTRA = (REPO / "tests" / "oracle_profile", Path(__file__).resolve().parent)
sys.path[:0] = [str(p) for p in _EXTRA if str(p) not in sys.path]

import topo_pilot.world as tw  # noqa: E402
from topo_pilot.process import TransitionBuilder, TransitionConfig  # noqa: E402
from topo_pilot.world.complex import check_boundary_closed, rank_mod_p  # noqa: E402
from topo_pilot.world.metrics import check_flat_bounds  # noqa: E402

S0, S2, S3, A, B = range(5)
NV, NS, K_DEPTH = 5, 12, 8
a, c, Z, HALF = Fr(1, 5), Fr(3, 5), Fr(0), Fr(1, 2)
H_STAR, H_A = (A, S2, S3), (A, S2, S3, S0, A, S2, S3, S0, A, S2, S3)
H_B, H_EDGE, H_MAX = H_A[:4] + (B,) + H_A[5:], (A, S2, S3, S0, A, S2), (A, S2, S3, S0, A, B, S0, S3)
VARIANTS = ("frozen", "N1", "N2", "N3", "L1", "L2")
LITERAL_E = ["1 0 0 0 0"] * 3 + ["0 0 0 3/4 1/4", "0 0 0 1/2 1/2", "0 0 0 1/4 3/4"]
LITERAL_E += ["0 1 0 0 0"] * 3 + ["0 0 1 0 0"] * 3  # §2.4, rows 3x + y
Q1_HI = [a, a, c, Z, Z]
EXP = {"N_t": [2, 8, 32, 124, 480, 1852, 7144, 27548], "HI_t": [0, 0, 4, 16, 68, 264, 1028, 3968],
       "HI_mass_t": [Z, Z, Fr(2, 25), Fr(18, 125), Fr(116, 625), Fr(132, 625),
                     Fr(3542, 15625), Fr(18438, 78125)],
       "D_t": [Z] * 4 + [Fr(1, 625), Fr(2, 625), Fr(66, 15625), Fr(364, 78125)]}

def st(x, y): return 3 * x + y  # noqa: E704
def _R(s): return st(s // 3, 2 - s % 3)  # noqa: E704  reflection (x, y) -> (x, 2 - y)
def _seam(i, j): return {i // 3, j // 3} == {0, 3}  # noqa: E704
def _nb(T): return [[(j, t) for j, t in enumerate(row) if t] for row in T]  # noqa: E704
def _vec(d, n=NS): return [d.get(i, Z) for i in range(n)]  # noqa: E704
def _q2d(J): return [sum((J[i][j] for i in range(NV)), Z) for j in range(NV)]  # noqa: E704
def _delta(b): return sum((b.get(st(x, 0), Z) - b.get(st(x, 2), Z) for x in range(4)), Z)  # noqa: E704
def _dln(x): return Decimal(x.numerator).ln() - Decimal(x.denominator).ln()  # noqa: E704

def edge_set(world):
    out = {(st(x, y), st(x + 1, y)) for x in range(3) for y in range(3)}
    out |= {(st(x, y), st(x, y + 1)) for x in range(4) for y in range(2)}
    return out | {tuple(sorted((st(3, y), st(0, y if world == "C" else 2 - y)))) for y in range(3)}

def exact_world_T(world):
    E = edge_set(world)
    T = [[a if (min(i, j), max(i, j)) in E else Z for j in range(NS)] for i in range(NS)]
    return [[1 - sum(r) if i == j else v for j, v in enumerate(r)] for i, r in enumerate(T)]

def exact_E(variant="frozen"):
    rows = [[Fr(v) for v in r.split()] for r in LITERAL_E]
    if variant == "N2":
        rows[3:6] = [[Z, Z, Z, HALF, HALF] for _ in range(3)]
    if variant == "L2":
        rows[6:9] = [list(r) for r in rows[3:6]]
    return rows

def exact_model(variant="frozen"):
    TC, TM = exact_world_T("C"), exact_world_T("C" if variant == "N1" else "M")
    EC = exact_E(variant)
    EM = [list(EC[_R(s)] if variant == "L1" and s // 3 == 1 else EC[s]) for s in range(NS)]
    k = st(1, 1 if variant == "N3" else 0)
    mu = [HALF if i in (k, NS + k) else Z for i in range(2 * NS)]
    T = [r + [Z] * NS for r in TC] + [[Z] * NS + r for r in TM]
    return {"T": T, "E": EC + EM, "mu": mu, "T_C": TC, "T_M": TM, "E_C": EC, "E_M": EM, "start": k}

class _D1MobiusBuilder(tw.QuotientLatticeBuilder):  # deliberately NOT @register_world (§2.6)
    family: ClassVar[str] = "_d1_mobius_local"
    expected_betti: ClassVar[dict] = {2: (1, 1, 0), 3: (1, 1, 0)}
    identifications: ClassVar[tuple] = (tw.Identification(0, "flipped", flip_axis=1),)

def build_worlds():
    C = tw.build_world(tw.WorldConfig("cylinder", (4, 3), "flat"))
    M = _D1MobiusBuilder().build(tw.WorldConfig("_d1_mobius_local", (4, 3), "flat"))
    M.validate()
    check_boundary_closed(tw.CubicalComplex(M.n_states, M.cells))
    check_flat_bounds(M.dist, M.dist_graph, 2)
    return {"C": C, "M": M}

def float_model(worlds=None):
    worlds = worlds or build_worlds()
    tr = {f: TransitionBuilder().build(worlds[f], TransitionConfig(p_stay=0.2)) for f in "CM"}
    E = np.array([[float(v) for v in r] for r in exact_E()])
    T = np.block([[tr["C"].T, np.zeros((NS, NS))], [np.zeros((NS, NS)), tr["M"].T]])
    mu, one = np.eye(2 * NS)[[3, 15]].sum(0) / 2, np.eye(NS)[3]
    return {"T_C": tr["C"].T, "T_M": tr["M"].T, "E": E, "T": T, "E_mix": np.vstack((E, E)),
            "mu": mu, "mu_C": one, "mu_M": one.copy(), "pi_C": tr["C"].pi, "pi_M": tr["M"].pi}

def _step(al, nb, E, w, emit=None):
    out = {}
    for i, p in al.items():
        for j, t in nb[i]:
            e = emit(j, w) if emit else E[j][w]
            if e:
                out[j] = out.get(j, Z) + p * t * e
    return out

def _q1(al, nb, E): return [sum(_step(al, nb, E, v).values(), Z) for v in range(NV)]  # noqa: E704
def _J(b, nb, E): return [_q1(_step(b, nb, E, w), nb, E) for w in range(NV)]  # noqa: E704

def _norm(al):
    tot = sum(al.values(), Z)
    return ({k: v / tot for k, v in al.items()} if tot else {}), tot

def _mix(p, q, pi):
    if p and isinstance(p[0], list):
        return [_mix(r, s, pi) for r, s in zip(p, q)]
    return [(1 - pi) * x + pi * y for x, y in zip(p, q)]

def tv(p, q):
    if p and isinstance(p[0], list):
        return sum((tv(r, s) for r, s in zip(p, q)), Z)
    return sum((abs(x - y) for x, y in zip(p, q)), Z) / 2

def parity_profile(h):
    par, odd = 0, 0
    for s, w in enumerate(h):
        par ^= int(s > 0 and {h[s - 1], w} == {S3, S0})
        odd += int(w in (A, B) and par == 1)
    return par, odd

def exact_history(history, variant="frozen", model=None):
    m, out = model or exact_model(variant), {}
    for f in "CM":
        nb, E, k = _nb(m["T_" + f]), m["E_" + f], m["start"]
        al = {k: E[k][history[0]]} if E[k][history[0]] else {}
        for w in history[1:]:
            al = _step(al, nb, E, w)
        b, P = _norm(al)
        if not P:
            raise ValueError(f"P(h | {f}) = 0 for {history}")
        J = _J(b, nb, E)
        out.update({"P_" + f: P, "b_" + f: _vec(b), "Q1_" + f: _q1(b, nb, E), "J_" + f: J,
                    "Q2dist_" + f: _q2d(J)})
    pi = out["P_M"] / (out["P_C"] + out["P_M"])
    par, odd = parity_profile(history)
    out.update(P=(out["P_C"] + out["P_M"]) / 2, pi=pi, par=par, informed=odd > 0, m_odd=odd,
               b_mix=[(1 - pi) * v for v in out["b_C"]] + [pi * v for v in out["b_M"]],
               **{k: _mix(out[k + "_C"], out[k + "_M"], pi) for k in ("Q1", "J", "Q2dist")})
    return out

def _nodes(m, K):
    """Depth-first reachable histories: C, M, reflected-C (Theorem C(b)) and 24-state passes."""
    (nbC, EC), (nbM, EM) = (_nb(m["T_C"]), m["E_C"]), (_nb(m["T_M"]), m["E_M"])
    nbX, EX, k = _nb(m["T"]), m["E"], m["start"]
    stack = []
    for w in range(NV):
        aC, aM = ({k: E[k][w]} if E[k][w] else {} for E in (EC, EM))
        if aC or aM:
            aX = {i: m["mu"][i] * EX[i][w] for i in (k, NS + k) if EX[i][w]}
            stack.append(((w,), 0, 0, aC, aM, dict(aC), aX))
    while stack:
        node = stack.pop()
        yield node
        h, par, odd, aC, aM, aR, aX = node
        for w in range(NV) if len(h) < K else ():
            p2 = par ^ int({h[-1], w} == {S3, S0})
            cC, cM = _step(aC, nbC, EC, w), _step(aM, nbM, EM, w)
            if cC or cM:
                refl = (lambda j, v: EC[_R(j)][v]) if (w in (A, B) and p2) else None
                stack.append((h + (w,), p2, odd + int(w in (A, B) and p2), cC, cM,
                              _step(aR, nbC, EC, w, refl), _step(aX, nbX, EX, w)))

def gate_G2(variant="frozen", K=K_DEPTH):
    m = exact_model(variant)
    nb = {f: _nb(m["T_" + f]) for f in "CM"}
    N, HI, mass = [0] * K, [0] * K, [Z] * K
    marg = {f: [[Z] * NV for _ in range(K)] for f in "CM"}
    vio = dict.fromkeys(("lemmaB", "thmCb", "thmCa", "mixture", "thmA", "D2", "F1", "F2"), 0)
    cnt = dict.fromkeys(("pi_not_half", "tv1_nonzero", "tv2_nonzero_HI"), 0)  # control counters
    data, maxb, jm0, seen = {t: [] for t in range(1, K + 1)}, 0, 0, set()
    targets = {H_STAR, H_MAX, H_EDGE, H_A[:K], H_B[:K]}
    for h, par, odd, aC, aM, aR, aX in _nodes(m, K):
        t = len(h)
        (bC, PC), (bM, PM), (bX, PX) = _norm(aC), _norm(aM), _norm(aX)
        seen |= {h} & targets
        pi, N[t - 1] = PM / (PC + PM), N[t - 1] + 1
        marg["C"][t - 1][h[-1]] += PC
        marg["M"][t - 1][h[-1]] += PM
        vio["lemmaB"] += int(not (PC > 0 and PM > 0 and Fr(1, 3**odd) <= PM / PC <= 3**odd))
        vio["thmCb"] += int(PM != sum(aR.values(), Z))
        refl = {(_R(s) if par else s): v for s, v in bC.items()}
        vio["thmCa"] += int(odd == 0 and (PM != PC or refl != bM))
        mixb = {i: (1 - pi) * v for i, v in bC.items()} | {NS + i: pi * v for i, v in bM.items()}
        vio["mixture"] += int(bX != {i: v for i, v in mixb.items() if v})
        cnt["pi_not_half"] += int(pi != HALF)
        q1C, q1M = _q1(bC, nb["C"], m["E_C"]), _q1(bM, nb["M"], m["E_M"])
        cnt["tv1_nonzero"] += int(q1C != q1M)
        data[t].append((h, _vec(bC), _vec(bM), pi, PX))
        if h[-1] != S3:
            continue
        HI[t - 1], mass[t - 1] = HI[t - 1] + 1, mass[t - 1] + PX
        JC, JM = _J(bC, nb["C"], m["E_C"]), _J(bM, nb["M"], m["E_M"])
        tvJ, tvD = tv(JC, JM), tv(_q2d(JC), _q2d(JM))
        vio["thmA"] += int(not (q1C == q1M == Q1_HI))
        cont = [tv(*(_q1(_norm(_step(b, nb[f], m["E_" + f], w))[0], nb[f], m["E_" + f])
                     for b, f in ((bC, "C"), (bM, "M")))) for w in (S0, S2)]
        vio["D2"] += int(tvJ != a * (cont[0] + cont[1]))
        dC, dM = abs(_delta(bC)), abs(_delta(bM))
        vio["F1"] += int(tvJ != a * a / 2 * max(dC, dM))
        vio["F2"] += int(tvD != a * a / 2 * dC)
        cnt["tv2_nonzero_HI"] += int(tvJ != 0)
        maxb, jm0 = maxb + int(dM > dC), jm0 + int(tvJ > 0 and tvD == 0)
        data[t][-1] += (q1C, q1M, JC, JM)
    D = [marg["C"][t][A] - marg["M"][t][A] for t in range(K)]
    hs, hm, a2 = exact_history(H_STAR, variant), exact_history(H_MAX, variant), a * a
    named_ok = (hs["P"] == Fr(3, 100) and hs["pi"] == HALF and tv(hs["J_C"], hs["J_M"]) == Fr(1, 50)
                and tv(hs["Q2dist_C"], hs["Q2dist_M"]) == Fr(1, 50) and hm["pi"] == Fr(2, 5)
                and hm["P"] == Fr(3, 500000) and tv(hm["J_C"], hm["J_M"]) == Fr(3, 200)
                and tv(hm["Q2dist_C"], hm["Q2dist_M"]) == Fr(1, 100)
                and (hm["J_C"][S2][A], hm["J_M"][S2][A]) == (5 * a2 / 8, 11 * a2 / 16)
                and (hm["J_C"][S0][A], hm["J_M"][S0][A]) == (5 * a2 / 8, 5 * a2 / 16))
    values = {"N_t": N, "HI_t": HI, "HI_mass_t": mass, "D_t": D, "violations": vio,
              "control_counters": cnt, "max_branch_count": maxb, "joint_pos_marginal_zero": jm0,
              "named_reached": len(seen) == len(targets), "named_values_ok": named_ok,
              "named": {"h_star": (hs["P"], hs["pi"]), "h_max": (hm["P"], hm["pi"])}}
    ok = [N == EXP["N_t"], HI == EXP["HI_t"], mass == EXP["HI_mass_t"], D == EXP["D_t"],
          all(v == 0 for v in vio.values()), maxb > 0, values["named_reached"], named_ok]
    return {"status": "PASS" if all(ok) else "FAIL", "values": values, "_data": data}

def _gate(ck, values):
    return {"status": "PASS" if all(ck.values()) else "FAIL", "values": dict(values, checks=ck)}

def gate_G0(worlds, E_mix=None):
    ck, fm = {}, float_model(worlds)
    E_mix = fm["E_mix"] if E_mix is None else E_mix
    edges = {f: {tuple(e) for e in np.asarray(w.edges).tolist()} for f, w in worlds.items()}
    degs = {}
    for f, w in worlds.items():
        cx = tw.CubicalComplex(w.n_states, w.cells)
        d1, d2 = cx.boundary_matrix(1).toarray(), cx.boundary_matrix(2).toarray()
        degs[f] = deg = [sum(s in e for e in edges[f]) for s in range(NS)]
        Tx, Tf = exact_world_T(f), np.asarray(fm["T_" + f])
        ck[f + "_counts"] = (w.n_states, len(edges[f]), len(w.cells[2])) == (12, 20, 8)
        ck[f + "_chi_betti"] = (cx.euler_characteristic() == 0
                                and cx.betti(2) == cx.betti(3) == (1, 1, 0))
        ck[f + "_d1d2"] = not np.any(d1 @ d2)
        ck[f + "_edges"] = edges[f] == edge_set(f)
        ck[f + "_degrees"] = all(deg[s] == (3, 4, 3)[s % 3] for s in range(NS)) and max(deg) == 4
        ck[f + "_T_exact"] = all(sum(r) == 1 for r in Tx) and all(
            Tx[i][j] == Tx[j][i] and (Tx[i][j] != 0) == (Tf[i, j] != 0)
            and abs(Tf[i, j] - float(Tx[i][j])) <= 1e-15 for i in range(NS) for j in range(NS))
        ck[f + "_pi_uniform"] = bool(np.all(fm["pi_" + f] == fm["pi_" + f][0]))
    TC, TM = exact_world_T("C"), exact_world_T("M")
    ck["offseam_equal"] = all(TC[i][j] == TM[i][j] and fm["T_C"][i, j] == fm["T_M"][i, j]
                              for i in range(NS) for j in range(NS) if not _seam(i, j))
    ck["seam_symdiff"] = (edges["C"] ^ edges["M"] == {(0, 9), (2, 11), (2, 9), (0, 11)}
                          and (1, 10) in edges["C"] & edges["M"])
    ck["degree_multisets"] = sorted(degs["C"]) == sorted(degs["M"])
    lit = np.array([[float(Fr(v)) for v in r.split()] for r in LITERAL_E])
    ck["E_literal"] = bool(np.array_equal(fm["E"], lit))
    ck["E_blocks"] = bool(np.array_equal(E_mix[:NS], E_mix[NS:])
                          and np.array_equal(E_mix[:NS], lit))
    ck["mu"] = fm["mu"].tolist() == [0.5 if i in (3, 15) else 0.0 for i in range(2 * NS)]
    return _gate(ck, {"edges_C": sorted(edges["C"]), "edges_M": sorted(edges["M"])})

def _components(n, pairs):
    """Number of connected components of a graph on range(n) (reachability by matrix power)."""
    adj = np.eye(n, dtype=np.int64)
    for i, j in pairs:
        adj[i, j] = adj[j, i] = 1
    return len({tuple(r) for r in (np.linalg.matrix_power(adj, max(n, 1)) > 0).tolist()})

def _complex(w):
    cx = tw.CubicalComplex(w.n_states, w.cells)
    d2 = cx.boundary_matrix(2).toarray()
    return d2, np.abs(d2), [tuple(e) for e in np.asarray(w.cells[1]).tolist()]

def gate_G0S(worlds):
    ck, vals = {}, {}
    for f, w in worlds.items():
        _, d2, edges = _complex(w)
        ck[f + "_edge_links"] = sorted(d2.sum(1).tolist()) == [1] * 8 + [2] * 12
        shapes = []
        for v in range(NS):
            nodes = [i for i, e in enumerate(edges) if v in e]
            links = [tuple(i for i in nodes if d2[i, q]) for q in range(d2.shape[1])
                     if any(d2[i, q] for i in nodes)]
            n_, m_, pos = len(nodes), len(links), {e: k for k, e in enumerate(nodes)}
            deg = sorted(sum(i in lk for lk in links) for i in nodes)
            cyc, arc = m_ == n_ and deg == [2] * n_, m_ == n_ - 1 and deg == [1, 1] + [2] * (n_ - 2)
            conn = _components(n_, [(pos[x], pos[y]) for x, y in links]) == 1
            good = conn and all(len(lk) == 2 for lk in links) and (cyc or arc)
            shapes.append(("cycle" if cyc else "arc", n_) if good else ("bad", n_))
        ck[f + "_vertex_links"] = all(shapes[s] == (("arc", 3), ("cycle", 4), ("arc", 3))[s % 3]
                                      for s in range(NS))
        vals[f] = shapes
    return _gate(ck, vals)

def gate_G0O(worlds):
    ck, vals = {}, {}
    for f, w in worlds.items():
        d2, d2a, edges = _complex(w)
        bd = [edges[i] for i in range(len(edges)) if d2a[i].sum() == 1]
        verts = sorted({v for e in bd for v in e})
        n_comp = _components(len(verts), [(verts.index(x), verts.index(y)) for x, y in bd])
        interior = [i for i in range(len(edges)) if d2a[i].sum() == 2]
        sgn, consistent = {0: 1}, True
        for _ in range(8):  # breadth-first propagation over the 8-square dual graph
            for i in interior:
                q1, q2 = np.flatnonzero(d2[i])
                om = -d2[i, q1] * d2[i, q2]
                for p, q in ((q1, q2), (q2, q1)):
                    if p in sgn and q not in sgn:
                        sgn[q] = om * sgn[p]
                    elif p in sgn and sgn[q] != om * sgn[p]:
                        consistent = False
        s = np.array([sgn.get(q, 0) for q in range(d2.shape[1])])
        sub = d2[interior]
        r3, r2 = rank_mod_p(sub % 3, 3), rank_mod_p(sub % 2, 2)
        vals[f] = {"boundary_components": n_comp, "consistent": consistent, "rank_gf3": r3,
                   "nullity_gf2": sub.shape[1] - r2}
        exp = (2, True, 7) if f == "C" else (1, False, 8)
        ck[f] = ((n_comp, consistent, r3) == exp and sub.shape[1] - r2 == 1
                 and (not consistent or not np.any(sub @ s)))
    return _gate(ck, vals)

def gate_G1(variant="frozen"):
    m, ck = exact_model(variant), {}
    for f in "CM":
        T, E, nb = m["T_" + f], m["E_" + f], _nb(m["T_" + f])
        ck[f + "_lemma1"] = all(sum(T[s][st(x2, y)] for y in range(3)) == (
            a if (x2 - s // 3) % 4 in (1, 3) else c if x2 == s // 3 else Z)
            for s in range(NS) for x2 in range(4))
        Ks = [[[T[st(x, y)][st(x, y2)] for y2 in range(3)] for y in range(3)] for x in range(4)]
        ck[f + "_lemma1p"] = all(K == Ks[0] for K in Ks) and all(
            Ks[0][2 - y][2 - y2] == Ks[0][y][y2] for y in range(3) for y2 in range(3))
        ck[f + "_thmA_rows"] = all(_q1({st(3, y): Fr(1)}, nb, E) == Q1_HI for y in range(3))
        J0 = _J({st(3, 0): Fr(1)}, nb, E)
        for y in range(3):
            J, e = _J({st(3, y): Fr(1)}, nb, E), (lambda yy: E[st(1, yy)][A])
            ck[f"{f}_J{y}"] = (all(J[i][j] == J0[i][j] for i in range(3) for j in range(3))
                               and J[S2][A] == a * a * e(y)
                               and J[S0][A] == a * a * e(y if f == "C" else 2 - y))
        if variant == "frozen":
            ck[f + "_J_star"] = J0 == (JC_STAR if f == "C" else JM_STAR)
    TC, TM = m["T_C"], m["T_M"]
    ck["thmC_offseam"] = all(TM[_R(i)][_R(j)] == TC[i][j] for i in range(NS) for j in range(NS)
                             if not _seam(i, j))
    ck["thmC_seam"] = all(TM[st(3, 2 - y)][st(0, y)] == TC[st(3, y)][st(0, y)] == a
                          and TM[st(0, 2 - y)][st(3, y)] == TC[st(0, y)][st(3, y)] == a
                          for y in range(3))
    return _gate(ck, {})

_JROWS = ("3/25 0 1/25 3/100 1/100", "0 3/25 1/25 3/100 1/100", "3/25 3/25 9/25 0 0")
JC_STAR = [[Fr(v) for v in r.split()] for r in _JROWS] + [[Z] * 5, [Z] * 5]
JM_STAR = [JC_STAR[0][:3] + [Fr(1, 100), Fr(3, 100)]] + JC_STAR[1:]

def _kl(P, Q):
    return sum((Decimal(p.numerator) / p.denominator * _dln(p / q)
                for rp, rq in zip(P, Q) for p, q in zip(rp, rq) if p), Decimal(0))

def gate_G3():
    hs, hA, hB, he = (exact_history(h) for h in (H_STAR, H_A, H_B, H_EDGE))
    d0, a10, ck, q2 = [Fr(int(s == 9)) for s in range(NS)], a**10, {}, [Fr(6, 25)] * 2
    ck["h_star"] = (hs["P_C"] == hs["P_M"] == hs["P"] == Fr(3, 100) and hs["pi"] == HALF
                    and hs["b_C"] == hs["b_M"] == d0 and hs["Q1_C"] == hs["Q1_M"] == Q1_HI
                    and hs["J_C"] == JC_STAR and hs["J_M"] == JM_STAR
                    and tv(hs["J_C"], hs["J_M"]) == Fr(1, 50)
                    and hs["Q2dist_C"] == q2 + [Fr(11, 25), Fr(3, 50), Fr(1, 50)]
                    and hs["Q2dist_M"] == q2 + [Fr(11, 25), Fr(1, 25), Fr(1, 25)]
                    and tv(hs["Q2dist_C"], hs["Q2dist_M"]) == Fr(1, 50))
    t1 = [tv(x["Q1_C"], x["Q1_M"]) for x in (exact_history(H_STAR + (w,)) for w in (S0, S2))]
    ck["chain_identity"] = t1 == [Fr(1, 10), Z] and a * t1[0] + a * t1[1] == Fr(1, 50)
    with localcontext() as ctx:
        ctx.prec = 80
        Jbar, lim = _mix(JC_STAR, JM_STAR, HALF), Decimal(10) ** -45
        vals = {"KL": _kl(JC_STAR, JM_STAR), "KL_rev": _kl(JM_STAR, JC_STAR),
                "MI": (_kl(JC_STAR, Jbar) + _kl(JM_STAR, Jbar)) / 2}
        ck["logs"] = (abs(vals["KL"] - Decimal(3).ln() / 50) <= lim
                      and abs(vals["KL_rev"] - Decimal(3).ln() / 50) <= lim
                      and abs(vals["MI"] - (Decimal(27) / 16).ln() / 100) <= lim)
    pAB = (hA["P_C"], hA["P_M"], hB["P_C"], hB["P_M"])
    ck["pair"] = (pAB == (27 * a10 / 64, 9 * a10 / 64, 9 * a10 / 64, 27 * a10 / 64)
                  and (hA["pi"], hB["pi"]) == (Fr(1, 4), Fr(3, 4))
                  and hA["P"] == hB["P"] == Fr(9, 312500000)
                  and all(x[k] == d0 for x in (hA, hB) for k in ("b_C", "b_M"))
                  and hA["Q1"] == hB["Q1"] == Q1_HI
                  and hA["J"] == _mix(JC_STAR, JM_STAR, Fr(1, 4))
                  and hB["J"] == _mix(JC_STAR, JM_STAR, Fr(3, 4))
                  and tv(hA["J"], hB["J"]) == Fr(1, 100) and tv(hA["J"], hB["J"]) / 2 == Fr(1, 200)
                  and hA["Q2dist"] == q2 + [Fr(11, 25), Fr(11, 200), Fr(5, 200)]
                  and hB["Q2dist"] == q2 + [Fr(11, 25), Fr(9, 200), Fr(7, 200)]
                  and tv(hA["Q2dist"], hB["Q2dist"]) == Fr(1, 100))
    ck["F3"] = tv(hA["J"], hB["J"]) == abs(hA["pi"] - hB["pi"]) * tv(hA["J_C"], hA["J_M"])
    ck["h_edge"] = ((he["P_C"], he["P_M"], he["pi"], he["P"])
                    == (9 * a**5 / 16, 3 * a**5 / 16, Fr(1, 4), Fr(3, 25000))
                    and he["Q1_C"] == [Z, c, a, Fr(3, 20), Fr(1, 20)]
                    and he["Q1_M"] == [Z, c, a, Fr(1, 20), Fr(3, 20)]
                    and tv(he["Q1_C"], he["Q1_M"]) == Fr(1, 10)
                    and he["Q1"] == [Z, c, a, Fr(1, 8), Fr(3, 40)])
    return _gate(ck, {k: str(v)[:32] for k, v in vals.items()})

from d1_seam_checks import gate_G4, gate_G5, gate_G6, run  # noqa: E402,F401  (addendum 2 re-export)
