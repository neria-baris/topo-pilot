"""Independent tests (author B, job 0026), TEST_PLAN B-5: histories, registry digests, separation.

Protocol §2.2 (fixed 4096-row streams, w33 and states dropped, panels), §2.3 (stream and
sequence-id rules), §2.4 (U_s unions and the three empty intersections), §16 row 2
(`check_first_token`); API.md §12. Written from the protocol and the four contract documents
only; no tools/c1prime source was read and nothing was executed by the author. References: the
unchanged `HMMSampler`, `SeedTree`, `dataset.checks` and K4 `scores.history_digests`.

Ambiguities recorded: `separation` is given the union digest sets U_cal, U_val and R1 (the
protocol's notation); `lowest` is required to return rows in ascending sequence_id order (the
landmark order of §14); the `history_table` key names are not fixed, so its three digest lists
are matched by value. `build_registry`'s `sources` format is not specified in API.md, so the
REGISTRY_INCOMPLETE rule is not tested here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset.checks import check_first_token, make_sequence_ids, process_code
from topo_pilot.dataset.sampler import HMMSampler

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_data  # noqa: E402
import scores  # noqa: E402

pytestmark = pytest.mark.analysis

LINEAGE = "FAIL_TECHNICAL/LINEAGE"


def _status(res) -> str:
    return res if isinstance(res, str) else res["status"]


def _stream(split, block):
    return SeedTree(0).generator("data", "c1-sf-v1", split, block, "cylinder", "overlap", "1.25")


def _process(N=6, V=36, seed=1):
    rng = np.random.default_rng(seed)
    T = rng.random((N, N)) + 0.1
    E = rng.random((N, V)) + 0.05
    return T / T.sum(axis=1, keepdims=True), E / E.sum(axis=1, keepdims=True), np.full(N, 1 / N)


def _tau(canon, k):
    a, b = canon // 6, canon % 6
    return 6 * ((a + k) % 6) + b


def _donor(canon32, k):
    out = canon32.astype(np.int64).copy()
    out[:, :31] = _tau(out[:, :31], k)
    return out


def test_history_stream_and_sequence_ids():
    for split, block in (("cal", 0), ("cal", 1), ("val", 0), ("test", 4)):
        got = c1_data.history_generator(split, block)
        assert np.array_equal(got.random(5), _stream(split, block).random(5))
        code = process_code("cylinder", "overlap", "1.25", f"c1-sf-v1/{split}/b{block}")
        ids = np.asarray(c1_data.sequence_ids(split, block))
        assert ids.dtype == np.int64 and ids.shape == (4096,)
        assert np.array_equal(ids, make_sequence_ids(code, "test", 4096))
    a, b = c1_data.sequence_ids("cal", 0), c1_data.sequence_ids("val", 0)
    assert np.intersect1d(a, b).size == 0
    assert np.intersect1d(c1_data.sequence_ids("cal", 0), c1_data.sequence_ids("cal", 1)).size == 0


def test_sample_block_is_one_fixed_4096_row_stream_with_w33_dropped():
    T, E, pi = _process()
    canon32, ids = c1_data.sample_block(T, E, pi, "val", 0)
    tokens, _ = HMMSampler(T, E, pi, SequenceLayout()).sample(4096, _stream("val", 0))
    canon32 = np.asarray(canon32)
    assert canon32.shape == (4096, 32) and canon32.dtype == np.uint8
    assert np.array_equal(canon32, tokens[:, :32])
    assert np.array_equal(np.asarray(ids), c1_data.sequence_ids("val", 0))


def test_panels_follow_rank_in_block():
    ids = np.random.default_rng(2).permutation(c1_data.sequence_ids("cal", 1))
    rank = np.empty(4096, dtype=np.int64)
    rank[np.argsort(ids, kind="stable")] = np.arange(4096)
    got = np.asarray(c1_data.panels(ids, 1))
    assert np.array_equal(got, 4 * 1 + rank // 1024)
    assert sorted(set(got.tolist())) == [4, 5, 6, 7]
    assert np.all(np.bincount(got)[4:] == 1024)


def test_lowest_selects_the_n_lowest_ids_in_ascending_id_order():
    ids = np.random.default_rng(3).permutation(c1_data.sequence_ids("val", 0))
    got = np.asarray(c1_data.lowest(ids, 512))
    assert got.dtype.kind in "iu" and got.shape == (512,)
    assert set(ids[got].tolist()) == set(np.sort(ids)[:512].tolist())
    assert np.all(np.diff(ids[got]) > 0)
    assert np.array_equal(np.asarray(c1_data.lowest(ids, 4)), np.argsort(ids)[:4])


def test_history_table_digests_of_H_and_both_donors():
    rng = np.random.default_rng(4)
    canon32 = rng.integers(0, 36, size=(20, 32)).astype(np.uint8)
    ids = np.arange(20, dtype=np.int64) + 10**12
    panel = np.zeros(20, dtype=np.int64)
    table = c1_data.history_table(canon32, ids, panel)
    expected = [scores.history_digests(canon32), scores.history_digests(_donor(canon32, 1)),
                scores.history_digests(_donor(canon32, -1))]
    found = [list(v) for v in table.values()
             if isinstance(v, (list, tuple, np.ndarray)) and len(v) == 20
             and all(isinstance(x, str) and len(x) == 64 for x in v)]
    for digests in expected:
        assert digests in found
    assert any(np.array_equal(np.asarray(v), canon32) for v in table.values()
               if isinstance(v, np.ndarray) and np.asarray(v).shape == (20, 32))
    assert np.array_equal(_donor(canon32, 1)[:, 31], canon32[:, 31])  # w32 kept


def test_registry_digests_are_the_history_digest_set():
    canon32 = np.random.default_rng(5).integers(0, 36, size=(30, 32)).astype(np.uint8)
    assert set(c1_data.registry_digests(canon32)) == set(scores.history_digests(canon32))


def _three_sets(seed):
    rng = np.random.default_rng(seed)
    hist = rng.integers(0, 36, size=(30, 32)).astype(np.uint8)
    roles = [set(scores.history_digests(h)) for h in (hist, _donor(hist, 1), _donor(hist, -1))]
    return roles, set().union(*roles)


def test_separation_passes_when_all_three_intersections_are_empty():
    (_, u_cal), (_, u_val), (_, r1) = _three_sets(6), _three_sets(7), _three_sets(8)
    assert _status(c1_data.separation(u_cal, u_val, r1)) == "PASS"


@pytest.mark.parametrize("collision", ["cal_H_vs_R1", "val_donor_vs_R1", "cal_Hp_vs_val_Hm",
                                       "cal_Hm_vs_val_H"])
def test_separation_collision_is_lineage_failure(collision):
    (cal_roles, u_cal), (val_roles, u_val), (_, r1) = (
        _three_sets(9), _three_sets(10), _three_sets(11))
    if collision == "cal_H_vs_R1":
        r1 = r1 | {next(iter(cal_roles[0]))}
    elif collision == "val_donor_vs_R1":
        r1 = r1 | {next(iter(val_roles[1]))}
    elif collision == "cal_Hp_vs_val_Hm":
        u_val = u_val | {next(iter(cal_roles[1]))}
    else:
        u_val = u_val | {next(iter(cal_roles[2]))}
    assert _status(c1_data.separation(u_cal, u_val, r1)) == LINEAGE


def test_first_token_ok_is_check_first_token_not_raising():
    T, E, pi = _process(seed=12)
    pE = pi @ E
    rng = np.random.default_rng(13)
    good = rng.choice(36, size=5000, p=pE / pE.sum())
    biased = np.zeros(5000, dtype=np.int64)

    def raises(first):
        try:
            check_first_token(first, pE, "val")
        except Exception:
            return True
        return False

    for first in (good, biased, good[:150]):
        assert bool(c1_data.first_token_ok(first, pE, "val")) is (not raises(first))
    assert not c1_data.first_token_ok(biased, pE, "val")
    assert c1_data.first_token_ok(good[:150], pE, "val")  # n < 200: test skipped, no raise
