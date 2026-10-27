"""Author B (job 0119), TEST_PLAN §3 `test_b_worlds.py`: grid, keys, X1 worlds, tiers, the
rectangular centres, the emission builders (canonical OverlapGaussian at W = 12 bitwise, the
mirrored softmax elsewhere), features, the anchored alias map (CONTRACT `alias.maps`, §4.3
table), merging, symbol sizes, the known-zero and tiny builders, E3 symmetry, E2 and the
E1 -> E2 -> E3 order. Protocol §4.1-§4.6, §5.1; DR3, DR4, DR5.

Written from the protocol copy, API.md, CONTRACT.json, TEST_PLAN.md and the 0118 review only;
tools/hws/*.py was never read. Expected values come from the protocol, CONTRACT and independent
computations in this file."""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hws") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hws"))

import hws_worlds as hw  # noqa: E402

import oracle_profile  # noqa: E402
from scipy.special import logsumexp  # noqa: E402
from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure  # noqa: E402
from topo_pilot.process import (  # noqa: E402
    EmissionConfig,
    GridCenters,
    OverlapGaussian,
    TransitionBuilder,
    TransitionConfig,
)
from topo_pilot.process._geometry import point_distances  # noqa: E402
from topo_pilot.world import WorldConfig  # noqa: E402
from topo_pilot.world import build_world as src_build_world  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hws" / "CONTRACT.json").read_text(encoding="utf-8"))
P_LEVELS = [F(s) for s in CONTRACT["levels"]["p"]]
S_LEVELS = [F(s) for s in CONTRACT["levels"]["sigma"]]
CELLS = [tuple(c) for c in CONTRACT["grid"]["eligible_cells_expected"]]
SYMMETRIC = [(8, 2), (8, 3), (12, 3)]
ASYMMETRIC = [(12, 2), (16, 2), (16, 3), (8, 1), (12, 1), (16, 1)]
PROTOCOL_VPRIME = {(8, 1): 24, (8, 2): 18, (8, 3): 12, (12, 1): 36, (12, 2): 24, (12, 3): 18,
                   (16, 1): 48, (16, 2): 30, (16, 3): 24}


def _key(W, q, s, p) -> str:
    return f"W{W}-q{q}-s{float(s)!r}-p{float(p)!r}"


def _world(W, Hh=12):
    return src_build_world(WorldConfig("cylinder", (W, Hh), "flat"))


def _mirrored(world, centres, sigma):
    """The 4-line softmax of emission._overlap_core, written here independently."""
    d = point_distances(world, centres, "flat")
    logits = -(d**2) / (2.0 * float(sigma) ** 2)
    return np.exp(logits - logsumexp(logits, axis=1, keepdims=True))


