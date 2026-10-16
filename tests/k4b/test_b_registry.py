"""Author B, K4b TEST_PLAN B2, B15, B16, B17 (registry side): recursive inventory and the
NOT_SCANNED/INCOMPLETE classes, C1'-style digest columns (d1, d2 incl. superseded/), the D-2a
reader that never opens sealed tokens, handoff-JSON pre-validation, the non-default artifact
root with an explicit store, and the manifest/load round trip.

Synthetic roots under tmp_path only; module defaults pointing at the real project root are
monkeypatched to the synthetic root wherever a build could otherwise reach them."""

from __future__ import annotations

import builtins
import hashlib
import io
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import c1_registry_sources  # noqa: E402
import k4b_config  # noqa: E402
import k4b_registry  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

INCOMPLETE = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
POOLS = list(k4b_config.CONTRACT["registry"]["d2a"]["pools"])
SEALED = ("test", "testN")


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dig(i) -> str:
    return hashlib.sha256(bytes([i % 256]) * 32 + str(i).encode()).hexdigest()


def outcome(fn, *args, **kwargs):
    """(status, result): a refusal raised as C1GateFailure or a returned status dict."""
    try:
        result = fn(*args, **kwargs)
    except C1GateFailure as exc:
        return exc.status, None
    return result["status"], result


def entry(mapping, root, name):
    for key in (name, str(root / name), root / name, (root / name).as_posix()):
        if key in mapping:
            return mapping[key]
    raise KeyError(name)


def names(paths) -> set:
    return {Path(p).name for p in paths}


# ------------------------------------------------------------------- inventory and classes (B2)

def inventory_root(tmp_path) -> Path:
    root = tmp_path / "root"
    (root / "notes-dir").mkdir(parents=True)
    (root / "notes-dir" / "README.txt").write_text("plans only\n", encoding="utf-8")
    deep = root / "topo-pilot-wt" / "deep" / "nested"
    deep.mkdir(parents=True)
    np.savez(deep / "hist.npz", tokens=np.zeros((5, 33), dtype=np.uint8))
    tmpd = root / "tmp-scratch" / "a" / "b" / "c"
    tmpd.mkdir(parents=True)
    np.savez(tmpd / "arr.npz", x=np.ones((3, 32), dtype=np.int64))
    return root


def test_inventory_is_recursive_and_counts_worktrees_and_temp_dirs(tmp_path):
    root = inventory_root(tmp_path)
    inv = k4b_registry.inventory(root)
    wt = entry(inv, root, "topo-pilot-wt")
    tmpd = entry(inv, root, "tmp-scratch")
    notes = entry(inv, root, "notes-dir")
    assert "hist.npz" in names(wt["history_files"])
    assert "arr.npz" in names(tmpd["history_files"])
    assert not notes["history_files"] and not notes["identity_refs"]
    assert not notes["observation_set_roots"]


def test_classify_not_scanned_only_with_inventory_reason(tmp_path):
    root = inventory_root(tmp_path)
    inv = k4b_registry.inventory(root)
    classes = k4b_registry.classify(inv, {})
    for name in ("notes-dir", "topo-pilot-wt", "tmp-scratch"):
        entry(classes, root, name)  # every top-level directory is classified
    notes = entry(classes, root, "notes-dir")
    assert notes["class"] == "NOT_SCANNED"
    assert notes["reason"]
    # history-bearing sources with no reader are INCOMPLETE, never NOT_SCANNED
    assert entry(classes, root, "topo-pilot-wt")["class"] == "INCOMPLETE"
    assert entry(classes, root, "tmp-scratch")["class"] == "INCOMPLETE"


# ------------------------------------------------------------- C1'-style digest columns (B2)

