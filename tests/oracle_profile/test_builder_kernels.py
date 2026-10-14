"""BUILDER tests (not independent): hardened kernel invariants from the pre-freeze review.

Written by the job-0014 builder; see BUILDER_TESTS.md. Independent numerical tests are in the
other test files (separate author, frozen at 027e3e0).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.oracle
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "x4_oracle_profile"))
import oracle_profile as op  # noqa: E402

T = np.array([[0.5, 0.5], [0.25, 0.75]])
E = np.array([[0.9, 0.1], [0.2, 0.8]])
PI = np.array([1 / 3, 2 / 3])
TOK = np.array([[0, 1, 1]])


def test_valid_baseline():
    post = op.suffix_posterior(T, E, PI, TOK, 2)
    assert post.shape == (1, 2) and abs(post.sum() - 1) < 1e-15


@pytest.mark.parametrize(
    "bad",
    [
        {"T": np.array([[np.nan, 1.0], [0.25, 0.75]])},
        {"E": np.array([[np.inf, 0.1], [0.2, 0.8]])},
        {"pi": np.array([-0.1, 1.1])},
        {"T": np.eye(3)},
        {"E": np.ones((3, 2)) / 2},
        {"pi": [[0.5, 0.5]]},
        {"T": [[0.5, 0.5], [0.25]]},
        {"E": "abc"},
    ],
)
def test_kernel_rejects_invalid_model(bad):
    args = {"T": T, "E": E, "pi": PI, **bad}
    with pytest.raises(op.ProfileError):
        op.suffix_posterior(args["T"], args["E"], args["pi"], TOK, 2)


def test_infinite_mass_rejected():
    huge = np.full((2, 2), 1e308)
    with pytest.raises(op.ProfileError):
        op.suffix_posterior(huge, huge, np.array([1e308, 1e308]), TOK, 1)


def test_posterior_means_contract():
    with pytest.raises(op.ProfileError):
        op.posterior_means(T, E, PI, TOK, (), np.ones((2, 2)))
    with pytest.raises(op.ProfileError):
        op.posterior_means(T, E, PI, TOK, (1,), np.ones((2, 3)))
    with pytest.raises(op.ProfileError):
        op.posterior_means(T, E, PI, TOK, (1,), np.ones((3, 2)))


def test_residual_rows_rejects_nonfinite_and_shape():
    good = np.zeros((3, 2))
    for bad in (np.full((3, 2), np.nan), np.zeros((3, 3)), np.zeros(3), "x"):
        with pytest.raises(op.ProfileError):
            op.residual_rows({32: good, 1: bad})
        with pytest.raises(op.ProfileError):
            op.residual_rows({32: bad, 1: good})


def test_profile_point_and_bootstrap_error_paths():
    rng = np.random.Generator(np.random.PCG64(0))
    with pytest.raises(op.ProfileError):
        op.profile_point({}, {})
    with pytest.raises(op.ProfileError):
        op.profile_point({1: np.array([np.nan])}, {1: np.array([1.0])})
    rows = {1: np.array([1.0, 2.0])}
    for norm, sq, ks, draws in (
        (rows, rows, (), 3),
        ({1: np.float64(1.0)}, rows, (1,), 3),
        (rows, rows, (2,), 3),
        (rows, rows, (1,), True),
        ({1: [[1.0, 2.0]]}, rows, (1,), 3),
    ):
        with pytest.raises(op.ProfileError):
            op.bootstrap_profile(norm, sq, ks, rng, draws)


def test_percentile_interval_rejects_bad_probs():
    for probs in ([], [1.5], [np.nan]):
        with pytest.raises(op.ProfileError):
            op.percentile_interval(np.arange(4.0), probs)
    with pytest.raises(op.ProfileError):
        op.percentile_interval(np.array([1.0, np.inf]), [0.5])


def test_malformed_inputs_raise_profile_error():
    with pytest.raises(op.ProfileError):
        op.suffix_posterior(T, E, PI, [[0, 1], [1]], 1)
    with pytest.raises(op.ProfileError):
        op.circle_features([[0], [1, 2]])
    with pytest.raises(op.ProfileError):
        op.canonical_emission([[0.5, 0.5], [1.0]], np.array([1, 0]))
