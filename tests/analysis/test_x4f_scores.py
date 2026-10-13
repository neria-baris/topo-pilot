"""Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
before reading the implementation.

Scores, support and verdict (X4F_GATES_API section 2.3; x4f-exec-v2 sections 4, 7, 9, 10, 11).
"""
import math

import numpy as np
import pytest

from topo_pilot.analysis import (
    gate_verdict,
    kl_rows,
    ledoit_wolf,
    r2_pooled,
    rbf_bandwidth,
    rbf_features,
    rbf_map,
    standardizer,
    support_gate,
    support_report,
)
from topo_pilot.contracts import ErrorCode, StageFailure

pytestmark = pytest.mark.analysis


def _pairwise_median(X):
    i, j = np.triu_indices(X.shape[0], k=1)
    return float(np.median(np.linalg.norm(X[i] - X[j], axis=1)))


def _lw_reference(X):
    """Ledoit and Wolf (2004): population covariance S shrunk toward m*I, m = tr(S)/d, with
    the normalised Frobenius norm ||A||^2 = tr(A A^T)/d."""
    n, d = X.shape
    Xc = X - X.mean(0)
    S = Xc.T @ Xc / n
    m = np.trace(S) / d
    d2 = np.sum((S - m * np.eye(d)) ** 2) / d
    b2_bar = sum(np.sum((np.outer(x, x) - S) ** 2) / d for x in Xc) / n**2
    shrink = min(b2_bar, d2) / d2
    return S, shrink * m * np.eye(d) + (1 - shrink) * S


def _mahalanobis(X, mu, cov):
    diff = X - mu
    return np.sqrt(np.einsum("ij,ij->i", diff @ np.linalg.inv(cov), diff))


# --------------------------------------------------------------------------- standardizer

def test_standardizer_population_std_and_zero_floor():
    rng = np.random.default_rng(0)
    n = 200
    X = np.stack([3 * rng.normal(size=n) + 1, np.full(n, 5.0), 2 + 1e-13 * rng.normal(size=n),
                  rng.normal(size=n)], axis=1)
    mean, scale = standardizer(X)
    np.testing.assert_allclose(mean, X.mean(0), atol=1e-12)
    np.testing.assert_allclose(scale[[0, 3]], X.std(0, ddof=0)[[0, 3]], rtol=1e-12)
    assert scale[1] == 1.0 and scale[2] == 1.0
    assert mean.shape == (4,) and scale.shape == (4,)


# --------------------------------------------------------------------------- r2_pooled

def test_r2_pooled_hand_values_around_calibration_mean():
    Y_val = np.array([[1.0, 2.0], [3.0, 4.0]])
    Y_pred = np.array([[1.0, 2.0], [3.0, 5.0]])
    r2, status = r2_pooled(Y_pred, Y_val, np.array([0.0, 0.0]))
    assert status == "ok"
    assert r2 == pytest.approx(1 - 1 / 30, abs=1e-14)      # not 0.75 (validation mean)


def test_r2_pooled_is_pooled_over_coordinates():
    Y_val = np.array([[1.0, 10.0], [3.0, 30.0]])
    Y_pred = np.array([[2.0, 10.0], [3.0, 30.0]])
    r2, status = r2_pooled(Y_pred, Y_val, np.array([2.0, 20.0]))
    assert status == "ok"
    assert r2 == pytest.approx(1 - 1 / 202, abs=1e-14)     # per-coordinate average would be 0.75


def test_r2_pooled_one_dimensional_and_negative():
    r2, status = r2_pooled(np.array([1.0, 2.0, 4.0]), np.array([1.0, 2.0, 3.0]), 0.0)
    assert status == "ok" and r2 == pytest.approx(1 - 1 / 14, abs=1e-14)
    r2, _ = r2_pooled(np.array([5.0, 5.0]), np.array([1.0, -1.0]), 0.0)
    assert r2 == pytest.approx(1 - 52 / 2, abs=1e-12)
    r2, _ = r2_pooled(np.array([[1.0], [2.0]]), np.array([[1.0], [2.0]]), np.array([0.0]))
    assert r2 == pytest.approx(1.0, abs=1e-14)


