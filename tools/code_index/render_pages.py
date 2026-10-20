"""Per-code-file pages: docs/code_index/files/<path>.md."""
import posixpath

from .model import import_text
from .scan import OUT_DIR


def code(text):
    text = str(text).replace("\n", " ")
    return f"`` {text} ``" if "`" in text else f"`{text}`"


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def page_path(path):
    return f"files/{path}.md"


def link_page(src_page_dir, target):
    return posixpath.relpath(page_path(target), src_page_dir)


def link_source(path, page_rel):
    """Relative link from an index page to the repo file (index lives in docs/code_index)."""
    page_dir = posixpath.dirname(f"{OUT_DIR}/{page_rel}")
    return posixpath.relpath(path, page_dir)


def lines_text(nums):
    return ", ".join(str(n) for n in sorted(set(nums)))


def imports_section(path, info, page_dir):
    groups = {"internal": [], "external": {}, "stdlib": {}, "unresolved": [], "ambiguous": []}
    for rec in info["imports"]:
        lazy = " (inside a function)" if rec["lazy"] else ""
        st = rec["status"]
        if st == "internal":
            links = ", ".join(f"[{t}]({link_page(page_dir, t)})" for t in rec["targets"])
            via = rec["how"]
            groups["internal"].append(
                f"- {code(import_text(rec))} -> {links or 'itself'} (line {rec['line']}, via {via})"
                + lazy)
        elif st in ("external", "stdlib"):
            groups[st].setdefault(rec["top"], []).append(rec["line"])
        elif st == "ambiguous":
            cands = ", ".join(code(c) for c in rec["candidates"])
            groups["ambiguous"].append(f"- {code(import_text(rec))} (line {rec['line']}): {cands}")
        else:
            groups["unresolved"].append(f"- {code(import_text(rec))} (line {rec['line']})")
    out = ["## Imports", ""]
    out += ["### Internal (repo files)", ""] + (groups["internal"] or ["- none"]) + [""]
    for title, key in (("External (third-party)", "external"), ("Standard library", "stdlib")):
        out += [f"### {title}", ""]
        items = groups[key]
        out += [f"- `{k}` (lines {lines_text(v)})" for k, v in sorted(items.items())] or [
            "- none"]
        out.append("")
    out += ["### Unresolved internal-looking imports", ""]
    out += (groups["unresolved"] or ["- none"]) + [""]
    out += ["### Ambiguous imports (several candidate files)", ""]
    out += (groups["ambiguous"] or ["- none"]) + [""]
    out += ["### Dynamic imports", ""]
    for dyn in info["dynamic"]:
        tgt = ", ".join(f"[{t}]({link_page(page_dir, t)})" for t in dyn["targets"])
        out.append(f"- {code(dyn['func'])} line {dyn['line']}: {code(dyn['label'])}"
                   + (f" -> {tgt}" if tgt else ""))
    out += ["- none"] if not info["dynamic"] else []
    out += ["", "### sys.path additions", ""]
    for sp in info["syspath"]:
        dirs = ", ".join(code(d) for d in sp["dirs"]) or "not statically determinable"
        out.append(f"- line {sp['line']}: {code(sp['expr'])} -> {dirs}")
    out += ["- none"] if not info["syspath"] else []
    return out + [""]


def symbols_section(info, notebook):
    out = ["## Classes and functions", ""]
    if notebook:
        out += ["Line numbers refer to the concatenated code cells.", ""]
    if not info["symbols"]:
        return out + ["- none", ""]
    for s in info["symbols"]:
        span = f"L{s['start']}-{s['end']}"
        deco = "".join(f" @{d}" for d in s["decorators"])
        doc = f" - {s['doc']}" if s["doc"] else ""
        if s["kind"] == "class":
            bases = f"({', '.join(s['bases'])})" if s["bases"] else ""
            out.append(f"- **class {code(s['qual'] + bases)}** [{span}]{_deco(deco)}{doc}")
        else:
            out.append(f"- **{s['kind']} {code(s['qual'])}** [{span}]: {code(s['sig'])}"
                       f"{_deco(deco)}{doc}")
    return out + [""]


def _deco(deco):
    return f" decorators:{deco}" if deco else ""


def py_page(path, rec, info, inn_edges):
    rel = page_path(path)
    page_dir = posixpath.dirname(rel)
    out = [f"# {code(path)}", "", f"- Source: [{path}]({link_source(path, rel)})",
           f"- Kind: {rec['kind']}", f"- Lines: {rec['lines']}"]
    if info["error"]:
        out.append(f"- Parse error: {code(info['error'])}")
    out += ["", "## Module docstring", ""]
    out += [f"> {ln}" if ln else ">" for ln in info["doc"].split("\n")] if info["doc"] else [
        "(none)"]
    out += [""] + imports_section(path, info, page_dir)
    out += ["## Imported by", ""]
    rows = sorted(inn_edges)
    out += [f"- [{s}]({link_page(page_dir, s)}) (line {ln}, {kind})" for s, kind, ln in rows] or [
        "- none"]
    out += ["", "## Top-level constants", ""]
    out += [f"- `{c}`" for c in info["constants"]] or ["- none"]
    out.append("")
    return "\n".join(out + symbols_section(info, rec["kind"] == "notebook")) + "\n"


def sh_page(path, rec, info, inn_edges):
    rel = page_path(path)
    page_dir = posixpath.dirname(rel)
    out = [f"# {code(path)}", "", f"- Source: [{path}]({link_source(path, rel)})",
           f"- Kind: {rec['kind']}", f"- Lines: {rec['lines']}",
           f"- Purpose: {rec['purpose'] or '(none)'}", "", "## Functions", ""]
    out += [f"- {code(f['name'])} (line {f['line']})" for f in info["functions"]] or ["- none"]
    out += ["", "## Invoked repo scripts", ""]
    out += [f"- {code(i['token'])} -> [{i['target']}]({link_page(page_dir, i['target'])})"
            f" (line {i['line']})" for i in info["invokes"]] or ["- none"]
    out += ["", "## Invoked by", ""]
    out += [f"- [{s}]({link_page(page_dir, s)}) (line {ln}, {kind})"
            for s, kind, ln in sorted(inn_edges)] or ["- none"]
    return "\n".join(out) + "\n"
