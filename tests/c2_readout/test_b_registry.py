"""Author B (job 0101): T-REG and T-NAMESPACE (RC-11; three tests) (C2-FROZEN-v1 §13.3, §5.2,
§5.3, §11 item 7; API.md §4.4, §5, §16, §18).

Written from the protocol, API.md and CONTRACT.json only; tools/c2_readout/*.py never read.
Every store, registry, mailbox and project root is synthetic under pytest's tmp_path; the
c2_config path constants are redirected there so no real store is opened or hashed.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402  (first: the sys.path convention)
import c2_data as cd  # noqa: E402
import c2_driver as cdr  # noqa: E402
import c2_registry as cg  # noqa: E402
import x6s1_registry as xr  # noqa: E402

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
PROTO = "4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8"
PATHS = {"PROJECT_ROOT": "", "STORE": "c2-readout-store", "WORKTREE": "topo-pilot-c2",
         "MAILBOX": "agent-handoff", "ARTIFACT_ROOT": "topo-pilot/artifacts",
         "C1P_STORE": "c1prime-store", "X6S1_STORE": "x6-stage1-store",
         "K4_FREEZE": "x4-circle-history-feas-store-0015/FREEZE.json"}


def _isolate(monkeypatch, root):
    for name, rel in PATHS.items():
        for mod in (cc, cd, cg, cdr):
            monkeypatch.setattr(mod, name, root / rel, raising=False)
        key = name.lower().replace("c1p_", "c1prime_")  # the CONTRACT.json "paths" keys
        monkeypatch.setitem(cc.CONTRACT["paths"], key, str(root / rel))
    return root


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else json.dumps(data).encode())
    return _sha(path)


def _hist(seed, n):
    return np.random.default_rng(seed).integers(0, 36, size=(n, 32)).astype(np.uint8)


def _table(seed, n, id0):
    canon = _hist(seed, n)
    ids = np.arange(id0, id0 + n, dtype=np.int64)
    return cd.history_table(canon, ids, np.zeros(n, dtype=np.int64))


def _digests(table):
    return set().union(*(set(np.asarray(table[k]).tolist()) for k in
                         ("digest_H", "digest_Hp", "digest_Hm", "digest_HR")))


class _Reg:
    """Registry stand-in for separation (API-AMBIGUITY: API.md 5.3 fixes the attributes, not
    the sealed_ranges layout; the K4b layout {pool: (lo, hi)} is used)."""

    def __init__(self, digests=(), ranges=None):
        self.digests, self.x6, self.manifest = set(digests), None, {}
        self.sealed_ranges, self.predicates = dict(ranges or {}), ["sealed_d2a"]

    def contains(self, hex_digests):
        return np.array([h in self.digests for h in np.asarray(hex_digests).tolist()], bool)


# ---- T-REG: separation ----
def _tables():
    fit, feas, val = _table(1, 12, 10_000), _table(2, 6, 20_000), _table(3, 6, 30_000)
    return {"fit": fit, "feas": feas, "val": val}


def test_separation_pass_with_duplicates_kept():
    t = _tables()
    canon = t["fit"]["canonical"].copy()
    canon[11] = canon[0]  # a within-split duplicate history (distinct sequence id)
    t["fit"] = cd.history_table(canon, t["fit"]["sequence_id"], t["fit"]["panel"])
    res = cg.separation(_Reg({"f" * 64}), t)
    assert res["status"] == "PASS" and res["seq_ids"] == "PASS"
    assert res["duplicates"]["fit"] >= 1 and res["duplicates"]["val"] == 0


def test_collision_with_R_is_lineage():
    t = _tables()
    res = cg.separation(_Reg({str(t["fit"]["digest_HR"][3])}), t)
    assert res["status"] == LINEAGE and res["collisions"]["fit_R"] >= 1


def test_cross_split_collision_and_seq_id_overlap_are_lineage():
    t = _tables()
    canon = t["val"]["canonical"].copy()
    canon[2] = t["fit"]["canonical"][5]
    t["val"] = cd.history_table(canon, t["val"]["sequence_id"], t["val"]["panel"])
    res = cg.separation(_Reg(), t)
    hits = [v for k, v in res["collisions"].items() if "fit" in k and "val" in k]
    assert res["status"] == LINEAGE and hits and max(hits) >= 1
    t = _tables()
    ids = t["val"]["sequence_id"].copy()
    ids[0] = t["fit"]["sequence_id"][4]
    t["val"] = cd.history_table(t["val"]["canonical"], ids, t["val"]["panel"])
    res = cg.separation(_Reg(), t)
    assert res["status"] == LINEAGE and res["seq_ids"] != "PASS"
    res = cg.separation(_Reg(ranges={"d2a_sealed": (10_005, 10_006)}), _tables())
    assert res["status"] == LINEAGE  # an id inside a sealed D-2a range


def test_sealed_d2a_predicate_hit_is_incomplete():
    t = _tables()
    canon = t["feas"]["canonical"].copy()
    canon[1] = 1  # every symbol in {0..4}: the sealed D-2a alphabet
    t["feas"] = cd.history_table(canon, t["feas"]["sequence_id"], t["feas"]["panel"])
    res = cg.separation(_Reg(), t)
    assert res["status"] == INCOMPLETE and res["predicate"]["hits"] >= 1


# ---- T-REG: inventory against the frozen table ----
def _npz(path, **arrays):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **arrays)


def test_inventory_violations_and_admitted_empty_directory(tmp_path, monkeypatch):
    root = _isolate(monkeypatch, tmp_path / "proj")
    (root / "agent-handoff").mkdir(parents=True)
    (root / "tmp-0999").mkdir()  # unlisted and empty: admitted as a new exclusion
    _write(root / "circular-audit-store" / "record.json", {"kind": "metric"})
    _npz(root / "coord-scratch" / "hist.npz", tokens=np.zeros((5, 33), np.int64))  # EXCLUSION
    _npz(root / "brand-new-store" / "a.npz", canonical32=np.zeros((5, 32), np.uint8))
    res = cg.inventory(root)
    bad = {v["name"] for v in res["violations"]}
    assert res["status"] == INCOMPLETE
    assert {"coord-scratch", "brand-new-store"} <= bad
    assert "tmp-0999" in res["unlisted"] and "tmp-0999" not in bad
    assert "circular-audit-store" not in bad


def test_inventory_admits_an_unlisted_empty_directory_alone(tmp_path, monkeypatch):
    root = _isolate(monkeypatch, tmp_path / "proj")
    (root / "tmp-0998").mkdir(parents=True)
    res = cg.inventory(root)
    assert "tmp-0998" in res["unlisted"]
    assert "tmp-0998" not in {v["name"] for v in res["violations"]}


# ---- T-REG: reader x6 on a synthetic X6-style store with its own REG manifest ----
def _x6_store(store):
    base = _hist(50, 6)
    xr._write_reg(store, "X6-REG2", [("synthetic", "synthetic", [xr.row_digests(base)])])
    pools = {"smoke": np.random.default_rng(51).integers(0, 36, (4, 33)).astype(np.uint8),
             "os": np.random.default_rng(52).integers(0, 36, (2, 33)).astype(np.int64),
             "e0": np.random.default_rng(53).integers(0, 36, (3, 32)).astype(np.int64)}
    (store / "pools" / "npy").mkdir(parents=True)
    np.save(store / "pools" / "npy" / "smoke.npy", pools["smoke"])
    _npz(store / "pools" / "ObservationSet" / "abc" / "payload.npz", tokens=pools["os"])
    _npz(store / "stages" / "E0" / "partners_test_NA_t32.npz", tokens=pools["e0"])
    dig = _hist(54, 2)
    hexes = np.array([hashlib.sha256(r.tobytes()).hexdigest() for r in dig])
    _npz(store / "tables" / "designed.npz", digest_H=hexes)
    _npz(store / "run" / "model.npz", T_base=np.eye(4))  # not history-bearing
    return base, pools, dig, _sha(store / "registry" / "X6-REG2.json")


def test_x6_source_binding_and_history_arrays(tmp_path, monkeypatch):
    store = tmp_path / "x6s"
    base, pools, dig, man_sha = _x6_store(store)
    res = cg.x6_source(store, tmp_path / "runs_a")
    assert res["status"] == LINEAGE  # the synthetic manifest is not the frozen X6-REG2
    monkeypatch.setitem(cc.CONTRACT["registry"], "x6_reg2_manifest_sha256", man_sha)
    res = cg.x6_source(store, tmp_path / "runs_b")
    assert res["status"] == "PASS" and res["base"]["manifest_sha256"] == man_sha
    ds = res["digestset"]
    for tok in (base, pools["smoke"][:, :32], pools["os"][:, :32], pools["e0"], dig):
        assert ds.contains(xr.row_digests(tok)).all()
    assert not ds.contains(xr.row_digests(_hist(55, 3))).any()
    rows = {Path(f["path"]).name: f["rows"] for f in res["files"]}
    assert rows.get("smoke.npy") == 4 and "model.npz" not in rows
    (store / "pools" / "npy" / "broken.npy").write_bytes(b"not an array")
    res = cg.x6_source(store, tmp_path / "runs_c")
    assert res["status"] == INCOMPLETE
    assert any(Path(o["path"]).name == "broken.npy" for o in res["other"])


# ---- T-REG: builds ----
def test_build_refuses_existing_output(tmp_path, monkeypatch):
    root = _isolate(monkeypatch, tmp_path / "proj")
    store = root / "c2-readout-store"
    _write(store / "registry" / "C2-REG1.json", {"version": "C2-REG1"})
    with pytest.raises(FileExistsError):
        cg.build("C2-REG1", store, root=root)


def test_build_unreadable_sources_incomplete_and_R_prime_has_four_roles(tmp_path,
                                                                         monkeypatch):
    root = _isolate(monkeypatch, tmp_path / "proj")
    (root / "agent-handoff").mkdir(parents=True)
    _, _, _, man_sha = _x6_store(root / "x6-stage1-store")
    monkeypatch.setitem(cc.CONTRACT["registry"], "x6_reg2_manifest_sha256", man_sha)
    store = root / "c2-readout-store"
    (store / "registry").mkdir(parents=True)
    tabs = _tables()
    # API-AMBIGUITY: API.md 5.3 build(extra=...) holds "the FIT, FEAS and VAL history tables";
    # passed keyed by split, as separation's `tables`.
    man = cg.build("C2-REG2", store, root=root, extra=tabs)
    assert man["status"] == INCOMPLETE  # no c1prime-store, mailbox sources, d2a-store, ...
    with np.load(store / "registry" / "C2-REG2_digests.npz", allow_pickle=False) as z:
        got = set(z["digests"].astype(str).tolist())
    for split in ("fit", "feas", "val"):
        assert _digests(tabs[split]) <= got, split
    saved = json.loads((store / "registry" / "C2-REG2.json").read_text(encoding="utf-8"))
    assert saved["registry_version"] == "c2-reg-v1" and saved["status"] == INCOMPLETE


def test_registry_load_rehash_mismatch_is_lineage(tmp_path, monkeypatch):
    root = _isolate(monkeypatch, tmp_path / "proj")
    reg = root / "c2-readout-store" / "registry"
    reg.mkdir(parents=True)
    np.savez_compressed(reg / "C2-REG1_digests.npz", digests=np.array(["a" * 64]),
                        seq_ids=np.array([1], dtype=np.int64))
    _write(reg / "C2-REG1.json", {"version": "C2-REG1", "status": "PASS",
                                  "digest_file_sha256": "0" * 64, "x6": {"runs": []}})
    with pytest.raises(RuntimeError) as info:
        cg.Registry.load(root / "c2-readout-store", "C2-REG1")
    assert getattr(info.value, "status", None) == LINEAGE


# ---- T-REG: frozen inventory, landmarks, basetemp ----
WORKTREES = ("c1p", "c2", "causal-planning-codex", "circle-history-k4", "d1", "d2a", "int",
             "k4b", "reorg", "verify", "x2a", "x4-history-feas", "x4b", "x6", "x6s1")
TMPS = ("0027", "0028", "0029", "0031", "0032", "0033", "0034", "0035c", "0036", "0039",
        "0039c", "0041", "0042", "0042c", "0044", "0045", "0046", "0046r", "0047")
READERS = {"agent-handoff": ["c"], "c1prime-store": ["d"], "chart-diag-store-0023": ["b"],
           "d1-seam-oracle-store": ["b"], "d2a-store": ["e"], "k4b-store": ["k"],
           "topo-pilot": ["a"], "x2a-stage0-oracle-store": ["b"],
           "x4-circle-history-feas-store-0015": ["b"], "x4-history-feas-store": ["b"],
           "x4-oracle-profile-store-0014": ["b"], "x4b-research-store": ["b"],
           "x4b2-research-store": ["b"], "x4f-gates-research-store": ["b"],
           "x5g1-research-store": ["f"], "x5g1t-research-store": ["f"],
           "x5g1t-fixture-run": ["f"], "x6-stage1-store": ["x6"]}
EXCLUSIONS = ("circular-audit-store", "coord-scratch", "docs-0024-store", "int-0021-store",
              "int-0022-store", "x5g1-techbench-store", "x6-stage0-oracle-store")


def test_contract_inventory_lists_every_section_18_directory():
    # API-AMBIGUITY: API.md 18 says "tmp-0028 ... tmp-0047 (19 directories: ...)" but names
    # 18; with tmp-0027 the table has 19 tmp rows, which is what CONTRACT.json holds.
    inv = cc.CONTRACT["registry"]["inventory"]
    excl = set(EXCLUSIONS) | {f"tmp-{t}" for t in TMPS} | {f"topo-pilot-{w}" for w in WORKTREES}
    assert set(inv) == set(READERS) | excl | {"c2-readout-store"}
    for name, tags in READERS.items():
        assert inv[name] == {"decision": "READER", "readers": tags}, name
    for name in excl:
        assert inv[name]["decision"] == "EXCLUSION" and inv[name]["reason"], name
    assert inv["c2-readout-store"]["decision"] == "OWN"
    assert cg.INVENTORY == inv


def test_c1prime_landmarks_enter_R_through_reader_d():
    h = cc.CONTRACT["hashes"]["c1prime_hist"]
    assert h["c1prime-store/HIST_cal_b0.npz"] == (
        "d80ad5f42e333b4dc910667c0465cf03adc66518a22e961dec50a8eca2d5ba5e")  # 512 landmarks
    assert set(h) == {f"c1prime-store/HIST_{s}.npz" for s in ("cal_b0", "cal_b1", "val_b0")}
    assert cc.CONTRACT["registry"]["inventory"]["c1prime-store"]["readers"] == ["d"]


def test_pytest_basetemp_is_outside_the_project_root(tmp_path):
    tp, root = Path(tmp_path).resolve(), Path(cc.PROJECT_ROOT).resolve()
    assert root not in tp.parents and tp != root


# ---- T-NAMESPACE ----
def _ns_root(tmp_path, monkeypatch):
    root = _isolate(monkeypatch, tmp_path / "proj")
    pin = _write(root / "topo-pilot-c2" / "tools" / "c2_readout" / "CONTRACT.json",
                 {"scope": "c2-v1"})
    store = root / "c2-readout-store"
    lineage = {"FREEZE.json": _write(store / "FREEZE.json", {
        "schema": "c2-freeze-v1", "protocol_id": "C2-FROZEN-v1", "protocol_sha256": PROTO,
        "scope": "c2-v1"}), "AUTH.json": _write(store / "AUTH.json", {
            "schema": "c2-auth-v1", "protocol_sha256": PROTO, "scope": "c2-v1"})}
    _write(store / "cpu_ledger.json", {"schema": "x4-oracle-profile-ledger-v1"})
    _write(root / "topo-pilot-c2" / ".git" / "CONTRACT.json", {"scope": "c2-v1"})  # skipped
    return root, store, {"tools/c2_readout/CONTRACT.json": pin}, lineage


def test_namespace_initial_admission(tmp_path, monkeypatch):
    root, store, pinned, lineage = _ns_root(tmp_path, monkeypatch)
    ns = cd.namespace_scan(root, pinned, lineage)
    assert ns["status"] == "PASS" and ns["hits"]
    assert {h["class"] for h in ns["hits"]} <= {"PINNED", "LINEAGE"}
    assert cd.store_admission(store, lineage, True)["status"] == "PASS"
    _write(store / "hist" / "HIST_fit_b0.npz", b"payload")  # prior scientific data
    adm = cd.store_admission(store, lineage, True)
    assert adm["status"] == LINEAGE
    assert any(str(p).replace("\\", "/").endswith("hist/HIST_fit_b0.npz") for p in
               adm["payload"])


def test_namespace_legitimate_continuation(tmp_path, monkeypatch):
    root, store, pinned, _ = _ns_root(tmp_path, monkeypatch)
    ctx = cdr.Ctx(store=store, worktree=root / "topo-pilot-c2", head="0" * 40, job="0102",
                  task_sha256="a" * 64, session="synthetic", release=None, policy=None,
                  data={})
    _write(store / "hist" / "HIST_fit_b0.npz", b"attempt 1")
    rul = root / "agent-handoff" / "rulings" / "R1.md"
    rsha = _write(rul, b"synthetic ruling")
    cdr.supersede(ctx, "0102", 1, ["hist/HIST_fit_b0.npz"],
                  {"defect": "D1 (synthetic)", "path": str(rul), "ruling_path": str(rul),
                   "sha256": rsha, "ruling_sha256": rsha})
    hsha = _write(store / "hist" / "HIST_fit_b0.npz", b"attempt 2")
    gsha = _write(store / "GATES.jsonl", b'{"gate": "H2", "scope": "c2-v1"}\n')
    ssha = _write(store / "STAGES.jsonl", b'{"event": "STARTED", "stage": "S1"}\n')
    msha = _write(store / "manifests" / "0102.json", {
        "schema": "c2-manifest-v1", "job": "0102", "stage": "S1", "head": "0" * 40,
        "files": {"hist/HIST_fit_b0.npz": hsha},
        "append_only": {"GATES.jsonl": gsha, "STAGES.jsonl": ssha}, "utc": "x"})
    _write(store / "manifests" / "0102.accepted.json", {
        "job": "0102", "manifest_sha256": msha, "review_path": "r", "review_sha256": "c" * 64,
        "coordinator": "synthetic", "utc": "x"})
    lineage = cdr.recognised(store)
    keys = {str(k).replace("\\", "/"): v for k, v in lineage.items()}
    assert keys.get("hist/HIST_fit_b0.npz") == hsha and "FREEZE.json" in keys
    assert cd.store_admission(store, lineage, False)["status"] == "PASS"
    assert cd.namespace_scan(root, pinned, lineage)["status"] == "PASS"
    _write(store / "hist" / "HIST_fit_b0.npz", b"attempt 2 altered")  # one altered hash
    adm = cd.store_admission(store, lineage, False)
    assert adm["status"] == LINEAGE and adm["unrecognised"]


@pytest.mark.parametrize("rel, data", [
    ("x9-research-store/notes.json", b'{"scope": "c2-v1"}'),  # a foreign store record
    ("other-dir/FREEZE_old.json", b'{"scope": "c2-v1"}'),  # FREEZE*.json anywhere
    ("c2-readout-store/extra.json", b'{"tag": "c2-v1"}'),  # outside the lineage manifest
    ("big-store/big.txt", b"x" * (2**20 - 2) + b"c2-v1" + b"y" * 9)],  # across a 1 MiB chunk
    ids=["foreign-store", "freeze-anywhere", "store-unlisted", "chunk-boundary"])  # short ids
def test_namespace_unrelated_collision_is_lineage(tmp_path, monkeypatch, rel, data):
    root, _, pinned, lineage = _ns_root(tmp_path, monkeypatch)
    assert cd.namespace_scan(root, pinned, lineage)["status"] == "PASS"
    _write(root / rel, data)
    ns = cd.namespace_scan(root, pinned, lineage)
    assert ns["status"] == LINEAGE
    foreign = [h for h in ns["hits"] if h["class"] == "FOREIGN"]
    assert any(str(h["path"]).replace("\\", "/").endswith(rel.split("/")[-1]) for h in foreign)
