#!/usr/bin/env python3
"""Fail on .py files over 400 lines (outside .venv) and tracked files over 5 MB.

Exit 0 = clean, 1 = violations (one line each), 2 = usage error.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MAX_LINES = 400
MAX_BYTES = 5 * 1024 * 1024
PRUNE = {".venv", ".git", "__pycache__"}
FALLBACK_PRUNE = {".venv", ".git", "artifacts", "bundles", "__pycache__"}


def display(path):
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def walk(prune):
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames if d not in prune]
        for name in filenames:
            yield Path(dirpath) / name


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO,
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return list(walk(FALLBACK_PRUNE))
    return [REPO / name for name in out.decode("utf-8", "replace").split("\0") if name]


def main():
    ap = argparse.ArgumentParser(
        description="Check .py line counts (max 400) and tracked file sizes (max 5 MB).")
    ap.parse_args()
    problems = []
    for path in walk(PRUNE):
        if path.suffix == ".py":
            lines = len(path.read_bytes().splitlines())
            if lines > MAX_LINES:
                problems.append(f"{display(path)}: {lines} lines > {MAX_LINES}")
    for path in tracked_files():
        if path.is_file() and path.stat().st_size > MAX_BYTES:
            problems.append(f"{display(path)}: {path.stat().st_size} bytes > 5 MB (tracked)")
    if problems:
        for line in sorted(problems):
            print(line)
        return 1
    print("check_file_sizes: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
