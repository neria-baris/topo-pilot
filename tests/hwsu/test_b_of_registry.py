"""Author B (job 0198): the J11 obligation reader on fixtures written in the other track's form,
the fail-closed rules of J10/J11, the root inventory (§8.4 hygiene) and the registry rows of
CONTRACT_OF. Joint rulings J4, J10 (addendum 3), J11 (addendum 4); API J11 erratum; DRO9.
Readers: `hwsu_resv.read_obligation` (J11 erratum) and `hwsu_dry.obligation_reader_fixture`."""

from __future__ import annotations

import builtins
import copy
import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_records as ur  # noqa: E402
import k4b_data  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
INC = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
D_RULES = [{"kind": "chart", "regex": r"stages/(?:.+/)?CHART_[^/]*\.npz"},
           {"kind": "score", "regex": r"stages/(?:.+/)?SCORES_[^/]*\.npz"}]


def _readers():
    import hwsu_dry as udry
    import hwsu_resv
    return [hwsu_resv.read_obligation, udry.obligation_reader_fixture]


def _norm(p) -> str:
    return os.path.normcase(os.path.abspath(str(p)))


def _hook(monkeypatch) -> list:
    seen, real_open, real_load = [], builtins.open, np.load

    def rec(file, *a, **k):
        if isinstance(file, (str, Path)):
            seen.append(_norm(file))
        return real_open(file, *a, **k)

    monkeypatch.setattr(builtins, "open", rec)
    monkeypatch.setattr(io, "open", rec)
    for name in ("open", "read_bytes", "read_text"):
        real = getattr(Path, name)

        def wrap(self, *a, _real=real, **k):
            seen.append(_norm(self))
            return _real(self, *a, **k)

        monkeypatch.setattr(Path, name, wrap)
    monkeypatch.setattr(np, "load", lambda f, *a, **k: (seen.append(_norm(f)), real_load(f, *a, **k))[1])
    return seen


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _npz(path, **arrays) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **(arrays or {"x": np.arange(3.0)}))
    return path


def _hist(path):
    canon = np.full((4, 32), 9, dtype=np.uint8)
    canon[:, 1] = np.arange(4) + 5
    t = k4b_data.history_table(canon, np.arange(4, dtype=np.int64) + 7, "test", 0)
    return _npz(path, **{k: t[k] for k in ("canon32", "seq_ids", "digest", "landmark", "ref_row",
                                           "decoder_panel")})


def _entry(store, rel, cls, basis=None):
    p = Path(store) / rel
    ck = rel.startswith("artifacts/Checkpoint/")
    reader = {"K4b history table": "k4b_history_table",
              "ObservationSet": "hwsb_registry.registry_digests"}.get(cls)
    return {"relpath": rel, "sha256": None if ck else _sha(p), "bytes": p.stat().st_size,
            "class": cls, "reader": reader, "basis": basis}


def _d_store(root):
    """A store as track D would write it (J11 form, track "D", its own name rules)."""
    store = root / "hwsd-store"
    _hist(store / "stages/SAMPLE/HIST_d_b0.npz")
    _npz(store / "stages/S4/CHART_m1.npz")
    _npz(store / "stages/S5/SCORES_m1.npz", s=np.ones(3))
    _npz(store / "registry/K-REG1_digests.npz", d=np.arange(4))
    _npz(store / "artifacts/Checkpoint/ck9/payload.npz")
    _npz(store / "artifacts/WorldSpec/w9/payload.npz", w=np.eye(2))
    for t, d in (("Checkpoint", "ck9"), ("WorldSpec", "w9")):
        (store / "artifacts" / t / d / "meta.json").write_text(json.dumps({"artifact_type": t}),
                                                               encoding="utf-8")
    files = [_entry(store, "artifacts/Checkpoint/ck9/payload.npz", "NON_HISTORY", "artifact"),
             _entry(store, "artifacts/WorldSpec/w9/payload.npz", "NON_HISTORY", "artifact"),
             _entry(store, "registry/K-REG1_digests.npz", "NON_HISTORY", "registry"),
             _entry(store, "stages/S4/CHART_m1.npz", "NON_HISTORY", "name_rule"),
             _entry(store, "stages/S5/SCORES_m1.npz", "NON_HISTORY", "name_rule"),
             _entry(store, "stages/SAMPLE/HIST_d_b0.npz", "K4b history table")]
    return store, files


