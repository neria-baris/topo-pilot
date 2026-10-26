"""Author B, T-REG-ND (protocol §6.2-§6.5; API.md §5; rulings R-0116-3, R-0116-4).

Synthetic project roots, C2 stores, scratch roots and parallel stores live under pytest's
tmp_path (scratch roots under tmp_path_factory.mktemp, so no path component starts with
"test_" except where the exclusion is tested). Every path constant is monkeypatched on
nd_config, and CONTRACT entries are patched in place and restored.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md §1 "Test imports")

# isort: split
import c1_data  # noqa: E402
import c2_data as cd  # noqa: E402
import c2_registry as cg  # noqa: E402
import k4b_registry as kr  # noqa: E402
import nd_registry as nrg  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

PASS, INC = "PASS", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
LIN, AUTH = "FAIL_TECHNICAL/LINEAGE", "FAIL_TECHNICAL/AUTHORITY"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def table(seed, n=8):
    rng = np.random.default_rng(seed)
    canon = rng.integers(0, 36, size=(n, 32)).astype(np.uint8)
    ids = np.arange(n, dtype=np.int64) + 1000 * seed
    return cd.history_table(canon, ids, np.zeros(n, np.int64), np.ones(n, np.int64))


def save(path, **arrays):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        np.savez(fh, **arrays)
    return Path(path)


def garbage(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(b"not a zip archive")


def tokens(seed, n=4):
    return np.random.default_rng(seed).integers(0, 36, size=(n, 32)).astype(np.uint8)


def row_hex(tok):
    return {hashlib.sha256(r.astype(np.uint8).tobytes()).hexdigest() for r in tok}


@pytest.fixture
def loads(monkeypatch):
    """Every np.load path (a registry reader must never np.load a payload or sealed file)."""
    seen, real = [], np.load

    def spy(file, *a, **k):
        seen.append(str(getattr(file, "name", file)).replace("\\", "/"))
        return real(file, *a, **k)

    monkeypatch.setattr(np, "load", spy)
    return seen


@pytest.fixture
def scratch(tmp_path_factory, monkeypatch):
    root = tmp_path_factory.mktemp("scr")
    monkeypatch.setattr(nc, "SCRATCH_ROOT", root)
    return root


@pytest.fixture
def expected_roots():
    """Replace CONTRACT scratch_roots_expected in place (restored afterwards)."""
    lst = nc.CONTRACT["registry"]["scratch_roots_expected"]
    old = list(lst)

    def put(paths):
        lst[:] = [str(p) for p in paths]

    yield put
    lst[:] = old


@pytest.fixture
def c2_store(tmp_path, monkeypatch):
    store, hist, tabs = tmp_path / "c2-readout-store", nc.CONTRACT["registry"]["c2_hist"], {}
    for i, rel in enumerate(sorted(hist)):
        tabs[rel] = table(i + 1)
        monkeypatch.setitem(hist, rel, sha(save(store / rel, **tabs[rel])))
    monkeypatch.setattr(nc, "C2_STORE", store)
    return store, tabs


def union(tabs):
    out = set()
    for t in tabs:
        out |= cd.table_digests(t)
    return out


# ---- row 2: reader c2; separation ------------------------------------------------------------
def test_source_c2(c2_store):
    store, tabs = c2_store
    res = nrg.source_c2(store)
    assert res["status"] == PASS and res["digests"] == union(tabs.values())
    extra = table(40)
    save(store / "hist" / "HIST_extra_b0.npz", **extra)
    res = nrg.source_c2(store)
    assert union([extra]) <= res["digests"]  # a further HIST file is read and listed
    assert any(str(f["path"]).endswith("HIST_extra_b0.npz") for f in res["files"])


def test_source_c2_missing_and_mismatch(c2_store):
    store, tabs = c2_store
    rel = sorted(tabs)[0]
    save(store / rel, **table(99))  # one bound file re-hashes differently
    assert nrg.source_c2(store)["status"] == LIN
    (store / rel).unlink()
    assert nrg.source_c2(store)["status"] == INC


def test_planted_collision_with_a_c2_test_table(c2_store):
    store, tabs = c2_store
    fit = table(50)
    reg = cg.Registry(nrg.source_c2(store)["digests"], None, {}, [], {})
    assert nrg.separation(reg, {"fit": fit})["status"] == PASS
    rel = "hist/HIST_test_b0.npz"
    planted = dict(tabs[rel])
    planted["digest_H"] = planted["digest_H"].copy()
    planted["digest_H"][0] = fit["digest_H"][3]  # a DFIT history inside the C2 TEST table
    hist = nc.CONTRACT["registry"]["c2_hist"]
    hist[rel] = sha(save(store / rel, **planted))  # restored by the fixture's monkeypatch
    reg = cg.Registry(nrg.source_c2(store)["digests"], None, {}, [], {})
    sep = nrg.separation(reg, {"fit": fit})
    assert sep["status"] == LIN and sep["collisions"]["fit_R"] >= 1


# ---- row 3: superseded C2 attempts ----------------------------------------------------------
def test_source_c2_superseded(tmp_path, loads):
    store = tmp_path / "c2-readout-store"
    for d in ("0107-a1", "0107-a2", "0109-a1"):
        (store / "superseded" / d).mkdir(parents=True)
        (store / "superseded" / d / "SHA256SUMS").write_text("", encoding="utf-8")
        (store / "superseded" / d / "SUPERSEDED.json").write_text("{}", encoding="utf-8")
    res = nrg.source_c2_superseded(store)
    assert res["status"] == PASS and not res["digests"]
    save(store / "superseded" / "0109-a1" / "hist" / "HIST_fit_b0.npz", **table(3))
    assert nrg.source_c2_superseded(store)["status"] == INC
    assert not [p for p in loads if "superseded" in p]  # fail closed, nothing opened


# ---- rows 4-6, 9: scratch -------------------------------------------------------------------
def test_source_scratch(scratch, expected_roots, loads):
    good = scratch / "0104" / "dry" / "frc1" / "hist"
    t = table(7)
    save(good / "HIST_fit_b0.npz", **t)
    expected_roots([good])
    res = nrg.source_scratch(scratch)
    assert res["status"] == PASS and union([t]) <= res["digests"]
    save(scratch / "misc" / "HIST_tokens.npz", tokens=tokens(1))  # not the C2 table format
    res = nrg.source_scratch(scratch)
    assert res["status"] == PASS
    assert [str(x["path"]).replace("\\", "/").endswith("misc/HIST_tokens.npz")
            for x in res["non_c2_format"]] == [True]
    assert not [p for p in loads if p.endswith("HIST_tokens.npz")]  # listed, not read
    garbage(scratch / "misc2" / "HIST_bad.npz")
    assert nrg.source_scratch(scratch)["status"] == INC


def test_source_scratch_skips_test_trees(scratch, expected_roots, loads):
    good = scratch / "0109-pre" / "livecopy-0115" / "hist"
    save(good / "HIST_val_b0.npz", **table(8))
    expected_roots([good])
    garbage(scratch / "pt" / "test_reg0" / "HIST_fit_b0.npz")
    hidden = table(9)
    save(scratch / "pt" / "test_other0" / "deep" / "HIST_fit_b1.npz", **hidden)
    res = nrg.source_scratch(scratch)
    assert res["status"] == PASS
    assert not union([hidden]) & res["digests"]
    assert not [p for p in loads if "/test_" in p]


def test_source_scratch_expected_roots(scratch, expected_roots):
    good = scratch / "0105" / "dry" / "smoke1" / "hist"
    save(good / "HIST_fit_b0.npz", **table(10))
    expected_roots([good, scratch / "0105" / "dry" / "smoke2" / "hist"])  # the second absent
    assert nrg.source_scratch(scratch)["status"] == INC
    empty = scratch / "0105" / "dry" / "smoke3" / "hist"
    save(empty / "HIST_tokens.npz", tokens=tokens(2))  # exists, but no C2-format file
    expected_roots([good, empty])
    assert nrg.source_scratch(scratch)["status"] == INC
    expected_roots([good])
    assert nrg.source_scratch(scratch)["status"] == PASS


# ---- rows 7-8: parallel stores (R-0116-3, R-0116-4) ----------------------------------------
def frozen(store):
    store.mkdir(parents=True, exist_ok=True)
    (store / "FREEZE.json").write_text('{"schema": "frozen"}\n', encoding="utf-8")
    return store


def test_parallel_absent_and_unfrozen(tmp_path, scratch):
    for tag in ("hws", "x6zc"):
        res = nrg.source_parallel(tmp_path / f"{tag}-store", tag)
        assert res["status"] == PASS and res["present"] is False and not res["digests"]
    store = tmp_path / "hws-store"
    save(store / "hist" / "S0" / "k1.npz", tokens=tokens(3))
    assert nrg.source_parallel(store, "hws")["status"] == INC  # no FREEZE.json
    assert nrg.source_parallel(tmp_path / "x6zc-store", "x6zc")["status"] == PASS
    (tmp_path / "x6zc-store").mkdir()
    assert nrg.source_parallel(tmp_path / "x6zc-store", "x6zc")["status"] == INC


def test_parallel_hws_reader(tmp_path, scratch):
    store = frozen(tmp_path / "hws-store")
    t1, t2 = tokens(4), tokens(5)
    save(store / "hist" / "S0" / "k1.npz", tokens=t1)
    save(store / "hist" / "S0" / "superseded" / "k1.npz", tokens=t2)
    res = nrg.source_parallel(store, "hws")
    assert res["status"] == PASS and res["present"] is True
    assert row_hex(t1) | row_hex(t2) <= res["digests"]
    assert all(h == h.lower() for h in res["digests"])
    save(store / "hist" / "S1" / "notes.npz", w=np.zeros((3, 4)))  # not history-bearing
    assert nrg.source_parallel(store, "hws")["status"] == INC


def test_parallel_hws_dry_scratch(tmp_path, scratch):
    """R-0116-3: reader hws also reads <SCRATCH_ROOT>/hws-dry/hist/** when present."""
    store = frozen(tmp_path / "hws-store")
    save(store / "hist" / "S0" / "k1.npz", tokens=tokens(4))
    dry = tokens(6)
    save(scratch / "hws-dry" / "hist" / "S0" / "d1.npz", tokens=dry)
    res = nrg.source_parallel(store, "hws")
    assert res["status"] == PASS and row_hex(dry) <= res["digests"]
    garbage(scratch / "hws-dry" / "hist" / "S0" / "d2.npz")
    assert nrg.source_parallel(store, "hws")["status"] == INC


@pytest.mark.parametrize("where", ("run/payload.npz", "sealed/k9.npz"))
def test_parallel_payload_or_sealed_is_never_opened(tmp_path, scratch, loads, where):
    store = frozen(tmp_path / "hws-store")
    save(store / "hist" / "S0" / "k1.npz", tokens=tokens(4))
    save(store / where, tokens=tokens(7))
    assert nrg.source_parallel(store, "hws")["status"] == INC
    assert not [p for p in loads if p.endswith(where)]


def test_parallel_x6zc_layout(tmp_path, scratch, loads):
    store = frozen(tmp_path / "x6zc-store")
    names = ("stages/A/qstar_NA.npz", "stages/B/1729/pairs.npz", "stages/C/1729/variants.npz")
    for rel in names:
        save(store / rel, x=np.linspace(0.0, 1.0, 12).reshape(3, 4))
    res = nrg.source_parallel(store, "x6zc")
    assert res["status"] == PASS and not res["digests"]
    assert not [p for p in loads if p.endswith(names)]  # NON_HISTORY: listed, not read
    save(store / "stages" / "A" / "other.npz", x=np.zeros(3))
    assert nrg.source_parallel(store, "x6zc")["status"] == INC


# ---- inventory, build, reservation ----------------------------------------------------------
def names(res):
    return {v["name"] for v in res["violations"]}


def test_inventory_adapter(tmp_path):
    root = tmp_path / "root"
    save(root / "c2nd-store" / "hist" / "HIST_fit_b0.npz", **table(11))  # OWN: not inventoried
    res = nrg.inventory(root, readers={})
    assert not names(res) & {"hws-store", "x6zc-store", "c2nd-store"}
    assert res["status"] == INC  # the frozen READER directories are absent here
    save(frozen(root / "hws-store") / "hist" / "S0" / "k1.npz", tokens=tokens(4))
    assert "hws-store" in names(nrg.inventory(root, readers={}))
    assert "hws-store" not in names(nrg.inventory(root, readers={"hws-store": ["hws"]}))
    save(root / "mystery" / "x.npz", tokens=tokens(5, n=5))
    res = nrg.inventory(root, readers={"hws-store": ["hws"]})
    assert "mystery" in names(res) and "mystery" in res["unlisted"]


# API-AMBIGUITY: build composes the reused readers named in API.md §5.3; to keep the test off
# the real project root those reader functions (module attributes of c2_registry, k4b_registry,
# c1_data and nd_registry) are replaced by empty PASS stubs. The test checks only the ND part:
# version names, exclusive create, the rows 2-9 digests in the C2-format manifest, reload.
def test_build_writes_a_c2_format_manifest(tmp_path, monkeypatch):
    root, store, planted = tmp_path / "root", tmp_path / "store", "ab" * 32
    root.mkdir()
    e = {"sources": [], "problems": [], "predicates": [], "sealed_ranges": {}, "ranges": {}}
    src = {"art": root / "topo-pilot" / "artifacts", "store_a": None, "problems": [],
           "lineage": [], "a": None, "b": [], "c": [], "d": [], "e": e, "k": None}
    x6 = {"status": PASS, "digestset": None, "files": [], "other": [], "base": None}
    inv = {"status": PASS, "inv": {}, "classes": {}, "unlisted": [], "violations": []}
    ok = {"status": PASS, "digests": {planted}, "files": [], "other": [], "non_c2_format": [],
          "present": True}
    stubs = ((cg, "token_sources", src), (cg, "x6_source", x6), (nrg, "inventory", inv),
             (kr, "source_f", []), (kr, "revalidate_coverage", {"ok": True, "missing": []}),
             (kr, "validate_handoff_json", {}), (kr, "summary", {}),
             (c1_data, "build_registry", {"digests": set(), "missing": [], "entries": []}))
    for mod, name, val in stubs:
        monkeypatch.setattr(mod, name, lambda *a, _v=val, **k: _v)
    for name in ("source_c2", "source_c2_superseded", "source_scratch", "source_parallel"):
        monkeypatch.setattr(nrg, name, lambda *a, **k: dict(ok))
    man = nrg.build("ND-REG1", store=store, root=root)
    assert man["status"] == PASS
    on_disk = json.loads((store / "registry" / "ND-REG1.json").read_text(encoding="utf-8"))
    assert on_disk["registry_version"] == "c2nd-reg-v1"
    assert on_disk["protocol_sha256"] == nc.PROTOCOL_SHA256
    assert set(on_disk["nd_sources"]) == {"c2", "c2sup", "c2scratch", "hws", "x6zc"}
    reg = cg.Registry.load(store, "ND-REG1")
    assert planted in reg.digests and reg.manifest == on_disk
    assert planted in nrg.load(store, "ND-REG1").digests
    with pytest.raises(FileExistsError):
        nrg.build("ND-REG1", store=store, root=root)
    with pytest.raises(Exception):
        nrg.build("C2-REG1", store=tmp_path / "s2", root=root)
    with pytest.raises(Exception):
        nrg.build("ND-REG1", store=tmp_path / "s3", root=root, extra={"fit": table(1)})


def reservation(tmp_path, monkeypatch, **change):
    root, store = tmp_path / "root", tmp_path / "root" / "c2nd-store"
    store.mkdir(parents=True, exist_ok=True)
    for name, attr in (("hws-store", "HWS_STORE"), ("x6zc-store", "X6ZC_STORE")):
        monkeypatch.setattr(nc, attr, root / name)
    monkeypatch.setattr(nc, "PROJECT_ROOT", root)
    monkeypatch.setattr(nc, "STORE", store)
    hws = frozen(root / "hws-store")
    rec = {"schema": "c2nd-reservation-v1", "stage": "S1", "job": "0130",
           "no_live_reservation": True, "other_reservations": [],
           "parallel_stores": {"hws-store": {"exists": True,
                                             "freeze_sha256": sha(hws / "FREEZE.json")},
                               "x6zc-store": {"exists": False, "freeze_sha256": None}},
           "coordinator": "c", "utc": "2026-10-26T00:00:00Z"}
    rec.update(change)
    (store / "RESERVATION_S1.json").write_text(json.dumps(rec), encoding="utf-8")
    return nrg.reservation_check(store, "S1", root)["status"]


def test_reservation_check(tmp_path, monkeypatch):
    assert reservation(tmp_path / "a", monkeypatch) == PASS
    assert reservation(tmp_path / "b", monkeypatch, no_live_reservation=False) == AUTH
    assert reservation(tmp_path / "c", monkeypatch, stage="S5") == AUTH
    assert reservation(tmp_path / "d", monkeypatch, schema="c2-reservation-v1") == AUTH
    flags = {"hws-store": {"exists": False, "freeze_sha256": None},
             "x6zc-store": {"exists": False, "freeze_sha256": None}}
    assert reservation(tmp_path / "e", monkeypatch, parallel_stores=flags) == AUTH
    flags["hws-store"] = {"exists": True, "freeze_sha256": "0" * 64}
    assert reservation(tmp_path / "f", monkeypatch, parallel_stores=flags) == AUTH
    store = tmp_path / "g" / "root" / "c2nd-store"
    store.mkdir(parents=True)
    assert nrg.reservation_check(store, "S5", tmp_path / "g" / "root")["status"] == AUTH
