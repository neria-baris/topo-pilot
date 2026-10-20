"""Build the in-memory index model: records, per-file facts, resolved edges, cycles, stats."""
import posixpath
from collections import defaultdict

from . import pyinfo, shinfo
from .resolve import Resolver
from .scan import list_tracked, read_file, sources_digest

PY_KINDS = ("python", "notebook")
SH_KINDS = ("powershell", "shell")


def import_text(rec):
    if rec["form"] == "import":
        return "import " + rec["names"][0]
    return "from " + "." * rec["level"] + rec["module"] + " import " + ", ".join(rec["names"])


def ancestors(paths):
    dirs = {"."}
    for p in paths:
        d = posixpath.dirname(p)
        while d and d not in dirs:
            dirs.add(d)
            d = posixpath.dirname(d)
    return dirs


def tarjan(nodes, out):
    """Iterative Tarjan SCC; returns the list of components (each a sorted list)."""
    index, low, on, stack, comps, counter = {}, {}, set(), [], [], [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(out.get(root, ())))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        on.add(root)
        while work:
            node, it = work[-1]
            advanced = False
            for nxt in it:
                if nxt not in index:
                    index[nxt] = low[nxt] = counter[0]
                    counter[0] += 1
                    stack.append(nxt)
                    on.add(nxt)
                    work.append((nxt, iter(out.get(nxt, ()))))
                    advanced = True
                    break
                if nxt in on:
                    low[node] = min(low[node], index[nxt])
            if advanced:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == node:
                        break
                comps.append(sorted(comp))
    return comps


def resolve_dynamic(dyn, path, resolver, sp_dirs, pyfiles):
    targets = sorted(p for p in dyn["paths"] if p in pyfiles and p != path)
    status = "internal" if targets else ""
    if not targets and dyn["literal"] and dyn["func"] != "spec_from_file_location":
        lit = dyn["literal"]
        if not lit.startswith("."):
            rec = {"form": "import", "names": [lit], "module": "", "level": 0}
            res = resolver.resolve(rec, path, sp_dirs)
            status, targets = res["status"], res["targets"]
    dyn["targets"] = targets
    dyn["status"] = status if targets or status in ("stdlib", "external") else "dynamic"
    dyn["label"] = dyn["literal"] if dyn["literal"] and dyn["func"] != (
        "spec_from_file_location") else f"dynamic: {dyn['expr']}"


def build_model(root):
    records = {}
    for name in list_tracked(root):
        rec = read_file(root, name)
        if rec is not None:
            records[name] = rec
    dirs = ancestors(records)
    pyfiles = {p for p, r in records.items() if r["kind"] == "python"}
    resolver = Resolver(pyfiles, dirs)
    code = sorted(p for p, r in records.items() if r["kind"] in PY_KINDS + SH_KINDS)
    code_set = set(code)
    py, sh = {}, {}
    for p in code:
        r = records[p]
        if r["kind"] in PY_KINDS:
            py[p] = pyinfo.extract(p, r["data"], dirs, r["kind"] == "notebook")
            r["purpose"] = py[p]["doc1"]
        else:
            text = r["data"].decode("utf-8", "replace")
            sh[p] = shinfo.extract(p, text, r["kind"], code_set)
    edges = set()
    stats = defaultdict(int)
    problems = []
    for p, info in py.items():
        sp_dirs = [d for e in info["syspath"] for d in e["dirs"]]
        for rec in info["imports"]:
            res = resolver.resolve(rec, p, sp_dirs)
            rec.update(res)
            stats[res["status"]] += 1
            for t in res["targets"]:
                edges.add((p, t, "import", rec["line"]))
            if res["status"] in ("ambiguous", "unresolved"):
                problems.append({"file": p, "line": rec["line"], "text": import_text(rec),
                                 "status": res["status"], "candidates": res["candidates"],
                                 "how": res["how"]})
        for dyn in info["dynamic"]:
            resolve_dynamic(dyn, p, resolver, sp_dirs, pyfiles)
            stats["dynamic_" + dyn["status"]] += 1
            for t in dyn["targets"]:
                edges.add((p, t, "dynamic", dyn["line"]))
    for p, info in sh.items():
        for inv in info["invokes"]:
            edges.add((p, inv["target"], "invoke", inv["line"]))
    edges = sorted(e for e in edges if e[0] in code_set and e[1] in code_set)
    out, inn = defaultdict(set), defaultdict(set)
    for s, d, _k, _l in edges:
        out[s].add(d)
        inn[d].add(s)
    comps = [c for c in tarjan(code, out) if len(c) > 1 or c[0] in out[c[0]]]
    return {
        "records": records, "code": code, "py": py, "sh": sh, "edges": edges,
        "out": {k: sorted(v) for k, v in out.items()},
        "inn": {k: sorted(v) for k, v in inn.items()},
        "cycles": sorted(comps), "stats": dict(sorted(stats.items())),
        "problems": sorted(problems, key=lambda x: (x["file"], x["line"], x["text"])),
        "digest": sources_digest(records),
    }
