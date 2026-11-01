"""Author B: R9, the stage-C layout reader, on a synthetic stage-C-like store (J1; DRD8, DRD9)."""

from __future__ import annotations  # noqa: I001

import json
import shutil
import sys
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_readers as drd  # noqa: E402
import test_b_util as bu  # noqa: E402

import c2_registry  # noqa: E402
import hwsb_registry  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

PASS, INC, LIN = "PASS", "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
IDENT = "FAIL_TECHNICAL/IDENTITY"
CK = "artifacts/Checkpoint/c0ffee0000000042"
B_FILES = ["stages/S3/HIST_lgate_b0.npz", "stages/S3/HIST_cal_b0.npz", "stages/S3/HIST_val_b0.npz",
           "stages/S7/HIST_test_b0.npz"]


def _build(store: Path) -> dict:
    art = store / "artifacts"
    info = bu.tiny_artifacts(art)
    bu.fake_artifact(art, "Checkpoint", CK.rsplit("/", 1)[1], ("payload.npz", "state.pt"))
    em = sorted((art / "EmissionSpec").iterdir())[0]
    shutil.copytree(em, store / "superseded/0184-a1/artifacts/EmissionSpec" / em.name)
    sup = bu.hist_table("cal", 520, 21, 3_000_000)
    bu.save_table(store / "superseded/0184-a1/stages/S3/HIST_cal_b0.npz", sup)
    tables = {}
    for i, rel in enumerate(B_FILES):
        split = rel.split("_")[1]
        tables[rel] = bu.hist_table(split, 520, 100 + i, 4_000_000 + 1000 * i)
        bu.save_table(store / rel, tables[rel])
    bu.stage_complete(store, "S3", B_FILES[:3])
    bu.stage_complete(store, "S7", B_FILES[3:])
    for rel in ("stages/S4/ORACLE_cal.npz", "stages/S4/ORACLE_val.npz", "stages/S4a/CHART_620301.npz",
                "stages/S4a/INIT_CHART_620301.npz", "stages/S4a/DECODER_620301.npz",
                "stages/S4a/ACTS_cal_b0.npz", "registry/runs/K-REG1/run_00000.npz"):
        bu.array_npz(store / rel)
    digests = set()
    for t in list(tables.values()) + [sup]:
        digests |= set(np.asarray(t["digest"]).astype(str).tolist())
    os_d = bu.expected_os_digests(art)
    kreg2 = bu.array_npz(store / "registry/K-REG2_digests.npz",
                         digests=np.array(sorted(digests | os_d), "<U64"))
    bu.write_json(store / "registry/K-REG2.json", {"digest_file_sha256": bu.sha(kreg2)})
    bu.junk(store / "logs/superseded-reg2-0192a1/K-REG2_digests.npz")
    (store / "logs/meter.log").write_text("620413\n", encoding="utf-8")
    bu.junk(store / "sealed/SEALED.npz")
    bu.write_json(store / "stages/TRAIN/620301/TRAIN_RECORD.json",
                  {"status": "COMPLETE", "run_key": ["hwsc-v1"], "checkpoint_ids": {},
                   "checksums": {}, "process_ids": {}, "dev_ce": [1.5, 1.2]})
    inv = hwsb_registry.history_inventory(store)
    obs = bu.write_json(store / "stages/TRAIN/OBS_INVENTORY.json", inv)
    bu.write_json(store / "RELEASE_A.json", {"obs_inventory_sha256": bu.sha(obs)})
    bu.stage_complete(store, "TRAIN_INVENTORY", ["stages/TRAIN/OBS_INVENTORY.json"])
    seq = set()
    for t in list(tables.values()) + [sup]:
        seq |= set(t["seq_ids"].tolist())
    return {"digests": digests | os_d, "seq_ids": seq, "tables": tables}


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    store = tmp_path_factory.mktemp("r9") / "hwsc-store"
    return store, _build(store)


@pytest.fixture
def store(base, tmp_path, monkeypatch):
    src, info = base
    dst = tmp_path / "hwsc-store"
    shutil.copytree(src, dst)
    _bind_obs(dst, monkeypatch)
    return dst, info


def _bind_obs(store: Path, monkeypatch):
    """dc.read_obs_inventory bound to the fixture's sha (TEST_PLAN B r9)."""
    fx = bu.sha(store / "stages/TRAIN/OBS_INVENTORY.json")
    monkeypatch.setitem(dc.CONTRACT["identity"]["rows"]["obs_inventory"], "sha256", fx)
    orig = dc.read_obs_inventory

    def bound(store=dc.HWSC_STORE, expected_sha256=None):
        return orig(store, expected_sha256 or fx)

    monkeypatch.setattr(dc, "read_obs_inventory", bound)


def _never_opened(spy, store: Path):
    assert spy.opened_under(store / CK / "payload.npz") == []
    assert spy.opened_under(store / CK / "state.pt") == []
    assert spy.opened_under(store / "sealed") == []
    assert spy.opened_under(store / "logs") == []
    train = [p for p in spy.opened_under(store / "stages/TRAIN")
             if not p.endswith("stages/train/obs_inventory.json")]
    assert train == []


