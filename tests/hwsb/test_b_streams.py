"""Author B (job 0161), TEST_PLAN section 3 `test_b_streams.py`: streams and sequence IDs
(section 2.3, RC-3, RC-12; DRB4, DRB16), sampling, canonical/named maps, hist blocks, H2-B.
Written from the protocol, API.md, CONTRACT.json and TEST_PLAN.md only; tools/hwsb/*.py unread."""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_data as hd  # noqa: E402
import hws_worlds as hw  # noqa: E402
import scores  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    ArtifactStore, MemoryBackend, ObservationSet, SeedTree, SequenceLayout)
from topo_pilot.dataset import DatasetConfig, DatasetStage, HMMSampler  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402
from topo_pilot.process.emission import EmissionConfig  # noqa: E402

KEY = "W12-q1-s1.75-p0.2"
REAL = hc.REAL_PLAN

def draw(g):
    return g.integers(0, 2**62, size=8).tolist()

def stop_status(excinfo):
    return str(excinfo.value.status)

# ------------------------------------------------------------------ generators (RC-3, RC-12)
@pytest.mark.parametrize("master", [620201, 620202])
@pytest.mark.parametrize("role", ["train", "dev"])
def test_real_train_dev_streams_match_contract(role, master):
    want = SeedTree(master).generator("data", "hwsb-v1", role, KEY, master)
    assert draw(hd.data_generator(role, REAL, master)) == draw(want)
    tree = SeedTree(master)
    assert draw(hd.data_generator(role, REAL, master, tree)) == draw(
        SeedTree(master).generator("data", "hwsb-v1", role, KEY, master))
    assert any(k.startswith("data/hwsb-v1/" + role) for k in tree.issued)


@pytest.mark.parametrize("role", ["LGATE", "CAL", "VAL"])
def test_real_block_streams_match_contract(role):
    want = SeedTree(0).generator("data", "hwsb-v1", role, KEY)
    assert draw(hd.data_generator(role, REAL)) == draw(want)


@pytest.mark.parametrize("kind", ["dry_tiny", "dry_e4"])
def test_dry_streams_match_contract(kind):
    plan = hc.dry_plan(kind, "BCASE")
    assert plan.dry and plan.key == "BCASE" and not REAL.dry
    for role in ("train", "dev"):
        for m in (629901, 629902):
            want = SeedTree(m).generator("data", "hwsb-v1", "DRY", "BCASE", role, m)
            assert draw(hd.data_generator(role, plan, m)) == draw(want)
    for role in ("LGATE", "CAL", "VAL"):
        want = SeedTree(0).generator("data", "hwsb-v1", "DRY", "BCASE", role)
        assert draw(hd.data_generator(role, plan)) == draw(want)


def test_dry_plan_rejects_unknown_kind():
    with pytest.raises(ValueError):
        hc.dry_plan("dry_huge", "x")


DRY = hc.dry_plan("dry_tiny", "BCASE")
REFUSALS = [
    ("unknown role", lambda f: f("bogus", REAL, 620201)),
    ("train without master", lambda f: f("train", REAL)),
    ("dev without master", lambda f: f("dev", REAL, None)),
    ("block with master", lambda f: f("LGATE", REAL, 620201)),
    ("master not in plan", lambda f: f("train", REAL, 123456)),
    ("dry master in real plan", lambda f: f("train", REAL, 629901)),
    ("real master in dry plan", lambda f: f("train", DRY, 620201)),
    ("foreign dry master", lambda f: f("dev", DRY, 777777)),
    ("block with master in dry plan", lambda f: f("CAL", DRY, 629901)),
]


@pytest.mark.parametrize("name,call", REFUSALS, ids=[r[0] for r in REFUSALS])
def test_data_generator_refusals(name, call):
    with pytest.raises(ValueError):
        call(hd.data_generator)


