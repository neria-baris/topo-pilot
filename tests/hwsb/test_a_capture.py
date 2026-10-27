"""HWSB author A: B5 pilot capture at 80 % planned power (protocol §4 B5, refinement 1; DRB10).

Targets (API.md §6.3): hwsb_gates.c_min, c_min_literal, capture_pass, b5, b5_N; hwsb_config
Z_C, Z_P, RANKS. c_min = (M + F_plan + (z_{1-alpha} + z_{0.80}) SD^U / sqrt(N_C)) / D4hat with
M = 1/100, alpha = 1/60; equality passes. The bootstrap CI is one c1_means.bootstrap_means call
over X_minus_<j> and D4 with seed 620214 (ranks 125 and 4,875 of the ratio draws; rank 125 of
the X- draws). Expected values are computed here from those definitions. Synthetic arrays only.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_oracle_profile", "tools/x4_circle_history", "tools/c1prime_registry",
             "tools/c1prime", "tools/k4b", "tools/hws"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import c1_means  # noqa: E402
import k4b_cert  # noqa: E402
import precision  # noqa: E402

try:
    import hwsb_config as hc  # noqa: E402
    import hwsb_gates as hg  # noqa: E402
except ImportError as _exc:  # the implementation is written in parallel
    hc = hg = None
    MISSING = repr(_exc)
else:
    MISSING = None

M = Fraction(1, 100)
ALPHA = Fraction(1, 60)
A, B = 620201, 620202
MODELS = (A, B)
SEED = 620214
Z_C = NormalDist().inv_cdf(1.0 - float(ALPHA))
Z_P = NormalDist().inv_cdf(0.8)


def need():
    if MISSING:
        pytest.fail("tools/hwsb modules not importable: " + MISSING)


def F_plan():
    return k4b_cert.F_plan(Fraction(1, 10**6))


def sd_arg(values):
    """API-AMBIGUITY: b5's sdU_minus may be keyed by j or by (j, "-") (the ladder's sdU keys);
    the map carries both readings with equal values."""
    out = dict(values)
    out.update({(j, "-"): v for j, v in values.items()})
    return out


def mde_cfg(F, N):
    return {"delta": float(M + F), "alpha": float(ALPHA), "power": 0.80, "projected_N": int(N)}


def b5_ref(X_minus, D4, sdU, N_C, F, models=MODELS, seed=SEED):
    D4hat = float(c1_means.tree_mean(D4))
    draws = c1_means.bootstrap_means({**{f"X_minus_{j}": X_minus[j] for j in models},
                                      "D4": D4}, seed, 5000)
    per = {}
    for j in models:
        mean_x = float(c1_means.tree_mean(X_minus[j]))
        c_hat = mean_x / D4hat
        cmin = precision.mde(sdU[j], mde_cfg(F, N_C)) / D4hat
        ratio = draws[f"X_minus_{j}"] / draws["D4"]
        lo, k_lo = c1_means.quantile_with_rank(ratio, 0.025)
        hi, k_hi = c1_means.quantile_with_rank(ratio, 0.975)
        low125, k125 = c1_means.quantile_with_rank(draws[f"X_minus_{j}"], 0.025)
        assert (k_lo, k_hi, k125) == (125, 4875, 125)
        per[j] = {"mean_X_minus": mean_x, "c_hat": c_hat, "c_min": cmin,
                  "c_min_literal": (float(M + F) + Z_C * float(sdU[j]) / math.sqrt(N_C)) / D4hat,
                  "pass": c_hat >= cmin, "ci95": (lo, hi), "lower_rank125_mean_X_minus": low125}
    return {"D4hat": D4hat, "N_C": N_C, "per_model": per,
            "status": "PASS" if all(p["pass"] for p in per.values()) else "FAIL",
            "positive_below_planning": all(p["lower_rank125_mean_X_minus"] > 0
                                           for p in per.values())}


def assert_b5(res, ref):
    assert res["D4hat"] == ref["D4hat"]
    assert res["N_C"] == ref["N_C"]
    assert res["status"] == ref["status"]
    assert bool(res["positive_below_planning"]) is ref["positive_below_planning"]
    assert set(res["per_model"]) == set(ref["per_model"])
    for j, r in ref["per_model"].items():
        g = res["per_model"][j]
        for key in ("mean_X_minus", "c_hat", "c_min", "lower_rank125_mean_X_minus"):
            assert g[key] == r[key], (j, key)
        assert g["c_min_literal"] == pytest.approx(r["c_min_literal"], rel=1e-15)
        assert tuple(float(v) for v in g["ci95"]) == r["ci95"], j
        assert bool(g["pass"]) is r["pass"], j


@pytest.fixture(scope="module")
def planted():
    rng = np.random.default_rng(616401)
    n = 256
    X = {A: rng.normal(0.03, 0.06, n), B: rng.normal(0.01, 0.06, n)}
    D4 = rng.normal(0.05, 0.02, n)
    return X, D4, {A: 0.09, B: 0.11}


# ------------------------------------------------------------- pure reference checks

def test_reference_z_values_match_contract_report_values():
    assert Z_C == pytest.approx(2.128045234184984, abs=1e-12)
    assert Z_P == pytest.approx(0.8416212335729144, abs=1e-12)
    assert Z_C + Z_P == pytest.approx(2.9696664677578983, abs=1e-12)
    assert c1_means.rank_for(Fraction(1, 40)) == 125 and c1_means.rank_for(0.975) == 4875


def test_reference_ulp_construction_is_exact():
    sd, N, F = 0.09, 3072, F_plan()
    t = precision.mde(sd, mde_cfg(F, N))
    assert float(c1_means.tree_mean(np.full(256, t))) == t
    t_below = math.nextafter(t, -math.inf)
    assert float(c1_means.tree_mean(np.full(256, t_below))) == t_below
    assert t / 0.0625 == 16 * t and t_below / 0.0625 < t / 0.0625


# ------------------------------------------------------------- constants and c_min

def test_constants():
    need()
    assert hc.M == M and hc.ALPHA_C == ALPHA and hc.POWER == Fraction(4, 5)
    assert hc.Z_C == Z_C and hc.Z_P == Z_P
    assert hc.Z_SUM == pytest.approx(Z_C + Z_P, rel=1e-15)
    assert hc.RANKS == {"sd_upper": 4917, "proj_alpha": 84, "ci_lo": 125, "ci_hi": 4875}
    assert hc.SEEDS["capture_ci"] == SEED and hc.C_MIN_FALLBACK_N == 12288


@pytest.mark.parametrize("sd, N, D4hat", [(0.09, 3072, 0.047), (0.2, 6144, 0.031),
                                          (0.05, 12288, 0.12)])
def test_c_min_formula(sd, N, D4hat):
    need()
    F = F_plan()
    got = hg.c_min(sd, N, F, D4hat)
    formula = (float(M + F) + (Z_C + Z_P) * sd / math.sqrt(N)) / D4hat
    assert got == pytest.approx(formula, rel=1e-15)
    assert got == precision.mde(sd, mde_cfg(F, N)) / D4hat


def test_c_min_expected_orientation():
    need()
    # protocol §4 "Expected values" (orientation only): SD^U 0.09, N_C 3,072, D4 0.047:
    # c_min about 0.32, the §10.2 literal form about 0.29
    F = k4b_cert.F_plan(Fraction(0))
    assert hg.c_min(0.09, 3072, F, 0.047) == pytest.approx(0.32, abs=0.01)
    assert hg.c_min_literal(0.09, 3072, F, 0.047) == pytest.approx(0.29, abs=0.01)


def test_c_min_literal_uses_z_one_minus_alpha_only_and_keeps_f_plan():
    need()
    F = F_plan()
    got = hg.c_min_literal(0.09, 3072, F, 0.047)
    assert got == pytest.approx((float(M + F) + Z_C * 0.09 / math.sqrt(3072)) / 0.047,
                                rel=1e-15)
    without_f = (float(M) + Z_C * 0.09 / math.sqrt(3072)) / 0.047
    assert got - without_f == pytest.approx(float(F) / 0.047, rel=1e-9)
    assert got < hg.c_min(0.09, 3072, F, 0.047)


def test_capture_pass_equality_and_one_ulp_below():
    need()
    c = hg.c_min(0.09, 3072, F_plan(), 0.047)
    assert bool(hg.capture_pass(c, c)) is True
    assert not hg.capture_pass(math.nextafter(c, -math.inf), c)
    assert hg.capture_pass(math.nextafter(c, math.inf), c)


# ------------------------------------------------------------- b5

def test_b5_matches_reference(planted):
    need()
    X, D4, sd = planted
    res = hg.b5(X, D4, sd_arg(sd), 3072, F_plan(), MODELS, seed=SEED)
    assert_b5(res, b5_ref(X, D4, sd, 3072, F_plan()))


def test_b5_default_seed_is_620214(planted):
    need()
    X, D4, sd = planted
    a = hg.b5(X, D4, sd_arg(sd), 3072, F_plan(), MODELS)
    b = hg.b5(X, D4, sd_arg(sd), 3072, F_plan(), MODELS, seed=SEED)
    assert a["per_model"][A]["ci95"] == b["per_model"][A]["ci95"]
    other = b5_ref(X, D4, sd, 3072, F_plan(), seed=SEED + 1)
    assert tuple(a["per_model"][A]["ci95"]) != other["per_model"][A]["ci95"]


def test_b5_ulp_boundary_drb10():
    need()
    sd, N, F, n = 0.09, 3072, F_plan(), 256
    t = precision.mde(sd, mde_cfg(F, N))
    X = {A: np.full(n, t), B: np.full(n, math.nextafter(t, -math.inf))}
    D4 = np.full(n, 0.0625)
    res = hg.b5(X, D4, sd_arg({A: sd, B: sd}), N, F, MODELS, seed=SEED)
    assert res["D4hat"] == 0.0625
    pa, pb = res["per_model"][A], res["per_model"][B]
    assert pa["c_hat"] == pa["c_min"] == 16 * t
    assert bool(pa["pass"]) is True
    assert pb["c_min"] == 16 * t
    assert pb["c_hat"] == math.nextafter(16 * t, -math.inf)      # one ulp below c_min
    assert bool(pb["pass"]) is False
    assert res["status"] == "FAIL"
    assert bool(res["positive_below_planning"]) is True
    assert_b5(res, b5_ref(X, D4, {A: sd, B: sd}, N, F))


def test_b5_both_pass_status():
    need()
    rng = np.random.default_rng(616402)
    n = 256
    X = {A: rng.normal(0.04, 0.03, n), B: rng.normal(0.045, 0.03, n)}
    D4 = rng.normal(0.05, 0.01, n)
    sd = {A: 0.05, B: 0.05}
    ref = b5_ref(X, D4, sd, 3072, F_plan())
    assert ref["status"] == "PASS"
    res = hg.b5(X, D4, sd_arg(sd), 3072, F_plan(), MODELS)
    assert_b5(res, ref)


def test_b5_positive_below_planning_needs_every_model():
    need()
    rng = np.random.default_rng(616403)
    n = 256
    X = {A: rng.normal(0.004, 0.01, n), B: rng.normal(-0.02, 0.01, n)}
    D4 = rng.normal(0.05, 0.01, n)
    sd = {A: 0.09, B: 0.09}
    ref = b5_ref(X, D4, sd, 3072, F_plan())
    assert ref["status"] == "FAIL"
    assert ref["per_model"][A]["lower_rank125_mean_X_minus"] > 0
    assert ref["per_model"][B]["lower_rank125_mean_X_minus"] < 0
    res = hg.b5(X, D4, sd_arg(sd), 3072, F_plan(), MODELS)
    assert_b5(res, ref)
    assert bool(res["positive_below_planning"]) is False
    single = hg.b5({A: X[A]}, D4, sd_arg({A: 0.09}), 3072, F_plan(), (A,))
    assert bool(single["positive_below_planning"]) is True


@pytest.mark.parametrize("value", [0.0, -0.01])
def test_b5_nonpositive_d4hat_is_numerical_failure(planted, value):
    need()
    X, _, sd = planted
    D4 = np.full(256, value)
    with pytest.raises(hc.HwsbStop) as ei:
        hg.b5(X, D4, sd_arg(sd), 3072, F_plan(), MODELS)
    assert ei.value.status == "FAIL_TECHNICAL/NUMERICAL"


def test_b5_nonfinite_d4hat_is_numerical_failure(planted):
    need()
    X, D4, sd = planted
    bad = D4.copy()
    bad[7] = np.inf
    with pytest.raises(hc.HwsbStop) as ei:
        hg.b5(X, bad, sd_arg(sd), 3072, F_plan(), MODELS)
    assert ei.value.status == "FAIL_TECHNICAL/NUMERICAL"


def test_b5_fallback_n_enters_c_min(planted):
    need()
    X, D4, sd = planted
    N_C = hg.b5_N({"status": "INCONCLUSIVE/UNDERPOWERED", "N": None, "k": None})
    assert N_C == 12288
    res = hg.b5(X, D4, sd_arg(sd), N_C, F_plan(), MODELS)
    assert res["N_C"] == 12288
    D4hat = float(c1_means.tree_mean(D4))
    for j in MODELS:
        assert res["per_model"][j]["c_min"] == \
            precision.mde(sd[j], mde_cfg(F_plan(), 12288)) / D4hat
    assert_b5(res, b5_ref(X, D4, sd, 12288, F_plan()))
