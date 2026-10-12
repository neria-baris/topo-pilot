"""Independent tests W01-W13 for `topo_pilot.world`, written from SPEC.md / TEST_PLAN.md only."""
from __future__ import annotations

from typing import ClassVar

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec
from topo_pilot.contracts.testing import memory_store
from topo_pilot.world import (
    WORLD_REGISTRY,
    CubicalComplex,
    FlatQuotientMetric,
    Identification,
    QuotientLatticeBuilder,
    WorldBuilder,
    WorldConfig,
    WorldStage,
    build_world,
    register_world,
)

pytestmark = pytest.mark.world

PRIMES = (2, 3)


# ----------------------------------------------------------------------------- helpers
def _rank_mod_p(mat: np.ndarray, p: int) -> int:
    a = np.array(mat, dtype=np.int64) % p
    rows, cols = a.shape
    rank = 0
    for c in range(cols):
        if rank == rows:
            break
        piv = next((r for r in range(rank, rows) if a[r, c] % p), None)
        if piv is None:
            continue
        a[[rank, piv]] = a[[piv, rank]]
        a[rank] = (a[rank] * pow(int(a[rank, c]), -1, p)) % p
        for r in range(rows):
            if r != rank and a[r, c]:
                a[r] = (a[r] - a[r, c] * a[rank]) % p
        rank += 1
    return rank


def _own_boundary(cells: dict[int, np.ndarray], k: int) -> np.ndarray:
    """Independent cubical boundary: d = sum_i (-1)^i (upper_i - lower_i); edges canonical (lo,hi).

    Axis i of a k-cube tuple is bit (k-1-i) of the local index (lexicographic order)."""
    lower = {tuple(int(v) for v in c): j for j, c in enumerate(cells[k - 1])}
    mat = np.zeros((len(cells[k - 1]), len(cells[k])), dtype=np.int64)
    for j, cell in enumerate(cells[k]):
        for i in range(k):
            for side, sgn in ((1, 1), (0, -1)):
                face = tuple(int(cell[idx]) for idx in range(2**k)
                             if ((idx >> (k - 1 - i)) & 1) == side)
                s = sgn * (-1) ** i
                if k == 2 and face[0] > face[1]:
                    face, s = (face[1], face[0]), -s
                mat[lower[face], j] += s
    return mat


def _own_betti(cells: dict[int, np.ndarray], p: int) -> tuple[int, ...]:
    top = max(cells)
    ranks = {k: _rank_mod_p(_own_boundary(cells, k), p) for k in range(1, top + 1)}
    ranks[0] = ranks[top + 1] = 0
    return tuple(len(cells[k]) - ranks[k] - ranks[k + 1] for k in range(top + 1))


def _cx(spec: WorldSpec) -> CubicalComplex:
    return CubicalComplex(spec.n_states, {k: np.asarray(v) for k, v in spec.cells.items()})


def _cfg(family: str, n: int, metric: str = "flat") -> WorldConfig:
    return WorldConfig(family=family, dims=(n, n), metric=metric)


def _vid(x: int, y: int, n: int = 12) -> int:
    return x * n + y


def _assert_metric(d: np.ndarray) -> None:
    assert np.allclose(d, d.T, atol=1e-9)
    assert np.allclose(np.diag(d), 0.0, atol=1e-12)
    assert (d >= -1e-12).all()
    for k in range(d.shape[0]):
        assert (d <= d[:, k, None] + d[None, k, :] + 1e-9).all()


@pytest.fixture
def registered():
    """Register in-test builders under unique names; always clean the registry afterwards."""
    added: list[str] = []

    def _register(cls):
        added.append(cls.family)
        return register_world(cls)

    yield _register
    for name in added:
        WORLD_REGISTRY.pop(name, None)


def _make_builders(registered):
    @registered
    class _TestTorus(QuotientLatticeBuilder):
        family: ClassVar[str] = "_t_torus"
        expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 2, 1)}
        identifications: ClassVar[tuple] = (Identification(0, "periodic"),
                                            Identification(1, "periodic"))

    @registered
    class _TestKlein(QuotientLatticeBuilder):
        family: ClassVar[str] = "_t_klein"
        expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 1, 0)}
        identifications: ClassVar[tuple] = (Identification(0, "flipped", flip_axis=1),
                                            Identification(1, "periodic"))

    @registered
    class _TestBadExpected(QuotientLatticeBuilder):
        family: ClassVar[str] = "_t_badexp"
        expected_betti: ClassVar[dict] = {2: (1, 1, 0), 3: (1, 1, 0)}
        identifications: ClassVar[tuple] = ()

    return _TestTorus, _TestKlein, _TestBadExpected


