"""Author B (job 0223, phase 2): the registry readers with planted defects (protocol 8.2-8.3;
API_U2 3; DRU-REG). Synthetic stores under tmp_path; history tables are made with the K4b table
builder (canon32, seq_ids, digest, ...); access hooks record every file open."""

from __future__ import annotations

import builtins
import copy
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


def _r():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_registry")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _table(path: Path, seed: int, n: int = 8, split="val", block=0) -> list:
    rng = np.random.default_rng(seed)
    canon = rng.integers(0, 36, size=(n, 32)).astype(np.uint8)
    ids = np.arange(n, dtype=np.int64) + seed * 1000
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **kd.history_table(canon, ids, split, block))
    return list(kd.digests(canon))


def _stages(store: Path, entries: dict) -> None:
    lines = [{"stage": st, "event": "STAGE_COMPLETE", "files": files} for st, files in entries.items()]  # noqa: E501
    (store / "STAGES.jsonl").write_text("\n".join(json.dumps(x) for x in lines) + "\n",
                                        encoding="utf-8")


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


def _hwsc(tmp_path, extra=True):
    """hwsc-store fixture: u2_hist tables listed in S3/S7 STAGE_COMPLETE, OBS_INVENTORY, plus a
    Checkpoint artifact (payload.npz) and a sealed/ file that must never be opened."""
    store = tmp_path / "hwsc-store"
    c = copy.deepcopy(uc.CONTRACT)
    sc = c["stage_c_u2"]
    by_stage: dict = {}
    digs: list = []
    for i, (rel, stage) in enumerate(sorted(sc["u2_hist"].items())):
        digs += _table(store / rel, 11 + i)
        by_stage.setdefault(stage, {})[rel] = _sha((store / rel).read_bytes())
    inv = store / sc["obs_inventory"]["relpath"]
    inv.parent.mkdir(parents=True, exist_ok=True)
    inv.write_bytes(b"{}")
    by_stage[sc["obs_inventory"]["stage"]] = {sc["obs_inventory"]["relpath"]: _sha(b"{}")}
    sc["obs_inventory"]["sha256"] = _sha(b"{}")
    if extra:
        ck = store / "artifacts" / "Checkpoint" / "abc123"
        ck.mkdir(parents=True)
        (ck / "meta.json").write_text(json.dumps({"artifact_type": "Checkpoint"}), encoding="utf-8")
        (ck / "payload.npz").write_bytes(b"NOT-AN-NPZ-PLANTED")
        (store / "sealed").mkdir()
        (store / "sealed" / "secret.npz").write_bytes(b"SEALED-PLANTED")
    _stages(store, by_stage)
    return store, c, digs


def _first_hist(c):
    return sorted(c["stage_c_u2"]["u2_hist"])[0]


# ------------------------------------------------------------------ source_hwsc
def test_source_hwsc_reads_planted_tables_by_the_k4b_reader(tmp_path):
    store, c, digs = _hwsc(tmp_path)
    r = _r().source_hwsc(store, contract=c)
    assert r["status"] == "PASS", r
    assert set(digs) <= set(r["digests"]) and len(r["seq_ids"]) >= len(digs)
    assert {"status", "digests", "seq_ids", "files", "other", "non_history", "present"} <= set(r)


def test_source_hwsc_sha_differs_from_stage_complete_entry(tmp_path):
    store, c, _ = _hwsc(tmp_path)
    p = store / _first_hist(c)
    p.write_bytes(p.read_bytes() + b"\0")
    assert _r().source_hwsc(store, contract=c)["status"] == INC


def test_source_hwsc_missing_listed_file(tmp_path):
    store, c, _ = _hwsc(tmp_path)
    (store / _first_hist(c)).unlink()
    assert _r().source_hwsc(store, contract=c)["status"] == INC


def test_source_hwsc_unlisted_array_file(tmp_path):
    store, c, _ = _hwsc(tmp_path)
    _table(store / "stages" / "S3" / "HIST_other_b9.npz", 99)
    assert _r().source_hwsc(store, contract=c)["status"] == INC


