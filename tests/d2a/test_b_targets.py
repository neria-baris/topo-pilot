"""Independent tests (author B, job 0028): T-BETA, ``d2a_targets.beta`` and ``band_edge_table``.

Written from D2A-FROZEN-v1 (§0, §3.1, §3.3, §3.5, §6, §9.4, §11.4) and tools/d2a/API.md (§2.2)
only; no tools/d2a source was read. Every expected value is computed here from the unchanged
``BayesFilter`` / ``FutureOperator`` on ``d1_seam.float_model()``; nothing is taken from
``d2a_targets`` itself.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.oracle import BayesFilter, FutureOperator

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/d2a", "tools/d1_seam", "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import d1_seam  # noqa: E402
import d2a_targets  # noqa: E402

S0, S2, S3, A, B = range(5)
TOL = 1e-12
KEYS = ("ep", "p", "d", "r8", "rm")


# ---------------------------------------------------------------- beta(r, d) on hand inputs

def test_beta_oracle_is_one_and_pi_blind_is_zero():
    d = np.array([0.3, -0.1, 0.25, 0.0, -0.4])
    value, status = d2a_targets.beta(d.copy(), d)
    assert status == "ok" and value == pytest.approx(1.0, abs=1e-15)
    value, status = d2a_targets.beta(np.zeros_like(d), d)  # pi-blind: r = 0 exactly (§6)
    assert status == "ok" and value == 0.0


def test_beta_is_slope_through_origin_on_hand_example():
    # sum r*d = 1 + 2 + 6 = 9; sum d^2 = 1 + 1 + 4 = 6; slope 3/2 (no intercept)
    value, status = d2a_targets.beta(np.array([1.0, 2.0, 3.0]), np.array([1.0, 1.0, 2.0]))
    assert status == "ok" and value == pytest.approx(1.5, abs=1e-15)
    # an intercept fit would give a different number: r = d + 5 has slope-through-origin
    # (sum d^2 + 5 sum d) / sum d^2 = (6 + 20) / 6
    value, _ = d2a_targets.beta(np.array([6.0, 6.0, 7.0]), np.array([1.0, 1.0, 2.0]))
    assert value == pytest.approx(26.0 / 6.0, abs=1e-14)


def test_beta_pools_two_dimensional_contrasts():
    r = np.array([[1.0, 0.0], [2.0, 1.0]])
    d = np.array([[1.0, 1.0], [0.0, 2.0]])
    # pooled: (1 + 0 + 0 + 2) / (1 + 1 + 0 + 4) = 0.5; the mean of per-column slopes is 0.7
    value, status = d2a_targets.beta(r, d)
    assert status == "ok" and value == pytest.approx(0.5, abs=1e-15)


def test_beta_scale_and_sign():
    d = np.array([[0.02, -0.01], [0.005, 0.0]])
    assert d2a_targets.beta(-2.0 * d, d)[0] == pytest.approx(-2.0, abs=1e-14)
    assert d2a_targets.beta(0.25 * d, d)[0] == pytest.approx(0.25, abs=1e-14)


@pytest.mark.parametrize("d", [
    np.zeros(4),                                  # sum d^2 = 0 (all rows uninformed)
    np.zeros((3, 2)),
    np.array([0.1, np.nan, 0.2]),                 # non-finite contrast
    np.array([0.1, np.inf]),
    np.array([1e200, 1e200]),                     # sum d^2 overflows to inf: not finite
])
def test_beta_undefined_denominator(d):
    assert d2a_targets.beta(np.ones_like(d), d) == (None, "UNDEFINED")


def test_beta_tiny_positive_denominator_is_defined():
    # "not positive and finite" is the only undefined case; a tiny positive sum is defined
    value, status = d2a_targets.beta(np.array([3e-100]), np.array([1e-100]))
    assert status == "ok" and value == pytest.approx(3.0, rel=1e-12)


# ------------------------------------------------------------ independent oracle reference

def _pad(history):
    return list(history) + [S0] * (33 - len(history))


@pytest.fixture(scope="module")
def fm():
    return d1_seam.float_model()


@pytest.fixture(scope="module")
def tokens(fm):
    """64 natural C/M episodes plus the padded canonical pair (w_12..w_33 = sigma0, so p = 33
    carries sigma0 and must never be selected)."""
    rng = np.random.default_rng(2026101599)
    tok, _ = HMMSampler(fm["T"], fm["E_mix"], fm["mu"], SequenceLayout()).sample(64, rng)
    extra = np.array([_pad(d1_seam.H_A), _pad(d1_seam.H_B)], dtype=np.uint8)
    return np.vstack([np.asarray(tok, dtype=np.uint8), extra])


@pytest.fixture(scope="module")
def ref(fm, tokens):
    """q, q_half [R, 33, 5]: index p = law of w_{p+1} after w_{1:p} (mixture, pi-blind)."""
    tok = tokens[:, :32].astype(np.int64)
    q = BayesFilter(fm["T"], fm["E_mix"], fm["mu"]).run(tok).q
    q_c = BayesFilter(fm["T_C"], fm["E"], fm["mu_C"]).run(tok).q
    q_m = BayesFilter(fm["T_M"], fm["E"], fm["mu_M"]).run(tok).q
    w8 = np.empty_like(q)
    for p in range(1, 33):  # §3.5: m_p = min(8, p), prior mu T^(p - m_p), window w_{p-m_p+1..p}
        m = min(8, p)
        prior = fm["mu"] @ np.linalg.matrix_power(fm["T"], p - m)
        w8[:, p] = BayesFilter(fm["T"], fm["E_mix"], prior).run(tok[:, p - m:p]).q[:, m]
    rows, cols = np.nonzero(np.isin(tokens[:, :32], (S0, S2)))
    p = cols + 1
    half = 0.5 * (q_c + q_m)

    def contrast(x):
        return (x[rows, p, A] - x[rows, p, B]) - (half[rows, p, A] - half[rows, p, B])

    return {"q": q, "half": half, "ep": rows, "p": p, "d": contrast(q), "r8": contrast(w8)}


def _table(out):
    if isinstance(out, dict):
        got = {k: None if out.get(k) is None else np.asarray(out[k]) for k in KEYS}
    else:  # a tuple in the documented order ep, p, d, r8, rm
        got = {k: np.asarray(v) for k, v in zip(KEYS, out)}
        got.setdefault("rm", None)
    order = np.lexsort((got["p"], got["ep"]))
    return {k: None if v is None else v[order] for k, v in got.items()}


def test_reference_has_informed_band_edges(ref):
    assert np.sum(ref["d"] ** 2) > 1e-6  # otherwise the beta checks below would be vacuous
    assert np.all((ref["p"] >= 1) & (ref["p"] <= 32))


def test_band_edge_table_selects_exactly_sigma0_sigma2_rows(tokens, ref):
    got = _table(d2a_targets.band_edge_table(tokens))
    np.testing.assert_array_equal(got["ep"].astype(np.int64), ref["ep"])
    np.testing.assert_array_equal(got["p"].astype(np.int64), ref["p"])
    # every selected position carries sigma0 or sigma2 and lies in 1..32 (never 33)
    ep, p = got["ep"].astype(np.int64), got["p"].astype(np.int64)
    assert set(np.unique(tokens[ep, p - 1])) <= {S0, S2}
    assert p.min() >= 1 and p.max() <= 32
    assert np.any(np.isin(tokens[:, 32], (S0, S2)))  # the p = 33 trap is present


def test_band_edge_d_equals_oracle_contrast(tokens, ref):
    got = _table(d2a_targets.band_edge_table(tokens))
    np.testing.assert_allclose(got["d"], ref["d"], rtol=0, atol=TOL)


def test_band_edge_r8_uses_the_exact_window8_law(tokens, ref):
    got = _table(d2a_targets.band_edge_table(tokens))
    np.testing.assert_allclose(got["r8"], ref["r8"], rtol=0, atol=TOL)
    early = got["p"] <= 8  # §3.5 / §6: window-8 equals the full-history oracle for p <= 8
    assert early.any()
    np.testing.assert_allclose(got["r8"][early], got["d"][early], rtol=0, atol=TOL)


def test_band_edge_oracle_model_gives_rm_equal_d_and_beta_one(tokens, ref):
    got = _table(d2a_targets.band_edge_table(tokens, q_model=ref["q"].copy()))
    np.testing.assert_allclose(got["rm"], got["d"], rtol=0, atol=TOL)
    value, status = d2a_targets.beta(got["rm"], got["d"])
    assert status == "ok" and value == pytest.approx(1.0, abs=1e-9)


def test_band_edge_pi_blind_model_gives_beta_zero(tokens, ref):
    got = _table(d2a_targets.band_edge_table(tokens, q_model=ref["half"].copy()))
    np.testing.assert_allclose(got["rm"], 0.0, rtol=0, atol=TOL)
    value, status = d2a_targets.beta(got["rm"], got["d"])
    assert status == "ok" and value == pytest.approx(0.0, abs=1e-9)


def test_band_edge_rm_reads_model_index_p(tokens, ref):
    """rm uses q_model[row, p] (index p sees w_1..w_p and predicts w_{p+1}); a model whose law
    is the oracle shifted by one index must not reproduce d."""
    shifted = ref["q"].copy()
    shifted[:, 1:] = ref["q"][:, :-1]
    got = _table(d2a_targets.band_edge_table(tokens, q_model=shifted))
    assert not np.allclose(got["rm"], got["d"], rtol=0, atol=1e-6)


# --------------------------------------------- beta_2 (§9.4) on oracle decision contrasts

def test_beta2_oracle_and_pi_blind_on_decision_contrasts(fm, tokens):
    tok = tokens[:, :31].astype(np.int64)
    b_mix = BayesFilter(fm["T"], fm["E_mix"], fm["mu"]).run(tok).b
    b_c = BayesFilter(fm["T_C"], fm["E"], fm["mu_C"]).run(tok).b
    b_m = BayesFilter(fm["T_M"], fm["E"], fm["mu_M"]).run(tok).b
    rows, cols = np.nonzero(tokens[:, :31] == S3)  # decision positions t <= 31
    J = FutureOperator(fm["T"], fm["E_mix"]).F2(b_mix[rows, cols]).reshape(-1, 25)
    J_c = FutureOperator(fm["T_C"], fm["E"]).F2(b_c[rows, cols]).reshape(-1, 25)
    J_m = FutureOperator(fm["T_M"], fm["E"]).F2(b_m[rows, cols]).reshape(-1, 25)
    J_half = 0.5 * (J_c + J_m)

    def con(x):  # (sigma2,A) - (sigma2,B), (sigma0,A) - (sigma0,B): indices 8, 9, 3, 4
        return np.stack([x[:, 8] - x[:, 9], x[:, 3] - x[:, 4]], axis=1)

    d = con(J - J_half)  # T_2 on the contrasts
    assert np.sum(d ** 2) > 1e-8  # the padded canonical pair is informed at t = 11
    value, status = d2a_targets.beta(con(J) - con(J_half), d)
    assert status == "ok" and value == pytest.approx(1.0, abs=1e-9)
    value, status = d2a_targets.beta(con(J_half) - con(J_half), d)
    assert status == "ok" and value == 0.0