def test_foreign_tree_is_refused():
    with pytest.raises(ValueError):
        hd.data_generator("train", REAL, 620201, SeedTree(620202))


@pytest.mark.parametrize("name,call", REFUSALS, ids=[r[0] for r in REFUSALS])
def test_sequence_ids_refusals(name, call):
    with pytest.raises(ValueError):
        call(lambda role, plan, master=None: hd.sequence_ids(role, 8, plan, master))

# ------------------------------------------------------------------ sequence IDs
def test_sequence_ids_follow_contract_replicates():
    got = hd.sequence_ids("train", 40, REAL, 620201)
    want = make_sequence_ids(process_code("cylinder", "overlap", "1.75", "hwsb-v1/train/620201"),
                             "train", 40)
    assert got.dtype == np.int64 and np.array_equal(got, want)
    want = make_sequence_ids(process_code("cylinder", "overlap", "1.75", "hwsb-v1/dev/620202"),
                             "dev", 7)
    assert np.array_equal(hd.sequence_ids("dev", 7, REAL, 620202), want)
    for role in ("LGATE", "CAL", "VAL"):
        want = make_sequence_ids(process_code("cylinder", "overlap", "1.75", f"hwsb-v1/{role}"),
                                 "test", 50)
        assert np.array_equal(hd.sequence_ids(role, 50, REAL), want)


def test_dry_sequence_ids_follow_contract_replicates():
    proc = ("cylinder", "overlap", "1.0")
    assert DRY.process == proc
    want = make_sequence_ids(process_code(*proc, "hwsb-v1/DRY/BCASE/train/629901"), "train", 9)
    assert np.array_equal(hd.sequence_ids("train", 9, DRY, 629901), want)
    want = make_sequence_ids(process_code(*proc, "hwsb-v1/DRY/BCASE/VAL"), "test", 9)
    assert np.array_equal(hd.sequence_ids("VAL", 9, DRY), want)


def test_real_tables_have_pairwise_disjoint_ids():
    tables = {f"{r}_{m}": hd.sequence_ids(r, REAL.sizes[r], REAL, m)
              for m in hc.MASTERS for r in ("train", "dev")}
    tables.update({r: hd.sequence_ids(r, REAL.sizes[r], REAL) for r in ("LGATE", "CAL", "VAL")})
    assert tables["train_620201"].size == 131072 and tables["VAL"].size == 3072
    names = list(tables)
    for i, a in enumerate(names):
        assert np.unique(tables[a]).size == tables[a].size
        for b in names[i + 1:]:
            assert np.intersect1d(tables[a], tables[b]).size == 0, (a, b)


def test_stream_record_lists_the_scope():
    rec = hd.stream_record("LGATE", REAL)
    assert [str(x) for x in rec] == ["data", "hwsb-v1", "LGATE", KEY]
    # API-AMBIGUITY: the master inside a train/dev record may be an int or a string.
    rec = hd.stream_record("train", REAL, 620201)
    assert [str(x) for x in rec] == ["data", "hwsb-v1", "train", KEY, "620201"]

# ------------------------------------------------------------------ DRB4: E4 scopes
@pytest.fixture(scope="module")
def w0():
    store = ArtifactStore(MemoryBackend())
    cfg = EmissionConfig("overlap", 36, 1.25, "grid")
    return store, hd.build_process(store, masters=(1729,), emission_cfg=cfg)


def test_sample_observations_equals_dataset_stage_bitwise(w0):
    store, proc = w0
    cfg = DatasetConfig(n_train=256, n_dev=256, n_test=512, n_panels=2, panel_size=256)
    ids = DatasetStage().run(proc["ids"]["transition"], proc["ids"]["emission"][1729], cfg,
                             SeedTree(1729), store)
    for split in ("train", "dev"):
        ref = store.load(ObservationSet, ids[f"obs_{split}"], consumer="experiment").tokens
        rng = SeedTree(1729).generator("data", split, "cylinder", "overlap", "1.25", 1729)
        got = hd.sample_observations(proc["T"], proc["E_named"][1729], proc["pi"],
                                     proc["perm"][1729], 256, rng, split)
        assert got.dtype == ref.dtype == np.uint8 and got.shape == (256, 33)
        assert np.array_equal(got, ref)

