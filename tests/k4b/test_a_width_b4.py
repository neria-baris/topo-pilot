"""K4b author A, TEST_PLAN A12 (v2) and A13 (protocol §7.6, §5.5 item 4, §6 B4-VAL).

A12: k4b_stats.width_diagnostic on synthetic arrays. With C = A u r and D = (1 - A)|r|, the
endpoints are X+- = C +- D; translating both arrays by -C_bar leaves the centred draws unchanged,
so the diagnostic depends on D_bar and the centred draws only (invariance to C_bar), and D_bar
shifts the upper condition up and the lower condition down. A13: k4b_cert.b4_guard
(PASS, HEADROOM, NUMERICAL band; the FRESH_B4_LOW basis status != PASS)."""

from __future__ import annotations

import inspect
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
             "tools/x4_circle_history", "tools/x4_oracle_profile"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import c1_bounds  # noqa: E402
import c1_means  # noqa: E402
import k4b_cert  # noqa: E402
import k4b_stats  # noqa: E402

MODELS = (1729, 2718, 3141)
KEYS = [(j, s) for j in MODELS for s in ("-", "+")]
ALPHA = Fr(5, 300)
NDRAW = 5000
Z = Fr(212, 10 ** 14)


@pytest.fixture(scope="module")
def f_plan():
    return k4b_cert.F_plan(Fr(0))


def ref_width(D_bar, e, F):
    f = float(F)
    per, joint = {}, np.ones(NDRAW, bool)
    for i, j in enumerate(MODELS):
        em, ep = e[:, 2 * i], e[:, 2 * i + 1]
        qa = c1_means.quantile_with_rank(em, ALPHA)[0]
        qb = c1_means.quantile_with_rank(ep, 1 - ALPHA)[0]
        d = float(D_bar[j])
        s = (d + ep + qb + f < 0.01) & (-d + em + qa - f > -0.01)
        per[j] = int(s.sum())
        joint &= s
    return per, int(joint.sum())


def wcounts(res):
    return {j: int(res["per_model"][j]) for j in MODELS}, int(res["joint"])


def endpoint_arrays(seed, n=3072):
    """Synthetic X-+ = C -+ D per model, with A, u.r and |r| drawn at random."""
    rng = np.random.default_rng(seed)
    X, Cbar, Dbar = {}, {}, {}
    for j in MODELS:
        A = rng.random(n) < 0.8
        nr = np.abs(rng.normal(0.0, 0.05, n))
        ur = nr * np.cos(rng.uniform(0.0, 2 * np.pi, n))
        c, d = np.where(A, ur, 0.0), np.where(A, 0.0, nr)
        X[(j, "-")], X[(j, "+")] = c - d, c + d
        Cbar[j], Dbar[j] = float(np.mean(c)), float(np.mean(d))
    return X, Cbar, Dbar


def designed_e():
    """Columns as in the projection tests: fail set range(1000) for every model and side."""
    e = np.empty((NDRAW, 6))
    fail = np.arange(NDRAW) < 1000
    for i in range(3):
        e[:, 2 * i] = np.where(fail, -0.01, 0.001)
        e[:, 2 * i + 1] = np.where(fail, 0.01, -0.001)
    return e


# ---------------------------------------------------------------- width diagnostic (A12)

def test_width_signature_never_takes_C_bar():
    params = list(inspect.signature(k4b_stats.width_diagnostic).parameters)
    assert params == ["D_bar", "e", "keys", "F_plan"]


def test_width_matches_reference(f_plan):
    X, _, Dbar = endpoint_arrays(11)
    e = k4b_stats.centered(X, KEYS, 3072)
    for D in (Dbar, {j: 0.0 for j in MODELS}, {1729: 0.001, 2718: 0.003, 3141: 0.0}):
        assert wcounts(k4b_stats.width_diagnostic(D, e, KEYS, f_plan)) == ref_width(D, e, f_plan)


def test_width_at_zero_equals_registered_exclusion_projection(f_plan):
    X, _, _ = endpoint_arrays(12)
    e = k4b_stats.centered(X, KEYS, 3072)
    w = k4b_stats.width_diagnostic({j: 0.0 for j in MODELS}, e, KEYS, f_plan)
    p = k4b_stats.projection(e, KEYS, f_plan)["exclusion"]
    assert wcounts(w) == ({j: int(p["per_model"][j]) for j in MODELS}, int(p["joint"]))


def test_width_D_shift_on_designed_draws(f_plan):
    """Success draws have e+ + q+ + F = 0.0091 and e- + q- - F = -0.0091, so a shift by
    D_bar = 0.0008 keeps them (0.0099 < 0.01) and D_bar = 0.0012 loses them (0.0103)."""
    e = designed_e()
    res = k4b_stats.width_diagnostic({1729: 0.0008, 2718: 0.0012, 3141: 0.0}, e, KEYS, f_plan)
    assert wcounts(res) == ({1729: 4000, 2718: 0, 3141: 4000}, 0)
    res = k4b_stats.width_diagnostic({j: 0.0008 for j in MODELS}, e, KEYS, f_plan)
    assert wcounts(res) == ({j: 4000 for j in MODELS}, 4000)


