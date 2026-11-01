"""Author B: the versioned binding, the audit, the never-called list, constants (§3.3; KD2, DRD3)."""

from __future__ import annotations  # noqa: I001

import dataclasses
import importlib
import sys
import types
from fractions import Fraction
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_bind as db  # noqa: E402
import test_b_util as bu  # noqa: E402

import hwsb_config  # noqa: E402
import hwsc_bind  # noqa: E402
import k4b_config  # noqa: E402
import k4b_data  # noqa: E402
import pytest  # noqa: E402
from topo_pilot.contracts import SeedTree  # noqa: E402

BIND = "FAIL_TECHNICAL/BINDING"
ROOT = Path("X:/Downloads/projects/topo-pilot")
K4B_OLD_SEEDS = {"val_sd": 610101, "val_b4": 610102, "endpoint": 610103, "fresh_b4": 610104,
                 "val_projection": 610105}
SEEDS = {"val_sd": 620411, "val_b4": 620412, "endpoint": 620413, "fresh_b4": 620414,
         "val_projection": 620415}
DRY_SEEDS = {"val_sd": 629961, "val_b4": 629962, "endpoint": 629963, "fresh_b4": 629964,
             "val_projection": 629965}
EXPECTED_NEW = {
    ("k4b_config", "MODELS"): (620301, 620302, 620303), ("k4b_config", "SCOPE"): "hwsd-v1",
    ("k4b_config", "PROCESS"): ("cylinder", "overlap", "1.75"), ("k4b_config", "SEEDS"): SEEDS,
    ("k4b_config", "STORE"): ROOT / "hwsd-store",
    ("k4b_config", "CONTRACT_PATH"): bu.REPO / "tools/hwsd/CONTRACT.json",
    ("k4b_config", "PROTOCOL_PATH"): bu.REPO / "tools/hwsd/PROTOCOL_HWSD_v1.md",
    ("k4b_data", "MODELS"): (620301, 620302, 620303),
    ("k4b_data", "PROCESS"): ("cylinder", "overlap", "1.75"), ("k4b_data", "SCOPE"): "hwsd-v1",
    ("k4b_stats", "MODELS"): (620301, 620302, 620303), ("k4b_driver", "MODELS"): (620301, 620302, 620303),
    ("k4b_driver", "SEEDS"): SEEDS, ("k4b_driver", "ARTIFACTS"): ROOT / "hwsc-store/artifacts",
    ("k4b_fresh", "MODELS"): (620301, 620302, 620303), ("k4b_fresh", "SEEDS"): SEEDS,
    ("k4b_decoder", "SCOPE"): "hwsd-v1",
}


def _snapshot(rows):
    return {(r["module"], r["name"]): getattr(importlib.import_module(r["module"]), r["name"])
            for r in rows}


def _restored(before):
    for (m, n), obj in before.items():
        assert getattr(importlib.import_module(m), n) is obj, (m, n)


def test_load_table_rows_and_values():
    rows = db.load_table()
    assert len(rows) == 18
    assert [(r["module"], r["name"]) for r in rows] == \
        [(r["module"], r["name"]) for r in dc.CONTRACT["binding"]["table"]]
    for r in rows:
        assert set(r) >= {"module", "name", "old", "new"}
        if (r["module"], r["name"]) in EXPECTED_NEW:
            want = EXPECTED_NEW[(r["module"], r["name"])]
            assert r["new"] == want and type(r["new"]) is type(want), r
    view = next(r["new"] for r in rows if r["name"] == "CONTRACT")
    assert view == dc.CONTRACT["k4b_contract_view"] and view is not dc.CONTRACT["k4b_contract_view"]
    old = {(r["module"], r["name"]): r["old"] for r in rows}
    assert old[("k4b_config", "MODELS")] == (1729, 2718, 3141)
    assert old[("k4b_driver", "SEEDS")] == K4B_OLD_SEEDS
    assert hwsc_bind.check_old(rows) == []


def test_decode():
    assert db.decode([1, 2]) == (1, 2)
    assert db.decode({"__path__": "X:/a/b"}) == Path("X:/a/b")
    assert db.decode({"__repo__": "tools/hwsd/API.md"}) == bu.REPO / "tools/hwsd/API.md"
    assert db.decode({"__dict__": {"a": 1}}) == {"a": 1}
    v = db.decode({"__contract_view__": "k4b_contract_view"})
    assert v == dc.CONTRACT["k4b_contract_view"] and v is not dc.CONTRACT["k4b_contract_view"]
    assert db.decode(7) == 7 and db.decode("s") == "s"


