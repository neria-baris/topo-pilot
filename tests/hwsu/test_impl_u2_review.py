"""Implementer regression tests for the real-tree path review R-0223-10 (items 1, 2, 4, 5)."""

from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest

TOOLS = Path(__file__).resolve().parents[2] / "tools" / "hwsu"
for p in (TOOLS, TOOLS / "u2"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def mod(name):
    importlib.import_module("u2")
    return importlib.import_module(name)


def _table(path, seed=1, n=8):
    mod("hwsu_dry2d")._table(path, n=n, seed=seed)


# ----------------------------------------------------------------------------- item 1
def test_fixture_prefixes_from_contract():
    ureg = mod("hwsu_registry")
    assert set(ureg.fixture_prefixes()) == {"test_hwsg-", "hwsg-dry"}
    rows = mod("hwsu_config").CONTRACT["registry_u2"]["scratch_u2"]["rows"]
    assert all(r["decision"] == "EXCLUSION" and r["rule"] == "J4 fixture" for r in rows.values())


@pytest.mark.parametrize("name,flagged", [("test_hwsg-0224", False), ("hwsg-dry-0230", False),
                                          ("otherstudy-0001", True)])
def test_scratch_matcher_excludes_other_study_fixtures(tmp_path, name, flagged):
    ureg = mod("hwsu_registry")
    _table(tmp_path / name / "pytest-r9" / "t0" / "s-store" / "stages" / "A" / "HIST_a.npz")
    res = ureg._scratch_u(tmp_path, set())
    assert bool([o for o in res["other"] if str(o["path"]).startswith(name)]) is flagged


# ----------------------------------------------------------------------------- item 2
def _stage_files(out):
    for rel in ("stages/E1/PAIR_x.npz", "registry/K-REG1_digests.npz", "stages/E2/BOOT_x.npz"):
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        np.savez(out / rel, x=np.arange(3))
    (out / "registry" / "K-REG1.json").write_text("{}", encoding="utf-8")
    _table(out / "stages" / "E1" / "DRYHIST_val_a1_b0.npz")


def test_archive_previous_moves_same_stage_only(tmp_path):
    drv = mod("hwsu_driver")
    _stage_files(tmp_path)
    dest = drv.archive_previous(tmp_path, "E1", "J")
    assert dest == tmp_path / "superseded" / "J-a1"
    assert not (tmp_path / "registry" / "K-REG1.json").exists()
    assert (tmp_path / "stages" / "E2" / "BOOT_x.npz").is_file()  # other stage untouched
    sums = (dest / "SHA256SUMS").read_text(encoding="utf-8")
    assert "registry/K-REG1.json" in sums and "stages/E1/PAIR_x.npz" in sums
    assert drv.archive_previous(tmp_path, "E1", "J") is None  # nothing left to archive


def test_second_archive_gets_a2_and_obligation_lists_archived_arrays(tmp_path):
    drv, rs = mod("hwsu_driver"), mod("hwsu_regsrc")
    _stage_files(tmp_path)
    drv.archive_previous(tmp_path, "E1", "J")
    np.savez(tmp_path / "stages" / "E1" / "PAIR_y.npz", x=np.arange(2))
    assert drv.archive_previous(tmp_path, "E1", "J") == tmp_path / "superseded" / "J-a2"
    ob = drv.write_obligation_u2(tmp_path, "REGISTRY_OBLIGATION_E1-a1.json", "E1", "t", dry=True,
                                 attempt=1)
    rels = {e["relpath"] for e in json.loads(ob.read_text(encoding="utf-8"))["files"]}
    assert "superseded/J-a1/stages/E1/DRYHIST_val_a1_b0.npz" in rels
    assert rs.read_obligation_u2(tmp_path)["status"] == "PASS"


def test_own_reader_follows_archived_listed_table(tmp_path):
    drv, rs, ur = mod("hwsu_driver"), mod("hwsu_regsrc"), mod("hwsu_records")
    rel = "stages/E1/DRYHIST_val_a1_b0.npz"
    _table(tmp_path / rel)
    ur.complete_stage(tmp_path, "E1_S3", [rel])
    drv.archive_previous(tmp_path, "E1", "J")
    out = rs.source_own_u(tmp_path, [rel])
    assert out["status"] == "PASS" and len(out["digests"]) == 8


def test_unrecorded_compares_sha_not_only_name(tmp_path):
    drv, ur = mod("hwsu_driver"), mod("hwsu_records")
    f = tmp_path / "stages" / "E1" / "R.json"
    f.parent.mkdir(parents=True)
    f.write_text("a", encoding="utf-8")
    ur.complete_stage(tmp_path, "E1", [f])
    assert drv._unrecorded(tmp_path, ["stages/E1"]) == []
    f.write_text("b", encoding="utf-8")  # same name, new content (a rerun's output)
    assert drv._unrecorded(tmp_path, ["stages/E1"]) == ["stages/E1/R.json"]


# ----------------------------------------------------------------------------- items 4, 5
def test_bind_stage_uses_the_stage_when_phase1_knows_it():
    drv = mod("hwsu_driver")
    assert drv.bind_stage("OF") == "OF"
    assert drv.bind_stage("E1") == "OF"  # not in the phase-1 table: the phase-2 cap replaces it
    caps = mod("hwsu_config").CONTRACT["resources"]["memory_cap_bytes"]
    assert all(drv.bind_stage(s) == s for s in caps)


@pytest.mark.parametrize("name", ["hwsu_driver", "hwsu_gates", "hwsu_known"])
def test_handoff_is_decoded_with_a_bom_tolerant_codec(name):
    src = (TOOLS / "u2" / f"{name}.py").read_text(encoding="utf-8")
    lines = [ln for ln in src.splitlines() if "HANDOFF_PATH" in ln and "decode(" in ln]
    assert lines and all('decode("utf-8-sig")' in ln for ln in lines)
    assert not re.search(r'HANDOFF_PATH\)\.decode\("utf-8"\)', src)


# ----------------------------------------------------------------------------- R-0228-1
def test_s0_allowlist_admits_the_implementer_phase2_tests():
    known = mod("hwsu_known")
    assert known._allowed_s0("A", "tests/hwsu/test_impl_u2_review.py")
    assert known._allowed_s0("A", "tests/hwsu/test_impl_u2_mirror.py")
    assert not known._allowed_s0("A", "tests/hwsu/test_impl_other.py")
    assert not known._allowed_s0("M", "tests/hwsu/test_impl_u2_review.py")
    allow = mod("hwsu_config").CONTRACT["s0_u2"]["allow"]["A"]
    assert "tests/hwsu/test_impl_u2_*.py" in allow
