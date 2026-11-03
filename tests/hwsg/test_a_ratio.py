"""Author A (job 0224): capture ratio and its joint bootstrap (§2.7; N1, N7; KG7; DRG10).

Synthetic arrays only (TEST_PLAN §4 KG7 fixture, in memory). Expected ranks and ratios are
computed here with numpy sorting, independent of hwsg_ratio.
"""

from __future__ import annotations  # noqa: I001


import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _d in ("c1prime", "k4b", "hwsb", "hwsc", "hwsg"):
    if str(REPO / "tools" / _d) not in sys.path:
        sys.path.insert(0, str(REPO / "tools" / _d))
_ERR = None
try:
    import hwsg_config as gc  # noqa: F401
    import hwsg_ratio as gq
    import c1_means
    import k4b_fresh
    import k4b_stats
except Exception as e:
    _ERR = e

J = (620631, 620632, 620633)  # hi masters
CS = (Fraction(1, 2), Fraction(9, 10), Fraction(3, 2))
SEED = 620913  # dry endpoint seed (OPEN-6)
N = 3072


@pytest.fixture(autouse=True)
def _imports(monkeypatch):
    if _ERR is not None:
        pytest.fail(f"hwsg modules not importable: {_ERR!r}")
    # bootstrap_inputs iterates k4b_fresh.MODELS; the world binding sets it to the masters.
    monkeypatch.setattr(k4b_fresh, "MODELS", J)


def _v(x):
    return float(x[0]) if isinstance(x, (tuple, list)) else float(x)


def _status(fn, *a, **k):
    try:
        r = fn(*a, **k)
    except Exception as e:
        return getattr(e, "status", repr(e)), None
    return (r.get("status") if isinstance(r, dict) else None), r


def _fixture(shift=0.0):
    rng = np.random.default_rng(77)
    D = 0.05 + 0.01 * rng.standard_normal(N) + shift
    arrays = {}
    for j, c in zip(J, CS):
        xm = float(c) * D
        arrays[j] = {"X_minus": xm, "X_plus": xm + 0.002}
    return arrays, {"delta4_orc": {"all": {"X": D}}}


_CACHE = {}


def _draws():
    if "d" not in _CACHE:
        a, c = _fixture()
        _CACHE["d"] = (a, c, gq.draws(a, c, SEED))
    return _CACHE["d"]


def test_d_key():
    assert gq.D_KEY == "delta4_orc:all"


def test_draws_equal_joint_bootstrap_bitwise():
    a, c, dr = _draws()
    ref = k4b_stats.joint_bootstrap(k4b_fresh.bootstrap_inputs(a, c), SEED)
    assert set(dr) == set(ref) and gq.D_KEY in dr
    for k in ref:
        assert np.array_equal(np.asarray(dr[k]), ref[k])
        assert len(ref[k]) == 5000


def test_planted_ratio_point_and_bounds():
    a, c, dr = _draws()
    D = c["delta4_orc"]["all"]["X"]
    pD = float(c1_means.tree_mean(D))
    for j, cc in zip(J, CS):
        pm = float(c1_means.tree_mean(a[j]["X_minus"]))
        r = gq.model_ratio(dr, j, pm, pD)
        assert abs(_v(r["rho"]) - float(cc)) <= 1e-12
        rd = np.sort(np.asarray(dr[f"X:{j}:-"]) / np.asarray(dr[gq.D_KEY]))
        assert _v(r["rhoL"]) == rd[83] and _v(r["rhoU"]) == rd[4916]
        assert _v(r["rhoL"]) <= float(cc) + 1e-12 and float(cc) - 1e-12 <= _v(r["rhoU"])


def test_ratio_draws_definition():
    a, c, dr = _draws()
    rr = gq.ratio_draws(dr, J[0])
    assert np.array_equal(rr["minus"], dr[f"X:{J[0]}:-"] / dr[gq.D_KEY])
    assert np.array_equal(rr["plus"], dr[f"X:{J[0]}:+"] / dr[gq.D_KEY])


def test_seed_sensitivity():
    a, c, dr = _draws()
    other = gq.draws(a, c, SEED + 1)
    assert not np.array_equal(other[gq.D_KEY], dr[gq.D_KEY])
    again = gq.draws(a, c, SEED)
    assert all(np.array_equal(again[k], dr[k]) for k in dr)