def test_inside_the_binding_and_restoration():
    rows = db.load_table()
    before = _snapshot(rows)
    hwsb_scope = hwsb_config.SCOPE
    with db.bound_hwsd() as info:
        assert hwsc_bind.ACTIVE is True and info is not None
        import k4b_decoder
        import k4b_driver

        assert k4b_config.MODELS == (620301, 620302, 620303)
        assert k4b_data.SCOPE == "hwsd-v1" and k4b_decoder.SCOPE == "hwsd-v1"
        assert k4b_driver.SEEDS["endpoint"] == 620413
        assert Path(k4b_driver.ARTIFACTS) == ROOT / "hwsc-store/artifacts"
        assert k4b_config.CONTRACT["protocol_sha256"] == dc.PROTOCOL_SHA256
        assert k4b_config.CONTRACT["authority"]["c1prime_disclosure"] == dc.DISCLOSURE
        assert k4b_config.check_chart_equality()["equal"] is True
        assert hwsb_config.SCOPE == hwsb_scope == "hwsb-v1"
        a = db.audit()
        assert a["status"] == "PASS", a["unlisted"]
        assert a["unlisted"] == [] and a["n_hits"] >= 1
        assert "hwsd_config" in a["modules"] and "k4b_config" in a["modules"]
        assert db.strong_seed() == 620416
    assert hwsc_bind.ACTIVE is False
    _restored(before)
    with pytest.raises(bu.C1GateFailure) as e:
        db.strong_seed()
    assert bu.status_of(e.value) == BIND


def test_restoration_after_an_exception():
    before = _snapshot(db.load_table())
    with pytest.raises(ZeroDivisionError):
        with db.bound_hwsd():
            1 / 0
    _restored(before)
    assert hwsc_bind.ACTIVE is False


def test_nesting_fails_closed():
    before = _snapshot(db.load_table())
    with db.bound_hwsd():
        with pytest.raises(bu.C1GateFailure) as e:
            with db.bound_hwsd():
                pass
        assert bu.status_of(e.value) == BIND
        assert k4b_config.MODELS == (620301, 620302, 620303)
    _restored(before)


def test_planted_drift_raises_and_sets_nothing(monkeypatch):
    monkeypatch.setattr(k4b_data, "SCOPE", "hwsc-v1")
    models = k4b_config.MODELS
    with pytest.raises(bu.C1GateFailure) as e:
        with db.bound_hwsd():
            pass
    assert bu.status_of(e.value) == BIND and "drift" in str(e.value.reason)
    assert k4b_config.MODELS is models and k4b_data.SCOPE == "hwsc-v1"


def _module(name, src):
    m = types.ModuleType(name)
    m.__file__ = str(bu.REPO / "tools/hwsd" / f"{name}.py")
    sys.modules[name] = m  # dataclasses resolve their module during class creation
    try:
        exec(compile(src, m.__file__, "exec"), m.__dict__)
    finally:
        del sys.modules[name]
    return m


PLANTED = {
    "glob_tuple": "X = (1729, 2718, 3141)\n",
    "fn_default": "def f(a=610101):\n    return a\n",
    "kw_default": "def g(*, s=620313):\n    return s\n",
    "frozen_dc": ("import dataclasses\n@dataclasses.dataclass(frozen=True)\nclass C:\n"
                  "    seeds: tuple = (620201, 620202)\nINST = C()\n"),
    "scope_str": "S = 'hwsc-v1'\n",
    "s3_path": "P = 'X:/Downloads/projects/topo-pilot/hwsc-store/stages/S3/'\n",
    "s7_pathlib": "import pathlib\nP = pathlib.Path('X:/Downloads/projects/topo-pilot/hwsc-store/stages/S7')\n",
    "seed_dict": "D = {'val_sd': 610101, 'other': 1}\n",
    "method_default": "class K:\n    def m(self, x=620314):\n        return x\n",
}


@pytest.mark.parametrize("which", sorted(PLANTED))
def test_audit_catches_planted_leftovers(which):
    m = _module(f"syn_b_{which}", PLANTED[which])
    with db.bound_hwsd():
        a = db.audit(modules=[m])
    assert a["status"] == BIND, which
    assert a["hits"] and a["unlisted"]
    assert all(h["module"] == m.__name__ for h in a["unlisted"])


