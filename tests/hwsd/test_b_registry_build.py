"""Author B: K-REG-D composition, scratch scan/check mirrors, root inventory, tables (§4.1; DRD8)."""

from __future__ import annotations  # noqa: I001

import sys
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_readers as drd  # noqa: E402
import hwsd_registry as dr  # noqa: E402
import test_b_util as bu  # noqa: E402

import hwsc_dry  # noqa: E402
import hwsc_registry  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

PASS, INC, LIN = "PASS", "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
UTCDIR = "DRD1/20261101T120000Z"


def _hist(path, n=8):
    return bu.array_npz(path, canon32=np.full((n, 32), 7, np.uint8))


def test_effective_tables():
    assert dc.inherited_sha_ok() is True
    st, rt = dc.scratch_table(), dc.root_table()
    assert len(st) == 197 and len(rt) == 73
    for k in ("hwsc-job-0181", "hwsc-job-0196", "hwsd-dry", "hwsd-dry-<job>", "hwsd-kd-<job>",
              "hwsu-*", "test_hwsd-<job>", "test_hwsu-<job>", "hwsc-dry-<job>", "test_hwsc-<job>"):
        assert k in st, k
    assert st["hwsc-job-0181"]["decision"] == "EXCLUSION"  # TO_FREEZE review erratum
    assert rt["hwsc-store"]["decision"] == "READER" and rt["hwsc-store"]["readers"] == ["R9"]
    assert rt["hwsd-store"]["decision"] == "OWN"
    assert rt["hwsu-store"] == dc.CONTRACT["registry"]["inventory"]["rows"]["hwsu-store"]
    rt["hwsd-store"] = {"decision": "EXCLUSION"}
    st.clear()
    assert dc.root_table()["hwsd-store"]["decision"] == "OWN" and len(dc.scratch_table()) == 197


def test_tables_refuse_a_changed_stage_c_contract(monkeypatch):
    for sec in ("scratch_inventory", "inventory"):
        monkeypatch.setitem(dc.CONTRACT["registry"][sec]["inherit"], "sha256", "0" * 64)
    monkeypatch.setitem(dc.CONTRACT["identity"]["rows"]["hwsc_contract"], "sha256", "0" * 64)
    assert dc.inherited_sha_ok() is False
    for fn in (dc.scratch_table, dc.root_table):
        with pytest.raises(bu.C1GateFailure) as e:
            fn()
        assert bu.status_of(e.value) == "FAIL_TECHNICAL/IDENTITY"


@pytest.mark.parametrize("name,key", [
    ("hwsc-dry-0177", "hwsc-dry-<job>"), ("test_hwsc-0190", "test_hwsc-<job>"),
    ("hwsd-dry-0201", "hwsd-dry-<job>"), ("hwsd-kd-0300", "hwsd-kd-<job>"),
    ("test_hwsd-0197", "test_hwsd-<job>"), ("test_hwsu-0198", "test_hwsu-<job>"),
    ("hwsu-dry", "hwsu-*"), ("hwsu-job-1", "hwsu-*"), ("hwsd-dry", "hwsd-dry")])
def test_row_for_d_patterns(name, key):
    t = dc.scratch_table()
    assert dr.row_for_d(name, t) == t[key]


def test_row_for_d_none():
    assert dr.row_for_d("brand-new-folder", dc.scratch_table()) is None


def _scratch(tmp_path, monkeypatch=None) -> Path:
    sc = tmp_path / "scratch"
    _hist(sc / "plain/a.npz")
    _hist(sc / "plain/test_deep/b.npz")
    _hist(sc / "test_top/c.npz")
    _hist(sc / "hwsb-dry/test_inner/d.npz")
    _hist(sc / "test_hwsb-0300/pytest/e.npz")
    bu.junk(sc / "hwsc-job-0181/logs/arr.npz")
    bu.junk(sc / "hwsc-job-0181/w.pt")
    bu.junk(sc / "plain/m.pt")
    bu.write_json(sc / "plain/st/ObservationSet/ab12/meta.json", {"artifact_type": "ObservationSet"})
    _hist(sc / "top.npz")
    return sc


