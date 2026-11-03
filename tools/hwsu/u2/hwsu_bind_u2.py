"""HWSU phase-2 call allowlist and constant-read audit (API_U2.md section 2.6; protocol 11.2).

Counterpart of the phase-1 hwsu_bind (not edited): it audits tools/hwsu/u2/*.py against the
phase-1 tables merged with the phase-2 tables, admits the sanctioned forbidden reads of
binding.conditional_reads(_u2) and reads one function by path (AST, no import) where the module
cannot be imported (R-0223-5).
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_bind as ub
import u2  # noqa: F401
import ast
import copy
import importlib
from pathlib import Path

BIND = "FAIL_TECHNICAL/BINDING"
# functions that may be referenced from the DRU dry run only (R-0223-3, R-0223-6)
DRY_ONLY = {("hwsb_train", "train"), ("hwsc_data", "make_train_dev_c"),
            ("hwsc_registry_build", "build")}


def u2_files() -> list:
    return sorted((uc.HERE / "u2").glob("*.py"))


def merged_contract(contract=None) -> dict:
    c = copy.deepcopy(uc.CONTRACT if contract is None else contract)
    b = c["binding"]
    for mod, names in b.get("allowlist_conditional_u2", {}).items():
        b["allowlist"].setdefault(mod, {}).update(copy.deepcopy(names))
    b["never_called"] = list(b["never_called"]) + list(b.get("never_called_u2", []))
    b["conditional_reads"] = list(b.get("conditional_reads", [])) + list(
        b.get("conditional_reads_u2", []))
    return c


def _find_module(module):
    hits = sorted((uc.REPO / "tools").rglob(f"{module}.py"))
    if not hits:
        raise ImportError(f"No module named {module!r}")
    return hits[0]


def reads_by_path(module, qualname) -> dict:
    """alias.name references of one top-level function, parsed without importing the module."""
    tree = ast.parse(_find_module(module).read_text(encoding="utf-8"))
    alias = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for a in node.names:
                alias[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(
                    ".")[0]
    fn = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name == qualname), None)
    if fn is None:
        raise AttributeError(f"{module}.{qualname}")
    out = {}
    for n in ast.walk(fn):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in alias:
            out[f"{alias[n.value.id]}.{n.attr}"] = True
    return out


def function_reads_u2(module, qualname, entry) -> dict:
    if entry.get("ast_by_path"):
        return reads_by_path(module, qualname)
    for m in entry.get("import_first", []):
        importlib.import_module(m)
    return ub.function_reads(module, qualname)


def _resolve(mod, qualname):
    obj = importlib.import_module(mod)
    for part in qualname.split("."):
        obj = getattr(obj, part)
    return obj


def _audit_reads(c) -> tuple:
    b = c["binding"]
    cond = {(x["function"], x["read"]) for x in b.get("conditional_reads", [])}
    forb = set(b["forbidden_reads"])
    unlisted, forbidden, by_path = [], [], []
    for mod, names in b["allowlist"].items():
        for name, entry in names.items():
            if entry.get("kind") != "function":
                continue
            fq = f"{mod}.{name}"
            try:
                if entry.get("ast_by_path"):
                    by_path.append(fq)
                else:
                    for m in entry.get("import_first", []):
                        importlib.import_module(m)
                    if not ub._under_tools(_resolve(mod, name)):
                        continue
                got = set(function_reads_u2(mod, name, entry))
            except (ImportError, AttributeError) as exc:
                unlisted.append({"function": fq, "problem": repr(exc),
                                 "missing_module": getattr(exc, "name", None)})
                continue
            want = set(entry["ast_refs"] if entry.get("ast_by_path")
                       else entry.get("call_time_reads", {}))
            if got != want:
                unlisted.append({"function": fq, "extra": sorted(got - want),
                                 "missing": sorted(want - got)})
            for key in sorted(got):
                last = key.rsplit(".", 1)[-1] if "[" not in key else key.split(".", 1)[1]
                bad = last in forb or (last.startswith("CONTRACT[")
                                       and key != 'hwsc_config.CONTRACT["world"]')
                if bad and (fq, key) not in cond:
                    forbidden.append({"function": fq, "read": key})
    return unlisted, forbidden, by_path


def rebindings(path) -> list:
    """Assignments to an attribute of an imported module (mod.NAME = ...) in one file."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    mods = {k: v for k, v in ub.module_imports(tree).items() if isinstance(v, str)}
    out = []
    for n in ast.walk(tree):
        tg = (n.targets if isinstance(n, ast.Assign) else
              [n.target] if isinstance(n, (ast.AugAssign, ast.AnnAssign)) else [])
        out += [{"module": mods[t.value.id], "name": t.attr, "line": n.lineno,
                 "file": Path(path).name} for t in tg if isinstance(t, ast.Attribute)
                and isinstance(t.value, ast.Name) and t.value.id in mods]
    return out


def audit_u2(files=None, contract=None) -> dict:
    c = merged_contract(contract)
    fl = [Path(f) for f in (u2_files() if files is None else files)]
    calls = ub.audit_calls(fl, c)
    misplaced = [dict(r, file=f.name) for f in fl if f.name != "hwsu_dry2.py"
                 for r in ub.references(f) if (r["module"], r["name"]) in DRY_ONLY]
    unlisted, forbidden, by_path = _audit_reads(c)
    reads = {"status": "PASS" if not (unlisted or forbidden) else BIND, "unlisted": unlisted,
             "forbidden": forbidden}
    declared = {(d["module"], d["name"], d["file"])
                for d in c["binding"].get("dry_rebinding_u2", [])}
    undeclared = [r for f in fl for r in rebindings(f)
                  if (r["module"], r["name"], r["file"]) not in declared]
    ok = (calls["status"] == "PASS" and reads["status"] == "PASS" and not misplaced
          and not undeclared)
    return {"status": "PASS" if ok else BIND, "calls": calls, "reads": reads,
            "by_path": by_path, "misplaced": misplaced, "undeclared_rebindings": undeclared}
