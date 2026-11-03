"""Author A (job 0223): the response estimand theta and A_full (protocol 2.5; API_U2 1.2, 4.7).

Synthetic readout bases only: A_full = 1/2 d^T (z1 - z2) with z = closed_logits(y) (C2 Lemma R),
the named/canonical mapping of d, the response arrays, theta-hat = mean A / mean G, Lemma P1
(suffix-only readout gives A = 0 bitwise) and Lemma D2 (oracle readout gives A = G)."""

from __future__ import annotations  # noqa: I001

import importlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,F401
import hwsu_oracle as uo  # noqa: E402
import c1_means  # noqa: E402
import c1_oracle  # noqa: E402
import c2_model  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

MASTERS = (620301, 620302, 620303)


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


def _basis(rng, V=36, k=127):
    M = rng.standard_normal((V, k))
    return {"M": M, "WUbeta": rng.standard_normal(V)}


def _probs(rng, n, V=36):
    x = rng.random((n, V)) + 0.05
    return x / x.sum(axis=1, keepdims=True)


def test_a_full_equals_half_dot_of_closed_logit_difference():
    um2 = mod("hwsu_model")
    rng = np.random.default_rng(1)
    b, n = _basis(rng), 50
    y1, y2 = rng.standard_normal((n, 127)), rng.standard_normal((n, 127))
    d = _probs(rng, n) - _probs(rng, n)
    z1, z2 = c2_model.closed_logits(y1, b), c2_model.closed_logits(y2, b)
    want = 0.5 * np.sum(d * (z1 - z2), axis=1)
    got = np.asarray(um2.a_full(d, b["M"], y1, y2), dtype=np.float64)
    assert got.shape == (n,)
    assert np.all(np.abs(got - want) <= 1e-12 * np.maximum(1.0, np.abs(want)))


def test_a_full_uses_named_d_and_canonical_d_is_wrong():
    um2 = mod("hwsu_model")
    rng = np.random.default_rng(2)
    b, n = _basis(rng), 40
    perm = rng.permutation(36)
    assert not np.array_equal(perm, np.arange(36))
    y1, y2 = rng.standard_normal((n, 127)), rng.standard_normal((n, 127))
    d_canon = _probs(rng, n) - _probs(rng, n)
    d_named = c1_oracle.named_from_canonical(d_canon, perm)
    dz = c2_model.closed_logits(y1, b) - c2_model.closed_logits(y2, b)
    want = 0.5 * np.sum(d_named * dz, axis=1)
    right = np.asarray(um2.a_full(d_named, b["M"], y1, y2))
    wrong = np.asarray(um2.a_full(d_canon, b["M"], y1, y2))
    assert np.allclose(right, want, rtol=1e-12, atol=1e-12)
    assert not np.allclose(wrong, want, rtol=1e-6, atol=1e-9)


def test_response_arrays_exact():
    um2 = mod("hwsu_model")
    rng = np.random.default_rng(3)
    A, G = rng.standard_normal(30), rng.random(30)
    r = um2.response_arrays(A, G)
    assert set(r) == {"ZR010", "ZR030", "AF"}
    assert np.array_equal(r["ZR010"], A - 0.1 * G)
    assert np.array_equal(r["ZR030"], A - 0.3 * G)
    assert np.array_equal(r["AF"], A)
    assert all(np.asarray(v).dtype == np.float64 for v in r.values())


def test_response_arrays_constants_are_contract_lines():
    from fractions import Fraction

    um2 = mod("hwsu_model")
    A, G = np.zeros(4), np.ones(4)
    r = um2.response_arrays(A, G)
    assert np.array_equal(r["ZR010"], np.full(4, -float(Fraction(1, 10))))
    assert np.array_equal(r["ZR030"], np.full(4, -float(Fraction(3, 10))))


def test_suffix_only_readout_gives_zero_bitwise():
    """Lemma P1: a readout that is a function of w29..w32 gives y1 == y2 on suffix-matched pairs."""
    um2 = mod("hwsu_model")
    rng = np.random.default_rng(4)
    b, n = _basis(rng), 64
    suffix = rng.integers(0, 36, size=(n, 4))
    W = rng.standard_normal((4 * 36, 127))

    def readout(suf):
        onehot = np.zeros((len(suf), 4 * 36))
        for k in range(4):
            onehot[np.arange(len(suf)), 36 * k + suf[:, k]] = 1.0
        return onehot @ W

    y1, y2 = readout(suffix), readout(suffix.copy())
    d = _probs(rng, n) - _probs(rng, n)
    A = np.asarray(um2.a_full(d, b["M"], y1, y2))
    assert np.array_equal(A, np.zeros(n))
    r = um2.response_arrays(A, rng.random(n))
    assert np.array_equal(r["AF"], np.zeros(n))


def test_oracle_readout_gives_A_equal_G_via_helmert():
    """Lemma D2: with M = N (Helmert), y = log q N, A_full equals the phase-1 readout_A and G."""
    um2 = mod("hwsu_model")
    rng = np.random.default_rng(5)
    n = 80
    q1, q2 = _probs(rng, n), _probs(rng, n)
    N = uo.helmert(36)
    l1, l2 = np.log(q1), np.log(q2)
    d = q1 - q2
    A = np.asarray(um2.a_full(d, N, l1 @ N, l2 @ N))
    ref = np.asarray(uo.readout_A(d, l1, l2, N))
    G = 0.5 * np.sum((q1 - q2) * (l1 - l2), axis=1)
    assert np.allclose(A, ref, rtol=1e-12, atol=1e-14)
    assert np.allclose(A, G, rtol=1e-10, atol=1e-13)


def test_theta_hat_is_ratio_of_tree_means(tmp_path):
    """theta_j in SEALED_VALIDATION.json = tree_mean(A_j) / tree_mean(G) (API_U2 4.7)."""
    ug = mod("hwsu_gates")
    rng = np.random.default_rng(6)
    G = rng.random(256) + 0.1
    arrays = {"G": G}
    theta = {620301: 0.5, 620302: 0.2, 620303: -0.05}
    for j, t in theta.items():
        A = t * G + 0.01 * rng.standard_normal(256)
        arrays[f"A_{j}"] = A
        arrays[f"ZR010_{j}"] = A - 0.1 * G
        arrays[f"ZR030_{j}"] = A - 0.3 * G
    ug.write_sealed_u(tmp_path, arrays)
    body = json.loads((tmp_path / "SEALED_VALIDATION.json").read_text(encoding="utf-8"))
    mG = float(c1_means.tree_mean(G))
    for j in theta:
        mA = float(c1_means.tree_mean(arrays[f"A_{j}"]))
        assert body["means"][f"A_{j}"] == repr(mA)
        got = float(body["means"][f"theta_{j}"])
        assert got == pytest.approx(mA / mG, rel=1e-15)
