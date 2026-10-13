"""Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
before reading the implementation.

Lineage (paired generators, named tokens, sequence ids, calibration ObservationSet) and the
oracle gate quantities (permutation equivalence, w33 isolation, bootstrap batching);
protocol x5g1-feas-v2 §4-§5, API §3.
"""

from __future__ import annotations

import hashlib

import numpy as np
import pytest

from topo_pilot.contracts import (
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
    canonical_json,
)
from topo_pilot.contracts.testing import tiny_hmm
from topo_pilot.dataset import HMMSampler
from topo_pilot.experiment.x5g1_lineage import (
    ARMS,
    N_POOL,
    NAMESPACE_CODE,
    STREAM,
    calibration_obs,
    paired_generators,
    sample_named,
    sequence_ids,
)
from topo_pilot.experiment.x5g1_oracle import bootstrap_means, gate_quantities

pytestmark = pytest.mark.experiment

PERM = np.array([2, 0, 4, 1, 3])
INV = np.argsort(PERM)
E5 = np.array([[0.50, 0.20, 0.10, 0.15, 0.05],
               [0.05, 0.50, 0.20, 0.10, 0.15],
               [0.15, 0.05, 0.50, 0.20, 0.10],
               [0.10, 0.15, 0.05, 0.20, 0.50]])
T1, _, PI = tiny_hmm()
T2 = 0.6 * np.eye(4) + 0.4 * np.full((4, 4), 0.25)       # symmetric, uniform pi, != T1
KEYS = ("kl_last", "kl_stationary", "kl_two")


def _named(n=300, seed=5, T=T1):
    return sample_named(T, E5, PERM, PI, np.random.default_rng(seed), n=n)


def _code(arm: str) -> int:
    blob = canonical_json(["cylinder", "overlap", "1.25", "x5g1-v1:calibration:" + arm])
    return int.from_bytes(hashlib.sha256(blob.encode()).digest()[:4], "big") >> 1


# ---------------------------------------------------------------- constants and generators


def test_frozen_constants():
    assert STREAM == ("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")
    assert N_POOL == 16_384 and NAMESPACE_CODE == 8 and tuple(ARMS) == ("a0", "a020")


def test_paired_generators_distinct_objects_identical_draws():
    g1, g2 = paired_generators()
    assert g1 is not g2 and g1.bit_generator is not g2.bit_generator
    ref = SeedTree(0).generator(*STREAM).random(8)
    a, b = g1.random(8), g2.random(8)
    np.testing.assert_array_equal(a, b)
    np.testing.assert_array_equal(a, ref)


def test_paired_arms_share_first_symbol_and_misuse_is_detected():
    n = 400
    g1, g2 = paired_generators()
    a = sample_named(T1, E5, PERM, PI, g1, n=n)
    b = sample_named(T2, E5, PERM, PI, g2, n=n)
    np.testing.assert_array_equal(a[:, 0], b[:, 0])                  # named first token
    np.testing.assert_array_equal(INV[a[:, 0]], INV[b[:, 0]])        # canonical first symbol
    assert not np.array_equal(a, b)                                  # kernels do differ
    # negative control: one advanced generator reused for the second arm
    (g,) = paired_generators()[:1]
    c = sample_named(T1, E5, PERM, PI, g, n=n)
    d = sample_named(T2, E5, PERM, PI, g, n=n)
    assert not np.array_equal(c[:, 0], d[:, 0])


# ---------------------------------------------------------------- sample_named


def test_sample_named_is_perm_of_canonical():
    n = 250
    named = sample_named(T1, E5, PERM, PI, np.random.default_rng(9), n=n)
    # identity naming on the canonical E[:, perm] with the same seed gives canon itself
    canon = sample_named(T1, E5[:, PERM], np.arange(5), PI, np.random.default_rng(9), n=n)
    np.testing.assert_array_equal(named, PERM[canon])
    np.testing.assert_array_equal(INV[named], canon)                  # exact round trip
    ref, _ = HMMSampler(T1, E5[:, PERM], PI, SequenceLayout()).sample(
        n, np.random.default_rng(9))
    np.testing.assert_array_equal(canon, ref)


def test_sample_named_shape_dtype_and_no_states():
    out = _named(n=64)
    assert isinstance(out, np.ndarray)
    assert out.shape == (64, 33) and out.dtype == np.uint8
    assert out.max() < 5 and out.min() >= 0


def test_sample_named_one_call_deterministic():
    np.testing.assert_array_equal(_named(n=100, seed=1), _named(n=100, seed=1))


# ---------------------------------------------------------------- sequence ids and pools


def test_sequence_ids_namespace_and_disjoint():
    ids = {arm: sequence_ids(arm, 1000) for arm in ARMS}
    for arm, a in ids.items():
        assert a.dtype == np.int64 and a.shape == (1000,)
        assert np.all((a >> 32) == _code(arm))
        assert np.all(((a >> 28) & 0xF) == 8)
        np.testing.assert_array_equal(a & ((1 << 28) - 1), np.arange(1000))
    assert np.intersect1d(ids["a0"], ids["a020"]).size == 0
    assert sequence_ids("a0").shape == (N_POOL,)


def test_sequence_ids_unknown_arm():
    with pytest.raises(StageFailure) as ei:
        sequence_ids("a010", 10)
    assert ei.value.code == ErrorCode.INVALID_CONFIG


