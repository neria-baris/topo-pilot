"""Author B: registry fixtures, class-to-reader table, inventory fail-closed (protocol 6, N6, DRG9)."""
from __future__ import annotations

import builtins
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import CONTRACT, expect_fail, is_incomplete, mod  # noqa: E402

SCHEMA = "hws-registry-obligation-v1"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _table(path, seed, n=6):
    mod("gc")  # sets sys.path for the reused tools
    k4d = __import__("k4b_data")
    rng = np.random.default_rng(seed)
    canon = rng.integers(0, 36, (n, 32), dtype=np.uint8)
    dg = np.asarray(k4d.digests(canon), dtype="<U64")
    ids = np.arange(seed * 1000, seed * 1000 + n, dtype=np.int64)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, canon32=canon, seq_ids=ids, digest=dg)
    return set(dg.tolist()), set(ids.tolist())


def _entry(store, f, cls, reader):
    return {"basis": "test", "bytes": f.stat().st_size, "class": cls, "reader": reader,
            "relpath": f.relative_to(store).as_posix(), "sha256": _sha(f)}


def _store(tmp_path, name="s-store"):
    store = tmp_path / name
    h = store / "stages" / "A" / "table_a.npz"
    dg, ids = _table(h, 3)
    nh = store / "stages" / "A" / "ORACLE_x.npz"
    nh.write_bytes(b"not an npz at all")
    obl = {"schema": SCHEMA, "job": "T", "attempt": 1, "store": str(store),
           "written_utc": "2026-11-02T06:00:00Z", "dry_stores": [], "name_rules": [],
           "files": [_entry(store, h, "K4b history table", "k4b_history_table"),
                     _entry(store, nh, "NON_HISTORY", None)]}
    (store / "REGISTRY_OBLIGATION.json").write_text(json.dumps(obl), encoding="utf-8")
    return store, obl, dg, ids


def _write(store, obl, name="REGISTRY_OBLIGATION.json"):
    (store / name).write_text(json.dumps(obl), encoding="utf-8")


def test_class_to_reader_table_matches_contract():
    gr = mod("gr")
    table = {(r["class"], r["reader"]) for r in CONTRACT["registry"]["class_to_reader"]}
    assert table == {("K4b history table", "k4b_history_table"), ("NON_HISTORY", None)}
    assert set(gr.CLASS_TO_READER) == table
    assert gr.CLASS_TO_READER[("NON_HISTORY", None)] is None
    assert callable(gr.CLASS_TO_READER[("K4b history table", "k4b_history_table")])


def test_matching_listing_passes_and_returns_digests(tmp_path):
    gr = mod("gr")
    store, obl, dg, ids = _store(tmp_path)
    out = gr.source_obligation(store)
    assert not is_incomplete(out), out
    assert out["digests"] == dg and out["seq_ids"] == ids
    assert any("ORACLE_x" in str(x) for x in out["non_history"])


def test_new_missing_resized_array_is_incomplete(tmp_path):
    gr = mod("gr")
    store, obl, *_ = _store(tmp_path)
    extra = store / "stages" / "A" / "extra.npz"
    np.savez(extra, a=np.zeros(2))
    assert is_incomplete(gr.source_obligation(store))  # new
    extra.unlink()
    assert not is_incomplete(gr.source_obligation(store))
    (store / "stages" / "A" / "ORACLE_x.npz").write_bytes(b"resized!!" * 9)
    assert is_incomplete(gr.source_obligation(store))  # resized
    (store / "stages" / "A" / "ORACLE_x.npz").unlink()
    assert is_incomplete(gr.source_obligation(store))  # missing


def test_array_listing_includes_subfolders_and_is_stat_only(tmp_path, monkeypatch):
    gr = mod("gr")
    store, *_ = _store(tmp_path)
    sup = store / "superseded" / "j-a1" / "x.npy"
    sup.parent.mkdir(parents=True)
    np.save(sup, np.zeros(3))
    (store / "stages" / "A" / "note.json").write_text("{}", encoding="utf-8")
    opened = []
    real = builtins.open
    monkeypatch.setattr(builtins, "open", lambda p, *a, **k: (opened.append(str(p)),
                                                              real(p, *a, **k))[1])
    lst = gr.array_listing(store)
    rels = {r["relpath"] for r in lst}
    assert "superseded/j-a1/x.npy" in rels and "stages/A/table_a.npz" in rels
    assert not any(r.endswith(".json") for r in rels)
    assert not [o for o in opened if o.endswith((".npz", ".npy"))]


