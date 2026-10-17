"""Author B, correction round 3 (ruling R26, jobs/0051/review.md). D2: `validate_handoff_json`
(API §3, RC7) accepts a UTF-8 BOM like the reused `utf-8-sig` reader; malformed JSON still fails
and `source_c` refuses it (INCONCLUSIVE/REGISTRY_INCOMPLETE). D3: coverage revalidation uses the
sequence ids the source-(a) readers populated (`seqs` is filled lazily inside each reader), via the
pinned `revalidate_coverage(root_art, root)` and `build` on a synthetic root holding every file
`store_sources`/`coverage` read. Unpinned: the nesting of manifest `coverage` and the item format
of `missing`; the tests find the reused report (the dict holding `x4b_seq_in_a`) anywhere in it
and require the missing id's decimal text. ArtifactStore.load is monkeypatched as in
test_b_registry."""

from __future__ import annotations

import hashlib
import json
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
SEQ = np.arange(7_340_000, 7_340_006, dtype=np.int64)  # source-(a) ObservationSet ids
REFS = (7_340_000, 7_340_003, 7_340_005)               # ids referenced by the x4b id-only store
GONE = 7_340_003                                       # removed from source (a) in the miss case
SEQ_MISS = np.where(SEQ == GONE, GONE + 1_000_000, SEQ)


def put(path: Path, **arrays) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **arrays)
    return path


