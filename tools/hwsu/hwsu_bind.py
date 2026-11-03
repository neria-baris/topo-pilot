"""HWSU call allowlist and constant-read audit (API.md §7; protocol §11.2; run by OF-B, RC-10)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import ast
import fnmatch
import importlib
import inspect
import types
from pathlib import Path

MISSING = object()


def module_imports(tree) -> dict:
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            for a in node.names:
                out[a.asname or a.name] = (node.module, a.name)
    return out


def references(path) -> list:
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    imp = module_imports(tree)
    mods = {k: v for k, v in imp.items() if isinstance(v, str)}
    refs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id in mods:
            refs.append({"module": mods[node.value.id], "name": node.attr, "line": node.lineno})
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            refs += [{"module": node.module, "name": a.name, "line": node.lineno, "from": True}
                     for a in node.names]
    return refs


def _never(module, name, patterns) -> bool:
    full = f"{module}.{name}"
    return any(fnmatch.fnmatchcase(full, str(p).split()[0]) for p in patterns)


def _default_files() -> list:
    listed = {uc.REPO / p for p in uc.CONTRACT["phase1_files"]
              if Path(p).name.startswith("hwsu_") and p.endswith(".py")}
    return sorted(p for p in listed | set(uc.HERE.glob("hwsu_*.py")) if p.is_file())


EXPLICIT = {("hwsb_known", "classify_hits"): ((1, "fragments"), (2, "job_scratch")),
            ("hwsb_data", "build_process"): ((1, "masters"),),
            ("hwsb_dry", "build_tiny_process"): ((1, "masters"),)}


def argument_less(path) -> list:
    """Calls of the accepted conditional-read functions without their explicit arguments."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    mods = {k: v for k, v in module_imports(tree).items() if isinstance(v, str)}
    bad = []
    for n in ast.walk(tree):
        f = n.func if isinstance(n, ast.Call) else None
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in mods:
            key = (mods[f.value.id], f.attr)
            if key in EXPLICIT:
                have = {k.arg for k in n.keywords}
                if any(len(n.args) <= pos and name not in have for pos, name in EXPLICIT[key]):
                    bad.append({"module": key[0], "name": key[1], "line": n.lineno})
    return bad


def audit_calls(files=None, contract=None) -> dict:
    b = (uc.CONTRACT if contract is None else contract)["binding"]
    ext, allow, froms = set(b["external_ok"]), b["allowlist"], b["from_imports"]
    meters = b.get("meter_modules", {})
    unlisted, never, n = [], [], 0
    for f in _default_files() if files is None else [Path(x) for x in files]:
        unlisted += [dict(r, file=Path(f).name, why="argument-less call") for r in argument_less(f)]
        for r in references(f):
            n += 1
            mod, name = r["module"], r["name"]
            row = dict(r, file=Path(f).name)
            if _never(mod, name, b["never_called"]):
                never.append(row)
            ok = (mod.startswith("hwsu_") or mod in ext or name in allow.get(mod, {})
                  or name in meters.get(mod, []))
            if r.get("from"):
                ok = mod in ext or name in froms.get(mod, [])
            if not ok:
                unlisted.append(row)
    return {"status": "PASS" if not (unlisted or never) else "FAIL_TECHNICAL/BINDING",
            "unlisted": unlisted, "never_called": never, "n_refs": n}


# ------------------------------------------------------------------------ constant reads (D-25)
def _tools_path(f) -> bool:
    parts = Path(f).resolve().parts
    return "tools" in parts and "src" not in parts


def _under_tools(obj) -> bool:
    try:
        f = inspect.getsourcefile(obj)
    except (TypeError, OSError):
        return False
    return bool(f) and _tools_path(f)


def _tool_module(mod) -> bool:
    f = getattr(mod, "__file__", None)
    return bool(f) and _tools_path(f)


