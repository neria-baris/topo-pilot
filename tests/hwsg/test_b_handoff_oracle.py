"""Author B: WORLD_HANDOFF and oracle identity/reproduction (protocol 2.6, O1, O3, O4)."""
from __future__ import annotations

import copy
import importlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import CONTRACT, TAGS, expect_fail, mod, sha_bytes  # noqa: E402

Z = Fraction(1046856722546615729545115383, 1250000000000000000000000000000000000000)


def _handoff(tag="hi", **over):
    gc = mod("gc")
    W = gc.world(tag)
    kc = importlib.import_module("k4b_cert")
    h = {"key": W.key, "sigma": str(W.sigma), "p": str(W.p), "neighbour": str((1 - W.p) / 4),
         "Z_bound": str(Z), "F_plan": str(kc.F_plan(Z)), "p_D2a": 1.5e-7, "N_C": 3072,
         "model_count": 3, "process_identities": {"ids": {"world": "w"}, "arrays_sha256": "x"},
         "exclusions": ["a", "b"], "protocol_sha256": gc.PROTOCOL_SHA}
    h.update(over)
    return h


def _put(tmp_path, h, tag="hi"):
    """Write bytes directly (bypasses write()) and return (store, sha)."""
    gc = mod("gc")
    wd = gc.world_dir(tmp_path, tag)
    wd.mkdir(parents=True)
    raw = json.dumps(h, sort_keys=True).encode()
    (wd / "WORLD_HANDOFF.json").write_bytes(raw)
    return tmp_path, sha_bytes(raw)


def test_contract_key_set_is_the_handoff_key_set():
    assert set(_handoff()) == set(CONTRACT["handoff"]["keys"])


@pytest.mark.parametrize("tag", TAGS)
def test_write_load_round_trip(tmp_path, tag):
    gc, gh = mod("gc"), mod("gh")
    h = _handoff(tag)
    wd = gc.world_dir(tmp_path, tag)
    wd.mkdir(parents=True)
    sha = gh.write(wd, h)
    assert sha == sha_bytes((wd / "WORLD_HANDOFF.json").read_bytes())
    got = gh.load(tag, store=tmp_path, expected_sha256=sha)
    W = gc.world(tag)
    assert got["key"] == W.key and got["neighbour"] == (1 - W.p) / 4
    assert got["Z_bound"] == Z and isinstance(got["Z_bound"], Fraction)
    assert got["N_C"] == 3072 and got["model_count"] == 3
    with pytest.raises(FileExistsError):  # exclusive create
        gh.write(wd, h)


def _bad_cases():
    h = _handoff()
    extra = dict(h, surplus=1)
    missing = {k: v for k, v in h.items() if k != "N_C"}
    deep = _handoff(process_identities={"x": {"y": {"outcome": "SUPPORT"}}})
    return {
        "extra_key": extra, "missing_key": missing, "forbidden_depth": deep,
        "wrong_world": _handoff(key="W12-q1-s1.25-p5/6"),
        "bad_neighbour": _handoff(neighbour=str((1 - Fraction(repr(5 / 6))) / 4)),
        "neighbour_not_quarter": _handoff(neighbour="1/7"),
        "bad_fplan": _handoff(F_plan="1/1000"),
    }


@pytest.mark.parametrize("name", list(_bad_cases()))
def test_defective_handoff_fails_identity(tmp_path, name):
    gh = mod("gh")
    store, sha = _put(tmp_path, _bad_cases()[name])
    expect_fail("FAIL_TECHNICAL/IDENTITY", gh.load, "hi", store=store, expected_sha256=sha)


def test_sha_mismatch_and_absent_binding_fail_identity(tmp_path):
    gh = mod("gh")
    store, sha = _put(tmp_path, _handoff())
    expect_fail("FAIL_TECHNICAL/IDENTITY", gh.load, "hi", store=store, expected_sha256="0" * 64)
    # no STAGES.jsonl O event and no explicit sha256: refused
    expect_fail("FAIL_TECHNICAL/IDENTITY", gh.load, "hi", store=store)


