"""Author B: blocks, streams and sequence IDs, tables, H2-D, risk, references, controls (§2.5, §4.2)."""

from __future__ import annotations  # noqa: I001

import json
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_bind as db  # noqa: E402
import hwsd_data as dd  # noqa: E402
import test_b_util as bu  # noqa: E402

import c2_registry  # noqa: E402
import hwsb_dry  # noqa: E402
import hwsb_eval  # noqa: E402
import hwsc_data  # noqa: E402
import k4b_driver  # noqa: E402
import k4b_scores  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
from topo_pilot.contracts import ArtifactStore, MemoryBackend, SeedTree  # noqa: E402
from topo_pilot.dataset import HMMSampler  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402

PASS, INC, LIN = "PASS", "INCONCLUSIVE/REGISTRY_INCOMPLETE", "FAIL_TECHNICAL/LINEAGE"
PROC = ("cylinder", "overlap", "1.75")
DTYPES = {"canon32": np.uint8, "seq_ids": np.int64, "landmark": np.bool_, "ref_row": np.bool_,
          "decoder_panel": np.int8}


def _draws(g, n=16):
    return g.integers(0, 2**63, size=n).tolist()


def test_contract_stream_formulas():
    s = dc.CONTRACT["streams"]
    assert s["order"] == ["lgate", "cal", "val", "test"] == list(dc.SPLITS)
    for split, row in s["blocks"].items():
        assert row["generator"] == (f"SeedTree(0).generator('data', 'hwsd-v1', '{split}', 0, "
                                    "'cylinder', 'overlap', '1.75')")
        assert f"'hwsd-v1/{split}/b0'" in row["sequence_ids"] and row["n"] == dc.SIZES[split]


@pytest.mark.parametrize("split", ["lgate", "cal", "val", "test"])
def test_block_generator_and_ids_under_the_binding(split):
    ref = _draws(SeedTree(0).generator("data", "hwsd-v1", split, 0, *PROC))
    ids_ref = make_sequence_ids(process_code(*PROC, f"hwsd-v1/{split}/b0"), "test", 64)
    with db.bound_hwsd():
        assert _draws(dd.block_generator(split)) == ref
        assert np.array_equal(dd.block_ids(split, 64), ids_ref)
    assert _draws(dd.block_generator(split, scope="hwsd-v1", process=PROC)) == ref
    assert np.array_equal(dd.block_ids(split, 64, scope="hwsd-v1", process=PROC), ids_ref)
    other = _draws(SeedTree(0).generator("data", "hwsc-v1", split, 0, *PROC))
    assert ref != other


def test_split_ids_disjoint_and_differ_from_stage_c():
    ids = {s: set(dd.block_ids(s, 4096, scope="hwsd-v1", process=PROC).tolist()) for s in dc.SPLITS}
    for a in dc.SPLITS:
        assert len(ids[a]) == 4096
        for b in dc.SPLITS:
            if a < b:
                assert not ids[a] & ids[b], (a, b)
        c = set(dd.block_ids(a, 4096, scope="hwsc-v1", process=PROC).tolist())
        assert not ids[a] & c


@pytest.fixture(scope="module")
def tiny():
    return hwsb_dry.build_tiny_process(ArtifactStore(MemoryBackend()))


def test_sample_block_d_mirror_under_the_dry_binding(tiny, tmp_path, monkeypatch):
    p = tiny
    rows = db.load_table(which="dry", case="T", case_dir=tmp_path)
    with db.bound_hwsd(rows):
        ref_c, ref_i = hwsc_data.sample_block_c(p["T"], p["E_canon_shared"], p["pi"], "cal", 0, 3072)
        calls = []
        orig = HMMSampler.sample

        def counting(self, *a, **k):
            calls.append(a[0] if a else k.get("n"))
            return orig(self, *a, **k)

        monkeypatch.setattr(HMMSampler, "sample", counting)
        trip = bu.tripwire(monkeypatch, ["hwsc_data.sample_block_c", "k4b_data.sample_block"])
        canon, ids = dd.sample_block_d(p["T"], p["E_canon_shared"], p["pi"], "cal", 3072)
    assert trip == [] and calls == [3072]
    assert canon.dtype == np.uint8 and canon.shape == (3072, 32) and canon.flags["C_CONTIGUOUS"]
    assert np.array_equal(canon, ref_c) and np.array_equal(ids, ref_i)
    assert np.all(np.diff(ids) > 0)
    want = make_sequence_ids(process_code(*dc.TINY_PROCESS, "hwsd-dry-v1/T/cal/b0"), "test", 3072)
    assert np.array_equal(ids, np.sort(want))