def test_source_hwsc_digest_column_differs_from_canon32(tmp_path):
    store, c, _ = _hwsc(tmp_path)
    p = store / _first_hist(c)
    with np.load(p, allow_pickle=False) as z:
        d = {k: z[k] for k in z.files}
    d["digest"] = d["digest"].copy()
    d["digest"][0] = "0" * 64
    np.savez(p, **d)
    # the STAGE_COMPLETE entry is re-written for the altered bytes: only the column defect remains
    lines = [json.loads(x) for x in (store / "STAGES.jsonl").read_text(encoding="utf-8").splitlines()]  # noqa: E501
    for ln in lines:
        if _first_hist(c) in ln["files"]:
            ln["files"][_first_hist(c)] = _sha(p.read_bytes())
    (store / "STAGES.jsonl").write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")  # noqa: E501
    assert _r().source_hwsc(store, contract=c)["status"] == INC


def test_source_hwsc_checkpoint_payload_and_sealed_never_opened(tmp_path, opens):
    store, c, _ = _hwsc(tmp_path)
    r = _r().source_hwsc(store, contract=c)
    assert r["status"] == "PASS", r
    assert not [p for p in opens if "payload.npz" in p or "state.pt" in p]
    assert not [p for p in opens if "sealed" in Path(p).parts or "secret.npz" in p]


# ------------------------------------------------------------------ source_kreg2_c
def _kreg2(tmp_path, n=12):
    store = tmp_path / "hwsc-store"
    (store / "registry").mkdir(parents=True)
    rng = np.random.default_rng(3)
    dig = np.array(sorted(_sha(rng.bytes(8)) for _ in range(n)))
    p = store / "registry" / "K-REG2_digests.npz"
    np.savez(p, digests=dig.astype("<U64"), seq_ids=np.arange(n, dtype=np.int64))
    c = copy.deepcopy(uc.CONTRACT)
    c["stage_c_u2"]["k_reg2"]["digest_file_sha256"] = _sha(p.read_bytes())
    return store, c, dig


def test_source_kreg2_c_reads_digest_file(tmp_path):
    store, c, dig = _kreg2(tmp_path)
    r = _r().source_kreg2_c(store, contract=c)
    assert r["status"] == "PASS" and r["n"] == len(dig)
    assert list(r["digests"]) == list(dig)


def test_source_kreg2_c_sha_mismatch_refused(tmp_path):
    store, c, _ = _kreg2(tmp_path)
    c["stage_c_u2"]["k_reg2"]["digest_file_sha256"] = "0" * 64
    assert _r().source_kreg2_c(store, contract=c)["status"] == INC


def test_source_kreg2_c_missing_file_refused(tmp_path):
    store, c, _ = _kreg2(tmp_path)
    (store / "registry" / "K-REG2_digests.npz").unlink()
    assert _r().source_kreg2_c(store, contract=c)["status"] == INC


# ------------------------------------------------------------------ superset_diagnostic (S-2)
def _sorted_union(n=40, seed=1):
    rng = np.random.default_rng(seed)
    return np.array(sorted(_sha(rng.bytes(8)) for _ in range(n)))


def test_superset_diagnostic_counts_and_lists_missing():
    union = _sorted_union()
    kreg = np.array(sorted(list(union[::2]) + [_sha(b"missing-1"), _sha(b"missing-2")]))
    d = _r().superset_diagnostic(union, kreg, chunk=3)
    assert d["n_missing"] == 2 and set(d["missing_head"]) == {_sha(b"missing-1"), _sha(b"missing-2")}  # noqa: E501
    assert set(d) >= {"n_missing", "missing_head"} and "status" not in d


def test_superset_diagnostic_chunk_size_invariant_and_empty_case():
    union = _sorted_union(60)
    kreg = np.array(sorted(list(union[::3]) + [_sha(b"m%d" % i) for i in range(7)]))
    ds = [_r().superset_diagnostic(union, kreg, chunk=k) for k in (1, 4, 1000)]
    assert ds[0] == ds[1] == ds[2] and ds[0]["n_missing"] == 7
    ok = _r().superset_diagnostic(union, union[::2], chunk=5)
    assert ok["n_missing"] == 0 and list(ok["missing_head"]) == []