def _locals(tree) -> set:
    names, imports = set(), {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            names.add(n.id)
        elif isinstance(n, ast.arg):
            names.add(n.arg)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            names.add(n.name)
        elif isinstance(n, ast.Import):
            for a in n.names:
                imports[a.asname or a.name.split(".")[0]] = a.name
                names.add(a.asname or a.name.split(".")[0])
    return names, imports


def _resolve(mod, qualname):
    obj = mod
    for part in qualname.split("."):
        obj = getattr(obj, part)
    return obj


def function_reads(module, qualname) -> dict:
    reads, seen = {}, set()

    def note(mod, name, sub=None):
        key = f'{mod.__name__}.{name}' + (f'["{sub}"]' if sub is not None else "")
        reads[key] = True

    def classify(mod, name, sub, visit):
        val = getattr(mod, name, MISSING)
        if isinstance(val, types.ModuleType):
            return
        if callable(val) and val is not MISSING:
            if _under_tools(val):
                visit(val)
            return
        if _tool_module(mod):
            note(mod, name, sub)

    def visit_obj(obj):
        if id(obj) in seen:
            return
        seen.add(id(obj))
        mod = importlib.import_module(obj.__module__)
        try:
            src = inspect.getsource(obj)
            tree = ast.parse(("if 1:" + chr(10) + src) if src[:1].isspace() else src)
        except (OSError, TypeError):
            return
        loc, imports = _locals(tree)
        parent = {id(c): p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}

        def sub_of(node):
            up = parent.get(id(node))
            if isinstance(up, ast.Subscript) and up.value is node and isinstance(
                    up.slice, ast.Constant) and isinstance(up.slice.value, str):
                return up.slice.value
            return None

        for n in ast.walk(tree):
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
                base = n.value.id
                if base in imports:
                    target = importlib.import_module(imports[base])
                elif base in loc:
                    continue
                else:
                    target = getattr(mod, base, MISSING)
                if isinstance(target, types.ModuleType) and _tool_module(target):
                    classify(target, n.attr, sub_of(n), visit_obj)
            elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id not in loc:
                if hasattr(mod, n.id):
                    classify(mod, n.id, sub_of(n), visit_obj)

    m = importlib.import_module(module) if isinstance(module, str) else module
    visit_obj(_resolve(m, qualname))
    return reads


def audit_reads(contract=None) -> dict:
    b = (uc.CONTRACT if contract is None else contract)["binding"]
    cond = {(c["function"], c["read"]) for c in b.get("conditional_reads", [])}
    forb = set(b["forbidden_reads"])
    unlisted, forbidden = [], []
    for mod, names in b["allowlist"].items():
        for name, entry in names.items():
            if entry.get("kind") != "function":
                continue
            try:
                m = importlib.import_module(mod)
                obj = _resolve(m, name)
            except (ImportError, AttributeError) as exc:
                unlisted.append({"function": f"{mod}.{name}", "problem": repr(exc)})
                continue
            if not _under_tools(obj):
                continue
            got, want = set(function_reads(mod, name)), set(entry.get("call_time_reads", {}))
            if got != want:
                unlisted.append({"function": f"{mod}.{name}", "extra": sorted(got - want),
                                 "missing": sorted(want - got)})
            for key in sorted(got):
                last = key.rsplit(".", 1)[-1] if "[" not in key else key.split(".", 1)[1]
                bad = last in forb or (last.startswith("CONTRACT[")
                                       and key != 'hwsc_config.CONTRACT["world"]')
                if bad and (f"{mod}.{name}", key) not in cond:
                    forbidden.append({"function": f"{mod}.{name}", "read": key})
    return {"status": "PASS" if not (unlisted or forbidden) else "FAIL_TECHNICAL/BINDING",
            "unlisted": unlisted, "forbidden": forbidden}


def audit(files=None, contract=None) -> dict:
    calls, reads = audit_calls(files, contract), audit_reads(contract)
    ok = calls["status"] == "PASS" and reads["status"] == "PASS"
    return {"status": "PASS" if ok else "FAIL_TECHNICAL/BINDING", "calls": calls, "reads": reads}
