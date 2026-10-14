"""Independent integration regressions for the X5 G1 v4 stage integration (API v4 §2, §4, §6, §7).

Written from the contract only (test writer F, job 0010): the actual stages and CLI on the tiny
SYNTHETIC fixture. Reproduces the job-0009 root probes (control STOP during an export, fresh draw
entered despite a STOP) and checks guard wiring, tampered prerequisites and a read-only validate.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import types
from pathlib import Path

import pytest

from topo_pilot.experiment import x5g1t_exports, x5g1t_lineage, x5g1t_runtime, x5g1t_stages_eval
from topo_pilot.experiment.x5g1t_exports import ExportIncomplete, verify_export_complete
from topo_pilot.experiment.x5g1t_fixture import build_fixture
from topo_pilot.experiment.x5g1t_main import main

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]
ARMS, MASTERS = ("a0", "a020"), (310001, 310002, 310003)
SIZES = {"train": 64, "dev": 1100, "test": 24}  # dev > 2 * SCORE_BATCH: three score batches
_REAL_DUMPS = json.dumps


def _cli(cfg, *args) -> int:
    return main(["--config", str(cfg), "--repo", str(REPO), *args])


def _tables(root: Path) -> Path:
    return root / "study" / "tables"


def _ledger_last(root: Path) -> dict:
    return json.loads((root / "ledger.json").read_text(encoding="utf-8"))["entries"][-1]


def _snapshot(root: Path) -> dict:
    out = {}
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = Path(dp) / f
            st = p.stat()
            out[str(p.relative_to(root))] = (st.st_size, st.st_mtime_ns,
                                             hashlib.sha256(p.read_bytes()).hexdigest())
    return out


def _clone(src: Path, dst: Path) -> Path:
    """Copy a fixture root and re-point its config's absolute paths at the copy."""
    shutil.copytree(src, dst)
    cfg_path = dst / "study_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    def fix(v):
        if isinstance(v, str):
            return v.replace(str(src), str(dst))
        if isinstance(v, list):
            return [fix(x) for x in v]
        if isinstance(v, dict):
            return {k: fix(x) for k, x in v.items()}
        return v

    for key in ("read_roots", "study_root", "ledger_path", "mailbox"):
        cfg[key] = fix(cfg[key])
    cfg_path.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    return cfg_path


def _on_first_export_write(monkeypatch, action):
    """Run ``action`` while the first export file is being serialised (the write in flight)."""
    state = {"n": 0}

    def dumps(*a, **k):
        state["n"] += 1
        if state["n"] == 1:
            action()
        return _REAL_DUMPS(*a, **k)

    monkeypatch.setattr(x5g1t_exports, "json",
                        types.SimpleNamespace(dumps=dumps, loads=json.loads))
    return state


def _write_json(path: Path, obj) -> None:
    path.write_text(_REAL_DUMPS(obj), encoding="utf-8")


# --- shared expensive states (built once, cloned per test) -----------------------------------

@pytest.fixture(scope="module")
def pools_root(tmp_path_factory) -> Path:
    root = tmp_path_factory.mktemp("pools_base") / "fx"
    cfg = build_fixture(root, sizes=SIZES)
    assert _cli(cfg, "pools") == 0
    return root


@pytest.fixture(scope="module")
def trained_root(pools_root, tmp_path_factory) -> Path:
    root = tmp_path_factory.mktemp("trained_base") / "fx"
    cfg = _clone(pools_root, root)
    for m in MASTERS:
        for a in ARMS:
            assert _cli(cfg, "train", "--arm", a, "--master", str(m)) == 0
    return root


@pytest.fixture(scope="module")
def dev_done(trained_root, tmp_path_factory):
    """dev-analysis on a clone of the trained state, with the oracle/score guards recorded."""
    root = tmp_path_factory.mktemp("dev_base") / "fx"
    cfg = _clone(trained_root, root)
    calls = {"oracle_q32": [], "regret_rows": []}

    def spy(name, real):
        def wrapped(*a, **k):
            guard = k.get("guard")
            rec = {"guard_callable": callable(guard), "labels": []}
            calls[name].append(rec)
            if callable(guard):
                def recording_guard(label, *ga, **gk):
                    rec["labels"].append(label)
                    return guard(label, *ga, **gk)
                k["guard"] = recording_guard
            return real(*a, **k)
        return wrapped

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(x5g1t_stages_eval, "oracle_q32",
                   spy("oracle_q32", x5g1t_stages_eval.oracle_q32))
        mp.setattr(x5g1t_stages_eval, "regret_rows",
                   spy("regret_rows", x5g1t_stages_eval.regret_rows))
        rc = _cli(cfg, "dev-analysis")
    return root, rc, calls


# --- 1/2. STOP during the pools export (root probe) ------------------------------------------

def _stop_worker_control(mb: Path):
    _write_json(mb / "worker_control.json", {"command": "STOP"})


def _stop_request(mb: Path):
    _write_json(mb / "request.json", {"command": "STOP"})


def _stop_file(mb: Path):
    (mb / "STOP").write_text("stop", encoding="utf-8")


