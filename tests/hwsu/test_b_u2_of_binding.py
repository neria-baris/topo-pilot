"""Author B (job 0223, phase 2): R-0206-1 and the share outcome (API_U2 section 2.1;
TEST_PLAN_U2 row test_b_u2_of_binding). Fixture stores live under tmp_path; the real OF_ACCEPT.json
and FREEZE_OF.json are read (JSON/hash only) for the 'real' checks."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
from c1_records import C1GateFailure  # noqa: E402

AUTH = "INCONCLUSIVE/AUTHORITY"
SHARE = "INCONCLUSIVE/ORACLE_FEASIBILITY"
KEYS = ["schema", "verdict", "outcome", "N_resp", "freeze_of_sha256", "of_report_sha256", "h_exec"]


def _known():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_known")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _acc(**over) -> dict:
    d = {"schema": "hwsu-of-accept-v1", "verdict": "ACCEPT", "outcome": "OF_PASS_RESPONSE_ONLY",
         "N_resp": 4096, "freeze_of_sha256": None, "of_report_sha256": "ab" * 32,
         "h_exec": "49ac9c96420dd5a91ffbc1496ab1d00f584dd13e", "EG": {"point": "not-read"}}
    d.update(over)
    return d


def _fixture(tmp_path, acc_over=None, freeze_bytes=b'{"fixture": "freeze_of"}', bind_freeze=None):
    store = tmp_path / "hwsu-store"
    store.mkdir()
    (store / "FREEZE_OF.json").write_bytes(freeze_bytes)
    fz = _sha(freeze_bytes)
    acc = _acc(freeze_of_sha256=fz)
    acc.update(acc_over or {})
    raw = json.dumps(acc, sort_keys=True).encode("utf-8")
    (store / "OF_ACCEPT.json").write_bytes(raw)
    c = copy.deepcopy(uc.CONTRACT)
    a = c["authority_u2"]
    a["of_accept"]["sha256"] = _sha(raw)
    a["of_accept"]["freeze_of_sha256"] = bind_freeze or fz
    a["freeze_of"]["sha256"] = bind_freeze or fz
    return store, c, raw


def _fail(fn, *a, **k):
    with pytest.raises(C1GateFailure) as e:
        fn(*a, **k)
    return e.value.status


def test_pass_for_response_only_with_matching_freeze_of(tmp_path):
    store, c, raw = _fixture(tmp_path)
    r = _known().of_binding(store, contract=c)
    assert r["status"] == "PASS" and r["outcome"] == "OF_PASS_RESPONSE_ONLY"
    assert r["share_outcome"] == SHARE
    assert r["freeze_of_sha256"] == _sha(b'{"fixture": "freeze_of"}')
    assert r["of_accept_sha256"] == _sha(raw)


def test_freeze_of_sha_mismatch_in_accept_refused(tmp_path):
    """R-0206-1: OF_ACCEPT freeze_of_sha256 differs from the sha256 of FREEZE_OF.json."""
    store, c, _ = _fixture(tmp_path, acc_over={"freeze_of_sha256": "0" * 64})
    assert _fail(_known().of_binding, store, contract=c) == AUTH


def test_freeze_of_file_changed_refused(tmp_path):
    store, c, _ = _fixture(tmp_path)
    (store / "FREEZE_OF.json").write_bytes(b'{"fixture": "tampered"}')
    assert _fail(_known().of_binding, store, contract=c) == AUTH


def test_contract_freeze_of_copy_differs_refused(tmp_path):
    store, c, _ = _fixture(tmp_path, bind_freeze="1" * 64)
    assert _fail(_known().of_binding, store, contract=c) == AUTH


def test_of_accept_bytes_differ_from_contract_refused(tmp_path):
    store, c, raw = _fixture(tmp_path)
    (store / "OF_ACCEPT.json").write_bytes(raw + b"\n")
    assert _fail(_known().of_binding, store, contract=c) == AUTH


@pytest.mark.parametrize("over", [
    {"outcome": "OF_PASS"}, {"outcome": "OF_FAIL"}, {"outcome": "OF_PASS_SHARE_ONLY"},
    {"verdict": "REJECT"}, {"verdict": "accept"}, {"N_resp": 8192}])
def test_wrong_outcome_verdict_or_size_refused(tmp_path, over):
    store, c, _ = _fixture(tmp_path, acc_over=over)
    assert _fail(_known().of_binding, store, contract=c) == AUTH


def test_missing_key_or_missing_file_refused(tmp_path):
    store, c, _ = _fixture(tmp_path)
    (store / "FREEZE_OF.json").unlink()
    assert _fail(_known().of_binding, store, contract=c) == AUTH
    empty = tmp_path / "empty"
    empty.mkdir()
    assert _fail(_known().of_binding, empty, contract=c) == AUTH


def test_extra_keys_do_not_matter_and_share_outcome_is_fixed(tmp_path):
    """Only keys_read are used: an unlisted key (e.g. a planted EG value) changes nothing."""
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    s1, c1, _ = _fixture(tmp_path / "a", acc_over={"EG": {"point": "1.0"}})
    s2, c2, _ = _fixture(tmp_path / "b", acc_over={"EG": {"point": "999"}})
    r1, r2 = _known().of_binding(s1, contract=c1), _known().of_binding(s2, contract=c2)
    assert r1["share_outcome"] == r2["share_outcome"] == SHARE
    assert r1["outcome"] == r2["outcome"]


def test_keys_read_in_contract():
    assert uc.CONTRACT["authority_u2"]["of_accept"]["keys_read"] == KEYS


def test_real_of_accept_and_freeze_of_satisfy_the_rule():
    store = uc.STORE
    if not (store / "OF_ACCEPT.json").exists():
        pytest.skip("no real hwsu-store")
    a = uc.CONTRACT["authority_u2"]
    assert uc.sha256_file(store / "OF_ACCEPT.json") == a["of_accept"]["sha256"]
    assert uc.sha256_file(store / "FREEZE_OF.json") == a["freeze_of"]["sha256"]
    acc = uc.read_json(store / "OF_ACCEPT.json")
    assert acc["verdict"] == "ACCEPT" and acc["outcome"] == "OF_PASS_RESPONSE_ONLY"
    assert acc["freeze_of_sha256"] == a["freeze_of"]["sha256"] and acc["N_resp"] == 4096
    r = _known().of_binding(store)
    assert r["status"] == "PASS" and r["share_outcome"] == SHARE
