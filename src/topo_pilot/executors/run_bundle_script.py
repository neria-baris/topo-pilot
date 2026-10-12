"""Standalone ``run_bundle.py`` shipped inside every bundle (standard library only until the
environment is installed).

Usage, from the unpacked ``bundle_<job>/`` folder::

    python run_bundle.py [--no-install | --install-only]

Steps: optionally install ``requirements.lock`` (local version suffixes such as ``+cpu`` are
stripped from pins; ``torch`` is skipped if already importable), verify and import the input
artifacts into a fresh store, run ``topo_pilot.executors.entry``, and pack
``outputs_<job>.tar.gz`` with the new artifacts and the RunManifest.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def filtered_requirements(text: str, torch_present: bool) -> list[str]:
    """Pins without local version suffixes; ``torch`` dropped when it is already importable."""
    lines = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        line = re.sub(r"\+[A-Za-z0-9.]+(?=\s*(;|$))", "", line)
        name = re.split(r"[=<>!~\[ ;]", line, maxsplit=1)[0].lower().replace("_", "-")
        if name == "torch" and torch_present:
            continue
        lines.append(line)
    return lines


def install(work: Path) -> None:
    """``pip install`` the filtered lock; fall back to one package at a time on failure."""
    lock = (HERE / "requirements.lock").read_text(encoding="utf-8")
    lines = filtered_requirements(lock, importlib.util.find_spec("torch") is not None)
    work.mkdir(parents=True, exist_ok=True)
    req = work / "requirements.filtered.txt"
    req.write_text("\n".join(lines) + "\n", encoding="utf-8")
    pip = [sys.executable, "-m", "pip", "install", "-q"]
    if subprocess.run([*pip, "-r", str(req)]).returncode == 0:
        return
    print("bulk install failed; retrying package by package", file=sys.stderr)
    for line in lines:
        if subprocess.run([*pip, line]).returncode != 0:
            print(f"warning: could not install {line}", file=sys.stderr)


def run(work: Path) -> int:
    """Verify inputs, run the job, pack outputs; returns the job exit code."""
    sys.path.insert(0, str(HERE / "src"))
    from topo_pilot.contracts import ArtifactStore, LocalFSBackend

    job_doc = json.loads((HERE / "job.json").read_text(encoding="utf-8"))
    job_id = job_doc["job"]["job_id"]
    store = ArtifactStore(LocalFSBackend(work / "store"),
                          producer_version=job_doc.get("git_sha", "unknown"))
    inputs = store.import_bundle(HERE / "inputs.tar.gz")
    print(f"verified {len(inputs)} input artifact(s)")
    job_doc.update(store_root=str(work / "store"), repo_root=str(HERE))
    run_json = work / "job_run.json"
    run_json.write_text(json.dumps(job_doc), encoding="utf-8")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [str(HERE / "src"), os.environ.get("PYTHONPATH", "")]).rstrip(os.pathsep))
    code = subprocess.run([sys.executable, "-m", "topo_pilot.executors.entry", str(run_json)],
                          env=env, cwd=HERE).returncode
    result_file = run_json.with_name("job_run.result.json")
    if not result_file.is_file():
        print("entry produced no result file", file=sys.stderr)
        return code or 1
    result = json.loads(result_file.read_text(encoding="utf-8"))
    dest = HERE / f"outputs_{job_id}.tar.gz"
    store.export_bundle([*result["outputs"], result["manifest"]], dest, with_parents=False)
    print(f"wrote {dest}")
    return code


def main() -> int:
    """CLI entry."""
    parser = argparse.ArgumentParser(description="Run this bundle's job.")
    parser.add_argument("--no-install", action="store_true", help="skip installing the lock")
    parser.add_argument("--install-only", action="store_true", help="only install, then stop")
    parser.add_argument("--work", type=Path, default=HERE / "work")
    args = parser.parse_args()
    if not args.no_install:
        install(args.work)
    if args.install_only:
        return 0
    return run(args.work)


if __name__ == "__main__":
    sys.exit(main())
