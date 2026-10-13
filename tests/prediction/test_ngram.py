"""R03, R04, R05 (unit part): n-gram baselines."""

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, ObservationSet, StageFailure
from topo_pilot.prediction import NGramBaseline

pytestmark = pytest.mark.prediction


def make_obs(tokens, split="train", V=3):
    tokens = np.asarray(tokens, dtype=np.uint8)
    return ObservationSet(split=split, V=V, sequence_id=np.arange(len(tokens), dtype=np.int64),
                          tokens=tokens)


def test_R03_unigram_exact_frequencies():
    row0 = [0] * 33
    row1 = [1] * 22 + [2] * 11
    model = NGramBaseline(1, "additive", alpha=0.0).fit(make_obs([row0, row1]))
    probs = model.predict(np.zeros((2, 32), dtype=np.int64))
    np.testing.assert_allclose(probs, [[0.5, 1 / 3, 1 / 6]] * 2, atol=1e-15)


def test_R03_additive_smoothing_hand_value():
    model = NGramBaseline(1, "additive", alpha=1.0).fit(make_obs([[0] * 33]))
    np.testing.assert_allclose(model.predict(np.zeros((1, 4), dtype=int))[0],
                               [34 / 36, 1 / 36, 1 / 36])


def test_R03_kneser_ney_order1_equals_mle():
    obs = make_obs([[0] * 33, [1] * 22 + [2] * 11])
    kn = NGramBaseline(1, "kneser_ney").fit(obs).predict(np.zeros((1, 3), dtype=int))
    mle = NGramBaseline(1, "additive", alpha=0.0).fit(obs).predict(np.zeros((1, 3), dtype=int))
    np.testing.assert_allclose(kn, mle)


def test_R04_bigram_on_cycle_predicts_successor():
    rows = [[(s + t) % 3 for t in range(33)] for s in (0, 1, 2)]
    model = NGramBaseline(2, "additive", alpha=1e-3).fit(make_obs(rows))
    probs = model.predict(np.array([[5, 0], [5, 1], [5, 2]]))
    assert probs[0, 1] > 0.999 and probs[1, 2] > 0.999 and probs[2, 0] > 0.999
    np.testing.assert_allclose(probs.sum(axis=1), 1.0)


def test_bigram_contexts_do_not_cross_sequences():
    obs = make_obs([[0] * 33, [1] * 33])
    probs = NGramBaseline(2, "additive", alpha=0.0).fit(obs).predict(np.array([[0], [1]]))
    np.testing.assert_allclose(probs, [[1, 0, 0], [0, 1, 0]])


def test_bigram_unseen_context_alpha_zero_backs_off_to_unigram():
    obs = make_obs([[0] * 11 + [1] * 22])
    model = NGramBaseline(2, "additive", alpha=0.0).fit(obs)
    np.testing.assert_allclose(model.predict(np.array([[2]]))[0], [1 / 3, 2 / 3, 0.0])


def test_kneser_ney_hand_value_and_rows_normalised():
    obs = make_obs([[0, 1] * 16 + [0]])
    model = NGramBaseline(2, "kneser_ney", alpha=0.5).fit(obs)
    # context 0: n(0,1)=16, n(0)=16, N1+(0,.)=1; context 1: n(1,0)=16; p_cont = (1/2, 1/2, 0)
    probs = model.predict(np.array([[0], [2]]))
    np.testing.assert_allclose(probs[0], [0.5 / 16 * 0.5, 15.5 / 16 + 0.5 / 16 * 0.5, 0.0])
    np.testing.assert_allclose(probs[1], [0.5, 0.5, 0.0])
    np.testing.assert_allclose(probs.sum(axis=1), 1.0)


def test_R05_select_smoothing_uses_dev_and_picks_argmin():
    train = make_obs([[0] * 33], V=2)
    dev = make_obs([[0] * 32 + [1]] * 4, split="dev", V=2)
    model = NGramBaseline(1, "additive").fit(train)
    chosen = model.select_smoothing(dev, (1e-3, 1e-1, 1.0))
    assert chosen == 1.0 and model.alpha == 1.0
    dev_zero = make_obs([[0] * 33] * 4, split="dev", V=2)
    assert model.select_smoothing(dev_zero, (1e-3, 1e-1, 1.0)) == 1e-3


def test_error_paths():
    with pytest.raises(StageFailure) as exc:
        NGramBaseline(3, "additive")
    assert exc.value.code == ErrorCode.INVALID_CONFIG
    with pytest.raises(StageFailure):
        NGramBaseline(1, "additive", alpha=-1.0)
    with pytest.raises(StageFailure) as exc:
        NGramBaseline(1, "additive").predict(np.zeros((1, 3), dtype=int))
    assert exc.value.code == ErrorCode.ALIGNMENT_ERROR