def c1prime_store(root: Path, with_object=True) -> tuple[Path, set]:
    store = root / "c1prime-store"
    (store / "registry").mkdir(parents=True)
    d1 = [dig(i) for i in range(5)]
    (store / "registry" / "registry_v1.json").write_text(
        json.dumps({"schema": "c1prime-registry-v1", "digests": d1}), encoding="utf-8")
    expected = set(d1)
    files = [(store / "stages" / "S3" / "HIST_cal_b0.npz", 100),
             (store / "superseded" / "0039" / "stages" / "S3" / "HIST_val_b0.npz", 200)]
    for path, base in files:
        path.parent.mkdir(parents=True)
        cols = {k: np.array([dig(base + 10 * j + i) for i in range(4)])
                for j, k in enumerate(("digest_H", "digest_Hp", "digest_Hm"))}
        for v in cols.values():
            expected |= set(v.tolist())
        if with_object:
            # an object column: reading it would need allow_pickle (identity-only access never
            # does: source_d reads the three digest columns only)
            cols["oracle_m32"] = np.array([{"m": 1}], dtype=object)
        np.savez(path, **cols)
    return store, expected


def test_source_d_reads_digest_list_and_columns_incl_superseded(tmp_path, monkeypatch):
    store, expected = c1prime_store(tmp_path)
    monkeypatch.setitem(k4b_config.CONTRACT["registry"], "c1prime_registry_v1_sha256",
                        sha(store / "registry" / "registry_v1.json"))
    sources = k4b_registry.source_d(store)
    union = set().union(*(set(s["digests"]) for s in sources))
    assert union == expected
    for s in sources:
        assert s["sha256"] == sha(s["path"])
    assert any("superseded" in Path(s["path"]).parts for s in sources)


def test_source_d_refuses_unbound_registry_v1(tmp_path):
    store, _ = c1prime_store(tmp_path)  # sha256 differs from CONTRACT ebcebe18...
    with pytest.raises(Exception):
        k4b_registry.source_d(store)


# ----------------------------------------------------------------- D-2a reader (B2, B17)

def d2a_store(root: Path, with_meta=True) -> Path:
    store = root / "d2a-store"
    store.mkdir(parents=True)
    rng = np.random.default_rng(21)
    if with_meta:
        meta = {p: {"n": 10 + i} for i, p in enumerate(POOLS)}
        (store / "pools.json").write_text(json.dumps(meta), encoding="utf-8")
    for i, p in enumerate(POOLS):
        n = 10 + i
        tok = (rng.integers(0, 5, (n, 33)) if p in SEALED
               else rng.integers(5, 36, (n, 33))).astype(np.uint8)
        for path in (store / "pools" / f"{p}.npz", store / f"{p}.npz", store / p / "tokens.npz"):
            path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(path, tokens=tok)
    return store


def test_source_e_never_opens_sealed_token_arrays(tmp_path, monkeypatch):
    store = d2a_store(tmp_path)
    opened, real_open = [], builtins.open

    def spy(file, *args, **kwargs):
        if isinstance(file, (str, os.PathLike)):
            opened.append(Path(os.fspath(file)))
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", spy)
    monkeypatch.setattr(io, "open", spy)
    try:
        res = k4b_registry.source_e(store)
    except C1GateFailure as exc:
        res = {"status": exc.status}
    monkeypatch.undo()
    base = store.resolve()

    def sealed_part(p):
        try:
            rel = p.resolve().relative_to(base)
        except ValueError:
            return False
        return any(Path(part).stem in SEALED for part in rel.parts)

    assert not [p for p in opened if sealed_part(p)]
    assert res["status"] in ("PASS", INCOMPLETE)
    if res["status"] == "PASS":
        assert res["predicates"] == ["sealed_d2a"]
        assert set(res["sealed_ranges"]) == set(SEALED)
    for pool, rng in (res.get("sealed_ranges") or {}).items():
        code, n = POOLS.index(pool) + 1, 10 + POOLS.index(pool)
        assert tuple(int(v) for v in rng) == (code * 2**32, code * 2**32 + n)
    assert (POOLS.index("test") + 1, POOLS.index("testN") + 1) == (17, 19)


