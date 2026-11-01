"""hwsd synthetic dry run: helpers, DRD1, DRD4/KD4 (seq_cases, plant_acts), run_dry (API.md §12).

Cases DRD2, DRD3, DRD6, DRD12-DRD14 live in hwsd_dry3 and DRD5, DRD7, DRD8-DRD11 in hwsd_dry2 (split by size);
every documented name stays reachable as hwsd_dry.<name> through the lazy module __getattr__.
Streams only from the dry scopes hwsd-dry-v1/<case>; masters 629951-629953; seeds 629961-629965.
"""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import hashlib
import json
import os
import shutil
import time
import traceback
import uuid
from fractions import Fraction
from pathlib import Path

import c1_means
import c1_model
import hwsc_records
import hwsb_dry
import hwsb_train
import hwsc_data
import k4b_cert
import k4b_config
import k4b_driver
import k4b_scores
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure

import hwsd_bind as db
import hwsd_data as dd
import hwsd_records as drec
import hwsd_score as ds
import hwsd_statements as dst
import hwsd_summary as dsum

from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend
from topo_pilot.contracts.backends import LocalFSBackend

REGISTERED = ("PASS", "FAIL", "NOT_RUN", "PAUSE", "REPORTED")
_LAZY = {**dict.fromkeys(("drd5", "drd7", "drd8", "drd9", "drd10", "drd11"), "hwsd_dry2"),
         **dict.fromkeys(("drd2", "drd3", "drd6", "drd12", "drd13", "drd14"), "hwsd_dry3")}
KD4_DEFAULT = {"g_mass": 0.01,
               "noise": {"i": 1e-7, "ii": 0.01, "iii": 0.01, "iv": 0.01, "v": 0.01},
               "seeds": {"i": 629971, "ii": 629972, "iii": 629973, "iv": 629974, "v": 629975}}
_PROC = {}


def __getattr__(name):
    if name in _LAZY:
        import importlib

        return getattr(importlib.import_module(_LAZY[name]), name)
    raise AttributeError(name)


def _registered(s) -> bool:
    return s in REGISTERED or str(s).startswith(("INCONCLUSIVE/", "FAIL_TECHNICAL/"))


def _res(ok, reading="EXACT", **details) -> dict:
    return {"status": "PASS" if ok else "FAIL", "reading": reading,
            "details": json.loads(json.dumps(details, default=str))}


def case_dir(out, case) -> Path:
    d = Path(out) / case / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d.mkdir(parents=True, exist_ok=False)
    return d


def fixture_root(job, case) -> Path:
    return dc.SCRATCH / f"test_hwsd-{job}" / "dry" / case


def fresh_fixture(job, case) -> Path:
    """A new empty folder under fixture_root (decision 6: never inside the hwsd-dry store)."""
    d = fixture_root(job, case) / f"{time.strftime('%H%M%S', time.gmtime())}-{uuid.uuid4().hex[:6]}"
    d.mkdir(parents=True, exist_ok=False)
    return d


def _job(ctx) -> str:
    return str((ctx or {}).get("job") or "adhoc")


def proc_star() -> dict:
    if "star" not in _PROC:
        _PROC["star"] = hwsc_data.build_process_c(ArtifactStore(MemoryBackend()),
                                                  masters=dc.DRY_MASTERS)
    return _PROC["star"]


def in_memory_rows(case, n, splits=dc.SPLITS, process=dc.PROCESS) -> dict:
    tabs = dd.sample_tables(proc_star(), scope=f"hwsd-dry-v1/{case}", process=process,
                            sizes={s: n for s in dc.SPLITS})  # sample_tables needs every split
    return {s: tabs[s] for s in splits}


def _u(ids) -> np.ndarray:
    return np.array([int(hashlib.sha256(str(int(i)).encode()).hexdigest()[:16], 16) / 2**64
                     for i in ids])


def _g(theta, a) -> np.ndarray:
    tp, c = 2 * np.pi, 2 * np.pi * a
    return np.where(theta < c, theta / c * (np.pi / 6),
                    np.pi / 6 + (theta - c) / (tp - c) * (tp - np.pi / 6))


