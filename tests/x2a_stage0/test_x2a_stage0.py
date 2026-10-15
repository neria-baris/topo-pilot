"""Independent tests of tools/x2a_stage0 (job 0025), part 1: construction, exact laws, JS, nulls.

Written from X2A-FROZEN-v1 and tools/x2a_stage0/API.md only. The module is imported, never read.
Every ``ref_*`` reference is coded from the protocol's formulas (numpy, fractions, decimal, math)
and imports nothing from the module; module outputs are only compared against it (protocol 8.4)."""

from __future__ import annotations

import importlib.util
import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.oracle import BayesFilter
from topo_pilot.process import _geometry
from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation
from topo_pilot.process.transition import TransitionBuilder, TransitionConfig
from topo_pilot.world import WORLD_REGISTRY, CubicalComplex, Identification

pytestmark = pytest.mark.oracle

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = REPO_ROOT / "tools" / "x2a_stage0"
for _parts in (("tools", "x2a_stage0"), ("tools", "x4_oracle_profile"),
               ("tests", "oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

_REGISTRY_BEFORE_IMPORT = dict(WORLD_REGISTRY)
import oracle_profile as op  # noqa: E402
import x2a_mc as xc  # noqa: E402, F401
import x2a_model as xm  # noqa: E402
import x2a_ph as xp  # noqa: E402, F401

_REGISTRY_AFTER_IMPORT = dict(WORLD_REGISTRY)

V, SIG2 = 36, 2 * 1.25**2  # 2 sigma^2 = 3.125 (section 2.3)
GRID = np.arange(12)
SX, SY = (a.ravel() for a in np.meshgrid(GRID, GRID, indexing="ij"))  # state 12x + y -> (x, y)
CENTRES = 0.5 + 2.0 * np.arange(6)
VARIANTS = ("main", "N-iso", "N-same", "N-id", "N-swap", "P-ref", "N-local")
LN2 = math.log(2.0)


def ref_d12(u, v) -> np.ndarray:  # section 0: delta_12
    r = np.mod(np.abs(np.asarray(u, dtype=float) - np.asarray(v, dtype=float)), 12.0)
    return np.minimum(r, 12.0 - r)
def ref_e() -> np.ndarray:  # section 2.3: e[x, a], 12 x 6
    w = np.exp(-ref_d12(GRID[:, None], CENTRES[None, :]) ** 2 / SIG2)
    return w / w.sum(axis=1, keepdims=True)
def ref_field_2d(mode: str = "min") -> np.ndarray:
    """G1 reference: squared distance over the 9 deck images (m, n in {-1, 0, 1}), then a 2-D
    softmax over the 36 centres. ``min`` is the protocol's minimum image (A1); ``sum`` sums the
    9 Gaussian images (the rejected reading, used only by the negative test)."""
    cx, cy = np.repeat(CENTRES, 6), np.tile(CENTRES, 6)  # token 6a + b -> (0.5 + 2a, 0.5 + 2b)
    dx, dy = SX[:, None] - cx[None, :], SY[:, None] - cy[None, :]
    sq = np.stack([(dx + 12.0 * m) ** 2 + (dy + 12.0 * n) ** 2
                   for m in (-1, 0, 1) for n in (-1, 0, 1)])
    if mode == "sum":
        w = np.exp(-sq / SIG2).sum(axis=0)
        return w / w.sum(axis=1, keepdims=True)
    logit = -sq.min(axis=0) / SIG2
    top = logit.max(axis=1, keepdims=True)
    lse = top + np.log(np.exp(logit - top).sum(axis=1, keepdims=True))
    return np.exp(logit - lse)
def ref_neighbours(i: int) -> set[int]:  # the 4 torus neighbours of state i
    x, y = divmod(i, 12)
    return {12 * ((x + dx) % 12) + (y + dy) % 12 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
def ref_G(e: np.ndarray, d: int) -> float:  # T2: G(d) = sum_x e[x, 0] e[x + d, 0]
    return math.fsum(float(e[x, 0] * e[(x + d) % 12, 0]) for x in range(12))
def ref_pair(T: np.ndarray, E: np.ndarray) -> np.ndarray:  # section 4.1 item 1
    return E.T @ T @ E / T.shape[0]
def ref_law2(T: np.ndarray, E: np.ndarray) -> np.ndarray:  # explicit sum over z1, then z2
    n, out = T.shape[0], np.zeros((E.shape[1], E.shape[1]))
    for z1 in range(n):
        out += np.outer(E[z1], T[z1] @ E) / n
    return out
def ref_law3(T: np.ndarray, E: np.ndarray) -> np.ndarray:  # backward recursion, loop over w2
    n, v = T.shape[0], E.shape[1]
    tail, out = T @ E, np.zeros((v, v, v))  # tail[z2, w3] = sum_z3 T[z2, z3] E[z3, w3]
    for w2 in range(v):
        out[:, w2, :] = E.T @ (T @ (E[:, w2, None] * tail)) / n
    return out
def ref_js(pa, pb) -> float:  # JS with weights 1/2: 1/2 KL(PA || M) + 1/2 KL(PB || M)
    pa, pb = np.asarray(pa, dtype=float).ravel(), np.asarray(pb, dtype=float).ravel()
    m = 0.5 * (pa + pb)
    with np.errstate(divide="ignore", invalid="ignore"):
        ta = np.where(pa > 0, pa * np.log(pa / np.where(m > 0, m, 1.0)), 0.0)
        tb = np.where(pb > 0, pb * np.log(pb / np.where(m > 0, m, 1.0)), 0.0)
    return 0.5 * (math.fsum(ta) + math.fsum(tb))
def ref_acc(pa, pb) -> float:  # section 4.1 item 4
    return 0.5 * math.fsum(np.maximum(np.ravel(pa), np.ravel(pb)))
def ref_phi(r: float) -> float:  # phi(r) in 50-digit decimal arithmetic, closed form
    with localcontext() as ctx:
        ctx.prec = 50
        one, x = Decimal(1), Decimal(r)
        return float(((one + x) * (one + x).ln() + (one - x) * (one - x).ln()) / 2)


@pytest.fixture(scope="module")
def spec():
    return xm.build_world()
@pytest.fixture(scope="module")
def models(spec):
    return {v: xm.variant_model(v, spec) for v in VARIANTS}


def test_constants_and_index_helpers():
    assert (xm.N_SIDE, xm.N, xm.N_MIX, xm.V) == (12, 144, 288, 36)
    assert (xm.SIGMA, xm.P_STAY, xm.ALPHA, xm.TAU, xm.Z99) == (1.25, 0.2, 0.2, 1e-12, 2.576)
    assert (xm.T_STAR, xm.K_S, xm.BLOCK, xm.N_BLOCKS) == (32, 8, 8, 4)
    assert tuple(xm.WINDOWS) == (1, 2, 4, 8) and tuple(xm.VARIANTS) == VARIANTS
    assert (xm.MASTER_X2A0, xm.FAMILY) == (20261015, "_x2a_torus_local")
    assert xm.BASE_COMMIT == "c364f95e5573940cdc24b569b0fb7c6a16c97ab8"
    assert xm.REQUEST_SHA256.upper() == (
        "4132C43812F50171F118C61FB69B8111B068B7BF598C03E30CE00F9C7DC94595")
    assert xm.PROTOCOL_SHA256.upper() == (
        "C80808CB7F22D9A171385FCB1AB7D03973E80DAFE638DFA758B6A84CA8341939")
    assert (xm.state(0, 0), xm.state(13, -1), xm.state(11, 11)) == (0, 23, 143)
    assert (xm.token(0, 0), xm.token(3, 0), xm.token(5, 5)) == (0, 18, 35)
    got = xm.delta12(np.array([0.0, 0.0, 0.0, 3.0, 1.0]), np.array([5.0, 7.0, 11.5, 9.0, 1.0]))
    assert np.array_equal(np.asarray(got, dtype=float), [5.0, 5.0, 0.5, 6.0, 0.0])


def test_E_A_matches_minimum_image_softmax():  # 8.4 test 1; G1.1
    e, E_A = xm.field_e(), xm.emission_A()
    assert e.shape == (12, 6) and E_A.shape == (144, 36) and E_A.dtype == np.float64
    assert np.max(np.abs(e - ref_e())) <= 1e-15
    ref = ref_field_2d("min")
    err = np.abs(E_A - ref)
    assert np.all(err <= 1e-15) and np.all(err <= 1e-12 * ref)
    assert np.max(np.abs(xm.emission_A(e) - E_A)) <= 1e-16
    p = {0.5: 0.589233, 1.5: 0.310698, 2.5: 0.0863856, 3.5: 0.0126647, 4.5: 0.000979,
         5.5: 0.0000399}  # section 2.3 hand values [W]
    col0 = [p[d] for d in (0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 5.5, 4.5, 3.5, 2.5, 1.5)]
    assert np.max(np.abs(e[:, 0] - col0)) <= 1e-6
def test_summed_images_differ_from_minimum_image():  # 8.4 test 1, negative test
    s, j = xm.state(0, 0), xm.token(3, 0)  # state (0, 0), centre (6.5, 0.5)
    e_min, e_sum = ref_field_2d("min"), ref_field_2d("sum")
    assert abs(e_min[s, j] - e_sum[s, j]) > 1e-7
    assert abs(xm.emission_A()[s, j] - e_sum[s, j]) > 1e-7


def test_world_counts_betti_and_builder(spec):  # 8.4 test 2; G0.1-G0.3
    B = xm._X2aTorusBuilder
    assert B.family == "_x2a_torus_local" and dict(B.expected_betti) == {2: (1, 2, 1),
                                                                          3: (1, 2, 1)}
    assert tuple(B.identifications) == (Identification(0, "periodic"),
                                        Identification(1, "periodic"))
    assert spec.family == B.family and tuple(spec.dims) == (12, 12) and spec.metric == "flat"
    assert sorted(spec.cells) == [0, 1, 2]
    assert [len(spec.cells[k]) for k in (0, 1, 2)] == [144, 288, 144]
    cx = CubicalComplex(spec.n_states, spec.cells)
    assert cx.euler_characteristic() == 0 and cx.betti(2) == (1, 2, 1) and cx.betti(3) == (1, 2, 1)
    assert (cx.boundary_matrix(1) @ cx.boundary_matrix(2)).count_nonzero() == 0
    edges = {tuple(sorted(map(int, e))) for e in np.asarray(spec.edges)}
    assert edges == {tuple(sorted((i, j))) for i in range(144) for j in ref_neighbours(i)}
    assert len(edges) == 288 and np.all(np.bincount(np.asarray(spec.edges).ravel()) == 4)
    assert np.array_equal(np.asarray(spec.coords), np.stack([SX, SY], axis=1).astype(float))
    flat = np.hypot(ref_d12(SX[:, None], SX[None, :]), ref_d12(SY[:, None], SY[None, :]))
    assert np.max(np.abs(np.asarray(spec.dist) - flat)) <= 1e-12
def test_kernel_matches_fraction_formula(spec):  # 8.4 test 2; G0.3-G0.4
    T = xm.kernel(spec)
    prod = TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2))
    assert T.dtype == np.float64 and np.array_equal(T, prod.T) and prod.d_max == 4
    support = np.zeros((144, 144), dtype=bool)
    for i in range(144):
        support[i, sorted(ref_neighbours(i) | {i})] = True
    assert np.array_equal(T > 0, support) and np.all(T[~support] == 0.0)
    assert all(abs(Q(float(v)) - Q(1, 5)) <= Q(1, 10**15) for v in np.unique(T[support]))
    assert np.array_equal(T, T.T)
    assert xm.gate_G0(spec, T)["status"] == "PASS"
def test_mixture_blocks_and_stationarity(models):  # G0.5-G0.6, section 2.5
    m = models["main"]
    T, Tt, Et, pit = m["T"], m["Tt"], m["Et"], m["pit"]
    assert Tt.shape == (288, 288) and Et.shape == (288, 36) and pit.shape == (288,)
    assert np.array_equal(Tt[:144, :144], T) and np.array_equal(Tt[144:, 144:], T)
    assert not Tt[:144, 144:].any() and not Tt[144:, :144].any()
    assert np.array_equal(Et[:144], m["E1"]) and np.array_equal(Et[144:], m["E2"])
    assert np.array_equal(pit, np.full(288, 1 / 288))
    assert np.max(np.abs(pit @ Tt - pit)) <= 1e-15
    op.validate_process(Tt, Et, pit, tol=1e-12)
    Tt2, Et2, pit2 = xm.mixture(T, m["E1"], m["E2"])
    assert np.array_equal(Tt2, Tt) and np.array_equal(Et2, Et) and np.array_equal(pit2, pit)


def test_emission_variants_against_reference(spec, models):  # G1.2-G1.7, section 2.6
    E_A = models["main"]["E1"]
    assert np.max(np.abs(E_A - ref_field_2d())) <= 1e-15
    dehn, iso = 12 * ((SX + SY) % 12) + SY, 12 * ((SX + 1) % 12) + SY
    assert np.array_equal(xm.dehn_perm(), dehn) and np.array_equal(xm.iso_perm(), iso)
    assert np.array_equal(np.sort(dehn), np.arange(144))  # phi is a bijection
    nb0 = {int(b) for a, b in np.asarray(spec.edges) if int(a) == 0}
    assert dehn[1] == 13 and 1 in nb0 and 13 not in nb0  # (0,0)-(0,1) -> (0,0)-(1,1): no edge
    E_B = E_A[dehn]
    sx, sy = draw_axis_permutation(spec)
    perm = axis_state_perm(sx, sy, (12, 12))
    up, dn = 12 * ((SX + 2) % 12) + SY, 12 * ((SX - 2) % 12) + SY
    E_N = 0.75 * E_A + 0.125 * E_A[up] + 0.125 * E_A[dn]
    blocks = {"main": (E_A, E_B), "N-iso": (E_A, E_A[iso]), "N-same": (E_A, E_A),
              "N-swap": (E_B, E_A), "P-ref": (E_A, E_A[perm])}
    for v, (e1, e2) in blocks.items():
        m = models[v]
        assert np.array_equal(m["E1"], e1) and np.array_equal(m["E2"], e2), v
        assert np.array_equal(m["Et"], np.vstack((e1, e2))), v
        assert np.array_equal(m["Tt"][144:, 144:], m["T"]), v
    loc = models["N-local"]
    assert np.array_equal(loc["E1"], E_A) and np.max(np.abs(loc["E2"] - E_N)) <= 1e-15
    E3 = E_A.reshape(144, 6, 6)  # Proposition N(3): the symbol channel a -> a + xi
    chan = 0.75 * E3 + 0.125 * np.roll(E3, 1, axis=1) + 0.125 * np.roll(E3, -1, axis=1)
    assert np.max(np.abs(loc["E2"] - chan.reshape(144, 36))) <= 1e-15
    assert np.max(np.abs(xm.emission_local(E_A) - E_N)) <= 1e-15
    nid = models["N-id"]["Et"]
    assert nid.shape == (288, 36) and np.max(np.abs(nid - 1 / 36)) <= 1e-17
    pref = models["P-ref"]
    assert np.array_equal(pref["sx"], sx) and np.array_equal(pref["sy"], sy)
    assert np.array_equal(pref["state_perm"], perm)
    E_P, sx2, sy2, perm2 = xm.emission_pref(spec, E_A)
    assert np.array_equal(E_P, E_A[perm]) and np.array_equal(perm2, perm)
    assert np.array_equal(sx2, sx) and np.array_equal(sy2, sy)
    for E in (E_A, E_B, E_N, E_P):
        assert np.max(np.abs(E.sum(axis=1) - 1.0)) <= 1e-14 and E.min() > 0
        assert np.max(np.abs(E.sum(axis=0) - 4.0)) <= 1e-12  # T1 column sums
    for E in (E_B, E_P):
        assert np.array_equal(np.sort(E_A, axis=0), np.sort(E, axis=0))
    E4 = E_A.reshape(12, 12, 6, 6)  # Z_6^2 equivariance, x then y
    for ax_s, ax_j in ((0, 2), (1, 3)):
        assert np.max(np.abs(np.roll(np.roll(E4, -2, axis=ax_s), -1, axis=ax_j) - E4)) <= 1e-15
    assert E_A.min() == pytest.approx(ref_field_2d().min(), rel=1e-12)
    assert 1.5e-9 < E_A.min() < 1.7e-9  # p(5.5)^2
    assert xm.gate_G1(models)["status"] == "PASS"


def test_T1_T2_and_lemma_U_closed_forms(models):  # 8.4 test 3; G2.1-G2.3
    e = ref_e()
    g0, g1 = ref_G(e, 0), ref_G(e, 1)
    drep = (0.2 / 2) * g1 * (g0 - g1)
    assert abs(g0 - 0.902705) <= 1e-5 and abs(g1 - 0.769235) <= 1e-5
    assert abs(drep - 0.010267) <= 1e-5 and drep > 0
    em = xm.field_e()
    assert all(abs(xm.G_overlap(em, d) - ref_G(e, d)) <= 1e-14 for d in range(7))
    assert abs(xm.delta_rep_closed(em) - drep) <= 1e-14  # the G2.2 tolerance
    m = models["main"]
    T, E_A, E_B = m["T"], m["E1"], m["E2"]
    assert np.max(np.abs(E_A.sum(axis=0) - 4.0)) <= 1e-12
    assert np.max(np.abs(E_B.sum(axis=0) - 4.0)) <= 1e-12
    MA, MB = ref_pair(T, E_A), ref_pair(T, E_B)
    assert abs(np.trace(MA) - 0.179622) <= 1e-5 and abs(np.trace(MB) - 0.169355) <= 1e-5
    assert abs((np.trace(MA) - np.trace(MB)) - drep) <= 1e-14
    assert np.max(np.abs(xm.pair_law(T, E_A) - MA)) <= 1e-15
    assert np.max(np.abs(xm.pair_law(T, E_B) - MB)) <= 1e-15
    Tu = np.zeros((144, 144))  # Lemma U: the K_B walk 0, +-(1, 0), +-(1, 1), each 1/5
    for i in range(144):
        x, y = divmod(i, 12)
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (1, 1), (-1, -1)):
            Tu[i, 12 * ((x + dx) % 12) + (y + dy) % 12] += 0.2
    assert np.max(np.abs(MB - ref_pair(Tu, E_A))) <= 1e-15


