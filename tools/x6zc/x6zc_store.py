"""X6ZC store: JSON helpers, exclusive-create records (EXPOSURE, EVALUATIONS, STAGES, rulings),
the stage-1 store no-write inventory, environment, closure and master checks, the meter binding
and its template, ledger and pause points, the freeze check (API.md §11.1-§11.3, §20 C-52)."""
# fmt: off

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
import time
from fractions import Fraction
from pathlib import Path

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
import numpy as np  # noqa: E402

from topo_pilot.contracts import canonical_json  # noqa: E402

C, X = zc.CONTRACT, zc.CONTRACT["x6s1_store"]
FAM, VO, CO = zc.FAMILIES, zc.VARIANT_ORDER, zc.CELL_ORDER
def _utc() -> str: return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def _sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def _norm(p) -> str: return os.path.normcase(os.path.abspath(str(p)))
def _js(v):  # JSON-ready: numpy scalars and arrays, tuple keys "a|b", Fractions "p/q", NaN null
    if isinstance(v, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): _js(x)
                for k, x in v.items()}
    if isinstance(v, (list, tuple, np.ndarray)):
        return [_js(x) for x in (v.tolist() if isinstance(v, np.ndarray) else v)]
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return float(v) if math.isfinite(v) else None
    return f"{v.numerator}/{v.denominator}" if isinstance(v, Fraction) else v
def _cj(obj) -> bytes: return canonical_json(_js(obj)).encode("utf-8")

# ---- records (API §11.1-§11.2) ----
def xwrite(path, data: bytes) -> str:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as fh:  # exclusive create: FileExistsError on an existing file
        fh.write(data)
    return _sha(data)
def _append(path, obj) -> dict:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "ab") as fh:
        fh.write(_cj(obj) + b"\n")
    return obj
def _lines(path) -> list:
    p = Path(path)
    return [json.loads(x) for x in p.read_text("utf-8").splitlines() if x.strip()] if (
        p.exists()) else []
def log_exposure(store, stage, artifact, expected_sha256, purpose) -> dict:
    ex = _lines(Path(store) / "EXPOSURE.jsonl")
    k = 1 + sum(str(e.get("id", "")).startswith("X") for e in ex)
    return _append(Path(store) / "EXPOSURE.jsonl", {
        "id": f"X{k}", "stage": stage, "store": "x6-stage1-store", "artifact": artifact,
        "expected_sha256": expected_sha256, "purpose": purpose, "utc": _utc()})
def guard(stage, set_name) -> None:
    if set_name == "fresh" and stage != "C":
        raise RuntimeError(f"a model evaluation on the fresh set outside Stage C ({stage})")
def log_evaluation(store, model, kind, stage, set_name) -> dict:
    guard(stage, set_name)
    return _append(Path(store) / "EVALUATIONS.jsonl", {
        "model": model, "kind": kind, "stage": stage, "set": set_name, "utc": _utc()})
def write_stage(store, stage, record) -> Path:
    p = Path(store) / "stages" / stage / "record.json"
    sha = xwrite(p, _cj(record))
    _append(Path(store) / "STAGES.jsonl", {"stage": stage, "record_sha256": sha,
                                           "stop": record.get("stop"), "utc": _utc()})
    return p
def write_ruling(store, rid, check, stage, cause_identified, affects_beta, cause, defect_md=None,
                 setup=False) -> Path:
    p = Path(store) / "rulings" / f"{rid}.json"
    xwrite(p, _cj({"id": rid, "check": check, "stage": stage, "cause": cause, "setup": setup,
                   "cause_identified": bool(cause_identified), "affects_beta": bool(affects_beta),
                   "defect_md": defect_md, "utc": _utc()}))
    return p
def rulings(store) -> list:
    return [json.loads(p.read_text("utf-8"))
            for p in sorted((Path(store) / "rulings").glob("*.json"))]

# ---- guards and environment (API §11.3) ----
def x6s1_inventory(store=zc.X6S1_STORE) -> dict:
    root, out = Path(store), {}
    for d, dirs, files in os.walk(root):
        for s in [x for x in dirs if x == "sealed"]:  # never listed: only its own mtime (C-15)
            dirs.remove(s)
            rel = (Path(d) / s).relative_to(root).as_posix() + "/"
            out[rel] = [0, os.stat(Path(d) / s).st_mtime_ns]
        for f in files:
            st = os.stat(Path(d) / f)
            out[(Path(d) / f).relative_to(root).as_posix()] = [st.st_size, st.st_mtime_ns]
    return out
def inventory_equal(a, b) -> bool:
    return {k: list(v) for k, v in a.items()} == {k: list(v) for k, v in b.items()}
def env_check(env) -> dict:
    import x6s1_run as sr
    ref = json.loads((Path(zc.X6S1_STORE) / X["env_reference"]["path"]).read_bytes())["env_local"]
    ch = sr.env_changed(env, ref)
    return {"status": "PASS" if set(ch) <= {"commit"} else "SETUP_ERROR", "changed": ch}
