"""P04, P05, P09, P10 (and the dead-symbol / sigma error paths) for the overlap emission."""

from __future__ import annotations

import math

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure
from topo_pilot.process import (
    CENTER_REGISTRY,
    CenterStrategy,
    EmissionConfig,
    GridCenters,
    OverlapGaussian,
)
from topo_pilot.process._diagnostics import check_symbols_alive

pytestmark = pytest.mark.process


def _build(world, seed=1729, **kw):
    cfg = EmissionConfig(mode="overlap", **kw)
    return OverlapGaussian().build(world, cfg, SeedTree(seed))


def _centers():
    return [(0.5 + 2 * a, 0.5 + 2 * b) for a in range(6) for b in range(6)]


def test_P04_rows_sum_to_one_and_direct_formula_square(square12):
    spec = _build(square12, sigma=1.25)
    assert spec.E.shape == (144, 36)
    assert np.max(np.abs(spec.E.sum(axis=1) - 1.0)) < 1e-12
    # state (3, 7) -> id 3*12+7 = 43; direct plain-python softmax over the 36 centers
    z = (3, 7)
    w = [math.exp(-((z[0] - cx) ** 2 + (z[1] - cy) ** 2) / (2 * 1.25**2)) for cx, cy in _centers()]
    expected = np.array(w) / sum(w)
    got = spec.E[43][spec.symbol_perm]  # center order: column of center j is symbol_perm[j]
    assert np.max(np.abs(got - expected)) < 1e-14
    # hand value: nearest centers of (3,7) are (2.5,6.5),(2.5,8.5),(4.5,6.5),(4.5,8.5)
    assert expected.argmax() == _centers().index((2.5, 6.5))


def test_P04_cylinder_x_distance_is_periodic(cylinder12, square12):
    # state (11, 0) vs centers c00=(0.5,0.5) (j=0) and c50=(10.5,0.5) (j=30), sigma=1.25.
    # cylinder: dx(c00) = min(10.5, 1.5) = 1.5 -> d^2 = 2.25+0.25 = 2.5 ; dx(c50)=0.5 -> d^2 = 0.5
    sig = 1.25
    cyl = _build(cylinder12, sigma=sig)
    row = cyl.E[11 * 12 + 0][cyl.symbol_perm]
    assert row[0] / row[30] == pytest.approx(math.exp(-(2.5 - 0.5) / (2 * sig**2)), rel=1e-12)
    # square: d^2(c00) = 10.5^2 + 0.25 = 110.5 vs 0.5
    sq = _build(square12, sigma=sig)
    row = sq.E[11 * 12 + 0][sq.symbol_perm]
    assert row[0] / row[30] == pytest.approx(math.exp(-(110.5 - 0.5) / (2 * sig**2)), rel=1e-9)


def test_logsumexp_no_underflow_nan_with_tiny_sigma(square12):
    spec = _build(square12, sigma=0.45)
    assert np.all(np.isfinite(spec.E))
    assert np.max(np.abs(spec.E.sum(axis=1) - 1.0)) < 1e-12


@pytest.mark.parametrize("family", ["square", "cylinder"])
def test_P05_factorizes_on_core_worlds(family, square12, cylinder12):
    world = {"square": square12, "cylinder": cylinder12}[family]
    spec = _build(world, sigma=1.25)
    assert spec.diagnostics["factorizes"] is True
    # independent reconstruction in center order
    Ec = spec.E[:, spec.symbol_perm].reshape(12, 12, 6, 6)
    Ex = Ec.sum(axis=(1, 3)) / 12
    Ey = Ec.sum(axis=(0, 2)) / 12
    assert np.max(np.abs(Ec - np.einsum("xa,yb->xyab", Ex, Ey))) < 1e-12
    assert set(spec.diagnostics) == {"H_W_given_Z", "H_W", "p_w", "coverage_radius",
                                     "row_entropy_quantiles", "factorizes"}


def test_diagnostics_values(square12):
    d = _build(square12, sigma=1.25).diagnostics
    assert sum(d["p_w"]) == pytest.approx(1.0, abs=1e-12)
    assert 0 < d["H_W_given_Z"] < d["H_W"] <= math.log(36) + 1e-12
    assert len(d["row_entropy_quantiles"]) == 5
    assert d["row_entropy_quantiles"] == sorted(d["row_entropy_quantiles"])
    # every state is within sqrt(0.5^2+0.5^2)... worst corner (0,0)->(0.5,0.5): 0.7071
    assert d["coverage_radius"] == pytest.approx(math.sqrt(0.5), abs=1e-12)


