import numpy as np
import pytest
from scipy import stats

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.contracts import testing as CT
from topo_pilot.dataset import HMMSampler

pytestmark = pytest.mark.dataset


def test_D01_deterministic_cycle_known_answer():
    # T: 0->1->2->3->0 (permutation cycle), E = identity, pi = delta_0, so w_t = (t-1) mod 4.
    T = np.roll(np.eye(4), 1, axis=1)
    pi = np.array([1.0, 0, 0, 0])
    tokens, states = HMMSampler(T, np.eye(4), pi, SequenceLayout()).sample(
        5, SeedTree(3).generator("x"))
    expected = np.arange(33) % 4
    assert tokens.dtype == np.uint8 and states.dtype == np.int16
    assert tokens.shape == (5, 33)
    assert np.array_equal(tokens, np.tile(expected, (5, 1)))
    assert np.array_equal(states, tokens)


def test_D02_empirical_frequencies_match_T_E_pi():
    T, E, pi = CT.tiny_hmm()
    tokens, states = HMMSampler(T, E, pi, SequenceLayout()).sample(
        20_000, SeedTree(11).generator("d02"))
    n = tokens.shape[0]
    z = states.astype(int)
    w = tokens.astype(int)
    assert stats.chisquare(np.bincount(w[:, 0], minlength=3), n * (pi @ E)).pvalue > 1e-3
    assert stats.chisquare(np.bincount(z[:, 0], minlength=4), n * pi).pvalue > 1e-3
    for i in range(4):
        nxt = z[:, 1:][z[:, :-1] == i]
        counts = np.bincount(nxt, minlength=4)
        keep = T[i] > 0
        assert counts[~keep].sum() == 0
        assert stats.chisquare(counts[keep], counts.sum() * T[i][keep]).pvalue > 1e-3
        emitted = w[z == i]
        assert stats.chisquare(np.bincount(emitted, minlength=3),
                               emitted.size * E[i]).pvalue > 1e-3


def test_D03_emission_before_transition():
    T, _, pi = CT.tiny_hmm()
    tokens, states = HMMSampler(T, np.eye(4), pi, SequenceLayout()).sample(
        500, SeedTree(5).generator("d03"))
    assert np.array_equal(tokens, states.astype(np.uint8))
    # a transition happened somewhere, so the check is not vacuous
    assert (states[:, 1:] != states[:, :-1]).any()


def test_sampler_never_draws_zero_probability_symbols():
    T = np.roll(np.eye(3), 1, axis=1)
    E = np.array([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.5, 0.0, 0.5]])
    tokens, states = HMMSampler(T, E, np.full(3, 1 / 3), SequenceLayout()).sample(
        2000, SeedTree(1).generator("z"))
    assert np.all(E[states, tokens] > 0)
