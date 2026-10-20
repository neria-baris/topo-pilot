# `reports/he_summary/build.py`

- Source: [reports/he_summary/build.py](../../../../../reports/he_summary/build.py)
- Kind: python
- Lines: 109

## Module docstring

> Build the Hebrew research-summary PDF (LaTeX).

## Imports

### Internal (repo files)

- `import charts` -> [reports/he_summary/charts.py](charts.py.md) (line 21, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 11)
- `pathlib` (lines 19)
- `re` (lines 13)
- `shutil` (lines 14)
- `subprocess` (lines 15)
- `sys` (lines 16)
- `tempfile` (lines 17)
- `time` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `BROWSERS`
- `FIGS`
- `HERE`
- `OUT`

## Classes and functions

- **function `browser`** [L31-35]: `def browser() -> str`
- **function `print_pdf`** [L38-63]: `def print_pdf(html: str, out: Path, work: Path) -> None`
- **function `export_figures`** [L66-82]: `def export_figures() -> None` - One cropped PDF per SVG; the page size equals the SVG viewBox (1 user unit = 1 px).
- **function `typeset`** [L85-99]: `def typeset() -> None`
- **function `main`** [L102-105]: `def main() -> None`

