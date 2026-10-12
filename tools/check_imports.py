#!/usr/bin/env python3
"""Check import rules in src/topo_pilot (see tools/SPEC.md).

Exit 0 = clean, 1 = violations (one line each), 2 = usage error.
"""
import argparse
import os
import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODULES = {"contracts", "world", "process", "dataset", "oracle", "learner",
           "activations", "prediction", "topology", "analysis", "experiment", "executors"}
LEARNER_BANNED = {"world", "process", "oracle", "analysis", "prediction"}
SCIENCE = {"world", "process", "dataset", "oracle", "learner", "activations",
           "prediction", "topology", "analysis"}


def import_paths(node, root, path):
    """Return the topo_pilot paths (parts after 'topo_pilot') that one import touches."""
    if isinstance(node, ast.Import):
        names = [alias.name.split(".") for alias in node.names]
    else:
        if node.level:
            pkg = ["topo_pilot", *path.relative_to(root).parts[:-1]]
            base = pkg[: max(len(pkg) - node.level + 1, 0)]
            target = base + (node.module.split(".") if node.module else [])
        else:
            target = (node.module or "").split(".")
        names = [target]
        if target[:1] == ["topo_pilot"]:
            for alias in node.names:
                # "from topo_pilot.x import y" where y is a file or folder of x is a deep import
                parent = root.joinpath(*target[1:])
                # exact (case-sensitive) match: Windows paths are case-insensitive
                entries = set(os.listdir(parent)) if parent.is_dir() else set()
                is_sub = f"{alias.name}.py" in entries or (
                    alias.name in entries and (parent / alias.name).is_dir())
                module_name = len(target) == 1 and alias.name in MODULES
                if module_name or (is_sub and alias.name != "*"):
                    names.append(target + [alias.name])
    return [name[1:] for name in names if name[:1] == ["topo_pilot"]]


def violations_for(module, parts):
    """Return the rule messages that importing topo_pilot.<parts> from <module> breaks."""
    msgs = []
    if parts[:2] == ["contracts", "testing"]:
        msgs.append("contracts.testing imported from src/")
    top = parts[0] if parts else None
    if len(parts) >= 2 and top in MODULES and top != module:
        msgs.append("imports another module's internals: topo_pilot." + ".".join(parts))
    if top in MODULES and top != module:
        if module in ("learner", "activations") and top in LEARNER_BANNED:
            msgs.append(f"{module} must not import {top}")
        if module == "topology" and top != "contracts":
            msgs.append(f"topology must not import {top}")
        if module == "executors" and top in SCIENCE:
            msgs.append(f"executors must not import science module {top}")
    return msgs


def display(path):
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def scan(root):
    problems = []
    files = sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)
    for path in files:
        rel_parts = path.relative_to(root).parts
        module = rel_parts[0] if len(rel_parts) > 1 else None
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            problems.append(f"{display(path)}:{exc.lineno}: syntax error: {exc.msg}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for parts in import_paths(node, root, path):
                    for msg in violations_for(module, parts):
                        problems.append(f"{display(path)}:{node.lineno}: {msg}")
    return problems, len(files)


def main():
    ap = argparse.ArgumentParser(description="Check topo_pilot import rules (tools/SPEC.md).")
    ap.add_argument("--root", default=str(REPO / "src" / "topo_pilot"),
                    help="package directory to scan (default: src/topo_pilot)")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"usage error: not a directory: {root}", file=sys.stderr)
        return 2
    problems, count = scan(root)
    if problems:
        for line in problems:
            print(line)
        return 1
    print(f"check_imports: ok ({count} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
