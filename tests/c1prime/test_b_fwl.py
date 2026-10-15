"""Independent tests (author B, job 0026), TEST_PLAN B-3 part 1: FWL, F1, whitening, forced states.

Protocol §5.2-§5.5; API.md §9. Written from the protocol and the four contract documents only;
no tools/c1prime source was read and nothing was executed by the author. References: numpy
least squares on the full 41-column design, the explicit Frisch-Waugh-Lovell formula of §5.2,
and the unchanged `x4f_scores.ledoit_wolf`.

The F1 boundary cases edit the `cond`, `rank`, `B` and `sv_B` fields of a real `fit_fwl` result
(API.md §9 lists them as the fit's fields); B and sv_B are always edited together.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
from topo_pilot.analysis.x4f_scores import ledoit_wolf

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_fit  # noqa: E402
import c1_records  # noqa: E402

pytestmark = pytest.mark.analysis

D = 128
TWO_PI = 2.0 * np.pi
DEGENERATE = "INCONCLUSIVE/PATCH_MODEL_DEGENERATE"


def _status(res) -> str:
    return res if isinstance(res, str) else res["status"]


def _onehot(w) -> np.ndarray:
    out = np.zeros((w.size, 36))
    out[np.arange(w.size), w] = 1.0
    return out


def _f(phi) -> np.ndarray:
    return np.column_stack((np.cos(phi), np.sin(phi)))


def _truth(seed, per_symbol=6, phase="free"):
    rng = np.random.default_rng(seed)
    w = rng.permutation(np.repeat(np.arange(36), per_symbol))
    zt = rng.normal(size=(w.size, 3))
    if phase == "free":
        phi = rng.uniform(0.0, TWO_PI, w.size)
    elif phase == "correlated":  # phase mostly determined by the symbol
        phi = (TWO_PI * w / 36 + 0.3 * rng.uniform(-1.0, 1.0, w.size)) % TWO_PI
    else:  # exactly a function of the symbol: F lies in the span of the indicators
        phi = TWO_PI * w / 36
    alpha, Gamma, B = rng.normal(size=(36, D)), rng.normal(size=(3, D)), rng.normal(size=(D, 2))
    a = alpha[w] + zt @ Gamma + _f(phi) @ B.T
    return {"w": w, "zt": zt, "phi": phi, "alpha": alpha, "Gamma": Gamma, "B": B, "a": a}


def _fit(t, a=None):
    return c1_fit.fit_fwl(t["a"] if a is None else a, t["w"], t["zt"], t["phi"])


def test_fwl_design_column_order():
    t = _truth(4, per_symbol=2)
    X = np.asarray(c1_fit.fwl_design(t["w"], t["zt"], _f(t["phi"])))
    assert X.shape == (72, 41)
    assert np.array_equal(X, np.hstack([_onehot(t["w"]), t["zt"], _f(t["phi"])]))


def test_fwl_recovers_a_known_B_noiselessly():
    t = _truth(1)
    fit = _fit(t)
    np.testing.assert_allclose(fit["B"], t["B"], rtol=0, atol=1e-9)
    np.testing.assert_allclose(fit["alpha"], t["alpha"], rtol=0, atol=1e-9)
    np.testing.assert_allclose(fit["Gamma"], t["Gamma"], rtol=0, atol=1e-9)
    assert int(fit["rank"]) == 41
    X = np.hstack([_onehot(t["w"]), t["zt"], _f(t["phi"])])
    assert abs(float(fit["cond"]) / np.linalg.cond(X, 2) - 1.0) <= 1e-8
    sv = np.sort(np.ravel(np.asarray(fit["sv_B"], dtype=np.float64)))[::-1]
    np.testing.assert_allclose(sv, np.linalg.svd(t["B"], compute_uv=False), rtol=1e-9)
    assert _status(c1_fit.f1_check(fit)) == "PASS"


def test_joint_fwl_is_not_sequential_residualisation():
    t = _truth(2, phase="correlated")
    fit = _fit(t)
    np.testing.assert_allclose(fit["B"], t["B"], rtol=0, atol=1e-7)
    # The trap: residualise A on C, then regress that residual on the UNresidualised F.
    C = np.hstack([_onehot(t["w"]), t["zt"]])
    F = _f(t["phi"])
    resid = t["a"] - C @ np.linalg.lstsq(C, t["a"], rcond=None)[0]
    B_naive = np.linalg.lstsq(F, resid, rcond=None)[0].T
    assert np.max(np.abs(B_naive - t["B"])) / np.max(np.abs(t["B"])) > 0.05
    assert np.max(np.abs(np.asarray(fit["B"]) - B_naive)) > 0.05


def test_fwl_matches_the_frisch_waugh_lovell_formula_with_noise():
    t = _truth(3, per_symbol=8)
    a = t["a"] + np.random.default_rng(31).normal(size=t["a"].shape)
    fit = _fit(t, a)
    C = np.hstack([_onehot(t["w"]), t["zt"]])
    F = _f(t["phi"])

    def m_c(Y):
        return Y - C @ np.linalg.lstsq(C, Y, rcond=None)[0]

    BT = np.linalg.solve(F.T @ m_c(F), F.T @ m_c(a))  # B^T = (F'M_C F)^-1 F'M_C A
    np.testing.assert_allclose(fit["B"], BT.T, rtol=0, atol=1e-9)


def test_standardise_nuisance_population_sd_and_constant_columns():
    rng = np.random.default_rng(5)
    z = rng.normal(size=(50, 3)) * np.array([1.0, 3.0, 0.0]) + np.array([0.0, 1.0, 2.5])
    mean, scale = c1_fit.standardise_nuisance(z)
    np.testing.assert_allclose(mean, z.mean(axis=0), rtol=1e-14, atol=1e-15)
    assert float(np.asarray(scale)[2]) == 1.0
    np.testing.assert_allclose(np.asarray(scale)[:2], z[:, :2].std(axis=0), rtol=1e-14)


# --- F1 ------------------------------------------------------------------------------------------


def test_f1_symbol_determined_phase_is_degenerate():
    t = _truth(6, phase="degenerate")
    try:
        fit = _fit(t)
    except c1_records.C1GateFailure as exc:  # a fit that refuses is acceptable if labelled so
        assert exc.status == DEGENERATE
        return
    assert int(fit["rank"]) < 41
    assert _status(c1_fit.f1_check(fit)) == DEGENERATE


def _with_B(fit, s1, s2):
    B = np.zeros((D, 2))
    B[0, 0], B[1, 1] = s1, s2
    out = dict(fit)
    out["B"], out["sv_B"] = B, np.array([max(s1, s2), min(s1, s2)])
    return out


@pytest.fixture(scope="module")
def good_fit():
    return _fit(_truth(1))


@pytest.mark.parametrize("edit,expected", [
    ({"cond": 1e8}, "PASS"),
    ({"cond": float(np.nextafter(1e8, np.inf))}, DEGENERATE),
    ({"rank": 40}, DEGENERATE),
])
def test_f1_rank_and_condition_boundaries(good_fit, edit, expected):
    fit = dict(good_fit)
    fit.update(edit)
    assert _status(c1_fit.f1_check(fit)) == expected


@pytest.mark.parametrize("s1,s2,expected", [
    (1.0, 1.01e-6, "PASS"), (1.0, 0.99e-6, DEGENERATE), (0.0, 0.0, DEGENERATE),
    (2.0, 3.0, "PASS"),
])
def test_f1_singular_value_boundaries(good_fit, s1, s2, expected):
    assert _status(c1_fit.f1_check(_with_B(good_fit, s1, s2))) == expected


# --- whitening, residual, forced state ------------------------------------------------------------


def test_whitening_is_the_symmetric_inverse_root_of_ledoit_wolf():
    rng = np.random.default_rng(7)
    r = rng.normal(size=(300, 8)) @ rng.normal(size=(8, 8)) + 0.3
    res = c1_fit.whitening(r)
    assert res.get("status", "PASS") == "PASS"
    _, S = ledoit_wolf(r)
    lam, U = np.linalg.eigh(S)
    W_ref = (U * lam**-0.5) @ U.T
    W, W_inv = np.asarray(res["W"]), np.asarray(res["W_inv"])
    np.testing.assert_allclose(W, W_ref, rtol=1e-9, atol=1e-12)
    np.testing.assert_allclose(W, W.T, rtol=0, atol=1e-12)
    np.testing.assert_allclose(W @ S @ W, np.eye(8), rtol=0, atol=1e-10)
    np.testing.assert_allclose(W_inv @ W, np.eye(8), rtol=0, atol=1e-10)


def test_whitening_degenerate_covariance():
    r = np.tile(np.arange(8.0), (50, 1))  # identical rows: LW covariance is exactly zero
    assert _status(c1_fit.whitening(r)) == "INCONCLUSIVE/SUPPORT_DEGENERATE"


def test_residual_keeps_the_phase_term():
    t = _truth(8)
    fit = _fit(t)
    r = np.asarray(c1_fit.residual(t["a"], t["w"], t["zt"], fit))
    expected = t["a"] - np.asarray(fit["alpha"])[t["w"]] - t["zt"] @ np.asarray(fit["Gamma"])
    np.testing.assert_allclose(r, expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(r, _f(t["phi"]) @ t["B"].T, rtol=0, atol=1e-8)


def test_forced_state_is_a_plus_B_times_the_phase_difference():
    rng = np.random.default_rng(9)
    a, B = rng.normal(size=(11, D)), rng.normal(size=(D, 2))
    phi_s, phi_d = rng.uniform(0, TWO_PI, 11), rng.uniform(0, TWO_PI, 11)
    got = np.asarray(c1_fit.forced(a, B, phi_s, phi_d))
    np.testing.assert_allclose(got, a + (_f(phi_d) - _f(phi_s)) @ B.T, rtol=0, atol=1e-13)
    assert np.array_equal(np.asarray(c1_fit.forced(a, B, phi_s, phi_s.copy())), a)