def test_r2_pooled_zero_variance_threshold_scales_with_n_q():
    mean_cal = np.array([1.0, -1.0])
    Y_same = np.tile(mean_cal, (10, 1))
    assert r2_pooled(Y_same + 0.3, Y_same, mean_cal) == (None, "R2_UNDEFINED_ZERO_VARIANCE")
    tiny = Y_same + 1e-7                                   # SST = 20 * 1e-14 <= 1e-12 * 20
    assert r2_pooled(tiny, tiny, mean_cal) == (None, "R2_UNDEFINED_ZERO_VARIANCE")
    small = Y_same + 1e-5                                  # SST = 20 * 1e-10 > 1e-12 * 20
    r2, status = r2_pooled(small, small, mean_cal)
    assert status == "ok" and r2 == pytest.approx(1.0, abs=1e-12)


# --------------------------------------------------------------------------- kl_rows

def test_kl_rows_hand_values_in_nats():
    P = np.array([[0.5, 0.5], [1.0, 0.0], [0.2, 0.8]])
    Q = np.array([[0.25, 0.75], [0.5, 0.5], [0.2, 0.8]])
    kl, status = kl_rows(P, Q)
    assert status == "ok"
    expected = [0.5 * math.log(2) + 0.5 * math.log(2 / 3), math.log(2), 0.0]
    np.testing.assert_allclose(kl, expected, atol=1e-14)


def test_kl_rows_zero_p_terms_contribute_nothing_even_where_q_is_zero():
    P = np.array([[1.0, 0.0, 0.0]])
    Q = np.array([[0.5, 0.5, 0.0]])
    kl, status = kl_rows(P, Q)
    assert status == "ok"
    np.testing.assert_allclose(kl, [math.log(2)], atol=1e-14)


def test_kl_rows_undefined_when_q_zero_where_p_positive():
    P = np.array([[0.5, 0.5], [0.3, 0.7]])
    Q = np.array([[0.5, 0.5], [1.0, 0.0]])
    assert kl_rows(P, Q) == (None, "KL_UNDEFINED")


@pytest.mark.parametrize("shape_q", [(2, 3), (3, 2), (2,)])
def test_kl_rows_shape_mismatch(shape_q):
    P = np.full((2, 2), 0.5)
    Q = np.full(shape_q, 1.0 / shape_q[-1])
    with pytest.raises(StageFailure) as exc:
        kl_rows(P, Q)
    assert exc.value.code is ErrorCode.ALIGNMENT_ERROR


# --------------------------------------------------------------------------- RBF

def test_rbf_bandwidth_median_rule_hand_value():
    X = np.array([[0.0, 0.0], [3.0, 0.0], [0.0, 4.0]])   # distances 3, 4, 5
    ell, status = rbf_bandwidth(X, np.random.default_rng(0))
    assert status == "ok" and ell == pytest.approx(4.0, abs=1e-14)


def test_rbf_bandwidth_subsample_follows_rng_choice():
    X = np.random.default_rng(1).normal(size=(50, 3)) * np.array([1.0, 5.0, 0.2])
    ell, status = rbf_bandwidth(X, np.random.default_rng(5), n_sub=10)
    idx = np.random.default_rng(5).choice(50, 10, replace=False)
    assert status == "ok"
    assert ell == pytest.approx(_pairwise_median(X[idx]), rel=1e-12)
    assert ell != pytest.approx(_pairwise_median(X), rel=1e-6)   # fixture: subsampling matters


def test_rbf_bandwidth_degenerate_for_identical_rows():
    X = np.tile([1.0, 2.0, 3.0], (12, 1))
    assert rbf_bandwidth(X, np.random.default_rng(0)) == (None, "RBF_DEGENERATE")


def test_rbf_map_draw_order_and_shapes():
    Omega, b = rbf_map(3, 64, 2.5, np.random.default_rng(9))
    ref = np.random.default_rng(9)
    Om_ref = ref.standard_normal((3, 64)) / 2.5
    b_ref = ref.uniform(0, 2 * np.pi, 64)
    assert Omega.shape == (3, 64) and b.shape == (64,)
    np.testing.assert_allclose(Omega, Om_ref, rtol=0, atol=1e-15)
    np.testing.assert_allclose(b, b_ref, rtol=0, atol=1e-15)