def test_default_sha_comes_from_o_stage_complete(tmp_path):
    gh = mod("gh")
    store, sha = _put(tmp_path, _handoff())
    rel = "worlds/" + mod("gc").world("hi").key + "/WORLD_HANDOFF.json"
    ev = {"stage": "O", "event": "STAGE_COMPLETE", "files": {rel: sha}}
    (store / "STAGES.jsonl").write_text(json.dumps(ev) + "\n", encoding="utf-8")
    assert gh.load("hi", store=store)["key"] == mod("gc").world("hi").key


def test_as_hwsc_view():
    gh = mod("gh")
    h = {"key": "k", "sigma": Fraction(5, 2), "p": Fraction(1, 2), "neighbour": Fraction(1, 8),
         "Z_bound": Z, "F_plan": Fraction(1, 2000), "p_D2a": 1.5e-7, "N_C": 3072,
         "model_count": 3, "process_identities": {}, "exclusions": ["a", "b"],
         "protocol_sha256": "x"}
    v = gh.as_hwsc(h)
    for k in ("Z_bound", "F_plan", "p_D2a", "N_C", "k_C", "model_count", "stage_c_exclusions",
              "registry_value"):
        assert k in v, k
    assert "outcome" not in v and "report_sha256" not in v
    assert v["k_C"] == 1 and tuple(v["stage_c_exclusions"]) == ("a", "b")
    assert v["registry_value"] == (10240 + 3072) * Fraction(1.5e-7)


@pytest.fixture(scope="module")
def lo_proc():
    go = mod("go")
    from topo_pilot.contracts import ArtifactStore, MemoryBackend
    store = ArtifactStore(MemoryBackend())
    return store, go.build_process_g(store, "lo")


def test_process_sigma_neighbour_are_exact(lo_proc):
    store, proc = lo_proc
    W = mod("gc").world("lo")
    assert proc["sigma"] == W.sigma
    assert proc["neighbour"] == (1 - W.p) / 4 == Fraction(1, 24)
    go = mod("go")
    assert go.identity(store, proc, "lo")["ok"] is True


def test_identity_fails_on_planted_id_difference(lo_proc):
    store, proc = lo_proc
    go = mod("go")
    bad = dict(proc)
    bad["neighbour"] = (1 - Fraction(repr(5 / 6))) / 4
    r = None
    try:
        r = go.identity(store, bad, "lo")
    except Exception as exc:  # noqa: BLE001  either a refusal or ok False
        assert "FAIL_TECHNICAL" in str(getattr(exc, "status", exc))
    assert r is None or r["ok"] is False


def test_identity_checker_compares_handoff_identities(lo_proc, monkeypatch):
    store, proc = lo_proc
    go, gh = mod("go"), mod("gh")
    chk = go.identity_checker("lo")
    assert callable(chk)
    ref = go.identity(store, proc, "lo")
    good = {"ids": ref["ids"], "arrays_sha256": ref["arrays_sha256"]}
    # API-AMBIGUITY: the checker reads WORLD_HANDOFF through gh.load (stubbed here)
    stub = dict(_handoff("lo"), process_identities=good)
    monkeypatch.setattr(gh, "load", lambda *a, **k: stub)
    r_ok = chk(store, proc)
    bad = copy.deepcopy(stub)
    bad["process_identities"]["arrays_sha256"] = "0" * 64
    monkeypatch.setattr(gh, "load", lambda *a, **k: bad)
    try:
        r_bad = chk(store, proc)
    except Exception as exc:  # noqa: BLE001
        r_bad = {"ok": False, "exc": exc}
    assert r_ok["ok"] is True and r_bad["ok"] is False


def test_reproduce_wrong_table_fails_oracle(tmp_path):
    """A synthetic stored table that is not the stage-A table cannot pass O4 (OPEN-2).
    API-AMBIGUITY: the PASS path needs a synthetic stage-A record bound by sha256; only the
    fail-closed side is black-box testable."""
    go = mod("go")
    p = tmp_path / "DRYHIST_synthetic.npz"
    rng = np.random.default_rng(5)
    np.savez(p, canon32=rng.integers(0, 36, (16, 32), dtype=np.uint8))
    with pytest.raises(Exception):  # noqa: B017  any refusal; PASS is impossible here
        go.reproduce(object(), "lo", hist_path=p)