def write_json(path: Path, obj, bom=False, text=None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(obj) if text is None else text
    path.write_bytes((("﻿" if bom else "") + body).encode("utf-8"))
    return path


# ------------------------------------------------------------------------ D2: handoff BOM

def mailbox(base: Path, bom=False, bad=None) -> Path:
    root = base / "agent-handoff"
    write_json(root / "jobs" / "0001" / "status.json", {"row": list(range(32))}, bom=bom)
    if bad is not None:  # bad = True: truncated with a BOM; False: truncated without
        write_json(root / "jobs" / "0002" / "result.json", None, bom=bad, text='{"a": [1, 2,')
    return root


@pytest.mark.parametrize("bom", [True, False])
def test_handoff_json_with_or_without_bom_passes(tmp_path, bom):
    root = mailbox(tmp_path, bom=bom)
    assert (root / "jobs" / "0001" / "status.json").read_bytes().startswith(b"\xef\xbb\xbf") == bom
    v = k4b_registry.validate_handoff_json(root)
    assert v["ok"] is True and v["n_files"] == 1 and v["failures"] == []


def test_bom_json_contributes_through_source_c_like_the_reused_reader(tmp_path):
    root = mailbox(tmp_path, bom=True)
    got = k4b_registry.source_c(root)
    ref = c1_registry_sources.handoff_sources(root)
    assert [s["name"] for s in got] == [s["name"] for s in ref]
    rows = np.asarray(got[0]["reader"](got[0]["path"]))
    assert np.array_equal(rows, np.arange(32, dtype=np.uint8)[None, :])  # not an empty one


@pytest.mark.parametrize("bad_bom", [False, True])
def test_truncated_json_is_registry_incomplete(tmp_path, bad_bom):
    root = mailbox(tmp_path, bom=True, bad=bad_bom)
    v = k4b_registry.validate_handoff_json(root)
    assert v["ok"] is False and v["n_files"] == 2 and v["failures"][0]["error"]
    assert [Path(f["path"]).name for f in v["failures"]] == ["result.json"]
    with pytest.raises(C1GateFailure) as exc:
        k4b_registry.source_c(root)
    assert exc.value.status == INCOMPLETE


# ------------------------------------------------------------- D3: synthetic coverage root

def dig(i) -> str:
    return hashlib.sha256(bytes([i % 256]) * 32 + str(i).encode()).hexdigest()


def earlier_stores(root: Path) -> None:
    """Every file store_sources and coverage read, with consistent identity references."""
    rng = np.random.default_rng(5)

    def tok(n, w=33):
        return rng.integers(5, 36, (n, w)).astype(np.uint8)

    for i, kind in enumerate(("reference", "repetition1", "repetition2", "repetition3")):
        put(root / "x4b2-research-store" / "exports" / f"pool_{kind}_tokens.npz",
            canonical_tokens=tok(3), sequence_id=np.arange(3, dtype=np.int64) + 9_000_000 + 10 * i)
    ids = {}
    for split in ("calibration", "validation"):
        ids[split] = np.array([f"hf-{split}-{i}" for i in range(3)])
        put(root / "x4-history-feas-store" / f"{split}.npz", tokens=tok(3), ids=ids[split])
    k4 = root / "x4-circle-history-feas-store-0015"
    for m in (1729, 2718, 3141):
        put(k4 / f"oracle_{m}.npz", calibration_canonical32=tok(2, 32),
            validation_canonical32=tok(2, 32))
    write_json(k4 / "REFERENCE_CACHE.json", {"entries": []})
    put(root / "x4b-research-store" / "exports" / "pool_test.npz",
        canonical_ids=np.array([f"E4test|{s}" for s in REFS]))
    put(root / "x4-oracle-profile-store-0014" / "profile" / "rows_calibration.npz",
        ids=ids["calibration"][:2])
    put(root / "x4f-gates-research-store" / "exports" / "x4f_gates_1729.npz",
        history_id=np.array([], dtype="<U8"))
    for rel, obj in (("d1-seam-oracle-store/run_0020/report.json", {"note": "none"}),
                     ("chart-diag-store-0023/DIAG.json", {"cases": {}}),
                     ("x2a-stage0-oracle-store/report.json", {"note": "none"})):
        write_json(root / rel, obj)


def artifacts(root: Path, seq: np.ndarray, monkeypatch) -> Path:
    from topo_pilot.contracts import ArtifactStore

    art = root / "topo-pilot" / "artifacts"
    for sub in ("ObservationSet", "EmissionSpec", "HistoryIndex"):
        (art / sub).mkdir(parents=True)
    (art / "EmissionSpec" / "em1").mkdir()
    obs = art / "ObservationSet" / "obs1"
    write_json(obs / "meta.json", {"parent_ids": ["em1"], "config": {"split": "test"}})
    put(obs / "payload.npz", x=np.zeros(1))
    rng = np.random.default_rng(31)
    perm, named = rng.permutation(36), rng.integers(0, 36, (len(seq), 33)).astype(np.uint8)

    def fake_load(self, cls, oid, consumer=None, **kwargs):
        if cls.__name__ == "ObservationSet" and oid == "obs1":
            return SimpleNamespace(tokens=named, sequence_id=np.asarray(seq))
        if cls.__name__ == "EmissionSpec" and oid == "em1":
            return SimpleNamespace(symbol_perm=perm)
        raise KeyError(f"{cls.__name__}/{oid}")

    monkeypatch.setattr(ArtifactStore, "load", fake_load)
    return art


def coverage_root(tmp_path, monkeypatch, seq) -> tuple[Path, Path]:
    root = tmp_path / "root"
    art = artifacts(root, seq, monkeypatch)
    earlier_stores(root)
    mailbox(root)
    c1p = root / "c1prime-store"
    reg = write_json(c1p / "registry" / "registry_v1.json",
                     {"schema": "c1prime-registry-v1", "digests": [dig(i) for i in range(4)]})
    put(c1p / "stages" / "S3" / "HIST_cal_b0.npz",
        **{k: np.array([dig(50 + 10 * j + i) for i in range(3)])
           for j, k in enumerate(("digest_H", "digest_Hp", "digest_Hm"))})
    monkeypatch.setitem(k4b_config.CONTRACT["registry"], "c1prime_registry_v1_sha256",
                        hashlib.sha256(reg.read_bytes()).hexdigest())
    d2a = root / "d2a-store"
    write_json(d2a / "pools.json", {p: {"n": 10 + i} for i, p in enumerate(POOLS)})
    for i, p in enumerate(POOLS):
        lo, hi = (0, 5) if p in SEALED else (5, 36)
        put(d2a / "pools" / f"{p}.npz",
            tokens=np.random.default_rng(i).integers(lo, hi, (10 + i, 33)).astype(np.uint8))
    monkeypatch.setattr(c1_registry_sources, "ROOT", root)
    monkeypatch.setattr(c1_registry_sources, "ART", art)
    monkeypatch.setattr(k4b_config, "ROOT", root)
    for name, value in (("ROOT", root), ("ART", art)):
        if hasattr(k4b_registry, name):
            monkeypatch.setattr(k4b_registry, name, value)
    return root, art


def dicts(obj):
    if isinstance(obj, dict):
        yield obj
        obj = list(obj.values())
    if isinstance(obj, (list, tuple)):
        for v in obj:
            yield from dicts(v)


def build_manifest(tmp_path, root) -> dict:
    out = tmp_path / "out"
    out.mkdir()
    try:
        return k4b_registry.build("K-REG1", out, root=root)
    except C1GateFailure:
        path = out / "K-REG1.json"  # API §3: an incomplete build still writes its manifest
        if not path.exists():
            pytest.fail("build wrote no K-REG1 manifest with its coverage results")
        return json.loads(path.read_text(encoding="utf-8"))


def reports(manifest) -> list:
    reps = [d for d in dicts(manifest["coverage"]) if "x4b_seq_in_a" in d]
    assert reps, "the reused coverage(seqs_a, hist_ids, root) report is recorded in coverage"
    return reps


# ---------------------------------------------------------------- D3: revalidate_coverage

def test_revalidate_coverage_complete_when_source_a_ids_cover_refs(tmp_path, monkeypatch):
    root, art = coverage_root(tmp_path, monkeypatch, SEQ)
    res = k4b_registry.revalidate_coverage(art, root=root)
    assert res["ok"] is True and list(res["missing"]) == [], res


def test_revalidate_coverage_reports_the_removed_id(tmp_path, monkeypatch):
    root, art = coverage_root(tmp_path, monkeypatch, SEQ_MISS)
    res = k4b_registry.revalidate_coverage(art, root=root)
    assert res["ok"] is False
    text = json.dumps(res["missing"], default=str)
    assert str(GONE) in text
    assert not [s for s in REFS if s != GONE and str(s) in text]  # present ids are not missing


# ------------------------------------------------------------------------ D3: build manifest

def test_build_coverage_complete_with_no_seq_in_a_problem(tmp_path, monkeypatch):
    root, _ = coverage_root(tmp_path, monkeypatch, SEQ)
    manifest = build_manifest(tmp_path, root)
    for rep in reports(manifest):
        assert (rep["x4b_seq_in_a"]["n"], rep["x4b_seq_in_a"]["missing"]) == (len(REFS), 0)
        assert rep["x4f_seq_in_a"]["missing"] == 0 and rep["complete"] is True
    for d in dicts(manifest):
        for key in ("problems", "missing"):
            items = d.get(key)
            if isinstance(items, list):
                assert not [p for p in items if "_seq_in_a" in str(p) or "73400" in str(p)]


def test_build_coverage_reports_the_missing_id(tmp_path, monkeypatch):
    root, _ = coverage_root(tmp_path, monkeypatch, SEQ_MISS)
    manifest = build_manifest(tmp_path, root)
    assert manifest["status"] == INCOMPLETE
    reps = reports(manifest)
    # exactly the removed id is missing; the other referenced ids resolve to source (a)
    assert all(r["x4b_seq_in_a"]["missing"] == 1 and r["complete"] is False for r in reps)
    assert str(GONE) in json.dumps(manifest["coverage"], default=str)
