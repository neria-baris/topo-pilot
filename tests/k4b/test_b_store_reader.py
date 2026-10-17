"""Author B, correction round 4: coordinator ruling R28 (API §16, defect D5). K4b's own store
`k4b-store` gets the dedicated reader "k": `source_k(store_root) -> {"sources", "derived", "other",
"status"}`. Derived registry lineage records (registry/K-REG*.json, registry/K-REG*_digests.npz,
the same under superseded/*/registry/) are listed in `derived` with their sha256, contribute
nothing and are never INCOMPLETE. History-bearing npz under stages/ and superseded/*/stages/ are
`sources`, with their sha256. Any other history-bearing, identity-bearing or unreadable file is
`other` and makes the k4b-store class INCOMPLETE through `build`. `OWN_READERS["k4b-store"] == "k"`
keeps it out of the generic deep scan. A raising `source_k` makes k4b-store INCOMPLETE, never an
empty contribution.

Unpinned by API §16: the item format of `derived`/`sources`/`other` (the tests find an item by any
str value naming the file, absolute or relative to the store or its root, and look for the file's
sha256 anywhere in the item); the `status` value of a clean store (accepted: "PASS" or "OK"; a
stray must give neither); the layout of manifest `k4b_store` (the tests require the sha256s in it);
the source format of a stage table (its digests are not checked here). Build roots reuse
test_b_registry_fixes.coverage_root (every file store_sources/coverage read)."""

from __future__ import annotations

import builtins
import hashlib
import io
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in [REPO / s for s in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
                              "tools/x4_circle_history", "tools/x4_oracle_profile")] + [HERE]:
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import k4b_registry  # noqa: E402
import test_b_registry_fixes as fx  # noqa: E402

INCOMPLETE = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
CLEAN = ("PASS", "OK")
KS = "k4b-store"


def put(path: Path, **arrays) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **arrays)
    return path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def derived_files(store: Path) -> list:
    """The three D5 lineage records: K-REG1 manifest and digests, and the superseded digests."""
    man = text(store / "registry" / "K-REG1.json",
               json.dumps({"version": "K-REG1", "status": "PASS", "n_digests": 6}))
    cur = put(store / "registry" / "K-REG1_digests.npz",
              digests=np.array([fx.dig(i) for i in range(6)]),
              seq_ids=np.arange(100, 106, dtype=np.int64))
    old = put(store / "superseded" / "0051" / "registry" / "K-REG1_digests.npz",
              digests=np.array([fx.dig(i) for i in range(5)]),
              seq_ids=np.arange(100, 105, dtype=np.int64))
    return [man, cur, old]


def free_files(store: Path) -> None:
    """Category (c): not history files, ignored."""
    text(store / "FREEZE.json", json.dumps({"frozen": True}))
    text(store / "SHA256SUMS", "0" * 64 + "  FREEZE.json\n")
    text(store / "logs" / "run.log", "notes only\n")
    text(store / "operations" / "op.txt", "notes only\n")


def stage_tables(store: Path) -> list:
    rng = np.random.default_rng(28)
    return [put(store / "stages" / "S3" / "HIST_cal_b0.npz",
                canon32=rng.integers(5, 36, (6, 32)).astype(np.uint8)),
            put(store / "superseded" / "0049" / "stages" / "S3" / "HIST_val_b0.npz",
                canon32=rng.integers(5, 36, (4, 32)).astype(np.uint8))]


def stray(path: Path, kind: str) -> Path:
    if kind == "junk":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"not an npz archive\n" * 4)
        return path
    arrays = {"ids": {"seq_ids": np.arange(7, 12, dtype=np.int64)},
              "tokens": {"tokens": np.zeros((4, 33), dtype=np.uint8)},
              "canon": {"canon32": np.full((3, 32), 9, dtype=np.uint8)}}[kind]
    return put(path, **arrays)


def names_file(item, store: Path, path: Path) -> bool:
    if isinstance(item, dict):
        vals = [v for v in item.values() if isinstance(v, (str, Path))]
    else:
        vals = [item] if isinstance(item, (str, Path)) else []
    want = path.resolve()
    for v in vals:
        try:
            p = Path(v)
            cands = (p,) if p.is_absolute() else (store / p, store.parent / p)
            if any(c.resolve() == want for c in cands):
                return True
        except (OSError, ValueError):
            continue
    return False


def find(items, store: Path, path: Path) -> list:
    return [it for it in items if names_file(it, store, path)]


def has_sha(item, path: Path) -> bool:
    return sha(path) in json.dumps(item, default=str)


def is_under(path, base: Path) -> bool:
    try:
        Path(path).resolve().relative_to(base.resolve())
    except (ValueError, OSError):
        return False
    return True


def entry(mapping, root: Path, name: str):
    for key in (name, str(root / name), (root / name).as_posix()):
        if key in mapping:
            return mapping[key]
    return None


# ------------------------------------------------------------------ source_k on a store

def test_derived_registry_records_are_listed_with_sha256(tmp_path):
    store = tmp_path / "root" / KS
    files = derived_files(store)
    free_files(store)
    res = k4b_registry.source_k(store)
    assert {"sources", "derived", "other", "status"} <= set(res)
    assert len(res["derived"]) == 3, res["derived"]
    for f in files:
        hits = find(res["derived"], store, f)
        assert len(hits) == 1 and has_sha(hits[0], f), (f, res["derived"])
        assert not find(res["sources"], store, f)
    assert list(res["sources"]) == []  # derived records contribute nothing; free files ignored
    assert list(res["other"]) == []
    assert res["status"] in CLEAN