def _obl(store, files, name="REGISTRY_OBLIGATION.json", utc="2026-11-01T12:00:00Z", **over):
    rec = {"schema": "hws-registry-obligation-v1", "store": Path(store).resolve().as_posix(),
           "track": "D", "job": "0300", "attempt": 1, "written_utc": utc,
           "written_by": "hwsd_records.write_obligation (fixture)", "reservation_id": "RES-HWSD-W2",
           "name_rules": copy.deepcopy(D_RULES), "dry_stores": [], "files": copy.deepcopy(files),
           "rule": "fail closed"}
    rec.update(over)
    p = Path(store) / name
    p.write_bytes(json.dumps(rec, indent=1).encode("utf-8"))
    return p


def _status(store):
    out = []
    for reader in _readers():
        r = reader(store)
        assert set(r) >= {"status", "problems"}
        out.append(r["status"])
    return out


# ------------------------------------------------------------------ J11 reader on track-D form
def test_reader_track_d_form_passes(tmp_path, monkeypatch):
    store, files = _d_store(tmp_path / "root")
    _obl(store, files)
    seen = _hook(monkeypatch)
    assert _status(store) == ["PASS", "PASS"]
    monkeypatch.undo()
    assert _norm(store / "artifacts/Checkpoint/ck9/payload.npz") not in seen  # never opened


def _mutations():
    def drop_top(r): r.pop("rule")
    def extra_top(r): r["extra"] = 1
    def bad_schema(r): r["schema"] = "hws-registry-obligation-v2"
    def bad_track(r): r["track"] = "X"
    def bad_rule(r): r["rule"] = "fail open"
    def drop_file_key(r): r["files"][0].pop("bytes")
    def extra_file_key(r): r["files"][1]["note"] = "x"
    def bad_class(r): r["files"][5]["class"] = "History"
    def bad_basis(r): r["files"][2]["basis"] = "ii"
    def bad_reader(r): r["files"][5]["reader"] = "hwsb_registry.registry_digests"
    def nh_reader(r): r["files"][2]["reader"] = "k4b_history_table"
    def hist_basis(r): r["files"][5]["basis"] = "name_rule"
    def null_sha_not_ck(r): r["files"][1]["sha256"] = None
    def upper_sha(r): r["files"][2]["sha256"] = r["files"][2]["sha256"].upper()
    def bad_kind(r): r["name_rules"][0]["kind"] = "plot"
    return [drop_top, extra_top, bad_schema, bad_track, bad_rule, drop_file_key, extra_file_key,
            bad_class, bad_basis, bad_reader, nh_reader, hist_basis, null_sha_not_ck, upper_sha,
            bad_kind]


@pytest.mark.parametrize("mut", _mutations(), ids=lambda f: f.__name__)
def test_reader_one_mutated_key_is_incomplete(tmp_path, mut):
    store, files = _d_store(tmp_path / "root")
    p = _obl(store, files)
    rec = json.loads(p.read_text(encoding="utf-8"))
    mut(rec)
    p.write_bytes(json.dumps(rec).encode("utf-8"))
    assert _status(store) == [INC, INC]


def test_reader_unlisted_array_is_incomplete(tmp_path):
    store, files = _d_store(tmp_path / "root")
    _obl(store, files)
    _npz(store / "stages/S4/CHART_m2.npz")  # one unlisted chart array (J10 item 5)
    assert _status(store) == [INC, INC]


def test_reader_sha_mismatch_is_incomplete(tmp_path):
    store, files = _d_store(tmp_path / "root")
    _obl(store, files)
    _npz((store / "stages/S5/SCORES_m1.npz").with_name("tmp.npz"), s=np.zeros(3))
    os.replace(store / "stages/S5/tmp.npz", store / "stages/S5/SCORES_m1.npz")
    assert _status(store) == [INC, INC]


