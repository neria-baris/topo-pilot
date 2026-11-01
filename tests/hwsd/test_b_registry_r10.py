"""Author B: obligations (J3, J4, J10, J11) and the R10 reader (API.md §3.4, §4; DRD8)."""

from __future__ import annotations  # noqa: I001

import copy
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

import numpy as np  # noqa: E402
import pytest  # noqa: E402

PASS, INC = "PASS", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
OBL = dc.CONTRACT["obligation"]
TOP = ["schema", "store", "track", "job", "attempt", "written_utc", "written_by",
       "reservation_id", "name_rules", "dry_stores", "files", "rule"]
PER_FILE = ["relpath", "sha256", "bytes", "class", "reader", "basis"]


def test_contract_obligation_is_exactly_j11():
    assert OBL["schema"] == "hws-registry-obligation-v1"
    assert OBL["fields"] == TOP
    assert OBL["file_fields"] == PER_FILE
    assert OBL["classes"] == ["ObservationSet", "K4b history table", "NON_HISTORY"]
    assert set(OBL["bases"]) == {"artifact", "registry", "name_rule"}
    assert OBL["name_kinds"] == ["chart", "decoder", "activation", "oracle-moment", "score",
                                 "bootstrap", "certificate"]
    assert OBL["readers"] == bu.READER
    assert all(set(r) == {"kind", "regex"} and r["kind"] in OBL["name_kinds"]
               for r in OBL["name_rules"])


# ----------------------------------------------------------------- writer (track D)


def _d_store(tmp_path) -> Path:
    s = tmp_path / "hwsd-store"
    bu.tiny_artifacts(s / "artifacts")
    bu.fake_artifact(s / "artifacts", "Checkpoint", "abc0000000000001", ("payload.npz", "state.pt"))
    bu.save_table(s / "stages/S3/HIST_cal_b0.npz", bu.hist_table("cal", 520, 3, 9_000_000))
    bu.array_npz(s / "registry/K-REG1_digests.npz", digests=np.array(["b" * 64], "<U64"))
    (s / "registry/runs/K-REG1").mkdir(parents=True)
    np.save(s / "registry/runs/K-REG1/run_00000.npy", np.zeros((4, 32), np.uint8))
    bu.array_npz(s / "stages/SCORE/620301/s0/CHART.npz")
    bu.array_npz(s / "stages/SCORE/620301/s0/ARRAYS.npz")
    bu.array_npz(s / "stages/S4/ORACLE_cal.npz")
    bu.array_npz(s / "stages/S4/LGATE_Q.npz")
    bu.write_json(s / "stages/KD/KD_RECORD.json", {"status": "PASS"})
    return s


def _expected_class(rel: str):
    parts = rel.split("/")
    if rel.startswith("stages/S3/HIST_"):
        return "K4b history table", None
    if "artifacts" in parts:
        t = parts[parts.index("artifacts") + 1]
        return ("ObservationSet", None) if t == "ObservationSet" else ("NON_HISTORY", "artifact")
    if "registry" in parts[:-1]:
        return "NON_HISTORY", "registry"
    return "NON_HISTORY", "name_rule"


