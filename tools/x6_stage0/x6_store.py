"""X6 stage 0: labels and outcome (D), S0, store lineage, archive and compare, canonical JSON,
per-gate records and the preflight record (X6-FROZEN-v1 sections 8.1, 8.3-8.5, 10.5, 10.8;
API.md 6.2-6.5, 7 choice 21). Moved unchanged in behaviour from x6_run.py (coordinator
addendum 1, ruling X5); x6_run re-exports every moved name."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

import x6_model as xm
import x6_dp as xd
import x6_exact as xe
from x6_model import G_MIN

MAILBOX = Path("X:/Downloads/projects/topo-pilot/agent-handoff")
ORDER = ("PF", "S0", "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7")
GATES = ("G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "D")
OUTCOMES = ("GO_X6_NATURAL", "GO_X6_CHALLENGE_ONLY", "INCONCLUSIVE_NATURAL", "STOP_X6", "WITHHELD")
G7_ITEMS = ("AB.spread", "AB.ambiguity", "AB.G_S", "AB.D_blk", "AB.filter", "ZC.spread",
            "ZC.ambiguity", "ZC.G_S", "ZC.D_blk", "ZC.filter", "TRIV.spread", "TRIV.G_S",
            "TRIV.D_blk", "TRIV.filter", "ETA1.cue_uniform", "ETA1.G_S", "ETA1.filter",
            "GAUGE-NA.filter", "GAUGE-NA.exact", "GAUGE-TRIV.filter", "GAUGE-TRIV.noncommuting",
            "GAUGE-COV.filter", "GAUGE-COV.exact", "NOCUE", "TOKPERM", "FIXED-POINT",
            "SAME-HOLONOMY")
G7_DP_ITEMS = ("AB.ambiguity", "AB.G_S", "AB.D_blk", "ZC.ambiguity", "ZC.G_S", "ZC.D_blk",
               "TRIV.G_S", "TRIV.D_blk", "ETA1.G_S", "FIXED-POINT")
S8_NOT_RUN = ("G6",) + G7_DP_ITEMS
PF_SUITES = ("tests/world", "tests/process", "tests/oracle", "tests/oracle_profile",
             "tests/dataset", "tests/d1_seam", "tests/x2a_stage0")
PROTECTED_PATHS = ("src", "tools/x4_oracle_profile", "tools/d1_seam", "tools/x2a_stage0",
                   "tools/check_file_sizes.py", "tools/x6_stage0") + PF_SUITES[:4] + (
                   "tests/dataset", "tests/d1_seam", "tests/x2a_stage0", "tests/x6_stage0",
                   "pyproject.toml")
ALLOWLIST = tuple(f"tools/x6_stage0/{f}" for f in ("API.md", "x6_model.py", "x6_exact.py",
                                                  "x6_run.py", "x6_dp.py", "x6_store.py")) + tuple(
    f"tests/x6_stage0/{f}" for f in ("test_x6_stage0.py", "test_x6_stage0_dp.py", "AUTHORSHIP.md"))
KERNEL_DIFF_EXPECTED = ("A\tsrc/topo_pilot/learner/multihorizon.py",
                        "M\tsrc/topo_pilot/learner/trainer.py")
METER_FILES = ("x6_meter_bind.py", "cpu_ledger.json", "cpu_ledger.json.tmp",
               "cpu_ledger.emergency.jsonl", "RUN.lock", "METER_ACTIVE.lock")
ATTEMPT_RE = r"^\d{4}-a[1-9]\d*$"
VOLATILE_KEYS = frozenset({"cpu_s", "wall_s", "utc", "started_utc", "finished_utc", "timestamp",
                           "path", "out_dir", "store", "worktree", "tempdir", "basetemp"})

# ---- labels and outcome (API 6.2, sections 8.3-8.5) ----
def decide(statuses, o1, o2, s8=None) -> dict:
    s8_mode = False
    for g in ORDER:
        s, fail = statuses[g], None
        if g in ("PF", "S0") and s != "PASS":
            fail = "INVALID"
        elif g == "G4" and s == "RESOURCE_LIMIT":
            s8_mode, fail = True, None if s8 and s8["completed_checks_pass"] else "FAIL"
        elif s in ("INVALID", "FAIL") or (s == "NOT_RUN" and not (s8_mode and g == "G6")):
            fail = "INVALID" if s == "NOT_RUN" else s
        if fail:
            return {"verdict": fail, "first_failed": g, "outcome": "WITHHELD",
                    "window_clause": False, "not_run": list(ORDER[ORDER.index(g) + 1:]) + ["D"]}
    if s8_mode:
        return {"verdict": "RESOURCE_LIMIT", "first_failed": None, "not_run": list(S8_NOT_RUN),
                "outcome": "INCONCLUSIVE_NATURAL" if o1 else "STOP_X6",
                "window_clause": bool(o1 and s8["theorem4"])}
    outcome = "STOP_X6" if not o1 else {"PASS": "GO_X6_NATURAL", "FAIL": "GO_X6_CHALLENGE_ONLY",
                                        "UNCERTIFIED": "INCONCLUSIVE_NATURAL"}[o2]
    return {"verdict": "PASS", "first_failed": None, "outcome": outcome,
            "window_clause": outcome != "STOP_X6", "not_run": []}

def label_cert(cert: str, yes: str, no: str) -> str:
    return yes if cert == "PASS" else no if cert == "FAIL" else "UNRESOLVED"
def labels(g3, g4, poe_values) -> dict:
    na, bt, cert = g4["natural"]["NA"], g3["beta"], lambda e: xd.certify(e, G_MIN)  # noqa: E731
    j8, gp = na["J"][8][32], na["G"]["Parikh"][32]
    p1 = ("LONG_HISTORY" if Fraction(j8["hi"]) <= Fraction(gp["lo"]) / 2 else
          "SHORT_HISTORY" if Fraction(j8["lo"]) > Fraction(gp["hi"]) / 2 else "UNRESOLVED")
    blk = label_cert(cert(g4["kblk"]["NA"]["D_blk"]), "BLOCK_ORDER_NEEDED", "BLOCK_ORDER_SMALL")
    return {"P1_link": p1, "BLOCK": "BLOCK_UNRESOLVED" if blk == "UNRESOLVED" else blk,
            "INCENTIVE": label_cert(cert(na["mean_G_parikh"]), "ABOVE", "BELOW"),
            "HEADROOM": label_cert(cert(na["G_k"][8][32]), "HEADROOM", "NO_HEADROOM"),
            "PoE": poe_values, "FAMILY": {f: {"label": xe.family_label(r), "balanced_beta": {
                k: c["balanced"] for k, c in r.items()} if f == "W3" else None}
                for f, r in bt.items()}}

# ---- S0 (API 6.3, section 8.1) ----
def _git(wt, *args) -> list:
    out = subprocess.run(["git", "-C", str(wt), *args], capture_output=True, text=True, check=True)
    return [ln for ln in out.stdout.splitlines() if ln.strip()]
def allowlist_ok(lines) -> bool: return all(ln[:2] == "A\t" and ln[2:] in ALLOWLIST for ln in lines)
def kernel_diff_ok(lines) -> bool:
    return len(lines) == len(set(lines)) and set(lines) == set(KERNEL_DIFF_EXPECTED)
def _norm(p) -> str: return os.path.normcase(os.path.abspath(str(p))).lower()
def s0_check(worktree, head, store, dispatch) -> dict:
    wt, store = Path(worktree), Path(store)
    disp = dispatch if isinstance(dispatch, dict) else _load(dispatch)
    bind, lin = store / "x6_meter_bind.py", s0_lineage(store)
    diff = _git(wt, "diff", "--no-renames", "--name-status", xm.R_COMMIT, head, "--",
                *PROTECTED_PATHS)
    kdiff = _git(wt, "diff", "--no-renames", "--name-status", xm.KERNEL_BASE, head, "--", "src",
                 "tools/x4_oracle_profile", "tests/oracle_profile")
    sha = lambda p: sha256_file(p).upper()  # noqa: E731
    items = {"1": sha(wt / "docs/x6/PROTOCOL_X6_v1.md") == xm.PROTOCOL_SHA256 ==
             sha(MAILBOX / "planning/responses/X6-FROZEN-v1.md"),
             "2": sha(MAILBOX / "planning/requests/coord-x6-stage0-20261015.md") ==
             xm.REQUEST_SHA256,
             "3": allowlist_ok(diff), "4": kernel_diff_ok(kdiff), "6": lin["status"] == "PASS",
             "5": bind.is_file() and str(disp.get("meter_bind_sha256")).upper() == sha(bind) and
             _norm(disp.get("meter_import_dir", "?")) == _norm(wt / "tools" / "x4_oracle_profile")}
    return {"status": "PASS" if all(items.values()) else "INVALID", "diff": diff,
            "items": dict(sorted(items.items())), "kernel_diff": kdiff, "lineage": lin}

# ---- store, lineage and per-gate records (API 6.4, section 10.8) ----
def sha256_file(path) -> str: return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_manifest(attempt_dir) -> Path:
    d = Path(attempt_dir)
    man = d / "SHA256SUMS"
    files = sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file() and p != man)
    man.write_bytes("".join(f"{sha256_file(d / f)}  {f}\n" for f in files).encode("ascii"))
    return man
def read_manifest(path) -> dict:
    lines = Path(path).read_bytes().decode("ascii").splitlines()
    return {rel: h.lower() for h, rel in (ln.split("  ", 1) for ln in lines if ln.strip())}
def _lineage(store, s0: bool) -> dict:
    store, listed, sums = Path(store), {}, set()
    run_dir, sup = store / "run", store / "superseded"
    out = {"status": "PASS", "run_absent": not run_dir.exists(), "attempts": [], "unrecognised": [],
           "missing": [], "mismatch": []}
    for d in sorted(sup.iterdir()) if sup.is_dir() else ():
        if d.is_dir() and re.match(ATTEMPT_RE, d.name) and (d / "SHA256SUMS").is_file():
            out["attempts"].append(d.name)
            sums.add(f"superseded/{d.name}/SHA256SUMS")
            listed.update({f"superseded/{d.name}/{r}": h
                           for r, h in read_manifest(d / "SHA256SUMS").items()})
    for p in sorted(store.rglob("*")) if store.is_dir() else ():
        rel = p.relative_to(store).as_posix()
        known = rel in METER_FILES or rel[:5] == "logs/" or rel in sums or rel in listed
        if p.is_file() and not known and not (s0 and rel[:4] == "run/"):
            out["unrecognised"].append(rel)
    for rel, h in sorted(listed.items()):
        if not (store / rel).is_file():
            out["missing"].append(rel)
        elif sha256_file(store / rel) != h:
            out["mismatch"].append(rel)
    bad = bool(out["unrecognised"] or out["missing"] or out["mismatch"])
    if s0:
        out["run_contents"] = sorted(p.name for p in run_dir.iterdir()) if run_dir.is_dir() else []
        bad |= out["run_contents"] != ["preflight.json"]
        bad |= not (run_dir / "preflight.json").is_file()
    out["status"] = "INVALID/LINEAGE" if bad or not (s0 or out["run_absent"]) else "PASS"
    return out
def lineage_precheck(store) -> dict: return _lineage(store, s0=False)
def s0_lineage(store) -> dict: return _lineage(store, s0=True)

def archive_attempt(store, job: str, ledger_entries=(), logs=()) -> Path:
    store, k = Path(store), 1
    if not (store / "run").is_dir():
        raise FileNotFoundError(store / "run")
    while (store / "superseded" / f"{job}-a{k}").exists():
        k += 1
    dest = store / "superseded" / f"{job}-a{k}"
    dest.mkdir(parents=True)
    shutil.move(str(store / "run"), str(dest / "run"))
    (dest / "ledger_entries.json").write_bytes(canonical_json(list(ledger_entries)))
    for p in logs:
        (dest / "logs").mkdir(exist_ok=True)
        shutil.copy2(p, dest / "logs" / Path(p).name)
    write_manifest(dest)
    return dest
def compare_attempt(attempt_dir, run_dir, affected=()) -> dict:
    out = {"status": "PASS", "compared": [], "mismatch": [], "missing": []}
    for rel, h in sorted(read_manifest(Path(attempt_dir) / "SHA256SUMS").items()):
        parts = rel.split("/")
        if len(parts) == 4 and parts[:2] == ["run", "gates"] and parts[2] not in affected:
            f = Path(run_dir) / "gates" / parts[2] / parts[3]
            out["compared" if f.is_file() else "missing"].append(rel)
            if f.is_file() and sha256_file(f) != h:
                out["mismatch"].append(rel)
    out["status"] = "INVALID/LINEAGE" if out["mismatch"] else "PASS"
    return out

def _key(k) -> str: return ",".join(str(p) for p in k) if isinstance(k, tuple) else str(k)
def jsonable(obj):
    if isinstance(obj, (Fraction, Decimal)):
        return str(obj)
    if isinstance(obj, dict):
        return {_key(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set, frozenset, np.ndarray)):
        vals = [jsonable(v) for v in (obj.tolist() if isinstance(obj, np.ndarray) else obj)]
        return sorted(vals, key=str) if isinstance(obj, (set, frozenset)) else vals
    return obj.item() if isinstance(obj, np.generic) else obj
def canonical_json(obj) -> bytes:
    out = json.dumps(jsonable(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return out.encode("ascii")
def _volatile(k) -> bool:
    return isinstance(k, str) and (k in VOLATILE_KEYS or k.endswith(("_utc", "_path", "_dir")))
def strip_volatile(obj):
    if isinstance(obj, dict):
        return {k: strip_volatile(v) for k, v in obj.items() if not _volatile(k)}
    return type(obj)(map(strip_volatile, obj)) if isinstance(obj, (list, tuple)) else obj
def reports_equal(a, b) -> bool: return jsonable(strip_volatile(a)) == jsonable(strip_volatile(b))
def write_marker(run_dir, gate: str) -> None:
    if gate not in GATES:
        raise ValueError(gate)
    (Path(run_dir) / "gates" / gate).mkdir(parents=True, exist_ok=True)
    Path(run_dir, "gates", gate, "STARTED").open("xb").close()
def write_gate(run_dir, gate: str, status: str, values) -> dict:
    d, files = Path(run_dir) / "gates" / gate, {}
    if gate in GATES:
        with open(d / "values.json", "xb") as fh:
            fh.write(canonical_json(strip_volatile(values)))
        files = {name: sha256_file(d / name) for name in ("STARTED", "values.json")}
    elif gate not in ("PF", "S0"):
        raise ValueError(gate)
    rec = {"gate": gate, "status": status, "files": files}
    with open(Path(run_dir) / "GATES.jsonl", "ab") as fh:
        fh.write(canonical_json(rec) + b"\n")
    return rec

# ---- preflight records (API 6.5) ----
def _load(path) -> dict: return json.loads(Path(path).read_text(encoding="utf-8-sig"))
def scratch_ok(path, job) -> bool:
    return _norm(path).startswith(_norm(Path(xm.SCRATCH_ROOT) / str(job)) + os.sep)
def write_preflight(store, record: dict) -> dict:
    pre, r, job = lineage_precheck(store), record, str(record.get("job"))
    if pre["status"] != "PASS":
        return {"status": "INVALID", "lineage_precheck": pre}
    ok = r["head"] == r["head_expected"] and r["porcelain"] == []
    ok &= set(r["suites"]) == set(PF_SUITES)
    ok &= scratch_ok(r["tempdir"], job) and scratch_ok(r["basetemp"], job) and r["new_tests"] == 0
    ok &= r["file_sizes"] == 0 and all(c == 0 for c in r["suites"].values())
    out = {**record, "lineage_precheck": pre, "status": "PASS" if ok else "INVALID"}
    (Path(store) / "run").mkdir(parents=True)
    with open(Path(store) / "run" / "preflight.json", "xb") as fh:
        fh.write(canonical_json(out))
    return out
def _typed(obj):
    if isinstance(obj, Fraction):
        return {"type": "exact", "value": str(obj)}
    if isinstance(obj, dict):
        typed = obj.get("type") in ("enclosure", "mc", "float", "resource")
        return obj if typed else {k: _typed(v) for k, v in obj.items()}
    return [_typed(v) for v in obj] if isinstance(obj, (list, tuple)) else obj
