"""Author B (operations): T-SEED, T-POOL, T-REG (X6S1-FROZEN-v1 §6.1-§6.6, §14.3; API.md §3, §10).

Synthetic fixtures only (pytest tmp_path); no real store, pool, mailbox or K-REG2 is read.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_data as sd  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6s1_registry as sg  # noqa: E402
import x6s1_run as sr  # noqa: E402
import x6s1_stats as ss  # noqa: E402
import x6_model as xm  # noqa: E402
import x6_run as xr  # noqa: E402
import d2a_train  # noqa: E402
from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout  # noqa: E402
from topo_pilot.dataset import HMMSampler, PublicTokenDataset  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
ROWS = {"train": 2**20, "dev": 2**12, "smoke": 2**12, "prefix": 2**12, "val": 2**15,
        "test": 2**21}


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _specs():
    return list(sd.NONTEST_POOLS) + list(sd.TEST_POOLS)


def _toks(n, seed=3):
    return np.random.default_rng(seed).integers(0, 18, size=(n, 33), dtype=np.uint8)


# ---------------------------------------------------------------- T-SEED
def test_masters_are_registered_and_fresh_against_known_lineages():
    assert (sd.DATA_MASTER, sd.MODEL_MASTER, sd.SCOPE) == (2026101861, 2026101862, "x6s1")
    known = {xm.MASTER_SEED, 2026101531, 2026101532}  # x6 stage 0; D-2a DATA/MODEL
    assert not known & {sd.DATA_MASTER, sd.MODEL_MASTER}


@pytest.mark.parametrize("maps,fresh", [
    ([{"init/x6s0/1": 5}, {"cfg": {"master": 420700}}], True),
    ([{"a": {"b": [1, 2026101861]}}], False),
    ([{"model_master": 2026101862}], False),
    ([{"nested": [{"deep": np.int64(2026101861)}]}], False),
    ([], True),
])
def test_seed_fresh_compares_values_recursively(maps, fresh):
    # API-AMBIGUITY: seed_fresh(seed_maps) container type is not fixed; a list of maps is used.
    assert sr.seed_fresh(maps) is fresh


def test_data_streams_distinct_and_scoped():
    streams = [tuple(s["stream"]) for s in _specs()]
    assert len(streams) == 36 and len(set(streams)) == 36
    assert all(st[0] == "x6s1" for st in streams)
    seeds = {SeedTree(sd.DATA_MASTER).seed(*st) for st in streams}
    assert len(seeds) == 36
    extra = [("x6s1", "prefix_len"), ("x6s1", "feas")]
    assert not {SeedTree(sd.DATA_MASTER).seed(*e) for e in extra} & seeds


def test_model_streams_scope_map_and_arm_sharing():
    inits = {}
    for s in sd.SEEDS:
        want = SeedTree(sd.MODEL_MASTER).seed("init", "x6s1", s)
        for name in (f"NA-s{s}", f"AB-s{s}", f"ZC-s{s}", f"init-s{s}"):
            assert sd.run_key(name) == ("x6s1", s)
            assert sd.init_seed(name) == want  # identical init across arms for one seed
            ref = SeedTree(sd.MODEL_MASTER).generator("batch_order", "x6s1", s)
            assert sd.batch_generator(name).bit_generator.state == ref.bit_generator.state
        inits[s] = want
    smoke = sd.init_seed("SMOKE")
    assert sd.run_key("SMOKE") == ("x6s1", "smoke")
    assert smoke == SeedTree(sd.MODEL_MASTER).seed("init", "x6s1", "smoke")
    assert len(set(inits.values()) | {smoke}) == 5
    batch = {SeedTree(sd.MODEL_MASTER).seed("batch_order", "x6s1", s)
             for s in (1, 2, 3, 4, "smoke")}
    assert len(batch) == 5 and not batch & (set(inits.values()) | {smoke})


def test_partner_and_bootstrap_streams():
    assert sp.partner_seed("test_NA", 32, 7) == SeedTree(sd.DATA_MASTER).seed(
        "x6s1", "partner", "test_NA", 32, 7)
    seeds = {sp.partner_seed(p, 32, r) for p in ("test_NA", "val_NA") for r in range(4)}
    assert len(seeds) == 8
    g = ss.boot_stream("learn", "NA-s1")
    ref = SeedTree(sd.DATA_MASTER).generator("x6s1", "boot", "learn", "NA-s1")
    assert g.bit_generator.state == ref.bit_generator.state
    cord = SeedTree(sd.DATA_MASTER).generator("x6s1", "boot", "cord")
    assert ss.boot_stream("cord").bit_generator.state == cord.bit_generator.state
    assert g.bit_generator.state != ss.boot_stream("learn", "NA-s2").bit_generator.state


@pytest.mark.parametrize("name,want", [("NA-s3", ("NA", 3)), ("ZC-s1", ("ZC", 1)),
                                       ("init-s2", ("init", 2)), ("SMOKE", ("NA", "smoke"))])
def test_parse_model(name, want):
    assert sd.parse_model(name) == want


@pytest.mark.parametrize("bad", ["NA-s5", "XX-s1", "na-s1", "smoke", "NA-s0", ""])
def test_parse_model_refuses(bad):
    with pytest.raises(ValueError):
        sd.parse_model(bad)


# ---------------------------------------------------------------- T-POOL
def test_pool_table_order_sizes_splits_names():
    assert len(sd.NONTEST_POOLS) == 33 and len(sd.TEST_POOLS) == 3
    names = [s["name"] for s in _specs()]
    head = ["smoke", "gate_NA", "gate_AB", "gate_ZC", "prefix", "val_NA", "val_AB", "val_ZC"]
    tail = [f"{p}_{a}_s{s}" for a in sd.ARMS for s in sd.SEEDS for p in ("train", "dev")]
    assert names == head + tail + ["test_NA", "test_AB", "test_ZC"]
    total = 0
    for spec in _specs():
        pool = spec["pool"]
        want_rows = ROWS.get(pool) if pool != "gate" else (2**16 if spec["arm"] == "NA" else 2**14)
        assert spec["rows"] == want_rows, spec["name"]
        assert spec["split"] == {"train": "train", "test": "test"}.get(pool, "dev")
        total += spec["rows"]
    assert total == 19_128_320  # §6.1


@pytest.mark.parametrize("args,stream,code_args", [
    (("train", "AB", 3), ("x6s1", "train", "AB", 3), ("x6s1", "AB", "train", 3)),
    (("dev", "ZC", 1), ("x6s1", "dev", "ZC", 1), ("x6s1", "ZC", "dev", 1)),
    (("smoke",), ("x6s1", "smoke", "NA"), ("x6s1", "NA", "smoke", 0)),
    (("gate", "AB"), ("x6s1", "gate", "AB"), ("x6s1", "AB", "gate", 0)),
    (("prefix",), ("x6s1", "prefix"), ("x6s1", "NA", "prefix", 0)),
    (("val", "NA"), ("x6s1", "val", "NA"), ("x6s1", "NA", "val", 0)),
    (("test", "ZC"), ("x6s1", "test", "ZC"), ("x6s1", "ZC", "test", 0)),
])
def test_pool_spec_streams_and_codes(args, stream, code_args):
    spec = sd.pool_spec(*args)
    assert tuple(spec["stream"]) == stream
    assert spec["code"] == process_code(*code_args)
    assert spec["replicate"] == code_args[3]


@pytest.mark.parametrize("args", [("smoke", "AB"), ("train", "NA", 5), ("train", "NA", None),
                                  ("bogus", "NA"), ("prefix", "ZC"), ("test", "XX")])
def test_unregistered_pool_refused(args):
    with pytest.raises(ValueError):
        sd.pool_spec(*args)


def test_sequence_ids_exact_and_disjoint_across_all_pools():
    ranges = []
    for spec in _specs():
        ids = sd.sequence_ids(spec)
        assert ids.dtype == np.int64 and ids.shape == (spec["rows"],)
        assert np.array_equal(ids, make_sequence_ids(spec["code"], spec["split"], spec["rows"]))
        ranges.append((int(ids[0]), int(ids[-1])))
    ranges.sort()
    assert all(a[1] < b[0] for a, b in zip(ranges, ranges[1:]))


def test_sample_pool_returns_tokens_only_and_matches_sampler():
    spec = dict(sd.pool_spec("smoke"), rows=64)
    toks = sd.sample_pool(spec)
    assert isinstance(toks, np.ndarray) and toks.dtype == np.uint8 and toks.shape == (64, 33)
    m = xm.model("NA")
    gen = SeedTree(sd.DATA_MASTER).generator(*spec["stream"])
    ref = HMMSampler(m["Tf"], m["Ef"], m["pif"], SequenceLayout()).sample(64, gen)[0]
    assert np.array_equal(toks, ref)
    assert np.array_equal(sd.sample_pool(spec), toks)  # bit-identical regeneration
    obs = sd.observation_set(spec, toks)
    assert isinstance(obs, ObservationSet) and obs.split == "dev" and obs.V == 18
    assert {f.name for f in dataclasses.fields(obs)} <= {
        "split", "V", "sequence_id", "tokens", "layout_version"}  # no latent state field
    assert np.array_equal(obs.sequence_id, sd.sequence_ids(spec))
    assert len(PublicTokenDataset(obs, SequenceLayout())) == 64  # assert_public passes


def test_save_and_load_pool(tmp_path):
    toks = _toks(32)
    assert sd.token_digest(toks) == _sha(np.ascontiguousarray(toks).tobytes())
    path = tmp_path / "pool.npy"
    sha = sd.save_pool(path, toks)
    assert sha == _sha(path.read_bytes())
    back = np.load(path, allow_pickle=False)
    assert back.dtype == np.uint8 and np.array_equal(back, toks)
    with pytest.raises(FileExistsError):
        sd.save_pool(path, toks)
    assert np.array_equal(sd.load_pool(path, sha), toks)
    with pytest.raises(ValueError):
        sd.load_pool(path, "0" * 64)


# ---------------------------------------------------------------- T-REG
@pytest.mark.parametrize("counts,status", [
    ({"E_cue": 200306, "amb_nb": 13402}, "PASS"),
    ({"E_cue": 200305, "amb_nb": 13402}, LINEAGE),
    ({"E_cue": 200306, "amb_nb": 13403}, LINEAGE),
])
def test_stage0_regeneration_count_check(counts, status):
    assert sd.stage0_count_check(counts) == status


def test_row_digests_keys_and_hex():
    toks = _toks(5)
    dig = sg.row_digests(toks)
    assert dig.dtype == np.uint8 and dig.shape == (5, 32)
    for i in range(5):
        assert bytes(dig[i]) == hashlib.sha256(toks[i, :32].tobytes()).digest()
    keys = sg.digest_keys(dig)
    assert keys.dtype == np.uint64
    assert [int(k) for k in keys] == [int.from_bytes(bytes(d[:8]), "big") for d in dig]
    hexes = np.array([bytes(d).hex() for d in dig])
    assert np.array_equal(sg.hex_to_digests(hexes), dig)


def test_digest_set_runs_full_confirmation_and_hash(tmp_path):
    a = np.random.default_rng(5).integers(0, 256, size=(10, 32), dtype=np.uint8)
    near = a.copy()
    near[:, 31] ^= 1  # same 8-byte key, different full digest
    ds = sg.DigestSet.build([a[:4], a[4:], a[:2]], tmp_path / "runs", run=3)
    assert ds.n == len(ds.keys) == 12
    assert np.all(ds.keys[1:] >= ds.keys[:-1]) and ds.keys.dtype == np.uint64
    assert ds.contains(a).all() and not ds.contains(near).any()
    want = _sha(b"".join(sorted({bytes(r) for r in a})))
    assert ds.sha256() == want


def test_collision_mass():
    assert sg.collision_mass(3) == 3 * Fraction(1, 16) * Fraction(1, 5**31)
    assert abs(float(sg.collision_mass(1)) - 1.342e-23) < 1e-26


@pytest.mark.parametrize("kind", ["rows", "ids"])
def test_separation_collision_is_lineage(tmp_path, kind):
    # API-AMBIGUITY: separation(reg2, pools) argument types are not fixed by API.md; here reg2 is
    # the DigestSet of the non-test rows and pools maps pool name -> ObservationSet.
    tr, te, te2 = _toks(16, 1), _toks(16, 2), _toks(16, 4)

    def obs(split, code, t):
        return ObservationSet(split=split, V=18, sequence_id=make_sequence_ids(code, split, 16),
                              tokens=t)
    if kind == "rows":  # a test row equal to a registered (REG2) row
        te[3, :32] = tr[5, :32]
        pools = {"train_NA_s1": obs("train", 10, tr), "test_NA": obs("test", 11, te)}
    else:  # two test pools with one process code and split -> identical sequence ids
        pools = {"train_NA_s1": obs("train", 10, tr), "test_NA": obs("test", 12, te),
                 "test_AB": obs("test", 12, te2)}
    reg2 = sg.DigestSet.build([sg.row_digests(tr)], tmp_path / "runs", run=8)
    assert sg.separation(reg2, pools)["status"] == LINEAGE


def _x6_rows(n):
    return np.asarray(xr.sample("NA", n, SeedTree(9))[0], dtype=np.uint8)


def test_handoff_rows_malformed_json_is_incomplete(tmp_path):
    (tmp_path / "jobs").mkdir()
    (tmp_path / "jobs" / "ok.json").write_text(json.dumps({"h": [0] * 3}), encoding="utf-8")
    (tmp_path / "jobs" / "bad.json").write_text("{not json", encoding="utf-8")
    assert sg.handoff_rows(mailbox=tmp_path)["status"] == INCOMPLETE


def test_handoff_rows_keeps_x6_valid_lists(tmp_path):
    rows = _x6_rows(3)
    body = {"a": rows[0].tolist(), "b": rows[1, :32].tolist(), "junk": [0] * 32}
    (tmp_path / "rec.json").write_text(json.dumps(body), encoding="utf-8")
    out = sg.handoff_rows(mailbox=tmp_path)
    assert out["status"] != INCOMPLETE
    got = {bytes(np.asarray(r, dtype=np.uint8)[:32]) for r in out["rows"]}
    assert got == {bytes(rows[0, :32]), bytes(rows[1, :32])}


def _scratch(tmp_path):
    proj, scr = tmp_path / "proj", tmp_path / "scratch" / "0070"
    (proj / "empty").mkdir(parents=True)
    (scr / "cloud_in").mkdir(parents=True)
    return proj, scr


def test_inventory_registered_copy_passes(tmp_path):
    proj, scr = _scratch(tmp_path)
    p = scr / "cloud_in" / "train_copy.npy"
    np.save(p, _toks(8))
    out = sg.inventory_x6(proj, [scr], {_sha(p.read_bytes()): "train_NA_s1"})
    assert out["status"] == "PASS" and out["unclassified"] == []


def test_inventory_unregistered_npy_is_incomplete(tmp_path):
    proj, scr = _scratch(tmp_path)
    p = scr / "stray.npy"
    np.save(p, _toks(8))
    out = sg.inventory_x6(proj, [scr], {})
    assert out["status"] == INCOMPLETE
    assert any(Path(u).name == "stray.npy" for u in out["unclassified"])


def test_inventory_unregistered_observation_set_root_is_incomplete(tmp_path):
    proj, scr = _scratch(tmp_path)
    d = scr / "pools" / "ObservationSet" / "abc123"
    d.mkdir(parents=True)
    (d / "meta.json").write_text("{}", encoding="utf-8")
    np.savez(d / "payload.npz", tokens=_toks(8), sequence_id=np.arange(8, dtype=np.int64))
    assert sg.inventory_x6(proj, [scr], {})["status"] == INCOMPLETE


def test_inventory_unclassified_x6_directory_is_incomplete(tmp_path):
    proj, scr = _scratch(tmp_path)
    (proj / "x6-stray-store").mkdir()
    np.savez(proj / "x6-stray-store" / "hist.npz", tokens=_toks(8))
    assert sg.inventory_x6(proj, [scr], {})["status"] == INCOMPLETE


def test_no_sealed_d2a_predicate():
    src = Path(sg.__file__).read_text(encoding="utf-8")
    assert "sealed_d2a" not in src and "predicate_alphabet" not in src  # §6.6 item 2


# ---- RC10: bounded-memory K-REG2 reader vs k4b_registry.load on synthetic fixtures
def _kreg2(d, n=37, unsorted=False, edit=None):
    rng = np.random.default_rng(11)
    digests = sorted({_sha(rng.bytes(16)) for _ in range(n)})
    seqs = np.array(sorted(set(rng.integers(0, 2**40, size=n).tolist())), dtype=np.int64)
    arr = np.array(digests[::-1] if unsorted else digests)
    path = d / "K-REG2_digests.npz"
    with path.open("xb") as fh:
        np.savez_compressed(fh, digests=arr, seq_ids=seqs)
    man = {"version": "K-REG2", "status": "PASS", "n_digests": len(digests), "problems": [],
           "digests_sha256": _sha("\n".join(digests).encode()),
           "seq_id_union_sha256": _sha(seqs.tobytes()), "sealed_ranges": {},
           "d2a_ranges": {"pool1": [2**32, 2**32 + 5]}, "predicates": ["sealed_d2a"],
           "digest_file_sha256": _sha(path.read_bytes())}
    if edit:
        man.update(edit(man))
    (d / "K-REG2.json").write_text(json.dumps(man, indent=1, sort_keys=True) + "\n",
                                   encoding="utf-8")
    return digests, seqs, man


@pytest.mark.parametrize("run", [1, 5, 2**22])
def test_kreg2_reader_equals_k4b_load(tmp_path, run):
    import k4b_registry

    digests, seqs, man = _kreg2(tmp_path)
    d_set, s_set, _ranges, _preds, m = k4b_registry.load(tmp_path, "K-REG2")
    got = sg.read_kreg2(tmp_path, "K-REG2", run=run)
    assert got["n_digests"] == len(d_set) == len(digests)
    assert got["n_seq_ids"] == len(s_set) == len(seqs)
    assert got["dtype"] == "<U64" and list(got["shape"]) == [len(digests)]
    assert got["seq_dtype"] == "int64"
    assert got["digests_sha256"] == _sha("\n".join(sorted(d_set)).encode()) == m["digests_sha256"]
    assert got["seq_id_union_sha256"] == _sha(np.array(sorted(s_set), np.int64).tobytes())
    assert got["digest_file_sha256"] == m["digest_file_sha256"] and got["manifest"] == m
    keys = np.array(sorted(int(h[:16], 16) for h in d_set), dtype=np.uint64)
    assert got["keys"].dtype == np.uint64 and np.array_equal(got["keys"], keys)
    chunks = list(sg.iter_kreg2(tmp_path, "K-REG2", run=run))
    assert all(len(c) <= run and c.dtype == np.dtype("<U64") for c in chunks)
    assert np.concatenate(chunks).tolist() == sorted(d_set)
    seq_chunks = list(sg.iter_kreg2_seq_ids(tmp_path, "K-REG2", run))
    assert all(len(c) <= run and c.dtype == np.int64 for c in seq_chunks)
    assert np.concatenate(seq_chunks).tolist() == sorted(s_set)


@pytest.mark.parametrize("case", ["file_hash", "count", "union", "seq_union", "unsorted"])
def test_kreg2_reader_refuses_mismatch(tmp_path, case):
    edits = {"file_hash": lambda m: {"digest_file_sha256": "0" * 64},
             "count": lambda m: {"n_digests": m["n_digests"] + 1},
             "union": lambda m: {"digests_sha256": "1" * 64},
             "seq_union": lambda m: {"seq_id_union_sha256": "2" * 64}}
    _kreg2(tmp_path, unsorted=case == "unsorted", edit=edits.get(case))
    with pytest.raises(sg.RegistryError) as err:
        sg.read_kreg2(tmp_path, "K-REG2", run=4)
    assert err.value.status == LINEAGE
    if case in ("file_hash", "union"):
        import k4b_registry

        with pytest.raises(Exception):
            k4b_registry.load(tmp_path, "K-REG2")


# ---------------------------------------------------------------- T-RESOURCE (disk floors, §13.4)
@pytest.mark.parametrize("c,x,bad", [(2 * 10**9, 30 * 10**9, None), (2 * 10**9 - 1, 10**12, "C:"),
                                     (10**12, 30 * 10**9 - 1, "X:")])
def test_disk_floors(c, x, bad):
    why = d2a_train.disk_reason(usage=lambda d: SimpleNamespace(free=c if d[0] == "C" else x))
    assert why is None if bad is None else bad in why
