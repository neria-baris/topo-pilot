"""Author B (job 0223, phase 2): U5 (source_hwsd), J10 obligations of another store and R-0213-1
(API_U2 2.4, 3; TEST_PLAN_U2 row test_b_u2_hwsd). Track-D-form fixtures only, under tmp_path; no
real hwsd-store file is opened. Obligations use the phase-1 obligation shape
(hws-registry-obligation-v1), with their own name_rule."""

from __future__ import annotations

import builtins
import hashlib
import importlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import k4b_data as kd  # noqa: E402

INC = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
AUTH = "INCONCLUSIVE/AUTHORITY"


def _reg():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_registry")


def _known():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_known")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _put(p: Path, data: bytes) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return _sha(data)


RULES = [{"kind": "oracle-moment", "regex": r"stages/(?:.+/)?ORACLE_[^/]*\.npz"},
         {"kind": "score", "regex": r"stages/(?:.+/)?PAIR_[^/]*\.npz"}]


def _nonhist(store: Path, rel="stages/KC/ORACLE_kc.npz") -> dict:
    p = store / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez(p, G=np.arange(4.0))
    raw = p.read_bytes()
    return {"relpath": rel, "sha256": _sha(raw), "bytes": len(raw), "class": "NON_HISTORY",
            "reader": None, "basis": "name_rule"}


def _hist(store: Path, rel="stages/KC/HIST_kc_b0.npz", seed=1) -> dict:
    p = store / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    canon = rng.integers(0, 36, size=(6, 32)).astype(np.uint8)
    np.savez(p, **kd.history_table(canon, np.arange(6) + seed * 100, "val", 0))
    raw = p.read_bytes()
    return {"relpath": rel, "sha256": _sha(raw), "bytes": len(raw), "class": "K4b history table",
            "reader": "k4b_history_table", "basis": None}


def _obl(store: Path, files: list, name="REGISTRY_OBLIGATION.json", utc="2026-11-02T12:00:00Z",
         rules=None):
    """A J11-form obligation (API.md J11 erratum): all top-level keys, files sorted by relpath."""
    rec = {"schema": "hws-registry-obligation-v1", "store": str(store).replace("\\", "/"),
           "track": "U", "job": "x", "attempt": 1, "written_utc": utc, "written_by": "fixture",
           "reservation_id": None, "name_rules": RULES if rules is None else rules,
           "dry_stores": [], "files": sorted(files, key=lambda f: f["relpath"]), "rule": "fail closed"}  # noqa: E501
    return _put(store / name, json.dumps(rec).encode("utf-8")), rec


@pytest.fixture
def opens(monkeypatch):
    seen: list = []
    real_open, real_load = builtins.open, np.load
    rb, rt = Path.read_bytes, Path.read_text

    def o(f, *a, **k):
        seen.append(str(f))
        return real_open(f, *a, **k)

    def ld(f, *a, **k):
        seen.append(str(f))
        return real_load(f, *a, **k)

    def prb(self):
        seen.append(str(self))
        return rb(self)

    def prt(self, *a, **k):
        seen.append(str(self))
        return rt(self, *a, **k)

    monkeypatch.setattr(builtins, "open", o)
    monkeypatch.setattr(np, "load", ld)
    monkeypatch.setattr(Path, "read_bytes", prb)
    monkeypatch.setattr(Path, "read_text", prt)
    return seen


def _roots(tmp_path):
    root, scratch = tmp_path / "root", tmp_path / "scratch"
    root.mkdir()
    scratch.mkdir()
    return root, scratch


# ------------------------------------------------------------------ source_hwsd (U5)
def test_hwsd_store_absent_passes(tmp_path):
    root, scratch = _roots(tmp_path)
    r = _reg().source_hwsd(root, scratch)
    assert r["status"] == "PASS" and len(r.get("digests", [])) == 0


def test_hwsd_store_without_obligation_is_incomplete(tmp_path):
    root, scratch = _roots(tmp_path)
    (root / "hwsd-store").mkdir()
    _hist(root / "hwsd-store")
    assert _reg().source_hwsd(root, scratch)["status"] == INC


def test_hwsd_known_case_only_store_passes(tmp_path):
    root, scratch = _roots(tmp_path)
    st = root / "hwsd-store"
    _obl(st, [_nonhist(st)])
    assert _reg().source_hwsd(root, scratch)["status"] == "PASS"


def test_hwsd_listed_history_file_is_read_by_its_reader(tmp_path):
    root, scratch = _roots(tmp_path)
    st = root / "hwsd-store"
    e = _hist(st)
    _obl(st, [e])
    r = _reg().source_hwsd(root, scratch)
    assert r["status"] == "PASS" and len(r["digests"]) == 6


