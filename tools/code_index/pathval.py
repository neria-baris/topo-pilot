"""Best-effort static evaluation of path expressions (used for sys.path and dynamic imports).

Values are lists of alternatives `(tag, text)` where tag is "p" (repo-relative posix path,
"." = repo root) or "s" (plain string). Nothing is executed.
"""
import ast
import copy
import itertools
import posixpath

MAX_ALT = 16
PATH_CTORS = ("Path", "PurePath", "PurePosixPath", "PureWindowsPath")
PASS_METHODS = ("resolve", "absolute", "as_posix", "expanduser")
PASS_FUNCS = ("str", "os.fspath", "os.path.abspath", "os.path.realpath", "os.path.normpath")


def norm(text):
    text = text.replace("\\", "/")
    if text.startswith("/") or (len(text) > 1 and text[1] == ":"):
        return None
    out = posixpath.normpath(text)
    return None if out == ".." or out.startswith("../") else out


def _join(parts):
    items = []
    for _tag, text in parts:
        text = text.replace("\\", "/")
        if text.startswith("/") or (len(text) > 1 and text[1] == ":"):
            return None
        items.append(text)
    return norm(posixpath.join(*items)) if items else None


def _cap(values):
    seen = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return seen[:MAX_ALT]


def _parent(path):
    if path in (".", ""):
        return None
    return posixpath.dirname(path) or "."


class _Subst(ast.NodeTransformer):
    def __init__(self, name, value):
        self.name, self.value = name, value

    def visit_Name(self, node):  # noqa: N802
        return self.value if node.id == self.name else node


def iter_nodes(node, env, depth=0):
    """Element nodes of a literal iterable (directly, through a Name, `+`, or a comprehension)."""
    if depth > 6:
        return []
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return list(node.elts)
    if isinstance(node, ast.Name):
        return [e for n in env.get(node.id, []) for e in iter_nodes(n, env, depth + 1)]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return iter_nodes(node.left, env, depth + 1) + iter_nodes(node.right, env, depth + 1)
    if isinstance(node, (ast.ListComp, ast.GeneratorExp)) and len(node.generators) == 1:
        gen = node.generators[0]
        if isinstance(gen.target, ast.Name):
            return [_Subst(gen.target.id, e).visit(copy.deepcopy(node.elt))
                    for e in iter_nodes(gen.iter, env, depth + 1)]
    return []


def _args(call, env, fpath, depth):
    """Argument sequences (each a list of alternative-lists); starred literals are expanded."""
    seqs = [[]]
    for arg in call.args:
        if isinstance(arg, ast.Starred):
            tuples = env.get(arg.value.id, []) if isinstance(arg.value, ast.Name) else [arg.value]
            tuples = [t for t in tuples if isinstance(t, (ast.List, ast.Tuple))]
            seqs = [seq + [evaluate(e, env, fpath, depth + 1) for e in t.elts]
                    for seq in seqs for t in tuples]
        else:
            seqs = [seq + [evaluate(arg, env, fpath, depth + 1)] for seq in seqs]
    return seqs


def evaluate(node, env, fpath, depth=0):
    if depth > 14:
        return []

    def ev(n):
        return evaluate(n, env, fpath, depth + 1)

    if isinstance(node, ast.Constant):
        return [("s", node.value)] if isinstance(node.value, str) else []
    if isinstance(node, ast.Name):
        if node.id == "__file__":
            return [("p", fpath)]
        return _cap(v for n in env.get(node.id, []) for v in ev(n))
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return _cap(v for e in node.elts if not isinstance(e, ast.Starred) for v in ev(e))
    if isinstance(node, ast.IfExp):
        return _cap(ev(node.body) + ev(node.orelse))
    if isinstance(node, (ast.ListComp, ast.GeneratorExp)) and len(node.generators) == 1:
        gen = node.generators[0]
        if isinstance(gen.target, ast.Name):
            env2 = dict(env)
            env2[gen.target.id] = iter_nodes(gen.iter, env)
            return _cap(evaluate(node.elt, env2, fpath, depth + 1))
        return []
    if isinstance(node, ast.Attribute) and node.attr == "parent":
        return _cap(("p", d) for t, v in ev(node.value) if t == "p"
                    for d in [_parent(v)] if d is not None)
    if isinstance(node, ast.Subscript):
        base, idx = node.value, node.slice
        if (isinstance(base, ast.Attribute) and base.attr == "parents"
                and isinstance(idx, ast.Constant) and isinstance(idx.value, int)):
            out = []
            for tag, val in ev(base.value):
                for _ in range(idx.value + 1):
                    val = _parent(val) if val is not None else None
                if tag == "p" and val is not None:
                    out.append(("p", val))
            return _cap(out)
        return []
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        res = (_join([a, b]) for a in ev(node.left) for b in ev(node.right))
        return _cap(("p", r) for r in res if r is not None)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _cap(("s", a[1] + b[1]) for a in ev(node.left) for b in ev(node.right)
                    if a[0] == b[0] == "s")
    if isinstance(node, ast.Call):
        return _call(node, env, fpath, depth, ev)
    return []


def _call(node, env, fpath, depth, ev):
    name = ast.unparse(node.func)
    last = name.rsplit(".", 1)[-1]
    if last in PATH_CTORS or name == "os.path.join" or last == "joinpath":
        out = []
        for lists in _args(node, env, fpath, depth):
            if last == "joinpath" and isinstance(node.func, ast.Attribute):
                lists = [ev(node.func.value)] + lists
            if lists:
                res = (_join(list(c)) for c in itertools.islice(itertools.product(*lists), 200))
                out += [("p", r) for r in res if r is not None]
        return _cap(out)
    if name == "os.path.dirname" and node.args:
        return _cap(("p", d) for t, v in ev(node.args[0]) for d in [_parent(v)] if d)
    if name in PASS_FUNCS and node.args:
        return _cap(ev(node.args[0]))
    if last in PASS_METHODS and isinstance(node.func, ast.Attribute):
        return _cap(ev(node.func.value))
    return []
