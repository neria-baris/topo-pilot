"""Author B (job 0176): R6 scratch scan/check, R8 inventory, registry build, H2-FRESH.
(H2 separation_c is in test_b_streams.py for the 400-line limit.)

Written from PROTOCOL_HWSC_v1.md sections 3.3-3.4, API.md sections 3.3 and 4 (with section
18, R-0176-G9), CONTRACT.json `registry` and TEST_PLAN.md section 3 only. Synthetic roots under
tmp_path; heavy sources replaced via build(sources=...), reused K4b helpers by monkeypatch.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[0] != _HWSC:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402, I001
import hwsc_data as cd  # noqa: E402
import hwsc_registry as cr  # noqa: E402
import c1_records  # noqa: E402
import c2_registry  # noqa: E402
import k4b_data  # noqa: E402
import k4b_registry  # noqa: E402
import k4b_release  # noqa: E402

INCOMPLETE, LINEAGE = "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
_REC: list | None = None


def _audit(event, args):
    if _REC is not None and event in ("open", "os.scandir", "os.listdir") and args:
        _REC.append((event, str(args[0]).replace("\\", "/").lower()))


sys.addaudithook(_audit)


@pytest.fixture
def rec():
    global _REC
    _REC = []
    yield _REC
    _REC = None


def _hist(path, rows=5, seed=0):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, canon32=np.random.default_rng(seed).integers(0, 36, (rows, 32)).astype(np.uint8))
    return path


def _find(entries, suffix):
    return [v for k, v in entries.items() if str(k).replace("\\", "/").endswith(suffix)]


# ---------------------------------------------------------------- R6: header scan
@pytest.fixture
def scratch(tmp_path):
    s = tmp_path / "scratch"
    _hist(s / "x" / "a.npz")
    _hist(s / "x" / "test_a" / "h.npz")
    (s / "x").mkdir(exist_ok=True)
    np.savez(s / "x" / "ids.npz", seq_ids=np.arange(5, dtype=np.int64))
    np.savez(s / "x" / "f.npz", foo=np.zeros(3))
    (s / "x" / "bad.npz").write_bytes(b"not a zip archive")
    (s / "x" / "m.pt").write_bytes(b"torch-ish")
    meta = s / "x" / "store" / "ObservationSet" / "abc" / "meta.json"
    meta.parent.mkdir(parents=True)
    meta.write_text("{}", encoding="utf-8")
    _hist(s / "top.npz")
    _hist(s / "test_foo" / "h.npz")
    _hist(s / "test_hwsb-x" / "pytest" / "test_case0" / "h.npz")
    _hist(s / "hwsb-x" / "test_q" / "h.npz")
    _hist(s / "hwsb-dry-x" / "test_q" / "h.npz")
    return s


def test_r6_scan_classes_and_pruning(scratch, rec, monkeypatch):
    def no_load(*a, **k):
        raise AssertionError("np.load called: only headers may be read")

    monkeypatch.setattr(np, "load", no_load)
    scan = cr.scratch_scan(scratch)
    x = scan["x"]
    assert [v["class"] for v in _find(x, "a.npz")] == ["history"]
    assert tuple(_find(x, "a.npz")[0]["shape"]) == (5, 32)
    assert [v["class"] for v in _find(x, "ids.npz")] == ["identity"]
    assert [v["class"] for v in _find(x, "bad.npz")] == ["unreadable"]
    assert [v["class"] for v in _find(x, "m.pt")] == ["pt"]
    assert any(v["class"] == "os_root" for v in x.values())
    assert not _find(x, "f.npz") and not _find(x, "test_a/h.npz")
    assert "top.npz" in json.dumps(scan["__top_level__"], default=str)
    assert "test_foo" not in scan
    assert [v["class"] for v in _find(scan["test_hwsb-x"], "test_case0/h.npz")] == ["history"]
    assert [v["class"] for v in _find(scan["hwsb-x"], "test_q/h.npz")] == ["history"]
    assert [v["class"] for v in _find(scan["hwsb-dry-x"], "test_q/h.npz")] == ["history"]
    assert not [p for _, p in rec if "/x/test_a" in p]  # never listed, never opened
    assert not [p for e, p in rec if e == "open" and p.endswith("m.pt")]


def _rows(scratch, overrides):
    """A table whose frozen_files are written from the header scan, as at the freeze."""
    scan = cr.scratch_scan(scratch)
    table = {}
    for top, files in scan.items():
        if top == "__top_level__":
            continue
        frozen = {k: v["class"] for k, v in files.items()}
        table[top] = {"decision": "EXCLUSION", "reason": "fixture", "frozen_files": frozen}
    for top, row in overrides.items():
        table[top] = dict(table.get(top, {"frozen_files": {}}), **row)
    return table


def _check(scratch, table, readers_ok=()):
    return cr.scratch_check(scratch, table=table, readers_ok=set(readers_ok))


def test_r6_check_baseline_pass(tmp_path):
    s = tmp_path / "s"
    _hist(s / "x" / "a.npz")
    r = _check(s, _rows(s, {}))
    assert r["status"] == "PASS", r["other"]
    assert r["scan_counts"]["x"]["history"] == 1


R6_DEFECTS = {
    "new_top_level_dir": (lambda s: _hist(s / "newdir" / "h.npz"), {}),
    "to_freeze_row": (lambda s: None, {"x": {"decision": "TO_FREEZE"}}),
    "file_not_frozen": (lambda s: _hist(s / "x" / "later.npz", seed=3), {}),
    "top_level_array": (lambda s: _hist(s / "loose.npz"), {})}


@pytest.mark.parametrize("name", list(R6_DEFECTS))
def test_r6_defects_are_incomplete(tmp_path, name):
    s = tmp_path / "s"
    _hist(s / "x" / "a.npz")
    mutate, override = R6_DEFECTS[name]
    table = _rows(s, override)
    mutate(s)
    assert _check(s, table)["status"] == INCOMPLETE


def test_r6_reader_row_needs_its_reader(tmp_path):
    s = tmp_path / "s"
    _hist(s / "x" / "a.npz")
    table = _rows(s, {"x": {"decision": "READER", "readers": ["R5"]}})
    assert _check(s, table, readers_ok=())["status"] == INCOMPLETE
    assert _check(s, table, readers_ok=("c2scratch",))["status"] == INCOMPLETE
    assert _check(s, table, readers_ok=("R5",))["status"] == "PASS"


@pytest.mark.parametrize("rows,status", [(1000, "PASS"), (2000, INCOMPLETE)])
def test_r6_fixture_max_rows(tmp_path, rows, status):
    s = tmp_path / "s"
    _hist(s / "y" / "pt-x" / "h.npz", rows=rows)
    table = _rows(s, {"y": {"fixture_max_rows": 1024}})
    assert _check(s, table)["status"] == status


def test_r6_stage_b_folders_full_walk_and_empty_rows(tmp_path):
    s = tmp_path / "s"
    (s / "hwsb-0168").mkdir(parents=True)
    _hist(s / "test_hwsb-x" / "pytest" / "test_case0" / "h.npz", rows=1000)
    table = _rows(s, {"hwsb-0168": {"frozen_files": {}, "full_walk": True},
                      "test_hwsb-x": {"fixture_max_rows": 1024, "fixture_components": ["pytest"],
                                      "full_walk": True}})
    assert table["test_hwsb-x"]["frozen_files"], "the test_hwsb folder must be walked"
    assert _check(s, table)["status"] == "PASS"
    _hist(s / "hwsb-0168" / "test_late" / "a.npz")
    assert _check(s, table)["status"] == INCOMPLETE


# ---------------------------------------------------------------- R8: inventory
def test_r8_inventory_against_a_synthetic_table(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    _hist(root / "unlisted" / "h.npz")
    _hist(root / "hwsc-store" / "stages" / "S3" / "h.npz")
    (root / "listed-ex").mkdir(parents=True)
    (root / "listed-ex" / "notes.txt").write_text("no arrays", encoding="utf-8")
    table = {"listed-ex": {"decision": "EXCLUSION", "reason": "fixture"},
             "maybe-store": {"decision": "READER_IF_PRESENT", "readers": ["x6zc"]},
             "hwsc-store": {"decision": "OWN", "reason": "own"}}
    # API-AMBIGUITY: inventory_c reads CONTRACT registry.inventory at call time.
    monkeypatch.setitem(cc.CONTRACT["registry"], "inventory", table)
    r = cr.inventory_c(root, readers={})
    names = [v["name"] for v in r["violations"]]
    assert r["status"] == INCOMPLETE and "unlisted" in names
    assert "maybe-store" not in names and "listed-ex" not in names
    assert "hwsc-store" not in r["inv"] and "hwsc-store" not in names
    assert "unlisted" in r["unlisted"]


# ---------------------------------------------------------------- build (stub sources)
def _hexes(seed, n=3):
    rng = np.random.default_rng(seed)
    return {hashlib.sha256(rng.bytes(16)).hexdigest() for _ in range(n)}


def _src(digests=(), status="PASS", seq=()):
    other = [] if status == "PASS" else [{"path": "planted", "reason": status}]
    return {"status": status, "digests": set(digests), "seq_ids": set(seq), "files": [],
            "other": other, "non_history": [], "non_c2_format": [], "present": True,
            "known_gaps": []}


SOURCE_NAMES = ("c2", "c2sup", "c2scratch", "hws", "x6zc", "c2nd", "hwsb", "dry", "scratch", "own")


@pytest.fixture
def stubs(tmp_path, monkeypatch):
    monkeypatch.setattr(k4b_registry, "source_f", lambda *a, **k: [])
    monkeypatch.setattr(k4b_registry, "revalidate_coverage",
                        lambda *a, **k: {"ok": True, "missing": []})
    monkeypatch.setattr(k4b_registry, "validate_handoff_json",
                        lambda *a, **k: {"ok": True, "n_files": 0, "failures": []})
    monkeypatch.setattr(k4b_registry, "summary", lambda *a, **k: {"status": "NOT_READ (stub)"})
    calls = []

    def make(status=None, digests=None, x6_status="PASS", inv=None):
        status, digests = status or {}, digests or {}
        e = {"sources": [], "problems": [], "predicates": ["sealed_d2a"], "sealed_ranges": {},
             "ranges": {}}
        tok = {"a": ([], {}), "b": [], "c": [], "d": [], "e": e, "k": None, "problems": [],
               "lineage": [], "art": tmp_path / "art", "store_a": None}
        inv = inv or {"status": "PASS", "inv": {}, "classes": {}, "unlisted": [],
                      "violations": []}
        src = {"token_sources": lambda *a, **k: tok, "inventory": lambda *a, **k: inv,
               "x6_source": lambda *a, **k: {"status": x6_status, "digestset": None, "files": [],
                                             "other": [], "base": None}}
        for i, n in enumerate(SOURCE_NAMES):
            d = digests.get(n, _hexes(100 + i))

            def fn(*a, _n=n, _d=d, **k):
                calls.append(_n)
                return _src(_d, status.get(_n, "PASS"))

            src[n] = fn
        want = set().union(*[digests.get(n, _hexes(100 + i)) for i, n in enumerate(SOURCE_NAMES)])
        return src, want

    make.calls = calls
    return make


def _build(tmp_path, version, sources, **kw):
    store = tmp_path / "store"
    out = store / "registry" if version != "REHEARSAL" else store / "registry" / "rehearsal"
    own = kw.pop("own_expected", {} if version != "REHEARSAL" else None)
    return store, cr.build(version, out, root=tmp_path / "root", scratch=tmp_path / "scr",
                           handoff={"store_inventory": {}}, own_expected=own, sources=sources,
                           **kw)


def test_build_k_reg1_loads_unchanged(tmp_path, stubs):
    src, want = stubs()
    store, m = _build(tmp_path, "K-REG1", src)
    assert m["status"] == "PASS", m.get("problems")
    assert (store / "registry" / "K-REG1.json").is_file()
    assert (store / "registry" / "K-REG1_digests.npz").is_file()
    reg = c2_registry.Registry.load(store, "K-REG1")
    assert reg.digests == want
    disk = json.loads((store / "registry" / "K-REG1.json").read_text(encoding="utf-8"))
    assert disk["registry_version"] == "hwsc-reg-v1" and disk["version"] == "K-REG1"
    assert disk["protocol_sha256"] == cc.CONTRACT["protocol_sha256"]
    assert disk["n_digests"] == len(want) and "hwsc_sources" in disk and "cpu_s" in disk
    assert "own" in stubs.calls


@pytest.mark.parametrize("planted,status", [
    ({"c2nd": LINEAGE}, LINEAGE), ({"dry": INCOMPLETE}, INCOMPLETE),
    ({"scratch": INCOMPLETE, "hwsb": LINEAGE}, LINEAGE), ({"own": INCOMPLETE}, INCOMPLETE),
    ({"hws": INCOMPLETE}, INCOMPLETE)])
def test_build_status_precedence(tmp_path, stubs, planted, status):
    src, _ = stubs(status=planted)
    assert _build(tmp_path, "K-REG1", src)[1]["status"] == status


def test_build_x6_lineage_and_inventory_violation(tmp_path, stubs):
    src, _ = stubs(x6_status=LINEAGE)
    assert _build(tmp_path / "a", "K-REG1", src)[1]["status"] == LINEAGE
    bad = {"status": INCOMPLETE, "inv": {}, "classes": {}, "unlisted": ["new"],
           "violations": [{"name": "new", "reason": "planted"}]}
    src, _ = stubs(inv=bad)
    assert _build(tmp_path / "b", "K-REG1", src)[1]["status"] == INCOMPLETE


def _tables(n=600, seed=0):
    rng = np.random.default_rng(seed)
    out = {}
    for i, s in enumerate(("lgate", "cal", "val")):
        canon = rng.integers(0, 36, (n, 32)).astype(np.uint8)
        out[s] = k4b_data.history_table(canon, np.arange(n, dtype=np.int64) + 10_000 * (i + 1),
                                        s, 0)
    return out


def test_build_extra_only_for_k_reg2(tmp_path, stubs):
    src, want = stubs()
    t = _tables()
    with pytest.raises(ValueError):
        _build(tmp_path / "a", "K-REG1", src, extra=t)
    store, m = _build(tmp_path / "b", "K-REG2", src, extra=t)
    reg = c2_registry.Registry.load(store, "K-REG2")
    extra_d = {d for s in t.values() for d in s["digest"].tolist()}
    assert m["status"] == "PASS" and reg.digests == want | extra_d
    assert {i for s in t.values() for i in s["seq_ids"].tolist()} <= reg.seq_ids


def test_build_rehearsal_refusals_and_exclusivity(tmp_path, stubs):
    src, _ = stubs()
    with pytest.raises(ValueError):
        _build(tmp_path / "a", "REHEARSAL", src, own_expected={})
    stubs.calls.clear()
    _, m = _build(tmp_path / "b", "REHEARSAL", src)
    assert m["status"] == "PASS" and "own" not in stubs.calls
    _build(tmp_path / "c", "K-REG1", src)
    with pytest.raises(FileExistsError):
        _build(tmp_path / "c", "K-REG1", src)
    with pytest.raises(ValueError):
        _build(tmp_path / "d", "K-REG9", src)


# ---------------------------------------------------------------- H2-FRESH
@pytest.fixture
def fresh(tmp_path, stubs):
    def make(planted_test_digest=False):
        out = tmp_path / "store"
        tables = _tables()
        canon = np.random.default_rng(99).integers(0, 36, (600, 32)).astype(np.uint8)
        tb = k4b_data.history_table(canon, np.arange(600, dtype=np.int64) + 50_000, "test", 0)
        test = {"canon32": tb["canon32"], "seq_ids": tb["seq_ids"], "digest": tb["digest"],
                "blocks": [tb]}
        dig = {"dry": {tb["digest"][4]}} if planted_test_digest else {}
        src, _ = stubs(digests=dig)
        cr.build("K-REG2", out / "registry", root=tmp_path / "root", scratch=tmp_path / "scr",
                 handoff={"store_inventory": {}}, own_expected={}, extra=tables, sources=src)
        res = out / cc.RESERVATION_FILE
        k4b_release.start_reservation(res, "HWSC-W2", "2026-10-29T00:00:00Z")
        ctx = {"reservation_path": res, "release": {"reservation": cc.RESERVATION_ID},
               "tables": tables, "test": test}
        return out, ctx

    return make


def test_h2_fresh_clean_pass(fresh):
    out, ctx = fresh()
    r = cd.h2_fresh_c(out, ctx)
    assert r.get("status", "PASS") == "PASS"


def test_h2_fresh_test_digest_in_k_reg2_is_lineage(fresh):
    out, ctx = fresh(planted_test_digest=True)
    with pytest.raises(c1_records.C1GateFailure) as e:
        cd.h2_fresh_c(out, ctx)
    assert e.value.status == LINEAGE


def test_h2_fresh_interrupted_reservation_stops(fresh):
    out, ctx = fresh()
    rec = json.loads(ctx["reservation_path"].read_text(encoding="utf-8"))
    rec["interruptions"].append({"utc": "2026-10-29T01:00:00Z", "reason": "planted"})
    ctx["reservation_path"].write_text(json.dumps(rec), encoding="utf-8")
    with pytest.raises(c1_records.C1GateFailure) as e:
        cd.h2_fresh_c(out, ctx)
    assert e.value.status == "STOP/LINEAGE_REVIEW"
