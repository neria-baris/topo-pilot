"""Author B: streams carry the world key; seeds; disjointness (protocol 2.4, G4, KG2, DRG4)."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import CONTRACT, TAGS, mod  # noqa: E402


def _lib():
    mod("gc")
    from topo_pilot.contracts import SeedTree
    from topo_pilot.dataset.checks import make_sequence_ids, process_code
    return SeedTree, make_sequence_ids, process_code


def _draw(g, n=8):
    return np.asarray(g.random(n))


@pytest.mark.parametrize("tag", TAGS)
def test_train_dev_generators_carry_world_key(tag):
    gb, gc = mod("gb"), mod("gc")
    SeedTree, _, _ = _lib()
    W = gc.world(tag)
    hd = importlib.import_module("hwsb_data")
    with gb.world(tag):
        for split in ("train", "dev"):
            for m in W.masters:
                got = hd.data_generator(split, gc.plan(tag), m, SeedTree(m))
                exp = SeedTree(m).generator("data", "hwsg-v1", split, W.key, m)  # OPEN-1
                assert np.array_equal(_draw(got), _draw(exp)), (split, m)


@pytest.mark.parametrize("tag", TAGS)
def test_block_generators_and_ids(tag):
    gb, gc = mod("gb"), mod("gc")
    SeedTree, make_ids, pcode = _lib()
    W = gc.world(tag)
    hdata = importlib.import_module("hwsc_data")
    with gb.world(tag):
        for split in ("lgate", "cal", "val"):
            for b in (0, 1):
                got = hdata.block_generator(split, b)
                exp = SeedTree(0).generator("data", "hwsg-v1/" + W.key, split, b, *W.process)
                assert np.array_equal(_draw(got), _draw(exp))
                ids = hdata.block_ids(split, b, 64)
                code = pcode(W.process[0], W.process[1], "|".join(W.process[2:]),  # erratum E1
                             f"hwsg-v1/{W.key}/{split}/b{b}")
                assert np.array_equal(np.asarray(ids), np.asarray(make_ids(code, "test", 64)))


def test_train_dev_sequence_ids_follow_scope_role_master():
    gb, gc = mod("gb"), mod("gc")
    _, make_ids, pcode = _lib()
    hdata = importlib.import_module("hwsc_data")
    W = gc.world("mid")
    with gb.world("mid"):
        m = W.masters[0]
        got = hdata.sequence_ids_c("train", 64, gc.plan("mid"), m, "hwsg-v1")
        exp = make_ids(pcode(W.process[0], W.process[1], "|".join(W.process[2:]),  # erratum E1
                             f"hwsg-v1/train/{m}"), "train", 64)
        assert np.array_equal(np.asarray(got), np.asarray(exp))


def test_cal_draws_differ_across_worlds_and_from_stage_c():
    gb, gc = mod("gb"), mod("gc")
    hdata = importlib.import_module("hwsc_data")
    first = {}
    for tag in TAGS:
        with gb.world(tag):
            first[tag] = tuple(_draw(hdata.block_generator("cal", 0), 64).tolist())
    star = tuple(_draw(hdata.block_generator("cal", 0), 64).tolist())  # stage C binding
    assert len({first[t] for t in TAGS} | {star}) == 4


def test_lgate_cal_val_id_sets_pairwise_disjoint_across_worlds():
    gb = mod("gb")
    hdata = importlib.import_module("hwsc_data")
    sets = {}
    for tag in TAGS:
        with gb.world(tag):
            for split in ("lgate", "cal", "val"):
                sets[(tag, split)] = set(np.asarray(hdata.block_ids(split, 0, 64)).tolist())
    keys = list(sets)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            assert not (sets[a] & sets[b]), (a, b)


def test_planted_shared_sigma_pair_collides_under_sigma_only_tags():
    SeedTree, _, _ = _lib()
    sig = "2.0"
    a = SeedTree(0).generator("data", "hwsg-v1", "cal", 0, "cylinder", "overlap", sig)
    b = SeedTree(0).generator("data", "hwsg-v1", "cal", 0, "cylinder", "overlap", sig)
    assert np.array_equal(_draw(a), _draw(b))  # the hazard (DRG4)
    wa = ("cylinder", "overlap", sig, "0.2", "W-a")
    wb = ("cylinder", "overlap", sig, "0.5", "W-b")
    ga = SeedTree(0).generator("data", "hwsg-v1/W-a", "cal", 0, *wa)
    gb_ = SeedTree(0).generator("data", "hwsg-v1/W-b", "cal", 0, *wb)
    assert not np.array_equal(_draw(ga), _draw(gb_))


@pytest.mark.parametrize("tag", TAGS)
def test_seeds_masters_and_run_keys_equal_contract(tag):
    gc = mod("gc")
    W, c = gc.world(tag), CONTRACT["worlds"][tag]
    assert dict(W.seeds) == c["seeds"] and list(W.masters) == c["masters"]
    assert tuple(W.p1_seeds) == tuple(c["p1_seeds"])
    for m in W.masters:
        assert tuple(gc.run_key(tag, m)) == ("hwsg-v1", c["key"], m)
        assert tuple(gc.run_key(c["key"], m)) == ("hwsg-v1", c["key"], m)
    assert len({m for t in TAGS for m in gc.world(t).masters}) == 9
    allseeds = [v for t in TAGS for v in gc.world(t).seeds.values()]
    assert len(set(allseeds)) == len(allseeds) == 15
    assert tuple(W.process) == tuple(c["process_code_args"])


def test_dry_seeds_and_masters_do_not_touch_real_ones():
    gc = mod("gc")
    real = {m for t in TAGS for m in gc.world(t).masters}
    real |= {v for t in TAGS for v in gc.world(t).seeds.values()}
    dry = {m for ms in gc.DRY_MASTERS.values() for m in ms} | set(gc.DRY_SEEDS.values())
    assert not (real & dry)
    assert sorted(m for ms in gc.DRY_MASTERS.values() for m in ms) == list(range(620901, 620910))
