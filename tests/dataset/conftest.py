"""Module-local fixtures: a tiny stored process (world, T, E) built by hand."""
import numpy as np
import pytest

from topo_pilot import contracts as C
from topo_pilot.contracts import testing as CT
from topo_pilot.dataset import DatasetConfig


def make_emission(E: np.ndarray, pi: np.ndarray, perm, sigma: float = 0.5) -> C.EmissionSpec:
    """EmissionSpec with hand-filled diagnostics; ``perm[j]`` = public id of canonical symbol j."""
    diag = {"H_W_given_Z": 0.0, "H_W": 0.0, "p_w": (pi @ E).tolist(), "coverage_radius": 0.0,
            "row_entropy_quantiles": [0.0], "factorizes": False}
    return C.EmissionSpec(E=E, symbol_perm=np.asarray(perm, dtype=np.int32), mode="overlap",
                          sigma=sigma, diagnostics=diag)


@pytest.fixture
def tiny_cfg() -> DatasetConfig:
    return DatasetConfig(n_train=200, n_dev=100, n_test=40, n_panels=2, panel_size=8)


@pytest.fixture
def process():
    """``(store, transition_id, emission_id, E_canon)`` with an identity symbol permutation."""
    store = CT.memory_store()
    T, E, pi = CT.tiny_hmm()
    wid = store.save(CT.tiny_world_spec("cylinder"), config={"family": "cylinder"}, parents=[],
                     seed_map={}, consumer="world")
    tid = store.save(C.TransitionSpec(T=T, pi=pi), config={"p": 1}, parents=[wid], seed_map={},
                     consumer="process")
    eid = store.save(make_emission(E, pi, [0, 1, 2]), config={"mode": "overlap", "sigma": 0.5},
                     parents=[wid], seed_map={}, consumer="process")
    return store, tid, eid, E


@pytest.fixture
def add_emission(process):
    """Factory: store an emission whose canonical form ``E[:, perm]`` equals ``E_canon``."""
    store, tid, eid, _ = process
    _, _, pi = CT.tiny_hmm()
    wid = store.meta(eid).parent_ids[0]

    def _add(E_canon: np.ndarray, perm) -> str:
        E = E_canon[:, np.argsort(perm)]
        cfg = {"mode": "overlap", "sigma": 0.5, "perm": [int(p) for p in perm]}
        return store.save(make_emission(E, pi, perm), config=cfg, parents=[wid],
                          seed_map={}, consumer="process")

    return _add
