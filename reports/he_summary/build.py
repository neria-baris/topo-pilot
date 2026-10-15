"""Build the Hebrew research-summary PDF.

    python build.py [out.pdf]

content.html holds the Hebrew body with {{fig:name}} placeholders (charts.py) and
<h2 id=...>/<h3 id=...> headings. Pass 1 prints with invisible ASCII markers next to every
heading and reads their page numbers back (pypdf); pass 2 prints the final PDF with the
table of contents filled in. Intermediates go to a temp directory.

Requires Chrome or Edge, numpy and pypdf (pypdf is not in requirements.lock; install it
anywhere and point PYTHONPATH at it). data/*.json come from extract_data.py.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import charts

HERE = Path(__file__).resolve().parent
BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]

CSS = """
@font-face { font-family: 'David Libre'; font-weight: 400; src: url('{FONTS}/DavidLibre-Regular.ttf'); }
@font-face { font-family: 'David Libre'; font-weight: 500; src: url('{FONTS}/DavidLibre-Medium.ttf'); }
@font-face { font-family: 'David Libre'; font-weight: 700; src: url('{FONTS}/DavidLibre-Bold.ttf'); }
:root { --ink:#0b0b0b; --ink2:#52514e; --muted:#8a8984; --grid:#e4e3df; --accent:#2a78d6;
        --tint:#f1f0ec; --good:#1f7a3a; --bad:#b42318; --warn:#a15c00; }
@page { size: A4; margin: 22mm 20mm 20mm 20mm;
  @bottom-center { content: counter(page); font-family: 'David Libre'; font-size: 10pt; color: #52514e; }
  @top-right { content: "טופולוגיה של עולם סמוי בייצוגי Transformer"; font-family: 'David Libre';
               font-size: 9pt; color: #8a8984; }
}
@page :first { @bottom-center { content: none; } @top-right { content: none; } }
html { direction: rtl; }
body { font-family: 'David Libre', 'Times New Roman', serif; font-size: 12pt; line-height: 1.55; color: var(--ink);
       background: #fff; margin: 0; text-align: justify; text-justify: inter-word;
       hyphens: manual; font-variant-numeric: lining-nums; }
p, li { text-align: justify; }
p { margin: 0 0 0.7em; orphans: 3; widows: 3; }
h1, h2, h3, h4 { font-weight: 700; text-align: right; break-after: avoid; line-height: 1.25; }
h2 { font-size: 19pt; margin: 0 0 0.5em; padding-bottom: 4px; border-bottom: 2px solid var(--ink);
     break-before: page; }
h3 { font-size: 14.5pt; margin: 1.1em 0 0.4em; color: var(--ink); }
h4 { font-size: 12.5pt; margin: 0.9em 0 0.3em; color: var(--ink2); }
.ltr, code, .m { direction: ltr; unicode-bidi: isolate; }
code { font-family: Consolas, 'Courier New', monospace; font-size: 9.5pt; background: var(--tint);
       padding: 0 3px; border-radius: 3px; }
.m { font-style: italic; white-space: nowrap; }
.eq { direction: ltr; text-align: center; margin: 0.6em 0 0.8em; font-size: 12.5pt; font-style: italic; }
ul, ol { margin: 0.2em 0 0.8em; padding-right: 1.4em; padding-left: 0; }
li { margin-bottom: 0.25em; }
figure { margin: 0.8em 0 1.1em; break-inside: avoid; }
figure svg { display: block; }
figcaption { font-size: 10.5pt; color: var(--ink2); margin-top: 0.35em; text-align: justify; }
figcaption b { color: var(--ink); }
table { border-collapse: collapse; width: 100%; margin: 0.5em 0 1em; font-size: 10.5pt;
        break-inside: avoid; line-height: 1.35; }
th, td { border-bottom: 1px solid var(--grid); padding: 4px 6px; text-align: right; vertical-align: top; }
th { border-bottom: 1.5px solid var(--ink); font-weight: 700; background: #faf9f6; }
td.n, th.n { text-align: center; font-variant-numeric: tabular-nums; direction: ltr; }
caption { caption-side: bottom; font-size: 10pt; color: var(--ink2); text-align: justify; padding-top: 4px; }
.box { border-right: 4px solid var(--accent); background: #f4f8fd; padding: 8px 12px; margin: 0.8em 0 1em;
       break-inside: avoid; }
.box.meaning { border-color: #1baf7a; background: #f1faf6; }
.box.caveat { border-color: var(--warn); background: #fdf7ee; }
.box h4 { margin-top: 0; color: var(--ink); }
.box p:last-child, .box ul:last-child { margin-bottom: 0; }
.chip { display: inline-block; font-size: 9.5pt; font-weight: 700; padding: 0 7px; border-radius: 9px;
        border: 1px solid; line-height: 1.5; white-space: nowrap; }
.good { color: var(--good); background: #e7f4ea; border-color: var(--good); }
.bad { color: var(--bad); background: #fbeceb; border-color: var(--bad); }
.warn { color: var(--warn); background: #fdf1e0; border-color: var(--warn); }
.neu { color: var(--ink2); background: var(--tint); border-color: var(--muted); }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover .kicker { font-size: 13pt; color: var(--ink2); letter-spacing: 0.02em; }
.cover h1 { font-size: 32pt; margin: 0.25em 0 0.2em; border: 0; }
.cover .sub { font-size: 16pt; color: var(--ink2); margin-bottom: 1.6em; }
.cover .meta { font-size: 11.5pt; color: var(--ink2); border-top: 1px solid var(--grid); padding-top: 10px; }
.cover .status { margin-top: 1.4em; font-size: 12pt; }
.toc { list-style: none; padding: 0; margin: 0; }
.toc li { display: flex; align-items: baseline; margin: 0 0 0.3em; text-align: right; }
.toc li.l3 { padding-right: 1.6em; font-size: 11pt; color: var(--ink2); }
.toc a { color: inherit; text-decoration: none; }
.toc .dots { flex: 1; border-bottom: 1px dotted var(--muted); margin: 0 6px; transform: translateY(-4px); }
.toc .pg { font-variant-numeric: tabular-nums; min-width: 1.6em; text-align: left; }
.mk { position: absolute; font-size: 1px; color: #ffffff; }
.keep { break-inside: avoid; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
small { font-size: 10pt; color: var(--ink2); }
.nw { white-space: nowrap; }
ul.plain li { text-align: right; }
"""


def browser() -> str:
    for b in BROWSERS:
        if Path(b).is_file():
            return b
    raise SystemExit("Chrome/Edge not found")


def headings(body: str) -> list[tuple[str, str, str]]:
    return [(lvl, hid, re.sub(r"<[^>]+>", "", txt).strip())
            for lvl, hid, txt in re.findall(r'<h([23]) id="([^"]+)"[^>]*>(.*?)</h\1>', body, re.S)]


def toc_html(heads, pages) -> str:
    items = []
    for lvl, hid, txt in heads:
        pg = pages.get(hid, "00")
        items.append(f'<li class="l{lvl}"><a href="#{hid}">{txt}</a><span class="dots"></span>'
                     f'<span class="pg">{pg}</span></li>')
    return '<ol class="toc">' + "".join(items) + "</ol>"


def assemble(body: str, heads, pages, markers: bool) -> str:
    figs = charts.render_all()
    # keep numeric ranges (0.158–0.176, 13–16) on one line
    body = re.sub(r"(?<![\w.])(−?\d[\d.,]*–−?\d[\d.,]*)", lambda m: f'<span class="nw">{m.group(1)}</span>', body)
    body = re.sub(r"\{\{fig:(\w+)\}\}", lambda m: figs[m.group(1)], body)
    body = body.replace("{{toc}}", toc_html(heads, pages))
    if markers:
        body = re.sub(r'(<h[23] id="([^"]+)"[^>]*>)',
                      lambda m: f'{m.group(1)}<span class="mk">QQ{m.group(2)}QQ</span>', body)
    return ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
            '<title>טופולוגיה של עולם סמוי בייצוגי Transformer: סיכום מחקר</title>'
            f"<style>{CSS.replace('{FONTS}', (HERE / 'fonts').as_uri())}</style></head><body>{body}</body></html>")


def print_pdf(html: str, out: Path, work: Path) -> None:
    src = work / "render.html"
    src.write_text(html, encoding="utf-8")
    out.unlink(missing_ok=True)
    proc = subprocess.Popen([browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                             f"--user-data-dir={work / 'chrome_profile'}", "--no-first-run",
                             "--generate-pdf-document-outline", f"--print-to-pdf={out}",
                             src.as_uri()], stdin=subprocess.DEVNULL,
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
        raise SystemExit("Chrome did not produce the PDF")
    if proc.poll() is None:
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def marker_pages(pdf: Path) -> dict[str, int]:
    from pypdf import PdfReader
    pages = {}
    for i, page in enumerate(PdfReader(str(pdf)).pages, start=1):
        for hid in re.findall(r"QQ([\w-]+)QQ", page.extract_text() or ""):
            pages.setdefault(hid, i)
    return pages


def main() -> None:
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "topo_pilot_research_summary_he.pdf"
    body = (HERE / "content.html").read_text(encoding="utf-8")
    heads = headings(body)
    work = Path(tempfile.mkdtemp(prefix="he_summary_"))
    tmp = work / "pass1.pdf"
    print_pdf(assemble(body, heads, {}, markers=True), tmp, work)
    pages = marker_pages(tmp)
    missing = [h for _, h, _ in heads if h not in pages]
    if missing:
        print("warning: no page found for", missing)
    print_pdf(assemble(body, heads, pages, markers=False), out, work)
    print(f"wrote {out} ({len(pages)} headings paged)")


if __name__ == "__main__":
    main()