def test_scratch_scan_d(tmp_path, monkeypatch):
    sc = _scratch(tmp_path)
    spy = bu.OpenSpy().install(monkeypatch)
    scan = dr.scratch_scan_d(sc)
    assert spy.opened_under(sc / "hwsc-job-0181") == []
    assert spy.opened_under(sc / "test_top") == [] and spy.opened_under(sc / "plain/test_deep") == []
    job = {k.replace("\\", "/"): v for k, v in scan["hwsc-job-0181"].items()}
    assert set(job) == {"logs/arr.npz", "w.pt"}
    assert all(v["class"] == "blinded_array" and v["shape"] is None for v in job.values())
    plain = {k.replace("\\", "/"): v["class"] for k, v in scan["plain"].items()}
    assert plain.get("a.npz") == "history" and "test_deep/b.npz" not in plain
    assert plain.get("m.pt") == "pt" and plain.get("st/ObservationSet/ab12/meta.json") == "os_root"
    assert "test_top" not in scan
    assert "test_inner/d.npz" in {k.replace("\\", "/") for k in scan["hwsb-dry"]}
    assert "pytest/e.npz" in {k.replace("\\", "/") for k in scan["test_hwsb-0300"]}
    assert [Path(str(x)).name for x in scan["__top_level__"]] == ["top.npz"]


def _dry_store(sc: Path, name="hwsd-dry") -> Path:
    d = sc / name
    bu.tiny_artifacts(d / UTCDIR / "artifacts", 16, 8)
    _hist(d / UTCDIR / "stages/S3/DRYHIST_cal_b0.npz", 16)
    ck = bu.fake_artifact(d / UTCDIR / "artifacts", "Checkpoint", "ab01", ("state.pt",))
    bu.array_npz(ck / "payload.npz", w=np.zeros((3, 2)))
    bu.array_npz(d / UTCDIR / "registry/K-REG1_digests.npz",
                 digests=np.array(["a" * 64], "<U64"), seq_ids=np.array([1], np.int64))
    (d / UTCDIR / "registry/runs/K-REG1").mkdir(parents=True)
    np.save(d / UTCDIR / "registry/runs/K-REG1/run_00000.npy", np.zeros((4, 32), np.uint8))
    return d


def _recs(sc: Path, name: str) -> dict:
    return {k.replace("\\", "/"): v for k, v in dr.scratch_scan_d(sc)[name].items()}


def test_dry_class_d(tmp_path):
    sc = tmp_path / "scratch"
    d = _dry_store(sc)
    recs = _recs(sc, "hwsd-dry")
    got = {rel: dr.dry_class_d(d, rel, rec) for rel, rec in recs.items()}
    for rel, cls in got.items():
        if "/ObservationSet/" in rel or "DRYHIST" in rel:
            assert cls == "R5", rel
        elif "/Checkpoint/" in rel:
            assert cls == "CHECKPOINT", rel
        elif "/registry/" in rel:
            assert cls == "REGISTRY_FIXTURE", rel
    assert any("/ObservationSet/" in r and r.endswith("payload.npz") for r in got)
    assert any(r.endswith("meta.json") for r in got)
    rec = {"class": "history", "shape": [16, 32]}
    for bad in (f"{UTCDIR}/stages/S4/X.npz", "DRD1/2026-11-01/stages/S3/DRYHIST_cal_b0.npz",
                "XYZ1/20261101T120000Z/stages/S3/DRYHIST_cal_b0.npz",
                f"{UTCDIR}/stages/S3/HIST_cal_b0.npz", "stages/S3/DRYHIST_cal_b0.npz"):
        assert dr.dry_class_d(d, bad, rec) is None, bad
    extra = d / UTCDIR / "registry/K-REG1_digests.npz"
    extra.unlink()
    bu.array_npz(extra, digests=np.array(["a" * 64], "<U64"), seq_ids=np.array([1]), x=np.zeros(1))
    rel = f"{UTCDIR}/registry/K-REG1_digests.npz"
    assert dr.dry_class_d(d, rel, _recs(sc, "hwsd-dry").get(rel, rec)) is None


def _check(sc, **kw):
    return dr.scratch_check_d(sc, **kw)


def test_scratch_check_d_clean_and_fail_closed(tmp_path):
    sc = tmp_path / "scratch"
    _dry_store(sc)
    bu.array_npz(sc / "test_hwsd-0197/pytest/x.npz", canon32=np.zeros((5000, 32), np.uint8))
    r = _check(sc, readers_ok={"R5"})
    assert r["status"] == PASS, r["other"]
    assert _check(sc, readers_ok=set())["status"] == INC  # an R5 file needs R5 PASS
    _hist(sc / "hwsd-dry" / UTCDIR / "stages/S4/unknown.npz")
    assert _check(sc, readers_ok={"R5"})["status"] == INC


@pytest.mark.parametrize("plant", ["newdir/h.npz", "hwsd-kd-0300/x.npz", "top.npz",
                                   "hwsc-job-0181/a.npz", "hwsd-dry-0202/stray/x.npz"])
def test_scratch_check_d_incomplete(tmp_path, plant):
    sc = tmp_path / "scratch"
    _hist(sc / plant)
    r = _check(sc, readers_ok={"R5", "R10"})
    assert r["status"] == INC and r["other"]


