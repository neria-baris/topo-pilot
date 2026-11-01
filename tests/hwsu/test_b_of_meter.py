"""Author B (job 0198): meter binding, basetemps and the output cap (protocol §8.4, §10.3;
API §8; the hwsc_meter_bind pattern). TEST_PLAN §3 row test_b_of_bind_meter (meter part).
Every meter/winjob/k4b_meter_bind attribute that bind() sets is restored by monkeypatch."""

from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_meter_bind as um  # noqa: E402
import k4b_meter_bind  # noqa: E402
import meter  # noqa: E402
import winjob  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
GIB8 = 8 * 1024**3
SCRATCH = Path(C["resources"]["scratch_root"])
ROOT = Path(C["resources"]["project_root"])
STORE = Path(C["resources"]["store"])


def _guard_attrs(monkeypatch):
    for mod, names in ((meter, ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S",
                                "STOP_NEW_S", "OUTPUT_CAP", "WORKER_SESSION", "limit_reason")),
                       (winjob, ("MEMORY_CAP",)), (k4b_meter_bind, ("TEMP_ROOT",))):
        for n in names:
            if hasattr(mod, n):
                monkeypatch.setattr(mod, n, getattr(mod, n))
    import controls
    for n in ("JOB_ID", "TASK_SHA256"):
        if hasattr(controls, n):
            monkeypatch.setattr(controls, n, getattr(controls, n))


# ------------------------------------------------------------------ job paths (§8.4)
def test_job_paths_test():
    p = um.job_paths("0300", "test")
    assert Path(p["out"]) == SCRATCH / "test_hwsu-0300" == Path(p["temp_root"])
    assert Path(p["basetemp"]) == SCRATCH / "test_hwsu-0300" / "pytest" and p["kind"] == "test"


def test_job_paths_dry():
    p = um.job_paths("0300", "dry")
    assert Path(p["out"]) == SCRATCH / "hwsu-dry-of-0300"
    assert Path(p["temp_root"]) == SCRATCH / "test_hwsu-0300"
    assert Path(p["basetemp"]) == SCRATCH / "test_hwsu-0300" / "pytest" and p["kind"] == "dry"


def test_job_paths_store():
    p = um.job_paths("0300", "store")
    assert Path(p["out"]) == STORE and Path(p["temp_root"]) == STORE / "tmp"
    assert p["basetemp"] is None and p["kind"] == "store"
    assert Path(C["resources"]["store_temp_root"]) == STORE / "tmp"


@pytest.mark.parametrize("kind", ["meter", "", "Test", "e1"])
def test_job_paths_unknown(kind):
    with pytest.raises(ValueError):
        um.job_paths("0300", kind)


@pytest.mark.parametrize("kind", ["test", "dry", "store"])
def test_placement_ok_contract_paths(kind):
    r = um.placement_ok(um.job_paths("0300", kind))
    assert r["ok"] is True, r


@pytest.mark.parametrize("key,value", [
    ("basetemp", ROOT / "topo-pilot" / "pytest"),
    ("basetemp", ROOT / "hwsu-store" / "tmp" / "pytest"),
    ("temp_root", ROOT / "tmp"),
    ("temp_root", SCRATCH / "other-0300"),
    ("temp_root", SCRATCH / "x" / "test_hwsu-0300"),
    ("out", ROOT / "hwsu-dry-of-0300"),
])
def test_placement_rejects_bad_test_paths(key, value):
    p = dict(um.job_paths("0300", "test"), **{key: value})
    assert um.placement_ok(p)["ok"] is False


def test_placement_rejects_bad_store_paths():
    p = um.job_paths("0300", "store")
    assert um.placement_ok(dict(p, temp_root=SCRATCH / "test_hwsu-0300"))["ok"] is False
    assert um.placement_ok(dict(p, out=ROOT / "hwsc-store"))["ok"] is False


def test_placement_against_synthetic_root(tmp_path):
    root = tmp_path / "proj"
    p = {"kind": "test", "out": root / "x", "temp_root": root / "x", "basetemp": root / "x" / "p"}
    assert um.placement_ok(p, root=root)["ok"] is False


def test_this_suite_runs_outside_the_project_root(tmp_path):
    """§8.4 (the K4b registry trap): this run's basetemp and TEMP are outside the project root."""
    for p in (tmp_path, Path(os.environ.get("TEMP", tmp_path))):
        assert ROOT.resolve() not in Path(p).resolve().parents


# ------------------------------------------------------------------ memory cap (§10.3)
def test_memory_cap():
    for stage in ("J-OF", "DRO", "OF"):
        assert um.memory_cap(stage) == GIB8 == C["resources"]["memory_cap_bytes"][stage]
    for stage in ("E1", "KC", "of"):
        with pytest.raises(ValueError):
            um.memory_cap(stage)


