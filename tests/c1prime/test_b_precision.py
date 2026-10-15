"""Independent tests (author B, job 0026), TEST_PLAN B-2 part 2: ladder, k rule, H5 and V3.

Protocol §12.4 (P1 ladder; `precision.py` called as specified), §16 row 20 (fresh fraction),
§3.5 and §15.3.11 (H) for H5, §11 and §15.3.11 (V) for V3. Written from the protocol and the
four contract documents only; no tools/c1prime source was read and nothing was executed by the
author. The ladder reference calls the unchanged K4 `precision.py` exactly as §12.4 prescribes.

Ambiguities recorded: the key layout of the `ladder`, `h5` and `v3` result dicts is not fixed by
API.md (tests read `N_test`/`status` and per-model values flexibly); `v3` is given `B_V3` as a
dict keyed by model seed.
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
import oracle_profile  # noqa: E402
import precision  # noqa: E402

pytestmark = pytest.mark.analysis

MODELS = [1729, 2718, 3141]
LADDER = (4096, 8192, 16384)


def _status(res) -> str:
    return res if isinstance(res, str) else res["status"]


def _tree_mean(values) -> float:
    level = [float(x) for x in values]
    n = len(level)
    while len(level) > 1:
        nxt = [level[k] + level[k + 1] for k in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0] / n


# --- ladder (§12.4) -------------------------------------------------------------------------------


def _reference_ladder(Z, G):
    n = G.shape[0]
    X = {m: Z[m] for m in MODELS}
    sd, _ = precision.sd_b4_draws(X=X, r4n={m: G for m in MODELS}, models=MODELS,
                                  seed=520501, draws=5000, size=n)
    out = {}
    for N in LADDER:
        e = precision.centered_draws(X=X, models=MODELS, seed=520502, draws=5000, size=N)
        cfg = {"alpha": 0.05 / 3, "power": 0.80, "delta": 0.0,
               "alternative": (0.20 - 0.10) * float(np.mean(G)), "projected_N": N}
        out[N] = precision.precision_summary(sd, e, MODELS, cfg)
    passing = [N for N in LADDER if out[N]["status"] == "PASS"]
    return out, (passing[0] if passing else None)


def _unit_sd_rows(seed, n=400):
    rng = np.random.default_rng(seed)
    out = {}
    for m in MODELS:
        z = rng.standard_normal(n)
        out[m] = (z - z.mean()) / z.std(ddof=1)
    return out


@pytest.fixture(scope="module")
def middle_case():
    # sd ~ 1 and alternative 0.1 * 0.4 = 0.04: mde_upper(4096) ~ 0.050 > 0.04 >= mde_upper(8192)
    Z, G = _unit_sd_rows(21), np.full(400, 0.4)
    return Z, G, _reference_ladder(Z, G)


def _summary_for(res, N):
    for container in (res.get("summaries"), res.get("per_N"), res.get("by_N"), res):
        if isinstance(container, dict):
            for key in (N, str(N)):
                if isinstance(container.get(key), dict) and "models" in container[key]:
                    return container[key]
    return None


def _underpowered(res) -> bool:
    return "INCONCLUSIVE/UNDERPOWERED" in (res.get("status"), res.get("N_test"))


def test_ladder_picks_the_smallest_passing_N(middle_case):
    Z, G, (ref, n_test) = middle_case
    assert n_test == 8192 and ref[4096]["status"] != "PASS"  # fixture precondition
    res = c1_endpoint.ladder(Z, G, MODELS)
    assert int(res["N_test"]) == 8192
    assert not _underpowered(res)
    for N in LADDER:
        got = _summary_for(res, N)
        if got is None:
            continue
        for m in MODELS:
            mine = got["models"].get(m, got["models"].get(str(m)))
            assert mine["sd_upper"] == ref[N]["models"][m]["sd_upper"]
            assert mine["q_alpha"] == ref[N]["models"][m]["q_alpha"]


def test_ladder_underpowered_when_no_N_passes():
    Z, G = _unit_sd_rows(22), np.full(400, 0.001)
    ref, n_test = _reference_ladder(Z, G)
    assert n_test is None
    res = c1_endpoint.ladder(Z, G, MODELS)
    assert _underpowered(res)


@pytest.mark.parametrize("N,f_val,k", [
    (4096, 0.92, 2), (8192, 0.92, 3), (16384, 0.92, 5), (16384, 1.0, 5), (4096, 1.0, 2),
    (8192, 0.95, 3), (16384, 0.90, 5), (8192, 0.99, 3), (4096, 0.90, 2),
])
def test_k_blocks(N, f_val, k):
    assert int(c1_endpoint.k_blocks(N, f_val)) == k
    exact = Fraction(N) / ((Fraction(f_val) - Fraction(1, 50)) * 4096)
    assert k - 1 < exact <= k  # the ceiling, far from an integer in every case


def test_k_blocks_never_exceeds_five_for_admissible_fractions():
    for f_val in np.linspace(0.90, 1.0, 41):
        for N in LADDER:
            assert 1 <= int(c1_endpoint.k_blocks(N, float(f_val))) <= 5


@pytest.mark.parametrize("f_test,f_val,ok", [
    (0.93, 0.92, True), (0.91, 0.92, True), (0.92, 0.92, True), (0.95, 0.92, False),
    (0.89, 0.92, False), (0.97, 0.96, True), (0.93, 0.96, False),
])
def test_fresh_fraction_rule(f_test, f_val, ok):
    assert bool(c1_endpoint.fresh_fraction_ok(f_test, f_val)) is ok


# --- H5 (§3.5, §15.3.11 H) ------------------------------------------------------------------------


def _h5_lower(G, seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    n = G.shape[0]
    means = np.array([_tree_mean(G[rng.integers(0, n, size=n)]) for _ in range(5000)])
    return float(oracle_profile.percentile_interval(means, [0.05])[0])


def test_h5_pass_headroom_and_guard_band():
    G = 0.5 + 0.01 * np.random.default_rng(31).random(30)
    lower = _h5_lower(G, 520505)
    gamma = Fraction(lower) - Fraction(1, 100)
    assert _status(c1_endpoint.h5(G, Fraction(1, 10**12), 520505)) == "PASS"
    assert _status(c1_endpoint.h5(G, gamma, 520505)) == "INCONCLUSIVE/NUMERICAL"
    tight = gamma - Fraction(1, 10**30)
    res = c1_endpoint.h5(G, tight, 520505)
    assert _status(res) == "PASS"
    if isinstance(res, dict) and "lower" in res:
        assert float(res["lower"]) == lower
    low = 0.001 * (1.0 + np.random.default_rng(32).random(30))
    assert _status(c1_endpoint.h5(low, Fraction(1, 10**12), 520506)) == "INCONCLUSIVE/HEADROOM"


# --- V3 (§11, §15.3.11 V) -------------------------------------------------------------------------


def _v3_lowers(Zf, seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    n = Zf[MODELS[0]].shape[0]
    means = {m: np.empty(5000) for m in MODELS}
    for d in range(5000):
        idx = rng.integers(0, n, size=n)
        for m in MODELS:
            means[m][d] = _tree_mean(Zf[m][idx])
    return {m: np.sort(means[m])[83] for m in MODELS}


def _zf(seed, centres):
    rng = np.random.default_rng(seed)
    return {m: c + 0.05 * rng.normal(size=30) for m, c in zip(MODELS, centres)}


def test_v3_pass_and_model_headroom():
    small = {m: Fraction(1, 10**12) for m in MODELS}
    assert _status(c1_endpoint.v3(_zf(41, (0.4, 0.3, 0.5)), small, 520504)) == "PASS"
    res = c1_endpoint.v3(_zf(42, (0.4, -0.3, 0.5)), small, 520507)
    assert _status(res) == "INCONCLUSIVE/MODEL_HEADROOM"


def test_v3_guard_band_is_numerical_and_uses_rank_84_of_shared_draws():
    Zf = _zf(43, (0.4, 0.3, 0.5))
    lowers = _v3_lowers(Zf, 520504)
    band = {m: Fraction(1, 10**12) for m in MODELS}
    band[2718] = Fraction(float(lowers[2718]))  # Gamma_j == g_j exactly: not a PASS
    assert _status(c1_endpoint.v3(Zf, band, 520504)) == "INCONCLUSIVE/NUMERICAL"
    band[2718] = Fraction(float(lowers[2718])) - Fraction(1, 10**30)
    assert _status(c1_endpoint.v3(Zf, band, 520504)) == "PASS"
