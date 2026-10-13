"""Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
before reading the implementation.

Metric-conductance kernel (protocol x5g1-feas-v2 §2-§3.1, API §1): warp profile, a = 0
equivalence, a = 0.2 validity, closed-form C_max, edge classes, metadata and ProcessStage.
"""

from __future__ import annotations

import dataclasses
import json
import math

import numpy as np
import pytest
from scipy.sparse.csgraph import connected_components

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    MemoryBackend,
    StageFailure,
    TransitionSpec,
    canonical_json,
)
from topo_pilot.contracts.testing import tiny_world_spec
from topo_pilot.process import (
    ConductanceConfig,
    ProcessStage,
    TransitionBuilder,
    TransitionConfig,
    conductance_kernel,
    warp_profile,
)
from topo_pilot.world import WorldConfig, build_world

pytestmark = pytest.mark.process

R12 = 12.0 / (2.0 * math.pi)


@pytest.fixture(scope="module")
def world():
    """12 x 12 cylinder from the world package (state id = x * 12 + y)."""
    return build_world(WorldConfig("cylinder", (12, 12)))


@pytest.fixture(scope="module")
def k020(world):
    return conductance_kernel(world, ConductanceConfig(a=0.20, move=0.8))


def _lh(y: int, a: float, ny: int) -> float:
    return 1.0 + a * math.cos(2.0 * math.pi * y / (ny - 1))


def _edge_classes(world):
    e = np.asarray(world.edges)
    c = np.asarray(world.coords)
    horiz = c[e[:, 0], 1] == c[e[:, 1], 1]
    vert = c[e[:, 0], 0] == c[e[:, 1], 0]
    return e, horiz, vert


# ---------------------------------------------------------------- warp_profile


def test_warp_profile_hand_values_12x12():
    f, l_h = warp_profile((12, 12), 0.2)
    assert f.shape == (12,) and l_h.shape == (12,)
    assert f.dtype == np.float64 and l_h.dtype == np.float64
    # y = 0 and y = ny - 1 = 11: cos(0) = cos(2 pi) = 1 -> l_h = 1.2
    assert l_h[0] == pytest.approx(1.2, abs=1e-15)
    assert l_h[11] == pytest.approx(1.2, abs=1e-15)
    assert f[0] == pytest.approx(R12 * 1.2, abs=1e-14)
    assert f[11] == pytest.approx(R12 * 1.2, abs=1e-14)
    # interior y = 5: cos(10 pi / 11)
    assert l_h[5] == pytest.approx(1 + 0.2 * math.cos(10 * math.pi / 11), abs=1e-15)
    assert f[5] == pytest.approx(R12 * (1 + 0.2 * math.cos(10 * math.pi / 11)), abs=1e-14)
    np.testing.assert_allclose(l_h, f * 2 * math.pi / 12, atol=1e-14)
    np.testing.assert_allclose(l_h, [_lh(y, 0.2, 12) for y in range(12)], atol=1e-15)


def test_warp_profile_exact_mid_row_when_ny_odd():
    # ny = 13 -> ny - 1 = 12; y = 6 gives cos(pi) = -1 -> l_h = 0.8; y = 3 gives ~1.
    f, l_h = warp_profile((12, 13), 0.2)
    assert f.shape == (13,)
    assert l_h[6] == pytest.approx(0.8, abs=1e-15)
    assert f[6] == pytest.approx(R12 * 0.8, abs=1e-14)
    assert l_h[3] == pytest.approx(1.0, abs=1e-15)
    assert l_h[0] == pytest.approx(1.2, abs=1e-15) and l_h[12] == pytest.approx(1.2, abs=1e-15)


def test_warp_profile_a0_is_flat():
    f, l_h = warp_profile((12, 12), 0.0)
    np.testing.assert_allclose(l_h, 1.0, atol=0)
    np.testing.assert_allclose(f, R12, atol=1e-15)


