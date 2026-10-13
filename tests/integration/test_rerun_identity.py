"""I06: a from-scratch rerun of S1-S3 into a second store reproduces every artifact id and
payload checksum (CPU, fixed thread count, bitwise determinism)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import _mini_pipeline as mp  # noqa: E402

pytestmark = [pytest.mark.integration, pytest.mark.experiment]


def test_I06_rerun_identity(tmp_path_factory):
    a = mp.all_artifacts(mp.get_store(tmp_path_factory, "plain"))
    b = mp.all_artifacts(mp.build_store(tmp_path_factory.mktemp("rerun")))
    assert a.get("Checkpoint"), "no checkpoints trained"
    assert a.get("ActivationSet"), "no activation sets"
    a.pop("GateReport", None)
    b.pop("GateReport", None)
    assert set(a) == set(b)
    for t in a:
        assert a[t] == b[t], f"{t}: ids or payload checksums differ"