def test_source_e_unresolved_pool_inventory_is_incomplete(tmp_path):
    store = d2a_store(tmp_path, with_meta=False)
    status, _ = outcome(k4b_registry.source_e, store)
    assert status == INCOMPLETE


# --------------------------------------------------------------- handoff JSON (B15)

def mailbox(tmp_path, bad=False) -> Path:
    root = tmp_path / "agent-handoff"
    (root / "jobs" / "0001").mkdir(parents=True)
    (root / "jobs" / "0001" / "status.json").write_text(
        json.dumps({"status": "DONE", "row": list(range(32))}), encoding="utf-8")
    if bad:
        (root / "jobs" / "0002").mkdir(parents=True)
        (root / "jobs" / "0002" / "result.json").write_text('{"a": [1, 2,', encoding="utf-8")
    return root


def test_validate_handoff_json_reports_parse_failure(tmp_path):
    root = mailbox(tmp_path, bad=True)
    v = k4b_registry.validate_handoff_json(root)
    assert v["ok"] is False and v["n_files"] == 2
    assert len(v["failures"]) == 1
    assert Path(v["failures"][0]["path"]).name == "result.json"
    assert v["failures"][0]["error"]


def test_source_c_malformed_json_refused_never_empty(tmp_path):
    root = mailbox(tmp_path, bad=True)
    with pytest.raises(C1GateFailure) as exc:
        k4b_registry.source_c(root)
    assert exc.value.status == INCOMPLETE


def test_source_c_valid_mailbox_delegates_unchanged(tmp_path):
    root = mailbox(tmp_path)
    v = k4b_registry.validate_handoff_json(root)
    assert v["ok"] is True and v["n_files"] == 1 and v["failures"] == []
    got = k4b_registry.source_c(root)
    ref = c1_registry_sources.handoff_sources(root)
    assert [s["name"] for s in got] == [s["name"] for s in ref]
    rows = got[0]["reader"](got[0]["path"])
    assert np.array_equal(np.asarray(rows), np.arange(32, dtype=np.uint8)[None, :])


# ------------------------------------------------------------ non-default artifact root (B16)

def artifact_root(tmp_path) -> Path:
    art = tmp_path / "other-artifacts"
    obs = art / "ObservationSet" / "obs1"
    obs.mkdir(parents=True)
    (art / "EmissionSpec" / "em1").mkdir(parents=True)
    (obs / "meta.json").write_text(json.dumps({"parent_ids": ["em1"],
                                               "config": {"split": "train"}}), encoding="utf-8")
    np.savez(obs / "payload.npz", x=np.zeros(1))
    return art


def test_source_a_non_default_root_without_store_refused(tmp_path, monkeypatch):
    art = artifact_root(tmp_path)

    def no_default_store():
        raise AssertionError("main's default ArtifactStore must not be built")

    monkeypatch.setattr(c1_registry_sources, "_store", no_default_store)
    with pytest.raises(C1GateFailure) as exc:
        k4b_registry.source_a(art, store=None)
    assert exc.value.status == "FAIL_TECHNICAL/REGISTRY"


def test_source_a_explicit_store_reads_that_root(tmp_path, monkeypatch):
    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    art = artifact_root(tmp_path)
    store = ArtifactStore(LocalFSBackend(art))
    rng = np.random.default_rng(31)
    perm = rng.permutation(36)
    named = rng.integers(0, 36, (6, 33)).astype(np.uint8)
    seq = np.arange(6, dtype=np.int64) + 77
    loads = []

    def fake_load(self, cls, oid, consumer=None, **kwargs):
        loads.append((self, cls.__name__, oid))
        if cls.__name__ == "ObservationSet":
            return SimpleNamespace(tokens=named, sequence_id=seq)
        return SimpleNamespace(symbol_perm=perm)

    monkeypatch.setattr(ArtifactStore, "load", fake_load)
    monkeypatch.setattr(c1_registry_sources, "_store",
                        lambda: (_ for _ in ()).throw(AssertionError("default store built")))
    sources, seqs = k4b_registry.source_a(art, store=store)
    assert [s["name"] for s in sources] == ["a:ObservationSet/obs1"]
    assert Path(sources[0]["path"]).parent.resolve() == (art / "ObservationSet" / "obs1").resolve()
    canon = sources[0]["reader"](sources[0]["path"])
    assert np.array_equal(canon, c1_registry_sources.canonical32(named, perm))
    assert loads and all(s is store for s, _, _ in loads)
    assert {(c, o) for _, c, o in loads} == {("ObservationSet", "obs1"), ("EmissionSpec", "em1")}
    assert np.array_equal(seqs["obs1"], seq)