def test_superset_diagnostic_head_is_capped_at_100():
    union = _sorted_union(10)
    kreg = np.array(sorted(_sha(b"x%d" % i) for i in range(150)))
    d = _r().superset_diagnostic(union, kreg, chunk=64)
    assert d["n_missing"] == 150 and len(d["missing_head"]) == 100


# ------------------------------------------------------------------ source_own_u
def _own(tmp_path, names=("stages/OF/HIST_OF_eval_a1_b0.npz", "stages/OF/HIST_OF_eval_a2_b0.npz")):
    store = tmp_path / "hwsu-store"
    files = {}
    for i, rel in enumerate(names):
        _table(store / rel, 40 + i)
        files[rel] = _sha((store / rel).read_bytes())
    _stages(store, {"OF": files})
    return store, list(names)


def test_source_own_u_reads_listed_tables(tmp_path):
    store, names = _own(tmp_path)
    r = _r().source_own_u(store, names)
    assert r["status"] == "PASS" and len(r["digests"]) >= 2


def test_source_own_u_unlisted_history_file_refused(tmp_path):
    store, names = _own(tmp_path)
    _table(store / "stages" / "OF" / "HIST_OF_stray_b0.npz", 77)
    assert _r().source_own_u(store, names)["status"] == INC


def test_source_own_u_sha_mismatch_and_missing_expected_refused(tmp_path):
    store, names = _own(tmp_path)
    p = store / names[0]
    p.write_bytes(p.read_bytes() + b"\0")
    assert _r().source_own_u(store, names)["status"] == INC
    store2, names2 = _own(tmp_path / "second")
    assert _r().source_own_u(store2, names2 + ["stages/OF/HIST_OF_never_b0.npz"])["status"] == INC


# ------------------------------------------------------------------ source_own_dry (U2')
def test_source_own_dry_store_without_obligation_refused(tmp_path):
    _table(tmp_path / "hwsu-dry-u2-x" / "stages" / "E1" / "DRYHIST_a.npz", 5)
    assert _r().source_own_dry(tmp_path)["status"] == INC


def test_source_own_dry_test_root_with_history_file_refused(tmp_path):
    _table(tmp_path / "test_hwsu-0999" / "dru1" / "HIST_a_b0.npz", 6)
    assert _r().source_own_dry(tmp_path)["status"] == INC


def test_source_own_dry_empty_or_array_free_roots_pass(tmp_path):
    (tmp_path / "test_hwsu-0998").mkdir()
    (tmp_path / "test_hwsu-0998" / "note.txt").write_text("x", encoding="utf-8")
    assert _r().source_own_dry(tmp_path)["status"] == "PASS"
    assert _r().source_own_dry(tmp_path / "does-not-exist")["status"] == "PASS"


# ------------------------------------------------------------------ inventory_u (U7, R8)
def test_inventory_u_flags_unlisted_top_level_dir_with_history_file(tmp_path):
    _table(tmp_path / "mystery-store" / "stages" / "S1" / "HIST_q_b0.npz", 8)
    r = _r().inventory_u(tmp_path, {})
    assert r["status"] == INC and "mystery-store" in r["unlisted"]
    assert {"status", "inv", "classes", "unlisted", "violations"} <= set(r)


def test_inventory_u_table_rows_of_root_table_u2_are_known(tmp_path):
    add = uc.CONTRACT["registry_u2"]["root_table_u2"]["add"]
    names = [k for k in add if not k.startswith("_")]
    for n in names:
        (tmp_path / n).mkdir()
    r = _r().inventory_u(tmp_path, {})
    assert not set(names) & set(r["unlisted"])


def test_root_table_u_hwsc_store_is_a_reader_row():
    t = _r().root_table_u() if hasattr(_r(), "root_table_u") else None
    if t is None:
        pytest.skip("root_table_u not exposed")
    assert t["hwsc-store"]["decision"] in ("READER", "READER_IF_PRESENT")
