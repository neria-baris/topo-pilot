"""Independent contract tests, written from the API contract (X5_G1_TRAINING_API.md §2-§4, §8
"Lineage and oracle") and protocol x5g1-train-v3 §2-§4, without reading the implementation.

Covers the study lineage (frozen constants, streams, paired generators, sequence-id bit layout,
paired draws, pool ObservationSets and configs, disjointness), the w33-free oracle row under a
non-identity symbol permutation, and the p32 scoring functions. Tiny N=4 / V=3 processes only.
"""

from __future__ import annotations

import numpy as np
import pytest
import torch

from topo_pilot.contracts import (
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
)
from topo_pilot.contracts.testing import tiny_hmm
from topo_pilot.dataset import HMMSampler
from topo_pilot.experiment import x5g1_lineage as calib
from topo_pilot.experiment import x5g1t_lineage as lin
from topo_pilot.experiment.x4b2 import process_code
from topo_pilot.experiment.x5g1t_oracle import oracle_q32
from topo_pilot.experiment.x5g1t_score import kl_from_log_probs, p32_log_probs, regret_rows
from topo_pilot.learner import ModelConfig, TransformerLM
from topo_pilot.oracle import BayesFilter

pytestmark = pytest.mark.experiment

PERM = np.array([2, 0, 1])  # non-identity permutation of the 3 named symbols
T_FLAT, E, PI = tiny_hmm()
# A second symmetric doubly-stochastic kernel (pi stays uniform): stay 0.4, else 0.2.
T_OTHER = np.full((4, 4), 0.2) + np.eye(4) * 0.2
KERNELS = {"a0": T_FLAT, "a020": T_OTHER}
TINY_MODEL = ModelConfig(vocab_in=4, vocab_out=3, n_layers=1, d_model=8, n_heads=2, d_mlp=16)


def _code(exc: pytest.ExceptionInfo) -> ErrorCode:
    return exc.value.code


# ---------------------------------------------------------------- lineage: frozen constants


def test_constants_frozen():
    assert lin.NAMESPACE == "x5g1-train-v1"
    assert lin.PROTOCOL == "x5g1-train-v3"
    assert lin.MASTERS == (310001, 310002, 310003)
    assert lin.ARMS == ("a0", "a020")
    assert lin.CODES == {"train": 9, "dev": 10, "test": 11}
    assert lin.SIZES == {"train": 131072, "dev": 4096, "test": 4096}
    assert lin.TEST_MASTER == "shared"


@pytest.mark.parametrize("split", ["train", "dev", "test"])
def test_stream(split):
    assert tuple(lin.stream(split)) == ("x5g1-train-v1", split, "cylinder", "overlap", "1.25")


def test_stream_unknown_split():
    with pytest.raises(StageFailure) as exc:
        lin.stream("calibration")
    assert _code(exc) == ErrorCode.INVALID_CONFIG


# ---------------------------------------------------------------- lineage: sequence ids


@pytest.mark.parametrize("split,arm,master", [("train", "a0", 310001), ("dev", "a020", 310003),
                                              ("test", "a020", "shared")])
def test_sequence_ids_formula_and_bits(split, arm, master):
    n = 37
    ids = lin.sequence_ids(split, arm, master, n)
    code = process_code("cylinder", "overlap", "1.25", f"x5g1-train-v1:{split}:{arm}:{master}")
    expected = ((code << 32) | (lin.CODES[split] << 28)) | np.arange(n, dtype=np.int64)
    assert ids.dtype == np.int64 and ids.shape == (n,)
    np.testing.assert_array_equal(ids, expected)
    np.testing.assert_array_equal(ids >> 32, np.full(n, code))
    np.testing.assert_array_equal((ids >> 28) & 0xF, np.full(n, lin.CODES[split]))
    np.testing.assert_array_equal(ids & ((1 << 28) - 1), np.arange(n))


@pytest.mark.parametrize("split,arm,n", [("calibration", "a0", 4), ("train", "a1", 4),
                                         ("dev", "a0", 0), ("dev", "a0", 2**28 + 1)])
def test_sequence_ids_invalid(split, arm, n):
    with pytest.raises(StageFailure) as exc:
        lin.sequence_ids(split, arm, 310001, n)
    assert _code(exc) == ErrorCode.INVALID_CONFIG


# ---------------------------------------------------------------- lineage: generators


def test_paired_generators_separate_and_identical():
    g1, g2 = lin.paired_generators("train", 310002)
    assert g1 is not g2
    ref = SeedTree(310002).generator(*lin.stream("train")).random(20)
    a = g1.random(20)  # advancing g1 must not advance g2
    b = g2.random(20)
    np.testing.assert_array_equal(a, ref)
    np.testing.assert_array_equal(b, ref)


def test_paired_generators_test_split_uses_seed_zero():
    g1, g2 = lin.paired_generators("test", "shared")
    ref = SeedTree(0).generator(*lin.stream("test")).random(10)
    np.testing.assert_array_equal(g1.random(10), ref)
    np.testing.assert_array_equal(g2.random(10), ref)


