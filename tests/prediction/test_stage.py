"""R05 (stage part): run_baselines wiring, split use, saved artifacts."""

import numpy as np
import pytest

from topo_pilot.contracts import (
    BaselineOutputs,
    HistoryIndex,
    ObservationSet,
    make_history_id,
    tokens_hash,
)
from topo_pilot.contracts.testing import memory_store, tiny_observations
from topo_pilot.prediction import NGramBaseline, PredictionStage

pytestmark = pytest.mark.prediction


def retarget(obs, split):
    return ObservationSet(split=split, V=obs.V, sequence_id=obs.sequence_id + 1000 * len(split),
                          tokens=obs.tokens)


def build(store):
    train = retarget(tiny_observations(16, seed=1), "train")
    dev = retarget(tiny_observations(8, seed=2), "dev")
    test = tiny_observations(8, seed=3)
    ids = [store.save(o, config={"split": o.split}, parents=[], seed_map={}, consumer="dataset")
           for o in (train, dev, test)]
    rows = [6, 2, 5, 0]
    hashes = [tokens_hash(test.tokens[r, :32]) for r in rows]
    hist_ids = [make_history_id("ds", int(test.sequence_id[r]), 32, h)
                for r, h in zip(rows, hashes)]
    index = HistoryIndex(dataset_id="ds", history_id=np.array(hist_ids),
                         sequence_id=test.sequence_id[rows], end=np.full(4, 32),
                         panel=np.ones(4, dtype=int), tokens_hash=np.array(hashes),
                         panel_size=4, n_panels=1)
    hid = store.save(index, config={"ds": "ds"}, parents=[ids[2]], seed_map={}, consumer="dataset")
    return ids, hid


def test_R05_run_baselines_uses_train_for_fit_dev_for_select(monkeypatch):
    store = memory_store()
    (tr, dv, te), hid = build(store)
    seen = {"fit": [], "select": []}
    real_fit, real_sel = NGramBaseline.fit, NGramBaseline.select_smoothing

    def spy_fit(self, train):
        seen["fit"].append(train.split)
        return real_fit(self, train)

    def spy_sel(self, dev, grid):
        seen["select"].append(dev.split)
        return real_sel(self, dev, grid)

    monkeypatch.setattr(NGramBaseline, "fit", spy_fit)
    monkeypatch.setattr(NGramBaseline, "select_smoothing", spy_sel)
    ids = PredictionStage().run_baselines(tr, dv, te, hid, store)
    assert seen == {"fit": ["train", "train"], "select": ["dev", "dev"]}
    assert len(ids) == 2

    out1, out2 = (store.load(BaselineOutputs, i, consumer="prediction") for i in ids)
    assert (out1.ngram_order, out2.ngram_order) == (1, 2)
    assert out1.smoothing.startswith("additive:") and out1.probs.shape == (4, 3)
    index = store.load(HistoryIndex, hid, consumer="prediction")
    assert out2.history_id.tolist() == index.history_id.tolist()
    np.testing.assert_allclose(out1.probs.sum(axis=1), 1.0)


def test_run_metrics_and_probes_deferred():
    with pytest.raises(NotImplementedError):
        PredictionStage().run_metrics("a", "b", memory_store())
    with pytest.raises(NotImplementedError):
        PredictionStage().run_probes(["a"], "b", None, memory_store())
