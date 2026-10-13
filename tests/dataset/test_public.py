import dataclasses

import numpy as np
import pytest
import torch

from topo_pilot.contracts import (
    ErrorCode,
    EvalSidecar,
    ObservationSet,
    SequenceLayout,
    StageFailure,
)
from topo_pilot.contracts import testing as CT
from topo_pilot.dataset import PublicTokenDataset

pytestmark = pytest.mark.dataset


def test_D06_observation_set_has_no_latent_field_and_sidecar_is_rejected():
    names = {f.name for f in dataclasses.fields(ObservationSet)}
    assert names == {"split", "V", "sequence_id", "tokens", "layout_version"}
    side = EvalSidecar(split="test", N=4, sequence_id=np.arange(2, dtype=np.int64),
                       z=np.zeros((2, 33), dtype=np.int16))
    with pytest.raises(StageFailure) as exc:
        PublicTokenDataset(side, SequenceLayout())
    assert exc.value.code is ErrorCode.LEAKAGE


def test_latent_field_added_to_observation_subclass_is_leakage():
    @dataclasses.dataclass(frozen=True, eq=False)
    class Leaky(ObservationSet):
        z: object = None

    base = CT.tiny_observations(4)
    leaky = Leaky(split="test", V=3, sequence_id=base.sequence_id, tokens=base.tokens,
                  z=np.zeros((4, 33)))
    with pytest.raises(StageFailure) as exc:
        PublicTokenDataset(leaky, SequenceLayout())
    assert exc.value.code is ErrorCode.LEAKAGE


def test_D07_inputs_and_targets_via_layout():
    tokens = (np.arange(66) % 3).astype(np.uint8).reshape(2, 33)
    tokens[1] = 2 - tokens[1]
    obs = ObservationSet(split="train", V=3, sequence_id=np.arange(2, dtype=np.int64),
                         tokens=tokens)
    ds = PublicTokenDataset(obs, SequenceLayout())
    assert len(ds) == 2
    for i in range(2):
        x, y = ds[i]
        assert x.dtype == torch.int64 and y.dtype == torch.int64
        assert x.tolist() == [3] + tokens[i, :32].tolist()  # [BOS=V, w1..w32]
        assert y.tolist() == tokens[i].tolist()             # [w1..w33]
        assert x.shape == (33,) and y.shape == (33,)
