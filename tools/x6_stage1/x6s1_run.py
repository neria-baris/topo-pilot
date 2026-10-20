"""X6S1 run (local): S0 and bindings, NB-STATIC, environment, sealing, lineage, gate and stage
records, local waves under the repaired D-2a supervisor, RUNTIME-ACCT, TRAIN-EQUIV, the stage
runner and CLI (X6S1-FROZEN-v1 §4.6, §5.11, §8, §12, §14.5; API.md §11, §13 items 27-28). Gate
content: x6s1_stage_pre/_post via a lazy import (R-0079-1); no import-time I/O (§13 item 24)."""
# fmt: off

from __future__ import annotations

import dataclasses
import hashlib
import io
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import x6s1_data as sd  # first: its import applies the API §1 sys.path convention

# isort: split
import d2a_train
import numpy as np
import torch
import x6_store as xs
import x6s1_cloud as sc
import x6s1_ingest as si
from d2a_train import D2AStop, Limits, Supervisor, bound_controls, boundary, disk_reason

from topo_pilot.contracts import canonical_json

REPO, TOOL = sd.REPO, sd.REPO / "tools" / "x6_stage1"
archive_attempt, compare_attempt, lineage_precheck = (  # the x6_store generics, unchanged
    xs.archive_attempt, xs.compare_attempt, xs.lineage_precheck)
strip_volatile, write_manifest, read_manifest = (
    xs.strip_volatile, xs.write_manifest, xs.read_manifest)
PROTECTED = ("src", "pyproject.toml", "tools/x4_oracle_profile", "tools/x6_stage0", "tools/d2a",
             "tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/check_file_sizes.py", "tools/check_imports.py", "tools/x6_stage1",
             "tests/learner", "tests/dataset", "tests/contracts", "tests/oracle",
             "tests/oracle_profile", "tests/world", "tests/process", "tests/x6_stage0", "tests/d2a",
             "tests/k4b", "tests/c1prime_registry", "tests/x6_stage1")
MODULES = ("x6s1_data.py", "x6s1_pairs.py", "x6s1_cloud.py", "x6s1_ingest.py", "x6s1_eval.py",
           "x6s1_decide.py", "x6s1_run.py", "x6s1_registry.py", "x6s1_stats.py",
           "x6s1_stage_pre.py", "x6s1_stage_post.py")  # eleven (R-0079-1)
_FIXED = tuple(f"tools/x6_stage1/{f}" for f in (
    "API.md", "PROTOCOL_X6S1_v1.md", "X6S1_colab.ipynb") + MODULES) + tuple(
    f"tests/x6_stage1/AUTHORSHIP_{x}.md" for x in "AB")
ALLOWLIST = _FIXED + ("tests/x6_stage1/test_a_<name>.py", "tests/x6_stage1/test_b_<name>.py")
_TEST_RE = re.compile(r"tests/x6_stage1/test_([ab])_[a-z0-9_]+\.py")
GATES = ("IMPL", "AUTH-ADMIT", "S0", "PF", "G0-ORC", "SCORE", "G0-POS", "REG", "G0-FEAS",
         "HEADROOM-D", "CLOUD-PREP", "AUTH-VERIFY", "SMOKE-INGEST", "INGEST-C1", "LEARN", "LC-1",
         "INGEST-C2", "LC-2", "E3.0", "E3.1", "E3.A", "E3.2", "E3.3", "E3.4", "E3.5", "E3.6",
         "E3.7", "E3.8", "E3.9")
STAGES = ("E0", "E0b", "E1", "E2", "E3a", "E3w", "E3z")
STUDY_ROWS = ("S0", "S1", "S2", "S3", "S3R", "S4", "S6", "S7", "S9", "S10", "S11", "S12", "S13")
METER_VALUES = {"OUTPUT_CAP": 16 * 2**30, "MEMORY_CAP": 12 * 2**30, "CAP_S": math.inf,
                "STOP_NEW_S": math.inf}
VOLATILE_KEYS = xs.VOLATILE_KEYS | {"session_id", "pid", "peak_mem_bytes", "built_utc", "env_local"}
AUTH_FIELDS = ("protocol_sha256", "local_budget", "cloud_use", "smoke_preflight", "transfers",
               "owner_sessions")
