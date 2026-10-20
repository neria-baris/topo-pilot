"""FILES.md, FUNCTIONS*.md, index.json and README.md."""
import json
import posixpath
from collections import defaultdict

from .render_pages import cell, code, page_path
from .scan import EXCLUDE

EXCLUSION_NOTE = (
    "Excluded by project rule (public research summary, for external readers only): "
    + ", ".join(f"`{p}`" for p in EXCLUDE) + ". These paths are never opened or indexed.")
CHUNK_BYTES = 700_000


def size_text(rec):
    return f"{rec['bytes']} bytes" if not rec["text"] else f"{rec['lines']} lines"


def files_md(model):
    recs = model["records"]
    by_dir = defaultdict(list)
    for p in sorted(recs):
        by_dir[posixpath.dirname(p) or "."].append(p)
    out = ["# Files", "", EXCLUSION_NOTE, "",
           "The generated index itself (`docs/code_index/`) is not indexed. "
           f"{len(recs)} tracked files; {len(model['code'])} code files (linked to their pages).",
           ""]
    for d in sorted(by_dir):
        out += [f"## {d}/" if d != "." else "## (repo root)", "",
                "| File | Kind | Size | Purpose |", "|---|---|---|---|"]
        for p in by_dir[d]:
            r = recs[p]
            name = posixpath.basename(p)
            shown = (f"[{name}]({page_path(p)})" if p in model["py"] or p in model["sh"]
                     else f"`{name}`")
            out.append(f"| {shown} | {r['kind']} | {size_text(r)} | {cell(r['purpose'])} |")
        out.append("")
    return "\n".join(out)


def function_rows(model):
    rows = []
    for p, info in model["py"].items():
        for s in info["symbols"]:
            rows.append((s["name"], s["kind"], s["qual"], p, s["start"], s["doc"]))
    for p, info in model["sh"].items():
        for f in info["functions"]:
            rows.append((f["name"], "function", f["name"], p, f["line"], ""))
    return sorted(rows, key=lambda r: (r[0].lower(), r[0], r[2], r[3], r[4]))


def functions_md(model):
    rows = function_rows(model)
    chunks, cur, size = [], [], 0
    for row in rows:
        line = (f"| {cell(code(row[0]))} | {row[1]} | {cell(code(row[2]))} | "
                f"[{row[3]}:{row[4]}](../../{row[3]}#L{row[4]}) | {cell(row[5])} |")
        if cur and size + len(line) > CHUNK_BYTES:
            chunks.append(cur)
            cur, size = [], 0
        cur.append((row, line))
        size += len(line) + 1
    if cur:
        chunks.append(cur)
    head = ["| Name | Kind | Qualified name | Location | First docstring line |",
            "|---|---|---|---|---|"]
    outputs = {}
    index = ["# Function key", "",
             f"{len(rows)} classes, functions and methods, alphabetical (case-insensitive).", "",
             "| Page | First name | Last name | Entries |", "|---|---|---|---|"]
    for i, chunk in enumerate(chunks, 1):
        name = f"FUNCTIONS_{i:02d}.md"
        outputs[name] = "\n".join([f"# Function key, part {i} of {len(chunks)}", ""] + head
                                  + [ln for _r, ln in chunk]) + "\n"
        index.append(f"| [{name}]({name}) | {code(chunk[0][0][0])} | "
                     f"{code(chunk[-1][0][0])} | {len(chunk)} |")
    outputs["FUNCTIONS.md"] = "\n".join(index) + "\n"
    return outputs


def index_json(model, counts):
    files = {}
    for p, r in sorted(model["records"].items()):
        entry = {"kind": r["kind"], "sha256": r["sha256"], "purpose": r["purpose"]}
        entry["bytes" if not r["text"] else "lines"] = r.get("bytes", r.get("lines"))
        files[p] = entry
    data = {
        "schema": 1, "sources_digest": model["digest"], "excluded_prefixes": list(EXCLUDE),
        "counts": counts, "files": files, "python": model["py"], "shell": model["sh"],
        "edges": [list(e) for e in model["edges"]], "cycles": model["cycles"],
        "problems": model["problems"],
    }
    return json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def readme_md(model, counts):
    return "\n".join([
        "# Code index", "",
        "Generated, deterministic index of the tracked code. Do not edit by hand; change "
        "`tools/build_code_index.py` (package `tools/code_index/`) instead.", "",
        EXCLUSION_NOTE, "",
        "## Regenerate and check", "",
        "```text", ".venv/Scripts/python.exe tools/build_code_index.py          # regenerate",
        ".venv/Scripts/python.exe tools/build_code_index.py --check  # exit 1 if stale, no write",
        "```", "",
        "Input: `git ls-files` minus the excluded prefixes and minus `docs/code_index/` itself. "
        "No code is imported or executed (Python is parsed with `ast`). Output is sorted, "
        "has no timestamps, uses `/` separators, LF newlines and UTF-8.", "",
        f"Sources digest: `{model['digest']}`", "",
        "## Layout", "",
        "- [FILES.md](FILES.md): every indexed tracked file by directory (kind, size, purpose).",
        "- `files/<path>.md`: one page per code file (`.py`, `.ps1`, `.sh`, `.ipynb`): imports, "
        "imported-by, constants, classes and functions with signatures and line ranges.",
        "- [DEPENDENCIES.md](DEPENDENCIES.md): package graph, per-file adjacency, trees per "
        "entry-point group, cycles, unresolved and ambiguous imports.",
        "- [FUNCTIONS.md](FUNCTIONS.md): alphabetical function/method/class key (several parts).",
        "- [index.json](index.json): machine-readable data and `sources_digest`.", "",
        "## Resolution rules and caveats", "",
        "- `topo_pilot...` resolves under `src/topo_pilot` (`pkg/__init__.py` for packages). "
        "For `from topo_pilot.x import y`, the edge goes to submodule `y` when it exists, "
        "otherwise to `x`.",
        "- Relative imports resolve from the importing file's directory.",
        "- Bare names (`import c1_config`) are resolved in this order, stopping at the first "
        "step that finds a file: (1) the importing file's directory; (2) directories added by "
        "`sys.path.insert/append/extend` or `sys.path[...] =` when statically evaluable "
        "(literals, `Path(__file__).parents[n]`, `/` joins, `os.path.join`, module-level names "
        "and literal loop variables; otherwise the longest string-literal prefix that is a repo "
        "directory); (3) the paired `tests/<n>` <-> `tools/<m>` directory (same name, or one "
        "name ends with `_` plus the other); (4) a unique tracked basename elsewhere "
        "(excluding `conftest` and `test_*`). Standard-library names skip steps 3 and 4. "
        "Several candidates are reported as ambiguous; nothing is guessed.",
        "- Imports not found anywhere are `stdlib` (`sys.stdlib_module_names`), `external` "
        "(third party), or `unresolved` when the name starts with a digit-bearing token shared "
        "with tracked modules (such as `c1`, `x6s1`).",
        "- Dynamic imports record string literals of `importlib.import_module`, `__import__` "
        "and `spec_from_file_location`; everything else is shown as `dynamic: <expr>`.",
        "- Edges also include shell/PowerShell script invocations (`invoke`) and resolved dynamic "
        "imports (`dynamic`). Imports inside functions are marked.",
        "- Notebook code cells are parsed as Python on a best-effort basis; line numbers refer "
        "to the concatenated code cells.", "",
        "## Counts at generation time", "",
        *[f"- {k}: {v}" for k, v in counts.items()], "",
    ])