@pytest.mark.parametrize("split,master", [("test", 310001), ("test", 0), ("train", "shared"),
                                          ("dev", "shared"), ("calibration", 310001)])
def test_paired_generators_invalid(split, master):
    with pytest.raises(StageFailure) as exc:
        lin.paired_generators(split, master)
    assert _code(exc) == ErrorCode.INVALID_CONFIG


def test_draw_pair_matches_sample_named_per_arm():
    out = lin.draw_pair(KERNELS, E, PERM, PI, "dev", 310001, 24)
    assert set(out) == set(lin.ARMS)
    gens = lin.paired_generators("dev", 310001)
    for arm, rng in zip(lin.ARMS, gens):
        ref = calib.sample_named(KERNELS[arm], E, PERM, PI, rng, 24)
        assert out[arm].shape == (24, 33)
        np.testing.assert_array_equal(out[arm], ref)


def test_draw_pair_first_symbol_identical_across_arms():
    # w1 depends only on pi and E (common randomness), so it is identical across arms; later
    # symbols depend on T and differ.
    out = lin.draw_pair(KERNELS, E, PERM, PI, "train", 310003, 64)
    np.testing.assert_array_equal(out["a0"][:, 0], out["a020"][:, 0])
    assert not np.array_equal(out["a0"], out["a020"])
    same = lin.draw_pair({"a0": T_FLAT, "a020": T_FLAT}, E, PERM, PI, "train", 310003, 64)
    np.testing.assert_array_equal(same["a0"], same["a020"])
    np.testing.assert_array_equal(same["a0"], out["a0"])


def test_draw_pair_test_split_is_master_independent():
    a = lin.draw_pair(KERNELS, E, PERM, PI, "test", "shared", 8)
    g = SeedTree(0).generator(*lin.stream("test"))
    np.testing.assert_array_equal(a["a0"], calib.sample_named(T_FLAT, E, PERM, PI, g, 8))


# ---------------------------------------------------------------- lineage: pools


@pytest.mark.parametrize("split", ["train", "dev", "test"])
def test_pool_observation_valid(split):
    master = "shared" if split == "test" else 310001
    named = lin.draw_pair(KERNELS, E, PERM, PI, split, master, 16)["a0"]
    ids = lin.sequence_ids(split, "a0", master, 16)
    obs = lin.pool_observation(split, named, ids, 3)
    assert isinstance(obs, ObservationSet)
    assert obs.split == split and obs.V == 3
    np.testing.assert_array_equal(obs.tokens, named)
    np.testing.assert_array_equal(obs.sequence_id, ids)
    obs.validate()


def test_pool_observation_rejects_invalid():
    named = lin.draw_pair(KERNELS, E, PERM, PI, "dev", 310001, 4)["a0"]
    dup = np.array([1, 1, 2, 3], dtype=np.int64)
    with pytest.raises(StageFailure):
        lin.pool_observation("dev", named, dup, 3)
    ids = lin.sequence_ids("dev", "a0", 310001, 4)
    with pytest.raises(StageFailure):
        lin.pool_observation("dev", named, ids, 2)  # symbol 2 >= V


def test_pool_config_contents():
    assert lin.pool_config("train", "a020", 310002) == {
        "role": "x5g1t-train", "protocol": "x5g1-train-v3", "arm": "a020", "master": 310002,
        "stream": "x5g1-train-v1/train/cylinder/overlap/1.25", "namespace_code": 9}
    cfg = lin.pool_config("test", "a0", "shared")
    assert cfg["master"] == "shared" and cfg["namespace_code"] == 11
    assert cfg["role"] == "x5g1t-test" and cfg["stream"].split("/")[1] == "test"


# ---------------------------------------------------------------- lineage: disjointness


def _all_planned(n: int) -> dict[str, np.ndarray]:
    new = {}
    for arm in lin.ARMS:
        for split in ("train", "dev"):
            for m in lin.MASTERS:
                new[f"{split}:{arm}:{m}"] = lin.sequence_ids(split, arm, m, n)
        new[f"test:{arm}"] = lin.sequence_ids("test", arm, "shared", n)
    return new


def test_disjoint_across_splits_arms_masters():
    new = _all_planned(64)
    assert len(new) == 14
    stored = np.concatenate([calib.sequence_ids(a, 64) for a in calib.ARMS])
    res = lin.collisions(new, stored)
    assert res == {**{k: 0 for k in new}, "internal": 0}
    every = np.concatenate(list(new.values()))
    assert np.unique(every).size == every.size


def test_collisions_counts():
    new = _all_planned(8)
    stored = np.concatenate([new["dev:a0:310002"][:3], new["test:a020"][-1:],
                             np.array([7, 11], dtype=np.int64)])
    res = lin.collisions(new, stored)
    assert res["dev:a0:310002"] == 3 and res["test:a020"] == 1
    assert sum(v for k, v in res.items() if k != "internal") == 4
    assert res["internal"] == 0
    dup = {"x": np.array([1, 2, 3], dtype=np.int64), "y": np.array([3, 4], dtype=np.int64)}
    assert lin.collisions(dup, np.array([2, 9], dtype=np.int64)) == {"x": 1, "y": 0,
                                                                      "internal": 1}


