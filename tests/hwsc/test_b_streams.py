"""Author B (job 0176): streams, sequence IDs, the train/dev mirror (DRC4) and evaluation blocks.

Written from PROTOCOL_HWSC_v1.md sections 2.3-2.4, API.md sections 1.3 and 3.1-3.2, CONTRACT.json
`streams`, `sequence_ids`, `hist_file` and TEST_PLAN.md section 3 only. Block sampling uses the
dry binding and the tiny DRB1 world only; real-scope generators are compared draw for draw.
"""

from __future__ import annotations

import dataclasses
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
import hwsb_config  # noqa: E402
import hwsb_data  # noqa: E402
import hwsb_dry  # noqa: E402
import c2_registry  # noqa: E402
import k4b_data  # noqa: E402
from topo_pilot.contracts import ArtifactStore, MemoryBackend, ObservationSet, SeedTree  # noqa: E402
from topo_pilot.dataset import HMMSampler  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402

W_STAR = ("cylinder", "overlap", "1.75")
DRY = (629911, 629912, 629913)


def _ids(rep, split, n, process=W_STAR):
    return make_sequence_ids(process_code(*process, rep), split, n)


def _draws(gen, n=32):
    return gen.integers(0, 2**63, size=n)


@pytest.fixture
def dry_binding(tmp_path):
    def enter(case="DRC4"):
        return cb.bound_stage_c(cb.load_table(which="dry", case=case, case_dir=tmp_path / case))

    return enter


# ---------------------------------------------------------------- plans and run keys
def test_hwsc_plan_fields():
    p = cc.HWSC_PLAN
    assert isinstance(p, hwsb_config.Plan) and p.kind == "real" and not p.dry
    assert p.masters == cc.MASTERS and p.key == "W12-q1-s1.75-p0.2"
    assert tuple(p.process) == W_STAR and p.site == "resid_post_3"
    assert dict(p.sizes) == {"train": 131072, "dev": 4096}
    assert (p.gate_step, p.init_step) == (5000, 0)
    assert p.model_cfg == hwsb_config.MODEL_CFG and p.train_cfg == hwsb_config.TRAIN_CFG


@pytest.mark.parametrize("kind,sizes", [("dry_tiny", {"train": 4096, "dev": 512}),
                                        ("dry_e4", {"train": 2048, "dev": 256})])
def test_dry_plan(kind, sizes):
    p = cc.dry_plan(kind, "DRCX")
    ref = hwsb_config.dry_plan(kind, "DRCX")
    assert p.masters == DRY and dict(p.sizes) == sizes and p.key == "DRCX" and p.dry
    assert dataclasses.replace(ref, masters=DRY, sizes=p.sizes) == p


def test_dry_plan_refuses_other_kinds():
    with pytest.raises(ValueError):
        cc.dry_plan("real", "X")


def test_run_key_real_and_dry():
    assert cc.run_key(cc.HWSC_PLAN, 620302) == ("hwsc-v1", "W12-q1-s1.75-p0.2", 620302)
    dp = cc.dry_plan("dry_e4", "DRC2")
    assert cc.run_key(dp, 629912) == ("hwsc-v1", "DRY", "DRC2", 629912)
    with cb.bound_stage_c():
        assert tuple(hwsb_config.run_key(cc.HWSC_PLAN, 620302)) == cc.run_key(cc.HWSC_PLAN, 620302)
        assert tuple(hwsb_config.run_key(dp, 629912)) == cc.run_key(dp, 629912)


# ---------------------------------------------------------------- sequence IDs (train/dev)
@pytest.mark.parametrize("master", cc.MASTERS)
@pytest.mark.parametrize("split", ["train", "dev"])
def test_sequence_ids_real(split, master):
    want = _ids(f"hwsc-v1/{split}/{master}", split, 64)
    with cb.bound_stage_c():  # stream_record's master check reads hwsb_config.MASTERS
        got = cd.sequence_ids_c(split, 64, cc.HWSC_PLAN, master)
    assert got.dtype == np.int64 and np.array_equal(got, want)


