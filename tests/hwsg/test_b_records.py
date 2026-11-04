"""Author B: sealing, terminal RESULTs, S8 export, markers, barrier, cross inputs, ledger."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import CONTRACT, expect_fail, mod, ok_of  # noqa: E402

TERMINAL_KEYS = set(CONTRACT["records"]["TERMINAL_RESULT"])


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _events(wd):
    f = Path(wd) / "STAGES.jsonl"
    return [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]


def _terminal(tmp_path, tag="lo", status="INCONCLUSIVE/NOT_LEARNED"):
    gc, grec = mod("gc"), mod("grec")
    wd = gc.world_dir(tmp_path, tag)
    wd.mkdir(parents=True, exist_ok=True)
    with mod("gb").world(tag):
        p = grec.terminal_result(wd, tag, status, "TRAIN", "T_" + tag, {"k": 1}, False)
    return wd, Path(p)


def test_terminal_result_keys_exclusive_and_one_stage_complete(tmp_path):
    wd, p = _terminal(tmp_path)
    assert p == wd / "stages" / "TERMINAL" / "RESULT.json"
    body = json.loads(p.read_text(encoding="utf-8"))
    assert TERMINAL_KEYS <= set(body) and body["p1_passed"] is False
    assert body["protocol_sha256"] == mod("gc").PROTOCOL_SHA
    assert CONTRACT["disclosure"] in json.dumps(body) or body["lineage_disclosure"]
    ev = [e for e in _events(wd) if e["event"] == "STAGE_COMPLETE" and e["stage"] == "TERMINAL"]
    assert len(ev) == 1
    # marker ordering: the event names the file with the hash of the bytes already on disk
    assert ev[0]["files"]["stages/TERMINAL/RESULT.json"] == _sha(p)
    with pytest.raises(Exception):  # noqa: B017  exclusive create refuses a second write
        with mod("gb").world("lo"):
            mod("grec").terminal_result(wd, "lo", "INCONCLUSIVE/NOT_LEARNED", "TRAIN", "T", {},
                                        False)
    assert _sha(p) == ev[0]["files"]["stages/TERMINAL/RESULT.json"]


def test_load_world_hash_checked(tmp_path):
    gx = mod("gx")
    wd, p = _terminal(tmp_path)
    r = gx.load_world(tmp_path, "lo")
    assert r["tag"] == "lo" and r["endpoint"] is False and r["outcome"]
    p.write_text(p.read_text(encoding="utf-8") + " ", encoding="utf-8")  # changed byte
    expect_fail("FAIL_TECHNICAL/LINEAGE", gx.load_world, tmp_path, "lo")


def test_registered_world_without_result_is_lineage_not_exclusion(tmp_path):
    gx, gc = mod("gx"), mod("gc")
    gc.world_dir(tmp_path, "mid").mkdir(parents=True)
    e = expect_fail("FAIL_TECHNICAL/LINEAGE", gx.load_world, tmp_path, "mid")
    assert "EXCLUSION" not in str(getattr(e, "status", ""))


def test_export_g_puts_four_files_in_one_s8_event(tmp_path):
    gc, grec = mod("gc"), mod("grec")
    wd = gc.world_dir(tmp_path, "hi")
    wd.mkdir(parents=True)
    (wd / "SEALED_VALIDATION.json").write_text(json.dumps({"N": 3072}), encoding="utf-8")
    ratio = wd / "ratio_in"
    ratio.mkdir()
    (ratio / "RATIO.json").write_text(json.dumps({"status": "DEFINED"}), encoding="utf-8")
    np.savez(ratio / "RATIO_DRAWS.npz", rho_minus_620631=np.zeros(5000))
    oc = {"outcome": "SUPPORT", "label": "SUPPORT", "k": 3, "models": 3, "criterion": "c"}
    with mod("gb").world("hi"):
        # API-AMBIGUITY: ratio_files is the pair (RATIO.json, RATIO_DRAWS.npz) of local paths
        grec.export_g(wd, {"world": "hi"}, oc, [], {"world": "hi", "N": 3072},
                      [ratio / "RATIO.json", ratio / "RATIO_DRAWS.npz"])
    ev = [e for e in _events(wd) if e["event"] == "STAGE_COMPLETE" and e["stage"] == "S8"]
    assert len(ev) == 1
    names = {Path(k).name for k in ev[0]["files"]}
    assert {"RESULT.json", "SEALED_OPENED.json", "RATIO.json", "RATIO_DRAWS.npz"} <= names
    body = json.loads((wd / "stages" / "S8" / "RESULT.json").read_text(encoding="utf-8"))
    assert body["outcome"] == "SUPPORT" and "3072" in body["licence"]


def test_marker_replace_retries_permission_error(tmp_path, monkeypatch):
    grec = mod("grec")
    target = tmp_path / "OPERATION_ACTIVE.json"
    real, calls = os.replace, {"n": 0}

    def flaky(a, b):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise PermissionError("locked")
        return real(a, b)

    monkeypatch.setattr(os, "replace", flaky)
    grec.marker_replace(target, {"active": False}, retries=5, sleep_s=0)
    assert calls["n"] == 3 and json.loads(target.read_text(encoding="utf-8")) == {"active": False}
    calls["n"] = -100  # always fails
    with pytest.raises(PermissionError):
        grec.marker_replace(target, {"active": True}, retries=2, sleep_s=0)


def _accept(wd, name, sha):
    # API-AMBIGUITY: the accept record names the bound sha256 under several plausible keys
    rec = {k: sha for k in ("sha256", "result_sha256", "report_sha256", "terminal_result_sha256",
                            "validation_report_sha256", "bound_sha256")}
    (wd / name).write_text(json.dumps(rec), encoding="utf-8")


def _e1_accepted(tmp_path, tag):
    gc = mod("gc")
    wd = gc.world_dir(tmp_path, tag)
    (wd / "stages" / "S5").mkdir(parents=True)
    rep = wd / "stages" / "S5" / "VALIDATION_REPORT.json"
    rep.write_text(json.dumps({"world": tag}), encoding="utf-8")
    _accept(wd, "ACCEPT_VALIDATION.json", _sha(rep))
    return wd


def test_release_barrier(tmp_path):
    grec = mod("grec")
    for tag in ("lo", "mid"):
        wd, p = _terminal(tmp_path, tag)
        _accept(wd, "ACCEPT_TERMINAL.json", _sha(p))
    _e1_accepted(tmp_path, "hi")
    assert ok_of(grec.release_barrier(tmp_path))
    # a world neither terminal nor accepted blocks the first E2
    (tmp_path / "worlds" / mod("gc").world("hi").key / "ACCEPT_VALIDATION.json").unlink()
    assert not ok_of(grec.release_barrier(tmp_path))


def test_window_ok(tmp_path):
    grec = mod("grec")
    sched = {"track_u_real_finished": True, "frozen_registries_awaiting_draw": []}
    assert ok_of(grec.window_ok(sched, root=tmp_path))
    assert not ok_of(grec.window_ok(dict(sched, track_u_real_finished=False), root=tmp_path))
    assert not ok_of(grec.window_ok(dict(sched, frozen_registries_awaiting_draw=["K-REG9"]),
                                    root=tmp_path))
    foreign = tmp_path / "hwsu-store"
    foreign.mkdir()
    (foreign / "OPERATION_ACTIVE.json").write_text(json.dumps({"active": True}), encoding="utf-8")
    assert not ok_of(grec.window_ok(sched, root=tmp_path))


def test_ledger_append_duplicate_label_refused(tmp_path):
    grec = mod("grec")
    path = tmp_path / "LEDGER.json"
    grec.ledger_append(path, "0224-TRAIN-lo-620611-a1", "0224", "TRAIN", 12.5, "meter",
                       world="lo", master=620611)
    grec.ledger_append(path, "0224-TRAIN-lo-620612-a1", "0224", "TRAIN", 7.0, "meter",
                       world="lo", master=620612)
    expect_fail("FAIL_TECHNICAL/LEDGER", grec.ledger_append, path, "0224-TRAIN-lo-620611-a1",
                "0224", "TRAIN", 1.0, "meter", world="lo", master=620611)
    led = grec.ledger_read(path)
    assert led["study"] == "hwsg-v1" and len(led["entries"]) == 2
    assert led["cumulative_cpu_s"] == pytest.approx(19.5)