@pytest.mark.parametrize("a", [1.0, -1.0, 1.5, -3.0])
def test_warp_profile_rejects_abs_a_ge_1(a):
    with pytest.raises(StageFailure) as ei:
        warp_profile((12, 12), a)
    assert ei.value.code == ErrorCode.INVALID_CONFIG


def test_warp_profile_rejects_ny_below_2():
    with pytest.raises(StageFailure) as ei:
        warp_profile((12, 1), 0.2)
    assert ei.value.code == ErrorCode.INVALID_CONFIG


def test_conductance_config_defaults():
    cfg = ConductanceConfig()
    assert cfg.a == 0.20 and cfg.move == 0.8
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.a = 0.1  # type: ignore[misc]


# ---------------------------------------------------------------- a = 0 equivalence


@pytest.mark.parametrize("source", ["build_world", "tiny_world_spec"])
def test_a0_equals_max_degree_lazy_walk(source, world):
    w = world if source == "build_world" else tiny_world_spec("cylinder", n=12)
    spec, meta = conductance_kernel(w, ConductanceConfig(a=0.0, move=0.8))
    ref = TransitionBuilder().build(w, TransitionConfig("max_degree_lazy_walk", 0.2))
    assert isinstance(spec, TransitionSpec)
    assert np.max(np.abs(spec.T - ref.T)) <= 1e-15
    np.testing.assert_allclose(spec.pi, ref.pi, atol=1e-15)
    assert meta["C_max"] == pytest.approx(4.0, abs=1e-15)


# ---------------------------------------------------------------- a = 0.2 validity


def test_a020_kernel_validity(world, k020):
    spec, _ = k020
    T = spec.T
    n = 144
    assert T.shape == (n, n) and T.dtype == np.float64
    assert np.max(np.abs(T - T.T)) <= 1e-12
    assert np.max(np.abs(T.sum(axis=1) - 1.0)) <= 1e-12
    assert T.min() >= 0.0
    assert np.diag(T).min() >= 0.2 - 1e-12
    np.testing.assert_allclose(spec.pi, np.full(n, 1.0 / n), atol=1e-15)
    assert np.max(np.abs(spec.pi @ T - spec.pi)) <= 1e-12
    assert spec.p_stay == pytest.approx(0.2, abs=1e-15)
    assert spec.d_max == 4 and isinstance(spec.d_max, int)
    spec.validate()


def test_a020_support_only_edges_and_diagonal(world, k020):
    spec, _ = k020
    allowed = np.eye(144, dtype=bool)
    e = np.asarray(world.edges)
    allowed[e[:, 0], e[:, 1]] = True
    allowed[e[:, 1], e[:, 0]] = True
    assert not np.any((spec.T > 0) & ~allowed)
    # every edge carries positive mass (conductances are positive)
    assert np.all(spec.T[e[:, 0], e[:, 1]] > 0)


def test_a020_connected(k020):
    spec, _ = k020
    adj = (spec.T > 0) & ~np.eye(144, dtype=bool)
    n_comp, _ = connected_components(adj.astype(np.int8), directed=False)
    assert n_comp == 1


def test_a020_c_max_closed_form_and_entries(world, k020):
    spec, meta = k020
    n_vert = [1 if y in (0, 11) else 2 for y in range(12)]
    c_max = max(2.0 / _lh(y, 0.2, 12) ** 2 + n_vert[y] for y in range(12))
    assert meta["C_max"] == pytest.approx(c_max, rel=1e-13)
    e, horiz, vert = _edge_classes(world)
    ys = np.asarray(world.coords)[e[:, 0], 1].astype(int)
    for (i, j), h, y in zip(e, horiz, ys):
        c = 1.0 / _lh(int(y), 0.2, 12) ** 2 if h else 1.0
        assert spec.T[i, j] == pytest.approx(0.8 * c / c_max, abs=1e-15)
    diag_ref = 1.0 - (spec.T.sum(axis=1) - np.diag(spec.T))
    np.testing.assert_allclose(np.diag(spec.T), diag_ref, atol=1e-14)