def test_sequence_ids_dry_replicates():
    plan = cc.dry_plan("dry_tiny", "DRC4")
    with cb.bound_stage_c():
        for m in DRY:
            for split in ("train", "dev"):
                got = cd.sequence_ids_c(split, 32, plan, m)
                want = _ids(f"hwsc-v1/DRY/DRC4/{split}/{m}", split, 32, plan.process)
                assert np.array_equal(got, want)


@pytest.mark.parametrize("role", ["lgate", "cal", "val", "test", "LGATE", "CAL"])
def test_block_roles_refused(role):
    with cb.bound_stage_c(), pytest.raises(ValueError):
        cd.sequence_ids_c(role, 8, cc.HWSC_PLAN, 620301)


@pytest.mark.parametrize("master", [620201, 1729, 629911])
def test_master_outside_plan_refused(master):
    with cb.bound_stage_c(), pytest.raises(ValueError):
        cd.sequence_ids_c("train", 8, cc.HWSC_PLAN, master)


# ---------------------------------------------------------------- DRC4: the train/dev mirror
def _obs(store, oid):
    return store.load(ObservationSet, oid, consumer="experiment")


def test_drc4_mirror_equals_stage_b_unbound():
    plan = hwsb_config.dry_plan("dry_tiny", "T")
    s1, s2 = ArtifactStore(MemoryBackend()), ArtifactStore(MemoryBackend())
    p1, p2 = hwsb_dry.build_tiny_process(s1), hwsb_dry.build_tiny_process(s2)
    m = plan.masters[0]
    ref = hwsb_data.make_train_dev(s1, p1, m, plan)
    got = cd.make_train_dev_c(s2, p2, m, plan, scope="hwsb-v1")
    for split in ("train", "dev"):
        assert got[split] == ref[split]
        assert s2.meta(got[split]).payload_sha256 == s1.meta(ref[split]).payload_sha256
        a, b = _obs(s2, got[split]), _obs(s1, ref[split])
        assert np.array_equal(a.tokens, b.tokens) and np.array_equal(a.sequence_id, b.sequence_id)
        assert got["n"][split] == plan.sizes[split]
        assert got["replicates"][split] == f"hwsb-v1/DRY/T/{split}/{m}"
    assert got["streams"] == ref["streams"]


def test_drc4_hwsc_scope_differs_and_is_disjoint(dry_binding):
    bplan = hwsb_config.dry_plan("dry_tiny", "T")
    sb = ArtifactStore(MemoryBackend())
    pb = hwsb_dry.build_tiny_process(sb)
    ref = hwsb_data.make_train_dev(sb, pb, bplan.masters[0], bplan)
    ref_obs = {s: _obs(sb, ref[s]) for s in ("train", "dev")}
    sc = ArtifactStore(MemoryBackend())
    with dry_binding("DRC4"):
        plan = cc.dry_plan("dry_tiny", "DRC4")
        pc = hwsb_dry.build_tiny_process(sc, masters=DRY)
        got = cd.make_train_dev_c(sc, pc, DRY[0], plan, scope="hwsc-v1")
        s3 = ArtifactStore(MemoryBackend())
        p3 = hwsb_dry.build_tiny_process(s3, masters=DRY)
        same_plan_b = cd.make_train_dev_c(s3, p3, DRY[0], plan, scope="hwsb-v1")
    ref_ids = set(np.concatenate([o.sequence_id for o in ref_obs.values()]).tolist())
    for split in ("train", "dev"):
        o = _obs(sc, got[split])
        assert got[split] != ref[split]
        assert not np.array_equal(o.tokens, ref_obs[split].tokens)
        assert ref_ids.isdisjoint(set(o.sequence_id.tolist()))
        assert got["replicates"][split] == f"hwsc-v1/DRY/DRC4/{split}/{DRY[0]}"
        assert got["streams"][split][1] == "hwsc-v1"
        assert sc.meta(got[split]).config["study"] == "hwsc-v1"
        other = _obs(s3, same_plan_b[split]).sequence_id  # the scope argument changes the IDs
        assert set(other.tolist()).isdisjoint(set(o.sequence_id.tolist()))
        assert same_plan_b["replicates"][split] == f"hwsb-v1/DRY/DRC4/{split}/{DRY[0]}"
    assert set(got["streams"]) == {"train", "dev"}


