"""HWSB author A: B4-B6 inputs on planted moments and support (protocol §4 B4, B5, B6; DRB8).

Targets (API.md §4, §6.1): hwsb_eval.endpoints, support, d4_rows; hwsb_gates.b4_status.
X- = X+ = u(phi).r4 on supported rows and -/+ ||r4|| on unsupported rows (K4B §1.4 as used
by protocol §4 B5/B6), missing mass = mean((1 - A)||r4||), width = 2 missing mass. Expected
values are computed here from those definitions (an own tree mean, explicit cos/sin), and
the reused k4b_scores functions are checked against them first. Synthetic arrays only.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from types import SimpleNamespace

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
import k4b_scores  # noqa: E402

try:
    import hwsb_config as hc  # noqa: E402
    import hwsb_eval as he  # noqa: E402
    import hwsb_gates as hg  # noqa: E402
except ImportError as _exc:  # the implementation is written in parallel
    hc = he = hg = None
    MISSING = repr(_exc)
else:
    MISSING = None

A, B = 620201, 620202


def need():
    if MISSING:
        pytest.fail("tools/hwsb modules not importable: " + MISSING)


def tree_mean_ref(x) -> float:
    """Own balanced-tree mean: adjacent pairs level by level (odd last entry carried), / n."""
    level = [float(v) for v in np.asarray(x, dtype=np.float64)]
    n = len(level)
    while len(level) > 1:
        nxt = [level[i] + level[i + 1] for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0] / float(n)


def planted(n=41, seed=616201, n_sup=27):
    rng = np.random.default_rng(seed)
    m = {K: rng.normal(0.0, 0.4, size=(n, 2)) for K in (1, 2, 4, 32)}
    m[32][3] = (0.0, 0.0)                    # a zero oracle mean: phase 0 by convention
    sup = np.zeros(n, dtype=bool)
    sup[rng.choice(n, size=n_sup, replace=False)] = True
    ext = SimpleNamespace(phase=rng.uniform(0.0, 2 * math.pi, size=n), supported=sup,
                          resultant=rng.uniform(0.0, 1.0, size=n),
                          eighth_distance=rng.uniform(0.0, 2.0, size=n),
                          duplicate=np.zeros(n, dtype=bool))
    return m, ext


def endpoints_ref(phi, sup, m32, m4):
    r = m32 - m4
    x = np.cos(phi) * r[:, 0] + np.sin(phi) * r[:, 1]
    norm = np.sqrt(r[:, 0] * r[:, 0] + r[:, 1] * r[:, 1])
    return {"X_minus": np.where(sup, x, -norm), "X_plus": np.where(sup, x, norm), "r4n": norm}


# ------------------------------------------------------------- pure reference checks

def test_reference_tree_mean_matches_reused():
    rng = np.random.default_rng(616202)
    for n in (1, 2, 3, 7, 64, 101):
        x = rng.normal(size=n)
        assert tree_mean_ref(x) == float(c1_means.tree_mean(x))


def test_reference_endpoints_match_reused():
    m, ext = planted()
    ref = endpoints_ref(ext.phase, ext.supported, m[32], m[4])
    got = k4b_scores.endpoint_arrays(ext.phase, ext.supported, m[32], m[4])
    for key in ("X_minus", "X_plus", "r4n"):
        assert np.array_equal(got[key], ref[key]), key


# ------------------------------------------------------------- endpoints (DRB8)

def test_endpoints_partial_support_exact():
    need()
    m, ext = planted()
    a = he.endpoints(ext, m)
    ref = endpoints_ref(ext.phase, ext.supported, m[32], m[4])
    sup = ext.supported
    for key in ("X_minus", "X_plus", "r4n"):
        assert np.array_equal(np.asarray(a[key]), ref[key]), key
    assert np.array_equal(a["X_minus"][sup], a["X_plus"][sup])
    assert np.array_equal(a["X_minus"][~sup], -ref["r4n"][~sup])
    assert np.array_equal(a["X_plus"][~sup], ref["r4n"][~sup])
    assert np.all(a["X_minus"] <= a["X_plus"])
    assert np.array_equal(a["phi"], ext.phase)
    assert a["supported"].dtype == bool and np.array_equal(a["supported"], sup)


@pytest.mark.parametrize("n_sup", [0, 41])
def test_endpoints_no_or_full_support(n_sup):
    need()
    m, ext = planted(n_sup=n_sup)
    a = he.endpoints(ext, m)
    ref = endpoints_ref(ext.phase, ext.supported, m[32], m[4])
    assert np.array_equal(a["X_minus"], ref["X_minus"])
    assert np.array_equal(a["X_plus"], ref["X_plus"])
    if n_sup == 0:
        assert np.array_equal(a["X_plus"] - a["X_minus"], 2 * ref["r4n"])
    else:
        assert np.array_equal(a["X_plus"], a["X_minus"])


def test_endpoints_supported_rows_use_the_extension_phase_only():
    need()
    m, ext = planted()
    a = he.endpoints(ext, m)
    moved = SimpleNamespace(**vars(ext))
    moved.phase = np.where(ext.supported, ext.phase, ext.phase + 1.0)  # unsupported phases
    b = he.endpoints(moved, m)
    assert np.array_equal(a["X_minus"], b["X_minus"])
    assert np.array_equal(a["X_plus"], b["X_plus"])


# ------------------------------------------------------------- support report

def test_support_missing_mass_and_width_exact():
    need()
    m, ext = planted()
    a = he.endpoints(ext, m)
    R = 0.7
    rep = he.support(ext, R, a, m)
    r = endpoints_ref(ext.phase, ext.supported, m[32], m[4])["r4n"]
    A_ = ext.supported
    missing = tree_mean_ref(np.where(A_, 0.0, r))
    assert rep["missing_mass"] == missing
    assert rep["width"] == 2.0 * missing
    assert rep["n"] == A_.size and rep["n_supported"] == int(A_.sum())
    assert rep["fraction"] == pytest.approx(A_.sum() / A_.size, abs=1e-15)
    assert rep["mean_r4_supported"] == tree_mean_ref(r[A_])
    assert rep["mean_r4_unsupported"] == tree_mean_ref(r[~A_])
    x = np.cos(ext.phase) * (m[32] - m[4])[:, 0] + np.sin(ext.phase) * (m[32] - m[4])[:, 1]
    # unsealed form (pilot models never enter stage C, Q1 default): contribution reported
    assert rep["supported_contribution"] == pytest.approx(tree_mean_ref(A_ * x), abs=1e-15)
    expected = k4b_scores.support_report(ext, R, a["r4n"], ext.phase, m[32], m[4], False)
    assert rep == expected


def test_support_reasons_count_unsupported_rows():
    need()
    m, ext = planted()
    rep = he.support(ext, 0.7, he.endpoints(ext, m), m)
    un = ~ext.supported
    low, far = ext.resultant < 0.2, ext.eighth_distance > 0.7
    reasons = rep["reasons"]
    assert reasons["resultant_only"] == int(np.sum(un & low & ~far))
    assert reasons["distance_only"] == int(np.sum(un & far & ~low))
    assert reasons["both"] == int(np.sum(un & low & far))


# ------------------------------------------------------------- D4 rows (B5 denominator)

def test_d4_rows_equal_k4b_delta4_orc():
    need()
    m, _ = planted()
    got = he.d4_rows(m)
    ref = k4b_scores.phase_scores(k4b_scores.oracle_phase(m[32]), m[32], m[4])
    assert np.array_equal(np.asarray(got), ref)
    # independent reading: u(phase(m32)).(m32 - m4) = |m32| - u.m4 (phase 0 at m32 = 0)
    norm = np.hypot(m[32][:, 0], m[32][:, 1])
    ux = np.where(norm > 0, m[32][:, 0] / np.where(norm > 0, norm, 1.0), 1.0)
    uy = np.where(norm > 0, m[32][:, 1] / np.where(norm > 0, norm, 1.0), 0.0)
    alt = norm - (ux * m[4][:, 0] + uy * m[4][:, 1])
    assert np.allclose(got, alt, rtol=0, atol=1e-12)
    assert got[3] == -m[4][3, 0]            # m32 = 0: u = (1, 0), r4 = -m4


# ------------------------------------------------------------- B4 status (§4 B4, choice 17)

def _maps(cal_val):
    """cal_val: {j: (c0_cal status, c0_val status)} -> the b4_cal-like and b4_val-like dicts."""
    # API-AMBIGUITY: b4_status may read either map["status"][j] or map["per_model"][j]
    # ["status"]; both are filled consistently here.
    cal = {"per_model": {j: {"status": s[0]} for j, s in cal_val.items()},
           "status": {j: s[0] for j, s in cal_val.items()}}
    val = {"per_model": {j: {"status": s[1]} for j, s in cal_val.items()},
           "status": {j: s[1] for j, s in cal_val.items()}}
    return cal, val


NO_CHART = "NOT_RUN/NO_CHART"
UNAV = "INCONCLUSIVE/CHART_UNAVAILABLE"


def test_b4_status_both_pass():
    need()
    res = hg.b4_status(*_maps({A: ("PASS", "PASS"), B: ("PASS", "PASS")}), (A, B))
    assert res["pass"]
    assert res["failing"] == [] and res["criterion"] is None and res["technical"] is None
    for j in (A, B):
        assert res["per_model"][j] == {"c0_cal": "PASS", "c0_val": "PASS", "pass": True}


def test_b4_status_cal_failure_is_c0_cal():
    need()
    res = hg.b4_status(*_maps({A: (UNAV, NO_CHART), B: ("PASS", "PASS")}), (A, B))
    assert not res["pass"]
    assert res["failing"] == [A] and res["criterion"] == "C0_CAL"
    assert res["technical"] is None
    assert not res["per_model"][A]["pass"]
    assert res["per_model"][B]["pass"]


def test_b4_status_first_failing_model_in_master_order():
    need()
    maps = _maps({A: ("PASS", "FAIL"), B: (UNAV, NO_CHART)})
    res = hg.b4_status(*maps, (A, B))
    assert res["failing"] == [A, B] and res["criterion"] == "C0_VAL"
    res = hg.b4_status(*maps, (B, A))
    assert res["failing"] == [B, A] and res["criterion"] == "C0_CAL"


def test_b4_status_no_chart_counts_against_c0_val():
    need()
    res = hg.b4_status(*_maps({A: ("PASS", "PASS"), B: ("PASS", NO_CHART)}), (A, B))
    assert not res["pass"] and res["failing"] == [B] and res["criterion"] == "C0_VAL"
    assert res["per_model"][B] == {"c0_cal": "PASS", "c0_val": NO_CHART, "pass": False}


def test_b4_status_technical_status_reported():
    need()
    tech = "FAIL_TECHNICAL/NUMERICAL"
    res = hg.b4_status(*_maps({A: ("PASS", "PASS"), B: (tech, NO_CHART)}), (A, B))
    assert res["technical"] == tech and res["criterion"] == "C0_CAL"
    assert res["failing"] == [B]
    tech2 = "FAIL_TECHNICAL/BUILD"
    res = hg.b4_status(*_maps({A: ("PASS", tech2), B: ("PASS", "PASS")}), (A, B))
    assert res["technical"] == tech2 and res["criterion"] == "C0_VAL"
    res = hg.b4_status(*_maps({A: (tech2, NO_CHART), B: ("PASS", tech)}), (A, B))
    assert res["technical"] == tech2        # first in master order under every reading
