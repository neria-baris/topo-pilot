"""Builder-authored smoke test of the technical benchmark plumbing (tiny sizes; timing values are
not checked): outputs, decision field, separate technical ledger, immutable output directory."""
import json

import pytest

from topo_pilot.experiment import x5g1_techbench as tb
from topo_pilot.experiment.x5g1_safety import OutputExists

pytestmark = pytest.mark.experiment


def test_techbench_plumbing(tmp_path, monkeypatch):
    monkeypatch.setattr(tb, "N_TRAIN", 256)
    monkeypatch.setattr(tb, "N_DEV_FULL", 64)
    monkeypatch.setattr(tb, "REPEATS", 1)
    monkeypatch.setattr(tb, "THREADS", (1,))
    mailbox = tmp_path / "mb"
    mailbox.mkdir()
    res = tb.run(tmp_path, tmp_path / "store", tmp_path / "out", mailbox)
    assert res["decision"]["B1"] in ("RESOLVED", "UNRESOLVED")
    s = res["settings"][0]
    sizes = s["checkpoint_bytes"]
    assert s["threads"] == 1 and sizes["final"] > sizes["intermediate"]
    for name in ("timings.json", "projection.json", "MANIFEST.json"):
        assert (tmp_path / "out" / name).exists()
    ledger = json.loads((tmp_path / "store" / "tech_ledger.json").read_text())
    assert ledger["entries"][-1]["job"] == "0008-techbench"
    with pytest.raises(OutputExists):
        tb.run(tmp_path, tmp_path / "store", tmp_path / "out", mailbox)
