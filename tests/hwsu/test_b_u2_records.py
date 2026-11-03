"""Author B (job 0223, phase 2): sealing, records, obligations, reservations, meter binding and
basetemps (API_U2 4.7, 4.9, 5, 9; R-0213-2; TEST_PLAN_U2 row test_b_u2_records). Everything under
tmp_path; meter attributes are restored by monkeypatch and the meter itself is never started."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_records as ur  # noqa: E402
from c1_means import tree_mean  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

PROTO = "9efbabdfae58b2ac893bbfbc66aa0cb25e419e10aff9fbf34f45123314af88eb"
GIB = 1024**3
SCRATCH = Path(uc.CONTRACT["resources"]["scratch_root"])
ROOT = Path(uc.CONTRACT["resources"]["project_root"])


def _gates():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_gates")


def _drv():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_driver")


def _dry2():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_dry2")


def _fail(fn, *a, **k):
    with pytest.raises(C1GateFailure) as e:
        fn(*a, **k)
    return e.value.status


# ------------------------------------------------------------------ sealing
def _arrays():
    rng = np.random.default_rng(2)
    G = rng.random(64) + 1.0
    d = {"G": G}
    for j in (620301, 620302):
        A = 0.2 * G + 0.01 * rng.standard_normal(64)
        d[f"A_{j}"] = A
        d[f"ZR010_{j}"] = A - 0.1 * G
        d[f"ZR030_{j}"] = A - 0.3 * G
    return d


def test_write_sealed_u_exclusive_once_with_protocol_sha_and_means_only(tmp_path):
    g = _gates()
    arr = _arrays()
    sha = g.write_sealed_u(tmp_path, arr)
    p = tmp_path / "SEALED_VALIDATION.json"
    raw = p.read_bytes()
    import hashlib

    assert sha == hashlib.sha256(raw).hexdigest()
    body = json.loads(raw)
    assert body["protocol_sha256"] == PROTO
    means = body["means"]
    assert set(means) >= {"A_620301", "ZR010_620301", "ZR030_620301", "theta_620301"}
    assert means["A_620301"] == repr(float(tree_mean(arr["A_620301"])))
    assert means["ZR030_620302"] == repr(float(tree_mean(arr["ZR030_620302"])))
    th = float(means["theta_620301"])
    assert th == pytest.approx(float(tree_mean(arr["A_620301"])) / float(tree_mean(arr["G"])), rel=1e-12)  # noqa: E501
    assert all(isinstance(v, str) for v in means.values())  # means only, no row values
    assert raw.endswith(b"\n") and raw == (json.dumps(body, sort_keys=True) + "\n").encode("utf-8")


def test_write_sealed_u_second_call_never_overwrites(tmp_path):
    g = _gates()
    arr = _arrays()
    g.write_sealed_u(tmp_path, arr)
    before = (tmp_path / "SEALED_VALIDATION.json").read_bytes()
    with pytest.raises(Exception):  # noqa: B017  exclusive create
        g.write_sealed_u(tmp_path, {k: v + 1 for k, v in arr.items()})
    assert (tmp_path / "SEALED_VALIDATION.json").read_bytes() == before


SEALED = ["A_full", "AF", "ZR010", "ZR030", "theta", "theta_hat", "mean_A", "mean_ZR010",
          "mean_ZR030", "sign_agreement", "row_cross_check", "family_bounds", "per_model_status"]


def test_sealed_keys_u_constant():
    assert set(_gates().SEALED_KEYS_U) == set(SEALED)


@pytest.mark.parametrize("key", SEALED)
def test_check_unsealed_u_refuses_each_key_at_any_depth(key):
    g = _gates()
    assert g.check_unsealed_u({"ok": 1, "nested": [{"deep": {"x": 1}}]}) is None
    for rep in ({key: 1}, {"a": {key: 1}}, {"a": [{"b": {"c": {key: [1]}}}]}):
        assert _fail(g.check_unsealed_u, rep) == "FAIL_TECHNICAL/SEALING"


# ------------------------------------------------------------------ share-dropped entry points
def test_share_dropped_returns_not_run_and_computes_nothing():
    r = _gates().share_dropped({})
    assert r["status"] == "NOT_RUN/SHARE_DROPPED" and "OF_PASS_RESPONSE_ONLY" in r["reason"]


def test_share_family_and_share_only_names_fail_closed():
    g = _gates()
    assert _fail(g.share_family) == "FAIL_TECHNICAL/BINDING"
    assert _fail(g.share_family, 1, 2, k=3) == "FAIL_TECHNICAL/BINDING"
    for mod, name in (("hwsu_gates", "share_arrays_u"), ("hwsu_gates", "haar_frames_u")):
        assert _fail(getattr(importlib.import_module(mod), name)) == "FAIL_TECHNICAL/BINDING"
    importlib.import_module("u2")
    uk = importlib.import_module("hwsu_known")
    assert _fail(uk.ku_cases) == "FAIL_TECHNICAL/BINDING"


def test_run_gates_u_continues_through_share_dropped(tmp_path):
    cont = uc.CONTRACT["gates_u2"]["continuing_statuses"]
    assert "NOT_RUN/SHARE_DROPPED" in cont and "PASS" in cont
    ran = []
    steps = [("SUP", lambda: {"status": "NOT_RUN/SHARE_DROPPED"}),
             ("M0", lambda: ran.append(1) or {}),
             ("BAD", lambda: {"status": "FAIL_TECHNICAL/MODEL"}),
             ("X1", lambda: ran.append(2) or {})]
    recs = ur.run_gates_u(tmp_path, steps, continuing=cont)
    st = {r["gate"]: r["status"] for r in recs}
    assert st["SUP"] == "NOT_RUN/SHARE_DROPPED" and st["M0"] == "PASS"
    assert st["BAD"] == "FAIL_TECHNICAL/MODEL" and st["X1"] == "NOT_RUN" and ran == [1]


# ------------------------------------------------------------------ arrays, obligations, reservations  # noqa: E501
def test_phase2_arrays_use_phase1_prefixes_and_obligation_lists_them(tmp_path):
    for rel in ("stages/E1/PAIR_E1_val.npz", "stages/E1/ORACLE_E1_val.npz", "stages/E1/PREC_E1.npz",
                "stages/E1/BOOT_E1.npz", "stages/E1/HIST_fit_s_b0.npz"):
        ur.save_array(tmp_path, rel, A=np.arange(3.0))
    for bad in ("ACTS_x.npz", "Y_x.npz", "DECODER_x.npz", "SCORES_x.npz", "ENDPOINT_x.npz"):
        assert _fail(ur.save_array, tmp_path, f"stages/E1/{bad}", A=np.arange(3.0)) == "FAIL_TECHNICAL/LINEAGE"  # noqa: E501
        assert not (tmp_path / "stages" / "E1" / bad).exists()
    p = ur.write_obligation(tmp_path, "REGISTRY_OBLIGATION_E1-a1.json", "E1", "fixture")
    rec = json.loads(p.read_text(encoding="utf-8"))
    by = {f["relpath"]: f for f in rec["files"]}
    assert set(by) == {"stages/E1/PAIR_E1_val.npz", "stages/E1/ORACLE_E1_val.npz",
                       "stages/E1/PREC_E1.npz", "stages/E1/BOOT_E1.npz", "stages/E1/HIST_fit_s_b0.npz"}  # noqa: E501
    assert by["stages/E1/PAIR_E1_val.npz"]["class"] == "NON_HISTORY"
    assert by["stages/E1/HIST_fit_s_b0.npz"]["class"] == "K4b history table"
    assert ur.obligation_name("E1", 1) == "REGISTRY_OBLIGATION_E1-a1.json"
    assert ur.obligation_name("KC", 1) == "REGISTRY_OBLIGATION_KC-a1.json"
    assert ur.obligation_name("E2", 2) == "REGISTRY_OBLIGATION_E2-a2.json"


def test_drawing_job_stopped_before_first_row_ends_reservation_and_reruns_on_a2(tmp_path):
    store = tmp_path / "hwsu-store"
    store.mkdir()
    rf = ur.write_reservation(store, "RES-HWSU-U", "hwsu-v1", ur.utc(), "fixture")
    assert rf.name == "RESERVATION_U.json"
    obl = ur.write_obligation(store, ur.obligation_name("E1", 1), "E1", "fixture")
    assert json.loads(obl.read_text(encoding="utf-8"))["files"] == []
    end = ur.end_reservation(store, "RES-HWSU-U", ur.utc(), obl)
    assert end == store / "reservations" / "RES-HWSU-U.END.json"
    e = json.loads(end.read_text(encoding="utf-8"))
    assert e["schema"] == "hws-reservation-end-v1" and e["obligation_file"].endswith(obl.name)
    assert ur.reservation_file("RES-HWSU-U-a2") == "RESERVATION_U-a2.json"
    ur.write_reservation(store, "RES-HWSU-U-a2", "hwsu-v1", ur.utc(), "fixture")
    assert (store / "RESERVATION_U-a2.json").exists()
    assert _fail(ur.end_reservation, store, "RES-HWSU-U", ur.utc(), obl) == "FAIL_TECHNICAL/LINEAGE"
    with pytest.raises(ValueError):
        ur.reservation_file("RES-HWSU-U-a1")


# ------------------------------------------------------------------ memory caps and paths
@pytest.mark.parametrize("stage,cap", [("KC", 12), ("E1", 12), ("REG2", 12), ("E2", 12),
                                       ("J-U", 8), ("DRU", 8)])
def test_memory_cap_u2(stage, cap):
    assert _drv().memory_cap_u2(stage) == cap * GIB


def test_memory_cap_u2_unknown_stage_and_phase1_cap_still_refuses():
    with pytest.raises(ValueError):
        _drv().memory_cap_u2("OF")
    with pytest.raises(ValueError):
        _drv().memory_cap_u2("nonsense")
    mb = importlib.import_module("hwsu_meter_bind")
    with pytest.raises(ValueError):
        mb.memory_cap("E1")


def test_job_paths_u2_dru_test_store():
    d = _drv()
    p = d.job_paths_u2("0300", "dru")
    assert Path(p["out"]) == SCRATCH / "hwsu-dry-u2-0300"
    assert Path(p["temp_root"]) == SCRATCH / "test_hwsu-0300"
    assert Path(p["basetemp"]) == SCRATCH / "test_hwsu-0300" / "pytest"
    mb = importlib.import_module("hwsu_meter_bind")
    for kind in ("test", "store"):
        assert d.job_paths_u2("0300", kind) == mb.job_paths("0300", kind)
    with pytest.raises(ValueError):
        d.job_paths_u2("0300", "bogus")


def test_dru_paths_lie_outside_the_project_root():
    p = _drv().job_paths_u2("0223", "dru")
    for k in ("out", "temp_root", "basetemp"):
        q = Path(p[k]).resolve()
        assert ROOT.resolve() not in (q, *q.parents), k
    assert Path(p["temp_root"]).parent == SCRATCH and Path(p["temp_root"]).name.startswith("test_hwsu-")  # noqa: E501


# ------------------------------------------------------------------ meter_main
def _guard_attrs(monkeypatch):
    import controls
    import k4b_meter_bind
    import meter
    import winjob

    for mod, names in ((meter, ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S",
                                "STOP_NEW_S", "OUTPUT_CAP", "WORKER_SESSION", "limit_reason")),
                       (winjob, ("MEMORY_CAP",)), (k4b_meter_bind, ("TEMP_ROOT",)),
                       (controls, ("JOB_ID", "TASK_SHA256"))):
        for n in names:
            if hasattr(mod, n):
                monkeypatch.setattr(mod, n, getattr(mod, n))
    return meter, winjob, k4b_meter_bind


@pytest.mark.parametrize("stage,cap", [("DRU", 8), ("J-U", 8)])
def test_meter_main_sets_u2_memory_cap_and_measure_only_argv(stage, cap, monkeypatch, tmp_path):
    meter, winjob, k4bm = _guard_attrs(monkeypatch)
    import op_guard

    seen = {}
    monkeypatch.setattr(meter, "main", lambda: seen.update(cap=winjob.MEMORY_CAP, argv=list(sys.argv)) or 0)  # noqa: E501
    monkeypatch.setattr(op_guard, "archive_stale", lambda *a, **k: None)
    monkeypatch.setattr(k4bm, "make_limiter", lambda **k: (lambda *a, **kw: None))
    monkeypatch.setenv("TEMP", str(tmp_path))
    kind = "dru" if stage == "DRU" else "test"
    monkeypatch.setattr(sys, "argv", ["hwsu_driver.py", "--job", "0223tb", "--task-sha256", "abc",
                                      "--session", "sess-b", "--kind", kind, "--stage", stage,
                                      "--", "python", "-c", "0"])
    code = _drv().meter_main()
    assert code == 0 and seen["cap"] == cap * GIB
    a = seen["argv"]
    assert "--max-cpu" in a and a[a.index("--max-cpu") + 1] == "inf"
    assert "--max-wall" in a and a[a.index("--max-wall") + 1] == "inf"


@pytest.mark.parametrize("argv", [
    ["--job", "0223tb", "--task-sha256", "a", "--session", "s", "--kind", "bogus", "--stage", "E1"],
    ["--job", "0223tb", "--task-sha256", "a", "--session", "s", "--kind", "store", "--stage", "ZZ"],
    ["--job", "0223tb"]])
def test_meter_main_refuses_unknown_kind_stage_or_missing_flags(monkeypatch, argv):
    meter, _, k4bm = _guard_attrs(monkeypatch)
    ran = []
    monkeypatch.setattr(meter, "main", lambda: ran.append(1) or 0)
    monkeypatch.setattr(sys, "argv", ["hwsu_driver.py"] + argv + ["--", "python", "-c", "0"])
    try:
        code = _drv().meter_main()
    except SystemExit as exc:  # argparse exit(2) accepted as exit 2
        code = exc.code
    assert code == 2 and ran == []


def test_no_pause_line_in_u2_contract_jobs():
    """Addenda 41-43: no pause check; the phase-2 job table names no PAUSE gate."""
    jobs = uc.CONTRACT["gates_u2"]["jobs"]
    assert "pause" not in json.dumps(jobs).lower()


# ------------------------------------------------------------------ run_dru placement (R-0213-2)
def test_run_dru_refuses_out_under_the_project_root(tmp_path):
    out = ROOT / "hwsu-dry-u2-refusal-probe"
    assert not out.exists()
    r = _dry2().run_dru(out)
    assert r["status"] == "REFUSED"
    assert not out.exists()


def test_run_dru_refuses_out_not_named_like_a_dry_store(tmp_path):
    r = _dry2().run_dru(tmp_path / "somewhere")
    assert r["status"] == "REFUSED" and not (tmp_path / "somewhere").exists()
