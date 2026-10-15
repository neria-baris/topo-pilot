"""Independent tests of tools/d1_seam (job 0019), from D1-FROZEN-v1, its addendum and API.md only.
The module is imported, never read; the exact ``ref_*`` reference uses none of its kernels."""

from __future__ import annotations

import importlib.util
import json
import sys
from decimal import Decimal
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.process import _geometry
from topo_pilot.process.transition import TransitionBuilder, TransitionConfig
from topo_pilot.world import WORLD_REGISTRY

pytestmark = pytest.mark.oracle

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "d1_seam"), ("tests", "oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

_REGISTRY_BEFORE_IMPORT = dict(WORLD_REGISTRY)
import d1_seam  # noqa: E402
import independent_reference as ref  # noqa: E402

S0, S2, S3, A, B = 0, 1, 2, 3, 4
AX = Q(1, 5)  # a, the x-move probability
NU = [Q(1, 5), Q(1, 5), Q(3, 5), Q(0), Q(0)]  # Theorem A next-symbol law
H_STAR, H_EDGE = (A, S2, S3), (A, S2, S3, S0, A, S2)
H_A = (A, S2, S3, S0, A, S2, S3, S0, A, S2, S3)
H_B = (A, S2, S3, S0, B, S2, S3, S0, A, S2, S3)
H_MAX = (A, S2, S3, S0, A, B, S0, S3)
N_T = [2, 8, 32, 124, 480, 1852, 7144, 27548]  # section 3.2
HI_T = [0, 0, 4, 16, 68, 264, 1028, 3968]
HI_MASS = [Q(0), Q(0), Q(2, 25), Q(18, 125), Q(116, 625), Q(132, 625), Q(3542, 15625),
           Q(18438, 78125)]  # section 3.8
D_T = [Q(0)] * 4 + [Q(1, 625), Q(2, 625), Q(66, 15625), Q(364, 78125)]  # section 4
GATES = ("G0", "G0S", "G0O", "G1", "G2", "G3", "G4", "G5", "G6")

def _vec(spec: str) -> list[Q]:
    return [Q(v) for v in spec.split()]
def _rows(*specs: str) -> list[list[Q]]:
    return [_vec(s) for s in specs]
def idx(x: int, y: int) -> int:
    return 3 * x + y
def unit(i: int, n: int = 12) -> list[Q]:
    return [Q(int(j == i)) for j in range(n)]
def _vm(v, M) -> list[Q]:
    return [sum((v[i] * M[i][j] for i in range(len(v)) if v[i]), Q(0)) for j in range(len(M[0]))]
def _mix(pc, pm, pi):
    return [(1 - pi) * c + pi * m for c, m in zip(pc, pm)]
def _norm(x):
    return tuple(_norm(v) for v in x) if isinstance(x, (list, tuple, np.ndarray)) else Q(x)
def rho(b) -> list[Q]:
    return [sum((b[idx(x, y)] for x in range(4)), Q(0)) for y in range(3)]
def tv(p, q) -> Q:
    if isinstance(p[0], (list, tuple)):
        return sum((tv(r, s) for r, s in zip(p, q)), Q(0))
    return sum((abs(Q(x) - Q(y)) for x, y in zip(p, q)), Q(0)) / 2

E_LIT = _rows(*["1 0 0 0 0"] * 3, "0 0 0 3/4 1/4", "0 0 0 1/2 1/2", "0 0 0 1/4 3/4",
              *["0 1 0 0 0"] * 3, *["0 0 1 0 0"] * 3)  # section 2.4, rows 3x + y

def ref_edges(world: str) -> set[tuple[int, int]]:  # section 2.1, sorted vertex-id pairs
    edges = {(idx(x, y), idx(x + 1, y)) for x in range(3) for y in range(3)}
    edges |= {(idx(x, y), idx(x, y + 1)) for x in range(4) for y in range(2)}
    return edges | {(idx(0, y if world == "C" else 2 - y), idx(3, y)) for y in range(3)}
def ref_T(world: str) -> list[list[Q]]:  # section 2.2: a per neighbour, 1 - deg/5 on the diagonal
    T = [[Q(0)] * 12 for _ in range(12)]
    for i, j in ref_edges(world):
        T[i][j] = T[j][i] = AX
    for i in range(12):
        T[i][i] = 1 - Q(sum(1 for v in T[i] if v), 5)
    return T
@lru_cache(maxsize=None)
def ref_model(variant: str = "frozen") -> dict:  # per world (T, E, start, T E); section 5.2 G6
    e = [list(r) for r in E_LIT]
    for y in range(3):
        if variant == "N2":
            e[idx(1, y)] = _vec("0 0 0 1/2 1/2")
        if variant == "L2":
            e[idx(2, y)] = list(E_LIT[idx(1, y)])
    e_m = [list(r) for r in e]
    for y in range(3 if variant == "L1" else 0):
        e_m[idx(1, y)] = list(e[idx(1, 2 - y)])
    start = unit(idx(1, 1 if variant == "N3" else 0))
    worlds = (("C", ref_T("C"), e), ("M", ref_T("C" if variant == "N1" else "M"), e_m))
    return {f: (T, E, start, [_vm(row, E) for row in T]) for f, T, E in worlds}
def ref_mixture(variant: str = "frozen"):
    m = ref_model(variant)
    T = [r + [Q(0)] * 12 for r in m["C"][0]] + [[Q(0)] * 12 + r for r in m["M"][0]]
    return T, m["C"][1] + m["M"][1], [x / 2 for x in m["C"][2] + m["M"][2]]
def ref_forward(wm, h) -> list[Q]:  # unnormalised forward vector, emit then transition
    T, E, start, _ = wm
    alpha = [start[i] * E[i][h[0]] for i in range(12)]
    for w in h[1:]:
        alpha = [x * E[j][w] for j, x in enumerate(_vm(alpha, T))]
    return alpha
def ref_futures(wm, b):  # Q1 = b T E; J[v][u] = b T diag(E[:, v]) T E[:, u]
    T, E, _, TE = wm
    bt = _vm(b, T)
    return _vm(bt, E), [[sum((bt[k] * E[k][v] * TE[k][u] for k in range(12)), Q(0))
                         for u in range(5)] for v in range(5)]
def ref_parity(h) -> tuple[int, int]:  # (par(h), number of odd outside observations), 3.3
    par = m_odd = 0
    for s, w in enumerate(h):
        par ^= int(s > 0 and {h[s - 1], w} == {S3, S0})
        m_odd += int(w in (A, B) and par == 1)
    return par, m_odd
@lru_cache(maxsize=None)
def ref_history(h: tuple, variant: str = "frozen") -> dict:
    m, out = ref_model(variant), {}
    for f in "CM":
        alpha = ref_forward(m[f], h)
        out["P_" + f] = p = sum(alpha, Q(0))
        if p == 0:
            raise ValueError(f"impossible history {h}")
        out["b_" + f] = b = [x / p for x in alpha]
        out["Q1_" + f], out["J_" + f] = ref_futures(m[f], b)
        out["Q2dist_" + f] = [sum((r[u] for r in out["J_" + f]), Q(0)) for u in range(5)]
    pi = out["P_M"] / (out["P_C"] + out["P_M"])
    out.update(P=(out["P_C"] + out["P_M"]) / 2, pi=pi,
               b_mix=[(1 - pi) * x for x in out["b_C"]] + [pi * x for x in out["b_M"]])
    out["Q1"], out["Q2dist"] = (_mix(out[k + "_C"], out[k + "_M"], pi) for k in ("Q1", "Q2dist"))
    out["J"] = [_mix(rc, rm, pi) for rc, rm in zip(out["J_C"], out["J_M"])]
    out["par"], out["informed"] = ref_parity(h)[0], ref_parity(h)[1] > 0
    return out
@lru_cache(maxsize=None)
def ref_enumerate(K: int) -> dict:  # every h, len <= K, with P_C > 0 or P_M > 0 -> (aC, aM)
    m, level, nodes = ref_model(), [()], {}
    for _ in range(K):
        cand = {h + (w,): tuple(ref_forward(m[f], h + (w,)) for f in "CM")
                for h in level for w in range(5)}
        level = [h for h, al in cand.items() if any(map(any, al))]
        nodes.update((h, cand[h]) for h in level)
    return nodes
def ref_marginals(variant: str, K: int = 8) -> dict:  # P_f(W_t = v), t = 1..K, from the start
    out = {}
    for f, (T, E, start, _) in ref_model(variant).items():
        p, out[f] = list(start), []
        for _ in range(K):
            out[f].append(_vm(p, E))
            p = _vm(p, T)
    return out

KEYS = ("P_C", "P_M", "P", "pi", "b_C", "b_M", "b_mix", "Q1_C", "Q1_M", "Q1", "J_C", "J_M", "J",
        "Q2dist_C", "Q2dist_M", "Q2dist")
def check_module(h: tuple, variant: str = "frozen") -> dict:  # module == reference on every key
    got, exp = d1_seam.exact_history(h, variant=variant), ref_history(h, variant)
    for k in KEYS:
        assert _norm(got[k]) == _norm(exp[k]), (h, variant, k)
    assert int(got["par"]) == exp["par"] and bool(got["informed"]) == exp["informed"], h
    return exp

def test_constants():
    assert (d1_seam.S0, d1_seam.S2, d1_seam.S3, d1_seam.A, d1_seam.B, d1_seam.K_DEPTH,
            tuple(d1_seam.VARIANTS)) == (0, 1, 2, 3, 4, 8, ("frozen", "N1", "N2", "N3", "L1", "L2"))
    assert (d1_seam.H_STAR, d1_seam.H_A, d1_seam.H_B, d1_seam.H_EDGE, d1_seam.H_MAX) == (
        H_STAR, H_A, H_B, H_EDGE, H_MAX)
@pytest.mark.parametrize("variant", ["frozen", "N1", "N2", "N3", "L1", "L2"])
def test_exact_model_matches_reference(variant):
    got, (T, E, mu) = d1_seam.exact_model(variant), ref_mixture(variant)
    assert (_norm(got["T"]), _norm(got["E"]), _norm(got["mu"])) == (_norm(T), _norm(E), _norm(mu))
    assert all(_norm(d1_seam.exact_world_T(f)) == _norm(ref_T(f)) for f in "CM")
    if variant in ("frozen", "N2", "L2"):
        assert _norm(d1_seam.exact_E(variant)) == _norm(ref_model(variant)["C"][1])
def test_float_model_is_the_production_kernels():
    fm, worlds = d1_seam.float_model(), d1_seam.build_worlds()
    for f in "CM":
        prod, exact = TransitionBuilder().build(worlds[f], TransitionConfig(p_stay=0.2)).T, ref_T(f)
        assert fm["T_" + f].dtype == np.float64 and np.array_equal(fm["T_" + f], prod)
        assert np.array_equal(prod > 0, np.array([[v > 0 for v in r] for r in exact]))
        assert max(abs(Q(float(prod[i, j])) - exact[i][j]) for i in range(12)
                   for j in range(12)) <= Q(1, 10**15)
    T, E = np.zeros((24, 24)), np.array([[float(v) for v in r] for r in E_LIT])
    T[:12, :12], T[12:, 12:] = fm["T_C"], fm["T_M"]
    assert np.array_equal(fm["T"], T) and np.array_equal(fm["E_mix"], np.vstack((E, E)))
    assert np.array_equal(fm["E"], E) and np.array_equal(fm["mu"], np.eye(24)[[3, 15]].sum(0) / 2)
    assert np.array_equal(fm["mu_C"], np.eye(12)[3]) and np.array_equal(fm["mu_M"], np.eye(12)[3])
def _square_boundary(cell) -> dict:  # square (v00, v01, v10, v11) -> {canonical edge: sign}
    v00, v01, v10, v11 = (int(v) for v in cell)
    out: dict = {}
    for (u, w), s in (((v10, v11), 1), ((v00, v01), -1), ((v01, v11), -1), ((v00, v10), 1)):
        out[(min(u, w), max(u, w))] = out.get((min(u, w), max(u, w)), 0) + (s if u < w else -s)
    return out
def _rank_mod(rows, p: int) -> int:
    m, rank = [[x % p for x in r] for r in rows], 0
    for c in range(len(m[0])):
        piv = next((r for r in range(rank, len(m)) if m[r][c]), None)
        if piv is not None:
            m[rank], m[piv] = m[piv], m[rank]
            m[rank] = [x * pow(m[rank][c], p - 2, p) % p for x in m[rank]]
            m = [r if i == rank or not r[c] else [(x - r[c] * y) % p for x, y in zip(r, m[rank])]
                 for i, r in enumerate(m)]
            rank += 1
    return rank
def test_worlds_edges_boundary_and_orientability():  # G0.3; G0O: components 2/1, GF(3) ranks 7/8
    worlds = d1_seam.build_worlds()
    assert worlds["C"].family == "cylinder" and worlds["M"].family == "_d1_mobius_local"
    assert ref_edges("C") ^ ref_edges("M") == {(0, 9), (2, 11), (2, 9), (0, 11)}
    for f, n_comp, rank3 in (("C", 2, 7), ("M", 1, 8)):
        spec = worlds[f]
        assert {tuple(sorted(map(int, e))) for e in np.asarray(spec.edges)} == ref_edges(f)
        bnds = [_square_boundary(c) for c in np.asarray(spec.cells[2])]
        assert len(bnds) == 8 and all(sorted(map(abs, b.values())) == [1] * 4 for b in bnds)
        count = {e: sum(e in b for b in bnds) for e in ref_edges(f)}
        bdry, inner = ([e for e, n in count.items() if n == k] for k in (1, 2))
        assert len(bdry) == 8 and len(inner) == 12
        verts = sorted({v for e in bdry for v in e})  # components = V - rank(incidence)
        inc = np.array([[int(v == e[0]) - int(v == e[1]) for e in bdry] for v in verts])
        assert len(verts) - np.linalg.matrix_rank(inc) == n_comp
        rows = [[b.get(e, 0) for b in bnds] for e in inner]
        assert _rank_mod(rows, 3) == rank3 and 8 - _rank_mod(rows, 2) == 1
def test_registry_untouched_by_import_and_build(monkeypatch):
    before = dict(WORLD_REGISTRY)
    assert before == _REGISTRY_BEFORE_IMPORT
    spec = importlib.util.spec_from_file_location("_d1_seam_fresh_copy", d1_seam.__file__)
    fresh = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "_d1_seam_fresh_copy", fresh)
    spec.loader.exec_module(fresh)
    assert dict(WORLD_REGISTRY) == before
    fresh.build_worlds(), d1_seam.build_worlds()
    assert dict(WORLD_REGISTRY) == before and "_d1_mobius_local" not in WORLD_REGISTRY