# ---------------------------------------------------------------- evaluation blocks
def test_block_generator_formula_explicit_and_default():
    want = _draws(SeedTree(0).generator("data", "hwsc-v1", "cal", 0, *W_STAR))
    assert np.array_equal(_draws(cd.block_generator("cal", 0, scope="hwsc-v1",
                                                    process=W_STAR)), want)
    with cb.bound_stage_c():
        assert np.array_equal(_draws(cd.block_generator("cal", 0)), want)
    k4b = _draws(SeedTree(0).generator("data", "k4b-sf-v1", "cal", 0, "cylinder", "overlap",
                                       "1.25"))
    assert np.array_equal(_draws(cd.block_generator("cal", 0)), k4b)  # unbound: call-time K4b


def test_block_ids_formula():
    want = _ids("hwsc-v1/val/b2", "test", 16)
    got = cd.block_ids("val", 2, 16, scope="hwsc-v1", process=W_STAR)
    assert got.dtype == np.int64 and np.array_equal(got, want)
    with cb.bound_stage_c():
        assert np.array_equal(cd.block_ids("val", 2, 16), want)
        assert np.array_equal(cd.block_ids("cal", 0, 3072), k4b_data.sequence_ids("cal", 0))


def test_sample_block_c_equals_k4b_sample_block_under_dry_binding(dry_binding):
    proc = hwsb_dry.build_tiny_process(ArtifactStore(MemoryBackend()), masters=DRY)
    T, E, pi = proc["T"], proc["E_canon_shared"], proc["pi"]
    with dry_binding("DRC4"):
        c1, i1 = cd.sample_block_c(T, E, pi, "cal", 0, 3072)
        c2, i2 = k4b_data.sample_block(T, E, pi, "cal", 0)
    assert c1.dtype == c2.dtype == np.uint8 and c1.shape == (3072, 32)
    assert np.array_equal(c1, c2) and np.array_equal(i1, i2) and c1.tobytes() == c2.tobytes()


def test_sample_block_c_one_sampler_call_and_shape(dry_binding, monkeypatch):
    proc = hwsb_dry.build_tiny_process(ArtifactStore(MemoryBackend()), masters=DRY)
    calls, orig = [], HMMSampler.sample

    def spy(self, *a, **k):
        calls.append(a)
        return orig(self, *a, **k)

    monkeypatch.setattr(HMMSampler, "sample", spy)
    with dry_binding("DRC4"):
        out = cd.sample_block_c(proc["T"], proc["E_canon_shared"], proc["pi"], "lgate", 0, 512)
        ids_ref = cd.block_ids("lgate", 0, 512)
    assert len(calls) == 1 and calls[0][0] == 512
    assert isinstance(out, tuple) and len(out) == 2  # no states returned
    canon, ids = out
    assert canon.dtype == np.uint8 and canon.shape == (512, 32) and canon.flags.c_contiguous
    assert ids.dtype == np.int64 and np.all(np.diff(ids) > 0)
    assert np.array_equal(np.sort(ids_ref), ids)
    assert int(canon.max()) < 3  # tiny world, V = 3


def test_hist_names():
    assert cd.hist_name("cal", 0) == "HIST_cal_b0.npz"
    assert cd.hist_name("test", 3) == "HIST_test_b3.npz"
    assert cd.hist_name("lgate", 0, dry=True) == "DRYHIST_lgate_b0.npz"
    assert cd.hist_name("test", 1, dry=True) == "DRYHIST_test_b1.npz"
    assert not cd.hist_name("val", 0, dry=True).startswith("HIST_")


