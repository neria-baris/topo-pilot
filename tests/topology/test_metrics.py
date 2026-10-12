"""T01, T02: metric hand values, metric axioms, error paths."""
import math

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.topology import METRIC_REGISTRY, Chord, Euclidean, Hellinger, SqrtJS

pytestmark = pytest.mark.topology

# Three distributions a=(1,0,0), b=(0,1,0), c=(.5,.5,0).
X3 = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.5, 0.5, 0.0]])
R2 = math.sqrt(2.0)


def test_registry_names():
    for name, cls in {"euclidean": Euclidean, "chord": Chord, "hellinger": Hellinger,
                      "sqrt_js": SqrtJS}.items():
        assert METRIC_REGISTRY[name] is cls
        assert cls.name == name


def test_euclidean_hand_values():
    # |a-b| = sqrt2 ; |a-c| = sqrt(.25+.25) = sqrt(.5) ; |b-c| = sqrt(.5)
    D = Euclidean().pairwise(X3)
    assert D.shape == (3, 3) and D.dtype == np.float64
    np.testing.assert_allclose(D[0, 1], R2, atol=1e-12)
    np.testing.assert_allclose(D[0, 2], math.sqrt(0.5), atol=1e-12)
    np.testing.assert_allclose(D[1, 2], math.sqrt(0.5), atol=1e-12)


def test_chord_hand_values():
    # Rows normalised: a, b stay; c -> (1/sqrt2, 1/sqrt2, 0).
    # |a-b| = sqrt2 ; |a-c|^2 = (1-1/sqrt2)^2 + 1/2 = 2 - sqrt2.
    D = Chord().pairwise(X3)
    np.testing.assert_allclose(D[0, 1], R2, atol=1e-12)
    np.testing.assert_allclose(D[0, 2], math.sqrt(2 - R2), atol=1e-12)
    np.testing.assert_allclose(D[1, 2], math.sqrt(2 - R2), atol=1e-12)
    # scale of a row is irrelevant
    D2 = Chord().pairwise(X3 * np.array([[5.0], [0.1], [3.0]]))
    np.testing.assert_allclose(D2, D, atol=1e-12)


def test_hellinger_hand_values():
    # H(a,b) = |sqrt a - sqrt b| / sqrt2 = sqrt2/sqrt2 = 1.
    # H(a,c)^2 = ((1-1/sqrt2)^2 + 1/2)/2 = (2 - sqrt2)/2.
    D = Hellinger().pairwise(X3)
    np.testing.assert_allclose(D[0, 1], 1.0, atol=1e-12)
    np.testing.assert_allclose(D[0, 2], math.sqrt((2 - R2) / 2), atol=1e-12)
    np.testing.assert_allclose(D[1, 2], math.sqrt((2 - R2) / 2), atol=1e-12)


def test_sqrt_js_hand_values():
    # a vs b: m=(.5,.5,0); JS = .5 ln2 + .5 ln2 = ln2 -> sqrt(ln 2).
    # a vs c: m=(.75,.25,0); KL(a||m)=ln(4/3); KL(c||m)=.5ln(2/3)+.5ln2=.5 ln(4/3)
    #         JS = .5 ln(4/3) + .25 ln(4/3) = .75 ln(4/3).
    D = SqrtJS().pairwise(X3)
    np.testing.assert_allclose(D[0, 1], math.sqrt(math.log(2)), atol=1e-12)
    np.testing.assert_allclose(D[0, 2], math.sqrt(0.75 * math.log(4 / 3)), atol=1e-12)
    np.testing.assert_allclose(D[1, 2], math.sqrt(0.75 * math.log(4 / 3)), atol=1e-12)


@pytest.mark.parametrize("cls", [Euclidean, Chord, Hellinger, SqrtJS])
def test_metric_axioms_random(cls):
    rng = np.random.default_rng(0)
    X = rng.dirichlet(np.ones(6) * 0.7, size=40)
    D = cls().pairwise(X)
    assert D.shape == (40, 40) and D.dtype == np.float64
    assert np.all(np.isfinite(D))
    np.testing.assert_allclose(D, D.T, atol=1e-10)
    np.testing.assert_allclose(np.diag(D), 0.0, atol=1e-7)
    assert D.min() >= 0.0
    # triangle inequality: D[i,j] <= D[i,k] + D[k,j] for all i,j,k
    viol = D[:, :, None] - (D[:, None, :] + D.T[None, :, :])
    assert viol.max() < 1e-7
    assert D[np.triu_indices(40, 1)].min() > 0.0  # distinct random rows


@pytest.mark.parametrize("cls", [Hellinger, SqrtJS])
def test_nondistribution_raises(cls):
    bad_sum = np.array([[0.5, 0.2, 0.1], [0.3, 0.3, 0.4]])
    neg = np.array([[1.2, -0.2, 0.0], [0.3, 0.3, 0.4]])
    for bad in (bad_sum, neg):
        with pytest.raises(StageFailure) as ei:
            cls().pairwise(bad)
        assert ei.value.code == ErrorCode.NUMERICAL_FAILURE


def test_chord_zero_row_raises():
    X = np.array([[1.0, 0.0], [0.0, 0.0], [0.3, 0.4]])
    with pytest.raises(StageFailure) as ei:
        Chord().pairwise(X)
    assert ei.value.code == ErrorCode.NUMERICAL_FAILURE
