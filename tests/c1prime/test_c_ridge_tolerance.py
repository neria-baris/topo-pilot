"""Coordinator regression test (job 0042 review, ruling R13): `c1_fit.equivalence_tolerance`
is the M1 cho_solve-vs-lstsq tolerance max(1e-10, 64·ε·κ₂(Xc'Xc+λI)·‖pred‖∞). Synthetic only."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_fit  # noqa: E402


def _two_solvers(F, Y, lam):
    Xc, Yc = F - F.mean(axis=0), Y - Y.mean(axis=0)
    G = Xc.T @ Xc + lam * np.eye(F.shape[1])
    w_l = np.linalg.lstsq(G, Xc.T @ Yc, rcond=None)[0]
    w_c = cho_solve(cho_factor(G), Xc.T @ Yc)
    return Xc @ w_l, Xc @ w_c


def test_well_conditioned_keeps_frozen_1e10():
    rng = np.random.default_rng(1)
    F, Y = rng.standard_normal((2000, 50)), rng.standard_normal((2000, 2))
    p_l, p_c = _two_solvers(F, Y, 1.0)
    tol, kappa = c1_fit.equivalence_tolerance(F, 1.0, p_l)
    assert tol == 1e-10 and kappa < 1e3
    assert np.max(np.abs(p_l - p_c)) <= tol


def test_ill_conditioned_solver_gap_is_within_bound():
    rng = np.random.default_rng(2)
    z = rng.standard_normal((2000, 3))
    F = np.tanh(z @ rng.standard_normal((3, 300)) * 3) + 1e-4 * rng.standard_normal((2000, 300))
    Y = np.stack([np.sin(z[:, 0]), np.cos(z[:, 1])], axis=1)
    p_l, p_c = _two_solvers(F, Y, 1e-3)
    tol, kappa = c1_fit.equivalence_tolerance(F, 1e-3, p_l)
    assert kappa > 1e6 and tol > 1e-10
    assert np.max(np.abs(p_l - p_c)) <= tol


def test_implementation_mismatch_still_fails():
    rng = np.random.default_rng(3)
    F, Y = rng.standard_normal((2000, 50)), rng.standard_normal((2000, 2))
    p_l, _ = _two_solvers(F, Y, 1e-2)
    tol, _ = c1_fit.equivalence_tolerance(F, 1e-2, p_l)
    assert np.max(np.abs(p_l - 1.001 * p_l)) > tol