def test_hwsd_unlisted_chart_array_is_incomplete(tmp_path):
    root, scratch = _roots(tmp_path)
    st = root / "hwsd-store"
    _obl(st, [_nonhist(st)])
    _put(st / "stages" / "S4" / "CHART_1.npz", b"PLANTED-CHART")
    assert _reg().source_hwsd(root, scratch)["status"] == INC


def test_hwsd_newest_obligation_governs(tmp_path):
    root, scratch = _roots(tmp_path)
    st = root / "hwsd-store"
    e = _nonhist(st)
    _obl(st, [e], name="REGISTRY_OBLIGATION_a.json", utc="2026-11-01T00:00:00Z")
    bad = dict(e, sha256="0" * 64)
    _obl(st, [bad], name="REGISTRY_OBLIGATION_b.json", utc="2026-11-02T00:00:00Z")
    assert _reg().source_hwsd(root, scratch)["status"] == INC


def test_hwsd_newer_complete_obligation_rescues_older_incomplete(tmp_path):
    root, scratch = _roots(tmp_path)
    st = root / "hwsd-store"
    e = _nonhist(st)
    _obl(st, [dict(e, sha256="0" * 64)], name="REGISTRY_OBLIGATION_a.json", utc="2026-11-01T00:00:00Z")  # noqa: E501
    _obl(st, [e], name="REGISTRY_OBLIGATION_b.json", utc="2026-11-02T00:00:00Z")
    assert _reg().source_hwsd(root, scratch)["status"] == "PASS"


def test_hwsd_dry_directory_without_obligation_is_incomplete(tmp_path):
    root, scratch = _roots(tmp_path)
    _put(scratch / "hwsd-dry-x" / "stages" / "D" / "ORACLE_d.npz", b"planted")
    assert _reg().source_hwsd(root, scratch)["status"] == INC


