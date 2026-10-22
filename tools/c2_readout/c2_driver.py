"""C2 driver (API.md §12, §19.2-§19.3; C2-FROZEN-v2 §5.7, §7, §11): gate order, LogitPolicy,
sealing, records, lineage, release, G0, meter check, lazy stage dispatch, CLI. Gate bodies:
c2_stage_pre (S1-S3), c2_stage_val (S4), c2_stage_post (S5), helpers c2_stage_base (R-0104-1)."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c2_data as cd
import numpy as np
import stage_records as sr
from c1_records import C1GateFailure, classify_exception

GATE_ORDER = tuple("IMPL AUTH-ADMIT G0 PF H1 REG H2 H3 H4 H5 M0 C0c F1 C0v L1 R1 N2".split())
GATE_ORDER += tuple("SURVIVAL X1 V3x V3y Y1 Y1* Y2 P1 ACCEPT REG2 T-PRE T-PRE-MODEL".split())
GATE_ORDER += ("RESP-SPEC", "NUM", "ENDPOINT", "REPORT")
_ST = ("IMPL",) + ("S1",) * 9 + ("S2",) * 3 + ("S3",) * 5 + ("S4",) * 7 + ("ACCEPT",)
GATE_STAGE = dict(zip(GATE_ORDER, _ST + ("S5",) * 7))
STAGE_ENTRY = ("AUTH-ADMIT", "G0")
ALLOWED = {"m0": {"M0", "T-PRE"}, "x1": {"X1", "T-PRE"}, "val_sealed": {"P1"}}
ALLOWED["val_gate"] = {"V3x", "V3y", "Y1", "Y1*", "Y2"}
ALLOWED["test_endpoint"] = {"RESP-SPEC", "NUM", "ENDPOINT", "REPORT"}
OK = ("PASS", "NOT_RUN")
STATE_SHA = {"1729": "062d0a0aa71c41ad5afd9d3f76e58cf38a81419d629defcf2e3ac6316ffaf8f8"}
STATE_SHA["2718"] = "501d9c9ad80d4ffe272d7e03003cdee24b7fe3b25bed40e044f2111afd69aa5c"
STATE_SHA["3141"] = "197cccd6cf5491143171fe8ccd6ce79f71cb2f16995aa99af4e9dffe4bec94c8"  # §4
PREREQ = {"S1": None, "S2": "S1", "S3": "S2", "S4": "S3", "S5": "S4"}
APPEND, SKIP_DIRS = ("GATES.jsonl", "STAGES.jsonl"), ("manifests", "superseded")
OWNER, AUTH_KEYS = ("path", "sha256", "owner_verbatim", "granted_utc"), ("budget", "coordinator")
AUTH_KEYS += ("written_utc",)
STAGE_MODULE = {s: f"c2_stage_{m}" for s, m in zip(PREREQ, ("pre",) * 3 + ("val", "post"))}
StageRefused = sr.StageRefused
ALWAYS, META = ("REPORT",), ("status", "reason", "records", "model", "family", "problem", "scope")


# ---- the policy (§5.7, §7, NEW-2; API.md §12.1) ----------------------------------------------
class LogitPolicy:
    def __init__(self, done=()):
        self.done, self.current = list(dict.fromkeys(done)), None

    def begin(self, gate) -> None:
        pos = max((GATE_ORDER.index(g) for g in self.done if g in GATE_ORDER), default=-1)
        idx = GATE_ORDER.index(gate) if gate in GATE_ORDER else None
        ok = idx is not None and (idx == pos + 1 or idx == pos >= 0)
        if self.current is not None or not (ok or (gate in STAGE_ENTRY and gate in self.done)):
            raise C1GateFailure("FAIL_TECHNICAL", f"gate {gate} out of order ({self.current})")
        self.current = gate
        self.done += [] if gate in self.done else [gate]

    def end(self, gate) -> None:
        self.current = None

    def require(self, kind) -> None:
        tpre = kind != "test_endpoint" or {"T-PRE", "T-PRE-MODEL"} <= set(self.done)
        if self.current not in ALLOWED.get(kind, ()) or not tpre:
            raise C1GateFailure("FAIL_TECHNICAL", f"{kind} logits refused at {self.current}")

    def require_write(self, kind) -> None:
        if self.current in ("X1", "T-PRE") or self.current not in ALLOWED.get(kind, ()):
            raise C1GateFailure("INVALID/LEAKAGE", f"{kind} write refused at {self.current}")


def check_sequence(gates_jsonl) -> bool:
    pos, seen = -1, set()
    for rec in sr._lines(Path(gates_jsonl)):
        g = rec["gate"]
        if g in STAGE_ENTRY and g in seen:
            continue
        if g not in GATE_ORDER or GATE_ORDER.index(g) < pos:
            return False
        pos = GATE_ORDER.index(g)
        seen.add(g)
    return True


@dataclass
class Ctx:
    store: Path
    worktree: Path
    head: str
    job: str
    task_sha256: str
    session: str
    release: dict | None
    policy: LogitPolicy | None
    data: dict = field(default_factory=dict)


# ---- records (API.md §2 JSON, §15.1) ---------------------------------------------------------
def _js(v):
    if isinstance(v, dict):
        return {str(k): _js(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set)):
        return [_js(x) for x in (sorted(v) if isinstance(v, set) else v)]
    if isinstance(v, np.ndarray):
        return _js(v.tolist()) if v.size <= 64 else f"<array {list(v.shape)}>"
    if isinstance(v, np.generic):
        v = v.item()
    if isinstance(v, float) and not np.isfinite(v):
        return str(v)
    if isinstance(v, Fraction):
        return f"{v.numerator}/{v.denominator}"
    return str(v) if isinstance(v, (Decimal, Path)) else v


def run_gate(ctx, gate, fn, scope, model=None, family=None, problem=None) -> dict:
    """One GATES.jsonl line, or one per entry of res["records"] (API.md §19.2); an exception is
    classified and recorded with scope study. "stop": a study-scope line not PASS/NOT_RUN."""
    try:
        res = dict(fn() or {})
    except Exception as exc:  # noqa: BLE001  every failure is classified and recorded
        res, scope = dict(zip(("status", "reason"), classify_exception(exc))), "study"
    res["status"], stop = str(res.get("status", "PASS")), False
    for r in res.get("records") or [dict(res, model=model, family=family, problem=problem)]:
        full, sc = str(r.get("status", "PASS")), r.get("scope", scope)
        vals = r["values"] if "values" in r else {k: v for k, v in r.items() if k not in META}
        rec = {"full_status": full, "reason": r.get("reason"), "values": _js(vals), "scope": sc}
        rec.update({k: r.get(k) for k in ("model", "family", "problem")})
        sr.record_gate(ctx.store, gate, cc.status_of(full)[0], stage=ctx.data.get("stage"), **rec)
        stop = stop or (sc == "study" and full not in OK)
    return dict(res, stop=stop)


def _jr(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _eq(a, b) -> bool:
    return str(a).lower() == str(b).lower()


# ---- sealing (§5.7; API.md §12.4) ------------------------------------------------------------
def seal(ctx, name, arrays) -> str:
    ctx.policy.require_write("val_sealed")
    path = Path(ctx.store) / "sealed" / f"{name}.npz"
    rec = Path(ctx.store) / "stages" / "S4" / "SEALED.json"
    for d in (path.parent, rec.parent):
        d.mkdir(parents=True, exist_ok=True)
    sr.save_npz(path, **arrays)
    data = dict(_jr(rec) or {}, **{name: sr.sha256(path)})
    rec.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return data[name]


def unseal(ctx, name, sha256) -> dict:
    gates = sr.gates_so_far(ctx.store)
    study = any(g.get("scope") == "study" and g["status"] not in OK for g in gates)
    stops = [g for g in gates if g["gate"] == "ENDPOINT" or g["status"] not in OK]
    done = {g.get("family") for g in stops if g["gate"] == "ENDPOINT" or g.get("scope") == "family"}
    if not (study or set(cc.FAMILIES) <= done):
        raise RuntimeError("INVALID/LEAKAGE: sealed values before the fresh outcome")
    path = Path(ctx.store) / "sealed" / f"{name}.npz"
    if sr.sha256(path) != str(sha256).lower():
        raise RuntimeError("FAIL_TECHNICAL/LINEAGE: sealed file does not re-hash")
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def auth_ok(store) -> bool:
    a = _jr(Path(store) / "AUTH.json")
    try:
        o = a["owner_record"]
        ok = a["schema"] == "c2-auth-v1" and _eq(a["protocol_sha256"], cc.PROTOCOL_SHA256)
        ok = ok and bool(cc.AUTH_SHA256) and _eq(o["sha256"], cc.AUTH_SHA256)  # v2 AUTH bound
        return bool(ok and all(map(o.get, OWNER)) and all(map(a.get, AUTH_KEYS)))
    except (TypeError, KeyError, AttributeError):
        return False


def _release_why(ctx, stage, r) -> str:
    fz = Path(ctx.store) / "FREEZE.json"
    want = {"schema": "c2-release-v1", "job": ctx.job, "task_sha256": ctx.task_sha256}
    want.update(head=ctx.head, protocol_sha256=cc.PROTOCOL_SHA256)
    want["freeze_sha256"] = sr.sha256(fz) if fz.exists() else None
    bad = [k for k, v in want.items() if v is None or not _eq(r.get(k), v)]
    bad += [] if stage in (r.get("stages") or []) else ["stages"]
    if stage == "S5":
        p1 = _jr(Path(ctx.store) / "stages" / "S4" / "P1.json") or {}
        bad += [k for k in ("N_test", "k") if r.get(k) is None or r.get(k) != p1.get(k)]
        bad += [] if r.get("accept_review_sha256") else ["accept_review_sha256"]
    return ", ".join(bad)


def release_ok(ctx, stage) -> dict:
    k, why = int(str(stage)[1:]), ""
    for name in [f"RELEASE_R{k}.json"] + (["RELEASE_R3.json"] if k == 4 else []):
        r = _jr(Path(ctx.store) / name)
        why = _release_why(ctx, stage, r) if isinstance(r, dict) else f"{name} missing"
        if not why:
            return {"ok": True, "status": "PASS", "reason": name}
    return {"ok": False, "status": "REFUSED", "reason": why}


def meter_bind_check(path, expected_sha256, import_dir) -> None:
    if sr.sha256(path) != str(expected_sha256).lower():
        raise RuntimeError(f"meter binding {path} sha256 differs from FREEZE.json")
    want = (Path(cc.WORKTREE) / "tools" / "x4_oracle_profile").resolve()
    if Path(import_dir).resolve() != want:
        raise RuntimeError(f"meter import directory {import_dir} is not {want}")


# ---- G0 and PF (§7 rows 1-2; API.md §12.3) ---------------------------------------------------
def _blob(wt, head, rel) -> str:
    cmd = ["git", "-C", str(wt), "show", f"{head}:{rel}"]
    return hashlib.sha256(subprocess.run(cmd, capture_output=True, check=True).stdout).hexdigest()


def _item(fn) -> dict:
    try:
        return {"status": "PASS" if fn() else "FAIL", "detail": ""}
    except Exception as exc:  # noqa: BLE001  a failed check is a failed item (E-25)
        return {"status": "FAIL", "detail": repr(exc)}


def g0(ctx, stage=None) -> dict:
    """Items (i)-(viii), never raising (E-25); LINEAGE iff only (vi)-(vii) fail (R-0100-2)."""
    S, H, P = cd.file_sha, cc.CONTRACT["hashes"], cc.PROTOCOL_SHA256
    wt, store = Path(ctx.worktree), Path(ctx.store)
    stage, fz = stage or ctx.data.get("stage"), _jr(store / "FREEZE.json") or {}
    pkg, lin = wt / "tools" / "c2_readout", recognised(store)
    proto, c2c = pkg / Path(cc.PROTOCOL_FILE).name, pkg / "CONTRACT.json"
    mail = Path(cc.PROJECT_ROOT) / cc.CONTRACT["protocol"]["mailbox_file"]  # R-0105-1
    iv = ((cc.K4_FREEZE, H["k4_freeze"]),)
    iv += ((pkg.parent / "c1prime" / "CONTRACT.json", H["c1prime_contract"]),)
    pins = {f"tools/c2_readout/{p.name}": S(p) for p in pkg.glob("*") if p.is_file()}
    blobs = {**H["reused_blobs"], **H["reused_extra"]}
    charts = {Path(cc.C1P_STORE) / Path(p).name: s for p, s in H["charts"].items()}
    task = Path(cc.MAILBOX) / "jobs" / str(ctx.job) / "task.md"
    mb, mdir = (store / "c2_meter_bind.py", fz.get("meter_bind_sha256")), pkg.parent

    def viii():
        ok = _eq(S(task), ctx.task_sha256) and bool(ctx.session)
        ok = ok and release_ok(ctx, stage or "S1")["ok"]
        meter_bind_check(*mb, mdir / "x4_oracle_profile")
        return ok and Path(cc.__file__).resolve().parent == pkg.resolve()

    out = {"i": _item(lambda: S(proto) == P and proto.read_bytes() == mail.read_bytes())}
    state_ok = H["state_sha_f32"] == STATE_SHA
    out["ii"] = _item(lambda: _eq(S(c2c), fz.get("contract_sha256")) and state_ok)
    out["iii"] = _item(lambda: all(_blob(wt, ctx.head, p) == s for p, s in blobs.items()))
    out["iv"] = _item(lambda: all(S(p) == s for p, s in iv))
    out["v"] = _item(lambda: all(S(p) == s for p, s in charts.items()))
    out["vi"] = _item(lambda: cd.namespace_scan(cc.PROJECT_ROOT, pins, lin)["status"] == "PASS")
    out["vii"] = _item(lambda: cd.store_admission(store, lin, stage == "S1")["status"] == "PASS")
    out["viii"] = _item(viii)
    bad = [k for k, v in out.items() if v["status"] != "PASS"]
    cls = "LINEAGE" if bad and set(bad) <= {"vi", "vii"} else "AUTHORITY"
    out["status"] = f"FAIL_TECHNICAL/{cls}" if bad else "PASS"
    return out


def _skip(rel) -> bool:
    coord = rel in ("FREEZE.json", "AUTH.json", "c2_meter_bind.py") or rel.startswith("RELEASE_R")
    return rel in APPEND or cd._meter_file(rel) or rel.split("/")[0] in SKIP_DIRS or coord


def write_manifest(ctx, stage) -> Path:
    store = Path(ctx.store)
    path = store / "manifests" / f"{ctx.job}.json"
    if path.exists():
        raise FileExistsError(path)
    files = {cd._rel(f, store): cd.file_sha(f) for f in cd._walk(store)}
    man = {"schema": "c2-manifest-v1", "job": ctx.job, "stage": stage, "head": ctx.head}
    man["files"] = {k: v for k, v in files.items() if not _skip(k)}
    man.update(append_only={k: files[k] for k in APPEND if k in files}, utc=sr._utc())
    path.parent.mkdir(parents=True, exist_ok=True)
    sr.write_new(path, man)
    return path


def recognised(store) -> dict:
    store, out, app = Path(store), {}, {}
    schema = {"FREEZE.json": "c2-freeze-v1", "AUTH.json": "c2-auth-v1"}
    for p in [store / "FREEZE.json", store / "AUTH.json"] + sorted(store.glob("RELEASE_R*.json")):
        r = _jr(p)
        if isinstance(r, dict) and r.get("schema") == schema.get(p.name, "c2-release-v1"):
            ok = _eq(r.get("protocol_sha256"), cc.PROTOCOL_SHA256)
            out.update({p.name: sr.sha256(p)} if ok else {})
    mb, fz = store / "c2_meter_bind.py", _jr(store / "FREEZE.json") or {}
    if mb.exists() and _eq(sr.sha256(mb), fz.get("meter_bind_sha256")):
        out[mb.name] = sr.sha256(mb)
    for acc in sorted(store.glob("manifests/*.accepted.json")):
        a = _jr(acc) or {}
        man = store / "manifests" / f"{a.get('job')}.json"
        if man.exists() and _eq(sr.sha256(man), a.get("manifest_sha256")):
            m = _jr(man)
            out.update(m["files"], **{f"manifests/{man.name}": sr.sha256(man)})
            out[f"manifests/{acc.name}"], app = sr.sha256(acc), m.get("append_only", {})
    out.update(app)
    for sums in sorted(store.glob("superseded/*/SHA256SUMS")):
        d = sums.parent.relative_to(store).as_posix()
        for line in sums.read_text(encoding="utf-8").splitlines():
            sha, _, rel = line.partition("  ")
            out[f"{d}/{rel}"] = sha
        for p in (sums, sums.parent / "SUPERSEDED.json"):
            out.update({f"{d}/{p.name}": sr.sha256(p)} if p.exists() else {})
    return out


def supersede(ctx, job, attempt, paths, ruling) -> Path:
    store = Path(ctx.store)
    dest = store / "superseded" / f"{job}-a{int(attempt)}"
    dest.mkdir(parents=True, exist_ok=False)
    lines = []
    for rel in paths:
        lines.append(f"{sr.sha256(store / rel)}  {rel}")
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        os.replace(store / rel, dest / rel)
    with (dest / "SHA256SUMS").open("x", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    rec = {k: ruling.get(k) for k in ("defect", "ruling_path", "ruling_sha256")}
    sr.write_new(dest / "SUPERSEDED.json", dict(rec, job=job, attempt=int(attempt), moved=paths))
    return dest


def regen_compare(ctx, path, archived_sha256) -> bool:
    return _eq(sr.sha256(path), archived_sha256)


def begin_stage(ctx, stage) -> None:
    store, stages, gates = Path(ctx.store), sr.stages_so_far(ctx.store), sr.gates_so_far(ctx.store)
    rel, prior = release_ok(ctx, stage), PREREQ[stage]
    done = [r for r in stages if r["stage"] == prior and r["event"] == "COMPLETED"]
    stop = any(g.get("scope") == "study" and g["status"] not in OK for g in gates)
    checks = ((any(r["stage"] == stage for r in stages), "stage already attempted"),)
    checks += ((not auth_ok(store), "AUTH-ADMIT: no valid AUTH.json"),)
    checks += ((not rel["ok"], f"release: {rel['reason']}"), (stop, "prior study-scope stop"))
    checks += ((prior and not done, f"prerequisite {prior} not completed"),)
    why = [w for c, w in checks if c]
    for n, s in done[-1]["evidence"].items() if done else ():
        why += [] if (store / n).exists() and sr.sha256(store / n) == s else [f"{n} changed"]
    if why:
        sr.refuse(store, stage, "; ".join(why), integrity=any("changed" in w for w in why))
    sr._append(store / "STAGES.jsonl", {"stage": stage, "event": "STARTED", "utc": sr._utc()})


def complete_stage(ctx, stage, files) -> None:
    sr.complete(ctx.store, stage, files)


def run_stage(stage, ctx) -> dict:
    """Lazy dispatch (API.md §19.2-§19.3): PLAN steps in order; NOT_RUN after a study stop."""
    if stage not in PREREQ:
        raise ValueError(f"unknown stage {stage}")
    plan = importlib.import_module(STAGE_MODULE[stage]).PLAN[stage]
    begin_stage(ctx, stage)
    ctx.release, ctx.data["stage"] = release_ok(ctx, stage), stage
    ctx.policy = LogitPolicy(done=[g["gate"] for g in sr.gates_so_far(ctx.store)])
    stopped, seen = None, {}
    for gate, fn, scope in plan:
        run = fn if stopped is None or gate in ALWAYS else (lambda c: {"status": "NOT_RUN"})
        ctx.policy.begin(gate)
        try:
            res = run_gate(ctx, gate, lambda: run(ctx), scope)
        finally:
            ctx.policy.end(gate)
        seen[gate], stopped = res["status"], stopped or (gate if res["stop"] else None)
    rel, ctx.data["stopped"] = f"stages/{stage}/record.json", stopped
    (Path(ctx.store) / rel).parent.mkdir(parents=True, exist_ok=True)
    sr.write_new(Path(ctx.store) / rel, _js({"stage": stage, "gates": seen, "stopped": stopped}))
    complete_stage(ctx, stage, ctx.data.setdefault("files", []) + [rel])
    write_manifest(ctx, stage)
    return {"stage": stage, "stopped": stopped}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="c2_driver")
    ap.add_argument("stage", choices=sorted(PREREQ))
    for opt in ("--store", "--job", "--task-sha256", "--session"):
        ap.add_argument(opt, required=True)
    a = ap.parse_args(argv)
    wt = Path(__file__).resolve().parents[2]
    git = subprocess.run(["git", "-C", str(wt), "rev-parse", "HEAD"], capture_output=1, text=1)
    ctx = Ctx(Path(a.store), wt, git.stdout.strip(), a.job, a.task_sha256, a.session, None, None)
    try:
        res = run_stage(a.stage, ctx)
    except StageRefused as exc:
        print(exc, file=sys.stderr)
        return 3
    return 2 if res.get("stopped") else 0


if __name__ == "__main__":
    raise SystemExit(main())