def test_write_obligation_j11_form_and_round_trip(tmp_path):
    s = _d_store(tmp_path)
    path, obl = dd.write_obligation(s, "REGISTRY_OBLIGATION_0300-a1.json", "0300", 1, bu.UTC)
    assert path == s / "REGISTRY_OBLIGATION_0300-a1.json"
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    assert set(on_disk) == set(TOP) and on_disk["files"] == obl["files"]
    assert on_disk["schema"] == "hws-registry-obligation-v1" and on_disk["track"] == "D"
    assert on_disk["job"] == "0300" and on_disk["attempt"] == 1 and on_disk["written_utc"] == bu.UTC
    assert on_disk["written_by"] == "hwsd" and on_disk["reservation_id"] is None
    assert on_disk["name_rules"] == OBL["name_rules"] and on_disk["dry_stores"] == []
    assert on_disk["rule"] == "fail closed"
    # SPEC-QUESTION: API.md writes "store": str(store) (backslashes on Windows); CONTRACT
    # obligation.types and J11 say "absolute path, forward slashes". Tested per J11.
    assert "\\" not in on_disk["store"] and Path(on_disk["store"]) == s
    rels = [f["relpath"] for f in on_disk["files"]]
    arrays = sorted(p.relative_to(s).as_posix() for p in s.rglob("*")
                    if p.suffix in (".npz", ".npy", ".pt"))
    assert rels == sorted(rels) == arrays
    for f in on_disk["files"]:
        assert set(f) == set(PER_FILE)
        cls, basis = _expected_class(f["relpath"])
        assert (f["class"], f["basis"], f["reader"]) == (cls, basis, bu.READER[cls]), f
        assert f["bytes"] == (s / f["relpath"]).stat().st_size
        if "/artifacts/Checkpoint/" in "/" + f["relpath"]:
            assert f["sha256"] is None  # J11: never opened or hashed
        else:
            assert f["sha256"] == bu.sha(s / f["relpath"])
    r = drd.obligation_check(s)
    assert r["status"] == PASS, r["other"]
    assert r["obligation"] == "REGISTRY_OBLIGATION_0300-a1.json"
    assert bu.expected_os_digests(s / "artifacts") <= r["digests"]
    hist = np.load(s / "stages/S3/HIST_cal_b0.npz")
    assert set(hist["digest"].astype(str).tolist()) <= r["digests"]
    assert set(hist["seq_ids"].tolist()) <= r["seq_ids"]


@pytest.mark.parametrize("rel", ["stages/S4/UNKNOWN.npz", "stages/SCORE/620301/s0/X.npy",
                                 "tmp/w.pt", "artifacts/Bogus/abc1/payload.npz"])
def test_write_obligation_unclassifiable_is_lineage_and_writes_nothing(tmp_path, rel):
    s = tmp_path / "st"
    bu.junk(s / rel)
    with pytest.raises(bu.C1GateFailure) as e:
        dd.write_obligation(s, "REGISTRY_OBLIGATION.json", "0300", 1, bu.UTC)
    assert bu.status_of(e.value) == "FAIL_TECHNICAL/LINEAGE"
    assert not (s / "REGISTRY_OBLIGATION.json").exists()


def test_classify_file_rules(tmp_path):
    s = _d_store(tmp_path)
    os_rel = bu.os_payloads(s / "artifacts")[0].relative_to(s).as_posix()
    assert dd.classify_file(s, os_rel) == ("ObservationSet", None)
    assert dd.classify_file(s, "stages/S3/HIST_cal_b0.npz") == ("K4b history table", None)
    assert dd.classify_file(s, "artifacts/Checkpoint/abc0000000000001/state.pt") == \
        ("NON_HISTORY", "artifact")
    assert dd.classify_file(s, "registry/K-REG1_digests.npz") == ("NON_HISTORY", "registry")
    assert dd.classify_file(s, "stages/SCORE/620301/s0/CHART.npz") == ("NON_HISTORY", "name_rule")
    bu.fake_artifact(s / "artifacts", "Checkpoint", "abc0000000000002", meta="WorldSpec")
    with pytest.raises(bu.C1GateFailure) as e:
        dd.classify_file(s, "artifacts/Checkpoint/abc0000000000002/payload.npz")
    assert bu.status_of(e.value) == "FAIL_TECHNICAL/LINEAGE"


@pytest.mark.parametrize("name", ["REGISTRY_OBLIGATION_0301-a1.json", "REGISTRY_OBLIGATION_0300-a2.json",
                                  "REGISTRY_OBLIGATION_X.json", "OBLIGATION.json"])
