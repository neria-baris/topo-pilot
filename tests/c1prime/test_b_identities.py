"""Independent tests (author B, job 0026), TEST_PLAN B-1: the A identities and kernels C4-C6.

Protocol §1.2, §12.1 and §15.3.16 item 5 (v4 review fix 4); API.md §11. Written from the
protocol and the four contract documents only. No tools/c1prime source was read, and the
author executed nothing. Expected values are exact Fractions on dyadic fixtures (every float64
operation of the prescribed kernels is then exact) or 60-digit Decimal evaluations of the
protocol formulas.

The zero patch (§15.1) leaves both arms' logits bitwise equal, so it is covered by the
equal-arm cases. API.md does not say whether `A_logsoftmax` re-normalises its log-probability
inputs; every case here passes properly normalised log-probabilities, which makes the two
readings agree.
"""

from __future__ import annotations

import sys
from decimal import Decimal, localcontext
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

pytestmark = pytest.mark.analysis

V = 36
ROWS = 4


def _fr(x) -> Fraction:
    return Fraction(float(x))


def _dec(x) -> Decimal:
    return Decimal(float(x))


def _dyadic(seed, equal_mass=False):
    """q = k/4096 and logits = j/64: every product and 36-term sum used below is exact."""
    rng = np.random.default_rng(seed)
    kp = rng.integers(1, 200, size=(ROWS, V))
    km = rng.permuted(kp, axis=1) if equal_mass else rng.integers(1, 200, size=(ROWS, V))
    jp = rng.integers(-400, 400, size=(ROWS, V))
    jm = rng.integers(-400, 400, size=(ROWS, V))
    return kp / 4096.0, km / 4096.0, jp / 64.0, jm / 64.0


def _exact_logit_A(qp, qm, zp, zm, i) -> Fraction:
    terms = ((_fr(qp[i, v]) - _fr(qm[i, v])) * (_fr(zp[i, v]) - _fr(zm[i, v])) for v in range(V))
    return sum(terms, Fraction(0)) / 2


def _delta_m(qp, qm, i) -> Fraction:
    return sum((_fr(qp[i, v]) - _fr(qm[i, v]) for v in range(V)), Fraction(0))


def _lse(row) -> Decimal:
    return sum((_dec(z).exp() for z in row), Decimal(0)).ln()


def _log_softmax(z) -> np.ndarray:
    out = np.empty_like(z)
    with localcontext() as ctx:
        ctx.prec = 60
        for i in range(z.shape[0]):
            lse = _lse(z[i])
            out[i] = [float(_dec(x) - lse) for x in z[i]]
    return out


def _vec(x) -> np.ndarray:
    return np.asarray(x, dtype=np.float64).reshape(-1)


# --- logit-difference form (C4), exact on dyadic fixtures -------------------------------------


def test_logit_difference_form_is_the_exact_rational_on_dyadic_fixture():
    qp, qm, zp, zm = _dyadic(1)
    A = _vec(c1_endpoint.A_hat(qp - qm, zp, zm))
    assert A.shape == (ROWS,)
    for i in range(ROWS):
        assert _fr(A[i]) == _exact_logit_A(qp, qm, zp, zm, i)


@pytest.mark.parametrize("k", [0.375, -2.5, 7.0])
def test_symbol_constant_arm_difference_contributes_half_k_delta_m(k):
    qp, qm, zp, zm = _dyadic(2)
    d = qp - qm
    base = _vec(c1_endpoint.A_hat(d, zp, zm))
    shifted = _vec(c1_endpoint.A_hat(d, zp + k, zm))
    for i in range(ROWS):
        dm = _delta_m(qp, qm, i)
        assert dm != 0  # non-stochastic fixture: delta_m != 0
        assert _fr(shifted[i]) - _fr(base[i]) == Fraction(k) * dm / 2


def test_symbol_constant_cancels_exactly_when_masses_are_equal():
    qp, qm, zp, zm = _dyadic(3, equal_mass=True)
    d = qp - qm
    for i in range(ROWS):
        assert _delta_m(qp, qm, i) == 0
    assert np.array_equal(c1_endpoint.A_hat(d, zp + 3.25, zm), c1_endpoint.A_hat(d, zp, zm))


def test_arm_common_additive_perturbation_cancels_exactly():
    qp, qm, zp, zm = _dyadic(4)
    c = np.random.default_rng(40).integers(-300, 300, size=(ROWS, V)) / 128.0
    d = qp - qm
    assert np.array_equal(c1_endpoint.A_hat(d, zp + c, zm + c), c1_endpoint.A_hat(d, zp, zm))


