"""I04: scrambling EvalSidecar.z leaves every Checkpoint / ActivationSet id and payload
checksum unchanged, so the learner and activations never read the latents."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import _mini_pipeline as mp  # noqa: E402

from topo_pilot.contracts import ActivationSet, Checkpoint, EvalSidecar  # noqa: E402

pytestmark = [pytest.mark.integration, pytest.mark.experiment]


def test_I04_scrambled_latents_do_not_reach_learner(tmp_path_factory):
    plain = mp.get_store(tmp_path_factory, "plain")
    scrambled = mp.get_store(tmp_path_factory, "scrambled")
    for t in (Checkpoint, ActivationSet):
        p = mp.ids_and_hashes(plain, t)
        assert p, f"no {t.ARTIFACT_TYPE} artifacts"
        assert p == mp.ids_and_hashes(scrambled, t)
    sp, ss = (mp.ids_and_hashes(s, EvalSidecar) for s in (plain, scrambled))
    assert sp and ss
    assert sorted(sp.values()) != sorted(ss.values()), "scramble did not change the sidecars"