def closure_diff(worktree=zc.WORKTREE) -> list:
    out = subprocess.run(["git", "-C", str(worktree), "diff", "--name-status", zc.H3, "HEAD", "--",
                          *zc.CLOSURE], capture_output=True, text=True, check=True).stdout
    return [ln for ln in out.splitlines() if ln.strip()]
def _hit(v, master) -> bool:
    if isinstance(v, dict):
        return any(_hit(x, master) for x in v.values())
    if isinstance(v, (list, tuple)):
        return any(_hit(x, master) for x in v)
    return isinstance(v, (int, np.integer)) and not isinstance(v, bool) and int(v) == master
def master_fresh(project_root=zc.PROJECT_ROOT, master=zc.X6ZC_MASTER) -> dict:
    hits = []
    for root in sorted(p for p in Path(project_root).glob("*store*") if p.is_dir()):
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x not in ("sealed", ".git", ".venv")]
            try:
                m = json.loads((Path(d) / "meta.json").read_text("utf-8")) if (
                    "meta.json" in files) else {}
            except (OSError, ValueError):
                continue
            hits += [str(Path(d) / "meta.json")] * (_hit(m.get("seed_map"), master)
                                                     or _hit(m.get("config"), master))
    import x6s1_data as sd
    return {"fresh": not hits and master not in (sd.DATA_MASTER, sd.MODEL_MASTER), "hits": hits}
def meter_bind_check(path, expected_sha256, import_dir) -> None:
    if _sha(Path(path).read_bytes()) != str(expected_sha256).strip().lower():
        raise RuntimeError(f"meter binding {path}: sha256 differs from FREEZE.json")
    if _norm(import_dir) != _norm(zc.METER_IMPORT_DIR):
        raise RuntimeError(f"meter import directory {import_dir} is not the X6ZC worktree's")
