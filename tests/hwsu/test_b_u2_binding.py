"""Author B (job 0223, phase 2): stage-C binding and identity (protocol 3.1; API_U2 1.1; DRU8).
Synthetic hwsc-store fixtures under tmp_path; chart 'files' are random bytes (never np.load-ed).
The 'real' checks read JSON/hash only (no payload, no blinded path)."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
from c1_records import C1GateFailure  # noqa: E402

IDENT = "FAIL_TECHNICAL/IDENTITY"
MASTERS = (620301, 620302, 620303)


def _m():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_model")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _get(d, j):
    return d[j] if j in d else d[str(j)]


def _set(d, j, v):
    d[j if j in d else str(j)] = v


def _fail(fn, *a, **k):
    with pytest.raises(C1GateFailure) as e:
        fn(*a, **k)
    return e.value.status


def _record(j, **over):
    rec = {"checkpoint_ids": {"5000": f"ck{j}"}, "checksums": {"5000": "y"}, "run_key": "RK",
           "status": "COMPLETE", "dev_ce": 1.2345, "extra_secret": [1, 2]}
    rec.update(over)
    return rec


def _stage_store(tmp_path, rec_over=None, stage_sha_over=None):
    """hwsc-store fixture with three TRAIN_RECORDs, STAGES.jsonl and a CONTRACT copy."""
    store = tmp_path / "hwsc-store"
    c = copy.deepcopy(uc.CONTRACT)
    sc = c["stage_c_u2"]
    lines = []
    for j in MASTERS:
        rel = _get(sc["train_records"], j)["relpath"]
        p = store / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        raw = json.dumps(_record(j, **(rec_over or {}))).encode("utf-8")
        p.write_bytes(raw)
        _get(sc["train_records"], j)["sha256"] = _sha(raw)
        _set(sc["checkpoint_ids"], j, f"ck{j}")
        sha = (stage_sha_over or {}).get(j, _sha(raw))
        lines.append({"stage": f"TRAIN_{j}", "event": "STAGE_COMPLETE", "files": {rel: sha}})
    (store / "STAGES.jsonl").write_text("\n".join(json.dumps(x) for x in lines) + "\n",
                                        encoding="utf-8")
    return store, c


def _charts(tmp_path, bad_gauge=False):
    store = tmp_path / "hwsc-store"
    c = copy.deepcopy(uc.CONTRACT)
    pf = c["stage_c_u2"]["production_frozen"]
    d = store / "stages" / "S4a"
    d.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(5)
    files = {}
    for name in sorted(pf["charts"]):
        b = rng.bytes(64)
        (d / name).write_bytes(b)
        files[name] = _sha(b)
        pf["charts"][name] = files[name]
    gauges = {k: list(v) for k, v in pf["gauges"].items()}
    rec = {"files": files, "gauges": gauges}
    if bad_gauge:
        k = sorted(gauges)[0]
        rec["gauges"][k] = [x + 1e-9 if isinstance(x, float) else x for x in gauges[k]]
    raw = json.dumps(rec).encode("utf-8")
    (d / "PRODUCTION_FROZEN.json").write_bytes(raw)
    pf["sha256"] = _sha(raw)
    return store, c, d


# ------------------------------------------------------------------ read_train_record
def test_read_train_record_drops_dev_ce_and_everything_else(tmp_path):
    store, c = _stage_store(tmp_path)
    rel = _get(c["stage_c_u2"]["train_records"], 620301)["relpath"]
    out = _m().read_train_record(store / rel)
    assert set(out) == set(_m().TRAIN_KEYS) == {"checkpoint_ids", "checksums", "run_key", "status"}
    assert "dev_ce" not in out and "extra_secret" not in out
    assert out["checkpoint_ids"] == {"5000": "ck620301"}


def test_read_train_record_dev_ce_dropped_whatever_its_shape(tmp_path):
    """A dev_ce value of any shape (here nested) is dropped; a UTF-8 BOM is accepted."""
    raw = json.dumps(_record(1, dev_ce={"a": [1, 2]})).encode("utf-8")
    p = tmp_path / "rec.json"
    p.write_bytes(b"\xef\xbb\xbf" + raw)
    out = _m().read_train_record(p)
    assert "dev_ce" not in out and out["status"] == "COMPLETE"


@pytest.mark.parametrize("drop", ["checkpoint_ids", "checksums", "run_key", "status"])
def test_read_train_record_missing_whitelisted_key_refused(tmp_path, drop):
    rec = _record(1)
    rec.pop(drop)
    p = tmp_path / "rec.json"
    p.write_text(json.dumps(rec), encoding="utf-8")
    assert _fail(_m().read_train_record, p) == IDENT


# ------------------------------------------------------------------ stage_complete_sha
def test_stage_complete_sha_last_record_wins(tmp_path):
    (tmp_path / "STAGES.jsonl").write_text("\n".join(json.dumps(x) for x in [
        {"stage": "S", "event": "BEGIN"},
        {"stage": "S", "event": "STAGE_COMPLETE", "files": {"a": "1"}},
        {"stage": "S", "event": "STAGE_COMPLETE", "files": {"a": "2"}},
        {"stage": "T", "event": "STAGE_COMPLETE", "files": {"a": "9"}}]) + "\n", encoding="utf-8")
    m = _m()
    assert m.stage_complete_sha(tmp_path, "S", "a") == "2"
    assert m.stage_complete_sha(tmp_path, "S", "zz") is None
    assert m.stage_complete_sha(tmp_path, "NOPE", "a") is None


# ------------------------------------------------------------------ identity_c refusals
HANDOFF = {"p_D2a": 0.0, "stage_c_exclusions": ()}


def test_identity_c_train_record_differs_from_contract(tmp_path):
    store, c = _stage_store(tmp_path)
    _get(c["stage_c_u2"]["train_records"], 620301)["sha256"] = "0" * 64
    assert _fail(_m().identity_c, store, HANDOFF, contract=c) == IDENT


def test_identity_c_train_record_differs_from_stage_complete(tmp_path):
    store, c = _stage_store(tmp_path, stage_sha_over={620301: "f" * 64})
    assert _fail(_m().identity_c, store, HANDOFF, contract=c) == IDENT


def test_identity_c_status_not_complete_refused(tmp_path):
    store, c = _stage_store(tmp_path, rec_over={"status": "RUNNING"})
    assert _fail(_m().identity_c, store, HANDOFF, contract=c) == IDENT


def test_identity_c_checkpoint_id_differs_from_contract(tmp_path):
    store, c = _stage_store(tmp_path)
    _set(c["stage_c_u2"]["checkpoint_ids"], 620301, "other-id")
    assert _fail(_m().identity_c, store, HANDOFF, contract=c) == IDENT


def test_identity_c_excluded_checkpoint_id_refused(tmp_path):
    # AMBIGUITY: on a synthetic store the meta step also fails; the status is IDENTITY either way.
    store, c = _stage_store(tmp_path)
    handoff = {"p_D2a": 0.0, "stage_c_exclusions": ("ck620302",)}
    assert _fail(_m().identity_c, store, handoff, contract=c) == IDENT


# ------------------------------------------------------------------ charts_identity
def test_charts_identity_pass_without_np_load(tmp_path, monkeypatch):
    store, c, _ = _charts(tmp_path)

    def boom(*a, **k):
        raise AssertionError("np.load called on a chart")

    monkeypatch.setattr(np, "load", boom)
    r = _m().charts_identity(store, contract=c)
    assert r is None or r.get("status", "PASS") == "PASS"


def test_chart_off_by_one_byte_refused(tmp_path):
    store, c, d = _charts(tmp_path)
    name = sorted(c["stage_c_u2"]["production_frozen"]["charts"])[0]
    b = bytearray((d / name).read_bytes())
    b[-1] ^= 1
    (d / name).write_bytes(bytes(b))
    assert _fail(_m().charts_identity, store, contract=c) == IDENT


def test_gauges_differ_from_contract_refused(tmp_path):
    store, c, _ = _charts(tmp_path, bad_gauge=True)
    assert _fail(_m().charts_identity, store, contract=c) == IDENT


def test_production_frozen_rehash_mismatch_refused(tmp_path):
    store, c, d = _charts(tmp_path)
    p = d / "PRODUCTION_FROZEN.json"
    p.write_bytes(p.read_bytes() + b" ")
    assert _fail(_m().charts_identity, store, contract=c) == IDENT


def test_chart_record_hash_differs_from_contract_copy(tmp_path):
    store, c, _ = _charts(tmp_path)
    name = sorted(c["stage_c_u2"]["production_frozen"]["charts"])[0]
    c["stage_c_u2"]["production_frozen"]["charts"][name] = "0" * 64
    assert _fail(_m().charts_identity, store, contract=c) == IDENT


# ------------------------------------------------------------------ load_stage_c threads
def test_load_stage_c_requires_one_torch_thread(tmp_path, monkeypatch):
    torch = pytest.importorskip("torch")
    monkeypatch.setattr(torch, "set_num_threads", lambda n: None)
    monkeypatch.setattr(torch, "get_num_threads", lambda: 4)
    ident = {"ids": {j: f"ck{j}" for j in MASTERS}}
    assert _fail(_m().load_stage_c, tmp_path, ident) == IDENT


# ------------------------------------------------------------------ real (read-only JSON/hash)
def test_real_stage_c_hashes_equal_contract():
    sc = uc.CONTRACT["stage_c_u2"]
    store = Path(sc["store"])
    if not store.is_dir():
        pytest.skip("no real hwsc-store")
    assert uc.sha256_file(store / "FREEZE.json") == sc["freeze_sha256"]
    assert uc.sha256_file(store / sc["stages_jsonl"]["relpath"]) == \
        sc["stages_jsonl"]["sha256_2026_11_03"]
    assert uc.sha256_file(store / sc["production_frozen"]["relpath"]) == \
        sc["production_frozen"]["sha256"]
    for j in MASTERS:
        e = _get(sc["train_records"], j)
        assert uc.sha256_file(store / e["relpath"]) == e["sha256"]
    o = sc["obs_inventory"]
    assert uc.sha256_file(store / o["relpath"]) == o["sha256"]
    assert uc.sha256_file(store / sc["k_reg2"]["manifest"]) == sc["k_reg2"]["manifest_sha256"]
    m = _m()
    for j in MASTERS:
        rec = m.read_train_record(store / _get(sc["train_records"], j)["relpath"])
        assert set(rec) == set(m.TRAIN_KEYS) and rec["status"] == "COMPLETE"
        assert rec["checkpoint_ids"]["5000"] == _get(sc["checkpoint_ids"], j)