def test_audit_clean_module_and_bool(monkeypatch):
    forb = dc.CONTRACT["binding"]["audit"]["forbidden"]
    monkeypatch.setitem(forb, "ints", list(forb["ints"]) + [1])
    clean = _module("syn_b_clean", "FLAG = True\nN = 620301\nS = 'hwsd-v1'\n")
    with db.bound_hwsd():
        assert db.audit(modules=[clean])["status"] == "PASS"
        one = _module("syn_b_one", "ONE = 1\n")
        assert db.audit(modules=[one])["status"] == BIND


def test_audit_outside_the_binding_fails_by_design():
    a = db.audit()
    assert a["status"] == BIND and a["unlisted"]


def test_left_unchanged_and_forbidden_rows():
    lu = {(r["module"], r["name"]) for r in dc.CONTRACT["binding"]["left_unchanged"]}
    assert len(dc.CONTRACT["binding"]["left_unchanged"]) == 58
    for row in [("hwsb_config", "SCOPE"), ("hwsb_config", "MASTERS"), ("hwsc_bind", "_STACK"),
                ("hwsc_config", "SCOPE"), ("hwsc_config", "SEEDS"), ("hwsd_config", "CONTRACT"),
                ("k4b_stats", "sd_upper.__defaults__"), ("k4b_stats", "centered.__defaults__"),
                ("hwsc_registry", "REG"), ("hwsc_records", "C")]:
        assert row in lu, row
    f = dc.CONTRACT["binding"]["audit"]["forbidden"]
    assert set(range(620311, 620316)) <= set(f["ints"]) and "hwsc-v1" in f["strings"]
    assert {"X:/Downloads/projects/topo-pilot/hwsc-store/stages/S3",
            "X:/Downloads/projects/topo-pilot/hwsc-store/stages/S7"} <= set(f["paths"])


def test_never_called_list():
    nc = db.never_called()
    assert isinstance(nc, tuple) and list(nc) == dc.CONTRACT["binding"]["never_called"]
    protocol = ["k4b_driver.g0", "k4b_driver.h1", "k4b_driver.reg1", "k4b_driver.h2", "k4b_driver.p1",
                "k4b_driver.c0_cal_stage", "k4b_driver.c0_val_stage", "k4b_driver.cert_val",
                "k4b_fresh.sample_test", "k4b_fresh.h2_fresh", "k4b_fresh.t_pre", "k4b_fresh.endpoint",
                "k4b_fresh.export", "k4b_charts.c0_cal", "k4b_charts.init_charts",
                "k4b_charts.freeze_production", "k4b_scores.control_arrays",
                "hwsc_data.sample_block_c", "hwsc_data.sample_lgate", "hwsc_data.sample_eval",
                "hwsc_gates.h1c", "hwsc_registry_build.obligation", "hwsc_known.seed_search_c",
                "hwsc_records.lineage_c", "hwsc_registry.inventory_c", "hwsc_registry.scratch_check"]
    for name in protocol:
        assert name in nc, name
    for name in bu.never_called_names():
        mod, _, attr = name.partition(".")
        assert hasattr(importlib.import_module(mod), attr), name


def test_scope_modules():
    import hwsd_data  # noqa: F401

    mods = db.scope_modules()
    names = [m.__name__ for m in mods]
    assert names == sorted(names)
    for n in ("hwsd_config", "hwsd_bind", "hwsd_data", "k4b_config", "hwsc_bind", "hwsb_config"):
        assert n in names, n
    dirs = [bu.norm(bu.REPO / d) for d in dc.CONTRACT["binding"]["audit"]["module_dirs"]]
    for m in mods:
        assert bu.norm(Path(m.__file__).resolve().parent) in dirs
    assert "numpy" not in names and "test_b_util" not in names


