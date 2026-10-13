"""X4 Phase B adapter (protocol x4b-v1): future maps, canonical remapping, store isolation,
precision and permutation agreement flags, and an end-to-end pool screen on a tiny HMM."""
import numpy as np
import pytest

from topo_pilot.contracts import MemoryBackend, tokens_hash
from topo_pilot.experiment.x4b import (
    Pool,
    ReadThroughBackend,
    canonical_tokens,
    future_maps,
    map_failures,
    pool_checks,
    pool_failures,
)
from topo_pilot.experiment.x4b_audit import agreement_failures, pool_audit

pytestmark = pytest.mark.experiment


def _stochastic(rng, n, m):
    a = rng.random((n, m)) + 0.05
    return a / a.sum(1, keepdims=True)


def test_future_maps_routes_agree_and_checks_pass():
    rng = np.random.default_rng(0)
    T, E = _stochastic(rng, 8, 8), _stochastic(rng, 8, 3)
    maps = future_maps(T, E)
    assert maps.G1.shape == (8, 3) and maps.G2.shape == (8, 9)
    assert map_failures(maps) == []
    assert maps.checks["second_marginal_vs_G1"] > 1e-3      # bT²E differs from Q1
    explicit = np.einsum("nm,mi,mj->nij", T, E, T @ E).reshape(8, 9)
    np.testing.assert_allclose(maps.G2, explicit, atol=1e-14)


def test_future_maps_four_state_path():
    T = np.array([[.6, .4, 0, 0], [.4, .2, .4, 0], [0, .4, .2, .4], [0, 0, .4, .6]])
    E = np.array([[1., 0], [1, 0], [1, 0], [0, 1]])
    maps = future_maps(T, E)
    assert maps.G1[0].tolist() == maps.G1[1].tolist() == [1.0, 0.0]
    assert maps.G2[0, 0] == pytest.approx(1.0) and maps.G2[1, 1] == pytest.approx(0.16)


def test_map_failures_flag_a_corrupted_joint():
    rng = np.random.default_rng(1)
    maps = future_maps(_stochastic(rng, 5, 5), _stochastic(rng, 5, 2))
    maps.checks["first_marginal_diff"] = 1e-6
    assert "first_marginal_diff" in map_failures(maps)


def test_canonical_tokens_invert_the_symbol_permutation():
    perm = np.array([2, 0, 3, 1])
    canon = np.array([[0, 1, 2, 3, 3]])
    run = perm[canon]                       # token = symbol_perm[j] (D-019)
    np.testing.assert_array_equal(canonical_tokens(run, perm), canon)


def test_read_through_backend_never_writes_to_the_main_store():
    main, out = MemoryBackend(), MemoryBackend()
    main.put("A/1/meta.json", b"main")
    store = ReadThroughBackend(main, out)
    store.put("B/2/meta.json", b"new")
    assert store.get("A/1/meta.json") == b"main" and store.get("B/2/meta.json") == b"new"
    assert main.list("") == ["A/1/meta.json"] and out.list("") == ["B/2/meta.json"]


def _agreement(**over):
    base = {"b32_run_filter_vs_canonical": 0.0, "b32_stored_vs_canonical": 0.0,
            "q_stored_vs_recomputed": 0.0, "Q1_run_perm_vs_canonical": 0.0,
            "F2_float32_vs_float64_max": 3e-8, "run_vocab_partners_identical": True,
            "run_vocab_flags_identical": True, "float32_status": "WITNESS"}
    return {**base, **over}


def test_agreement_failures_flag_precision_and_permutation():
    assert agreement_failures(_agreement(), "WITNESS") == []
    assert agreement_failures(_agreement(F2_float32_vs_float64_max=2e-4), "WITNESS") == [
        "F2_float32_vs_float64_max"]
    assert "run_vocab_permutation" in agreement_failures(
        _agreement(run_vocab_partners_identical=False), "WITNESS")
    assert "float32_status_change" in agreement_failures(_agreement(), "NO_MATERIAL_GAP")


def _tiny_pool(rng, m=600):
    T, E = _stochastic(rng, 6, 6), _stochastic(rng, 6, 3)
    maps = future_maps(T, E)
    canon = rng.integers(0, 3, size=(m, 32))
    b = _stochastic(rng, m, 6)
    keys = tuple(tokens_hash(c) for c in canon)
    ids = tuple(f"test|{i}|{k}" for i, k in enumerate(keys))
    return Pool("test", ids, keys, canon, canon[:, -1], b, b @ maps.G1, b @ maps.G2,
                {1729: tuple(f"h{i}" for i in range(m))}, np.arange(m)), maps


def test_pool_audit_end_to_end_is_deterministic():
    pool, _ = _tiny_pool(np.random.default_rng(2))
    assert pool_failures(pool_checks(pool, 3)) == []
    a, b = pool_audit(pool), pool_audit(pool)
    assert len(a["anchors"]) == 512 and np.array_equal(a["anchors"], b["anchors"])
    assert np.array_equal(a["partners"].idx, b["partners"].idx)
    same = pool.last_symbol[a["partners"].idx[a["partners"].idx >= 0]]
    rows = np.nonzero(a["partners"].idx >= 0)[0]
    np.testing.assert_array_equal(same, pool.last_symbol[a["anchors"][rows]])
    s = a["summary"]
    assert s["d2_below_d1_violations"] == 0 and s["status"] in (
        "WITNESS", "NO_MATERIAL_GAP", "UNDERCOVERED")
    assert len(a["table"]) == 512 and "history_id_1729" in a["table"][0]
