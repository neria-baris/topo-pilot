"""X4 Phase B2 lineage adapter (protocol x4b2-v1): frozen streams and namespaces, determinism,
state discarding, chunked beliefs, window overlap and the Phase B ambient link."""
import numpy as np
import pytest

from topo_pilot.contracts import StageFailure
from topo_pilot.experiment.x4b2 import (
    FROZEN_CODES,
    ROLES,
    ambient_match,
    beliefs_p32,
    first_token_p,
    sample_pool,
    sequence_ids,
    windows,
)

pytestmark = pytest.mark.experiment


def _hmm(rng, n=6, v=3):
    T = rng.random((n, n)) + 0.1
    E = rng.random((n, v)) + 0.1
    T /= T.sum(1, keepdims=True)
    E /= E.sum(1, keepdims=True)
    pi = np.full(n, 1.0 / n)
    return T, E, pi


def test_sequence_ids_frozen_namespace_and_disjoint():
    ids = {r: sequence_ids(r, 100) for r in ROLES}
    for r, a in ids.items():
        assert int(a[0]) >> 32 == FROZEN_CODES[r]
        assert (int(a[0]) >> 28) & 0xF == 5            # not a DatasetStage split code
        assert np.all(np.diff(a) == 1)
    allids = np.concatenate(list(ids.values()))
    assert np.unique(allids).size == allids.size
    with pytest.raises(StageFailure):
        sequence_ids("test", 10)


def test_sample_pool_is_deterministic_and_returns_no_states():
    T, E, pi = _hmm(np.random.default_rng(0))
    a, meta = sample_pool("reference", T, E, pi, n=400)
    b, _ = sample_pool("reference", T, E, pi, n=400)
    c, _ = sample_pool("repetition1", T, E, pi, n=400)
    assert a.shape == (400, 33) and np.array_equal(a, b) and not np.array_equal(a, c)
    assert set(meta) == {"role", "stream", "seed", "n", "first_token_chi2_p"}
    assert meta["stream"] == "x4b2-v1/pool/cylinder/overlap/1.25/reference"
    with pytest.raises(StageFailure):
        sample_pool("unknown", T, E, pi, n=10)


def test_first_token_p_detects_bias():
    p_w = np.array([0.5, 0.3, 0.2])
    fair = np.repeat([0, 1, 2], [500, 300, 200])
    assert first_token_p(fair, p_w) > 0.5
    assert first_token_p(np.zeros(1000, dtype=int), p_w) < 1e-4


def test_beliefs_chunked_equal_unchunked():
    rng = np.random.default_rng(1)
    T, E, pi = _hmm(rng)
    tok = rng.integers(0, 3, size=(37, 32))
    np.testing.assert_array_equal(beliefs_p32(T, E, pi, tok, chunk=5),
                                  beliefs_p32(T, E, pi, tok, chunk=1000))


def test_windows_count_identical_histories():
    a = np.array([[0] * 32, [1] * 32, [0] * 32], dtype=np.uint8)
    b = np.array([[1] * 32, [2] * 32], dtype=np.uint8)
    assert windows(a).size == 2 and np.intersect1d(windows(a), windows(b)).size == 1


class _Row:
    def __init__(self, rho):
        self.rho = rho


class _Audit:
    verdict = "ALLOWS_STABLE"
    H_singular_values = (1.0, 0.5)
    G2_singular_values = (2.0, 1.0)
    rows = (_Row(0.1), _Row(0.1), _Row(0.1))


def test_ambient_match_requires_identical_result():
    ref = {"verdict": "ALLOWS_STABLE", "H_singular_values": [1.0, 0.5],
           "G2_singular_values": [2.0, 1.0], "rows": [{"rho": 0.1}] * 3}
    assert ambient_match(_Audit(), ref)["ok"]
    assert not ambient_match(_Audit(), {**ref, "H_singular_values": [1.0, 0.6]})["ok"]
    assert not ambient_match(_Audit(), {**ref, "verdict": "FACTORIZES"})["ok"]
    assert not ambient_match(_Audit(), {**ref, "H_singular_values": [1.0]})["ok"]
