"""Author B (job 0101): T-POLICY (RC-13, NEW-2), T-SEED, T-SIZE, T-METER.

C2-FROZEN-v1 §13.3, §5.1, §5.2, §5.7, §7, §13.2; API.md §1, §4.1, §8.5, §12, §13, §14. Written
from the protocol, API.md and CONTRACT.json only. tools/c2_readout/*.py is never read by the
author; T-SIZE lists that directory at run time only (TEST_PLAN.md §3). Synthetic stores in
pytest's tmp_path.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402  (first: the sys.path convention)
import c2_code as ck  # noqa: E402
import c2_data as cd  # noqa: E402
import c2_driver as cdr  # noqa: E402
import c1_fit  # noqa: E402
import stage_records  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

from topo_pilot.contracts import SeedTree  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402

ORDER = ("IMPL", "AUTH-ADMIT", "G0", "PF", "H1", "REG", "H2", "H3", "H4", "H5", "M0", "C0c",
         "F1", "C0v", "L1", "R1", "N2", "SURVIVAL", "X1", "V3x", "V3y", "Y1", "Y1*", "Y2",
         "P1", "ACCEPT", "REG2", "T-PRE", "T-PRE-MODEL", "RESP-SPEC", "NUM", "ENDPOINT",
         "REPORT")  # protocol §7 rows 0-28 with the API.md 12.1 names
ALLOWED = {"m0": {"M0", "T-PRE"}, "x1": {"X1", "T-PRE"},
           "val_gate": {"V3x", "V3y", "Y1", "Y1*", "Y2"}, "val_sealed": {"P1"},
           "test_endpoint": {"RESP-SPEC", "NUM", "ENDPOINT", "REPORT"}}
REFUSED = (C1GateFailure, RuntimeError)


def _name(g):
    # API-AMBIGUITY: API.md 12.1 gives GATE_ORDER as "exact names; stage" without fixing whether
    # an entry is a name or a (name, stage) tuple; the gate name is taken either way.
    if isinstance(g, str):
        return g
    return next((x for x in g if isinstance(x, str) and x in ORDER), g[0])


def _at(gate):
    pol = cdr.LogitPolicy(done=ORDER[:ORDER.index(gate)])
    pol.begin(gate)
    return pol


def _refused(fn, word=None):
    with pytest.raises(REFUSED) as info:
        fn()
    if word is not None:
        assert word in str(info.value) or word in str(getattr(info.value, "status", ""))


# ---- T-POLICY ----
def test_gate_order_equals_protocol_section_7():
    assert tuple(_name(g) for g in cdr.GATE_ORDER) == ORDER
    assert tuple(cdr.STAGE_ENTRY) == ("AUTH-ADMIT", "G0")


def test_full_walk_in_order():
    pol = cdr.LogitPolicy(done=())
    for g in ORDER[:ORDER.index("ACCEPT")]:
        pol.begin(g)
        pol.end(g)
    pol = cdr.LogitPolicy(done=ORDER[:ORDER.index("REG2")])  # ACCEPT entered by release_ok
    for g in ORDER[ORDER.index("REG2"):]:
        pol.begin(g)
        pol.end(g)


@pytest.mark.parametrize("gate", [g for g in ORDER if g != "ACCEPT"])
def test_require_table_over_every_gate(gate):
    for kind, gates in ALLOWED.items():
        pol = _at(gate)
        if gate in gates:
            pol.require(kind)
        else:
            _refused(lambda: pol.require(kind))


def test_no_fit_logit_outside_m0_and_no_feas_logit():
    for gate in ("REG", "H2", "H3", "H4", "H5", "C0c", "F1"):  # FIT gates other than M0
        _refused(lambda: _at(gate).require("m0"))
    for gate in ("C0v", "L1", "R1", "N2", "SURVIVAL"):  # FEAS: no logit of any kind
        for kind in ALLOWED:
            _refused(lambda: _at(gate).require(kind))


def test_test_endpoint_refused_before_t_pre_and_t_pre_model():
    pol = _at("T-PRE")
    _refused(lambda: pol.require("test_endpoint"))
    pol.end("T-PRE")
    pol.begin("T-PRE-MODEL")
    _refused(lambda: pol.require("test_endpoint"))
    pol.end("T-PRE-MODEL")
    pol.begin("RESP-SPEC")
    pol.require("test_endpoint")


def test_x1_and_t_pre_cannot_write_endpoint_arrays():
    for gate in ("X1", "T-PRE"):
        pol = _at(gate)
        pol.require("x1")
        for kind in ("val_sealed", "test_endpoint"):
            _refused(lambda: pol.require_write(kind), "LEAKAGE")
    _at("P1").require_write("val_sealed")
    _at("ENDPOINT").require_write("test_endpoint")


def test_out_of_order_gates_are_refused():
    pol = _at("H1")
    _refused(lambda: pol.begin("REG"))  # another gate is current
    pol.end("H1")
    _refused(lambda: pol.begin("H2"))  # FIT sampling (H2) before REG
    for gate, early in (("REG", "H3"), ("H1", "M0"), ("H4", "M0"), ("H2", "H4")):
        p = _at(gate)
        p.end(gate)
        _refused(lambda: p.begin(early))  # SYMBOL-ORDER (c) before H3, two-route before M0


def test_same_gate_again_and_stage_entry_keep_the_position():
    pol = _at("M0")
    pol.end("M0")
    pol.begin("M0")  # another model of the same gate
    pol.end("M0")
    pol = cdr.LogitPolicy(done=ORDER[:ORDER.index("M0")])
    for g in ("AUTH-ADMIT", "G0", "M0"):  # S2 start: stage entry, then the next gate
        pol.begin(g)
        if g != "M0":
            pol.end(g)
    pol.require("m0")


def _gates_file(out, seq):
    out.mkdir()
    for gate, stage, model in seq:
        stage_records.record_gate(out, gate, "PASS", full_status="PASS", stage=stage,
                                  model=model, family=None, problem=None, scope="study")
    return out / "GATES.jsonl"


def test_check_sequence(tmp_path):
    # API-AMBIGUITY: check_sequence(gates_jsonl) is called with the GATES.jsonl path.
    s1 = [(g, "S1", None) for g in ORDER[1:10]]  # AUTH-ADMIT .. H5
    s2 = [("AUTH-ADMIT", "S2", None), ("G0", "S2", None)]
    s2 += [("M0", "S2", j) for j in cc.MODELS]
    assert bool(cdr.check_sequence(_gates_file(tmp_path / "a", s1 + s2))) is True
    bad = s1[:5] + [s1[6], s1[5]] + s1[7:]  # H3 recorded before H2
    assert bool(cdr.check_sequence(_gates_file(tmp_path / "b", bad))) is False


def _ctx(store, pol):
    return cdr.Ctx(store=store, worktree=REPO, head="0" * 40, job="0199", task_sha256="a" * 64,
                   session="synthetic", release=None, policy=pol, data={})


def test_val_sealed_arrays_refused_before_the_outcome(tmp_path):
    store = tmp_path / "store"
    (store / "sealed").mkdir(parents=True)
    (store / "stages" / "S4").mkdir(parents=True)
    _refused(lambda: cdr.seal(_ctx(store, _at("X1")), "VAL_R_1729", {"x": np.ones(3)}),
             "LEAKAGE")
    ctx = _ctx(store, _at("P1"))
    sha = cdr.seal(ctx, "VAL_R_1729", {"x": np.arange(3.0)})
    path = store / "sealed" / "VAL_R_1729.npz"
    assert sha == hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha in (store / "stages" / "S4" / "SEALED.json").read_text(encoding="utf-8")
    with pytest.raises(Exception):  # exclusive create
        cdr.seal(ctx, "VAL_R_1729", {"x": np.arange(3.0)})
    _refused(lambda: cdr.unseal(ctx, "VAL_R_1729", sha), "LEAKAGE")
    for fam in cc.FAMILIES:
        stage_records.record_gate(store, "ENDPOINT", "PASS", full_status="PASS", stage="S5",
                                  model=None, family=fam, problem=None, scope="family")
    with pytest.raises(Exception):  # the file must re-hash to the recorded sha256
        cdr.unseal(ctx, "VAL_R_1729", "b" * 64)
    out = cdr.unseal(ctx, "VAL_R_1729", sha)
    assert np.array_equal(np.asarray(out["x"]), np.arange(3.0))


# ---- T-SEED ----
def test_scope_and_history_streams():
    assert cc.SCOPE == "c2-v1" == cc.CONTRACT["scope"]
    seen = set()
    for split, block in (("fit", 0), ("fit", 1), ("feas", 0), ("val", 0), ("test", 0),
                         ("test", 3)):
        got = cd.history_generator(split, block).integers(0, 2**62, 4).tolist()
        want = SeedTree(0).generator("data", "c2-v1", split, block, "cylinder", "overlap",
                                     "1.25").integers(0, 2**62, 4).tolist()
        assert got == want
        seen.add(tuple(got))
        c1 = SeedTree(0).generator("data", "c1-sf-v1", split, block, "cylinder", "overlap",
                                   "1.25").integers(0, 2**62, 4).tolist()
        assert c1 != got
    frame = tuple(SeedTree(0).generator("c2-v1", "frame", 1729, 0).integers(0, 2**62, 4))
    assert len(seen) == 6 and frame not in seen


SEQ = {"fit/b0": (1330034805, 5712455990822043648, 5712455990822047743),
       "fit/b1": (1413089761, 6069174310612762624, 6069174310612766719),
       "feas/b0": (586295093, 2518118251045584896, 2518118251045588991),
       "val/b0": (1860234253, 7989645280339296256, 7989645280339300351),
       "test/b0": (1551631348, 6664205895913701376, 6664205895913705471),
       "test/b1": (696827854, 2992852844677169152, 2992852844677173247),
       "test/b2": (1649812666, 7085891445801877504, 7085891445801881599),
       "test/b3": (1883241381, 8088460142674182144, 8088460142674186239)}  # API.md §14


def test_sequence_id_codes():
    ids_all = []
    for key, (code, first, last) in SEQ.items():
        split, block = key.split("/b")
        assert process_code("cylinder", "overlap", "1.25", f"c2-v1/{split}/b{block}") == code
        assert cc.CONTRACT["sequence_ids"]["codes"][key] == code
        assert cc.CONTRACT["sequence_ids"]["first_ids"][key] == first
        ids = cd.sequence_ids(split, int(block))
        assert ids.dtype == np.int64 and ids.shape == (4096,)
        assert int(ids[0]) == first == (code << 32) | (3 << 28) and int(ids[-1]) == last
        assert np.array_equal(ids, make_sequence_ids(code, "test", 4096))
        ids_all.append(ids)
    cat = np.concatenate(ids_all)
    assert len(np.unique(cat)) == len(cat)  # disjoint id ranges


def test_seed_map_620501_to_620518():
    want = {"val_p1_R_sd": 620501, "val_p1_R_c": 620502, "test_R": 620503, "val_V3x": 620504,
            "val_H5": 620505, "test_H5": 620506, "val_p1_M_c": 620507, "val_V3y": 620508,
            "val_Y1": 620509, "val_Y2": 620510, "val_p1_M_sd": 620511, "val_p1_S_sd": 620512,
            "test_M": 620513, "val_p1_S_c": 620514, "val_Y1s": 620515, "test_S": 620516,
            "test_rot": 620517, "test_M_desc": 620518}  # protocol §5.2 / API.md §13.2
    assert cc.CONTRACT["seeds"] == want
    assert {name: cc.seed(name) for name in want} == want
    assert sorted(want.values()) == list(range(620501, 620519))


@pytest.mark.parametrize("j, count, p", [(1729, 2, 127), (3141, 8, 128)])
def test_haar_frames_streams(j, count, p):
    d = np.linspace(0.5, 3.0, p)
    for Sigma in (np.eye(p), np.diag(d)):
        frames = ck.haar_frames(j, count, p, Sigma)
        assert len(frames) == count
        for r in (0, count - 1):
            Q = c1_fit.qr_pos(SeedTree(0).generator("c2-v1", "frame", j, r)
                              .standard_normal((p, 6)))
            sh = np.sqrt(np.diag(Sigma))
            want = (sh[:, None] * (Q @ Q.T)) / sh[None, :]  # S^1/2 Q Q' S^-1/2
            P = frames[r]
            assert P.shape == (p, p) and np.max(np.abs(P - want)) <= 1e-12
            assert np.max(np.abs(P @ P - P)) <= 1e-12 and abs(np.trace(P) - 6) <= 1e-12


# ---- T-SIZE ----
MODULES = ("c2_config.py", "c2_data.py", "c2_registry.py", "c2_oracle.py", "c2_model.py",
           "c2_code.py", "c2_stats.py", "c2_attrib.py", "c2_decide.py", "c2_driver.py")


def test_module_set_and_400_line_limit():
    pkg = REPO / "tools" / "c2_readout"
    found = sorted(p.name for p in pkg.glob("*.py"))  # run time only (TEST_PLAN.md §3)
    assert found == sorted(MODULES)
    for name in MODULES:
        assert len((pkg / name).read_bytes().splitlines()) <= 400, name
    mine = sorted((REPO / "tests" / "c2_readout").glob("test_b_*.py"))
    assert 1 <= len(mine) <= 6
    for f in mine:
        lines = f.read_bytes().splitlines()
        assert len(lines) <= 400 and max(len(x.decode("utf-8")) for x in lines) <= 100
        assert b"\r\n" not in f.read_bytes()


# ---- T-METER ----
def test_meter_binding_sha_and_import_directory(tmp_path):
    bind = tmp_path / "c2_meter_bind.py"
    bind.write_bytes(b"# synthetic store-local meter binding\n")
    sha = hashlib.sha256(bind.read_bytes()).hexdigest()
    good = cc.WORKTREE / "tools" / "x4_oracle_profile"
    cdr.meter_bind_check(bind, sha, good)
    with pytest.raises(RuntimeError):
        cdr.meter_bind_check(bind, "0" * 64, good)
    with pytest.raises(RuntimeError):
        cdr.meter_bind_check(bind, sha, cc.PROJECT_ROOT / "topo-pilot" / "tools"
                             / "x4_oracle_profile")
    with pytest.raises(Exception):
        cdr.meter_bind_check(tmp_path / "absent.py", sha, good)


def test_measure_only_caps_in_the_contract():
    res = cc.CONTRACT["resources"]
    assert "--max-cpu inf" in res["cpu_policy"] and "--max-wall inf" in res["cpu_policy"]
    assert res["cpu_policy"].startswith("measure-only")
    assert res["disk_min_free_bytes"] == {"C:": 2000000000, "X:": 30000000000}
    assert res["ledger_schema"] == "x4-oracle-profile-ledger-v1"
    assert cc.CONTRACT["numerics"]["threads"] == 1
    assert cc.CONTRACT["hashes"]["c1_meter_bind"] == (
        "3c1439fc5e053091c683c863ad7b5f0b3fe56253eb2394c57e62fdb0c4b1458d")