@pytest.mark.parametrize("beta", [0.5, 0.75, 2.0])
def test_common_inverse_temperature_scales_the_logit_form_exactly(beta):
    qp, qm, zp, zm = _dyadic(5)
    d = qp - qm
    A = _vec(c1_endpoint.A_hat(d, zp, zm))
    Ab = _vec(c1_endpoint.A_hat(d, beta * zp, beta * zm))
    for i in range(ROWS):
        assert _fr(Ab[i]) == Fraction(beta) * _fr(A[i])


def test_logit_form_equals_log_softmax_form_exactly_when_sum_d_is_zero():
    # With sum_v d_v = 0 the exact log-softmax form is 1/2 sum d (z+ - z-) - 1/2 dlse * 0, a
    # rational that the dyadic logit form reproduces exactly.
    qp, qm, zp, zm = _dyadic(6, equal_mass=True)
    A = _vec(c1_endpoint.A_hat(qp - qm, zp, zm))
    for i in range(ROWS):
        assert _delta_m(qp, qm, i) == 0
        assert _fr(A[i]) == _exact_logit_A(qp, qm, zp, zm, i)
    A_ls = _vec(c1_endpoint.A_logsoftmax(qp, qm, _log_softmax(zp), _log_softmax(zm)))
    assert np.max(np.abs(A_ls - A)) <= 1e-12


def test_equal_arms_give_exactly_zero():
    rng = np.random.default_rng(7)
    qp, qm = rng.random((5, V)), rng.random((5, V))
    z = rng.normal(size=(5, V)) * 3.0
    assert np.all(_vec(c1_endpoint.A_hat(qp - qm, z, z.copy())) == 0.0)
    lp = _log_softmax(z)
    assert np.all(_vec(c1_endpoint.A_logsoftmax(qp, qm, lp, lp.copy())) == 0.0)


# --- log-softmax form against 60-digit Decimal evaluations -----------------------------------


def _masses_fixture(seed, masses, rows=2):
    rng = np.random.default_rng(seed)
    bp, bm = rng.random((rows, V)) + 0.05, rng.random((rows, V)) + 0.05
    qp = bp / bp.sum(axis=1, keepdims=True) * masses[0]
    qm = bm / bm.sum(axis=1, keepdims=True) * masses[1]
    return qp, qm


def _G_dec(qp_row, qm_row) -> Decimal:
    terms = ((_dec(a) - _dec(b)) * (_dec(a).ln() - _dec(b).ln()) for a, b in zip(qp_row, qm_row))
    return sum(terms, Decimal(0)) / 2


@pytest.mark.parametrize("masses", [(1.003, 0.998), (1.0, 1.0)])
def test_oracle_perfect_readout_gives_G_minus_mass_correction(masses):
    qp, qm = _masses_fixture(8, masses)
    lpp, lpm, target, G = [], [], [], []
    with localcontext() as ctx:
        ctx.prec = 60
        for i in range(qp.shape[0]):
            mp = sum((_dec(x) for x in qp[i]), Decimal(0))
            mm = sum((_dec(x) for x in qm[i]), Decimal(0))
            lpp.append([float((_dec(x) / mp).ln()) for x in qp[i]])
            lpm.append([float((_dec(x) / mm).ln()) for x in qm[i]])
            G.append(_G_dec(qp[i], qm[i]))
            target.append(G[-1] - (mp - mm) * (mp / mm).ln() / 2)
    A = _vec(c1_endpoint.A_logsoftmax(qp, qm, np.array(lpp), np.array(lpm)))
    for i in range(qp.shape[0]):
        assert abs(A[i] - float(target[i])) <= 1e-13
        if masses[0] != masses[1]:
            assert abs(float(target[i] - G[i])) > 1e-7  # the correction is not negligible
        else:
            assert abs(A[i] - float(G[i])) <= 1e-13


def test_log_softmax_form_differs_from_logit_form_by_the_normaliser_term():
    # Masses fixed at 1.06 and 0.95 (delta_m ~ 0.11) and zm = zp + 0.7 + 0.1 eps, so that
    # lse(zp) - lse(zm) lies in [-0.7 - 0.1 max eps, -0.7 - 0.1 min eps] and |corr| >= ~0.01.
    qp, qm = _masses_fixture(9, (1.06, 0.95), rows=3)
    rng = np.random.default_rng(9)
    zp = rng.normal(size=(3, V))
    zm = zp + 0.7 + 0.1 * rng.normal(size=(3, V))
    A_logit = _vec(c1_endpoint.A_hat(qp - qm, zp, zm))
    A_ls = _vec(c1_endpoint.A_logsoftmax(qp, qm, _log_softmax(zp), _log_softmax(zm)))
    with localcontext() as ctx:
        ctx.prec = 60
        for i in range(3):
            dm = sum((_dec(a) - _dec(b) for a, b in zip(qp[i], qm[i])), Decimal(0))
            corr = float(dm * (_lse(zp[i]) - _lse(zm[i])) / 2)
            assert abs(corr) > 1e-3
            assert abs((A_ls[i] - A_logit[i]) + corr) <= 1e-13