def test_save_table_six_keys_and_exclusive(tmp_path):
    rng = np.random.default_rng(3)
    canon = rng.integers(0, 36, (600, 32)).astype(np.uint8)
    table = k4b_data.history_table(canon, np.arange(10_000, 10_600, dtype=np.int64), "cal", 0)
    path = tmp_path / "table.npz"
    assert Path(cd.save_table(path, table)) == path
    with np.load(path, allow_pickle=False) as z:
        keys = {k: (z[k].dtype, z[k].shape) for k in z.files}
    want = {"canon32": np.uint8, "seq_ids": np.int64, "digest": np.dtype("<U64"),
            "landmark": np.bool_, "ref_row": np.bool_, "decoder_panel": np.int8}
    assert set(keys) == set(want) == set(cc.CONTRACT["hist_file"]["keys"])
    for k, dt in want.items():
        assert keys[k][0] == np.dtype(dt) and keys[k][1][0] == 600
    assert keys["canon32"][1] == (600, 32)
    before = path.read_bytes()
    with pytest.raises(Exception):
        cd.save_table(path, table)
    assert path.read_bytes() == before


def _tables(n=600, seed=0):
    rng = np.random.default_rng(seed)
    out = {}
    for i, s in enumerate(("lgate", "cal", "val")):
        canon = rng.integers(0, 36, (n, 32)).astype(np.uint8)
        out[s] = k4b_data.history_table(canon, np.arange(n, dtype=np.int64) + 10_000 * (i + 1),
                                        s, 0)
    return out


LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"


# ---------------------------------------------------------------- H2: separation_c
def _reg(digests=(), seq=(), ranges=None):
    return c2_registry.Registry(set(digests), None, ranges or {"pool": (9_000_000, 9_000_100)},
                                ["sealed_d2a"], {}, set(seq))


def _retable(t, split, canon):
    return k4b_data.history_table(canon, t["seq_ids"], split, 0)


def test_h2_clean_pass_and_keys():
    r = cd.separation_c(_reg(), _tables())
    assert r["status"] == "PASS"
    assert r["collisions"] == {"lgate_R": 0, "cal_R": 0, "val_R": 0, "lgate_cal": 0,
                               "lgate_val": 0, "cal_val": 0}
    assert set(r["predicates"]) == set(r["duplicates"]) == {"lgate", "cal", "val"}


def test_h2_planted_registry_digest_is_lineage():
    t = _tables()
    r = cd.separation_c(_reg({t["cal"]["digest"][5]}), t)
    assert r["status"] == LINEAGE and r["collisions"]["cal_R"] == 1


def test_h2_cross_split_collision_is_lineage():
    t = _tables()
    canon = t["cal"]["canon32"].copy()
    canon[0] = t["lgate"]["canon32"][0]
    t["cal"] = _retable(t["cal"], "cal", canon)
    r = cd.separation_c(_reg(), t)
    assert r["status"] == LINEAGE and r["collisions"]["lgate_cal"] == 1


def test_h2_seq_id_overlaps_are_lineage():
    t = _tables()
    val_id = int(t["val"]["seq_ids"][7])
    assert cd.separation_c(_reg(seq={val_id}), t)["status"] == LINEAGE
    cal_id = int(t["cal"]["seq_ids"][3])
    assert cd.separation_c(_reg(ranges={"p": (cal_id, cal_id + 1)}), t)["status"] == LINEAGE


def test_h2_d2a_predicate_row_is_incomplete():
    t = _tables()
    canon = t["val"]["canon32"].copy()
    canon[3] = np.array([0, 1, 2, 3, 4] * 6 + [0, 1], dtype=np.uint8)
    t["val"] = _retable(t["val"], "val", canon)
    assert cd.separation_c(_reg(), t)["status"] == INCOMPLETE


def test_h2_duplicates_counted_and_kept():
    t = _tables()
    canon = t["lgate"]["canon32"].copy()
    canon[2] = canon[1]
    t["lgate"] = _retable(t["lgate"], "lgate", canon)
    r = cd.separation_c(_reg(), t)
    assert r["status"] == "PASS" and r["duplicates"]["lgate"]["n_duplicate_rows"] == 1
    assert r["duplicates"]["lgate"]["n_rows"] == 600
