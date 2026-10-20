# `tools/d2a/d2a_targets.py`

- Source: [tools/d2a/d2a_targets.py](../../../../../tools/d2a/d2a_targets.py)
- Kind: python
- Lines: 392

## Module docstring

> D-2a oracle targets, window baselines, band-edge beta and stage 0 (D2A-FROZEN-v1 §3, §5, §6;
> tools/d2a/API.md §2.2). Existing kernels only: BayesFilter, FutureOperator, suffix_posterior.

## Imports

### Internal (repo files)

- `import d2a_world` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 14, via same directory)
- `from d2a_world import d1` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 15, via same directory)
- `from oracle_profile import suffix_posterior` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 16, via unique basename)
- `from topo_pilot.analysis import kl_rows` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 18, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 19, via package root)
- `from topo_pilot.oracle import BayesFilter, FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 20, via package root)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 8)
- `json` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(Path(__file__).resolve().parent)` -> `tools/d2a`

## Imported by

- [tests/d2a/test_a_targets.py](../../tests/d2a/test_a_targets.py.md) (line 29, import)
- [tests/d2a/test_a_templates.py](../../tests/d2a/test_a_templates.py.md) (line 26, import)
- [tests/d2a/test_b_targets.py](../../tests/d2a/test_b_targets.py.md) (line 27, import)
- [tools/d2a/d2a_decide.py](d2a_decide.py.md) (line 172, import)
- [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 21, import)

## Top-level constants

- `Q1_DEC`
- `_K`

## Classes and functions

- **function `kernels`** [L27-38]: `def kernels(proc: str) -> dict` - Cached filters, future operators and 3-step observability blocks for a process.
- **function `window_prior`** [L41-43]: `def window_prior(t: int, m: int, proc: str = 'CM') -> np.ndarray`
- **function `window_posterior`** [L46-49]: `def window_posterior(tokens, t: int, m: int, proc: str = 'CM') -> np.ndarray`
- **function `_filtered`** [L52-56]: `def _filtered(tok: np.ndarray, proc: str) -> dict`
- **function `_quantities`** [L59-82]: `def _quantities(F: dict, loc: np.ndarray, ts: np.ndarray, tok: np.ndarray, proc: str) -> dict`
- **function `oracle_rows`** [L85-98]: `def oracle_rows(tokens, positions, proc: str = 'CM') -> tuple[np.ndarray, dict]` - Oracle quantities at one position per row (``positions [R]``, 0 = no row), in row order.
- **function `oracle_at`** [L101-103]: `def oracle_at(tokens, t: int, proc: str = 'CM') -> dict`
- **function `beta`** [L106-112]: `def beta(r, d) -> tuple[float | None, str]`
- **function `_ab`** [L115-116]: `def _ab(x) -> np.ndarray`
- **function `band_edge_table`** [L119-136]: `def band_edge_table(tokens, q_model=None) -> dict` - All (row, p), p = 1..32 with w_p in {σ0, σ2}: oracle d, window-8 r8 and model rm.
- **function `_gate`** [L139-141]: `def _gate(checks: dict, values: dict) -> dict`
- **function `_f`** [L144-145]: `def _f(x) -> np.ndarray`
- **function `_tv`** [L148-149]: `def _tv(p, q) -> float`
- **function `_q2d`** [L152-153]: `def _q2d(J2) -> np.ndarray`
- **function `g0_fix`** [L156-183]: `def g0_fix() -> dict` - D-2a float pipeline against d1_seam.exact_history at the named histories (§5.2).
- **function `_parity`** [L186-193]: `def _parity(tok: np.ndarray) -> tuple[np.ndarray, np.ndarray]` - Per-position seam parity and 'informed' flag (d1_seam.parity_profile, vectorised).
- **function `_delta`** [L196-197]: `def _delta(b12: np.ndarray) -> np.ndarray`
- **function `g0_num`** [L200-262]: `def g0_num(tok0, tok0N) -> dict` - Numerical identities on stage0 (decision and band-edge t <= 32) and stage0N (§5.2).
- **function `g0_tpl`** [L265-290]: `def g0_tpl() -> dict` - Exact (Fractions) checks of the canonical pair and every registered template (§5.2).
- **function `_split`** [L293-295]: `def _split(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]`
- **function `g0_pos`** [L298-308]: `def g0_pos(tok0) -> dict`
- **function `g0_feas`** [L311-330]: `def g0_feas(tok0) -> dict`
- **function `reported`** [L333-362]: `def reported(tok0, zN_rate: float) -> dict` - §5.2 'reported, not gated' quantities (descriptive).
- **function `stage0`** [L365-392]: `def stage0(store_root=W.STORE) -> str` - CLI ``stage0``: S0, pools, gates in §10.6 order, STAGE0.json; returns the outcome.