@pytest.mark.parametrize("beta,masses", [(0.6, (1.004, 0.997)), (1.7, (1.004, 0.997)),
                                         (0.6, (1.0, 1.0))])
def test_common_inverse_temperature_identity_for_log_probabilities(beta, masses):
    qp, qm = _masses_fixture(10, masses)
    rng = np.random.default_rng(11)
    zp, zm = rng.normal(size=qp.shape), rng.normal(size=qp.shape)
    lp_rows, lpb_rows, A_dec, Ab_dec, corr = [[], []], [[], []], [], [], []
    with localcontext() as ctx:
        ctx.prec = 60
        bd = Decimal(beta)
        for i in range(qp.shape[0]):
            lnZ, ells, ellbs = [], [], []
            for k, z in enumerate((zp[i], zm[i])):
                lse = _lse(z)
                ell = [_dec(x) - lse for x in z]
                Zb = sum(((e * bd).exp() for e in ell), Decimal(0))
                ellb = [e * bd - Zb.ln() for e in ell]
                lnZ.append(Zb.ln())
                ells.append(ell)
                ellbs.append(ellb)
                lp_rows[k].append([float(e) for e in ell])
                lpb_rows[k].append([float(e) for e in ellb])
            dv = [_dec(a) - _dec(b) for a, b in zip(qp[i], qm[i])]
            A_dec.append(sum((x * (a - b) for x, a, b in zip(dv, *ells)), Decimal(0)) / 2)
            Ab_dec.append(sum((x * (a - b) for x, a, b in zip(dv, *ellbs)), Decimal(0)) / 2)
            corr.append(sum(dv, Decimal(0)) * (lnZ[0] - lnZ[1]) / 2)
            # the protocol identity itself, at 60 digits
            assert abs(Ab_dec[i] - (bd * A_dec[i] - corr[i])) < Decimal(10) ** -50
    A = _vec(c1_endpoint.A_logsoftmax(qp, qm, np.array(lp_rows[0]), np.array(lp_rows[1])))
    Ab = _vec(c1_endpoint.A_logsoftmax(qp, qm, np.array(lpb_rows[0]), np.array(lpb_rows[1])))
    for i in range(qp.shape[0]):
        assert abs(A[i] - float(A_dec[i])) <= 1e-13
        assert abs(Ab[i] - float(Ab_dec[i])) <= 1e-13
        assert abs(Ab[i] - (beta * A[i] - float(corr[i]))) <= 3e-13
        if masses[0] == masses[1]:
            assert abs(float(corr[i])) <= 1e-14  # A_beta = beta A when delta_m = 0


# --- C5 and C6 kernels, bitwise -----------------------------------------------------------------


def _c5_c6(A_T, A_C, G, A_full):
    m = np.array(A_C[0], dtype=np.float64)
    for r in range(1, 32):
        m = m + A_C[r]
    m = m * 0.03125
    Y = A_T - m
    return Y, Y - 0.1 * G, A_full - 0.3 * G


def test_Y_Z_Zfull_kernels_follow_C5_and_C6_bitwise():
    rng = np.random.default_rng(12)
    R = 7
    A_T, A_full, G = rng.normal(size=R) * 0.3, rng.normal(size=R), rng.random(R) * 0.2
    A_C = [rng.normal(size=R) * 10.0 ** int(rng.integers(-6, 1)) for _ in range(32)]
    Y, Z, Zf = _c5_c6(A_T, A_C, G, A_full)
    assert np.array_equal(_vec(c1_endpoint.Y_hat(A_T, A_C)), Y)
    assert np.array_equal(_vec(c1_endpoint.Z_hat(Y, G)), Z)
    assert np.array_equal(_vec(c1_endpoint.Zfull_hat(A_full, G)), Zf)


def test_frame_mean_is_an_ordered_left_to_right_sum():
    # 2**53 + 1 + 1 is 2**53 left to right (two ties to even), but 2**53 + 2 in other orders.
    A_C = [np.array([2.0**53]), np.array([1.0]), np.array([1.0])]
    A_C += [np.array([0.0]) for _ in range(29)]
    Y = _vec(c1_endpoint.Y_hat(np.array([0.0]), A_C))
    assert Y[0] == -(2.0**48)


def test_zero_patch_contrast_and_scores():
    rng = np.random.default_rng(13)
    qp, qm = rng.random((3, V)), rng.random((3, V))
    z = rng.normal(size=(3, V))
    A0 = _vec(c1_endpoint.A_hat(qp - qm, z, z))
    zeros = [A0.copy() for _ in range(32)]
    G = rng.random(3)
    Y = _vec(c1_endpoint.Y_hat(A0, zeros))
    assert np.all(Y == 0.0)
    assert np.array_equal(_vec(c1_endpoint.Z_hat(Y, G)), Y - 0.1 * G)