REQUEST = Path(sd.MAILBOX) / "planning" / "requests" / "coord-x6-stage1-20261018.md"
FROZEN = Path(sd.MAILBOX) / "planning" / "responses" / "X6S1-FROZEN-v1.md"
NB_REL, BIND = "tools/x6_stage1/X6S1_colab.ipynb", "x6s1_meter_bind.py"
STORE_FILES = ("FREEZE.json", "AUTH.json", BIND, "cpu_ledger.json", "cpu_ledger.json.tmp",
               "cpu_ledger.emergency.jsonl", "RUN.lock", "METER_ACTIVE.lock")
K_ACCT = 50  # RUNTIME-ACCT recipe: one chunk of the 50 ACCT_CFG updates (API.md §13 item 27)
_CTX = {"store": sd.STORE, "job": None, "task": None}  # the dispatch identities of this process

def _sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def _cj(obj) -> bytes: return canonical_json(xs.jsonable(obj)).encode("utf-8")
def _load(p): return p if isinstance(p, dict) else json.loads(Path(p).read_text("utf-8-sig"))
def _utc() -> str: return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def _st(ok, detail=None) -> dict: return {"status": "PASS" if ok else "FAIL", "detail": detail}
def _norm(p) -> str: return os.path.normcase(os.path.abspath(str(p)))
def _git(wt, *args, text=True):
    return subprocess.run(["git", "-C", str(wt), *args], capture_output=True, text=text,
                          check=True).stdout
def _lines(wt, *args) -> list: return [ln for ln in _git(wt, *args).splitlines() if ln.strip()]
def _blob(wt, head, rel) -> bytes: return _git(wt, "cat-file", "blob", f"{head}:{rel}", text=False)

# ---- S0 and binding (API 11.1; §8 row 1, §14.5) ----
def allowlist_ok(lines) -> bool:
    tests = []
    for ln in lines:
        m = _TEST_RE.fullmatch(ln[2:])
        if ln[:2] != "A	" or not (m or ln[2:] in _FIXED):
            return False
        tests += [m.group(1)] if m else []
    return tests.count("a") <= 5 and tests.count("b") <= 5
def repair_ok(worktree, head, freeze=None) -> dict:
    """§8 S0 (iv): P ancestor of R; blobs at H = REPAIR_BLOBS (= FREEZE's); tools/d2a P = H."""
    bad, wt = [], Path(worktree)
    if subprocess.run(["git", "-C", str(wt), "merge-base", "--is-ancestor", sd.P_COMMIT,
                       sd.R_COMMIT]).returncode != 0:
        bad.append("P not an ancestor of R")
    for rel, (sha, blob) in sd.REPAIR_BLOBS.items():
        frz = (freeze or {}).get("repair_blobs", {}).get(rel) if freeze is not None else (sha, blob)
        try:
            got = (_sha(_blob(wt, head, rel)), _git(wt, "rev-parse", f"{head}:{rel}").strip())
        except subprocess.CalledProcessError:
            got = None
        if got != (sha, blob) or [str(x).lower() for x in frz or ()] != [sha, blob]:
            bad.append(rel)
    if _lines(wt, "diff", "--name-only", sd.P_COMMIT, head, "--", "tools/d2a"):
        bad.append("tools/d2a changed P → H")
    return _st(not bad, bad)
def notebook_sha_ok(worktree, head, freeze) -> bool:
    try:
        want = str(_load(freeze).get("notebook_sha256", "")).strip().lower()
        return _sha(_blob(worktree, head, NB_REL)) == want
    except (OSError, ValueError, subprocess.CalledProcessError):
        return False
def seed_fresh(seed_maps) -> bool:
    masters = {sd.DATA_MASTER, sd.MODEL_MASTER}
    def hit(v):
        if isinstance(v, dict):
            return any(hit(x) for x in v.values())
        if isinstance(v, (list, tuple)):
            return any(hit(x) for x in v)
        return isinstance(v, (int, np.integer)) and not isinstance(v, bool) and int(v) in masters
    return not any(hit(m) for m in seed_maps)