# ------------------------------------------------------------- build, manifest and load (B2)

def build_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "root"
    (root / "notes-dir").mkdir(parents=True)
    (root / "notes-dir" / "README.txt").write_text("no histories\n", encoding="utf-8")
    art = root / "topo-pilot" / "artifacts"
    for sub in ("ObservationSet", "EmissionSpec", "HistoryIndex"):
        (art / sub).mkdir(parents=True)
    mailbox(root)
    store, _ = c1prime_store(root, with_object=False)
    monkeypatch.setitem(k4b_config.CONTRACT["registry"], "c1prime_registry_v1_sha256",
                        sha(store / "registry" / "registry_v1.json"))
    d2a_store(root)
    monkeypatch.setattr(c1_registry_sources, "ROOT", root)
    monkeypatch.setattr(c1_registry_sources, "ART", art)
    monkeypatch.setattr(k4b_config, "ROOT", root)
    for name, value in (("ROOT", root), ("ART", art)):
        if hasattr(k4b_registry, name):
            monkeypatch.setattr(k4b_registry, name, value)
    return root


def test_build_on_synthetic_root_is_incomplete_and_written_once(tmp_path, monkeypatch):
    root = build_root(tmp_path, monkeypatch)
    out_dir = tmp_path / "out" / "registry"
    out_dir.mkdir(parents=True)
    # the X4/K4 stores of source (b) are absent here: unreadable sources -> INCOMPLETE
    status, manifest = outcome(k4b_registry.build, "K-REG1", out_dir, root=root)
    assert status == INCOMPLETE
    if manifest is None:
        return
    assert manifest["version"] == "K-REG1" and manifest["status"] == INCOMPLETE
    assert manifest["protocol_sha256"] == k4b_config.CONTRACT["protocol_sha256"]
    mpath, dpath = out_dir / "K-REG1.json", out_dir / "K-REG1_digests.npz"
    assert mpath.exists() and dpath.exists()
    classes = json.dumps(manifest["classes"], default=str)
    for name in ("notes-dir", "agent-handoff", "c1prime-store", "d2a-store", "topo-pilot"):
        assert name in classes
    assert "notes-dir" in json.dumps(manifest["not_scanned"], default=str)
    before = mpath.read_bytes()
    with pytest.raises(Exception):
        k4b_registry.build("K-REG1", out_dir, root=root)
    assert mpath.read_bytes() == before
    digests, _, _, predicates, m2 = k4b_registry.load(out_dir, "K-REG1")
    assert len(digests) == manifest["n_digests"] == m2["n_digests"]
    assert list(predicates) == ["sealed_d2a"]
    with dpath.open("ab") as handle:
        handle.write(b"tamper")
    with pytest.raises(C1GateFailure) as exc:
        k4b_registry.load(out_dir, "K-REG1")
    assert exc.value.status == "FAIL_TECHNICAL/LINEAGE"


def test_build_refuses_unknown_version(tmp_path, monkeypatch):
    root = build_root(tmp_path, monkeypatch)
    out_dir = tmp_path / "out2"
    out_dir.mkdir()
    with pytest.raises(Exception):
        k4b_registry.build("K-REG3", out_dir, root=root)
    assert not (out_dir / "K-REG3.json").exists()