def test_rbf_features_formula():
    rng = np.random.default_rng(10)
    X = rng.normal(size=(7, 3))
    Omega = rng.normal(size=(3, 16))
    b = rng.uniform(0, 2 * np.pi, 16)
    phi = rbf_features(X, Omega, b)
    assert phi.shape == (7, 16)
    np.testing.assert_allclose(phi, np.sqrt(2 / 16) * np.cos(X @ Omega + b), atol=1e-14)


# --------------------------------------------------------------------------- Ledoit-Wolf

@pytest.mark.parametrize("n,d", [(300, 5), (10, 20)])
def test_ledoit_wolf_shrinks_population_covariance_toward_scaled_identity(n, d):
    rng = np.random.default_rng(n + d)
    X = rng.normal(size=(n, d)) @ rng.normal(size=(d, d)) + 3.0
    mu, cov = ledoit_wolf(X)
    S, ref = _lw_reference(X)
    np.testing.assert_allclose(mu, X.mean(0), atol=1e-12)
    np.testing.assert_allclose(cov, cov.T, atol=1e-14 * np.abs(cov).max())
    assert np.linalg.eigvalsh(cov).min() > 0
    assert abs(np.trace(cov) - np.trace(S)) <= 1e-10 * max(1.0, np.trace(S))
    # structure: cov = (1 - delta) S + delta * (tr S / d) I with delta in [0, 1]
    off = ~np.eye(d, dtype=bool)
    delta = 1 - np.sum(cov[off] * S[off]) / np.sum(S[off] ** 2)
    assert -1e-10 <= delta <= 1 + 1e-10
    np.testing.assert_allclose(cov, (1 - delta) * S + delta * np.trace(S) / d * np.eye(d),
                               atol=1e-10 * np.abs(S).max())
    np.testing.assert_allclose(cov, ref, atol=1e-10 * np.abs(S).max())


def test_ledoit_wolf_zero_shrinkage_known_answer():
    X = np.tile([[1.0, 0.0], [-1.0, 0.0]], (10, 1))   # every x x^T equals S: no shrinkage
    mu, cov = ledoit_wolf(X)
    np.testing.assert_allclose(mu, [0.0, 0.0], atol=1e-15)
    np.testing.assert_allclose(cov, np.diag([1.0, 0.0]), atol=1e-12)


# --------------------------------------------------------------------------- support_report

def _support_data(seed=0, n=2000, d=4):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(d, d)) + 2 * np.eye(d)
    return rng.normal(size=(n, d)) @ A, rng.normal(size=(n, d)) @ A


def test_support_identity_patch_and_planted_shift():
    X_cal, X_val = _support_data()
    shift = X_val + 10.0 * X_cal.std(0)
    rep = support_report(X_cal, X_val, {"id": X_val.copy(), "shift": shift})
    assert rep["status"] == "ok"
    mu, cov = ledoit_wolf(X_cal)
    D_cal = _mahalanobis(X_cal, mu, cov)
    q99 = rep["q99_cal"]
    assert q99 == pytest.approx(np.quantile(D_cal, 0.99), rel=1e-2)   # a distance, not squared
    assert 0.005 <= np.mean(D_cal > q99) <= 0.015
    D_val = _mahalanobis(X_val, mu, cov)
    assert rep["frac_unpatched_val"] == pytest.approx(np.mean(D_val > q99), abs=1e-12)
    assert abs(rep["frac_unpatched_val"] - 0.01) <= 0.01
    assert rep["frac"]["id"] == pytest.approx(rep["frac_unpatched_val"], abs=1e-12)
    assert rep["frac"]["shift"] >= 0.99
    assert isinstance(rep["knn_ratio"], dict)
    assert rep["knn_ratio"]["id"] == pytest.approx(1.0, abs=1e-12)
    assert rep["knn_ratio"]["shift"] > 2.0


