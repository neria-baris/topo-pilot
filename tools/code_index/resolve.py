"""Import resolution against the tracked Python files (heuristics documented in README)."""
import posixpath
import re
import sys
from collections import defaultdict

STDLIB = frozenset(sys.stdlib_module_names)
SRC_ROOTS = {"topo_pilot": "src"}


def join(*parts):
    return posixpath.normpath(posixpath.join(*parts))


class Resolver:
    def __init__(self, pyfiles, dirs):
        self.py = set(pyfiles)
        self.dirs = set(dirs)
        self.tokens = set()  # digit-bearing prefixes of tracked module names (c1, x6s1, ...)
        self.step4 = defaultdict(set)  # bare name -> directories offering it
        for f in self.py:
            stem = f.rsplit("/", 1)[-1][:-3]
            if stem == "__init__":
                continue
            token = stem.split("_")[0]
            if re.search(r"\d", token):
                self.tokens.add(token)
            if stem == "conftest" or stem.startswith("test_"):
                continue
            self.step4[stem].add(posixpath.dirname(f) or ".")
        for f in self.py:
            if f.endswith("/__init__.py"):
                pkg = posixpath.dirname(f)
                self.step4[posixpath.basename(pkg)].add(posixpath.dirname(pkg) or ".")

    # -- helpers -------------------------------------------------------------------------
    def module_file(self, base, parts):
        """Walk `parts` from directory `base`. Returns (file or None, complete)."""
        cur, result, done = base, None, 0
        for part in parts:
            pkg, mod = join(cur, part, "__init__.py"), join(cur, part + ".py")
            if pkg in self.py:
                result, cur, done = pkg, join(cur, part), done + 1
            elif mod in self.py:
                return mod, True
            elif join(cur, part) in self.dirs:
                cur, done = join(cur, part), done + 1
            else:
                break
        return result, done == len(parts) and result is not None

    def pair_dirs(self, d):
        top, _, name = d.partition("/")
        name = name.split("/")[0]
        if top not in ("tests", "tools") or not name:
            return []
        other = "tools" if top == "tests" else "tests"
        out = []
        for e in sorted(self.dirs):
            if e.count("/") != 1 or not e.startswith(other + "/"):
                continue
            n = e.split("/")[1]
            if n == name or n.endswith("_" + name) or name.endswith("_" + n):
                out.append(e)
        return out

    def bare_steps(self, fpath, syspath_dirs, parts):
        here = posixpath.dirname(fpath) or "."
        steps = [("same directory", [here]), ("sys.path edit", sorted(set(syspath_dirs)))]
        if parts[0] not in STDLIB:
            steps.append(("paired directory", self.pair_dirs(here)))
            steps.append(("unique basename", sorted(self.step4.get(parts[0], ()))))
        return steps

    def find_module(self, fpath, syspath_dirs, parts):
        """Resolve a level-0 dotted name. Returns (status, files, how)."""
        if parts[0] in SRC_ROOTS:
            f, ok = self.module_file(SRC_ROOTS[parts[0]], parts)
            return ("internal", [f], "package root") if f else ("unresolved", [], "")
        for how, dirs in self.bare_steps(fpath, syspath_dirs, parts):
            found = sorted({f for d in dirs for f, ok in [self.module_file(d, parts)] if f})
            if len(found) == 1:
                return "internal", found, how
            if len(found) > 1:
                return "ambiguous", found, how
        if parts[0] in STDLIB:
            return "stdlib", [], ""
        if parts[0].split("_")[0] in self.tokens:
            return "unresolved", [], ""
        return "external", [], ""

    def submodules(self, mfile, base_dir, names):
        """Targets of `from M import names`: submodule files where they exist, else M."""
        pkg = posixpath.dirname(mfile) if mfile and mfile.endswith("/__init__.py") else base_dir
        out = []
        for n in names:
            sub = None
            if pkg is not None and n != "*":
                sub, ok = self.module_file(pkg, [n])
                if sub and not ok:
                    sub = None
            out.append(sub or mfile)
        return [o for o in out if o]

    # -- public --------------------------------------------------------------------------
    def resolve(self, rec, fpath, syspath_dirs):
        """Return dict(status, targets, candidates, how, top) for one import record."""
        parts = rec["module"].split(".") if rec["module"] else []
        if rec["form"] == "import":
            return self._one(fpath, syspath_dirs, rec["names"][0].split("."), None, 0)
        return self._one(fpath, syspath_dirs, parts, rec["names"], rec["level"])

    def _one(self, fpath, syspath_dirs, parts, names, level):
        top = parts[0] if parts else ""
        if level:
            base = posixpath.dirname(fpath) or "."
            for _ in range(level - 1):
                base = posixpath.dirname(base) or "."
            mfile, ok = (self.module_file(base, parts) if parts else (None, True))
            if parts and not ok:
                return {"status": "unresolved", "targets": [], "candidates": [],
                        "how": "relative", "top": "." * level + ".".join(parts)}
            if not parts and join(base, "__init__.py") in self.py:
                mfile = join(base, "__init__.py")
            base_dir = base if not parts else None
            targets = self.submodules(mfile, base_dir, names) if names else [mfile]
            targets = sorted({t for t in targets if t and t != fpath})
            status = "internal" if targets or mfile == fpath else "unresolved"
            return {"status": status, "targets": targets, "candidates": [],
                    "how": "relative", "top": "." * level + ".".join(parts)}
        status, files, how = self.find_module(fpath, syspath_dirs, parts)
        if status == "ambiguous":
            return {"status": status, "targets": [], "candidates": files, "how": how, "top": top}
        if status == "internal":
            targets = files
            if names:
                targets = self.submodules(files[0], None, names)
            targets = sorted({t for t in targets if t != fpath})
            return {"status": status, "targets": targets, "candidates": [], "how": how,
                    "top": top}
        return {"status": status, "targets": [], "candidates": [], "how": how, "top": top}