def test_scratch_check_d_to_freeze_row_without_files(tmp_path):
    sc = tmp_path / "scratch"
    (sc / "hwsc-job-0184").mkdir(parents=True)
    # TO_FREEZE review erratum: the contract row is now EXCLUSION, so a TO_FREEZE row is planted
    assert _check(sc, readers_ok={"R5"})["status"] == PASS
    t = dc.scratch_table()
    t["hwsc-job-0184"] = dict(t["hwsc-job-0184"], decision="TO_FREEZE", frozen_files="TO_FREEZE")
    assert _check(sc, table=t, readers_ok={"R5"})["status"] == INC  # "row not frozen"


def test_scratch_check_d_hwsu_needs_r10(tmp_path):
    sc = tmp_path / "scratch"
    _hist(sc / "hwsu-job-0200/x.npz")
    assert _check(sc, readers_ok={"R5"})["status"] == INC
    assert _check(sc, readers_ok={"R5", "R10"})["status"] == PASS


def test_scratch_check_d_blinded_rows(tmp_path):
    sc = tmp_path / "scratch"
    bu.junk(sc / "hwsc-job-0181/a.npz")
    t = dc.scratch_table()
    t["hwsc-job-0181"] = {"decision": "EXCLUSION", "frozen_files": {"a.npz": "blinded_array"},
                          "reason": "test"}
    assert _check(sc, table=t, readers_ok=set())["status"] == PASS
    t["hwsc-job-0181"] = {"decision": "EXCLUSION", "frozen_files": {}, "reason": "test"}
    assert _check(sc, table=t, readers_ok=set())["status"] == INC


def _root_tree(tmp_path) -> Path:
    root = tmp_path / "root"
    _hist(root / "hwsd-store/stages/S3/HIST_cal_b0.npz")
    (root / "quiet").mkdir(parents=True)
    return root


def test_inventory_d(tmp_path):
    root = _root_tree(tmp_path)
    t = {"hwsd-store": {"decision": "OWN"}, "quiet": {"decision": "EXCLUSION", "reason": "empty"},
         "hwsu-store": {"decision": "READER_IF_PRESENT", "readers": ["R10"]}}
    r = dr.inventory_d(root, readers={}, table=t)
    assert r["status"] == PASS, r["violations"]
    assert "hwsd-store" not in r["inv"]
    _hist(root / "unlisted/h.npz")
    r = dr.inventory_d(root, readers={}, table=t)
    assert r["status"] != PASS and r["violations"]
    (root / "unlisted/h.npz").unlink()
    t["quiet"] = {"decision": "TO_FREEZE"}
    assert dr.inventory_d(root, readers={}, table=t)["status"] != PASS


# -------------------------------------------------------------------- build_d


def _src(digests=(), lineage=False, other=False):
    s = hwsc_registry._new()
    s["digests"] = set(digests)
    if other:
        s["other"].append({"path": "x", "reason": "planted"})
    return hwsc_registry._close(s, lineage=lineage)


def _sources(own=None, sup=PASS):
    s = dict(hwsc_dry.stub_sources())
    s["own"] = lambda *a, **k: own or _src(digests=["c" * 64])
    s["dry"] = lambda *a, **k: _src()
    s["scratch"] = lambda *a, **k: dict(_src(), scan_counts={})
    s["inventory"] = lambda *a, **k: {"status": PASS, "inv": {}, "classes": {}, "unlisted": [],
                                      "violations": []}
    s["superset"] = lambda *a, **k: {"status": sup, "n_kreg2": 1, "missing": int(sup != PASS),
                                     "n_test": 1, "missing_test": 0}
    return s


def _syn(tmp_path):
    (tmp_path / "syn/root").mkdir(parents=True)
    (tmp_path / "syn/scratch").mkdir(parents=True)
    return tmp_path / "syn/root", tmp_path / "syn/scratch"


@pytest.mark.parametrize("own,sup,want", [
    (None, PASS, PASS), ("lineage", PASS, LIN), ("other", PASS, INC), (None, INC, INC),
    ("lineage", INC, LIN)])
