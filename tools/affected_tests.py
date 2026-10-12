#!/usr/bin/env python3
"""Print the minimal pytest folders for changed paths (see tools/SPEC.md).

Prints one existing folder per line, then a ready-to-run command, or "nothing to run".
"""
import argparse
import ast
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODULES = ["contracts", "world", "process", "dataset", "oracle", "learner", "activations",
           "prediction", "topology", "analysis", "experiment", "executors"]
DEPENDENTS = {
    "world": ["process", "analysis"],
    "process": ["dataset", "oracle", "analysis"],
    "dataset": ["learner", "activations"],
    "oracle": ["prediction", "analysis"],
    "learner": ["activations"],
    "activations": ["prediction", "analysis"],
    "prediction": ["experiment"],
    "topology": ["analysis"],
    "analysis": ["experiment"],
    "executors": ["experiment"],
    "experiment": [],
}


def repo_rel(raw):
    """Return the repo-relative posix path for a path given as \\ or /, absolute or relative."""
    path = Path(raw.replace("\\", "/"))
    if not path.is_absolute():
        path = REPO / path
    try:
        return path.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        return None


def signature(node):
    """Return a comparable text signature of a top-level function or class."""
    if isinstance(node, ast.ClassDef):
        bases = ", ".join(ast.unparse(base) for base in node.bases)
        methods = [signature(m) for m in node.body
                   if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and (m.name == "__init__" or not m.name.startswith("_"))]
        return f"class {node.name}({bases}) :: " + "; ".join(methods)
    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"{prefix}def {node.name}({ast.unparse(node.args)}){returns}"


def api_of(source):
    """Return (sorted __all__ names, {name: signature}) for a module source text."""
    all_names, defs = None, {}
    for node in ast.parse(source).body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if node.value is not None and any(
                    isinstance(t, ast.Name) and t.id == "__all__" for t in targets):
                try:
                    all_names = sorted(ast.literal_eval(node.value))
                except ValueError:
                    all_names = ast.unparse(node.value)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs[node.name] = signature(node)
    return all_names, defs


def api_changed(module):
    """True if the public API of <module>/__init__.py differs from HEAD (or cannot be compared)."""
    rel = f"src/topo_pilot/{module}/__init__.py"
    current = REPO / rel
    if not current.is_file():
        return True
    try:
        head = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=REPO,
                              capture_output=True, check=True).stdout.decode("utf-8")
        return api_of(head) != api_of(current.read_text(encoding="utf-8"))
    except (OSError, subprocess.CalledProcessError, SyntaxError, UnicodeDecodeError):
        return True


def main():
    ap = argparse.ArgumentParser(description="Print the pytest folders affected by changed paths.")
    ap.add_argument("--changed", nargs="*", default=[], metavar="PATH",
                    help="changed paths (absolute or repo-relative, \\ or / separators)")
    args = ap.parse_args()

    touched, suites = set(), set()
    for raw in args.changed:
        rel = repo_rel(raw)
        parts = rel.split("/") if rel else []
        if parts[:2] == ["src", "topo_pilot"] and len(parts) >= 3 and parts[2] in MODULES:
            if parts[2] == "contracts":
                suites.update(MODULES)
            else:
                touched.add(parts[2])
        elif parts[:1] == ["tests"] and len(parts) >= 2 and parts[1] in MODULES:
            suites.add(parts[1])

    for module in sorted(touched):
        suites.add(module)
        if api_changed(module):
            suites.update(DEPENDENTS[module] + ["experiment"])
    folders = [f"tests/{m}" for m in MODULES if m in suites and (REPO / "tests" / m).is_dir()]
    for folder in folders:
        print(folder)
    if folders:
        print("python -m pytest " + " ".join(folders) + " -q")
    else:
        print("nothing to run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
