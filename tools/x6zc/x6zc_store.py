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
BIND_TEMPLATE = '''"""x6zc-store meter binding (BIND_TEMPLATE of tools/x6zc/x6zc_run.py): the
project meter, unchanged, with its store globals rebound to x6zc-store (--max-cpu inf)."""
import sys
from pathlib import Path
IMPORT_DIR, STORE = r"{import_dir}", Path(r"{store}")
sys.path.insert(0, IMPORT_DIR)
import meter  # noqa: E402
meter.OUT, meter.LEDGER = STORE, STORE / "cpu_ledger.json"
meter.EMERGENCY, meter.LOCK = STORE / "cpu_ledger.emergency.jsonl", STORE / "RUN.lock"
meter.ACTIVE, meter.LOG_DIR = STORE / "METER_ACTIVE.lock", STORE / "logs"
meter.WORKER_SESSION = r"{session}"
if __name__ == "__main__":
    sys.exit(meter.main())
'''
def bind_template(out, session, store=zc.STORE, import_dir=zc.METER_IMPORT_DIR) -> str:
    return xwrite(out, BIND_TEMPLATE.format(import_dir=import_dir, store=store,
                                            session=session).encode("utf-8"))
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
