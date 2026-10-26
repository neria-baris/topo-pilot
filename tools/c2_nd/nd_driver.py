"""C2ND driver (API.md §9, §14, §15, §20; C2ND-DESIGN-v1 §3, §6.7, §10, §12): gate order, the ND
LogitPolicy, records, sealing, AUTH and release binding, G0 (i)-(x), the meter check, lazy stage
dispatch (no stage module at import time) and the CLI. Loaders, caches and lineage records live
in nd_stage_base (ND-C43) and are re-exported here under their API.md §9 names."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c2_config as cc
import c2_data as cd
import nd_data as nda
import nd_registry as nrg
import nd_stage_base as nsb
import stage_records as sr
from c1_records import C1GateFailure, classify_exception

GATE_ORDER = tuple(nc.CONTRACT["gate_order"])
_ST = ("IMPL",) + ("S1",) * 10 + ("S2",) * 4 + ("S3",) * 5 + ("S4",) * 11 + ("ACCEPT",)
GATE_STAGE = dict(zip(GATE_ORDER, _ST + ("S5",) * 7))
STAGE_ENTRY, IDENTITY_GATES, OK = ("AUTH-ADMIT", "G0"), ("X1", "DX", "T-PRE"), ("PASS", "NOT_RUN")
RELEASE_ONLY, RELEASE_KEYS = tuple(nc.CONTRACT["release_pass_fail_only"]), ("result", "cases")
ALLOWED = {"m0": {"M0", "M0-D", "T-PRE"}, "x1": {"X1", "T-PRE"}, "dx": {"DX", "T-PRE"}}
ALLOWED.update(val_gate={"V3x", "V3y", "Y1", "V3x'", "Y1'", "V3x'-g1"}, val_kc={"KC", "KC-R"})
ALLOWED.update(val_sealed={"P1"}, construction={"M0-D", "F1", "DX", "T-PRE"})
ALLOWED["test_endpoint"] = {"RESP-SPEC", "NUM", "ENDPOINT", "REPORT"}
STATE_SHA = {"1729": "062d0a0aa71c41ad5afd9d3f76e58cf38a81419d629defcf2e3ac6316ffaf8f8"}
STATE_SHA["2718"] = "501d9c9ad80d4ffe272d7e03003cdee24b7fe3b25bed40e044f2111afd69aa5c"
STATE_SHA["3141"] = "197cccd6cf5491143171fe8ccd6ce79f71cb2f16995aa99af4e9dffe4bec94c8"  # §2.1
PREREQ = {"S1": None, "S2": "S1", "S3": "S2", "S4": "S3", "S5": "S4"}
STAGE_MODULE = {"S1": "nd_stage_pre", "S2": "nd_stage_pre", "S3": "nd_stage_pre"}
STAGE_MODULE.update(S4="nd_stage_val", S5="nd_stage_post")
SCHEMA, _js, _jr, _eq, _sha_ok, _npz = nsb.SCHEMA, nsb._js, nsb._jr, nsb._eq, nsb._sha_ok, nsb._npz
cache, npz, js, c2npz, c2js, c2_store, c2_rehash = (
    nsb.cache,
    nsb.npz,
    nsb.js,
    nsb.c2npz,
    nsb.c2js,
    nsb.c2_store,
    nsb.c2_rehash,
)
recognised, write_manifest, supersede = nsb.recognised, nsb.write_manifest, nsb.supersede
regen_compare, manifest_stem = nsb.regen_compare, nsb.manifest_stem
OWNER, AUTH_KEYS = ("path", "sha256", "owner_verbatim", "granted_utc"), ("budget", "coordinator")
AUTH_KEYS += ("written_utc",)
META = ("status", "reason", "records", "model", "family", "problem", "scope", "decoy")
StageRefused = sr.StageRefused


# ---- the policy (§3, §6.7; API.md §9.1, §20 B-3) ---------------------------------------------
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
            raise C1GateFailure("FAIL_TECHNICAL", f"{kind} refused at {self.current}")

    def require_write(self, kind) -> None:
        if self.current in IDENTITY_GATES or self.current not in ALLOWED.get(kind, ()):
            raise C1GateFailure("INVALID/LEAKAGE", f"{kind} write refused at {self.current}")

    def require_release(self, gate, values) -> None:
        extra = set(values or {}) - set(RELEASE_KEYS + ("model",)) if gate in RELEASE_ONLY else 0
        if extra:
            raise C1GateFailure("INVALID/LEAKAGE", f"{gate} releases PASS/FAIL only: {extra}")


def require_release(policy, gate, values) -> None:
    (policy or LogitPolicy()).require_release(gate, values)


def check_sequence(gates_jsonl) -> bool:
    pos, seen = -1, set()
    for g in (r["gate"] for r in sr._lines(Path(gates_jsonl))):
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
    release: dict | None = None
    policy: LogitPolicy | None = None
    data: dict = field(default_factory=dict)
    dry: bool = False


# ---- records (API.md §14.1) ------------------------------------------------------------------
def run_gate(ctx, gate, fn, scope, model=None, family=None, problem=None) -> dict:
    """One GATES.jsonl line per record (C2 API §19.2) plus the key `decoy`; a release-only gate
    carrying any value beyond PASS/FAIL is recorded INVALID/LEAKAGE instead (T-SEAL-ND)."""
    try:
        res = dict(fn() or {})
    except Exception as exc:  # noqa: BLE001  every failure is classified and recorded
        res, scope = dict(zip(("status", "reason"), classify_exception(exc))), "study"
    res["status"], stop = str(res.get("status", "PASS")), False
    for r in res.get("records") or [dict(res, model=model, family=family, problem=problem)]:
        full, sc = str(r.get("status", "PASS")), r.get("scope", scope)
        vals = r["values"] if "values" in r else {k: v for k, v in r.items() if k not in META}
        try:
            require_release(ctx.policy, gate, vals)
        except C1GateFailure as exc:
            full, sc, vals = exc.status, "study", {"refused": str(exc)}
        rec = {"full_status": full, "reason": r.get("reason"), "values": _js(vals), "scope": sc}
        rec.update({k: r.get(k) for k in ("model", "family", "problem", "decoy")})
        sr.record_gate(ctx.store, gate, cc.status_of(full)[0], stage=ctx.data.get("stage"), **rec)
        stop = stop or (sc == "study" and full not in OK)
    return dict(res, stop=stop)


# ---- sealing (§6.7 L5; API.md §9.4) ----------------------------------------------------------
def seal(ctx, name, arrays) -> str:
    ctx.policy.require_write("val_sealed")
    path, rec = (
        Path(ctx.store) / "sealed" / f"{name}.npz",
        Path(ctx.store) / "stages/S4/SEALED.json",
    )
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
    if not (study or set(nc.FAMILIES) <= done):
        raise RuntimeError("INVALID/LEAKAGE: sealed values before the fresh outcome")
    path = Path(ctx.store) / "sealed" / f"{name}.npz"
    if sr.sha256(path) != str(sha256).lower():
        raise RuntimeError("FAIL_TECHNICAL/LINEAGE: sealed file does not re-hash")
    return _npz(path)


# ---- AUTH, the binding record, release, meter (API.md §9.3, §9.6, §9.8) -----------------------
def auth_ok(store, name="AUTH.json") -> bool:
    a = _jr(Path(store) / name)
    try:
        o = a["owner_record"]
        ok = a["schema"] == SCHEMA[name] and _eq(a["protocol_sha256"], nc.PROTOCOL_SHA256)
        ok = ok and bool(nc.AUTH_SHA256) and _eq(o["sha256"], nc.AUTH_SHA256)
        return bool(ok and all(map(o.get, OWNER)) and all(map(a.get, AUTH_KEYS)))
    except (TypeError, KeyError, AttributeError):
        return False


def is_dry_store(store) -> bool:
    """A FREEZE-free scratch store under SCRATCH_ROOT holding a valid AUTH_IMPL.json (§10.1)."""
    store = Path(store).resolve()
    under = Path(nc.SCRATCH_ROOT).resolve() in store.parents
    return under and not (store / "FREEZE.json").exists() and auth_ok(store, "AUTH_IMPL.json")


def binding_path(ctx) -> Path:
    """FREEZE.json; in a dry-run store DRY.json (H, contract and meter bindings, ND-C42)."""
    return Path(ctx.store) / ("DRY.json" if ctx.dry else "FREEZE.json")


def _release_why(ctx, stage, r) -> str:
    fz = binding_path(ctx)
    want = {"schema": "c2nd-release-v1", "job": ctx.job, "task_sha256": ctx.task_sha256}
    want.update(head=ctx.head, protocol_sha256=nc.PROTOCOL_SHA256)
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
        raise RuntimeError(f"meter binding {path} sha256 differs from the binding record")
    want = (Path(nc.WORKTREE) / "tools" / "x4_oracle_profile").resolve()
    if Path(import_dir).resolve() != want:
        raise RuntimeError(f"meter import directory {import_dir} is not {want}")


# ---- G0 (§3 row 1; API.md §9.3, §20 B-6) ----------------------------------------------------
def _git(wt, *args) -> bytes:
    return subprocess.run(["git", "-C", str(wt), *args], capture_output=True, check=True).stdout


def _blobs_ok(wt, head) -> bool:
    def sha(rel):
        return hashlib.sha256(_git(wt, "show", f"{head}:{rel}")).hexdigest()

    for name, m in nc.CONTRACT["c2_code"]["modules"].items():
        rel = f"tools/c2_readout/{name}"
        if _git(wt, "rev-parse", f"{head}:{rel}").decode().strip() != m["git_blob"]:
            return False
        if sha(rel) != m["sha256"]:
            return False
    H = nc.CONTRACT["hashes"]
    return all(sha(rel) == s for rel, s in {**H["reused_blobs"], **H["reused_extra"]}.items())


def _c2_store_ok(ctx) -> bool:
    """(iv): every C2 store file re-hashes; 0115.accepted names the 0115 manifest; the FIT/DEC
    key sets from the zip directory only (ND-C7)."""
    (root, table), fk = c2_store(ctx), nc.CONTRACT["c2_store"]["fit_keys"]
    acc = _jr(root / "manifests" / "0115.accepted.json") or {}
    ok = bool(table) and not c2_rehash(ctx)
    ok = ok and _eq(acc.get("manifest_sha256"), table.get("manifests/0115.json"))
    fit, dk = list(fk["basis"]) + list(fk["other"]), nc.CONTRACT["c2_store"]["dec_keys"]
    for p in fk["problems"]:
        fit += [f"{p}_{k}" for k in nsb.PROB_KEYS] + ([f"{p}_Sigma"] if p != "R_E" else [])
    dec = [f"{F}_{k}_{x}" for F in dk["F"] for k in dk["k"] for x in dk["x"]]
    for j in nc.MODELS:
        for name, keys in ((f"FIT_{j}", fit), (f"DEC_{j}", dec)):
            with zipfile.ZipFile(root / "fits" / f"{name}.npz") as z:
                ok = ok and {f"{k}.npy" for k in keys} <= set(z.namelist())
    return ok


def _item(fn) -> dict:
    try:
        return {"status": "PASS" if fn() else "FAIL", "detail": ""}
    except Exception as exc:  # noqa: BLE001  a failed check is a failed item (C2 E-25)
        return {"status": "FAIL", "detail": repr(exc)}


def g0(ctx, stage=None) -> dict:
    """Items "i"-"x", never raising; FAIL_TECHNICAL/LINEAGE iff only (vi)-(vii) fail."""
    S, H, wt, store = cd.file_sha, nc.CONTRACT["hashes"], Path(ctx.worktree), Path(ctx.store)
    stage, fz = stage or ctx.data.get("stage"), _jr(binding_path(ctx)) or {}
    pkg, lin, meter = wt / "tools" / "c2_nd", recognised(store), wt / "tools" / "x4_oracle_profile"
    proto, mail = pkg / nc.PROTOCOL_FILE.name, Path(nc.PROJECT_ROOT) / nc.MAILBOX_FILE
    bound = {Path(cc.C1P_STORE) / Path(p).name: s for p, s in H["charts"].items()}
    bound[Path(cc.K4_FREEZE)] = H["k4_freeze"]
    bound[wt / "tools" / "c1prime" / "CONTRACT.json"] = H["c1prime_contract"]
    task = Path(nc.MAILBOX) / "jobs" / str(ctx.job) / "task.md"
    pins = {f"tools/c2_nd/{p.name}": S(p) for p in pkg.glob("*") if p.is_file()}
    dirs = (pkg.resolve(), (wt / "tools" / "c2_readout").resolve())

    def viii():
        ok = _eq(S(task), ctx.task_sha256) and ctx.session and release_ok(ctx, stage)["ok"]
        meter_bind_check(store / "nd_meter_bind.py", fz.get("meter_bind_sha256"), meter)
        return ok and tuple(Path(m.__file__).resolve().parent for m in (nc, cc)) == dirs

    def ix():
        if stage in ("S1", "S5"):
            return nrg.reservation_check(store, stage)["status"] == "PASS"
        return _sha_ok(store / "RESERVATION_S1.json", lin.get("RESERVATION_S1.json"))

    def vi():
        ok = nda.namespace_scan(nc.PROJECT_ROOT, pins, lin)["status"] == "PASS"
        return ok and nda.hygiene_check(nc.PROJECT_ROOT)["status"] == "PASS"

    out = {"i": _item(lambda: S(proto) == nc.PROTOCOL_SHA256 and _same(proto, mail))}
    st_ok = {j: m["state_sha_f32"] for j, m in nc.CONTRACT["models"].items()} == STATE_SHA
    out["ii"] = _item(lambda: _eq(S(pkg / "CONTRACT.json"), fz.get("contract_sha256")) and st_ok)
    out["iii"] = _item(lambda: _blobs_ok(wt, ctx.head))
    out["iv"] = _item(lambda: _c2_store_ok(ctx))
    out["v"] = _item(lambda: all(_sha_ok(p, s) for p, s in bound.items()))
    adm = {**lin, **nda.own_records(store, stage, lin)}
    out["vi"] = _item(vi)
    out["vii"] = _item(lambda: nda.store_admission(store, adm, stage == "S1")["status"] == "PASS")
    out["viii"], out["ix"] = _item(viii), _item(ix)
    out["x"] = _item(lambda: bool(ctx.dry) == is_dry_store(store))
    bad = [k for k, x in out.items() if x["status"] != "PASS"]
    cls = "LINEAGE" if bad and set(bad) <= {"vi", "vii"} else "AUTHORITY"
    out["status"] = f"FAIL_TECHNICAL/{cls}" if bad else "PASS"
    return out


def _same(a, b) -> bool:
    return Path(a).read_bytes() == Path(b).read_bytes()


# ---- stages (API.md §9.2) --------------------------------------------------------------------
def begin_stage(ctx, stage) -> None:
    store, stages, gates = Path(ctx.store), sr.stages_so_far(ctx.store), sr.gates_so_far(ctx.store)
    rel, prior = release_ok(ctx, stage), PREREQ[stage]
    done = [r for r in stages if r["stage"] == prior and r["event"] == "COMPLETED"]
    stop = any(g.get("scope") == "study" and g["status"] not in OK for g in gates)
    auth = auth_ok(store, "AUTH_IMPL.json" if ctx.dry else "AUTH.json")
    checks = ((any(r["stage"] == stage for r in stages), "stage already attempted"),)
    checks += ((not auth, "AUTH-ADMIT: no valid AUTH record"), (not rel["ok"], rel["reason"]))
    checks += ((stop, "prior study-scope stop"), (prior and not done, f"{prior} not completed"))
    checks += ((bool(ctx.dry) != is_dry_store(store), "dry-run switch and store differ"),)
    why = [w for c, w in checks if c]
    for n, s in done[-1]["evidence"].items() if done else ():
        why += [] if (store / n).exists() and sr.sha256(store / n) == s else [f"{n} changed"]
    if why:
        sr.refuse(store, stage, "; ".join(why), integrity=any("changed" in w for w in why))
    sr._append(store / "STAGES.jsonl", {"stage": stage, "event": "STARTED", "utc": sr._utc()})


def complete_stage(ctx, stage, files) -> list:
    """sr.complete, then the C2 store re-hash of G0 (iv) at the end of every stage (L7)."""
    sr.complete(ctx.store, stage, files)
    return c2_rehash(ctx)


def run_stage(stage, ctx) -> dict:
    """Lazy dispatch (C2 API §19.2): PLAN steps in order, NOT_RUN after a study stop, REPORT
    always runs. PREP (a dry-run store and --dry only) writes the synthetic prerequisites."""
    if stage == "PREP":
        if not (ctx.dry and is_dry_store(ctx.store)):
            raise StageRefused("PREP: a dry-run store and --dry only (G0 (x))")
        return importlib.import_module("nd_dry").prepare(ctx)
    plan = importlib.import_module(STAGE_MODULE[stage]).PLAN[stage]
    begin_stage(ctx, stage)
    ctx.release, ctx.data["stage"] = release_ok(ctx, stage), stage
    ctx.policy = LogitPolicy(done=[g["gate"] for g in sr.gates_so_far(ctx.store)])
    stopped, seen = None, {}
    for gate, fn, scope in plan:
        run = fn if stopped is None or gate == "REPORT" else (lambda c: {"status": "NOT_RUN"})
        ctx.policy.begin(gate)
        try:
            res = run_gate(ctx, gate, lambda: run(ctx), scope)
        finally:
            ctx.policy.end(gate)
        seen[gate], stopped = res["status"], stopped or (gate if res["stop"] else None)
    rel, ctx.data["stopped"] = f"stages/{stage}/record.json", stopped
    (Path(ctx.store) / rel).parent.mkdir(parents=True, exist_ok=True)
    sr.write_new(Path(ctx.store) / rel, _js({"stage": stage, "gates": seen, "stopped": stopped}))
    bad = complete_stage(ctx, stage, ctx.data.setdefault("files", []) + [rel])
    write_manifest(ctx, stage)
    print(f"L7: C2 store files changed: {bad}", file=sys.stderr) if bad else None
    return {"stage": stage, "stopped": stopped or ("L7" if bad else None)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="nd_driver")
    ap.add_argument("stage", choices=sorted(PREREQ) + ["PREP"])
    for opt in ("--store", "--job", "--task-sha256", "--session"):
        ap.add_argument(opt, required=True)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    wt = Path(__file__).resolve().parents[2]
    head = subprocess.run(["git", "-C", str(wt), "rev-parse", "HEAD"], capture_output=1, text=1)
    ctx = Ctx(Path(a.store), wt, head.stdout.strip(), a.job, a.task_sha256, a.session, dry=a.dry)
    try:
        res = run_stage(a.stage, ctx)
    except StageRefused as exc:
        print(exc, file=sys.stderr)
        return 3
    return 2 if res.get("stopped") else 0


if __name__ == "__main__":
    raise SystemExit(main())