def plant_acts(case_id, table, m, params) -> np.ndarray:
    """Planted float64 activations [n, 128]: coordinates 0 and 1 carry the signal."""
    ids, n = table["seq_ids"], len(table["seq_ids"])
    u = _u(ids)
    if case_id == "i":
        x0, x1 = u, np.zeros(n)
    else:
        th = {"ii": lambda: k4b_scores.m4_phase(m[4]), "iii": lambda: k4b_scores.oracle_phase(m[32]),
              "iv": lambda: _g(k4b_scores.oracle_phase(m[32]), params["g_mass"]),
              "v": lambda: 2 * np.pi * u}[case_id]()
        x0, x1 = np.cos(th), np.sin(th)
    rng = np.random.Generator(np.random.PCG64(int(params["seeds"][case_id])))
    A = float(params["noise"][case_id]) * rng.standard_normal((n, 128))
    A[:, 0] += x0
    A[:, 1] += x1
    return A


def bounds_row(rec, arrays, step, Z=None) -> dict:
    """The statement row of one checkpoint: bootstraps on the dry seeds (inside a dry binding)."""
    row = {"status": rec["status"], "valid": bool(rec["valid"]), "step": step, "L": None,
           "U": None, "L_S": None, "U_S": None, "F_minus": None, "F_plus": None,
           "learn_pass": False, "B2_L_zS": -1.0}
    if arrays is not None:
        xm, xp = arrays["X_minus"], arrays["X_plus"]
        dr = k4b_stats.joint_bootstrap({"-": xm, "+": xp}, dc.DRY_SEEDS["endpoint"])
        bd = k4b_stats.bounds(dr["-"], dr["+"])
        sd = c1_means.bootstrap_means({"-": xm, "+": xp}, db.strong_seed(), dc.STRONG_DRAWS)
        sb = dsum.strong_bounds(sd["-"], sd["+"])
        fm, fp = dsum.f_sides(rec, Z)
        row.update(L=bd["L"][0], U=bd["U"][0], L_S=sb["L_S"], U_S=sb["U_S"], F_minus=fm,
                   F_plus=fp, point=c1_means.tree_mean(xm),
                   se=float(np.std(xm) / np.sqrt(len(xm))))
    return row


# --------------------------------------------------------------------------------- KD4 / DRD4
_EXPECT = {"AFTER": (("NOT_EVALUABLE", "BY_CONSTRUCTION"), ("TRUE", None), ("TRUE", None)),
           "WITH": (("NOT_EVALUABLE", "BY_CONSTRUCTION"), ("FALSE", None), ("TRUE", None)),
           "BEFORE": (("FALSE", None), ("FALSE", None), ("TRUE", None)),
           "NEVER": (("NOT_EVALUABLE", "FINAL_NOT_SUPPORT"), ("NOT_EVALUABLE", "NEVER"),
                     ("NOT_EVALUABLE", "NO_STRONG_CROSSING")),
           "NO_CHART": (("NOT_EVALUABLE", "NO_CHART"), ("NOT_EVALUABLE", "NO_CHART"),
                        ("NOT_EVALUABLE", "NO_STRONG_CROSSING")),
           "STEP0_CONTROL": (("NOT_EVALUABLE", "CHART_AT_INIT"),
                             ("NOT_EVALUABLE", "CHART_AT_INIT"),
                             ("NOT_EVALUABLE", "NO_STRONG_CROSSING"))}


def _case_ok(cid, row, delta4) -> bool:
    st, p, se = row["status"], row.get("point"), row.get("se")
    if cid == "i":
        return st == "CHART_UNAVAILABLE"
    if cid == "iv":
        return st == "SCORED_UNVALIDATED" and dst.above_s(row)
    if p is None or st != "SCORED":
        return False
    if cid == "iii":
        return dst.sigma(row) == "SUPPORT" and abs(p - delta4) <= 4 * se
    return dst.sigma(row) == "EXCLUDE" and (cid == "v" or abs(p) <= 4 * se)


