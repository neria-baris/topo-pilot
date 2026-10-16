"""Author B, K4b TEST_PLAN B1, B3 and B17 (data side): seed streams, fixed 3,072-row blocks
whose content does not depend on k, sequence IDs, int-keyed maps, history tables, duplicates,
separation (every collision -> FAIL_TECHNICAL/LINEAGE) and the sealed-D-2a predicate.

Synthetic only: a 4-state toy HMM over 36 symbols; no store, checkpoint or real history."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import k4b_config  # noqa: E402
import k4b_data  # noqa: E402
import scores  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402
from c1_registry_sources import canonical32  # noqa: E402
from topo_pilot.contracts import SeedTree, SequenceLayout  # noqa: E402
from topo_pilot.dataset import HMMSampler  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402

PROCESS = ("cylinder", "overlap", "1.25")
SCOPE = "k4b-sf-v1"
REASON = "potential overlap with sealed D-2a histories"
LINEAGE = "FAIL_TECHNICAL/LINEAGE"
INCOMPLETE = "INCONCLUSIVE/REGISTRY_INCOMPLETE"


def synthetic_process(seed=7, n_states=4, n_symbols=36):
    rng = np.random.default_rng(seed)
    T = rng.uniform(0.1, 1.0, (n_states, n_states))
    T /= T.sum(axis=1, keepdims=True)
    E = rng.uniform(0.1, 1.0, (n_states, n_symbols))
    E /= E.sum(axis=1, keepdims=True)
    pi = np.full(n_states, 1.0 / n_states)
    return T, E, pi


@pytest.fixture(scope="module")
def proc():
    return synthetic_process()


def ref_ids(split, block):
    code = process_code(*PROCESS, f"{SCOPE}/{split}/b{int(block)}")
    return np.asarray(make_sequence_ids(code, "test", 3072))


def expected_block(T, E, pi, split, block):
    """The protocol §3.1 recipe, written out independently of k4b_data."""
    rng = SeedTree(0).generator("data", SCOPE, split, int(block), *PROCESS)
    tokens, _ = HMMSampler(T, E, pi, SequenceLayout()).sample(3072, rng)
    ids = ref_ids(split, block)
    order = np.argsort(ids, kind="stable")
    return np.ascontiguousarray(tokens[:, :32][order]).astype(np.uint8), ids[order]


# ---------------------------------------------------------------- constants and int keys (B1)

def test_constants_match_contract():
    assert k4b_config.MODELS == (1729, 2718, 3141)
    assert all(type(m) is int for m in k4b_config.MODELS)
    assert (k4b_config.BLOCK, k4b_config.PANEL) == (3072, 512)
    assert k4b_config.SCOPE == SCOPE
    assert tuple(k4b_config.PROCESS) == PROCESS
    assert k4b_config.SEEDS == {"val_sd": 610101, "val_b4": 610102, "endpoint": 610103,
                                "fresh_b4": 610104, "val_projection": 610105}
    assert tuple(k4b_config.LADDER) == (3072, 6144, 12288)


def test_require_int_keys_returns_the_same_dict():
    d = {1729: "a", 2718: "b", 3141: "c"}
    assert k4b_config.require_int_keys(d, "maps") is d


@pytest.mark.parametrize("bad", [
    {"1729": 0, "2718": 0, "3141": 0},
    {1729: 0, 2718: 0, "3141": 0},
    {1729: 0, 2718: 0},
    {1729: 0, 2718: 0, 3141: 0, 9999: 0},
])
def test_require_int_keys_rejects_str_missing_or_extra(bad):
    with pytest.raises(C1GateFailure) as exc:
        k4b_config.require_int_keys(bad, "E_named")
    assert exc.value.status == "FAIL_TECHNICAL/IDENTITY"


# ------------------------------------------------------------------- seed streams and IDs (B1)

def test_history_generator_is_the_registered_seedtree_stream():
    got = k4b_data.history_generator("val", 0).random(16)
    ref = SeedTree(0).generator("data", SCOPE, "val", 0, *PROCESS).random(16)
    assert np.array_equal(got, ref)
    again = k4b_data.history_generator("val", np.int64(0)).random(16)
    assert np.array_equal(again, ref)


def test_history_streams_differ_by_split_and_block():
    draws = {(s, b): k4b_data.history_generator(s, b).random(8)
             for s, b in (("cal", 0), ("val", 0), ("test", 0), ("test", 1))}
    keys = list(draws)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            assert not np.array_equal(draws[a], draws[b]), (a, b)


@pytest.mark.parametrize("split,block", [("cal", 0), ("val", 0), ("test", 0), ("test", 3)])
def test_sequence_ids_follow_the_registered_rule(split, block):
    got = k4b_data.sequence_ids(split, block)
    assert got.dtype == np.int64 and got.shape == (3072,)
    assert np.array_equal(got, ref_ids(split, block))
    assert len(np.unique(got)) == 3072


def test_sequence_ids_disjoint_across_k4b_blocks():
    blocks = [("cal", 0), ("val", 0)] + [("test", b) for b in range(4)]
    seen = set()
    for split, block in blocks:
        ids = set(k4b_data.sequence_ids(split, block).tolist())
        assert not (ids & seen), (split, block)
        seen |= ids


# ---------------------------------------------------------------- fixed blocks (B1)

def test_sample_block_is_one_sampler_call_sorted_by_id(proc):
    T, E, pi = proc
    canon, ids = k4b_data.sample_block(T, E, pi, "cal", 0)
    exp_canon, exp_ids = expected_block(T, E, pi, "cal", 0)
    assert canon.dtype == np.uint8 and canon.shape == (3072, 32)
    assert canon.flags["C_CONTIGUOUS"]
    assert np.array_equal(ids, exp_ids)
    assert np.all(np.diff(ids) > 0)
    assert np.array_equal(canon, exp_canon)


def test_block_content_invariant_to_k(proc):
    T, E, pi = proc
    k1 = [k4b_data.sample_block(T, E, pi, "test", b) for b in range(1)]
    k2 = [k4b_data.sample_block(T, E, pi, "test", b) for b in range(2)]
    k4 = [k4b_data.sample_block(T, E, pi, "test", b) for b in range(4)]
    for b in range(1):
        assert np.array_equal(k1[b][0], k4[b][0]) and np.array_equal(k1[b][1], k4[b][1])
    for b in range(2):
        assert np.array_equal(k2[b][0], k4[b][0]) and np.array_equal(k2[b][1], k4[b][1])
    assert not np.array_equal(k4[0][0], k4[1][0])
    cal, _ = k4b_data.sample_block(T, E, pi, "cal", 0)
    assert not np.array_equal(cal, k4[0][0])


# --------------------------------------------------------- named maps, digests, panels (B1)

def test_named_from_canonical_round_trip():
    rng = np.random.default_rng(3)
    perm = rng.permutation(36)
    canon = rng.integers(0, 36, (50, 32)).astype(np.uint8)
    named = k4b_data.named_from_canonical(canon, perm)
    assert named.dtype == np.uint8 and named.shape == canon.shape
    assert np.array_equal(named, perm[canon])
    assert np.array_equal(canonical32(named, perm), canon)


def test_digests_are_sha256_of_uint8_rows():
    canon = np.random.default_rng(4).integers(0, 36, (20, 32)).astype(np.uint8)
    got = k4b_data.digests(canon)
    assert list(got) == scores.history_digests(canon)
    assert got[0] == hashlib.sha256(canon[0].tobytes()).hexdigest()


def test_lowest_rows_are_the_512_lowest_ids_ascending():
    ids = np.random.default_rng(5).permutation(3072).astype(np.int64) + 10**9
    rows = np.asarray(k4b_data.lowest_rows(ids))
    assert rows.shape == (512,)
    assert np.all(np.diff(ids[rows]) > 0)
    assert set(ids[rows].tolist()) == set(np.sort(ids)[:512].tolist())


def shuffled_table_inputs(seed=6):
    rng = np.random.default_rng(seed)
    canon = rng.integers(0, 36, (3072, 32)).astype(np.uint8)
    canon[20] = canon[10]  # a legitimate within-split duplicate
    ids = rng.permutation(3072).astype(np.int64) + 5 * 10**9
    return canon, ids


def test_history_table_cal_columns_by_sequence_id():
    canon, ids = shuffled_table_inputs()
    t = k4b_data.history_table(canon, ids, "cal", 0)
    t_ids = np.asarray(t["seq_ids"])
    assert t_ids.dtype == np.int64 and len(t_ids) == 3072
    assert np.asarray(t["canon32"]).dtype == np.uint8
    by_id = {int(s): i for i, s in enumerate(ids)}
    ranked = np.sort(ids)
    land, ref = set(ranked[:512].tolist()), set(ranked[:4].tolist())
    rest = ranked[512:]
    panel_of = {int(s): r // 512 for r, s in enumerate(rest)}
    for i, s in enumerate(t_ids.tolist()):
        assert np.array_equal(np.asarray(t["canon32"])[i], canon[by_id[s]])
        assert t["digest"][i] == hashlib.sha256(canon[by_id[s]].tobytes()).hexdigest()
        assert bool(t["landmark"][i]) == (s in land)
        assert bool(t["ref_row"][i]) == (s in ref)
        assert int(t["decoder_panel"][i]) == (-1 if s in land else panel_of[s])
    panel = np.asarray(t["decoder_panel"])
    assert panel.dtype == np.int8
    assert [int(np.sum(panel == v)) for v in (-1, 0, 1, 2, 3, 4)] == [512] * 6


def test_history_table_val_landmarks():
    canon, ids = shuffled_table_inputs(8)
    t = k4b_data.history_table(canon, ids, "val", 0)
    t_ids = np.asarray(t["seq_ids"])
    land = set(np.sort(ids)[:512].tolist())
    flags = np.asarray(t["landmark"], dtype=bool)
    assert int(flags.sum()) == 512
    assert set(t_ids[flags].tolist()) == land


# ------------------------------------------------------------- duplicates and separation (B3)

def test_duplicates_counted_never_removed():
    rng = np.random.default_rng(9)
    a, b, c = (rng.integers(0, 36, 32).astype(np.uint8) for _ in range(3))
    canon = np.stack([a, b, a, c, a, b])
    before = canon.copy()
    d = k4b_data.duplicates(canon)
    assert (d["n_rows"], d["n_unique"], d["max_multiplicity"]) == (6, 3, 3)
    assert d["n_duplicate_rows"] in (3, 5)  # extra copies, or rows in repeated groups
    assert np.array_equal(canon, before)
    t = k4b_data.history_table(np.repeat(canon, 512, axis=0),
                               np.arange(3072, dtype=np.int64) + 7 * 10**9, "cal", 0)
    assert len(t["seq_ids"]) == 3072 and len(t["digest"]) == 3072


def test_duplicates_none():
    canon = np.random.default_rng(10).integers(0, 36, (40, 32)).astype(np.uint8)
    d = k4b_data.duplicates(canon)
    assert (d["n_rows"], d["n_unique"], d["max_multiplicity"]) == (40, 40, 1)
    assert d["n_duplicate_rows"] == 0


def digest_sets(seed=11):
    rng = np.random.default_rng(seed)
    rows = rng.integers(0, 36, (30, 32)).astype(np.uint8)
    dig = scores.history_digests(rows)
    return set(dig[:10]), set(dig[10:20]), set(dig[20:30])


@pytest.mark.parametrize("case", ["none", "cal_R1", "val_R1", "cal_val"])
def test_separation_cal_val_every_collision_is_lineage(case):
    cal, val, reg = digest_sets()
    if case == "cal_R1":
        reg = reg | {next(iter(cal))}
    elif case == "val_R1":
        reg = reg | {next(iter(val))}
    elif case == "cal_val":
        val = val | {next(iter(cal))}
    r = k4b_data.separation_cal_val(cal, val, reg)
    if case == "none":
        assert r["status"] == "PASS"
        assert r["collisions"] == {"cal_R1": 0, "val_R1": 0, "cal_val": 0}
    else:
        assert r["status"] == LINEAGE
        assert r["collisions"][case] == 1


def test_separation_fresh_collision_is_lineage():
    test, reg, _ = digest_sets(12)
    ok = k4b_data.separation_fresh(sorted(test), reg)
    assert ok["status"] == "PASS" and ok["collisions"]["test_R2"] == 0
    hit = k4b_data.separation_fresh(sorted(test), reg | {sorted(test)[3]})
    assert hit["status"] == LINEAGE and hit["collisions"]["test_R2"] >= 1


def two_blocks():
    return k4b_data.sequence_ids("cal", 0), k4b_data.sequence_ids("val", 0)


def test_seq_disjoint_pass():
    cal, val = two_blocks()
    assert k4b_data.seq_disjoint({"cal_b0": cal, "val_b0": val}, set())["status"] == "PASS"


def test_seq_disjoint_overlap_between_blocks_is_lineage():
    cal, val = two_blocks()
    val2 = np.concatenate([val[:-1], cal[:1]]).astype(np.int64)
    r = k4b_data.seq_disjoint({"cal_b0": cal, "val_b0": val2}, set())
    assert r["status"] == LINEAGE


@pytest.mark.parametrize("as_array", [False, True])
def test_seq_disjoint_frozen_union_hit_is_lineage(as_array):
    cal, val = two_blocks()
    union = [int(val[7]), 12345]
    union = np.asarray(union, dtype=np.int64) if as_array else set(union)
    r = k4b_data.seq_disjoint({"cal_b0": cal, "val_b0": val}, union)
    assert r["status"] == LINEAGE


def test_seq_disjoint_ranges_are_half_open():
    cal, val = two_blocks()
    blocks = {"cal_b0": cal, "val_b0": val}
    lo = int(min(cal.min(), val.min()))
    hi = int(max(cal.max(), val.max()))
    hit = k4b_data.seq_disjoint(blocks, set(), [(int(cal[100]), int(cal[100]) + 1)])
    assert hit["status"] == LINEAGE
    below = k4b_data.seq_disjoint(blocks, set(), [(lo - 100, lo)])
    above = k4b_data.seq_disjoint(blocks, set(), [(hi + 1, hi + 50)])
    assert below["status"] == "PASS" and above["status"] == "PASS"
    edge = k4b_data.seq_disjoint(blocks, set(), [(lo - 100, lo + 1)])
    assert edge["status"] == LINEAGE


# --------------------------------------------------------------- sealed-D-2a predicate (B17)

def predicate_rows():
    rng = np.random.default_rng(13)
    rows = rng.integers(5, 36, (6, 32)).astype(np.uint8)
    rows[0] = 0
    rows[1] = 4
    rows[2] = rng.integers(0, 5, 32)
    rows[3] = rng.integers(0, 5, 32)
    rows[3, 17] = 5  # one symbol outside the alphabet
    return rows


def test_sealed_d2a_predicate():
    got = np.asarray(k4b_data.sealed_d2a_predicate(predicate_rows()))
    assert got.dtype == np.bool_ and got.shape == (6,)
    assert got.tolist() == [True, True, True, False, False, False]


def test_predicate_hit_is_registry_incomplete_and_rows_kept():
    rows = predicate_rows()
    before = rows.copy()
    r = k4b_data.predicate_check(rows, ["sealed_d2a"])
    assert r["status"] == INCOMPLETE
    assert r["hits"] == {"sealed_d2a": 3}
    assert REASON in str(r)
    assert np.array_equal(rows, before)


def test_predicate_pass_without_hits():
    rows = np.random.default_rng(14).integers(0, 36, (100, 32)).astype(np.uint8)
    rows[:, 0] = 35
    r = k4b_data.predicate_check(rows, ["sealed_d2a"])
    assert r["status"] == "PASS" and r["hits"] == {"sealed_d2a": 0}