def test_write_obligation_name_rule(tmp_path, name):
    s = tmp_path / "st"
    s.mkdir()
    with pytest.raises(ValueError):
        dd.write_obligation(s, name, "0300", 1, bu.UTC)


def test_write_obligation_exclusive(tmp_path):
    s = tmp_path / "st"
    s.mkdir()
    dd.write_obligation(s, "REGISTRY_OBLIGATION.json", "0300", 1, bu.UTC)
    before = (s / "REGISTRY_OBLIGATION.json").read_bytes()
    with pytest.raises(FileExistsError):
        dd.write_obligation(s, "REGISTRY_OBLIGATION.json", "0300", 1, "2026-11-02T00:00:00Z")
    assert (s / "REGISTRY_OBLIGATION.json").read_bytes() == before


def test_kd_only_store_with_its_obligation_passes(tmp_path):
    s = tmp_path / "hwsd-store"
    for rel in ("stages/KD/KD_RECORD.json", "stages/KD/G0D.json",
                "stages/KD/REPRO/620301/s0/CHART_CONSTRUCTIONS.json"):
        bu.write_json(s / rel, {"status": "PASS"})
    (s / "GATES.jsonl").write_text("{}\n", encoding="utf-8")
    _, obl = dd.write_obligation(s, "REGISTRY_OBLIGATION_0300-a1.json", "0300", 1, bu.UTC)
    assert obl["files"] == []
    assert drd.obligation_check(s)["status"] == PASS


# ---------------------------------------------- reader on track U's form (J11)


@pytest.fixture
def ustore(tmp_path):
    s = tmp_path / "hwsu-store"
    info = bu.build_u_store(s)
    bu.put_obligation(s, bu.u_obligation(s, info["entries"]))
    return s, info


def test_reader_accepts_track_u_form(ustore, monkeypatch):
    s, info = ustore
    spy = bu.OpenSpy().install(monkeypatch)
    r = drd.obligation_check(s)
    assert r["status"] == PASS, r["other"]
    assert r["obligation"] == "REGISTRY_OBLIGATION_OF.json"
    assert info["os_digests"] <= r["digests"] and info["hist_digests"] <= r["digests"]
    ck = s / "artifacts" / "Checkpoint" / "c0ffee0000000001"
    assert spy.opened_under(ck / "state.pt") == [] and spy.opened_under(ck / "payload.npz") == []


TOP_MUTATIONS = {
    "missing_key": lambda o: o.pop("written_by"),
    "extra_key": lambda o: o.__setitem__("note", "x"),
    "schema": lambda o: o.__setitem__("schema", "hws-registry-obligation-v2"),
    "track": lambda o: o.__setitem__("track", "X"),
    "rule": lambda o: o.__setitem__("rule", "fail open"),
    "name_kind": lambda o: o["name_rules"].append({"kind": "weights", "regex": "nothing"}),
    "name_rule_key": lambda o: o["name_rules"][0].__setitem__("glob", "x"),
}


def _file(o, suffix):
    return next(f for f in o["files"] if f["relpath"].endswith(suffix))


