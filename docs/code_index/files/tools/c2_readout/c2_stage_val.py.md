# `tools/c2_readout/c2_stage_val.py`

- Source: [tools/c2_readout/c2_stage_val.py](../../../../../tools/c2_readout/c2_stage_val.py)
- Kind: python
- Lines: 387

## Module docstring

> C2 stage body S4, VAL (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §5.7, §6.6, §6.7, §7 rows
> 17-20): PLAN["S4"] = X1, V3x, V3y, Y1, Y1*, Y2, P1. Also the helpers S5 reuses: the C2-M patch
> arms, the closed-form streams, the X1 arms and run, the bound wrapper. X1 is ephemeral; the VAL
> endpoint-bearing values are sealed at P1 (§5.7, C-22). The S5 descriptive compositions (the
> rotation arm, POST-DESC quantities, the C2-M intervals, the §2.12 descriptives, the opened VAL
> bundles) live here too (line budget, R-0104-1).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 10, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 13, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](c2_attrib.py.md) (line 14, via same directory)
- `import c2_code` -> [tools/c2_readout/c2_code.py](c2_code.py.md) (line 15, via same directory)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](c2_decide.py.md) (line 16, via same directory)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](c2_driver.py.md) (line 17, via same directory)
- `import c2_model` -> [tools/c2_readout/c2_model.py](c2_model.py.md) (line 18, via same directory)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 19, via same directory)
- `import c2_stage_base` -> [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 20, via same directory)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](c2_stats.py.md) (line 21, via same directory)
- `from c2_stage_base import C1, EXC, X3, alive, bundle, fitb, js, orc, prob, rec, table` -> [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 23, via same directory)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 23, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 26, import)

## Top-level constants

- `PLAN`
- `S4`

## Classes and functions

- **function `patched`** [L27-32]: `def patched(ctx, split, j, rep, kind, rows=None) -> np.ndarray`
- **function `cm_pair`** [L35-43]: `def cm_pair(ctx, split, j, kind) -> tuple` - C2-M x pair: F, S, C replacements of a2(H+-) in context H (§2.10); A_full.
- **function `placebo_m`** [L46-55]: `def placebo_m(ctx, split, j, kind) -> tuple` - Y2 arms on the Y_def rows only: a2(H^Y) (F) and its P2 part (S) patched in context H;
- **function `closed_streams`** [L59-78]: `def closed_streams(F, y, o, perm) -> dict` - The x/y pair quantities of every passing ln_final problem and the R and S* streams of one
- **function `lowid`** [L81-83]: `def lowid(E, seq, n) -> np.ndarray`
- **function `x1_arms`** [L86-110]: `def x1_arms(P, o, seq, w) -> dict` - X1 arms (§7 row 17): natural arms (H^Y on its Y_def rows); the R interchange arms on every
- **function `x1_run`** [L113-122]: `def x1_run(ctx, split, j) -> dict` - X1 (ephemeral, §5.7): identity diagnostics only; the natural logits are cleared after.
- **function `bounds`** [L125-127]: `def bounds(arrays, guards, seed, alpha=cc.VAL_ALPHA, draws=cc.VAL_DRAWS) -> dict`
- **function `sg`** [L130-131]: `def sg(b, side) -> int`
- **function `_E`** [L135-136]: `def _E(ctx, p, split='test') -> np.ndarray`
- **function `rotation`** [L139-159]: `def rotation(ctx, js_) -> dict` - Report only: A_rot, G_rot on every TEST E_x row, theta_rot with its 95 % interval (seed
- **function `cm_intervals`** [L162-179]: `def cm_intervals(ctx) -> dict` - C2-M descriptive intervals after the M outcome (seed 620518; 24 arrays; NEW-5).
- **function `describe`** [L182-197]: `def describe(ctx, fam, j, q) -> dict` - The §2.12 descriptives of one admitted model (TEST; descriptive only).
- **function `unsealed`** [L200-219]: `def unsealed(name, a, E) -> dict` - Point values of one opened VAL bundle (secondary; API.md §15.2 val_unsealed).
- **function `x1`** [L223-225]: `def x1(ctx) -> dict`
- **function `v3`** [L228-237]: `def v3(ctx, pair, seed, fail) -> dict`
- **function `v3x`** [L240-241]: `def v3x(ctx) -> dict`
- **function `v3y`** [L244-245]: `def v3y(ctx) -> dict`
- **function `y_on`** [L248-249]: `def y_on(ctx, j) -> bool`
- **function `yplac`** [L252-266]: `def yplac(ctx, fam, seed) -> dict` - Y1 (R) / Y1* (S*): U(A^Y_S - 0.10 A^Y_full) < -g on VAL E_y rows, if active.
- **function `y1`** [L269-270]: `def y1(ctx) -> dict`
- **function `y1s`** [L273-274]: `def y1s(ctx) -> dict`
- **function `y2`** [L277-294]: `def y2(ctx) -> dict` - Y2 (M): activity L(A^Y_M,F - 0.10 A^Y_full) > g, then U(A^Y_M,S - 0.10 A^Y_M,F) < -g.
- **function `m_extras`** [L298-315]: `def m_extras(ctx, j) -> dict` - VAL report-only C2-M (§2.10): 8 Sigma_e2-whitened Haar frames in place of P2 on the 1,024
- **function `rot_val`** [L318-329]: `def rot_val(ctx, j) -> dict` - The VAL rotation arm (report only; sealed until the fresh outcome, §5.7).
- **function `p1`** [L332-382]: `def p1(ctx) -> dict` - §6.7 per family; the VAL endpoint bundle is sealed here (§5.7, C-22); P1.json.