def seq_cases(out, params=None, cases=None, sequences=None, rows=3072) -> dict:
    out = Path(out)
    if params is None and os.environ.get("HWSD_KD4_PARAMS"):
        params = json.loads(Path(os.environ["HWSD_KD4_PARAMS"]).read_text(encoding="utf-8"))
    params = dict(params or KD4_DEFAULT)
    seqs = dict(sequences or dc.CONTRACT["known_cases"]["KD4"]["sequences"])
    ids = list(cases or dc.CONTRACT["known_cases"]["KD4"]["cases"])
    out.mkdir(parents=True, exist_ok=True)
    res = {"parameters": params, "cases": {}, "sequences": {}}
    with db.bound_hwsd(db.load_table(which="dry", case="KD4", case_dir=out, process=dc.PROCESS)):
        p = proc_star()
        tabs = in_memory_rows("KD4", rows, ("cal", "val", "test"))
        mom = {s: k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"],
                                            tabs[s]["canon32"], p["features"]) for s in tabs}
        delta4 = float(np.mean(dd.shared_controls(mom["test"], tabs["test"]["canon32"])
                               ["delta4_orc"]["all"]["X"]))
        ctx = {"proc": p, "tables": tabs, "moments": mom, "refs_test": None,
               "eps": k4b_cert.envelopes(), "q": None, "Z": dc.Z, "cfg": k4b_config.chart_cfg(),
               "timed": None, "planted": True}
        learn = {"learn_pass": False, "B2_L_zS": -1.0, "captured": 0.0, "regret": 0.0}
        j, rowd = dc.DRY_MASTERS[0], {}
        for cid in ids:
            cd = out / "cases" / cid
            rec = ds.score_checkpoint(dict(ctx, out=cd), j, dc.STEPS[0],
                                      acts=lambda sp, c=cid: plant_acts(c, tabs[sp], mom[sp],
                                                                         params), learn=learn)
            arr = ds.checkpoint_dir(cd, j, dc.STEPS[0]) / "ARRAYS.npz"
            a = dict(np.load(arr)) if arr.exists() else None
            rowd[cid] = bounds_row(rec, a, dc.STEPS[0])
            res["cases"][cid] = {"status": rec["status"], "label": rec["label"],
                                 "point": rowd[cid].get("point"), "se": rowd[cid].get("se"),
                                 "ok": _case_ok(cid, rowd[cid], delta4)}
        for name, cs in seqs.items():
            if any(c not in rowd for c in cs):
                continue
            rs = [dict(rowd[c], step=dc.STEPS[i]) for i, c in enumerate(cs)]
            ev = dst.evaluate({m: rs for m in dc.DRY_MASTERS})
            want = _EXPECT[name]
            got = [ev["statements"][d] for d in ("D2", "D3", "D6")]
            ok = (ev["order"][j]["chart"]["category"]
                  == dc.CONTRACT["known_cases"]["KD4"]["expected_order_at_chart"][name])
            for g, (rd, why) in zip(got, want):
                ok = ok and g["reading"] == rd and (why is None or why in g["reasons"])
            res["sequences"][name] = {"order": ev["order"][j]["chart"]["category"],
                                      "readings": [g["reading"] for g in got], "ok": ok}
    stage_records.write_new(out / "KD4_PARAMS.json", params)
    fb = not res["cases"].get("iv", {"ok": True})["ok"]
    res["fallback_before"] = fb
    res["status"] = "PASS" if (all(c["ok"] for k, c in res["cases"].items() if not (fb and k == "iv"))
                               and all(s["ok"] for k, s in res["sequences"].items()
                                       if not (fb and k == "BEFORE"))) else "FAIL"
    return res


def drd4(out, ctx) -> dict:
    d = case_dir(out, "DRD4")
    r = seq_cases(d, params=(ctx or {}).get("kd4_params"))
    return _res(r["status"] == "PASS", cases=r["cases"], sequences=r["sequences"],
                kd4_parameters=r["parameters"], fallback_before=r["fallback_before"])


# --------------------------------------------------------------------------------- DRD1
def _train_tiny(store, proc, plan, scope) -> dict:
    ids = {}
    for m in dc.DRY_MASTERS:
        obs = hwsc_data.make_train_dev_c(store, proc, m, plan, scope=scope)
        res = hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, m, plan=plan)
        ids[m] = {int(s): i for s, i in res["checkpoint_ids"].items()}
    return ids