def _clear_stops(mb: Path):
    for name in ("worker_control.json", "STOP"):
        if (mb / name).exists():
            (mb / name).unlink()
    _write_json(mb / "request.json", {"command": "RUN_NEXT"})


@pytest.mark.parametrize("source", [_stop_worker_control, _stop_request, _stop_file],
                         ids=["worker_control", "request", "stop_file"])
def test_stop_during_pools_export_writes_no_further_file(tmp_path, monkeypatch, caplog, source):
    cfg = build_fixture(tmp_path)
    mb = tmp_path / "mailbox"
    trig = _on_first_export_write(monkeypatch, lambda: source(mb))
    assert _cli(cfg, "pools") == 2
    assert trig["n"] >= 1, "the pools export never serialised a file"
    out = _tables(tmp_path) / "pools"
    status = json.loads((out / "EXPORT_STATUS.json").read_text(encoding="utf-8"))
    assert status["status"] == "STOPPED_DURING_EXPORT"
    # Only the file in flight when the STOP appeared; nothing after the boundary that saw it.
    assert len(status["completed_steps"]) == 1
    present = {p.name for p in out.iterdir()}
    assert present == {status["completed_steps"][0], "EXPORT_STATUS.json"}
    assert "MANIFEST.json" not in present
    with pytest.raises(ExportIncomplete):
        verify_export_complete(out)
    assert _ledger_last(tmp_path)["status"] == "stopped"
    # A later train with the controls cleared refuses: incomplete prerequisite.
    monkeypatch.undo()
    _clear_stops(mb)
    caplog.clear()
    assert _cli(cfg, "train", "--arm", "a0", "--master", "310001") == 3
    assert "ExportIncomplete" in caplog.text
    assert not (_tables(tmp_path) / "train" / "a0_310001" / "EXPORT_STATUS.json").exists()


# --- 3. HOLD released by the injected sleep ---------------------------------------------------

@pytest.mark.parametrize("when", ["stage_start", "during_export"])
def test_hold_released_by_sleep_completes(tmp_path, monkeypatch, when):
    cfg = build_fixture(tmp_path)
    mb = tmp_path / "mailbox"
    sleeps = []

    def hold():
        _write_json(mb / "worker_control.json", {"command": "WAIT_USAGE_RESET"})

    def fake_sleep(s):
        sleeps.append(s)
        if len(sleeps) > 5:
            raise AssertionError("hold was not released by CONTINUE")
        _write_json(mb / "worker_control.json", {"command": "CONTINUE"})

    monkeypatch.setattr(x5g1t_runtime.time, "sleep", fake_sleep)
    if when == "stage_start":
        hold()
    else:
        _on_first_export_write(monkeypatch, hold)
    assert _cli(cfg, "pools") == 0
    assert len(sleeps) >= 1, "the HOLD never reached the injected sleep"
    out = _tables(tmp_path) / "pools"
    status = json.loads((out / "EXPORT_STATUS.json").read_text(encoding="utf-8"))
    assert status["status"] == "COMPLETE"
    manifest = verify_export_complete(out)
    assert {"pools.json", "run.json"} <= set(manifest)
    assert _ledger_last(tmp_path)["status"] == "ok"


# --- 4. No fresh draw on STOP or ID collision -------------------------------------------------

def _draw_spy(monkeypatch):
    calls = []
    real = x5g1t_stages_eval.draw_pair

    def spy(*a, **k):
        calls.append((a, k))
        return real(*a, **k)

    monkeypatch.setattr(x5g1t_stages_eval, "draw_pair", spy)
    return calls


def _final_done(root: Path) -> bool:
    return (_tables(root) / "final_test" / "MANIFEST.json").exists()


def test_final_test_control_draws_once(dev_done, tmp_path, monkeypatch):
    """Positive control: the draw spy sees the fresh draw when nothing stops it."""
    src, rc, _ = dev_done
    assert rc == 0
    cfg = _clone(src, tmp_path / "fx")
    calls = _draw_spy(monkeypatch)
    assert _cli(cfg, "final-test", "--authorized-final") == 0
    assert len(calls) == 1
    verify_export_complete(_tables(tmp_path / "fx") / "final_test")


def test_stop_before_fresh_draw_never_draws(dev_done, tmp_path, monkeypatch):
    src, rc, _ = dev_done
    assert rc == 0
    root = tmp_path / "fx"
    cfg = _clone(src, root)
    _stop_worker_control(root / "mailbox")
    calls = _draw_spy(monkeypatch)
    assert _cli(cfg, "final-test", "--authorized-final") == 2
    assert calls == []
    assert not _final_done(root)


def test_stop_during_collision_check_never_draws(dev_done, tmp_path, monkeypatch):
    """The STOP appears after the stage started, while the fresh IDs are being planned."""
    src, rc, _ = dev_done
    assert rc == 0
    root = tmp_path / "fx"
    cfg = _clone(src, root)
    real_ids = x5g1t_stages_eval.sequence_ids

    def ids(split, *a, **k):
        if split == "test":
            _stop_worker_control(root / "mailbox")
        return real_ids(split, *a, **k)

    monkeypatch.setattr(x5g1t_stages_eval, "sequence_ids", ids)
    calls = _draw_spy(monkeypatch)
    assert _cli(cfg, "final-test", "--authorized-final") == 2
    assert calls == []
    assert not _final_done(root)


