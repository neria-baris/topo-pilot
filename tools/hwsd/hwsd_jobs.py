"""HWSD jobs SCORE and SUMMARY and the CLI (API.md §11, §15.3, §15.4; split from hwsd_driver by
size, API erratum; the driver re-exports run_score, run_summary and main). hwsd_driver is
imported lazily inside the functions (the hwsc_jobs pattern)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import argparse
import json
import os
import time
from fractions import Fraction
from pathlib import Path

import hwsb_driver
import hwsc_data
import hwsd_bind
import hwsd_data
import hwsd_readers
import hwsd_records
import hwsd_score
import k4b_cert
import k4b_config
import k4b_driver
import k4b_stats
import numpy as np
import op_guard
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore
from topo_pilot.contracts.backends import MemoryBackend

REFUSE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


def _npz(path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def _accept_sample_ok(out, acc) -> bool:
    if not (isinstance(acc, dict) and acc.get("verdict") == "ACCEPT"
            and isinstance(acc.get("sample_files_sha256"), dict)):
        return False
    return all((Path(out) / rel).is_file() and stage_records.sha256(Path(out) / rel) == sha
               for rel, sha in acc["sample_files_sha256"].items())


def _archive_interrupted(out, job, attempt, j) -> None:
    d = Path(out) / "stages" / "SCORE" / str(j)
    files = sorted(p for p in d.rglob("*") if p.is_file()) if d.is_dir() else []
    if files and int(attempt) > 1:
        marker = Path(out) / op_guard.MARKER
        hwsd_records.archive_attempt_d(out, job, int(attempt) - 1,
                                       files + ([marker] if marker.is_file() else []))


def _write_marker_d(out, record, tries=100) -> None:
    """op_guard.write_marker, retried: the meter reads the marker four times a second and Windows
    refuses the replace while it is open (R-0216-1)."""
    for k in range(tries):
        try:
            return op_guard.write_marker(out, record)
        except PermissionError:
            if k == tries - 1:
                raise
            time.sleep(0.02)


def timed_factory_d(out, wall_s, clock=time.monotonic, wall_clock=time.time):
    """op_guard.timed_factory line for line, with _write_marker_d (same records and log)."""
    out, wall_s, state = Path(out), float(wall_s), {"seq": 0}

    def timed(label, fn):
        state["seq"] += 1
        seq = state["seq"]
        op_guard._log(out, {"event": "start", "seq": seq, "label": label, "deadline_s": wall_s})
        _write_marker_d(out, {"state": "active", "seq": seq, "label": label,
                              "started_epoch": wall_clock(), "deadline_s": wall_s,
                              "pid": os.getpid()})
        t0 = clock()
        try:
            result = fn()
        except BaseException as exc:
            _write_marker_d(out, {"state": "idle", "seq": seq, "label": label})
            op_guard._log(out, {"event": "error", "seq": seq, "label": label,
                                "type": type(exc).__name__})
            raise
        elapsed = clock() - t0
        _write_marker_d(out, {"state": "idle", "seq": seq, "label": label})
        op_guard._log(out, {"event": "end", "seq": seq, "label": label, "elapsed_s": elapsed})
        if elapsed >= wall_s:
            op_guard._log(out, {"event": "exhausted", "seq": seq, "label": label,
                                "elapsed_s": elapsed})
            raise op_guard.Unresolved(f"native operation {label} exceeded its {wall_s} s wall")
        return result

    return timed


def _score_ident(out, accept, j) -> dict:
    out = Path(out)
    from hwsd_known import ident_d

    ident = ident_d(masters=(j,))
    checked = sorted(set(accept["sample_files_sha256"]) | {
        p.relative_to(out).as_posix() for s in ("S3", "S4") for p in (out / "stages" / s).glob(
            "*.npz")})
    for rel in checked:
        want = hwsd_readers.stage_complete_sha(out / "STAGES.jsonl", rel)
        if want is None or stage_records.sha256(out / rel) != want:
            raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"{rel} does not re-hash to its record")
    d = out / "stages" / "SCORE" / str(j)
    if list(d.rglob("CHECKPOINT_RECORD.json")):
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"SCORE {j} holds a CHECKPOINT_RECORD")
    d.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(d / "SCORE_IDENT.json", {"ident": ident, "files_checked": len(checked)})
    return {"n_files": len(checked)}


def _score_ctx(out, j) -> dict:
    out = Path(out)
    tables = hwsd_data.load_tables(out)
    s4 = out / "stages" / "S4"
    mom = {s: {int(k[1:]): v for k, v in _npz(s4 / f"ORACLE_{s}.npz").items()}
           for s in ("cal", "test")}
    proc = hwsc_data.build_process_c(ArtifactStore(MemoryBackend()))
    refs = hwsd_data.refs_from_json(
        dc.read_json(s4 / "REFS_test.json"), proc, len(tables["test"]["seq_ids"]),
        stage_records.sha256(out / "stages" / "S3" / hwsd_data.hist_name("test")))
    qz = _npz(s4 / "LGATE_Q.npz")
    z = Fraction(dc.read_json(out / "stages" / "SAMPLE" / "H1D.json")["Z_bound"])
    return {"proc": proc, "tables": tables, "moments": mom, "refs_test": refs,
            "eps": k4b_cert.envelopes(), "q": {1: qz["q1"], 4: qz["q4"], 32: qz["q32"]}, "Z": z,
            "cfg": k4b_config.chart_cfg(), "out": out, "timed": timed_factory_d(out, 600),
            "planted": False}


def run_score(out, auth, sched, job, attempt, master, accept_sample, cont=None) -> dict:
    import hwsd_driver as hd

    out, j, t0 = Path(out), int(master), time.process_time()
    pf = hwsd_records.preflight_d(out, "SCORE", auth, sched)
    if pf["refused"]:
        return hd.refuse_exit(out, pf, job, attempt)
    ctx, acc = {}, {}
    with hwsd_bind.bound_hwsd():
        hd.audit_gate(out)
        if not _accept_sample_ok(out, accept_sample):
            stage_records.record_gate(out, "ACCEPT_SAMPLE", REFUSE)
            return hd.refuse_exit(out, {"refused": True, "reason": "ACCEPT_SAMPLE"}, job, attempt)
        stage_records.record_gate(out, "ACCEPT_SAMPLE", "PASS")
        _archive_interrupted(out, job, attempt, j)

        def checkpoints():
            ctx.update(_score_ctx(out, j))
            ctx["records"] = hwsd_score.run_checkpoints(
                ctx, j, pause=lambda: hwsd_records.pause_or_raise_d(
                    out, "SCORE", t0, dc.STUDY_LEDGER, cont))
            return {}

        def h1():
            d = out / "stages" / "SCORE" / str(j)
            k4b_driver.complete_stage(out, f"SCORE_{j}", sorted(
                p for p in d.rglob("*") if p.is_file()))
            acc.update(hwsd_score.acceptance(out, j, job, attempt, ctx["records"],
                                             time.process_time() - t0,
                                             stage_records.sha256(out / "FREEZE.json")))
            k4b_driver.complete_stage(out, f"SCORE_{j}", [d / "ACCEPTANCE.json"])
            return {}

        steps = [("SCORE-IDENT", lambda: _score_ident(out, accept_sample, j)),
                 ("CHECKPOINTS", checkpoints),
                 ("DETERMINISM", lambda: hwsd_score.determinism_d(ctx, j, ctx["records"])),
                 ("H-1", h1)]
        recs = hd.run_gates_d(out, [(g, hd.paused(out, "SCORE", t0, f, cont)) for g, f in steps])
    hd.end_obligation(out, job, attempt)
    res = {"status": hd.first_bad(recs), "gates": {r["gate"]: r["status"] for r in recs}}
    if acc:
        res.update(counts=acc["counts"], cpu_s=acc["cpu_s"], acceptance_sha256=stage_records.sha256(
            out / "stages" / "SCORE" / str(j) / "ACCEPTANCE.json"))
    return res


def _shared(out) -> dict:
    z = _npz(Path(out) / "stages" / "S4" / "SHARED_CONTROLS.npz")
    return {n: {"all": {"X": z[f"{n}_X"], "phi": z[f"{n}_phi"]}}
            for n in ("m4_phase", "sha_suffix", "delta4_orc")}


def _accept_scores_ok(out, accepts) -> bool:
    if isinstance(accepts, list):
        accepts = {int(r["master"]): r for r in accepts if isinstance(r, dict)}
    for j in dc.MASTERS:
        acc = accepts or {}
        a = acc.get(j, acc.get(str(j)))  # R-0209-2 (F4): JSON object files have str keys
        f = Path(out) / "stages" / "SCORE" / str(j) / "ACCEPTANCE.json"
        if not (isinstance(a, dict) and a.get("verdict") == "ACCEPT" and f.is_file()
                and a.get("acceptance_sha256") == stage_records.sha256(f)):
            return False
    return True


def run_summary(out, auth, sched, job, attempt, accepts, cont=None) -> dict:
    import hwsd_driver as hd
    import hwsd_summary as dsum

    out, t0 = Path(out), time.process_time()
    pf = hwsd_records.preflight_d(out, "SUMMARY", auth, sched)
    if pf["refused"]:
        return hd.refuse_exit(out, pf, job, attempt)
    rep = {}
    with hwsd_bind.bound_hwsd():
        hd.audit_gate(out)
        if not _accept_scores_ok(out, accepts):
            stage_records.record_gate(out, "ACCEPT_SCORE", REFUSE)
            return hd.refuse_exit(out, {"refused": True, "reason": "ACCEPT_SCORE"}, job, attempt)
        stage_records.record_gate(out, "ACCEPT_SCORE", "PASS")
        shared = _shared(out)

        def bootstrap():
            scores = dsum.load_scores(out)
            inputs = dsum.bootstrap_inputs_d(scores, shared)
            draws = dsum.main_bootstrap(inputs)
            sdraws = dsum.strong_bootstrap(scores)
            n = 0
            for key in (k for k in inputs if k.startswith("X:") and k.endswith(":-")):
                plus = key[:-1] + "+"
                bd = k4b_stats.bounds(draws[key], draws[plus])
                if (bd["L_rank"], bd["U_rank"]) != (dc.RANKS["alpha"], dc.RANKS["one_minus_alpha"]):
                    raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", f"rank check {key}")
                dsum.strong_bounds(sdraws[key], sdraws[plus])
                n += 1
            return {"n_checkpoints": n}

        def statements():
            z = Fraction(dc.read_json(out / "stages" / "SAMPLE" / "H1D.json")["Z_bound"])
            b4 = dc.read_json(out / "stages" / "S4" / "B4_TEST.json")
            ref = dc.read_json(dc.HWSC_STORE / "stages" / "S8" / "RESULT.json")
            rep.update(dsum.report(out, z, shared, b4, ref))
            return {"outcome": rep["outcome"]}

        steps = [("BOOTSTRAP", bootstrap), ("STATEMENTS", statements)]
        recs = hd.run_gates_d(out, [(g, hd.paused(out, "SUMMARY", t0, f, cont)) for g, f in steps])
    hd.end_obligation(out, job, attempt)
    bad = hd.first_bad(recs)
    out_status = rep.get("outcome", bad) if bad == "PASS" else bad
    return {"status": out_status, "gates": {r["gate"]: r["status"] for r in recs}}


# --------------------------------------------------------------------------------------- CLI
def _load(p):
    return json.loads(Path(p).read_text(encoding="utf-8")) if p else None


def _exit(res) -> int:
    if res.get("refused"):
        return 2
    s = str(res.get("status", "PASS"))
    if s in ("PASS", "HWSD_REPORT", "COMPLETE"):
        return 0
    return 3 if s.startswith("FAIL_TECHNICAL") else 5


OPTS = ("--out", "--auth", "--sched", "--kd-accept", "--accept", "--master", "--job", "--attempt",
        "--continue", "--reason", "--h-exec", "--r-ref", "--dry-report", "--pf-record",
        "--kd4-params", "--run-approval", "--save", "--compare", "--store", "--only")


def main(argv=None) -> int:
    import hwsd_driver as hd

    ap = argparse.ArgumentParser(prog="hwsd_driver")
    ap.add_argument("cmd", choices=("s0", "audit", "kd", "sample", "score", "summary", "close",
                                    "dry", "freeze", "inventory", "obligation"))
    for opt in OPTS:
        ap.add_argument(opt, default=None)
    a = ap.parse_args(argv)
    out = Path(a.out) if a.out else (dc.DRY_STORE if a.cmd == "dry" else dc.STORE)
    auth, sched = _load(a.auth), _load(a.sched)
    attempt, job = int(a.attempt or 1), a.job
    try:
        if a.cmd == "inventory":
            res = hd.inventory(dc.ROOT, a.save, _load(a.compare) if a.compare else None)
            print(json.dumps(res, indent=1)[:4000])
            return 0 if res.get("ok", True) else 3
        if a.cmd == "s0":
            r = hwsd_records.s0_d(dc.REPO, a.r_ref, a.h_exec)
            print(json.dumps(r, indent=1))
            return 0 if r["status"] == "PASS" else 2
        if a.cmd == "freeze":
            hwsd_records.freeze_d(out, dc.REPO, a.h_exec, a.dry_report, a.pf_record,
                                  a.kd4_params, a.run_approval)
            return 0
        if a.cmd == "audit":
            with hwsd_bind.bound_hwsd():
                au = hwsd_bind.audit()
            out.mkdir(parents=True, exist_ok=True)
            stage_records.write_new(out / "AUDIT.json", json.loads(json.dumps(au, default=str)))
            return 0 if au["status"] == "PASS" else 3
        if a.cmd == "obligation":
            store = Path(a.store or out)
            p, _ = hwsd_data.write_obligation(
                store, f"REGISTRY_OBLIGATION_{job}-a{attempt}.json", job, attempt,
                hwsd_records.utc())
            print(str(p))
            return 0
        if a.cmd == "dry":
            import hwsd_dry

            only = a.only.split(",") if a.only else None
            return 0 if hwsd_dry.run_dry(out, sched, only, job).get("all_pass") else 3
        if a.cmd == "kd":
            res = hd.run_kd(out, auth, sched, job, attempt, cont=a.__dict__["continue"])
        elif a.cmd == "sample":
            res = hd.run_sample(out, auth, sched, job, attempt, _load(a.kd_accept),
                                cont=a.__dict__["continue"])
        elif a.cmd == "score":
            res = run_score(out, auth, sched, job, attempt, int(a.master), _load(a.accept),
                            a.__dict__["continue"])
        elif a.cmd == "summary":
            acc = _load(a.accept) or {j: _load(out / f"ACCEPT_SCORE_{j}.json") if (
                out / f"ACCEPT_SCORE_{j}.json").is_file() else None for j in dc.MASTERS}
            res = run_summary(out, auth, sched, job, attempt, acc, a.__dict__["continue"])
        else:
            res = hd.run_close(out, REFUSE, a.reason, job, attempt)
    except hwsb_driver.Paused:
        return 4
    except C1GateFailure as exc:
        print(f"{hwsd_records.status_of(exc)}: {exc.reason}")
        return 3
    print(json.dumps(res, indent=1, default=str)[:4000])
    return _exit(res if isinstance(res, dict) else {})
