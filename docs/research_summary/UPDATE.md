# Updating "READ ME FIRST: Summary of the Research So Far"

The PDF at `00_READ_ME_FIRST_Research_Summary_So_Far/READ_ME_FIRST_Research_Summary_So_Far.pdf`
is built from this directory. It is a living document: rebuild it at each X6 stage-1 (X6S1)
milestone.

## Rebuild

From the repository root (Windows, MiKTeX `pdflatex`/`bibtex` on PATH, project venv present):

```powershell
powershell -ExecutionPolicy Bypass -File docs\research_summary\build.ps1 -Refresh
```

- `-Refresh` re-reads the X6S1 store and the per-study CPU ledgers into the two snapshots in
  `data/` before drawing the figures. Leave it out to rebuild from the committed snapshots.
- The script runs `make_figures.py`, then `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` in
  `X:\Downloads\topo-scratch\paper\build` (outside the repository; override with `-BuildDir`),
  and copies the PDF into `00_READ_ME_FIRST_Research_Summary_So_Far/`.
- `build.sh` does the same from Git Bash.
- The script writes only into `docs/research_summary/{figures,data}/`, the build directory and
  the output folder. It never writes into any `*-store` or into `topo-pilot-x6s1`.

## What `--refresh` may read (sealing rule, X6S1 protocol §12 item 11)

`make_figures.py --refresh` copies only:

- `x6-stage1-store/GATES.jsonl` and `superseded/*/GATES.jsonl`: the `gate`, `status` and `utc`
  fields. The `values` field is never read.
- `x6-stage1-store/STAGES.jsonl`: `stage`, `stop`, `utc`.
- `x6-stage1-store/cpu_ledger.json`: the accounting fields of each metered run.
- `x6-stage1-store/stages/E0/frozen_C*.json`: `bundle_id`, `steps`, `K`.
- `<store>/cpu_ledger.json` for the stores listed in `LEDGERS`: `cumulative_cpu_s`.

It never opens `sealed/`, any other `stages/*/` payload, pools, tables, cloud files, partners,
learning curves or validation/test statistics. Keep it that way until E3 has unsealed: no
model-performance number from X6S1 may enter the document before then.

## What to update as X6S1 stages complete

| Milestone | Refresh | Edit in `research_summary.tex` |
|---|---|---|
| E2 done (job 0094) | done in the 2026-10-20 build | (already reflected) |
| Each E3a/E3w wave (jobs 0095, 0096) | `-Refresh` | §10.2 "What has run"; compute numbers in §10.2 and §12 |
| E3z (decision, unsealing) | `-Refresh` | Replace the "What is sealed" paragraph with the licensed outcome sentence and qualifiers quoted verbatim from the E3 review (`agent-handoff/jobs/<job>/review.md`); update the abstract, Table 1, §1 summary item 4, §13, §15 and Table B. Only then may unsealed X6S1 numbers be added, each with its source path |
| Any non-PASS gate | `-Refresh` | Describe the gate, the stop rule applied and the correction ruling, as in §10.2 |
| A new study | none | Add a section, a Table 1 row, an `EVENTS` entry in `make_figures.py` (date, lane, label, outcome class, source) and a Table B row |

Also update the title-page date and the "to 20 October 2026, ~13:35Z" marker in §10.2, and add
an `EVENTS` row in `make_figures.py` for each new X6S1 stage outcome.

## Provenance rule

Every plotted number must come from a file named in the figure caption and in a comment next
to the number in `make_figures.py`. Numbers transcribed from Markdown reports are typed in by
hand with their source path; numbers read at build time come from the snapshots in `data/`.
Never invent or estimate a value. Every `refs.bib` entry must be a verified real publication.

## After the X6S1 decision (2026-10-21)

- **New input:** E3z has unsealed, so `--refresh` now also copies selected fields of `x6-stage1-store/stages/E3z/report.json` into `data/x6s1_result.json`. Those fields are the outcome, rule, licence, qualifiers, the natural and designed statistics, and the flags.
- **Why this is allowed:** that file is the decision-stage report written by E3.9 after unsealing.
- **What feeds it:** Figure 14 (`fig14_x6s1_results`) and the section "Results (decision stage E3z)".
- **Still never read:** `sealed/` and the per-chunk payloads.
