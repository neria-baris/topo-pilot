"""Independent tests (author B) for precision.py: TEST_PLAN items B5 and B9 (spec v2.2).

Split from test_scores_precision.py for the 400-line limit. Written from API.md, CONTRACT.json
and TEST_PLAN.md only; no production code was read. Expected values come from manual re-runs of
the documented resampling loops with identically seeded Generator(PCG64(seed)), from
statistics.NormalDist, and from hand-placed inverted_cdf order statistics.

Ambiguity (API.md says only "per model: ..."): the per-model records are looked up literally as
summary["per_model"][m], summary["models"][m] or summary[m] (int or str key, or a list in model
order); the verdict key is "decision" (else "status").
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import errors  # noqa: E402
import precision  # noqa: E402

pytestmark = pytest.mark.analysis

_CONTRACT = REPO_ROOT / "tools" / "x4_circle_history" / "CONTRACT.json"
PREC = json.loads(_CONTRACT.read_text(encoding="utf-8"))["precision"]
CFG = {key: PREC[key] for key in ("delta", "alternative", "power", "alpha", "projected_N")}
MODELS = tuple(PREC["model_order"])


def _record(summary: dict, model: int) -> dict:
    for container in (summary.get("per_model"), summary.get("models"), summary):
        if isinstance(container, dict):
            for key in (model, str(model)):
                if isinstance(container.get(key), dict):
                    return container[key]
        if (isinstance(container, (list, tuple)) and len(container) == len(MODELS)
                and isinstance(container[MODELS.index(model)], dict)):
            return container[MODELS.index(model)]
    raise AssertionError(f"no per-model record for {model}: keys {sorted(map(str, summary))}")


def _verdict(summary: dict) -> str:
    for key in ("decision", "status"):
        if key in summary:
            return summary[key]
    raise AssertionError(f"no decision in {sorted(map(str, summary))}")


def _mde(sd: float) -> float:
    nd = NormalDist()
    z = nd.inv_cdf(1 - CFG["alpha"]) + nd.inv_cdf(CFG["power"])
    return CFG["delta"] + z * sd / math.sqrt(CFG["projected_N"])


def test_cfg_comes_from_contract_values() -> None:
    assert (CFG["delta"], CFG["alternative"], CFG["power"], CFG["projected_N"]) == (
        0.01, 0.02, 0.8, 3072)
    assert abs(CFG["alpha"] - 0.05 / 3) < 1e-17
    assert MODELS == (1729, 2718, 3141)


# ---- resampling loops ------------------------------------------------------------------------
N_EVAL = 13
BASE = np.array([((7 * i) % 13) * 0.1 - 0.4 for i in range(N_EVAL)])   # 13 distinct values
X_DICT = {MODELS[0]: BASE, MODELS[1]: 3.0 * BASE + 0.5, MODELS[2]: np.cos(np.arange(N_EVAL) * 1.3)}
R4N = {MODELS[0]: np.abs(BASE) + 0.01, MODELS[1]: np.abs(BASE) + 1.01,
       MODELS[2]: np.linspace(0.0, 0.2, N_EVAL)}


def _manual_sd_b4(seed: int, draws: int, size: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.Generator(np.random.PCG64(seed))
    sd = np.empty((draws, len(MODELS)))
    b4 = np.empty_like(sd)
    for b in range(draws):
        idx = rng.integers(0, N_EVAL, size=size)          # ONE call per draw, shared
        for k, m in enumerate(MODELS):
            sd[b, k] = np.std(X_DICT[m][idx], ddof=1)
            b4[b, k] = np.mean(R4N[m][idx])
    return sd, b4


def _manual_centered(seed: int, draws: int, size: int) -> np.ndarray:
    rng = np.random.Generator(np.random.PCG64(seed))
    e = np.empty((draws, len(MODELS)))
    for b in range(draws):
        idx = rng.integers(0, N_EVAL, size=size)
        for k, m in enumerate(MODELS):
            e[b, k] = np.mean(X_DICT[m][idx]) - np.mean(X_DICT[m])
    return e


@pytest.mark.parametrize("size", [9, N_EVAL])
def test_sd_b4_draws_reproduce_manual_loop_with_shared_idx(size: int) -> None:
    seed, draws = PREC["sd_seed"], 40
    sd, b4 = precision.sd_b4_draws(X_DICT, R4N, MODELS, seed, draws, size)
    assert np.shape(sd) == (draws, 3) and np.shape(b4) == (draws, 3)
    want_sd, want_b4 = _manual_sd_b4(seed, draws, size)
    np.testing.assert_allclose(sd, want_sd, rtol=1e-12, atol=1e-15)
    np.testing.assert_allclose(b4, want_b4, rtol=1e-12, atol=1e-15)
    # sharing proof: model 2 is an affine copy of model 1, so equal idx gives exact relations
    np.testing.assert_allclose(sd[:, 1], 3.0 * sd[:, 0], rtol=1e-12)
    np.testing.assert_allclose(b4[:, 1], b4[:, 0] + 1.0, rtol=0, atol=1e-12)


@pytest.mark.parametrize("size", [7, N_EVAL])
def test_centered_draws_reproduce_manual_loop_with_shared_idx(size: int) -> None:
    seed, draws = PREC["centered_seed"], 40
    e = precision.centered_draws(X_DICT, MODELS, seed, draws, size)
    assert np.shape(e) == (draws, 3)
    np.testing.assert_allclose(e, _manual_centered(seed, draws, size), rtol=1e-12, atol=1e-15)
    np.testing.assert_allclose(e[:, 1], 3.0 * e[:, 0], rtol=1e-10, atol=1e-14)


def test_mde_formula_via_normal_dist() -> None:
    assert precision.mde(0.0, CFG) == CFG["delta"]
    for sd in (0.05, 0.2, 1.3):
        assert precision.mde(sd, CFG) == pytest.approx(_mde(sd), rel=1e-14, abs=0)
    z = NormalDist().inv_cdf(1 - CFG["alpha"]) + NormalDist().inv_cdf(CFG["power"])
    assert abs(z - (2.1280 + 0.8416)) < 2e-3                    # sanity of the constants


# ---- precision_summary -----------------------------------------------------------------------
def test_precision_summary_inverted_cdf_quantiles_power_and_mde_fields() -> None:
    draws = 30
    rng = np.random.Generator(np.random.PCG64(5))
    sd = np.column_stack([0.15 + 0.002 * rng.permutation(draws) for _ in MODELS])
    # e on a grid offset by 3e-4 so that e_b + q_alpha never sits at delta - alternative
    e = np.column_stack([0.001 * (rng.permutation(draws) - 15.0) + 0.0003 for _ in MODELS])
    out = precision.precision_summary(sd, e, MODELS, CFG)
    for k, m in enumerate(MODELS):
        rec = _record(out, m)
        col, ecol = np.sort(sd[:, k]), np.sort(e[:, k])
        # 30 * alpha = 0.5 -> 1st order statistic; 30 * (1 - alpha) = 29.5 -> 30th
        assert rec["sd_lower"] == col[0] == np.quantile(sd[:, k], CFG["alpha"],
                                                        method="inverted_cdf")
        assert rec["sd_upper"] == col[29] == np.quantile(sd[:, k], 1 - CFG["alpha"],
                                                         method="inverted_cdf")
        assert rec["q_alpha"] == ecol[0]
        assert rec["mde_lower"] == pytest.approx(_mde(col[0]), rel=1e-14, abs=0)
        assert rec["mde_upper"] == pytest.approx(_mde(col[29]), rel=1e-14, abs=0)
        manual = np.mean(CFG["alternative"] + e[:, k] + ecol[0] > CFG["delta"])
        assert manual == pytest.approx(10 / 30)                 # hand count: 10 of 30 draws
        assert rec["power"] == pytest.approx(manual, abs=1e-15)
    assert _verdict(out) == "INCONCLUSIVE"
    assert "criterion_met" in out and not out["criterion_met"]


# power exactly .80 on 10 draws: q_alpha = min = -.006; .02 - .006 - .006 = .008 fails (2 rows)
E_GOOD = np.column_stack([[0.0, 0.0, -0.006, 0.0, 0.0, 0.0, -0.006, 0.0, 0.0, 0.0]] * 3)


def _mde_upper_at(sd_value: float) -> float:
    out = precision.precision_summary(np.full((10, 3), sd_value), E_GOOD, MODELS, CFG)
    return float(_record(out, MODELS[0])["mde_upper"])


@pytest.fixture(scope="module")
def boundary_sd() -> tuple[float, float]:
    """The float sd whose mde_upper is EXACTLY .02 in production arithmetic, and the next float
    sd over it. Monotone rounding makes the step at most one ulp of .02, so the search ends."""
    alt = CFG["alternative"]
    z = NormalDist().inv_cdf(1 - CFG["alpha"]) + NormalDist().inv_cdf(CFG["power"])
    sd = (alt - CFG["delta"]) * math.sqrt(CFG["projected_N"]) / z
    for _ in range(200):
        value = _mde_upper_at(sd)
        if value == alt:
            break
        sd = math.nextafter(sd, math.inf if value < alt else -math.inf)
    else:
        pytest.fail("no float sd gives mde_upper == .02 exactly")
    over = sd
    for _ in range(200):
        over = math.nextafter(over, math.inf)
        if _mde_upper_at(over) > alt:
            break
    else:
        pytest.fail("mde_upper does not increase above .02")
    assert abs(_mde(sd) - alt) < 1e-17                          # it IS the written formula
    return sd, over


def test_precision_pass_at_exact_equalities(boundary_sd) -> None:
    sd_eq, _ = boundary_sd
    out = precision.precision_summary(np.full((10, 3), sd_eq), E_GOOD, MODELS, CFG)
    for m in MODELS:
        rec = _record(out, m)
        assert rec["mde_upper"] == 0.02 and rec["power"] == 0.8
    assert _verdict(out) == "PASS"
    assert out.get("criterion_met", True)


def test_precision_just_over_mde_or_under_power_is_inconclusive(boundary_sd) -> None:
    sd_eq, sd_over = boundary_sd
    sd = np.full((10, 3), sd_eq)
    sd[:, 1] = sd_over
    out = precision.precision_summary(sd, E_GOOD, MODELS, CFG)
    assert _verdict(out) == "INCONCLUSIVE"
    assert "criterion_met" in out and not out["criterion_met"]
    assert _record(out, MODELS[1])["mde_upper"] > 0.02
    assert _record(out, MODELS[0])["mde_upper"] == 0.02         # every model still reported
    e = E_GOOD.copy()
    e[1, 2] = -0.006                                            # 3 of 10 fail: power .7
    out = precision.precision_summary(np.full((10, 3), sd_eq), e, MODELS, CFG)
    assert _verdict(out) == "INCONCLUSIVE"
    assert not out["criterion_met"]
    assert _record(out, MODELS[2])["power"] == pytest.approx(0.7, abs=1e-15)
    assert _record(out, MODELS[2])["mde_upper"] == 0.02


def test_precision_summary_nonfinite_raises_invalid() -> None:
    sd = np.full((10, 3), 0.1)
    bad_sd = sd.copy()
    bad_sd[3, 1] = np.nan
    with pytest.raises(errors.Invalid):
        precision.precision_summary(bad_sd, E_GOOD, MODELS, CFG)
    bad_e = E_GOOD.copy()
    bad_e[0, 2] = np.inf
    with pytest.raises(errors.Invalid):
        precision.precision_summary(sd, bad_e, MODELS, CFG)


# ---- b4_summary --------------------------------------------------------------------------------
def _b4_column(second: float) -> np.ndarray:
    """30 draws whose 2nd order statistic (the inverted_cdf 0.05 quantile) is ``second``."""
    col = np.array([0.005, second] + [0.02 + 0.001 * i for i in range(28)])
    return col[np.random.Generator(np.random.PCG64(11)).permutation(30)]


def _b4(draws: np.ndarray) -> dict:
    point = {m: float(np.mean(draws[:, k])) for k, m in enumerate(MODELS)}
    return precision.b4_summary(draws, point, MODELS, CFG)


def test_b4_lower_equal_to_delta_is_not_pass() -> None:
    draws = np.column_stack([_b4_column(0.0125), _b4_column(0.015), _b4_column(0.01)])
    out = _b4(draws)
    assert _verdict(out) == "INCONCLUSIVE"
    assert "criterion_met" in out and not out["criterion_met"]
    for k, m in enumerate(MODELS):
        rec, col = _record(out, m), np.sort(draws[:, k])
        # 30 * .05 = 1.5 -> 2nd order statistic; 30 * .95 = 28.5 -> 29th
        assert rec["lower"] == col[1] == np.quantile(draws[:, k], 0.05, method="inverted_cdf")
        assert rec["upper"] == col[28] == np.quantile(draws[:, k], 0.95, method="inverted_cdf")
    assert _record(out, MODELS[2])["lower"] == CFG["delta"]


def test_b4_lower_just_above_delta_passes() -> None:
    above = math.nextafter(0.01, 1.0)
    out = _b4(np.column_stack([_b4_column(0.0125), _b4_column(0.015), _b4_column(above)]))
    assert _verdict(out) == "PASS"
    assert out.get("criterion_met", True)
    assert _record(out, MODELS[2])["lower"] == above


# ---- B9 (spec v2.2): fail-closed shapes and keys ------------------------------------------------
GOOD_SD = np.full((10, 3), 0.1)


@pytest.mark.parametrize("models, sd, e", [
    ((), np.zeros((10, 0)), np.zeros((10, 0))),                          # empty models
    ((1729, 1729, 2718), GOOD_SD, E_GOOD),                               # duplicate models
    (MODELS, GOOD_SD[:, :2], E_GOOD),                                    # sd has 2 columns
    (MODELS, GOOD_SD, E_GOOD[:, :2]),                                    # e has 2 columns
    (MODELS, GOOD_SD[:, 0], E_GOOD),                                     # sd not 2-D
    (MODELS, GOOD_SD, E_GOOD.reshape(10, 3, 1)),                         # e 3-D
    (MODELS, np.zeros((0, 3)), E_GOOD),                                  # no sd rows
    (MODELS, GOOD_SD, np.zeros((0, 3))),                                 # no e rows
])
def test_precision_summary_fail_closed(models, sd, e) -> None:
    with pytest.raises(errors.Invalid):
        precision.precision_summary(sd, e, models, CFG)


def test_b4_summary_fail_closed() -> None:
    draws = np.column_stack([_b4_column(0.02)] * 3)
    point = {m: 0.03 for m in MODELS}
    bad_cases = [
        (np.zeros((30, 0)), {}, ()),
        (draws, {1729: 0.03, 2718: 0.03}, (1729, 1729, 2718)),
        (draws[:, :2], point, MODELS),
        (draws[:, 0], point, MODELS),
        (np.zeros((0, 3)), point, MODELS),
        (np.where(np.arange(90).reshape(30, 3) == 4, np.nan, draws), point, MODELS),
        (draws, {1729: 0.03, 2718: 0.03}, MODELS),                       # missing point key
        (draws, dict(point, **{"9999": 0.03}), MODELS),                  # extra point key
        (draws, {1729: 0.03, 2718: 0.03, 9999: 0.03}, MODELS),           # different key
    ]
    for b4_draws, b4_point, models in bad_cases:
        with pytest.raises(errors.Invalid):
            precision.b4_summary(b4_draws, b4_point, models, CFG)
    assert _verdict(precision.b4_summary(draws, point, MODELS, CFG)) == "PASS"