def test_calibration_obs_dev_v36():
    named = _named(n=50)
    seq = sequence_ids("a020", 50)
    obs = calibration_obs(named, seq)
    assert isinstance(obs, ObservationSet)
    assert obs.split == "dev" and obs.V == 36
    np.testing.assert_array_equal(obs.tokens, named)
    np.testing.assert_array_equal(obs.sequence_id, seq)
    obs.validate()


# ---------------------------------------------------------------- oracle reference


def _ref_row(T, E, pi, w):
    """Independent forward filter for one 33-token row (reads w[:32] only)."""
    pe = pi @ E
    b = pi.copy()
    q_pos = [pe]
    for t in range(32):
        b = b * E[:, w[t]]
        b = b / b.sum()
        q_pos.append(b @ T @ E)
        b = b @ T if t < 31 else b
    q_c = q_pos[-1]
    r = pi * E[:, w[31]]
    r = r / r.sum()
    b2 = pi * E[:, w[30]]
    b2 = (b2 / b2.sum()) @ T * E[:, w[31]]
    b2 = b2 / b2.sum()

    def kl(p, q):
        return float(np.sum(p * np.log(p / q)))
    ent = [float(-np.sum(q * np.log(q))) for q in q_pos]
    return kl(q_c, r @ T @ E), kl(q_c, pe), kl(q_c, b2 @ T @ E), ent


def test_gate_quantities_match_reference_filter():
    named = _named(n=40)
    out = gate_quantities(T1, E5, PI, named)
    assert bool(out["valid"])
    ref = [_ref_row(T1, E5, PI, row) for row in named]
    for k, key in enumerate(KEYS):
        np.testing.assert_allclose(out[key], [r[k] for r in ref], atol=1e-12)
    pe = np.asarray(out["position_entropy"])
    assert pe.shape == (33,)
    np.testing.assert_allclose(pe, np.mean([r[3] for r in ref], axis=0), atol=1e-12)


def test_gate_quantities_lawful_nonnegative():
    out = gate_quantities(T2, E5, PI, _named(n=200, T=T2))
    assert bool(out["valid"])
    for key in KEYS:
        v = np.asarray(out[key])
        assert v.shape == (200,) and np.all(np.isfinite(v)) and v.min() >= -1e-12


def test_gate_quantities_permutation_equivalence():
    named = _named(n=300)
    canon = INV[named].astype(named.dtype)
    a = gate_quantities(T1, E5, PI, named)
    b = gate_quantities(T1, E5[:, PERM], PI, canon)
    for key in KEYS + ("position_entropy",):
        np.testing.assert_allclose(a[key], b[key], atol=1e-12, rtol=0)
    assert bool(a["valid"]) and bool(b["valid"])


def test_w33_isolation():
    named = _named(n=300)
    other = named.copy()
    other[:, 32] = (other[:, 32] + 1 + np.arange(300) % 4) % 5
    assert not np.array_equal(other[:, 32], named[:, 32])
    a = gate_quantities(T1, E5, PI, named)
    b = gate_quantities(T1, E5, PI, other)
    assert set(a) == set(b)
    for key in a:
        np.testing.assert_array_equal(np.asarray(a[key]), np.asarray(b[key]))


def test_gate_quantities_batching_is_rowwise():
    named = _named(n=4100, seed=2)
    full = gate_quantities(T1, E5, PI, named)
    head = gate_quantities(T1, E5, PI, named[:4096])
    tail = gate_quantities(T1, E5, PI, named[4096:])
    for key in KEYS:
        np.testing.assert_allclose(full[key], np.concatenate([head[key], tail[key]]),
                                   atol=1e-12, rtol=0)


def test_impossible_history_sets_invalid_without_raising():
    E0 = np.concatenate([E5, np.zeros((4, 1))], axis=1)   # symbol 5 is never emitted
    tokens = _named(n=20)
    tokens[3, 10] = 5
    out = gate_quantities(T1, E0, PI, tokens)
    assert not bool(out["valid"])


# ---------------------------------------------------------------- bootstrap


def test_bootstrap_matches_definition_and_is_deterministic():
    values = np.random.default_rng(4).random(64)
    a = bootstrap_means(values, np.random.default_rng(7))
    b = bootstrap_means(values, np.random.default_rng(7))
    assert a.shape == (2000,)
    np.testing.assert_array_equal(a, b)
    rng = np.random.default_rng(7)
    ref = [values[rng.integers(0, 64, 64)].mean() for _ in range(2000)]
    np.testing.assert_allclose(a, ref, rtol=1e-12, atol=0)


def test_bootstrap_guard_before_and_after_each_batch():
    values = np.arange(32, dtype=np.float64)
    rng = np.random.default_rng(1)
    start = rng.bit_generator.state["state"]["state"]
    seen: list[int] = []

    def guard(*_args):
        seen.append(rng.bit_generator.state["state"]["state"])

    bootstrap_means(values, rng, guard=guard)
    assert len(seen) >= 5
    distinct = [s for k, s in enumerate(seen) if k == 0 or s != seen[k - 1]]
    assert len(distinct) == 5                          # 4 batches of 500 draws
    assert seen[0] == start                            # guard before the first batch
    assert seen[-1] == rng.bit_generator.state["state"]["state"]   # and after the last


class _Halt(RuntimeError):
    pass


def test_bootstrap_guard_exception_propagates():
    calls = []

    def guard(*_args):
        calls.append(1)
        if len(calls) == 3:
            raise _Halt("stop")

    with pytest.raises(_Halt):
        bootstrap_means(np.ones(10), np.random.default_rng(0), guard=guard)
    assert len(calls) == 3
