"""HWSG dry run, part 2: DRG1, DRG2, DRG9, DRG12-DRG14 and the DRY report (API.md §16; §10.1)."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hwsg_cross
import hwsg_dry
import hwsg_handoff
import hwsg_records as rec
import hwsg_registry as gr
import hwsg_train
import hashlib
import json
import os
import tempfile
from pathlib import Path

import k4b_release
import numpy as np
import scores
import stage_records
from c1_records import C1GateFailure

INC = "INCONCLUSIVE/REGISTRY_INCOMPLETE"


def _res(checks, **extra) -> dict:
    return hwsg_dry._res(checks, **extra)


def _hist(path, n=4, seed=0) -> dict:
    g = np.random.default_rng(seed)
    canon = g.integers(0, 36, size=(n, 32)).astype(np.uint8)
    dig = np.array(scores.history_digests(canon), dtype="<U64")
    ids = np.arange(n, dtype=np.int64) + seed * 1000
    stage_records.save_npz(path, canon32=canon, seq_ids=ids, digest=dig)
    return {"canon32": canon, "seq_ids": ids, "digest": dig}


def _entry(store, rel, cls="K4b history table", reader="k4b_history_table") -> dict:
    p = Path(store) / rel
    return {"relpath": rel, "bytes": p.stat().st_size, "class": cls, "reader": reader,
            "sha256": stage_records.sha256(p), "basis": "dry"}


def _obl(store, entries, name="REGISTRY_OBLIGATION.json", utc="2026-11-02T00:00:00Z") -> None:
    p = Path(store) / name
    p.write_text(json.dumps({"schema": "hws-registry-obligation-v1", "written_utc": utc,
                             "files": entries}), encoding="utf-8")


def drg9() -> dict:
    ch = {}
    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        s = Path(td) / "hwsu-like"
        (s / "stages").mkdir(parents=True)
        _hist(s / "stages" / "H.npz")
        stage_records.save_npz(s / "stages" / "N.npz", x=np.zeros(3))
        ents = [_entry(s, "stages/H.npz"),
                dict(_entry(s, "stages/N.npz"), **{"class": "NON_HISTORY", "reader": None})]
        _obl(s, ents)
        opened = []

        def opener(p, m="rb"):
            opened.append(Path(p).name)
            return open(p, m)

        r = gr.source_obligation(s, opener=opener)
        ch["matching_pass"] = r["status"] == "PASS" and len(r["digests"]) == 4
        ch["non_history_never_opened"] = "N.npz" not in opened and len(r["non_history"]) == 1
        _hist(s / "stages" / "X.npz", seed=3)
        ch["extra_file_incomplete"] = gr.source_obligation(s)["status"] == INC
        os.remove(s / "stages" / "X.npz")
        os.rename(s / "stages" / "N.npz", s / "stages" / "N2.npz")
        ch["missing_file_incomplete"] = gr.source_obligation(s)["status"] == INC
        os.rename(s / "stages" / "N2.npz", s / "stages" / "N.npz")
        stage_records.save_npz(s / "stages" / "M.npz", x=np.zeros(3))
        os.remove(s / "stages" / "M.npz")
        bad = [dict(e, **{"class": "Mystery"}) if e["relpath"].endswith("H.npz") else e
               for e in ents]
        _obl(s, bad)
        ch["unknown_class_incomplete"] = gr.source_obligation(s)["status"] == INC
        _obl(s, [dict(ents[0], bytes=ents[0]["bytes"] + 1), ents[1]])
        ch["resized_incomplete"] = gr.source_obligation(s)["status"] == INC
        e = Path(td) / "empty"
        e.mkdir()
        ch["missing_obligation_incomplete"] = gr.source_obligation(e)["status"] == INC
        ch["class_to_reader_bound"] = ("K4b history table", "k4b_history_table") in \
            gr.CLASS_TO_READER and ("NON_HISTORY", None) in gr.CLASS_TO_READER
        t1, t2 = _hist(Path(td) / "a.npz", seed=1), _hist(Path(td) / "b.npz", seed=1)

        class Reg:
            sealed_ranges, seq_ids, predicates = {}, set(), {}

            @staticmethod
            def contains(d):
                return np.zeros(len(d), dtype=bool)

        try:
            sep = gr.separation_g(Reg, {"lo": {"cal": t1}, "mid": {"cal": t2}})
            ch["cross_world_collision_lineage"] = sep["status"] == "FAIL_TECHNICAL/LINEAGE"
        except Exception as exc:  # noqa: BLE001
            ch["cross_world_collision_lineage"] = False
            ch["separation_error"] = repr(exc)[:200]
    return _res(ch)


def drg12() -> dict:
    ch = {}
    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        f = Path(td) / "x.json"
        stage_records.write_new(f, {"a": 1})
        try:
            stage_records.write_new(f, {"a": 2})
            ch["exclusive_create"] = False
        except FileExistsError:
            ch["exclusive_create"] = True
        calls = []
        real = os.replace

        def flaky(a, b):
            calls.append(1)
            if len(calls) < 3:
                raise PermissionError("busy")
            return real(a, b)

        os.replace = flaky
        try:
            rec.marker_replace(Path(td) / "m.json", {"k": 1}, retries=5, sleep_s=0.0)
        finally:
            os.replace = real
        ch["marker_replace_retried"] = len(calls) == 3 and (Path(td) / "m.json").is_file()
        led = Path(td) / "led.json"
        rec.ledger_append(led, "j-TRAIN-lo-1-a1", "j", "TRAIN", 1.0, "t")
        try:
            rec.ledger_append(led, "j-TRAIN-lo-1-a1", "j", "TRAIN", 1.0, "t")
            ch["ledger_unique_labels"] = False
        except C1GateFailure:
            ch["ledger_unique_labels"] = True
        rp = Path(td) / "RESERVATION_W2.json"
        k4b_release.start_reservation(rp, "HWSG-LO-W2", "2026-11-03T00:00:00Z")
        ch["reservation_active"] = k4b_release.verify_reservation(
            rp, {"reservation": "RES-HWSG-LO-W2"})["status"] == "PASS"
    return _res(ch, not_covered=["killed child and bitwise rerun need real children"])


def drg13() -> dict:
    ch = {}
    ch["ram_refused"] = not hwsg_train.ram_ok(3, 1 << 30)["ok"]
    ch["ram_ok"] = hwsg_train.ram_ok(3, 10 * (1 << 30))["ok"]
    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        env = hwsg_train.child_env("j", td, 620611)
        ch["one_thread"] = all(env[k] == "1" for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS"))
        ch["temp_under_out"] = str(env["TEMP"]).startswith(str(td))
    ch["train_child_cap"] = rec.meter_caps("TRAIN_child")["max_cpu"] == gc.HOLD_S
    ch["e2_central"] = rec.central("E2", 2) == 1900.0
    ch["registry_cap_separate"] = rec.output_cap("registry") > rec.output_cap("world")
    return _res(ch)


def drg14() -> dict:
    ch = {}
    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        for t, kind in (("lo", "terminal"), ("mid", "terminal"), ("hi", "valid")):
            wd = gc.world_dir(td, t)
            wd.mkdir(parents=True)
            if kind == "terminal":
                p = rec.terminal_result(wd, t, "INCONCLUSIVE/NOT_LEARNED", "E1", "L1", {}, False)
                stage_records.write_new(wd / "ACCEPT_TERMINAL.json",
                                        {"terminal_result_sha256": stage_records.sha256(p)})
            else:
                v = wd / "stages" / "S5" / "VALIDATION_REPORT.json"
                v.parent.mkdir(parents=True)
                stage_records.write_new(v, {"ok": True})
                stage_records.write_new(wd / "ACCEPT_VALIDATION.json",
                                        {"validation_report_sha256": stage_records.sha256(v)})
        bar = rec.release_barrier(td)
        ch["barrier_ok"] = bar["ok"]
        ch["release_b_for_valid_world_only"] = bar["release_b_missing"] == ["hi"]
        ws = [hwsg_cross.load_world(td, t) for t in ("lo", "mid")]
        ch["terminal_worlds_load"] = all(not w["endpoint"] for w in ws)
        os.remove(gc.world_dir(td, "mid") / "ACCEPT_TERMINAL.json")
        ch["neither_terminal_nor_accepted_blocks"] = not rec.release_barrier(td)["ok"]
    return _res(ch)


def drg2() -> dict:
    ch = {}
    for t in gc.TAGS:
        r = hwsg_train.kg4_child(gc.DRY_MASTERS[t][0], None, steps=20, persist=False)
        ch[f"{t}_stops_at_first_checkpoint"] = r["stopped_at"] is not None and bool(r["checksums"])
    return _res(ch, persisted=False)


def drg1() -> dict:
    """Record-side pipeline on synthetic inputs; geometry-dependent K4b gates are planted."""
    parts = {"DRG9": drg9, "DRG12": drg12, "DRG13": drg13, "DRG14": drg14}
    out = {k: f()["status"] for k, f in parts.items()}
    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        wd = gc.world_dir(td, "mid")
        wd.mkdir(parents=True)
        h = hwsg_handoff.build("mid", {"law": {"Z_bound": gc.CONTRACT["worlds"]["mid"]["stage_a"][
            "law_bound_Z_exact_upper"], "F_plan": "1/10000"}, "identity": {"ids": {}},
            "p_D2a": 1e-16})
        out["handoff_written"] = bool(hwsg_handoff.write(wd, h))
    return {"status": "PASS" if all(v in ("PASS", True) for v in out.values()) else "FAIL",
            "records": out, "kernels_run_directly": ["registry readers", "release barrier",
                                                      "cross readings", "handoff"],
            "inputs_planted": ["K4b geometry gates", "training", "endpoint"],
            "whole_pipeline_pass": False}


def run_dry(out, auth=None, sched=None, job="dry", repo=None) -> dict:
    out, repo = Path(out), Path(gc.REPO if repo is None else repo)
    cases = {"DRG1": drg1, "DRG2": drg2, "DRG3": hwsg_dry.drg3, "DRG4": hwsg_dry.drg4,
             "DRG5": hwsg_dry.drg5, "DRG6": hwsg_dry.drg6, "DRG7": hwsg_dry.drg7,
             "DRG8": hwsg_dry.drg8, "DRG9": drg9, "DRG10": hwsg_dry.drg10,
             "DRG11": hwsg_dry.drg11, "DRG12": drg12, "DRG13": drg13, "DRG14": drg14}
    results = {}
    for k, fn in cases.items():
        try:
            results[k] = fn()
        except Exception as exc:  # noqa: BLE001
            results[k] = {"status": rec.status_of(exc), "reason": str(exc)[:500]}
    names = rec._git(repo, "ls-tree", "-r", "--name-only", "HEAD", "--", "tools/hwsg",
                     "tests/hwsg").decode().splitlines()
    files = {p: hashlib.sha256(rec._git(repo, "show", f"HEAD:{p}")).hexdigest()
             for p in names if p}
    report = {"job": job, "cases": results, "protocol_sha256": gc.PROTOCOL_SHA,
              "implementation_sha256": hashlib.sha256(
                  json.dumps(files, sort_keys=True).encode()).hexdigest(),
              "status": "PASS" if all(r["status"] == "PASS" for r in results.values())
              else "FAIL", "utc": rec.utc()}
    out.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(out / "DRY_REPORT.json", report)
    return report
