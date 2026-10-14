"""Hash snapshots of protected records and the pre-profile implementation freeze (stdlib only).

Usage (always through meter.py, base interpreter):
  python -I freeze.py snapshot NAME      # protected-record hashes -> OUT/snapshots/NAME.json
  python -I freeze.py compare A B        # differences between two snapshots -> stdout + file
  python -I freeze.py freeze             # implementation/test/config/input freeze
                                         # -> OUT/FREEZE.json
  python -I freeze.py verify             # exit 1 unless every FREEZE.json hash still matches
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"X:\Downloads\projects\topo-pilot")
OUT = ROOT / "x4-oracle-profile-store-0014"
REPO = ROOT / "topo-pilot-x4b"
TOOL = REPO / "tools" / "x4_oracle_profile"
TESTS = REPO / "tests" / "oracle_profile"
STORES = (
    "circular-audit-store",
    "x4-history-feas-store",
    "x4b-research-store",
    "x4b2-research-store",
    "x4f-gates-research-store",
    "x5g1-research-store",
    "x5g1-techbench-store",
    "x5g1t-fixture-run",
    "x5g1t-research-store",
)
ARTIFACTS = (
    "WorldSpec/21feee1d8ee5422e",
    "TransitionSpec/e4dafc7b9785c172",
    "EmissionSpec/3633ac27dab50cf4",
    "EmissionSpec/97838b9e13a26f74",
    "EmissionSpec/8c29c329c197c79e",
)
MAILBOX_FILES = (
    "request.json",
    "worker_control.json",
    "Wait-Task.ps1",
    "Complete-Task.ps1",
    "Wait-Result.ps1",
    "Wait-UsageReset.ps1",
    "PROTOCOL.md",
    "USAGE_PROTOCOL.md",
    "jobs/0014/task.md",
    "jobs/0014/task.json",
    "jobs/0014/owner_authorization.md",
)
GIT_REFS = {
    "main": ROOT / "topo-pilot",
    "x4b": REPO,
    "x4_history_feas": ROOT / "topo-pilot-x4-history-feas",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def tree(base: Path) -> dict:
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(base.rglob("*")) if p.is_file()}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def snapshot() -> dict:
    files: dict = {}
    for store in STORES:
        files.update(tree(ROOT / store))
    for job in sorted((ROOT / "agent-handoff" / "jobs").iterdir()):
        if job.is_dir() and job.name.isdigit() and int(job.name) <= 13:
            files.update(tree(job))
    for aid in ARTIFACTS:
        files.update(tree(ROOT / "topo-pilot" / "artifacts" / aid))
    files.update(tree(ROOT / "topo-pilot-x4-history-feas" / "tools" / "x4_history_feas"))
    for name in MAILBOX_FILES:
        path = ROOT / "agent-handoff" / name
        files[path.relative_to(ROOT).as_posix()] = sha(path)
    heads = {name: git(repo, "rev-parse", "HEAD") for name, repo in GIT_REFS.items()}
    heads["x4b_branch_x5-g1-input-identity-fix"] = git(
        REPO, "rev-parse", "x5-g1-input-identity-fix"
    )
    return {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "files": files, "git": heads}


def write_new(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(obj, indent=1, sort_keys=True) + "\n")


def frozen_files() -> dict:
    paths = sorted(p for p in TOOL.iterdir() if p.is_file() and p.suffix in (".py", ".json", ".md"))
    paths += sorted(p for p in TESTS.iterdir() if p.is_file() and p.suffix in (".py", ".md"))
    return {p.relative_to(REPO).as_posix(): sha(p) for p in paths}


def freeze() -> dict:
    config = json.loads((TOOL / "config.json").read_text(encoding="utf-8"))
    dirty = git(
        REPO, "status", "--porcelain", "--", "tools/x4_oracle_profile", "tests/oracle_profile"
    )
    if dirty:
        raise SystemExit(f"refusing to freeze uncommitted implementation/test files:\n{dirty}")
    attempts = sorted((OUT / "validation").glob("attempt_*"))
    if not attempts:
        raise SystemExit("no validation attempt")
    latest = attempts[-1]
    numeric = json.loads((latest / "NUMERICAL_VERIFICATION.json").read_text(encoding="utf-8"))
    k8 = json.loads((latest / "K8_REPRODUCTION.json").read_text(encoding="utf-8"))
    tests = json.loads((OUT / "tests" / "ACCEPTED.json").read_text(encoding="utf-8"))
    if numeric["status"] != "PASS" or k8["status"] != "PASS" or not tests["passed"]:
        raise SystemExit("refusing to freeze: latest validation or accepted test run is not PASS")
    current = frozen_files()
    sources = json.loads((latest / "SOURCES.json").read_text(encoding="utf-8"))
    if tests["files"] != current:
        raise SystemExit("refusing to freeze: accepted tests ran against different files")
    if sources["files"] != current or sources["commit"] != git(REPO, "rev-parse", "HEAD"):
        raise SystemExit("refusing to freeze: latest validation was produced by different sources")
    validation = {
        "attempt": latest.name,
        "files": {p.name: sha(p) for p in sorted(latest.glob("*")) if p.is_file()},
        "accepted_tests": sha(OUT / "tests" / "ACCEPTED.json"),
    }
    record = {
        "protocol": config["protocol"],
        "commit": git(REPO, "rev-parse", "HEAD"),
        "files": frozen_files(),
        "inputs_sha256": config["inputs_sha256"],
        "K_grid": config["K_grid"],
        "splits": config["splits"],
        "expected_shapes": {
            s: {"tokens": [n, 32], "m_K": [n, 2]} for s, n in config["splits"].items()
        },
        "tolerances": config["tolerances"],
        "bootstrap": config["bootstrap"],
        "validation_outputs_sha256": validation,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    write_new(OUT / "FREEZE.json", record)
    return record


def verify() -> list:
    record = json.loads((OUT / "FREEZE.json").read_text(encoding="utf-8"))
    bad = [name for name, digest in record["files"].items() if sha(REPO / name) != digest]
    vrec = record["validation_outputs_sha256"]
    bad += [
        f"validation/{vrec['attempt']}/{name}"
        for name, digest in vrec["files"].items()
        if sha(OUT / "validation" / vrec["attempt"] / name) != digest
    ]
    if sha(OUT / "tests" / "ACCEPTED.json") != vrec["accepted_tests"]:
        bad.append("tests/ACCEPTED.json changed after freeze")
    later = sorted((OUT / "validation").glob("attempt_*"))[-1].name
    if later != vrec["attempt"]:
        bad.append(f"a later validation attempt exists: {later}")
    if set(frozen_files()) != set(record["files"]):
        bad.append("frozen file set changed")
    if git(REPO, "rev-parse", "HEAD") != record["commit"]:
        bad.append("HEAD moved after freeze")
    return bad


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    command = sys.argv[1]
    if command == "snapshot":
        write_new(OUT / "snapshots" / f"{sys.argv[2]}.json", snapshot())
    elif command == "compare":
        a, b = (json.loads((OUT / "snapshots" / f"{n}.json").read_text()) for n in sys.argv[2:4])
        changed = sorted(
            k
            for k in a["files"].keys() | b["files"].keys()
            if a["files"].get(k) != b["files"].get(k)
        )
        result = {
            "a": sys.argv[2],
            "b": sys.argv[3],
            "changed": changed,
            "git_changed": {
                k: [a["git"].get(k), b["git"].get(k)]
                for k in a["git"].keys() | b["git"].keys()
                if a["git"].get(k) != b["git"].get(k)
            },
        }
        write_new(OUT / "snapshots" / f"compare_{sys.argv[2]}_{sys.argv[3]}.json", result)
        print(json.dumps(result, indent=1))
    elif command == "freeze":
        print(json.dumps(freeze()["files"], indent=1))
    elif command == "verify":
        bad = verify()
        print(json.dumps({"freeze_mismatches": bad}))
        return 1 if bad else 0
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
