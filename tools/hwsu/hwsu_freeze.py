"""HWSU freeze and OF-B (API.md §5.3, §5.4; split from hwsu_records by size, re-exported there)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import fnmatch
import json
import platform
import subprocess
import sys
from pathlib import Path

import hwsu_records as ur
import numpy as np
import stage_records
from c1_records import C1GateFailure

FREEZE = "FAIL_TECHNICAL/FREEZE"
_sha = ur._sha


def _canon_sha(obj) -> str:
    return _sha(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


# --------------------------------------------------------------------------- freeze (§4.1)
def _git(repo, *args) -> bytes:
    try:
        return subprocess.run(["git", *args], cwd=repo, capture_output=True, check=True).stdout
    except (subprocess.CalledProcessError, OSError) as exc:
        raise C1GateFailure(FREEZE, f"git {' '.join(args[:2])}: {exc!r}"[:300]) from exc


def _blob(repo, ref, path) -> bytes:
    return _git(repo, "cat-file", "blob", f"{ref}:{path}")


def _test_files(names) -> list:
    pats = ("tests/hwsu/test_a_of_*.py", "tests/hwsu/test_b_of_*.py", "tests/hwsu/AUTHORSHIP_A.md",
            "tests/hwsu/AUTHORSHIP_B.md")
    return sorted(n for n in names if any(fnmatch.fnmatchcase(n, p) for p in pats))


def implementation_files(repo, h_exec, contract=None) -> dict:
    c = uc.CONTRACT if contract is None else contract
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec).decode().splitlines()
    return {p: _sha(_blob(repo, h_exec, p)) for p in list(c["phase1_files"]) + _test_files(names)}


def freeze_of(store, repo, h_exec, dro_report, j_of_records, written_by) -> dict:
    C = uc.CONTRACT
    files = implementation_files(repo, h_exec)
    impl = _canon_sha(files)
    reuse = {p: _sha(_blob(repo, h_exec, p)) for p in C["reuse_sha256"]}
    bad = [p for p, h in reuse.items() if C["reuse_sha256"][p] != h]
    if bad:
        raise C1GateFailure(FREEZE, f"reuse files differ at h_exec: {bad[:10]}")
    rep = json.loads(Path(dro_report).read_text(encoding="utf-8"))
    if rep.get("implementation_sha256") != impl or rep.get("all_pass") is not True:
        raise C1GateFailure(FREEZE, "dry report implementation_sha256 differs or not all_pass")
    jo = []
    for r in j_of_records:
        path, want = (r["path"], r.get("sha256")) if isinstance(r, dict) else (r, None)
        h = stage_records.sha256(path)
        if want is not None and want != h:
            raise C1GateFailure(FREEZE, f"J-OF record differs: {path}")
        jo.append({"path": str(path), "sha256": h})
    doc = {}
    for key, name in (("api", "API.md"), ("test_plan", "TEST_PLAN.md")):
        b = _blob(repo, h_exec, f"tools/hwsu/{name}")
        doc[f"{key}_sha256"], doc[f"{key}_bytes"] = _sha(b), len(b)
    rec = dict(doc, protocol=C["protocol"], protocol_sha256=_sha(
        _blob(repo, h_exec, "tools/hwsu/PROTOCOL_HWSU_v1.md")),
        contract_of_sha256=_sha(_blob(repo, h_exec, "tools/hwsu/CONTRACT_OF.json")),
        h_exec=h_exec, r_ref=C["of_b"]["r_ref"], implementation_files=files,
        implementation_sha256=impl, reuse_sha256=reuse, dry_run_report_path=str(dro_report),
        dry_run_report_sha256=stage_records.sha256(dro_report), j_of_records=jo,
        environment={"python": sys.version, "numpy": np.__version__,
                     "platform": platform.platform()}, written_by=written_by, created_utc=ur.utc())
    stage_records.write_new(Path(store) / "FREEZE_OF.json", rec)
    return rec


def verify_freeze_of(store, repo) -> dict:
    f, repo = Path(store) / "FREEZE_OF.json", Path(repo)
    if not f.is_file():
        raise C1GateFailure("INVALID", "FREEZE_OF.json absent")
    frz = json.loads(f.read_text(encoding="utf-8"))
    prefix = {"tools/hwsu/API.md": frz["api_bytes"], "tools/hwsu/TEST_PLAN.md":
              frz["test_plan_bytes"]}
    bad = []
    for p, h in frz["implementation_files"].items():
        q = repo / p
        data = q.read_bytes() if q.is_file() else None
        if data is not None and p in prefix:
            data = data[:prefix[p]]
        if data is None or _sha(data) != h:
            bad.append(p)
    for key, name in (("protocol_sha256", "PROTOCOL_HWSU_v1.md"),
                      ("contract_of_sha256", "CONTRACT_OF.json")):
        if _sha((repo / "tools" / "hwsu" / name).read_bytes()) != frz[key]:
            bad.append(name)
    for p, h in uc.CONTRACT["reuse_sha256"].items():
        if frz["reuse_sha256"].get(p) != h or not (repo / p).is_file() or _sha(
                (repo / p).read_bytes()) != h:
            bad.append(p)
    if bad:
        raise C1GateFailure("INVALID", f"FREEZE_OF mismatch: {bad[:10]}")
    return {"status": "PASS", "freeze": frz, "freeze_sha256": stage_records.sha256(f)}


def of_b(store, repo, r_ref=None) -> dict:
    import hwsu_bind

    C = uc.CONTRACT
    frz = verify_freeze_of(store, repo)["freeze"]
    r_ref = C["of_b"]["r_ref"] if r_ref is None else r_ref
    h = frz["h_exec"]
    diff = _git(repo, "diff", "--no-renames", "--name-status", r_ref, h).decode().splitlines()
    ok_names = set(C["phase1_files"])
    bad = []
    for ln in (x for x in diff if x.strip()):
        st, _, path = ln.partition("\t")
        ok = (st == "A" and (path in ok_names or path in _test_files([path]))) or (
            st in ("A", "M") and path.startswith("docs/code_index/"))
        if not ok:
            bad.append(ln)
    if bad:
        raise C1GateFailure("INVALID", f"diff outside the allowlist: {bad[:10]}")
    for p, want in C["reuse_sha256"].items():
        if _sha(_blob(repo, h, p)) != want or _sha(_blob(repo, r_ref, p)) != want:
            raise C1GateFailure("INVALID", f"reuse hash differs: {p}")
    audit = hwsu_bind.audit()
    if audit["status"] != "PASS":
        raise C1GateFailure("INVALID", "binding audit failed")
    return {"status": "PASS", "h_exec": h, "diff": diff,
            "audit": {"status": audit["status"], "n_refs": audit["calls"].get("n_refs")}}


