#!/usr/bin/env python3
"""Check state/PROGRESS.md length, state/DECISIONS.md line format, and tracked transcript files.

Exit 0 = clean, 1 = violations (one line each), 2 = usage error.
"""
import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "state"
PROGRESS_MAX = 80
DECISION_RE = re.compile(r"\d{4}-\d{2}-\d{2} \| D-\d{3} \| .+ \| .+ \| .+")
BAD_NAMES = ["*transcript*", "*chat*", "*.log"]


def check_progress(problems):
    path = STATE / "PROGRESS.md"
    if path.is_file():
        lines = len(path.read_text(encoding="utf-8").splitlines())
        if lines > PROGRESS_MAX:
            problems.append(f"state/PROGRESS.md: {lines} lines > {PROGRESS_MAX}")


def check_decisions(problems):
    path = STATE / "DECISIONS.md"
    if not path.is_file():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    start = 0
    while start < len(lines) and (lines[start].startswith("#") or not lines[start].strip()):
        start += 1
    for number in range(start + 1, len(lines) + 1):
        line = lines[number - 1]
        if line.strip() and not DECISION_RE.fullmatch(line):
            problems.append(f"state/DECISIONS.md:{number}: malformed decision line")


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO,
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [name for name in out.decode("utf-8", "replace").split("\0") if name]


def check_tracked(problems):
    files = tracked_files()
    if files is None:
        print("warning: git ls-files failed; tracked-file check skipped", file=sys.stderr)
        return
    for name in files:
        if any(fnmatch.fnmatch(name.lower(), pat) for pat in BAD_NAMES):
            problems.append(f"{name}: transcript-like file is tracked")


def main():
    ap = argparse.ArgumentParser(
        description="Check state/PROGRESS.md, state/DECISIONS.md and tracked transcript files.")
    ap.parse_args()
    problems = []
    check_progress(problems)
    check_decisions(problems)
    check_tracked(problems)
    if problems:
        for line in problems:
            print(line)
        return 1
    print("check_state_files: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