def test_build_d_wrapper_and_precedence(tmp_path, own, sup, want):
    root, scratch = _syn(tmp_path)
    o = {None: None, "lineage": _src(lineage=True), "other": _src(other=True)}[own]
    reg_dir = tmp_path / "hwsd-store" / "registry"
    w = dr.build_d(reg_dir, root, scratch, handoff={"store_inventory": {}}, sources=_sources(o, sup))
    on_disk = (reg_dir / "K-REG-D.json")
    assert on_disk.exists() and (reg_dir / "K-REG1.json").exists()
    assert (reg_dir / "K-REG1_digests.npz").exists()
    assert w["status"] == want
    assert w["registry_version"] == "hwsd-reg-v1" and w["inner_version"] == "K-REG1"
    assert w["protocol_sha256"] == dc.PROTOCOL_SHA256
    assert w["inner_manifest_sha256"] == bu.sha(reg_dir / "K-REG1.json")
    assert w["inner_digest_file_sha256"] == bu.sha(reg_dir / "K-REG1_digests.npz")
    assert w["known_label"] == dc.CONTRACT["registry"]["known_label"]
    assert w["superset"]["status"] == sup
    if want == PASS:
        reg = dr.load_d(tmp_path / "hwsd-store")
        assert bool(reg.contains(np.array(["c" * 64], "<U64"))[0])
    else:
        with pytest.raises(bu.C1GateFailure) as e:
            dr.load_d(tmp_path / "hwsd-store")
        assert bu.status_of(e.value) == want
    with pytest.raises(FileExistsError):
        dr.build_d(reg_dir, root, scratch, handoff={"store_inventory": {}}, sources=_sources())


def test_build_d_refusals_and_load_d_lineage(tmp_path):
    root, scratch = _syn(tmp_path)
    with pytest.raises(ValueError):
        dr.build_d(tmp_path / "hwsd-store" / "reg", root, scratch, handoff={}, sources=_sources())
    with pytest.raises(bu.C1GateFailure) as e:
        dr.load_d(tmp_path / "absent-store")
    assert bu.status_of(e.value) == LIN
    reg_dir = tmp_path / "hwsd-store" / "registry"
    dr.build_d(reg_dir, root, scratch, handoff={"store_inventory": {}}, sources=_sources())
    m = reg_dir / "K-REG1.json"
    m.write_text(m.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(bu.C1GateFailure) as e:
        dr.load_d(tmp_path / "hwsd-store")
    assert bu.status_of(e.value) == LIN


@pytest.mark.parametrize("r9,r10,want", [(PASS, PASS, PASS), (PASS, INC, INC), (LIN, PASS, LIN),
                                         (INC, PASS, INC)])
def test_build_d_composite_own_and_reader_tags(tmp_path, monkeypatch, r9, r10, want):
    root, scratch = _syn(tmp_path)
    seen = {}
    monkeypatch.setattr(drd, "source_hwsc", lambda *a, **k: _src(["d" * 64], r9 == LIN, r9 == INC))
    monkeypatch.setattr(drd, "source_hwsu", lambda *a, **k: _src((), r10 == LIN, r10 == INC))

    def scr(*a, **k):
        seen["readers_ok"] = set(k.get("readers_ok") or (a[-1] if len(a) > 1 else ()))
        return dict(_src(), scan_counts={})

    def inv(*a, **k):
        seen["readers"] = dict(k.get("readers") or a[1])
        return {"status": PASS, "inv": {}, "classes": {}, "unlisted": [], "violations": []}

    monkeypatch.setattr(dr, "scratch_check_d", scr)
    monkeypatch.setattr(dr, "inventory_d", inv)
    dry_calls = []
    for n in ("hwsd-dry-0201", "hwsd-dry", "hwsc-dry-0177"):
        (scratch / n).mkdir()
    monkeypatch.setattr(hwsc_registry, "source_dry",
                        lambda *a, **k: dry_calls.append(k.get("paths", a[0] if a else None)) or _src())
    monkeypatch.setattr(drd, "superset_check", lambda *a, **k: {"status": PASS, "n_kreg2": 0,
                                                                "missing": 0, "n_test": 0,
                                                                "missing_test": 0})
    s = dict(hwsc_dry.stub_sources())
    for k in ("own", "dry", "scratch", "inventory"):
        s.pop(k, None)
    w = dr.build_d(tmp_path / "hwsd-store" / "registry", root, scratch,
                   handoff={"store_inventory": {}}, sources=s)
    assert w["status"] == want
    assert w["r9"]["status"] == r9 and w["r10"]["status"] == r10
    assert ("R10" in seen["readers_ok"]) == (r10 == PASS)
    assert (seen["readers"].get("hwsc-store") == ["R9"]) == (r9 == PASS)
    assert (seen["readers"].get("hwsu-store") == ["R10"]) == (r10 == PASS)
    # R5': source_dry() (stage-C default paths) and source_dry(paths=<every hwsd-dry* folder>)
    assert None in dry_calls
    want = [bu.norm(scratch / "hwsd-dry"), bu.norm(scratch / "hwsd-dry-0201")]
    assert [[bu.norm(p) for p in c] for c in dry_calls if c is not None] == [want]
