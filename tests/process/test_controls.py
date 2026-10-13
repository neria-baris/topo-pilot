"""P06, P07, P08, P11, P12 and the ProcessStage I/O round trip."""

from __future__ import annotations

import inspect

import numpy as np
import pytest

from topo_pilot.contracts import (
    EmissionSpec,
    ErrorCode,
    SeedTree,
    StageFailure,
    TransitionSpec,
    WorldSpec,
)
from topo_pilot.contracts.testing import memory_store
from topo_pilot.process import (
    EMISSION_REGISTRY,
    AxisPermuted,
    EmissionConfig,
    EmissionModel,
    FPSCenters,
    FullPermuted,
    Identical,
    OverlapGaussian,
    ProcessStage,
    TransitionConfig,
    Unique,
)
from topo_pilot.process._diagnostics import check_row_multiset
from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation

pytestmark = pytest.mark.process


def _o_and_p(world, seed=1729, sigma=1.25):
    o = OverlapGaussian().build(world, EmissionConfig(mode="overlap", sigma=sigma), SeedTree(seed))
    p = AxisPermuted().build(world, EmissionConfig(mode="axis_permuted", sigma=sigma),
                             SeedTree(seed))
    return o, p


def _sorted_rows(E):
    return E[np.lexsort(E.T[::-1])]


@pytest.mark.parametrize("family", ["square", "cylinder"])
def test_P06_axis_permuted_preserves_rows_and_structure(family, square12, cylinder12):
    world = {"square": square12, "cylinder": cylinder12}[family]
    o, p = _o_and_p(world)
    assert np.array_equal(_sorted_rows(o.E), _sorted_rows(p.E))
    assert not np.array_equal(o.E, p.E)
    assert p.diagnostics["factorizes"] is True
    assert np.allclose(p.diagnostics["p_w"], o.diagnostics["p_w"], atol=1e-15)
    for key in ("H_W_given_Z", "H_W", "coverage_radius", "row_entropy_quantiles"):
        assert p.diagnostics[key] == pytest.approx(o.diagnostics[key], abs=1e-12)
    sx, sy = draw_axis_permutation(world)
    for x, y in ((0, 0), (3, 7), (11, 11)):
        assert np.array_equal(p.E[x * 12 + y], o.E[sx[x] * 12 + sy[y]])
    assert p.mode == "axis_permuted" and p.sigma == o.sigma
    assert np.array_equal(p.symbol_perm, o.symbol_perm)  # same replicate, same names


def test_P06_full_permutation_keeps_rows_but_not_product(square12):
    o = OverlapGaussian().build(square12, EmissionConfig(mode="overlap"), SeedTree(1))
    f = FullPermuted().build(square12, EmissionConfig(mode="full_permuted"), SeedTree(1))
    assert np.array_equal(_sorted_rows(o.E), _sorted_rows(f.E))
    assert f.diagnostics["factorizes"] is False
    assert np.array_equal(np.sort(f.state_perm), np.arange(144))


def test_axis_state_perm_n3_hand_example():
    # sx = (1, 2, 0), sy = (2, 0, 1), n = 3: state (x, y) -> (sx[x], sy[y]), id 3*sx[x] + sy[y]
    perm = axis_state_perm(np.array([1, 2, 0]), np.array([2, 0, 1]), (3, 3))
    assert perm.tolist() == [5, 3, 4, 8, 6, 7, 2, 0, 1]


def test_P06_row_multiset_check_error_path():
    E = np.array([[0.5, 0.5], [1.0, 0.0], [0.25, 0.75]])
    check_row_multiset(E, E[[2, 0, 1]])
    bad = E[[2, 0, 1]].copy()
    bad[0] = [0.4, 0.6]
    with pytest.raises(StageFailure) as exc:
        check_row_multiset(E, bad)
    assert exc.value.code is ErrorCode.NONSTOCHASTIC and exc.value.check == "row_multiset"


def test_P07_permutations_depend_on_world_not_replicate(square12, cylinder12):
    a = AxisPermuted().build(square12, EmissionConfig(mode="axis_permuted"), SeedTree(1))
    b = AxisPermuted().build(square12, EmissionConfig(mode="axis_permuted"), SeedTree(2))
    assert np.array_equal(a.state_perm, b.state_perm)
    assert not np.array_equal(a.symbol_perm, b.symbol_perm)  # names do depend on replicate
    rng = SeedTree(0).generator("axis_permutation", "square")
    sx, sy = rng.permutation(12), rng.permutation(12)
    assert np.array_equal(a.state_perm, (sx[:, None] * 12 + sy[None, :]).ravel())
    c = AxisPermuted().build(cylinder12, EmissionConfig(mode="axis_permuted"), SeedTree(1))
    assert not np.array_equal(a.state_perm, c.state_perm)  # per world family