# ------------------------------------------------------------------ sample_block / sample_observations
TINY = hw.build_tiny()
T3, E3, PI3 = TINY["T"], TINY["E"], TINY["pi"]
PERM3 = np.array([2, 0, 1])


def named_tiny():
    E_named = np.empty_like(E3)
    E_named[:, PERM3] = E3
    return E_named


@pytest.fixture
def spy(monkeypatch):
    calls, original = [], HMMSampler.sample

    def sample(self, n, rng):
        calls.append(n)
        return original(self, n, rng)

    monkeypatch.setattr(HMMSampler, "sample", sample)
    return calls


def test_sample_block_one_call_contiguous_uint8_without_w33(spy):
    out = hd.sample_block(T3, E3, PI3, 300, np.random.default_rng(5))
    assert spy == [300]
    assert out.dtype == np.uint8 and out.shape == (300, 32) and out.flags["C_CONTIGUOUS"]
    ref, _ = HMMSampler(T3, E3, PI3, SequenceLayout()).sample(300, np.random.default_rng(5))
    assert np.array_equal(out, ref[:, :32])


def test_sample_observations_one_call_named_tokens(spy):
    got = hd.sample_observations(T3, named_tiny(), PI3, PERM3, 300, np.random.default_rng(6),
                                 "train")
    assert spy == [300] and got.shape == (300, 33) and got.dtype == np.uint8
    canon, _ = HMMSampler(T3, E3, PI3, SequenceLayout()).sample(300, np.random.default_rng(6))
    assert np.array_equal(got, PERM3[canon.astype(np.int64)])


def planted(monkeypatch, edit):
    original = HMMSampler.sample

    def sample(self, n, rng):
        tokens, states = original(self, n, rng)
        tokens, states = tokens.copy(), states.copy()
        edit(tokens, states)
        return tokens, states

    monkeypatch.setattr(HMMSampler, "sample", sample)


def bad_range(tokens, states):
    states[0, 5] = 12  # N = 12


def biased_first(tokens, states):
    tokens[:, 0] = 0


@pytest.mark.parametrize("edit", [bad_range, biased_first])
def test_sampler_defects_fail_technical(monkeypatch, edit):
    planted(monkeypatch, edit)
    with pytest.raises(hc.HwsbStop) as e:
        hd.sample_block(T3, E3, PI3, 1000, np.random.default_rng(1))
    assert stop_status(e) == "FAIL_TECHNICAL/SAMPLER"
    with pytest.raises(hc.HwsbStop) as e:
        hd.sample_observations(T3, named_tiny(), PI3, PERM3, 1000, np.random.default_rng(1), "dev")
    assert stop_status(e) == "FAIL_TECHNICAL/SAMPLER"

# ------------------------------------------------------------------ canonical / named / inputs
def test_canonical32_and_named32_invert_exactly():
    rng = np.random.default_rng(3)
    perm = rng.permutation(36)
    canon = rng.integers(0, 36, size=(20, 33)).astype(np.uint8)
    named = perm[canon.astype(np.int64)].astype(np.uint8)
    got = hd.canonical32(named, perm)
    assert got.shape == (20, 32) and got.dtype == np.uint8
    assert np.array_equal(got, canon[:, :32])
    back = hd.named32(got, perm)
    assert back.dtype == np.uint8 and np.array_equal(back, named[:, :32])


