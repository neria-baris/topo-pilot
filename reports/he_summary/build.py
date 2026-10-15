"""Build the Hebrew research-summary PDF (LaTeX).

    python build.py            # figures + two LuaLaTeX passes -> topo_pilot_research_summary_he.pdf
    python build.py --figs     # figures only

Figures are drawn as SVG by charts.py and exported one by one to cropped vector PDFs in
figs/ with headless Chrome (or Edge). main.tex is typeset with LuaLaTeX (babel hebrew,
bidi=basic, fontspec David Libre from fonts/). Requires Chrome or Edge, numpy and a TeX
distribution with lualatex (MiKTeX or TeX Live). data/*.json come from extract_data.py.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import charts

HERE = Path(__file__).resolve().parent
FIGS = HERE / "figs"
OUT = HERE / "topo_pilot_research_summary_he.pdf"
BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "google-chrome", "chromium", "msedge"]


def browser() -> str:
    for b in BROWSERS:
        if Path(b).is_file() or shutil.which(b):
            return b
    raise SystemExit("Chrome/Edge not found")


def print_pdf(html: str, out: Path, work: Path) -> None:
    src = work / f"{out.stem}.html"
    src.write_text(html, encoding="utf-8")
    out.unlink(missing_ok=True)
    proc = subprocess.Popen([browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                             f"--user-data-dir={work / 'chrome_profile'}", "--no-first-run",
                             f"--print-to-pdf={out}", src.as_uri()], stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Under some parent processes Chrome writes the PDF but never exits: wait for a stable
    # file, then end the process ourselves.
    last, stable = -1, 0
    for _ in range(240):
        if proc.poll() is not None and out.is_file():
            break
        size = out.stat().st_size if out.is_file() else -1
        stable = stable + 1 if size > 0 and size == last else 0
        last = size
        if stable >= 4:
            break
        time.sleep(0.5)
    else:
        raise SystemExit(f"Chrome did not produce {out.name}")
    if proc.poll() is None:
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"] if sys.platform == "win32"
                       else ["kill", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def export_figures() -> None:
    """One cropped PDF per SVG; the page size equals the SVG viewBox (1 user unit = 1 px)."""
    FIGS.mkdir(exist_ok=True)
    fonts = (HERE / "fonts").as_uri()
    work = Path(tempfile.mkdtemp(prefix="he_figs_"))
    for name, svg in charts.render_all().items():
        w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
        svg = svg.replace('width="100%"', f'width="{w}px" height="{h}px"', 1)
        html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
                f"@font-face {{ font-family: 'David Libre'; font-weight: 400; src: url('{fonts}/DavidLibre-Regular.ttf'); }}"
                f"@font-face {{ font-family: 'David Libre'; font-weight: 700; src: url('{fonts}/DavidLibre-Bold.ttf'); }}"
                f"@page {{ size: {w}px {h}px; margin: 0; }} html, body {{ margin: 0; padding: 0; }}"
                "svg { display: block; }</style></head>"
                f"<body>{svg}</body></html>")
        print_pdf(html, FIGS / f"{name}.pdf", work)
    shutil.rmtree(work, ignore_errors=True)
    print(f"exported {len(charts.ALL)} figures to {FIGS}")


def typeset() -> None:
    for i in (1, 2):  # second pass resolves the table of contents and references
        r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                           cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        if not (HERE / "main.pdf").is_file() or r.returncode not in (0, 1):
            tail = "\n".join(r.stdout.splitlines()[-30:])
            raise SystemExit(f"lualatex failed on pass {i}:\n{tail}")
        errors = [ln for ln in r.stdout.splitlines() if ln.startswith("!")]
        if errors:
            raise SystemExit("lualatex errors:\n" + "\n".join(errors))
    shutil.move(HERE / "main.pdf", OUT)
    for ext in (".aux", ".log", ".out", ".toc"):
        (HERE / f"main{ext}").unlink(missing_ok=True)
    print(f"wrote {OUT}")


def main() -> None:
    export_figures()
    if "--figs" not in sys.argv:
        typeset()


if __name__ == "__main__":
    main()
