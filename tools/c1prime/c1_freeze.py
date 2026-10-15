"""C1' accepted test run, protected-record snapshots, implementation freeze and fresh-venv pin
check (API.md §14; K4 freeze_bind / run_tests_bind / live_context._pin_modules pattern).

Usage (through c1_meter_bind.py):
  base -I c1_freeze.py snapshot NAME | compare A B | freeze
  venv    c1_freeze.py accept           # pytest tests/c1prime -> OUT/tests/run_NN.json, ACCEPTED
  venv -I c1_freeze.py pincheck         # fresh venv process: every frozen hash, set and env
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [p for p in (str(HERE), str(HERE.parent / "x4_oracle_profile"),
                            str(HERE.parent / "x4_circle_history")) if p not in sys.path]

import freeze as f14  # noqa: E402  (job-0014, unchanged helpers: sha, tree, git, write_new)

ROOT = Path(r"X:\Downloads\projects\topo-pilot")
CONTRACT = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
OUT = Path(CONTRACT["resources"]["output_root"])
TESTS = REPO / "tests" / "c1prime"
VENV_PYTHON = ROOT / "topo-pilot" / ".venv" / "Scripts" / "python.exe"
PROTECTED_STORES = f14.STORES + (
    "x4-oracle-profile-store-0014", "x4-circle-history-feas-store-0015", "d1-seam-oracle-store",
    "chart-diag-store-0023", "x2a-stage0-oracle-store")
REUSED_K4 = tuple(f"tools/x4_circle_history/{n}" for n in (
    "chart.py", "cochain.py", "errors.py", "scores.py", "adapter.py", "stage_records.py",
    "precision.py", "error_bound.py", "op_guard.py", "env_identity.py"))
REUSED_0014 = ("tools/x4_oracle_profile/oracle_profile.py", "tools/x4_oracle_profile/meter.py",
               "tools/x4_oracle_profile/controls.py", "tools/x4_oracle_profile/winjob.py",
               "tools/x4_oracle_profile/freeze.py", "tests/oracle_profile/independent_reference.py")
DIST_PREFIXES = ("numpy-", "scipy-", "ripser-", "pytest-", "threadpoolctl-", "torch-")


def _listing(base: Path) -> dict:
    """Listing hash material (relative path -> size) without reading payload bytes."""
    return {p.relative_to(ROOT).as_posix(): p.stat().st_size for p in sorted(base.rglob("*"))
            if p.is_file()}


def snapshot() -> dict:
    files = {}
    for store in PROTECTED_STORES:
        if (ROOT / store).exists():
            files.update(f14.tree(ROOT / store))
    artifacts = _listing(ROOT / "topo-pilot" / "artifacts")
    heads = {"main": f14.git(ROOT / "topo-pilot", "rev-parse", "HEAD"),
             "c1p": f14.git(REPO, "rev-parse", "HEAD")}
    return {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "files": files,
            "artifact_listing": artifacts,
            "artifact_listing_sha256": _hash_json(artifacts), "git": heads}


def _hash_json(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def compare(a: dict, b: dict) -> dict:
    changed = sorted(k for k in a["files"].keys() | b["files"].keys()
                     if a["files"].get(k) != b["files"].get(k))
    return {"changed": changed, "artifact_listing_equal":
            a["artifact_listing_sha256"] == b["artifact_listing_sha256"],
            "git_changed": {k: [a["git"].get(k), b["git"].get(k)] for k in a["git"]
                            if a["git"].get(k) != b["git"].get(k)}}


def frozen_files() -> dict:
    own = sorted(p for p in HERE.iterdir() if p.is_file() and p.suffix in (".py", ".json", ".md"))
    tests = sorted(p for p in TESTS.iterdir() if p.is_file() and p.suffix in (".py", ".md")) \
        if TESTS.exists() else []
    src = sorted(p for p in (REPO / "src" / "topo_pilot").rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts and p.suffix in (".py", ".md"))
    rels = [p.relative_to(REPO).as_posix() for p in own + tests + src]
    rels += list(REUSED_K4) + list(REUSED_0014)
    return {rel: f14.sha(REPO / rel) for rel in sorted(set(rels))}


def reused_unchanged() -> dict:
    k4 = json.loads((ROOT / "x4-circle-history-feas-store-0015" / "FREEZE.json")
                    .read_text(encoding="utf-8"))["files"]
    j14 = json.loads((ROOT / "x4-oracle-profile-store-0014" / "FREEZE.json")
                     .read_text(encoding="utf-8"))["files"]
    out = {rel: f14.sha(REPO / rel) == k4.get(rel) for rel in REUSED_K4}
    out.update({rel: f14.sha(REPO / rel) == j14.get(rel) for rel in REUSED_0014})
    return out


def environment() -> dict:
    site = ROOT / "topo-pilot" / ".venv" / "Lib" / "site-packages"
    dists = sorted(p.name for p in site.iterdir()
                   if p.name.endswith(".dist-info") and p.name.lower().startswith(DIST_PREFIXES))
    return {"venv": str(site.parents[1]), "dist_info": dists, "threads": 1,
            "requirements_lock_sha256": f14.sha(REPO / "requirements.lock")}


def numerical_identity() -> dict:
    probe = subprocess.run([str(VENV_PYTHON), "-I", str(HERE / "c1_freeze.py"), "envrecord"],
                           capture_output=True, text=True, check=False, cwd=str(REPO))
    if probe.returncode != 0:
        raise SystemExit(f"numerical identity probe failed: {probe.stderr[-2000:]}")
    return json.loads(probe.stdout)


def freeze() -> dict:
    dirty = f14.git(REPO, "status", "--porcelain", "--", "tools/c1prime", "tests/c1prime")
    if dirty:
        raise SystemExit(f"refusing to freeze uncommitted files:\n{dirty}")
    accepted = json.loads((OUT / "tests" / "ACCEPTED.json").read_text(encoding="utf-8"))
    files = frozen_files()
    if accepted["files"] != files or not accepted["passed"]:
        raise SystemExit("accepted test run does not match the current frozen file set")
    reuse = reused_unchanged()
    if not all(reuse.values()):
        raise SystemExit(f"reused files differ from their freezes: {reuse}")
    record = {"protocol": CONTRACT["protocol"], "protocol_sha256": CONTRACT["protocol_sha256"],
              "job_id": CONTRACT["job_id"], "commit": f14.git(REPO, "rev-parse", "HEAD"),
              "files": files, "reused_unchanged": reuse,
              "contract_sha256": f14.sha(HERE / "CONTRACT.json"),
              "accepted_tests_sha256": f14.sha(OUT / "tests" / "ACCEPTED.json"),
              "environment": dict(environment(), numerical_identity=numerical_identity()),
              "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "scope": "implementation freeze only; no data; no stage executed"}
    if (OUT / "FREEZE.json").exists():
        raise SystemExit("FREEZE.json exists; a new freeze needs a new job")
    f14.write_new(OUT / "FREEZE.json", record)
    return record


def pin_check() -> dict:
    """Fresh venv process: frozen hashes, file set, dists, loaded modules and env identity."""
    freeze_rec = json.loads((OUT / "FREEZE.json").read_text(encoding="utf-8"))
    changed = [rel for rel, d in freeze_rec["files"].items() if f14.sha(REPO / rel) != d]
    if changed:
        raise SystemExit(f"frozen files changed: {changed}")
    if set(frozen_files()) != set(freeze_rec["files"]):
        raise SystemExit("frozen file set changed (file added or removed)")
    if environment()["dist_info"] != freeze_rec["environment"]["dist_info"]:
        raise SystemExit("installed numerical dependencies differ from the freeze")
    import c1_env
    import env_identity

    rec = c1_env.record()
    unfrozen = env_identity.unfrozen_project_modules(set(freeze_rec["files"]))
    if unfrozen:
        raise SystemExit(f"unfrozen project modules loaded: {unfrozen}")
    if rec != freeze_rec["environment"]["numerical_identity"]:
        raise SystemExit("numerical implementation identity differs from the freeze")
    return {"pin_check": "ACCEPTED", "files": len(freeze_rec["files"]),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def accept() -> int:
    import pytest

    out = OUT / "tests"
    out.mkdir(parents=True, exist_ok=True)
    number = 1 + max((int(p.stem.split("_")[1]) for p in out.glob("run_*.json")), default=0)
    junit = out / f"run_{number:02d}.xml"
    os.chdir(REPO)
    files, start = frozen_files(), time.process_time()
    code = pytest.main(["tests/c1prime", "-q", "-p", "no:cacheprovider", f"--junitxml={junit}"])
    record = {"run": number, "exit_code": int(code), "passed": int(code) == 0, "files": files,
              "pytest": pytest.__version__, "junit": junit.name,
              "in_process_cpu_s": time.process_time() - start,
              "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    path = out / f"run_{number:02d}.json"
    f14.write_new(path, record)
    if record["passed"]:
        tmp = out / "ACCEPTED.json.tmp"
        tmp.write_text(json.dumps(dict(record, record=path.name), indent=1, sort_keys=True),
                       encoding="utf-8")
        os.replace(tmp, out / "ACCEPTED.json")
    return int(code)


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "snapshot":
        f14.write_new(OUT / "snapshots" / f"{sys.argv[2]}.json", snapshot())
    elif cmd == "compare":
        a, b = (json.loads((OUT / "snapshots" / f"{n}.json").read_text(encoding="utf-8"))
                for n in sys.argv[2:4])
        result = compare(a, b)
        f14.write_new(OUT / "snapshots" / f"compare_{sys.argv[2]}_{sys.argv[3]}.json", result)
        print(json.dumps(result, indent=1))
    elif cmd == "freeze":
        print(json.dumps(freeze()["commit"]))
    elif cmd == "accept":
        return accept()
    elif cmd == "pincheck":
        result = pin_check()
        f14.write_new(OUT / f"PIN_CHECK_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json",
                      result)
        print(json.dumps(result))
    elif cmd == "envrecord":
        import c1_env

        print(json.dumps(c1_env.record(), sort_keys=True))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
