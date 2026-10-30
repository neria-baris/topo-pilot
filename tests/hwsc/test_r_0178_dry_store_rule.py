"""Coordinator-commissioned regression test for defect D-0178-1 (API.md §22): the hwsc-dry type
rule of the R6 scratch check. A synthetic dry store under tmp_path holds one file of each allowed
class; scratch_check passes it, and an unexpected array fails closed. Only hwsc-dry* folders are
ruled by type; the same unexpected array in another folder still needs the frozen table."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_config as cc  # noqa: E402,F401
import hwsc_drystore  # noqa: E402
import hwsc_registry as cr  # noqa: E402
import hwsc_scratch  # noqa: E402
import numpy as np  # noqa: E402

UTC = "20261029T120000Z"
OK = {"R5", "c2scratch"}


def _meta(d: Path, art_type: str, parents=()):
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps({"artifact_type": art_type,
                                             "parent_ids": list(parents)}), encoding="utf-8")


def _dry_store(root: Path) -> Path:
    store = root / "hwsc-dry-9999"
    c1 = store / "DRC1" / UTC
    arts = c1 / "artifacts"
    _meta(arts / "EmissionSpec" / "e1", "EmissionSpec")
    _meta(arts / "ObservationSet" / "o1", "ObservationSet", ["t1", "e1"])
    np.savez(arts / "ObservationSet" / "o1" / "payload.npz",
             tokens=np.zeros((4, 33), np.uint8))
    _meta(arts / "Checkpoint" / "k1", "Checkpoint")
    (arts / "Checkpoint" / "k1" / "state.pt").write_bytes(b"\x00synthetic")
    (c1 / "stages" / "S3").mkdir(parents=True)
    np.savez(c1 / "stages" / "S3" / "DRYHIST_cal_b0.npz", canon32=np.zeros((8, 32), np.uint8),
             seq_ids=np.arange(8))
    (c1 / "registry").mkdir()
    np.savez(c1 / "registry" / "K-REG1_digests.npz", digests=np.array(["ab" * 32], "<U64"),
             seq_ids=np.arange(1))
    c9 = store / "DRC9" / UTC
    (c9 / "scale").mkdir(parents=True)
    np.save(c9 / "scale" / "run_00000.npy", np.zeros((3, 32), np.uint8))
    hist = c9 / "syn" / "c2nd-store" / "hist"
    hist.mkdir(parents=True)
    col = np.array(["cd" * 32], "<U64")
    np.savez(hist / "HIST_fit_b0.npz", digest_H=col, digest_Hp=col, digest_Hm=col)
    (c9 / "syn" / "c2nd-store" / "stray.npz").write_bytes(b"x")
    c11 = store / "DRC11" / UTC / "root" / "hwsb-store" / "stages" / "EVAL"
    c11.mkdir(parents=True)
    (c11 / "a.npz").write_bytes(b"blinded")
    return store


def _check(scratch, readers=OK):
    return cr.scratch_check(scratch, readers_ok=readers)


def test_every_allowed_class_passes(tmp_path):
    store = _dry_store(tmp_path)
    scan = hwsc_scratch.scratch_scan(tmp_path)[store.name]
    classes = {rel: hwsc_drystore.dry_class(store, rel, r) for rel, r in scan.items()}
    assert None not in classes.values(), classes
    assert {"R5", "c2scratch", "CHECKPOINT", "REGISTRY_FIXTURE", "PLANTED_FIXTURE"} <= set(
        classes.values())
    r = _check(tmp_path)
    assert r["status"] == "PASS", r["other"]


def test_unexpected_array_fails_closed(tmp_path):
    store = _dry_store(tmp_path)
    np.savez(store / "DRC1" / UTC / "surprise.npz", canon32=np.zeros((2, 32), np.uint8))
    r = _check(tmp_path)
    assert r["status"] != "PASS"
    assert any("surprise.npz" in o["path"] for o in r["other"])


def test_registry_npz_with_extra_key_fails_closed(tmp_path):
    store = _dry_store(tmp_path)
    f = store / "DRC1" / UTC / "registry" / "K-REG2_digests.npz"
    np.savez(f, digests=np.array(["ab" * 32], "<U64"), seq_ids=np.arange(1),
             canon32=np.zeros((1, 32), np.uint8))
    assert _check(tmp_path)["status"] != "PASS"


def test_changed_planted_fixture_fails_closed(tmp_path):
    store = _dry_store(tmp_path)
    (store / "DRC9" / UTC / "syn" / "c2nd-store" / "stray.npz").write_bytes(b"y")
    assert _check(tmp_path)["status"] != "PASS"


def test_reader_classes_need_their_reader(tmp_path):
    _dry_store(tmp_path)
    r = _check(tmp_path, readers={"c2scratch"})
    assert r["status"] != "PASS"
    assert any("reader R5 not PASS" in o["reason"] for o in r["other"])


def test_rule_applies_only_to_hwsc_dry_folders(tmp_path):
    other = tmp_path / "somefolder"
    other.mkdir()
    np.savez(other / "x.npz", canon32=np.zeros((2, 32), np.uint8))
    assert not hwsc_drystore.is_dry_store("somefolder")
    assert _check(tmp_path)["status"] != "PASS"
