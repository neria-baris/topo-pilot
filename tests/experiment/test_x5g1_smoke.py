"""Builder-authored smoke tests (not the independent X5 G1 tests): integrity failure gives FAILED
with a ledger entry and exports; STOP before data gives INCONCLUSIVE; no real artifacts used."""
import json

import pytest

from topo_pilot.experiment.x5g1_main import run_gate

pytestmark = pytest.mark.experiment


def test_missing_parents_is_failed_not_a_scientific_verdict(tmp_path):
    main_root = tmp_path / "main"
    main_root.mkdir()
    out = tmp_path / "out"
    tables = tmp_path / "tables"
    mailbox = tmp_path / "mailbox"
    mailbox.mkdir()
    repo = __import__("pathlib").Path(__file__).resolve().parents[2]
    res = run_gate(repo, main_root, out, tables, mailbox)
    assert res["verdict"] == "FAILED" and "integrity" in res["reason"]
    ledger = json.loads((out / "cpu_ledger.json").read_text())
    assert len(ledger["entries"]) == 1 and ledger["entries"][0]["status"] == "ok"
    assert (tables / "verdict.json").exists() and (tables / "MANIFEST.json").exists()
    res2 = run_gate(repo, main_root, out, tables, mailbox)
    ledger2 = json.loads((out / "cpu_ledger.json").read_text())
    assert len(ledger2["entries"]) == 2
    assert ledger2["cumulative_cpu_s"] >= ledger["cumulative_cpu_s"]
    assert res2["verdict"] == "FAILED"


def test_stop_before_data_is_inconclusive(tmp_path):
    main_root = tmp_path / "main"
    main_root.mkdir()
    mailbox = tmp_path / "mailbox"
    mailbox.mkdir()
    (mailbox / "STOP").write_text("stop")
    repo = __import__("pathlib").Path(__file__).resolve().parents[2]
    res = run_gate(repo, main_root, tmp_path / "out", tmp_path / "tables", mailbox)
    assert res["verdict"] == "INCONCLUSIVE" and "StopRequested" in res["reason"]