def test_source_hwsc_passes_on_the_layout(store, monkeypatch):
    s, info = store
    spy = bu.OpenSpy().install(monkeypatch)
    r = drd.source_hwsc(s)
    assert r["status"] == PASS, r["other"]
    assert info["digests"] <= r["digests"]
    assert info["seq_ids"] <= r["seq_ids"]
    _never_opened(spy, s)
    nh = " ".join(str(e["path"]).replace("\\", "/") for e in r["non_history"])
    for frag in ("registry/runs/K-REG1/run_00000.npz", "stages/S4a/CHART_620301.npz",
                 "stages/S4/ORACLE_val.npz", f"{CK}/state.pt",
                 "superseded/0184-a1/artifacts/EmissionSpec", "logs/superseded-reg2-0192a1"):
        assert frag in nh, frag


@pytest.mark.parametrize("rel", ["tmp/unknown.npz", "stages/S5/X.npy", "w.pt",
                                 "logs/stray.npz", "stages/S4/ORACLE_test.npz"])
def test_unknown_array_is_incomplete(store, rel, monkeypatch):
    s, _ = store
    bu.junk(s / rel)
    spy = bu.OpenSpy().install(monkeypatch)
    r = drd.source_hwsc(s)
    assert r["status"] == INC and r["other"]
    if rel.startswith("logs/"):
        assert spy.opened_under(s / rel) == []  # names only under logs/


def test_array_in_train_is_incomplete_and_unopened(store, monkeypatch):
    s, _ = store
    bu.junk(s / "stages/TRAIN/620301/weights.npz")
    spy = bu.OpenSpy().install(monkeypatch)
    r = drd.source_hwsc(s)
    assert r["status"] == INC
    _never_opened(spy, s)


def test_hist_sha_differing_from_stage_complete_is_lineage(store):
    s, _ = store
    line = {"event": "STAGE_COMPLETE", "stage": "S3", "utc": bu.UTC,
            "files": {"stages/S3/HIST_cal_b0.npz": "0" * 64}}
    with (s / "STAGES.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")
    assert drd.source_hwsc(s)["status"] == LIN


def test_tampered_digest_column_is_incomplete(store):
    s, info = store
    t = dict(info["tables"]["stages/S3/HIST_val_b0.npz"])
    t["digest"] = np.asarray(t["digest"]).copy()
    t["digest"][0] = "f" * 64
    (s / "stages/S3/HIST_val_b0.npz").unlink()
    bu.save_table(s / "stages/S3/HIST_val_b0.npz", t)
    bu.stage_complete(s, "S3", ["stages/S3/HIST_val_b0.npz"])  # lineage still holds
    r = drd.source_hwsc(s)
    assert r["status"] == INC and r["other"]


def test_obs_inventory_not_equal_to_release_a_is_lineage(store):
    s, _ = store
    bu.write_json(s / "RELEASE_A.json", {"obs_inventory_sha256": "1" * 64})
    assert drd.source_hwsc(s)["status"] == LIN


def test_artifact_meta_mismatch_is_incomplete(store):
    s, _ = store
    bu.write_json(s / CK / "meta.json", {"artifact_type": "WorldSpec"})
    assert drd.source_hwsc(s)["status"] == INC


def test_obs_inventory_extra_file_fails_closed(store):
    s, _ = store
    bu.junk(s / "superseded/0184-a1/artifacts/EmissionSpec/zz/extra.json")
    assert drd.source_hwsc(s)["status"] != PASS


# ------------------------------------------------- exempt readers (DRD9) and table reader


def test_read_train_record_whitelist(tmp_path):
    s = tmp_path / "hwsc-store"
    rec = {"status": "COMPLETE", "run_key": ["hwsc-v1", "K", 620301], "checkpoint_ids": {"0": "a"},
           "checksums": {"0": "b"}, "process_ids": {"620301": "c"}, "dev_ce": [2.0, 1.0],
           "train_loss": [3.0]}
    p = bu.write_json(s / "stages/TRAIN/620301/TRAIN_RECORD.json", rec)
    sha, got = dc.read_train_record(620301, s)
    assert sha == bu.sha(p)
    assert got == {k: rec[k] for k in ("status", "run_key", "checkpoint_ids", "checksums", "process_ids")}
    assert dc.TRAIN_WHITELIST == ("status", "run_key", "checkpoint_ids", "checksums", "process_ids")
    p.write_text(json.dumps({k: v for k, v in rec.items() if k != "checksums"}), encoding="utf-8")
    with pytest.raises(bu.C1GateFailure) as e:
        dc.read_train_record(620301, s)
    assert bu.status_of(e.value) == IDENT and "dev_ce" not in str(e.value.reason)
    p.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(bu.C1GateFailure) as e:
        dc.read_train_record("620301", s)
    assert bu.status_of(e.value) == IDENT


