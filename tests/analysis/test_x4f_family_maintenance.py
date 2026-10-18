"""Synthetic fault injection into map construction and STOP within the draw loop."""
import numpy as np
import pytest

from topo_pilot.analysis import random_family, whiten
from topo_pilot.analysis import x4f_erasure as erasure

pytestmark = pytest.mark.analysis


def test_family_stop_before_second_draw():
    X = np.random.default_rng(3).normal(size=(32, 4))
    drawn = []

    def rng_for(j):
        drawn.append(j)
        return np.random.default_rng(j)

    def guard(step):
        if step == "random_family draw 1":
            raise RuntimeError("synthetic STOP")

    with pytest.raises(RuntimeError, match="synthetic STOP"):
        random_family(X, whiten(X), 1, 1e10, rng_for, max_draws=3, checkpoint=guard)
    assert drawn == [0]


@pytest.mark.parametrize("defect", ["idempotence", "small_idempotence", "rank", "range",
                                    "complement", "nonfinite"])
def test_invalid_accepted_map_fails_closed(monkeypatch, defect):
    X = np.random.default_rng(4).normal(size=(40, 4))
    X[:, -1] = 0
    wh = whiten(X)

    def bad_basis(*args):
        E = np.zeros((4, 4))
        E[0, 0] = .5 if defect == "idempotence" else 1
        if defect == "small_idempotence":
            E[0, 0] = 1 - 5e-9
        if defect == "rank":
            E[1, 1] = 1
        if defect == "range":
            E[:] = 0
            E[0, 0] = E[3, 3] = E[0, 3] = E[3, 0] = .5
        M = np.eye(4) - E
        if defect == "complement":
            M = np.eye(4)
        if defect == "nonfinite":
            M[0, 0] = np.nan
        return E, M

    monkeypatch.setattr(erasure, "eraser_from_basis", bad_basis)
    family = random_family(X, wh, 1, 1., lambda j: np.random.default_rng(j),
                           n_accept=1, max_draws=1, tol=1e3)
    assert family.status == "ERASER_INVALID"
    assert family.maps == []
