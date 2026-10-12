"""P01-P03 and error paths of the transition builder."""

from __future__ import annotations

import dataclasses
import inspect

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.process import TransitionBuilder, TransitionConfig
from topo_pilot.process.transition import check_support

pytestmark = pytest.mark.process


def _build(world, p_stay=0.2):
    return TransitionBuilder().build(world, TransitionConfig(p_stay=p_stay))


def test_P01_square_n3_hand_values(square3):
    # ids x*3+y. corner (0,0)=0: deg 2 -> stay 1 - 2*0.2 = 0.6 ; edge (0,1)=1: deg 3 -> 0.4 ;
    # centre (1,1)=4: deg 4 -> 0.2 ; every neighbour entry is (1-0.2)/4 = 0.2.
    T = _build(square3).T
    assert T[0, 0] == pytest.approx(0.6, abs=1e-15)
    assert T[1, 1] == pytest.approx(0.4, abs=1e-15)
    assert T[4, 4] == pytest.approx(0.2, abs=1e-15)
    assert {j for j in range(9) if j != 0 and T[0, j] > 0} == {1, 3}
    assert {j for j in range(9) if j != 1 and T[1, j] > 0} == {0, 2, 4}
    assert {j for j in range(9) if j != 4 and T[4, j] > 0} == {1, 3, 5, 7}
    for i, nbrs in ((0, (1, 3)), (1, (0, 2, 4)), (4, (1, 3, 5, 7))):
        assert all(T[i, j] == pytest.approx(0.2, abs=1e-15) for j in nbrs)
    assert np.sort(np.diag(T)).tolist() == pytest.approx([0.2] + [0.4] * 4 + [0.6] * 4)


def test_P02_cylinder_n3_no_corners_and_wrap(cylinder3):
    spec = _build(cylinder3)
    T = spec.T
    # y = 0 edge row: neighbours (x-1,0), (x+1,0), (x,1) -> deg 3 -> stay 0.4 for x=0,1,2.
    for x in range(3):
        assert T[x * 3, x * 3] == pytest.approx(0.4, abs=1e-15)
        assert T[x * 3 + 2, x * 3 + 2] == pytest.approx(0.4, abs=1e-15)
        assert T[x * 3 + 1, x * 3 + 1] == pytest.approx(0.2, abs=1e-15)
    assert np.diag(T).min() == pytest.approx(0.2)  # no corner (0.6) anywhere
    assert 0.6 not in np.round(np.diag(T), 12)
    # wrap neighbours: x=0 and x=2 are adjacent (period 3)
    assert T[0 * 3 + 1, 2 * 3 + 1] == pytest.approx(0.2, abs=1e-15)
    assert T[0, 6] == pytest.approx(0.2, abs=1e-15)
    assert spec.d_max == 4


@pytest.mark.parametrize("family", ["square", "cylinder"])
def test_P03_contract_invariants(family, square12, cylinder12):
    world = {"square": square12, "cylinder": cylinder12}[family]
    spec = _build(world)
    T, pi = spec.T, spec.pi
    n = world.n_states
    assert T.shape == (n, n)
    assert np.array_equal(T, T.T)
    assert np.max(np.abs(T.sum(axis=1) - 1.0)) < 1e-12
    assert np.all(pi == 1.0 / n)
    assert np.max(np.abs(pi @ T - pi)) <= 1e-12
    edges = {tuple(e) for e in np.asarray(world.edges).tolist()}
    off = {(i, j) for i, j in zip(*np.nonzero(T)) if i != j}
    assert {tuple(sorted(p)) for p in off} <= edges
    check_support(T, world)
    assert spec.p_stay == 0.2


def test_p_stay_changes_values_only_by_formula(square3):
    T = _build(square3, p_stay=0.0).T
    assert T[0, 0] == pytest.approx(0.5)  # 1 - 2 * 1/4
    assert T[4, 4] == pytest.approx(0.0)


def test_error_illegal_support(square3):
    T = np.eye(9)
    T[0, 8] = T[8, 0] = 0.5  # (0,0) and (2,2) are not adjacent
    T[0, 0] = T[8, 8] = 0.5
    with pytest.raises(StageFailure) as exc:
        check_support(T, square3)
    assert exc.value.code is ErrorCode.NONSTOCHASTIC
    assert exc.value.detail == "illegal_support"


def test_error_bad_p_stay_and_kind(square3):
    for cfg in (TransitionConfig(p_stay=1.0), TransitionConfig(p_stay=-0.1),
                TransitionConfig(kind="nope")):  # type: ignore[arg-type]
        with pytest.raises(StageFailure) as exc:
            TransitionBuilder().build(square3, cfg)
        assert exc.value.code is ErrorCode.INVALID_CONFIG


def test_error_state_order_mismatch(square3):
    shuffled = dataclasses.replace(square3, coords=square3.coords[::-1].copy())
    with pytest.raises(StageFailure) as exc:
        TransitionBuilder().build(shuffled, TransitionConfig())
    assert exc.value.code is ErrorCode.STATE_ORDER_MISMATCH


def test_P11_transition_builder_does_not_accept_emission():
    params = inspect.signature(TransitionBuilder.build).parameters
    assert list(params) == ["self", "world", "cfg"]
    assert not any("Emission" in str(p.annotation) for p in params.values())