def test_fresh_id_collision_refuses_without_draw(dev_done, tmp_path, monkeypatch, caplog):
    src, rc, _ = dev_done
    assert rc == 0
    root = tmp_path / "fx"
    cfg = _clone(src, root)
    real_ids = x5g1t_stages_eval.sequence_ids

    def ids(split, arm, master, n):
        if split == "test":  # collide with the study store's dev pool of the same arm
            return x5g1t_lineage.sequence_ids("dev", arm, MASTERS[0], n)
        return real_ids(split, arm, master, n)

    monkeypatch.setattr(x5g1t_stages_eval, "sequence_ids", ids)
    calls = _draw_spy(monkeypatch)
    assert _cli(cfg, "final-test", "--authorized-final") == 3
    assert "collision" in caplog.text
    assert calls == []
    assert not _final_done(root)


# --- 5. Guard counts in dev-analysis -----------------------------------------------------------

def test_dev_analysis_calls_batch_and_oracle_guards(dev_done):
    root, rc, calls = dev_done
    assert rc == 0
    verify_export_complete(_tables(root) / "dev_analysis")
    for name in ("oracle_q32", "regret_rows"):
        assert calls[name], f"{name} was never called"
        assert all(c["guard_callable"] for c in calls[name]), f"{name} without a callable guard"
    for c in calls["oracle_q32"]:
        assert len(c["labels"]) >= 2, "oracle batch guard not called before and after"
    n_batches = -(-SIZES["dev"] // 512)
    for c in calls["regret_rows"]:
        expected = [lab for k in range(n_batches)
                    for lab in (f"score batch {k}", f"score batch {k} done")]
        assert [lab for lab in c["labels"] if lab.startswith("score batch")] == expected


def test_scoring_guard_is_a_real_boundary(trained_root, tmp_path, monkeypatch):
    """A STOP that appears at 'score batch 1' stops dev-analysis with no result export."""
    root = tmp_path / "fx"
    cfg = _clone(trained_root, root)
    real = x5g1t_stages_eval.regret_rows

    def wrapped(*a, **k):
        guard = k["guard"]

        def g(label, *ga, **gk):
            if label == "score batch 1":
                _stop_worker_control(root / "mailbox")
            return guard(label, *ga, **gk)
        k["guard"] = g
        return real(*a, **k)

    monkeypatch.setattr(x5g1t_stages_eval, "regret_rows", wrapped)
    assert _cli(cfg, "dev-analysis") == 2
    out = _tables(root) / "dev_analysis"
    assert not (out / "MANIFEST.json").exists()
    assert not (out / "result.json").exists()


# --- 6. Tampered prerequisites ----------------------------------------------------------------

@pytest.mark.parametrize("tamper", ["mutate_pools_json", "extra_file"])
def test_tampered_pools_export_refuses_train(pools_root, tmp_path, caplog, tamper):
    root = tmp_path / "fx"
    cfg = _clone(pools_root, root)
    out = _tables(root) / "pools"
    verify_export_complete(out)
    if tamper == "mutate_pools_json":
        p = out / "pools.json"
        b = bytearray(p.read_bytes())
        i = b.index(b'"pools"')
        b[i + 1] = ord("P")  # same length, different bytes
        p.write_bytes(bytes(b))
    else:
        (out / "notes.json").write_text("{}", encoding="utf-8")
    assert _cli(cfg, "train", "--arm", "a0", "--master", "310001") == 3
    assert "ExportIncomplete" in caplog.text
    assert not (_tables(root) / "train" / "a0_310001" / "MANIFEST.json").exists()


def test_extra_file_in_train_export_refuses_dev_analysis(trained_root, tmp_path, caplog):
    root = tmp_path / "fx"
    cfg = _clone(trained_root, root)
    out = _tables(root) / "train" / "a0_310001"
    verify_export_complete(out)
    (out / "extra.json").write_text("{}", encoding="utf-8")
    assert _cli(cfg, "dev-analysis") == 3
    assert "ExportIncomplete" in caplog.text
    da = _tables(root) / "dev_analysis"
    assert not (da / "MANIFEST.json").exists()
    assert not (da / "result.json").exists()


# --- 7. validate is read-only -----------------------------------------------------------------

def test_validate_is_read_only(tmp_path, capsys):
    cfg = build_fixture(tmp_path)
    study = tmp_path / "study"
    study_before = sorted(os.listdir(study)) if study.exists() else None
    before = _snapshot(tmp_path)
    assert _cli(cfg, "validate") == 0
    report = json.loads(capsys.readouterr().out)
    assert report["mode"] == "synthetic-fixture"
    assert _snapshot(tmp_path) == before  # nothing in the study root, mailbox or ledger
    assert (sorted(os.listdir(study)) if study.exists() else None) == study_before
    assert not (tmp_path / "ledger.json").exists()
