"""hwsd dry-run cases DRD2, DRD3, DRD6, DRD7, DRD12, DRD13, DRD14 (API.md §12; TEST_PLAN §4).
Split from hwsd_dry by size; DRD2, DRD3, DRD6 are re-exported from hwsd_dry by its lazy __getattr__.
Fixtures live under test_hwsd-<job>/dry/<case>/ (decision 6); nothing real is opened."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import builtins
import io
import json
import types
from pathlib import Path

import c1_model
import hwsb_eval
import hwsb_dry
import hwsb_train
import hwsc_bind
import hwsc_config
import hwsc_data
import hwsc_known
import hwsc_records
import k4b_cert
import k4b_charts
import k4b_config
import k4b_data
import k4b_decoder
import k4b_meter_bind
import k4b_scores
import meter
import numpy as np
import op_guard
import winjob
from c1_records import C1GateFailure

import hwsd_bind as db
import hwsd_data as dd
import hwsd_known as dk
import hwsd_meter_bind as dm
import hwsd_score as ds
from hwsd_dry import (KD4_DEFAULT, _job, _res, case_dir, fresh_fixture, plant_acts, proc_star,
                      in_memory_rows)

from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend
from topo_pilot.contracts.backends import LocalFSBackend


def _raises(fn, status=None) -> bool:
    try:
        fn()
    except C1GateFailure as exc:
        return status is None or exc.status == status
    return False


def _tops(a) -> set:
    return {h["top"] for h in a["unlisted"]}

# --------------------------------------------------------------------------------- DRD2
def drd2(out, ctx) -> dict:
    """Real E4 architecture, 20-step checkpoints of one master on 2,048 in-memory w* rows.
    The scorer keys steps through K_OF, so the checkpoints at 0 and 20 are recorded as 0 and 50."""
    d, fx = case_dir(out, "DRD2"), fresh_fixture(_job(ctx), "DRD2")
    plan, scope, det = dc.dry_plan("dry_e4", "DRD2"), "hwsd-dry-v1/DRD2", {}
    m = dc.DRY_MASTERS[0]
    with db.bound_hwsd(db.load_table(which="dry", case="DRD2", case_dir=d, process=dc.PROCESS)):
        st = ArtifactStore(MemoryBackend())
        proc = hwsc_data.build_process_c(st, masters=dc.DRY_MASTERS)
        obs = hwsc_data.make_train_dev_c(st, proc, m, plan, scope=scope)
        res = hwsb_train.train(st, {"train": obs["train"], "dev": obs["dev"]}, m, plan=plan)
        tabs = dd.sample_tables(proc, scope, dc.PROCESS, {s: 2048 for s in dc.SPLITS})
        mom = {s: k4b_scores.oracle_moments(proc["T"], proc["E_canon_shared"], proc["pi"],
                                            tabs[s]["canon32"], proc["features"])
               for s in ("cal", "test")}
        q = dd.lgate_oracle(proc, tabs["lgate"]["canon32"])
        c = {"proc": proc, "tables": tabs, "moments": mom, "refs_test": None,
             "eps": k4b_cert.envelopes(), "q": q, "Z": dc.Z, "cfg": k4b_config.chart_cfg(),
             "out": fx, "timed": None, "planted": True}
        for step, label in zip(sorted(res["checkpoint_ids"]), dc.STEPS):
            ck = st.load(Checkpoint, res["checkpoint_ids"][step], consumer="experiment")
            m64 = c1_model.load_model64(ck)[0]
            canon = tabs["cal"]["canon32"]
            x = k4b_data.model_inputs(canon, proc["perm"][m])
            p = hwsb_eval.model_predictive(ck, tabs["lgate"]["canon32"], proc["perm"][m])
            a = c1_model.activations(m64, x)
            det[f"s{step}"] = {"inputs": [x.shape[1], int(x[0, 0])], "pred_cols": p.shape[1],
                               "pred_rows_sum1": bool(np.allclose(p.sum(axis=1), 1.0, atol=1e-5)),
                               "acts": [list(a.shape), str(a.dtype)]}
            r = ds.score_checkpoint(c, m, label, ck, m64, proc["perm"][m])
            det[f"s{step}"].update(status=r["status"], ledger=(ds.checkpoint_dir(fx, m, label)
                                   / "CHART_CONSTRUCTIONS.json").is_file())
    ok = all(
        v["inputs"] == [33, 36] and v["pred_cols"] == 36 and v["pred_rows_sum1"]
        and v["acts"] == [[2048, 128], "float64"] and v["ledger"] for v in det.values())
    ok = ok and not any(d.rglob("*.npz")) and sorted(res["checkpoint_ids"]) == [0, 20]
    return _res(ok, reading="VALUE", details=det)

# --------------------------------------------------------------------------------- DRD3
def drd3(out, ctx) -> dict:
    import importlib

    cases = {}
    before = {(r["module"], r["name"]): getattr(importlib.import_module(r["module"]), r["name"])
              for r in db.load_table()}
    cases["identity_kd2"] = dk.kd2()["status"] == "PASS"
    saved = k4b_data.SCOPE
    k4b_data.SCOPE = "hwsc-v1"
    try:
        cases["drift_refused"] = _raises(lambda: db.bound_hwsd().__enter__(),
                                         "FAIL_TECHNICAL/BINDING")
    finally:
        k4b_data.SCOPE = saved
    mod = types.ModuleType("planted_drd3")
    mod.__file__ = str(dc.HERE / "planted_drd3.py")
    mod.S, mod.SEEDS = "hwsc-v1", {"a": 620313}

    def f(a=610101):
        return a

    f.__module__ = "planted_drd3"
    mod.f = f
    with db.bound_hwsd():
        cases["audit_clean"] = db.audit()["status"] == "PASS"
        a = db.audit([mod])
    cases["planted_caught"] = a["status"] != "PASS" and {"S", "SEEDS", "f.__defaults__"} <= _tops(a)
    try:
        with db.bound_hwsd():
            raise RuntimeError("planted")
    except RuntimeError:
        pass
    cases["restored"] = all(getattr(importlib.import_module(m_), n) is o
                            for (m_, n), o in before.items()) and not hwsc_bind.ACTIVE
    return _res(all(cases.values()), cases=cases)

# --------------------------------------------------------------------------------- DRD6
def drd6(out, ctx) -> dict:
    fx, j, cases = fresh_fixture(_job(ctx), "DRD6"), dc.DRY_MASTERS[0], {}
    led = ds.ledger_for(fx, j, 0)
    cases["one_file"] = led.path == ds.checkpoint_dir(fx, j, 0) / "CHART_CONSTRUCTIONS.json"
    led.claim(j, "production")
    led.claim(j, "direct")
    cases["second_refused"] = _raises(lambda: led.claim(j, "production"))
    cases["order"] = led.claims() == [[j, "production"], [j, "direct"]] and 36 * 2 == 72
    cases["fail_technical_stops"] = _raises(lambda: ds.map_build(
        {"status": "FAIL_TECHNICAL/NUMERICAL", "reason": "x"}, "w"), "FAIL_TECHNICAL/NUMERICAL")
    for s in ("INCONCLUSIVE", "INCONCLUSIVE/CHART_UNAVAILABLE", "INCONCLUSIVE/RESOURCE"):
        r = ds.map_build({"status": s, "reason": "NO_H1_BAR"}, "w")
        cases[f"map_{s}"] = r == {"kind": s, "text": f"{s}: NO_H1_BAR"}
    wall = ds.map_build({"status": "INCONCLUSIVE", "reason": "native operation fit wall 600"}, "w")
    cases["map_wall"] = wall["kind"] == "NATIVE_WALL" and wall["text"].startswith("NATIVE_WALL")
    cal = {"status": "INCONCLUSIVE", "reason": "NO_H1_BAR", "diagnostics": {}}
    cases["label_cal"] = ds.status_of_checkpoint({"c0_cal": cal, "c0_val": None}, None) == (
        "CHART_UNAVAILABLE", "CHART_UNAVAILABLE/INCONCLUSIVE: NO_H1_BAR")
    ok_cert = {"status": "PASS", "certified": {}}
    for ds_, dr_, want in (("INCONCLUSIVE/RESOURCE", "r", "SCORED_UNVALIDATED/INCONCLUSIVE/RESOURCE: r"),
                           ("INCONCLUSIVE", "native operation x wall", "NATIVE_WALL")):
        v = {"status": ds_, "reason": dr_, "direct_status": ds_, "direct_reason": dr_,
             "criteria": None}
        s, lab = ds.status_of_checkpoint({"c0_cal": {"status": "PASS", "reason": ""},
                                          "c0_val": v}, ok_cert)
        cases[f"label_{ds_}"] = s == "SCORED_UNVALIDATED" and want in lab
    clock = iter([0.0, 601.0])
    timed = op_guard.timed_factory(fx, 600, clock=lambda: next(clock))
    try:
        timed("fit", lambda: 1)
        cases["wall"] = False
    except op_guard.Unresolved as exc:
        cases["wall"] = "exceeded" in str(exc)
    arch = fx / "w" / "superseded" / "job-a1"
    cdir = arch / "stages" / "SCORE" / str(j) / "s0"
    cdir.mkdir(parents=True)
    (cdir / "CHART_CONSTRUCTIONS.json").write_text(json.dumps({"claims": [[j, "production"]]}))
    (arch / "OPERATION_ACTIVE.json").write_text(json.dumps({"state": "active", "label": "fit"}))
    cases["archived_wall"] = ds.archived_wall(fx / "w", j, 0) == {"role": "production",
                                                                 "label": "fit"}
    (cdir / "CHECKPOINT_RECORD.json").write_text("{}")
    cases["archived_done_none"] = ds.archived_wall(fx / "w", j, 0) is None
    p = proc_star()
    tabs = in_memory_rows("DRD6", 1024, ("cal", "val"))
    mom = {s: k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"], tabs[s]["canon32"],
                                        p["features"]) for s in tabs}
    led2 = ds.ledger_for(fx, j, 50)
    ch = ds.chart_one(j, lambda s: plant_acts("i", tabs[s], mom[s], KD4_DEFAULT), tabs,
                      mom["cal"][32], led2, k4b_config.chart_cfg(), ds.checkpoint_dir(fx, j, 50))
    cases["cal_fail_no_direct"] = (ch["c0_cal"]["status"] != "PASS" and ch["c0_val"] is None
                                   and led2.claims() == [[j, "production"]])
    return _res(all(cases.values()), cases=cases)

# --------------------------------------------------------------------------------- DRD12
def drd12(out, ctx) -> dict:
    job, cases = _job(ctx), {}
    saved = (dict(vars(meter)), winjob.MEMORY_CAP, k4b_meter_bind.TEMP_ROOT)
    tp = dm.job_paths(job, "test")
    try:
        dm.bind(job, "ab", tp["out"], "s", "DRY", tp["temp_root"])
        eff = dm.effective_settings()
        env = dm.child_env_d(job)
        cases["caps"] = eff["memory_cap"] == 12 * 1024**3 and dm.memory_cap("SCORE") == 8 * 1024**3 \
            and dm.memory_cap("DRY") == dc.CONTRACT["resources"]["memory_cap_bytes"]["DRY"]
        cases["temp"] = eff["temp_root"] == str(tp["temp_root"]) and env["TEMP"].startswith(
            str(tp["temp_root"])) and Path(env["TEMP"]).is_dir()
        cases["threads"] = all(env[v] == "1" for v in meter.THREAD_VARS)
        cases["cpu_inf"] = eff["cap_s"] == float("inf")
        cases["output_cap"] = eff["output_cap"] == dc.CONTRACT["resources"]["output_cap_bytes"]
    finally:
        for k, v in saved[0].items():
            setattr(meter, k, v)
        winjob.MEMORY_CAP, k4b_meter_bind.TEMP_ROOT = saved[1], saved[2]
    cases["basetemp"] = Path(tp["basetemp"]).parent == Path(tp["out"]) and \
        tp["out"].parent == dc.SCRATCH
    cases["argv"] = k4b_meter_bind.rewrite_argv(["x"])[-4:] == ["--max-cpu", "inf", "--max-wall",
                                                                "inf"]
    cases["placement"] = dm.placement_ok(tp)["ok"] and not dm.placement_ok(
        dict(tp, out=dc.ROOT / "x"))["ok"] and dm.placement_ok(
        dm.job_paths(job, "store"))["ok"]
    cases["precedence"] = k4b_meter_bind.classify_stop(
        "disk safe-STOP: C:\\ free 1 < 2", "STOP") == "INCONCLUSIVE/RESOURCE"
    cases["bad_kind"] = _raises_value(lambda: dm.job_paths(job, "x"))
    return _res(all(cases.values()), cases=cases)


def _raises_value(fn) -> bool:
    try:
        fn()
    except ValueError:
        return True
    return False

# --------------------------------------------------------------------------------- DRD13
class _OpenHook:
    """Records every open() of a path containing one of the blinded tokens."""

    def __init__(self, tokens):
        self.tokens, self.seen = tokens, []

    def __enter__(self):
        self.o = (builtins.open, io.open, Path.open)

        def mk(f):
            def w(file, *a, **k):
                if any(t in str(file) for t in self.tokens):
                    self.seen.append(str(file))
                return f(file, *a, **k)
            return w

        builtins.open, io.open = mk(self.o[0]), mk(self.o[1])
        po = self.o[2]
        Path.open = lambda p, *a, **k: (self.seen.append(str(p)) if any(
            t in str(p) for t in self.tokens) else None) or po(p, *a, **k)
        return self

    def __exit__(self, *e):
        builtins.open, io.open, Path.open = self.o


def drd13(out, ctx) -> dict:
    root, cases = fresh_fixture(_job(ctx), "DRD13") / "root", {}
    nd = [n for n in dc.NEEDLES if n.isdigit()][0]
    word = [n for n in dc.NEEDLES if not n.isdigit()][0]
    files = {"a/seed.md": f"seed {nd},\n", "b/x.txt": f"a{nd}b {nd}1 {word}\n",
             "hwsc-store/stages/TRAIN/620301/TRAIN_RECORD.json": f'{{"x": "{nd}"}}\n',
             "scr/hwsc-job-x/log.txt": f"{nd}\n",
             "agent-handoff/planning/responses/x-coord-hws-use-20261101-y.md": f"{nd}\n",
             "hwsd-store/FREEZE.json": f"{nd}\n",
             "docs/code_index/files/tools/hwsd/x.md": f"{nd}\n",
             "tools/hwsu/CONTRACT.json": f"{nd}\n", "tools/hwsd/CONTRACT.json": f"{nd}\n",
             "topo-pilot/src/x.py": f"x = {nd}\n"}
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    scratch = root / "scr"
    with _OpenHook(("TRAIN", "hwsc-job-", "coord-hws-use")) as hook:
        hits = dk.seed_search_d(root, [nd, word], scratch)
    seen = {Path(h["path"]).relative_to(root).as_posix(): h["needle"] for h in hits}
    cases["whole_token"] = seen.get("a/seed.md") == nd and seen.get("b/x.txt") in (nd, word)
    cases["blinded_pruned"] = not any(("TRAIN" in k or "hwsc-job" in k or "coord-hws-use" in k)
                                      for k in seen) and not hook.seen
    cases["equal_to_c_without_prune"] = dk.seed_search_d(root / "a", [nd], scratch) == \
        hwsc_known.seed_search_c(root / "a", [nd])
    rel_hits = [dict(h, path="X:/proj/" + Path(h["path"]).relative_to(root).as_posix())
                for h in hits]  # the fixture sits under test_hwsd-*, so classify project-relative
    cl = hwsc_known.classify_hits_c(rel_hits, fragments=dc.CONTRACT["seeds"]["g0_declaration_fragments"],
                                    job_scratch=[])
    kinds = {h["path"][len("X:/proj/"):]: h.get("kind") for h in cl["hits"]}
    decl = ["hwsd-store/FREEZE.json", "docs/code_index/files/tools/hwsd/x.md",
            "tools/hwsu/CONTRACT.json", "tools/hwsd/CONTRACT.json"]
    cases["declarations"] = all(kinds.get(r) and kinds[r] != "unclassified" for r in decl)
    cases["unclassified_src"] = kinds.get("topo-pilot/src/x.py") == "unclassified" and \
        cl["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    D = {"scopes": ["hwsd-v1"], "store": "hwsd-store", "dry_store_glob": "hwsd-dry*",
         "test_root_glob": "test_hwsd-*", "seed_blocks": [[620411, 620416]]}
    U = {"scopes": ["hwsu-v1"], "store": "hwsu-store", "dry_store_glob": "hwsu-dry*",
         "test_root_glob": "test_hwsu-*", "seed_blocks": [[620501, 620503]]}
    cases["overlap_clean"] = dk.overlap_check({"tracks": {"D": D, "U": U}})["status"] == "PASS"
    U2 = dict(U, seed_blocks=[[620416, 620418]])
    cases["overlap_fails"] = dk.overlap_check({"tracks": {"D": D, "U": U2}})["common"] == ["620416"]
    cases["needles_other"] = "620502" in dk.needles_d({"tracks": {"D": D, "U": U}})["other"]
    return _res(all(cases.values()), cases=cases)

# --------------------------------------------------------------------------------- DRD14
def _repro_stage_c(fx) -> dict:
    """(1) A fresh stage-C DRC1 case: its recorded C0-CAL outcome reproduced by chart_one."""
    import hwsc_dry
    import stage_records

    hwsc_dry.drc1(fx, {})
    d = sorted((fx / "DRC1").iterdir())[-1]
    gate = [g for g in stage_records.gates_so_far(d) if g["gate"] == "C0-CAL"][0]
    store = ArtifactStore(LocalFSBackend(d / "artifacts"))
    table = hwsc_bind.load_table(which="dry", case="DRC1", case_dir=d)
    res = {"recorded": gate["status"]}
    with hwsc_bind.bound_stage_c(table):
        proc = hwsb_dry.build_tiny_process(store, masters=tuple(hwsc_config.DRY_MASTERS))
        t = {s: dict(np.load(d / "stages" / "S3" / f"DRYHIST_{s}_b0.npz")) for s in ("cal", "val")}
        t["cal"]["split"] = "cal"
        m32 = k4b_scores.oracle_moments(proc["T"], proc["E_canon_shared"], proc["pi"],
                                        t["cal"]["canon32"], proc["features"])[32]
        for m in hwsc_config.DRY_MASTERS:
            rec = json.loads((d / "stages" / "TRAIN" / str(m) / "TRAIN_RECORD.json").read_text())
            ck = store.load(Checkpoint, rec["checkpoint_ids"][str(max(map(int, rec["checkpoint_ids"])))],
                            consumer="experiment")
            m64 = c1_model.load_model64(ck)[0]
            led = ds.ledger_for(fx / "repro", m, 0)
            af = ds.acts_fn(m64, proc["perm"][m])
            try:
                ch = ds.chart_one(m, lambda sp: af(t[sp]["canon32"]), t, m32, led,
                                  k4b_config.chart_cfg(), ds.checkpoint_dir(fx / "repro", m, 0),
                                  skip_direct=True)
            except Exception as exc:  # noqa: BLE001  the recorded status of a failed gate
                res["failing_model"], res[str(m)] = str(m), hwsc_records.status_of(exc)
                break
            res[str(m)] = ch["c0_cal"]["status"]
            if gate["status"] == "PASS":
                ref = np.load(d / "stages" / "S4a" / f"CHART_{m}.npz")
                res[f"{m}_bitwise"] = all(np.array_equal(ref[k], ch["prod"]["serial"][k])
                                          for k in ref.files)
            elif ch["c0_cal"]["status"] != "PASS":
                res["failing_model"] = res.get("failing_model") or str(m)
                break
    res["ok"] = (all(v for k, v in res.items() if k.endswith("_bitwise"))
                 if gate["status"] == "PASS" else res.get(res.get("failing_model")) == gate["status"])
    return res


def drd14(out, ctx) -> dict:
    fx, cases, det = fresh_fixture(_job(ctx), "DRD14"), {}, {}
    (fx / "orig").mkdir()
    det["stage_c"] = _repro_stage_c(fx / "c1")
    cases["repro"] = bool(det["stage_c"]["ok"])
    with hwsc_bind.bound_stage_c():
        p, M = proc_star(), k4b_config.MODELS
        sizes = {"lgate": 64, "cal": 2048, "val": 1024, "test": 96}
        tabs = dd.sample_tables(p, "hwsd-dry-v1/DRD14", dc.PROCESS, sizes)
        mom = {s: k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"],
                                            tabs[s]["canon32"], p["features"]) for s in tabs}
        prm = dict(KD4_DEFAULT, seeds={"iii": 0})
        cfg, land = k4b_config.chart_cfg(), tabs["cal"]["landmark"]
        A = {}
        for i, j in enumerate(M):
            pr = dict(prm, seeds={"iii": 629980 + i})
            A[j] = {s: plant_acts("iii", tabs[s], mom[s], pr) for s in tabs}
        orig = k4b_charts.c0_cal(M, {j: A[j]["cal"][land] for j in M}, tabs["cal"]["seq_ids"][land],
                                 mom["cal"][32][land], (fx / "orig").resolve(), cfg)
        refs = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"],
                                   tabs["test"]["canon32"])
        eps, sc, ok = k4b_cert.envelopes(), {}, True
        ext, decs = {}, {}
        for j in M:
            sc[j] = ds.chart_one(j, lambda s, j=j: A[j][s], tabs, mom["cal"][32],
                                 ds.ledger_for(fx / "mir", j, 0), cfg,
                                 ds.checkpoint_dir(fx / "mir", j, 0), skip_direct=True)
            o = orig["per_model"][j]
            det.setdefault("c0_cal", {})[str(j)] = [o["status"], str(o["reason"]),
                                                   sc[j]["c0_cal"]["status"]]
            if not (sc[j]["c0_cal"]["status"] == o["status"] == "PASS"):
                ok = False
                break
            ok &= all(np.array_equal(o["serial"][k], sc[j]["prod"]["serial"][k]) for k in o["serial"])
            e0 = k4b_charts.extend(o["chart"], o["gauge"], A[j]["cal"][~land], cfg)
            dec = k4b_decoder.fit(tabs["cal"]["canon32"][~land], tabs["cal"]["seq_ids"][~land],
                                  e0.phase, j)
            ok &= all(np.array_equal(v, k4b_decoder.to_arrays(sc[j]["decoder"])[k])
                      for k, v in k4b_decoder.to_arrays(dec).items())
            r = ds.arrays_one(sc[j]["prod"], A[j]["test"], mom["test"], refs, eps, cfg)
            e = ext[j] = k4b_charts.extend(o["chart"], o["gauge"], A[j]["test"], cfg)
            a = k4b_scores.endpoint_arrays(e.phase, e.supported, mom["test"][32], mom["test"][4])
            b = k4b_cert.endpoint_bounds(a, e.supported, e.phase, refs, eps)
            ok &= all(np.array_equal(a[k], r["arrays"][k]) for k in a) and b == r["bounds"]
            decs[j] = dec
        want = k4b_scores.control_arrays(mom["test"], tabs["test"]["canon32"], ext,
                                         {j: {"unavailable": "x"} for j in M}, decs) if ok else {}
        for j in (M if ok else ()):
            c = ds.controls_one(mom["test"], tabs["test"]["canon32"], ext[j], decs[j])
            for name in ("decoder", "delta1", "delta2", "naive"):
                w = want[name][j]
                ok &= all(np.array_equal(np.asarray(w[k]), np.asarray(c[name][k])) for k in c[name]
                          if k in w)
        cases["mirrors_bitwise"] = bool(ok)
    return _res(all(cases.values()), cases=cases, details=det)
