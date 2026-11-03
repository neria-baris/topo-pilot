"""Author A (job 0223): P1 precision ladder and its blindness (protocol 2.9; API_U2 4.2; DRU5).

Expected N values come from a hand implementation of the API_U2 4.2 rule on the reused
`precision` module. A short ladder keeps the 5,000-draw bootstrap cheap (p1_u takes `ladder`)."""

from __future__ import annotations  # noqa: I001

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,F401
import c1_means  # noqa: E402
import c1_records  # noqa: E402
import precision  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

MASTERS = [620301, 620302, 620303]
SEEDS = {"p1_sd": 640114, "p1_centred": 640115}
LAD = (64, 256, 1024, 4096)
n = 256


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


def _data(noise, seed=31):
    rng = np.random.default_rng(seed)
    G = rng.random(n) + 0.5
    A = {j: 0.4 * G + s * rng.standard_normal(n) for j, s in zip(MASTERS, noise)}
    return A, G


def hand(A, G, ladder=LAD):
    alt = 0.10 * float(c1_means.tree_mean(G))
    passes = {}
    for X, c in (("ZR010", 0.1), ("ZR030", 0.3)):
        Xd = {j: A[j] - c * G for j in MASTERS}
        sd, _ = precision.sd_b4_draws(Xd, {j: G for j in MASTERS}, MASTERS, SEEDS["p1_sd"], 5000, len(G))
        passes[X] = {}
        for N in ladder:
            e = precision.centered_draws(Xd, MASTERS, SEEDS["p1_centred"], 5000, N)
            cfg = {"alpha": 1 / 300, "power": 0.80, "delta": 0.0, "alternative": alt, "projected_N": N}
            s = precision.precision_summary(sd, e, MASTERS, cfg)
            passes[X][N] = {j: s["models"][j]["mde_upper"] <= alt and s["models"][j]["power"] >= 0.80
                            for j in MASTERS}
    both = {N: [j for j in MASTERS if passes["ZR010"][N][j] and passes["ZR030"][N][j]] for N in ladder}
    for N in ladder:
        if len(both[N]) == 3:
            return N, passes, []
    for N in ladder:
        if len(both[N]) >= 2:
            return N, passes, [j for j in MASTERS if j not in both[N]]
    return None, passes, None


def _p1(A, G, ladder=LAD):
    return mod("hwsu_gates").p1_u(A, G, MASTERS, SEEDS, ladder=ladder)


def _norm_passes(p):
    return {X: {int(N): {int(j): bool(v) for j, v in d.items()} for N, d in p[X].items()}
            for X in ("ZR010", "ZR030")}


# noise levels chosen so the ladder's interior is exercised (all pass somewhere above 64)
ALL = (0.3, 0.3, 0.3)
TWO = (0.3, 0.3, 40.0)
NONE = (40.0, 40.0, 40.0)


def test_all_pass_smallest_N():
    A, G = _data(ALL)
    N, passes, pl = hand(A, G)
    assert N is not None and pl == []
    r = _p1(A, G)
    assert r["N_RESP"] == N and r["N"] == N
    assert r["k"] == N / 4096
    assert _norm_passes(r["passes"]) == passes
    assert list(r.get("precision_limited", [])) == []
    assert "N_SHARE" not in r


def test_two_pass_fallback_precision_limited():
    A, G = _data(TWO)
    N, passes, pl = hand(A, G)
    assert N is not None and pl == [MASTERS[2]]
    r = _p1(A, G)
    assert r["N_RESP"] == N
    assert any(str(MASTERS[2]) in str(x) for x in r["precision_limited"])
    assert not any(str(MASTERS[0]) in str(x) for x in r["precision_limited"])


def test_underpowered():
    A, G = _data(NONE)
    N, _, _ = hand(A, G)
    assert N is None
    try:
        r = _p1(A, G)
    except c1_records.C1GateFailure as e:
        assert e.status == "INCONCLUSIVE/UNDERPOWERED"
    else:
        assert r["N_RESP"] is None


def test_blindness_constant_shift_of_A():
    """Adding a constant to every A_j changes mean A_full only: N and passes are identical."""
    A, G = _data(TWO, seed=33)
    r0 = _p1(A, G)
    r1 = _p1({j: A[j] + 7.25 for j in MASTERS}, G)
    assert r1["N_RESP"] == r0["N_RESP"] and r1["N"] == r0["N"]
    assert _norm_passes(r1["passes"]) == _norm_passes(r0["passes"])


def test_seeds_alt_and_r4n_used(monkeypatch):
    A, G = _data(ALL)
    seen = {"sd": [], "c": [], "alt": [], "r4n": []}
    sd0, c0, s0 = precision.sd_b4_draws, precision.centered_draws, precision.precision_summary

    def sd_spy(X, r4n, models, seed, draws, size):
        seen["sd"].append((seed, draws, size))
        seen["r4n"].append(all(np.array_equal(r4n[j], G) for j in models))
        return sd0(X, r4n, models, seed, draws, size)

    def c_spy(X, models, seed, draws, size):
        seen["c"].append((seed, draws, size))
        return c0(X, models, seed, draws, size)

    def s_spy(sd, e, models, cfg):
        seen["alt"].append(cfg["alternative"])
        assert cfg["alpha"] == pytest.approx(1 / 300) and cfg["power"] == 0.80
        assert cfg["delta"] == 0.0
        return s0(sd, e, models, cfg)

    monkeypatch.setattr(precision, "sd_b4_draws", sd_spy)
    monkeypatch.setattr(precision, "centered_draws", c_spy)
    monkeypatch.setattr(precision, "precision_summary", s_spy)
    _p1(A, G)
    assert seen["sd"] and all(s == (640114, 5000, n) for s in seen["sd"])
    assert seen["c"] and all(s[0] == 640115 and s[1] == 5000 and s[2] in LAD for s in seen["c"])
    assert all(seen["r4n"])
    alt = 0.10 * float(c1_means.tree_mean(G))
    assert all(a == pytest.approx(alt, rel=1e-15) for a in seen["alt"])


def test_seed_sensitive():
    """Different seeds change the draws (a borderline fixture would change N): the seeds matter."""
    A, G = _data(ALL)
    Xd = {j: A[j] - 0.1 * G for j in MASTERS}
    a = precision.centered_draws(Xd, MASTERS, 640115, 50, 64)
    b = precision.centered_draws(Xd, MASTERS, 640114, 50, 64)
    assert not np.array_equal(a, b)
