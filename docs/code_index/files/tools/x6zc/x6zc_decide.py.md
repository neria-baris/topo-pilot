# `tools/x6zc/x6zc_decide.py`

- Source: [tools/x6zc/x6zc_decide.py](../../../../../tools/x6zc/x6zc_decide.py)
- Kind: python
- Lines: 191

## Module docstring

> X6ZC decision: the paired cluster bootstrap, ratio intervals, B9 sizing, the §9 decision,
> licences, qualifiers and the reuse verdict (X6ZC-DESIGN-v1 §5, §7-§9; API.md §8-§9, §20 C-52).
> Re-exported by x6zc_core. No I/O.

## Imports

### Internal (repo files)

- `from x6zc_const import CONTRACT, KC, NA_DIR, VARIANT_ORDER, CELLS, CELL_ORDER, T, N_FLOOR, N_D, N_LADDER, _fl` -> [tools/x6zc/x6zc_const.py](x6zc_const.py.md) (line 12, via same directory)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../x6_stage1/x6s1_stats.py.md) (line 18, via unique basename)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 9)
- `math` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 32, import)

## Top-level constants

- none

## Classes and functions

- **function `cluster_sums`** [L22-26]: `def cluster_sums(values, cluster, P) -> np.ndarray`
- **function `paired_cluster_boot`** [L27-36]: `def paired_cluster_boot(num, den, B, gen) -> dict`
- **function `interval`** [L37-41]: `def interval(draws, q) -> tuple`
- **function `ratio_interval`** [L42-48]: `def ratio_interval(draws_v, draws_pp, sign, q) -> dict`
- **function `_ratio`** [L49-49]: `def _ratio(a, b)`
- **function `cell_statistics`** [L50-70]: `def cell_statistics(point, draws, cell) -> dict`
- **function `halfwidth`** [L71-73]: `def halfwidth(n, se_d, beta_d, z) -> float`
- **function `choose_n`** [L74-88]: `def choose_n(n_avail, se) -> dict`
- **function `_ascii`** [L91-91]: `def _ascii(rule) -> str`
- **function `_lt`** [L92-92]: `def _lt(x, bar) -> bool`
- **function `_gt`** [L93-93]: `def _gt(x, bar) -> bool`
- **function `_unstable`** [L94-97]: `def _unstable(s) -> bool`
- **function `_cell_rule`** [L98-116]: `def _cell_rule(ev, c) -> tuple`
- **function `decide_x6zc`** [L117-143]: `def decide_x6zc(ev) -> dict`
- **function `_lkey`** [L144-147]: `def _lkey(outcome, table, case=None) -> str`
- **function `licence`** [L148-154]: `def licence(outcome, values, case=None) -> str`
- **function `not_licensed`** [L155-156]: `def not_licensed(outcome, case=None) -> str`
- **function `qualifiers`** [L157-174]: `def qualifiers(ev, decision, census) -> dict`
- **function `reuse_verdict`** [L175-191]: `def reuse_verdict(ev, decision) -> dict`

