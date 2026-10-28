"""Author B (job 0161), TEST_PLAN section 3 `test_b_process.py`: `build_process` on a
MemoryBackend store (KB1 identities, KB4 identity part), `arrays_sha256`, `spec_checksums`,
IDENTITY failures, and `hwsb_dry.build_tiny_process`. tools/hwsb/*.py unread."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_data as hd  # noqa: E402
import hwsb_dry as hdry  # noqa: E402
import hws_worlds as hw  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    ArtifactStore, EmissionSpec, MemoryBackend, SeedTree, payload_checksum)
from topo_pilot.process.emission import EmissionConfig  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hwsb" / "CONTRACT.json").read_text(encoding="utf-8"))
KB1 = CONTRACT["known_cases"]["KB1"]
KB2 = CONTRACT["known_cases"]["KB2"]
W0_CFG = EmissionConfig("overlap", 36, 1.25, "grid")


def f64_sha(x):
    return hashlib.sha256(np.ascontiguousarray(x, dtype=np.float64).tobytes()).hexdigest()


@pytest.fixture(scope="module")
def star():
    store = ArtifactStore(MemoryBackend())
    return store, hd.build_process(store)


@pytest.fixture(scope="module")
def w0():
    store = ArtifactStore(MemoryBackend())
    return store, hd.build_process(store, masters=(1729,), emission_cfg=W0_CFG)


# ------------------------------------------------------------------ w* (KB1)
def test_star_ids_match_contract(star):
    _, proc = star
    assert proc["ids"]["world"] == KB1["WorldSpec"]["id"] == "21feee1d8ee5422e"
    assert proc["ids"]["transition"] == KB1["TransitionSpec"]["id"] == "e4dafc7b9785c172"
    assert set(proc["ids"]["emission"]) == {620201, 620202}


def test_star_shapes_and_constants(star):
    _, proc = star
    assert (proc["V"], proc["N"], proc["W"], proc["Hh"], proc["n_axial"]) == (36, 144, 12, 12, 6)
    assert proc["sigma"] == Fraction(7, 4) and proc["neighbour"] == Fraction(1, 5)
    assert proc["T"].shape == (144, 144) and proc["T"].dtype == np.float64
    assert proc["pi"].shape == (144,) and proc["coords"].shape == (144, 2)
    assert proc["features"].shape == (144, 2)
    assert np.allclose(proc["T"].sum(axis=1), 1.0, atol=1e-12)
    assert np.allclose(proc["pi"] @ proc["T"], proc["pi"], atol=1e-12)


def test_star_spec_checksums_match_contract(star):
    store, proc = star
    sums = hd.spec_checksums(store, proc)
    assert sums["WorldSpec"] == KB1["WorldSpec"]["payload_sha256"]
    assert sums["TransitionSpec"] == KB1["TransitionSpec"]["payload_sha256"]
    for m in hc.MASTERS:
        spec = store.load(EmissionSpec, proc["ids"]["emission"][m], consumer="experiment")
        assert sums["EmissionSpec"][m] == payload_checksum(*spec.to_payload())


def test_star_arrays_sha256_equal_selection(star):
    _, proc = star
    want = KB1["selection_sha256"]
    got = hd.arrays_sha256(proc)
    assert {k: got[k] for k in want} == want
    for m in hc.MASTERS:  # KB1 b: each master's canonical emission hashes to the selection E
        assert f64_sha(proc["E_canon"][m]) == want["E"]
    assert f64_sha(proc["T"]) == want["T"] and f64_sha(proc["coords"]) == want["coords"]


def test_star_e_canon_is_shared_and_named_inverts(star):
    _, proc = star
    a, b = (proc["E_canon"][m] for m in hc.MASTERS)
    assert np.array_equal(a, b) and a.tobytes() == b.tobytes()
    assert np.array_equal(proc["E_canon_shared"], a)
    for m in hc.MASTERS:
        perm = np.asarray(proc["perm"][m])
        assert np.array_equal(np.sort(perm), np.arange(36))
        assert np.array_equal(perm[np.argsort(perm)], np.arange(36))
        assert np.array_equal(proc["E_named"][m][:, perm], proc["E_canon"][m])
    assert not np.array_equal(proc["perm"][620201], proc["perm"][620202])
    assert np.allclose(proc["E_canon_shared"].sum(axis=1), 1.0, atol=1e-12)


def test_star_canonical_symbol_is_axial_cell_centre(star):
    # protocol: canonical symbol v = 6a + b has its centre at (0.5 + 2a, 0.5 + 2b): the emission
    # mass of symbol v peaks at the lattice state nearest that centre.
    _, proc = star
    E, coords = proc["E_canon_shared"], proc["coords"]
    for v in (0, 7, 20, 35):
        a, b = divmod(v, 6)
        best = coords[int(np.argmax(E[:, v]))]
        assert abs(best[0] - (0.5 + 2 * a)) <= 0.5 + 1e-9 or abs(abs(best[0] - (0.5 + 2 * a)) - 12) <= 0.5
        assert abs(best[1] - (0.5 + 2 * b)) <= 0.5 + 1e-9


# ------------------------------------------------------------------ w0 (KB2/KB4 identity)
def test_w0_emission_identity_matches_contract(w0):
    store, proc = w0
    assert proc["ids"]["emission"][1729] == KB2["EmissionSpec_1729"]["id"] == "3633ac27dab50cf4"
    assert proc["ids"]["world"] == KB1["WorldSpec"]["id"]
    assert proc["ids"]["transition"] == KB1["TransitionSpec"]["id"]
    sums = hd.spec_checksums(store, proc)
    assert sums["EmissionSpec"][1729] == KB2["EmissionSpec_1729"]["payload_sha256"]
    assert sums["WorldSpec"] == KB1["WorldSpec"]["payload_sha256"]
    assert proc["sigma"] == Fraction(5, 4) and proc["neighbour"] == Fraction(1, 5)
    assert np.array_equal(proc["E_canon"][1729], proc["E_canon_shared"])


# ------------------------------------------------------------------ IDENTITY failures
class PlantedStore(ArtifactStore):
    """Returns a modified EmissionSpec for one planted artifact id (planted defect fixture)."""

    def __init__(self, target, mutate):
        super().__init__(MemoryBackend())
        self.target, self.mutate = target, mutate

    def load(self, cls, artifact_id, *, consumer):
        obj = super().load(cls, artifact_id, consumer=consumer)
        if cls is EmissionSpec and artifact_id == self.target:
            obj = copy.copy(obj)
            self.mutate(obj)
        return obj


def set_attr(obj, name, value):
    object.__setattr__(obj, name, value)


def test_non_permutation_perm_is_identity_failure(star):
    eid = star[1]["ids"]["emission"][620201]
    store = PlantedStore(eid, lambda s: set_attr(s, "symbol_perm", np.zeros(36, dtype=np.int64)))
    with pytest.raises(hc.HwsbStop) as e:
        hd.build_process(store)
    assert str(e.value.status) == "FAIL_TECHNICAL/IDENTITY"


def test_differing_e_canon_is_identity_failure(star):
    eid = star[1]["ids"]["emission"][620202]

    def perturb(spec):
        E = np.array(spec.E, dtype=np.float64)
        E[0, :2] = E[0, :2][::-1] + np.array([1e-3, -1e-3])
        set_attr(spec, "E", E)

    store = PlantedStore(eid, perturb)
    with pytest.raises(hc.HwsbStop) as e:
        hd.build_process(store)
    assert str(e.value.status) == "FAIL_TECHNICAL/IDENTITY"


# ------------------------------------------------------------------ tiny process (dry)
def test_build_tiny_process_shapes_and_naming():
    store = ArtifactStore(MemoryBackend())
    proc = hdry.build_tiny_process(store)
    tiny = hw.build_tiny()
    assert (proc["V"], proc["N"], proc["W"], proc["Hh"], proc["n_axial"]) == (3, 12, 6, 2, 1)
    assert set(proc["ids"]["emission"]) == set(hc.DRY_MASTERS) == {629901, 629902}
    assert np.array_equal(proc["E_canon_shared"], tiny["E"])
    assert np.array_equal(proc["T"], np.asarray(tiny["T"])) and proc["T"].shape == (12, 12)
    assert np.array_equal(proc["features"], hw.features(proc["coords"], 6))
    for m in hc.DRY_MASTERS:
        perm = np.asarray(proc["perm"][m])
        want = SeedTree(m).generator("symbol_names", "cylinder", m).permutation(3)
        assert np.array_equal(perm, want)
        assert np.array_equal(proc["E_named"][m][:, perm], tiny["E"])  # named = perm[canonical]
        assert np.array_equal(proc["E_canon"][m], tiny["E"])
        spec = store.load(EmissionSpec, proc["ids"]["emission"][m], consumer="experiment")
        assert np.array_equal(np.asarray(spec.symbol_perm), perm)
        assert np.array_equal(spec.E, proc["E_named"][m])


def test_build_tiny_process_masters_argument():
    proc = hdry.build_tiny_process(ArtifactStore(MemoryBackend()), masters=(629901,))
    assert set(proc["ids"]["emission"]) == {629901}
