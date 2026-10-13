"""T06, T07, T11 (gate G-A), plus shape / null-cloud contracts."""
import numpy as np
import pytest

from topo_pilot.topology import (
    DistancePipeline,
    Euclidean,
    NullClouds,
    PersistenceComputer,
    PHConfig,
    Summaries,
    SyntheticShapes,
)

pytestmark = pytest.mark.topology


def s_of(X):
    """H1 signal S of a point cloud under the Euclidean pipeline."""
    res = DistancePipeline(Euclidean()).compute(X, [str(i) for i in range(len(X))])
    diag = PersistenceComputer(PHConfig()).diagrams(res.D)
    return Summaries.S(diag, 1, res.scale_s)


def test_shape_generators_contract():
    for name in ("circle", "disk", "flat_torus"):
        f = getattr(SyntheticShapes, name)
        A = f(100, ambient=32, noise=0.05, rng=np.random.default_rng(1))
        B = f(100, ambient=32, noise=0.05, rng=np.random.default_rng(1))
        C = f(100, ambient=32, noise=0.05, rng=np.random.default_rng(2))
        assert A.shape == (100, 32) and np.all(np.isfinite(A))
        np.testing.assert_array_equal(A, B)  # same seed -> same cloud
        assert not np.array_equal(A, C)
    S2 = SyntheticShapes.sphere(80, dim=2, ambient=16, noise=0.05, rng=np.random.default_rng(3))
    assert S2.shape == (80, 16)


def test_null_clouds_contract():
    iso = NullClouds.isotropic(60, 12, np.random.default_rng(0))
    assert iso.shape == (60, 12)
    assert iso.std() > 0 and abs(iso.mean()) < 0.5  # scale convention unspecified
    X = np.random.default_rng(1).normal(size=(500, 6)) @ np.diag([5, 3, 2, 1, 0.5, 0.1])
    G = NullClouds.covariance_matched(X, np.random.default_rng(2))
    assert G.shape == X.shape
    # covariance of the null matches that of the data within sampling error
    np.testing.assert_allclose(np.cov(G.T), np.cov(X.T), rtol=0.4, atol=0.5)


def test_T06_circle_above_gaussian_floor():
    rng = np.random.default_rng(10)
    s_circle = s_of(SyntheticShapes.circle(200, ambient=128, noise=0.05, rng=rng))
    floor = np.mean([s_of(NullClouds.isotropic(200, 128, rng)) for _ in range(10)])
    assert s_circle > 0
    assert s_circle >= 3.0 * floor, (s_circle, floor)


def test_T07_disk_and_gaussian_below_threshold():
    # Threshold derivation (all quantities computed here, nothing hard-coded):
    #  * null level  = max S over 10 isotropic Gaussian draws (M=200, F=128).
    #    A fresh Gaussian cloud must not exceed 2x this null level.
    #  * signal level = mean S over 10 noisy circles (same M, F, noise).
    #    A disk has no H1 class, so its S must stay below half the circle signal
    #    (i.e. at least a factor 2 from the signal), and the disk must also be far
    #    below the circle.
    rng = np.random.default_rng(20)
    null = [s_of(NullClouds.isotropic(200, 128, rng)) for _ in range(10)]
    circles = [s_of(SyntheticShapes.circle(200, ambient=128, noise=0.05, rng=rng))
               for _ in range(10)]
    thr_gauss = 2.0 * max(null)
    thr_disk = 0.5 * float(np.mean(circles))
    assert thr_disk > 0
    s_gauss = s_of(NullClouds.isotropic(200, 128, rng))
    s_disk = s_of(SyntheticShapes.disk(200, ambient=128, noise=0.05, rng=rng))
    assert s_gauss <= thr_gauss, (s_gauss, thr_gauss)
    assert s_disk < thr_disk, (s_disk, thr_disk)


@pytest.mark.slow
def test_T11_gate_GA_circle_vs_disk():
    rng = np.random.default_rng(1234)
    circ = [s_of(SyntheticShapes.circle(512, ambient=128, noise=0.05, rng=rng))
            for _ in range(20)]
    disk = [s_of(SyntheticShapes.disk(512, ambient=128, noise=0.05, rng=rng))
            for _ in range(20)]
    max_disk = max(disk)
    wins = sum(c > max_disk for c in circ)
    assert wins >= 19, (wins, min(circ), max_disk)
