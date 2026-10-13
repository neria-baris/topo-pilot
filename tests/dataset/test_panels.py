import numpy as np
import pytest

from topo_pilot.contracts import (
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
    make_history_id,
    tokens_hash,
)
from topo_pilot.contracts import testing as CT
from topo_pilot.dataset import DatasetConfig, HMMSampler, PanelBuilder

pytestmark = pytest.mark.dataset


def _test_obs(r: int) -> ObservationSet:
    T, E, pi = CT.tiny_hmm()
    tokens, _ = HMMSampler(T, E, pi, SequenceLayout()).sample(r, SeedTree(2).generator("t"))
    return ObservationSet(split="test", V=3, sequence_id=np.arange(r, dtype=np.int64) + 7,
                          tokens=tokens)


def _panel_rng():
    return SeedTree(0).generator("panels", "cylinder", "overlap", "0.5")


def test_D05_panels_disjoint_distinct_and_reproducible():
    cfg = DatasetConfig()
    obs = _test_obs(4096)
    a = PanelBuilder().build(obs, cfg, _panel_rng(), dataset_id="abc")
    b = PanelBuilder().build(obs, cfg, _panel_rng(), dataset_id="abc")
    assert np.array_equal(a.history_id, b.history_id)
    assert len(a.history_id) == 8 * 512
    assert np.array_equal(a.panel, np.repeat(np.arange(1, 9), 512))
    assert np.all(a.end == 32)
    assert len(set(a.sequence_id.tolist())) == 4096  # all 4096 used once: disjoint and distinct
    for k in range(1, 9):
        assert len(set(a.sequence_id[a.panel == k].tolist())) == 512
    row = int(np.where(obs.sequence_id == a.sequence_id[5])[0][0])
    h = tokens_hash(obs.tokens[row, :32])
    assert a.tokens_hash[5] == h
    assert a.history_id[5] == make_history_id("abc", int(a.sequence_id[5]), 32, h)
    other = PanelBuilder().build(obs, cfg, _panel_rng(), dataset_id="xyz")
    assert a.history_id[0] != other.history_id[0]
    shifted = PanelBuilder().build(obs, cfg, SeedTree(0).generator("panels", "x"), dataset_id="abc")
    assert not np.array_equal(a.sequence_id, shifted.sequence_id)


def test_panel_config_sizes_and_too_few_trajectories():
    cfg = DatasetConfig(n_panels=2, panel_size=8)
    idx = PanelBuilder().build(_test_obs(40), cfg, _panel_rng(), dataset_id="d")
    assert idx.n_panels == 2 and idx.panel_size == 8 and len(idx.panel) == 16
    with pytest.raises(StageFailure) as exc:
        PanelBuilder().build(_test_obs(15), cfg, _panel_rng(), dataset_id="d")
    assert exc.value.code is ErrorCode.ALIGNMENT_ERROR
