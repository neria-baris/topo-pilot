"""AST extraction for one Python source: docstring, imports, sys.path edits, symbols."""
import ast
import json
import re

from .pathval import evaluate, iter_nodes, norm
from .scan import clean

CONST_RE = re.compile(r"^_*[A-Z][A-Z0-9_]*$")
DYN_FUNCS = ("import_module", "__import__", "spec_from_file_location")


def notebook_source(data):
    """Concatenate code cells (magics blanked) of a notebook; best effort."""
    nb = json.loads(data.decode("utf-8", "replace"))
    chunks = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        src = "".join(src) if isinstance(src, list) else src
        lines = ["" if ln.lstrip().startswith(("%", "!")) else ln for ln in src.split("\n")]
        chunks.append("\n".join(lines))
    return "\n\n".join(chunks).encode("utf-8")


def args_str(a):
    def one(arg, default):
        text = arg.arg
        if arg.annotation is not None:
            text += ": " + ast.unparse(arg.annotation)
        if default is not None:
            text += (" = " if arg.annotation is not None else "=") + ast.unparse(default)
        return text

    parts = []
    pos = a.posonlyargs + a.args
    defaults = [None] * (len(pos) - len(a.defaults)) + list(a.defaults)
    for i, (arg, default) in enumerate(zip(pos, defaults)):
        parts.append(one(arg, default))
        if a.posonlyargs and i == len(a.posonlyargs) - 1:
            parts.append("/")
    if a.vararg:
        parts.append("*" + one(a.vararg, None))
    elif a.kwonlyargs:
        parts.append("*")
    parts += [one(arg, d) for arg, d in zip(a.kwonlyargs, a.kw_defaults)]
    if a.kwarg:
        parts.append("**" + one(a.kwarg, None))
    return ", ".join(parts)


def signature(node):
    text = ("async def " if isinstance(node, ast.AsyncFunctionDef) else "def ")
    text += f"{node.name}({args_str(node.args)})"
    if node.returns is not None:
        text += " -> " + ast.unparse(node.returns)
    return text


def doc_first_line(node):
    doc = ast.get_docstring(node)
    if not doc:
        return ""
    for line in doc.splitlines():
        if line.strip():
            return clean(line.strip())
    return ""


def first_paragraph(doc, limit=1500):
    para = doc.strip().split("\n\n")[0].strip()
    return clean(para[:limit] + (" ..." if len(para) > limit else ""))


class Collector:
    """Single pass over a module collecting imports, dynamic imports and sys.path edits."""

    def __init__(self, tree, path, dirset):
        self.path, self.dirset = path, dirset
        self.env = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        self.env.setdefault(t.id, []).append(node.value)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.value is not None:
                    self.env.setdefault(node.target.id, []).append(node.value)
            elif isinstance(node, ast.For) and isinstance(node.target, ast.Name):
                self.env.setdefault(node.target.id, []).extend(iter_nodes(node.iter, self.env))
        self.imports, self.dynamic, self.syspath = [], [], []
        self.visit(tree, False)

    def visit(self, node, lazy):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Import):
                for alias in child.names:
                    self.imports.append({"line": child.lineno, "form": "import", "level": 0,
                                         "module": "", "names": [alias.name], "lazy": lazy})
            elif isinstance(child, ast.ImportFrom):
                self.imports.append({"line": child.lineno, "form": "from",
                                     "level": child.level, "module": child.module or "",
                                     "names": [a.name for a in child.names], "lazy": lazy})
            elif isinstance(child, ast.Call):
                self.call(child)
            elif isinstance(child, ast.Assign):
                for t in child.targets:
                    if isinstance(t, ast.Subscript) and ast.unparse(t.value) == "sys.path":
                        self.add_syspath(child, child.value)
            elif isinstance(child, ast.AugAssign):
                if ast.unparse(child.target) == "sys.path":
                    self.add_syspath(child, child.value)
            fn = isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            self.visit(child, lazy or fn)

    def add_syspath(self, node, expr):
        values = [v for t, v in evaluate(expr, self.env, self.path) if t in "ps"]
        dirs = sorted({n for v in values for n in [norm(v)] if n in self.dirset})
        text = ast.unparse(expr)
        if not dirs:
            dirs = self.fallback(expr)
        self.syspath.append({"line": node.lineno, "expr": clean(text[:160]), "dirs": dirs})

    def fallback(self, expr):
        lits = sorted((n for n in ast.walk(expr)
                       if isinstance(n, ast.Constant) and isinstance(n.value, str)),
                      key=lambda n: (n.lineno, n.col_offset))
        parts = [n.value for n in lits]
        for k in range(len(parts), 0, -1):
            cand = norm("/".join(parts[:k]))
            if cand in self.dirset:
                return [cand]
        return []

    def call(self, node):
        name = ast.unparse(node.func)
        last = name.rsplit(".", 1)[-1]
        if name in ("sys.path.insert", "sys.path.append", "sys.path.extend") and node.args:
            self.add_syspath(node, node.args[-1])
        elif last in DYN_FUNCS and node.args:
            idx = 1 if last == "spec_from_file_location" and len(node.args) > 1 else 0
            main = node.args[idx]
            lit = main.value if isinstance(main, ast.Constant) and isinstance(
                main.value, str) else None
            paths = []
            if last == "spec_from_file_location":
                paths = sorted({norm(v) for t, v in evaluate(main, self.env, self.path)
                                if norm(v)})
                first = node.args[0]
                lit = first.value if isinstance(first, ast.Constant) and isinstance(
                    first.value, str) else None
            self.dynamic.append({"line": node.lineno, "func": last, "literal": lit,
                                 "expr": clean(ast.unparse(main)[:120]), "paths": paths})


