"""Author B (job 0198): reservation files, the J8 end record and the W2 attestation
(protocol §8.2 item 3; joint rulings J2, J8, J10 item 3; S-3). TEST_PLAN §3 row
test_b_of_reservations; DRO7, DRO9. Synthetic roots under tmp_path only."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_records as ur  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
END_FIELDS = {"schema", "reservation_id", "reservation_file", "reservation_sha256", "end_utc",
              "obligation_file", "obligation_sha256", "written_by"}
UTC = "2026-11-01T12:00:00Z"


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _json(p, obj) -> Path:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(obj, indent=1).encode("utf-8"))
    return p


def _active(store, rid, name=None, **extra) -> Path:
    rec = {"id": rid, "scope": "x", "state": "ACTIVE", "start_utc": UTC, "end_utc": None,
           "interruptions": [], "job_states": {}, "written_by": "fixture"}
    rec.update(extra)
    return _json(Path(store) / (name or f"RESERVATION_{rid}.json"), rec)


def _end_fixture(store, rid, res_file, obl_file, root, schema="hws-reservation-end-v1"):
    """An end record written by hand in the J8 form (as track D's hwsd_data.end_reservation)."""
    rel = lambda p: Path(p).relative_to(root).as_posix()  # noqa: E731
    return _json(Path(store) / "reservations" / f"{rid}.END.json", {
        "schema": schema, "reservation_id": rid, "reservation_file": rel(res_file),
        "reservation_sha256": _sha(res_file), "end_utc": UTC, "obligation_file": rel(obl_file),
        "obligation_sha256": _sha(obl_file), "written_by": "hwsd_data.end_reservation (fixture)"})


def _fails(status, fn, *a, **k):
    with pytest.raises(C1GateFailure) as ei:
        fn(*a, **k)
    assert ei.value.status == status, ei.value.status


# ------------------------------------------------------------------ names (S-3)
@pytest.mark.parametrize("rid,name", [("RES-HWSU-OF", "RESERVATION_OF.json"),
                                      ("RES-HWSU-OF-a2", "RESERVATION_OF-a2.json"),
                                      ("RES-HWSU-OF-a11", "RESERVATION_OF-a11.json"),
                                      ("RES-HWSU-U", "RESERVATION_U.json"),
                                      ("RES-HWSU-U-a3", "RESERVATION_U-a3.json")])
def test_reservation_file_mapping(rid, name):
    assert ur.reservation_file(rid) == name


@pytest.mark.parametrize("rid", ["RES-HWSD-W2", "RES-HWSC-W2", "RES-HWSU-OF-a1", "RES-HWSU-OF-a0",
                                 "RES-HWSU-OF-ax", "RES-HWSU-E1", "RES-HWSU-OF-a2x", ""])
def test_reservation_file_refuses_other_ids(rid):
    with pytest.raises(ValueError):
        ur.reservation_file(rid)


def test_contract_reservation_names():
    r = C["reservations"]
    assert ur.reservation_file(r["OF"]["id"]) == r["OF"]["file"]
    assert ur.reservation_file(r["model"]["id"]) == r["model"]["file"]
    assert C["reservation_end"]["schema"] == "hws-reservation-end-v1"
    assert set(C["reservation_end"]["fields"]) == END_FIELDS


# ------------------------------------------------------------------ write_reservation (D-15)
def test_write_reservation_k4b_form_exclusive(tmp_path):
    store = tmp_path / "root" / "hwsu-store"
    store.mkdir(parents=True)
    p = Path(ur.write_reservation(store, "RES-HWSU-OF", "hwsu-of-v1", UTC, "coordinator"))
    assert p == store / "RESERVATION_OF.json"
    rec = json.loads(p.read_text(encoding="utf-8"))
    assert rec == {"id": "RES-HWSU-OF", "scope": "hwsu-of-v1", "state": "ACTIVE",
                   "start_utc": UTC, "end_utc": None, "interruptions": [], "job_states": {},
                   "written_by": "coordinator"}
    assert set(rec) == set(C["reservations"]["form"])
    before = p.read_bytes()
    with pytest.raises(Exception):  # exclusive create
        ur.write_reservation(store, "RES-HWSU-OF", "hwsu-of-v1", "2026-11-02T00:00:00Z", "x")
    assert p.read_bytes() == before
    ur.write_reservation(store, "RES-HWSU-OF-a2", "hwsu-of-v1", UTC, "coordinator")
    assert (store / "RESERVATION_OF-a2.json").is_file()


# ------------------------------------------------------------------ end_reservation (J8)
def _store_with_obligation(tmp_path, rid="RES-HWSU-OF"):
    root = tmp_path / "root"
    store = root / "hwsu-store"
    store.mkdir(parents=True)
    res = Path(ur.write_reservation(store, rid, "hwsu-of-v1", UTC, "coordinator"))
    obl = _json(store / "REGISTRY_OBLIGATION_OF.json", {"schema": "fixture", "files": []})
    return root, store, res, obl


def test_end_reservation_writes_exact_record(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    res_bytes = res.read_bytes()
    p = Path(ur.end_reservation(store, "RES-HWSU-OF", UTC, obl))
    assert p == store / "reservations" / "RES-HWSU-OF.END.json"
    rec = json.loads(p.read_text(encoding="utf-8"))
    assert set(rec) == END_FIELDS
    assert rec == {"schema": "hws-reservation-end-v1", "reservation_id": "RES-HWSU-OF",
                   "reservation_file": "hwsu-store/RESERVATION_OF.json",
                   "reservation_sha256": _sha(res), "end_utc": UTC,
                   "obligation_file": "hwsu-store/REGISTRY_OBLIGATION_OF.json",
                   "obligation_sha256": _sha(obl), "written_by": "hwsu_records.end_reservation"}
    assert res.read_bytes() == res_bytes  # the reservation file is never edited (J8 item 1)


def test_end_reservation_written_by_argument(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    p = ur.end_reservation(store, "RES-HWSU-OF", UTC, obl, written_by="hwsu_driver_of job 0")
    assert json.loads(Path(p).read_text(encoding="utf-8"))["written_by"] == "hwsu_driver_of job 0"


def test_end_reservation_refuses_absent_reservation(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    _fails("FAIL_TECHNICAL/LINEAGE", ur.end_reservation, store, "RES-HWSU-OF-a2", UTC, obl)
    assert not (store / "reservations" / "RES-HWSU-OF-a2.END.json").exists()


@pytest.mark.parametrize("state", ["ENDED", "active", None])
def test_end_reservation_refuses_not_active(tmp_path, state):
    root = tmp_path / "root"
    store = root / "hwsu-store"
    rec = {"id": "RES-HWSU-OF", "scope": "s", "start_utc": UTC, "end_utc": None,
           "interruptions": [], "job_states": {}, "written_by": "x"}
    if state is not None:
        rec["state"] = state
    _json(store / "RESERVATION_OF.json", rec)
    obl = _json(store / "REGISTRY_OBLIGATION_OF.json", {"files": []})
    _fails("FAIL_TECHNICAL/LINEAGE", ur.end_reservation, store, "RES-HWSU-OF", UTC, obl)
    assert not (store / "reservations").exists() or not any((store / "reservations").iterdir())


def test_end_reservation_refuses_absent_obligation(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    _fails("FAIL_TECHNICAL/LINEAGE", ur.end_reservation, store, "RES-HWSU-OF", UTC,
           store / "REGISTRY_OBLIGATION_OF-a1.json")
    assert not (store / "reservations" / "RES-HWSU-OF.END.json").exists()


def test_end_reservation_refuses_second_call(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    p = Path(ur.end_reservation(store, "RES-HWSU-OF", UTC, obl))
    first = p.read_bytes()
    _fails("FAIL_TECHNICAL/LINEAGE", ur.end_reservation, store, "RES-HWSU-OF",
           "2026-11-02T00:00:00Z", obl)
    assert p.read_bytes() == first


# ------------------------------------------------------------------ W2 attestation (J8 item 4)
def _attest(root, **k):  # API-AMBIGUITY: "active"/"live" read as lists of reservation ids
    return ur.w2_attestation(root, **k)


def test_attestation_live_without_end(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    r = _attest(root)
    assert r["status"] == "INCONCLUSIVE/AUTHORITY"
    assert "RES-HWSU-OF" in r["live"] and "RES-HWSU-OF" in r["active"]


def test_attestation_ended_by_own_end_record(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    ur.end_reservation(store, "RES-HWSU-OF", UTC, obl)
    r = _attest(root)
    assert r["status"] == "PASS" and r["ended"] == {"RES-HWSU-OF": "b"} and r["live"] == []


def test_attestation_reservation_changed_after_end_is_live(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    ur.end_reservation(store, "RES-HWSU-OF", UTC, obl)
    res.write_bytes(res.read_bytes() + b"\n")
    r = _attest(root)
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and "RES-HWSU-OF" in r["live"]


def test_attestation_obligation_changed_after_end_is_live(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    ur.end_reservation(store, "RES-HWSU-OF", UTC, obl)
    obl.write_bytes(obl.read_bytes().replace(b"[]", b"[ ]"))
    r = _attest(root)
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and "RES-HWSU-OF" in r["live"]


def test_attestation_obligation_deleted_after_end_is_live(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    ur.end_reservation(store, "RES-HWSU-OF", UTC, obl)
    obl.unlink()
    assert _attest(root)["status"] == "INCONCLUSIVE/AUTHORITY"


def test_attestation_wrong_schema_end_record_is_live(tmp_path):
    root = tmp_path / "root"
    store = root / "hwsd-store"
    res = _active(store, "RES-HWSD-X", name="RESERVATION_X.json")
    obl = _json(store / "REGISTRY_OBLIGATION.json", {"files": []})
    _end_fixture(store, "RES-HWSD-X", res, obl, root, schema="hws-reservation-end-v0")
    assert _attest(root)["status"] == "INCONCLUSIVE/AUTHORITY"


def test_attestation_accepts_track_d_form_end_record(tmp_path):
    """J8 item 5: the other track's end record, written by hand in the shared schema."""
    root = tmp_path / "root"
    store = root / "hwsd-store"
    res = _active(store, "RES-HWSD-X", name="RESERVATION_X.json")
    obl = _json(store / "REGISTRY_OBLIGATION.json", {"schema": "hws-registry-obligation-v1"})
    _end_fixture(store, "RES-HWSD-X", res, obl, root)
    r = _attest(root)
    assert r["status"] == "PASS" and r["ended"] == {"RES-HWSD-X": "b"}
    obl.write_bytes(obl.read_bytes() + b" ")
    assert _attest(root)["status"] == "INCONCLUSIVE/AUTHORITY"


def _w2_fixture(root, mailbox):
    store = root / "hwsc-store"
    res = _active(store, "RES-HWSC-W2", name="RESERVATION_W2.json", scope="hwsc-v1")
    end = _json(mailbox / "records" / "HWSC_W2_END.json", {
        "schema": "hwsc-w2-end-v1", "reservation_id": "RES-HWSC-W2",
        "reservation_file": "hwsc-store/RESERVATION_W2.json",
        "reservation_file_sha256": _sha(res), "ended": "fixture"})
    return res, end


def test_attestation_rule_a_hwsc_w2(tmp_path):
    root = tmp_path / "root"
    res, end = _w2_fixture(root, tmp_path / "mailbox")
    r = _attest(root, w2_end=end, w2_end_sha256=_sha(end))
    assert r["status"] == "PASS" and r["ended"] == {"RES-HWSC-W2": "a"}


def test_attestation_rule_a_mismatches_are_live(tmp_path):
    root = tmp_path / "root"
    res, end = _w2_fixture(root, tmp_path / "mailbox")
    r = _attest(root, w2_end=end, w2_end_sha256="0" * 64)  # record not bound
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and "RES-HWSC-W2" in r["live"]
    good = _sha(end)
    res.write_bytes(res.read_bytes() + b"\n")  # reservation differs from the bound sha256
    assert _attest(root, w2_end=end, w2_end_sha256=good)["status"] == "INCONCLUSIVE/AUTHORITY"


def test_attestation_rule_a_only_for_res_hwsc_w2(tmp_path):
    root = tmp_path / "root"
    store = root / "other-store"
    res = _active(store, "RES-OTHER", name="RESERVATION_W2.json")
    end = _json(tmp_path / "mb" / "records" / "HWSC_W2_END.json", {
        "reservation_id": "RES-OTHER", "reservation_file": "other-store/RESERVATION_W2.json",
        "reservation_file_sha256": _sha(res)})
    r = _attest(root, w2_end=end, w2_end_sha256=_sha(end))
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and "RES-OTHER" in r["live"]


def test_attestation_stateless_files_not_active(tmp_path):
    root = tmp_path / "root"
    _json(root / "c2nd-store" / "RESERVATION_S1.json", {"scope": "c2nd", "start_utc": UTC})
    _json(root / "c2nd-store" / "RESERVATION_S5.json", {"id": "X", "status": "ACTIVE"})
    r = _attest(root)
    assert r["status"] == "PASS" and r["active"] == [] and r["live"] == []


def test_attestation_own_is_excluded(tmp_path):
    root, store, res, obl = _store_with_obligation(tmp_path)
    assert _attest(root, own="RES-HWSU-OF")["status"] == "PASS"
    _active(root / "x-store", "RES-X")
    r = _attest(root, own="RES-HWSU-OF")
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and r["live"] == ["RES-X"]


def test_attestation_reservations_dir_files_inspected(tmp_path):
    root = tmp_path / "root"
    _json(root / "hwsd-store" / "reservations" / "RES-HWSD-Y.json",
          {"id": "RES-HWSD-Y", "state": "ACTIVE"})
    r = _attest(root)
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and "RES-HWSD-Y" in r["live"]


def test_attestation_unreadable_file_is_live(tmp_path):
    root = tmp_path / "root"
    p = root / "s-store" / "RESERVATION_BAD.json"
    p.parent.mkdir(parents=True)
    p.write_bytes(b"{not json")
    r = _attest(root)
    assert r["status"] == "INCONCLUSIVE/AUTHORITY" and r["live"]


def test_attestation_end_records_not_reservations(tmp_path):
    """END records are excluded from the inspected set; a stale END alone changes nothing."""
    root = tmp_path / "root"
    _json(root / "s-store" / "reservations" / "RES-Z.END.json",
          {"schema": "hws-reservation-end-v1", "reservation_id": "RES-Z", "state": "ACTIVE"})
    r = _attest(root)
    assert r["status"] == "PASS" and r["active"] == []


def test_stopped_attempt_then_rerun_reservation(tmp_path):
    """J10 item 3 / D-17: a no-history obligation ends RES-HWSU-OF; the rerun's own id is excluded."""
    root, store, res, obl = _store_with_obligation(tmp_path)
    obl1 = _json(store / "REGISTRY_OBLIGATION_OF-a1.json", {"files": []})
    ur.end_reservation(store, "RES-HWSU-OF", UTC, obl1)
    ur.write_reservation(store, "RES-HWSU-OF-a2", "hwsu-of-v1", UTC, "coordinator")
    r = _attest(root, own="RES-HWSU-OF-a2")
    assert r["status"] == "PASS" and r["ended"] == {"RES-HWSU-OF": "b"}
    assert _attest(root)["live"] == ["RES-HWSU-OF-a2"]