def test_edge_classification_counts(world, k020):
    _, meta = k020
    e, horiz, vert = _edge_classes(world)
    assert int(horiz.sum()) == 144 and int(vert.sum()) == 132
    assert not np.any(horiz & vert) and np.all(horiz | vert)
    x = np.asarray(world.coords)[:, 0]
    wraps = horiz & (np.abs(x[e[:, 0]] - x[e[:, 1]]) == 11)
    assert int(wraps.sum()) == 12
    assert meta["n_edges_h"] == 144 and meta["n_edges_v"] == 132


def test_wrap_edges_carry_horizontal_conductance(world, k020):
    spec, meta = k020
    for y in range(12):
        i, j = 0 * 12 + y, 11 * 12 + y           # (0, y) - (11, y) wrap
        assert spec.T[i, j] == pytest.approx(
            0.8 / _lh(y, 0.2, 12) ** 2 / meta["C_max"], abs=1e-15)


def test_metadata_matches_warp_profile(k020):
    _, meta = k020
    f, l_h = warp_profile((12, 12), 0.2)
    assert meta["kind"] == "metric_conductance"
    assert meta["a"] == 0.2 and meta["move"] == 0.8
    assert isinstance(meta["f_y"], list) and isinstance(meta["l_h"], list)
    np.testing.assert_allclose(meta["f_y"], f, rtol=0, atol=1e-15)
    np.testing.assert_allclose(meta["l_h"], l_h, rtol=0, atol=1e-15)
    assert {"kind", "a", "move", "f_y", "l_h", "C_max", "n_edges_h", "n_edges_v"} <= set(meta)
    json.loads(json.dumps(meta))                  # JSON-serialisable


def test_kernel_rejects_bad_state_order():
    t = tiny_world_spec("cylinder", n=12)
    sig = np.arange(144)
    sig[[0, 1]] = [1, 0]
    coords = np.empty_like(t.coords)
    coords[sig] = t.coords
    e = np.sort(sig[t.edges], axis=1)
    e = e[np.lexsort((e[:, 1], e[:, 0]))].astype(np.int32)
    dist = np.empty_like(t.dist)
    dist[np.ix_(sig, sig)] = t.dist
    dg = np.empty_like(t.dist_graph)
    dg[np.ix_(sig, sig)] = t.dist_graph
    bad = dataclasses.replace(t, coords=coords, edges=e, dist=dist, dist_graph=dg,
                              cells={0: t.cells[0], 1: e, 2: sig[t.cells[2]].astype(np.int32)})
    with pytest.raises(StageFailure) as ei:
        conductance_kernel(bad, ConductanceConfig())
    assert ei.value.code == ErrorCode.STATE_ORDER_MISMATCH


def test_kernel_rejects_abs_a_ge_1(world):
    with pytest.raises(StageFailure):
        conductance_kernel(world, ConductanceConfig(a=1.0))


# ---------------------------------------------------------------- ProcessStage


def test_process_stage_saves_with_world_parent(world, k020):
    store = ArtifactStore(MemoryBackend())
    world_id = store.save(world, config={"family": "cylinder", "dims": [12, 12]}, parents=[],
                          seed_map={}, consumer="world")
    cfg = ConductanceConfig()
    aid = ProcessStage().run_conductance_transition(world_id, cfg, store)
    meta = store.meta(aid)
    assert meta.artifact_type == "TransitionSpec"
    assert tuple(meta.parent_ids) == (world_id,)
    _, expected_cfg = k020
    assert json.loads(canonical_json(dict(meta.config))) == json.loads(
        canonical_json(expected_cfg))
    loaded = store.load(TransitionSpec, aid, consumer="process")
    np.testing.assert_array_equal(loaded.T, k020[0].T)
    # idempotent: same content -> same id
    assert ProcessStage().run_conductance_transition(world_id, cfg, store) == aid