def test_model_inputs_have_bos_36_and_width_33():
    rng = np.random.default_rng(4)
    perm = rng.permutation(36)
    canon = rng.integers(0, 36, size=(6, 32)).astype(np.uint8)
    x = hd.model_inputs(canon, perm)
    assert tuple(x.shape) == (6, 33) and str(x.dtype) == "torch.int64"
    assert (x[:, 0] == 36).all()
    assert np.array_equal(x[:, 1:].numpy(), perm[canon.astype(np.int64)])


def test_lowest_rows_picks_the_lowest_ids():
    ids = np.arange(1000, 1020, dtype=np.int64)
    assert np.array_equal(hd.lowest_rows(ids, 5), np.arange(5))
    assert hd.lowest_rows(np.arange(2000, dtype=np.int64)).size == 512
    shuffled = np.array([50, 10, 40, 20, 30, 60])
    rows = hd.lowest_rows(shuffled, 3)
    # SPEC-QUESTION: "row indices of the n lowest IDs, ascending" may mean ascending row index
    # or ascending ID; only the selected set is asserted.
    assert sorted(shuffled[rows].tolist()) == [10, 20, 30]

# ------------------------------------------------------------------ blocks on disk
def tiny_proc():
    return {"T": T3, "E_canon_shared": E3, "pi": PI3}


def small_plan():
    return replace(hc.dry_plan("dry_tiny", "BBLK"),
                   sizes={"train": 256, "dev": 64, "LGATE": 256, "CAL": 128, "VAL": 128})


def test_make_block_matches_independent_sampling():
    plan, role = small_plan(), "CAL"
    block = hd.make_block(tiny_proc(), role, plan)
    rng = SeedTree(0).generator("data", "hwsb-v1", "DRY", "BBLK", role)
    ref, _ = HMMSampler(T3, E3, PI3, SequenceLayout()).sample(128, rng)
    assert np.array_equal(block["canon32"], ref[:, :32]) and block["role"] == role
    want = make_sequence_ids(process_code("cylinder", "overlap", "1.0", "hwsb-v1/DRY/BBLK/CAL"),
                             "test", 128)
    assert np.array_equal(block["seq_ids"], want) and (np.diff(block["seq_ids"]) == 1).all()
    assert list(block["digest_canon32"]) == scores.history_digests(ref[:, :32])
    again = hd.make_block(tiny_proc(), role, plan)
    assert np.array_equal(again["canon32"], block["canon32"])


def test_block_round_trip_and_exclusive_create(tmp_path):
    block = hd.make_block(tiny_proc(), "LGATE", small_plan())
    path = Path(hd.save_block(tmp_path, block))
    assert path == tmp_path / "hist" / "LGATE.npz" and path.is_file()
    with np.load(path, allow_pickle=False) as z:
        assert set(z.files) == {"canon32", "seq_ids", "digest_canon32"}
        assert z["canon32"].dtype == np.uint8 and z["canon32"].shape == (256, 32)
        assert z["seq_ids"].dtype == np.int64 and z["seq_ids"].shape == (256,)
        assert z["digest_canon32"].dtype == np.dtype("<U64")
    before = path.read_bytes()
    loaded = hd.load_block(path)
    # API-AMBIGUITY: the returned dict may carry extra keys (e.g. role); the file keys are exact.
    assert set(loaded) >= {"canon32", "seq_ids", "digest_canon32"}
    assert np.array_equal(loaded["canon32"], block["canon32"])
    assert np.array_equal(loaded["seq_ids"], block["seq_ids"])
    assert list(loaded["digest_canon32"]) == list(block["digest_canon32"])
    with pytest.raises(Exception):
        hd.save_block(tmp_path, block)
    assert path.read_bytes() == before


def test_tampered_digest_fails_load_block(tmp_path):
    block = hd.make_block(tiny_proc(), "VAL", small_plan())
    digests = np.asarray(block["digest_canon32"], dtype="<U64").copy()
    digests[3] = "0" * 64
    bad = tmp_path / "VAL.npz"
    np.savez(bad, canon32=block["canon32"], seq_ids=block["seq_ids"], digest_canon32=digests)
    with pytest.raises(hc.HwsbStop) as e:
        hd.load_block(bad)
    assert stop_status(e) == "FAIL_TECHNICAL/LINEAGE"

