"""Author B (job 0119), TEST_PLAN §3 `test_b_records.py` and `test_b_meter.py` (merged: job
0119 task.md allows at most five author-B files; the G0 seed-search tests live in
`test_b_kc1.py`). Records: STAGES.jsonl line format, `save_hist` paths and the canon32 key,
exclusive-create refusals, `tree_sha`, `archive_partial` with SHA256SUMS, resume regenerating an
interrupted synthetic world bit-identically, FREEZE.json fields and the implementation hash,
`main` refusals (exit 2, nothing sampled), the pytest basetemp outside the project root.
Meter (§9.2 RC-9, DR12): `hm.bind` (MEMORY_CAP 8 GiB, TEMP_ROOT = out), `effective_settings`,
`main` (--max-cpu inf --max-wall inf, child env, RUN.lock refusal) with meter.main faked.

Every module global and environment variable the binding touches is restored by monkeypatch.
Written without reading tools/hws/*.py."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hws") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hws"))

import hws_worlds as hw  # noqa: E402
import hws_oracle as ho  # noqa: E402
import hws_driver as hd  # noqa: E402
import hws_meter_bind as hm  # noqa: E402

import controls  # noqa: E402
import k4b_meter_bind  # noqa: E402
import meter  # noqa: E402
import op_guard  # noqa: E402
import stage_records  # noqa: E402
import winjob  # noqa: E402
from topo_pilot.contracts import SequenceLayout, canonical_json  # noqa: E402
from topo_pilot.dataset.sampler import HMMSampler  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hws" / "CONTRACT.json").read_text(encoding="utf-8"))
INF = float("inf")
GIB = 1024**3
TINY = SequenceLayout(n_obs=9, context=8, analysis_position=8)


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _put(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _under(p: Path, root: Path) -> bool:
    s = str(p.resolve()).replace("\\", "/").lower()
    r = str(root.resolve()).replace("\\", "/").lower().rstrip("/") + "/"
    return s.startswith(r)


def _code(fn, *args) -> int:
    try:
        return int(fn(*args))
    except SystemExit as exc:
        return int(exc.code if isinstance(exc.code, int) else 2)


def _event(kind: str, **fields) -> dict:
    # API-AMBIGUITY: API.md names the event types but not the key holding them; the same type
    # is written under "event", "type" and "kind" so any reader of these keys finds it.
    return dict(fields, event=kind, type=kind, kind=kind)


# ------------------------------------------------------------------------------ records

def test_pytest_basetemp_is_outside_the_project_root(tmp_path):
    assert hw.ROOT == Path("X:/Downloads/projects/topo-pilot")
    assert not _under(tmp_path, hw.ROOT) and not _under(tmp_path, REPO)


def test_append_stage_event_line_format(tmp_path):
    ev1 = _event("STAGE_BEGIN", stage="DRY", worklist=["b", "a"], forecast_s=540)
    hd.append_stage_event(tmp_path, dict(ev1))
    first = (tmp_path / "STAGES.jsonl").read_text(encoding="utf-8")
    hd.append_stage_event(tmp_path, _event("STOP", stage="DRY", status="FAIL_TECHNICAL/X",
                                           reason=Path("r")))
    text = (tmp_path / "STAGES.jsonl").read_text(encoding="utf-8")
    assert text.startswith(first) and text.endswith("\n")
    lines = text.splitlines()
    assert len(lines) == 2
    for line in lines:
        obj = json.loads(line)
        assert line == json.dumps(obj, sort_keys=True, default=str)
        assert "utc" in obj
    one = json.loads(lines[0])
    assert {k: one[k] for k in ev1} == ev1
    assert json.loads(lines[1])["reason"] == "r"


def test_save_hist_paths_key_and_exclusive_create(tmp_path):
    tok = np.arange(64, dtype=np.uint8).reshape(2, 32)
    key = "W12-q1-s1.25-p0.2"
    p = hd.save_hist(tmp_path, "S1", key, tok)
    assert Path(p) == tmp_path / "hist" / "S1" / f"{key}.npz"
    with np.load(p) as z:
        assert z.files == ["canon32"] and z["canon32"].dtype == np.uint8
        assert np.array_equal(z["canon32"], tok)
    before = Path(p).read_bytes()
    with pytest.raises((FileExistsError, hw.HwsStop)):
        hd.save_hist(tmp_path, "S1", key, tok[::-1].copy())
    assert Path(p).read_bytes() == before
    q = hd.save_hist(tmp_path, "NULLCHK", "W8-q1-s2.0-p0.5", tok, origin="S1")
    assert Path(q) == tmp_path / "hist" / "NULLCHK" / "S1" / "W8-q1-s2.0-p0.5.npz"


def test_reused_writers_refuse_existing_paths(tmp_path):
    stage_records.write_new(tmp_path / "a.json", {"x": 1})
    with pytest.raises(FileExistsError):
        stage_records.write_new(tmp_path / "a.json", {"x": 2})
    assert json.loads((tmp_path / "a.json").read_text(encoding="utf-8")) == {"x": 1}
    stage_records.save_npz(tmp_path / "h.npz", canon32=np.zeros((1, 32), np.uint8))
    with pytest.raises(FileExistsError):
        stage_records.save_npz(tmp_path / "h.npz", canon32=np.ones((1, 32), np.uint8))


def test_tree_sha_definition(tmp_path):
    _put(tmp_path / "stages/S0/a.json", b"{}")
    _put(tmp_path / "hist/S0/w.npz", b"\x00\x01")
    prefixes = ["stages/S0", "hist/S0", "hist/NULLCHK/S0"]
    h1 = hd.tree_sha(tmp_path, prefixes)
    # API-AMBIGUITY: relpath form unstated; read as POSIX paths relative to `out`
    files = {"hist/S0/w.npz": _sha_bytes(b"\x00\x01"), "stages/S0/a.json": _sha_bytes(b"{}")}
    assert h1 == _sha_bytes(canonical_json(files).encode("utf-8"))
    _put(tmp_path / "other/x.txt", b"outside the prefixes")
    assert hd.tree_sha(tmp_path, prefixes) == h1  # deterministic, prefix-limited
    _put(tmp_path / "hist/NULLCHK/S0/w.npz", b"n")
    h2 = hd.tree_sha(tmp_path, prefixes)
    _put(tmp_path / "stages/S0/a.json", b"{ }")
    assert len({h1, h2, hd.tree_sha(tmp_path, prefixes)}) == 3


def _partial_store(out: Path) -> dict:
    files = {"A_json": _put(out / "stages/S1/worlds/A.json", b'{"a": 1}'),
             "A_npz": _put(out / "hist/S1/A.npz", b"A"),
             "B_json": _put(out / "stages/S1/worlds/B.json", b'{"b": 2}'),
             "B_npz": _put(out / "hist/S1/B.npz", b"B"),
             "S0": _put(out / "stages/S0/worlds/C.json", b"c")}
    hd.append_stage_event(out, _event("STAGE_BEGIN", stage="S1", worklist=["A", "B"],
                                      forecast_s=16))
    listed = {"stages/S1/worlds/A.json": _sha_bytes(b'{"a": 1}'),
              "hist/S1/A.npz": _sha_bytes(b"A")}
    hd.append_stage_event(out, _event("WORLD_COMPLETE", stage="S1", key="A", files=listed,
                                      cpu_s=1.0))
    return files


def test_archive_partial_moves_only_unlisted_files(tmp_path):
    f = _partial_store(tmp_path)
    dest = hd.archive_partial(tmp_path, "S1")
    assert dest is not None and Path(dest).is_dir()
    assert Path(dest).resolve().parent == (tmp_path / "superseded").resolve()
    assert Path(dest).name.startswith("S1-")
    assert f["A_json"].exists() and f["A_npz"].exists() and f["S0"].exists()
    assert not f["B_json"].exists() and not f["B_npz"].exists()
    moved = {p.name: p.read_bytes() for p in Path(dest).rglob("*")
             if p.is_file() and p.name != "SHA256SUMS"}
    assert moved == {"B.json": b'{"b": 2}', "B.npz": b"B"}
    sums = (Path(dest) / "SHA256SUMS").read_text(encoding="utf-8")
    for data in (b'{"b": 2}', b"B"):
        assert _sha_bytes(data) in sums
    assert _sha_bytes(b"A") not in sums
    assert hd.archive_partial(tmp_path, "S1") is None  # nothing unlisted remains


def test_resume_regenerates_the_interrupted_world_bit_identically(tmp_path):
    proc = hw.build_tiny()
    first = ho.world_look(proc, "DRY", 48, (1, 2, 4), layout=TINY)
    (tmp_path / "hist" / "DRY").mkdir(parents=True)
    stage_records.save_npz(tmp_path / "hist" / "DRY" / "tiny.npz", canon32=first["tok"])
    hd.append_stage_event(tmp_path, _event("STAGE_BEGIN", stage="DRY", worklist=["tiny"],
                                           forecast_s=1))
    dest = hd.archive_partial(tmp_path, "DRY")  # interrupted: no WORLD_COMPLETE
    archived = [p for p in Path(dest).rglob("tiny.npz")]
    assert len(archived) == 1 and not (tmp_path / "hist/DRY/tiny.npz").exists()
    again = ho.world_look(proc, "DRY", 48, (1, 2, 4), layout=TINY)
    with np.load(archived[0]) as z:
        assert np.array_equal(z["canon32"], again["tok"])
    for name in ("D", "rn", "G"):
        for K in (1, 2, 4):
            assert np.array_equal(first["rows"][name][K], again["rows"][name][K])


def _git(*args) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                          check=True).stdout


def test_freeze_fields_and_implementation_hash(tmp_path):
    if _git("status", "--porcelain", "--", "tools/hws", "tests/hws").strip():
        pytest.skip("tools/hws or tests/hws differ from HEAD; FREEZE binds committed files")
    head = _git("rev-parse", "HEAD").strip()
    names = [n for n in _git("ls-tree", "-r", "--name-only", head, "--", "tools/hws",
                             "tests/hws").splitlines()
             if (n.startswith("tools/hws/") and n.endswith(".py")) or n.startswith("tests/hws/")]
    expected = {n: _sha_bytes(subprocess.run(["git", "-C", str(REPO), "show", f"{head}:{n}"],
                                             capture_output=True, check=True).stdout)
                for n in names}
    impl = _sha_bytes(canonical_json(expected).encode("utf-8"))
    dry = tmp_path / "DRY_RUN_REPORT.json"
    dry.write_text(json.dumps({"cases": {f"DR{i}": {"status": "PASS", "details": {}}
                                         for i in range(1, 14)},
                               "implementation_sha256": impl, "all_pass": True}),
                   encoding="utf-8")
    out = tmp_path / "store"
    out.mkdir()
    hd.freeze(out, REPO, head, dry)
    rec = json.loads((out / "FREEZE.json").read_text(encoding="utf-8"))
    assert set(CONTRACT["freeze_fields"]) <= set(rec)
    assert rec["protocol"] == "HWS-FROZEN-v1" and rec["h_exec"] == head
    assert rec["protocol_sha256"] == CONTRACT["protocol_sha256"]
    assert rec["implementation_files"] == expected
    assert "tests/hws/test_b_records.py" in rec["implementation_files"]
    assert rec["implementation_sha256"] == _sha_bytes(
        canonical_json(rec["implementation_files"]).encode("utf-8")) == impl
    assert rec["reuse_sha256"] == CONTRACT["reuse_sha256"]
    assert rec["dry_run_report_sha256"] == _sha_bytes(dry.read_bytes())
    for field, name in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                        ("test_plan_sha256", "TEST_PLAN.md")):
        assert rec[field] == _sha_bytes((REPO / "tools" / "hws" / name).read_bytes())
    with pytest.raises((FileExistsError, hw.HwsStop)):
        hd.freeze(out, REPO, head, dry)


def test_main_refuses_without_freeze_auth_or_accept(tmp_path, monkeypatch):
    calls = []

    def no_sample(self, n, rng):
        calls.append(n)
        raise AssertionError("sampling during a refused run")

    monkeypatch.setattr(HMMSampler, "sample", no_sample)
    out = tmp_path / "store"
    out.mkdir()
    auth = tmp_path / "auth.json"
    auth.write_text(json.dumps({"job_id": "0119", "stages": ["S0", "S1", "X1", "S2", "S3"],
                                "owner_auth_sha256": "0" * 64}), encoding="utf-8")
    acc = tmp_path / "accept.json"
    acc.write_text(json.dumps({"accept": True, "s0_record_sha256": "0" * 64}),
                   encoding="utf-8")
    for argv in (["s0", "--out", str(out)], ["s0", "--out", str(out), "--auth", str(auth)],
                 ["sweep", "--out", str(out), "--auth", str(auth)],
                 ["sweep", "--out", str(out), "--auth", str(auth), "--s0-accept", str(acc)]):
        assert _code(hd.main, argv) == 2, argv
    assert calls == []
    assert not (out / "hist").exists() and not (out / "FREEZE.json").exists()


# -------------------------------------------------------------------------------- meter

@pytest.fixture
def preserved(monkeypatch):
    for name in ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S",
                 "STOP_NEW_S", "OUTPUT_CAP", "WORKER_SESSION", "limit_reason", "main"):
        monkeypatch.setattr(meter, name, getattr(meter, name))
    for name in ("JOB_ID", "TASK_SHA256"):
        monkeypatch.setattr(controls, name, getattr(controls, name))
    monkeypatch.setattr(winjob, "MEMORY_CAP", winjob.MEMORY_CAP)
    monkeypatch.setattr(k4b_meter_bind, "TEMP_ROOT", k4b_meter_bind.TEMP_ROOT)
    monkeypatch.setattr(op_guard, "archive_stale", op_guard.archive_stale)
    for var in ("TEMP", "TMP", "TMPDIR") + tuple(meter.THREAD_VARS):
        if var in os.environ:
            monkeypatch.setenv(var, os.environ[var])
        else:
            monkeypatch.setenv(var, "unset")
            monkeypatch.delenv(var)
    monkeypatch.setattr(sys, "argv", list(sys.argv))
    return monkeypatch


def test_bind_sets_the_hws_values(tmp_path, preserved):
    hm.bind("0119", "ab" * 32, tmp_path, "sess-hws")
    assert winjob.MEMORY_CAP == 8 * GIB == CONTRACT["resources"]["memory_cap_bytes"]
    assert k4b_meter_bind.TEMP_ROOT == str(tmp_path)
    assert Path(meter.LEDGER) == tmp_path / "cpu_ledger.json"
    assert Path(meter.LOCK) == tmp_path / "RUN.lock"
    assert Path(meter.ACTIVE) == tmp_path / "METER_ACTIVE.lock"
    assert Path(meter.LOG_DIR) == tmp_path / "logs"
    assert meter.CAP_S == INF and meter.STOP_NEW_S == INF
    assert meter.OUTPUT_CAP == 4 * GIB == CONTRACT["resources"]["output_cap_bytes"]
    assert meter.WORKER_SESSION == "sess-hws" and controls.JOB_ID == "0119"
    env = k4b_meter_bind.child_env("0119", base={})
    assert env["TEMP"] == env["TMP"] == env["TMPDIR"] == f"{tmp_path}/tmp-0119"
    assert all(env[v] == "1" for v in meter.THREAD_VARS)
    eff = hm.effective_settings()
    assert eff["memory_cap"] == 8 * GIB and eff["temp_root"] == str(tmp_path)
    assert eff["ledger"] == str(tmp_path / "cpu_ledger.json") and eff["cap_s"] == INF
    assert eff["output_cap"] == 4 * GIB and eff["thread_vars"] == list(meter.THREAD_VARS)


def test_bind_to_the_dry_store_puts_child_temp_on_x(preserved):
    hm.bind("0119", "ab" * 32, hw.DRY_STORE, "sess-hws")  # sets module values only
    temp = Path(k4b_meter_bind.child_env("0119", base={})["TEMP"])
    assert temp == Path("X:/Downloads/topo-scratch/hws-dry") / "tmp-0119"
    assert temp.drive.upper() == "X:" and winjob.MEMORY_CAP == 8 * GIB


def _argv(out, *extra):
    return ["hws_meter_bind.py", "--job", "0119", "--task-sha256", "ab" * 32, "--session",
            "sess-hws", "--out", str(out), *extra]


def test_main_binds_and_hands_over_to_the_meter(tmp_path, preserved):
    seen, archived = {}, []

    def fake_main():
        seen.update(argv=list(sys.argv), temp=os.environ.get("TEMP"), cap=winjob.MEMORY_CAP,
                    threads={v: os.environ.get(v) for v in meter.THREAD_VARS},
                    temp_root=k4b_meter_bind.TEMP_ROOT, limiter=meter.limit_reason)
        return 0

    original_limiter = meter.limit_reason
    preserved.setattr(meter, "main", fake_main)
    preserved.setattr(op_guard, "archive_stale", lambda out: archived.append(Path(out)))
    preserved.setattr(sys, "argv", _argv(tmp_path, "--label", "dry", "--max-cpu", "600", "--",
                                         "python", "-c", "pass"))
    assert hm.main() == 0
    assert seen["argv"] == ["hws_meter_bind.py", "--label", "dry", "--max-cpu", "inf",
                            "--max-wall", "inf", "--", "python", "-c", "pass"]
    assert seen["cap"] == 8 * GIB and seen["temp_root"] == str(tmp_path)
    assert Path(seen["temp"]) == tmp_path / "tmp-0119"
    assert all(v == "1" for v in seen["threads"].values())
    assert seen["limiter"] is not original_limiter
    assert archived == [tmp_path]  # METER_ACTIVE.lock absent


def test_main_refuses_a_foreign_run_lock_and_missing_out(tmp_path, preserved):
    called = []
    preserved.setattr(meter, "main", lambda: called.append(1) or 0)
    preserved.setattr(op_guard, "archive_stale", lambda out: None)
    (tmp_path / "RUN.lock").write_text(json.dumps({"session": "someone-else"}),
                                       encoding="utf-8")
    preserved.setattr(sys, "argv", _argv(tmp_path, "--label", "d", "--", "python"))
    assert _code(hm.main) == 3 and called == []
    (tmp_path / "RUN.lock").write_text(json.dumps({"session": "sess-hws"}), encoding="utf-8")
    preserved.setattr(sys, "argv", _argv(tmp_path, "--label", "d", "--", "python"))
    assert _code(hm.main) == 0 and called == [1]
    preserved.setattr(sys, "argv", ["hws_meter_bind.py", "--job", "0119", "--task-sha256",
                                    "ab" * 32, "--session", "s", "--label", "d", "--", "py"])
    assert _code(hm.main) != 0 and called == [1]