def _seed_maps(project_root, store) -> list:
    """§6.2: seed maps and configs of the project's other ArtifactStores (D-2a pattern)."""
    out = []
    for root in sorted(Path(project_root).glob("*store*")):
        if root.is_dir() and _norm(root) != _norm(store):
            for meta in sorted(root.rglob("meta.json")):
                try:
                    m = json.loads(meta.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    continue
                out.append({"seed_map": m.get("seed_map"), "config": m.get("config")})
    return out
def auth_ok(store, protocol_sha256) -> bool:
    try:
        a = json.loads((Path(store) / "AUTH.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return False
    if not isinstance(a, dict) or any(a.get(k) in (None, "", [], {}) for k in AUTH_FIELDS):
        return False
    return str(a["protocol_sha256"]).strip().lower() == str(protocol_sha256).strip().lower()
def meter_bind_check(path, expected_sha256, import_dir) -> None:
    if _sha(Path(path).read_bytes()) != str(expected_sha256).strip().lower():
        raise RuntimeError(f"meter binding {path}: sha256 differs from the dispatch record")
    if _norm(import_dir) != _norm(Path(sd.WORKTREE) / "tools" / "x4_oracle_profile"):
        raise RuntimeError(f"meter import directory {import_dir} is not the execution worktree's")
def dispatch_identities(mailbox, job_id, task_sha256, session, lock_path) -> None:
    d2a_train.verify_identity(mailbox, job_id, task_sha256, session, lock_path)
def store_lineage(store, accepted=None) -> dict:
    """§12 item 8: x6_store lineage + static files + earlier accepted outputs (relpath → sha)."""
    store, acc = Path(store), {k: str(v).lower() for k, v in (accepted or {}).items()}
    out = lineage_precheck(store)
    out["unrecognised"] = [r for r in out["unrecognised"] if r not in STORE_FILES and not (
        r in acc and xs.sha256_file(store / r) == acc[r])]
    bad = out["unrecognised"] or out["missing"] or out["mismatch"] or not out["run_absent"]
    out["status"] = "INVALID/LINEAGE" if bad else "PASS"
    return out
def s0_check(worktree, head, store, dispatch, freeze) -> dict:
    wt, store, disp, frz = Path(worktree), Path(store), _load(dispatch), _load(freeze)
    def item(fn):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001  (an unreadable binding is a failed item)
            return _st(False, f"{type(exc).__name__}: {exc}")
    def protocol():
        a = _sha(_blob(wt, head, "tools/x6_stage1/PROTOCOL_X6S1_v1.md"))
        b = _sha(FROZEN.read_bytes())
        return _st(a == b == sd.PROTOCOL_SHA256, {"copy": a, "frozen": b})
    def stage0():
        got = {r: xs.sha256_file(Path(sd.STAGE0_STORE) / r) for r in sd.STAGE0_FILES}
        rep = json.loads((Path(sd.STAGE0_STORE) / "run" / "report.json").read_text("utf-8"))
        const = sd.check_stage0_constants(rep)
        ok = got == sd.STAGE0_FILES and rep["outcome"]["outcome"] == sd.STAGE0_OUTCOME
        return _st(ok and const["status"] == "PASS", {"files": got, "constants": const})
    def ident():
        dispatch_identities(sd.MAILBOX, disp["job"], disp["task_sha256"], disp["worker_session"],
                            store / "RUN.lock")
        meter_bind_check(store / BIND, disp["meter_bind_sha256"], disp["meter_import_dir"])
        return _st(True)
    def lineage():
        lin = store_lineage(store, disp.get("accepted_outputs"))
        return _st(lin["status"] == "PASS", lin)
    def diff():
        return _lines(wt, "diff", "--no-renames", "--name-status", sd.R_COMMIT, head, "--",
                      *PROTECTED)
    def binding():
        r, a = repair_ok(wt, head, frz), auth_ok(store, sd.PROTOCOL_SHA256)
        return _st(r["status"] == "PASS" and a, {"repair": r, "auth": a})
    items = {
        "i": item(protocol),
        "ii": item(lambda: _st(_sha(REQUEST.read_bytes()) == sd.REQUEST_SHA256)),
        "iii": item(lambda: (lambda d: _st(allowlist_ok(d), d))(diff())),
        "iv": item(binding),
        "v": item(stage0),
        "vi": item(lambda: _st(seed_fresh(_seed_maps(sd.PROJECT_ROOT, store)))),
        "vii": item(ident), "viii": item(lineage),
        "ix": item(lambda: _st(notebook_sha_ok(wt, head, frz)))}
    return {**items, "status": "PASS" if all(v["status"] == "PASS" for v in items.values())
            else "INVALID"}

# ---- NB-STATIC (API 11.2; §5.11, T-NB) ----
def nb_static(path) -> dict:
    try:
        nb = json.loads(Path(path).read_text(encoding="utf-8"))
        cells = nb["cells"]
        code = [c for c in cells if c.get("cell_type") == "code"]
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return {"status": "FAIL", "detail": [f"unreadable: {type(exc).__name__}"]}
    src = [sc.normalise_source("".join(c.get("source", ""))) for c in code]
    bad = [f for f, ok in (
        ("nbformat", nb.get("nbformat") == 4), ("six code cells", len(code) == 6),
        ("cell types", all(c.get("cell_type") in ("code", "markdown") for c in cells)),
        ("sources", src == list(sc.CELL_TEMPLATES)),
        ("outputs", all(c.get("outputs") == [] and c.get("execution_count") is None for c in code)),
        ("code lines", sum(len(s.split("\n")) for s in src) <= 60)) if not ok]
    return {"status": "FAIL" if bad else "PASS", "detail": bad}
def bootstrap_check(bundle_dir, bundle_sha256) -> str:
    code = "\n".join(sc.CELL_TEMPLATES[2].split("\n")[1:8])  # template 3 lines 2-8 (API §12)
    try:
        exec(code, {"ROOT": Path(bundle_dir).as_posix(), "BUNDLE_SHA256": bundle_sha256})
    except SystemExit as exc:
        return str(exc)
    return "OK"

# ---- local environment, sealing, lineage (API 11.3; §2.2 OS 3, §12) ----
def env_local() -> dict:
    try:
        npc = np.show_config(mode="dicts")
    except TypeError:  # numpy without mode="dicts"
        npc = None
    return {"python": sys.version, "numpy": np.__version__, "torch": torch.__version__,
            "blas": {"numpy": xs.jsonable(npc), "torch": torch.__config__.show()},
            "cpu": {"processor": platform.processor(), "count": os.cpu_count()},
            "threads": {"intra": torch.get_num_threads(),
                        "interop": torch.get_num_interop_threads()},
            "thread_env": {v: os.environ.get(v) for v in d2a_train.THREAD_VARS[:3]},
            "batch": sd.EVAL_BATCH, "commit": _git(REPO, "rev-parse", "HEAD").strip()}
def env_changed(a, b) -> list:
    return sorted(k for k in set(a) | set(b)
                  if k not in VOLATILE_KEYS and a.get(k) != b.get(k))
def _strip(obj):
    if isinstance(obj, dict):
        return {k: _strip(v) for k, v in obj.items() if k not in VOLATILE_KEYS}
    return [_strip(v) for v in obj] if isinstance(obj, (list, tuple)) else obj
def reports_equal(a, b) -> bool: return xs.reports_equal(_strip(a), _strip(b))
def _released(store) -> bool:  # S9 (R-0082-4): an E3 stage record without a stop, or a study stop
    p, q = Path(store) / "STAGES.jsonl", Path(store) / "stages" / "STUDY_STOP.json"
    recs = [json.loads(ln) for ln in p.read_text("utf-8").splitlines()] if p.is_file() else []
    return q.is_file() or any(r["stage"].startswith("E3") and not r.get("stop") for r in recs)
def study_stop(store, row, stage, reason) -> str:  # a coordinator decision, recorded in a review
    if row not in STUDY_ROWS or stage not in STAGES or not str(reason or "").strip():
        raise ValueError(f"not a study stop: {row} {stage} (S5, S8 and a HOLD never are)")
    rec = {"row": row, "stage": stage, "reason": str(reason), "utc": _utc()}
    return si._xwrite(Path(store) / "stages" / "STUDY_STOP.json", _cj(rec))  # exclusive create
def seal(store, name, obj) -> str:
    (Path(store) / "sealed").mkdir(parents=True, exist_ok=True)
    return si._xwrite(Path(store) / "sealed" / name, _cj(obj))
def unseal(store, name, sha256) -> dict:
    if not _released(store):
        raise RuntimeError(f"sealed/{name} is sealed until E3 or a stop (§4.7, S9)")
    data = (Path(store) / "sealed" / name).read_bytes()
    if _sha(data) != str(sha256).lower():
        raise RuntimeError(f"sealed/{name}: sha256 differs from the stage record")
    return json.loads(data)
def log_evaluation(store, model, kind, stage) -> None:
    """Write-ahead evaluation log (§12 item 9): appended before any local evaluation."""
    with open(Path(store) / "EVALUATIONS.jsonl", "ab") as fh:
        fh.write(_cj({"model": model, "kind": kind, "stage": stage, "utc": _utc()}) + b"\n")
def evaluations(store, model) -> list:
    p = Path(store) / "EVALUATIONS.jsonl"
    rows = [json.loads(ln) for ln in p.read_text("utf-8").splitlines()] if p.is_file() else []
    return [r["kind"] for r in rows if r.get("model") == model]
def retrain_route_ok(store, model) -> bool:
    return si.retrain_eligible(store, model, evaluations(store, model))

# ---- gate and stage records (API 11.4) ----
def write_gate(store, gate, status, values) -> dict:
    if gate not in GATES:
        raise ValueError(gate)
    rec = {"gate": gate, "status": status, "values": xs.jsonable(values), "utc": _utc()}
    with open(Path(store) / "GATES.jsonl", "ab") as fh:
        fh.write(_cj(rec) + b"\n")
    return rec
def write_stage(store, stage, record) -> Path:
    d = Path(store) / "stages" / stage
    d.mkdir(parents=True, exist_ok=True)
    sha = si._xwrite(d / "record.json", _cj(record))
    with open(Path(store) / "STAGES.jsonl", "ab") as fh:
        fh.write(_cj({"stage": stage, "record_sha256": sha, "stop": record.get("stop"),
                      "utc": _utc()}) + b"\n")
    return d / "record.json"

# ---- local waves under the repaired supervisor (API 11.5; §4.6, §13.3-§13.4) ----
def limits(model_cpu_s=math.inf) -> Limits:
    return Limits(model_cpu_s, process_mem=sd.PROCESS_MEM, stage_cpu_s={
        "E3": math.inf, "PF": math.inf}, total_cpu_s=math.inf, job_mem=sd.JOB_MEM,
        poll_s=sd.ACCT_POLL_S)
def launch(args, log_path):
    from process_tree import TrainingProcess
    env = dict(os.environ, **{v: str(sd.THREADS["intra"]) for v in d2a_train.THREAD_VARS},
               PYTHONPATH=str(REPO / "src"), PYTHONDONTWRITEBYTECODE="1")
    with Path(log_path).open("xb") as out:
        return TrainingProcess([str(a) for a in args], stdout=out, stderr=subprocess.STDOUT,
                               env=env, cwd=str(REPO))
def supervise(children, limits, stage, clock=time.monotonic) -> dict:
    """Poll every `poll_s` until every child has exited (§4.6, S6); STOP/HOLD at each poll."""
    sup = Supervisor(limits, cpu_of=lambda h: h.cpu_s(), mem_of=lambda h: h.memory_bytes(),
                     kill=lambda h: h.terminate(), clock=clock)
    classify = bound_controls(_CTX["store"], _CTX["job"], _CTX["task"])
    live, out, peak = dict(children), {}, dict.fromkeys(children, 0)
    try:
        while live:
            time.sleep(limits.poll_s)
            boundary(classify, poll_s=limits.poll_s)
            why = disk_reason()
            if why:
                raise D2AStop(why)
            killed, now = sup.check(live, 0.0, 0.0, stage), clock()
            for name, h in list(live.items()):
                peak[name] = max(peak[name], int(h.memory_bytes()))
                if name not in killed and h.poll() is None:
                    continue
                while h.poll() is None:
                    time.sleep(0.05)
                rc, st = h.returncode, killed.get(name, {}).get("reason")
                out[name] = {"status": st or ("DONE" if rc == 0 else "FAILED"),
                             "cpu_s": float(h.cpu_s()), "peak_mem_bytes": peak[name],
                             "returncode": rc, "killed_at": now if st else None,
                             "exited_at": clock()}
                h.close()
                del live[name]
    finally:
        for h in live.values():
            try:
                h.terminate()
            finally:
                h.close()
    return out
def eval_wave(store, wave_name, names) -> dict:
    """E3.A: ≤ MAX_CHILDREN `eval-chunk` children under the wave lease; outputs under
    stages/<wave_name>/<name>/ by exclusive create (§13.3)."""
    from process_tree import wave_lease
    store, names = Path(store), list(names)
    out = store / "stages" / wave_name
    if len(names) > sd.MAX_CHILDREN or any((out / n).exists() for n in names):
        raise FileExistsError(f"wave {wave_name}: refused (outputs exist or > MAX_CHILDREN)")
    with wave_lease(store, wave_name):
        (store / "logs").mkdir(exist_ok=True)
        idn = ["--job", _CTX["job"], "--task-sha256", _CTX["task"]]
        kids = {n: launch([sys.executable, "-s", Path(__file__), "eval-chunk", n, "--store", store,
                           "--out", out, *idn], store / "logs" / f"eval_{n}_{sc.utc_stamp()}.txt")
                for n in names}
        res = supervise(kids, limits(), "E3")
    return {"wave": wave_name, "children": res, "chunks": {
        n: _load(out / n / "chunk.json") if (out / n / "chunk.json").is_file() else None
        for n in names}}

# ---- RUNTIME-ACCT and TRAIN-EQUIV (PF; §4.6) ----
def _smoke_root(root, smoke, cfg, k) -> dict:
    """A local C0-shaped root for the chunked trainer with the recipe (cfg, k) on the stored smoke
    pool (`smoke`: {"path", "file_sha256", "data_seed"}) and the SMOKE init state."""
    root = Path(root)
    (root / "data").mkdir(parents=True)
    (root / "init").mkdir()
    toks = sd.load_pool(smoke["path"], smoke["file_sha256"])
    shutil.copyfile(smoke["path"], root / "data" / "smoke.npy")
    init = sd.init_state("SMOKE")
    torch.save(init, root / "init" / "init_smoke.pt")
    pools = {"SMOKE": {"file_sha256": smoke["file_sha256"], "token_sha256": sd.token_digest(toks),
                       "n_rows": len(toks), "data_seed": smoke["data_seed"]}}
    inits = {"SMOKE": {"file_sha256": xs.sha256_file(root / "init" / "init_smoke.pt"),
                       "weights_sha256": sc.weights_digest(init["model"])}}
    t = si.make_ticket("C0", _git(REPO, "rev-parse", "HEAD").strip(), pools, inits)
    t.update(train_config=json.loads(_cj(dataclasses.asdict(cfg))), steps=cfg.steps, K=k,
             smoke_resume=False)
    t["models"][0]["expected"] = sc.expected_digests(sd.MODEL_MASTER, ("x6s1", "smoke"),
                                                     len(toks), cfg.steps, k)
    (root / "ticket_C0.json").write_bytes(_cj(t))
    return {"root": root, "tokens": toks, "ticket": t}
def _child(root, max_chunks=None) -> list:
    extra = ["--max-chunks", str(max_chunks)] if max_chunks else []
    return [sys.executable, "-s", TOOL / "x6s1_cloud.py", "train", root, "SMOKE", "--device",
            "cpu", *extra]
def _job_cpu_s() -> float:  # the CPU of this process's job object: the meter's job
    import winjob
    return sum(winjob.job_cpu(None)[:2])
def runtime_acct(scratch, smoke) -> dict:
    """§4.6 RUNTIME-ACCT items 1-5 (two normal children, one at 5 CPU-s; metered job)."""
    scratch = Path(scratch)
    r = {n: _smoke_root(scratch / f"acct_{n}", smoke, sd.ACCT_CFG, K_ACCT)["root"]
         for n in ("a", "b", "kill")}
    kid = lambda n: launch(_child(r[n]), scratch / f"acct_{n}.log")  # noqa: E731
    ch = supervise({n: kid(n) for n in ("a", "b")}, limits(), "PF")
    ch.update(supervise({"kill": kid("kill")}, limits(sd.ACCT_KILL_CPU), "PF"))
    meter = _job_cpu_s()
    fin = all(_load(r[n] / "out/SMOKE/rec" / f"{sd.ACCT_CFG.steps:06d}.json")["loss_finite"]
              for n in ("a", "b") if ch[n]["status"] == "DONE")
    k = ch["kill"]
    checks = {"1": fin and all(ch[n]["status"] == "DONE" for n in ("a", "b")),
              "2": all(ch[n]["cpu_s"] >= sd.ACCT_CPU_MIN for n in ("a", "b")),
              "3": all(c["peak_mem_bytes"] >= sd.ACCT_MEM_MIN for c in ch.values()),
              "4": sum(c["cpu_s"] for c in ch.values()) <= meter + 1.0,
              "5": k["status"] == "INCOMPLETE:MODEL_CPU" and k["exited_at"] - k["killed_at"]
              <= sd.ACCT_POLL_S + sd.ACCT_KILL_SLACK_S}
    return {"status": "PASS" if all(checks.values()) else "INVALID", "checks": checks,
            "children": ch, "meter_cpu_s": meter}
class _RecGen:  # delegates to the reference PCG64 generator and records every index array
    def __init__(self, gen): self._g, self.draws = gen, []  # noqa: E704
    bit_generator = property(lambda self: self._g.bit_generator)
    def integers(self, *a, **k):
        self.draws.append(np.array(self._g.integers(*a, **k), copy=True))
        return self.draws[-1]
class _Seeds:  # delegating SeedTree wrapper exposing the reference generator (§4.6, RC11)
    def __init__(self, master):
        from topo_pilot.contracts import SeedTree
        self._t, self.gen = SeedTree(master), None
        self.issued = self._t.issued
    def seed(self, name, *scope): return self._t.seed(name, *scope)  # noqa: E704
    def generator(self, name, *scope):
        g = self._t.generator(name, *scope)
        self.gen = _RecGen(g) if name == "batch_order" else self.gen
        return self.gen if name == "batch_order" else g
def _diff(a, b, path="$") -> list:
    if isinstance(a, torch.Tensor):
        ok = isinstance(b, torch.Tensor) and a.dtype == b.dtype and a.shape == b.shape
        return [] if ok and torch.equal(a.cpu(), b.cpu()) else [path]
    if isinstance(a, dict):
        if not isinstance(b, dict) or set(a) != set(b):
            return [path]
        return [m for k in a for m in _diff(a[k], b[k], f"{path}.{k}")]
    if isinstance(a, (list, tuple)):
        if not isinstance(b, (list, tuple)) or len(a) != len(b):
            return [path]
        return [m for i, (x, y) in enumerate(zip(a, b)) for m in _diff(x, y, f"{path}[{i}]")]
    return [] if a == b else [path]
def _reference(toks, cfg) -> dict:
    """§4.6 item 1: the unchanged Trainer.fit on CPU with 2 intra-op threads."""
    from topo_pilot.contracts import ObservationSet, SequenceLayout
    from topo_pilot.dataset import PublicTokenDataset
    from topo_pilot.dataset.checks import make_sequence_ids, process_code
    from topo_pilot.learner import Trainer
    def ds(t):
        ids = make_sequence_ids(process_code("x6s1", "NA", "smoke", 0), "dev", len(t))
        return PublicTokenDataset(ObservationSet("dev", 18, ids, t), SequenceLayout())
    seeds, final, init = _Seeds(sd.MODEL_MASTER), {}, {}
    tr = Trainer(sd.MODEL_CFG, cfg, seeds, ("x6s1", "smoke"))
    def cb(step, model, info):
        if step == 0:
            init.update({k: v.detach().clone() for k, v in model.state_dict().items()})
        if info["is_final"]:
            buf = io.BytesIO()
            torch.save({"optimizer": info["optimizer_state"],
                        "scheduler": info["scheduler_state"]}, buf)
            final.update(torch.load(io.BytesIO(buf.getvalue()), weights_only=False))
    old = torch.get_num_threads()
    torch.set_num_threads(sd.THREADS["intra"])
    try:
        tr.fit(ds(toks), ds(toks[:64]), cb)
    finally:
        torch.set_num_threads(old)
    final["model"] = {k: v.detach().clone() for k, v in tr.model.state_dict().items()}
    return {**final, "init": init, "pcg64": seeds.gen.bit_generator.state, "draws": seeds.gen.draws}
def train_equiv(scratch, smoke) -> dict:
    """§4.6 TRAIN-EQUIV: chunked training (K = 20, two fresh-process resumes) = Trainer.fit."""
    cfg, k = sd.EQUIV_CFG, sd.K_EQUIV
    b = _smoke_root(Path(scratch) / "equiv", smoke, cfg, k)
    env = dict(os.environ, PYTHONPATH=str(REPO / "src"),
               **{v: str(sd.THREADS["intra"]) for v in d2a_train.THREAD_VARS})
    codes = [subprocess.run([str(a) for a in _child(b["root"], m)], env=env, cwd=str(REPO),
                            capture_output=True).returncode for m in (1, 1, None)]
    ref, md = _reference(b["tokens"], cfg), b["root"] / "out" / "SMOKE"
    def ld(s):
        return torch.load(md / "ckpt" / f"{s:06d}.pt", map_location="cpu", weights_only=False)
    fin, mis = ld(cfg.steps), [f"exit {c}" for c in codes if c != 0]
    for key in ("model", "optimizer", "scheduler"):
        mis += _diff(fin[key], ref[key], key)
    mis += _diff(ld(0)["model"], ref["init"], "init")
    mis += [] if [g["lr"] for g in fin["optimizer"]["param_groups"]] == list(
        ref["scheduler"]["_last_lr"]) else ["lr"]
    mis += [] if fin["rng"]["pcg64"] == ref["pcg64"] else ["pcg64"]
    mis += [] if fin["step"] == cfg.steps == fin["scheduler"]["last_epoch"] else ["step"]
    for c, s in enumerate(range(k, cfg.steps + 1, k), start=1):
        rec = _load(md / "rec" / f"{s:06d}.json")
        want = sc.batch_digest(ref["draws"][(c - 1) * k:c * k])
        mis += [] if rec["batch_sha256"] == want and rec["step"] == s else [f"batch {s}"]
    return {"status": "PASS" if not mis else "INVALID", "mismatches": mis}

# ---- stage dispatch and CLI (API 11.6; §8; the gate content: R-0079-1) ----
def _stage(stage):  # lazy: the stage modules import this one (no cycle, no import-time I/O)
    import importlib
    return importlib.import_module("x6s1_stage_pre" if stage in STAGES[:2] else "x6s1_stage_post")
def run_stage(stage, store, dispatch) -> dict:
    """PLAN[stage] (step, fn(ctx), validity) in §8 order after the disk floor and boundary; the
    first non-PASS validity gate stops (later NOT_RUN); "G/part" records G only on failure."""
    store, disp = Path(store), _load(dispatch)
    _CTX.update(store=str(store), job=str(disp["job"]), task=str(disp["task_sha256"]))
    classify = bound_controls(store, disp["job"], disp["task_sha256"])
    ctx = {"store": store, "dispatch": disp, "head": disp["head"], "stage": stage, "res": {}}
    rec, t0, w0 = {"stage": stage, "head": disp["head"], "gates": {}, "values": {}, "stop": None,
                   "env_local": env_local()}, time.process_time(), time.perf_counter()
    for step, fn, validity in _stage(stage).PLAN[stage]:
        gate, part = step.partition("/")[::2]
        if rec["stop"] is None:
            try:
                why = disk_reason()
                if why:
                    raise D2AStop(why)
                boundary(classify)
                res = ctx["res"][step] = fn(ctx)
            except D2AStop as exc:  # S8: owner STOP, usage limit or disk floor
                res, rec["stop"] = {"status": "INVALID", "values": {"S8": str(exc)}}, f"S8 {gate}"
            except Exception as exc:  # noqa: BLE001  (a recorded defect, never a silent pass)
                res = {"status": "INVALID", "values": {"error": f"{type(exc).__name__}: {exc}"}}
        elif gate in rec["gates"]:
            continue
        else:
            res = {"status": "NOT_RUN", "values": None}
        rec["values"][step] = res.get("values")
        if not part or res["status"] != "PASS":
            rec["gates"][gate] = res["status"]
            write_gate(store, gate, res["status"], res.get("values"))
        if validity and rec["stop"] is None and res["status"] != "PASS":
            rec["stop"] = gate
    rec.update(cpu_s=time.process_time() - t0, wall_s=time.perf_counter() - w0)
    write_stage(store, ctx.get("stage_dir", stage), rec)
    return rec
def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=STAGES + ("eval-chunk", "study-stop"))
    ap.add_argument("name", nargs="?")
    for opt in ("--store", "--job", "--task-sha256", "--session", "--dispatch", "--out", "--row",
                "--stage", "--reason"):
        ap.add_argument(opt)
    a = ap.parse_args(argv)
    if a.cmd == "study-stop":  # stages/STUDY_STOP.json (R-0082-4)
        return print(study_stop(a.store or sd.STORE, a.row, a.stage, a.reason)) or 0
    _CTX.update(store=a.store or sd.STORE, job=a.job, task=a.task_sha256)
    if a.cmd == "eval-chunk":
        import x6s1_eval as se
        se.set_threads()
        plan = _stage("E3a").chunk_plan(Path(a.store), a.name)  # the E3.A input builder
        return 0 if se.eval_chunk(a.name, plan, Path(a.out)) else 2
    disp = _load(a.dispatch) if a.dispatch else {}
    if (disp.get("job"), disp.get("task_sha256", "").lower(), disp.get("worker_session")) != (
            a.job, str(a.task_sha256).lower(), a.session):
        print("STOP: dispatch record does not match --job/--task-sha256/--session")
        return 2
    rec = run_stage(a.cmd, a.store, disp)
    print(json.dumps({"stage": a.cmd, "gates": rec["gates"], "stop": rec["stop"]}))
    return 2 if rec["stop"] else 0

if __name__ == "__main__":
    sys.modules.setdefault("x6s1_run", sys.modules[__name__])  # the stage modules share _CTX
    sys.exit(main())