def drd1(out, ctx) -> dict:
    """The tiny-world pipeline: train, SAMPLE tables, H2-D, ORACLE-D, B4-TEST, LGATE, SCORE, SUMMARY."""
    import c2_registry

    d, fx = case_dir(out, "DRD1"), fresh_fixture(_job(ctx), "DRD1")
    work, st, Z = fx / "work", {}, Fraction(1, 10**12)
    work.mkdir()
    plan, scope = dc.dry_plan("dry_tiny", "DRD1"), "hwsd-dry-v1/DRD1"
    sizes = {k: int(v) for k, v in dc.CONTRACT["dry_run"]["tiny_sizes"].items() if k in dc.SPLITS}
    sizes["cal"] = 2048  # the decoder needs at least two non-landmark panels of 512
    store = ArtifactStore(LocalFSBackend(fx / "artifacts"))
    steps = tuple(plan.train_cfg.checkpoint_steps)

    def train():
        st["proc"] = hwsb_dry.build_tiny_process(store, masters=dc.DRY_MASTERS)
        st["ids"] = _train_tiny(store, st["proc"], plan, scope)
        return {"status": "PASS"}

    def sample():
        k4b_driver.begin_stage(work, "S3")
        st["tabs"] = dd.sample_tables(st["proc"], scope, dc.TINY_PROCESS, sizes)
        files = dd.save_tables(work, st["tabs"], dry=True)
        k4b_driver.complete_stage(work, "S3", files)
        (d / "stages" / "S3").mkdir(parents=True)
        for f in files:
            shutil.copy2(f, d / "stages" / "S3" / f.name)
        st["tabs"] = dd.load_tables(work, dry=True)
        return {"status": "PASS", "rows": {s: len(t["seq_ids"]) for s, t in st["tabs"].items()}}

    def h2d():
        reg = c2_registry.Registry(set(), None, {}, [], {})
        r = dd.separation_d(reg, st["tabs"])
        if r["status"] != "PASS":
            raise C1GateFailure(r["status"], "H2-D")
        return {"status": "PASS"}

    def oracle():
        p, t = st["proc"], st["tabs"]
        st["mom"] = {s_: k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"],
                                                   t[s_]["canon32"], p["features"])
                     for s_ in ("cal", "test")}
        st["refs"] = None  # the tiny geometry may fail ORACLE-D (VALUE); SCORE is then planted
        o = dd.oracle_d(p, t)
        st["refs"] = o["refs_test"]
        k4b_driver.begin_stage(work, "S4")
        k4b_driver.complete_stage(work, "S4", dd.save_oracle(work, o["moments"]))
        return {"status": "PASS", "max_gap": str(o["max_gap"])}

    def b4():
        st["b4"] = {"status": "NOT_RUN"}
        if st["refs"] is None:
            raise C1GateFailure("INCONCLUSIVE/HEADROOM", "no references (ORACLE-D failed)")
        st["b4"] = g = dd.b4_test(st["mom"]["test"], st["refs"], k4b_cert.envelopes(), Z)
        return {"status": g["status"]}

    def lgate():
        st["q"] = dd.lgate_oracle(st["proc"], st["tabs"]["lgate"]["canon32"])
        return {"status": "PASS"}

    def score(m):
        def run():
            c = {"proc": st["proc"], "tables": st["tabs"], "refs_test": st["refs"], "moments": st["mom"],
                 "eps": k4b_cert.envelopes(), "q": st["q"], "Z": Z, "cfg": k4b_config.chart_cfg(),
                 "out": work, "timed": None, "planted": st["refs"] is None}
            recs = []
            for s in steps:
                ck = store.load(Checkpoint, st["ids"][m][s], consumer="experiment")
                recs.append(ds.score_checkpoint(c, m, s, ck, c1_model.load_model64(ck)[0],
                                                st["proc"]["perm"][m]))
            st.setdefault("recs", {})[m] = recs
            return {"status": "PASS", "counts": [r["status"] for r in recs]}
        return run

    def summary():
        table = {}
        for m, recs in st["recs"].items():
            rows = []
            for s, r in zip(steps, recs):
                p = ds.checkpoint_dir(work, m, s) / "ARRAYS.npz"
                rows.append(bounds_row(r, dict(np.load(p)) if p.exists() else None, s, Z))
            table[m] = rows
        ev = dst.evaluate(table, headroom_ok=st.get("b4", {}).get("status") == "PASS")
        st["ev"] = ev
        return {"status": "PASS", "statements": {k: v["reading"] for k, v in ev["statements"].items()}}

    gates = ([("TRAIN", train), ("S3D", sample), ("H2D", h2d), ("ORACLE-D", oracle),
              ("B4-TEST", b4), ("LGATE-ORACLE", lgate)]
             + [(f"SCORE_{m}", score(m)) for m in dc.DRY_MASTERS] + [("SUMMARY", summary)])
    site, bos = c1_model.SITE, c1_model.BOS
    c1_model.SITE, c1_model.BOS = dc.CONTRACT["dry_run"]["tiny_site"], 3  # tiny hook, BOS = V
    try:
        with db.bound_hwsd(db.load_table(which="dry", case="DRD1", case_dir=work)):
            recs_g = drec.run_gates_c(work, gates, dry_continue=True)
    finally:
        c1_model.SITE, c1_model.BOS = site, bos
    names = [g["gate"] for g in stage_records.gates_so_far(work)]
    ok = (all(names.count(g) == 1 for g, _ in gates)
          and all(_registered(g["status"]) for g in stage_records.gates_so_far(work))
          and not any(p.name.startswith("HIST_") for p in d.rglob("*.npz")))
    return _res(ok, reading="VALUE", gates={g["gate"]: g["status"] for g in
                                            stage_records.gates_so_far(work)},
                reasons={g["gate"]: str(g.get("reason", ""))[:200]
                         for g in stage_records.gates_so_far(work) if g["status"] != "PASS"},
                statements=(st.get("ev") or {}).get("statements") and
                {k: v["reading"] for k, v in st["ev"]["statements"].items()},
                records=len(recs_g))