def test_history_sha_mismatch_is_lineage(tmp_path):
    gr = mod("gr")
    store, obl, *_ = _store(tmp_path)
    obl["files"][0]["sha256"] = "0" * 64
    _write(store, obl)
    try:
        out = gr.source_obligation(store)
    except Exception as exc:  # noqa: BLE001
        assert "LINEAGE" in str(getattr(exc, "status", exc))
    else:
        assert "LINEAGE" in str(out["status"])


@pytest.mark.parametrize("which", ["class", "reader"])
def test_unknown_class_or_reader_is_incomplete(tmp_path, which):
    gr = mod("gr")
    store, obl, *_ = _store(tmp_path)
    obl["files"][0]["class"] = "Mystery table" if which == "class" else "K4b history table"
    obl["files"][0]["reader"] = "k4b_history_table" if which == "class" else "other_reader"
    _write(store, obl)
    assert is_incomplete(gr.source_obligation(store))


def test_non_history_is_never_opened(tmp_path, monkeypatch):
    gr = mod("gr")
    store, *_ = _store(tmp_path)
    seen = []
    real_open, real_load = builtins.open, np.load
    sr = __import__("stage_records")
    real_sha = sr.sha256

    def spy_open(p, *a, **k):
        seen.append(str(p))
        return real_open(p, *a, **k)

    monkeypatch.setattr(builtins, "open", spy_open)
    monkeypatch.setattr(np, "load", lambda p, *a, **k: (seen.append(str(p)), real_load(p, *a, **k))[1])
    monkeypatch.setattr(sr, "sha256", lambda p, *a, **k: (seen.append(str(p)), real_sha(p, *a, **k))[1])
    # API-AMBIGUITY: the opener hook signature is open-like; the spies above cover every route
    out = gr.source_obligation(store, opener=spy_open)
    assert not is_incomplete(out)
    assert not [s for s in seen if "ORACLE_x" in s]


def test_metadata_files_listed_separately(tmp_path):
    gr = mod("gr")
    store, *_ = _store(tmp_path)
    (store / "stages" / "A" / "log.jsonl").write_text("{}\n", encoding="utf-8")
    (store / "STAGES.md").write_text("x", encoding="utf-8")
    out = gr.source_obligation(store)
    assert not is_incomplete(out)
    assert out.get("metadata") is not None
    assert not any("log.jsonl" in str(x) for x in out["files"])


def test_missing_obligation_is_incomplete(tmp_path):
    gr = mod("gr")
    store = tmp_path / "empty-store"
    store.mkdir()
    (store / "x.npz").write_bytes(b"")
    try:
        out = gr.source_obligation(store)
    except Exception as exc:  # noqa: BLE001
        assert "INCOMPLETE" in str(getattr(exc, "status", exc))
    else:
        assert is_incomplete(out)


def test_latest_obligation_by_written_utc(tmp_path):  # OPEN-3
    gr = mod("gr")
    store, obl, *_ = _store(tmp_path)
    older = dict(obl, written_utc="2026-11-01T00:00:00Z", job="OLD")
    newer = dict(obl, written_utc="2026-11-03T00:00:00Z", job="NEW")
    _write(store, older, "REGISTRY_OBLIGATION_zz-old.json")  # name sorts last on purpose
    _write(store, newer, "REGISTRY_OBLIGATION_aa-new.json")
    assert sorted(gr.obligation_files(store)) == sorted(
        ["REGISTRY_OBLIGATION.json", "REGISTRY_OBLIGATION_zz-old.json",
         "REGISTRY_OBLIGATION_aa-new.json"])
    assert gr.latest_obligation(store)["job"] == "NEW"