def test_read_obs_inventory(tmp_path):
    s = tmp_path / "hwsc-store"
    inv = {"artifacts/ObservationSet/ab/payload.npz": "a" * 64}
    p = bu.write_json(s / "stages/TRAIN/OBS_INVENTORY.json", inv)
    assert dc.read_obs_inventory(s, bu.sha(p)) == inv
    with pytest.raises(bu.C1GateFailure) as e:
        dc.read_obs_inventory(s, "0" * 64)
    assert bu.status_of(e.value) == IDENT
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(bu.C1GateFailure) as e:  # sha checked before parsing
        dc.read_obs_inventory(s, "0" * 64)
    assert bu.status_of(e.value) == IDENT
    for bad in ({"a": "A" * 64}, {"a": {"b": "c"}}, ["x"], {"a": "a" * 63}):
        p.write_text(json.dumps(bad), encoding="utf-8")
        with pytest.raises(bu.C1GateFailure) as e:
            dc.read_obs_inventory(s, bu.sha(p))
        assert bu.status_of(e.value) == IDENT
    assert dc.CONTRACT["identity"]["rows"]["obs_inventory"]["sha256"].startswith("bd385a96")


def test_read_k4b_table(tmp_path):
    t = bu.hist_table("cal", 520, 5, 10)
    p = bu.save_table(tmp_path / "HIST_cal_b0.npz", t)
    r = drd.read_k4b_table(p, bu.sha(p))
    assert r["n"] == 520 and r["seq_ids"] == set(range(10, 530))
    assert r["digests"] == set(np.asarray(t["digest"]).astype(str).tolist())
    assert drd.read_k4b_table(p)["n"] == 520
    with pytest.raises(ValueError):
        drd.read_k4b_table(p, "0" * 64)
    bad = dict(t, digest=np.asarray(t["digest"]).copy())
    bad["digest"][3] = "e" * 64
    with pytest.raises(ValueError):
        drd.read_k4b_table(bu.save_table(tmp_path / "bad.npz", bad))
    with pytest.raises(ValueError):
        drd.read_k4b_table(bu.array_npz(tmp_path / "nokeys.npz", canon32=t["canon32"]))
    wide = {k: v for k, v in t.items() if isinstance(v, np.ndarray)}
    wide["canon32"] = np.zeros((520, 33), np.uint8)
    with pytest.raises(ValueError):
        drd.read_k4b_table(bu.array_npz(tmp_path / "wide.npz", **wide))


def test_stage_complete_sha(tmp_path):
    s = tmp_path / "st"
    for rel in ("a/x.json", "b/y.json"):
        bu.write_json(s / rel, {"r": rel})
    bu.stage_complete(s, "A", ["a/x.json"])
    bu.stage_complete(s, "B", ["a/x.json", "b/y.json"])
    j = s / "STAGES.jsonl"
    assert drd.stage_complete_sha(j, "a/x.json") == bu.sha(s / "a/x.json")
    with j.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"event": "BEGIN", "stage": "C", "utc": bu.UTC}) + "\n")
        f.write(json.dumps({"event": "STAGE_COMPLETE", "stage": "C", "utc": bu.UTC,
                            "files": {"a/x.json": "9" * 64}}) + "\n")
    assert drd.stage_complete_sha(j, "a/x.json") == "9" * 64  # latest event wins
    assert drd.stage_complete_sha(j, "a/x.json", "A") == bu.sha(s / "a/x.json")
    assert drd.stage_complete_sha(j, "b/y.json", "A") is None
    assert drd.stage_complete_sha(j, "c/z.json") is None


class _X6:
    def contains(self, d):
        return np.zeros(len(d), bool)


def _reg(digests) -> c2_registry.Registry:
    return c2_registry.Registry(set(digests), _X6(), {}, ["sealed_d2a"], {}, seq_ids=set())


def test_superset_check(store):
    s, info = store
    r = drd.superset_check(_reg(info["digests"]), s)
    assert r["status"] == PASS and r["missing"] == 0 and r["missing_test"] == 0
    assert r["n_kreg2"] == len(info["digests"]) and r["n_test"] == 520
    test_d = set(np.asarray(info["tables"]["stages/S7/HIST_test_b0.npz"]["digest"]).astype(str))
    one = sorted(info["digests"] - test_d)[0]
    r = drd.superset_check(_reg(info["digests"] - {one}), s)
    assert r["status"] == INC and r["missing"] == 1 and r["missing_test"] == 0
    t0 = sorted(test_d)[0]
    r = drd.superset_check(_reg(info["digests"] - {t0}), s)
    assert r["status"] == INC and r["missing_test"] == 1
    bu.write_json(s / "registry/K-REG2.json", {"digest_file_sha256": "0" * 64})
    assert drd.superset_check(_reg(info["digests"]), s)["status"] == LIN


def test_os_digests_independent(store):
    s, _ = store
    pay = bu.os_payloads(s / "artifacts")
    got = set()
    for p in pay:
        got |= set(drd.os_digests(p))
    assert got == bu.expected_os_digests(s / "artifacts")