def test_reader_checkpoint_sha_null_not_rehashed(tmp_path):
    store, files = _d_store(tmp_path / "root")
    _obl(store, files)
    (store / "artifacts/Checkpoint/ck9/payload.npz").write_bytes(b"changed, never hashed")
    assert _status(store) == ["PASS", "PASS"]


def test_reader_unmatched_name_rule_basis_is_incomplete(tmp_path):
    store, files = _d_store(tmp_path / "root")
    rules = [r for r in D_RULES if r["kind"] != "score"]  # SCORES_ no longer matched
    _obl(store, files, name_rules=rules)
    assert _status(store) == [INC, INC]


def test_reader_newest_governs(tmp_path):
    store, files = _d_store(tmp_path / "root")
    _obl(store, files, name="REGISTRY_OBLIGATION_0300-a1.json", utc="2026-11-01T10:00:00Z")
    _obl(store, files[:-1], name="REGISTRY_OBLIGATION.json", utc="2026-11-01T11:00:00Z")
    assert _status(store) == [INC, INC]  # the newer one omits a file
    store2, files2 = _d_store(tmp_path / "root2")
    _obl(store2, files2[:-1], name="REGISTRY_OBLIGATION.json", utc="2026-11-01T10:00:00Z")
    _obl(store2, files2, name="REGISTRY_OBLIGATION_0300-a2.json", utc="2026-11-01T11:00:00Z")
    assert _status(store2) == ["PASS", "PASS"]


def test_reader_known_case_records_only(tmp_path):
    store = tmp_path / "root" / "hwsd-store"
    (store / "stages" / "KC").mkdir(parents=True)
    (store / "stages" / "KC" / "KC0.json").write_text("{}", encoding="utf-8")
    _obl(store, [])
    assert _status(store) == ["PASS", "PASS"]


def test_reader_arrays_without_obligation_until_coordinator_writes_one(tmp_path):
    """J10 item 4: an aborted dry store stays incomplete until an obligation lists every array."""
    store = tmp_path / "hwsd-dry-x"
    _npz(store / "stages/S4/CHART_m1.npz")
    assert _status(store) == [INC, INC]
    _obl(store, [_entry(store, "stages/S4/CHART_m1.npz", "NON_HISTORY", "name_rule")],
         attempt=None, written_by="coordinator recovery step", reservation_id=None)
    assert _status(store) == ["PASS", "PASS"]


def test_reader_accepts_own_writer_output(tmp_path):
    """Round trip: the HWSU writer's record (track U) is accepted by the J11 reader."""
    store = tmp_path / "root" / "hwsu-store"
    _hist(store / "stages/OF/HIST_OF_fit_b0.npz")
    _npz(store / "stages/OF/ORACLE_OF_eval.npz")
    ur.write_obligation(store, "REGISTRY_OBLIGATION_OF.json", "OF", "w", attempt=1,
                        reservation_id="RES-HWSU-OF")
    assert _status(store) == ["PASS", "PASS"]
    _npz(store / "stages/OF/BOOT_OF.npz")
    assert _status(store) == [INC, INC]


# ------------------------------------------------------------------ root inventory (§8.4; API §10)
def _touch(p):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"")