def test_P08_identical_all_rows_equal(square3):
    spec = Identical().build(square3, EmissionConfig(mode="identical", V=36), SeedTree(5))
    assert np.all(spec.E == 1.0 / 36) and spec.E.shape == (9, 36)
    assert spec.diagnostics["H_W_given_Z"] == pytest.approx(np.log(36))
    assert spec.diagnostics["H_W"] == pytest.approx(np.log(36))
    assert spec.sigma is None and spec.centers is None


def test_P08_unique_is_permutation_matrix(square3):
    spec = Unique().build(square3, EmissionConfig(mode="unique", V=9, sigma=None), SeedTree(5))
    E = spec.E
    assert set(np.unique(E)) == {0.0, 1.0}
    assert np.all(E.sum(axis=0) == 1) and np.all(E.sum(axis=1) == 1)
    assert np.array_equal(E.argmax(axis=1), spec.symbol_perm)  # state z -> symbol_perm[z]
    assert spec.diagnostics["H_W_given_Z"] == 0.0
    assert spec.diagnostics["H_W"] == pytest.approx(np.log(9))
    with pytest.raises(StageFailure) as exc:
        Unique().build(square3, EmissionConfig(mode="unique", V=8), SeedTree(5))
    assert exc.value.code is ErrorCode.INVALID_CONFIG


def test_P11_emission_builder_does_not_accept_transition():
    assert set(EMISSION_REGISTRY) == {"overlap", "axis_permuted", "full_permuted", "identical",
                                      "unique"}
    for cls in EMISSION_REGISTRY.values():
        params = inspect.signature(cls.build).parameters
        assert list(params) == ["self", "world", "cfg", "rng_tree"]
        assert not any("Transition" in str(p.annotation) for p in params.values())
    assert list(inspect.signature(EmissionModel.build).parameters) == [
        "self", "world", "cfg", "rng_tree"]


def test_P12_fps_greedy_maxmin_by_hand(square3):
    # n=3 square, start vertex 0=(0,0); farthest: (2,2) (sqrt 8). Next: (0,2) and (2,0) tie at
    # distance 2 from both chosen -> lowest id (0,2)=2.
    # Then (2,0)=6 (distance 2) beats (1,1) (sqrt 2).
    c = FPSCenters().centers(square3, 4, np.random.default_rng(0))
    assert c.tolist() == [[0, 0], [2, 2], [0, 2], [2, 0]]
    assert len({tuple(r) for r in c.tolist()}) == 4
    full = FPSCenters().centers(square3, 9, np.random.default_rng(0))
    assert len({tuple(r) for r in full.tolist()}) == 9
    with pytest.raises(StageFailure) as exc:
        FPSCenters().centers(square3, 10, np.random.default_rng(0))
    assert exc.value.code is ErrorCode.INVALID_CONFIG


def test_fps_overlap_builds_on_tiny_world(square3):
    cfg = EmissionConfig(mode="overlap", V=4, sigma=1.0, center_strategy="fps")
    spec = OverlapGaussian().build(square3, cfg, SeedTree(3))
    assert spec.E.shape == (9, 4) and spec.center_strategy == "fps"
    assert isinstance(spec.diagnostics["factorizes"], bool)
    assert spec.centers.tolist() == [[0, 0], [2, 2], [0, 2], [2, 0]]


def test_stage_round_trip_and_lineage(square12):
    store = memory_store()
    wid = store.save(square12, config={"family": "square", "n": 12}, parents=[], seed_map={},
                     consumer="world")
    stage = ProcessStage()
    tid = stage.run_transition(wid, TransitionConfig(), store)
    assert tid == stage.run_transition(wid, TransitionConfig(), store)
    assert store.meta(tid).parent_ids == (wid,)
    assert store.load(TransitionSpec, tid, consumer="process").T.shape == (144, 144)

    trees = {r: SeedTree(r) for r in (1, 2)}
    cfg = EmissionConfig(mode="axis_permuted")
    ids = {r: stage.run_emission(wid, cfg, trees[r], store) for r in (1, 2)}
    assert ids[1] != ids[2]
    spec = store.load(EmissionSpec, ids[1], consumer="process")
    assert spec.mode == "axis_permuted" and spec.state_perm is not None
    meta = store.meta(ids[1])
    assert meta.parent_ids == (wid,) and meta.config["replicate"] == 1
    assert meta.consumer == "process" and meta.seed_map
    assert any(k.startswith("symbol_names/") for k in meta.seed_map)
    assert stage.run_emission(wid, cfg, SeedTree(1), store) == ids[1]
    assert store.load(WorldSpec, wid, consumer="process").family == "square"


def test_stage_unknown_mode(square12):
    store = memory_store()
    wid = store.save(square12, config={"family": "square"}, parents=[], seed_map={},
                     consumer="world")
    with pytest.raises(StageFailure) as exc:
        ProcessStage().run_emission(wid, EmissionConfig(mode="bogus"), SeedTree(1), store)
    assert exc.value.code is ErrorCode.INVALID_CONFIG