def test_dry_and_identity_tables(tmp_path):
    with pytest.raises(ValueError):
        db.load_table(which="dry")
    with pytest.raises(ValueError):
        db.load_table(which="bogus")
    rows = db.load_table(which="dry", case="T", case_dir=tmp_path)
    assert len(rows) == 20
    new = {(r["module"], r["name"]): r["new"] for r in rows}
    for m in ("k4b_config", "k4b_data", "k4b_stats", "k4b_driver", "k4b_fresh"):
        assert new[(m, "MODELS")] == (629951, 629952, 629953)
    for m in ("k4b_config", "k4b_data", "k4b_decoder"):
        assert new[(m, "SCOPE")] == "hwsd-dry-v1/T"
    assert new[("k4b_config", "PROCESS")] == ("cylinder", "overlap", "1.0") == dc.TINY_PROCESS
    assert new[("k4b_config", "SEEDS")] == DRY_SEEDS == new[("k4b_driver", "SEEDS")]
    assert Path(new[("k4b_config", "STORE")]) == tmp_path
    assert Path(new[("k4b_driver", "ARTIFACTS")]) == tmp_path / "artifacts"
    assert new[("hwsb_config", "SCOPE")] == "hwsd-dry-v1"
    assert new[("hwsb_config", "DRY_MASTERS")] == (629951, 629952, 629953)
    w = db.load_table(which="dry", case="KD4", case_dir=tmp_path, process=dc.PROCESS)
    assert {(r["module"], r["name"]): r["new"] for r in w}[("k4b_data", "PROCESS")] == dc.PROCESS
    before = _snapshot(rows)
    with db.bound_hwsd(rows):
        assert hwsb_config.SCOPE == "hwsd-dry-v1" and k4b_data.SCOPE == "hwsd-dry-v1/T"
        assert db.strong_seed() == 629965 == dc.DRY_STRONG_SEED
    _restored(before)
    ident = db.load_table(which="identity")
    before = _snapshot(ident)
    for r in ident:
        assert r["new"] is before[(r["module"], r["name"])]
    with db.bound_hwsd(ident):
        _restored(before)
    _restored(before)


def test_kd2b_stream_check():
    def first64(g):
        return g.integers(0, 2**63, size=64).tolist()

    ref = first64(SeedTree(0).generator("data", "hwsd-v1", "cal", 0, "cylinder", "overlap", "1.75"))
    other = first64(SeedTree(0).generator("data", "hwsc-v1", "cal", 0, "cylinder", "overlap", "1.75"))
    with db.bound_hwsd():
        got = first64(k4b_data.history_generator("cal", 0))
    assert got == ref and got != other


def test_constants():
    assert dc.SCOPE == "hwsd-v1" and dc.DRY_SCOPE == "hwsd-dry-v1" and dc.KEY == "W12-q1-s1.75-p0.2"
    assert dc.MASTERS == (620301, 620302, 620303) and dc.DRY_MASTERS == (629951, 629952, 629953)
    assert dc.STEPS == (0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000)
    assert dc.K_OF == {s: i + 1 for i, s in enumerate(dc.STEPS)}
    assert dict(dc.SEEDS) == SEEDS and dict(dc.DRY_SEEDS) == DRY_SEEDS
    assert dc.STRONG_SEED == 620416 and dc.DRY_STRONG_SEED == 629965
    assert dc.SIZES == {"lgate": 4096, "cal": 3072, "val": 3072, "test": 3072}
    assert dc.M == Fraction(1, 100) and dc.F_PLANTED == Fraction(1, 10**9)
    assert set(dc.CHECKPOINTS) == {(j, s) for j in dc.MASTERS for s in dc.STEPS}
    assert all(dc.CHECKPOINTS[(j, s)]["k"] == dc.K_OF[s] for (j, s) in dc.CHECKPOINTS)
    assert bu.sha(dc.PROTOCOL_PATH) == dc.PROTOCOL_SHA256 == dc.CONTRACT["protocol_sha256"]
    assert dc.STORE == ROOT / "hwsd-store" and dc.DRY_STORE == Path("X:/Downloads/topo-scratch/hwsd-dry")
    assert dc.STUDY_LEDGER == ROOT / "agent-handoff" / "HWSD_CPU_LEDGER.json"


def test_dry_plans():
    with pytest.raises(ValueError):
        dc.dry_plan("real", "X")
    t = dc.dry_plan("dry_tiny", "DRD1")
    assert tuple(t.masters) == dc.DRY_MASTERS and t.sizes == {"train": 4096, "dev": 512}
    assert list(t.train_cfg.checkpoint_steps) == [0, 50, 100, 200]
    e = dc.dry_plan("dry_e4", "DRD2")
    assert tuple(e.masters) == dc.DRY_MASTERS[:1] and e.sizes == {"train": 2048, "dev": 256}
    assert e.train_cfg.steps == 20 and list(e.train_cfg.checkpoint_steps) == [0, 20]
    base = hwsb_config.dry_plan("dry_e4", "DRD2")
    assert e.train_cfg == dataclasses.replace(base.train_cfg, steps=20, checkpoint_steps=[0, 20])
    tb = hwsb_config.dry_plan("dry_tiny", "DRD1")
    assert t.train_cfg == dataclasses.replace(tb.train_cfg, checkpoint_steps=[0, 50, 100, 200])
    assert t.model_cfg == tb.model_cfg and t.process == tb.process and t.key == tb.key
