"""Author B (operations): T-CHAIN (discovery, quarantine, marker), T-LINEAGE, T-ENV-LOCAL, T-METER,
T-BUNDLE (classes, code.tar), T-INGEST (execution records) (X6S1-FROZEN-v1 §5, §12-§14; API.md).

Synthetic fixtures only (tmp_path); no real store, mailbox or meter binding is read or written.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import re
import subprocess
import sys
import tarfile
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_cloud as sc  # noqa: E402
import x6s1_data as sd  # noqa: E402
import x6s1_ingest as si  # noqa: E402
import x6s1_run as sr  # noqa: E402
import x6_store as xs  # noqa: E402
from topo_pilot.contracts import canonical_json  # noqa: E402

MODEL = "SMOKE"
ENTRY = {"model": MODEL, "run_key": ["x6s1", "smoke"]}
ENV_KEYS = {"python", "numpy", "torch", "blas", "cpu", "threads", "thread_env", "batch", "commit"}


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _fake_ckpt(step):
    buf = io.BytesIO()
    torch.save({"model": {"w": torch.full((3,), float(step))}, "optimizer": {},
                "scheduler": {"last_epoch": step}, "rng": {"pcg64": {}, "torch_cuda": []},
                "step": step}, buf)
    return buf.getvalue()


def build_chain(mdir, steps_list, entry=ENTRY):
    (mdir / "ckpt").mkdir(parents=True, exist_ok=True)
    (mdir / "rec").mkdir(exist_ok=True)
    prev, recs = sc.sha256_json(entry), []
    for s in steps_list:
        fsha = sc.write_checkpoint(mdir, s, _fake_ckpt(s))
        wsha = sc.weights_digest({"w": torch.full((3,), float(s))})
        pcg = np.random.Generator(np.random.PCG64(s)).bit_generator.state
        chunk = (None, None, None, None) if s == 0 else (1.0, 0.9, True, 0.5)
        rec = sc.make_record(MODEL, s, fsha, wsha, None if s == 0 else "ab" * 32, pcg, prev,
                             "sess", "cpu", None, *chunk)
        sc.write_json_atomic(mdir / "rec" / f"{s:06d}.json", rec)
        prev = rec["record_sha256"]
        recs.append(rec)
    return recs


def _names(paths):
    return {Path(p).name for p in paths}


def _marker(mdir, recs):
    return sc.write_marker(mdir, {"schema": sc.MARKER_SCHEMA, "model": MODEL, "step": 3,
                                  "chunk": 2, "session_id": "sess", "loss_bits": "7fc00000",
                                  "prev_record_sha256": recs[-1]["record_sha256"],
                                  "utc": "2026-10-19T00:00:00Z"})


# ---------------------------------------------------------------- T-CHAIN (discover)
def test_discover_full_chain_and_prefix(tmp_path):
    recs = build_chain(tmp_path / "m", [0, 2, 4])
    assert all(sc.valid_record(tmp_path / "m", r) for r in recs)
    assert all(r["record_sha256"] == sc.record_sha(r) for r in recs)
    assert recs[0]["prev_record_sha256"] == sc.sha256_json(ENTRY)
    assert all(recs[0][k] is None for k in ("batch_sha256", "train_loss_first", "train_loss_last",
                                            "loss_finite", "wall_s"))  # RC7 step-0 nulls
    d = sc.discover(tmp_path / "m", ENTRY, 4, 2)
    assert d["status"] == "OK" and d["last_step"] == 4 and d["terminal"] is None
    assert [r["step"] for r in d["chain"]] == [0, 2, 4] and d["orphans"] == []
    build_chain(tmp_path / "p", [0, 3])
    d = sc.discover(tmp_path / "p", ENTRY, 6, 3)  # parameterised by ticket steps and K
    assert d["status"] == "OK" and d["last_step"] == 3


@pytest.mark.parametrize("kind,name", [
    ("part_ckpt", "000004.pt.part"), ("part_rec", "000004.json.part"),
    ("ckpt_no_rec", "000004.pt"), ("rec_no_ckpt", "000004.json"), ("truncated", "000004.json"),
])
def test_discover_lists_nonterminal_orphans(tmp_path, kind, name):
    mdir = tmp_path / "m"
    recs = build_chain(mdir, [0, 2])
    data = _fake_ckpt(4)
    rec4 = sc.make_record(MODEL, 4, _sha(data), "cd" * 32, "ab" * 32, {"x": 1},
                          recs[-1]["record_sha256"], "sess", "cpu", None, 1.0, 1.0, True, 0.5)
    raw = canonical_json(rec4).encode("utf-8")
    if kind == "part_ckpt":
        (mdir / "ckpt" / name).write_bytes(data[:10])
    elif kind in ("part_rec", "rec_no_ckpt"):
        (mdir / "rec" / name).write_bytes(raw)
    elif kind == "ckpt_no_rec":
        (mdir / "ckpt" / name).write_bytes(data)
    else:
        (mdir / "ckpt" / "000004.pt").write_bytes(data)
        (mdir / "rec" / name).write_bytes(raw[: len(raw) // 2])
    d = sc.discover(mdir, ENTRY, 4, 2)
    assert d["status"] == "OK" and d["last_step"] == 2
    assert name in _names(d["orphans"])


def test_discover_broken_interior_link(tmp_path):
    mdir = tmp_path / "m"
    build_chain(mdir, [0, 2, 4])
    p = mdir / "ckpt" / "000002.pt"
    p.write_bytes(p.read_bytes() + b"\x00")  # step-2 digest fails, step 4 still links to it
    assert sc.discover(mdir, ENTRY, 4, 2)["status"] == "CHAIN_BROKEN"


def test_discover_read_failure_is_hold_then_stable_reread(tmp_path, monkeypatch):
    import builtins

    mdir = tmp_path / "m"
    build_chain(mdir, [0, 2])
    before = sorted(p.relative_to(mdir) for p in mdir.rglob("*"))
    real_open = io.open

    def flaky(file, *args, **kwargs):
        if str(file).endswith("000002.json"):
            raise PermissionError("synthetic Drive read failure")
        return real_open(file, *args, **kwargs)
    monkeypatch.setattr(io, "open", flaky)
    monkeypatch.setattr(builtins, "open", flaky)
    assert sc.discover(mdir, ENTRY, 4, 2)["status"] == "HOLD"
    monkeypatch.undo()
    assert sorted(p.relative_to(mdir) for p in mdir.rglob("*")) == before  # nothing moved
    assert sc.discover(mdir, ENTRY, 4, 2)["last_step"] == 2


def test_terminal_marker_survives_quarantine(tmp_path):
    root = tmp_path / "root"
    mdir = root / "out" / MODEL
    recs = build_chain(mdir, [0, 2])
    assert sc.read_marker(mdir) is None
    _marker(mdir, recs)
    m = sc.read_marker(mdir)
    body = {k: v for k, v in m.items() if k != "marker_sha256"}
    assert m["marker_sha256"] == sc.sha256_json(body) and m["step"] == 3
    with pytest.raises((sc.CloudStop, FileExistsError)):
        _marker(mdir, recs)
    part = mdir / "ckpt" / "000004.pt.part"
    part.write_bytes(b"partial checkpoint")
    d = sc.discover(mdir, ENTRY, 4, 2)
    assert d["terminal"] == m and "NONFINITE.json" not in _names(d["orphans"])
    q = sc.quarantine(root, MODEL, d["orphans"], "20261019T000000Z")
    assert len(q) == 1 and q[0]["sha256"] == _sha(b"partial checkpoint")
    assert Path(q[0]["original"]).name == "000004.pt.part" and not part.exists()
    kept = list((root / "orphans").rglob("000004.pt.part"))
    assert len(kept) == 1 and kept[0].read_bytes() == b"partial checkpoint"
    assert "20261019T000000Z-SMOKE" in kept[0].as_posix()
    assert sc.read_marker(mdir) == m
    d2 = sc.discover(mdir, ENTRY, 4, 2)
    assert d2["orphans"] == [] and d2["terminal"] == m and d2["last_step"] == 2


def test_quarantine_never_touches_chain_elements(tmp_path):
    root = tmp_path / "root"
    mdir = root / "out" / MODEL
    build_chain(mdir, [0, 2])
    files = {p: p.read_bytes() for p in mdir.rglob("*") if p.is_file()}
    sc.quarantine(root, MODEL, sc.discover(mdir, ENTRY, 4, 2)["orphans"], "20261019T000001Z")
    assert {p: p.read_bytes() for p in mdir.rglob("*") if p.is_file()} == files


@pytest.mark.parametrize("bad", ["garbage", "tampered"])
def test_unreadable_marker_stops_recovery(tmp_path, bad):
    mdir = tmp_path / "m"
    recs = build_chain(mdir, [0, 2])
    path = mdir / "rec" / "NONFINITE.json"
    if bad == "garbage":
        path.write_bytes(b"{\"step\": ")
    else:
        m = _marker(mdir, recs)
        path.unlink()
        path.write_bytes(canonical_json(dict(m, step=4)).encode("utf-8"))
    with pytest.raises(sc.CloudStop, match="STOP: MARKER UNREADABLE"):
        sc.read_marker(mdir)
    assert sc.discover(mdir, ENTRY, 4, 2)["status"] == "MARKER_UNREADABLE"


# ---------------------------------------------------------------- T-LINEAGE
def _run_dir(store, payload=b'{"a":1}'):
    gate = store / "run" / "gates" / "G1"
    gate.mkdir(parents=True)
    (gate / "values.json").write_bytes(payload)
    (store / "run" / "GATES.jsonl").write_bytes(b'{"gate":"G1"}\n')


def test_supersede_manifest_and_bit_identical_regeneration(tmp_path):
    store = tmp_path / "store"
    _run_dir(store)
    a1 = sr.archive_attempt(store, "0070")
    assert Path(a1).name == "0070-a1" and not (store / "run").exists()
    man = sr.read_manifest(Path(a1) / "SHA256SUMS")
    assert man["run/gates/G1/values.json"] == _sha(b'{"a":1}')
    assert all(_sha((Path(a1) / rel).read_bytes()) == h for rel, h in man.items())
    assert sr.lineage_precheck(store)["status"] == "PASS"
    regen = tmp_path / "regen"
    (regen / "gates" / "G1").mkdir(parents=True)
    (regen / "gates" / "G1" / "values.json").write_bytes(b'{"a":1}')
    assert sr.compare_attempt(a1, regen)["status"] == "PASS"  # unaffected: bit-identical
    (regen / "gates" / "G1" / "values.json").write_bytes(b'{"a":2}')
    assert sr.compare_attempt(a1, regen)["status"] == "INVALID/LINEAGE"
    _run_dir(store)
    assert Path(sr.archive_attempt(store, "0070")).name == "0070-a2"  # unique per attempt
    (store / "stray.txt").write_text("unrecognised", encoding="utf-8")
    assert sr.lineage_precheck(store)["status"] == "INVALID/LINEAGE"


def test_volatile_fields_ignored_in_report_comparison():
    extra = {"session_id", "pid", "peak_mem_bytes", "built_utc", "env_local"}
    assert set(sr.VOLATILE_KEYS) >= set(xs.VOLATILE_KEYS) | extra
    base = {"outcome": "ORDER_NOT_DETECTED", "gates": {"S0": "PASS"}}
    for key in sorted(sr.VOLATILE_KEYS):
        # API-AMBIGUITY: API §11.3 extends VOLATILE_KEYS but reuses x6_store.strip_volatile and
        # reports_equal "unchanged"; the protocol intent (these keys are volatile) is tested.
        a, b = dict(base, **{key: 1}), dict(base, **{key: 2})
        assert sr.reports_equal(a, b), key
    assert not sr.reports_equal(base, dict(base, outcome="INCONCLUSIVE"))


def test_regenerated_init_states_are_bit_identical():
    a, b = sd.init_state("NA-s2")["model"], sd.init_state("NA-s2")["model"]
    assert sc.weights_digest(a) == sc.weights_digest(b)
    assert sc.weights_digest(a) != sc.weights_digest(sd.init_state("NA-s3")["model"])


def test_retrain_route_refused_after_admission_or_any_local_evaluation(tmp_path):
    store = tmp_path / "store"
    store.mkdir()
    assert si.retrain_eligible(store, "NA-s1", []) is True
    for ev in (["LOSS-ECHO"], ["dev_curve"], ["validation"], ["emergence"]):
        assert si.retrain_eligible(store, "NA-s1", ev) is False
    assert sr.retrain_route_ok(store, "NA-s1") is True
    info = {"model": "NA-s1", "bundle_id": "C1-0123456789ab", "manifest_sha256": "a" * 64,
            "final_file_sha256": "b" * 64, "final_weights_sha256": "c" * 64,
            "chain_record_sha256": ["d" * 64], "utc": "2026-10-19T00:00:00Z"}
    lock = si.write_admission_lock(store, "NA-s1", info)
    assert Path(lock) == store / "cloud" / "ADMITTED" / "NA-s1.json"
    got = si.admitted(store, "NA-s1")
    assert got["final_weights_sha256"] == "c" * 64 and got["bundle_id"] == info["bundle_id"]
    before = Path(lock).read_bytes()
    with pytest.raises(FileExistsError):
        si.write_admission_lock(store, "NA-s1", dict(info, final_weights_sha256="e" * 64))
    assert Path(lock).read_bytes() == before
    assert si.retrain_eligible(store, "NA-s1", []) is False
    assert sr.retrain_route_ok(store, "NA-s1") is False
    assert si.admitted(store, "NA-s2") is None and si.retrain_eligible(store, "NA-s2", [])


# ---------------------------------------------------------------- T-ENV-LOCAL
def _head():
    return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def test_env_local_record_complete():
    env = sr.env_local()
    assert set(env) >= ENV_KEYS
    assert env["batch"] == sd.EVAL_BATCH == 1024
    assert set(env["threads"]) == {"intra", "interop"}
    assert set(env["thread_env"]) >= {"OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"}
    assert env["numpy"] == np.__version__ and env["torch"] == torch.__version__
    assert re.fullmatch(r"[0-9a-f]{40}", env["commit"]) and env["commit"] == _head()
    assert env["blas"] and env["cpu"]
    json.dumps(env, default=str)


def test_env_changed_reports_only_real_changes():
    a = sr.env_local()
    assert sr.env_changed(a, dict(a)) == []
    assert sr.env_changed(a, dict(a, torch="0.0.0")) == ["torch"]
    assert sorted(sr.env_changed(a, dict(a, numpy="0", batch=7))) == ["batch", "numpy"]


def test_evaluating_stage_record_holds_env_local(tmp_path):
    # API-AMBIGUITY: API §11.3 says every evaluating stage record holds "env_local" but fixes no
    # refusal for a record without it; the written record is checked for completeness only.
    p = sr.write_stage(tmp_path, "E3a", {"gates": {"E3.0": "PASS"}, "env_local": sr.env_local()})
    rec = json.loads(Path(p).read_text(encoding="utf-8"))
    assert set(rec["env_local"]) >= ENV_KEYS
    assert (tmp_path / "STAGES.jsonl").is_file()
    with pytest.raises(FileExistsError):
        sr.write_stage(tmp_path, "E3a", {"env_local": sr.env_local()})


# ---------------------------------------------------------------- T-METER
def test_meter_values():
    assert sr.METER_VALUES == {"OUTPUT_CAP": 16 * 2**30, "MEMORY_CAP": 12 * 2**30,
                               "CAP_S": math.inf, "STOP_NEW_S": math.inf}
    assert sd.OUTPUT_CAP == 16 * 2**30 and sd.JOB_MEM == 12 * 2**30
    assert sd.PROCESS_MEM == 3 * 2**30


def test_meter_bind_check_refusals(tmp_path):
    bind = tmp_path / "x6s1_meter_bind.py"
    bind.write_text("import meter, winjob\nmeter.CAP_S = meter.STOP_NEW_S = float('inf')\n"
                    "meter.OUTPUT_CAP = 16 * 1024**3\nwinjob.MEMORY_CAP = 12 * 1024**3\n",
                    encoding="utf-8")
    sha = _sha(bind.read_bytes())
    good = Path(sd.WORKTREE) / "tools" / "x4_oracle_profile"
    assert sr.meter_bind_check(bind, sha, good) is None
    with pytest.raises(RuntimeError):
        sr.meter_bind_check(bind, "0" * 64, good)
    main_tree = Path(sd.PROJECT_ROOT) / "topo-pilot" / "tools" / "x4_oracle_profile"
    with pytest.raises(RuntimeError):
        sr.meter_bind_check(bind, sha, main_tree)  # the main worktree's meter is refused
    bind.write_text(bind.read_text(encoding="utf-8") + "# edited\n", encoding="utf-8")
    with pytest.raises(RuntimeError):
        sr.meter_bind_check(bind, sha, good)


# ---------------------------------------------------------------- T-BUNDLE (classes, code.tar)
@pytest.mark.parametrize("rel,bad", [
    ("data/val_NA.npy", True), ("data/test_NA.npy", True), ("data/gate_NA.npy", True),
    ("data/prefix.npy", True), ("data/dev_NA_s1.npy", True), ("sealed/learn.json", True),
    ("registry/X6-REG2.json", True), ("data/states.npy", True), ("data/latent_z.npy", True),
    ("Data/TEST_na.npy", True), ("notes.txt", True), ("code.tar", False), ("SHA256SUMS", False),
    ("ticket_C1.json", False), ("data/train_NA_s1.npy", False), ("init/init_s1.pt", False),
    ("data/smoke.npy", False), ("init/init_smoke.pt", False), ("X6S1_colab.ipynb", False)])
def test_forbidden(rel, bad):
    assert si.forbidden(rel) is bad


@pytest.mark.parametrize("wave,rel,ok", [
    ("C1", "data/train_NA_s1.npy", True), ("C1", "data/train_ZC_s1.npy", True),
    ("C1", "init/init_s2.pt", True), ("C1", "data/train_NA_s3.npy", False),
    ("C1", "data/train_AB_s1.npy", False), ("C1", "init/init_s3.pt", False),
    ("C1", "data/smoke.npy", False), ("C0", "data/smoke.npy", True),
    ("C0", "init/init_smoke.pt", True), ("C0", "data/train_NA_s1.npy", False),
    ("C2", "data/train_AB_s4.npy", True), ("C2", "data/train_NA_s1.npy", False)])
def test_allowed_class(wave, rel, ok):
    assert si.allowed_class(rel, wave, sd.WAVES[wave]) is ok


def test_code_tar_is_git_archive_of_head(tmp_path):
    head, out = _head(), tmp_path / "code.tar"
    assert si.code_tar(REPO, head, out) == _sha(out.read_bytes())
    with tarfile.open(out) as tf:
        assert tf.pax_headers.get("comment") == head
        names = [m.name for m in tf.getmembers() if m.isfile()]
    assert "tools/x6_stage1/x6s1_cloud.py" in names and "pyproject.toml" in names
    assert all(n == "pyproject.toml" or n.startswith(("src/", "tools/x6_stage1/")) for n in names)


# ---------------------------------------------------------------- T-INGEST (execution records)
T = list(sc.CELL_TEMPLATES)
PASTED = T[1].replace(sc.HASH_PLACEHOLDER, "AB" * 32)


def _start(seq, sid="s1"):
    return {"schema": sc.SESSION_SCHEMA, "kind": "start", "session_id": sid,
            "executed_cells": [T[i - 1] if isinstance(i, int) else i for i in seq]}


def _final(start, seq):
    f = _start(seq, start["session_id"])
    f.update(kind="final", start_record={"file": f"20261019T000000Z-{start['session_id']}"
                                         ".start.json", "sha256": sc.sha256_json(start)})
    return f


@pytest.mark.parametrize("seq", [[1, 2, 3, 4, 5], [1, 2, 2, 3, 4, 5], [1, 2, 3, 4, 3, 4, 5],
                                 [1, PASTED, 3, 4, 5], [1, 1, 2, 3, 4, 5]])
def test_check_execution_accepts_registered_sequences(seq):
    s = _start(seq)
    assert si.check_execution([s])["status"] == "PASS"  # no cell-6 record: accepted
    assert si.check_execution([s, _final(s, seq + [6])])["status"] == "PASS"


@pytest.mark.parametrize("seq", [[1, 2, 3, T[3] + "\nprint(1)", 5], [1, 2, 3, 4, "import os", 5],
                                 [1, 3, 2, 4, 5], [2, 3, 4, 5], [1, 2, 3, 5], [1, 2, 3, 4, 5, 6]])
def test_check_execution_refuses_edits_extra_code_and_order(seq):
    assert si.check_execution([_start(seq)])["status"] == "FAIL"


def test_check_execution_final_record_rules():
    s, other = _start([1, 2, 3, 4, 5]), _start([1, 2, 3, 4, 5, 5])
    assert si.check_execution([s, _final(other, [1, 2, 3, 4, 5, 6])])["status"] == "FAIL"
    assert si.check_execution([s, _final(s, [1, 2, 3, 4, 5, T[5] + "\nx = 1"])])["status"] == "FAIL"