# ------------------------------------------------------------------ H2-B (DRB16)
def rows(seed, n):
    return np.random.default_rng(seed).integers(0, 36, size=(n, 32)).astype(np.uint8)


def blk(canon, start):
    return {"canon32": canon, "seq_ids": np.arange(start, start + len(canon), dtype=np.int64),
            "digest_canon32": scores.history_digests(canon)}


def tables(**edit):
    t = {"LGATE": rows(1, 30), "CAL": rows(2, 30), "VAL": rows(3, 30)}
    td = {"train_620201": rows(4, 60), "dev_620201": rows(5, 20),
          "train_620202": rows(6, 60), "dev_620202": rows(7, 20)}
    t.update({k: v for k, v in edit.items() if k in t})
    td.update({k: v for k, v in edit.items() if k in td})
    blocks = {r: blk(t[r], 1000 * (i + 1)) for i, r in enumerate(("LGATE", "CAL", "VAL"))}
    train_dev = {n: (c, np.arange(10**6 * (i + 1), 10**6 * (i + 1) + len(c), dtype=np.int64))
                 for i, (n, c) in enumerate(td.items())}
    return blocks, train_dev


def test_separation_clean_tables_pass():
    blocks, train_dev = tables()
    res = hd.separation(blocks, train_dev)
    assert res["status"] == "PASS" and res["id_overlap"] is None
    assert res["hws_store_collisions"] is None
    assert all(v == 0 for v in res["collisions"].values())


def test_separation_eval_train_collision_fails_lineage():  # DRB16
    c = rows(1, 30)
    c[7] = rows(4, 60)[11]
    blocks, train_dev = tables(LGATE=c)
    res = hd.separation(blocks, train_dev)
    assert res["status"] == "FAIL_TECHNICAL/LINEAGE"
    assert res["collisions"]["LGATE|train_dev"] == 1


def test_separation_eval_eval_collision_fails_lineage():
    c = rows(3, 30)
    c[0] = rows(2, 30)[4]
    blocks, train_dev = tables(VAL=c)
    res = hd.separation(blocks, train_dev)
    assert res["status"] == "FAIL_TECHNICAL/LINEAGE" and res["collisions"]["CAL|VAL"] == 1


def test_separation_id_overlap_fails_lineage():
    blocks, train_dev = tables()
    blocks["CAL"]["seq_ids"] = blocks["LGATE"]["seq_ids"].copy()
    res = hd.separation(blocks, train_dev)
    assert res["status"] == "FAIL_TECHNICAL/LINEAGE" and res["id_overlap"]


def test_duplicates_are_counted_and_kept():
    d = ["a", "b", "a", "c", "a", "b"]
    got = hd.duplicates(d)
    assert (got["n_rows"], got["n_unique"], got["n_duplicate_rows"], got["max_multiplicity"]) \
        == (6, 3, 3, 3)
    c = rows(1, 30)
    c[5] = c[6]
    blocks, train_dev = tables(LGATE=c)
    res = hd.separation(blocks, train_dev)
    # API-AMBIGUITY: duplicates keyed by table name (role or train_dev name).
    assert res["duplicates"]["LGATE"]["n_duplicate_rows"] == 1
    assert res["status"] == "PASS" and len(blocks["LGATE"]["canon32"]) == 30


def test_hws_collisions_are_reported_not_gating():
    blocks, train_dev = tables()
    hws = {blocks["LGATE"]["digest_canon32"][2], "f" * 64}
    res = hd.separation(blocks, train_dev, hws)
    assert res["status"] == "PASS"
    assert res["hws_store_collisions"]["LGATE"] == 1
    assert res["hws_store_collisions"]["CAL"] == 0