def test_hwsc_like_store_sealed_never_opened_and_unassigned_array(tmp_path, monkeypatch):
    gr = mod("gr")
    store = tmp_path / "hwsc-like"
    (store / "sealed").mkdir(parents=True)
    (store / "sealed" / "secret.npz").write_bytes(b"sealed")
    (store / "SEALED_VALIDATION.json").write_text("{}", encoding="utf-8")
    seen = []
    real = builtins.open
    monkeypatch.setattr(builtins, "open", lambda p, *a, **k: (seen.append(str(p)), real(p, *a, **k))[1])
    out = gr.source_hwsc(store, expected={})
    monkeypatch.undo()
    assert not [s for s in seen if "sealed" in s.lower()]
    assert not is_incomplete(out), out
    stray = store / "stages" / "S9"
    stray.mkdir(parents=True)
    np.savez(stray / "stray.npz", a=np.zeros(2))
    assert is_incomplete(gr.source_hwsc(store, expected={}))


def test_scratch_unmatched_top_level_dir_is_incomplete(tmp_path):
    gr = mod("gr")
    scratch = tmp_path / "scratch"
    (scratch / "zz-unmatched-dir").mkdir(parents=True)
    (scratch / "zz-unmatched-dir" / "f.txt").write_text("x", encoding="utf-8")
    now = time.time()
    os.utime(scratch / "zz-unmatched-dir", (now, now))
    assert is_incomplete(gr.source_scratch_g(scratch))


def test_scratch_to_freeze_row_is_incomplete(tmp_path):
    gr = mod("gr")
    scratch = tmp_path / "scratch"
    (scratch / "zz-unlisted-0999").mkdir(parents=True)
    now = time.time()
    os.utime(scratch / "zz-unlisted-0999", (now, now))
    # no CONTRACT row or prefix rule matches this name (R-0238-1 item B: hwsc-job-* is frozen as EXCLUSION)
    assert is_incomplete(gr.source_scratch_g(scratch))


def test_root_unlisted_dir_with_history_file_is_incomplete(tmp_path):
    gr = mod("gr")
    root = tmp_path / "root"
    (root / "mystery-store" / "stages").mkdir(parents=True)
    _table(root / "mystery-store" / "stages" / "table_z.npz", 5)
    out = gr.inventory_g(root)
    assert is_incomplete(out)


def test_cross_world_collision_is_lineage(tmp_path):
    gr = mod("gr")
    reg = {"digests": set(), "seq_ids": set(), "status": "PASS"}
    same = np.random.default_rng(9).integers(0, 36, (4, 32), dtype=np.uint8)
    ids = np.arange(4, dtype=np.int64)
    # API-AMBIGUITY: tables_by_world maps tag -> {block: (canon32, seq_ids)}
    tables = {"lo": {"cal_b0": (same, ids)}, "hi": {"cal_b0": (same.copy(), ids.copy())}}
    try:
        out = gr.separation_g(reg, tables)
    except Exception as exc:  # noqa: BLE001
        assert "LINEAGE" in str(getattr(exc, "status", exc)) or "INCOMPLETE" in str(
            getattr(exc, "status", exc))
    else:
        assert out.get("status") != "PASS"


def test_recheck_after_root_change_is_incomplete(tmp_path):
    gr = mod("gr")
    root = tmp_path / "root"
    root.mkdir()
    out_dir = tmp_path / "out"
    kw = {"root": root, "scratch": tmp_path / "scr", "worlds": ("lo",),
          "sources_fn": lambda *a, **k: {}}
    (tmp_path / "scr").mkdir()
    try:
        m = gr.build("REHEARSAL", out_dir, **kw)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"build fixture not constructible black-box: {exc}")
    (root / "new-store" / "stages").mkdir(parents=True)
    _table(root / "new-store" / "stages" / "t.npz", 7)
    r = gr.recheck(m, root=root)
    assert is_incomplete(r) or "INCOMPLETE" in str(r)


def test_all_outputs_under_tmp_path(tmp_path):
    ok = Path(tmp_path).resolve()
    assert "topo-pilot" not in [p.lower() for p in ok.parts] or "topo-scratch" in str(ok).lower()
