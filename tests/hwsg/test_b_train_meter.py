"""Author B: training children, meter caps, ledgers, basetemps (G7, 10.3, DRG12, DRG13, KG4)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import GIB, mod  # noqa: E402

THREADS = ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS")


def test_child_env_one_thread_and_temp_under_out(tmp_path):
    gt = mod("gt")
    env = gt.child_env("0224", tmp_path)
    for v in THREADS:
        assert env[v] == "1", v
    for v in ("TEMP", "TMP", "TMPDIR"):
        assert Path(env[v]).resolve().is_relative_to(tmp_path.resolve()), v
    assert "PYTHONPATH" in env


def test_child_env_distinct_per_job(tmp_path):
    gt = mod("gt")
    a, b = gt.child_env("0224", tmp_path), gt.child_env("0225", tmp_path)
    assert a["TEMP"] != b["TEMP"]


def test_child_argv_names_world_master_and_attempt(tmp_path):
    gt, gc = mod("gt"), mod("gc")
    W = gc.world("mid")
    argv = [str(x) for x in gt.child_argv("mid", W.masters[1], tmp_path, "0224", 2)]
    s = " ".join(argv)
    assert "-s" in argv and "child" in argv and W.key in argv
    assert str(W.masters[1]) in argv and "2" in argv and "0224" in argv
    assert str(W.masters[0]) not in s


def test_ram_ok_threshold():  # OPEN-10
    gt = mod("gt")
    need = 3 * 1610612736 + 4294967296
    assert gt.ram_ok(3, free_bytes=need)["ok"] is True
    assert gt.ram_ok(3, free_bytes=need - 1)["ok"] is False
    assert gt.ram_ok(3, free_bytes=0)["ok"] is False


def _child_records(wd, tag, job, statuses):
    gc = mod("gc")
    (wd / "logs").mkdir(parents=True, exist_ok=True)
    for m, st in zip(gc.world(tag).masters, statuses):
        rec = {"master": m, "pid": 1000 + m % 100, "cpu_s": 100.0 + m % 7, "peak_rss": 5 * GIB,
               "status": st, "utc": "2026-11-03T00:00:00Z"}
        (wd / "logs" / f"CHILD_{m}_a1.json").write_text(json.dumps(rec), encoding="utf-8")


def test_aggregate_one_ledger_entry_per_child_with_unique_labels(tmp_path):
    gt, gc, grec = mod("gt"), mod("gc"), mod("grec")
    wd = gc.world_dir(tmp_path, "lo")
    _child_records(wd, "lo", "0224", ["COMPLETE", "FAIL_TECHNICAL/RESOURCE", "COMPLETE"])
    ledger = tmp_path / "LEDGER.json"
    gt.aggregate(wd, "0224", ledger)
    led = grec.ledger_read(ledger)
    labels = [e["label"] for e in led["entries"]]
    assert len(labels) == 3 == len(set(labels))
    for m in gc.world("lo").masters:
        assert f"0224-TRAIN-lo-{m}-a1" in labels
    assert led["cumulative_cpu_s"] == pytest.approx(sum(e["cpu_s"] for e in led["entries"]))
    # a second job on the same ledger uses different labels and is not blocked
    gt.aggregate(wd, "0225", ledger)
    assert len(grec.ledger_read(ledger)["entries"]) == 6


def test_meter_caps_and_output_caps():
    grec = mod("grec")
    assert grec.meter_caps("TRAIN_child")["max_cpu"] == pytest.approx(6006.6282)
    assert grec.meter_caps("O")["max_cpu"] == pytest.approx(5 * 900)
    assert grec.meter_caps("KC")["max_cpu"] == pytest.approx(5 * 1500)
    assert grec.meter_caps("E2", 2)["max_cpu"] == pytest.approx(5 * (900 * 2 + 100))
    assert grec.central("E2", 4) == pytest.approx(900 * 4 + 100)
    assert grec.output_cap("world") == 16 * GIB
    assert grec.output_cap("registry") == 20 * GIB


def test_basetemp_and_tmp_outside_project_root(tmp_path):
    gc = mod("gc")
    root = Path(gc.ROOT).resolve()
    here = tmp_path.resolve()
    assert not here.is_relative_to(root), (here, root)
    assert "topo-scratch" in str(here).lower().replace("\\", "/")


def test_no_array_or_hist_name_inside_project_tests_dir():
    d = Path(__file__).resolve().parent
    assert not [p for p in d.rglob("*") if p.suffix in (".npz", ".npy")]