def test_P09_symbol_names_permute_columns_only(square12):
    a, b = _build(square12, seed=1), _build(square12, seed=2)
    assert not np.array_equal(a.symbol_perm, b.symbol_perm)
    # center j sits in column symbol_perm[j]: both must carry the same center-order matrix
    assert np.array_equal(a.E[:, a.symbol_perm], b.E[:, b.symbol_perm])
    for key in ("H_W_given_Z", "H_W", "coverage_radius", "row_entropy_quantiles", "factorizes"):
        assert a.diagnostics[key] == pytest.approx(b.diagnostics[key], abs=1e-12)
    assert sorted(a.diagnostics["p_w"]) == sorted(b.diagnostics["p_w"])
    # symbol_perm[j] is the public id of center j
    assert np.array_equal(np.sort(a.symbol_perm), np.arange(36))
    assert np.array_equal(a.centers, np.array(_centers()))


def test_symbol_perm_uses_replicate_seed_stream(square12):
    tree = SeedTree(7)
    spec = OverlapGaussian().build(square12, EmissionConfig(mode="overlap"), tree)
    expected = SeedTree(7).generator("symbol_names", "square", 7).permutation(36)
    assert np.array_equal(spec.symbol_perm, expected)
    assert "symbol_names/square/7" in tree.issued


@pytest.mark.parametrize("sigma", [0.0, -1.0, None, float("nan")])
def test_P10_nonpositive_sigma_raises(square12, sigma):
    with pytest.raises(StageFailure) as exc:
        _build(square12, sigma=sigma)
    assert exc.value.code is ErrorCode.INVALID_SIGMA


def test_P10_center_outside_chart_raises(square3):
    with pytest.raises(StageFailure) as exc:
        GridCenters().centers(square3, 36, np.random.default_rng(0))
    assert exc.value.code is ErrorCode.INVALID_SIGMA
    with pytest.raises(StageFailure) as exc2:
        _build(square3, sigma=1.25)
    assert exc2.value.code is ErrorCode.INVALID_SIGMA


def test_P10_dead_symbol_helper_and_constructed_build(square12, monkeypatch):
    with pytest.raises(StageFailure) as exc:
        check_symbols_alive(np.array([0.5, 0.49995, 5e-5]))
    assert exc.value.code is ErrorCode.INVALID_SIGMA and exc.value.detail == "dead_symbol"

    class Five(CenterStrategy):
        name = "five"

        def centers(self, world, n_centers, rng):
            # four vertices of a unit cell plus its midpoint: with sigma 0.2 the midpoint
            # symbol gets p_w ~ 4 * e^-6.25 / 144 = 5.4e-5 < 1e-4.
            return np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0.5]], dtype=float)

    monkeypatch.setitem(CENTER_REGISTRY, "five", Five)
    with pytest.raises(StageFailure) as exc2:
        _build(square12, V=5, sigma=0.2, center_strategy="five")
    assert exc2.value.code is ErrorCode.INVALID_SIGMA and exc2.value.detail == "dead_symbol"
    assert _build(square12, V=5, sigma=1.25, center_strategy="five").E.shape == (144, 5)


def test_error_state_order_and_unknown_strategy(square12):
    import dataclasses
    bad = dataclasses.replace(square12, coords=square12.coords[::-1].copy())
    with pytest.raises(StageFailure) as exc:
        _build(bad, sigma=1.25)
    assert exc.value.code is ErrorCode.STATE_ORDER_MISMATCH
    with pytest.raises(StageFailure) as exc2:
        _build(square12, sigma=1.25, center_strategy="nope")
    assert exc2.value.code is ErrorCode.INVALID_CONFIG


def test_graph_metric_uses_manhattan(square12):
    spec = _build(square12, sigma=1.25, metric="graph")
    # state (0,0) to center (0.5,0.5): graph distance 1.0 ; coverage radius = 1.0 at the corners
    assert spec.diagnostics["coverage_radius"] == pytest.approx(1.0)
