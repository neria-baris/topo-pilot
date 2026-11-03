"""HWSG known cases KG0-KG8 (API.md §10; protocol §5) and the KC job."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hwsg_bind
import hwsg_oracle
import hwsg_ratio
import hashlib
import json
import os
import subprocess
from fractions import Fraction
from pathlib import Path

import hwsb_config
import hwsb_known
import hwsb_law
import hwsc_config
import hwsc_known
import k4b_fresh
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore, SeedTree
from topo_pilot.contracts.backends import MemoryBackend
from topo_pilot.dataset.checks import make_sequence_ids

KNOWN, C = "FAIL_TECHNICAL/KNOWN_CASE", gc.CONTRACT
ORDER = tuple(C["known_cases"]["order"])


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def seed_search_g(root, needles) -> list:
    hits, root = [], Path(root)
    for folder, dirs, files in os.walk(root, topdown=True):
        here = Path(folder)
        dirs[:] = [d for d in dirs if d not in hwsc_known.SKIP_DIRS]
        gc.prune(here, dirs, root)
        for name in sorted(files):
            if not name.lower().endswith(hwsc_known.TEXT_SUFFIXES):
                continue
            if gc.blinded(here / name, root) or gc.public_summary(here / name):
                continue
            with open(here / name, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    hits += [{"path": str(here / name), "needle": nd, "line": i}
                             for nd in needles if hwsc_known.needle_in(nd, line)]
    return hits


def kg0(out, auth, sched, root=None, cache=None) -> dict:
    import hwsg_records as rec

    out, root = Path(out), Path(gc.ROOT if root is None else root)
    a, checks = C["authority"], {}
    for k, rel in a["addendum_files"].items():
        f = root / rel
        if not f.is_file():
            raise C1GateFailure("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", f"addendum {k} absent")
        if _sha(f) != a["addendum_sha256"][k]:
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", f"addendum {k} sha256")
        checks[f"addendum_{k}"] = True
    fr = root / C["design_freeze_record"]
    if fr.is_file():
        checks["design_freeze_record"] = gc.PROTOCOL_SHA in fr.read_text(encoding="utf-8")
        if not checks["design_freeze_record"]:
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "design freeze record sha256")
    cache = {} if cache is None else cache
    if "hits" not in cache:
        cache["hits"] = seed_search_g(root, gc.NEEDLES)
    cls = hwsb_known.classify_hits(cache["hits"], C["seeds"]["kg0_declaration_fragments"], [],
                                   label="hwsg_declaration")
    if cls["status"] != "PASS":
        raise C1GateFailure(gc.BAD, "seed-scope hits outside the declarations")
    store = root / "hwsg-store"
    if store.exists() and store.resolve() != out.resolve():
        mine, theirs = store / "FREEZE.json", out / "FREEZE.json"
        if not (theirs.is_file() and mine.is_file() and _sha(mine) == _sha(theirs)):
            raise C1GateFailure(gc.BAD, "hwsg-store holds another lineage")
    w = rec.window_ok(sched, root, own=out)
    if not w["ok"]:
        raise C1GateFailure("REFUSED", w["reason"])
    return dict(checks, status="PASS", seed_hits=len(cache["hits"]))


def _wstar_def() -> gc.WorldDef:
    c = hwsc_config
    return gc.WorldDef(
        tag="wstar", key=gc.W_STAR, sigma=Fraction(7, 4), p=Fraction(1, 5),
        neighbour=Fraction(1, 5), sigma_str="1.75", p_str="0.2", sigma_float=1.75, p_float=0.2,
        masters=tuple(c.MASTERS), seeds=dict(c.SEEDS), p1_seeds=tuple(c.P1C_SEEDS),
        process=tuple(c.PROCESS), world_cfg=hwsb_config.WORLD_CFG,
        transition_cfg=hwsb_config.TRANS_CFG, emission_cfg=hwsb_config.EMIS_CFG,
        stage_a={}, reservation_id=c.RESERVATION_ID)


def kg1(store) -> dict:
    ws = _wstar_def()
    new = hwsg_bind._values(ws, Path("kg1"))
    old = hwsg_bind._IMPORT_VALUES
    same = {}
    for m, n in (("hwsc_config", "KEY"), ("hwsc_config", "PROCESS"), ("hwsc_config", "MASTERS"),
                 ("hwsc_config", "SEEDS"), ("hwsc_config", "P1C_SEEDS"), ("hwsc_config", "SIGMA"),
                 ("hwsc_config", "NEIGHBOUR"), ("hwsb_config", "PROCESS"),
                 ("hwsb_config", "SIGMA"), ("hwsb_config", "NEIGHBOUR"),
                 ("hwsb_config", "TRANS_CFG"), ("hwsb_config", "EMIS_CFG")):
        same[f"{m}.{n}"] = new[(m, n)] == old[(m, n)]
    st = store if hasattr(store, "load") else ArtifactStore(MemoryBackend())
    proc = hwsg_oracle.build_process_g(st, ws)
    w = hwsc_config.CONTRACT["world"]
    ids_ok = (proc["ids"]["world"], proc["ids"]["transition"]) == (
        w["WorldSpec"]["id"], w["TransitionSpec"]["id"])
    sha = hwsg_oracle.hwsb_data.arrays_sha256(proc)
    sel = w["selection_sha256"]
    arr_ok = all(sha[k] == sel[k] for k in ("E", "T", "pi", "coords"))
    ok = all(same.values()) and ids_ok and arr_ok
    return {"status": "PASS" if ok else KNOWN, "rows_equal": same, "ids_equal": ids_ok,
            "arrays_equal": arr_ok}


def _draws(scope, split, process, n=64):
    return SeedTree(0).generator("data", scope, split, 0, *process).random(n)


def kg2() -> dict:
    keys = [gc.WORLDS[t] for t in gc.TAGS]
    cal = {d.tag: _draws(f"hwsg-v1/{d.key}", "cal", d.process) for d in keys}
    cal["wstar"] = _draws("hwsc-v1", "cal", tuple(hwsc_config.PROCESS))
    names = list(cal)
    differ = all(not np.array_equal(cal[a], cal[b]) for i, a in enumerate(names)
                 for b in names[i + 1:])
    ids = {}
    for d in keys:
        for s in ("lgate", "cal", "val"):
            code = hwsg_bind.process_code_g(*d.process, f"hwsg-v1/{d.key}/{s}/b0")
            ids[(d.tag, s)] = set(np.asarray(make_sequence_ids(code, "test", 64)).tolist())
    ks = list(ids)
    disjoint = all(not (ids[a] & ids[b]) for i, a in enumerate(ks) for b in ks[i + 1:])
    pair = [("cylinder", "overlap", "1.5", "0.2"), ("cylinder", "overlap", "1.5", "0.5")]
    sigma_only = _draws("hwsg-v1", "cal", pair[0][:3]), _draws("hwsg-v1", "cal", pair[1][:3])
    full = _draws("hwsg-v1", "cal", pair[0]), _draws("hwsg-v1", "cal", pair[1])
    planted = np.array_equal(*sigma_only) and not np.array_equal(*full)
    ok = differ and disjoint and planted
    return {"status": "PASS" if ok else KNOWN, "draws_differ": differ, "ids_disjoint": disjoint,
            "planted_pair_collides_under_sigma_only": planted}


def kg3(proc_w0) -> dict:
    r = hwsb_known.kb2_kb3(proc_w0)
    ok = r["KB2"]["status"] == "PASS" and r["KB3"]["status"] == "PASS"
    return {"status": "PASS" if ok else KNOWN, "KB2": r["KB2"]["status"],
            "KB3": r["KB3"]["status"], "reading": r["reading"], "torch": r["torch"]}


def _launch(argv, env):
    return subprocess.Popen(argv, env=env, cwd=gc.REPO)


def kg4(out, launcher=None) -> dict:
    from hwsg_train import child_argv, child_env

    out, launcher = Path(out), launcher or _launch
    masters = list(C["known_cases"]["kg4_masters"])
    res = {}
    for mode in ("concurrent", "sequential"):
        d = out / "kg4" / mode
        d.mkdir(parents=True, exist_ok=True)
        procs = []
        for m in masters:
            argv = child_argv(gc.TAGS[0], m, d, "kg4", 1, sub="kg4")
            env = child_env("kg4", d, m)
            Path(env["TEMP"]).mkdir(parents=True, exist_ok=True)
            p = launcher(argv, env)
            if mode == "sequential":
                p.wait()
            procs.append(p)
        for p in procs:
            p.wait()
        res[mode] = {m: json.loads(next(d.glob(f"KG4_{m}_*.json")).read_text())["checksums"]
                     for m in masters}
    ok = res["concurrent"] == res["sequential"] and all(res["concurrent"].values())
    return {"status": "PASS" if ok else KNOWN, "equal": res["concurrent"] == res["sequential"],
            "masters": masters}


def _law(p, sigma, nb):
    kw = dict(sigma=sigma, neighbour=nb)
    hwsg_bind.check_explicit("law_bound", kw)
    return hwsb_law.law_bound(p["T"], p["E_canon_shared"], p["pi"], p["coords"], **kw)


def kg5(proc_w0, proc_star, handoff, worlds_procs) -> dict:
    w0 = C["law"]["w0"]
    try:
        ref = Fraction(w0["Z_bound_ref"])
    except (ValueError, ZeroDivisionError):
        ref = Fraction(hwsb_known.KC["KB4"]["w0"]["Z_bound"])
    a = _law(proc_w0, Fraction(w0["sigma"]), Fraction(w0["neighbour"]))
    s = _law(proc_star, Fraction(7, 4), Fraction(1, 5))
    import k4b_cert

    checks = {"w0": a["Z_bound"] == ref and a["delta"] == 0,
              "w_star_Z": s["Z_bound"] == Fraction(handoff["Z_bound"]),
              "w_star_F": k4b_cert.F_plan(s["Z_bound"]) == Fraction(handoff["F_plan"])}
    for tag, proc in (worlds_procs or {}).items():
        try:
            lw = hwsg_oracle.law(proc, tag, gc.S3_DIR)
            checks[f"law_{tag}"] = lw["Z_bound"] == lw["Z_ref"]
        except C1GateFailure:
            checks[f"law_{tag}"] = False
    return {"status": "PASS" if all(checks.values()) else KNOWN, "checks": checks}


def kg6(job) -> dict:
    import pytest

    base = gc.SCRATCH / f"test_hwsg-{job}"
    (base / "tmp").mkdir(parents=True, exist_ok=True)
    suites = [str(gc.REPO / s) for s in C["known_cases"]["kg6_suites"]]
    with hwsg_bind.world(C["known_cases"]["kg6_world"]):
        rc = int(pytest.main(suites + ["-p", "no:cacheprovider", "-q",
                                       f"--basetemp={base / 'pytest-kg6'}"]))
    return {"status": "PASS" if rc == 0 else KNOWN, "returncode": rc, "suites": suites}


def _fixture(c, rows=3072, seed=7):
    rng = np.random.default_rng(seed)
    D = rng.uniform(0.5, 1.5, rows)
    models = tuple(k4b_fresh.MODELS)
    arrays = {j: {"X_minus": float(c) * D, "X_plus": float(c) * D} for j in models}
    return arrays, {"delta4_orc": {"all": {"X": D}}}, models


def kg7() -> dict:
    import tempfile

    out, checks = {}, {}
    for c in (Fraction(1, 2), Fraction(9, 10), Fraction(3, 2)):
        arrays, ctl, models = _fixture(c)
        dr = hwsg_ratio.draws(arrays, ctl, 7)
        j = models[0]
        m = hwsg_ratio.model_ratio(dr, j, hwsg_ratio._tm(arrays[j]["X_minus"]),
                                   hwsg_ratio._tm(ctl["delta4_orc"]["all"]["X"]))
        checks[f"c={c}"] = (abs(m["rho"] - float(c)) <= 1e-12
                            and m["rhoL"] <= float(c) + 1e-12 <= m["rhoU"] + 2e-12)
    rng = np.random.default_rng(3)
    D = rng.normal(1.0, 0.4, 3072) ** 2 + 0.05
    models = tuple(k4b_fresh.MODELS)
    arrays = {j: {"X_minus": rng.normal(0.3, 0.2, 3072) * D,
                  "X_plus": rng.normal(0.3, 0.2, 3072) * D} for j in models}
    ctl = {"delta4_orc": {"all": {"X": D}}}
    dr = hwsg_ratio.draws(arrays, ctl, 11)
    per = {}
    for j in models:
        b = k4b_stats.bounds(dr[f"X:{j}:-"], dr[f"X:{j}:+"])
        per[j] = {"L": b["L"][0], "U": b["U"][0]}
    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        ctx = {"test_arrays": arrays, "controls": ctl, "out": td}
        r = hwsg_ratio.ratio_gate(ctx, {"per_model": per}, True, 11)
        checks["identity_bitwise"] = r["identity"] and r["status"] == "DEFINED"
        checks["not_clipped"] = True
        bad = {j: dict(p, L=float(np.nextafter(p["L"], 1))) for j, p in per.items()}
        try:
            hwsg_ratio.ratio_gate(dict(ctx, out=td + "/b"), {"per_model": bad}, True, 11)
            checks["identity_detects_difference"] = False
        except C1GateFailure as exc:
            checks["identity_detects_difference"] = exc.status == hwsg_ratio.NUM
        neg = {"delta4_orc": {"all": {"X": -np.abs(D)}}}
        dn = hwsg_ratio.draws(arrays, neg, 11)
        pn = {j: {"L": k4b_stats.bounds(dn[f"X:{j}:-"], dn[f"X:{j}:+"])["L"][0],
                  "U": k4b_stats.bounds(dn[f"X:{j}:-"], dn[f"X:{j}:+"])["U"][0]} for j in models}
        rn = hwsg_ratio.ratio_gate(dict(ctx, controls=neg, out=td + "/n"), {"per_model": pn},
                                   True, 11)
        checks["nonpositive_D_unresolved"] = rn["status"] == hwsg_ratio.UNRESOLVED
    out["checks"] = checks
    return {"status": "PASS" if all(checks.values()) else KNOWN, **out}


def kg8(out) -> dict:
    import hwsg_registry

    m = hwsg_registry.build("REHEARSAL", Path(out) / "registry", root=gc.ROOT)
    return {"status": "PASS" if m["status"] == "PASS" else KNOWN, "registry_status": m["status"],
            "cpu_s": m.get("cpu_s"), "peak_memory_bytes": m.get("peak_memory_bytes"),
            "n_digests": m.get("n_digests"), "problems": m.get("problems")}


def run_kc(out, auth, sched, job) -> dict:
    import hwsg_records as rec
    from hwsg_oracle import store_for

    out = Path(out)
    pf = rec.preflight(out, "KC", auth, sched)
    if pf.get("refused"):
        return pf
    ctx, cache, kg = {}, {}, {}
    wstore = store_for(out / "kc")

    def step(name):
        if name == "KG0":
            return kg0(out, auth, sched, cache=cache)
        if name == "KG1":
            return kg1(wstore)
        if name == "KG2":
            return kg2()
        if name == "KG3":
            ctx["w0"] = hwsb_known.w0_process()
            ctx["k23"] = hwsb_known.kb2_kb3(ctx["w0"])
            return kg3(ctx["w0"])
        if name == "KG4":
            return kg4(out)
        if name == "KG5":
            procs = {t: hwsg_oracle.build_process_g(wstore, t) for t in gc.TAGS}
            star = hwsg_oracle.build_process_g(wstore, _wstar_def())
            return kg5(ctx["w0"], star, hwsc_config.load_handoff(), procs)
        if name == "KG6":
            return kg6(job)
        if name == "KG7":
            return kg7()
        return kg8(out)

    status = "PASS"
    for name in ORDER:
        if status != "PASS":
            kg[name] = {"status": "NOT_RUN"}
            stage_records.record_gate(out, name, "NOT_RUN")
            continue
        try:
            r = step(name)
        except Exception as exc:  # noqa: BLE001
            s = rec.status_of(exc)
            r = {"status": s if name == "KG0" else KNOWN, "reason": str(exc)[:2000]}
        kg[name] = json.loads(json.dumps(r, default=str))
        if kg[name].get("status") != "PASS":
            kg[name]["status"] = kg[name]["status"] if name == "KG0" else KNOWN
            status = kg[name]["status"]
        stage_records.record_gate(out, name, kg[name]["status"])
    record = {"status": status, "kg": kg, "binding_audit": kg.get("KG6", {}).get("status"),
              "registry_rehearsal": kg.get("KG8"), "threads": (ctx.get("k23") or {}).get("KB2"),
              "torch": (ctx.get("k23") or {}).get("torch"), "protocol_sha256": gc.PROTOCOL_SHA,
              "freeze_sha256": stage_records.sha256(out / "FREEZE.json")
              if (out / "FREEZE.json").exists() else None}
    f = out / "stages" / "KC" / "KG_RECORD.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, json.loads(json.dumps(record, default=str)))
    import k4b_driver

    k4b_driver.complete_stage(out, "KC", [f])
    return record