def test_root_inventory_counts_and_pruning(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    a = ["sA/stages/x/a.npz", "sA/stages/HIST_b.npz", "sA/hist/c.npy",
         "sA/artifacts/ObservationSet/obs1/payload.npz"]
    for rel in a:
        _touch(root / rel)
    _touch(root / "sA/artifacts/ObservationSet/obs1/meta.json")
    _touch(root / "sA/artifacts/Checkpoint/ck/meta.json")  # not an ObservationSet root
    _touch(root / "sA/sealed/s.npz")
    _touch(root / "sA/notes-hws-dyn/x.npz")
    _touch(root / "sA/hwsd-x/x.npz")
    _touch(root / "sA/.git/x.npz")
    _touch(root / "sA/__pycache__/x.npy")
    _touch(root / "tp/src/x.py")
    _touch(root / "topo-pilot-hwsd/x.npz")
    _touch(root / "hwsd-store/stages/y.npz")
    seen = _hook(monkeypatch)
    inv = ur.root_inventory(root)
    monkeypatch.undo()
    assert [s for s in seen if s.startswith(_norm(root))] == []  # name-only: nothing opened
    row = inv["sA"]
    assert row.get("listed", True) is True
    assert row["n_array_files"] == 4 and row["n_protected_names"] == 3
    assert row["n_observationset_roots"] == 1 and row["n_sealed_dirs_pruned"] == 1
    want = hashlib.sha256("\n".join(sorted(a)).encode("utf-8")).hexdigest()
    assert row["array_relpaths_sha256"] == want
    t = inv["tp"]
    assert (t["n_array_files"], t["n_protected_names"]) == (0, 0)
    assert t["array_relpaths_sha256"] == hashlib.sha256(b"").hexdigest()
    for top in ("topo-pilot-hwsd", "hwsd-store"):
        assert inv[top]["listed"] is False and inv[top].get("reason")
    assert set(row) >= set(C["hygiene"]["root_rule"]["row"])


def test_root_inventory_detects_new_array(tmp_path):
    root = tmp_path / "proj"
    _touch(root / "sA/x.json")
    before = ur.root_inventory(root)
    _touch(root / "sA/stages/new.npz")
    after = ur.root_inventory(root)
    assert before != after and after["sA"]["n_array_files"] == 1


# ------------------------------------------------------------------ CONTRACT registry rows
def test_contract_obligation_block_is_j11():
    ob = C["obligation"]
    assert ob["schema"] == "hws-registry-obligation-v1" and ob["track"] == "U"
    assert ob["top_level"] == ["schema", "store", "track", "job", "attempt", "written_utc",
                               "written_by", "reservation_id", "name_rules", "dry_stores",
                               "files", "rule"]
    assert ob["file_keys"] == ["relpath", "sha256", "bytes", "class", "reader", "basis"]
    assert ob["classes"] == ["ObservationSet", "K4b history table", "NON_HISTORY"]
    assert ob["bases"] == ["artifact", "registry", "name_rule"] and ob["rule"] == "fail closed"
    assert ob["readers"] == {"ObservationSet": "hwsb_registry.registry_digests",
                             "K4b history table": "k4b_history_table", "NON_HISTORY": None}
    assert set(ob["name_rule_kinds"]) == {"chart", "decoder", "activation", "oracle-moment",
                                          "score", "bootstrap", "certificate"}
    prefixes = C["name_rule"]["phase1"]["prefixes"]
    import re
    for pre in prefixes:  # the frozen regexes cover exactly the phase-1 prefixes under stages/
        rel = f"stages/OF/{pre}x.npz"
        assert sum(bool(re.fullmatch(r["regex"], rel)) for r in ob["name_rules"]) == 1
        assert not any(re.fullmatch(r["regex"], f"{pre}x.npz") for r in ob["name_rules"])
    assert not any(re.fullmatch(r["regex"], "stages/OF/HIST_OF_fit_b0.npz") for r in ob["name_rules"])


def test_contract_reservation_baseline_and_root_baseline():
    rb = C["hygiene"]["reservations_baseline"]
    assert rb["status"] == "REVIEWED" and len(rb["rows"]) == 3  # TO_FREEZE review erratum
    assert rb["rows"]["hwsc-store/RESERVATION_W2.json"]["state"] == "ACTIVE"
    assert rb["rows"]["hwsc-store/RESERVATION_W2.json"]["sha256"] == \
        "28c74163e992972b89238dccb30660b500027a78ac4a563fa0958df736e9dbe5"  # = HWSC_W2_END binding
    assert all(rb["rows"][k]["state"] is None for k in rb["rows"] if k.startswith("c2nd-store/"))
    root = C["hygiene"]["root_baseline"]
    assert root["status"] == "REVIEWED" and len(root["rows"]) == 70  # TO_FREEZE review erratum
    unlisted = [k for k, v in root["rows"].items() if v.get("listed") is False]
    assert unlisted == ["topo-pilot-hwsd"]
    assert "hwsu-store" not in root["rows"]  # no HWSU store before OF
    for k, v in root["rows"].items():
        if v.get("listed", True):
            assert set(v) >= set(C["hygiene"]["root_rule"]["row"]), k
