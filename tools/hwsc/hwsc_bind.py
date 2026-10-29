"""HWSC versioned binding: the binding table, bound_stage_c() and the binding audit (API.md §2;
protocol §3.1-§3.2, RC-1). No existing file is edited: K4b/HWSB module attributes are rebound
for the duration of a `with` block and restored in `finally`."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import copy
import dataclasses
import hashlib
import importlib
import inspect
import json
import sys
import types
from contextlib import contextmanager
from pathlib import Path, PurePath

from c1_records import C1GateFailure

BINDING = "FAIL_TECHNICAL/BINDING"
ACTIVE = False


class _ContractMarker:
    def __init__(self, sha):
        self.sha = sha

    def matches(self, value) -> bool:
        return isinstance(value, dict) and value.get("protocol_sha256") == self.sha


def decode(value, repo=cc.REPO):
    if isinstance(value, list):
        return tuple(decode(v, repo) for v in value)
    if isinstance(value, dict) and len(value) == 1:
        (k, v), = value.items()
        if k == "__path__":
            return Path(v)
        if k == "__repo__":
            return Path(repo) / v
        if k == "__dict__":
            return dict(v)
        if k == "__contract_view__":
            return copy.deepcopy(cc.CONTRACT[v])
        if k == "__contract__":
            return _ContractMarker(v)
    return value


def _rows(contract) -> list:
    return [dict(r) for r in contract["binding"]["table"]]


def load_table(contract=None, which="stage_c", case=None, case_dir=None) -> list:
    contract = cc.CONTRACT if contract is None else contract
    rows = [{"module": r["module"], "name": r["name"], "old": decode(r["old"]),
             "new": decode(r["new"])} for r in _rows(contract)]
    if which == "stage_c":
        return rows
    if which == "identity":
        for r in rows:
            r["new"] = getattr(importlib.import_module(r["module"]), r["name"])
        return rows
    if which != "dry":
        raise ValueError(f"unknown table {which!r}")
    if case is None or case_dir is None:
        raise ValueError("the dry table needs case and case_dir")
    dry = {"MODELS": cc.DRY_MASTERS, "SCOPE": f"hwsc-v1/DRY/{case}",
           "PROCESS": ("cylinder", "overlap", "1.0"), "SEEDS": dict(cc.DRY_SEEDS)}
    for r in rows:
        if r["module"].startswith("k4b_") and r["name"] in dry:
            r["new"] = copy.copy(dry[r["name"]])
        elif (r["module"], r["name"]) == ("k4b_config", "STORE"):
            r["new"] = Path(case_dir)
        elif (r["module"], r["name"]) == ("k4b_driver", "ARTIFACTS"):
            r["new"] = Path(case_dir) / "artifacts"
    return rows


def _same(cur, old) -> bool:
    if isinstance(old, _ContractMarker):
        return old.matches(cur)
    if isinstance(old, PurePath):
        return isinstance(cur, PurePath) and cur.as_posix() == old.as_posix()
    return type(cur) is type(old) and cur == old


def check_old(rows) -> list:
    bad = []
    for r in rows:
        cur = getattr(importlib.import_module(r["module"]), r["name"])
        if not _same(cur, r["old"]):
            bad.append(f"{r['module']}.{r['name']}")
    return bad


def _encode(v):
    if isinstance(v, PurePath):
        return {"__path__": v.as_posix()}
    if isinstance(v, (tuple, list)):
        return [_encode(x) for x in v]
    if isinstance(v, _ContractMarker):
        return {"__contract__": v.sha}
    if isinstance(v, dict):
        return {str(k): _encode(x) for k, x in v.items()}
    return v


@contextmanager
def bound_stage_c(table=None):
    global ACTIVE
    rows = load_table() if table is None else table
    bad = check_old(rows)
    if bad:
        raise C1GateFailure(BINDING, f"code drift: {bad}")
    saved, was = [], ACTIVE
    try:
        for r in rows:
            mod = importlib.import_module(r["module"])
            saved.append((mod, r["name"], getattr(mod, r["name"])))
            setattr(mod, r["name"], r["new"])
        ACTIVE = True
        enc = json.dumps([{"module": r["module"], "name": r["name"], "new": _encode(r["new"])}
                          for r in rows], sort_keys=True, default=str)
        yield {"rows": len(rows), "table_sha256": hashlib.sha256(enc.encode()).hexdigest()}
    finally:
        for mod, name, obj in reversed(saved):
            setattr(mod, name, obj)
        ACTIVE = was


def never_called() -> tuple:
    return tuple(cc.CONTRACT["binding"]["never_called"])


# ------------------------------------------------------------------------- audit (§3.2 item 3)
def _norm(p) -> str:
    return str(p).replace("\\", "/").rstrip("/")


class _Forbidden:
    def __init__(self, f):
        self.tuples = [tuple(t) for t in f["tuples"]]
        self.key_sets = [set(k) for k in f["key_sets"]]
        self.strings, self.ints = set(f["strings"]), set(f["ints"])
        self.paths = {_norm(p) for p in f["paths"]}

    def hit(self, v):
        if isinstance(v, bool):
            return None
        if isinstance(v, int) and v in self.ints:
            return f"int {v}"
        if isinstance(v, str):
            if v in self.strings:
                return f"str {v}"
            if _norm(v) in self.paths:
                return f"path {v}"
        if isinstance(v, PurePath) and _norm(v.as_posix()) in self.paths:
            return f"path {v}"
        if isinstance(v, tuple) and v in self.tuples:
            return f"tuple {v}"
        if isinstance(v, (dict, set, frozenset)):
            try:
                keys = set(v)
            except TypeError:
                keys = None
            if keys is not None and any(keys == k for k in self.key_sets):
                return "key set"
            if isinstance(v, dict) and v.get("val_sd") == 610101:
                return "K4b seed dict"
        return None


def _walk(v, where, forb, out, depth=0, seen=None):
    seen = set() if seen is None else seen
    if depth > 6 or id(v) in seen:
        return
    h = forb.hit(v)
    if h:
        out.append((where, h))
    if isinstance(v, (tuple, list, set, frozenset)):
        seen.add(id(v))
        for i, x in enumerate(v):
            _walk(x, f"{where}[{i}]", forb, out, depth + 1, seen)
    elif isinstance(v, dict):
        seen.add(id(v))
        for k, x in v.items():
            _walk(k, f"{where}.key({k!r})", forb, out, depth + 1, seen)
            _walk(x, f"{where}[{k!r}]", forb, out, depth + 1, seen)
    elif dataclasses.is_dataclass(v) and not isinstance(v, type):
        seen.add(id(v))
        for f in dataclasses.fields(v):
            _walk(getattr(v, f.name), f"{where}.{f.name}", forb, out, depth + 1, seen)


def _functions(mod):
    for name, obj in vars(mod).items():
        if isinstance(obj, types.FunctionType) and obj.__module__ == mod.__name__:
            yield name, obj
        elif inspect.isclass(obj) and obj.__module__ == mod.__name__:
            for mn, mo in vars(obj).items():
                f = mo.__func__ if isinstance(mo, (staticmethod, classmethod)) else mo
                if isinstance(f, types.FunctionType):
                    yield f"{name}.{mn}", f


def scope_modules() -> list:
    dirs = [(cc.REPO / d).resolve() for d in cc.CONTRACT["binding"]["audit"]["module_dirs"]]
    out = []
    for mod in list(sys.modules.values()):
        f = getattr(mod, "__file__", None)
        if not f:
            continue
        p = Path(f).resolve()
        if any(p.parent == d for d in dirs):
            out.append(mod)
    return sorted(out, key=lambda m: m.__name__)


def audit(modules=None, left_unchanged=None, forbidden=None) -> dict:
    a = cc.CONTRACT["binding"]["audit"]
    mods = scope_modules() if modules is None else list(modules)
    left = cc.CONTRACT["binding"]["left_unchanged"] if left_unchanged is None else left_unchanged
    allowed = {(r["module"], r["name"]) for r in left}
    forb = _Forbidden(a["forbidden"] if forbidden is None else forbidden)
    hits = []
    for mod in mods:
        for name, v in list(vars(mod).items()):
            if (name.startswith("__") and name.endswith("__")) or isinstance(v, types.ModuleType):
                continue
            if callable(v) and not dataclasses.is_dataclass(v):
                continue
            found = []
            _walk(v, name, forb, found)
            hits += [{"module": mod.__name__, "where": w, "kind": "global", "hit": h,
                      "top": name} for w, h in found]
        for qual, fn in _functions(mod):
            for attr in ("__defaults__", "__kwdefaults__"):
                found = []
                _walk(getattr(fn, attr) or (), f"{qual}.{attr}", forb, found)
                hits += [{"module": mod.__name__, "where": w, "kind": "default", "hit": h,
                          "top": f"{qual}.{attr}"} for w, h in found]
    unlisted = [h for h in hits if (h["module"], h["top"]) not in allowed]
    return {"status": "PASS" if not unlisted else BINDING, "hits": hits, "unlisted": unlisted,
            "modules": [m.__name__ for m in mods], "n_hits": len(hits)}
