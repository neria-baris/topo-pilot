import numpy as np
import pytest

from topo_pilot import contracts as C
from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.contracts import testing as T

pytestmark = pytest.mark.contracts


@pytest.mark.parametrize("family,n,vef,betti", [
    ("square", 3, (9, 12, 4), (1, 0, 0)),
    ("cylinder", 3, (9, 15, 6), (1, 1, 0)),
])
def test_C14_tiny_world_spec_valid_and_counts(family, n, vef, betti):
    w = T.tiny_world_spec(family, n)
    w.validate()
    v, e, f = vef
    assert w.coords.shape[0] == v and w.edges.shape[0] == e and w.cells[2].shape[0] == f
    assert v - e + f == sum(b * (-1) ** i for i, b in enumerate(betti))  # Euler characteristic
    assert w.betti_expected[2] == betti and w.betti_expected[3] == betti
    assert w.betti_computed == w.betti_expected
    assert w.dist.shape == (v, v) and np.all(np.diag(w.dist) == 0) and np.allclose(w.dist, w.dist.T)


def test_C14_tiny_world_spec_deterministic_and_sizes():
    a, b = T.tiny_world_spec("cylinder", 4), T.tiny_world_spec("cylinder", 4)
    b.validate()
    for k in ("coords", "edges", "dist", "dist_graph"):
        assert np.array_equal(getattr(a, k), getattr(b, k))
    assert a.coords.shape[0] == 16
    T.tiny_world_spec("square", 5).validate()
    with pytest.raises(StageFailure) as ei:
        T.tiny_world_spec("torus")  # type: ignore[arg-type]
    assert ei.value.code == ErrorCode.INVALID_CONFIG


def test_C14_tiny_hmm_is_a_valid_hmm():
    Tm, E, pi = T.tiny_hmm()
    assert Tm.shape == (4, 4) and E.shape == (4, 3) and pi.shape == (4,)
    assert np.allclose(Tm.sum(axis=1), 1) and np.allclose(E.sum(axis=1), 1)
    assert np.allclose(Tm, Tm.T) and np.isclose(pi.sum(), 1)
    assert np.allclose(pi @ Tm, pi)
    assert np.all(Tm >= 0) and np.all(E >= 0)
    assert np.all(pi @ E > 1e-4)
    C.TransitionSpec(T=Tm, pi=pi).validate()
    T2, E2, pi2 = T.tiny_hmm()
    assert np.array_equal(Tm, T2) and np.array_equal(E, E2) and np.array_equal(pi, pi2)


def test_C14_tiny_observations_valid_and_deterministic():
    a, b = T.tiny_observations(8, 0), T.tiny_observations(8, 0)
    a.validate()
    assert a.split == "test" and a.V == 3
    assert a.tokens.shape == (8, 33) and a.tokens.dtype == np.uint8 and a.tokens.max() < 3
    assert a.sequence_id.dtype == np.int64 and a.sequence_id.tolist() == list(range(8))
    assert np.array_equal(a.tokens, b.tokens) and np.array_equal(a.sequence_id, b.sequence_id)
    assert not np.array_equal(a.tokens, T.tiny_observations(8, 1).tokens)
    assert T.tiny_observations(3, 5).tokens.shape == (3, 33)
    # prefix property is not promised; but different R still validates
    T.tiny_observations(20, 2).validate()


def test_C14_memory_store_is_fresh_and_works():
    s1, s2 = T.memory_store(), T.memory_store()
    obs = T.tiny_observations()
    aid = s1.save(obs, config={"a": 1}, parents=[], seed_map={}, consumer="experiment")
    assert s1.find(C.ObservationSet) == [aid]
    assert s2.find(C.ObservationSet) == []
    assert np.array_equal(s1.load(C.ObservationSet, aid, consumer="learner").tokens, obs.tokens)
