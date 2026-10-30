"""Author B (job 0176): registry readers R2 (c2nd), R4 (hwsb), R5 (dry stores), R7 (own store).

Written from PROTOCOL_HWSC_v1.md section 3.4, API.md section 4 and 18 (R-0176-G4, G9), CONTRACT.json
`registry` and TEST_PLAN.md section 3 only. Every store is synthetic, under pytest's tmp_path.
An audit hook records every open/listing and refuses any access to the real dry stores.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[0] != _HWSC:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402, I001
import hwsc_bind as cb  # noqa: E402
import hwsc_data as cd  # noqa: E402
import hwsc_registry as cr  # noqa: E402
import hwsb_config  # noqa: E402
import hwsb_data  # noqa: E402
import hwsb_dry  # noqa: E402
import hwsb_registry  # noqa: E402
import k4b_data  # noqa: E402
import scores  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    ArtifactStore, Checkpoint, EmissionSpec, LocalFSBackend, ObservationSet)

INCOMPLETE, LINEAGE = "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
DRY = (629911, 629912, 629913)
_REC: list | None = None
_REAL_DRY = "x:/downloads/topo-scratch/hws"


def _audit(event, args):
    if event not in ("open", "os.scandir", "os.listdir") or not args or args[0] is None:
        return
    p = str(args[0]).replace("\\", "/").lower()
    if p.startswith(_REAL_DRY):
        raise PermissionError(f"test guard: real dry store touched: {p}")
    if _REC is not None:
        _REC.append((event, p))


sys.addaudithook(_audit)


@pytest.fixture
def rec():
    global _REC
    _REC = []
    yield _REC
    _REC = None


def _touched(records, fragment, events=("open",)):
    f = fragment.replace("\\", "/").lower()
    return [p for e, p in records if e in events and f in p]


def _has(entries, rel):
    return any(str(e["path"] if isinstance(e, dict) else e).replace("\\", "/").endswith(rel)
               for e in entries)


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _hexes(rng, n):
    return np.array([hashlib.sha256(rng.bytes(16)).hexdigest() for _ in range(n)], "<U64")


def _garbage(path, data=b"not an array file"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _canon_file(path, rows=8, seed=0, key="canon32"):
    path.parent.mkdir(parents=True, exist_ok=True)
    canon = np.random.default_rng(seed).integers(0, 36, (rows, 32)).astype(np.uint8)
    np.savez(path, **{key: canon})
    return set(scores.history_digests(canon))


# ---------------------------------------------------------------- R2: c2nd-store
NON_HISTORY = ["decoys/HEAD_1.npz", "fits/DEC_2.npz", "fits/REFIT_1.npz", "oracle/ORACLE_x.npz",
               "stages/S2/ACT_FIT_0.npz", "stages/S5/ACT_TEST_1.npz",
               "stages/S5/ENDPOINT_NR_1.npz", "stages/S5/ENDPOINT_D_2.npz",
               "stages/S5/ENDPOINT_NM_3.npz", "registry/runs/R/x.npz", "registry/K.npz"]
SEALED = ["sealed/ACT_1.npz", "sealed/deep/READOUT.npy", "sealed/m.pt"]


@pytest.fixture
def c2nd(tmp_path):
    rng = np.random.default_rng(1)
    s = tmp_path / "c2nd-store"
    (s / "hist").mkdir(parents=True)
    a = {k: _hexes(rng, 4) for k in ("digest_H", "digest_Hp", "digest_Hm")}
    a["digest_HY"] = np.array([_hexes(rng, 1)[0], "", _hexes(rng, 1)[0], ""], "<U64")
    a["sequence_id"] = np.arange(100, 104, dtype=np.int64)
    b = {k: _hexes(rng, 3) for k in ("digest_H", "digest_Hp", "digest_Hm", "digest_HY")}
    np.savez(s / "hist" / "HIST_a_b0.npz", **a)
    np.savez(s / "hist" / "HIST_b_b0.npz", **b)
    for rel in NON_HISTORY + SEALED:
        _garbage(s / rel)
    bound = {f"hist/HIST_{n}_b0.npz": _sha(s / "hist" / f"HIST_{n}_b0.npz") for n in "ab"}
    want = {str(x) for t in (a, b) for k, v in t.items() if k.startswith("digest") for x in v}
    return s, bound, want - {""}


def test_r2_pass_digests_seq_ids_and_known_gaps(c2nd, rec):
    s, bound, want = c2nd
    r = cr.source_c2nd(s, bound=bound)
    assert r["status"] == "PASS" and r["other"] == [], r["other"]
    assert set(r["digests"]) == want and "" not in r["digests"]
    assert set(r["seq_ids"]) == {100, 101, 102, 103}
    assert len(r["known_gaps"]) == 1 and "HIST_b_b0" in json.dumps(r["known_gaps"])
    for rel in NON_HISTORY + SEALED:
        assert _has(r["non_history"], rel), rel
        assert not _touched(rec, f"c2nd-store/{rel}"), rel
    assert not _touched(rec, "c2nd-store/sealed")


def test_r2_changed_hash_is_lineage(c2nd):
    s, bound, _ = c2nd
    k = "hist/HIST_a_b0.npz"
    bad = dict(bound, **{k: ("0" if bound[k][0] != "0" else "1") + bound[k][1:]})
    assert cr.source_c2nd(s, bound=bad)["status"] == LINEAGE
    (s / k).write_bytes((s / k).read_bytes() + b"\0")  # one more byte on disk
    assert cr.source_c2nd(s, bound=bound)["status"] == LINEAGE


def test_r2_missing_bound_file_is_incomplete(c2nd):
    s, bound, _ = c2nd
    r = cr.source_c2nd(s, bound=dict(bound, **{"hist/HIST_c_b0.npz": "a" * 64}))
    assert r["status"] == INCOMPLETE and _has(r["other"], "HIST_c_b0.npz")


def test_r2_required_column_missing_is_incomplete(c2nd):
    s, bound, _ = c2nd
    rng = np.random.default_rng(2)
    np.savez(s / "hist" / "HIST_d_b0.npz", digest_H=_hexes(rng, 2), digest_Hp=_hexes(rng, 2))
    bound = dict(bound, **{"hist/HIST_d_b0.npz": _sha(s / "hist" / "HIST_d_b0.npz")})
    assert cr.source_c2nd(s, bound=bound)["status"] == INCOMPLETE


def test_r2_unbound_hist_table_is_read(c2nd):
    s, bound, want = c2nd
    rng = np.random.default_rng(5)
    extra = {k: _hexes(rng, 2) for k in ("digest_H", "digest_Hp", "digest_Hm")}
    np.savez(s / "hist" / "HIST_e_b0.npz", **extra)
    r = cr.source_c2nd(s, bound=bound)
    assert r["status"] == "PASS"
    assert {str(x) for v in extra.values() for x in v} <= set(r["digests"])


@pytest.mark.parametrize("rel", ["superseded/0163-a1/hist/HIST_x_b0.npz", "misc/loose.npy",
                                 "stages/S9/T.npz"])
def test_r2_unexpected_array_files_are_incomplete(c2nd, rel):
    s, bound, _ = c2nd
    _garbage(s / rel)
    r = cr.source_c2nd(s, bound=bound)
    assert r["status"] == INCOMPLETE and _has(r["other"], rel.split("/")[-1])


# ---------------------------------------------------------------- R4: hwsb-store (stage-B shape)
def _stage_b_store(base, with_checkpoint=True):
    """A stage-B-like store: tiny-world artifacts, two ObservationSets and one hist block."""
    s = base
    art = ArtifactStore(LocalFSBackend(s / "artifacts"))
    proc = hwsb_dry.build_tiny_process(art)
    plan = hwsb_config.dry_plan("dry_tiny", "T")
    obs = hwsb_data.make_train_dev(art, proc, plan.masters[0], plan)
    if with_checkpoint:
        art.save(Checkpoint(run_id="r", step=0, observation_id=obs["train"], state=b"fake-state",
                            model_config={}, train_config={}, has_optimizer_state=False),
                 config={"fixture": True}, parents=[obs["train"], obs["dev"]], seed_map={},
                 consumer="learner")
    hwsb_data.save_block(s, hwsb_data.make_block(proc, "LGATE", plan))
    return art, proc, obs


@pytest.fixture(scope="module")
def hwsb_template(tmp_path_factory):
    base = tmp_path_factory.mktemp("tmpl") / "hwsb-store"
    _stage_b_store(base)
    return base


@pytest.fixture
def hwsb(tmp_path, hwsb_template):
    s = tmp_path / "hwsb-store"
    shutil.copytree(hwsb_template, s)
    _garbage(s / "stages" / "S4a" / "CHART_1.npz")
    _garbage(s / "stages" / "S4a" / "INIT_CHART_1.npz")
    _garbage(s / "stages" / "EVAL" / "B1.json", b'{"blinded": true}')
    _garbage(s / "stages" / "EVAL" / "deep" / "ACTS.npz")
    return s


def _paths_of(s, kind):
    root = s / "artifacts" / kind
    return sorted(p for p in root.rglob("*") if p.suffix in (".npz", ".npy", ".pt"))


def test_r4_pass_and_classification(hwsb, rec):
    expected = hwsb_registry.history_inventory(hwsb)
    reg = hwsb_registry.registry_digests(hwsb, expected=expected)
    r = cr.source_hwsb(hwsb, expected=expected)
    assert r["status"] == "PASS" and r["other"] == [], r["other"]
    assert set(r["digests"]) == set(reg["digests"]) and len(r["digests"]) > 0
    for kind in ("WorldSpec", "TransitionSpec", "EmissionSpec", "Checkpoint"):
        files = _paths_of(hwsb, kind)
        assert files, kind
        for f in files:
            assert _has(r["non_history"], f.relative_to(hwsb).as_posix()), f
    for kind in ("WorldSpec", "TransitionSpec", "Checkpoint"):
        assert not _payload_opened(rec, f"hwsb-store/artifacts/{kind}/"), kind
    assert _has(r["non_history"], "stages/S4a/CHART_1.npz")
    assert _has(r["non_history"], "stages/S4a/INIT_CHART_1.npz")
    assert "EVAL" not in json.dumps(r, default=str)
    assert not _touched(rec, "hwsb-store/stages/eval", ("open", "os.scandir", "os.listdir"))


def test_r4_extra_array_file_is_incomplete(hwsb):
    expected = hwsb_registry.history_inventory(hwsb)
    _garbage(hwsb / "misc" / "z.npz")
    r = cr.source_hwsb(hwsb, expected=expected)
    assert r["status"] == INCOMPLETE and _has(r["other"], "misc/z.npz")


@pytest.mark.parametrize("change", ["missing", "renamed"])
def test_r4_missing_or_renamed_hist_is_incomplete(hwsb, change):
    expected = hwsb_registry.history_inventory(hwsb)
    f = hwsb / "hist" / "LGATE.npz"
    if change == "missing":
        f.unlink()
    else:
        f.rename(hwsb / "hist" / "LGATE_old.npz")
    assert cr.source_hwsb(hwsb, expected=expected)["status"] == INCOMPLETE


# ---------------------------------------------------------------- R5: dry stores (file by file)
@pytest.fixture
def dry_root(tmp_path, hwsb_template):
    scr = tmp_path / "scr"
    hws = scr / "hws-dry"
    _garbage(hws / "hist" / "W12.npz")  # R3's: skipped, never opened by R5
    want = _canon_file(hws / "DR12" / "t" / "superseded" / "DRY-t" / "hist" / "DRY" / "DR12.npz")
    b = scr / "hwsb-dry"
    shutil.copytree(hwsb_template, b / "DRB4" / "t1")
    blk = b / "DRB4" / "t1" / "hist" / "LGATE.npz"
    (b / "DRB13" / "t-missing" / "hist").mkdir(parents=True)
    shutil.copy(blk, b / "DRB13" / "t-missing" / "hist" / "CAL.npz")
    (b / "DRB13" / "t-renamed" / "hist").mkdir(parents=True)
    shutil.copy(blk, b / "DRB13" / "t-renamed" / "hist" / "LGATE_renamed.npz")
    planted = _garbage(b / "DRB13" / "t-unreadable" / "hist" / "VAL.npz", b"not an npz")
    stored = _hexes(np.random.default_rng(9), 3)
    (scr / "hwsb-dry-0169").mkdir()
    np.savez(scr / "hwsb-dry-0169" / "digests.npz", digest_x=stored)
    want |= _canon_file(scr / "hwsb-dry-0171" / "test_q" / "pytest" / "h.npz", seed=4)
    with np.load(blk, allow_pickle=False) as z:
        want |= set(scores.history_digests(z["canon32"]))
    want |= {str(x) for x in stored}
    paths = [scr / n for n in ("hws-dry", "hwsb-dry", "hwsb-dry-0169", "hwsb-dry-0171",
                               "hwsc-dry")]
    return scr, paths, planted, want


def _register(monkeypatch, planted):
    entry = {"path": planted.resolve().as_posix(), "bytes": 10, "sha256": _sha(planted)}
    # API-AMBIGUITY: source_dry reads CONTRACT registry.dry_stores.planted_fixtures at call time.
    monkeypatch.setitem(cc.CONTRACT["registry"]["dry_stores"], "planted_fixtures", [entry])


def _obs_digests(art_root, kind):
    """{id: (digests, perm)}: canonical (the EmissionSpec parent's perm) or named-order rows."""
    store = ArtifactStore(LocalFSBackend(art_root))
    out = {}
    for d in sorted((art_root / "ObservationSet").iterdir()):
        meta = store.meta(d.name)
        pid = [p for p in meta.parent_ids if store.meta(p).artifact_type == "EmissionSpec"][0]
        perm = store.load(EmissionSpec, pid, consumer="experiment").symbol_perm
        tok = store.load(ObservationSet, d.name, consumer="experiment").tokens
        rows = (hwsb_data.canonical32(tok, perm) if kind == "canon"
                else np.ascontiguousarray(tok[:, :32], dtype=np.uint8))
        out[d.name] = (set(scores.history_digests(rows)), perm)
    return out


def _payload_opened(records, fragment):
    return [p for p in _touched(records, fragment)
            if p.endswith(("payload.npz", "state.pt", ".npy"))]


def test_r5_pass_file_by_file(dry_root, monkeypatch, rec):
    scr, paths, planted, want = dry_root
    _register(monkeypatch, planted)
    r = cr.source_dry(paths=paths)
    assert r["status"] == "PASS" and r["other"] == [], r["other"]
    assert want <= set(r["digests"])
    assert any(e.get("class") == "PLANTED_FIXTURE" and _has([e], "t-unreadable/hist/VAL.npz")
               for e in r["non_history"])
    assert not _touched(rec, "scr/hws-dry/hist/")
    art = scr / "hwsb-dry" / "DRB4" / "t1" / "artifacts"
    canon, named = _obs_digests(art, "canon"), _obs_digests(art, "named")
    assert canon
    for oid, (dig, perm) in canon.items():
        assert dig <= set(r["digests"]), oid
        if not np.array_equal(np.asarray(perm), np.arange(len(perm))):
            assert named[oid][0] != dig and not named[oid][0] <= set(r["digests"])
    for kind in ("WorldSpec", "TransitionSpec", "Checkpoint"):
        assert not _payload_opened(rec, f"t1/artifacts/{kind}/"), kind
    assert not _touched(rec, "state.pt")


def test_r5_unregistered_planted_file_is_incomplete(dry_root, monkeypatch):
    _, paths, planted, _ = dry_root
    monkeypatch.setitem(cc.CONTRACT["registry"]["dry_stores"], "planted_fixtures", [])
    r = cr.source_dry(paths=paths)
    assert r["status"] == INCOMPLETE and _has(r["other"], "t-unreadable/hist/VAL.npz")


def test_r5_observation_set_without_emission_parent_is_incomplete(dry_root, monkeypatch):
    scr, paths, planted, _ = dry_root
    _register(monkeypatch, planted)
    shutil.rmtree(scr / "hwsb-dry" / "DRB4" / "t1" / "artifacts" / "EmissionSpec")
    assert cr.source_dry(paths=paths)["status"] == INCOMPLETE


def test_r5_absent_optional_and_missing_required(tmp_path):
    r = cr.source_dry(paths=[tmp_path / "hwsc-dry"])
    # API-AMBIGUITY: "present False" is not pinned for the whole source; only PASS is asserted.
    assert r["status"] == "PASS" and r["other"] == []
    assert cr.source_dry(paths=[tmp_path / "hwsb-dry"])["status"] == INCOMPLETE


def test_r5_default_paths_glob_hwsb_dry_star(dry_root, monkeypatch):
    scr, paths, planted, want = dry_root
    _register(monkeypatch, planted)
    extra = _canon_file(scr / "hwsb-dry-x" / "test_inner" / "t.npz", seed=11)
    monkeypatch.setattr(cc, "SCRATCH", scr)
    monkeypatch.setattr(cr, "SCRATCH", scr, raising=False)
    fixed = [p.as_posix() for p in paths] + [(scr / "hwsc-dry-<job>").as_posix()]
    monkeypatch.setitem(cc.CONTRACT["registry"]["dry_stores"], "paths", fixed)
    r = cr.source_dry()
    assert r["status"] == "PASS", r["other"]
    assert extra <= set(r["digests"]) and want <= set(r["digests"])


# ---------------------------------------------------------------- R7: the own store
@pytest.fixture
def own(tmp_path):
    s = tmp_path / "own"
    art = ArtifactStore(LocalFSBackend(s / "artifacts"))
    with cb.bound_stage_c(cb.load_table(which="dry", case="R7", case_dir=tmp_path / "case")):
        plan = cc.dry_plan("dry_tiny", "R7")
        proc = hwsb_dry.build_tiny_process(art, masters=DRY)
        for m in DRY:
            cd.make_train_dev_c(art, proc, m, plan, scope="hwsc-v1")
    canon = np.random.default_rng(21).integers(0, 36, (64, 32)).astype(np.uint8)
    t = k4b_data.history_table(canon, np.arange(77_000, 77_064, dtype=np.int64), "lgate", 0)
    f = s / "superseded" / "a1" / "stages" / "S3" / "HIST_lgate_b0.npz"
    f.parent.mkdir(parents=True)
    np.savez(f, **{k: v for k, v in t.items() if isinstance(v, np.ndarray)})
    return s, t, f


def test_r7_six_observation_sets_and_archived_table(own):
    s, t, _ = own
    assert len(list((s / "artifacts" / "ObservationSet").iterdir())) == 6
    expected = hwsb_registry.history_inventory(s)
    reg = hwsb_registry.registry_digests(s, expected=expected)
    r = cr.source_own(s, expected)
    assert r["status"] == "PASS", r.get("other")
    assert set(reg["digests"]) <= set(r["digests"])
    assert set(t["digest"].tolist()) <= set(r["digests"])
    assert set(t["seq_ids"].tolist()) <= set(r["seq_ids"])


def test_r7_tampered_digest_column_fails(own):
    s, t, f = own
    arrays = {k: v for k, v in t.items() if isinstance(v, np.ndarray)}
    dig = arrays["digest"].copy()
    dig[0] = "f" * 64
    f.unlink()
    np.savez(f, **dict(arrays, digest=dig))
    r = cr.source_own(s, hwsb_registry.history_inventory(s))
    assert r["status"] != "PASS"
