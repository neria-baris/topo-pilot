# `reports/he_summary/charts.py`

- Source: [reports/he_summary/charts.py](../../../../../reports/he_summary/charts.py)
- Kind: python
- Lines: 712

## Module docstring

> SVG charts and diagrams for the Hebrew research summary (print, light mode).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 6)
- `json` (lines 8)
- `math` (lines 9)
- `pathlib` (lines 11)
- `re` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [reports/he_summary/build.py](build.py.md) (line 21, import)

## Top-level constants

- `ALL`
- `DATA`
- `FONT`
- `HEB`
- `HERE`

## Classes and functions

- **function `esc`** [L28-29]: `def esc(s: str) -> str`
- **function `T`** [L32-48]: `def T(x, y, s, anchor='middle', size=13, weight=400, fill=INK, italic=False, extra='')` - Text with a *visual* anchor: 'left' = text starts at x and runs right,
- **function `ML`** [L51-54]: `def ML(x, y, lines, size=13, lh=None, **kw)`
- **function `svg`** [L57-62]: `def svg(w, h, body, label='')`
- **function `box`** [L65-73]: `def box(x, y, w, h, lines, fill=NEU_T, stroke=MUTED, size=13, weight=400, r=8, sw=1.2, dash=None, color=INK)`
- **function `arrow`** [L76-79]: `def arrow(x1, y1, x2, y2, color=INK2, sw=1.4, dash=None)`
- **function `path_arrow`** [L82-85]: `def path_arrow(dpath, color=INK2, sw=1.4, dash=None)`
- **function `chip`** [L88-94]: `def chip(x, y, text, kind)`
- **class `Axis`** [L98-107]
- **method `Axis.__init__`** [L99-100]: `def __init__(self, d0, d1, r0, r1, log=False)`
- **method `Axis.__call__`** [L102-107]: `def __call__(self, v)`
- **function `ygrid`** [L110-117]: `def ygrid(ax, ticks, x0, x1, fmt='{:.2f}', size=11)`
- **function `legend`** [L120-134]: `def legend(x, y, items, size=12, gap=22)` - items: [(label, color, kind)] laid out right-to-left starting at x (right edge).
- **function `fig_pipeline`** [L140-186]: `def fig_pipeline()` - Overall research flow: generator -> two branches (model / oracle) -> analysis -> verdicts.
- **function `fig_stages`** [L189-232]: `def fig_stages()` - Stages S0..S8, gates, owner checkpoints and exit points (vertical timeline).
- **function `fig_decision`** [L235-267]: `def fig_decision()` - F1 decision rule as a flow chart.
- **function `fig_followups`** [L270-297]: `def fig_followups()`
- **function `fig_world`** [L300-337]: `def fig_world()` - Square vs cylinder lattice with emission centres.
- **function `emission_grid`** [L340-357]: `def emission_grid(perm=False, a=0, bsym=2, sigma=1.25)`
- **function `fig_emission`** [L360-385]: `def fig_emission()`
- **function `fig_ph`** [L388-423]: `def fig_ph()` - Schematic: ring point cloud -> barcode -> S.
- **function `fig_dcontrast`** [L426-442]: `def fig_dcontrast()`
- **function `chart_e0`** [L448-469]: `def chart_e0()` - reports/E0/summary.md
- **function `chart_e1`** [L472-497]: `def chart_e1()` - README.md, E1 table (replicate 1729, σ = 1.25, 8 panels).
- **function `chart_f1_panels`** [L500-531]: `def chart_f1_panels()` - data/d.json (per-panel D, read from the store) + u_r from reports/E2, E3.
- **function `chart_baselines`** [L534-554]: `def chart_baselines()` - reports/E2/summary.md, ratio of baseline median D to model median D.
- **function `chart_dynamics`** [L557-601]: `def chart_dynamics()` - data/dyn.json (S6 MetricRecords, panel 1, primary hook).
- **function `chart_layers`** [L604-630]: `def chart_layers()` - reports/E3/summary.md layer sweep: median D per replicate, per hook.
- **function `chart_probes`** [L633-655]: `def chart_probes()` - reports/E4/summary.md §4 (median test R² over 6 runs).
- **function `chart_circular`** [L658-677]: `def chart_circular()` - reports/E4/summary.md §5 (median agreement with the latent x angle).
- **function `chart_oracle`** [L680-699]: `def chart_oracle()` - README 'After E4', oracle profile job 0014 (calibration).
- **function `render_all`** [L711-712]: `def render_all() -> dict[str, str]`