# ----------------------------------------------------------------------------- W01
@pytest.mark.parametrize("family", ["square", "cylinder"])
@pytest.mark.parametrize("n", [3, 4, 12])
def test_w01_boundary_squared_is_zero_over_integers(family, n):
    spec = build_world(_cfg(family, n))
    cx = _cx(spec)
    d1, d2 = cx.boundary_matrix(1), cx.boundary_matrix(2)
    assert d1.shape == (n * n, len(spec.cells[1]))
    assert d2.shape == (len(spec.cells[1]), len(spec.cells[2]))
    prod = (d1 @ d2).toarray()
    assert not prod.any()
    assert d1.nnz and d2.nnz
    assert set(np.unique(d1.toarray())) <= {-1, 0, 1}
    assert (np.abs(d1.toarray()).sum(axis=0) == 2).all()   # each edge has two endpoints


# ----------------------------------------------------------------------------- W02
@pytest.mark.parametrize("family,expected", [("square", (1, 0, 0)), ("cylinder", (1, 1, 0))])
@pytest.mark.parametrize("p", PRIMES)
def test_w02_betti_known_answers(family, expected, p):
    spec = build_world(_cfg(family, 4))
    assert tuple(spec.betti_computed[p]) == expected
    assert tuple(spec.betti_expected[p]) == expected
    assert tuple(_cx(spec).betti(p)) == expected
    assert _own_betti({k: np.asarray(v) for k, v in spec.cells.items()}, p) == expected


# ----------------------------------------------------------------------------- W03
@pytest.mark.parametrize("family,counts,chi", [("square", (144, 264, 121), 1),
                                              ("cylinder", (144, 276, 132), 0)])
def test_w03_cell_counts_n12(family, counts, chi):
    spec = build_world(_cfg(family, 12))
    assert tuple(len(spec.cells[k]) for k in (0, 1, 2)) == counts
    assert counts[0] - counts[1] + counts[2] == chi
    assert _cx(spec).euler_characteristic() == chi
    assert len(spec.edges) == counts[1]
    assert _cx(spec).one_skeleton().shape == (counts[1], 2)


def test_w03_vertex_ids_and_coords():
    spec = build_world(_cfg("square", 12))
    assert spec.coords.dtype.kind == "f"
    assert np.array_equal(spec.coords[_vid(3, 7)], [3.0, 7.0])
    assert np.array_equal(spec.coords[_vid(11, 0)], [11.0, 0.0])
    assert all(a < b for a, b in spec.edges)


# ----------------------------------------------------------------------------- W04
def test_w04_graph_cycle_rank_differs_from_surface_betti1():
    spec = build_world(_cfg("square", 12))
    assert len(spec.edges) - spec.n_states + 1 == 121
    assert spec.betti_computed[2][1] == 0 and spec.betti_computed[3][1] == 0


# ----------------------------------------------------------------------------- W05
def test_w05_flat_metric_cylinder_known_and_axioms():
    d = build_world(_cfg("cylinder", 12)).dist
    for y in (0, 5, 11):
        assert d[_vid(11, y), _vid(0, y)] == pytest.approx(1.0, abs=1e-9)
    assert d[_vid(0, 0), _vid(6, 0)] == pytest.approx(6.0, abs=1e-9)
    assert d[_vid(0, 0), _vid(0, 11)] == pytest.approx(11.0, abs=1e-9)   # y is not periodic
    assert d[_vid(0, 0), _vid(10, 3)] == pytest.approx(np.hypot(2, 3), abs=1e-9)
    _assert_metric(d)


def test_w05_flat_metric_class_matches_built_dist():
    spec = build_world(_cfg("cylinder", 6))
    ids = (Identification(0, "periodic"), Identification(1, "none"))
    d = FlatQuotientMetric().pairwise(spec.coords, _cx(spec), ids, (6, 6))
    assert np.allclose(d, spec.dist, atol=1e-9)


# ----------------------------------------------------------------------------- W06
@pytest.mark.parametrize("family", ["square", "cylinder", "_t_torus", "_t_klein"])
def test_w06_flat_vs_graph_sandwich(family, registered):
    _make_builders(registered)
    spec = build_world(_cfg(family, 4 if family.startswith("_t") else 12))
    assert (spec.dist <= spec.dist_graph + 1e-9).all()
    assert (spec.dist >= spec.dist_graph / np.sqrt(2) - 1e-9).all()


def test_w06_graph_metric_option_is_graph_geodesic():
    spec = build_world(_cfg("cylinder", 6, metric="graph"))
    assert np.allclose(spec.dist, spec.dist_graph)
    assert spec.dist[_vid(0, 0, 6), _vid(5, 0, 6)] == pytest.approx(1.0)
    assert spec.dist[_vid(0, 0, 6), _vid(3, 2, 6)] == pytest.approx(5.0)
    _assert_metric(spec.dist)