def test_ratio_unclipped():
    rng = np.random.default_rng(5)
    D = 0.05 + 0.001 * rng.standard_normal(5000)
    dr = {gq.D_KEY: D, f"X:{J[0]}:-": -0.5 * D, f"X:{J[0]}:+": -0.5 * D + 0.002,
          f"X:{J[1]}:-": 1.5 * D, f"X:{J[1]}:+": 1.5 * D + 0.002}
    neg = gq.model_ratio(dr, J[0], -0.025, 0.05)
    big = gq.model_ratio(dr, J[1], 0.075, 0.05)
    assert _v(neg["rho"]) == -0.5 and _v(neg["rhoU"]) < 0
    assert _v(big["rho"]) > 1 and _v(big["rhoL"]) > 1


# ----------------------------------------------------------------------------- RATIO gate


def _gate(tmp_path, monkeypatch, dr, b4=True, result=None):
    a, c = _fixture()
    if result is None:
        result = {"per_model": {j: dict(zip(("L", "U"), _lu(dr, j))) for j in J}}
    monkeypatch.setattr(gq, "draws", lambda *x, **k: dr)
    monkeypatch.chdir(tmp_path)
    # API-AMBIGUITY: the output directory of RATIO.json is not named in the signature;
    # ctx carries both common names.
    ctx = {"test_arrays": a, "controls": c, "out": tmp_path, "world_dir": tmp_path}
    return _status(gq.ratio_gate, ctx, result, b4, SEED)


def _lu(dr, j):
    b = k4b_stats.bounds(dr[f"X:{j}:-"], dr[f"X:{j}:+"])
    return b["L"], b["U"]


def _planted(dshift=0.0, zero_at=None):
    rng = np.random.default_rng(11)
    D = 0.05 + 0.002 * rng.standard_normal(5000) + dshift
    if zero_at is not None:
        D[zero_at] = 0.0
    dr = {gq.D_KEY: D}
    for j, cc in zip(J, CS):
        dr[f"X:{j}:-"] = float(cc) * D + 1e-4 * rng.standard_normal(5000)
        dr[f"X:{j}:+"] = dr[f"X:{j}:-"] + 0.002
    return dr


def _ratio_status(st, r):
    return r.get("status") if r else st


def test_gate_defined(tmp_path, monkeypatch):
    st, r = _gate(tmp_path, monkeypatch, _planted())
    assert _ratio_status(st, r) == "DEFINED"
    assert _v(r["D_L"]) == np.sort(_planted()[gq.D_KEY])[83]


def test_gate_identity_mismatch_numerical(tmp_path, monkeypatch):
    dr = _planted()
    res = {"per_model": {j: dict(zip(("L", "U"), _lu(dr, j))) for j in J}}
    L = res["per_model"][J[1]]["L"]
    lv = _v(L)
    pert = np.nextafter(lv, 1.0)
    res["per_model"][J[1]]["L"] = (pert, L[1]) if isinstance(L, tuple) else pert
    st, r = _gate(tmp_path, monkeypatch, dr, result=res)
    assert st == "FAIL_TECHNICAL/NUMERICAL"


def test_gate_D_rank84_nonpositive(tmp_path, monkeypatch):
    st, r = _gate(tmp_path, monkeypatch, _planted(dshift=-0.048))
    assert np.sort(_planted(dshift=-0.048)[gq.D_KEY])[83] <= 0
    assert _ratio_status(st, r) == "RATIO_UNRESOLVED"


def test_gate_single_nonpositive_draw(tmp_path, monkeypatch):  # OPEN-11
    dr = _planted(zero_at=1234)
    assert np.sort(dr[gq.D_KEY])[83] > 0
    st, r = _gate(tmp_path, monkeypatch, dr)
    assert _ratio_status(st, r) == "RATIO_UNRESOLVED"


def test_gate_b4_not_passed(tmp_path, monkeypatch):
    st, r = _gate(tmp_path, monkeypatch, _planted(), b4=False)
    assert _ratio_status(st, r) == "RATIO_UNRESOLVED"


def test_gate_identity_real_draws(tmp_path, monkeypatch):
    """L, U re-derived from the real joint bootstrap equal a planted RESULT bitwise."""
    a, c, dr = _draws()
    st, r = _gate(tmp_path, monkeypatch, dr)
    assert _ratio_status(st, r) == "DEFINED"
    assert r.get("identity") is True
