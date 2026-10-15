"""Independent tests of tools/d2a/d2a_world.py, part 1 (job 0028, author A): T-SEED, the pool
table, processes, decision rows, padding, bin positions, master collisions and the test-pool
guard. Written from D2A-FROZEN-v1 and tools/d2a/API.md only, before the module existed.
Expected values come from d1_seam, SeedTree and hand computation; no pool is ever sampled.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "d2a"), ("tools", "d1_seam"), ("tools", "x4_oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

import d1_seam  # noqa: E402
import d2a_world as W  # noqa: E402

pytestmark = pytest.mark.oracle

DATA, MODEL = 2026101531, 2026101532
S0, S2, S3, A, B = 0, 1, 2, 3, 4
ORDER = ([f"train-s{s}" for s in range(1, 5)] + [f"dev-s{s}" for s in range(1, 5)]
         + ["trainN-s1", "trainN-s2", "devN-s1", "devN-s2", "stage0", "stage0N", "cal", "val",
            "test", "valN", "testN"])


def _expected_pools():
    """(proc, n, split, seed or None) and stream scope per pool, from API section 2.1."""
    out = {}
    for s in range(1, 5):
        out[f"train-s{s}"] = (("CM", 2**18, "train", s), ("d2a", "train", "CM", s))
        out[f"dev-s{s}"] = (("CM", 2**12, "dev", s), ("d2a", "dev", "CM", s))
    for s in (1, 2):
        out[f"trainN-s{s}"] = (("CC", 2**18, "train", s), ("d2a", "train", "CC", s))
        out[f"devN-s{s}"] = (("CC", 2**12, "dev", s), ("d2a", "dev", "CC", s))
    for pool, n, split in (("stage0", 2**16, "dev"), ("cal", 2**16, "dev"),
                           ("val", 2**14, "dev"), ("test", 2**16, "test")):
        out[pool] = (("CM", n, split, None), ("d2a", pool, "CM"))
    for pool, base, split in (("stage0N", "stage0", "dev"), ("valN", "val", "dev"),
                              ("testN", "test", "test")):
        out[pool] = (("CC", 2**14, split, None), ("d2a", base, "CC"))
    return out


EXPECTED = _expected_pools()


# ---- constants and the pool table ----------------------------------------------------------
def test_constants():
    assert (W.DATA, W.MODEL) == (DATA, MODEL)
    assert W.CHUNK == 4096 and tuple(W.POSITIONS) == (16, 28)
    assert tuple(map(tuple, W.BINS)) == ((1, 8, 16), (2, 17, 24), (3, 25, 31))
    assert tuple(W.S2) == (3, 4, 8, 9)
    assert tuple(W.S3) == (3, 4, 15, 16, 18, 19, 20, 21, 23, 24, 33, 34, 40, 41, 43, 44, 45, 46,
                           48, 49, 53, 54, 58, 59)


def test_pool_table_follows_api():
    assert list(W.POOLS) == ORDER and len(ORDER) == 21
    for pool, ((proc, n, split, seed), _) in EXPECTED.items():
        got = tuple(W.POOLS[pool])
        assert got[:3] == (proc, n, split), pool
        if seed is not None:
            assert got[3] == seed, pool


# ---- T-SEED --------------------------------------------------------------------------------
def test_T_SEED_pool_streams_follow_api_and_are_deterministic():
    for pool, (_, scope) in EXPECTED.items():
        ref = SeedTree(DATA).generator(*scope).random(6)
        assert np.array_equal(W.pool_generator(pool).random(6), ref), pool
        assert np.array_equal(W.pool_generator(pool).random(6), ref), pool  # fresh each call


def test_T_SEED_streams_pairwise_distinct():
    seeds = {pool: SeedTree(DATA).seed(*scope) for pool, (_, scope) in EXPECTED.items()}
    assert len(set(seeds.values())) == 21
    first = {tuple(W.pool_generator(p).random(4).tolist()) for p in ORDER}
    assert len(first) == 21
    others = [("d2a", "bin", "val", b) for b in (1, 2, 3)] + [("d2a", "templates", 28)]
    assert not {SeedTree(DATA).seed(*s) for s in others} & set(seeds.values())


def test_T_SEED_sequence_ids_disjoint_across_pools():
    assert dict(W.SEQ_CODE) == {pool: i + 1 for i, pool in enumerate(ORDER)}
    spans = []
    for pool in ORDER:
        n = W.POOLS[pool][1]
        ids = W.SEQ_CODE[pool] * 2**32 + np.arange(n, dtype=np.int64)
        assert ids.dtype == np.int64 and n < 2**32
        spans.append((int(ids[0]), int(ids[-1])))
    spans.sort()
    assert all(a[1] < b[0] for a, b in zip(spans, spans[1:]))  # no overlap at all


def _meta(path: Path, seed_map, config):
    path.mkdir(parents=True)
    body = {"artifact_type": "ObservationSet", "artifact_id": path.name, "seed_map": seed_map,
            "config": config, "parent_ids": [], "status": "complete"}
    (path / "meta.json").write_text(json.dumps(body, indent=1), encoding="utf-8")
    return (path / "meta.json").resolve()


def test_T_SEED_master_collisions(tmp_path):
    clean = tmp_path / "clean"
    _meta(clean / "ObservationSet" / "aaaa", {"tiny_observations": 1729, "init/r/0": 12345},
          {"split": "train", "master": 7})
    _meta(clean / "Checkpoint" / "bbbb", {}, {"run_key": ["d2a", 1], "step": 0})
    assert list(W.master_collisions([clean])) == []
    hit = tmp_path / "hit"
    p_data = _meta(hit / "ObservationSet" / "cccc", {"d2a/train/CM/1": DATA}, {"split": "dev"})
    p_model = _meta(hit / "Checkpoint" / "dddd", {"init/d2a/1": MODEL}, {"step": 0})
    p_cfg = _meta(hit / "MetricRecord" / "eeee", {}, {"note": f"master {MODEL}"})
    _meta(hit / "MetricRecord" / "ffff", {"x": 3}, {"y": 4})
    got = {Path(p).resolve() for p in W.master_collisions([clean, hit])}
    assert got == {p_data, p_model, p_cfg}


# ---- processes -----------------------------------------------------------------------------
def test_process_blocks():
    fm = d1_seam.float_model()
    cm, cc = W.process("CM"), W.process("CC")
    assert set(cm) == set(cc) == {"T", "E", "mu"}
    assert np.array_equal(cm["T"], fm["T"]) and np.array_equal(cm["E"], fm["E_mix"])
    assert np.array_equal(cm["mu"], fm["mu"])
    T = np.asarray(cc["T"])
    assert T.shape == (24, 24)
    assert np.array_equal(T[:12, :12], fm["T_C"]) and np.array_equal(T[12:, 12:], fm["T_C"])
    assert not T[:12, 12:].any() and not T[12:, :12].any()
    assert np.array_equal(cc["E"], fm["E_mix"]) and np.array_equal(cc["mu"], fm["mu"])
    assert not np.array_equal(cm["T"], cc["T"])  # the Möbius block differs


def test_world_kernels():
    fm = d1_seam.float_model()
    cm, cc = W.world_kernels("CM"), W.world_kernels("CC")
    assert set(cm) == set(cc) == {"T_C", "T_M", "E", "mu_C", "mu_M"}
    for key, ref in (("T_C", "T_C"), ("T_M", "T_M"), ("E", "E"), ("mu_C", "mu_C"),
                     ("mu_M", "mu_M")):
        assert np.array_equal(cm[key], fm[ref]), key
    assert np.array_equal(cc["T_C"], fm["T_C"]) and np.array_equal(cc["T_M"], fm["T_C"])
    assert np.array_equal(cc["E"], fm["E"])


# ---- decision rows, padding ----------------------------------------------------------------
def test_decision_rows():
    tok = np.zeros((5, 33), dtype=np.uint8)
    tok[1, 15] = S3
    tok[3, 15] = S3
    tok[4, 27] = S3
    tok[2, 15] = A
    assert np.array_equal(np.asarray(W.decision_rows(tok, 16)), [1, 3])
    assert np.array_equal(np.asarray(W.decision_rows(tok, 28)), [4])
    assert len(np.asarray(W.decision_rows(tok, 5))) == 0


def test_pad():
    for h in (d1_seam.H_STAR, d1_seam.H_A, d1_seam.H_MAX, (A,) * 32, (B,) * 20):
        row = np.asarray(W.pad(h))
        assert row.shape == (33,) and row.dtype == np.uint8
        assert row[:len(h)].tolist() == list(h) and not row[len(h):].any()


# ---- bin positions -------------------------------------------------------------------------
def _bin_tokens():
    tok = np.zeros((5, 33), dtype=np.uint8)  # all sigma0: no decision position
    marks = {1: (10,), 2: (7, 8, 16, 20, 25, 31, 32), 3: (7, 32, 33), 4: (17, 24, 3)}
    for r, ts in marks.items():
        for t in ts:
            tok[r, t - 1] = S3
    return tok


def test_bin_positions_follow_api_rule():
    tok, pool = _bin_tokens(), "val"
    got = np.asarray(W.bin_positions(tok, pool))
    assert got.shape == (3, 5) and got.dtype == np.int64
    # hand-checked rows with at most one candidate per bin (no draw matters)
    assert got[:, 0].tolist() == [0, 0, 0]
    assert got[:, 1].tolist() == [10, 0, 0]
    assert got[:, 3].tolist() == [0, 0, 0]  # 7, 32, 33 lie outside every bin
    assert got[1, 2] == 20 and got[0, 4] == 0 and got[2, 4] == 0
    for b, first, last in ((1, 8, 16), (2, 17, 24), (3, 25, 31)):
        u = SeedTree(DATA).generator("d2a", "bin", pool, b).random(5)
        for r in range(5):
            cands = [t for t in range(first, last + 1) if tok[r, t - 1] == S3]
            want = cands[math.floor(u[r] * len(cands))] if cands else 0
            assert got[b - 1, r] == want, (b, r)
    assert got[0, 2] in (8, 16) and got[2, 2] in (25, 31) and got[1, 4] in (17, 24)


def test_bin_positions_are_deterministic():
    tok = _bin_tokens()
    assert np.array_equal(W.bin_positions(tok, "cal"), W.bin_positions(tok, "cal"))


# ---- test-pool guard (S9) ------------------------------------------------------------------
@pytest.mark.parametrize("pool", ["test", "testN"])
@pytest.mark.parametrize("stage", [None, "0", "1", "2", "33"])
def test_test_pools_need_stage3(pool, stage, tmp_path, monkeypatch):
    if stage is None:
        monkeypatch.delenv("D2A_STAGE", raising=False)
    else:
        monkeypatch.setenv("D2A_STAGE", stage)
    for loader in (W.load_tokens, W.load_private):
        with pytest.raises(StageFailure) as exc:
            loader(pool, store_root=tmp_path)
        assert exc.value.code is ErrorCode.LEAKAGE


def _code_or_none(fn):
    try:
        fn()
    except StageFailure as exc:
        return exc.code
    except Exception:  # noqa: BLE001  any non-leakage failure on an empty store is acceptable
        return None
    return None


def test_guard_admits_stage3_and_ignores_other_pools(tmp_path, monkeypatch):
    monkeypatch.setenv("D2A_STAGE", "3")
    for pool in ("test", "testN"):
        code = _code_or_none(lambda p=pool: W.load_tokens(p, store_root=tmp_path))
        assert code is not ErrorCode.LEAKAGE, pool
    monkeypatch.delenv("D2A_STAGE", raising=False)
    for pool in ("val", "cal", "valN"):
        code = _code_or_none(lambda p=pool: W.load_tokens(p, store_root=tmp_path))
        assert code is not ErrorCode.LEAKAGE, pool