def test_width_monotone_in_D_bar(f_plan):
    X, _, _ = endpoint_arrays(13)
    e = k4b_stats.centered(X, KEYS, 3072)
    prev = None
    for d in (0.0, 0.0005, 0.001, 0.002, 0.004, 0.008, 0.02):
        per, joint = wcounts(k4b_stats.width_diagnostic({j: d for j in MODELS}, e, KEYS, f_plan))
        if prev is not None:
            assert all(per[j] <= prev[0][j] for j in MODELS) and joint <= prev[1]
        prev = (per, joint)
    assert prev == ({j: 0 for j in MODELS}, 0)  # D_bar >= 0.01: no exclusion success


def test_width_invariant_to_C_bar(f_plan):
    X, Cbar, Dbar = endpoint_arrays(14)
    for j in MODELS:  # X+- = C +- D, so the means are C_bar -+ D_bar
        assert abs(np.mean(X[(j, "-")]) - (Cbar[j] - Dbar[j])) < 1e-12
        assert abs(np.mean(X[(j, "+")]) - (Cbar[j] + Dbar[j])) < 1e-12
    translated = {(j, s): X[(j, s)] - Cbar[j] for j, s in KEYS}  # means -D_bar, +D_bar
    moved = {(j, s): X[(j, s)] + 0.37 for j, s in KEYS}  # another C_bar
    for j in MODELS:
        assert abs(np.mean(translated[(j, "-")]) + Dbar[j]) < 1e-12
        assert abs(np.mean(translated[(j, "+")]) - Dbar[j]) < 1e-12
    e0 = k4b_stats.centered(X, KEYS, 3072)
    e1 = k4b_stats.centered(translated, KEYS, 3072)
    e2 = k4b_stats.centered(moved, KEYS, 3072)
    assert np.allclose(e0, e1, atol=1e-12, rtol=0) and np.allclose(e0, e2, atol=1e-12, rtol=0)
    r0 = wcounts(k4b_stats.width_diagnostic(Dbar, e0, KEYS, f_plan))
    assert wcounts(k4b_stats.width_diagnostic(Dbar, e1, KEYS, f_plan)) == r0
    assert wcounts(k4b_stats.width_diagnostic(Dbar, e2, KEYS, f_plan)) == r0


# ---------------------------------------------------------------- B4 guard (A13)

def _guard(r4n, Bn, seed, n):
    return k4b_cert.b4_guard(np.asarray(r4n, dtype=np.float64), Bn, Z, seed, n)


def test_b4_guard_pass():
    r4n = np.full(1024, 0.0625)  # dyadic: every tree mean is exactly 0.0625
    Bn = Fr(1, 10 ** 12)
    res = _guard(r4n, Bn, 610102, 1024)
    assert float(res["lower"]) == 0.0625 and int(res["rank"]) == 250
    assert res["status"] == "PASS"
    assert res["B_H"] == k4b_cert.b_num(Bn, 0.0625, 1024)
    assert res["Z_bound"] == Z
    assert abs(float(res["point"]) - 0.0625) < 1e-15


def test_b4_guard_headroom():
    res = _guard(np.full(1024, 0.0078125), Fr(1, 10 ** 12), 610102, 1024)
    assert float(res["lower"]) == 0.0078125
    assert res["status"] == "INCONCLUSIVE/HEADROOM"


def test_b4_guard_numerical_band():
    res = _guard(np.full(1024, 0.01), Fr(1, 10 ** 12), 610102, 1024)
    assert float(res["lower"]) == 0.01  # 1024 * fl(0.01) is exact, so the mean is fl(0.01)
    assert res["status"] == "INCONCLUSIVE/NUMERICAL"
    res = _guard(np.full(1024, 0.0625), Fr(1, 10), 610102, 1024)  # B^H dominates the gap
    assert res["status"] == "INCONCLUSIVE/NUMERICAL"


@pytest.mark.parametrize("seed", [610102, 610104])
def test_b4_guard_matches_reused_kernels(seed):
    rng = np.random.default_rng(250)
    r4n = rng.uniform(0.0, 0.05, 512)
    Bn = Fr(3, 10 ** 13)
    res = _guard(r4n, Bn, seed, 512)
    draws = c1_means.bootstrap_means({"r4n": r4n}, seed)["r4n"]
    lower, k = c1_means.quantile_with_rank(draws, 0.05)
    assert float(res["lower"]) == lower and int(res["rank"]) == k == 250
    B_H = k4b_cert.b_num(Bn, float(np.max(r4n)), 512)
    assert res["B_H"] == B_H
    assert res["status"] == c1_bounds.guard_H5(lower, B_H + Z)
    assert abs(float(res["point"]) - float(np.mean(r4n))) < 1e-12


@pytest.mark.parametrize("value,Bn", [(0.0625, Fr(1, 10 ** 12)), (0.0078125, Fr(1, 10 ** 12)),
                                      (0.01, Fr(1, 10 ** 12)), (0.0625, Fr(1, 10))])
def test_fresh_b4_low_basis(value, Bn):
    """FRESH_B4_LOW (implementation choice 7) is set iff the guard status is not PASS, i.e.
    iff the certified lower bound minus (B^H + Z_bound) does not exceed 0.01."""
    res = _guard(np.full(1024, value), Bn, 610104, 1024)
    gap = Fr(float(res["lower"])) - Fr(1, 100)
    passes = gap > max(res["B_H"] + Z, c1_bounds.FLOOR)
    assert (res["status"] == "PASS") == passes
