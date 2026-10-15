"""Independent tests (author B, job 0026), TEST_PLAN B-3 part 2: Haar frames and the M1 identities.

Protocol §6 (positive-diagonal QR, frame streams, same frame on both arms, M1 comparison
definitions with the zero-norm and zero-spectrum rules) and §22.3 flag F3 (an exactly zero
diagonal entry of R gives a frame that fails orthonormality); API.md §9. Written from the
protocol and the four contract documents only; no tools/c1prime source was read and nothing was
executed by the author. References: `numpy.linalg.qr` with the sign fix, and SeedTree streams.

Ambiguity recorded: API.md names `m1_report(W, Delta_pm, Qt, frames, c_pm)` without fixing the
container of the two arms; these tests pass `(plus, minus)` tuples.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
from topo_pilot.contracts import SeedTree

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_fit  # noqa: E402

pytestmark = pytest.mark.analysis

D = 128
TWO_PI = 2.0 * np.pi


def _status(res) -> str:
    return res if isinstance(res, str) else res["status"]


def _qr_pos(M) -> np.ndarray:
    Q, R = np.linalg.qr(M)
    return Q * np.sign(np.diag(R))


def _f(phi) -> np.ndarray:
    return np.column_stack((np.cos(phi), np.sin(phi)))


def _frame(model_seed, r) -> np.ndarray:
    g = SeedTree(0).generator("c1-sf-v1", "frame", model_seed, r).standard_normal((D, 2))
    return _qr_pos(g)


def _family(seed, rows=24):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(D, D))
    lam, U = np.linalg.eigh(A @ A.T / D + 0.5 * np.eye(D))
    W, W_inv = (U * lam**-0.5) @ U.T, (U * lam**0.5) @ U.T
    B = rng.normal(size=(D, 2))
    phi_s, phi_p, phi_m = (rng.uniform(0.0, TWO_PI, rows) for _ in range(3))
    Dp, Dm = (_f(phi_p) - _f(phi_s)) @ B.T, (_f(phi_m) - _f(phi_s)) @ B.T
    Qt = _qr_pos(W @ B)
    return {"W": W, "W_inv": W_inv, "B": B, "Dp": Dp, "Dm": Dm, "Qt": Qt,
            "cp": (Dp @ W.T) @ Qt, "cm": (Dm @ W.T) @ Qt,
            "frames": [_frame(1729, r) for r in range(32)]}


@pytest.fixture(scope="module")
def fam():
    return _family(1)


def _m1(f, Dp=None, Dm=None, cp=None, cm=None, frames=None):
    return c1_fit.m1_report(
        f["W"], (f["Dp"] if Dp is None else Dp, f["Dm"] if Dm is None else Dm), f["Qt"],
        f["frames"] if frames is None else frames,
        (f["cp"] if cp is None else cp, f["cm"] if cm is None else cm))


# --- sign conventions and streams ----------------------------------------------------------------


def test_qr_pos_matches_numpy_with_a_positive_diagonal():
    rng = np.random.default_rng(2)
    M = rng.normal(size=(D, 2))
    M[:, 0] = -np.abs(M[:, 0]) - 0.1  # forces at least one sign flip
    got = np.asarray(c1_fit.qr_pos(M))
    assert np.array_equal(got, _qr_pos(M))
    R = got.T @ M
    assert R[0, 0] > 0 and R[1, 1] > 0 and abs(R[1, 0]) <= 1e-12
    np.testing.assert_allclose(got.T @ got, np.eye(2), rtol=0, atol=1e-14)


def test_haar_frames_are_the_seeded_streams():
    frames = c1_fit.haar_frames(1729)
    assert len(frames) == 32
    for r, Q in enumerate(frames):
        assert np.array_equal(np.asarray(Q), _frame(1729, r))
    three = c1_fit.haar_frames(2718, count=3)
    assert len(three) == 3
    for r in range(3):
        assert np.array_equal(np.asarray(three[r]), _frame(2718, r))
        assert not np.array_equal(np.asarray(three[r]), _frame(1729, r))


def test_primary_coordinates_basis_and_isometry(fam):
    Qt, c = c1_fit.primary_coords(fam["W"], fam["B"], fam["Dp"])
    np.testing.assert_allclose(np.asarray(Qt), fam["Qt"], rtol=0, atol=1e-13)
    np.testing.assert_allclose(np.asarray(c), fam["cp"], rtol=0, atol=1e-12)
    wd = np.linalg.norm(fam["Dp"] @ fam["W"].T, axis=1)
    np.testing.assert_allclose(np.linalg.norm(np.asarray(c), axis=1), wd, rtol=1e-12)


def test_control_displacement_isometry_and_the_same_frame_on_both_arms(fam):
    W, W_inv = fam["W"], fam["W_inv"]
    for r in (0, 7, 31):
        Q = fam["frames"][r]
        dp = np.asarray(c1_fit.control_delta(W_inv, Q, fam["cp"]))
        dm = np.asarray(c1_fit.control_delta(W_inv, Q, fam["cm"]))
        np.testing.assert_allclose(dp, (fam["cp"] @ Q.T) @ W_inv.T, rtol=0, atol=1e-12)
        wp, wm = dp @ W.T, dm @ W.T
        np.testing.assert_allclose(np.linalg.norm(wp, axis=1),
                                   np.linalg.norm(fam["cp"], axis=1), rtol=1e-10)
        # pair mapping: the inner product of the two arms is preserved only by a shared frame
        np.testing.assert_allclose(np.sum(wp * wm, axis=1),
                                   np.sum(fam["cp"] * fam["cm"], axis=1), rtol=0, atol=1e-10)


# --- M1 (§6 comparison definitions) --------------------------------------------------------------


def test_m1_passes_on_a_consistent_family(fam):
    assert _status(_m1(fam)) == "PASS"


def test_m1_fails_on_a_frame_that_is_not_orthonormal(fam):
    frames = list(fam["frames"])
    frames[5] = frames[5] * (1.0 + 1e-11)  # norm/spectrum within 1e-10, orthonormality 2e-11
    assert _status(_m1(fam, frames=frames)).startswith("FAIL_TECHNICAL")


def test_m1_fails_when_the_coordinates_lose_norm(fam):
    assert _status(_m1(fam, cp=fam["cp"] * 0.99)).startswith("FAIL_TECHNICAL")


def test_m1_fails_when_the_displacement_leaves_span_WB(fam):
    extra = np.zeros_like(fam["Dp"])
    extra[:, 0] = 1e-3  # c (from span(W B) only) no longer carries the full whitened norm
    assert _status(_m1(fam, Dp=fam["Dp"] + extra)).startswith("FAIL_TECHNICAL")


def test_m1_zero_primary_norm_requires_exact_zeros(fam):
    Dp, cp = fam["Dp"].copy(), fam["cp"].copy()
    Dp[0], cp[0] = 0.0, 0.0
    assert _status(_m1(fam, Dp=Dp, cp=cp)) == "PASS"
    cp_bad = cp.copy()
    cp_bad[0, 0] = 1e-300
    assert _status(_m1(fam, Dp=Dp, cp=cp_bad)).startswith("FAIL_TECHNICAL")


def test_m1_all_zero_displacements_use_the_zero_spectrum_rule(fam):
    z, zc = np.zeros_like(fam["Dp"]), np.zeros_like(fam["cp"])
    assert _status(_m1(fam, Dp=z, Dm=z.copy(), cp=zc, cm=zc.copy())) == "PASS"


def test_m1_frame_from_an_exactly_rank_deficient_draw_fails(fam):
    M = np.random.default_rng(3).normal(size=(D, 2))
    M[:, 1] = 0.0  # R[1, 1] = 0 exactly, so sign() = 0 zeroes the column (flag F3)
    bad = np.asarray(c1_fit.qr_pos(M))
    assert np.all(bad[:, 1] == 0.0)
    frames = list(fam["frames"])
    frames[0] = bad
    assert _status(_m1(fam, frames=frames)).startswith("FAIL_TECHNICAL")