BIND_TEMPLATE = r'''"""Store-local binding of the unchanged job-0014 meter for the X6ZC runs
(generated from BIND_TEMPLATE in tools/x6zc/x6zc_store.py; API.md §20 E-12, C-53; the
c2_meter_bind pattern).

Standard library only; run with the base interpreter and -I. Rebinds module-level names only:
this store's ledger, lock, emergency, active and log paths; CAP_S = STOP_NEW_S = inf (CPU
measured, not capped); OUTPUT_CAP 16 GiB; winjob.MEMORY_CAP 12 GiB; --max-cpu inf --max-wall inf
forced; the owner disk floors (C: 2 GB, X: 30 GB) as a launch refusal and a periodic safe-STOP.
controls.JOB_ID, controls.TASK_SHA256 and meter.WORKER_SESSION are read at launch from the
dispatch record named by the X6ZC_DISPATCH environment variable (keys "job", "task_sha256",
"worker_session"), so this file's sha256 does not depend on the run job.

Fail closed, before the meter starts: this file must lie in its store; the record must name this
file's sha256 ("meter_bind_sha256") and the import directory ("meter_import_dir") = the X6ZC
worktree's tools/x4_oracle_profile, and must carry the three identities; controls, meter and
winjob must be imported from that directory and have their recorded sha256.

Usage: X6ZC_DISPATCH=<record.json> python -I x6zc_meter_bind.py --label <stage>__<label>
       [meter options] -- CMD...
"""

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

WORKTREE = Path(r"@WORKTREE@")
IMPORT_DIR = WORKTREE / "tools" / "x4_oracle_profile"
OUT = Path(r"@STORE@")
GIB = 1024**3
DISK_MIN_FREE = {"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}
METER_FILES = {  # sha256 of the protected job-0014 meter (equal to the C2 binding's values)
    "controls": "c4fac9946c0fed21d6ac9eee913bad15e49cdc4595843e2737e7d8f4817f23eb",
    "meter": "738ea68accc7a02c0e5645fca75d1b0919cac66b9bdbe357d910f515d7de4903",
    "winjob": "3b29e863ab6ae97c16540c0d56dbf678d18b88922e54fbc731f5cc0ec5405785",
}


def _norm(p):
    return os.path.normcase(os.path.abspath(str(p)))


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _fail(why):
    sys.exit(f"x6zc_meter_bind: {why}")


if _norm(Path(__file__).resolve().parent) != _norm(OUT):
    _fail(f"this binding must lie in its store {OUT}")
RECORD = json.loads(Path(os.environ["X6ZC_DISPATCH"]).read_text(encoding="utf-8-sig"))
if str(RECORD.get("meter_bind_sha256", "")).strip().lower() != _sha(__file__):
    _fail("the dispatch record does not bind this file's sha256")
if _norm(RECORD.get("meter_import_dir", "?")) != _norm(IMPORT_DIR):
    _fail(f"the dispatch record's meter_import_dir is not {IMPORT_DIR}")
if any(not str(RECORD.get(k) or "").strip() for k in ("job", "task_sha256", "worker_session")):
    _fail("the dispatch record lacks job, task_sha256 or worker_session")
for name, want in METER_FILES.items():
    if _sha(IMPORT_DIR / f"{name}.py") != want:
        _fail(f"{IMPORT_DIR / name}.py differs from its recorded sha256")
sys.path.insert(0, str(IMPORT_DIR))

import controls  # noqa: E402  (job-0014, unchanged)
import meter  # noqa: E402  (job-0014, unchanged)
import winjob  # noqa: E402  (job-0014, unchanged)

for _mod in (controls, meter, winjob):
    if _norm(Path(_mod.__file__).parent) != _norm(IMPORT_DIR):
        _fail(f"{_mod.__name__} was imported from {_mod.__file__}, not from {IMPORT_DIR}")

controls.JOB_ID = str(RECORD["job"])
controls.TASK_SHA256 = str(RECORD["task_sha256"]).strip().upper()
meter.WORKER_SESSION = str(RECORD["worker_session"])
meter.OUT, meter.LEDGER, meter.LOCK = OUT, OUT / "cpu_ledger.json", OUT / "RUN.lock"
meter.EMERGENCY, meter.ACTIVE = OUT / "cpu_ledger.emergency.jsonl", OUT / "METER_ACTIVE.lock"
meter.LOG_DIR = OUT / "logs"
meter.CAP_S = meter.STOP_NEW_S = float("inf")  # owner override: CPU measured, not capped
meter.OUTPUT_CAP = 16 * GIB
winjob.MEMORY_CAP = 12 * GIB


def disk_reason(usage=shutil.disk_usage):
    for drive, minimum in DISK_MIN_FREE.items():
        try:
            free = usage(drive).free
        except OSError as exc:
            return f"disk safe-STOP: {drive} free space unreadable ({type(exc).__name__})"
        if free < minimum:
            return f"disk safe-STOP: {drive} free {free} < {minimum} bytes"
    return None


def make_limiter(disk=disk_reason, legacy=None):
    legacy = legacy or meter.limit_reason

    def limit_reason(ledger, child, args, active_wall, polls, mailboxes):
        if disk is not None and polls % 8 == 0:
            reason = disk()
            if reason:
                return reason, "CONTINUE"
        return legacy(ledger, child, args, active_wall, polls, mailboxes)

    return limit_reason


def _drop(args, flag):
    while flag in args:
        i = args.index(flag)
        del args[i : i + 2]


def rewrite_argv(argv):
    args = list(argv)
    sep = args.index("--") if "--" in args else len(args)
    head, tail = args[:sep], args[sep:]
    _drop(head, "--max-cpu")
    _drop(head, "--max-wall")
    return head + ["--max-cpu", "inf", "--max-wall", "inf"] + tail


def main():
    args = rewrite_argv(sys.argv[1:])
    reason = disk_reason()
    if reason:
        i = args.index("--label")
        args[i + 1] += "__REFUSED_disk_safe_stop"
        sep = args.index("--")
        args = args[:sep] + ["--", sys.executable, "-I", "-c", "raise SystemExit(4)"]
    meter.limit_reason = make_limiter()
    sys.argv = [sys.argv[0]] + args
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
'''
def bind_template(out, session=None, store=zc.STORE, worktree=zc.WORKTREE) -> str:
    """Writes the store-local binding (exclusive create); `session` is ignored (C-53: the worker
    session is read at launch from the X6ZC_DISPATCH record). Returns the file's sha256."""
    text = BIND_TEMPLATE.replace("@WORKTREE@", str(Path(worktree))).replace(
        "@STORE@", str(Path(store)))
    return xwrite(out, text.encode("utf-8"))
def ledger_cpu(store) -> float:
    led = json.loads((Path(store) / "cpu_ledger.json").read_text("utf-8"))
    return float(led["cumulative_cpu_s"])
def pause_check(boundary, cumulative_s, stage_s, n=None) -> dict:
    P = C["budget"]["pause"]
    key = boundary if boundary != "C" else {1024: "C_1024", 2048: "C_2048"}.get(n, "C_any")
    if key == "C_any":
        (a, b), (s,) = (map(float, re.findall(r"[\d.]+", P[key][k]))
                        for k in ("cumulative", "stage"))
        cum, st = a + b * n, s * n
    else:
        cum, st = P[key]["cumulative"], P[key]["stage"]
    return {"pause": cumulative_s > cum or stage_s > st, "cumulative_threshold": cum,
            "stage_threshold": st, "boundary": key}

def _head() -> str:
    return subprocess.run(["git", "-C", zc.WORKTREE, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
def _frozen(store) -> dict:
    fz, au = (Path(store) / n for n in ("FREEZE.json", "AUTH.json"))
    if not (fz.exists() and au.exists()):
        raise RuntimeError("FREEZE.json and AUTH.json are required before stages A-C")
    f = json.loads(fz.read_text("utf-8"))
    if str(f.get("protocol_sha256", "")).lower() != _sha(zc.PROTOCOL_FILE.read_bytes()):
        raise RuntimeError("protocol sha256 differs from FREEZE.json")
    return f