def symbols(tree, path):
    is_test = path.rsplit("/", 1)[-1].startswith("test_") or path.endswith("_test.py")
    out, consts = [], []

    def walk(body, prefix, in_class):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                kind = "method" if in_class else "function"
                if is_test and node.name.startswith("test"):
                    kind = "test"
                out.append({
                    "kind": kind, "name": node.name, "qual": prefix + node.name,
                    "sig": signature(node), "decorators": [ast.unparse(d) for d in
                                                           node.decorator_list],
                    "start": node.lineno, "end": node.end_lineno, "doc": doc_first_line(node)})
            elif isinstance(node, ast.ClassDef):
                out.append({
                    "kind": "class", "name": node.name, "qual": prefix + node.name,
                    "bases": [ast.unparse(b) for b in node.bases + [k.value for k in
                                                                    node.keywords]],
                    "decorators": [ast.unparse(d) for d in node.decorator_list],
                    "start": node.lineno, "end": node.end_lineno, "doc": doc_first_line(node)})
                walk(node.body, prefix + node.name + ".", True)
            elif isinstance(node, (ast.If, ast.Try, ast.With, ast.For, ast.While)):
                for field in ("body", "orelse", "finalbody"):
                    walk(getattr(node, field, []), prefix, in_class)
                for handler in getattr(node, "handlers", []):
                    walk(handler.body, prefix, in_class)
            elif not in_class and isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                consts.extend(t.id for t in targets
                              if isinstance(t, ast.Name) and CONST_RE.match(t.id))

    walk(tree.body, "", False)
    return sorted(out, key=lambda s: (s["start"], s["qual"])), sorted(set(consts))


def extract(path, data, dirset, is_notebook=False):
    info = {"doc": "", "doc1": "", "imports": [], "dynamic": [], "syspath": [],
            "constants": [], "symbols": [], "error": ""}
    try:
        if is_notebook:
            data = notebook_source(data)
        tree = ast.parse(data, filename=path)
    except (SyntaxError, ValueError) as exc:
        info["error"] = clean(f"{type(exc).__name__}: {exc}")[:200]
        return info
    doc = ast.get_docstring(tree) or ""
    info["doc"] = first_paragraph(doc) if doc else ""
    info["doc1"] = doc_first_line(tree)
    col = Collector(tree, path, dirset)
    info["imports"], info["dynamic"], info["syspath"] = col.imports, col.dynamic, col.syspath
    info["symbols"], info["constants"] = symbols(tree, path)
    return info