def test_sample_tables_hist_names_save_and_load(tiny, tmp_path):
    sizes = {"lgate": 64, "cal": 600, "val": 600, "test": 64}
    scope = "hwsd-dry-v1/T"
    tables = dd.sample_tables(tiny, scope=scope, process=dc.TINY_PROCESS, sizes=sizes)
    assert list(tables) == list(dc.SPLITS)
    for s, t in tables.items():
        assert t["canon32"].shape == (sizes[s], 32)
        canon, ids = dd.sample_block_d(tiny["T"], tiny["E_canon_shared"], tiny["pi"], s, sizes[s],
                                       scope=scope, process=dc.TINY_PROCESS)
        assert np.array_equal(t["canon32"], canon) and np.array_equal(t["seq_ids"], ids)
        assert int(t["landmark"].sum()) == (512 if s in ("cal", "val") else 0)
        assert int(t["ref_row"].sum()) == (4 if s == "cal" else 0)
    assert dd.hist_name("cal") == "HIST_cal_b0.npz" and dd.hist_name("test", True) == "DRYHIST_test_b0.npz"
    out = tmp_path / "store"
    out.mkdir()
    k4b_driver.begin_stage(out, "S3")
    paths = dd.save_tables(out, tables, dry=True)
    assert paths == [out / "stages/S3" / dd.hist_name(s, True) for s in dc.SPLITS]
    for path in paths:
        z = np.load(path)
        assert set(z.files) == set(DTYPES) | {"digest"}
        for k, dt in DTYPES.items():
            assert z[k].dtype == dt, k
        assert z["digest"].dtype.kind == "U"
    with pytest.raises(FileExistsError):
        dd.save_tables(out, tables, dry=True)
    k4b_driver.complete_stage(out, "S3", paths)
    back = dd.load_tables(out, dry=True)
    for s in dc.SPLITS:
        assert back[s]["split"] == s and back[s]["block"] == 0
        assert np.array_equal(back[s]["canon32"], tables[s]["canon32"])
    with open(paths[1], "r+b") as f:
        f.seek(40)
        f.write(b"\x00\x01")
    with pytest.raises(bu.C1GateFailure) as e:
        dd.load_tables(out, dry=True)
    assert bu.status_of(e.value) == LIN


class _X6:
    def contains(self, d):
        return np.zeros(len(d), bool)


def _reg(digests=(), sealed=None):
    return c2_registry.Registry(set(digests), _X6(), sealed or {}, ["sealed_d2a"], {}, seq_ids=set())


def _tables(**over):
    t = {s: bu.hist_table(s, 520, 7 + i, 1_000_000 * (i + 1)) for i, s in enumerate(dc.SPLITS)}
    t.update(over)
    return t


def test_separation_d():
    t = _tables()
    r = dd.separation_d(_reg(), t)
    assert r["status"] == PASS and r["rows"] == {s: 520 for s in dc.SPLITS}
    first = str(t["cal"]["digest"][0])
    assert dd.separation_d(_reg([first]), t)["status"] == LIN
    canon = t["test"]["canon32"].copy()
    canon[0] = t["cal"]["canon32"][0]
    clash = _tables(test=bu.k4b_data.history_table(canon, t["test"]["seq_ids"], "test", 0))
    assert dd.separation_d(_reg(), clash)["status"] == LIN
    lo = int(t["val"]["seq_ids"][5])
    assert dd.separation_d(_reg(sealed={"test": (lo, lo + 1)}), t)["status"] == LIN
    canon = t["lgate"]["canon32"].copy()
    canon[3] = 0
    pred = _tables(lgate=bu.k4b_data.history_table(canon, t["lgate"]["seq_ids"], "lgate", 0))
    assert dd.separation_d(_reg(), pred)["status"] == INC


