"""HWSB author A: the B6 pilot ladder (protocol §4 B6, refinement 2; DRB9).

Targets (API.md §6.2): hwsb_gates.ladder_pilot, b5_N. Reference: k4b_stats.ladder (K4b keys and
seeds, bitwise), and an independent re-implementation here of the §4 B6 rule from precision.*
and c1_means.* for the two stage-B keys and seeds 620212/620213: SD^U = rank 4,917 of the
sd_b4_draws columns (one seed for both sides), mde_ok, four-column centred draws, SUPPORT and
EXCLUSION per-model and two-model joint counts (>= 4,000 of 5,000), first qualifying N.
Synthetic arrays only (three planted cases: N = 3,072, first N = 6,144, none).
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

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
import k4b_config  # noqa: E402
import k4b_stats  # noqa: E402
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
LADDER = (3072, 6144, 12288)
STAGE_B = (620201, 620202)
SEEDS_B = (620212, 620213)
SEEDS_K4B = (610101, 610105)
N_ROWS = 3072
CASES = {"n3072": (0.10, 3072), "n6144": (0.20, 6144), "none": (0.60, None)}


def need():
    if MISSING:
        pytest.fail("tools/hwsb modules not importable: " + MISSING)


def F_plan():
    return k4b_cert.F_plan(Fraction(1, 10**6))


def planted(models, sd, seed):
    """Models share one base series (so the joint counts track the per-model ones)."""
    rng = np.random.default_rng(seed)
    base = rng.normal(0.03, sd, N_ROWS)
    Xm, Xp, r4n, D = {}, {}, {}, {}
    for j in models:
        Xm[j] = base + 0.002 * rng.normal(size=N_ROWS)
        Xp[j] = Xm[j] + np.abs(rng.normal(0.0, 0.004, N_ROWS))
        r4n[j] = np.abs(Xp[j]) + 0.01
        D[j] = 0.004
    return Xm, Xp, r4n, D


def ladder_ref(Xm, Xp, r4n, F, models, seeds, ladder=LADDER):
    """Independent §4 B6 rule (no k4b_stats code), width diagnostic omitted."""
    models = list(models)
    n = len(Xm[models[0]])
    sdU = {}
    for side, X in (("-", Xm), ("+", Xp)):
        sd, _ = precision.sd_b4_draws({j: X[j] for j in models}, {j: r4n[j] for j in models},
                                      models, seeds[0], 5000, n)
        for i, j in enumerate(models):
            v, k = c1_means.quantile_with_rank(sd[:, i], 1 - ALPHA)
            assert k == 4917
            sdU[(j, side)] = v
    keys = [(j, s) for j in models for s in ("-", "+")]
    cols = {(j, "-"): Xm[j] for j in models} | {(j, "+"): Xp[j] for j in models}
    f = float(F)
    cands, chosen = {}, None
    for N in ladder:
        cfg = {"delta": float(M + F), "alpha": float(ALPHA), "power": 0.80, "projected_N": N}
        mde_ok = all(precision.mde(v, cfg) <= 0.02 for v in sdU.values())
        e = precision.centered_draws(cols, keys, seeds[1], 5000, N)
        sup, exc = {}, {}
        js, jx = np.ones(5000, bool), np.ones(5000, bool)
        for j in models:
            em, ep = e[:, keys.index((j, "-"))], e[:, keys.index((j, "+"))]
            qa, ka = c1_means.quantile_with_rank(em, ALPHA)
            qb, kb = c1_means.quantile_with_rank(ep, 1 - ALPHA)
            assert (ka, kb) == (84, 4917)
            s = 0.02 + em + qa - f > 0.01
            x = (ep + qb + f < 0.01) & (em + qa - f > -0.01)
            sup[j], exc[j] = int(s.sum()), int(x.sum())
            js &= s
            jx &= x
        ok = all(min(min(d.values()), jnt) >= 4000
                 for d, jnt in ((sup, int(js.sum())), (exc, int(jx.sum()))))
        cands[N] = {"mde_ok": mde_ok, "support": sup, "exclusion": exc,
                    "joint": (int(js.sum()), int(jx.sum())), "ok": ok}
        if mde_ok and ok:
            chosen = N
            break
    return {"N": chosen, "sdU": sdU, "candidates": cands}


@pytest.fixture(scope="module")
def k4b_cases():
    out = {}
    for i, (name, (sd, _)) in enumerate(CASES.items()):
        args = planted(k4b_config.MODELS, sd, 616300 + i)
        out[name] = (args, k4b_stats.ladder(args[0], args[1], args[2], F_plan(), args[3]))
    return out


@pytest.fixture(scope="module")
def stage_b_cases():
    out = {}
    for i, (name, (sd, _)) in enumerate(CASES.items()):
        args = planted(STAGE_B, sd, 616310 + i)
        out[name] = (args, ladder_ref(args[0], args[1], args[2], F_plan(), STAGE_B, SEEDS_B))
    return out


# ------------------------------------------------------------- pure reference checks

def test_reference_cases_land_as_planted(k4b_cases, stage_b_cases):
    for name, (_, expected_N) in CASES.items():
        assert k4b_cases[name][1]["N"] == expected_N, name
        assert stage_b_cases[name][1]["N"] == expected_N, name


def test_reference_rule_equals_k4b_ladder(k4b_cases):
    for name, (args, ref) in k4b_cases.items():
        mine = ladder_ref(args[0], args[1], args[2], F_plan(), k4b_config.MODELS, SEEDS_K4B)
        assert mine["N"] == ref["N"] and mine["sdU"] == ref["sdU"], name
        assert set(mine["candidates"]) == set(ref["candidates"])
        for N, c in ref["candidates"].items():
            p = c["projection"]
            assert mine["candidates"][N]["mde_ok"] == c["mde_ok"]
            assert mine["candidates"][N]["support"] == p["support"]["per_model"]
            assert mine["candidates"][N]["exclusion"] == p["exclusion"]["per_model"]
            assert mine["candidates"][N]["joint"] == (p["support"]["joint"],
                                                      p["exclusion"]["joint"])
            assert mine["candidates"][N]["ok"] == p["ok"]


# ------------------------------------------------------------- DRB9: bitwise K4b mirror

@pytest.mark.parametrize("name", list(CASES))
def test_ladder_pilot_equals_k4b_ladder(k4b_cases, name):
    need()
    args, ref = k4b_cases[name]
    res = hg.ladder_pilot(args[0], args[1], args[2], F_plan(), models=k4b_config.MODELS,
                          seeds=SEEDS_K4B, D_bar=args[3])
    assert set(res) == set(ref)
    for key in ref:
        assert res[key] == ref[key], key
    assert res == ref


# ------------------------------------------------------------- stage-B keys and seeds

@pytest.mark.parametrize("name", list(CASES))
def test_ladder_pilot_stage_b_rule(stage_b_cases, name):
    need()
    args, ref = stage_b_cases[name]
    res = hg.ladder_pilot(args[0], args[1], args[2], F_plan())
    assert res["sdU"] == ref["sdU"]
    assert res["N"] == ref["N"] == CASES[name][1]
    assert res["status"] == ("PASS" if ref["N"] else "INCONCLUSIVE/UNDERPOWERED")
    assert res["k"] == (ref["N"] // 3072 if ref["N"] else None)
    assert set(res["candidates"]) == set(ref["candidates"])
    for N, c in ref["candidates"].items():
        got = res["candidates"][N]
        assert got["mde_ok"] == c["mde_ok"], N
        p = got["projection"]
        assert p["support"]["per_model"] == c["support"], N
        assert p["exclusion"]["per_model"] == c["exclusion"], N
        assert (p["support"]["joint"], p["exclusion"]["joint"]) == c["joint"], N
        assert p["ok"] == c["ok"], N
        assert got["width_diagnostic"] is None


def test_ladder_pilot_defaults_are_stage_b(stage_b_cases):
    need()
    assert tuple(hc.MASTERS) == STAGE_B
    assert hc.SEEDS["sd_upper"] == 620212 and hc.SEEDS["projection"] == 620213
    assert tuple(hc.LADDER) == LADDER
    args, ref = stage_b_cases["n3072"]
    explicit = hg.ladder_pilot(args[0], args[1], args[2], F_plan(), models=STAGE_B,
                               seeds=SEEDS_B, D_bar=None, ladder=LADDER)
    assert explicit["sdU"] == ref["sdU"] and explicit["N"] == ref["N"]


def test_ladder_pilot_width_diagnostic_with_d_bar(stage_b_cases):
    need()
    args, _ = stage_b_cases["n3072"]
    res = hg.ladder_pilot(args[0], args[1], args[2], F_plan(), D_bar=args[3])
    keys = [(j, s) for j in STAGE_B for s in ("-", "+")]
    cols = {(j, "-"): args[0][j] for j in STAGE_B} | {(j, "+"): args[1][j] for j in STAGE_B}
    e = precision.centered_draws(cols, keys, SEEDS_B[1], 5000, 3072)
    f = float(F_plan())
    joint = np.ones(5000, bool)
    for j in STAGE_B:
        em, ep = e[:, keys.index((j, "-"))], e[:, keys.index((j, "+"))]
        qa = c1_means.quantile_with_rank(em, ALPHA)[0]
        qb = c1_means.quantile_with_rank(ep, 1 - ALPHA)[0]
        d = float(args[3][j])
        w = (d + ep + qb + f < 0.01) & (-d + em + qa - f > -0.01)
        assert res["candidates"][3072]["width_diagnostic"]["per_model"][j] == int(w.sum())
        joint &= w
    assert res["candidates"][3072]["width_diagnostic"]["joint"] == int(joint.sum())


# ------------------------------------------------------------- MDE boundary (equality passes)

def boundary_sd():
    """A float sd with precision.mde(sd) == 0.02 exactly at N = 3,072, and Z_bound used."""
    for zb in (Fraction(1, 10**6), Fraction(0), Fraction(1, 10**5), Fraction(3, 10**6)):
        F = k4b_cert.F_plan(zb)
        cfg = {"delta": float(M + F), "alpha": float(ALPHA), "power": 0.80, "projected_N": 3072}
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if precision.mde(mid, cfg) <= 0.02 else (lo, mid)
        x = lo
        while precision.mde(math.nextafter(x, 2.0), cfg) <= 0.02:
            x = math.nextafter(x, 2.0)
        if precision.mde(x, cfg) == 0.02:
            assert precision.mde(math.nextafter(x, 2.0), cfg) > 0.02
            return x, F
    raise AssertionError("no exact MDE boundary found")


def test_reference_boundary_sd_exists():
    x, F = boundary_sd()
    cfg = {"delta": float(M + F), "alpha": float(ALPHA), "power": 0.80, "projected_N": 3072}
    assert precision.mde(x, cfg) == 0.02


@pytest.mark.parametrize("ulps_above, expected", [(0, True), (1, False)])
def test_mde_boundary_equality_passes(monkeypatch, stage_b_cases, ulps_above, expected):
    need()
    x, F = boundary_sd()
    for _ in range(ulps_above):
        x = math.nextafter(x, 2.0)

    def planted_sd(X, r4n, models, seed, draws, size):
        return np.full((int(draws), len(models)), x), np.zeros((int(draws), len(models)))

    # Test technique: ladder_pilot calls precision.sd_b4_draws (API §6.2); the planted SD^U
    # is injected there (and on hwsb_gates too if the module binds the name directly).
    monkeypatch.setattr(precision, "sd_b4_draws", planted_sd)
    if hasattr(hg, "sd_b4_draws"):
        monkeypatch.setattr(hg, "sd_b4_draws", planted_sd)
    args, _ = stage_b_cases["n3072"]
    res = hg.ladder_pilot(args[0], args[1], args[2], F)
    assert all(v == x for v in res["sdU"].values())
    assert bool(res["candidates"][3072]["mde_ok"]) is expected
    if expected:
        assert res["N"] == 3072
    else:
        assert res["N"] != 3072


# ------------------------------------------------------------- b5_N

def test_b5_n_returns_ladder_n_or_fallback():
    need()
    assert hc.C_MIN_FALLBACK_N == 12288
    for N in LADDER:
        assert hg.b5_N({"status": "PASS", "N": N, "k": N // 3072}) == N
    assert hg.b5_N({"status": "INCONCLUSIVE/UNDERPOWERED", "N": None, "k": None}) == 12288


def test_b5_n_on_real_ladder_output(stage_b_cases):
    need()
    args, _ = stage_b_cases["none"]
    res = hg.ladder_pilot(args[0], args[1], args[2], F_plan())
    assert res["N"] is None and hg.b5_N(res) == 12288
