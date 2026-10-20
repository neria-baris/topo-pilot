#!/usr/bin/env bash
# Build "READ ME FIRST - Summary of the Research So Far" (Git Bash / POSIX).
#   bash docs/research_summary/build.sh            # from snapshots
#   bash docs/research_summary/build.sh --refresh  # re-read X6S1 gate statuses and ledgers first
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
BUILD="${BUILD_DIR:-/x/Downloads/topo-scratch/paper/build}"
OUT="$REPO/00_READ_ME_FIRST_Research_Summary_So_Far"
PY="$REPO/.venv/Scripts/python.exe"
[ -x "$PY" ] || PY="$REPO/.venv/bin/python"

"$PY" -s "$HERE/make_figures.py" "$@"
mkdir -p "$BUILD" "$OUT"
cd "$HERE"
TEX=(-interaction=nonstopmode -halt-on-error "-output-directory=$BUILD" research_summary.tex)
pdflatex "${TEX[@]}" >/dev/null
(cd "$BUILD" && BIBINPUTS="$HERE:" bibtex research_summary >/dev/null)
pdflatex "${TEX[@]}" >/dev/null
pdflatex "${TEX[@]}" >/dev/null
cp "$BUILD/research_summary.pdf" "$OUT/READ_ME_FIRST_Research_Summary_So_Far.pdf"
echo "wrote $OUT/READ_ME_FIRST_Research_Summary_So_Far.pdf"