# ---------------------------------------------------------------- oracle


def _named_and_canon(n: int) -> tuple[np.ndarray, np.ndarray]:
    rng = SeedTree(5).generator("x5g1t-oracle-test")
    canon, _ = HMMSampler(T_OTHER, E[:, PERM], PI, SequenceLayout()).sample(n, rng)
    return PERM[canon.astype(np.int64)].astype(canon.dtype), canon


def test_oracle_equals_bayes_filter_on_w1_to_w32():
    named, _ = _named_and_canon(11)
    q = oracle_q32(T_OTHER, E, PI, named)
    ref = BayesFilter(T_OTHER, E, PI).run(named[:, :32]).q[:, 32]
    assert q.shape == (11, 3)
    np.testing.assert_allclose(q, ref, rtol=1e-12, atol=1e-14)


def test_oracle_ignores_column_33():
    named, _ = _named_and_canon(9)
    base = oracle_q32(T_FLAT, E, PI, named)
    for shift in (1, 2):
        alt = named.copy()
        alt[:, 32] = (alt[:, 32] + shift) % 3
        np.testing.assert_array_equal(oracle_q32(T_FLAT, E, PI, alt), base)
    np.testing.assert_array_equal(oracle_q32(T_FLAT, E, PI, named[:, :32]), base)


def test_oracle_named_equals_canonical_under_perm():
    named, canon = _named_and_canon(13)
    q_named = oracle_q32(T_OTHER, E, PI, named)
    q_canon = BayesFilter(T_OTHER, E[:, PERM], PI).run(canon[:, :32]).q[:, 32]
    np.testing.assert_allclose(q_named[:, PERM], q_canon, rtol=1e-12, atol=1e-14)
    # A non-identity perm matters: the un-permuted canonical vector is a different object.
    assert not np.allclose(q_named, q_canon)


def test_oracle_guard_and_batch_invariance():
    named, _ = _named_and_canon(7)
    calls = []
    q = oracle_q32(T_FLAT, E, PI, named, guard=lambda *a, **k: calls.append(a), batch=3)
    assert len(calls) == 6  # 3 batches (3 + 3 + 1), before and after each
    np.testing.assert_allclose(q, oracle_q32(T_FLAT, E, PI, named), rtol=1e-12, atol=1e-14)


# ---------------------------------------------------------------- score


def _model_and_inputs(r: int) -> tuple[TransformerLM, torch.Tensor, np.ndarray]:
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SeedTree(7).seed("x5g1t-score-test"))
        model = TransformerLM(TINY_MODEL)
    named, _ = _named_and_canon(r)
    x = torch.from_numpy(SequenceLayout().model_inputs(named, 3))
    return model, x, named


def test_regret_zero_on_own_softmax_and_nonnegative():
    model, x, named = _model_and_inputs(10)
    logp = p32_log_probs(model, x, batch=4)
    assert logp.shape == (10, 3) and logp.dtype == np.float64
    np.testing.assert_allclose(np.exp(logp).sum(axis=1), 1.0, atol=1e-12)
    np.testing.assert_allclose(regret_rows(model, x, np.exp(logp), batch=4), 0.0, atol=1e-10)
    reg = regret_rows(model, x, oracle_q32(T_OTHER, E, PI, named), batch=4)
    assert reg.shape == (10,) and np.all(np.isfinite(reg)) and np.all(reg >= -1e-12)
    assert reg.max() > 0


def test_regret_batch_invariant_and_training_flag_restored():
    model, x, named = _model_and_inputs(9)
    q = oracle_q32(T_FLAT, E, PI, named)
    model.train()
    a = regret_rows(model, x, q, batch=2)
    assert model.training
    model.eval()
    b = regret_rows(model, x, q, batch=512)
    assert not model.training
    np.testing.assert_allclose(a, b, rtol=1e-10, atol=1e-12)


def test_kl_hand_value_and_invalid_q():
    q = np.array([[0.5, 0.5, 0.0]])
    logp = np.log(np.array([[0.25, 0.25, 0.5]]))
    np.testing.assert_allclose(kl_from_log_probs(q, logp), [np.log(2.0)], rtol=1e-12)
    with pytest.raises(StageFailure) as exc:
        kl_from_log_probs(np.array([[1.2, -0.2, 0.0]]), logp)
    assert _code(exc) == ErrorCode.NUMERICAL_FAILURE
    with pytest.raises(StageFailure) as exc:
        kl_from_log_probs(q, np.array([[np.log(0.5), -np.inf, 0.0]]))
    assert _code(exc) == ErrorCode.NUMERICAL_FAILURE


def test_p32_requires_33_inputs():
    model, x, _ = _model_and_inputs(4)
    with pytest.raises((StageFailure, ValueError)):
        p32_log_probs(model, x[:, :32])
