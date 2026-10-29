"""HWSC dry-run cases DRC10-DRC14 (sealing and D6, blindness, records/budget/hold, meter,
G0c needles; API.md §8; rulings R-0176-G1, G2, G5, G12). Split from hwsc_dry2 by size."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import dataclasses
import json
from pathlib import Path

import hws_driver
import hwsb_train
import hwsc_bind
import hwsc_known
import hwsc_meter_bind
import hwsc_records
import hwsc_registry
import k4b_meter_bind
import k4b_release
import k4b_stats
import meter
import numpy as np
import stage_records
import winjob
from c1_records import C1GateFailure
from hwsc_dry import _mem, build_tiny_process_c, case_dir
from hwsc_dry2 import _res

from topo_pilot.contracts import SeedTree  # noqa: F401


# ---------------------------------------------------------------------------- DRC10 sealing
def drc10(out, ctx) -> dict:
    d = case_dir(out, "DRC10")
    cases = {}
    try:
        k4b_stats.check_unsealed({"a": {"b": [{"mean_X_minus": 1.0}]}})
        cases["refused"] = False
    except C1GateFailure as exc:
        cases["refused"] = exc.status == "FAIL_TECHNICAL/SEALING"
    with hwsc_bind.bound_stage_c():
        k4b_stats.write_sealed(d, {"mean_X_minus": {1: np.ones(4)}})
    sealed = json.loads((d / "SEALED_VALIDATION.json").read_text(encoding="utf-8"))
    cases["sealed_protocol"] = sealed["protocol_sha256"] == cc.PROTOCOL_SHA256
    res = {"overall": "EXCLUSION", "per_model": {}}
    oc = {"outcome": "EXCLUSION", "annotations": [], "pbm": None}
    hwsc_records.export_c(d, res, oc, [], {})
    ev = stage_records.stages_so_far(d)[-1]
    want = {"stages/S8/RESULT.json", "stages/S8/SEALED_OPENED.json"}
    cases["d6"] = ev["stage"] == "S8" and ev["event"] == "STAGE_COMPLETE" and \
        set(ev["files"]) == want and all(ev["files"][f] == stage_records.sha256(d / f)
                                         for f in want)
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ------------------------------------------------------------------------- DRC11 blindness
def drc11(out, ctx) -> dict:
    d = case_dir(out, "DRC11")
    root = d / "root"
    blind = ["hwsb-store/REPORT.json", "hwsb-store/stages/EVAL/x.json", "hwsb-store/GATES.jsonl",
             "hwsb-store/CHART_CONSTRUCTIONS_trained.json", "agent-handoff/jobs/0175/review.md"]
    readable = ["agent-handoff/jobs/0175/task.json", "agent-handoff/jobs/0175/request.before.json",
                "agent-handoff/jobs/0175/task.md", "hwsb-store/HANDOFF.json"]
    for rel in blind + readable:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('{"needle": "620301"}\n', encoding="utf-8")
    cases = {"blinded": all(cc.blinded(root / r, root) for r in blind),
             "readable": not any(cc.blinded(root / r, root) for r in readable)}

    def refused(p):
        try:
            cc.read_json(p, root)
        except C1GateFailure as exc:
            return exc.status == "FAIL_TECHNICAL/BLINDNESS"
        return False

    cases["guard"] = all(refused(root / r) for r in blind)
    cases["task_json_read"] = cc.read_json(root / readable[0], root)["needle"] == "620301"
    hits = hwsc_known.seed_search_c(root, ["620301"])
    seen = {Path(h["path"]).relative_to(root).as_posix() for h in hits}
    cases["search_prunes"] = not (seen & set(blind)) and set(readable) <= seen
    hs = root / "hwsb-store"
    (hs / "stages" / "EVAL" / "a.npz").write_bytes(b"blinded")
    r4 = hwsc_registry.source_hwsb(hs, expected={})
    listed = {f["path"] for f in r4["other"] + r4["non_history"]}
    cases["hwsb_never_lists_eval"] = not any("EVAL" in p for p in listed)
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ------------------------------------------------------------- DRC12 records, budget, hold
def _tiny_train(store, proc, plan, m, hold=None):
    import hwsc_data

    obs = hwsc_data.make_train_dev_c(store, proc, m, plan)
    return hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, m, plan=plan,
                            hold=hold)


def drc12(out, ctx) -> dict:
    d = case_dir(out, "DRC12")
    cases = {}
    stage_records.write_new(d / "x.json", {"a": 1})
    try:
        stage_records.write_new(d / "x.json", {"a": 2})
        cases["exclusive"] = False
    except FileExistsError:
        cases["exclusive"] = True
    sha = stage_records.sha256(d / "x.json")
    k4b_release.archive_attempt(d, "job-a1", [d / "x.json"], {})
    stage_records.write_new(d / "x.json", {"a": 1})
    cases["regenerated"] = k4b_release.regenerated_identical(sha, d / "x.json")
    p = hwsc_records.pause_check_c
    cases["pause"] = (p("KC", 4501, 0)["trigger"] == "STAGE"
                      and p("KC", 4500, 0)["pause"] is False
                      and p("TRAIN", 0, 27920.0)["trigger"] == "CUMULATIVE"
                      and p("E2", 3 * (300 + 1720.1 * 2) + 1, 0, k=2)["trigger"] == "STAGE")
    cpu = {"v": 0.0}
    sleeps = []

    def sleep(s, hold_dir=d / "hold"):
        sleeps.append(s)
        for h in hold_dir.glob("HOLD_*.json"):
            dec = hold_dir / h.name.replace("HOLD_", "DECISION_")
            if not dec.exists():
                dec.write_text('{"decision": "CONTINUE"}', encoding="utf-8")

    hr = hwsb_train.HoldRule(d / "hold", cap_s=cc.HOLD_S, steps=20, from_step=10,
                             cpu_fn=lambda: cpu["v"], sleep=sleep)
    cases["no_hold"] = hr(10) is None
    cpu["v"] = cc.HOLD_S
    cases["exact_cap_no_hold"] = hr(20) is None
    cpu["v"] = cc.HOLD_S / 2 + 1
    ev = hr(10)
    cases["hold_continue"] = ev is not None and ev["decision"] == "CONTINUE" and len(sleeps) == 1
    plan = cc.dry_plan("dry_tiny", "DRC12")
    plan = dataclasses.replace(plan, train_cfg=dataclasses.replace(
        plan.train_cfg, steps=20, warmup=5, checkpoint_steps=(0, 10, 20)), gate_step=20)
    m = plan.masters[0]
    with hwsc_bind.bound_stage_c(hwsc_bind.load_table(which="dry", case="DRC12", case_dir=d)):
        a = _tiny_train(*(lambda s: (s, build_tiny_process_c(s)))(_mem()), plan, m)
        cpu["v"] = 1e9
        h2 = hwsb_train.HoldRule(d / "hold2", cap_s=cc.HOLD_S, steps=20, from_step=10,
                                 cpu_fn=lambda: cpu["v"],
                                 sleep=lambda s: sleep(s, d / "hold2"))
        b = _tiny_train(*(lambda s: (s, build_tiny_process_c(s)))(_mem()), plan, m, h2)
    cases["held_bitwise"] = a["checksums"] == b["checksums"] and len(h2.events) == 1
    cases["hold_value"] = cc.HOLD_S == 3 * (6006.6282 / 3)
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ----------------------------------------------------------------------------- DRC13 meter
def drc13(out, ctx) -> dict:
    cases = {}
    saved = (dict(vars(meter)), winjob.MEMORY_CAP, k4b_meter_bind.TEMP_ROOT)
    tp = hwsc_meter_bind.job_paths("0176dry", "test")
    try:
        hwsc_meter_bind.bind("0176dry", "ab", tp["out"], "s", "DRY", tp["temp_root"])
        eff = hwsc_meter_bind.effective_settings()
        env = k4b_meter_bind.child_env("0176dry", base={})
        cases["cap"] = eff["memory_cap"] == 12 * 1024**3 and hwsc_meter_bind.memory_cap(
            "TRAIN") == 8 * 1024**3
        cases["temp"] = eff["temp_root"] == str(tp["temp_root"]) and env["TEMP"].startswith(
            str(tp["temp_root"]))
        cases["threads"] = all(env[v] == "1" for v in meter.THREAD_VARS)
        cases["cpu_inf"] = eff["cap_s"] == float("inf")
    finally:
        for k, v in saved[0].items():
            setattr(meter, k, v)
        winjob.MEMORY_CAP, k4b_meter_bind.TEMP_ROOT = saved[1], saved[2]
    cases["argv"] = k4b_meter_bind.rewrite_argv(["x"])[-4:] == ["--max-cpu", "inf",
                                                                "--max-wall", "inf"]
    cases["placement"] = hwsc_meter_bind.placement_ok(tp)["ok"] and not \
        hwsc_meter_bind.placement_ok(dict(tp, out=cc.ROOT / "x"))["ok"]
    cases["precedence"] = k4b_meter_bind.classify_stop(
        "disk safe-STOP: C:\\ free 1 < 2", "STOP") == "INCONCLUSIVE/RESOURCE"
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ---------------------------------------------------------------------------- DRC14 needles
def drc14(out, ctx) -> dict:
    d = case_dir(out, "DRC14")
    root = d / "root"
    files = {"a/seed.md": "seed 620301,\n", "b/x.txt": "a620301b 6203011 hwsc-v1\n",
             "c/y.json": '{"k": "ff620301ff"}\n', "c/z.py": "x = 629911\n"}
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    needles = list(cc.NEEDLES)
    a, b = hwsc_known.seed_search_c(root, needles), hws_driver.seed_search(root, needles)
    cases = {"equal_to_hws": a == b,
             "whole_token": sorted((Path(h["path"]).name, h["needle"]) for h in a) ==
             sorted([("seed.md", "620301"), ("x.txt", "hwsc-v1"), ("z.py", "629911")])}
    cl = hwsc_known.classify_hits_c([{"path": str(cc.SCRATCH / "hwsc-dry" / "r.json")},
                                     {"path": "X:/elsewhere/r.json"}])
    cases["classify"] = cl["status"] == "FAIL_TECHNICAL/SEED_SCOPE" and \
        cl["hits"][0]["kind"] == "hwsc_declaration" and cl["hits"][1]["kind"] == "unclassified"
    return _res(all(cases.values()), cases=cases, reading="EXACT")
