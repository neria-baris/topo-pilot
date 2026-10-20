"""Assemble all index outputs in memory; write them or compare them with the disk copy."""
import argparse
import sys
from collections import defaultdict

from . import render_deps, render_lists, render_pages
from .model import build_model
from .scan import OUT_DIR, REPO

PY_KINDS = ("python", "notebook")


def counts_of(model):
    syms = [s for info in model["py"].values() for s in info["symbols"]]
    st = model["stats"]
    return {
        "files indexed": len(model["records"]),
        "code files": len(model["code"]),
        "python files": len(model["py"]),
        "classes": sum(1 for s in syms if s["kind"] == "class"),
        "functions and methods (incl. tests)": sum(1 for s in syms if s["kind"] != "class"),
        "internal edges (file to file, with kind and line)": len(model["edges"]),
        "import statements, internal resolved": st.get("internal", 0),
        "import statements, internal ambiguous": st.get("ambiguous", 0),
        "import statements, internal unresolved": st.get("unresolved", 0),
        "import statements, standard library": st.get("stdlib", 0),
        "import statements, external": st.get("external", 0),
        "dynamic imports, internal": st.get("dynamic_internal", 0),
        "dynamic imports, stdlib/external literal": st.get("dynamic_stdlib", 0)
        + st.get("dynamic_external", 0),
        "dynamic imports, dynamic expression or unresolved": st.get("dynamic_dynamic", 0)
        + st.get("dynamic_unresolved", 0) + st.get("dynamic_ambiguous", 0),
        "import cycles (strongly connected components)": len(model["cycles"]),
    }


def generate(root=REPO):
    """Return ({relative output path: bytes}, counts)."""
    model = build_model(root)
    counts = counts_of(model)
    inn = defaultdict(list)
    for src, dst, kind, line in model["edges"]:
        inn[dst].append((src, kind, line))
    out = {
        "README.md": render_lists.readme_md(model, counts),
        "FILES.md": render_lists.files_md(model),
        "DEPENDENCIES.md": render_deps.render(model),
        "index.json": render_lists.index_json(model, counts),
    }
    out.update(render_lists.functions_md(model))
    for p in model["code"]:
        rec = model["records"][p]
        if p in model["py"]:
            text = render_pages.py_page(p, rec, model["py"][p], inn.get(p, []))
        else:
            text = render_pages.sh_page(p, rec, model["sh"][p], inn.get(p, []))
        out[render_pages.page_path(p)] = text
    return {k: v.encode("utf-8") for k, v in sorted(out.items())}, counts


def existing(base):
    return {f.relative_to(base).as_posix(): f for f in sorted(base.rglob("*")) if f.is_file()}


def write(root, outputs):
    base = root / OUT_DIR
    have = existing(base) if base.exists() else {}
    for rel, path in have.items():
        if rel not in outputs:
            path.unlink()
    for rel, data in outputs.items():
        target = base / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
    for d in sorted((p for p in base.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def check(root, outputs):
    base = root / OUT_DIR
    have = existing(base) if base.exists() else {}
    diffs = [f"stale (not generated any more): {r}" for r in have if r not in outputs]
    diffs += [f"missing: {r}" for r in outputs if r not in have]
    diffs += [f"changed: {r}" for r, d in outputs.items() if r in have
              and have[r].read_bytes() != d]
    return diffs


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate or check the code index (docs/code_index).")
    ap.add_argument("--check", action="store_true",
                    help="regenerate in memory; exit 1 and list differences if stale; no write")
    args = ap.parse_args(argv)
    outputs, counts = generate(REPO)
    if args.check:
        diffs = check(REPO, outputs)
        for line in diffs:
            print(line)
        print("code index is stale" if diffs else "code index is current")
        return 1 if diffs else 0
    write(REPO, outputs)
    print(f"wrote {len(outputs)} files to {OUT_DIR}/")
    for key, val in counts.items():
        print(f"  {key}: {val}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