# ------------------------------------------------------------------ bind (API §8)
def test_bind_sets_caps_from_contract(tmp_path, monkeypatch):
    _guard_attrs(monkeypatch)
    calls = []
    monkeypatch.setattr(k4b_meter_bind, "bind", lambda *a, **k: calls.append((a, k)))
    out = tmp_path / "out"
    um.bind("0300", "abc", out, "sess-1", "J-OF", temp_root=tmp_path / "t")
    assert len(calls) == 1
    a, k = calls[0]
    args = list(a) + [k.get(n) for n in ("job_id", "task_sha256", "out", "worker_session") if n in k]
    assert "0300" in args and "abc" in args and "sess-1" in args
    assert any(isinstance(x, (str, Path)) and Path(x) == out for x in args)
    assert winjob.MEMORY_CAP == GIB8
    assert Path(k4b_meter_bind.TEMP_ROOT) == tmp_path / "t"
    assert meter.CAP_S == float("inf") and meter.STOP_NEW_S == float("inf")
    assert meter.OUTPUT_CAP == C["resources"]["output_cap_bytes"] == 16 * 1024**3


def test_bind_temp_root_defaults_to_out(tmp_path, monkeypatch):
    _guard_attrs(monkeypatch)
    monkeypatch.setattr(k4b_meter_bind, "bind", lambda *a, **k: None)
    um.bind("0300", "abc", tmp_path / "out", "s", "DRO")
    assert Path(k4b_meter_bind.TEMP_ROOT) == tmp_path / "out"


def test_bind_output_cap_never_hard_coded(tmp_path, monkeypatch):
    _guard_attrs(monkeypatch)
    monkeypatch.setattr(k4b_meter_bind, "bind", lambda *a, **k: None)
    c = copy.deepcopy(uc.CONTRACT)
    c["resources"]["output_cap_bytes"] = 123456789
    c["resources"]["memory_cap_bytes"]["OF"] = 3 * 1024**3
    monkeypatch.setattr(uc, "CONTRACT", c)
    um.bind("0300", "abc", tmp_path / "out", "s", "OF")
    assert meter.OUTPUT_CAP == 123456789 and winjob.MEMORY_CAP == 3 * 1024**3


def test_bind_real_k4b_bind_then_overrides(tmp_path, monkeypatch):
    """With the unchanged k4b_meter_bind.bind (which sets 4 GiB / 12 GiB), the HWSU values win."""
    _guard_attrs(monkeypatch)
    out = tmp_path / "out"
    um.bind("0300", "abc", out, "sess-2", "OF", temp_root=tmp_path / "t")
    assert Path(meter.OUT) == out and Path(meter.LEDGER) == out / "cpu_ledger.json"
    assert meter.OUTPUT_CAP == C["resources"]["output_cap_bytes"] and winjob.MEMORY_CAP == GIB8
    eff = um.effective_settings()
    assert set(eff) >= {"memory_cap", "temp_root", "ledger", "cap_s", "output_cap", "thread_vars"}
    assert eff["memory_cap"] == GIB8 and eff["output_cap"] == C["resources"]["output_cap_bytes"]
    assert eff["cap_s"] == float("inf") and Path(eff["temp_root"]) == tmp_path / "t"


def test_child_env_u(tmp_path, monkeypatch):
    _guard_attrs(monkeypatch)
    monkeypatch.setattr(k4b_meter_bind, "TEMP_ROOT", str(tmp_path))
    env = um.child_env_u("0300")
    tmp = Path(f"{tmp_path}/tmp-0300")
    assert Path(env["TEMP"]) == Path(env["TMP"]) == Path(env["TMPDIR"]) == tmp
    assert tmp.is_dir()
    assert all(env[v] == "1" for v in meter.THREAD_VARS)


# ------------------------------------------------------------------ main (API §8)
@pytest.mark.parametrize("argv", [
    [],
    ["--job", "0300"],
    ["--job", "0300", "--task-sha256", "a", "--session", "s", "--kind", "test"],
    ["--job", "0300", "--task-sha256", "a", "--session", "s", "--stage", "OF"],
    ["--job", "0300", "--task-sha256", "a", "--session", "s", "--kind", "bogus", "--stage", "OF"],
    ["--job", "0300", "--task-sha256", "a", "--session", "s", "--kind", "test", "--stage", "E1"],
])
def test_main_refuses_missing_or_unknown_flags(monkeypatch, argv):
    _guard_attrs(monkeypatch)
    ran = []
    monkeypatch.setattr(meter, "main", lambda: ran.append(1) or 0)
    monkeypatch.setattr(k4b_meter_bind, "bind", lambda *a, **k: ran.append(2))
    monkeypatch.setattr(sys, "argv", ["hwsu_meter_bind.py"] + argv + ["--", "python", "-c", "0"])
    try:
        code = um.main()
    except SystemExit as exc:  # API-AMBIGUITY: argparse's exit(2) is accepted as "exit 2"
        code = exc.code
    assert code == 2 and ran == []
