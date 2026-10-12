"""T12 (circular coordinates), T13 (PCA contract)."""
import numpy as np
import pytest
from scipy.spatial.distance import cdist

from topo_pilot.topology import CircularCoordinates, DistancePipeline, Euclidean

pytestmark = pytest.mark.topology


def circular_agreement(a, b):
    """Resultant length of (a -+ b): 1 means equal up to rotation, sign allowed."""
    return max(abs(np.mean(np.exp(1j * (a - b)))), abs(np.mean(np.exp(1j * (a + b)))))


@pytest.mark.slow
def test_T12_circular_coordinates_recover_angle():
    rng = np.random.default_rng(0)
    m, ambient = 200, 128
    theta = rng.uniform(0, 2 * np.pi, m)
    frame, _ = np.linalg.qr(rng.normal(size=(ambient, 2)))
    X = np.c_[np.cos(theta), np.sin(theta)] @ frame.T + 0.05 * rng.normal(size=(m, ambient))
    ang = np.asarray(CircularCoordinates(coeff_p=47).fit_transform(cdist(X, X)))
    assert ang.shape == (m,)
    assert ang.min() >= 0.0 and ang.max() < 2 * np.pi
    # circular correlation up to orientation and rotation (the cocycle fixes neither)
    assert circular_agreement(ang, theta) > 0.95


def test_T13_pca_fit_on_one_set_applied_to_another():
    rng = np.random.default_rng(1)
    X_fit = rng.normal(size=(200, 20)) @ np.diag(np.linspace(5.0, 0.2, 20))
    X_other = rng.normal(size=(60, 20)) @ np.diag(np.linspace(0.2, 5.0, 20))  # other covariance
    k = 4
    pipe = DistancePipeline(Euclidean(), pca_dims=k)
    fitted = pipe.fit_pca(X_fit)
    assert fitted is not None
    res = pipe.compute(X_other, [f"q{i}" for i in range(60)])
    # Expected: centre on the FIT mean, project on the fit's top-k right singular vectors.
    mu = X_fit.mean(axis=0)
    _, _, vt = np.linalg.svd(X_fit - mu, full_matrices=False)
    Y = (X_other - mu) @ vt[:k].T
    np.testing.assert_allclose(res.D, cdist(Y, Y), rtol=1e-6, atol=1e-8)
    # the dimension is respected: differs from full-dimensional distances
    assert not np.allclose(res.D, cdist(X_other, X_other), rtol=1e-3)
    # and differs from a PCA fitted on the other set (no refit inside compute)
    _, _, vt2 = np.linalg.svd(X_other - X_other.mean(axis=0), full_matrices=False)
    Y2 = (X_other - X_other.mean(axis=0)) @ vt2[:k].T
    assert not np.allclose(res.D, cdist(Y2, Y2), rtol=1e-3)


def test_T13_pca_none_is_noop():
    X = np.random.default_rng(2).normal(size=(40, 10))
    res = DistancePipeline(Euclidean(), pca_dims=None).compute(X, [f"q{i}" for i in range(40)])
    np.testing.assert_allclose(res.D, cdist(X, X), rtol=1e-9, atol=1e-9)