def _g(W, q) -> list:
    m = -(-(W // 2 - 1) // q)
    return [0] + [1 + ((i - 1) % m) for i in range(1, W // 2)]


def _perm_reflect(W, Hh, c):
    return np.array([((c - z // Hh) % W) * Hh + z % Hh for z in range(W * Hh)])


# ------------------------------------------------------------------ grid, keys, levels

def test_grid_has_225_worlds_in_the_stated_order():
    g = hw.grid()
    expected = [(W, q, s, p) for W in (8, 12, 16) for q in (1, 2, 3)
                for s in S_LEVELS for p in P_LEVELS]
    assert len(g) == 225 == CONTRACT["grid"]["n_worlds"]
    assert [(w.W, w.q, w.sigma, w.p) for w in g] == expected
    assert [w.key for w in g] == [_key(*t) for t in expected]
    assert all(isinstance(w.sigma, F) and isinstance(w.p, F) for w in g)
    assert len({w.key for w in g}) == 225


def test_world_keys():
    assert hw.W0.key == "W12-q1-s1.25-p0.2" == CONTRACT["w0"]["key"]
    assert hw.world_key(12, 1, F(5, 4), F(1, 5)) == "W12-q1-s1.25-p0.2"
    assert hw.world_key(8, 3, F(3), F(15, 16)) == "W8-q3-s3.0-p0.9375"
    assert hw.world_key(16, 2, F(2), F(1, 2)) == "W16-q2-s2.0-p0.5"
    assert hw.world_key(12, 1, F(7, 2), F(31, 32)) == "W12-q1-s3.5-p0.96875"
    assert hw.world_key(12, 2, F(11, 8), F(2, 3)) == "W12-q2-s1.375-p" + repr(2 / 3)
    assert hw.World(12, 2, F(11, 8), F(2, 3)).key == hw.world_key(12, 2, F(11, 8), F(2, 3))


def test_level_constants_match_contract():
    lv = CONTRACT["levels"]
    assert tuple(hw.P_LEVELS) == tuple(P_LEVELS) and tuple(hw.SIGMA_LEVELS) == tuple(S_LEVELS)
    assert tuple(hw.Q_LEVELS) == (1, 2, 3) and tuple(hw.W_LEVELS) == (8, 12, 16)
    assert tuple(hw.X1_P) == (F(31, 32),) and tuple(hw.X1_SIGMA) == (F(7, 2), F(4))
    assert (hw.H, hw.L, hw.N_AXIAL) == (12, 32, 6)
    assert hw.S2_P_MID == {(F(a), F(b)): F(m) for a, b, m in lv["s2_p_edges"]}
    assert hw.S2_SIGMA_MID == {(F(a), F(b)): F(m) for a, b, m in lv["s2_sigma_edges"]}
    assert set(hw.S2_P_MID.values()) == {F(3, 8), F(2, 3), F(5, 6), F(11, 12), F(23, 24)}
    assert hw.P_INDEX == {F(k): F(v) for k, v in lv["index"]["p"].items()}
    assert hw.SIGMA_INDEX == {F(k): F(v) for k, v in lv["index"]["sigma"].items()}
    assert hw.W0 == hw.World(12, 1, F(5, 4), F(1, 5))


@pytest.mark.parametrize("add_p, add_sigma, count",
                         [(True, False, 30), (False, True, 60), (True, True, 102),
                          (False, False, 0)])
def test_x1_world_counts_and_order(add_p, add_sigma, count):
    got = hw.x1_worlds(add_p, add_sigma, CELLS)
    assert len(got) == count
    if count:
        assert count == CONTRACT["grid"]["x1_counts_max"][
            {(True, False): "p_only", (False, True): "sigma_only", (True, True): "both"}[
                (add_p, add_sigma)]]
    ps = P_LEVELS + ([F(31, 32)] if add_p else [])
    ss = S_LEVELS + ([F(7, 2), F(4)] if add_sigma else [])
    expected = [(W, q, s, p) for (W, q) in sorted(CELLS) for s in ss for p in ps
                if not (s in S_LEVELS and p in P_LEVELS)]
    assert [(w.W, w.q, w.sigma, w.p) for w in got] == expected
    assert not {w.key for w in got} & {w.key for w in hw.grid()}


def test_tiers():
    assert hw.tier(hw.World(12, 1, F(2), F(1, 2))) == 0
    assert hw.tier(hw.World(12, 2, F(5, 4), F(1, 5))) == 1
    for W in (8, 16):
        for q in (1, 2, 3):
            assert hw.tier(hw.World(W, q, F(5, 4), F(1, 5))) == 2
    with pytest.raises(ValueError):
        hw.tier(hw.World(12, 3, F(5, 4), F(1, 5)))


# ------------------------------------------------------------- centres, emission, features

def test_centres_rectangular_and_gridcenters_bitwise():
    ref = GridCenters().centers(_world(12), 36, np.random.default_rng(0))
    got = hw.centres(12)
    assert got.dtype == np.float64 and got.shape == (36, 2)
    assert np.array_equal(got, ref)
    for W in (6, 8, 16):
        c = hw.centres(W)
        assert c.shape == (6 * W // 2, 2)
        for i in range(W // 2):
            for b in range(6):
                assert tuple(c[6 * i + b]) == (0.5 + 2 * i, 0.5 + 2 * b)
    assert hw.centres(6, n_axial=1).tolist() == [[0.5, 0.5], [2.5, 0.5], [4.5, 0.5]]


@pytest.mark.parametrize("sigma", [F(5, 4), F(2), F(11, 8)])
def test_w12_emission_is_the_canonical_overlap_bitwise(sigma):
    world = _world(12)
    cfg = EmissionConfig("overlap", 36, float(sigma), "grid")
    spec = OverlapGaussian().build(world, cfg, SeedTree(1729))
    canon = oracle_profile.canonical_emission(spec.E, spec.symbol_perm)
    assert np.array_equal(hw.centre_emission(world, 12, sigma), canon)
    # the mirrored softmax used for W != 12 reproduces the src builder at W = 12 (DR5)
    assert np.array_equal(_mirrored(world, hw.centres(12), sigma), canon)


@pytest.mark.parametrize("W, N, V", [(8, 96, 24), (16, 192, 48)])
def test_other_circumferences_build(W, N, V):
    w = hw.World(W, 1, F(3, 2), F(1, 2))
    proc = hw.build_process(w)
    world = _world(W)
    ref = _mirrored(world, hw.centres(W), F(3, 2))
    assert proc["e1"]["status"] == "PASS"
    assert proc["N"] == N and proc["V"] == V and proc["key"] == w.key
    assert proc["T"].shape == (N, N) and proc["E"].shape == (N, V)
    assert np.array_equal(hw.centre_emission(world, W, F(3, 2)), ref)
    assert np.array_equal(proc["E_centres"], ref)
    assert np.array_equal(proc["E"], ref)  # q = 1: v = 6i + b, one centre per symbol
    T_ref = TransitionBuilder().build(world, TransitionConfig(p_stay=0.5)).T
    assert np.array_equal(proc["T"], T_ref)
    np.testing.assert_allclose(proc["pi"], 1.0 / N, rtol=0, atol=1e-15)
    assert np.array_equal(proc["coords"], np.asarray(world.coords, dtype=np.float64))
    a = 2.0 * np.pi * proc["coords"][:, 0] / W
    assert np.array_equal(proc["features"], np.column_stack((np.cos(a), np.sin(a))))
    assert proc["tier"] == 2 and proc["n_axial"] == 6
    assert proc["labels"].tolist() == list(range(W // 2))


def test_features_equal_circle_features_and_posterior_means():
    coords = np.asarray(_world(12).coords, dtype=np.float64)
    f = hw.features(coords, 12)
    cf = oracle_profile.circle_features(coords)
    assert f.dtype == np.float64 and np.array_equal(f, cf)
    proc = hw.build_process(hw.W0)
    assert np.array_equal(proc["features"], cf)
    spec = OverlapGaussian().build(_world(12), EmissionConfig("overlap", 36, 1.25, "grid"),
                                   SeedTree(1729))
    assert np.array_equal(proc["E"], oracle_profile.canonical_emission(spec.E, spec.symbol_perm))
    tok = (np.arange(4 * 32).reshape(4, 32) * 7 % 36).astype(np.uint8)
    args = (proc["T"], proc["E"], proc["pi"], tok, (4, 32))
    a = oracle_profile.posterior_means(*args, f)
    b = oracle_profile.posterior_means(*args, cf)
    assert all(np.array_equal(a[K], b[K]) for K in (4, 32))


def test_repeated_builds_are_identical():
    w = hw.World(12, 2, F(2), F(3, 4))
    one, two = hw.build_process(w), hw.build_process(w)
    for name in ("T", "pi", "E_centres", "E", "labels", "sizes", "coords", "features"):
        assert np.array_equal(one[name], two[name]), name
    assert np.array_equal(hw.anchored_labels(16, 3), hw.anchored_labels(16, 3))


# ------------------------------------------------------------------------- alias map

@pytest.mark.parametrize("W", [6, 8, 12, 16])
@pytest.mark.parametrize("q", [1, 2, 3])
def test_anchored_labels_match_contract_and_formula(W, q):
    ref = CONTRACT["alias"]["maps"][str(W)][str(q)]
    lab = hw.anchored_labels(W, q)
    assert lab.dtype == np.int64 and lab.tolist() == ref["g"] == _g(W, q)
    assert hw.n_labels(lab) == ref["n_A"]
    assert hw.v_prime(lab) == ref["V_prime"] == 6 * ref["n_A"]
    assert hw.v_prime(lab, n_axial=1) == ref["n_A"]
    if W != 6:
        assert ref["V_prime"] == PROTOCOL_VPRIME[(W, q)]
    groups = [[i for i in range(W // 2) if lab[i] == g] for g in range(ref["n_A"])]
    assert groups == ref["groups"]
    sizes = hw.symbol_sizes(lab)
    assert sizes.dtype == np.int64 and sizes.shape == (ref["V_prime"],)
    for g in range(ref["n_A"]):
        for b in range(6):
            assert sizes[6 * g + b] == ref["centres_per_label"][g] == len(groups[g])


def test_unanchored_labels():
    assert hw.unanchored_labels(12, 2).tolist() == [0, 1, 2, 0, 1, 2]
    assert hw.unanchored_labels(12, 3).tolist() == [0, 1, 0, 1, 0, 1]
    assert hw.unanchored_labels(12, 2).dtype == np.int64
    with pytest.raises(ValueError):
        hw.unanchored_labels(8, 3)


@pytest.mark.parametrize("W, q", [(8, 2), (12, 2), (12, 3), (16, 3), (16, 1)])
def test_merge_columns_sums_never_averages(W, q):
    rng = np.random.default_rng(11)
    E = rng.random((10, 6 * W // 2))  # not normalised: a renormalisation would show
    lab = hw.anchored_labels(W, q)
    out = hw.merge_columns(E, lab)
    ref = np.zeros((10, 6 * (int(lab.max()) + 1)))
    for i in range(W // 2):  # ascending i
        for b in range(6):
            ref[:, 6 * lab[i] + b] += E[:, 6 * i + b]
    assert out.dtype == np.float64 and out.shape == ref.shape
    np.testing.assert_allclose(out, ref, rtol=1e-15, atol=0)
    np.testing.assert_allclose(out.sum(axis=1), E.sum(axis=1), rtol=1e-14, atol=0)


def test_merge_q1_w12_is_identity_and_tiny_merge():
    E = hw.centre_emission(_world(12), 12, F(5, 4))
    assert np.array_equal(hw.merge_columns(E, hw.anchored_labels(12, 1)), E)
    e3 = np.random.default_rng(2).random((12, 3))
    out = hw.merge_columns(e3, np.array([0, 1, 1], dtype=np.int64), n_axial=1)
    assert out.shape == (12, 2) and np.array_equal(out[:, 0], e3[:, 0])
    assert np.array_equal(out[:, 1], e3[:, 1] + e3[:, 2])


# ------------------------------------------------------------- tiny and known-zero worlds

def test_build_tiny_world():
    t = hw.build_tiny()
    world = _world(6, 2)
    cen = np.array([[0.5, 0.5], [2.5, 0.5], [4.5, 0.5]])
    ref = _mirrored(world, cen, F(1))
    assert t["N"] == 12 and t["V"] == 3 and t["n_axial"] == 1
    assert np.array_equal(t["E"], ref)
    T_ref = TransitionBuilder().build(world, TransitionConfig(p_stay=0.5)).T
    assert np.array_equal(t["T"], T_ref)
    for z, (x, y) in enumerate(np.asarray(world.coords, dtype=np.float64)):
        logits = []
        for cx, cy in cen:
            dx = abs(x - cx) % 6
            dx = min(dx, 6 - dx)
            logits.append(-(dx * dx + (y - cy) ** 2) / 2.0)
        s = sum(math.exp(v) for v in logits)
        for j in range(3):
            assert abs(t["E"][z, j] - math.exp(logits[j]) / s) <= 1e-15
    t2 = hw.build_tiny(q=2)
    assert t2["V"] == 2 and t2["labels"].tolist() == [0, 1, 1]
    assert np.array_equal(t2["E"][:, 1], ref[:, 1] + ref[:, 2])


def test_known_zero_builders():
    U, N = hw.build_known_zero("U"), hw.build_known_zero("N")
    assert U["key"] == "U-W12" and N["key"] == "N-W12"
    assert U["n_axial"] == 12 and N["n_axial"] == 6 and U["tier"] == N["tier"] == 0
    assert U["E"].shape == (144, 144) and np.array_equal(U["E"], np.eye(144))
    assert N["E"].shape == (144, 36) and np.all(N["E"] == 1.0 / 36)


# ------------------------------------------------------------------------ E3 symmetry

def test_state_maps():
    W, Hh = 8, 12
    t, r = hw.translate_states(W, Hh, 3), hw.reflect_states(W, Hh, 1)
    assert t.dtype == np.int64 and r.dtype == np.int64
    for x in range(W):
        for y in range(Hh):
            assert t[x * Hh + y] == ((x + 3) % W) * Hh + y
            assert r[x * Hh + y] == ((1 - x) % W) * Hh + y


@pytest.mark.parametrize("W, q", SYMMETRIC)
def test_reflection_symmetric_cells(W, q):
    proc = hw.build_process(hw.World(W, q, F(5, 4), F(1, 5)))
    rec = hw.symmetry_check(proc["E"], W, 12)
    assert bool(rec["symmetric"]) is True
    assert 1 in rec["reflections"] and rec["min_dev_reflection"] <= 1e-9
    assert list(rec["translations"]) == []  # the anchor removes every translation
    E = proc["E"]
    assert np.max(np.abs(E[_perm_reflect(W, 12, 1)] - E)) <= 1e-9  # x -> 1 - x


@pytest.mark.parametrize("W, q", ASYMMETRIC)
def test_asymmetric_cells(W, q):
    proc = hw.build_process(hw.World(W, q, F(5, 4), F(1, 5)))
    rec = hw.symmetry_check(proc["E"], W, 12)
    assert bool(rec["symmetric"]) is False
    assert list(rec["translations"]) == [] and list(rec["reflections"]) == []
    assert rec["min_dev_reflection"] > 1e-9 and rec["min_dev_translation"] > 1e-9


def test_unanchored_and_tiny_maps():
    un = hw.build_process(hw.World(12, 2, F(5, 4), F(1, 5)), alias="unanchored")
    rec = hw.symmetry_check(un["E"], 12, 12)
    assert bool(rec["symmetric"]) and 6 in rec["translations"]
    assert hw.exact_filters(un, un["sizes"] / 36)["status"] == "INELIGIBLE/E3"
    tiny2 = hw.build_tiny(q=2)
    rec2 = hw.symmetry_check(tiny2["E"], 6, 2)
    assert bool(rec2["symmetric"]) and 1 in rec2["reflections"]
    assert not bool(hw.symmetry_check(hw.build_tiny()["E"], 6, 2)["symmetric"])


# ------------------------------------------------------------------------- E1, E2, order

def test_e2_threshold_boundaries():
    sizes = np.array([1, 2], dtype=np.int64)
    assert hw.e2_check(np.array([0.125, 0.25]), sizes, 4)["status"] == "PASS"
    below = hw.e2_check(np.array([0.125, np.nextafter(0.25, 0.0)]), sizes, 4)
    assert below["status"] == "INELIGIBLE/E2" and below["worst"]["v"] == 1
    t = F(1, 72)  # W = 12, q = 1: 0.5/V' with V' = 36 centres
    x = float(t)
    seen = set()
    for c in (np.nextafter(x, 0.0), x, np.nextafter(x, 1.0)):
        want = "PASS" if F(float(c)) >= t else "INELIGIBLE/E2"
        seen.add(want)
        assert hw.e2_check(np.array([c]), np.array([1], dtype=np.int64), 36)["status"] == want
    assert seen == {"PASS", "INELIGIBLE/E2"}
    # scaled rule: three centres merged at W = 8 need 3/(2*12) = 1/8
    assert hw.e2_check(np.array([0.125]), np.array([3]), 12)["status"] == "PASS"


def test_exact_filters_order_e1_e2_e3():
    proc = hw.build_process(hw.World(8, 2, F(5, 4), F(1, 5)))  # E3-symmetric cell
    good = proc["sizes"] / 24.0  # twice every threshold
    r = hw.exact_filters(proc, good)
    # API-AMBIGUITY: "all three records kept" does not name the keys; "e1".."e3" assumed
    assert r["status"] == "INELIGIBLE/E3"
    assert r["e1"]["status"] == "PASS" and r["e2"]["status"] == "PASS"
    r2 = hw.exact_filters(proc, np.zeros_like(good))
    assert r2["status"] == "INELIGIBLE/E2" and r2["e3"]["status"] == "INELIGIBLE/E3"
    planted = dict(proc, e1={"status": "INELIGIBLE/E1", "reason": "planted"})
    assert hw.exact_filters(planted, np.zeros_like(good))["status"] == "INELIGIBLE/E1"
    asym = hw.build_process(hw.World(12, 2, F(5, 4), F(1, 5)))
    assert hw.exact_filters(asym, asym["sizes"] / 36.0)["status"] == "PASS"


def test_builder_failures_are_e1(monkeypatch):
    def boom(self, world, cfg):
        raise StageFailure(ErrorCode.INVALID_CONFIG, "test", "planted", "planted failure")

    with monkeypatch.context() as m:
        m.setattr(TransitionBuilder, "build", boom)
        proc = hw.build_process(hw.World(12, 2, F(5, 4), F(1, 5)))
    assert proc["e1"]["status"] == "INELIGIBLE/E1" and proc["key"] == "W12-q2-s1.25-p0.2"
    assert "E" not in proc and "T" not in proc

    def bad_validate(*args, **kwargs):
        raise oracle_profile.ProfileError("planted")

    monkeypatch.setattr(oracle_profile, "validate_process", bad_validate)
    proc2 = hw.build_process(hw.World(8, 1, F(2), F(1, 2)))
    assert proc2["e1"]["status"] == "INELIGIBLE/E1" and "E" not in proc2
