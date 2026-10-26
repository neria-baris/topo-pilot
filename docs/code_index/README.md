# Code index

Generated, deterministic index of the tracked code. Do not edit by hand; change `tools/build_code_index.py` (package `tools/code_index/`) instead.

Excluded by project rule (public research summary, for external readers only): `00_READ_ME_FIRST_Research_Summary_So_Far/`, `docs/research_summary/`. These paths are never opened or indexed.

## Regenerate and check

```text
.venv/Scripts/python.exe tools/build_code_index.py          # regenerate
.venv/Scripts/python.exe tools/build_code_index.py --check  # exit 1 if stale, no write
```

Input: `git ls-files` minus the excluded prefixes and minus `docs/code_index/` itself. No code is imported or executed (Python is parsed with `ast`). Output is sorted, has no timestamps, uses `/` separators, LF newlines and UTF-8.

Sources digest: `f11450450bd844c810211b9b007751e4176603b2d24eaa098689becd5e81f083`

## Layout

- [FILES.md](FILES.md): every indexed tracked file by directory (kind, size, purpose).
- `files/<path>.md`: one page per code file (`.py`, `.ps1`, `.sh`, `.ipynb`): imports, imported-by, constants, classes and functions with signatures and line ranges.
- [DEPENDENCIES.md](DEPENDENCIES.md): package graph, per-file adjacency, trees per entry-point group, cycles, unresolved and ambiguous imports.
- [FUNCTIONS.md](FUNCTIONS.md): alphabetical function/method/class key (several parts).
- [index.json](index.json): machine-readable data and `sources_digest`.

## Resolution rules and caveats

- `topo_pilot...` resolves under `src/topo_pilot` (`pkg/__init__.py` for packages). For `from topo_pilot.x import y`, the edge goes to submodule `y` when it exists, otherwise to `x`.
- Relative imports resolve from the importing file's directory.
- Bare names (`import c1_config`) are resolved in this order, stopping at the first step that finds a file: (1) the importing file's directory; (2) directories added by `sys.path.insert/append/extend` or `sys.path[...] =` when statically evaluable (literals, `Path(__file__).parents[n]`, `/` joins, `os.path.join`, module-level names and literal loop variables; otherwise the longest string-literal prefix that is a repo directory); (3) the paired `tests/<n>` <-> `tools/<m>` directory (same name, or one name ends with `_` plus the other); (4) a unique tracked basename elsewhere (excluding `conftest` and `test_*`). Standard-library names skip steps 3 and 4. Several candidates are reported as ambiguous; nothing is guessed.
- Imports not found anywhere are `stdlib` (`sys.stdlib_module_names`), `external` (third party), or `unresolved` when the name starts with a digit-bearing token shared with tracked modules (such as `c1`, `x6s1`).
- Dynamic imports record string literals of `importlib.import_module`, `__import__` and `spec_from_file_location`; everything else is shown as `dynamic: <expr>`.
- Edges also include shell/PowerShell script invocations (`invoke`) and resolved dynamic imports (`dynamic`). Imports inside functions are marked.
- Notebook code cells are parsed as Python on a best-effort basis; line numbers refer to the concatenated code cells.

## Counts at generation time

- files indexed: 862
- code files: 505
- python files: 504
- classes: 286
- functions and methods (incl. tests): 6917
- internal edges (file to file, with kind and line): 2060
- import statements, internal resolved: 2028
- import statements, internal ambiguous: 1
- import statements, internal unresolved: 0
- import statements, standard library: 2075
- import statements, external: 737
- dynamic imports, internal: 13
- dynamic imports, stdlib/external literal: 2
- dynamic imports, dynamic expression or unresolved: 7
- import cycles (strongly connected components): 6
