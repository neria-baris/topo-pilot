"""Author B (job 0101): T-REG with the v2 H^Y donor and the NEW-10 Y-donor preparation fixture
(C2-FROZEN-v2 §13.3, §2.2, §5.2-§5.5, §7 rows 4-6; API.md §5, §16, §18, §19.3).

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
import c2_oracle as co2  # noqa: E402
import x6s1_registry as xr  # noqa: E402

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
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


ROLE_KEYS = ("digest_H", "digest_Hp", "digest_Hm", "digest_HY")


def _hist(seed, n):
    """y-rows 1..4 only, so both one-row shifts stay on the grid (Y_def on every row)."""
    rng = np.random.default_rng(seed)
    return (6 * rng.integers(0, 6, (n, 32)) + rng.integers(1, 5, (n, 32))).astype(np.uint8)


def _k(n):
    return np.where(np.arange(n) % 2 == 0, 1, -1).astype(np.int64)


def _table(seed, n, id0, off=()):
    canon, k = _hist(seed, n), _k(n)
    for i in off:  # OFF_GRID_Y: a prefix symbol in the row the shift would leave
        canon[i, 3] = 6 * 2 + (5 if k[i] > 0 else 0)
    ids = np.arange(id0, id0 + n, dtype=np.int64)
    return cd.history_table(canon, ids, np.zeros(n, dtype=np.int64), k)


def _redo(table, canon=None, ids=None):
    canon = table["canonical"] if canon is None else canon
    ids = table["sequence_id"] if ids is None else ids
    return cd.history_table(canon, ids, table["panel"], np.asarray(table["k_Y"], np.int64))


def _hex(tokens):
    return [hashlib.sha256(np.asarray(r).astype(np.uint8).tobytes()).hexdigest() for r in tokens]


def _expected_hy(canon, k):  # the v2 §2.2 map, written independently (fy_alt.py rule)
    a, b = canon[:, :31].astype(np.int64) // 6, canon[:, :31].astype(np.int64) % 6
    nb = b + np.asarray(k, np.int64)[:, None]
    ok = np.all((nb >= 0) & (nb <= 5), axis=1)
    return np.column_stack((6 * a + nb, canon[:, 31].astype(np.int64))), ok


def _digests(table):
    return set().union(*(set(np.asarray(table[c]).tolist()) for c in ROLE_KEYS)) - {""}


class _Reg:
    """Registry stand-in for separation (sealed_ranges {pool: (lo, hi)}, API.md 19.1 E-20)."""

    def __init__(self, digests=(), ranges=None):
        self.digests, self.x6, self.manifest = set(digests), None, {}
        self.sealed_ranges, self.predicates = dict(ranges or {}), ["sealed_d2a"]

    def contains(self, hex_digests):
        return np.array([h in self.digests for h in np.asarray(hex_digests).tolist()], bool)


# ---- T-REG: the H^Y donor (v2 §2.2, §5.3, §5.5; API.md 19.3) ----
def test_y_donor_map_and_off_grid_rows():
    rng = np.random.default_rng(71)
    canon = rng.integers(0, 36, (40, 32)).astype(np.uint8)
    canon[:20] = _hist(72, 20)  # half defined under either sign
    k = rng.choice(np.array([-1, 1]), 40)
    hy, ok = cd.y_donor(canon, k)
    want, want_ok = _expected_hy(canon, k)
    assert np.array_equal(np.asarray(ok, bool), want_ok) and want_ok[:20].all()
    assert not want_ok[20:].all()
    assert np.array_equal(hy[want_ok], want[want_ok])
    assert np.all(hy[~want_ok] == cd.OFF) and cd.OFF == 255  # never clamped or wrapped
    assert np.array_equal(hy[want_ok][:, 31], canon[want_ok][:, 31].astype(np.int64))


def test_history_table_with_the_y_donor():
    t = _table(73, 8, 500, off=(3, 6))
    canon, k = t["canonical"], np.asarray(t["k_Y"], np.int64)
    assert t["k_Y"].dtype == np.int8 and t["k_Y"].tolist() == _k(8).tolist()
    hy, ok = _expected_hy(canon, k)
    assert np.asarray(t["Y_def"], bool).tolist() == ok.tolist() and (~ok).sum() == 2
    assert list(t["digest_HY"][~ok]) == ["", ""]
    assert list(t["digest_HY"][ok]) == _hex(hy[ok])
    assert list(t["digest_H"]) == _hex(canon)
    assert _digests(t) == set(cd.table_digests(t))
    roles = cd.table_roles(t)
    assert np.array_equal(roles["HY"][1], np.flatnonzero(ok))
    assert np.array_equal(roles["HY"][0], hy[ok]) and len(roles["H"][1]) == 8


# ---- T-REG: separation ----
def _tables():
    fit, feas = _table(1, 12, 10_000), _table(2, 6, 20_000, off=(4,))
    return {"fit": fit, "feas": feas, "val": _table(3, 6, 30_000)}


def test_separation_pass_with_duplicates_kept():
    t = _tables()
    canon = t["fit"]["canonical"].copy()
    canon[10] = canon[0]  # a within-split duplicate history (same k_Y, distinct id)
    t["fit"] = _redo(t["fit"], canon=canon)
    res = cg.separation(_Reg({"f" * 64}), t)
    assert res["status"] == "PASS" and res["seq_ids"] == "PASS"
    every = [d for c in ROLE_KEYS for d in t["fit"][c].tolist() if d != ""]
    assert len(every) == 3 * 12 + int(np.sum(t["fit"]["Y_def"]))
    assert res["duplicates"]["fit"] == len(every) - len(set(every)) == 4
    assert res["duplicates"]["feas"] == 0 and res["duplicates"]["val"] == 0


def test_collision_with_R_is_lineage():
    t = _tables()
    res = cg.separation(_Reg({str(t["fit"]["digest_HY"][3])}), t)
    assert res["status"] == LINEAGE and res["collisions"]["fit_R"] >= 1


def test_off_grid_rows_form_no_donor():
    t = _tables()  # feas row 4 is OFF_GRID_Y
    canon, k = t["feas"]["canonical"][4:5], np.asarray(t["feas"]["k_Y"][4:5], np.int64)
    a, b = canon[:, :31].astype(np.int64) // 6, canon[:, :31].astype(np.int64) % 6
    near = [np.column_stack((6 * a + f(b + k[:, None]), canon[:, 31:])) for f in
            (lambda x: np.clip(x, 0, 5), lambda x: np.mod(x, 6))]  # clamped, wrapped
    full = np.full((1, 32), cd.OFF)
    res = cg.separation(_Reg(_hex(np.vstack(near + [full]))), t)
    assert res["status"] == "PASS"


def test_cross_split_collision_and_seq_id_overlap_are_lineage():
    t = _tables()
    canon = t["val"]["canonical"].copy()
    canon[2] = t["fit"]["canonical"][4]  # row 4 of fit and row 2 of val share k_Y = +1
    t["val"] = _redo(t["val"], canon=canon)
    res = cg.separation(_Reg(), t)
    hits = [v for c, v in res["collisions"].items() if "fit" in c and "val" in c]
    assert res["status"] == LINEAGE and hits and max(hits) >= 1
    t = _tables()
    ids = t["val"]["sequence_id"].copy()
    ids[0] = t["fit"]["sequence_id"][4]
    t["val"] = _redo(t["val"], ids=ids)
    res = cg.separation(_Reg(), t)
    assert res["status"] == LINEAGE and res["seq_ids"] != "PASS"
    res = cg.separation(_Reg(ranges={"d2a_sealed": (10_005, 10_006)}), _tables())
    assert res["status"] == LINEAGE  # an id inside a sealed D-2a range


def test_sealed_d2a_predicate_hit_is_incomplete():
    t = _tables()
    canon = t["feas"]["canonical"].copy()
    canon[1] = 1  # every symbol in {0..4}: the sealed D-2a alphabet
    t["feas"] = _redo(t["feas"], canon=canon)
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


# ---- T-POLICY NEW-10: the Y-donor preparation in H2/H2' (v2 §7 note; API.md 19.3) ----
def _toy_process():
    rng = np.random.default_rng(1010)
    T, E = rng.dirichlet(np.full(144, 0.3), 144), rng.dirichlet(np.ones(36), 144)
    coords = np.array([(i % 12, i // 12) for i in range(144)], dtype=np.float64)
    return T, E, np.full(144, 1.0 / 144), coords


def test_y_donor_preparation_from_the_cached_natural_oracle():
    T, E, pi, coords = _toy_process()
    canon = _hist(1011, 6)
    canon[5, 2], canon[5, 3] = 6 + 5, 6 + 0  # rows 5 and 0 in the prefix: OFF for either k
    o_H = co2.oracle_role(T, E, pi, canon, coords)  # H2: the natural histories only
    k = cd.k_y(o_H["b31"], coords)  # b31(H) is used only for k_Y, Y_def and the donors
    want = np.where(o_H["b31"] @ coords[:, 1] < 5.5, 1, -1)
    assert np.asarray(k).tolist() == want.tolist()
    table = cd.history_table(canon, np.arange(6, dtype=np.int64), np.zeros(6, np.int64), k)
    ok = np.asarray(table["Y_def"], bool)
    assert ok.tolist() == [True] * 5 + [False]
    res = cg.separation(_Reg(), {"fit": table})  # over every defined donor role, before H3
    every = [d for c in ROLE_KEYS for d in table[c].tolist() if d != ""]
    assert res["status"] == "PASS" and len(every) == 3 * 6 + 5
    assert res["duplicates"]["fit"] == len(every) - len(set(every))
    cache = dict(o_H, s=np.asarray(o_H["s"]) + 1.0)  # a marked cache
    o = co2.oracle_split(T, E, pi, coords, canon, k, o_H=cache)  # H3 consumes the cache
    assert np.array_equal(np.asarray(o["H"]["s"]), cache["s"])  # not recomputed
    assert np.array_equal(np.asarray(o["H"]["b31"]), np.asarray(o_H["b31"]))
    hy, _ = _expected_hy(canon, np.asarray(k, np.int64))
    ref = co2.oracle_role(T, E, pi, hy[ok], coords)
    q = np.asarray(o["HY"]["q"])
    assert np.allclose(q[ok], ref["q"], rtol=1e-12, atol=0) and np.isnan(q[~ok]).all()
    assert np.isnan(np.asarray(o["G_y"])[~ok]).all() and np.isfinite(o["G_y"][ok]).all()
    assert np.asarray(o["Y_def"], bool).tolist() == ok.tolist()