FILE_MUTATIONS = {
    "file_missing_key": lambda o: _file(o, "CHART_1.npz").pop("reader"),
    "file_extra_key": lambda o: _file(o, "CHART_1.npz").__setitem__("note", 1),
    "unknown_class": lambda o: _file(o, "CHART_1.npz").__setitem__("class", "History"),
    "reader_for_class": lambda o: _file(o, "HIST_of_b0.npz").__setitem__(
        "reader", "hwsb_registry.registry_digests"),
    "reader_on_non_history": lambda o: _file(o, "CHART_1.npz").__setitem__(
        "reader", "k4b_history_table"),
    "old_basis_form": lambda o: _file(o, "state.pt").__setitem__("basis", "artifact:Checkpoint"),
    "basis_on_history": lambda o: _file(o, "HIST_of_b0.npz").__setitem__("basis", "registry"),
    "basis_null_non_history": lambda o: _file(o, "ORACLE_cal.npz").__setitem__("basis", None),
    "unknown_basis": lambda o: _file(o, "ORACLE_cal.npz").__setitem__("basis", "bootstrap"),
    "name_rule_unmatched": lambda o: o["name_rules"].pop(0),
    "registry_basis_wrong": lambda o: _file(o, "CHART_1.npz").__setitem__("basis", "registry"),
    "artifact_basis_wrong": lambda o: _file(o, "ORACLE_cal.npz").__setitem__("basis", "artifact"),
    "sha_mismatch": lambda o: _file(o, "ORACLE_cal.npz").__setitem__("sha256", "0" * 64),
    "hist_sha_mismatch": lambda o: _file(o, "HIST_of_b0.npz").__setitem__("sha256", "1" * 64),
    "null_sha_non_checkpoint": lambda o: _file(o, "CHART_1.npz").__setitem__("sha256", None),
    "unlisted_array": lambda o: o["files"].remove(_file(o, "CHART_1.npz")),
    "duplicate": lambda o: o["files"].append(copy.deepcopy(_file(o, "CHART_1.npz"))),
    "listed_missing": lambda o: o["files"].append(dict(_file(o, "CHART_1.npz"),
                                                       relpath="stages/OF/charts/CHART_9.npz")),
}


@pytest.mark.parametrize("which", sorted(TOP_MUTATIONS) + sorted(FILE_MUTATIONS))
def test_one_mutated_key_or_value_is_incomplete(ustore, which):
    s, info = ustore
    obl = bu.u_obligation(s, info["entries"])
    (TOP_MUTATIONS.get(which) or FILE_MUTATIONS[which])(obl)
    (s / "REGISTRY_OBLIGATION_OF.json").unlink()
    bu.put_obligation(s, obl)
    r = drd.obligation_check(s)
    assert r["status"] == INC, which
    assert r["other"]


def test_os_payload_sha_mismatch_is_incomplete(ustore):
    s, info = ustore
    obl = bu.u_obligation(s, info["entries"])
    next(f for f in obl["files"] if f["class"] == "ObservationSet")["sha256"] = "2" * 64
    (s / "REGISTRY_OBLIGATION_OF.json").unlink()
    bu.put_obligation(s, obl)
    assert drd.obligation_check(s)["status"] == INC


def test_unlisted_array_added_after_obligation_is_incomplete(ustore):
    s, _ = ustore
    bu.array_npz(s / "stages/OF/charts/CHART_2.npz")
    assert drd.obligation_check(s)["status"] == INC


def test_newest_obligation_governs(ustore):
    s, info = ustore
    full = bu.u_obligation(s, info["entries"], utc="2026-11-01T10:00:00Z")
    short = bu.u_obligation(s, info["entries"][1:], utc="2026-11-02T10:00:00Z")
    (s / "REGISTRY_OBLIGATION_OF.json").unlink()
    bu.put_obligation(s, full, "REGISTRY_OBLIGATION_OF.json")
    bu.put_obligation(s, short, "REGISTRY_OBLIGATION.json")
    assert drd.obligation_check(s)["status"] == INC
    (s / "REGISTRY_OBLIGATION.json").unlink()
    bu.put_obligation(s, dict(short, written_utc="2026-10-31T10:00:00Z"), "REGISTRY_OBLIGATION.json")
    r = drd.obligation_check(s)
    assert r["status"] == PASS and r["obligation"] == "REGISTRY_OBLIGATION_OF.json", (r["other"], r.get("obligation"))


def test_written_utc_tie_takes_last_name(ustore):
    s, info = ustore
    (s / "REGISTRY_OBLIGATION_OF.json").unlink()
    bu.put_obligation(s, bu.u_obligation(s, info["entries"][1:]), "REGISTRY_OBLIGATION_A.json")
    bu.put_obligation(s, bu.u_obligation(s, info["entries"]), "REGISTRY_OBLIGATION_B.json")
    assert drd.obligation_check(s)["status"] == PASS
    (s / "REGISTRY_OBLIGATION_A.json").rename(s / "REGISTRY_OBLIGATION_C.json")
    assert drd.obligation_check(s)["status"] == INC