def test_read_obligation_u2_uses_each_obligations_own_name_rules(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    e = _nonhist(st, "stages/KC/ORACLE_kc.npz")
    _obl(st, [e])
    r = _reg().read_obligation_u2(st, root)
    assert r["status"] == "PASS" and not r["problems"]
    # a prefix outside this obligation's own rules is a problem ...
    odd = _nonhist(st, "stages/KC/SPECIAL_x.npz")
    _obl(st, [e, odd], name="REGISTRY_OBLIGATION_z.json", utc="2026-11-03T00:00:00Z")
    r2 = _reg().read_obligation_u2(st, root)
    assert r2["status"] == INC and r2["problems"]
    # ... and admitted when that (newest) obligation carries a rule that fullmatches it
    own = RULES + [{"kind": "score", "regex": r"stages/(?:.+/)?SPECIAL_[^/]*\.npz"}]
    _obl(st, [e, odd], name="REGISTRY_OBLIGATION_y.json", utc="2026-11-04T00:00:00Z", rules=own)
    r3 = _reg().read_obligation_u2(st, root)
    assert r3["status"] == "PASS", r3


def test_only_obligation_reservation_and_end_files_are_opened(tmp_path, opens):
    root, scratch = _roots(tmp_path)
    st = root / "hwsd-store"
    _obl(st, [_nonhist(st)])
    _put(st / "stages" / "S9" / "REPORT.json", b'{"result": "blinded"}')
    _put(st / "planning-HWSD-round.md", b"round file")
    _reg().source_hwsd(root, scratch)
    _known().w2_attestation_u2(root)
    assert not [p for p in opens if p.endswith(("REPORT.json", "HWSD-round.md"))]
    assert not [p for p in opens if "stages" in Path(p).parts and "hwsd-store" in Path(p).parts
                and not p.endswith(".npz")]


# ------------------------------------------------------------------ R-0213-1 path resolution
def _end(store: Path, rel: str, rid="RES-HWSD-1"):
    p = store / "reservations" / f"{rid}.END.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"obligation_file": rel}), encoding="utf-8")
    return json.loads(p.read_text(encoding="utf-8")), p


def test_store_relative_obligation_file_resolves_in_store(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    _put(st / "REGISTRY_OBLIGATION.json", b"{}")
    rec, p = _end(st, "REGISTRY_OBLIGATION.json")
    got = _known().end_obligation_path(rec, p, root)
    assert got is not None and Path(got).resolve() == (st / "REGISTRY_OBLIGATION.json").resolve()


def test_root_relative_path_inside_the_store_is_accepted(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    _put(st / "REGISTRY_OBLIGATION.json", b"{}")
    rec, p = _end(st, "hwsd-store/REGISTRY_OBLIGATION.json")
    got = _known().end_obligation_path(rec, p, root)
    assert got is not None and Path(got).resolve() == (st / "REGISTRY_OBLIGATION.json").resolve()


def test_store_candidate_wins_over_root_candidate(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    _put(st / "O.json", b"{}")
    _put(root / "O.json", b"{}")
    rec, p = _end(st, "O.json")
    assert Path(_known().end_obligation_path(rec, p, root)).resolve() == (st / "O.json").resolve()


def test_candidates_existing_only_outside_the_store_are_not_used(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    st.mkdir()
    _put(root / "other-store" / "OBL.json", b"{}")
    rec, p = _end(st, "other-store/OBL.json")  # exists only at <root>/<rel>, outside the store
    assert _known().end_obligation_path(rec, p, root) is None
    _put(root / "escape.json", b"{}")
    rec2, p2 = _end(st, "../escape.json", rid="RES-HWSD-2")  # <store>/../escape.json: outside
    assert _known().end_obligation_path(rec2, p2, root) is None
    rec3, p3 = _end(st, "nothing-here.json", rid="RES-HWSD-3")
    assert _known().end_obligation_path(rec3, p3, root) is None


# ------------------------------------------------------------------ w2_attestation_u2
def _reservation(store: Path, rid="RES-HWSD-1", state="ACTIVE"):
    rec = {"id": rid, "scope": "x", "state": state, "start_utc": "2026-11-01T00:00:00Z",
           "end_utc": None, "interruptions": [], "job_states": {}, "written_by": "fixture"}
    f = f"RESERVATION_{rid[-1]}.json"
    return _put(store / f, json.dumps(rec).encode("utf-8")), f


def _end_record(store: Path, rid, res_f, res_sha, obl_f, obl_sha, root):
    rec = {"schema": "hws-reservation-end-v1", "reservation_id": rid,
           "reservation_file": f"{store.name}/{res_f}", "reservation_sha256": res_sha,
           "end_utc": "2026-11-02T00:00:00Z", "obligation_file": obl_f, "obligation_sha256": obl_sha,  # noqa: E501
           "written_by": "fixture"}
    p = store / "reservations" / f"{rid}.END.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec), encoding="utf-8")


def _ended_store(root: Path, obl_rel="REGISTRY_OBLIGATION.json"):
    st = root / "hwsd-store"
    res_sha, res_f = _reservation(st)
    obl_sha = _put(st / "REGISTRY_OBLIGATION.json", b'{"fixture": 1}')
    _end_record(st, "RES-HWSD-1", res_f, res_sha, obl_rel, obl_sha, root)
    return st, res_f


def test_w2_store_relative_end_record_counts_as_ended(tmp_path):
    root, _ = _roots(tmp_path)
    _ended_store(root)
    r = _known().w2_attestation_u2(root)
    assert r["status"] == "PASS" and r["live"] == [] and r["ended"].get("RES-HWSD-1") == "b"


def test_w2_root_relative_end_record_inside_store_counts_as_ended(tmp_path):
    root, _ = _roots(tmp_path)
    _ended_store(root, obl_rel="hwsd-store/REGISTRY_OBLIGATION.json")
    assert _known().w2_attestation_u2(root)["status"] == "PASS"


def test_w2_reservation_without_end_record_is_live(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    _reservation(st)
    r = _known().w2_attestation_u2(root)
    assert r["status"] == AUTH and "RES-HWSD-1" in r["live"]


def test_w2_changed_reservation_file_is_live(tmp_path):
    root, _ = _roots(tmp_path)
    st, res_f = _ended_store(root)
    p = st / res_f
    p.write_bytes(p.read_bytes() + b" ")
    r = _known().w2_attestation_u2(root)
    assert r["status"] == AUTH and "RES-HWSD-1" in r["live"]


def test_w2_obligation_only_outside_the_store_is_live(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    res_sha, res_f = _reservation(st)
    obl_sha = _put(root / "elsewhere" / "OBL.json", b"{}")
    _end_record(st, "RES-HWSD-1", res_f, res_sha, "elsewhere/OBL.json", obl_sha, root)
    r = _known().w2_attestation_u2(root)
    assert r["status"] == AUTH and "RES-HWSD-1" in r["live"]


def test_w2_changed_obligation_bytes_is_live(tmp_path):
    root, _ = _roots(tmp_path)
    st, _ = _ended_store(root)
    p = st / "REGISTRY_OBLIGATION.json"
    p.write_bytes(p.read_bytes() + b" ")
    assert _known().w2_attestation_u2(root)["status"] == AUTH


def test_w2_own_reservation_is_excluded(tmp_path):
    root, _ = _roots(tmp_path)
    st = root / "hwsd-store"
    _reservation(st)
    r = _known().w2_attestation_u2(root, own="RES-HWSD-1")
    assert "RES-HWSD-1" not in r["live"]
    assert uc.CONTRACT["authority"]  # contract loaded (own/end keys follow phase-1 w2_attestation)
