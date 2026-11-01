"""Author B (job 0198): streams, sequence ids, history tables and names (protocol §2.1 S2, §2.8;
API §2.3). TEST_PLAN §3 row test_b_of_streams. Sampling only in the dry scope `hwsu-dry-v1` on a
synthetic 3-state world (V = 36); real-scope generators are created and compared but never
sampled from."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_pairs as up  # noqa: E402
import k4b_data  # noqa: E402
from topo_pilot.contracts import SeedTree, SequenceLayout  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402
from topo_pilot.dataset.sampler import HMMSampler  # noqa: E402

PROC = ("cylinder", "overlap", "1.75")
DRY = "hwsu-dry-v1"


def _world():
    T = np.array([[0.2, 0.5, 0.3], [0.3, 0.2, 0.5], [0.5, 0.3, 0.2]])  # doubly stochastic
    pi = np.full(3, 1 / 3)
    E = np.random.default_rng(7).random((3, 36)) + 0.05
    return T, E / E.sum(axis=1, keepdims=True), pi


def _first(g, k=64):
    return g.integers(0, 2**63, size=k)


# ------------------------------------------------------------------ generators (§2.8)
@pytest.mark.parametrize("scope,split,block", [("hwsu-of-v1", "of-fit", 0), ("hwsu-of-v1", "of-eval", 1),
                                               ("hwsu-of-v1", "of-eval/cf", 0), (DRY, "of-fit", 1)])
def test_generator_equals_seedtree(scope, split, block):
    got = _first(up.generator(scope, split, block))
    want = _first(SeedTree(0).generator("data", scope, split, block, *PROC))
    assert np.array_equal(got, want)


def test_generator_block_cast_and_process_argument():
    assert np.array_equal(_first(up.generator(DRY, "of-fit", np.int64(1))),
                          _first(SeedTree(0).generator("data", DRY, "of-fit", 1, *PROC)))
    other = ("cylinder", "overlap", "2.0")
    assert np.array_equal(_first(up.generator(DRY, "of-fit", 0, other)),
                          _first(SeedTree(0).generator("data", DRY, "of-fit", 0, *other)))
    assert not np.array_equal(_first(up.generator(DRY, "of-fit", 0)),
                              _first(up.generator(DRY, "of-fit", 0, other)))


def test_streams_distinct_across_scope_split_block():
    keys = [("hwsu-of-v1", "of-fit", 0), ("hwsu-of-v1", "of-fit", 1), ("hwsu-of-v1", "of-eval", 0),
            ("hwsu-of-v1", "of-eval/cf", 0), ("hwsu-v1", "of-fit", 0), (DRY, "of-fit", 0)]
    firsts = {tuple(_first(up.generator(*k), 4)) for k in keys}
    assert len(firsts) == len(keys)


# ------------------------------------------------------------------ sequence ids (§2.8)
@pytest.mark.parametrize("scope,split,block,arm", [("hwsu-of-v1", "of-fit", 0, "s"),
                                                   ("hwsu-of-v1", "of-eval", 1, "a1"),
                                                   ("hwsu-of-v1", "of-eval", 1, "a2"),
                                                   (DRY, "of-eval", 0, "a2")])
def test_seq_ids_rule(scope, split, block, arm):
    got = up.seq_ids(scope, split, block, arm, 50)
    want = make_sequence_ids(process_code(*PROC, f"{scope}/{split}/b{block}/{arm}"), "test", 50)
    assert got.dtype == np.int64 and np.array_equal(got, want)
    assert np.all(np.diff(got) > 0)


def test_seq_ids_distinct_across_arms_blocks_scopes():
    sets = [set(up.seq_ids(s, sp, b, a, 64).tolist())
            for s, sp, b, a in [("hwsu-of-v1", "of-eval", 0, "a1"), ("hwsu-of-v1", "of-eval", 0, "a2"),
                                ("hwsu-of-v1", "of-fit", 0, "s"), ("hwsu-of-v1", "of-eval", 1, "a1"),
                                (DRY, "of-eval", 0, "a1")]]
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            assert not sets[i] & sets[j]


@pytest.mark.parametrize("arm", ["a3", "S", "", "a"])
def test_seq_ids_unknown_arm(arm):
    with pytest.raises(ValueError):
        up.seq_ids(DRY, "of-fit", 0, arm, 4)


def test_contract_stream_and_id_rules():
    import json
    c = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
    assert c["sequence_ids"]["arms"] == {"of-fit": "s", "of-eval": ["a1", "a2"]}
    assert c["sizes"]["uniforms_per_arm2_row"] == 1 + 28 + 27
    assert c["streams"]["of-eval arm 2"].count('"of-eval/cf"') == 1


# ------------------------------------------------------------------ sampling (dry scope)
def test_sample_singles_stream_and_ids():
    T, E, pi = _world()
    s = up.sample_singles(T, E, pi, DRY, "of-fit", 0, 40)
    assert set(s) == {"canon32", "ids"}
    assert s["canon32"].dtype == np.uint8 and s["canon32"].shape == (40, 32)
    tok, _ = HMMSampler(T, E, pi, SequenceLayout()).sample(
        40, SeedTree(0).generator("data", DRY, "of-fit", 0, *PROC))
    assert np.array_equal(s["canon32"], tok[:, :32].astype(np.uint8))
    assert np.array_equal(s["ids"], up.seq_ids(DRY, "of-fit", 0, "s", 40))


def test_sample_pairs_streams_rows_and_ids():
    T, E, pi = _world()
    p = up.sample_pairs(T, E, pi, DRY, "of-eval", 1, 40)
    assert set(p) == {"a1", "a2", "ids_a1", "ids_a2"}
    tok, _ = HMMSampler(T, E, pi, SequenceLayout()).sample(
        40, SeedTree(0).generator("data", DRY, "of-eval", 1, *PROC))
    a1 = tok[:, :32].astype(np.uint8)
    assert np.array_equal(p["a1"], a1)
    a2 = up.sample_prefix(T, E, pi, a1, SeedTree(0).generator("data", DRY, "of-eval/cf", 1, *PROC))
    assert np.array_equal(p["a2"], a2)  # arm 2 uses the split + "/cf" stream
    assert p["a2"].dtype == np.uint8 and p["a2"].shape == (40, 32)
    assert np.array_equal(p["a1"][:, 28:], p["a2"][:, 28:])  # row i pairs with row i
    assert not np.array_equal(p["a1"][:, :28], p["a2"][:, :28])
    assert np.array_equal(p["ids_a1"], up.seq_ids(DRY, "of-eval", 1, "a1", 40))
    assert np.array_equal(p["ids_a2"], up.seq_ids(DRY, "of-eval", 1, "a2", 40))  # never sorted


def test_sampling_deterministic():
    T, E, pi = _world()
    a, b = up.sample_pairs(T, E, pi, DRY, "of-eval", 0, 30), up.sample_pairs(T, E, pi, DRY, "of-eval", 0, 30)
    assert all(np.array_equal(a[k], b[k]) for k in a)
    c = up.sample_pairs(T, E, pi, DRY, "of-eval", 1, 30)
    assert not np.array_equal(a["a1"], c["a1"])


# ------------------------------------------------------------------ history tables (§2.3)
@pytest.mark.parametrize("label", ["of-fit", "of-eval-a1", "of-eval-a2"])
def test_history_table(label):
    T, E, pi = _world()
    s = up.sample_singles(T, E, pi, DRY, "of-fit", 0, 24)
    t = up.history_table(s["canon32"], s["ids"], label, 1)
    assert set(t) >= {"canon32", "seq_ids", "digest", "landmark", "ref_row", "decoder_panel",
                      "split", "block"}
    assert t["canon32"].dtype == np.uint8 and t["seq_ids"].dtype == np.int64
    assert np.array_equal(t["canon32"], s["canon32"]) and np.array_equal(t["seq_ids"], s["ids"])
    assert not t["landmark"].any() and not t["ref_row"].any()
    assert np.all(t["decoder_panel"] == -1)
    assert list(t["digest"]) == list(k4b_data.digests(s["canon32"]))  # re-derivable from canon32
    assert t["split"] == label and t["block"] == 1
    arrays = up.table_arrays(t)
    assert set(arrays) == {"canon32", "seq_ids", "digest", "landmark", "ref_row", "decoder_panel"}
    assert all(np.array_equal(arrays[k], t[k]) for k in arrays)


@pytest.mark.parametrize("kind,block,dry,name", [
    ("fit", 0, False, "HIST_OF_fit_b0.npz"), ("eval_a1", 1, False, "HIST_OF_eval_a1_b1.npz"),
    ("eval_a2", 0, False, "HIST_OF_eval_a2_b0.npz"), ("fit", 1, True, "DRYHIST_OF_fit_b1.npz"),
    ("eval_a2", 1, True, "DRYHIST_OF_eval_a2_b1.npz")])
def test_hist_name(kind, block, dry, name):
    assert up.hist_name(kind, block, dry=dry) == name


def test_hist_names_follow_name_rule():
    import hwsu_records as ur
    for kind in ("fit", "eval_a1", "eval_a2"):
        for b in (0, 1):
            assert ur.name_class(f"stages/OF/{up.hist_name(kind, b)}") == "K4b history table"
            assert ur.name_class(f"stages/OF/{up.hist_name(kind, b, dry=True)}", dry=True) == \
                "K4b history table"
            assert ur.name_class(f"stages/OF/{up.hist_name(kind, b, dry=True)}") is None