def test_registry_risk_d_exact():
    p = dc.CONTRACT["registry"]["risk"]["p_D2a_ref"]
    r = dd.registry_risk_d(p)
    assert r["rows"] == 13312 == dc.CONTRACT["sizes"]["rows_total"]
    assert Fraction(r["value"]) == 13312 * Fraction(float(p)) and r["ok"] is True
    hi = float(Fraction(1, 100) / 13312) * (1 + 1e-12)
    assert dd.registry_risk_d(hi)["ok"] is False
    lo = float(Fraction(1, 100) / 13312) * (1 - 1e-12)
    assert dd.registry_risk_d(lo)["ok"] is True
    # API-AMBIGUITY: equality (13312 * Fraction(float(p)) == 1/100) has no float solution
    # (1/1331200 is not dyadic), so the "equality passes" boundary is not reachable here.


def _refs(n=3):
    return [{K: (Decimal(f"{i}.{K}5"), Decimal(f"-{K}.{i}1")) for K in (1, 2, 4, 32)}
            for i in range(n)]


def test_refs_json_round_trip_and_refusals(tiny):
    refs, sha = _refs(), "ab" * 32
    obj = dd.refs_to_json(refs, tiny, sha)
    assert set(obj) == {"schema", "identity", "test_table_sha256", "Ks", "n", "M"}
    assert obj["schema"] == "hwsd-refs-v1" and obj["Ks"] == [1, 2, 4, 32] and obj["n"] == 3
    obj = json.loads(json.dumps(obj))
    assert dd.refs_from_json(obj, tiny, 3, sha) == refs
    for vals in obj["M"].values():
        for row in vals:
            assert all(isinstance(x, str) and Decimal(x) == Decimal(x) for x in row)
    text = json.dumps(obj)
    assert "canon32" not in text and "tokens" not in text and "history" not in text
    pi = np.asarray(tiny["pi"], dtype=float).copy()
    pi[0], pi[1] = pi[0] + 1e-3, pi[1] - 1e-3
    other = dict(tiny, pi=pi)
    bad = [(obj, other, 3, sha), (obj, tiny, 3, "cd" * 32), (obj, tiny, 4, sha),
           (dict(obj, schema="hwsd-refs-v0"), tiny, 3, sha),
           (dict(obj, M=dict(obj["M"], **{"32": obj["M"]["32"][:2]})), tiny, 3, sha)]
    for o, p, n, s in bad:
        with pytest.raises(bu.C1GateFailure) as e:
            dd.refs_from_json(o, p, n, s)
        assert bu.status_of(e.value) == LIN


def _q(n, rng):
    q = {}
    for K in (1, 4, 32):
        x = rng.random((n, 36)) + 0.01
        q[K] = x / x.sum(axis=1, keepdims=True)
    return q


def test_lgate_oracle_row_sums(monkeypatch):
    rng = np.random.default_rng(3)
    canon = rng.integers(0, 36, (20, 32)).astype(np.uint8)
    q = _q(20, rng)
    seen = {}

    def fake(proc, c, Ks=(1, 4)):
        seen["Ks"] = tuple(Ks)
        return {k: v.copy() for k, v in q.items()}

    monkeypatch.setattr(hwsb_eval, "oracle_predictives", fake)
    got = dd.lgate_oracle({"planted": True}, canon)
    assert seen["Ks"] == (1, 4) and all(np.array_equal(got[k], q[k]) for k in q)
    for bad in ("sum", "nan"):
        q2 = {k: v.copy() for k, v in q.items()}
        if bad == "sum":
            q2[4][7] *= 1 + 2e-6
        else:
            q2[32][2, 5] = np.nan
        monkeypatch.setattr(hwsb_eval, "oracle_predictives", lambda p, c, Ks=(1, 4), _q=q2: _q)
        with pytest.raises(bu.C1GateFailure) as e:
            dd.lgate_oracle({"planted": True}, canon)
        assert bu.status_of(e.value) == "FAIL_TECHNICAL/NUMERICAL"


def test_shared_controls_bitwise():
    rng = np.random.default_rng(11)
    n = 64
    m = {K: rng.normal(size=(n, 2)) for K in (1, 2, 4, 32)}
    canon = rng.integers(0, 36, (n, 32)).astype(np.uint8)
    got = dd.shared_controls(m, canon)
    assert set(got) == {"m4_phase", "sha_suffix", "delta4_orc"}
    phis = {"m4_phase": k4b_scores.m4_phase(m[4]), "sha_suffix": k4b_scores.sha_phase(canon),
            "delta4_orc": k4b_scores.oracle_phase(m[32])}
    for name, phi in phis.items():
        e = got[name]["all"]
        assert np.array_equal(e["phi"], phi)
        assert np.array_equal(e["X"], k4b_scores.phase_scores(phi, m[32], m[4]))