# --------------------------------------------------------------------------------- run_dry
def run_dry(out=dc.DRY_STORE, sched=None, only=None, job=None) -> dict:
    out = Path(out)
    if not drec.sched_ok(sched, "DRY")["ok"]:
        return {"status": "REFUSED", "reason": "SCHED W2 rule"}
    import hwsd_dry2
    import hwsd_dry3

    results, ctx = {}, {"job": job}
    for i in range(1, 15):
        name = f"DRD{i}"
        if only and name not in only:
            continue
        fn = globals().get(f"drd{i}") or getattr(hwsd_dry2, f"drd{i}", None) or getattr(
            hwsd_dry3, f"drd{i}")
        try:
            results[name] = fn(out, ctx)
        except Exception as exc:  # noqa: BLE001  a crashing case is a FAIL
            results[name] = {"status": "FAIL", "reading": "EXACT", "details": {
                "error": f"{type(exc).__name__}: {exc}", "trace": traceback.format_exc()[-2000:]}}
    h = drec._git(dc.REPO, "rev-parse", "HEAD").decode().strip()
    files = drec.implementation_files_d(dc.REPO, h)
    rep = {"cases": results,
           "all_pass": all(r["status"] == "PASS" for r in results.values()) and not only,
           "implementation_files": files,
           "implementation_sha256": drec._sha(json.dumps(files, sort_keys=True).encode()),
           "h_exec": h,
           "tree_clean": not drec._git(dc.REPO, "status", "--porcelain", "--", "tools/hwsd",
                                       "tests/hwsd").strip(),
           "kd4_parameters": (results.get("DRD4", {}).get("details") or {}).get("kd4_parameters"),
           "inventory_before": ctx.get("inventory_before"),
           "inventory_after": ctx.get("inventory_after")}
    p = out / "stages" / "DRY" / "DRY_REPORT.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(p, json.loads(json.dumps(rep, default=str)))
    first = not (out / "REGISTRY_OBLIGATION.json").exists()
    job = str(job or "adhoc")
    dd.write_obligation(out, "REGISTRY_OBLIGATION.json" if first else
                        f"REGISTRY_OBLIGATION_{job}-a1.json", job, None if first else 1,
                        hwsc_records.utc())
    return rep