def test_geometry_helpers_are_never_called(monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("point_distances / is_x_periodic must not be called")
    originals = {n: getattr(_geometry, n) for n in ("point_distances", "is_x_periodic")}
    for mod in list(sys.modules.values()):
        for name, fn in originals.items():
            if getattr(mod, "__dict__", {}).get(name) is fn:
                monkeypatch.setattr(mod, name, boom)
    assert _geometry.point_distances is boom and _geometry.is_x_periodic is boom
    assert set(d1_seam.build_worlds()) == {"C", "M"}
    assert d1_seam.float_model()["T"].shape == (24, 24)
    assert Q(d1_seam.exact_history(H_STAR)["P"]) == Q(3, 100)
def test_module_file_at_most_400_lines():
    path = REPO_ROOT / "tools" / "d1_seam" / "d1_seam.py"
    assert Path(d1_seam.__file__).resolve() == path.resolve()
    with open(path, encoding="utf-8") as fh:
        assert sum(1 for _ in fh) <= 400

def test_h_star_closed_forms_and_chain_identity():
    r = check_module(H_STAR)
    assert r["P_C"] == r["P_M"] == r["P"] == Q(3, 100) and r["pi"] == Q(1, 2)
    assert r["b_C"] == r["b_M"] == unit(idx(3, 0)) and r["Q1_C"] == r["Q1_M"] == r["Q1"] == NU
    J_C = _rows("3/25 0 1/25 3/100 1/100", "0 3/25 1/25 3/100 1/100", "3/25 3/25 9/25 0 0",
                "0 0 0 0 0", "0 0 0 0 0")
    J_M = [list(row) for row in J_C]
    J_M[S0][A:] = [Q(1, 100), Q(3, 100)]
    assert r["J_C"] == J_C and r["J_M"] == J_M
    assert r["Q2dist_C"] == _vec("6/25 6/25 11/25 3/50 1/50")
    assert r["Q2dist_M"] == _vec("6/25 6/25 11/25 1/25 1/25")
    assert tv(J_C, J_M) == tv(r["Q2dist_C"], r["Q2dist_M"]) == Q(1, 50)
    assert d1_seam.tv(J_C, J_M) == Q(1, 50) and d1_seam.tv(NU, unit(0, 5)) == Q(4, 5)
    e0, e2 = check_module(H_STAR + (S0,)), check_module(H_STAR + (S2,))
    assert tv(e0["Q1_C"], e0["Q1_M"]) == Q(1, 10) and tv(e2["Q1_C"], e2["Q1_M"]) == 0
    assert tv(J_C, J_M) == AX * Q(1, 10)  # chain identity
def test_posterior_isolation_pair():
    a10, d30 = AX**10, unit(idx(3, 0))
    ra, rb = check_module(H_A), check_module(H_B)
    assert (ra["P_C"], ra["P_M"], rb["P_C"], rb["P_M"]) == (
        Q(27, 64) * a10, Q(9, 64) * a10, Q(9, 64) * a10, Q(27, 64) * a10)
    assert ra["pi"] == Q(1, 4) and rb["pi"] == Q(3, 4)
    assert ra["P"] == rb["P"] == Q(9, 32) * a10 == Q(9, 312_500_000)
    for r in (ra, rb):
        assert r["b_C"] == r["b_M"] == d30 and r["Q1"] == NU and r["par"] == 0 and r["informed"]
        assert r["b_mix"] == [(1 - r["pi"]) * x for x in d30] + [r["pi"] * x for x in d30]
        assert r["J_C"] == ref_history(H_STAR)["J_C"] and r["J_M"] == ref_history(H_STAR)["J_M"]
    assert ra["Q2dist"] == _vec("6/25 6/25 11/25 11/200 5/200")
    assert rb["Q2dist"] == _vec("6/25 6/25 11/25 9/200 7/200")
    pair = tv(ra["J"], rb["J"])
    assert pair == tv(ra["Q2dist"], rb["Q2dist"]) == Q(1, 100)
    assert pair == abs(ra["pi"] - rb["pi"]) * tv(ra["J_C"], ra["J_M"])  # F3
    mid = [_mix(x, y, Q(1, 2)) for x, y in zip(ra["J"], rb["J"])]
    assert tv(mid, ra["J"]) == tv(mid, rb["J"]) == Q(1, 200)
def test_band_edge_and_h_max_probe():
    r = check_module(H_EDGE)
    assert (r["P_C"], r["P_M"]) == (Q(9, 16) * AX**5, Q(3, 16) * AX**5)
    assert r["pi"] == Q(1, 4) and r["P"] == Q(3, 8) * AX**5 == Q(3, 25_000)
    assert r["b_C"] == unit(idx(2, 0)) and r["b_M"] == unit(idx(2, 2))
    assert r["Q1_C"] == _vec("0 3/5 1/5 3/20 1/20") and r["Q1_M"] == _vec("0 3/5 1/5 1/20 3/20")
    assert tv(r["Q1_C"], r["Q1_M"]) == Q(1, 10) and r["Q1"] == _vec("0 3/5 1/5 1/8 3/40")
    r, a2 = check_module(H_MAX), AX**2
    assert (r["P_C"], r["P_M"]) == (Q(9, 80) * AX**6, Q(3, 40) * AX**6)
    assert r["pi"] == Q(2, 5) and r["P"] == Q(3, 500_000)
    assert rho(r["b_C"]) == _vec("1/2 1/2 0") and rho(r["b_M"]) == _vec("3/4 1/4 0")
    assert (r["J_C"][S2][A], r["J_M"][S2][A]) == (5 * a2 / 8, 11 * a2 / 16)
    assert (r["J_C"][S0][A], r["J_M"][S0][A]) == (5 * a2 / 8, 5 * a2 / 16)
    assert tv(r["J_C"], r["J_M"]) == Q(3, 200) and tv(r["Q2dist_C"], r["Q2dist_M"]) == Q(1, 100)
def test_reachable_counts_by_recursion():
    v, N, HI = [0, 2, 0, 0], [2], [0]
    for _ in range(7):
        v = [(2 if x == 1 else 1) * (v[x - 1] + v[x] + v[(x + 1) % 4]) for x in range(4)]
        N, HI = N + [sum(v)], HI + [v[3]]
    assert N == N_T and HI == HI_T and sum(N) == 37_190 and sum(HI) == 5_348
def test_exhaustive_enumeration_to_depth_5():  # counts, Lemma B, C(a), A, D2, F1/F2 + module
    nodes = ref_enumerate(5)
    assert [sum(len(h) == t for h in nodes) for t in range(1, 6)] == N_T[:5]
    assert [sum(len(h) == t and h[-1] == S3 for h in nodes) for t in range(1, 6)] == HI_T[:5]
    assert len(nodes) == 646
    for h, (ac, am) in nodes.items():
        (pc, pm), (par, m_odd) = (sum(ac, Q(0)), sum(am, Q(0))), ref_parity(h)
        assert pc > 0 and pm > 0 and Q(1, 3**m_odd) <= pm / pc <= 3**m_odd, h
        if m_odd == 0:
            assert pc == pm and all(am[idx(x, y)] == ac[idx(x, 2 - y if par else y)]
                                    for x in range(4) for y in range(3)), h
        if h[-1] != S3:
            if len(h) <= 4:
                check_module(h)
            continue
        r = check_module(h)
        assert r["Q1_C"] == r["Q1_M"] == r["Q1"] == NU, h
        gap, ends = tv(r["J_C"], r["J_M"]), [ref_history(h + (w,)) for w in (S0, S2)]
        assert gap == AX * sum(tv(e["Q1_C"], e["Q1_M"]) for e in ends), h
        dc, dm = (rho(r[k])[0] - rho(r[k])[2] for k in ("b_C", "b_M"))
        assert gap == AX**2 / 2 * max(abs(dc), abs(dm)), h
        assert tv(r["Q2dist_C"], r["Q2dist_M"]) == AX**2 / 2 * abs(dc), h
    for bad in ((S0,), (A, S3), (A, A, S3)):
        with pytest.raises(ValueError):
            d1_seam.exact_history(bad)
def test_start_law_artefact_and_decision_phase_mass():
    m = ref_marginals("frozen")
    assert [m["C"][t][A] - m["M"][t][A] for t in range(8)] == D_T
    for t in range(8):
        assert all(m["C"][t][v] == m["M"][t][v] for v in (S0, S2, S3))
        assert tv(m["C"][t], m["M"][t]) == abs(D_T[t])
    mass = [(m["C"][t][S3] + m["M"][t][S3]) / 2 for t in range(8)]
    assert mass == HI_MASS == [(1 - 2 * Q(3, 5)**t + Q(1, 5)**t) / 4 for t in range(8)]
    for variant in ("N1", "N2", "N3"):
        mv = ref_marginals(variant)
        assert all(mv["C"][t][A] == mv["M"][t][A] for t in range(8)), variant
@pytest.mark.parametrize("name", ["G0", "G0S", "G0O", "G1", "G3", "G6"])
def test_gates_pass(name):
    args = (d1_seam.build_worlds(),) if name.startswith("G0") else ()
    assert getattr(d1_seam, "gate_" + name)(*args)["status"] == "PASS"
def test_gate_G2_values():
    res = d1_seam.gate_G2()
    v = res["values"]
    assert res["status"] == "PASS"
    assert [int(x) for x in v["N_t"]] == N_T and [int(x) for x in v["HI_t"]] == HI_T
    assert [Q(x) for x in v["HI_mass_t"]] == HI_MASS and [Q(x) for x in v["D_t"]] == D_T
    assert int(v["max_branch_count"]) > 0
    assert all(int(n) == 0 for n in v["violations"].values()), v["violations"]
_DSTR = {Q(0): "0", Q(1): "1", Q(1, 5): "0.2", Q(2, 5): "0.4", Q(3, 4): "0.75", Q(1, 2): "0.5",
         Q(1, 4): "0.25"}
def test_decimal_trap():  # section 6.2; Decimal -> Fraction directly, never through float
    h, (T, E, mu) = (A, A), ref_mixture()
    exact = ref_history(h)["b_mix"]
    assert exact == [Q(0)] * 3 + [Q(3, 8), Q(1, 8)] + [Q(0)] * 10 + [Q(3, 8), Q(1, 8)] + [Q(0)] * 7
    assert all(Q(Decimal(s)) == q for q, s in _DSTR.items())
    T_d = [[Decimal(_DSTR[q]) for q in row] for row in T]  # Decimal objects built from strings
    E_d, mu_d = [[Decimal(_DSTR[q]) for q in row] for row in E], [Decimal(_DSTR[q]) for q in mu]
    fr = [Q(d) for d in ref.decimal_suffix_posterior(T_d, E_d, mu_d, list(h), digits=80)]
    assert len(fr) == 24 and all(abs(x - q) <= Q(1, 10**45) for x, q in zip(fr, exact))
    assert abs(sum(fr[12:], Q(0)) - sum(exact[12:], Q(0))) <= Q(1, 10**45)  # pi
    T_prod = d1_seam.float_model()["T"]  # production float64 TransitionBuilder kernels
    post_f = ref.decimal_suffix_posterior(T_prod, E_d, mu_d, list(h), digits=80)
    gaps = [abs(Q(d) - q) for d, q in zip(post_f, exact)]
    assert max(gaps) > Q(1, 10**19), "the production-kernel trap did not fire"
    assert max(gaps) <= Q(1, 10**12)
def test_controls_N1_N2_null():
    for variant in ("N1", "N2"):
        ra, rb, r = (check_module(h, variant) for h in (H_A, H_B, H_STAR))
        assert ra["pi"] == rb["pi"] == Q(1, 2) and tv(r["J_C"], r["J_M"]) == 0, variant
    assert tv(check_module(H_A, "N1")["J"], check_module(H_B, "N1")["J"]) == 0
    assert tv(*(check_module(H_EDGE, "N1")[k] for k in ("Q1_C", "Q1_M"))) == 0
def test_control_N3_symmetric_start():
    r, ra, rb, e = (check_module(h, "N3") for h in (H_STAR, H_A, H_B, H_EDGE))
    assert tv(r["J_C"], r["J_M"]) == 0 and tv(e["Q1_C"], e["Q1_M"]) == 0
    assert ra["pi"] == rb["pi"] == Q(1, 2) and tv(ra["J"], rb["J"]) == 0
    inf = check_module((A, A, S2, S3, S0, A), "N3")
    assert inf["informed"] and inf["P_C"] / inf["P_M"] == Q(7, 5)
def test_control_L1_label_leak():
    r = check_module((A,), "L1")
    assert (r["P_C"], r["P_M"], r["pi"], r["informed"]) == (Q(3, 4), Q(1, 4), Q(1, 4), False)
    E = _norm(d1_seam.exact_model("L1")["E"])
    assert E[:12] != E[12:]
def test_control_L2_narrow_interior():
    m = d1_seam.exact_model("L2")
    T, E = [[Q(x) for x in row] for row in m["T"]], [[Q(x) for x in row] for row in m["E"]]
    for z in (0, 1):
        rows = [_vm(_vm(unit(12 * z + idx(3, y), 24), T), E) for y in (0, 2)]
        assert rows[0] != rows[1] and rows[0] != NU  # the G1.4 identity fails
    r = check_module((A, A, S3), "L2")
    assert r["Q1_C"] == _vec("1/5 0 3/5 3/20 1/20") != NU
@pytest.mark.parametrize("preflight", [{}, {"x": False}])
def test_run_without_passing_preflight_is_invalid(tmp_path, preflight):
    report = d1_seam.run(tmp_path, preflight)
    assert report["verdict"] == "INVALID"
    statuses = {str(k).removeprefix("gate_"): (v["status"] if isinstance(v, dict) else v)
                for k, v in report["gates"].items()}
    assert set(GATES) <= set(statuses) and set(statuses.values()) == {"NOT_RUN"}, statuses
    assert json.loads((tmp_path / "report.json").read_bytes())["verdict"] == "INVALID"
