"""K4b author A, TEST_PLAN A7, A9 (protocol §5.4, §7.1, §7.2).

A7: registered ranks 84, 125, 250, 4,875, 4,917 (k4b_config.RANKS, c1_means.rank_for,
k4b_stats.bounds). A9: the precision ladder on synthetic arrays: k4b_stats.centered (mean-shift
invariance), projection (per-model and joint thresholds 4,000 of 5,000), mde_ok, ladder
(PASS at 3,072, PASS at 6,144, INCONCLUSIVE/UNDERPOWERED). Synthetic arrays only."""

from __future__ import annotations

import math
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

import c1_means  # noqa: E402
import k4b_cert  # noqa: E402
import k4b_config  # noqa: E402
import k4b_stats  # noqa: E402
import precision  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

MODELS = (1729, 2718, 3141)
KEYS = [(j, s) for j in MODELS for s in ("-", "+")]
ALPHA = Fr(5, 300)
NDRAW = 5000


def leaves(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from leaves(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from leaves(v)
    elif isinstance(x, np.ndarray):
        yield from (float(v) for v in x.ravel())
    else:
        yield x


def numbers(x):
    return {float(v) for v in leaves(x)
            if isinstance(v, (int, float, Fr, np.integer, np.floating)) and not isinstance(v, bool)}


def val(x):
    return float(x[0]) if isinstance(x, (tuple, list)) else float(x)


@pytest.fixture(scope="module")
def f_plan():
    return k4b_cert.F_plan(Fr(0))


# ---------------------------------------------------------------- ranks (A7)

def test_rank_constants():
    assert k4b_config.RANKS == {"alpha": 84, "one_minus_alpha": 4917, "b4_lower": 250,
                                "central_lo": 125, "central_hi": 4875}
    assert k4b_config.DRAWS == NDRAW
    assert k4b_config.ALPHA == ALPHA == c1_means.P_THIRD
    assert c1_means.rank_for(c1_means.P_THIRD) == 84
    assert c1_means.rank_for(1 - c1_means.P_THIRD) == 4917
    assert c1_means.rank_for(0.05) == 250
    assert c1_means.rank_for(0.025) == 125
    assert c1_means.rank_for(0.975) == 4875
    assert math.ceil(Fr(NDRAW) * ALPHA) == 84 and math.ceil(Fr(NDRAW) * (1 - ALPHA)) == 4917


def test_bounds_ranks_on_distinct_draws():
    rng = np.random.default_rng(84)
    dm = rng.permutation(NDRAW).astype(np.float64)
    dp = rng.permutation(NDRAW).astype(np.float64) + 10000.0
    res = k4b_stats.bounds(dm, dp)
    assert val(res["L"]) == 83.0  # the 84th smallest of 0..4999
    assert val(res["U"]) == 14916.0  # the 4,917th smallest of 10000..14999
    got = numbers(res)
    assert {83.0, 14916.0, 124.0, 4874.0, 10124.0, 14874.0} <= got


def test_bounds_with_ties():
    d = np.full(NDRAW, 0.5)
    res = k4b_stats.bounds(d, d + 0.25)
    assert val(res["L"]) == 0.5 and val(res["U"]) == 0.75


def test_bounds_rank_check_failure_is_numerical():
    bad = np.full(NDRAW, np.nan)
    with pytest.raises(C1GateFailure) as exc:
        k4b_stats.bounds(bad, np.arange(NDRAW, dtype=np.float64))
    assert exc.value.status == "FAIL_TECHNICAL/NUMERICAL"


# ---------------------------------------------------------------- projection (A9)

def designed_e(fail_minus, fail_plus):
    """'-' column: -0.01 on the fail set (>= 84 draws, so q_alpha = -0.01), else 0.001.
    '+' column: +0.01 on its fail set (>= 84 draws, so q_{1-alpha} = 0.01), else -0.001.
    SUPPORT succeeds off fail_minus; EXCLUSION succeeds off fail_minus | fail_plus."""
    e = np.empty((NDRAW, 6))
    b = np.arange(NDRAW)
    for i, j in enumerate(MODELS):
        e[:, 2 * i] = np.where(np.isin(b, list(fail_minus[j])), -0.01, 0.001)
        e[:, 2 * i + 1] = np.where(np.isin(b, list(fail_plus[j])), 0.01, -0.001)
    return e


def ref_projection(e, F):
    f = float(F)
    out = {}
    for name in ("support", "exclusion"):
        out[name] = {"per_model": {}, "joint": None}
    js, jx = np.ones(NDRAW, bool), np.ones(NDRAW, bool)
    for i, j in enumerate(MODELS):
        em, ep = e[:, 2 * i], e[:, 2 * i + 1]
        qa = c1_means.quantile_with_rank(em, ALPHA)[0]
        qb = c1_means.quantile_with_rank(ep, 1 - ALPHA)[0]
        s = 0.02 + em + qa - f > 0.01
        x = (ep + qb + f < 0.01) & (em + qa - f > -0.01)
        out["support"]["per_model"][j] = int(s.sum())
        out["exclusion"]["per_model"][j] = int(x.sum())
        js &= s
        jx &= x
    out["support"]["joint"], out["exclusion"]["joint"] = int(js.sum()), int(jx.sum())
    return out


def counts(res):
    return {name: ({j: int(res[name]["per_model"][j]) for j in MODELS}, int(res[name]["joint"]))
            for name in ("support", "exclusion")}


def test_projection_exact_threshold_passes(f_plan):
    F = {j: set(range(1000)) for j in MODELS}
    res = k4b_stats.projection(designed_e(F, F), KEYS, f_plan)
    want = ({j: 4000 for j in MODELS}, 4000)
    assert counts(res) == {"support": want, "exclusion": want}
    assert bool(res["ok"])


def test_projection_joint_one_below_fails(f_plan):
    F = {j: set(range(1000)) for j in MODELS}
    F[2718] = set(range(999)) | {1000}
    res = k4b_stats.projection(designed_e(F, F), KEYS, f_plan)
    c = counts(res)
    assert c["support"] == ({j: 4000 for j in MODELS}, 3999)
    assert c["exclusion"] == ({j: 4000 for j in MODELS}, 3999)
    assert not res["ok"]


def test_projection_exclusion_per_model_one_below_fails(f_plan):
    F = {j: set(range(1000)) for j in MODELS}
    H = dict(F)
    H[3141] = set(range(1001))
    res = k4b_stats.projection(designed_e(F, H), KEYS, f_plan)
    c = counts(res)
    assert c["support"] == ({j: 4000 for j in MODELS}, 4000)
    assert c["exclusion"][0] == {1729: 4000, 2718: 4000, 3141: 3999}
    assert c["exclusion"][1] == 3999
    assert not res["ok"]


def test_projection_support_per_model_one_below_fails(f_plan):
    F = {j: set(range(1000)) for j in MODELS}
    F[1729] = set(range(1001))
    res = k4b_stats.projection(designed_e(F, F), KEYS, f_plan)
    assert counts(res)["support"][0][1729] == 3999
    assert not res["ok"]


def _random_X(seed, shift=None, n=3072):
    rng = np.random.default_rng(seed)
    base = {k: rng.normal(0.0, 0.1, n) for k in KEYS}
    if shift is None:
        return base
    return {k: base[k] + shift[k] for k in KEYS}


def test_centered_is_precision_centered_draws():
    X = _random_X(1)
    e = k4b_stats.centered(X, KEYS, 3072)
    assert e.shape == (NDRAW, 6)
    ref = precision.centered_draws(X, KEYS, 610105, NDRAW, 3072)
    assert np.array_equal(e, ref)


def test_projection_matches_reference_and_is_mean_shift_invariant(f_plan):
    shift = {k: c for k, c in zip(KEYS, (0.3, -0.2, 0.05, 1.5, -0.75, 0.011))}
    e0 = k4b_stats.centered(_random_X(2), KEYS, 3072)
    e1 = k4b_stats.centered(_random_X(2, shift), KEYS, 3072)
    assert np.allclose(e0, e1, atol=1e-12, rtol=0)
    r0 = k4b_stats.projection(e0, KEYS, f_plan)
    r1 = k4b_stats.projection(e1, KEYS, f_plan)
    want = ref_projection(e0, f_plan)
    assert counts(r0) == counts(want)
    assert counts(r1) == counts(r0)
    assert bool(r0["ok"]) == bool(r1["ok"])


# ---------------------------------------------------------------- mde_ok (A9)

def test_mde_ok_boundary(f_plan):
    cfg = {"delta": float(Fr(1, 100) + f_plan), "alpha": float(ALPHA), "power": 0.80,
           "projected_N": 3072}
    assert precision.mde(0.1846, cfg) <= 0.02 < precision.mde(0.1850, cfg)
    assert k4b_stats.mde_ok({k: 0.1846 for k in KEYS}, 3072, f_plan)
    assert not k4b_stats.mde_ok({k: 0.1850 for k in KEYS}, 3072, f_plan)
    one_bad = {k: 0.1 for k in KEYS}
    one_bad[(3141, "+")] = 0.1850
    assert not k4b_stats.mde_ok(one_bad, 3072, f_plan)
    assert k4b_stats.mde_ok({k: 0.1850 for k in KEYS}, 6144, f_plan)


# ---------------------------------------------------------------- ladder (A9)

def _alternating(c, n=3072):
    return np.where(np.arange(n) % 2 == 0, c, -c).astype(np.float64)


def _ladder_inputs(c, r):
    X = {j: _alternating(c) for j in MODELS}
    return X, {j: X[j].copy() for j in MODELS}, {j: np.full(3072, r) for j in MODELS}


def test_ladder_passes_at_3072(f_plan):
    Xm, Xp, r4n = _ladder_inputs(0.01, 0.02)
    res = k4b_stats.ladder(Xm, Xp, r4n, f_plan, {j: 0.0 for j in MODELS})
    assert res["status"] == "PASS"
    assert res["N"] == 3072 and res["k"] == 1
    assert res["candidates"][3072]["mde_ok"]
    assert res["candidates"][3072]["projection"]["ok"]


def test_ladder_passes_at_6144(f_plan):
    """SD 0.2: MDE fails at 3,072 (0.2082 > 0.02) and passes at 6,144 (0.0177)."""
    Xm, Xp, r4n = _ladder_inputs(0.2, 0.25)
    res = k4b_stats.ladder(Xm, Xp, r4n, f_plan, {j: 0.0 for j in MODELS})
    assert res["status"] == "PASS"
    assert res["N"] == 6144 and res["k"] == 2
    assert not res["candidates"][3072]["mde_ok"]
    cand = res["candidates"][6144]
    assert cand["mde_ok"] and cand["projection"]["ok"]
    X = {}
    for j in MODELS:
        X[(j, "-")], X[(j, "+")] = Xm[j], Xp[j]
    e = k4b_stats.centered(X, KEYS, 6144)  # same seed 610105 for every candidate
    assert counts(cand["projection"]) == counts(k4b_stats.projection(e, KEYS, f_plan))
    sd, _ = precision.sd_b4_draws(Xm, r4n, list(MODELS), 610101, NDRAW, 3072)
    for i, j in enumerate(MODELS):
        q = c1_means.quantile_with_rank(sd[:, i], 1 - ALPHA)[0]
        assert res["sdU"][(j, "-")] == q and res["sdU"][(j, "+")] == q
        assert 0.199 < q < 0.201


def test_ladder_underpowered(f_plan):
    Xm, Xp, r4n = _ladder_inputs(1.0, 1.0)
    res = k4b_stats.ladder(Xm, Xp, r4n, f_plan, {j: 0.0 for j in MODELS})
    assert res["status"] == "INCONCLUSIVE/UNDERPOWERED"
    assert res["N"] is None and res["k"] is None
    for N in k4b_config.LADDER:
        assert not res["candidates"][N]["mde_ok"]
    assert tuple(k4b_config.LADDER) == (3072, 6144, 12288)
