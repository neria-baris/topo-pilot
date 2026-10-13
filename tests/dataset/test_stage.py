import numpy as np
import pytest

from topo_pilot import contracts as C
from topo_pilot.dataset import DatasetConfig, DatasetStage, HMMSampler
from topo_pilot.dataset.checks import (
    check_disjoint,
    check_first_token,
    check_ranges,
    make_sequence_ids,
    process_code,
)

pytestmark = pytest.mark.dataset


def _run(process, cfg, master=1, eid=None):
    store, tid, e0, _ = process
    return DatasetStage().run(tid, eid or e0, cfg, C.SeedTree(master), store)


def _load(store, cls, aid):
    return store.load(cls, aid, consumer="experiment")


def test_D04_disjoint_ids_test_shared_across_replicates_train_differs(process, tiny_cfg):
    store = process[0]
    a, b = _run(process, tiny_cfg, 1), _run(process, tiny_cfg, 2)
    assert set(a) == {"obs_train", "obs_dev", "obs_test", "sidecar_dev", "sidecar_test",
                      "history_index"}
    ids = {s: _load(store, C.ObservationSet, a[f"obs_{s}"]).sequence_id
           for s in ("train", "dev", "test")}
    allids = np.concatenate(list(ids.values()))
    assert allids.min() >= 0 and len(np.unique(allids)) == len(allids)
    assert a["obs_test"] == b["obs_test"] and a["history_index"] == b["history_index"]
    assert a["sidecar_test"] == b["sidecar_test"]
    assert a["obs_train"] != b["obs_train"] and a["obs_dev"] != b["obs_dev"]
    assert a["sidecar_dev"] != b["sidecar_dev"]
    t1 = _load(store, C.ObservationSet, a["obs_train"]).tokens
    t2 = _load(store, C.ObservationSet, b["obs_train"]).tokens
    assert not np.array_equal(t1, t2)
    assert "replicate" not in store.meta(a["obs_test"]).config
    assert store.meta(a["obs_train"]).config["replicate"] == 1


def test_symbol_renaming_keeps_test_latents_and_relabels_tokens(process, tiny_cfg, add_emission):
    store, _, e0, E = process
    perm = [2, 0, 1]
    e1 = add_emission(E, perm)
    ra, rb = _run(process, tiny_cfg, 1, eid=e0), _run(process, tiny_cfg, 2, eid=e1)
    ta = _load(store, C.ObservationSet, ra["obs_test"]).tokens
    tb = _load(store, C.ObservationSet, rb["obs_test"]).tokens
    assert np.array_equal(np.array(perm)[ta.astype(int)], tb)
    za = _load(store, C.EvalSidecar, ra["sidecar_test"]).z
    zb = _load(store, C.EvalSidecar, rb["sidecar_test"]).z
    assert np.array_equal(za, zb)


def test_stage_saves_expected_lineage_and_split_labels(process, tiny_cfg):
    store = process[0]
    r = _run(process, tiny_cfg)
    assert set(store.meta(r["obs_dev"]).parent_ids) == {process[1], process[2]}
    assert store.meta(r["history_index"]).parent_ids == (r["obs_test"],)
    assert store.meta(r["obs_dev"]).consumer == "dataset"
    hist = _load(store, C.HistoryIndex, r["history_index"])
    assert hist.dataset_id == r["obs_test"] and len(hist.panel) == 16
    assert _load(store, C.EvalSidecar, r["sidecar_dev"]).split == "dev"


def test_D08_no_train_sidecar_persisted(process, tiny_cfg):
    store = process[0]
    _run(process, tiny_cfg)
    found = store.find(C.EvalSidecar)
    assert len(found) == 2
    assert sorted(store.meta(i).config["split"] for i in found) == ["dev", "test"]
    assert store.find(C.EvalSidecar, split="train") == []
    assert all(_load(store, C.EvalSidecar, i).z.shape[0] != tiny_cfg.n_train for i in found)


def test_D09_biased_sampler_caught_by_first_token_chi2(process, tiny_cfg, monkeypatch):
    def biased(self, n, rng):
        return np.zeros((n, 33), dtype=np.uint8), np.zeros((n, 33), dtype=np.int16)

    monkeypatch.setattr(HMMSampler, "sample", biased)
    with pytest.raises(C.StageFailure) as exc:
        _run(process, tiny_cfg)
    assert exc.value.code is C.ErrorCode.NUMERICAL_FAILURE
    assert "sampler_bias" in exc.value.detail


def test_chi2_skipped_below_200_and_passes_on_exact_counts():
    p_w = np.array([0.5, 0.3, 0.2])
    assert check_first_token(np.zeros(199, dtype=np.uint8), p_w, "test") is None
    exact = np.repeat(np.arange(3), [250, 150, 100])
    assert check_first_token(exact, p_w, "train") == pytest.approx(1.0)


def test_n_test_smaller_than_panels_is_alignment_error(process):
    cfg = DatasetConfig(n_train=200, n_dev=100, n_test=10, n_panels=2, panel_size=8)
    with pytest.raises(C.StageFailure) as exc:
        _run(process, cfg)
    assert exc.value.code is C.ErrorCode.ALIGNMENT_ERROR


def test_split_overlap_and_range_errors():
    with pytest.raises(C.StageFailure) as exc:
        check_disjoint(train=np.array([1, 2]), test=np.array([2, 3]))
    assert exc.value.code is C.ErrorCode.SPLIT_OVERLAP
    check_disjoint(train=np.array([1]), test=np.array([2]))
    z = np.zeros((1, 33), dtype=np.int16)
    for tok, st in ((np.full((1, 33), 3, np.uint8), z), (np.zeros((1, 33), np.uint8), z + 4)):
        with pytest.raises(C.StageFailure) as exc:
            check_ranges(tok, st, 3, 4)
        assert exc.value.code is C.ErrorCode.ALIGNMENT_ERROR


def test_sequence_id_rule_known_answer():
    code = process_code("cylinder", "overlap", "0.5", "shared")
    assert 0 <= code < 2**31
    ids = make_sequence_ids(code, "dev", 3)
    assert ids.dtype == np.int64
    assert ids.tolist() == [(code << 32) | (2 << 28) | i for i in range(3)]
    assert make_sequence_ids(code, "test", 1)[0] != ids[0]
    assert process_code("cylinder", "overlap", "0.5", 1) != code