def test_store_without_obligation_is_incomplete(tmp_path):
    s = tmp_path / "hwsu-store"
    s.mkdir()
    assert drd.obligation_check(s)["status"] == INC  # empty store too (API §4)
    bu.array_npz(s / "registry/x.npz")
    r = drd.obligation_check(s)
    assert r["status"] == INC and r["other"]


def test_kd_only_store_in_track_u_form_passes(tmp_path):
    s = tmp_path / "hwsu-store"
    bu.write_json(s / "stages/KC/KC_RECORD.json", {"status": "PASS"})
    bu.put_obligation(s, bu.u_obligation(s, []))
    assert drd.obligation_check(s)["status"] == PASS


# ------------------------------------------------------------------ source_hwsu


def _hwsu_dry(folder: Path, with_obligation: bool) -> None:
    bu.tiny_artifacts(folder / "artifacts")
    if with_obligation:
        entries = []
        for p in sorted(folder.rglob("*.npz")):
            rel = p.relative_to(folder).as_posix()
            cls = "ObservationSet" if "/ObservationSet/" in rel else "NON_HISTORY"
            entries.append(bu.u_entry(folder, rel, cls, None if cls == "ObservationSet" else "artifact"))
        obl = dict(bu.u_obligation(folder, entries), attempt=None, job="0198-DRY")
        bu.put_obligation(folder, obl, "REGISTRY_OBLIGATION.json")


def test_source_hwsu_store_with_of_obligation_only(tmp_path, ustore):
    s, info = ustore
    root, scratch = s.parent, tmp_path / "scratch"
    scratch.mkdir()
    r = drd.source_hwsu(root, scratch)
    assert r["status"] == PASS, r["other"]
    assert info["os_digests"] <= r["digests"]


def test_source_hwsu_absent_everything(tmp_path):
    (tmp_path / "root").mkdir()
    (tmp_path / "scratch").mkdir()
    r = drd.source_hwsu(tmp_path / "root", tmp_path / "scratch")
    assert r["status"] == PASS and not r["digests"]


def test_source_hwsu_dry_store_needs_its_own_obligation(tmp_path):
    root, scratch = tmp_path / "root", tmp_path / "scratch"
    root.mkdir()
    _hwsu_dry(scratch / "hwsu-dry", with_obligation=False)
    assert drd.source_hwsu(root, scratch)["status"] == INC  # J4, no exception
    _hwsu_dry(scratch / "hwsu-dry-0199", with_obligation=True)
    assert drd.source_hwsu(root, scratch)["status"] == INC
    import shutil

    shutil.rmtree(scratch / "hwsu-dry")
    r = drd.source_hwsu(root, scratch)
    assert r["status"] == PASS, r["other"]
    assert bu.expected_os_digests(scratch / "hwsu-dry-0199" / "artifacts") <= r["digests"]


def test_source_hwsu_unreadable_array_in_job_folder(tmp_path):
    root, scratch = tmp_path / "root", tmp_path / "scratch"
    root.mkdir()
    bu.junk(scratch / "hwsu-job-0200" / "x.npz", b"not a zip file")
    assert drd.source_hwsu(root, scratch)["status"] == INC


def test_source_hwsu_skips_test_roots(tmp_path, monkeypatch):
    root, scratch = tmp_path / "root", tmp_path / "scratch"
    root.mkdir()
    bu.junk(scratch / "test_hwsu-0198" / "pytest" / "bad.npz", b"not a zip file")
    spy = bu.OpenSpy().install(monkeypatch)
    r = drd.source_hwsu(root, scratch)
    assert r["status"] == PASS
    assert spy.opened_under(scratch / "test_hwsu-0198") == []