# ----------------------------------------------------------------------------- W07
@pytest.mark.parametrize("family", ["square", "cylinder"])
def test_w07_betti_invariant_under_vertex_relabelling(family):
    spec = build_world(_cfg(family, 4))
    cells = {k: np.asarray(v) for k, v in spec.cells.items()}
    perm = np.random.default_rng(7).permutation(spec.n_states)
    new = {0: np.arange(spec.n_states)[:, None]}
    new[1] = np.sort(perm[cells[1]], axis=1)
    new[2] = perm[cells[2]]
    cx = CubicalComplex(spec.n_states, new)
    assert cx.euler_characteristic() == _cx(spec).euler_characteristic()
    for p in PRIMES:
        assert tuple(cx.betti(p)) == tuple(_cx(spec).betti(p))
    assert not (cx.boundary_matrix(1) @ cx.boundary_matrix(2)).toarray().any()


# ----------------------------------------------------------------------------- W08
def test_w08_face_repeating_a_vertex_raises_invalid_glue():
    cells = {0: np.arange(3)[:, None],
             1: np.array([[0, 1], [0, 2], [1, 2]]),
             2: np.array([[0, 1, 2, 0]])}
    with pytest.raises(StageFailure) as exc:
        CubicalComplex(3, cells).betti(2)
    assert exc.value.code == ErrorCode.INVALID_GLUE


# ----------------------------------------------------------------------------- W09
def test_w09_wrong_expected_betti_raises(registered):
    _make_builders(registered)
    with pytest.raises(StageFailure) as exc:
        build_world(WorldConfig(family="_t_badexp", dims=(4, 4)))
    assert exc.value.code == ErrorCode.BETTI_MISMATCH


# ----------------------------------------------------------------------------- W10
def test_w10_registry_dispatch_and_unknown_family(registered):
    assert {"square", "cylinder"} <= set(WORLD_REGISTRY)
    assert issubclass(WORLD_REGISTRY["square"], WorldBuilder)
    assert build_world(_cfg("square", 3)).family == "square"
    assert build_world(_cfg("cylinder", 3)).family == "cylinder"
    calls: list[tuple] = []

    @registered
    class _Spy(WORLD_REGISTRY["square"]):
        family: ClassVar[str] = "_t_spy"

        def build(self, cfg):
            calls.append(cfg.dims)
            return super().build(cfg)

    assert WORLD_REGISTRY["_t_spy"] is _Spy
    build_world(WorldConfig(family="_t_spy", dims=(3, 3)))
    assert calls == [(3, 3)]
    with pytest.raises(StageFailure) as exc:
        build_world(WorldConfig(family="_no_such_family_", dims=(3, 3)))
    assert exc.value.code == ErrorCode.INVALID_CONFIG


# ----------------------------------------------------------------------------- W11 / W12
def test_w11_torus_extension(registered):
    _make_builders(registered)
    spec = build_world(WorldConfig(family="_t_torus", dims=(4, 4)))
    assert tuple(len(spec.cells[k]) for k in (0, 1, 2)) == (16, 32, 16)
    cells = {k: np.asarray(v) for k, v in spec.cells.items()}
    for p in PRIMES:
        assert tuple(spec.betti_computed[p]) == (1, 2, 1)
        assert _own_betti(cells, p) == (1, 2, 1)
        assert tuple(_cx(spec).betti(p)) == (1, 2, 1)
    assert not (_cx(spec).boundary_matrix(1) @ _cx(spec).boundary_matrix(2)).toarray().any()


def test_w12_klein_extension(registered):
    _make_builders(registered)
    spec = build_world(WorldConfig(family="_t_klein", dims=(4, 4)))
    assert tuple(len(spec.cells[k]) for k in (0, 1, 2)) == (16, 32, 16)
    cells = {k: np.asarray(v) for k, v in spec.cells.items()}
    assert _own_betti(cells, 2) == (1, 2, 1)
    assert _own_betti(cells, 3) == (1, 1, 0)
    assert tuple(spec.betti_computed[2]) == (1, 2, 1)
    assert tuple(spec.betti_computed[3]) == (1, 1, 0)
    assert not (_cx(spec).boundary_matrix(1) @ _cx(spec).boundary_matrix(2)).toarray().any()
    _assert_metric(spec.dist)


# ----------------------------------------------------------------------------- W13
def test_w13_world_stage_saves_valid_spec_with_stable_id():
    store = memory_store()
    cfg = _cfg("cylinder", 4)
    aid = WorldStage().run(cfg, store)
    assert isinstance(aid, str) and aid
    spec = store.load(WorldSpec, aid, consumer="analysis")
    spec.validate()
    assert spec.family == "cylinder" and tuple(spec.dims) == (4, 4)
    assert tuple(spec.betti_computed[2]) == (1, 1, 0)
    ref = build_world(cfg)
    assert np.array_equal(spec.dist, ref.dist)
    assert WorldStage().run(cfg, store) == aid
    assert WorldStage().run(_cfg("square", 4), store) != aid


def test_builds_are_deterministic():
    a, b = build_world(_cfg("cylinder", 5)), build_world(_cfg("cylinder", 5))
    assert all(np.array_equal(a.cells[k], b.cells[k]) for k in a.cells)
    assert np.array_equal(a.dist, b.dist) and np.array_equal(a.edges, b.edges)
