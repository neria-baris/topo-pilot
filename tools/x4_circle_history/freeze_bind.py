"""Protected-record snapshots and implementation freeze for job 0016 (standard library only).

Reuses the hashing helpers of the job-0014 freeze.py UNCHANGED (sha, tree, git). That module's
own snapshot and freeze functions are job-0014-specific, so this module is the job-0016 binding.

Usage (through meter_bind.py, base interpreter):
  python -I freeze_bind.py snapshot NAME | compare A B | freeze | verify
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "x4_oracle_profile"))

import freeze as f14  # noqa: E402  (job-0014, unchanged helpers)

ROOT = Path(r"X:\Downloads\projects\topo-pilot")
CONTRACT = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
OUT = Path(CONTRACT["resources"]["output_root"])
TESTS = REPO / "tests" / "circle_history"
STORES = f14.STORES + ("x4-oracle-profile-store-0014",)
REUSED_0014 = (
    "tools/x4_oracle_profile/oracle_profile.py",
    "tools/x4_oracle_profile/inputs.py",
    "tools/x4_oracle_profile/meter.py",
    "tools/x4_oracle_profile/controls.py",
    "tools/x4_oracle_profile/winjob.py",
    "tools/x4_oracle_profile/freeze.py",
    "tools/x4_oracle_profile/config.json",
    "tests/oracle_profile/independent_reference.py",
)
GIT_REFS = {
    "main": ROOT / "topo-pilot",
    "x4b_shared": ROOT / "topo-pilot-x4b",
    "x4_history_feas": ROOT / "topo-pilot-x4-history-feas",
    "circle_k4": REPO,
}
DIST_PREFIXES = ("numpy-", "scipy-", "ripser-", "pytest-", "threadpoolctl-", "matplotlib-")


def snapshot() -> dict:
    files: dict = {}
    for store in STORES:
        if (ROOT / store).exists():
            files.update(f14.tree(ROOT / store))
    for job in sorted((ROOT / "agent-handoff" / "jobs").iterdir()):
        if job.is_dir() and job.name.isdigit() and int(job.name) <= 15:
            files.update(f14.tree(job))
    for aid in f14.ARTIFACTS:
        files.update(f14.tree(ROOT / "topo-pilot" / "artifacts" / aid))
    for kind, ids in (
        ("ActivationSet", "ActivationSet"),
        ("ObservationSet", "ObservationSet"),
        ("HistoryIndex", "HistoryIndex"),
    ):
        for model in CONTRACT["artifacts"]["per_model"].values():
            for name in ("meta.json", "extra.json"):
                path = ROOT / "topo-pilot" / "artifacts" / kind / model[ids] / name
                files[path.relative_to(ROOT).as_posix()] = f14.sha(path)
    files.update(f14.tree(ROOT / "topo-pilot-x4-history-feas" / "tools" / "x4_history_feas"))
    heads = {name: f14.git(repo, "rev-parse", "HEAD") for name, repo in GIT_REFS.items()}
    return {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "files": files, "git": heads}


def frozen_files() -> dict:
    own = sorted(p for p in HERE.iterdir() if p.is_file() and p.suffix in (".py", ".json", ".md"))
    tests = sorted(p for p in TESTS.iterdir() if p.is_file() and p.suffix in (".py", ".md"))
    paths = [p.relative_to(REPO).as_posix() for p in own + tests] + list(REUSED_0014)
    return {rel: f14.sha(REPO / rel) for rel in paths}


def reused_unchanged() -> dict:
    record = json.loads(
        (ROOT / "x4-oracle-profile-store-0014" / "FREEZE.json").read_text(encoding="utf-8")
    )["files"]
    return {rel: (f14.sha(REPO / rel) == record.get(rel)) for rel in REUSED_0014}


def environment() -> dict:
    site = ROOT / "topo-pilot" / ".venv" / "Lib" / "site-packages"
    dists = sorted(
        p.name
        for p in site.iterdir()
        if p.name.endswith(".dist-info") and p.name.lower().startswith(DIST_PREFIXES)
    )
    return {
        "venv": str(site.parents[1]),
        "dist_info": dists,
        "threads": "OPENBLAS/MKL/OMP/NUMEXPR/VECLIB=1 via meter; HiGHS threads=1/parallel=False",
        "seeds": {
            "sd": CONTRACT["precision"]["sd_seed"],
            "centered": CONTRACT["precision"]["centered_seed"],
            "algorithm": "numpy.random.Generator(PCG64(seed))",
        },
    }


def freeze() -> dict:
    dirty = f14.git(
        REPO, "status", "--porcelain", "--", "tools/x4_circle_history", "tests/circle_history"
    )
    if dirty:
        raise SystemExit(f"refusing to freeze uncommitted files:\n{dirty}")
    accepted = json.loads((OUT / "tests" / "ACCEPTED.json").read_text(encoding="utf-8"))
    files = frozen_files()
    if accepted["files"] != files or not accepted["passed"]:
        raise SystemExit("accepted test run does not match the current frozen file set")
    reuse = reused_unchanged()
    if not all(reuse.values()):
        raise SystemExit(f"reused job-0014 files differ from their job-0014 freeze: {reuse}")
    record = {
        "protocol": CONTRACT["protocol"],
        "job_id": CONTRACT["job_id"],
        "commit": f14.git(REPO, "rev-parse", "HEAD"),
        "files": files,
        "reused_0014_unchanged": reuse,
        "contract_sha256": f14.sha(HERE / "CONTRACT.json"),
        "accepted_tests_sha256": f14.sha(OUT / "tests" / "ACCEPTED.json"),
        "environment": environment(),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scope": "implementation freeze only; no real payload accessed; no feasibility run",
    }
    f14.write_new(OUT / "FREEZE.json", record)
    return record


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "snapshot":
        f14.write_new(OUT / "snapshots" / f"{sys.argv[2]}.json", snapshot())
    elif cmd == "compare":
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
                for k in a["git"]
                if a["git"].get(k) != b["git"].get(k)
            },
        }
        f14.write_new(OUT / "snapshots" / f"compare_{sys.argv[2]}_{sys.argv[3]}.json", result)
        print(json.dumps(result, indent=1))
    elif cmd == "freeze":
        print(json.dumps(freeze()["files"], indent=1))
    elif cmd == "reuse":
        print(json.dumps(reused_unchanged(), indent=1))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