def test_exact_enumeration_k2_k3(models):  # 8.4 test 4; G2.5
    m = models["main"]
    T, E_A, E_B = m["T"], m["E1"], m["E2"]
    laws = {}
    for c, E in (("A", E_A), ("B", E_B)):
        l2, l3 = ref_law2(T, E), ref_law3(T, E)
        assert np.allclose(l3.sum(axis=2), l2, rtol=1e-12, atol=0)
        assert np.max(np.abs(xm.window_law(T, E, 1) - 1 / 36)) <= 1e-15  # T1
        assert np.allclose(xm.window_law(T, E, 2), l2.ravel(), rtol=1e-12, atol=0), c
        assert np.allclose(xm.window_law(T, E, 3), l3.ravel(), rtol=1e-12, atol=0), c
        laws[c] = (l2.ravel(), l3.ravel())
    ref_I = [ref_js(laws["A"][k], laws["B"][k]) for k in (0, 1)]
    ref_a = [ref_acc(laws["A"][k], laws["B"][k]) for k in (0, 1)]
    cur = xm.exact_curve(T, E_A, E_B, kmax=3)
    I, acc = [float(x) for x in cur["I"]], [float(x) for x in cur["acc"]]
    assert len(I) == len(acc) == 3
    assert abs(I[0]) <= 1e-15 and abs(acc[0] - 0.5) <= 1e-15
    for k in (1, 2):
        assert abs(I[k] - ref_I[k - 1]) <= 1e-9 * ref_I[k - 1], k
        assert abs(acc[k] - ref_a[k - 1]) <= 1e-13, k
    assert I[1] > 0 and I[1] - I[0] >= -1e-15 and I[2] - I[1] >= -1e-15
    assert abs(I[1] - ref_js(ref_pair(T, E_A), ref_pair(T, E_B))) <= 1e-10 * I[1]
    pa, pb = np.trace(ref_pair(T, E_A)), np.trace(ref_pair(T, E_B))
    rep = ref_js([pa, 1 - pa], [pb, 1 - pb])  # the repeat indicator alone (T2)
    assert abs(rep - 9.149e-5) <= 1e-7 and I[1] >= rep