def test_stage_history_tables_are_sources_with_sha256(tmp_path):
    store = tmp_path / "root" / KS
    derived = derived_files(store)
    tables = stage_tables(store)
    free_files(store)
    res = k4b_registry.source_k(store)
    for f in tables:
        hits = find(res["sources"], store, f)
        assert hits and all(has_sha(h, f) for h in hits), (f, res["sources"])
        assert not find(res["derived"], store, f) and not find(res["other"], store, f)
    for f in derived:
        assert find(res["derived"], store, f) and not find(res["sources"], store, f)
    assert list(res["other"]) == []
    assert res["status"] in CLEAN


STRAYS = [(("misc", "x.npz"), "ids"),
          (("misc", "deep", "h.npz"), "tokens"),
          (("registry", "copy_digests.npz"), "ids"),         # not a K-REG* record
          (("superseded", "0051", "exports", "h.npz"), "canon"),
          (("misc", "broken.npz"), "junk")]                  # unreadable


@pytest.mark.parametrize("rel,kind", STRAYS)
def test_stray_file_is_other_and_not_clean(tmp_path, rel, kind):
    store = tmp_path / "root" / KS
    derived_files(store)
    stage_tables(store)
    f = stray(store.joinpath(*rel), kind)
    res = k4b_registry.source_k(store)
    assert find(res["other"], store, f), res["other"]
    assert not find(res["derived"], store, f) and not find(res["sources"], store, f)
    assert res["status"] not in CLEAN


# ------------------------------------------------------------- exclusion from generic scan

def spy(mp, seen: list) -> None:
    real_open, real_load = builtins.open, np.load

    def note(file):
        if isinstance(file, (str, bytes, os.PathLike)):
            seen.append(Path(os.fsdecode(os.fspath(file))))

    def spy_open(file, *args, **kwargs):
        note(file)
        return real_open(file, *args, **kwargs)

    def spy_load(file, *args, **kwargs):
        note(file)
        return real_load(file, *args, **kwargs)

    mp.setattr(builtins, "open", spy_open)
    mp.setattr(io, "open", spy_open)
    mp.setattr(np, "load", spy_load)


def test_own_readers_excludes_k4b_store_from_the_deep_scan(tmp_path, monkeypatch):
    assert k4b_registry.OWN_READERS["k4b-store"] == "k"
    root = tmp_path / "root"
    store = root / KS
    derived_files(store)
    stage_tables(store)
    stray(store / "misc" / "x.npz", "ids")
    put(root / "work-dir" / "h.npz", tokens=np.zeros((3, 33), dtype=np.uint8))
    seen: list = []
    with monkeypatch.context() as mp:
        spy(mp, seen)
        inv = k4b_registry.inventory(root, exclude=tuple(k4b_registry.OWN_READERS))
    assert not [p for p in seen if is_under(p, store)]
    e = entry(inv, root, KS)
    if e is not None:
        assert not e["history_files"] and not e["identity_refs"]
        assert not e["observation_set_roots"]
    assert "h.npz" in {Path(p).name for p in entry(inv, root, "work-dir")["history_files"]}


# ------------------------------------------------------------------- through build

def k4b_class(manifest, root: Path) -> dict:
    c = entry(manifest["classes"], root, KS)
    if c is None:
        pytest.fail(f"manifest classes has no {KS} entry: {sorted(manifest['classes'])}")
    return c


def test_build_with_only_derived_records_is_not_incomplete(tmp_path, monkeypatch):
    root, _ = fx.coverage_root(tmp_path, monkeypatch, fx.SEQ)
    store = root / KS
    files = derived_files(store)
    free_files(store)
    manifest = fx.build_manifest(tmp_path, root)
    assert k4b_class(manifest, root)["class"] != "INCOMPLETE"
    assert "k4b_store" in manifest
    record = json.dumps(manifest["k4b_store"], default=str)
    assert all(sha(f) in record for f in files)


@pytest.mark.parametrize("kind", ["ids", "tokens"])
def test_build_with_stray_file_makes_k4b_store_incomplete(tmp_path, monkeypatch, kind):
    root, _ = fx.coverage_root(tmp_path, monkeypatch, fx.SEQ)
    store = root / KS
    derived_files(store)
    f = stray(store / "misc" / "x.npz", kind)
    manifest = fx.build_manifest(tmp_path, root)
    c = k4b_class(manifest, root)
    assert c["class"] == "INCOMPLETE" and c["reason"]
    assert manifest["status"] == INCOMPLETE
    assert sha(f) in json.dumps(manifest.get("k4b_store"), default=str)


@pytest.mark.parametrize("exc", [OSError, RuntimeError])
def test_raising_source_k_makes_k4b_store_incomplete(tmp_path, monkeypatch, exc):
    root, _ = fx.coverage_root(tmp_path, monkeypatch, fx.SEQ)
    store = root / KS
    derived_files(store)
    stage_tables(store)
    calls: list = []
    real = k4b_registry.source_k

    def boom(*args, **kwargs):
        calls.append(args)
        raise exc("simulated partial read of k4b-store")

    monkeypatch.setattr(k4b_registry, "source_k", boom)
    for name, value in list(vars(k4b_registry).items()):  # reader tables bound at import
        if isinstance(value, dict):
            for key, fn in list(value.items()):
                if fn is real:
                    monkeypatch.setitem(value, key, boom)
    manifest = fx.build_manifest(tmp_path, root)
    assert calls, "build never called reader k"
    c = k4b_class(manifest, root)
    assert c["class"] == "INCOMPLETE" and c["reason"]  # never an empty contribution
    assert manifest["status"] == INCOMPLETE
