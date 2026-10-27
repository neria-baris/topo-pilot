"""HWSB records: the study ledger, project-root inventories, and FREEZE.json (API.md §8,
§13; protocol §6.4 rule 1, §8.2 RC-7). Split out of hwsb_driver by size; hwsb_driver
re-exports every name.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import json
import os
import platform
import subprocess
import time
from pathlib import Path

import hws_records
import k4b_registry
import numpy as np
import stage_records

from topo_pilot.contracts import canonical_json

FREEZE = "FAIL_TECHNICAL/FREEZE"
C = hc.CONTRACT


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def ledger_read(path) -> dict:
    path = Path(path)
    if not path.exists():
        return {"study": hc.SCOPE, "entries": [], "cumulative_cpu_s": 0.0}
    return json.loads(path.read_text(encoding="utf-8"))


def ledger_append(path, job, stage, cpu_s, source, master=None) -> dict:
    path = Path(path)
    led = ledger_read(path)
    if any(e["job"] == str(job) for e in led["entries"]):
        raise hc.HwsbStop("FAIL_TECHNICAL/LEDGER", f"job {job} already in the study ledger")
    led["entries"].append(
        {
            "job": str(job),
            "stage": stage,
            "cpu_s": float(cpu_s),
            "source": str(source),
            "master": master,
            "utc": utc(),
        }
    )
    led["cumulative_cpu_s"] = float(sum(e["cpu_s"] for e in led["entries"]))
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(led, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return led


def inventory_snapshot(root=hc.ROOT, exclude=()) -> dict:
    inv = k4b_registry.inventory(root, exclude)
    keys = ("history_files", "identity_refs", "observation_set_roots")
    return {
        top: dict(
            {k: sorted(r.get(k, [])) for k in keys},
            unreadable=sorted(u["path"] for u in r.get("unreadable", [])),
        )
        for top, r in inv.items()
    }


def inventory_diff(before, after) -> dict:
    new = {}
    for top, rec in after.items():
        old = before.get(top, {})
        d = {k: [p for p in v if p not in set(old.get(k, []))] for k, v in rec.items()}
        d = {k: v for k, v in d.items() if v}
        if d:
            new[top] = d
    return {"ok": not new, "new": new}


def _git(repo, *args) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def implementation_files(repo, h_exec) -> dict:
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec, "--", "tools/hwsb", "tests/hwsb")
    keep = [
        n
        for n in names.decode("utf-8").splitlines()
        if n.startswith("tests/hwsb/") or n.endswith(".py")
    ]
    return {n: hws_records.sha_bytes(_git(repo, "show", f"{h_exec}:{n}")) for n in keep}


def _hashes(repo) -> dict:
    t = Path(repo) / "tools" / "hwsb"
    names = {
        "protocol_sha256": "PROTOCOL_HWSB_v1.md",
        "contract_sha256": "CONTRACT.json",
        "api_sha256": "API.md",
        "test_plan_sha256": "TEST_PLAN.md",
        "proof_note_sha256": "ENCLOSURE_PROOF.md",
    }
    out = {k: stage_records.sha256(t / v) for k, v in names.items()}
    reuse = {rel: stage_records.sha256(Path(repo) / rel) for rel in C["reuse_sha256"]}
    if out["protocol_sha256"] != C["protocol_sha256"]:
        raise hc.HwsbStop(FREEZE, "protocol copy differs from CONTRACT protocol_sha256")
    bad = sorted(k for k, v in reuse.items() if v != C["reuse_sha256"][k])
    if bad:
        raise hc.HwsbStop(FREEZE, f"reused files changed: {bad}")
    return dict(out, reuse_sha256=reuse)


def freeze(out, repo, h_exec, dry_report) -> dict:
    files = implementation_files(repo, h_exec)
    impl = hws_records.sha_bytes(canonical_json(files).encode("utf-8"))
    dry = json.loads(Path(dry_report).read_text(encoding="utf-8"))
    if dry.get("implementation_sha256") != impl:
        raise hc.HwsbStop(FREEZE, "dry-run report is not bound to this implementation hash")
    import scipy
    import torch

    rec = {
        "protocol": "HWSB-FROZEN-v1",
        "h_exec": h_exec,
        "implementation_files": files,
        "implementation_sha256": impl,
        "dry_run_report_sha256": stage_records.sha256(dry_report),
        "dry_run_report_path": str(dry_report),
        "created_utc": utc(),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "torch": torch.__version__,
        },
    }
    rec.update(_hashes(repo))
    Path(out).mkdir(parents=True, exist_ok=True)
    stage_records.write_new(Path(out) / "FREEZE.json", rec)
    return rec


def verify_freeze(out, repo) -> dict:
    path = Path(out) / "FREEZE.json"
    if not path.exists():
        raise hc.HwsbStop(FREEZE, "FREEZE.json missing")
    rec = json.loads(path.read_text(encoding="utf-8"))
    now = {rel: stage_records.sha256(Path(repo) / rel) for rel in rec["implementation_files"]}
    if now != rec["implementation_files"]:
        raise hc.HwsbStop(FREEZE, "implementation files differ from FREEZE.json")
    bad = [k for k, v in _hashes(repo).items() if rec.get(k) != v]
    if bad:
        raise hc.HwsbStop(FREEZE, f"FREEZE.json mismatch: {bad}")
    return dict(rec, freeze_sha256=stage_records.sha256(path))


# ---------------------------------------------------------------------------------- TRAIN