def test_js_on_toy_laws_and_series_branch():  # 8.4 test 5; section 4.1 item 3, 10.2 C1
    disjoint = xm.js_information(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    assert math.isclose(disjoint, LN2, rel_tol=1e-15)  # 2 ln 2 would be the C1 factor-2 error
    phi_end = np.asarray(xm.js_phi(np.array([1.0, -1.0, 0.0])), dtype=float)
    assert math.isclose(phi_end[0], LN2, rel_tol=1e-15) and math.isclose(phi_end[1], LN2,
                                                                         rel_tol=1e-15)
    assert phi_end[2] == 0.0
    small = np.array([1e-8, -1e-6, 1e-4, -5e-4, 9.9e-4])  # series branch, |r| < 1e-3
    for r, got in zip(small, np.asarray(xm.js_phi(small), dtype=float)):
        assert abs(got - ref_phi(r)) <= 1e-15 * ref_phi(r), r
    large = np.array([5e-3, -0.25, 0.5, 0.9, -0.999])
    for r, got in zip(large, np.asarray(xm.js_phi(large), dtype=float)):
        assert abs(got - ref_phi(r)) <= 1e-11 * ref_phi(r), r
    half = xm.js_information(np.array([0.5, 0.5, 0.0]), np.array([0.0, 0.5, 0.5]))
    assert math.isclose(half, 0.5 * LN2, rel_tol=1e-15)
    same = np.array([0.25, 0.25, 0.5, 0.0])
    assert xm.js_information(same, same.copy()) == 0.0
    pa, pb = np.array([0.5, 0.5, 0.0, 0.0]), np.array([0.25, 0.75, 0.0, 0.0])  # M = 0 entries
    assert math.isclose(xm.js_information(pa, pb), ref_js(pa, pb), rel_tol=1e-12)
    rng = np.random.default_rng(3)
    pa, pb = rng.dirichlet(np.ones(50)), rng.dirichlet(np.ones(50))
    assert math.isclose(xm.js_information(pa, pb), ref_js(pa, pb), rel_tol=1e-12)
    pa, pb = np.array([0.179622, 0.820378]), np.array([0.169355, 0.830645])
    assert abs(xm.js_information(pa, pb) - 9.149e-5) <= 1e-7
    assert xm.bayes_accuracy(np.array([1.0, 0.0]), np.array([0.0, 1.0])) == 1.0
    assert xm.bayes_accuracy(same, same.copy()) == 0.5
    assert math.isclose(xm.bayes_accuracy(np.array([0.7, 0.3]), np.array([0.4, 0.6])), 0.65,
                        rel_tol=1e-15)


def test_null_and_swap_identities_on_short_histories(models):  # 8.4 test 8; G5, G3.1
    tok = np.random.default_rng(20261015).integers(0, V, size=(64, 8))
    def run(v):
        m = models[v]
        res = BayesFilter(m["Tt"], m["Et"], m["pit"]).run(tok)
        return res, res.b[..., 144:].sum(axis=-1)
    main, pi = run("main")
    assert np.max(np.abs(pi - 0.5)) > 1e-6  # the main construction is informative
    for v in ("N-iso", "N-same"):
        assert np.max(np.abs(run(v)[1] - 0.5)) <= 1e-12, v
    assert np.max(np.abs(run("N-swap")[1] - (1.0 - pi))) <= 1e-12
    res_id, pi_id = run("N-id")
    assert np.max(np.abs(res_id.b - 1 / 288)) <= 1e-15 and np.max(np.abs(pi_id - 0.5)) <= 1e-15
    T, E_A = models["main"]["T"], models["main"]["E1"]
    assert np.max(np.abs(ref_law2(T, models["N-iso"]["E2"]) - ref_law2(T, E_A))) <= 1e-15  # T6
    for v, tol in (("N-iso", 1e-12), ("N-same", 1e-15)):  # G5 exact rows, here k <= 2
        exact_I = xm.exact_curve(T, E_A, models[v]["E2"], kmax=2)["I"]
        assert max(float(x) for x in exact_I) <= tol, v
    st = xm.stencil_filter(models["main"]["E1"], models["main"]["E2"], tok)
    assert np.asarray(st["b"]).shape == (64, 8, 288)
    assert np.max(np.abs(st["b"] - main.b)) <= 1e-12 and np.max(np.abs(st["pi"] - pi)) <= 1e-11
    assert np.max(np.abs(st["log_evidence"] - main.log_evidence)) <= 1e-10


def test_registry_untouched_by_import_and_build(monkeypatch):  # 8.4 test 9; R8
    assert _REGISTRY_AFTER_IMPORT == _REGISTRY_BEFORE_IMPORT
    before = dict(WORLD_REGISTRY)
    fresh = {}
    for name in ("x2a_model", "x2a_mc", "x2a_ph"):
        spec_ = importlib.util.spec_from_file_location(f"_{name}_fresh_copy",
                                                       MODULE_DIR / f"{name}.py")
        fresh[name] = importlib.util.module_from_spec(spec_)
        monkeypatch.setitem(sys.modules, f"_{name}_fresh_copy", fresh[name])
        spec_.loader.exec_module(fresh[name])
        assert dict(WORLD_REGISTRY) == before, name
    world = fresh["x2a_model"].build_world()
    fresh["x2a_model"].variant_model("main", world)
    xm.variant_model("P-ref")
    assert dict(WORLD_REGISTRY) == before and xm.FAMILY not in WORLD_REGISTRY


def test_geometry_helpers_are_never_called(monkeypatch):  # 8.4 test 10; R7
    def boom(*args, **kwargs):
        raise AssertionError("point_distances / is_x_periodic must not be called")
    originals = {n: getattr(_geometry, n) for n in ("point_distances", "is_x_periodic")}
    for mod in list(sys.modules.values()):
        for name, fn in originals.items():
            if getattr(mod, "__dict__", {}).get(name) is fn:
                monkeypatch.setattr(mod, name, boom)
    assert _geometry.point_distances is boom and _geometry.is_x_periodic is boom
    world = xm.build_world()
    built = {v: xm.variant_model(v, world) for v in VARIANTS}
    assert set(built) == set(VARIANTS) and xm.variant_model("main")["Et"].shape == (288, 36)
    xm.emission_pref(world, xm.emission_A())
    assert xm.gate_G0(world, xm.kernel(world))["status"] == "PASS"
    with pytest.raises(ValueError):
        xm.variant_model("not-a-variant", world)


@pytest.mark.parametrize("name", ["x2a_model", "x2a_mc", "x2a_ph"])
def test_module_files_at_most_400_lines(name):  # S6, 8.1
    path = MODULE_DIR / f"{name}.py"
    assert Path(sys.modules[name].__file__).resolve() == path.resolve()
    with open(path, encoding="utf-8") as fh:
        assert sum(1 for _ in fh) <= 400
