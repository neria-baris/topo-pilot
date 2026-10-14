"""Builder-authored SYNTHETIC end-to-end tests of the X5 G1 training-study CLI (job 0009): tiny
N4/V3 processes, tiny models, temporary stores; persistence, endpoint and bootstrap composition
only (not real-architecture training)."""

import hashlib
import json

import pytest

from topo_pilot.experiment.x5g1t_fixture import build_fixture
from topo_pilot.experiment.x5g1t_main import main

pytestmark = pytest.mark.experiment
ARMS, MASTERS = ("a0", "a020"), (310001, 310002, 310003)


def _cli(cfg, *args):
    return main(["--config", str(cfg), *args])


def _manifest_ok(d):
    m = json.loads((d / "MANIFEST.json").read_text())
    return m and all(hashlib.sha256((d / k).read_bytes()).hexdigest() == v for k, v in m.items())


def test_full_staged_run(tmp_path):
    cfg = build_fixture(tmp_path)
    tables = tmp_path / "study" / "tables"
    assert _cli(cfg, "final-test", "--authorized-final") == 3  # refused before dev-analysis
    assert _cli(cfg, "pools") == 0
    assert _cli(cfg, "pools") == 3  # immutable output version
    pools = json.loads((tables / "pools" / "pools.json").read_text())
    assert len(pools["pools"]) == 12 and not any(pools["collisions"].values())
    assert not any(k.startswith("test") for k in pools["pools"])  # no fresh test yet
    for m in MASTERS:
        for a in ARMS:
            assert _cli(cfg, "train", "--arm", a, "--master", str(m)) == 0
    assert _cli(cfg, "train", "--arm", "a0", "--master", "310001") == 3  # no retry
    outcomes = [json.loads((tmp_path / "study" / "outcomes" / f"{a}_{m}.json").read_text())
                for m in MASTERS for a in ARMS]
    assert all(o["status"] == "COMPLETE" and len(o["checkpoints"]) == 7 for o in outcomes)
    ids = {o["arm"]: [c["checkpoint_id"] for c in o["checkpoints"]] for o in outcomes[:2]}
    assert not set(ids["a0"]) & set(ids["a020"])  # same run_key, distinct parents
    assert _cli(cfg, "final-test") == 3  # needs explicit authorisation
    assert _cli(cfg, "dev-analysis") == 0
    res = json.loads((tables / "dev_analysis" / "result.json").read_text())
    assert res["verdict"] in ("SUPPORTED", "REJECTED", "INCONCLUSIVE") and len(res["pairs"]) == 3
    assert _cli(cfg, "final-test", "--authorized-final") == 0
    final = json.loads((tables / "final_test" / "result.json").read_text())
    assert len(final["models"]) == 6 and set(final["test_pools"]) == set(ARMS)
    for d in ("pools", "dev_analysis", "final_test", "train/a0_310001"):
        assert _manifest_ok(tables / d)
    ledger = json.loads((tmp_path / "ledger.json").read_text())
    assert [e["status"] for e in ledger["entries"]].count("ok") >= 9
    assert not (tmp_path / "study" / "RUN.lock").exists()


def test_budget_stop_records_incomplete_and_inconclusive(tmp_path):
    cfg = build_fixture(tmp_path, cap_s=600.0)  # below the real-scale evaluation reserve
    assert _cli(cfg, "pools") == 0
    assert _cli(cfg, "train", "--arm", "a0", "--master", "310001") == 2
    o = json.loads((tmp_path / "study" / "outcomes" / "a0_310001.json").read_text())
    assert o["status"] == "INCOMPLETE" and o["cause"].startswith("BudgetExceeded")
    assert o["checkpoints"] == []
    entry = json.loads((tmp_path / "ledger.json").read_text())["entries"][-1]
    assert entry["status"] == "budget"
    assert _cli(cfg, "dev-analysis") == 0
    res = json.loads((tmp_path / "study" / "tables" / "dev_analysis" / "verdict.json").read_text())
    assert res["verdict"] == "INCONCLUSIVE"


def test_stop_and_hold_controls(tmp_path):
    cfg = build_fixture(tmp_path)
    mailbox = tmp_path / "mailbox"
    assert _cli(cfg, "pools") == 0
    (mailbox / "worker_control.json").write_text("{not json")  # malformed: fail closed
    assert _cli(cfg, "train", "--arm", "a0", "--master", "310001") == 2
    o = json.loads((tmp_path / "study" / "outcomes" / "a0_310001.json").read_text())
    assert o["status"] == "INCOMPLETE" and o["checkpoints"] == []
    (mailbox / "worker_control.json").unlink()
    (mailbox / "STOP").write_text("stop")
    assert _cli(cfg, "train", "--arm", "a020", "--master", "310001") == 2
    assert not (tmp_path / "study" / "RUN.lock").exists()
