"""Author B: reservations, the J8 end record, W2 attestation, stopped sampling (J8, J10 item 3)."""

from __future__ import annotations  # noqa: I001

import json
import sys
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_data as dd  # noqa: E402
import hwsd_readers as drd  # noqa: E402
import test_b_util as bu  # noqa: E402

import k4b_release  # noqa: E402
import pytest  # noqa: E402

AUTH, LIN = "INCONCLUSIVE/AUTHORITY", "FAIL_TECHNICAL/LINEAGE"
END_FIELDS = ["schema", "reservation_id", "reservation_file", "reservation_sha256", "end_utc",
              "obligation_file", "obligation_sha256", "written_by"]


def _active(path: Path, rid: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    k4b_release.start_reservation(path, rid[len("RES-"):], bu.UTC)
    assert json.loads(path.read_text(encoding="utf-8"))["id"] == rid
    return path


def _end_record(store: Path, res: Path, obligation_rel: str, at: Path | None = None) -> Path:
    rid = json.loads(res.read_text(encoding="utf-8"))["id"]
    rec = {"schema": "hws-reservation-end-v1", "reservation_id": rid,
           "reservation_file": res.relative_to(store).as_posix(), "reservation_sha256": bu.sha(res),
           "end_utc": bu.UTC, "obligation_file": obligation_rel,
           "obligation_sha256": bu.sha(store / obligation_rel),
           "written_by": "hwsu_records.end_reservation"}
    return bu.write_json(at or res.with_name(f"{rid}.END.json"), rec)


def test_contract_reservation_and_window():
    assert dc.CONTRACT["reservation"]["end_fields"] == END_FIELDS
    assert dc.CONTRACT["reservation"]["end_schema"] == "hws-reservation-end-v1"
    assert dc.RESERVATION_PREFIX == "RES-HWSD-W2-a"
    assert "hwsu-store/reservations/*.json" in dc.CONTRACT["window"]["reservation_globs"]
    assert "hwsc-store/RESERVATION_W2.json" in dc.CONTRACT["window"]["reservation_globs"]


def test_start_and_verify_reservation(tmp_path):
    s = tmp_path / "hwsd-store"
    path, rec = dd.start_reservation_d(s, 1, bu.UTC)
    assert path == dd.reservation_path(s, 1) == s / "reservations" / "RES-HWSD-W2-a1.json"
    assert rec["id"] == "RES-HWSD-W2-a1" and rec["state"] == "ACTIVE" and rec["end_utc"] is None
    assert dd.verify_reservation_d(path, "RES-HWSD-W2-a1")["status"] == "PASS"
    assert dd.verify_reservation_d(path, "RES-HWSD-W2-a9")["status"] != "PASS"


def test_start_refused_while_another_active_unended(tmp_path):
    s = tmp_path / "hwsd-store"
    dd.start_reservation_d(s, 1, bu.UTC)
    with pytest.raises(bu.C1GateFailure) as e:
        dd.start_reservation_d(s, 2, bu.UTC)
    assert bu.status_of(e.value) == AUTH
    assert not dd.reservation_path(s, 2).exists()


def test_end_reservation_writes_the_j8_record(tmp_path):
    s = tmp_path / "hwsd-store"
    res, _ = dd.start_reservation_d(s, 1, bu.UTC)
    before = res.read_bytes()
    obl, _ = dd.write_obligation(s, "REGISTRY_OBLIGATION.json", "0300", 1, bu.UTC,
                                 reservation_id="RES-HWSD-W2-a1")
    rec = dd.end_reservation(s, "RES-HWSD-W2-a1", "2026-11-01T13:00:00Z", obl)
    end = s / "reservations" / "RES-HWSD-W2-a1.END.json"
    assert json.loads(end.read_text(encoding="utf-8")) == rec
    assert set(rec) == set(END_FIELDS)
    assert rec["schema"] == "hws-reservation-end-v1" and rec["reservation_id"] == "RES-HWSD-W2-a1"
    assert rec["reservation_file"] == "reservations/RES-HWSD-W2-a1.json"
    assert rec["reservation_sha256"] == bu.sha(res) and rec["end_utc"] == "2026-11-01T13:00:00Z"
    assert rec["obligation_file"] == "REGISTRY_OBLIGATION.json"
    assert rec["obligation_sha256"] == bu.sha(obl)
    assert rec["written_by"] == "hwsd_data.end_reservation"
    assert res.read_bytes() == before  # J8 item 1: never edited
    assert dd.reservation_ended(res)["ended"] is True
    assert dd.reservation_ended(res)["rule"] == "b"
    second = end.read_bytes()
    with pytest.raises(bu.C1GateFailure) as e:  # J8 item 3: end record exists
        dd.end_reservation(s, "RES-HWSD-W2-a1", bu.UTC, obl)
    assert bu.status_of(e.value) == LIN and end.read_bytes() == second
    path2, _ = dd.start_reservation_d(s, 2, bu.UTC)  # the ended one no longer blocks
    assert path2.name == "RES-HWSD-W2-a2.json"


def test_end_reservation_refusals_write_nothing(tmp_path):
    s = tmp_path / "hwsd-store"
    res, _ = dd.start_reservation_d(s, 1, bu.UTC)
    end = s / "reservations" / "RES-HWSD-W2-a1.END.json"
    with pytest.raises(bu.C1GateFailure) as e:  # obligation absent
        dd.end_reservation(s, "RES-HWSD-W2-a1", bu.UTC, s / "REGISTRY_OBLIGATION.json")
    assert bu.status_of(e.value) == LIN and not end.exists()
    outside = bu.write_json(tmp_path / "elsewhere" / "REGISTRY_OBLIGATION.json", {})
    with pytest.raises(bu.C1GateFailure) as e:  # obligation not in the store
        dd.end_reservation(s, "RES-HWSD-W2-a1", bu.UTC, outside)
    assert bu.status_of(e.value) == LIN and not end.exists()
    obl, _ = dd.write_obligation(s, "REGISTRY_OBLIGATION.json", "0300", 1, bu.UTC)
    with pytest.raises(bu.C1GateFailure) as e:  # reservation missing
        dd.end_reservation(s, "RES-HWSD-W2-a7", bu.UTC, obl)
    assert bu.status_of(e.value) == LIN
    assert not (s / "reservations" / "RES-HWSD-W2-a7.END.json").exists()
    rec = json.loads(res.read_text(encoding="utf-8"))
    rec["state"] = "RELEASED"
    res.write_text(json.dumps(rec), encoding="utf-8")
    with pytest.raises(bu.C1GateFailure) as e:  # not ACTIVE
        dd.end_reservation(s, "RES-HWSD-W2-a1", bu.UTC, obl)
    assert bu.status_of(e.value) == LIN and not end.exists()


def test_attestation_live_without_end_and_after_changes(tmp_path):
    root = tmp_path / "root"
    s = root / "hwsd-store"
    res, _ = dd.start_reservation_d(s, 1, bu.UTC)
    a = dd.w2_attest(root)
    assert a["status"] == AUTH and len(a["live"]) == 1
    assert dd.w2_attest(root, exclude=(res,))["status"] == "PASS"  # CONTRACT window.own_rule
    obl, _ = dd.write_obligation(s, "REGISTRY_OBLIGATION.json", "0300", 1, bu.UTC)
    dd.end_reservation(s, "RES-HWSD-W2-a1", bu.UTC, obl)
    a = dd.w2_attest(root)
    assert a["status"] == "PASS" and a["live"] == [] and a["schema_failures"] == []
    assert [c["id"] for c in a["checked"]] == ["RES-HWSD-W2-a1"]  # *.END.json not attested
    obl.write_text(obl.read_text(encoding="utf-8") + " ", encoding="utf-8")
    assert dd.reservation_ended(res)["ended"] is False  # obligation changed after the end
    assert dd.w2_attest(root)["status"] == AUTH
    obl.write_text(obl.read_text(encoding="utf-8")[:-1], encoding="utf-8")
    assert dd.w2_attest(root)["status"] == "PASS"
    res.write_text(res.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert dd.reservation_ended(res)["ended"] is False  # reservation changed after its end
    assert dd.w2_attest(root)["status"] == AUTH


def test_track_u_end_record_is_accepted(tmp_path):
    root = tmp_path / "root"
    u = root / "hwsu-store"
    res = _active(u / "reservations" / "RES-HWSU-OF-a1.json", "RES-HWSU-OF-a1")
    obl = bu.put_obligation(u, bu.u_obligation(u, []))
    _end_record(u, res, obl.name)
    r = dd.reservation_ended(res)
    assert r["ended"] is True and r["rule"] == "b"
    assert dd.w2_attest(root)["status"] == "PASS"
    obl.write_text(obl.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert dd.w2_attest(root)["status"] == AUTH


def test_track_u_top_level_reservation(tmp_path):
    # SPEC-QUESTION: API.md reservation_ended (b) looks for <dir of res_path>/<id>.END.json; the
    # CONTRACT window.ended_rule (and J8 item 2) put it in <store>/reservations/ for a
    # top-level reservation. Tested per CONTRACT/J8.
    root = tmp_path / "root"
    u = root / "hwsu-store"
    res = _active(u / "RESERVATION_OF.json", "RES-HWSU-OF-a2")
    obl = bu.put_obligation(u, bu.u_obligation(u, []))
    assert dd.w2_attest(root)["status"] == AUTH
    _end_record(u, res, obl.name, at=u / "reservations" / "RES-HWSU-OF-a2.END.json")
    assert dd.reservation_ended(res)["ended"] is True
    assert dd.w2_attest(root)["status"] == "PASS"


def test_end_record_of_wrong_schema_is_live(tmp_path):
    root = tmp_path / "root"
    u = root / "hwsu-store"
    res = _active(u / "reservations" / "RES-HWSU-OF-a1.json", "RES-HWSU-OF-a1")
    obl = bu.put_obligation(u, bu.u_obligation(u, []))
    end = _end_record(u, res, obl.name)
    rec = json.loads(end.read_text(encoding="utf-8"))
    end.write_text(json.dumps(dict(rec, schema="hwsc-w2-end-v1")), encoding="utf-8")
    assert dd.reservation_ended(res)["ended"] is False
    assert dd.w2_attest(root)["status"] == AUTH


def test_non_active_and_schema_failures(tmp_path):
    root = tmp_path / "root"
    k = bu.write_json(root / "k4b-store" / "RESERVATION_K.json",
                      {"id": "RES-K", "state": "RELEASED", "end_utc": bu.UTC})
    a = dd.w2_attest(root)
    assert a["status"] == "PASS" and a["live"] == [] and len(a["checked"]) == 1
    bu.write_json(root / "hwsb-store" / "RESERVATION_B.json", {"scope": "x"})
    a = dd.w2_attest(root)
    assert a["status"] == AUTH and len(a["schema_failures"]) == 1 and a["live"] == []
    (root / "hwsb-store" / "RESERVATION_B.json").write_text("[1, 2]", encoding="utf-8")
    assert dd.w2_attest(root)["status"] == AUTH
    (root / "hwsb-store" / "RESERVATION_B.json").unlink()
    k.write_text(json.dumps({"id": "RES-K", "state": "ACTIVE"}), encoding="utf-8")
    assert dd.w2_attest(root)["status"] == AUTH
    bu.write_json(root / "hwsd-store" / "reservations" / "RES-X.END.json", {"orphan": True})
    k.unlink()
    assert dd.w2_attest(root)["status"] == "PASS"  # *.END.json files are excluded


def _hwsc_w2(root: Path, res_bytes: bytes, end_bytes: bytes) -> Path:
    res = root / "hwsc-store" / "RESERVATION_W2.json"
    res.parent.mkdir(parents=True)
    res.write_bytes(res_bytes)
    end = root / "agent-handoff" / "records" / "HWSC_W2_END.json"
    end.parent.mkdir(parents=True)
    end.write_bytes(end_bytes)
    return res


def test_hwsc_w2_end_fixture_rule_a(tmp_path, monkeypatch):
    root = tmp_path / "root"
    res_bytes = json.dumps({"id": "RES-HWSC-W2", "state": "ACTIVE", "end_utc": None}).encode()
    import hashlib

    end_obj = {"schema": "hwsc-w2-end-v1", "reservation_id": "RES-HWSC-W2",
               "reservation_file": "hwsc-store/RESERVATION_W2.json",
               "reservation_file_sha256": hashlib.sha256(res_bytes).hexdigest()}
    end_bytes = json.dumps(end_obj).encode()
    res = _hwsc_w2(root, res_bytes, end_bytes)
    assert dd.reservation_ended(res, root=root)["ended"] is False  # CONTRACT sha differs
    monkeypatch.setitem(dc.CONTRACT["identity"]["rows"]["hwsc_w2_end"], "sha256",
                        hashlib.sha256(end_bytes).hexdigest())
    r = dd.reservation_ended(res, root=root)
    assert r["ended"] is True and r["rule"] == "a"
    assert dd.w2_attest(root)["status"] == "PASS"
    res.write_bytes(res_bytes + b"\n")  # changed after the end record
    assert dd.reservation_ended(res, root=root)["ended"] is False
    assert dd.w2_attest(root)["status"] == AUTH


def test_real_hwsc_w2_end_record_copy(tmp_path):
    """The bound mailbox record and stage C's reservation record (JSON records, copied)."""
    real_end = dc.MAILBOX / "records" / "HWSC_W2_END.json"
    real_res = dc.HWSC_STORE / "RESERVATION_W2.json"
    if not (real_end.exists() and real_res.exists()):
        pytest.skip("stage-C records not present")
    assert bu.sha(real_end) == dc.CONTRACT["identity"]["rows"]["hwsc_w2_end"]["sha256"]
    root = tmp_path / "root"
    res = _hwsc_w2(root, real_res.read_bytes(), real_end.read_bytes())
    r = dd.reservation_ended(res, root=root)
    assert r["ended"] is True and r["rule"] == "a"
    assert dd.w2_attest(root)["status"] == "PASS"


def test_stopped_sample_before_first_row_and_rerun(tmp_path):
    """J10 item 3 / F-1: no history file, obligation + END, a rerun opens a new id."""
    root = tmp_path / "root"
    s = root / "hwsd-store"
    bu.tiny_artifacts(s / "artifacts")  # the process artifacts SAMPLE builds before H1D
    dd.start_reservation_d(s, 1, bu.UTC)
    out = dd.stop_obligation(s, "0300", 1, "RES-HWSD-W2-a1", "2026-11-01T14:00:00Z")
    assert set(out) == {"obligation", "end"}
    obl_path = s / "REGISTRY_OBLIGATION_0300-a1.json"
    obl = json.loads(obl_path.read_text(encoding="utf-8"))
    assert obl["job"] == "0300" and obl["attempt"] == 1 and obl["reservation_id"] == "RES-HWSD-W2-a1"
    assert {f["class"] for f in obl["files"]} <= {"NON_HISTORY", "ObservationSet"}
    assert not any(f["class"] == "K4b history table" for f in obl["files"])
    end = json.loads((s / "reservations" / "RES-HWSD-W2-a1.END.json").read_text(encoding="utf-8"))
    assert end["obligation_file"] == "REGISTRY_OBLIGATION_0300-a1.json"
    assert end["obligation_sha256"] == bu.sha(obl_path)
    assert dd.w2_attest(root)["status"] == "PASS"
    assert drd.obligation_check(s)["status"] == "PASS"
    path2, rec2 = dd.start_reservation_d(s, 2, bu.UTC)
    assert rec2["id"] == "RES-HWSD-W2-a2" and path2.name == "RES-HWSD-W2-a2.json"
    assert (s / "reservations" / "RES-HWSD-W2-a1.json").exists()