def test_support_ratio_undefined_with_duplicated_rows():
    base = np.random.default_rng(3).normal(size=(20, 3))
    X_cal = np.repeat(base, 10, axis=0)           # every validation row has 10 exact copies
    X_val = base.copy()
    rep = support_report(X_cal, X_val, {"id": X_val.copy()})
    assert rep["status"] == "ok"
    assert rep["knn_ratio"] == "RATIO_UNDEFINED"


def test_support_degenerate_covariance():
    X_cal = np.tile([[1.0, 0.0], [-1.0, 0.0]], (10, 1))   # Ledoit-Wolf gives diag(1, 0)
    X_val = X_cal[:6].copy()
    rep = support_report(X_cal, X_val, {"id": X_val.copy()})
    assert rep["status"] == "SUPPORT_DEGENERATE"


# --------------------------------------------------------------------------- support_gate

@pytest.mark.parametrize("frac,randoms,expected", [
    (0.03, [0.02] * 20, True),
    (0.05, [0.025] * 20, True),          # both boundaries are inclusive
    (0.051, [0.1] * 20, False),          # above the 0.05 ceiling
    (0.03, [0.01] * 20, False),          # above twice the median
    (0.0, [0.0] * 20, True),             # zero median: literal rule, zero passes
    (1e-9, [0.0] * 20, False),           # zero median: anything above zero fails
    (1e-9, [0.0] * 11 + [0.5] * 9, False),
    (0.02, [0.0] * 9 + [0.01] * 11, True),
    (0.03, [0.0] * 9 + [0.01] * 11, False),
])
def test_support_gate_literal_rule(frac, randoms, expected):
    assert support_gate(frac, randoms) is expected


# --------------------------------------------------------------------------- gate_verdict

GATES = ("G1", "G2", "G3", "G4", "G5")


def _model(**over):
    g = {k: "PASS" for k in GATES}
    g.update(over)
    return g


def test_verdict_all_pass_is_feasible():
    verdict, _ = gate_verdict({1729: _model(), 2718: _model(), 3141: _model()})
    assert verdict == "FEASIBLE"


def test_verdict_g1_fail_is_not_feasible_even_with_inconclusive_gates():
    per = {1729: _model(G2="INCONCLUSIVE", G3="NOT_RUN", G4="NOT_RUN", G5="NOT_RUN"),
           2718: _model(G1="FAIL", G2="NOT_RUN", G3="NOT_RUN", G4="NOT_RUN", G5="NOT_RUN"),
           3141: _model(G1="INCONCLUSIVE", G2="NOT_RUN", G3="NOT_RUN", G4="NOT_RUN",
                        G5="NOT_RUN")}
    verdict, _ = gate_verdict(per)
    assert verdict == "NOT_FEASIBLE"


def test_verdict_g2_inconclusive_names_g2_and_model():
    per = {1729: _model(), 2718: _model(G2="INCONCLUSIVE"), 3141: _model()}
    verdict, reason = gate_verdict(per)
    assert verdict == "INCONCLUSIVE"
    assert "G2" in reason and "2718" in reason


def test_verdict_names_first_gate_in_g1_to_g5_order():
    per = {1729: _model(G3="FAIL", G4="NOT_RUN", G5="NOT_RUN"),
           2718: _model(G2="INCONCLUSIVE"),
           3141: _model()}
    verdict, reason = gate_verdict(per)
    assert verdict == "INCONCLUSIVE"
    assert "G2" in reason and "2718" in reason


def test_verdict_not_run_after_later_failure_is_inconclusive():
    per = {1729: _model(G2="FAIL", G3="NOT_RUN", G4="NOT_RUN", G5="NOT_RUN"),
           2718: _model(), 3141: _model()}
    verdict, reason = gate_verdict(per)
    assert verdict == "INCONCLUSIVE"
    assert "G2" in reason and "1729" in reason


@pytest.mark.parametrize("gate,status", [("G5", "NOT_RUN"), ("G4", "FAIL"), ("G1", "INCONCLUSIVE"),
                                         ("G3", "INCONCLUSIVE")])
def test_verdict_any_single_non_pass_blocks_feasible(gate, status):
    per = {1729: _model(), 2718: _model(), 3141: _model(**{gate: status})}
    verdict, reason = gate_verdict(per)
    assert verdict == "INCONCLUSIVE"
    assert gate in reason and "3141" in reason
