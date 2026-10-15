"""Independent tests (author B, job 0026), TEST_PLAN B-2 part 1 (§12.2-§13, §15.3.2 C7, §3.5).

Decision rule, balanced-tree mean (Theorem 5), shared bootstrap index streams, the H5 wrapper's
equality with `oracle_profile.bootstrap_profile`, inverted_cdf ranks and the run-time rank check.
Written from the protocol and the four contract documents only; no tools/c1prime source was
read and nothing was executed by the author. References: a pure-Python balanced tree, identically
seeded Generator(PCG64(seed)) streams, the unchanged job-0014 `oracle_profile`, and Fractions.

Ambiguity (API.md §6, `rank_for`): "ceil(draws*p) in exact rationals" would give 251 for the float
p = 0.05 (5000*Fraction(0.05) exceeds 250 by 1.4e-14). The protocol (§15.3.2 C7, §23.4 item 18)
fixes the rank numpy actually uses, 250; these tests require 250, 84 and 4917.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_endpoint  # noqa: E402
import c1_means  # noqa: E402
import c1_records  # noqa: E402
import oracle_profile  # noqa: E402

pytestmark = pytest.mark.analysis

MODELS = (1729, 2718, 3141)
U = Fraction(1, 2**53)
ZETA = Fraction(1, 2**800)


def _gamma(n) -> Fraction:
    return n * U / (1 - n * U)


def _tree_mean(values) -> float:
    level = [float(x) for x in values]
    n = len(level)
    while len(level) > 1:
        nxt = [level[k] + level[k + 1] for k in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0] / n


def _scalar(x) -> float:
    arr = np.asarray(x, dtype=np.float64).reshape(-1)
    assert arr.size == 1
    return float(arr[0])


def _model_value(res, model, key):
    for container in (res, res.get("models"), res.get("per_model")):
        if not isinstance(container, dict):
            continue
        for mk in (model, str(model)):
            sub = container.get(mk)
            if isinstance(sub, dict) and key in sub:
                return sub[key]
        sub = container.get(key)
        if isinstance(sub, dict):
            for mk in (model, str(model)):
                if mk in sub:
                    return sub[mk]
        if isinstance(sub, (list, tuple)) and len(sub) == len(MODELS):
            return sub[MODELS.index(model)]
    raise AssertionError(f"no {key!r} for model {model} in {sorted(map(str, res))}")


# --- decision rule (§12.2, §13) -----------------------------------------------------------------


@pytest.mark.parametrize("meanY,meanG,c,expected", [
    (0.3, 1.0, 0.1, True), (0.05, 1.0, 0.1, False), (0.1, 1.0, 0.1, False),
    (0.021, 0.2, 0.1, True), (-0.4, 0.5, 0.1, False), (0.8, 2.5, 0.3, True),
])
def test_ratio_to_mean_reduction(meanY, meanG, c, expected):
    assert bool(c1_endpoint.ratio_reduction(meanY, meanG, c)) is expected
    exact = Fraction(meanY) / Fraction(meanG) > Fraction(c)  # theta > c
    if (meanY, meanG, c) != (0.1, 1.0, 0.1):  # float c*G is exact only in the equality case
        assert exact is expected


@pytest.mark.parametrize("L,U_,expected", [
    (0.1, 0.2, "PASS_j"), (-0.2, -0.1, "FAIL_j"), (0.0, 0.1, "INC_j"), (-0.1, 0.0, "INC_j"),
    (-0.1, 0.1, "INC_j"), (0.0, 0.0, "INC_j"), (5e-324, 1.0, "PASS_j"), (-1.0, -5e-324, "FAIL_j"),
])
def test_per_model_status_boundaries(L, U_, expected):
    assert c1_endpoint.per_model_status(L, U_) == expected


@pytest.mark.parametrize("statuses,expected", [
    (["PASS_j"] * 3, "PASS"), (["FAIL_j"] * 3, "FAIL"), (["PASS_j", "PASS_j", "INC_j"], "MIXED"),
    (["FAIL_j", "FAIL_j", "PASS_j"], "MIXED"), (["INC_j"] * 3, "MIXED"),
])
def test_overall_rule(statuses, expected):
    assert c1_endpoint.overall(statuses) == expected


# --- tree mean (C7, Theorem 5) -------------------------------------------------------------------


@pytest.mark.parametrize("n", [1, 2, 3, 5, 8, 37, 100])
def test_tree_mean_is_the_balanced_pairwise_tree(n):
    rng = np.random.default_rng(100 + n)
    X = rng.normal(size=(4, n)) * 10.0 ** rng.integers(-8, 9, size=(4, n))
    got = np.asarray(c1_means.tree_mean(X), dtype=np.float64)
    assert got.shape == (4,)
    for i in range(4):
        assert got[i] == _tree_mean(X[i])
    assert _scalar(c1_means.tree_mean(X[0])) == _tree_mean(X[0])


def test_tree_mean_order_differs_from_left_to_right():
    # (2**53 + 0) + (1 + 1) = 2**53 + 2 by the tree; left to right it would be 2**53 (two ties).
    x = np.array([2.0**53, 0.0, 1.0, 1.0])
    assert _scalar(c1_means.tree_mean(x)) == (2.0**53 + 2.0) / 4


def test_tree_mean_within_theorem5_with_cancellation_and_subnormals():
    tiny = 2.0**-1074
    cases = [
        [1e16, 3.0, -1e16, 5.0, 1.0, -7.5, 2.0**-30, 1e-300, 4.0],
        [tiny] * 7 + [-tiny] * 2,
        [2.0**-1022, -(2.0**-1023), tiny, 3 * tiny, 1.0, -1.0],
        list(np.random.default_rng(11).normal(size=1000) * 1e3) + [1e12, -1e12],
    ]
    for vals in cases:
        n = len(vals)
        got = _scalar(c1_means.tree_mean(np.asarray(vals, dtype=np.float64)))
        assert got == _tree_mean(vals)
        exact = sum((Fraction(v) for v in vals), Fraction(0)) / n
        bound = _gamma((n - 1).bit_length() + 1) * max(abs(Fraction(v)) for v in vals) + ZETA
        assert abs(Fraction(got) - exact) <= bound


# --- bootstrap streams (C7, §3.5, §11, §12.3) ---------------------------------------------------


def test_bootstrap_means_share_one_integers_call_per_draw():
    rng0 = np.random.default_rng(12)
    n, draws, seed = 23, 64, 777
    arrays = {"a": rng0.normal(size=n), "b": rng0.normal(size=n) * 1e-3}
    arrays["a2"] = 2.0 * arrays["a"]
    got = c1_means.bootstrap_means(arrays, seed, draws)
    rng = np.random.Generator(np.random.PCG64(seed))
    for d in range(draws):
        idx = rng.integers(0, n, size=n)
        for name, x in arrays.items():
            assert got[name][d] == _tree_mean(x[idx])
    assert np.array_equal(np.asarray(got["a2"]), 2.0 * np.asarray(got["a"]))
    assert np.asarray(c1_means.bootstrap_means({"x": arrays["b"]}, 5)["x"]).shape == (5000,)


def test_h5_wrapper_index_stream_equals_bootstrap_profile():
    x = np.random.default_rng(13).integers(0, 50, size=40).astype(np.float64)
    rng1 = np.random.Generator(np.random.PCG64(520505))
    rng2 = np.random.Generator(np.random.PCG64(520505))
    mine = np.asarray(c1_means.c1_bootstrap_means(x, rng1, 300), dtype=np.float64)
    prof = oracle_profile.bootstrap_profile({1: x}, {1: x}, (1,), rng2, 300)["B"][:, 0]
    assert np.array_equal(mine, prof)  # integer data: exact sums, so the kernels agree bitwise
    assert np.array_equal(rng1.integers(0, 10**9, size=4), rng2.integers(0, 10**9, size=4))


def test_h5_wrapper_uses_the_tree_kernel_on_real_valued_data():
    x = np.random.default_rng(14).normal(size=29) * 1e-2
    got = np.asarray(c1_means.c1_bootstrap_means(x, np.random.Generator(np.random.PCG64(9)), 50))
    rng = np.random.Generator(np.random.PCG64(9))
    for d in range(50):
        assert got[d] == _tree_mean(x[rng.integers(0, 29, size=29)])


# --- quantiles and ranks (C7) -------------------------------------------------------------------


@pytest.mark.parametrize("p,rank", [(0.05, 250), (0.05 / 3, 84), (1 - 0.05 / 3, 4917)])
def test_rank_for_protocol_ranks(p, rank):
    assert c1_means.rank_for(p) == rank
    assert c1_means.rank_for(p, 5000) == rank
    ladder = np.arange(1, 5001, dtype=np.float64)  # numpy's own one-based rank, as a check
    assert np.quantile(ladder, p, method="inverted_cdf") == rank


@pytest.mark.parametrize("p,rank", [(0.05, 250), (0.05 / 3, 84), (1 - 0.05 / 3, 4917)])
def test_quantile_with_rank_returns_the_input_element_at_the_rank(p, rank):
    values = np.random.default_rng(15).normal(size=5000)
    v, k = c1_means.quantile_with_rank(values, p)
    assert int(k) == rank
    assert float(v) == np.sort(values)[rank - 1]
    assert np.any(values == float(v))


def test_rank_check_accepts_order_statistics_and_rejects_others():
    vals = np.array([3.0, 2.0, 1.0, 2.0, 2.0])
    for k in (2, 3, 4):
        assert c1_means.rank_check(vals, 2.0, k)
    assert not c1_means.rank_check(vals, 2.0, 1)
    assert not c1_means.rank_check(vals, 2.0, 5)
    assert c1_means.rank_check(vals, 3.0, 5)
    assert not c1_means.rank_check(vals, 2.5, 5)
    assert c1_means.rank_check(vals, 1.0, 1)


def test_quantile_with_rank_rejects_a_wrong_order_statistic(monkeypatch):
    values = np.random.default_rng(16).normal(size=5000)

    def shifted(a, q, *args, **kwargs):  # returns the (k+1)-th order statistic instead
        s = np.sort(np.asarray(a, dtype=np.float64).ravel())
        qs = np.atleast_1d(np.asarray(q, dtype=np.float64))
        out = np.array([s[min(s.size - 1, int(np.ceil(s.size * p)))] for p in qs])
        return out[0] if np.ndim(q) == 0 else out

    monkeypatch.setattr(np, "quantile", shifted)
    with pytest.raises(c1_records.C1GateFailure) as info:
        c1_means.quantile_with_rank(values, 0.05)
    assert info.value.status == "FAIL_TECHNICAL/NUMERICAL"


# --- endpoint bounds (§12.3) ----------------------------------------------------------------------


def test_endpoint_bounds_use_shared_draws_and_ranks_84_and_4917():
    rng0 = np.random.default_rng(17)
    n = 25
    Z = {m: rng0.normal(size=n) * 0.1 + 0.02 * k for k, m in enumerate(MODELS)}
    res = c1_endpoint.endpoint_bounds(Z, seed=520503, draws=5000)
    rng = np.random.Generator(np.random.PCG64(520503))
    means = {m: np.empty(5000) for m in MODELS}
    for d in range(5000):
        idx = rng.integers(0, n, size=n)
        for m in MODELS:
            means[m][d] = _tree_mean(Z[m][idx])
    for m in MODELS:
        s = np.sort(means[m])
        assert float(_model_value(res, m, "L")) == s[83]
        assert float(_model_value(res, m, "U")) == s[4916]
